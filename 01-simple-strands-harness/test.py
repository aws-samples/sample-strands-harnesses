"""Check the deployed runtime end to end, in one session.

    uv run test.py

The test sends two prompts, then reads the harness state and prints one status block. It
proves five claims: the runtime accepts a SigV4-signed call and streams the reply, the
agent loop calls a tool, the loop continues with the tool result, the tool writes to the
microVM disk of the session, and the runtime holds the structured history.
"""

import sys
import uuid

import boto3

from cli import get_state, print_history, runtime_arn, stream


STACK = "SimpleStrandsHarness"  # the stack that deploy.py creates


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


def log_group(session: boto3.Session, runtime_id: str) -> str:
    """Return the log group of the runtime, or say that it has none yet."""
    prefix = f"/aws/bedrock-agentcore/runtimes/{runtime_id}"
    found = session.client("logs").describe_log_groups(logGroupNamePrefix=prefix)
    groups = [g["logGroupName"] for g in found["logGroups"]]
    return groups[0] if groups else f"{prefix}* (none yet)"


def status(deployed: dict, rows: list, logs: str, state: dict, checks: dict,
           session_id: str) -> None:
    """Print one block: what is deployed, what it did, and what passed."""
    print("\nDeployed resources")
    print(f"  stack     {STACK} in {deployed['region']}")
    for kind, name, resource_status in rows:
        print(f"  {kind:<26} {name}  {resource_status}")
    print(f"  logs      {logs}")
    print(f"  arn       {deployed['arn']}")

    print("\nRuntime")
    print(f"  status    {deployed['status']}, version {deployed['version']}")
    print(f"  model     {state['model']}")
    print(f"  tools     {', '.join(state['tools'])}")

    print("\nSession")
    print(f"  id        {session_id}")
    print(f"  messages  {len(state['messages'])}   loop cycles {state['cycles']}")
    print(f"  tokens    {state['tokens']['totalTokens']} total"
          f" ({state['tokens']['inputTokens']} in, {state['tokens']['outputTokens']} out)")
    print(f"  notes     {' | '.join(state['notes'].splitlines())}")

    print("\nHistory held by the runtime")
    print_history(state["messages"])

    print("\nChecks")
    for claim, passed in checks.items():
        print(f"  {'pass' if passed else 'FAIL'}  {claim}")


def main() -> int:
    session = boto3.Session()
    client = session.client("bedrock-agentcore")
    arn = runtime_arn(session)
    session_id = str(uuid.uuid4())
    word = f"harness-{uuid.uuid4().hex[:8]}"

    turns = [
        (f"Remember this code word: {word}", word),
        ("What code word did I give you? Answer with the word only.", word),
    ]
    for prompt, expected in turns:
        print(f"> {prompt}")
        reply = "".join(stream(client, arn, session_id, prompt))
        print(reply.strip() or "(empty reply)")
        if expected not in reply:
            print(f"\nFAIL: {expected} is missing from the reply")
            return 1

    state = get_state(client, arn, session_id)
    seen = [name for m in state["messages"] for b in m["content"] for name in b]
    checks = {
        "the loop called a tool": "toolUse" in seen,
        "the loop used the tool result": "toolResult" in seen,
        "more loop cycles than turns": state["cycles"] > len(turns),
        "the tool wrote to the session disk": word in state["notes"],
        "the runtime holds the history": len(state["messages"]) > len(turns),
    }
    deployed = deployment(session, arn)
    status(
        deployed,
        resources(session),
        log_group(session, deployed["runtime"]),
        state,
        checks,
        session_id,
    )

    if not all(checks.values()):
        return 1
    print("\nPASS: the deployed harness runs the loop, the tools, and the history.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
