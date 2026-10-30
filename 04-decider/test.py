"""Live checks against a running decider server and Amazon Bedrock.

1. The decider server answers /health.
2. A request with no city: the guessed call is guided back, and the guessed tool call never runs.
3. A request that names a city: the call proceeds and the tool result reaches the reply.
"""

from __future__ import annotations

import sys

from agent import build_agent
from decider_client import Decider, ServerUnavailable

failures = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global failures
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {name}{'  ' + detail if detail else ''}")


def tool_ran(agent) -> bool:
    return any(
        "toolResult" in block
        for message in agent.messages
        for block in message.get("content", [])
        if isinstance(block, dict)
    )


def main() -> int:
    decider = Decider()
    try:
        health = decider.health()
    except ServerUnavailable as exc:
        check("decider server answers /health", False, str(exc))
        return 1
    check("decider server answers /health", True, f"{health.get('checkpoint')} on {health.get('device')}")

    agent, reviewer = build_agent(decider)
    agent("What's the weather?")
    first = reviewer.log[0] if reviewer.log else {}
    check("vague request: first call is guided back", first.get("verdict") == "guided", str(first))
    check("vague request: guessed tool call never runs", not tool_ran(agent))

    agent, reviewer = build_agent(decider)
    reply = str(agent("What's the weather in Paris?"))
    check("grounded request: call proceeds", any(r["verdict"] == "proceeded" for r in reviewer.log), str(reviewer.log))
    check("grounded request: tool result reaches the reply", "21" in reply, reply.strip()[:120])

    print(f"\n{5 - failures} of 5 checks passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
