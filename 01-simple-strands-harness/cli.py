"""Chat with the agent that deploy.py put on AgentCore. Calls are SigV4-signed.

    uv run cli.py

Needs the SimpleStrandsHarness stack. It does not talk to a local agent.py.
One run is one runtime session, so the agent remembers the conversation.

    /history    message history held by the runtime
    /state      history plus model, tools, loop cycles, tokens, notes
    exit        quit
"""

import json
import uuid

import boto3

STACK_NAME = "SimpleStrandsHarness"  # the stack that deploy.py creates
CUT = 96  # characters of each text block to print


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
    for line in response["response"].iter_lines():
        if line.startswith(b"data: "):
            yield json.loads(line[6:])


def stream(client, arn: str, session_id: str, prompt: str):
    """Yield the reply to one prompt as it streams back."""
    return invoke(client, arn, session_id, {"prompt": prompt})


def get_state(client, arn: str, session_id: str) -> dict:
    """Ask the runtime for the harness state of this session."""
    return next(chunk for chunk in invoke(client, arn, session_id, {"command": "state"}))


def one_line(block: dict) -> str:
    """Render one content block: text, reasoning, a tool call, or a tool result."""
    if "text" in block:
        return " ".join(block["text"].split())[:CUT]
    if "reasoningContent" in block:
        text = block["reasoningContent"].get("reasoningText", {}).get("text", "")
        return f"thinks ({len(text)} characters)" if text else "thinks (kept by the model)"
    if "toolUse" in block:
        call = block["toolUse"]
        return f"calls {call['name']}({json.dumps(call['input'])[:CUT]})"
    if "toolResult" in block:
        inner = block["toolResult"]["content"][0]
        return f"returns {str(inner.get('text', inner))[:CUT]}"
    return next(iter(block), "?")


def print_history(messages: list[dict]) -> None:
    for i, message in enumerate(messages, 1):
        for block in message["content"]:
            print(f"  {i:>2} {message['role']:<9} {one_line(block)}")


def print_state(state: dict) -> None:
    print(f"  model    {state['model']}")
    print(f"  tools    {', '.join(state['tools'])}")
    print(f"  messages {len(state['messages'])}   loop cycles {state['cycles']}")
    print(f"  tokens   {state['tokens']['totalTokens']} total"
          f" ({state['tokens']['inputTokens']} in, {state['tokens']['outputTokens']} out)")
    print(f"  notes    {' | '.join(state['notes'].splitlines())}")
    print_history(state["messages"])


def main() -> None:
    session = boto3.Session()
    client = session.client("bedrock-agentcore")
    arn = runtime_arn(session)
    session_id = str(uuid.uuid4())
    print(f"session {session_id}. Try /history, /state, or exit.")

    while True:
        try:
            prompt = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt in ("exit", "quit"):
            break
        if prompt in ("/history", "/state"):
            state = get_state(client, arn, session_id)
            print_state(state) if prompt == "/state" else print_history(state["messages"])
        elif prompt:
            for chunk in stream(client, arn, session_id, prompt):
                print(chunk, end="", flush=True)
            print()


if __name__ == "__main__":
    main()
