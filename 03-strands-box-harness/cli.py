"""Ask the deployed agent whether a value propagated. Calls are SigV4-signed.

    export AGENT_SECRET_VALUE=...    # the value stored in the agent/demo-secret secret
    uv run cli.py                    # then type: hello

Needs the StrandsBoxHarness stack. It does not talk to a local agent.py. One run is one
runtime session.

At the prompt:
    hello       check the propagated value against AGENT_SECRET_VALUE in this shell
    <anything>  same check, any prompt text works; the value is what matters
    /state      model, tools, env presence and length, loop cycles, tokens
    exit        quit

The client sends the value from this shell's AGENT_SECRET_VALUE as `expected`. A true means
the agent in the Runtime holds the same value. Change this shell's value and send again to
see a false, which proves the agent reads its own propagated value and not the client's.
"""

import json
import os
import uuid

import boto3
from botocore.config import Config

STACK_NAME = "StrandsBoxHarness"  # the stack that deploy.py creates
ENV_NAME = "AGENT_SECRET_VALUE"


def runtime_arn(session: boto3.Session) -> str:
    stack = session.client("cloudformation").describe_stacks(StackName=STACK_NAME)
    outputs = stack["Stacks"][0]["Outputs"]
    return next(o["OutputValue"] for o in outputs if o["OutputKey"] == "RuntimeArn")


def invoke(client, arn: str, session_id: str, payload: dict):
    """Send one payload and yield each streamed chunk, text or state."""
    response = client.invoke_agent_runtime(
        agentRuntimeArn=arn,
        runtimeSessionId=session_id,  # AgentCore requires at least 33 characters
        payload=json.dumps(payload).encode(),
    )
    for line in response["response"].iter_lines(chunk_size=1):
        if line.startswith(b"data: "):
            yield json.loads(line[6:])


def ask(client, arn: str, session_id: str, prompt: str, expected: str):
    """Yield the verdict to one prompt, with the expected value attached."""
    return invoke(client, arn, session_id, {"prompt": prompt, "expected": expected})


def get_state(client, arn: str, session_id: str) -> dict:
    """Ask the runtime for the harness state of this session."""
    return next(chunk for chunk in invoke(client, arn, session_id, {"command": "state"}))


def print_state(state: dict) -> None:
    env = state["env"]
    print(f"  model    {state['model']}")
    print(f"  tools    {', '.join(state['tools'])}")
    print(f"  env      {env['name']} present={env['present']} length={env['length']}")
    print(f"  messages {len(state['messages'])}   loop cycles {state['cycles']}")
    print(f"  tokens   {state['tokens']['totalTokens']} total"
          f" ({state['tokens']['inputTokens']} in, {state['tokens']['outputTokens']} out)")


def main() -> None:
    expected = os.environ.get(ENV_NAME, "")
    if not expected:
        print(f"warning: {ENV_NAME} is empty in this shell, so every check will be false.")

    session = boto3.Session()
    client = session.client("bedrock-agentcore", config=Config(read_timeout=900))
    arn = runtime_arn(session)
    session_id = str(uuid.uuid4())
    print(f"session {session_id}. Type hello to check, /state, or exit.")
    print(f"sending expected={expected!r} from this shell's {ENV_NAME}.")

    while True:
        try:
            prompt = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt in ("exit", "quit"):
            break
        if prompt == "/state":
            print_state(get_state(client, arn, session_id))
        elif prompt:
            for chunk in ask(client, arn, session_id, prompt, expected):
                print(chunk, end="", flush=True)
            print()


if __name__ == "__main__":
    main()
