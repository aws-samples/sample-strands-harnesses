"""Deploy agent.py to Amazon Bedrock AgentCore Runtime as a code zip.

    uv run deploy.py       build, deploy, and print how to verify it

Create the secret first (README, step 1). `cdk.json` points the cdk command at this file.
When the cdk command runs it, this file only describes the stack. When you run it yourself,
it describes the stack and then calls `npx aws-cdk deploy` for you.

This file follows Steps 6 and 7 of the guide. The runtime gets the NAME of the secret in
SECRET_ID, never the value, and the execution role may read that one secret. The code zip
runs on the managed Python runtime, so deploying needs neither Docker nor Finch. Callers
authenticate with SigV4 using their own AWS credentials, which is the runtime default.
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
STACK = "StrandsBoxHarness"
PROFILE = "us.anthropic.claude-haiku-5-5"  # must match MODEL_ID in agent.py
MODEL = PROFILE.split(".", 1)[1]  # the foundation model behind the profile
SECRET_ID = "agent/demo-secret"  # the secret that README step 1 creates


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
    shutil.copy(HERE / "run_box.py", BUILD)
    shutil.copytree(HERE / "box", BUILD / "box")
    # Guide Step 7: the Linux arm64 Strands Box binaries ride in the code zip, in box-bin/.
    if not (HERE / "bin-linux" / "strands-box").exists():
        raise SystemExit("bin-linux/strands-box is missing. Build it first; see the README.")
    shutil.copytree(HERE / "bin-linux", BUILD / "box-bin")
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
        runtime_name="strands_box_harness",
        agent_runtime_artifact=agentcore.AgentRuntimeArtifact.from_code_asset(
            path=str(stage()),
            runtime=agentcore.AgentCoreRuntime.PYTHON_3_12,
            entrypoint=["agent.py"],
        ),
        # Only the name of the secret. agent.py fetches the value at each request.
        environment_variables={"SECRET_ID": SECRET_ID},
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

    # Step 6 of the guide: the role may read this one secret, and nothing else.
    runtime.add_to_role_policy(
        iam.PolicyStatement(
            actions=["secretsmanager:GetSecretValue"],
            resources=[
                f"arn:aws:secretsmanager:{stack.region}:{stack.account}:secret:{SECRET_ID}-*"
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


# The cdk command sets CDK_OUTDIR when it reads this file, and then it wants the stack and
# nothing else. Without that variable a person ran the file, so deploy for them.
# The __main__ guard keeps an import of this file (for example from a test) from deploying.
if __name__ == "__main__":
    if os.environ.get("CDK_OUTDIR"):
        build_app().synth()
    else:
        deploy()
