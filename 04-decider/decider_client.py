"""A small client for a running Strands Decider server.

The server answers POST /v1/systemone with one state and many typed questions. The state is
read once and shared across the questions, so ask everything you need in one request.
Adapted from examples/strands/_client.py in strands-labs/strands-decider.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

DEFAULT_URL = os.environ.get("STRANDS_DECIDER_URL", "http://127.0.0.1:8099")
SERVE_HINT = "uv run --group decider strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8099 --device mlx"


class ServerUnavailable(RuntimeError):
    """Nothing is answering at the decider URL."""


def noul(instructions: str, true: str, false: str) -> dict[str, Any]:
    """A yes/no question. The answer is P(true), from 0 to 1.

    The descriptions of true and false carry most of the signal, so write them carefully.
    """
    return {"type": "noul", "instructions": instructions, "criteria": {"true": true, "false": false}}


class Decider:
    def __init__(self, url: str = DEFAULT_URL, timeout: float = 120.0) -> None:
        self.url = url.rstrip("/")
        # The first request at a new input length can pay a one-off compile on Apple silicon.
        self.timeout = timeout
        self.last_latency_ms: float | None = None

    def _get(self, path: str, body: dict | None = None) -> dict[str, Any]:
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(
            f"{self.url}{path}", data=data, headers={"content-type": "application/json"}
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read())
        except urllib.error.URLError as exc:
            raise ServerUnavailable(
                f"no Strands Decider at {self.url} ({exc}). Start one with:\n    {SERVE_HINT}"
            ) from exc

    def health(self) -> dict[str, Any]:
        """The loaded checkpoint and device. Raises ServerUnavailable if nothing is serving."""
        return self._get("/health")

    def ask(self, state: str, questions: dict[str, dict[str, Any]]) -> dict[str, Any]:
        """Answer every question about `state`. Answers come back under the same keys."""
        payload = self._get("/v1/systemone", {"state": state, "questions": questions})
        self.last_latency_ms = payload.get("latency_ms")
        return payload["answers"]
