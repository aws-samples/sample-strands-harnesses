# 05 · Software factory

This chapter turns one product goal into a released MVP. Six agents run in turn on Amazon Bedrock
AgentCore Runtime: clarify, plan, build, test, review, and release. Build, test, and review repeat until the
reviewer approves, three rounds at most. Then the factory stops and asks a person before it releases.
See [architecture.md](architecture.md) for the design.

Every call is signed with SigV4 from your own AWS credentials. The runtime has no Cognito and no
bearer token. Every stage sends an OpenTelemetry audit trail to CloudWatch by default.

## Prerequisites

You need these items:

1. [uv](https://docs.astral.sh/uv/) and Node.js for `npx aws-cdk`.
2. AWS credentials and a Region in your environment or `~/.aws`. The examples use `us-west-2`.
3. Amazon Bedrock access to Claude Sonnet 5 in that Region. `agent.py` and `deploy.py` name
   `us.anthropic.claude-sonnet-5`.
4. A CDK bootstrap in that account and Region. Run `npx aws-cdk bootstrap` once.

## How to run this chapter

```bash
cd 05-software-factory
uv sync                                    # once
uv run deploy.py                           # build the code zip and deploy the SoftwareFactory stack
uv run cli.py "a task tracker MVP with projects, tasks, workflow, assignment and a summary"
uv run test.py --yes                       # the full cycle on the built-in goal, then the checks
npx aws-cdk destroy                        # remove the stack
```

`deploy.py` is safe to run again. A change to `agent.py` or `telemetry.py` updates the same runtime
in place. A change to `cli.py` or `test.py` needs no deploy, because those files run on your laptop.

## Give the factory a goal

`cli.py` takes a short goal as an argument, or a longer goal from a file:

```bash
uv run cli.py "a task tracker MVP with projects, tasks, workflow, assignment and a summary"
uv run cli.py --goal-file goal.md
uv run cli.py --goal-file goal.md --yes    # take every default and approve every gate
```

The factory stops for you three times:

1. After the clarify step, it asks up to five questions, each with a default in brackets. Press
   Enter to keep the default, or type your own answer. The answers go to the planner.
2. After the plan step, it shows `features.md` and asks `Build these features?`. Type `yes`,
   `no`, or the changes you want. The planner applies your changes and shows the list again.
3. After the reviewer approves, it shows `review.md` and asks `Release this work item?`.

A goal with five features takes about 15 to 30 minutes. The terminal shows each stage in its own
color, each tool call as one line, and a progress line every minute while an agent is busy. Use
`--yes` only for an unattended run. Set `NO_COLOR=1` to turn the colors off.

At the start, the factory asks for an app name, with a default taken from the goal, for example
`task-tracker-mvp`. Pass `--app taskflow` to set it without the question. `cli.py` keeps each
name and its work item in `out/apps.json`. Use the name to get the code and a URL later:

```bash
uv run cli.py --apps                       # list the apps and their work items
uv run cli.py --download taskflow          # get the code, then serve the app on a local URL
uv run cli.py --download taskflow --no-serve
uv run cli.py --stage review --work-item sdlc-4eef6708-6065-4c4d-872b-10a7e1d627e8
```

## Where the code goes

The agents write every file in the workspace of the work item, inside its AgentCore session.
After review, `cli.py` downloads the workspace to your laptop and shows the source files in the
terminal with syntax highlighting:

```
out/sdlc-<id>.zip     the zip, to keep or share
out/sdlc-<id>/        the same files, unzipped, ready to run
```

After the release, the download runs again, so the zip also holds `release.md`. At the end of a
run, a panel shows the folder and the run and test commands from the generated `README.md`.

## Test the app through a SigV4 URL

`uv run cli.py --download <app>` downloads the code, then starts the app in its AgentCore session
and prints a local URL, `http://127.0.0.1:8765/` by default. Open it in a browser or call it with
`curl`. Press Ctrl+C to stop the app and the URL. Use `--port` to choose another local port.

The app listens on 127.0.0.1 inside the microVM, so nothing outside the microVM can reach it.
`cli.py` runs a small server on your laptop, bound to 127.0.0.1. It sends each request to the app
as one `invoke_agent_runtime` call, signed with SigV4 from your own credentials, and returns the
app's answer. The URL gets no public address and no token.

The runtime starts the app with the `start` command in the `app.json` that the builder writes. If
there is no `app.json`, it runs the first `server.py`, `app.py`, or `main.py` that it finds, in
the root or in `backend/`. It installs `requirements.txt` first and sets `PORT=8765`.

The workspace lives only as long as the AgentCore session. When AgentCore ends an idle session,
the next call gets a new microVM with an empty workspace. Then `--download` keeps your earlier
download, copies it to the new workspace, and serves the app from there. Use `--out` to choose
another download folder.

## How to prove it works

`uv run test.py --yes` runs the whole cycle and ends with a list of checks. A good run ends with
`PASS: the factory ran the full cycle for sdlc-...`. The checks confirm that each stage wrote its
files, that the reviewer approved within three rounds, that the release ran only after the approval,
and that the metrics reached CloudWatch.

To see the audit trail:

1. Open CloudWatch Query Studio and query the metrics `factory_stage_duration`,
   `factory_stage_tokens`, `factory_review_verdicts`, `factory_rounds`, and
   `factory_release_decisions`.
2. Open X-Ray traces for the service `software_factory.DEFAULT`.
3. Read the runtime log group `/aws/bedrock-agentcore/runtimes/<runtime id>-DEFAULT`. It has one
   line for each stage start, each tool call, and each stage end.

## Grade the agents with evals

`test.py` checks one product that the factory builds. `evals.py` checks the agents that build
it. Run the evals after every change to `agent.py`, for example to a stage's instructions, its
tools, or the model:

```bash
uv run evals.py                  # both suites, about two minutes
uv run evals.py --suite review   # one suite
```

The evals run the real stage agents on your laptop with your own AWS credentials, so you do not
deploy first. The reviewer suite checks that the reviewer rejects a stub and approves finished
work. The planner suite checks that the planner writes `requirements.md` and `spec.md` and no
code. Each suite must score 0.8 or more, and the command exits 1 when a suite scores less. Every
score also goes to CloudWatch as `factory_eval_score`. The docstring of `evals.py` explains the
scoring and how to add a case.

## Configuration

These environment variables change the defaults:

| Variable | Where | Default | Effect |
|---|---|---|---|
| `FACTORY_RUNTIME_ARN` | laptop | stack output | The runtime that `cli.py` calls |
| `FACTORY_STAGE_TIMEOUT_SECONDS` | runtime | `4800` | The time limit for one stage |
| `FACTORY_STAGE_IDLE_SECONDS` | runtime | `600` | A stage that sends nothing for this long fails |
| `FACTORY_METRICS` / `FACTORY_TRACES` | both | `on` | Set `off` to stop metrics or traces |
| `FACTORY_METRICS_SECONDS` | both | `15` | The export interval for metrics |

## Known limits

1. The runtime has no Node.js, so an MCP server that needs `npx` is skipped. The Playwright server in
   `mcp.json` is skipped for this reason, and the stages test an app with `curl` and pytest instead.
   For browser tests, use AgentCore Browser or a container runtime.
2. When Bedrock returns a temporary error, `cli.py` starts the stage again, up to three times. The
   files that the stage already wrote stay in place.
3. A stage can leave a test server running after it ends. The next stage can then reach the old
   server on the same port.
