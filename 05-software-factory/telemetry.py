"""OpenTelemetry for every file in this chapter, sent to Amazon CloudWatch by default.

Call `start` once per process, then use `log`, `span`, `timed_stage`, and the `record_*`
functions. Every file in the chapter shares this module, so a stage that runs in the
runtime and a stage that runs on your laptop report the same names.

Nothing here is a private telemetry path. Strands emits OpenTelemetry natively: one span
per agent invocation, per event loop cycle, per model call, and per tool call, with token
usage on each one
([traces](https://strandsagents.com/docs/user-guide/sdk/observability-evaluation/traces/)).
This module configures the exporters that Strands then uses, and it adds the metrics the
factory itself owns, such as which stage ran and whether the reviewer approved.

CloudWatch takes OTLP directly, so no collector runs on your machine and none runs in the
runtime. Two endpoints matter here, and both authenticate with SigV4
([OTLP endpoints](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-OTLPEndpoint.html)):

    metrics   https://monitoring.<region>.amazonaws.com/v1/metrics   signing name monitoring
    traces    https://xray.<region>.amazonaws.com/v1/traces          signing name xray

The OpenTelemetry HTTP exporters take a `session` argument, so a requests session that
signs each POST is the whole of the AWS authentication. Metrics need
`cloudwatch:PutMetricData` and traces need `xray:PutTraceSegments` and
`xray:PutSpans`, which deploy.py grants to the execution role. Traces appear in the
CloudWatch GenAI observability pages once Transaction Search is on for the account, and
metrics appear in Query Studio one or two minutes after the first point.

Inside AgentCore Runtime, AWS runs a collector and sets the OTLP endpoint itself
([observability](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html)).
This module sends spans to that collector when it finds it, and falls back to the
CloudWatch traces endpoint when it does not. Metrics always go straight to CloudWatch,
because no collector collects them.

Logs stay on stderr on purpose. The runtime already copies stderr into CloudWatch Logs, so
a second OTLP path for logs would store every line twice.

Environment variables, and what each one changes:

    FACTORY_METRICS=off               send no metrics, for a run you do not want recorded
    FACTORY_TRACES=off                send no spans anywhere
    FACTORY_METRICS_ENDPOINT=<url>    send metrics elsewhere, such as a local collector
    FACTORY_TRACES_ENDPOINT=<url>     send spans elsewhere
    FACTORY_METRICS_SECONDS=<int>     the metric export interval, 15 by default
    OTEL_EXPORTER_OTLP_ENDPOINT=<url> a collector for spans, which then needs no signing
    AGENT_OBSERVABILITY_ENABLED=true  set by deploy.py, so the runtime collector is used
    FACTORY_TRACE_CONSOLE=true        also print spans to the console, for a local run
"""

import atexit
import logging
import os
import sys
import time
from contextlib import contextmanager

import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

SERVICE = "software-factory"

# The SigV4 signing names of the two CloudWatch OTLP endpoints. They are the names of the
# APIs behind them, which are monitoring for metrics and xray for traces.
METRIC_SIGNING_NAME = "monitoring"
TRACE_SIGNING_NAME = "xray"

# The metrics this chapter owns. Strands reports tokens and tool calls on its own spans, so
# these are the facts only the factory knows: which stage ran, how the review went, and
# what a person decided. CloudWatch turns the dots into underscores, so `factory.rounds` is
# `factory_rounds` in a query.
DURATION = "factory.stage.duration"  # seconds one stage took, by stage and outcome
CYCLES = "factory.stage.cycles"  # loop cycles one stage used
TOKENS = "factory.stage.tokens"  # tokens one stage spent, by stage and kind
RUNS = "factory.stage.runs"  # stages started, by stage and outcome
VERDICTS = "factory.review.verdicts"  # reviewer results, by verdict
ROUNDS = "factory.rounds"  # build, test and review rounds one work item needed
DECISIONS = "factory.release.decisions"  # human gate answers, by answer
EVAL_SCORE = "factory.eval.score"  # Strands Evals score, by suite and evaluator

_started = False
_provider: MeterProvider | None = None
_instruments: dict = {}


class SigV4Session(requests.Session):
    """A requests session that signs every request with SigV4 for one AWS service.

    Both OpenTelemetry HTTP exporters accept a `session`, which is why sending signed OTLP
    needs no collector and no bearer token. Only the headers given to `add_auth` are
    covered by the signature, so the signed set is host, date, and content type.
    """

    def __init__(self, service: str, region: str, credentials):
        super().__init__()
        self._auth = SigV4Auth(credentials, service, region)

    def send(self, request, **kwargs):
        signed = AWSRequest(
            method=request.method,
            url=request.url,
            data=request.body,
            headers={
                "Content-Type": request.headers.get("Content-Type", "application/x-protobuf")
            },
        )
        self._auth.add_auth(signed)
        request.headers.update(dict(signed.headers))
        return super().send(request, **kwargs)


def _aws() -> tuple[str, object | None]:
    """Return the Region and the credentials of the current session."""
    session = boto3.Session()
    return session.region_name or "us-east-1", session.get_credentials()


def _resource(role: str, region: str) -> Resource:
    """Return the resource attributes that every span and every metric point carries."""
    return Resource.create(
        {"service.name": SERVICE, "service.namespace": role, "cloud.region": region}
    )


def _start_metrics(role: str, region: str, credentials) -> None:
    """Set the global meter provider, sending OTLP metrics to CloudWatch.

    Strands reads the global meter provider, so setting it here means the metrics the SDK
    records arrive next to the metrics this file records, under one resource.
    """
    global _provider
    endpoint = os.environ.get(
        "FACTORY_METRICS_ENDPOINT", f"https://monitoring.{region}.amazonaws.com/v1/metrics"
    )
    seconds = int(os.environ.get("FACTORY_METRICS_SECONDS", "15"))
    exporter = OTLPMetricExporter(
        endpoint=endpoint,
        session=SigV4Session(METRIC_SIGNING_NAME, region, credentials),
    )
    _provider = MeterProvider(
        metric_readers=[
            PeriodicExportingMetricReader(exporter, export_interval_millis=seconds * 1000)
        ],
        resource=_resource(role, region),
    )
    metrics.set_meter_provider(_provider)

    meter = metrics.get_meter(SERVICE)
    _instruments.update(
        {
            DURATION: meter.create_histogram(DURATION, unit="s", description="stage wall time"),
            CYCLES: meter.create_histogram(CYCLES, description="agent loop cycles per stage"),
            TOKENS: meter.create_counter(TOKENS, unit="{token}", description="tokens per stage"),
            RUNS: meter.create_counter(RUNS, unit="{run}", description="stages started"),
            VERDICTS: meter.create_counter(VERDICTS, unit="{verdict}", description="reviews"),
            ROUNDS: meter.create_histogram(ROUNDS, description="rounds per work item"),
            DECISIONS: meter.create_counter(DECISIONS, unit="{answer}", description="decisions"),
            EVAL_SCORE: meter.create_histogram(EVAL_SCORE, description="eval case score"),
        }
    )
    atexit.register(flush)
    logging.getLogger(SERVICE).info(f"metrics to {endpoint} every {seconds}s")


def _start_traces(role: str, region: str, credentials) -> None:
    """Set up the Strands tracer provider and give it somewhere to export.

    StrandsTelemetry creates the provider, sets it as global, and installs the batch span
    processor. It passes any keyword argument through to the OTLP span exporter, so the
    signed session and the CloudWatch endpoint go in here and the SDK does the rest.
    """
    from opentelemetry.sdk.trace import TracerProvider

    from strands.telemetry import StrandsTelemetry

    telemetry = StrandsTelemetry(tracer_provider=TracerProvider(resource=_resource(role, region)))
    trace.set_tracer_provider(telemetry.tracer_provider)

    collector = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    if collector:
        # A collector is present, in the runtime or on this machine. It owns the credentials
        # and the destination, so export plainly and let it forward.
        telemetry.setup_otlp_exporter()
        logging.getLogger(SERVICE).info(f"spans to the collector at {collector}")
    else:
        endpoint = os.environ.get(
            "FACTORY_TRACES_ENDPOINT", f"https://xray.{region}.amazonaws.com/v1/traces"
        )
        telemetry.setup_otlp_exporter(
            endpoint=endpoint,
            session=SigV4Session(TRACE_SIGNING_NAME, region, credentials),
        )
        logging.getLogger(SERVICE).info(f"spans to {endpoint}")

    if os.environ.get("FACTORY_TRACE_CONSOLE") == "true":
        telemetry.setup_console_exporter()


def start(role: str) -> None:
    """Set up metrics, traces, and logging for this process. Safe to call twice.

    Args:
        role: the part of the chapter that runs. It becomes service.namespace on every
            metric point and every span, so runtime, cli, test, and evals stay apart.
    """
    global _started
    if _started:
        return
    _started = True

    os.environ.setdefault("OTEL_SERVICE_NAME", SERVICE)
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stderr,
        format=f"%(asctime)s {role} %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    region, credentials = _aws()
    if credentials is None:  # no credentials means no signature, so send nothing
        logging.getLogger(SERVICE).warning("no AWS credentials, so telemetry stays local")
        return
    if os.environ.get("FACTORY_METRICS", "on").lower() != "off":
        _start_metrics(role, region, credentials)
    if os.environ.get("FACTORY_TRACES", "on").lower() != "off":
        _start_traces(role, region, credentials)


def log(message: str, **fields) -> None:
    """Write one structured line, and attach the same fields to the current span."""
    pairs = " ".join(f"{k}={v}" for k, v in fields.items())
    logging.getLogger(SERVICE).info(f"{message} {pairs}".strip())
    current = trace.get_current_span()
    for key, value in fields.items():
        current.set_attribute(key, value)


def _record(name: str, value, **attributes) -> None:
    """Add one value to one instrument, if metrics are on in this process."""
    instrument = _instruments.get(name)
    if instrument is None:
        return
    if hasattr(instrument, "record"):
        instrument.record(value, attributes=attributes)
    else:
        instrument.add(value, attributes=attributes)


def record_stage(stage: str, seconds: float, cycles: int, tokens: dict, outcome: str) -> None:
    """Record one finished stage. Work item ids stay off metrics, because they are unique.

    Args:
        stage: the stage name, such as plan or review.
        seconds: wall time of the stage.
        cycles: loop cycles the agent used.
        tokens: the accumulated usage map from the agent, holding the token counts.
        outcome: ok when the stage returned, error when it raised.
    """
    _record(DURATION, seconds, stage=stage, outcome=outcome)
    _record(RUNS, 1, stage=stage, outcome=outcome)
    _record(CYCLES, cycles, stage=stage)
    for kind, key in (("input", "inputTokens"), ("output", "outputTokens")):
        if tokens.get(key):
            _record(TOKENS, tokens[key], stage=stage, kind=kind)


def record_verdict(verdict: str) -> None:
    """Record one reviewer result. The verdict is approved or revision."""
    _record(VERDICTS, 1, verdict=verdict)


def record_rounds(rounds: int, outcome: str) -> None:
    """Record how many build, test and review rounds one work item needed."""
    _record(ROUNDS, rounds, outcome=outcome)


def record_decision(answer: str) -> None:
    """Record the answer a person gave at the release gate."""
    _record(DECISIONS, 1, answer="yes" if answer.lower() in ("y", "yes") else "no")


def record_eval(suite: str, evaluator: str, score: float) -> None:
    """Record one Strands Evals score, so agent quality sits next to pipeline output."""
    _record(EVAL_SCORE, score, suite=suite, evaluator=evaluator)


def flush() -> bool:
    """Send what is buffered now, and say whether the export finished.

    Short processes end before the next export interval, so every entry point calls this.
    True means the exporters finished inside the timeout. It does not prove CloudWatch
    stored the points, which takes one or two minutes to become queryable.
    """
    sent = False
    if _provider is not None:
        sent = bool(_provider.force_flush(timeout_millis=10_000))
    provider = trace.get_tracer_provider()
    if hasattr(provider, "force_flush"):
        provider.force_flush(10_000)
    return sent


@contextmanager
def span(name: str, **attributes):
    """Run a block inside one span, so a failure is recorded on the trace."""
    tracer = trace.get_tracer(SERVICE)
    with tracer.start_as_current_span(name, attributes=attributes) as active:
        try:
            yield active
        except Exception as error:
            active.record_exception(error)
            active.set_status(trace.Status(trace.StatusCode.ERROR, str(error)))
            raise


@contextmanager
def timed_stage(stage: str, **attributes):
    """Run one stage inside a span and a timer, and record its metrics either way.

    The block receives a dict. Put `cycles` and `tokens` in it before the block ends, and
    they land on the metrics next to the duration.
    """
    result: dict = {"cycles": 0, "tokens": {}}
    started = time.monotonic()
    outcome = "ok"
    try:
        with span(f"stage.{stage}", **attributes):
            yield result
    except Exception:
        outcome = "error"
        raise
    finally:
        record_stage(
            stage,
            time.monotonic() - started,
            int(result.get("cycles") or 0),
            result.get("tokens") or {},
            outcome,
        )
