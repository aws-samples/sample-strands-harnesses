"""Terminal output for cli.py and test.py, drawn with Rich.

Everything a person sees goes through this file: stage banners, the streamed agent text,
tool calls, questions, the feature list, the downloaded code, and the checks. The rest of
the chapter never prints styling of its own, so the look can change here in one place.
Set NO_COLOR=1 to turn colors off.
"""

import re
import time
from pathlib import Path

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

console = Console(theme=Theme({
    "stage": "bold magenta",
    "tool": "bold cyan",
    "muted": "grey50",
    "ok": "bold green",
    "warn": "bold yellow",
    "bad": "bold red",
    "ask": "bold blue",
}), highlight=False)

# One color for each stage, so a person can tell the stages apart at a glance.
STAGE_COLOR = {"clarify": "blue", "plan": "magenta", "build": "yellow", "test": "cyan",
               "review": "green", "release": "bright_white"}

# How the runtime writes a tool call into the stream: "\n[shell] {...}\n".
TOOL_LINE = re.compile(r"^\[([\w.-]+)\] (.*)$")

CODE_SUFFIXES = {".py": "python", ".js": "javascript", ".ts": "typescript", ".sh": "bash",
                 ".toml": "toml", ".json": "json", ".yml": "yaml", ".yaml": "yaml",
                 ".html": "html", ".css": "css", ".sql": "sql"}
CODE_LINES = 120  # lines of each file shown in the terminal; the rest is in the download


def banner(work_item: str, goal: str) -> None:
    body = Text.assemble(("work item  ", "muted"), (work_item, "bold"), "\n",
                         ("goal       ", "muted"), goal.strip()[:400])
    console.print(Panel(body, title="[bold]software factory[/]", border_style="magenta"))


def stage_start(name: str, purpose: str) -> None:
    color = STAGE_COLOR.get(name, "white")
    console.print()
    console.print(Rule(f"[bold {color}]{name.upper()}[/]  [muted]{purpose}[/]",
                       style=color, align="left"))


class Stream:
    """Print the text a stage streams back, one whole line at a time.

    The runtime sends text in chunks that split lines anywhere. Holding the tail until its
    newline arrives lets a tool call be drawn as one styled line.
    """

    def __init__(self) -> None:
        self.tail = ""
        self.last = "starting"

    def feed(self, chunk: str) -> None:
        lines = (self.tail + chunk).split("\n")
        self.tail = lines.pop()
        for line in lines:
            self._line(line)

    def flush(self) -> None:
        if self.tail:
            self._line(self.tail)
            self.tail = ""

    def _line(self, line: str) -> None:
        if match := TOOL_LINE.match(line.strip()):
            name, args = match.groups()
            self.last = f"{name} {args[:80]}"
            console.print(Text.assemble(("  ⏺ ", "tool"), (name, "tool"), " ",
                                        (args[:140], "muted")))
        elif line.strip():
            self.last = line.strip()[:100]
            console.print(Text(line))
        else:
            console.print()


def heartbeat(name: str, elapsed: str, last: str) -> None:
    console.print(f"  [muted]… {name} still working, {elapsed} so far. Last: {last}[/]")


def stage_done(name: str, elapsed: str, steps: int, tokens: int, files: list[str]) -> None:
    console.print(Text.assemble(("✔ ", "ok"), (f"{name} done", "ok"),
                                (f"  {elapsed} · {steps} steps · {tokens:,} tokens", "muted")))
    if files:
        console.print(f"  [muted]workspace:[/] {', '.join(files)}")


def round_start(number: int, total: int) -> None:
    console.print()
    console.print(Panel(f"round {number} of {total}: build, test, review",
                        border_style="yellow", expand=False))


def info(message: str) -> None:
    console.print(f"[muted]{message}[/]")


def ok(message: str) -> None:
    console.print(f"[ok]✔ {message}[/]")


def warn(message: str) -> None:
    console.print(f"[warn]! {message}[/]")


def fail(message: str) -> None:
    console.print(f"[bad]✘ {message}[/]")


def markdown(title: str, text: str, style: str = "blue") -> None:
    """Show a Markdown file from the workspace in a titled panel."""
    console.print(Panel(Markdown(text or "_(empty)_"), title=f"[bold]{title}[/]",
                        border_style=style))


def ask(question: str, default: str) -> str:
    return Prompt.ask(f"[ask]?[/] {question}", default=default or None, console=console) or ""


def ask_text(question: str) -> str:
    """Ask until the person types something."""
    while True:
        answer = Prompt.ask(f"[ask]?[/] {question}", console=console).strip()
        if answer:
            return answer


def auto(question: str, answer: str) -> None:
    """Show a question that --yes answered, so the log still reads as a conversation."""
    console.print(f"[ask]?[/] {question} [muted](auto)[/] {answer}")


def artifacts(items: list[dict], title: str = "workspace files") -> None:
    table = Table(title=title, title_justify="left", show_edge=False, header_style="muted")
    table.add_column("file")
    table.add_column("bytes", justify="right", style="muted")
    for item in items:
        if "__pycache__" not in item["path"]:
            table.add_row(item["path"], f"{item['bytes']:,}")
    console.print(table)


def code(folder: Path) -> None:
    """Show every source file of the downloaded work item with syntax highlighting."""
    for file in sorted(folder.rglob("*")):
        language = CODE_SUFFIXES.get(file.suffix)
        if language is None and file.name != "README.md":
            continue
        text = file.read_text(errors="replace")
        lines = text.splitlines()
        shown = "\n".join(lines[:CODE_LINES])
        title = f"[bold]{file.relative_to(folder)}[/] [muted]{len(lines)} lines[/]"
        if file.name == "README.md":
            console.print(Panel(Markdown(text), title=title, border_style="grey50"))
            continue
        more = len(lines) - CODE_LINES
        console.print(Panel(
            Syntax(shown, language, line_numbers=True, theme="monokai", word_wrap=False),
            title=title,
            subtitle=f"[muted]{more} more lines in the download[/]" if more > 0 else None,
            border_style="grey50",
        ))


def download(zip_path: Path, folder: Path, size: int) -> None:
    console.print(Panel(
        Text.assemble(("zip     ", "muted"), str(zip_path), f"  ({size:,} bytes)\n",
                      ("folder  ", "muted"), str(folder)),
        title="[ok]code downloaded[/]", border_style="green"))


def next_steps(folder: Path) -> None:
    """Say where the code is and how to run it, from the commands in its own README."""
    readme = folder / "README.md"
    blocks = []
    if readme.exists():
        text, fence = readme.read_text(errors="replace"), "`" * 3
        parts = text.split(fence)
        for body in parts[1::2]:  # the text inside each fenced block
            language, _, code = body.partition("\n")
            if language.strip() in ("bash", "sh", "shell", "console", "") and code.strip():
                blocks.append(code.strip())
    commands = "\n\n".join(blocks[:3]) or "# read README.md in this folder"
    console.print(Panel(
        Group(
            Text.assemble(("Your code is in  ", "muted"), (str(folder.resolve()), "bold")),
            Text("Run it with the commands from its README.md:", style="muted"),
            Syntax(f"cd {folder.resolve()}\n\n{commands}", "bash", theme="monokai", word_wrap=True),
        ),
        title="[ok]next: run the code[/]", border_style="green"))


def serving(url: str, start: str) -> None:
    """Show the local URL that forwards to the app inside its AgentCore session."""
    console.print(Panel(
        Group(
            Text.assemble(("Open  ", "muted"), (url, "bold underline")),
            Text.assemble(("The app runs in its AgentCore session", "muted"),
                          (f" ({start})" if start else "", "muted"), (".", "muted")),
            Text("Each request goes there as one SigV4-signed call. Press Ctrl+C to stop.",
                 style="muted"),
        ),
        title="[ok]app running[/]", border_style="green"))


def apps(found: dict) -> None:
    """List the app names that cli.py knows, newest last."""
    if not found:
        info("No apps yet. A run asks for a name, or takes one with --app.")
        return
    table = Table(show_edge=False)
    for column in ("app", "work item", "created", "goal"):
        table.add_column(column)
    for name, item in found.items():
        table.add_row(name, item["work_item"], item.get("created", ""), item.get("goal", "")[:60])
    console.print(table)


def checks(results: dict[str, bool]) -> None:
    table = Table(show_edge=False, show_header=False)
    table.add_column(width=6)
    table.add_column()
    for claim, passed in results.items():
        table.add_row("[ok]pass[/]" if passed else "[bad]FAIL[/]", claim)
    console.print(Panel(table, title="[bold]checks[/]", border_style="green"
                        if all(results.values()) else "red"))


def clock() -> str:
    return time.strftime("%H:%M:%S")
