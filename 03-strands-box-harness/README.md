# Chapter 03: a vendor secret reaches a Strands Box on AgentCore Runtime

This chapter is the runnable version of the Strands Box and 1Password guide, with AWS Secrets
Manager as a stand-in for the vendor tool. You store a value in Secrets Manager. The Runtime
entrypoint fetches it at each request and puts it in `os.environ`, as `op run` does in the guide.
Then you type `hello`, and the agent answers `true` if its value matches the value in your shell.

## What you need

1. [uv](https://docs.astral.sh/uv/) and Node.js for `npx`.
2. AWS credentials for an account with a CDK bootstrap, and the Region `us-west-2`.
3. Amazon Bedrock access to Claude Haiku 5.5 (`us.anthropic.claude-haiku-5-5`).

## Run and verify

You need the Strands Box binaries first. They are not committed:

```bash
cd 03-strands-box-harness
curl -fsSLO https://raw.githubusercontent.com/strands-agents/box/main/download.sh
BOX_DOWNLOAD_DIR="$PWD/bin-macos" sh download.sh   # the macOS release
# bin-linux/: strands-box, strands-box-contain-trampoline, strands-box-sock-alias, built for
# Linux arm64 against glibc 2.34 (Amazon Linux 2023), for example in an amazonlinux:2023 container:
#   cargo build --release -p strands-box -p strands-box-containment
```

Run the laptop check, then deploy and run the live check, in one shell:

```bash
uv sync
export AGENT_SECRET_VALUE="box-demo-$(date +%s)"
uv run run_box.py       # laptop: Strands Box on macOS, the same path as in Runtime
# Store the value: update the secret if an earlier run created it, otherwise create it.
aws secretsmanager put-secret-value --secret-id agent/demo-secret --secret-string "$AGENT_SECRET_VALUE" 2>/dev/null \
  || aws secretsmanager create-secret --name agent/demo-secret --secret-string "$AGENT_SECRET_VALUE"
uv run deploy.py        # deploy the StrandsBoxHarness stack as a code zip, no Docker
uv run test.py          # the live check in AgentCore Runtime
```

If the whole path works, `test.py` ends with these lines:

```
  pass  the runtime streamed a verdict
  pass  AGENT_SECRET_VALUE is present in the runtime
  pass  the matching value returns true
  pass  a wrong value returns false
  pass  Strands Box started in the Runtime microVM
  pass  the agent inside Strands Box holds only a strands_box_ placeholder
  pass  the API got the real secret, redacted in the response

PASS: the secret reached the Runtime through Secrets Manager, Strands Box gave the agent a placeholder, and the API received the real secret.
```

The Strands Box checks use `box/probe.py` as the workload. It sends its placeholder to
`https://httpbin.org/headers` with the box shell's `curl`. The gateway swaps in the real secret, and
httpbin echoes it back, so the probe sees `[REDACTED]` in the response. That proves the API received the
real value while the agent held only the placeholder.

To check it by hand, use `cli.py`. `/state` shows whether the value is present and its length,
never the value. Type `exit` to quit.

```bash
uv run cli.py                              # type hello, the agent answers true
AGENT_SECRET_VALUE=other uv run cli.py     # type hello, the agent answers false
```

To see rotation with no redeploy, put a new value in the secret and export it, then run
`uv run test.py` again:

```bash
export AGENT_SECRET_VALUE="box-demo-$(date +%s)"
aws secretsmanager put-secret-value --secret-id agent/demo-secret --secret-string "$AGENT_SECRET_VALUE"
```

To remove the chapter, destroy the stack with the CDK (`npx aws-cdk destroy`), then delete the
secret with `aws secretsmanager delete-secret --secret-id agent/demo-secret`.

## How it maps to the guide

| Guide step                                   | This chapter                                                          |
| -------------------------------------------- | --------------------------------------------------------------------- |
| 1 to 3: `box.toml`, policy | `run_box.py` writes `box.toml` per run; `box/policy.dw` is the policy |
| 4: run on a laptop | `uv run run_box.py` with `AGENT_SECRET_VALUE` exported |
| 5: store the vendor token in Secrets Manager | `aws secretsmanager create-secret` stores the value itself            |
| 6: let the execution role read it            | `deploy.py` grants `secretsmanager:GetSecretValue` on that one secret |
| 7: package the code | `deploy.py` builds a code zip with the Linux build of Strands Box in `box-bin/` |
| 8: entrypoint fetches the secret, then starts Strands Box | `load_secret()`, then `run_probe()` for `{"command": "box_probe"}` |
| 9: test one Runtime session                  | `uv run test.py`                                                      |

[architecture.md](architecture.md) has the diagram and details.

## Limits

1. The workload in the box is a probe, not a model-driven agent. The harness agent outside the box
   still holds the real value for its true/false check.
2. Secrets Manager holds the secret itself here. In the guide it holds only the 1Password token,
   and 1Password holds the secret.
