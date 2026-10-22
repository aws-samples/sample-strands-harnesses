"""Start Strands Box with the probe as its workload, as `op run -- strands-box run` does in the guide.

    export AGENT_SECRET_VALUE=...   # on a laptop, the vendor tool's job
    uv run run_box.py               # run the box once and check what it reports

The same function runs on the laptop and in AgentCore Runtime. In Runtime, agent.py calls it after
load_secret() has put the secret in os.environ, so Strands Box reads it from there, exactly as it
reads the variable that `op run` sets.

box.toml is written per run because a box needs absolute paths: the Python that runs the probe,
its install tree, and a fresh state directory. The policy and the probe are fixed files in box/.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent.resolve()
NAME = "AGENT_SECRET_VALUE"
# The laptop uses the macOS release; the Runtime code zip carries the Linux arm64 build in box-bin/.
BIN = HERE / ("bin-macos" if platform.system() == "Darwin" else "box-bin")

# Python's C extensions on Amazon Linux link these system libraries. The box refuses a grant on
# all of /usr/lib64 and refuses symlinks, so each is granted as its real file. macOS needs none.
LINUX_LIBS = ["libz.so.1", "libssl.so.3", "libcrypto.so.3", "libffi.so.8"]
SYSTEM_LIBS = [
    os.path.realpath(f"/usr/lib64/{lib}") for lib in LINUX_LIBS
    if platform.system() == "Linux" and os.path.exists(f"/usr/lib64/{lib}")
]

BOX_TOML = """\
name = "secret-probe"
box_dir = "{state}"
policy = "policy.dw"

[agent]
command = ["{python}", "{probe}"]
workspace = "{work}"

[agent.filesystem]
read = [{read}]
read_file = ["{probe}"]
# The sandbox maps code only from exec grants: Python's C extensions, and on Linux the system
# libraries they link (libz, libssl, libcrypto).
exec = [{exec}]

# The real value comes from AGENT_SECRET_VALUE in this process. The probe gets a placeholder in the
# same variable, and the gateway puts the real value in x-api-key only on requests to httpbin.org.
[egress.api]
destinations = ["httpbin.org"]
secret = {{ ref = "env://{name}", header = "x-api-key" }}
"""


def box_binary(root: Path) -> Path:
    """Return the box program. On Linux, copy the binaries out, because a zip may drop exec bits."""
    if platform.system() == "Darwin":
        return BIN / "box"
    bin_dir = root / "bin"
    shutil.copytree(BIN, bin_dir)
    for f in bin_dir.iterdir():
        f.chmod(0o755)
    return bin_dir / "strands-box"


def run_probe(timeout: int = 180) -> dict:
    """Run the probe in a fresh box and return its report, plus the box's exit code."""
    if not os.environ.get(NAME):
        return {"ok": False, "error": f"{NAME} is not set in the environment that starts the box"}
    root = Path(os.path.realpath(tempfile.mkdtemp(prefix="box-")))
    cfg, work = root / "cfg", root / "work"
    cfg.mkdir()
    work.mkdir()
    shutil.copy(HERE / "box" / "policy.dw", cfg / "policy.dw")
    probe = work / "probe.py"
    shutil.copy(HERE / "box" / "probe.py", probe)
    prefix = os.path.realpath(sys.base_prefix)
    (cfg / "box.toml").write_text(BOX_TOML.format(
        state=root / "state",
        python=os.path.realpath(sys.executable),
        read=", ".join(f'"{p}"' for p in [prefix]),
        exec=", ".join(f'"{p}"' for p in [f"{prefix}/lib", *SYSTEM_LIBS]),
        probe=probe,
        work=work,
        name=NAME,
    ))
    # Runtime sets no HOME, and Strands Box needs one; the laptop keeps its own.
    env = dict(os.environ)
    if not env.get("HOME"):
        (root / "home").mkdir()
        env["HOME"] = str(root / "home")
    done = subprocess.run(
        [str(box_binary(root)), "run", "--config", str(cfg / "box.toml")],
        capture_output=True, text=True, timeout=timeout, env=env,
    )
    report: dict = {"exit_code": done.returncode}
    for line in reversed(done.stdout.splitlines()):
        if line.startswith("{"):
            report.update(json.loads(line))
            break
    report["ok"] = report.get("env_is_placeholder") is True and report.get("api_saw") == "[REDACTED]"
    if not report["ok"]:
        report["stderr_tail"] = done.stderr[-3000:]  # box diagnostics; the probe never prints the value
        if platform.system() == "Linux":
            ext = sorted(Path(prefix, "lib").glob("python3*/lib-dynload/_ssl*.so"))
            if ext:
                report["ssl_links"] = subprocess.run(["ldd", str(ext[0])], capture_output=True,
                                                     text=True).stdout
    shutil.rmtree(root, ignore_errors=True)
    return report


if __name__ == "__main__":
    result = run_probe()
    print(json.dumps(result, indent=2))
    print("\nPASS: the agent saw only a placeholder, and the API got the real secret."
          if result["ok"] else "\nFAIL")
    sys.exit(0 if result["ok"] else 1)
