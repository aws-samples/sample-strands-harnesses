# Strands harness samples

This repository holds runnable demos of agents built with the [Strands Agents SDK](https://strandsagents.com/)
and its projects: the Strands harness, [Strands Box](https://strandsagents.com/docs/user-guide/box/),
Strands Evals, and custom integrations with AWS services and third-party tools. Each demo deploys to
Amazon Bedrock AgentCore Runtime and comes with a test that proves it works.

## Chapters

Each chapter is a folder that deploys on its own with the AWS CDK. Every chapter puts the agent behind
an AWS API instead of a terminal, so a program calls it with an IAM role, and each session runs in its
own microVM. Chapter 01 explains that choice in its
[rationale](01-simple-strands-harness/README.md#rationale-why-not-a-coding-cli-on-a-remote-box).

| Chapter | What it shows |
| ------- | ------------- |
| [01 · Simple Strands harness](01-simple-strands-harness/) | A simple Strands harness deployed on AgentCore Runtime, with SigV4 auth and session state |
| [03 · Strands Box harness](03-strands-box-harness/) | A vendor-held secret (like 1Password) reaches an agent in Strands Box, on a laptop and in AgentCore Runtime, and the agent sees only a placeholder |
| [05 · Software factory](05-software-factory/) | Six agents turn one product goal into tested code and a release, graded with Strands Evals, and you approve each step |

Every chapter has the same shape. `agent.py` is the code that runs on AgentCore Runtime. `deploy.py`
builds a code zip and deploys a CDK stack, so you need neither Docker nor Finch. `cli.py` runs on your
laptop and calls the runtime with your own AWS credentials. `test.py` checks the deployed runtime end
to end. `architecture.md` explains the design and walks through the code.

## Chapter 01: a simple Strands harness

Chapter 01 is the smallest harness that is still a harness: one Strands agent, two tools, SigV4
authentication, and a session state that you can read. Each `cli.py` run is one runtime session, so
the notes that one session saves are on a disk that no other session can read.

```bash
cd 01-simple-strands-harness
uv sync
uv run deploy.py         # deploy the SimpleStrandsHarness stack, about a minute
uv run cli.py            # chat, then /history, /state, or exit
uv run test.py           # check the loop, the tools, the session disk, and the history
npx aws-cdk destroy      # remove the stack
```

## Chapter 03: a vendor secret through Strands Box

Chapter 03 is the runnable version of the Strands Box and 1Password integration. AWS Secrets Manager
stands in for the vendor. The Runtime entrypoint fetches the secret at each request, puts it in the
environment, and starts Strands Box. The agent inside the box holds only a `strands_box_` placeholder,
and the box's egress gateway puts the real secret only on requests to the approved API.

The chapter needs the Strands Box binaries, which are not committed: the macOS release for the laptop
check, and a Linux arm64 build for Runtime. Its [README](03-strands-box-harness/README.md) shows how to
get both. Then run these commands in one shell:

```bash
cd 03-strands-box-harness
uv sync
export AGENT_SECRET_VALUE="box-demo-$(date +%s)"
uv run run_box.py        # laptop: Strands Box on macOS
aws secretsmanager put-secret-value --secret-id agent/demo-secret --secret-string "$AGENT_SECRET_VALUE" 2>/dev/null \
  || aws secretsmanager create-secret --name agent/demo-secret --secret-string "$AGENT_SECRET_VALUE"
uv run deploy.py         # deploy the StrandsBoxHarness stack
uv run test.py           # seven live checks in AgentCore Runtime
npx aws-cdk destroy      # remove the stack
```

## Chapter 05: the software factory

Chapter 05 turns one product goal into tested code and a release. An example goal is "a task
tracker MVP with projects, tasks, workflow, assignment and a summary". Six agents run in turn on
AgentCore Runtime: clarify, plan, build, test, review, and release. The factory stops for you three
times. You answer its questions, you approve the feature list, and you approve the release. After
the review, it downloads the code to your laptop as a zip and shows the code in the terminal.
Every stage writes an OpenTelemetry audit trail to CloudWatch, and every call is signed with SigV4.

To learn the chapter, read these files in order:

1. [architecture.md](05-software-factory/architecture.md) explains what happens when you run the
   factory and what each component does. It also walks through the code.
2. [README.md](05-software-factory/README.md) explains how to run the factory, where the code
   goes, the settings, and the known limits.
3. The docstring at the top of [evals.py](05-software-factory/evals.py) explains how the agents
   are graded.

To run the chapter, use these commands:

```bash
cd 05-software-factory
uv sync
uv run deploy.py                           # deploy the SoftwareFactory stack
uv run cli.py "your product goal here"     # name the app, answer the questions, approve, get the code
uv run cli.py --apps                       # list your app names
uv run cli.py --download <app>             # get the code and a local SigV4 URL for the app
uv run test.py --yes                       # the full cycle on a built-in goal, then the checks
uv run evals.py                            # grade the agents, about two minutes
npx aws-cdk destroy                        # remove the stack
```

A goal with five features takes about 15 to 30 minutes.

## Prerequisites

You need these items for every chapter:

1. [uv](https://docs.astral.sh/uv/) and Node.js for `npx`.
2. AWS credentials and a US Region in your environment or `~/.aws`. A chapter deploys to whichever
   account and Region those credentials point to. The examples use `us-west-2`.
3. A CDK bootstrap in that account and Region. Run `npx aws-cdk bootstrap` once, from any chapter
   folder.
4. Amazon Bedrock model access in that Region. Chapters 01 and 05 use Claude Sonnet 5 through
   `us.anthropic.claude-sonnet-5`, and chapter 03 uses Claude Haiku 5.5 through
   `us.anthropic.claude-haiku-5-5`.

Each chapter deploys its own stack, so you can run one chapter without the others. Remove a stack when
you finish with it, because a deployed runtime keeps its IAM role and logs.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
