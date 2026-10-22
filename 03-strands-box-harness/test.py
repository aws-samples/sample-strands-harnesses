"""Check the deployed runtime end to end: prove the value propagated.

    export AGENT_SECRET_VALUE=...    # the value stored in the agent/demo-secret secret
    uv run test.py

The test sends two checks in one session, then reads the harness state and prints one
status block. It proves four claims:
    the runtime accepts a SigV4-signed call and streams a verdict,
    the propagated env var is present inside the runtime,
    the matching value returns true (the client's value reached the agent intact),
    a wrong value returns false (the agent reads its own value, not the client's).

The true/false pair is the real test. A tool that always returned true would pass the first
check and fail the second, so both must hold.
"""

import json
import os
import sys
import uuid

import boto3

from cli import ask, get_state, invoke, print_state, runtime_arn

STACK = "StrandsBoxHarness"  # the stack that deploy.py creates
ENV_NAME = "AGENT_SECRET_VALUE"


def deployment(session: boto3.Session, arn: str) -> dict:
    """Return what AWS reports about the deployed runtime."""
    runtime_id = arn.split("/")[-1]
    got = session.client("bedrock-agentcore-control").get_agent_runtime(
        agentRuntimeId=runtime_id
    )
    return {
        "region": session.region_name,
        "runtime": runtime_id,
        "arn": arn,
        "status": got["status"],
        "version": got["agentRuntimeVersion"],
    }


def resources(session: boto3.Session) -> list[tuple[str, str, str]]:
    """Return every resource in the stack: type, name, and state, as AWS reports it."""
    found = session.client("cloudformation").describe_stack_resources(StackName=STACK)
    rows = []
    for r in found["StackResources"]:
        kind = r["ResourceType"].replace("AWS::", "")
        name = r["PhysicalResourceId"].split("/")[-1]
        rows.append((kind, name, r["ResourceStatus"]))
    return rows


def verdict(client, arn: str, session_id: str, expected: str) -> str:
    """Send one hello check and return the agent's one-word reply, lowercased."""
    reply = "".join(ask(client, arn, session_id, "hello", expected))
    return reply.strip().lower()


def status(deployed: dict, rows: list, state: dict, checks: dict,
           true_reply: str, false_reply: str) -> None:
    """Print one block: what is deployed, what it answered, and what passed."""
    print("\nDeployed resources")
    print(f"  stack     {STACK} in {deployed['region']}")
    for kind, name, resource_status in rows:
        print(f"  {kind:<26} {name}  {resource_status}")
    print(f"  arn       {deployed['arn']}")

    print("\nRuntime")
    print(f"  status    {deployed['status']}, version {deployed['version']}")
    print_state(state)

    print("\nPropagation check")
    print(f"  matching value   -> {true_reply!r}")
    print(f"  wrong value      -> {false_reply!r}")

    print("\nChecks")
    for claim, passed in checks.items():
        print(f"  {'pass' if passed else 'FAIL'}  {claim}")


def main() -> int:
    expected = os.environ.get(ENV_NAME, "")
    if not expected:
        print(f"FAIL: set {ENV_NAME} to the value stored in the agent/demo-secret secret, then run again.")
        return 1

    session = boto3.Session()
    client = session.client("bedrock-agentcore")
    arn = runtime_arn(session)

    # Two sessions: a true check and a false check. Separate ids keep the histories clean.
    true_reply = verdict(client, arn, str(uuid.uuid4()), expected)
    false_reply = verdict(client, arn, str(uuid.uuid4()), expected + "-wrong")

    # State from a third session, read after one check so the env snapshot is populated.
    state_session = str(uuid.uuid4())
    verdict(client, arn, state_session, expected)
    state = get_state(client, arn, state_session)

    # Guide Steps 8 and 9: Strands Box in the Runtime microVM, started with the fetched secret.
    probe = next(invoke(client, arn, str(uuid.uuid4()), {"command": "box_probe"}))

    checks = {
        "the runtime streamed a verdict": true_reply in ("true", "false"),
        f"{ENV_NAME} is present in the runtime": state["env"]["present"],
        "the matching value returns true": true_reply == "true",
        "a wrong value returns false": false_reply == "false",
        "Strands Box started in the Runtime microVM": probe.get("exit_code") == 0,
        "the agent inside Strands Box holds only a strands_box_ placeholder":
            probe.get("env_is_placeholder") is True,
        "the API got the real secret, redacted in the response": probe.get("api_saw") == "[REDACTED]",
    }
    deployed = deployment(session, arn)
    status(deployed, resources(session), state, checks, true_reply, false_reply)
    if not probe.get("ok"):
        print("\nStrands Box probe report:\n" + json.dumps(probe, indent=2))

    if not all(checks.values()):
        return 1
    print("\nPASS: the secret reached the Runtime through Secrets Manager, Strands Box gave the "
          "agent a placeholder, and the API received the real secret.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
