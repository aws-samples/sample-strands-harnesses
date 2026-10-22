"""The workload inside Strands Box: report what the agent sees, and what the API receives.

Strands Box starts this file as its [agent] command. It stands in for an agent that calls an
API with a key through its shell tool. It never prints the value it holds, only facts about it:

    env_is_placeholder   the AGENT_SECRET_VALUE this process holds starts with strands_box_
    api_saw              what https://httpbin.org/headers echoed back for the x-api-key header:
                           "[REDACTED]"   the gateway swapped in the real secret on the way out,
                                          then redacted it from the response
                           "placeholder"  the API got the placeholder, so no swap happened
                           "other"        anything else; the value is not printed

The request runs `curl` in the box's own shell, as an agent's shell tool would. Strands Box puts
that `sh` on PATH, and its built-in curl goes through the egress gateway. httpbin echoes request
headers, which is what makes the swap visible from inside the box.
"""

import json
import os
import subprocess

NAME = "AGENT_SECRET_VALUE"

value = os.environ.get(NAME, "")
# Pass the placeholder in as text: it is not the secret, and the box shell gets a minimal environment.
done = subprocess.run(
    ["sh", "-c", f'curl -s -H "x-api-key: {value}" https://httpbin.org/headers'],
    capture_output=True, text=True, timeout=60,
)
try:
    echoed = json.loads(done.stdout)["headers"].get("X-Api-Key", "")
except (ValueError, KeyError):
    echoed = None

if echoed == "[REDACTED]":
    api_saw = "[REDACTED]"
elif echoed == value:
    api_saw = "placeholder"
elif echoed is None:
    api_saw = f"no JSON from curl (exit {done.returncode}): {done.stderr.strip()[-300:]}"
else:
    api_saw = "other"

print(json.dumps({
    "env_is_placeholder": value.startswith("strands_box_"),
    "env_length": len(value),
    "api_saw": api_saw,
}))
