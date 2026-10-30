"""A Strands agent whose tool calls are checked by Strands Decider before they run.

The agent has one tool, get_weather, and an eager system prompt that tells it to guess a city
instead of asking. Before each tool call runs, a Strands intervention sends the conversation and
the proposed call to the local decider, which answers two yes/no questions:

1. Are the argument values grounded in what the user said?
2. Is it premature to call this tool before asking the user?

Plain Python turns the two probabilities into an action. Guide hands the turn back to the model
with feedback, so the agent asks which city you meant. Proceed lets the call run.
The model classifies; the code decides.

    uv run agent.py "What's the weather?"          # guessed city, so the call is guided back
    uv run agent.py "What's the weather in Paris?"  # grounded, so the call proceeds

Based on examples/strands/tool_call_intervention.py in strands-labs/strands-decider.
"""

from __future__ import annotations

import json
import sys

from strands import Agent, tool
from strands.interventions import Guide, InterventionHandler, Proceed

from decider_client import Decider, ServerUnavailable, noul

MODEL_ID = "us.anthropic.claude-haiku-5-5"

QUESTIONS = {
    "args_grounded": noul(
        "Are the tool's argument values grounded in facts the user actually provided?",
        true="every argument value traces back to something the user said",
        false="an argument value was guessed or invented, not stated by the user",
    ),
    "premature": noul(
        "Is it premature to call this tool now, before clarifying with the user?",
        true="the assistant should ask a clarifying question before calling the tool",
        false="there is nothing left to clarify; calling now is appropriate",
    ),
}

# A probability at or above YES reads as "yes". This is the policy knob, owned by the code.
# 0.45 comes from the upstream example; tune it on your own traffic.
YES = 0.45

SYSTEM_PROMPT = (
    "You are an eager weather assistant. Always answer weather questions by calling the "
    "get_weather tool immediately. Never ask the user for clarification. If no city is "
    "given, assume Seattle and call the tool with location='Seattle'."
)


@tool
def get_weather(location: str) -> str:
    """Get the current weather for a city.

    Args:
        location: The city to look up, for example "Seattle" or "Paris".
    """
    return f"It's 21C and sunny in {location}."


class ToolCallReviewer(InterventionHandler):
    """Ask the decider about each proposed tool call, then return Guide or Proceed."""

    name = "strands-decider-tool-call-reviewer"

    def __init__(self, decider: Decider) -> None:
        self.decider = decider
        self.log: list[dict[str, object]] = []

    @staticmethod
    def _conversation(messages: list[dict]) -> str:
        lines = [
            f"{m.get('role', 'unknown')}: {block['text']}"
            for m in messages
            for block in m.get("content", [])
            if isinstance(block, dict) and "text" in block
        ]
        return "\n".join(lines) or "(no conversation yet)"

    def before_tool_call(self, event, **kwargs):
        tool_name = event.tool_use["name"]
        arguments = event.tool_use.get("input") or {}
        state = (
            "A conversation between a user and an AI assistant is below, followed by a "
            "tool call the assistant now wants to make.\n\n"
            f"--- CONVERSATION ---\n{self._conversation(event.agent.messages)}\n\n"
            f"--- PROPOSED TOOL CALL ---\ntool: {tool_name}\narguments: {json.dumps(arguments)}"
        )
        answers = self.decider.ask(state, QUESTIONS)
        grounded = answers["args_grounded"]["noul"]
        premature = answers["premature"]["noul"]

        if grounded < YES:
            verdict, action = "guided", Guide(
                feedback="The arguments look guessed, not stated by the user. "
                "Ask the user for the values instead of inventing them."
            )
        elif premature >= YES:
            verdict, action = "guided", Guide(
                feedback="It is too early to call this tool. Ask the user first, then try again."
            )
        else:
            verdict, action = "proceeded", Proceed()

        row = {
            "tool": tool_name,
            "arguments": arguments,
            "args_grounded": round(grounded, 2),
            "premature": round(premature, 2),
            "latency_ms": self.decider.last_latency_ms,
            "verdict": verdict,
        }
        self.log.append(row)
        print(f"[decider] {json.dumps(row)}")
        return action


def build_agent(decider: Decider) -> tuple[Agent, ToolCallReviewer]:
    reviewer = ToolCallReviewer(decider)
    agent = Agent(
        model=MODEL_ID,
        tools=[get_weather],
        interventions=[reviewer],
        system_prompt=SYSTEM_PROMPT,
        callback_handler=None,
    )
    return agent, reviewer


def main() -> int:
    prompt = " ".join(sys.argv[1:]) or "What's the weather?"
    decider = Decider()
    try:
        health = decider.health()
    except ServerUnavailable as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"decider: {health.get('checkpoint')} on {health.get('device')} at {decider.url}")
    agent, _ = build_agent(decider)
    print(f"USER: {prompt}")
    print(f"AGENT: {agent(prompt)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
