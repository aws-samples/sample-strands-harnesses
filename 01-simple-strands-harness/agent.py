"""A Strands agent served on the AgentCore Runtime contract.

    uv run agent.py    serve /invocations and /ping on :8080, on your laptop

Locally it needs only AWS credentials that can call Bedrock. deploy.py runs this same
file on AgentCore, where each runtimeSessionId gets its own microVM.

Payloads:
    {"prompt": "..."}       run the agent loop and stream the reply
    {"command": "state"}    return the model, tools, history, loop cycles, tokens, notes
"""

import tempfile
from pathlib import Path

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool

# On the microVM disk of this session, not in the model context. The temporary
# directory, because the runtime mounts the deployed code read-only.
NOTES = Path(tempfile.gettempdir()) / "notes.txt"

# Anthropic Claude Sonnet 5 through the us cross-Region inference profile, which serves
# the call from a US Region with capacity. Named here on purpose, because the Strands
# default is still Sonnet 4.6. The execution role that deploy.py creates allows this one
# profile and nothing else.
MODEL_ID = "us.anthropic.claude-sonnet-5"

SYSTEM_PROMPT = """\
You are a friendly assistant. Keep replies short.
Use the remember tool when the user states a fact worth keeping, and the recall tool
when the user asks what you know. Do not answer from the conversation alone."""


@tool
def remember(fact: str) -> str:
    """Append one fact to the notes file of this session.

    Args:
        fact: The fact to keep, in one line.
    """
    with NOTES.open("a") as f:
        f.write(fact.strip() + "\n")
    return f"saved: {fact.strip()}"


@tool
def recall() -> str:
    """Return every fact saved in this session, one per line."""
    return NOTES.read_text() if NOTES.exists() else "(nothing saved yet)"


app = BedrockAgentCoreApp()
agent = Agent(
    model=MODEL_ID,
    system_prompt=SYSTEM_PROMPT,
    tools=[remember, recall],
    callback_handler=None,  # no terminal in the runtime, so do not print the stream
)


def state() -> dict:
    """Return the harness state that the runtime holds for this session."""
    metrics = agent.event_loop_metrics
    return {
        "type": "state",
        "model": MODEL_ID,
        "tools": sorted(agent.tool_names),
        "messages": agent.messages,  # role plus content blocks, tool calls included
        "cycles": metrics.cycle_count,  # one cycle per model call in the loop
        "tokens": dict(metrics.accumulated_usage),
        "notes": recall(),
    }


@app.entrypoint
async def invoke(payload: dict):
    """Stream the reply to payload["prompt"], or return the state of the harness."""
    if payload.get("command") == "state":
        yield state()
        return
    async for event in agent.stream_async(payload["prompt"]):
        if "data" in event:
            yield event["data"]


if __name__ == "__main__":
    # Explicit, because the SDK binds 0.0.0.0 only when it detects Docker and otherwise
    # falls back to 127.0.0.1, which the runtime cannot reach.
    app.run(host="0.0.0.0")  # nosec B104
