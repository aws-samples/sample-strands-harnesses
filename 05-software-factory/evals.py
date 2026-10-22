"""Grade the factory itself with Strands Evals, and send the scores to CloudWatch.

    uv run evals.py                  write the suites, run them, print and record the scores
    uv run evals.py --suite review   run one suite
    uv run evals.py --write          write the experiment files and stop
    uv run evals.py --fail-under 0.9 raise the pass mark (the default is 0.8)

WHAT THE EVALS ARE FOR

test.py checks one product that the factory builds. This file checks the agents that do the
building. Run it after you change a stage in agent.py: the instruction block, the tool list,
the CONTRACT text, or MODEL_ID. A change that makes the reviewer approve a stub, or makes the
planner write code, fails here in about two minutes. Without this file, the defect shows up
only after a full factory run, which takes about fifteen minutes.

Each suite grades a gate, a yes or no decision that the pipeline depends on, not a matter of
taste:

    review    the reviewer rejects a stub, and approves work that meets its specification
    plan      the planner turns a goal into requirements.md and spec.md, and writes no code

The build, test and release stages have no suite yet. Their output is code and reports, and a
full test.py run is the check for them today.

HOW ONE CASE RUNS

1. suites() builds each Experiment. A Case carries the task text in `input`, the expected
   verdict in `expected_output` where there is one, and in `metadata` the stage name and
   the files to seed.
2. stage_agent() makes a temporary directory, writes the seed files into it, and makes it
   the current directory. The temporary directory stands in for the per-session microVM disk.
3. stage_agent() builds a harness agent from agent.CONTRACT, agent.STAGES[stage] and
   agent.MODEL_ID. These are the same instructions and the same tools that the runtime
   deploys, so a change to a stage changes the suite with it. The AWS MCP tools are left
   out, so a suite needs only Bedrock to start.
4. The agent runs the task on your laptop and calls Bedrock with your own credentials. No
   AgentCore runtime takes part, so you do not deploy before you run the evals.
5. The evaluators of the suite score the reply from 0.0 to 1.0.

HOW EACH SUITE IS SCORED

    review    VerdictEvaluator, defined below. It is deterministic and calls no model. It
              reads the verdict in the reply. It looks for REVISION NEEDED first and
              APPROVED second, because a reply that asks for changes and also says
              APPROVED has failed the gate. The score is 1.0 when the verdict matches
              expected_output, else 0.0.
              The stub case (`STUB`) must get REVISION NEEDED. The finished case (`GOOD`)
              must get APPROVED. With both cases, a reviewer that always says the same word
              scores 0.5 and fails.
    plan      OutputEvaluator, with PLAN_RUBRIC. A judge model, the same MODEL_ID, reads the
              reply against the rubric: 1.0 for both files, testable criteria and no code,
              0.5 for one missing file or an untestable criterion, 0.0 for code, a question
              to the user, or no files.

The overall score of a suite is the mean of its case scores. A suite passes at PASS_MARK
(0.8) or above. The command exits 1 when any suite scores under the mark, so CI can gate on
it.

WHAT IT PRINTS

A real run of `uv run evals.py` on 25 September 2026 printed this, after about two minutes:

    suite plan
      pass  goal-becomes-two-files OutputEvaluator=1.00
      overall 1.00 over 1 scores
    suite review
      pass  rejects-a-stub VerdictEvaluator=1.00
      pass  approves-finished-work VerdictEvaluator=1.00
      overall 1.00 over 2 scores
    Scores
      pass  plan 1.00
      pass  review 1.00
    metrics export accepted: True
    PASS: every suite scored 0.8 or better

A failed case also prints the reason the evaluator gave, for example `wanted REVISION
NEEDED, the reviewer said APPROVED`.

WHERE THE SCORES GO

Every case score becomes one `factory.eval.score` point in Amazon CloudWatch, through the
same SigV4-signed OTLP metrics path that telemetry.py uses for the pipeline. The suite and
the evaluator are dimensions. In Query Studio the metric is named `factory_eval_score`, so
agent quality sits beside the stage metrics. Tracing is off in this file, because Strands
Evals installs its own tracer provider to read the spans of each case.

HOW TO ADD A CASE

Add a Case to the matching Experiment in suites(). Put the files the agent must find in
metadata["files"], and put the expected verdict in expected_output when the evaluator
compares verdicts. Every production failure is a good new case: seed the files that caused
it, and state the verdict the stage should have given. A new suite for another stage also
needs an entry in TASKS and an @eval_task function like review_agent.

RUNNING THE SUITES FROM THE COMMAND LINE

Continuous integration can use the command line instead of this file, because both suites
are written to experiments/*.json
([Evals CLI](https://strandsagents.com/docs/user-guide/evals-sdk/cli/)). The reviewer suite
uses VerdictEvaluator, which lives in this file, so the command must name it:

    uv run evals.py --write
    strands-evals validate experiments/review.json
    strands-evals run experiments/review.json --agent evals:review_agent \
      --custom-evaluator evals:VerdictEvaluator --fail-on threshold:0.8 -o review.json
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

from strands_evals import Case, Experiment, TracedHandler, eval_task
from strands_evals.evaluators import OutputEvaluator
from strands_evals.evaluators.evaluator import Evaluator
from strands_evals.types.evaluation import EvaluationData, EvaluationOutput

import telemetry

# Strands Evals installs its own tracer provider, because it reads the spans of each case
# to build the trajectory the trace-based evaluators grade. A provider can only be set
# once, so this file leaves tracing to the evals SDK and keeps only the metrics path, which
# is what carries the scores to CloudWatch. telemetry.start runs before agent.py is
# imported, because that module starts telemetry as the runtime when it loads.
os.environ.setdefault("FACTORY_TRACES", "off")
telemetry.start("evals")

HERE = Path(__file__).parent
SUITES_DIR = HERE / "experiments"
PASS_MARK = 0.8  # the score a suite must reach, and the same number a CI gate should use

# A stub with a specification it does not meet. A reviewer that approves this is broken,
# and this case is the one that catches an instruction block that only praises.
STUB = {
    "spec.md": "# Spec\nOne function, add(a, b), that returns the sum of two numbers.\n",
    "requirements.md": "- add(1, 2) returns 3\n- add returns a number, never None\n",
    "calc.py": "def add(a, b):\n    pass  # TODO implement\n",
    "test-report.md": "I ran no tests.\n",
}

# The same work item done properly: one test per acceptance criterion, and a report that
# quotes the command and the output it really produced.
GOOD = {
    "spec.md": "# Spec\nOne function, add(a, b), that returns the sum of two numbers.\n",
    "requirements.md": "- add(1, 2) returns 3\n- add returns a number, never None\n",
    "calc.py": "def add(a, b):\n    return a + b\n",
    "test_calc.py": (
        "from calc import add\n\n\n"
        "def test_add():\n    assert add(1, 2) == 3\n\n\n"
        "def test_add_returns_a_number():\n"
        "    result = add(2, 3)\n"
        "    assert result is not None\n"
        "    assert isinstance(result, (int, float))\n"
    ),
    "test-report.md": (
        "Command: python -m pytest -q\nOutput: 2 passed in 0.01s\n\n"
        "- add(1, 2) returns 3: pass, test_add\n"
        "- add returns a number, never None: pass, test_add_returns_a_number\n"
    ),
}

PLAN_RUBRIC = """\
Score 1.0 when the reply reports that both requirements.md and spec.md were written, the
acceptance criteria are testable one line at a time, and no implementation code was
written. Score 0.5 when one file is missing, or a criterion is not testable. Score 0.0
when the agent wrote code, asked the user a question, or produced no files."""


class VerdictEvaluator(Evaluator):
    """Score the reviewer on its verdict, not on the words around it.

    The reviewer stage must end its reply with APPROVED or with REVISION NEEDED. A reply
    that argues for changes and then says APPROVED is a failure of the gate, so REVISION
    NEEDED is read first. The case carries the verdict it expects in expected_output.
    """

    @staticmethod
    def verdict(text: str) -> str:
        upper = str(text).upper()
        if "REVISION NEEDED" in upper:
            return "REVISION NEEDED"
        if "APPROVED" in upper:
            return "APPROVED"
        return "NO VERDICT"

    def evaluate(self, evaluation_case: EvaluationData) -> list[EvaluationOutput]:
        want = str(evaluation_case.expected_output or "").upper()
        got = self.verdict(evaluation_case.actual_output)
        passed = got == want
        return [
            EvaluationOutput(
                score=1.0 if passed else 0.0,
                test_pass=passed,
                reason=f"wanted {want}, the reviewer said {got}",
            )
        ]

    async def evaluate_async(self, evaluation_case: EvaluationData) -> list[EvaluationOutput]:
        return self.evaluate(evaluation_case)


def suites() -> dict[str, Experiment]:
    """Build both suites. The judge runs on the model the factory itself uses."""
    from agent import MODEL_ID

    return {
        "review": Experiment(
            cases=[
                Case(
                    name="rejects-a-stub",
                    input="Grade the work and write review.md.",
                    expected_output="REVISION NEEDED",
                    metadata={"stage": "review", "files": STUB},
                ),
                Case(
                    name="approves-finished-work",
                    input="Grade the work and write review.md.",
                    expected_output="APPROVED",
                    metadata={"stage": "review", "files": GOOD},
                ),
            ],
            evaluators=[VerdictEvaluator()],
        ),
        "plan": Experiment(
            cases=[
                Case(
                    name="goal-becomes-two-files",
                    input=(
                        "The product goal is below. Write requirements.md and spec.md.\n\n"
                        "A command line tool that counts the words in a text file and "
                        "prints the ten most common words with their counts."
                    ),
                    metadata={"stage": "plan", "files": {}},
                ),
            ],
            evaluators=[OutputEvaluator(rubric=PLAN_RUBRIC, model=MODEL_ID)],
        ),
    }


def stage_agent(case: Case):
    """Build the harness for the stage this case names, in a seeded temporary directory.

    The instructions and the tool list come from agent.py, so a change to a stage changes
    the suite as well. The AWS MCP tools are left out, because these two stages do not use
    them and a suite should not need the network to start.
    """
    from strands_harness import create_harness

    from agent import CONTRACT, MODEL_ID, STAGES

    metadata = case.metadata or {}
    stage = metadata["stage"]
    workspace = Path(tempfile.mkdtemp(prefix=f"eval-{stage}-"))
    for name, text in (metadata.get("files") or {}).items():
        (workspace / name).write_text(text)
    os.chdir(workspace)
    telemetry.log("eval case", suite=stage, case=case.name or "case", workspace=str(workspace))

    spec = STAGES[stage]
    return create_harness(
        model=MODEL_ID,
        instructions=f"{CONTRACT}\n\n{spec['instructions']}",
        builtin_tools=spec["tools"],
        memory=False,
        session=False,
        interventions=None,
        callback_handler=None,
    )


@eval_task(TracedHandler())
def review_agent(case: Case):
    """The reviewer stage, for `strands-evals run --agent evals:review_agent`."""
    return stage_agent(case)


@eval_task(TracedHandler())
def plan_agent(case: Case):
    """The planner stage, for `strands-evals run --agent evals:plan_agent`."""
    return stage_agent(case)


TASKS = {"review": review_agent, "plan": plan_agent}


def write_suites(built: dict[str, Experiment]) -> None:
    """Write each suite as an experiment file, which is what the CLI gate reads."""
    SUITES_DIR.mkdir(exist_ok=True)
    for name, experiment in built.items():
        path = SUITES_DIR / f"{name}.json"
        experiment.to_file(str(path))
        print(f"wrote {path.relative_to(HERE)}, {len(experiment.cases)} cases")


def run_suite(name: str, experiment: Experiment) -> float:
    """Run one suite, record every score in CloudWatch, and return the overall score."""
    started = Path.cwd()  # each case moves the process into its workspace, so come back
    try:
        with telemetry.span("evals.suite", suite=name):
            report = experiment.run_evaluations(TASKS[name])
    finally:
        os.chdir(started)

    print(f"\nsuite {name}")
    names = [evaluator.get_name() for evaluator in experiment.evaluators]
    for index, case in enumerate(experiment.cases):
        outputs = report.detailed_results[index] if index < len(report.detailed_results) else []
        for evaluator_name, output in zip(names, outputs):
            telemetry.record_eval(name, evaluator_name, float(output.score))
            mark = "pass" if output.test_pass else "FAIL"
            print(f"  {mark}  {case.name} {evaluator_name}={output.score:.2f}")
            if not output.test_pass and output.reason:
                print(f"        {str(output.reason)[:300]}")
    print(f"  overall {report.overall_score:.2f} over {len(report.scores)} scores")
    return float(report.overall_score)


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade the factory agents.")
    built = suites()
    parser.add_argument("--suite", choices=sorted(built), help="run one suite only")
    parser.add_argument("--write", action="store_true", help="write the files and stop")
    parser.add_argument("--fail-under", type=float, default=PASS_MARK)
    args = parser.parse_args()

    write_suites(built)
    if args.write:
        print("\nNow run:  strands-evals validate experiments/review.json")
        return 0

    chosen = [args.suite] if args.suite else sorted(built)
    scores = {name: run_suite(name, built[name]) for name in chosen}
    sent = telemetry.flush()

    print("\nScores")
    for name, score in scores.items():
        print(f"  {'pass' if score >= args.fail_under else 'FAIL'}  {name} {score:.2f}")
    print(f"metrics export accepted: {sent}")
    print("query them in CloudWatch as factory_eval_score, by suite and evaluator")

    if any(score < args.fail_under for score in scores.values()):
        print(f"\nFAIL: a suite scored under {args.fail_under}")
        return 1
    print(f"\nPASS: every suite scored {args.fail_under} or better")
    return 0


if __name__ == "__main__":
    sys.exit(main())
