"""Draw images/factory-flow.svg, the process figure in architecture.md.

    uv run images/make_factory_flow.py

GitHub shows an SVG only as an image file, so the figure is a file and this script makes it.
"""

from pathlib import Path
from xml.sax.saxutils import escape

W, H = 912, 628
INK, NAVY, SLATE, MUTED = "#1a1a2e", "#232F3E", "#44546f", "#6b7a90"
ORANGE, BLUE, RED, GREEN = "#FF9900", "#0052CC", "#de350b", "#1e7e34"
MONO = "SFMono-Regular, Menlo, Consolas, monospace"
out: list[str] = []


def text(x, y, s, size=8.5, fill=INK, anchor="start", weight="normal", mono=False):
    family = f' font-family="{MONO}"' if mono else ""
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
               f'font-weight="{weight}"{family}>{escape(s)}</text>')


def rect(x, y, w, h, fill, stroke=None, rx=5, dash=False):
    d = ' stroke-dasharray="4 3"' if dash else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
               f'stroke="{stroke or fill}" stroke-width="1.2"{d}/>')


def pill(x, y, w, s, fill="#3d5068", stroke="#51657f", color="#e0e6ed", size=7.5):
    rect(x, y, w, 18, fill, stroke, rx=9)
    text(x + w / 2, y + 12.5, s, size, color, "middle", mono=True)


def arrow(x1, y1, x2, y2, color, marker, width=1.4):
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
               f'stroke-width="{width}" marker-end="url(#{marker})"/>')


def path(d, color, marker, dash=True, width=1.4):
    dd = ' stroke-dasharray="4 3"' if dash else ""
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{dd} '
               f'marker-end="url(#{marker})"/>')


markers = "".join(
    f'<marker id="{i}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6.5" '
    f'markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
    for i, c in [("m-o", ORANGE), ("m-b", BLUE), ("m-r", RED), ("m-d", NAVY), ("m-g", GREEN)])

text(0, 13, "THE SOFTWARE FACTORY: ONE GOAL IN, TESTED CODE AND A RELEASE OUT", 8.5, MUTED, weight="700")

# Your laptop.
rect(0, 40, 162, 238, NAVY)
text(81, 62, "your laptop", 10, "#ffffff", "middle", "600")
text(81, 75, "cli.py, ui.py, test.py", 8.5, "#c9d2de", "middle")
for i, s in enumerate(['uv run cli.py "goal"', "asks you, 3 stops", "Rich terminal output",
                       "boto3 signs SigV4", "start a stage, then poll", "retries Bedrock errors",
                       "holds the round loop", "unzips out/<work item>/"]):
    pill(7, 88 + i * 22, 148, s)
arrow(164, 83, 186, 83, ORANGE, "m-o")
text(175, 77, "SigV4", 8, "#9a5b00", "middle", "600")

# The runtime.
rect(188, 24, 724, 380, "#f8f9fb", "#dfe1e6", rx=8)
text(200, 42, "AMAZON BEDROCK AGENTCORE RUNTIME  ·  ONE microVM PER WORK ITEM", 8.5, MUTED, weight="700")
text(200, 56, "every call carries runtimeSessionId = sdlc-<uuid>, so every stage lands in the same microVM",
     8.5, SLATE)
rect(200, 64, 698, 36, NAVY)
text(549, 79, "agent.py  ·  @app.entrypoint", 10, "#ffffff", "middle", "600")
text(549, 93, "stage: start that agent as a background task  ·  status: new progress  ·  read: one file  ·  bundle: the workspace as a zip",
     8.5, "#c9d2de", "middle")

# The stages and the three stops for a person.
AGENT_W, GATE_W, GAP = 78, 56, 7.75
steps = [
    ("agent", "1 · Clarify", "clarifier", "read only", "questions"),
    ("gate", "You", "answer", "questions", "or defaults"),
    ("agent", "2 · Plan", "planner", "read, write, web", "features, spec"),
    ("gate", "You", "approve", "features.md", "yes/no/edits"),
    ("agent", "3 · Build", "builder", "all tools", "code, README"),
    ("agent", "4 · Test", "tester", "all tools", "tests, report"),
    ("agent", "5 · Review", "reviewer", "read, shell", "review.md"),
    ("gate", "You", "release?", "zip to laptop", "yes or no"),
    ("agent", "6 · Release", "release agent", "read,write,shell", "release.md"),
]
x, centers = 200.0, []
for kind, title, sub, p1, p2 in steps:
    w = AGENT_W if kind == "agent" else GATE_W
    if kind == "agent":
        rect(x, 140, w, 50, NAVY)
        text(x + w / 2, 162, title, 9.5, "#ffffff", "middle", "600")
        text(x + w / 2, 176, sub, 8, "#c9d2de", "middle")
        pill(x, 198, w, p1, "#e6f0ff", "#b3d4ff", INK)
        pill(x, 220, w, p2, "#e3fcef", "#abf5d1", INK)
    else:
        rect(x, 140, w, 50, "#fffae6", "#f5c56b")
        text(x + w / 2, 162, title, 9.5, INK, "middle", "600")
        text(x + w / 2, 176, sub, 8, SLATE, "middle")
        pill(x, 198, w, p1, "#fffae6", "#f5c56b", INK, 7)
        pill(x, 220, w, p2, "#fffae6", "#f5c56b", INK, 7)
    centers.append(x + w / 2)
    if len(centers) < len(steps):
        arrow(x + w + 0.5, 165, x + w + GAP - 0.5, 165, NAVY, "m-d", 1.2)
    x += w + GAP

# The two loops: a person's changes go back to the planner, a review back to the builder.
path(f"M{centers[3]} 139 C{centers[3]} 118 {centers[2]} 118 {centers[2]} 139", "#8e44ad", "m-r")
text((centers[2] + centers[3]) / 2, 116, "YOUR CHANGES", 8, "#8e44ad", "middle", "700")
path(f"M{centers[6]} 139 C{centers[6]} 112 {centers[4]} 112 {centers[4]} 139", RED, "m-r")
out.append(f'<rect x="{(centers[4] + centers[6]) / 2 - 86}" y="111" width="172" height="11" '
           f'fill="#f8f9fb"/>')
text((centers[4] + centers[6]) / 2, 120, "REVISION NEEDED · AT MOST 3 ROUNDS", 8, RED, "middle", "700")
text(centers[0], 132, "your goal", 8, MUTED, "middle")

# The shared workspace, and the zip that goes back to the laptop.
pill(200, 250, 698, "/tmp/factory/<work item>   one workspace, read and written by every stage in turn",
     "#fffae6", "#f5c56b", INK, 8.5)
path("M199 259 L166 259", GREEN, "m-g", dash=False)
text(182, 272, "zip", 8, GREEN, "middle", "700")

# The guards.
rect(200, 280, 698, 96, NAVY, rx=8)
text(216, 298, "GUARDS THAT KEEP A STAGE FROM HANGING", 8.5, ORANGE, weight="700")
for i, s in enumerate([
    "A stage never runs a command that does not return. It starts a test server in the background with a timeout.",
    "A stage that sends nothing for 10 minutes fails with a reason. No stage runs longer than 80 minutes.",
    "An MCP server whose command the runtime does not have is skipped, so it cannot fail every stage.",
    "Every tool call is logged and streamed, so a quiet stage still shows what it is running.",
]):
    text(216, 316 + i * 16, s, 9.5, "#ffffff")

# The services the runtime calls.
services = [
    ("Amazon Bedrock", "Claude Sonnet 5 runs every agent", "#e6f0ff", "#b3d4ff", False),
    ("AWS MCP Server", "AWS documentation and APIs", "#e6f0ff", "#b3d4ff", False),
    ("Amazon CloudWatch", "metrics, X-Ray traces, logs", ORANGE, ORANGE, False),
]
bw = 220
gap = (724 - len(services) * bw) / (len(services) - 1)
for i, (name, sub, fill, stroke, dash) in enumerate(services):
    bx = 188 + i * (bw + gap)
    rect(bx, 428, bw, 48, fill, stroke, dash=dash)
    text(bx + bw / 2, 448, name, 10, INK, "middle", "600")
    text(bx + bw / 2, 462, sub, 8.5, SLATE, "middle")
    color, marker = (ORANGE, "m-o") if i == 3 else (BLUE, "m-b")
    arrow(bx + bw / 2, 406, bx + bw / 2, 426, color, marker)
text(188, 492, "THE RUNTIME SIGNS EACH OF THESE CALLS WITH SigV4, AS ITS EXECUTION ROLE", 8.5, MUTED,
     weight="700")
cw = 188 + 3 * (bw + gap) + bw / 2
path(f"M81 280 L81 506 L{cw} 506 L{cw} 478", ORANGE, "m-o", width=1.2)
out.append('<rect x="92" y="500" width="262" height="12" fill="#ffffff"/>')
text(96, 509, "cli.py sends its own spans and your decisions too", 8, "#9a5b00")

# The audit trail.
rect(0, 518, 912, 110, NAVY, rx=8)
text(16, 538, "AGENTIC SDLC AUDIT TRAIL · OPENTELEMETRY · ON BY DEFAULT", 8.5, ORANGE, weight="700")
metrics = ["factory.stage.duration", "factory.stage.tokens", "factory.stage.cycles",
           "factory.stage.runs", "factory.review.verdicts", "factory.rounds",
           "factory.release.decisions", "factory.eval.score"]
px = 16.0
for m in metrics:
    w = len(m) * 4.45 + 12
    pill(px, 548, w, m)
    px += w + 6
text(16, 586, "Metrics go to CloudWatch through its OTLP endpoint, and you query them in Query Studio. Spans factory.run,",
     9.5, "#ffffff")
text(16, 602, "call.<stage> and stage.<stage> go to X-Ray. Each stage start, tool call, and stage end is a line in the runtime log group.",
     9.5, "#ffffff")
text(16, 618, "Every call is signed with SigV4. Nothing issues a token, and no identity provider takes part.",
     9.5, "#c9d2de")

svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
       f'xmlns="http://www.w3.org/2000/svg" role="img" font-family="Helvetica, Arial, sans-serif" '
       f'aria-label="The software factory from goal to release">\n<defs>{markers}</defs>\n'
       + "\n".join(out) + "\n</svg>\n")
Path(__file__).with_name("factory-flow.svg").write_text(svg)
print(f"wrote factory-flow.svg, {len(out)} elements")
