# Strands Agents: a technical overview

*What an agent harness is, and how Strands maps each concept to concrete APIs, a CLI, and framework terms.*

---

## What a harness is

A language model takes a prompt and returns text, and it takes no action. An agent harness is the program around the model: it gives the model information and a fixed set of actions, runs the actions the model picks, returns the results, and repeats until the goal is met. Users experience the harness as "the agent", so two agents on the same model behave differently when their harnesses differ.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c1-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c1-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c1-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c1-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c1-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c1-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<polygon points="0.0,18.0 111.0,18.0 121.0,32.0 111.0,46.0 0.0,46.0" fill="#FF9900"/>
<text x="55.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Plan</text>
<path d="M50.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="114.0,18.0 225.0,18.0 235.0,32.0 225.0,46.0 114.0,46.0 124.0,32.0" fill="#FF9900"/>
<text x="169.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Specify</text>
<path d="M164.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="228.0,18.0 339.0,18.0 349.0,32.0 339.0,46.0 228.0,46.0 238.0,32.0" fill="#FF9900"/>
<text x="283.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Build</text>
<path d="M278.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="342.0,18.0 453.0,18.0 463.0,32.0 453.0,46.0 342.0,46.0 352.0,32.0" fill="#FF9900"/>
<text x="397.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Test</text>
<path d="M392.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="456.0,18.0 567.0,18.0 577.0,32.0 567.0,46.0 456.0,46.0 466.0,32.0" fill="#FF9900"/>
<text x="511.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Verify</text>
<path d="M506.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#FF9900"/>
<text x="625.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Deploy</text>
<path d="M620.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#FF9900"/>
<text x="739.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Eval</text>
<path d="M734.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#FF9900"/>
<text x="853.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Operate</text>
<path d="M848.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c1-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M183.0 115.0 L292 64 L292 252 L183.0 205.0 Z" fill="#FF9900" opacity="0.10"/>
<line x1="183.0" y1="115.0" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="183.0" y1="205.0" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#FF9900"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#232F3E" text-anchor="middle" font-weight="700">Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#232F3E" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">Three layers in every harness</text>
<text x="386.0" y="106.0" font-size="8" fill="#0052CC" text-anchor="middle" font-weight="700">DATA AND API: DETERMINISTIC</text>
<rect x="316.0" y="114.0" width="140.0" height="28.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="386.0" y="131.4" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">Internal services</text>
<rect x="316.0" y="148.0" width="140.0" height="28.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="386.0" y="165.4" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">Third-party APIs</text>
<rect x="316.0" y="182.0" width="140.0" height="28.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="386.0" y="199.4" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">MCP servers</text>
<text x="590.0" y="106.0" font-size="8" fill="#9a5b00" text-anchor="middle" font-weight="700">MODEL: PROBABILISTIC</text>
<rect x="520.0" y="136.0" width="140.0" height="56.0" rx="5" fill="#FF9900" stroke="#FF9900" stroke-width="1.2"/>
<text x="590.0" y="162.5" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="600">Model layer</text>
<text x="590.0" y="174.0" font-size="8.5" fill="#4a3200" text-anchor="middle" font-weight="normal">model, prompts, inference</text>
<text x="750.0" y="106.0" font-size="8" fill="#1e7e34" text-anchor="middle" font-weight="700">VERIFICATION: MIXED</text>
<rect x="692.0" y="136.0" width="116.0" height="56.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="750.0" y="162.5" font-size="10" fill="#1e7e34" text-anchor="middle" font-weight="600">Verification</text>
<text x="750.0" y="174.0" font-size="8.5" fill="#1e7e34" text-anchor="middle" font-weight="normal">evals, handoff checks</text>
<rect x="836.0" y="136.0" width="60.0" height="56.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="866.0" y="162.5" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">Output</text>
<text x="866.0" y="174.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">the world</text>
<line x1="518.0" y1="146.0" x2="459.0" y2="128.0" stroke="#0052CC" stroke-width="1.4" marker-end="url(#c1-b)"/>
<text x="486.0" y="128.0" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="normal">tool calls</text>
<line x1="459.0" y1="163.0" x2="518.0" y2="166.0" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c1-g)"/>
<line x1="459.0" y1="196.0" x2="518.0" y2="182.0" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c1-g)"/>
<text x="488.0" y="206.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">results</text>
<line x1="662.5" y1="164.0" x2="689.5" y2="164.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c1-d)"/>
<line x1="810.5" y1="164.0" x2="833.5" y2="164.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c1-gr)"/>
<path d="M750 194 C750 236 590 236 590 196" fill="none" stroke="#de350b" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#c1-r)"/>
<text x="670.0" y="244.0" font-size="9" fill="#de350b" text-anchor="middle" font-weight="normal">reject and retry</text>
</svg>
</div>

The top strip is the lifecycle of an agent, from Plan to Operate, and the dashed arc returns production feedback to planning. The wheel shows the concerns a harness adds around the core loop of the model. The right panel shows the three layers of every harness: model output passes through verification before it reaches the world, and a rejected result goes back for a retry. [Building Effective Agent Harnesses](building-effective-harnesses.md) covers each segment without reference to a framework.

| Layer | What it holds | Nature |
| --- | --- | --- |
| Model | The model, the prompts, the inference pattern | Probabilistic |
| Data and API | Internal services, third-party APIs, MCP servers | Deterministic |
| Verification | Evaluation, structured handoffs, rules for unverified data | Mixed |

Each layer fails differently. Ordinary software tests cover the data and API layer. Most teams skip the verification layer, so a small error in step two becomes a confident wrong answer in step nine. The amount of harness a task needs depends on how easily you can check its output: code has a built-in pass or fail signal, so its harness can stay light, and a task without that signal needs more verification, more structure, and more human checkpoints.

---

## How Strands builds a harness

Strands Agents is an open-source SDK for Python and TypeScript that implements each segment of the wheel. It is model-driven: you give an agent a model, tools, and a prompt, the model decides how to reach the goal, and the SDK runs the loop. Amazon Q Developer and AWS Glue use it in production, and version 1.0 shipped in July 2025. Strands works at two levels. The SDK gives each concern as a primitive that you connect, and the Strands Harness connects them for you: one `create_harness()` call returns an agent with a shell, file tools, web access, memory, prompt caching, and context management. The smallest SDK program below gets a default Amazon Bedrock model and context management, but no prompt caching, because caching is on by default only in `create_harness()`.

```python
from strands import Agent

agent = Agent()
agent("Summarize the last three AWS re:Invent keynotes.")
```

<div class="figure">
<table style="width:auto;max-width:560px;margin:0 auto;border-collapse:collapse;font-size:8.5pt;line-height:1.35">
<tr style="background:#232F3E;color:#ffffff"><th style="padding:4px 10px;text-align:left">Harness concept</th><th style="padding:4px 10px;text-align:left">Strands API, CLI, or term</th></tr>
<tr style="background:#f8f9fb"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Core loop</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6"><code>Agent()</code>, <code>agent(...)</code>, <code>stream_async</code></td></tr>
<tr style="background:#ffffff"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Model</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6"><code>BedrockModel</code>, <code>OpenAIModel</code>, 20+ providers</td></tr>
<tr style="background:#f8f9fb"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Tools</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6"><code>@tool</code>, <code>strands.vended_tools</code>, MCP client</td></tr>
<tr style="background:#ffffff"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Context</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6">sliding-window, summarizing, or null manager</td></tr>
<tr style="background:#f8f9fb"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Caching</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6"><code>CacheConfig(strategy="auto")</code>, harness <code>caching="auto"</code></td></tr>
<tr style="background:#ffffff"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Memory and state</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6">agent state, <code>FileSessionManager</code>, harness memory</td></tr>
<tr style="background:#f8f9fb"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Bounds</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6"><code>Limits</code>, <code>interventions</code></td></tr>
<tr style="background:#ffffff"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Orchestration</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6">agents as tools, <code>Swarm</code>, <code>GraphBuilder</code>, A2A</td></tr>
<tr style="background:#f8f9fb"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Sandbox</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6"><code>DockerSandbox</code>, Strands Box, AgentCore microVM</td></tr>
<tr style="background:#ffffff"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Evals</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6"><code>strands-evals validate</code>, <code>run --fail-on</code></td></tr>
<tr style="background:#f8f9fb"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Guardrails</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6">hooks, steering, Agent Control, AgentCore Policy</td></tr>
<tr style="background:#ffffff"><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6;background:#fff3e0;color:#9a5b00;font-weight:700;white-space:nowrap">Observability</td><td style="padding:3px 10px;border-bottom:1px solid #dfe1e6">OpenTelemetry export, <code>EventLoopMetrics</code></td></tr>
</table>
</div>

The figure below places the same components on the eight phases of the lifecycle from the first figure. Secure is not a phase: its controls run under every phase, so it spans the whole line.

<div class="figure">
<svg viewBox="0 0 922 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="top-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker></defs>
<polygon points="0,34 111,34 121,48 111,62 0,62" fill="#FF9900"/>
<text x="55.5" y="51.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Plan</text>
<rect x="0" y="72" width="111" height="104" rx="6" fill="#f8f9fb" stroke="#dfe1e6"/>
<rect x="5" y="79" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="55.5" y="91.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">create_harness planner</text>
<rect x="5" y="103" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="55.5" y="115.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">read-only built-ins</text>
<rect x="5" y="127" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="55.5" y="139.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">Agent SOPs</text>
<rect x="5" y="151" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="55.5" y="163.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">Agent Skills</text>
<polygon points="114,34 225,34 235,48 225,62 114,62 124,48" fill="#FF9900"/>
<text x="169.5" y="51.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Specify</text>
<rect x="114" y="72" width="111" height="104" rx="6" fill="#f8f9fb" stroke="#dfe1e6"/>
<rect x="119" y="79" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="169.5" y="91.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">structured output</text>
<rect x="119" y="103" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="169.5" y="115.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">Pydantic contracts</text>
<rect x="119" y="127" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="169.5" y="139.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">instructions=</text>
<rect x="119" y="151" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="169.5" y="163.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">eval cases (JSON)</text>
<polygon points="228,34 339,34 349,48 339,62 228,62 238,48" fill="#FF9900"/>
<text x="283.5" y="51.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Build</text>
<rect x="228" y="72" width="111" height="104" rx="6" fill="#f8f9fb" stroke="#dfe1e6"/>
<rect x="233" y="79" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="283.5" y="91.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">Agent() &#183; @tool</text>
<rect x="233" y="103" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="283.5" y="115.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">MCP &#183; vended tools</text>
<rect x="233" y="127" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="283.5" y="139.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">20+ model providers</text>
<rect x="233" y="151" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="283.5" y="163.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">Swarm &#183; Graph &#183; A2A</text>
<polygon points="342,34 453,34 463,48 453,62 342,62 352,48" fill="#FF9900"/>
<text x="397.5" y="51.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Test</text>
<rect x="342" y="72" width="111" height="104" rx="6" fill="#f8f9fb" stroke="#dfe1e6"/>
<rect x="347" y="79" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="397.5" y="91.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">DockerSandbox</text>
<rect x="347" y="103" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="397.5" y="115.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">Strands Box (local)</text>
<rect x="347" y="127" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="397.5" y="139.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">evals validate</text>
<rect x="347" y="151" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="397.5" y="163.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">stream_async view</text>
<polygon points="456,34 567,34 577,48 567,62 456,62 466,48" fill="#FF9900"/>
<text x="511.5" y="51.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Verify</text>
<rect x="456" y="72" width="111" height="104" rx="6" fill="#f8f9fb" stroke="#dfe1e6"/>
<rect x="461" y="79" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="511.5" y="91.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">run --fail-on 0.85</text>
<rect x="461" y="103" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="511.5" y="115.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">score threshold</text>
<rect x="461" y="127" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="511.5" y="139.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">steering feedback</text>
<rect x="461" y="151" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="511.5" y="163.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">interventions</text>
<polygon points="570,34 681,34 691,48 681,62 570,62 580,48" fill="#FF9900"/>
<text x="625.5" y="51.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Deploy</text>
<rect x="570" y="72" width="111" height="104" rx="6" fill="#f8f9fb" stroke="#dfe1e6"/>
<rect x="575" y="79" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="625.5" y="91.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">BedrockAgentCoreApp</text>
<rect x="575" y="103" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="625.5" y="115.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">agentcore deploy</text>
<rect x="575" y="127" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="625.5" y="139.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">microVM per session</text>
<rect x="575" y="151" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="625.5" y="163.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">SigV4 or JWT</text>
<polygon points="684,34 795,34 805,48 795,62 684,62 694,48" fill="#FF9900"/>
<text x="739.5" y="51.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Eval</text>
<rect x="684" y="72" width="111" height="104" rx="6" fill="#f8f9fb" stroke="#dfe1e6"/>
<rect x="689" y="79" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="739.5" y="91.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">strands-evals run</text>
<rect x="689" y="103" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="739.5" y="115.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">OpenTelemetry traces</text>
<rect x="689" y="127" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="739.5" y="139.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">regression report</text>
<rect x="689" y="151" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="739.5" y="163.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">failure &#8594; new case</text>
<polygon points="798,34 909,34 919,48 909,62 798,62 808,48" fill="#FF9900"/>
<text x="853.5" y="51.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Operate</text>
<rect x="798" y="72" width="111" height="104" rx="6" fill="#f8f9fb" stroke="#dfe1e6"/>
<rect x="803" y="79" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="853.5" y="91.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">SessionManager</text>
<rect x="803" y="103" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="853.5" y="115.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">EventLoopMetrics</text>
<rect x="803" y="127" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="853.5" y="139.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">Limits (budget caps)</text>
<rect x="803" y="151" width="101" height="19" rx="4" fill="#e6f0ff" stroke="#b3d4ff"/>
<text x="853.5" y="163.6" font-size="7.6" fill="#1a1a2e" text-anchor="middle">context manager</text>
<path d="M853.5 33 C853.5 13 55.5 13 55.5 33" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#top-g)"/>
<rect x="338" y="8" width="236" height="12" rx="2" fill="#ffffff"/>
<text x="456" y="17" font-size="9" fill="#6b7a90" text-anchor="middle">production feedback returns to planning</text>
<rect x="0" y="188" width="919" height="62" rx="6" fill="#232F3E"/>
<text x="12" y="206" font-size="8.5" fill="#FF9900" font-weight="700">SECURE: RUNS UNDER EVERY PHASE</text>
<rect x="12" y="216" width="175" height="22" rx="4" fill="#3d5068"/>
<text x="99.5" y="230.5" font-size="8.5" fill="#e0e6ed" text-anchor="middle">hooks</text>
<rect x="192" y="216" width="175" height="22" rx="4" fill="#3d5068"/>
<text x="279.5" y="230.5" font-size="8.5" fill="#e0e6ed" text-anchor="middle">Agent Control deny rules</text>
<rect x="372" y="216" width="175" height="22" rx="4" fill="#3d5068"/>
<text x="459.5" y="230.5" font-size="8.5" fill="#e0e6ed" text-anchor="middle">AgentCore Policy at the gateway</text>
<rect x="552" y="216" width="175" height="22" rx="4" fill="#3d5068"/>
<text x="639.5" y="230.5" font-size="8.5" fill="#e0e6ed" text-anchor="middle">Strands Box with Dogwood policy</text>
<rect x="732" y="216" width="175" height="22" rx="4" fill="#3d5068"/>
<text x="819.5" y="230.5" font-size="8.5" fill="#e0e6ed" text-anchor="middle">IAM roles, SigV4 signing</text>
</svg>
</div>

---

## The agent loop

Each call to an agent runs one or more cycles of the agent loop. A cycle sends the conversation to the model, receives a final answer or a request for tools, runs the tools, and adds the results to the conversation, and the loop starts another cycle until the model returns an answer, so one user turn can drive many rounds of model and tools. The loop also handles errors, records metrics for each cycle, enforces per-invocation budget caps so that a runaway agent stops, and raises an overflow error when the input grows past the context window. It is asynchronous, so independent tool calls and whole agents can run at the same time, and you can watch it as a stream of typed events (text, tool calls, reasoning) instead of waiting for one final string.

<div class="figure">
<svg viewBox="0 0 912 252" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="l1-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker><marker id="l1-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="l1-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker></defs>
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">ONE CYCLE OF THE AGENT LOOP</text>
<rect x="0" y="30" width="150" height="48" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/><text x="75" y="50" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">conversation</text><text x="75" y="63" font-size="8.5" fill="#c9d2de" text-anchor="middle">messages + prompt</text>
<rect x="222" y="30" width="150" height="48" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/><text x="297" y="50" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">model</text><text x="297" y="63" font-size="8.5" fill="#44546f" text-anchor="middle">answer or tool call</text>
<rect x="444" y="30" width="150" height="48" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/><text x="519" y="50" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">tools</text><text x="519" y="63" font-size="8.5" fill="#44546f" text-anchor="middle">run in parallel, async</text>
<rect x="666" y="30" width="150" height="48" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/><text x="741" y="50" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">results appended</text><text x="741" y="63" font-size="8.5" fill="#c9d2de" text-anchor="middle">back to conversation</text>
<line x1="150" y1="54" x2="219" y2="54" stroke="#232F3E" stroke-width="1.4" marker-end="url(#l1-d)"/>
<line x1="372" y1="54" x2="441" y2="54" stroke="#0052CC" stroke-width="1.4" marker-end="url(#l1-b)"/>
<line x1="594" y1="54" x2="663" y2="54" stroke="#0052CC" stroke-width="1.4" marker-end="url(#l1-b)"/>
<path d="M741 80 V110 H75 V80" fill="none" stroke="#FF9900" stroke-width="1.6" stroke-dasharray="4 3" marker-end="url(#l1-o)"/>
<rect x="320" y="101" width="176" height="16" rx="8" fill="#ffffff"/><text x="408" y="113" font-size="8.5" fill="#9a5b00" text-anchor="middle" font-weight="700">recurse while the model asks for tools</text>
<rect x="0" y="140" width="912" height="100" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="16" y="160" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">THE LOOP ALSO OWNS</text>
<text x="16" y="182" font-size="10" fill="#1a1a2e" text-anchor="start">Error handling and recovery &#183; per-invocation budget caps &#183; metrics on every cycle &#183; context-overflow detection.</text>
<text x="16" y="202" font-size="10" fill="#1a1a2e" text-anchor="start">The model decides when to stop by returning a final answer instead of a tool call. You supply the model, the</text>
<text x="16" y="218" font-size="10" fill="#1a1a2e" text-anchor="start">tools, and the prompt. You do not write the control flow. Every event is streamed as it happens.</text>
</svg>
</div>

---

## Models: provider-agnostic by design

Every model reaches the agent through one `Model` interface, so the same agent code runs on any supported provider and each agent in a system can use a different model. More than 20 providers ship with the SDK, including Amazon Bedrock, Amazon Nova, Anthropic, OpenAI (Chat and Responses APIs), Google, Mistral, Writer, SageMaker, Ollama, llama.cpp, and LiteLLM, a gateway to many more. Community packages add NVIDIA NIM, vLLM, xAI, and others, and you can add your own provider by implementing the streaming method of `Model`. Streaming, tool calling, and structured output work the same on every first-party provider. Prompt caching varies: Amazon Bedrock, Anthropic, LiteLLM, and llama.cpp write cache points, and OpenAI and Google cache automatically on the server side.

<div class="figure">
<svg viewBox="0 0 912 250" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="m1-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker></defs>
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">ONE Model INTERFACE, MANY PROVIDERS &#8212; SWAP THE MODEL, KEEP THE AGENT</text>
<rect x="356" y="30" width="200" height="40" rx="5" fill="#232F3E"/><text x="456" y="50" font-size="10" fill="#fff" text-anchor="middle" font-weight="600">your agent code</text><text x="456" y="63" font-size="8.5" fill="#c9d2de" text-anchor="middle">tools and logic unchanged</text>
<rect x="356" y="86" width="200" height="26" rx="5" fill="#FF9900"/><text x="456" y="103" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">Model interface</text>
<line x1="456" y1="70" x2="456" y2="84" stroke="#232F3E" stroke-width="1.4"/>
<rect x="20" y="150" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="85" y="166" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Amazon Bedrock</text>
<rect x="160" y="150" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="225" y="166" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Anthropic</text>
<rect x="300" y="150" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="365" y="166" font-size="8.5" fill="#1a1a2e" text-anchor="middle">OpenAI / Responses</text>
<rect x="440" y="150" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="505" y="166" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Google</text>
<rect x="580" y="150" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="645" y="166" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Mistral &#183; Writer</text>
<rect x="720" y="150" width="172" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="806" y="166" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Ollama &#183; llama.cpp (local)</text>
<rect x="20" y="182" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="85" y="198" font-size="8.5" fill="#1a1a2e" text-anchor="middle">SageMaker</text>
<rect x="160" y="182" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="225" y="198" font-size="8.5" fill="#1a1a2e" text-anchor="middle">LiteLLM (gateway)</text>
<rect x="300" y="182" width="130" height="24" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="365" y="198" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Amazon Nova</text>
<rect x="440" y="182" width="130" height="24" rx="5" fill="#fffae6" stroke="#f5c56b"/><text x="505" y="198" font-size="8.5" fill="#1a1a2e" text-anchor="middle">NVIDIA NIM, vLLM, xAI</text>
<rect x="580" y="182" width="130" height="24" rx="5" fill="#fffae6" stroke="#f5c56b"/><text x="645" y="198" font-size="8.5" fill="#1a1a2e" text-anchor="middle">+ community set</text>
<rect x="720" y="182" width="172" height="24" rx="5" fill="#f8f9fb" stroke="#dfe1e6" stroke-dasharray="4 3"/><text x="806" y="198" font-size="8.5" fill="#44546f" text-anchor="middle">custom (implement Model)</text>
<line x1="456" y1="112" x2="456" y2="134" stroke="#0052CC" stroke-width="1.4"/><line x1="90" y1="134" x2="822" y2="134" stroke="#8a96a8" stroke-width="1"/>
<line x1="90" y1="134" x2="85" y2="148" stroke="#0052CC" stroke-width="1" marker-end="url(#m1-b)"/><line x1="456" y1="134" x2="456" y2="148" stroke="#0052CC" stroke-width="1" marker-end="url(#m1-b)"/><line x1="822" y1="134" x2="806" y2="148" stroke="#0052CC" stroke-width="1" marker-end="url(#m1-b)"/>
<text x="20" y="228" font-size="8" fill="#6b7a90" font-weight="700">SOLID = first-party</text><text x="200" y="228" font-size="8" fill="#9a5b00" font-weight="700">AMBER = community</text><text x="390" y="228" font-size="8" fill="#6b7a90" font-weight="700">DASHED = write your own</text>
<text x="640" y="228" font-size="9" fill="#44546f">Streaming, tool calling, structured output: same on every first-party provider.</text>
</svg>
</div>

To switch providers, construct a different model class and pass it to the agent.

```python
from strands import Agent
from strands.models import BedrockModel
from strands.models.openai import OpenAIModel

bedrock = BedrockModel(model_id="us.amazon.nova-pro-v1:0", temperature=0.3, region_name="us-west-2")
openai = OpenAIModel(client_args={"api_key": "..."}, model_id="gpt-4o", params={"temperature": 0.7})

researcher = Agent(name="researcher", model=bedrock, tools=[web_fetch])
writer = Agent(name="writer", model=openai, tools=[document_formatter])
```

| Provider | Streaming | Tool calling | Structured output | Prompt caching |
| --- | --- | --- | --- | --- |
| Amazon Bedrock, Anthropic, LiteLLM, llama.cpp | yes | yes | yes | yes |
| OpenAI / Responses, Google | yes | yes | yes | automatic |
| Ollama, Mistral, Writer, SageMaker, Llama API | yes | yes | yes | no |
| Custom provider | yes | depends | depends | depends |

---

## Tools: how the model acts

A tool is a function that the model can call, and Strands accepts tools from four sources. Your own functions become tools with `@tool`: the SDK turns the typed signature and the docstring into the schema the model reads. The SDK vends ready tools in `strands.vended_tools`, among them `shell`, `file_editor`, `http_request`, `web_fetch`, `notebook`, and `handoff_to_user`, and the harness adds built-ins such as `web_search`. A Model Context Protocol (MCP) server, local or remote, adds its tools with no glue code, and other agents can be tools too, as the multi-agent section shows. The model decides when to call a tool and with which arguments, so you bound those choices with guardrails instead of scripting them.

<div class="figure">
<svg viewBox="0 0 912 220" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="t1-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker></defs>
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">FOUR WAYS TO GIVE AN AGENT TOOLS &#8212; THE MODEL CHOOSES WHEN TO CALL EACH</text>
<rect x="356" y="90" width="200" height="40" rx="5" fill="#FF9900"/><text x="456" y="110" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">the agent</text><text x="456" y="123" font-size="8.5" fill="#4a3200" text-anchor="middle">model picks a tool each cycle</text>
<rect x="20" y="40" width="190" height="48" rx="6" fill="#e6f0ff" stroke="#b3d4ff"/><text x="115" y="60" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">1. Your functions</text><text x="115" y="75" font-size="8.5" fill="#44546f" text-anchor="middle">@tool + docstring &#8594; schema</text>
<rect x="20" y="132" width="190" height="48" rx="6" fill="#e6f0ff" stroke="#b3d4ff"/><text x="115" y="152" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">2. Vended tools</text><text x="115" y="167" font-size="8.5" fill="#44546f" text-anchor="middle">shell, file_editor, web_fetch</text>
<rect x="702" y="40" width="190" height="48" rx="6" fill="#e6f0ff" stroke="#b3d4ff"/><text x="797" y="60" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">3. MCP servers</text><text x="797" y="75" font-size="8.5" fill="#44546f" text-anchor="middle">any server, local or remote</text>
<rect x="702" y="132" width="190" height="48" rx="6" fill="#232F3E"/><text x="797" y="152" font-size="9.5" fill="#fff" text-anchor="middle" font-weight="600">4. Other agents</text><text x="797" y="167" font-size="8.5" fill="#c9d2de" text-anchor="middle">a specialist wrapped as a tool</text>
<line x1="210" y1="64" x2="354" y2="104" stroke="#0052CC" stroke-width="1.4" marker-end="url(#t1-b)"/>
<line x1="210" y1="156" x2="354" y2="116" stroke="#0052CC" stroke-width="1.4" marker-end="url(#t1-b)"/>
<line x1="702" y1="64" x2="558" y2="104" stroke="#0052CC" stroke-width="1.4" marker-end="url(#t1-b)"/>
<line x1="702" y1="156" x2="558" y2="116" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#t1-b)"/>
<text x="456" y="165" font-size="8.5" fill="#44546f" text-anchor="middle">no glue code: every source</text><text x="456" y="178" font-size="8.5" fill="#44546f" text-anchor="middle">appears as one tool list</text>
</svg>
</div>

```python
from strands import Agent, tool
from strands.vended_tools import shell, file_editor

@tool
def ticket_status(ticket_id: str) -> str:
    """Return the current status of a support ticket by its ID."""
    return lookup(ticket_id)

agent = Agent(tools=[ticket_status, shell, file_editor])
```

---

## Context, state, and memory

An agent keeps three kinds of state. A conversation manager keeps the message list inside the context window, agent state holds structured data that tools read and write without spending context tokens, and a `SessionManager` persists both and restores them after a restart. The Strands Harness also turns on long-term memory by default and stores it under `./.agent/memory`.

<div class="figure">
<svg viewBox="0 0 912 250" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="ctx-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker></defs>
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">THREE KINDS OF STATE, AND WHAT KEEPS EACH IN BOUNDS</text>
<rect x="0" y="28" width="288" height="150" rx="8" fill="#f8f9fb" stroke="#dfe1e6"/>
<text x="144" y="48" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">Conversation</text>
<text x="144" y="64" font-size="8.5" fill="#44546f" text-anchor="middle">the running message list</text>
<rect x="24" y="78" width="240" height="22" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="144" y="93" font-size="8.5" fill="#1a1a2e" text-anchor="middle">sliding window: keep recent, drop old</text>
<rect x="24" y="106" width="240" height="22" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="144" y="121" font-size="8.5" fill="#1a1a2e" text-anchor="middle">summarizing: replace old with a summary</text>
<rect x="24" y="134" width="240" height="22" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="144" y="149" font-size="8.5" fill="#1a1a2e" text-anchor="middle">null: leave it untouched</text>
<text x="144" y="170" font-size="8" fill="#6b7a90" text-anchor="middle">managed so it never overflows the window</text>
<rect x="312" y="28" width="288" height="150" rx="8" fill="#f8f9fb" stroke="#dfe1e6"/>
<text x="456" y="48" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">Agent state</text>
<text x="456" y="64" font-size="8.5" fill="#44546f" text-anchor="middle">structured data outside the chat</text>
<rect x="336" y="82" width="240" height="26" rx="5" fill="#232F3E"/><text x="456" y="99" font-size="8.5" fill="#fff" text-anchor="middle">work item id, user profile, counters</text>
<text x="456" y="128" font-size="8.5" fill="#44546f" text-anchor="middle">tools read and write it</text>
<text x="456" y="144" font-size="8.5" fill="#44546f" text-anchor="middle">costs no context tokens</text>
<rect x="624" y="28" width="288" height="150" rx="8" fill="#232F3E"/>
<text x="768" y="48" font-size="10" fill="#FF9900" text-anchor="middle" font-weight="700">Sessions (durable)</text>
<text x="768" y="64" font-size="8.5" fill="#c9d2de" text-anchor="middle">persist both, restore after a restart</text>
<rect x="648" y="82" width="110" height="26" rx="5" fill="#3d5068"/><text x="703" y="99" font-size="8.5" fill="#e0e6ed" text-anchor="middle">filesystem</text>
<rect x="766" y="82" width="122" height="26" rx="5" fill="#3d5068"/><text x="827" y="99" font-size="8.5" fill="#e0e6ed" text-anchor="middle">Amazon S3</text>
<rect x="648" y="116" width="240" height="26" rx="5" fill="#3d5068"/><text x="768" y="133" font-size="8.5" fill="#e0e6ed" text-anchor="middle">your own backend (DAO pattern)</text>
<text x="768" y="162" font-size="8" fill="#c9d2de" text-anchor="middle">give it a session id; persistence is automatic</text>
<text x="456" y="206" font-size="9.5" fill="#44546f" text-anchor="middle">Conversation and agent state are per-run working memory. A session is the datastore that lets a run survive a</text>
<text x="456" y="222" font-size="9.5" fill="#44546f" text-anchor="middle">crash, a restart, or a scaling event and resume exactly where it left off.</text>
</svg>
</div>

```python
from strands import Agent
from strands.session.file_session_manager import FileSessionManager

session = FileSessionManager(session_id="customer_support", base_dir="./sessions")
agent = Agent(id="support_bot_1", session_manager=session, tools=[knowledge_base])

agent("Help me reset my password.")        # saved as the turn completes
# ...after a restart, a new manager with the same id restores the whole history
```

## Structured output and streaming

Structured output makes the model return a typed object, such as a Pydantic model, so that another program can use the result without parsing prose. Streaming sends output as it is produced: `stream_async` yields events that you forward to a UI, with cancellation when the user leaves.

```python
async for event in agent.stream_async("Draft the release notes."):
    if "data" in event:
        print(event["data"], end="")
    elif "current_tool_use" in event:
        print(f"[calling {event['current_tool_use']['name']}]")
```

---

## Many agents working together

Strands has four multi-agent patterns. With agents as tools, an orchestrator keeps control and calls specialists wrapped in `@tool`. A swarm is a team that coordinates through shared memory with no fixed order. A graph runs nodes and conditional edges, for a process that needs the same steps every time. The Agent-to-Agent protocol (A2A) connects agents across organizations through a published agent card.

<div class="figure">
<svg viewBox="0 0 912 210" xmlns="http://www.w3.org/2000/svg" role="img">
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">FOUR PATTERNS, ONE BUILDING BLOCK: THE PLAIN AGENT</text>
<rect x="0" y="28" width="216" height="150" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="108" y="48" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">Agents as tools</text>
<rect x="63" y="60" width="90" height="26" rx="5" fill="#232F3E"/><text x="108" y="77" font-size="9" fill="#fff" text-anchor="middle">orchestrator</text>
<rect x="18" y="104" width="78" height="22" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="57" y="119" font-size="8.5" fill="#1a1a2e" text-anchor="middle">specialist</text>
<rect x="120" y="104" width="78" height="22" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="159" y="119" font-size="8.5" fill="#1a1a2e" text-anchor="middle">specialist</text>
<line x1="90" y1="86" x2="57" y2="104" stroke="#8a96a8" stroke-width="1.2"/><line x1="126" y1="86" x2="159" y2="104" stroke="#8a96a8" stroke-width="1.2"/>
<text x="108" y="152" font-size="8.5" fill="#44546f" text-anchor="middle">manager keeps control,</text><text x="108" y="166" font-size="8.5" fill="#44546f" text-anchor="middle">consults experts</text>
<rect x="232" y="28" width="216" height="150" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="340" y="48" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">Swarm</text>
<rect x="268" y="66" width="68" height="22" rx="5" fill="#232F3E"/><text x="302" y="81" font-size="8.5" fill="#fff" text-anchor="middle">agent</text>
<rect x="356" y="66" width="68" height="22" rx="5" fill="#232F3E"/><text x="390" y="81" font-size="8.5" fill="#fff" text-anchor="middle">agent</text>
<rect x="312" y="104" width="68" height="22" rx="5" fill="#232F3E"/><text x="346" y="119" font-size="8.5" fill="#fff" text-anchor="middle">agent</text>
<line x1="302" y1="88" x2="346" y2="104" stroke="#FF9900" stroke-width="1.2" stroke-dasharray="3 2"/><line x1="390" y1="88" x2="346" y2="104" stroke="#FF9900" stroke-width="1.2" stroke-dasharray="3 2"/><line x1="336" y1="77" x2="356" y2="77" stroke="#FF9900" stroke-width="1.2" stroke-dasharray="3 2"/>
<text x="340" y="152" font-size="8.5" fill="#44546f" text-anchor="middle">shared memory,</text><text x="340" y="166" font-size="8.5" fill="#44546f" text-anchor="middle">self-organizing</text>
<rect x="464" y="28" width="216" height="150" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="572" y="48" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">Graph</text>
<rect x="494" y="64" width="64" height="22" rx="5" fill="#FF9900"/><text x="526" y="79" font-size="8.5" fill="#1a1a2e" text-anchor="middle">analyze</text>
<rect x="494" y="104" width="64" height="22" rx="5" fill="#FF9900"/><text x="526" y="119" font-size="8.5" fill="#1a1a2e" text-anchor="middle">normal</text>
<rect x="586" y="104" width="64" height="22" rx="5" fill="#FF9900"/><text x="618" y="119" font-size="8.5" fill="#1a1a2e" text-anchor="middle">critical</text>
<line x1="526" y1="86" x2="526" y2="104" stroke="#232F3E" stroke-width="1.2"/><line x1="558" y1="80" x2="586" y2="104" stroke="#232F3E" stroke-width="1.2"/>
<text x="572" y="152" font-size="8.5" fill="#44546f" text-anchor="middle">fixed order,</text><text x="572" y="166" font-size="8.5" fill="#44546f" text-anchor="middle">conditional routing</text>
<rect x="696" y="28" width="216" height="150" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="804" y="48" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">A2A protocol</text>
<rect x="716" y="70" width="80" height="26" rx="5" fill="#232F3E"/><text x="756" y="87" font-size="8.5" fill="#fff" text-anchor="middle">your agent</text>
<rect x="818" y="70" width="80" height="26" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="858" y="87" font-size="8.5" fill="#1a1a2e" text-anchor="middle">partner</text>
<line x1="796" y1="83" x2="818" y2="83" stroke="#0052CC" stroke-width="1.4"/>
<text x="804" y="128" font-size="8.5" fill="#44546f" text-anchor="middle">agent card describes</text><text x="804" y="142" font-size="8.5" fill="#44546f" text-anchor="middle">capabilities; cross-org</text>
<text x="804" y="166" font-size="8.5" fill="#44546f" text-anchor="middle">discovery</text>
<text x="0" y="200" font-size="9" fill="#6b7a90" text-anchor="start">Patterns nest: a swarm can hold a graph, a graph can hold a swarm, and any agent can carry other agents as tools.</text>
</svg>
</div>

```python
from strands import Agent
from strands.multiagent import Swarm, GraphBuilder

team = Swarm([researcher, analyst, writer])          # self-organizing
team("Write a comprehensive report on the history of AI since 1950.")

builder = GraphBuilder()                             # deterministic
builder.add_node(analyzer, "analyze")
builder.add_node(normal, "normal"); builder.add_node(critical, "critical")
builder.add_edge("analyze", "normal", condition=is_routine)
builder.add_edge("analyze", "critical", condition=is_urgent)
builder.set_entry_point("analyze")
builder.build()("I need help with my order.")
```

---

## Guardrails: bounding a model that drives

The model picks the actions, so you cannot write a rule for every case in advance. Strands enforces control at runtime in the five layers below, from steering, which sends feedback so the model retries, to deny rules, which block the step. Agent Control is an open-source runtime control plane, and AgentCore Policy is the AWS service that enforces access control at the tool gateway.

<div class="figure">
<svg viewBox="0 0 912 210" xmlns="http://www.w3.org/2000/svg" role="img">
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">LAYERS OF RUNTIME CONTROL &#8212; SOFT NUDGE ON THE LEFT, HARD STOP ON THE RIGHT</text>
<defs><linearGradient id="g-grad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1e7e34"/><stop offset="1" stop-color="#de350b"/></linearGradient></defs>
<rect x="0" y="30" width="912" height="6" rx="3" fill="url(#g-grad)"/>
<text x="0" y="52" font-size="8" fill="#1e7e34" font-weight="700">GUIDE THE MODEL</text><text x="912" y="52" font-size="8" fill="#de350b" font-weight="700" text-anchor="end">BLOCK THE ACTION</text>
<rect x="0" y="64" width="172" height="110" rx="8" fill="#f8f9fb" stroke="#dfe1e6"/>
<text x="86" y="84" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">Steering</text>
<text x="86" y="104" font-size="8.5" fill="#44546f" text-anchor="middle">evaluate a response,</text><text x="86" y="117" font-size="8.5" fill="#44546f" text-anchor="middle">feed correction,</text><text x="86" y="130" font-size="8.5" fill="#44546f" text-anchor="middle">let it retry</text>
<text x="86" y="158" font-size="8" fill="#6b7a90" text-anchor="middle">stays in the lines</text>
<rect x="185" y="64" width="172" height="110" rx="8" fill="#f8f9fb" stroke="#dfe1e6"/>
<text x="271" y="84" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">Hooks</text>
<text x="271" y="104" font-size="8.5" fill="#44546f" text-anchor="middle">subscribe to loop</text><text x="271" y="117" font-size="8.5" fill="#44546f" text-anchor="middle">lifecycle events;</text><text x="271" y="130" font-size="8.5" fill="#44546f" text-anchor="middle">observe or alter</text>
<text x="271" y="158" font-size="8" fill="#6b7a90" text-anchor="middle">no core code change</text>
<rect x="370" y="64" width="172" height="110" rx="8" fill="#fffae6" stroke="#f5c56b"/>
<text x="456" y="84" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">Interventions</text>
<text x="456" y="104" font-size="8.5" fill="#44546f" text-anchor="middle">pause before a risky</text><text x="456" y="117" font-size="8.5" fill="#44546f" text-anchor="middle">call (push, publish),</text><text x="456" y="130" font-size="8.5" fill="#44546f" text-anchor="middle">ask a human</text>
<text x="456" y="158" font-size="8" fill="#9a5b00" text-anchor="middle">human in the loop</text>
<rect x="555" y="64" width="172" height="110" rx="8" fill="#232F3E"/>
<text x="641" y="84" font-size="9.5" fill="#fff" text-anchor="middle" font-weight="700">Agent Control</text>
<text x="641" y="104" font-size="8.5" fill="#c9d2de" text-anchor="middle">rules evaluate every</text><text x="641" y="117" font-size="8.5" fill="#c9d2de" text-anchor="middle">input and output;</text><text x="641" y="130" font-size="8.5" fill="#c9d2de" text-anchor="middle">deny raises, blocks</text>
<text x="641" y="158" font-size="8" fill="#9dbcf0" text-anchor="middle">runtime control plane</text>
<rect x="740" y="64" width="172" height="110" rx="8" fill="#232F3E"/>
<text x="826" y="84" font-size="9.5" fill="#fff" text-anchor="middle" font-weight="700">AgentCore Policy</text>
<text x="826" y="104" font-size="8.5" fill="#c9d2de" text-anchor="middle">declarative agent-to-</text><text x="826" y="117" font-size="8.5" fill="#c9d2de" text-anchor="middle">tool access control</text><text x="826" y="130" font-size="8.5" fill="#c9d2de" text-anchor="middle">at the tool gateway</text>
<text x="826" y="158" font-size="8" fill="#9dbcf0" text-anchor="middle">hard outer boundary</text>
<text x="456" y="198" font-size="9" fill="#44546f" text-anchor="middle">Combine them: steering keeps a well-behaved agent on track; a hard policy or deny rule stops a misbehaving one.</text>
</svg>
</div>

## Observability

Strands emits OpenTelemetry traces and metrics, so you can send them to any OpenTelemetry backend. The loop records tokens, latency, and tool calls for each cycle in `EventLoopMetrics`, and a call to an MCP server appears in the same trace as the model call that requested it.

---

## Evaluation: testing the agents themselves

Strands Evals tests changes to the agent itself, such as a new prompt, a smaller tool list, or a model upgrade. You write an experiment file of cases, each with an input and a way to score the output, and run it in continuous integration (CI). `validate` checks the file against its schema before any model call, and `run` executes the cases against an agent and fails the build when a `--fail-on` rule, such as a score threshold, is not met. Add each production failure to the suite as a new case. The package installs as `strands-agents-evals`.

```bash
strands-evals validate experiments/support.json
strands-evals run experiments/support.json --agent agents:responder \
  --fail-on threshold:0.85 -o support-report.json
```

<div class="figure">
<svg viewBox="0 0 912 190" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="e1-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="e1-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="e1-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">EVALS GATE A CHANGE TO THE AGENT BEFORE IT MERGES</text>
<rect x="0" y="34" width="150" height="44" rx="5" fill="#232F3E"/><text x="75" y="54" font-size="9.5" fill="#fff" text-anchor="middle" font-weight="600">agent change</text><text x="75" y="67" font-size="8" fill="#c9d2de" text-anchor="middle">new prompt, tools, model</text>
<rect x="196" y="34" width="150" height="44" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="271" y="54" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">validate</text><text x="271" y="67" font-size="8" fill="#44546f" text-anchor="middle">schema, before any call</text>
<rect x="392" y="34" width="150" height="44" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="467" y="54" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">run --fail-on</text><text x="467" y="67" font-size="8" fill="#44546f" text-anchor="middle">score each case</text>
<rect x="588" y="34" width="150" height="44" rx="5" fill="#fffae6" stroke="#f5c56b"/><text x="663" y="54" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">threshold met?</text><text x="663" y="67" font-size="8" fill="#9a5b00" text-anchor="middle">e.g. 0.85</text>
<rect x="784" y="22" width="128" height="30" rx="5" fill="#e3fcef" stroke="#1e7e34"/><text x="848" y="41" font-size="9" fill="#1e7e34" text-anchor="middle" font-weight="700">merge</text>
<rect x="784" y="60" width="128" height="30" rx="5" fill="#ffffff" stroke="#de350b"/><text x="848" y="79" font-size="9" fill="#de350b" text-anchor="middle" font-weight="700">fail the build</text>
<line x1="150" y1="56" x2="193" y2="56" stroke="#232F3E" stroke-width="1.4" marker-end="url(#e1-d)"/>
<line x1="346" y1="56" x2="389" y2="56" stroke="#232F3E" stroke-width="1.4" marker-end="url(#e1-d)"/>
<line x1="542" y1="56" x2="585" y2="56" stroke="#232F3E" stroke-width="1.4" marker-end="url(#e1-d)"/>
<line x1="738" y1="48" x2="781" y2="40" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#e1-gr)"/>
<line x1="738" y1="64" x2="781" y2="72" stroke="#de350b" stroke-width="1.4" marker-end="url(#e1-r)"/>
<path d="M848 90 C848 130 467 130 467 80" fill="none" stroke="#de350b" stroke-width="1.3" stroke-dasharray="4 3" marker-end="url(#e1-r)"/>
<text x="657" y="128" font-size="8.5" fill="#de350b" text-anchor="middle" font-weight="700">add the failure as a new case, then re-run</text>
<text x="0" y="176" font-size="9" fill="#44546f">Evals tests the agent itself, so a prompt or model change cannot lower quality without failing the build.</text>
</svg>
</div>

## Strands Box: a local policy sandbox

Strands Box is an open-source local sandbox for agents, in developer preview, that works with any model and any framework. It uses kernel isolation for one purpose: to make a single user-space policy layer the only way out of the sandbox. Every shell command, Python call, MCP call, file access, and network request passes through that layer, where Dogwood, an open policy language, allows or denies each action. The check is per tool and deterministic, so you can write rules such as "allow `git push` only if tests passed in the last 15 minutes" or "allow the payments API up to $100 a day".

<div class="figure">
<svg viewBox="0 0 912 210" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="b1-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="b1-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="b1-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">THE POLICY LAYER IS THE ONLY WAY OUT OF THE BOX</text>
<rect x="0" y="26" width="300" height="160" rx="8" fill="#232F3E"/>
<text x="150" y="46" font-size="9" fill="#FF9900" text-anchor="middle" font-weight="700">KERNEL-ENFORCED SANDBOX</text>
<rect x="40" y="58" width="220" height="40" rx="6" fill="#FF9900"/><text x="150" y="78" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">the agent</text><text x="150" y="90" font-size="8" fill="#4a3200" text-anchor="middle">shell, Python, MCP, network</text>
<rect x="40" y="112" width="100" height="20" rx="4" fill="#3d5068"/><text x="90" y="126" font-size="7.5" fill="#e0e6ed" text-anchor="middle">shell script</text>
<rect x="146" y="112" width="100" height="20" rx="4" fill="#3d5068"/><text x="196" y="126" font-size="7.5" fill="#e0e6ed" text-anchor="middle">Python code</text>
<rect x="40" y="136" width="100" height="20" rx="4" fill="#3d5068"/><text x="90" y="150" font-size="7.5" fill="#e0e6ed" text-anchor="middle">MCP call</text>
<rect x="146" y="136" width="100" height="20" rx="4" fill="#3d5068"/><text x="196" y="150" font-size="7.5" fill="#e0e6ed" text-anchor="middle">network request</text>
<rect x="356" y="46" width="200" height="120" rx="8" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.4"/>
<text x="456" y="66" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">policy layer (user space)</text>
<text x="456" y="86" font-size="8.5" fill="#44546f" text-anchor="middle">Strands Shell &#183; Monty</text>
<text x="456" y="100" font-size="8.5" fill="#44546f" text-anchor="middle">MCP broker &#183; network gateway</text>
<rect x="386" y="112" width="140" height="34" rx="5" fill="#FF9900"/><text x="456" y="128" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="700">Dogwood</text><text x="456" y="140" font-size="7.5" fill="#4a3200" text-anchor="middle">allow or deny each action</text>
<rect x="612" y="46" width="300" height="120" rx="8" fill="#f8f9fb" stroke="#dfe1e6"/>
<text x="762" y="66" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="700">THE WORLD</text>
<rect x="636" y="80" width="118" height="22" rx="4" fill="#ffffff" stroke="#dfe1e6"/><text x="695" y="95" font-size="8" fill="#1a1a2e" text-anchor="middle">commands</text>
<rect x="770" y="80" width="118" height="22" rx="4" fill="#ffffff" stroke="#dfe1e6"/><text x="829" y="95" font-size="8" fill="#1a1a2e" text-anchor="middle">MCP servers</text>
<rect x="636" y="110" width="118" height="22" rx="4" fill="#ffffff" stroke="#dfe1e6"/><text x="695" y="125" font-size="8" fill="#1a1a2e" text-anchor="middle">filesystem</text>
<rect x="770" y="110" width="118" height="22" rx="4" fill="#ffffff" stroke="#dfe1e6"/><text x="829" y="125" font-size="8" fill="#1a1a2e" text-anchor="middle">the internet</text>
<line x1="300" y1="106" x2="353" y2="106" stroke="#232F3E" stroke-width="1.6" marker-end="url(#b1-d)"/>
<text x="326" y="100" font-size="7.5" fill="#6b7a90" text-anchor="middle">only exit</text>
<line x1="556" y1="100" x2="609" y2="100" stroke="#1e7e34" stroke-width="1.6" marker-end="url(#b1-gr)"/><text x="582" y="94" font-size="7.5" fill="#1e7e34" text-anchor="middle">allow</text>
<path d="M456 166 C456 190 326 190 326 150" fill="none" stroke="#de350b" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#b1-r)"/><text x="391" y="188" font-size="8" fill="#de350b" text-anchor="middle" font-weight="700">deny: blocked before it leaves</text>
<text x="612" y="186" font-size="8.5" fill="#44546f">Per-tool, deterministic: &#8220;git push only if tests passed&#8221;, &#8220;payments API up to $100/day&#8221;.</text>
</svg>
</div>

Box is the local counterpart of the AgentCore microVM: the microVM isolates a hosted session, and Box isolates and governs an agent on your laptop. Its policy engine uses the same technology as AgentCore Policy, which uses the Cedar policy language in the cloud. The [03-strands-box-harness](../03-strands-box-harness/README.md) sample runs an agent inside Strands Box.

---

## The layered stack: SDK, harness, and the tools around it

`create_harness()` resolves your options, adds the built-in tools and plugins, and returns a plain `Agent`. Every option has a default that you can override, so you start fast and drop to the raw SDK when your agent has a shape the harness does not expect. Agent Skills (instructions on disk that an agent loads when needed), Strands Evals, and Agent SOPs (procedures in natural language) sit beside the stack.

<div class="figure">
<svg viewBox="0 0 912 240" xmlns="http://www.w3.org/2000/svg" role="img">
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">THE STACK: EACH LAYER SITS ON THE ONE BELOW, AND YOU CAN STOP AT ANY LEVEL</text>
<rect x="120" y="150" width="672" height="40" rx="6" fill="#34465c"/><text x="456" y="168" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">Strands SDK</text><text x="456" y="182" font-size="8.5" fill="#c9d2de" text-anchor="middle">agent loop &#183; tools &#183; context &#183; sessions &#183; memory &#183; hooks &#183; interventions &#183; multi-agent</text>
<rect x="200" y="100" width="512" height="40" rx="6" fill="#0052CC"/><text x="456" y="118" font-size="10" fill="#fff" text-anchor="middle" font-weight="700">Strands Harness</text><text x="456" y="132" font-size="8.5" fill="#dbe6ff" text-anchor="middle">create_harness(): tuned defaults, built-in tools, one plain Agent out</text>
<rect x="286" y="50" width="340" height="40" rx="6" fill="#FF9900"/><text x="456" y="68" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">your agent</text><text x="456" y="82" font-size="8.5" fill="#4a3200" text-anchor="middle">a few lines of configuration</text>
<line x1="456" y1="90" x2="456" y2="100" stroke="#8a96a8" stroke-width="1.2"/><line x1="456" y1="140" x2="456" y2="150" stroke="#8a96a8" stroke-width="1.2"/>
<rect x="0" y="50" width="130" height="140" rx="8" fill="#f8f9fb" stroke="#dfe1e6"/>
<text x="65" y="68" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">ALONGSIDE</text>
<rect x="12" y="78" width="106" height="28" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="65" y="92" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Agent Skills</text><text x="65" y="102" font-size="7.5" fill="#44546f" text-anchor="middle">on-disk know-how</text>
<rect x="12" y="112" width="106" height="28" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="65" y="126" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Strands Evals</text><text x="65" y="136" font-size="7.5" fill="#44546f" text-anchor="middle">gate agent changes</text>
<rect x="12" y="146" width="106" height="28" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="65" y="160" font-size="8.5" fill="#1a1a2e" text-anchor="middle">Agent SOPs</text><text x="65" y="170" font-size="7.5" fill="#44546f" text-anchor="middle">NL workflows</text>
<rect x="782" y="50" width="130" height="140" rx="8" fill="#f8f9fb" stroke="#dfe1e6"/>
<text x="847" y="68" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">RUNS ON</text>
<rect x="794" y="90" width="106" height="34" rx="5" fill="#232F3E"/><text x="847" y="106" font-size="8.5" fill="#fff" text-anchor="middle">your laptop</text><text x="847" y="118" font-size="7.5" fill="#c9d2de" text-anchor="middle">local dev</text>
<rect x="794" y="130" width="106" height="34" rx="5" fill="#232F3E"/><text x="847" y="146" font-size="8.5" fill="#FF9900" text-anchor="middle">AgentCore</text><text x="847" y="158" font-size="7.5" fill="#c9d2de" text-anchor="middle">Runtime (hosted)</text>
<text x="456" y="214" font-size="9.5" fill="#44546f" text-anchor="middle">Build on the harness for speed, or on the raw SDK for an unusual shape. The same agent runs on your laptop</text>
<text x="456" y="230" font-size="9.5" fill="#44546f" text-anchor="middle">and in AgentCore Runtime; only where the loop runs and who signs the calls changes.</text>
</svg>
</div>

```python
from strands_harness import create_harness

# a planner that cannot run code: no shell, read and write only
planner = create_harness(name="planner", builtin_tools=["read", "write", "web_fetch", "web_search"],
                         instructions="Turn the issue into a spec with acceptance tests. Write no code.")
```

---

## Running agents in production

The usual production target is Amazon Bedrock AgentCore Runtime, a serverless host that gives each session its own microVM (a small virtual machine destroyed when the session ends). The microVM is the sandbox, so a deployed agent needs no extra sandbox for its shell. The runtime contract is to build for ARM64, listen on port 8080, and answer `POST /invocations` and `GET /ping`. The `BedrockAgentCoreApp` wrapper turns an agent function into that service, and the AgentCore CLI builds the image, pushes it to Amazon ECR, and creates the runtime.

<div class="figure">
<svg viewBox="0 0 912 170" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="d1-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="0" y="13" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">FROM A LOCAL AGENT TO A HOSTED, SIGNED ENDPOINT</text>
<rect x="0" y="30" width="200" height="48" rx="5" fill="#232F3E"/><text x="100" y="50" font-size="10" fill="#fff" text-anchor="middle" font-weight="600">your agent function</text><text x="100" y="63" font-size="8.5" fill="#c9d2de" text-anchor="middle">plain Python</text>
<rect x="237" y="30" width="200" height="48" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="337" y="50" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">BedrockAgentCoreApp</text><text x="337" y="63" font-size="8.5" fill="#44546f" text-anchor="middle">adds /invocations + /ping</text>
<rect x="474" y="30" width="200" height="48" rx="5" fill="#e6f0ff" stroke="#b3d4ff"/><text x="574" y="50" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">ARM64 image</text><text x="574" y="63" font-size="8.5" fill="#44546f" text-anchor="middle">agentcore deploy &#8594; ECR</text>
<rect x="711" y="30" width="201" height="48" rx="5" fill="#FF9900"/><text x="811" y="50" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">AgentCore Runtime</text><text x="811" y="63" font-size="8.5" fill="#4a3200" text-anchor="middle">one microVM per session</text>
<line x1="200" y1="54" x2="234" y2="54" stroke="#232F3E" stroke-width="1.4" marker-end="url(#d1-d)"/>
<line x1="437" y1="54" x2="471" y2="54" stroke="#232F3E" stroke-width="1.4" marker-end="url(#d1-d)"/>
<line x1="674" y1="54" x2="708" y2="54" stroke="#232F3E" stroke-width="1.4" marker-end="url(#d1-d)"/>
<rect x="0" y="100" width="912" height="56" rx="8" fill="#f8f9fb" stroke="#dfe1e6"/>
<text x="16" y="120" font-size="8.5" fill="#6b7a90" font-weight="700">AUTH AND STORAGE</text>
<text x="16" y="140" font-size="10" fill="#1a1a2e">SigV4 for service-to-service, or a JWT bearer token for end users. Per-session storage lets several invocations</text>
<text x="16" y="152" font-size="10" fill="#1a1a2e">in one session share a workspace, which is what makes a multi-stage pipeline pass files between its stages.</text>
</svg>
</div>

The samples in this repo put these pieces to work. [01-simple-strands-harness](../01-simple-strands-harness/README.md) deploys a harness agent to AgentCore Runtime and tests it end to end. [03-strands-box-harness](../03-strands-box-harness/README.md) runs an agent inside Strands Box. [05-software-factory](../05-software-factory/README.md) runs a multi-stage pipeline with evals.

## Where to start

Start with one agent, one model, and two or three tools. Add a session manager when the agent must survive a restart, structured output when another program reads the result, and agents as tools when one scope of work becomes two, then move to a swarm or a graph as coordination grows. Add guardrails before the agent can do anything expensive, and tracing before it runs where you cannot watch it. Each step is an argument to the same `Agent`, so the smallest program and the production system have the same shape.

Primary sources: the Strands Agents documentation and SDK reference at [strandsagents.com](https://strandsagents.com/), the [1.0 release announcement](https://strandsagents.com/blog/strands-agents-1-0/), the [model providers guide](https://strandsagents.com/docs/user-guide/sdk/model-providers/), the [multi-agent guides](https://strandsagents.com/docs/user-guide/sdk/multi-agent/graph/), and the [Agent Control runtime guardrails announcement](https://strandsagents.com/blog/strands-agents-with-agent-control/).
