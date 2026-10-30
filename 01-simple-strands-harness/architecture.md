# Simple Strands harness: architecture

*One agent, one code zip, one runtime.*

Four files do the whole job. `agent.py` is the agent, about eighty lines of
[Strands Agents](https://strandsagents.com). `deploy.py` is the AWS CDK app that ships it. `cli.py`
is the client you run in your terminal, and `test.py` proves what the deployed harness does. There is
no container, no API Gateway, no Lambda function, and no Amazon Cognito. You call the agent with your
own AWS credentials.

## How the code reaches the runtime

<div class="figure">
<svg viewBox="0 0 912 252" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="a1-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="16.0" y="14.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">ONE COMMAND: npx aws-cdk deploy</text>
<text x="896.0" y="14.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">your machine, then AWS</text>
<rect x="16.0" y="46.0" width="135.0" height="50.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="83.5" y="68.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">agent.py</text>
<text x="83.5" y="82.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">one agent, two tools</text>
<rect x="165.0" y="46.0" width="135.0" height="50.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="232.5" y="68.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">deploy.py stage()</text>
<text x="232.5" y="82.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">uv export, uv pip install</text>
<rect x="314.0" y="46.0" width="135.0" height="50.0" rx="5" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="381.5" y="68.0" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">.build/</text>
<text x="381.5" y="82.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">arm64 wheels + agent.py</text>
<rect x="463.0" y="46.0" width="135.0" height="50.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="530.5" y="68.0" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">asset zip in S3</text>
<text x="530.5" y="82.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">cdk bootstrap bucket</text>
<rect x="612.0" y="46.0" width="135.0" height="50.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="679.5" y="68.0" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">CloudFormation</text>
<text x="679.5" y="82.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">SimpleStrandsHarness</text>
<rect x="761.0" y="46.0" width="135.0" height="50.0" rx="5" fill="#FF9900" stroke="#FF9900" stroke-width="1.2"/>
<text x="828.5" y="68.0" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="600">AgentCore Runtime</text>
<text x="828.5" y="82.0" font-size="8.5" fill="#4a3200" text-anchor="middle" font-weight="normal">simple_strands_harness</text>
<line x1="151.0" y1="71.0" x2="163.0" y2="71.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a1-d)"/>
<line x1="300.0" y1="71.0" x2="312.0" y2="71.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a1-d)"/>
<line x1="449.0" y1="71.0" x2="461.0" y2="71.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a1-d)"/>
<line x1="598.0" y1="71.0" x2="610.0" y2="71.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a1-d)"/>
<line x1="747.0" y1="71.0" x2="759.0" y2="71.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a1-d)"/>
<text x="16.0" y="112.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="700">THE TWO RESOURCES IN THE STACK</text>
<rect x="16.0" y="122.0" width="430.0" height="116.0" rx="8" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="32.0" y="142.0" font-size="10" fill="#1a1a2e" text-anchor="start" font-weight="700">AWS::IAM::Role, the execution role</text>
<text x="32.0" y="160.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">bedrock:InvokeModel on one model only</text>
<text x="32.0" y="174.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">logs:CreateLogStream, logs:PutLogEvents</text>
<text x="32.0" y="188.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">xray:PutTraceSegments, cloudwatch:PutMetricData</text>
<text x="32.0" y="202.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">bedrock-agentcore:GetWorkloadAccessToken</text>
<text x="32.0" y="216.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">s3:GetObject on the asset zip</text>
<text x="32.0" y="231.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="normal">CDK adds every line except the Bedrock one</text>
<rect x="466.0" y="122.0" width="430.0" height="116.0" rx="8" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="482.0" y="142.0" font-size="10" fill="#1a1a2e" text-anchor="start" font-weight="700">AWS::BedrockAgentCore::Runtime</text>
<text x="482.0" y="160.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">AgentRuntimeName: simple_strands_harness</text>
<text x="482.0" y="174.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">Runtime: PYTHON_3_12, EntryPoint: agent.py</text>
<text x="482.0" y="188.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">ProtocolConfiguration: HTTP</text>
<text x="482.0" y="202.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">NetworkConfiguration: PUBLIC</text>
<text x="482.0" y="216.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">inbound auth: AWS IAM SigV4</text>
<text x="482.0" y="231.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="normal">SigV4 is the runtime default, so no auth code is written</text>
</svg>
</div>

`cdk.json` runs `uv run deploy.py`, so `deploy.py` is both the build script and the CDK app. Its
`stage()` function exports the locked dependencies to `requirements.txt` and installs them into
`.build/`. The install pins `aarch64-manylinux_2_34` and Python 3.12, because the AgentCore Python
runtime is Amazon Linux 2023 on arm64. The flag `--only-binary :all:` stops uv from compiling a
package for your Mac instead. `stage()` then copies `agent.py` next to the packages, and CDK uploads
the folder as an asset zip.

Deploy is idempotent, which means it is safe to run twice. A second deploy of unchanged code reports
no differences and does nothing. A change to `agent.py` updates the same runtime in place, and the
runtime ARN stays the same. The runtime takes minutes to reach `READY`. Your code must answer `/ping`
as healthy within 120 seconds of start, or creation fails
([how the runtime works](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html)).

The stack lands in the account and the Region of the credentials that you run the deploy with,
because `deploy.py` names neither. To find it later, read the stack output:

```bash
aws cloudformation describe-stacks --stack-name SimpleStrandsHarness \
  --query 'Stacks[0].Outputs'
# RuntimeArn = arn:aws:bedrock-agentcore:<region>:<account>:runtime/simple_strands_harness-<id>
```

## How a prompt reaches the model

<div class="figure">
<svg viewBox="0 0 912 286" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="a2-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker><marker id="a2-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker></defs>
<text x="16.0" y="14.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">ONE PROMPT, ROUND TRIP</text>
<rect x="16.0" y="34.0" width="150.0" height="92.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="91.0" y="50.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">your terminal</text>
<rect x="28.0" y="58.0" width="126.0" height="28.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="91.0" y="76.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">uv run cli.py</text>
<text x="91.0" y="101.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">boto3 signs with SigV4</text>
<text x="91.0" y="114.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">keys from ~/.aws or env</text>
<rect x="198.0" y="56.0" width="96.0" height="56.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="246.0" y="79.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">IAM check</text>
<text x="246.0" y="92.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">InvokeAgent</text>
<text x="246.0" y="103.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">Runtime</text>
<rect x="326.0" y="34.0" width="380.0" height="120.0" rx="8" fill="#ffffff" stroke="#232F3E" stroke-width="1.4"/>
<text x="340.0" y="50.0" font-size="9.5" fill="#1a1a2e" text-anchor="start" font-weight="700">AgentCore Runtime: one microVM per runtimeSessionId</text>
<rect x="338.0" y="60.0" width="112.0" height="52.0" rx="5" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="394.0" y="80.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">HTTP on :8080</text>
<text x="394.0" y="93.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">/invocations</text>
<text x="394.0" y="105.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">/ping</text>
<rect x="462.0" y="60.0" width="112.0" height="52.0" rx="5" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="518.0" y="80.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">agent.py</text>
<text x="518.0" y="93.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">BedrockAgentCoreApp</text>
<text x="518.0" y="105.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">@app.entrypoint</text>
<rect x="586.0" y="60.0" width="108.0" height="52.0" rx="5" fill="#FF9900" stroke="#FF9900" stroke-width="1.2"/>
<text x="640.0" y="80.0" font-size="9.5" fill="#232F3E" text-anchor="middle" font-weight="600">Strands Agent</text>
<text x="640.0" y="93.0" font-size="8.5" fill="#4a3200" text-anchor="middle" font-weight="normal">stream_async</text>
<text x="640.0" y="105.0" font-size="8.5" fill="#4a3200" text-anchor="middle" font-weight="normal">holds the history</text>
<text x="340.0" y="145.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="normal">the microVM has its own CPU, memory and file system, and is wiped when the session stops</text>
<rect x="738.0" y="56.0" width="158.0" height="56.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="817.0" y="76.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">Amazon Bedrock</text>
<text x="817.0" y="102.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">claude-sonnet-5</text>
<line x1="166.0" y1="84.0" x2="196.0" y2="84.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a2-d)"/>
<line x1="294.0" y1="84.0" x2="324.0" y2="84.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a2-d)"/>
<line x1="450.0" y1="86.0" x2="460.0" y2="86.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a2-d)"/>
<line x1="574.0" y1="86.0" x2="584.0" y2="86.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a2-d)"/>
<line x1="706.0" y1="84.0" x2="736.0" y2="84.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a2-d)"/>
<path d="M817 114 V 172 H 91 V 130" fill="none" stroke="#FF9900" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#a2-o)"/>
<rect x="300.0" y="165.0" width="320.0" height="14.0" rx="2" fill="#ffffff" stroke="none"/>
<text x="460.0" y="175.0" font-size="8.5" fill="#9a5b00" text-anchor="middle" font-weight="600">the reply streams back as data: lines on one HTTPS connection</text>
<text x="16.0" y="202.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="700">SESSION LIFECYCLE, ONE runtimeSessionId</text>
<rect x="16.0" y="212.0" width="200.0" height="44.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="116.0" y="232.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">Active</text>
<text x="116.0" y="245.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">an invoke is in flight</text>
<rect x="248.0" y="212.0" width="200.0" height="44.0" rx="5" fill="#fffae6" stroke="#ff991f" stroke-width="1.2"/>
<text x="348.0" y="232.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">Idle</text>
<text x="348.0" y="245.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">15 minutes by default</text>
<rect x="480.0" y="212.0" width="200.0" height="44.0" rx="5" fill="#ffebe6" stroke="#de350b" stroke-width="1.2"/>
<text x="580.0" y="232.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">Stopped</text>
<text x="580.0" y="245.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">microVM ends, memory wiped</text>
<rect x="712.0" y="212.0" width="184.0" height="44.0" rx="5" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="804.0" y="232.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">next invoke</text>
<text x="804.0" y="245.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">new microVM, no history</text>
<line x1="216.0" y1="234.0" x2="246.0" y2="234.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a2-d)"/>
<line x1="448.0" y1="234.0" x2="478.0" y2="234.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a2-d)"/>
<line x1="680.0" y1="234.0" x2="710.0" y2="234.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#a2-d)"/>
<text x="16.0" y="274.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="normal">A session also stops at the maximum compute lifetime, 8 hours by default. The session id stays valid, but the conversation is gone.</text>
</svg>
</div>

`cli.py` creates a `bedrock-agentcore` client from a plain `boto3.Session`, so boto3 signs each
request with SigV4 from your normal credentials. The runtime accepts that signature because AWS IAM
is its default inbound authentication, which is why this sample has no Cognito and no token code.
Each call carries a `runtimeSessionId` of at least 33 characters. AgentCore routes every call with
the same id to the same microVM, which is a small isolated virtual machine
([sessions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-sessions.html)).

Inside the microVM, `BedrockAgentCoreApp` serves `/invocations` and `/ping` on port 8080. `agent.py`
calls `app.run(host="0.0.0.0")` on purpose, because the SDK otherwise binds `127.0.0.1`, which the
runtime cannot reach. The entrypoint is an async generator. It reads `payload["prompt"]`, and yields
each `data` event from `agent.stream_async`. The SDK frames those strings as server-sent events, and
`cli.py` prints every line that starts with `data: ` as it arrives. The runtime mounts your code
read-only, so the `remember` tool writes to the temporary directory instead.

The model is `us.anthropic.claude-sonnet-5`, named in `MODEL_ID` in `agent.py`. The `us.` prefix is a
cross-Region inference profile, so Bedrock serves the call from whichever US Region has capacity. The
execution role allows that profile, and the foundation model in every Region the profile routes to. One
Region ARN is not enough, because the second Region then fails with `AccessDeniedException`. Make sure
that your account has Bedrock access to Claude Sonnet 5 before the first invoke. To change the model,
edit `MODEL_ID` in `agent.py` and `PROFILE` in `deploy.py`, then deploy.

## Why this is a harness, not a model call

A model call takes text and returns text. This harness runs a loop around the model, and holds state
between calls. You can read that state. A payload of `{"command": "state"}` returns the state instead
of an answer. It holds the model, the tool list, the message history, the loop cycle count, the token
count, and the notes on disk. `cli.py` prints it with `/state`, and `test.py` asserts against it. This
is the real output of two prompts in one session:

```
  model    us.anthropic.claude-sonnet-5
  tools    recall, remember
  messages 8   loop cycles 4
  tokens   2943 total (2800 in, 143 out)
  notes    Code word: harness-5c0230db
   1 user      Remember this code word: harness-5c0230db
   2 assistant thinks (kept by the model)
   2 assistant calls remember({"fact": "Code word: harness-5c0230db"})
   3 user      returns saved: Code word: harness-5c0230db
   4 assistant Got it, I've saved the code word: harness-5c0230db
   5 user      What code word did I give you? Answer with the word only.
   6 assistant thinks (kept by the model)
   6 assistant calls recall({})
   7 user      returns Code word: harness-5c0230db
   8 assistant harness-5c0230db
```

Read the shape, not the words. Two prompts produced eight messages and four loop cycles, so the
harness called the model twice per prompt. Between those two calls it ran a tool and fed the result
back as a message, which is the loop a wrapper does not have. The history is a list of typed content
blocks, `text`, `reasoningContent`, `toolUse` and `toolResult`, not a transcript of strings. Messages 2
and 6 hold two blocks each, the reasoning of the model and the tool call it decided on. Every assistant
message also carries its own token usage. The counters at the top add those up, so cost and depth are
measurable per session.

The state lives in three places, and each one has a different lifetime. The message list lives in the
`Agent` object, which exists once per microVM. The notes live in a file on the microVM disk, so a fact
survives a context trim but not a session stop. The token counters live in `event_loop_metrics`. The
terminal holds none of it. `cli.py` asks the runtime every time, which is why `/history` works from a
second terminal on the same session id.

The conversation ends when the session stops, after 15 idle minutes or 8 hours of life. For history
that must outlive the session, use AgentCore Memory instead of the process and the disk.

## Where to extend it

The harness has two tools, and no Model Context Protocol server, no subagent, and no sandbox. The goal
is the shortest working path from your terminal to a deployed agent. The seams are small. Tools go in
the `Agent(tools=[...])` list in `agent.py`, and extra permissions go in the `add_to_role_policy` call
in `deploy.py`. Both ship with the next `npx aws-cdk deploy`.
