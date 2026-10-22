"""A software factory in one file: five Strands harness stages on AgentCore Runtime.

    uv run agent.py          serve /invocations and /ping on :8080

One runtime holds every stage. The caller names the stage in the payload, and every call
that shares a runtimeSessionId lands in the same microVM, so the stages share one
workspace on disk. That is what lets the planner write a specification the builder reads,
and the builder write code the reviewer grades.

    {"stage": "plan", "work_item": "...", "task": "...", "mcp_servers": {...}}
    {"command": "status", "work_item": "...", "offset": 0}   progress, then the result
    {"command": "state", "work_item": "..."}                 the workspace and the files
    {"command": "read", "work_item": "...", "path": "spec.md"}
    {"command": "bundle", "work_item": "..."}                the workspace as a base64 zip
    {"command": "app_start", "work_item": "..."}             start the built app in the microVM
    {"command": "proxy", "work_item": "...", "method": "GET", "path": "/", ...}
                                                             one HTTP request to that app
    {"command": "app_stop", "work_item": "..."}              stop it
    {"command": "restore", "work_item": "...", "zip_base64": "..."}  put a download back

A stage runs as a background task, and the call that starts it returns at once. One
`InvokeAgentRuntime` request must finish inside 15 minutes, and a build stage often needs
longer, so a stage that answered on the open request would be cut off in the middle of the
work ([quotas](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/bedrock-agentcore-limits.html)).
`add_async_task` tells the runtime that work is still in flight, which turns the health
check to HealthyBusy and keeps the microVM alive for up to the session timeout, eight hours
at most. The caller then polls `status`, which returns the text written since the offset it
passes, so the terminal still shows the stage as it works.

Each stage is one create_harness() call with a narrowed tool list. The harness brings the
loop, the shell, the file tools, page fetching, context management, and todo tracking. This
file adds the AWS tools from the Agent Toolkit for AWS and any MCP server the caller sends.
"""

import asyncio
import base64
import io
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import boto3
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from mcp_proxy_for_aws.client import aws_iam_streamablehttp_client
from mcp_proxy_for_aws.sigv4_helper import create_sigv4_client
from strands.tools.mcp import MCPClient
from strands_harness import create_harness

import telemetry

telemetry.start("runtime")

# Anthropic Claude Sonnet 5 through the us cross-Region inference profile. The execution
# role that deploy.py creates allows this one profile and nothing else.
MODEL_ID = "us.anthropic.claude-sonnet-5"

# The microVM disk of the session. Every stage of one work item reads and writes here.
WORKSPACE = Path(os.environ.get("FACTORY_WORKSPACE", "/tmp/factory"))  # nosec B108

# The AWS MCP Server from the Agent Toolkit for AWS: AWS API access, sandboxed scripts,
# live documentation search, and AWS skills through retrieve_skill. It is signed in this
# process with SigV4, so it needs no command line tool in the runtime.
AWS_MCP_ENDPOINT = "https://aws-mcp.us-east-1.api.aws/mcp"

# The planner needs facts from outside the workspace. It gets web_fetch, which reads a page
# it already has a link for, and the AWS documentation search that arrives with the AWS MCP
# tools below. It does not get the harness `web_search` tool: Bedrock Claude has no native
# search, so the harness would only serve that tool through Exa, a third party that receives
# every query. Pass builtin_tools={"web_search": "exa"} yourself if you accept that.
WEB = ["web_fetch"]
CONTRACT = """\
You are one stage of an automated software factory. Work only inside the current
directory, which is the shared workspace of this work item. Read the files that earlier
stages left before you start. Keep every artifact small enough for a person to read in
one sitting. Never ask the user a question, because no person is watching this call.

Never run a command that does not return on its own. A server or any long-lived process
blocks this stage forever, because nobody is here to stop it. To test a server, start it
in the background with its output sent to a file, wait a moment, send the requests with a
curl timeout, then kill it, all in one command. For example:

    python taskflow.py > server.log 2>&1 & SERVER=$!; sleep 2; curl -s -m 5 localhost:8000/projects; kill $SERVER

A background process that still holds this shell's output keeps the call open, so always
redirect it. Keep the shell `timeout` argument at 300 seconds or less. A test runner like
pytest returns on its own, so run it directly, with `timeout 300` in front of it."""

# Each stage: the instructions, the tools it may use, and whether it keeps a session.
STAGES = {
    "clarify": {
        # No tools: the goal is all it needs, and a tool list only slows the first reply.
        "tools": [],
        "extra_tools": False,  # no AWS MCP tools either
        "session": False,
        "instructions": """\
Read the product goal in the task. Before anyone plans or builds, list the questions whose
answers would change what gets built: who uses it, the must-have features, the data, the
interface, and hard constraints. Ask five questions at most, and skip any that the goal
already answers. Give each question a sensible default answer. Reply with only a JSON
array, for example [{"question": "Who uses it?", "default": "a team of five"}]. Reply
with [] when the goal leaves nothing important open. Write no files.""",
    },
    "plan": {
        "tools": ["read", "write"] + WEB,
        "session": False,
        "instructions": """\
Turn the product goal in the task into three files. Write features.md for the person who
approves the plan: a title, then seven features at most, one line each in plain words,
then one line that says what is out of scope. Write requirements.md with the user stories
and the acceptance criteria, one criterion per line, each one testable. Write spec.md with
the architecture, the file layout, the data model, and the open questions. If the task
lists changes that a person asked for, apply them to all three files. Read a page with
web_fetch, or search the AWS documentation with the AWS tools, when a choice needs a fact.
Write no code.""",
    },
    "build": {
        "tools": None,  # every built-in tool, including shell and edit
        "session": True,  # a second attempt remembers the first
        "instructions": """\
Implement spec.md in this directory. Read review.md first if it exists, and fix what it
asks for. Write runnable code with no placeholder bodies, and a README.md that says how
to run it. Keep the dependency list short. If the product is a server or a web app, also
write app.json in this directory: {"start": "<the command that starts it>", "cwd": "<the
folder to run it from, relative to here>", "port": <the port it listens on>}. The server
must read the port from the PORT environment variable and listen on 127.0.0.1. Stop when
the code matches the specification.""",
    },
    "test": {
        "tools": None,
        "session": False,
        "instructions": """\
Write the tests that requirements.md asks for, then run them. Use the language and the
test runner the code already uses. Write test-report.md with the command you ran, its
output, and one line per acceptance criterion saying pass or fail. Fix the tests if the
tests are wrong. Do not change the implementation to make a failing test pass.""",
    },
    "review": {
        "tools": ["read", "shell"],  # it grades the work, so it cannot edit it
        "session": False,
        "instructions": """\
Grade the code in this directory against requirements.md, spec.md, and test-report.md.
Check that the tests were really run, that each acceptance criterion is met, and that no
function is a stub. Write review.md with your reasons and a list of required changes.
End your reply with the single word APPROVED, or with the words REVISION NEEDED.""",
    },
    "release": {
        "tools": ["read", "write", "shell"],
        "session": False,
        "instructions": """\
A person approved this work item. Write release.md with the change summary, how to run
the result, the acceptance criteria and their evidence, and the risks that remain. Then
list every file you are handing over with its size. Change no code.""",
    },
}


def work_dir(work_item: str) -> Path:
    """Return the directory of one work item, and make it the current directory."""
    safe = "".join(c for c in work_item if c.isalnum() or c in "-_")[:64] or "work"
    path = WORKSPACE / safe
    path.mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    return path


def aws_tools() -> list:
    """Return the AWS MCP Server tools, or an empty list if the endpoint is unreachable.

    The client comes from create_sigv4_client, not from the metadata= argument of
    aws_iam_streamablehttp_client. In mcp-proxy-for-aws 1.7.0 that argument rewrites the
    JSON body after httpx has set Content-Length and signed it, so the handshake fails.
    """
    region = boto3.Session().region_name or "us-east-1"

    def http_client(headers=None, timeout=None, auth=None):
        return create_sigv4_client(
            service="aws-mcp",
            region="us-east-1",  # the endpoint lives there, so it is the signing Region
            headers=headers,
            timeout=timeout,
            metadata={"AWS_REGION": region},
        )

    client = MCPClient(
        lambda: aws_iam_streamablehttp_client(
            AWS_MCP_ENDPOINT,
            aws_service="aws-mcp",
            aws_region="us-east-1",
            httpx_client_factory=http_client,
        )
    )
    try:
        client.start()
        tools = client.list_tools_sync()
        telemetry.log("aws mcp connected", tools=len(tools))
        return tools
    except Exception as error:  # a factory without AWS tools is still a factory
        telemetry.log("aws mcp unavailable", error=str(error)[:200])
        return []


_AWS_TOOLS: list | None = None


def tools() -> list:
    """Return the AWS MCP Server tools, connecting on first use and keeping them after.

    Lazy on purpose: evals.py imports this module to build one stage agent locally, and it
    has no reason to open an MCP connection it will not use.
    """
    global _AWS_TOOLS
    if _AWS_TOOLS is None:
        _AWS_TOOLS = aws_tools()
    return _AWS_TOOLS


def runnable(mcp_servers: dict | None) -> dict:
    """Return only the stdio servers whose command exists in this runtime, plus URL servers.

    A config written for a laptop often names `npx` or `uvx`, which the microVM does not
    have. Starting such a server fails inside every stage and prints a traceback, so drop
    it here and name it in the log once.
    """
    kept = {}
    for name, server in (mcp_servers or {}).items():
        command = server.get("command")
        if command and shutil.which(command) is None:
            telemetry.log("mcp server skipped", server=name, missing=command)
            continue
        kept[name] = server
    return kept


def build_stage(stage: str, work_item: str, mcp_servers: dict | None):
    """Return the harness agent for one stage, narrowed to that stage's job."""
    spec = STAGES[stage]
    mcp_servers = runnable(mcp_servers)
    return create_harness(
        model=MODEL_ID,
        instructions=f"{CONTRACT}\n\n{spec['instructions']}",
        builtin_tools=spec["tools"],
        tools=tools() if spec.get("extra_tools", True) else [],  # the AWS MCP tools
        # The harness loads each server with continue_on_error, so a server that needs a
        # command the runtime does not have is skipped and named in the log.
        mcp_servers=mcp_servers or None,
        session=(
            {"id": work_item, "dir": str(WORKSPACE / ".sessions")}
            if spec["session"]
            else False
        ),
        memory=False,  # the workspace is the memory, and it is readable
        interventions=None,  # headless: an approval prompt here would never be answered
        callback_handler=None,
    )


def artifacts(path: Path) -> list[dict]:
    """Return every file of the work item, newest last, with its size in bytes."""
    files = [p for p in sorted(path.rglob("*")) if p.is_file() and not SKIP_PARTS & set(p.parts)]
    return [{"path": str(p.relative_to(path)), "bytes": p.stat().st_size} for p in files]


# Left out of the download: harness sessions, caches, and the logs of test servers.
SKIP_PARTS = {".sessions", ".deps", "__pycache__", ".pytest_cache", ".venv", "node_modules"}
BUNDLE_LIMIT = 50 * 1024 * 1024  # bytes of zip that one response may carry


def bundle(path: Path) -> bytes:
    """Return the files of one work item as a zip, without caches and server logs."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(path.rglob("*")):
            relative = file.relative_to(path)
            if not file.is_file() or SKIP_PARTS & set(relative.parts):
                continue
            if file.suffix in (".log", ".pyc"):
                continue
            archive.write(file, str(relative))
    return buffer.getvalue()


APP_PORT = 8765  # the port a built app listens on inside the microVM
APPS: dict[str, subprocess.Popen] = {}  # work item -> the running app process
# Headers that describe one hop of HTTP, so the proxy must not copy them.
HOP_HEADERS = {"connection", "keep-alive", "transfer-encoding", "content-length", "host",
               "upgrade", "proxy-connection", "te", "trailer"}


def app_plan(path: Path) -> dict:
    """Return how to start the built app: app.json when the builder wrote it, else a guess."""
    config = path / "app.json"
    if config.is_file():
        found = json.loads(config.read_text())
        return {"start": found["start"], "cwd": found.get("cwd", "."),
                "port": int(found.get("port", APP_PORT))}
    for folder in (".", "backend", "server", "app"):
        for name in ("server.py", "app.py", "main.py"):
            if (path / folder / name).is_file():
                return {"start": f"python {name}", "cwd": folder, "port": APP_PORT}
    raise FileNotFoundError("no app.json and no server.py, app.py or main.py to start")


def wait_for_port(port: int, seconds: float = 30) -> bool:
    """Return True once something answers HTTP on 127.0.0.1:port."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2)
            return True
        except urllib.error.HTTPError:
            return True  # an HTTP error still means the server answered
        except OSError:
            time.sleep(0.5)
    return False


def install_requirements(requirements: Path, deps: Path, log) -> bool:
    """Install a requirements file into deps with the first installer that works.

    The runtime image may lack pip, so try pip, then pip after ensurepip, then uv. Every
    attempt writes to app.log, so a failed install is readable in the error it causes.
    """
    target = ["install", "-q", "--target", str(deps), "-r", str(requirements)]
    attempts = [[sys.executable, "-m", "pip", *target],
                [sys.executable, "-m", "ensurepip", "--upgrade"],
                [sys.executable, "-m", "pip", *target]]
    if shutil.which("uv"):
        attempts.append(["uv", "pip", "install", "--python", sys.executable, "-q",
                         "--target", str(deps), "-r", str(requirements)])
    for command in attempts:
        done = subprocess.run(command, timeout=300, check=False, stdout=log,
                              stderr=subprocess.STDOUT)
        if done.returncode == 0 and "ensurepip" not in command:
            return True
    return False


def app_start(work_item: str, path: Path) -> dict:
    """Install the app's Python dependencies, start it, and wait until it answers."""
    running = APPS.get(work_item)
    if running and running.poll() is None:
        return {"type": "app", "status": "running", "port": running.args_port}
    plan = app_plan(path)
    cwd = (path / plan["cwd"]).resolve()
    if path.resolve() not in (cwd, *cwd.parents):
        raise ValueError("app.json names a folder outside the workspace")
    deps = path / ".deps"
    log = open(path / "app.log", "ab")  # noqa: SIM115, the app process keeps it open
    for requirements in (cwd / "requirements.txt", path / "requirements.txt"):
        if requirements.is_file():
            install_requirements(requirements, deps, log)
            break
    env = dict(os.environ, PORT=str(plan["port"]), HOST="127.0.0.1",
               PYTHONPATH=os.pathsep.join(filter(None, [str(deps), os.environ.get("PYTHONPATH")])))
    command = plan["start"].replace("python3 ", f"{sys.executable} ", 1)
    command = command.replace("python ", f"{sys.executable} ", 1)
    process = subprocess.Popen(command, shell=True, cwd=cwd, env=env,  # nosec B602
                               stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    process.args_port = plan["port"]  # type: ignore[attr-defined]
    APPS[work_item] = process
    if not wait_for_port(plan["port"]):
        tail = (path / "app.log").read_text(errors="replace")[-2000:]
        process.terminate()
        return {"type": "error", "message": f"the app did not answer on port {plan['port']}",
                "log": tail}
    telemetry.log("app started", work_item=work_item, command=plan["start"], port=plan["port"])
    return {"type": "app", "status": "running", "port": plan["port"], "start": plan["start"]}


def proxy(work_item: str, payload: dict) -> dict:
    """Send one HTTP request to the running app and return its response, body in base64."""
    process = APPS.get(work_item)
    if process is None or process.poll() is not None:
        return {"type": "error", "message": "the app is not running, send app_start first"}
    path = str(payload.get("path", "/"))
    if not path.startswith("/"):
        return {"type": "error", "message": "path must start with /"}
    body = base64.b64decode(payload.get("body_base64") or "")
    headers = {k: v for k, v in (payload.get("headers") or {}).items()
               if k.lower() not in HOP_HEADERS}
    request = urllib.request.Request(f"http://127.0.0.1:{process.args_port}{path}",
                                     data=body or None, headers=headers,
                                     method=str(payload.get("method", "GET")).upper())
    try:
        response = urllib.request.urlopen(request, timeout=60)  # nosec B310, loopback only
    except urllib.error.HTTPError as error:
        response = error  # a 404 or a 500 is still the app's answer
    data = response.read()
    return {"type": "response", "status": response.status,
            "headers": {k: v for k, v in response.headers.items() if k.lower() not in HOP_HEADERS},
            "body_base64": base64.b64encode(data).decode()}


app = BedrockAgentCoreApp()

# What each work item is doing, in this process. One session is one work item and one
# microVM, so this map holds one entry in practice. `text` is everything the stage has said
# so far, which `status` returns from the offset the caller asks for.
WORK: dict[str, dict] = {}


async def run_stage(stage: str, work_item: str, task: str, mcp_servers: dict | None) -> None:
    """Run one stage to the end as a background task, and keep its progress in WORK.

    add_async_task and complete_async_task bracket the work. Between them the runtime
    reports HealthyBusy on /ping, which is how it knows the session is still working after
    the starting request has already been answered.
    """
    state = WORK[work_item]
    task_id = app.add_async_task("stage", {"stage": stage, "work_item": work_item})
    path = work_dir(work_item)  # the task owns the working directory while it runs
    try:
        agent = build_stage(stage, work_item, mcp_servers)
        # timed_stage records the duration, the cycles, the tokens, and whether the stage
        # raised, so a stage that fails is still counted in CloudWatch.
        with telemetry.timed_stage(stage, work_item=work_item, tools=len(agent.tool_names)) as done:
            telemetry.log("stage started", stage=stage, work_item=work_item)

            async def drive() -> None:
                # Append the streamed text as it arrives, so `status` can return it, and
                # log each tool call, so CloudWatch shows what a quiet stage is doing.
                events = agent.stream_async(task).__aiter__()
                idle = float(os.environ.get("FACTORY_STAGE_IDLE_SECONDS", "600"))
                while True:
                    try:
                        # A stage that emits nothing for this long is stuck, most often in
                        # a command that never returns. Fail it now instead of at the end
                        # of the whole budget.
                        event = await asyncio.wait_for(events.__anext__(), timeout=idle)
                    except StopAsyncIteration:
                        return
                    if "data" in event:
                        state["text"].append(event["data"])
                    message = event.get("message") or {}
                    for block in message.get("content", []) if isinstance(message, dict) else []:
                        if "toolUse" in block:
                            use = block["toolUse"]
                            call = json.dumps(use.get("input", {}))[:300]
                            telemetry.log("tool call", stage=stage, tool=use.get("name"), input=call)
                            state["text"].append(f"\n[{use.get('name')}] {call[:160]}\n")
                        elif "toolResult" in block:
                            telemetry.log("tool result", stage=stage,
                                          status=block["toolResult"].get("status"))

            # A hard ceiling on one stage. A stage that runs a command which never returns
            # would otherwise block until the session times out, hours later, which is the
            # hang this guards against. The default sits under the caller's STAGE_MINUTES
            # poll deadline, so the runtime reports the timeout before the caller gives up.
            budget = float(os.environ.get("FACTORY_STAGE_TIMEOUT_SECONDS", "4800"))
            await asyncio.wait_for(drive(), timeout=budget)

            metrics = agent.event_loop_metrics
            done["cycles"] = metrics.cycle_count
            done["tokens"] = dict(metrics.accumulated_usage)
            telemetry.log(
                "stage finished",
                stage=stage,
                cycles=metrics.cycle_count,
                tokens=metrics.accumulated_usage["totalTokens"],
            )
        text = "".join(state["text"])
        if stage == "review":
            telemetry.record_verdict(
                "revision" if "REVISION NEEDED" in text.upper() else "approved"
            )
        state["result"] = {
            "type": "result",
            "stage": stage,
            "text": text,
            "tools": sorted(agent.tool_names),
            "cycles": agent.event_loop_metrics.cycle_count,
            "tokens": dict(agent.event_loop_metrics.accumulated_usage),
            "artifacts": artifacts(path),
        }
        state["status"] = "done"
    except asyncio.TimeoutError:
        state["status"] = "error"
        budget = os.environ.get("FACTORY_STAGE_TIMEOUT_SECONDS", "4800")
        state["error"] = (
            f"the {stage} stage was stopped: it went silent for longer than "
            f"FACTORY_STAGE_IDLE_SECONDS or ran past its {budget}s budget. A command that "
            f"does not return, such as a server started in the foreground, is the usual cause."
        )
        telemetry.log("stage timeout", stage=stage, work_item=work_item, budget=budget)
    except Exception as error:  # the caller is polling, so hand it the reason
        state["status"] = "error"
        state["error"] = str(error)[:2000]
        telemetry.log("stage failed", stage=stage, work_item=work_item, error=state["error"])
    finally:
        app.complete_async_task(task_id)
        telemetry.flush()  # the poller may collect the result and stop calling


@app.entrypoint
async def invoke(payload: dict):
    """Start a stage, or answer a command about a work item. Every call returns at once."""
    work_item = payload.get("work_item", "default")
    path = work_dir(work_item)
    command = payload.get("command")

    if command == "state":
        yield {
            "type": "state",
            "workspace": str(path),
            "stages": list(STAGES),
            "aws_tools": len(tools()),
            "artifacts": artifacts(path),
        }
        return
    if command == "read":
        target = path / str(payload.get("path", ""))
        text = target.read_text()[:100_000] if target.is_file() else ""
        yield {"type": "file", "path": str(payload.get("path")), "text": text}
        return
    if command == "bundle":
        data = bundle(path)
        if len(data) > BUNDLE_LIMIT:
            yield {"type": "error", "message": f"the zip is {len(data)} bytes, over the limit"}
            return
        yield {"type": "bundle", "bytes": len(data), "zip_base64": base64.b64encode(data).decode()}
        return
    if command == "restore":
        # Put a downloaded workspace back, for a session that AgentCore already ended.
        data = base64.b64decode(payload.get("zip_base64") or "")
        if len(data) > BUNDLE_LIMIT:
            yield {"type": "error", "message": "the zip is over the limit"}
            return
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            root = path.resolve()
            for member in archive.infolist():
                target = (path / member.filename).resolve()
                if root not in target.parents:
                    continue  # skip absolute paths and ".." parts
                archive.extract(member, path)
        yield {"type": "restored", "artifacts": artifacts(path)}
        return
    if command == "app_start":
        try:
            yield await asyncio.to_thread(app_start, work_item, path)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
            yield {"type": "error", "message": f"the app did not start: {error}"}
        return
    if command == "proxy":
        yield await asyncio.to_thread(proxy, work_item, payload)
        return
    if command == "app_stop":
        process = APPS.pop(work_item, None)
        if process and process.poll() is None:
            process.terminate()
        yield {"type": "app", "status": "stopped"}
        return
    if command == "status":
        state = WORK.get(work_item)
        if state is None:
            yield {"type": "status", "status": "none", "text": "", "offset": 0}
            return
        offset = int(payload.get("offset", 0))
        said = "".join(state["text"])
        yield {
            "type": "status",
            "stage": state["stage"],
            "status": state["status"],
            "text": said[offset:],
            "offset": len(said),
            "result": state["result"],
            "error": state["error"],
        }
        return

    stage = payload.get("stage")
    task = payload.get("task")
    if stage not in STAGES or not isinstance(task, str) or not task.strip():
        yield {"type": "error", "message": f"send a stage in {list(STAGES)} and a task"}
        return
    if (WORK.get(work_item) or {}).get("status") == "running":
        yield {"type": "error", "message": f"{work_item} is already running a stage"}
        return

    WORK[work_item] = {"stage": stage, "status": "running", "text": [], "result": {}, "error": ""}
    asyncio.create_task(run_stage(stage, work_item, task, payload.get("mcp_servers")))
    yield {"type": "started", "stage": stage, "work_item": work_item}


if __name__ == "__main__":
    print(f"workspace {WORKSPACE}, stages {list(STAGES)}", flush=True)
    print(f"aws mcp tools loaded: {len(tools())}", flush=True)
    if os.environ.get("FACTORY_MCP_CONFIG"):  # a local run can name a config file
        print(f"mcp config {os.environ['FACTORY_MCP_CONFIG']}", flush=True)
        json.loads(Path(os.environ["FACTORY_MCP_CONFIG"]).read_text())
    # Explicit, because the SDK binds 0.0.0.0 only when it detects Docker and otherwise
    # falls back to 127.0.0.1, which the runtime cannot reach.
    app.run(host="0.0.0.0")  # nosec B104
