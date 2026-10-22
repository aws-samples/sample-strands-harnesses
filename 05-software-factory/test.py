"""Run one product idea through the whole factory and check what came out.

    uv run test.py                 # the built-in goal; you answer the questions and gates
    uv run test.py --yes           # take every default and approve every gate
    uv run test.py --goal "..."    # your own goal

The test runs the same cycle as cli.py: clarify, plan and the feature gate, build, test
and review until the reviewer approves, the download, the release gate, then release. It
fails unless each stage left the files it owns, the reviewer approved, the zip holds the
code, the release ran only after a yes, and the metrics reached CloudWatch.
"""

import argparse
import sys
import uuid
import zipfile
from pathlib import Path

import boto3

import telemetry
import ui
from cli import (
    ATTEMPTS,
    OUT,
    STACK,
    YES,
    approved,
    build_rounds,
    clarify,
    client,
    download,
    invoke,
    mcp_servers,
    plan,
    release_gate,
    runtime_arn,
    stage,
)

GOAL = """\
Build TaskFlow, the MVP of a small team task tracker, as a single Python file named
taskflow.py that uses only the Python standard library (http.server, json, sqlite3 or
in-memory storage). It serves a JSON HTTP API on port 8000 and has five features:

1. Projects: POST /projects {"name": "..."} creates a project; GET /projects lists them.
2. Tasks: POST /projects/<id>/tasks {"title": "...", "priority": "low|medium|high"}
   creates a task with status "todo"; GET /projects/<id>/tasks lists them, and accepts
   ?status= and ?priority= filters.
3. Workflow: PATCH /tasks/<id> {"status": "..."} moves a task along todo -> doing -> done
   only. Any other transition returns 409 with an error message.
4. Assignment: PATCH /tasks/<id> {"assignee": "..."} sets the owner; GET /users/<name>/tasks
   lists the open tasks of that person.
5. Summary: GET /projects/<id>/summary returns the task counts per status and the percent
   done.

Invalid JSON or a missing field returns 400, an unknown id returns 404, and an unsupported
method returns 405. Every response is JSON. Keep the program under 400 lines, and ship
pytest tests that start the server on a free port in the background and exercise every
feature."""


def resources(session: boto3.Session) -> None:
    """Print every resource in the stack, as CloudFormation reports it."""
    found = session.client("cloudformation").describe_stack_resources(StackName=STACK)
    ui.info(f"stack {STACK} in {session.region_name}")
    for r in found["StackResources"]:
        kind = r["ResourceType"].replace("AWS::", "")
        ui.info(f"  {kind:<26} {r['PhysicalResourceId'].split('/')[-1]}  {r['ResourceStatus']}")


def runtime_state(session: boto3.Session, arn: str) -> dict:
    control = session.client("bedrock-agentcore-control")
    got = control.get_agent_runtime(agentRuntimeId=arn.split("/")[-1])
    return {"status": got["status"], "version": got["agentRuntimeVersion"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the factory end to end.")
    parser.add_argument("--goal", default=GOAL)
    parser.add_argument("--mcp")
    parser.add_argument("--yes", action="store_true",
                        help="take every default and approve every gate")
    args = parser.parse_args()

    telemetry.start("test")
    session = boto3.Session()
    agentcore = client(session)
    arn = runtime_arn(session)
    servers = mcp_servers(args.mcp)
    work_item = f"sdlc-{uuid.uuid4()}"

    resources(session)
    deployed = runtime_state(session, arn)
    ui.info(f"runtime {deployed['status']}, version {deployed['version']}, "
            f"{len(servers)} MCP servers in the config")
    ui.banner(work_item, args.goal)

    verdict, rounds, answer, released, zip_path = {}, 0, "", {}, None
    with telemetry.span("test.run", work_item=work_item):
        goal = clarify(agentcore, arn, work_item, args.goal, servers, args.yes)
        planned = plan(agentcore, arn, work_item, goal, servers, args.yes)
        if planned:
            verdict, rounds = build_rounds(agentcore, arn, work_item, servers)
            zip_path = download(agentcore, arn, work_item)
            if zip_path:
                ui.code(OUT / work_item)
            if approved(verdict.get("text", "")):
                answer = release_gate(agentcore, arn, work_item, args.yes)
                if answer.strip(" .!").lower() in YES:
                    released = stage(agentcore, arn, work_item, "release",
                                     "A person approved this work item. Write release.md.",
                                     servers)
                    zip_path = download(agentcore, arn, work_item)

    state = invoke(agentcore, arn, work_item, {"command": "state", "work_item": work_item})
    files = {item["path"] for item in state.get("artifacts", [])}
    ui.artifacts(state.get("artifacts", []))
    zipped = set(zipfile.ZipFile(zip_path).namelist()) if zip_path else set()
    code_files = [f for f in files if f.endswith((".py", ".js", ".ts")) and "test" not in f]
    sent = telemetry.flush()
    checks = {
        "a person approved the feature list": planned,
        "the planner wrote the feature list": "features.md" in files,
        "the planner wrote the requirements": "requirements.md" in files,
        "the planner wrote the specification": "spec.md" in files,
        "the builder wrote code": bool(code_files),
        "the tester wrote a test report": "test-report.md" in files,
        "the reviewer wrote a review": "review.md" in files,
        "the reviewer approved": approved(verdict.get("text", "")),
        "the reviewer needed no more than the allowed rounds": 0 < rounds <= ATTEMPTS,
        "the zip holds the code": bool(code_files) and set(code_files) <= zipped,
        "the release ran only after a person said yes": bool(released) == (
            answer.strip(" .!").lower() in YES
        ),
        "the release notes exist when released": (not released) or "release.md" in zipped,
        "the metrics reached the CloudWatch endpoint": sent,
    }
    ui.checks(checks)
    if not all(checks.values()):
        ui.fail(f"the factory did not finish the cycle for {work_item}")
        return 1
    ui.ok(f"PASS: the factory ran the full cycle for {work_item}")
    ui.info(f"code: {Path(zip_path).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
