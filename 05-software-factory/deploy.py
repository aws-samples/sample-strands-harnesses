"""Deploy the software factory to Amazon Bedrock AgentCore Runtime as a code zip.

    uv run deploy.py             # build, deploy, and name the next step
    npx aws-cdk deploy           # the same deploy, driven by the cdk command
    npx aws-cdk destroy          # remove the stack

`cdk.json` points the cdk command at this file. When the cdk command runs it, this file
only describes the stack. When you run it yourself, it describes the stack and then calls
`npx aws-cdk deploy` for you.

No container: AgentCore runs the code on its managed Python runtime, so deploying needs
neither Docker nor Finch. Callers authenticate with SigV4 using their own AWS credentials,
which is the runtime default, so there is no Cognito.
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
STACK = "SoftwareFactory"
PROFILE = "us.anthropic.claude-sonnet-5"  # must match MODEL_ID in agent.py
MODEL = PROFILE.split(".", 1)[1]  # the foundation model behind the profile
FILES = ["agent.py", "telemetry.py"]  # the runtime code, next to its dependencies


def log(message: str) -> None:
    """Report progress on stderr, which the cdk command passes through to the terminal."""
    print(f"[deploy.py] {message}", file=sys.stderr, flush=True)


def stage() -> Path:
    """Build the zip contents: the runtime files plus dependencies for linux/arm64.

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
    for name in FILES:
        shutil.copy(HERE / name, BUILD)
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
        "Factory",
        runtime_name="software_factory",
        agent_runtime_artifact=agentcore.AgentRuntimeArtifact.from_code_asset(
            path=str(stage()),
            runtime=agentcore.AgentCoreRuntime.PYTHON_3_12,
            entrypoint=["agent.py"],
        ),
        # AWS runs the OpenTelemetry collector for the runtime and writes the traces to
        # CloudWatch, where the GenAI observability pages read them. telemetry.py sends
        # its spans to that collector instead of starting an exporter of its own, and it
        # sends its metrics straight to the CloudWatch OTLP endpoint, which needs no
        # collector at all.
        tracing_enabled=True,
        environment_variables={
            "AGENT_OBSERVABILITY_ENABLED": "true",
            "FACTORY_WORKSPACE": "/tmp/factory",  # nosec B108
            "FACTORY_METRICS": "on",  # OTLP metrics to CloudWatch, the default
            "FACTORY_METRICS_SECONDS": "15",  # an invocation flushes at the end anyway
            "BYPASS_TOOL_CONSENT": "true",  # headless, so no prompt can be answered
        },
    )

    runtime.add_to_role_policy(
        iam.PolicyStatement(
            sid="TheOneModel",
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

    # Telemetry. Strands emits OpenTelemetry natively, and telemetry.py posts it to the
    # CloudWatch OTLP endpoints signed with this role: metrics to
    # https://monitoring.<region>.amazonaws.com/v1/metrics, which authorizes on
    # cloudwatch:PutMetricData, and spans to the X-Ray endpoint when no collector is set.
    # AGENT_OBSERVABILITY_ENABLED below means the runtime collector usually takes the spans,
    # so the X-Ray actions are the fallback path, not the normal one.
    runtime.add_to_role_policy(
        iam.PolicyStatement(
            sid="TelemetryToCloudWatch",
            actions=[
                "cloudwatch:PutMetricData",
                "xray:PutTraceSegments",
                "xray:PutSpans",
                "xray:PutTelemetryRecords",
            ],
            resources=["*"],  # neither action takes a resource, so it cannot be narrowed
        )
    )

    # The AWS MCP Server from the Agent Toolkit for AWS. The agent signs its calls with
    # this role, so the role needs the endpoint and read-only access to the account. Read
    # only on purpose: a factory that plans and writes code has no reason to change
    # infrastructure. Widen this when a stage must deploy what it built.
    runtime.add_to_role_policy(
        iam.PolicyStatement(
            sid="AwsMcpServer",
            actions=["aws-mcp:*"],
            resources=["*"],
        )
    )
    runtime.role.add_managed_policy(
        iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")
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
# nothing else. Without that variable a person ran the file, so deploy for them. The child
# cdk process inherits the variable, so the work happens once.
if os.environ.get("CDK_OUTDIR"):
    build_app().synth()
else:
    deploy()
