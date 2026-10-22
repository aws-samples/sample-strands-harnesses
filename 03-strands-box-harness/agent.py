"""A Strands harness agent that proves a secret reached the AgentCore Runtime.

    uv run agent.py    serve /invocations and /ping on :8080, on your laptop

This chapter follows the Strands Box and 1Password guide with one stand-in: AWS Secrets
Manager plays the vendor tool (1Password and `op run` in the guide). The secret is never in
the code package or the runtime configuration. The entrypoint fetches it at each request and
puts it in os.environ before the agent runs, which is what `op run` does in the guide.

Where the value comes from:
    laptop     you export AGENT_SECRET_VALUE before `uv run agent.py`
    Runtime    SECRET_ID names the Secrets Manager secret; invoke() fetches it per request,
               so a rotated value takes effect at the next request with no redeploy

The test:
    The client sends {"prompt": "hello", "expected": "<value>"}. The check_propagation tool
    compares the agent's own AGENT_SECRET_VALUE with the expected value, and the agent
    answers true or false. A true means the value the client holds reached the agent.

Payloads:
    {"prompt": "hello", "expected": "..."}    check the secret, reply true or false
    {"command": "state"}                      return the model, tools, env presence, usage
    {"command": "box_probe"}                  run Strands Box once and return what the probe saw
"""

import os

import boto3
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import tool
from strands_harness import create_harness

from run_box import run_probe

# The env var the agent reads, and the Secrets Manager secret that fills it in the Runtime.
ENV_NAME = "AGENT_SECRET_VALUE"
SECRET_ID = os.environ.get("SECRET_ID")  # set by deploy.py; unset on a laptop

# A basic model: Claude Haiku 5.5 through the us cross-Region inference profile. The
# execution role that deploy.py creates allows this one profile only.
MODEL_ID = "us.anthropic.claude-haiku-5-5"

INSTRUCTIONS = """\
You verify that a configuration value reached this agent.
When the user says hello, call check_propagation with the expected value they give, then
answer with one word only: true if the tool returns true, false if it returns false.
Never guess. The tool can read the real value and you cannot."""


@tool
def check_propagation(expected: str) -> bool:
    """Return whether the propagated env var equals the value the client expects.

    Args:
        expected: The value the client believes was propagated.
    """
    return os.environ.get(ENV_NAME) == expected


app = BedrockAgentCoreApp()
agent = create_harness(
    model=MODEL_ID,
    instructions=INSTRUCTIONS,
    tools=[check_propagation],
    builtin_tools=[],  # no shell or file tools, so the agent cannot read os.environ itself
    session=False,  # one runtime session is one microVM, so the agent object is the session
    memory=False,
    skills=False,
    interventions=None,  # headless: an approval prompt here would never be answered
    callback_handler=None,  # no terminal in the runtime, so do not print the stream
    name="propagation_check",
)


def load_secret() -> None:
    """Fetch the secret into os.environ, as `op run` does before it starts Strands Box.

    On a laptop SECRET_ID is unset, so the value you exported is used as it is.
    """
    if SECRET_ID:
        secret = boto3.client("secretsmanager").get_secret_value(SecretId=SECRET_ID)
        os.environ[ENV_NAME] = secret["SecretString"]


def env_snapshot() -> dict:
    """Report whether the value is present and its length, never the value itself."""
    value = os.environ.get(ENV_NAME)
    return {"name": ENV_NAME, "present": value is not None, "length": len(value or "")}


def state() -> dict:
    """Return the harness state that the runtime holds for this session."""
    metrics = agent.event_loop_metrics
    return {
        "type": "state",
        "model": MODEL_ID,
        "tools": sorted(agent.tool_names),
        "env": env_snapshot(),
        "messages": agent.messages,
        "cycles": metrics.cycle_count,
        "tokens": dict(metrics.accumulated_usage),
    }


@app.entrypoint
async def invoke(payload: dict):
    """Stream the true or false verdict, or return the harness state."""
    load_secret()
    if payload.get("command") == "box_probe":
        # Guide Step 8: start Strands Box with the secret in its environment, as op run does.
        yield run_probe()
        return
    if payload.get("command") == "state":
        yield state()
        return
    expected = payload.get("expected", "")
    prompt = f'{payload.get("prompt", "hello")}\nExpected value: {expected}'
    async for event in agent.stream_async(prompt):
        if "data" in event:
            yield event["data"]


if __name__ == "__main__":
    # Explicit, because the SDK binds 0.0.0.0 only when it detects Docker and otherwise
    # binds 127.0.0.1, which the runtime cannot reach.
    app.run(host="0.0.0.0")  # nosec B104
