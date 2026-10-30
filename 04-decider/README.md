# 04 · Strands Decider harness

This chapter puts [Strands Decider](https://github.com/strands-labs/strands-decider) inside a Strands
agent. Strands Decider is a small decision model. It does not generate text. It picks between
options or gives a probability, and it answers in about 100 to 500 ms on a laptop.

The agent has one tool, `get_weather`, and a system prompt that tells it to guess a city when the
user does not name one. Before each tool call runs, a Strands intervention (a handler that runs
before a tool executes) sends the conversation and the proposed call to the decider. The decider
answers two yes/no questions:

1. Are the argument values grounded in what the user said?
2. Is it premature to call this tool before asking the user?

Plain Python turns the two probabilities into an action. `Guide` hands the turn back to the model
with feedback, so the agent asks which city you meant. `Proceed` lets the call run. The model
classifies, and the code decides.

This first version runs on your laptop only. It does not deploy to AgentCore Runtime yet. It is
adapted from the upstream [Strands example](https://github.com/strands-labs/strands-decider/tree/main/examples/strands)
and the [launch blog post](https://strandsagents.com/blog/introducing-strands-decider/).

## Files

| File | What it does |
| ---- | ------------ |
| `agent.py` | The agent, the `get_weather` tool, the two questions, and the `ToolCallReviewer` intervention |
| `decider_client.py` | A small HTTP client for the decider server's `/v1/systemone` endpoint |
| `test.py` | Five live checks against the decider server and Amazon Bedrock |

## Run it

The decider server needs torch and the model code, so it sits in its own dependency group. The first
`serve` downloads the 2B model weights from Hugging Face, about 4 GB.

Terminal 1, the decider server on an Apple-silicon Mac:

```bash
cd 04-decider
uv run --group decider strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8099 --device mlx
```

On another machine, use `--device cpu`, `--device mps` or `--device cuda`.

Terminal 2, the agent:

```bash
cd 04-decider
uv run agent.py "What's the weather?"            # the guessed city is guided back
uv run agent.py "What's the weather in Paris?"   # the call proceeds
uv run test.py                                   # five live checks
```

`STRANDS_DECIDER_URL` overrides the server address. The default is `http://127.0.0.1:8099`.

## Prerequisites

1. [uv](https://docs.astral.sh/uv/) and Python 3.11 or later.
2. AWS credentials with Amazon Bedrock access to `us.anthropic.claude-haiku-5-5`. The decider runs
   locally and needs no AWS access.
3. About 4 GB of disk for the model weights and about 5 GB of free memory to serve them.

## Limits

The questions, the 0.45 threshold and the policy come from the upstream example and were picked by
hand. Tune them on your own traffic before you rely on them.
