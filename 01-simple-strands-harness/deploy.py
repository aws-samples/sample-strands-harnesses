"""Deploy agent.py to Amazon Bedrock AgentCore Runtime as a code zip.

    uv run deploy.py             # build, deploy, and print how to verify it
    npx aws-cdk deploy           # the same deploy, driven by the cdk command
    npx aws-cdk destroy          # remove the stack

`cdk.json` points the cdk command at this file. When the cdk command runs it, this file
only describes the stack. When you run it yourself, it describes the stack and then calls
`npx aws-cdk deploy` for you, and prints the deployed ARN with a command that proves the
runtime answers.

No container: AgentCore runs the code on its managed Python runtime, so deploying needs
neither Docker nor Finch. Callers authenticate with SigV4 using their own AWS
credentials, which is the runtime default, so there is no Cognito. The execution role
can call one Bedrock model and write its own logs.
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import aws_cdk as cdk
from aws_cdk import aws_bedrockagentcore as agentcore
from aws_cdk import aws_iam as iam

HERE = Path(__file__).parent
BUILD = HERE / ".build"
STACK = "SimpleStrandsHarness"
PROFILE = "us.anthropic.claude-sonnet-5"  # must match MODEL_ID in agent.py
MODEL = PROFILE.split(".", 1)[1]  # the foundation model behind the profile


def log(message: str) -> None:
    """Report progress on stderr, which the cdk command passes through to the terminal."""
    print(f"[deploy.py] {message}", file=sys.stderr, flush=True)


def stage() -> Path:
    """Build the zip contents: agent.py plus its dependencies for linux/arm64.

    The AgentCore Python runtimes run on Amazon Linux 2023 (glibc 2.34), so uv installs
    manylinux wheels up to 2_34, and --only-binary stops it compiling for this machine.
    """
    started = time.monotonic()
    log("staging dependencies for linux/arm64 on Python 3.12")
    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir()
    requirements = BUILD / "requirements.txt"
    subprocess.run(
        ["uv", "export", "--frozen", "--no-dev", "--no-emit-project", "--no-hashes",
         "--quiet", "--output-file", str(requirements)],
        cwd=HERE,
        check=True,
    )
    subprocess.run(
        ["uv", "pip", "install", "--quiet", "--target", str(BUILD),
         "--python-platform", "aarch64-manylinux_2_34", "--python-version", "3.12",
         "--only-binary", ":all:", "--requirement", str(requirements)],
        cwd=HERE,
        check=True,
    )
    shutil.copy(HERE / "agent.py", BUILD)
    files = [p for p in BUILD.rglob("*") if p.is_file()]
    size = sum(p.stat().st_size for p in files) / 1e6
    log(f"staged {len(files)} files, {size:.0f} MB, in {time.monotonic() - started:.0f}s")
    return BUILD


def build_app() -> cdk.App:
    """Describe the stack. The cdk command calls this file to get exactly this."""
    app = cdk.App()
    stack = cdk.Stack(app, STACK)

    runtime = agentcore.Runtime(
        stack,
        "Harness",
        runtime_name="simple_strands_harness",
        agent_runtime_artifact=agentcore.AgentRuntimeArtifact.from_code_asset(
            path=str(stage()),
            runtime=agentcore.AgentCoreRuntime.PYTHON_3_12,
            entrypoint=["agent.py"],
        ),
    )

    runtime.add_to_role_policy(
        iam.PolicyStatement(
            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
            resources=[
                # The profile, plus the foundation model in every Region the profile
                # routes to. A cross-Region profile calls the model in another Region, so
                # one Region ARN here fails with AccessDeniedException in the other.
                f"arn:aws:bedrock:{stack.region}:{stack.account}:inference-profile/{PROFILE}",
                f"arn:aws:bedrock:*::foundation-model/{MODEL}",
                f"arn:aws:bedrock:::foundation-model/{MODEL}",
            ],
        )
    )

    cdk.CfnOutput(stack, "RuntimeArn", value=runtime.agent_runtime_arn)
    return app


def deploy() -> None:
    """Run the cdk deploy, then name the one command that verifies the result."""
    subprocess.run(
        ["npx", "--yes", "aws-cdk", "deploy", "--require-approval", "never"],
        cwd=HERE,
        check=True,
    )
    print("\nDeployed. Now run:  uv run test.py")


# The cdk command sets CDK_OUTDIR when it reads this file, and then it wants the stack
# and nothing else. Without that variable a person ran the file, so deploy for them. The
# child cdk process inherits the variable, so the work happens once.
if os.environ.get("CDK_OUTDIR"):
    build_app().synth()
else:
    deploy()
