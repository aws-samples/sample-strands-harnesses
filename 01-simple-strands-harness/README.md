# 01 · Simple Strands harness

This is a simple [Strands Agents](https://strandsagents.com) harness deployed on Amazon Bedrock
AgentCore Runtime. It is the smallest harness that is still a harness: one agent, two tools, SigV4
authentication, and a session state you can read. You call it from your terminal with your own AWS
credentials, so there is no Amazon Cognito. See [architecture.md](architecture.md) for the design and
the diagrams.

## Rationale: why not a coding CLI on a remote box

A command line agent such as Kiro CLI or Claude Code is the better tool when a person does the work.
It already has file tools, a shell, Model Context Protocol servers, permission prompts, and context
management, and this chapter has two small tools. If the job is one engineer working on a remote
machine, the CLI wins, and this chapter would need months of work to catch up. The reason to build
this instead is the interface, not the features.

This agent is an AWS API, not a terminal. Any program with an IAM role calls `InvokeAgentRuntime` with
no SSH, no shell, no terminal session, and no long-lived host. The agent runs in AWS, so the work does
not stop when a laptop sleeps, and a caller needs no model access of their own.

Isolation per user comes with the runtime, and you write no code for it. AgentCore gives every
`runtimeSessionId` its own microVM, which is a small separate virtual machine with its own CPU, memory,
and file system. That is what makes the `remember` tool in this chapter safe. The notes of one session
sit on a disk that no other session can read. When the session stops, AgentCore ends the microVM and
clears its memory. A thousand concurrent sessions need no scheduling work from you. One CLI host is the
opposite: one shared file system, one shared process space, and one shared credential file.

The security model is the part that is hard to copy on a box. Each caller signs the request with their
own credentials, so nothing long-lived is copied onto a shared machine. You grant or revoke access by
IAM policy, for each person or service. CloudTrail records every invoke. The agent runs under an
execution role that allows one Bedrock model and its own logs. It never sees the credentials of the
caller. A remote CLI inherits whatever the host can reach, and everyone who can log in inherits it too.

You also own the loop. You choose the tools, the system prompt, and the limits, which is what makes an
agent safe to expose to people you do not trust. A full CLI harness gives every user shell access by
design.

So choose by consumer. For your own work, use the CLI. For an application, a queue, a webhook, or many
end users, put a narrow agent behind an API. This chapter is a skeleton of that.

## Prerequisites

You need these items:

1. [uv](https://docs.astral.sh/uv/) and Node.js for `npx`.
2. AWS credentials and a Region in your environment or `~/.aws`.
3. Amazon Bedrock access to Claude Sonnet 5 in that Region. `agent.py` names
   `us.anthropic.claude-sonnet-5`, which is a cross-Region inference profile for US Regions.

## How to run this chapter

```bash
cd 01-simple-strands-harness
npx aws-cdk bootstrap    # once per account and Region
npx aws-cdk deploy       # about a minute, prints RuntimeArn
uv run cli.py            # chat, then /history, /state, or exit
uv run test.py           # prove the loop, the tools, the disk, and the history
npx aws-cdk destroy      # remove the stack
```

`deploy.py` puts `agent.py` and its dependencies in a code zip, so you need neither Docker nor Finch.
The deploy is idempotent, which means it is safe to run twice. A change to `agent.py` updates the same
runtime in place, and the runtime ARN stays the same.

## How to prove it is deployed

Every deploy prints two commands with the real runtime ARN filled in. `InvokeCommand` uses the AWS
CLI, and needs a CLI that knows `bedrock-agentcore`, which is version 2.31 or later. Check yours with
`aws --version`. `InvokeCommandBoto3` is the same call through boto3, for an older CLI. Paste either
one, and the runtime answers on the stream:

```
data: "it"

data: " works"
```

To reprint the commands without deploying, read the stack outputs:

```bash
aws cloudformation describe-stacks --stack-name SimpleStrandsHarness \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' --output text
```

## How to see the history

One run of `cli.py` is one runtime session. Type `/history` at the prompt to print the message history
that the runtime holds for that session, including every tool call and tool result. Type `/state` to
print the same history with four more facts. They are the tool list, the loop cycle count, the token
count, and the notes the agent saved on the session disk. Your terminal keeps no copy. Both commands
read the runtime.

## What `test.py` proves

The test sends two prompts in one session, then reads the state. It checks five claims, and fails if
any one of them is false. The agent loop called a tool. The loop continued with the tool result. The
loop ran more cycles than there were prompts. The tool wrote the code word to the session disk. The
returned history is longer than the prompts alone. That is the difference between a harness and a call
to a model.
