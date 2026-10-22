"""Drive the software factory from your terminal. One goal in, working code out.

    uv run cli.py "a task tracker MVP with projects, tasks and a summary"
    uv run cli.py --goal-file goal.md --yes         answer every question with its default
    uv run cli.py --app taskflow "a task tracker ..."   name the app, or be asked for a name
    uv run cli.py --download taskflow                  fetch the code, then serve the app on a
                                                       local URL that forwards through SigV4
    uv run cli.py --apps                               list the apps and their work items
    uv run cli.py --stage review --work-item sdlc-1a2b...   one stage on existing work

The cycle, and the three places where it stops for you:

    clarify    the factory asks up to five questions, each with a default   <- you answer
    plan       it writes features.md, requirements.md and spec.md
               it shows features.md and waits                              <- yes, no, or changes
    build, test, review, three rounds at most
               it downloads the code to out/<work item>.zip and shows it
               it shows review.md and waits                                <- release, yes or no
    release    it writes release.md, and the download is refreshed

The loop lives here, not in the runtime. A stage starts with one SigV4-signed call and this
file polls until it ends, because one AgentCore request must end inside 15 minutes and a
build stage often runs longer. Every call carries the same runtimeSessionId, so the stages
share one workspace in one microVM. The code stays there until the session ends, which is
why the download matters.

MCP servers come from --mcp, then ./mcp.json, then ~/.agents/mcp.json, then
~/.agents/agents.json. A server whose command is missing in the runtime is skipped.
"""

import argparse
import http.server
import io
import re
import base64
import json
import os
import sys
import time
import uuid
import zipfile
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

import telemetry
import ui

STACK = "SoftwareFactory"  # the stack that deploy.py creates
MCP_PLACES = ["mcp.json", "~/.agents/mcp.json", "~/.agents/agents.json"]
ATTEMPTS = 3  # how many build, test, review rounds before the factory gives up
PLAN_ROUNDS = 3  # how many times a person may send the feature list back
POLL_SECONDS = 5  # how often to ask the runtime what the running stage has said
STAGE_MINUTES = 90  # how long one stage may run before this side gives up on it
HEARTBEAT_SECONDS = 60  # how long a quiet stage may go before this side says it is alive
OUT = Path("out")  # where downloads go, one zip and one folder per work item
APPS_FILE = OUT / "apps.json"  # app name -> work item, written when a run starts
SERVE_PORT = 8765  # the local port of the SigV4 proxy that --download starts
# The answers a person types at a yes-or-no question. Anything else is asked again.
YES = ("y", "yes", "yea", "yeah", "yep", "yup", "ok", "okay", "sure", "approve", "approved")
NO = ("n", "no", "nope", "nah", "stop")

# One line per stage, printed when it starts, so a person watching knows what it is for.
STAGE_PURPOSE = {
    "clarify": "the clarifier lists what the goal leaves open",
    "plan": "the planner writes features.md, requirements.md and spec.md",
    "build": "the builder writes the code from the spec",
    "test": "the tester writes and runs the tests, then test-report.md",
    "review": "the reviewer grades the work and approves it or asks for changes",
    "release": "the release agent writes release.md after a person approves",
}


def elapsed(since: float) -> str:
    seconds = int(time.monotonic() - since)
    return f"{seconds // 60}m{seconds % 60:02d}s"


def mcp_servers(given: str | None) -> dict:
    """Return the mcpServers map from the named file, or from the first place found."""
    places = [given] if given else MCP_PLACES
    for place in places:
        path = Path(place).expanduser()
        if path.is_file():
            config = json.loads(path.read_text())
            servers = config.get("mcpServers", config)
            telemetry.log("mcp config", file=str(path), servers=len(servers))
            return servers
    telemetry.log("mcp config", file="none", servers=0)
    return {}


def runtime_arn(session: boto3.Session) -> str:
    if arn := os.environ.get("FACTORY_RUNTIME_ARN"):
        return arn
    stack = session.client("cloudformation").describe_stacks(StackName=STACK)
    outputs = stack["Stacks"][0]["Outputs"]
    return next(o["OutputValue"] for o in outputs if o["OutputKey"] == "RuntimeArn")


def client(session: boto3.Session):
    # Every call is short, because a stage runs in the background and this side polls.
    # The generous read timeout covers a poll that arrives while the runtime starts a stage.
    return session.client("bedrock-agentcore", config=Config(read_timeout=900))


def invoke(agentcore, arn: str, work_item: str, payload: dict, quiet: bool = True) -> dict:
    """Send one payload and return the final dict. Streamed text lands in result["text"]."""
    response = agentcore.invoke_agent_runtime(
        agentRuntimeArn=arn,
        runtimeSessionId=work_item,  # 33 characters or longer, shared by every stage
        payload=json.dumps(payload).encode(),
    )
    text, result = [], {}
    for line in response["response"].iter_lines():
        if not line.startswith(b"data: "):
            continue
        chunk = json.loads(line[6:])
        if isinstance(chunk, str):
            text.append(chunk)
            if not quiet:
                ui.console.print(chunk, end="")
        else:
            result = chunk
    result.setdefault("text", "".join(text))
    return result


class StageFailed(Exception):
    """A stage ended in an error. `transient` is true when trying again can succeed."""

    def __init__(self, message: str, transient: bool):
        super().__init__(message)
        self.transient = transient


# Errors that Bedrock returns for a passing fault on its side. The same stage started again
# usually runs to the end.
TRANSIENT = ("internalserverexception", "throttlingexception", "serviceunavailable",
             "modelstreamerrorexception", "try your request again", "too many requests")
STAGE_TRIES = 3  # how many times a stage starts before a transient error is final


def stage(agentcore, arn: str, work_item: str, name: str, task: str, servers: dict,
          show: bool = True) -> dict:
    """Run one stage to the end, starting it again after a transient Bedrock error.

    A new start keeps the workspace, because every file the stage wrote is still on the
    microVM disk, so the retried stage picks up the files and finishes the work.
    """
    for attempt in range(1, STAGE_TRIES + 1):
        try:
            return stage_once(agentcore, arn, work_item, name, task, servers, show)
        except StageFailed as failure:
            if not failure.transient or attempt == STAGE_TRIES:
                ui.fail(str(failure))
                sys.exit(1)
            ui.warn(f"{name} hit a temporary Bedrock error. Starting it again, try "
                    f"{attempt + 1} of {STAGE_TRIES}. ({str(failure)[:160]})")
            telemetry.log("stage retry", stage=name, attempt=attempt + 1, error=str(failure)[:200])
            time.sleep(15 * attempt)
    return {}


def stage_once(agentcore, arn: str, work_item: str, name: str, task: str, servers: dict,
               show: bool = True) -> dict:
    """Start one stage, follow it to the end, and report what it produced.

    show=False keeps the streamed text off the terminal, for a stage whose reply is data.
    """
    with telemetry.span(f"call.{name}", work_item=work_item):
        begun = time.monotonic()
        ui.stage_start(name, STAGE_PURPOSE.get(name, ""))
        started = invoke(agentcore, arn, work_item,
                         {"stage": name, "work_item": work_item, "task": task,
                          "mcp_servers": servers})
        if started.get("type") == "error":
            ui.fail(f"runtime rejected the call: {started['message']}")
            sys.exit(1)

        stream, result, offset = ui.Stream(), {}, 0
        deadline = time.monotonic() + STAGE_MINUTES * 60
        failures, last_output = 0, time.monotonic()
        while time.monotonic() < deadline:
            time.sleep(POLL_SECONDS)
            try:
                status = invoke(agentcore, arn, work_item,
                                {"command": "status", "work_item": work_item, "offset": offset})
            except (BotoCoreError, ClientError) as error:
                # One poll among hundreds can meet a throttle or a dropped connection. The
                # stage keeps running in the runtime, so ask again instead of giving up.
                failures += 1
                telemetry.log("status poll failed", stage=name, error=str(error)[:200])
                if failures >= 20:
                    ui.fail(f"the {name} stage could not be polled: {error}")
                    sys.exit(1)
                continue
            failures = 0
            if status.get("text"):
                if show:
                    stream.feed(status["text"])
                offset = status.get("offset", offset)
                last_output = time.monotonic()
            elif time.monotonic() - last_output >= HEARTBEAT_SECONDS:
                # The agent is inside one long step, such as a test run.
                ui.heartbeat(name, elapsed(begun), stream.last)
                last_output = time.monotonic()
            if status.get("status") == "error":
                stream.flush()
                error = str(status.get("error"))
                raise StageFailed(f"the {name} stage stopped after {elapsed(begun)}: {error}",
                                  transient=any(t in error.lower() for t in TRANSIENT))
            if status.get("status") == "done":
                stream.flush()
                result = status.get("result") or {}
                break
        else:
            ui.fail(f"the {name} stage ran longer than {STAGE_MINUTES} minutes")
            sys.exit(1)

        files = [item["path"] for item in result.get("artifacts", [])
                 if "__pycache__" not in item["path"]]
        ui.stage_done(name, elapsed(begun), result.get("cycles", 0),
                      result.get("tokens", {}).get("totalTokens", 0), files)
        telemetry.log("stage done", stage=name, cycles=result.get("cycles", 0),
                      tokens=result.get("tokens", {}).get("totalTokens", 0), files=len(files))
        return result


def read_artifact(agentcore, arn: str, work_item: str, name: str) -> str:
    got = invoke(agentcore, arn, work_item,
                 {"command": "read", "work_item": work_item, "path": name})
    return got.get("text", "")


def approved(text: str) -> bool:
    return "REVISION NEEDED" not in text.upper() and "APPROVED" in text.upper()


def parse_questions(text: str) -> list[dict]:
    """Return the clarifier's questions: the last JSON array of questions in its reply.

    The reply also holds tool-call lines such as `[read] {...}` and may wrap the array in a
    code fence, so try every `[` and keep the last one that decodes to a list of questions.
    """
    decoder, found = json.JSONDecoder(), []
    for start, char in enumerate(text):
        if char != "[":
            continue
        try:
            value, _ = decoder.raw_decode(text, start)
        except json.JSONDecodeError:
            continue
        if isinstance(value, list) and value and all(isinstance(q, dict) for q in value):
            questions = [q for q in value if q.get("question")]
            if questions:
                found = questions
    return found[:5]


def clarify(agentcore, arn, work_item: str, goal: str, servers: dict, auto_yes: bool) -> str:
    """Ask the clarifier's questions, and return the goal with the answers appended."""
    ui.info("Reading your goal to find what it leaves open. The questions follow in a moment.")
    result = stage(agentcore, arn, work_item, "clarify",
                   f"The product goal is below. List the questions to ask.\n\n{goal}", servers,
                   show=False)  # the reply is JSON; the questions are printed below
    questions = parse_questions(result.get("text", ""))
    if not questions:
        ui.ok("the goal is clear enough, no questions")
        return goal
    ui.info("Answer each question, or press Enter to keep the default in brackets.")
    answers = []
    for number, item in enumerate(questions, 1):
        question, default = f"{number}. {item['question']}", str(item.get("default", ""))
        if auto_yes:
            ui.auto(question, default)
            answer = default
        else:
            answer = ui.ask(question, default)
        answers.append(f"- {item['question']}\n  Answer: {answer}")
    telemetry.log("clarified", work_item=work_item, questions=len(questions))
    return f"{goal}\n\nAnswers to the clarifying questions:\n" + "\n".join(answers)


def plan(agentcore, arn, work_item: str, goal: str, servers: dict, auto_yes: bool) -> bool:
    """Plan, show features.md, and loop on the changes a person asks for. True means build."""
    task = f"The product goal is below. Write features.md, requirements.md and spec.md.\n\n{goal}"
    for _ in range(PLAN_ROUNDS):
        stage(agentcore, arn, work_item, "plan", task, servers)
        ui.markdown("features.md, for your approval",
                    read_artifact(agentcore, arn, work_item, "features.md"), "magenta")
        question = "Build these features? Type yes, no, or the changes you want"
        if auto_yes:
            ui.auto(question, "yes")
            answer = "yes"
        else:
            answer = ui.ask_text(question)
        telemetry.log("features decision", work_item=work_item,
                      answer=answer if answer.strip(" .!").lower() in YES + NO else "changes")
        if answer.strip(" .!").lower() in YES:
            return True
        if answer.strip(" .!").lower() in NO:
            return False
        task = (f"A person read features.md and asked for these changes:\n\n{answer}\n\n"
                f"Update features.md, requirements.md and spec.md to match. The goal:\n\n{goal}")
    ui.warn(f"the feature list was sent back {PLAN_ROUNDS} times, so the factory stops here")
    return False


def download(agentcore, arn: str, work_item: str, out: Path = OUT) -> Path | None:
    """Save the workspace as out/<work item>.zip, unzip it beside the zip, and return it.

    A session that AgentCore already ended comes back in a new microVM with an empty
    workspace. Then the earlier download is kept, never overwritten with an empty zip, and it
    is put back in the new workspace so the app can still be served.
    """
    got = invoke(agentcore, arn, work_item, {"command": "bundle", "work_item": work_item})
    if got.get("type") != "bundle":
        ui.fail(f"the download failed: {got.get('message', got.get('text', 'no reply'))}")
        return None
    data = base64.b64decode(got["zip_base64"])
    zip_path, folder = out / f"{work_item}.zip", out / work_item
    if not zipfile.ZipFile(io.BytesIO(data)).namelist():
        if not zip_path.exists():
            ui.fail("the session ended and its workspace is gone, and there is no earlier download")
            return None
        ui.warn("the session ended, so the code comes from your earlier download")
        restored = invoke(agentcore, arn, work_item, {
            "command": "restore", "work_item": work_item,
            "zip_base64": base64.b64encode(zip_path.read_bytes()).decode()})
        if restored.get("type") != "restored":
            ui.fail(f"could not put the code back: {restored.get('message', 'no reply')}")
        ui.download(zip_path.resolve(), folder.resolve(), zip_path.stat().st_size)
        return zip_path
    out.mkdir(parents=True, exist_ok=True)
    zip_path.write_bytes(data)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(folder)  # extractall drops absolute paths and ".." parts
    ui.download(zip_path.resolve(), folder.resolve(), got.get("bytes", 0))
    telemetry.log("downloaded", work_item=work_item, bytes=got.get("bytes", 0))
    return zip_path


def build_rounds(agentcore, arn, work_item: str, servers: dict) -> tuple[dict, int]:
    """Run build, test and review until the reviewer approves. Return the verdict, rounds."""
    verdict = {}
    for attempt in range(1, ATTEMPTS + 1):
        ui.round_start(attempt, ATTEMPTS)
        stage(agentcore, arn, work_item, "build",
              "Implement the specification, and address review.md if it exists.", servers)
        stage(agentcore, arn, work_item, "test",
              "Write the tests, run them, and write test-report.md.", servers)
        verdict = stage(agentcore, arn, work_item, "review",
                        "Grade the work and write review.md.", servers)
        if approved(verdict.get("text", "")):
            ui.ok(f"the reviewer approved in round {attempt}")
            telemetry.record_rounds(attempt, "approved")
            return verdict, attempt
        ui.warn(f"the reviewer asked for changes in round {attempt} of {ATTEMPTS}")
    telemetry.record_rounds(ATTEMPTS, "unapproved")
    return verdict, ATTEMPTS


def release_gate(agentcore, arn, work_item: str, auto_yes: bool) -> str:
    """Show review.md and ask whether to release. Return the answer."""
    ui.markdown("review.md", read_artifact(agentcore, arn, work_item, "review.md")[:4000],
                "green")
    question = "Release this work item? [yes/no]"
    if auto_yes:
        ui.auto(question, "yes")
        answer = "yes"
    else:
        answer = ui.ask_text(question).strip(" .!").lower()
        while answer not in YES + NO:  # ask again, rather than read a typo as a no
            answer = ui.ask_text("Please type yes or no").strip(" .!").lower()
    telemetry.log("human decision", work_item=work_item, answer=answer or "none")
    telemetry.record_decision(answer)
    return answer


def slug(text: str) -> str:
    """Return a short app name from free text, such as 'task-tracker-mvp'."""
    words = [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in ("a", "an", "the")]
    return "-".join(words[:3]) or "app"


def load_apps() -> dict:
    return json.loads(APPS_FILE.read_text()) if APPS_FILE.exists() else {}


def remember_app(name: str, work_item: str, goal: str) -> None:
    """Record that this app name belongs to this work item, so --download can find it."""
    apps = load_apps()
    apps[name] = {"work_item": work_item, "goal": goal[:200], "created": time.strftime("%Y-%m-%d %H:%M")}
    APPS_FILE.parent.mkdir(parents=True, exist_ok=True)
    APPS_FILE.write_text(json.dumps(apps, indent=2) + "\n")


def app_name(given: str | None, goal: str, auto_yes: bool) -> str:
    """Return the app name: --app, or the answer to a question with a default from the goal."""
    if given:
        return slug(given)
    default, taken = slug(goal), load_apps()
    for number in range(2, 100):
        if default not in taken:
            break
        default = f"{slug(goal)}-{number}"
    if auto_yes:
        ui.auto("App name", default)
        return default
    return slug(ui.ask("App name, for uv run cli.py --download <name> later", default))


def resolve_app(name: str) -> str:
    """Return the work item of an app name, or a work item id given as the name."""
    if name.startswith("sdlc-"):
        return name
    apps = load_apps()
    if name not in apps:
        known = ", ".join(sorted(apps)) or "none yet"
        raise SystemExit(f"no app named {name!r} in {APPS_FILE}. Known apps: {known}")
    return apps[name]["work_item"]


def serve(agentcore, arn: str, work_item: str, port: int) -> int:
    """Start the app in its microVM, then forward a local URL to it through SigV4 calls.

    The app listens on 127.0.0.1 inside the microVM, which nothing outside can reach. This
    local server takes each request from your browser, sends it as one signed
    invoke_agent_runtime call with the `proxy` command, and returns the app's answer. It binds
    127.0.0.1, so only this laptop can use the URL.
    """
    ui.info("Starting the app inside its AgentCore session. This installs its dependencies.")
    started = invoke(agentcore, arn, work_item, {"command": "app_start", "work_item": work_item})
    if started.get("type") != "app":
        ui.fail(started.get("message", "the app did not start"))
        if started.get("log"):
            ui.console.print(started["log"])
        return 1

    class Forward(http.server.BaseHTTPRequestHandler):
        def forward(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else b""
            try:
                got = invoke(agentcore, arn, work_item, {
                    "command": "proxy", "work_item": work_item, "method": self.command,
                    "path": self.path, "headers": dict(self.headers.items()),
                    "body_base64": base64.b64encode(body).decode()})
            except (BotoCoreError, ClientError) as error:
                got = {"type": "error", "message": str(error)}
            if got.get("type") != "response":
                data = str(got.get("message", "no answer")).encode()
                self.send_response(502)
                self.send_header("Content-Type", "text/plain")
            else:
                data = base64.b64decode(got["body_base64"])
                self.send_response(got["status"])
                for key, value in got.get("headers", {}).items():
                    self.send_header(key, value)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = do_OPTIONS = forward

        def log_message(self, format, *args):  # noqa: A002, one quiet line per request
            ui.console.print(f"  [muted]{self.command} {self.path} -> {args[1] if len(args) > 1 else ''}[/]")

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Forward)
    ui.serving(f"http://127.0.0.1:{port}/", started.get("start", ""))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        invoke(agentcore, arn, work_item, {"command": "app_stop", "work_item": work_item})
        ui.info("Stopped the app and the local URL.")
    return 0


def run(goal: str, servers: dict, work_item: str, auto_yes: bool, out: Path,
        name: str | None = None) -> int:
    """Run the whole cycle, with the three stops for a person."""
    session = boto3.Session()
    agentcore = client(session)
    arn = runtime_arn(session)
    ui.banner(work_item, goal)
    name = app_name(name, goal, auto_yes)
    remember_app(name, work_item, goal)
    ui.ok(f"app {name}: run  uv run cli.py --download {name}  later to get the code and a URL")

    with telemetry.span("factory.run", work_item=work_item):
        goal = clarify(agentcore, arn, work_item, goal, servers, auto_yes)
        if not plan(agentcore, arn, work_item, goal, servers, auto_yes):
            ui.info("Not built. The plan stays in the workspace for this work item.")
            telemetry.flush()
            return 2

        verdict, _ = build_rounds(agentcore, arn, work_item, servers)
        folder = download(agentcore, arn, work_item, out)
        if folder:
            ui.code(out / work_item)
        if not approved(verdict.get("text", "")):
            ui.fail("the reviewer never approved. Read review.md in the download.")
            telemetry.flush()
            return 1

        if release_gate(agentcore, arn, work_item, auto_yes).lower() not in YES:
            ui.info("Not released, so the release agent did not run.")
            ui.next_steps(out / work_item)
            telemetry.flush()
            return 2
        release = stage(agentcore, arn, work_item, "release",
                        "A person approved this work item. Write release.md.", servers)
        ui.artifacts(release.get("artifacts", []), "released files")
        download(agentcore, arn, work_item, out)  # again, so the zip holds release.md
        ui.ok(f"released {work_item}")
        ui.next_steps(out / work_item)
        telemetry.flush()
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the software factory.")
    parser.add_argument("goal", nargs="?", help="the product goal, in one sentence")
    parser.add_argument("--goal-file", help="a file holding a longer goal")
    parser.add_argument("--mcp", help="an mcpServers config file")
    parser.add_argument("--work-item", help="reuse an existing work item id")
    parser.add_argument("--stage", help="run only this stage on an existing work item")
    parser.add_argument("--app", help="the name of the app this run builds")
    parser.add_argument("--download", nargs="?", const=True, metavar="APP",
                        help="download the code of APP (or --work-item), then serve the app")
    parser.add_argument("--no-serve", action="store_true",
                        help="with --download, only download the code")
    parser.add_argument("--port", type=int, default=SERVE_PORT,
                        help=f"the local port for the app URL (default {SERVE_PORT})")
    parser.add_argument("--apps", action="store_true", help="list the apps and their work items")
    parser.add_argument("--out", default=str(OUT), help="the download folder (default: out)")
    parser.add_argument("--yes", action="store_true",
                        help="take every default and approve every gate")
    args = parser.parse_args()

    telemetry.start("cli")
    out = Path(args.out)
    servers = mcp_servers(args.mcp)
    work_item = args.work_item or f"sdlc-{uuid.uuid4()}"  # 33 characters or longer

    if args.apps:
        ui.apps(load_apps())
        return 0
    if isinstance(args.download, str):
        work_item = resolve_app(args.download)
    elif args.download and not args.work_item:
        parser.error("give --download an app name, or use --download with --work-item")

    if args.download or args.stage:
        if args.stage and not args.work_item:
            parser.error("--stage needs --work-item")
        session = boto3.Session()
        agentcore, arn = client(session), runtime_arn(session)
        if args.stage:
            stage(agentcore, arn, work_item, args.stage,
                  args.goal or "Continue this work item.", servers)
        code = 0
        if args.download:
            if not download(agentcore, arn, work_item, out):
                ui.info(f"If an earlier download exists, it is in {(out / work_item).resolve()}")
                telemetry.flush()
                return 1
            ui.next_steps(out / work_item)
            if not args.no_serve:
                code = serve(agentcore, arn, work_item, args.port)
        telemetry.flush()
        return code

    goal = Path(args.goal_file).read_text() if args.goal_file else args.goal
    if not goal:
        parser.error("give a goal, or a --goal-file, or --work-item with --stage or --download")
    return run(goal, servers, work_item, args.yes, out, args.app)


if __name__ == "__main__":
    sys.exit(main())
