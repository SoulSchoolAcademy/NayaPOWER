"""Bridge for executing the TypeScript node logic modules under node.

The LAW / ACT / KNOW / PROVE implementations live as pure-logic TypeScript
modules (law.ts, act.ts, know.ts, prove.ts) with only relative imports. Node
>= 22 strips types natively, so the real modules execute directly — no port,
no reimplementation, no mock.

Each invocation is an independent node subprocess: no shared state, no
cross-call contamination. Slower than in-process, but every result comes from
the actual implementation file.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_FUNCTIONS_DIR = _REPO_ROOT / "supabase" / "functions"

_MODULE_FUNCTION: dict[str, tuple[str, str]] = {
    # stage -> (module path relative to functions dir, exported function)
    "LAW": ("nayanet-law-runtime/law.ts", "evaluateLaw"),
    "ACT": ("nayanet-act-runtime/act.ts", "buildActPlan"),
    "KNOW": ("nayanet-know-runtime/know.ts", "selectKnowContext"),
    "PROVE": ("nayanet-prove-runtime/prove.ts", "assessKnowProof"),
}


class TsBridgeError(RuntimeError):
    """The TypeScript module raised or the bridge itself failed."""


def _node_binary() -> str:
    """Resolve the node executable to an absolute path.

    The child process runs with a deliberately minimal environment whose PATH
    does not necessarily include node (e.g. CI runners where node lives under
    a toolcache dir). Resolving here, in the parent process with the real
    PATH, keeps the hermetic child env while guaranteeing the binary exists.
    """
    node_bin = shutil.which("node")
    if node_bin is None:
        raise TsBridgeError("node executable not found on PATH")
    return node_bin


def call_ts(stage: str, args: list, timeout_s: int = 60) -> dict:
    """Invoke an exported function of a node logic module. Returns parsed JSON.

    Raises TsBridgeError on any failure — the orchestrator records this as a
    FAILED stage, never a silent drop.
    """
    if stage not in _MODULE_FUNCTION:
        raise TsBridgeError(f"no TS binding for stage: {stage}")
    module_rel, func_name = _MODULE_FUNCTION[stage]

    script = (
        "const mod = await import(process.env.TS_MODULE);\n"
        "const args = JSON.parse(process.env.TS_ARGS);\n"
        "const fn = mod[process.env.TS_FUNC];\n"
        "if (typeof fn !== 'function') throw new Error('not a function: ' + process.env.TS_FUNC);\n"
        "const out = await fn(...args);\n"
        "console.log(JSON.stringify(out === undefined ? null : out));\n"
    )
    env = {
        "TS_MODULE": "./" + module_rel,
        "TS_FUNC": func_name,
        "TS_ARGS": json.dumps(args),
        "PATH": "/usr/bin:/bin",
    }
    try:
        proc = subprocess.run(
            [_node_binary(), "--experimental-strip-types", "--input-type=module", "-e", script],
            cwd=str(_FUNCTIONS_DIR),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired as exc:
        raise TsBridgeError(f"TS call timed out after {timeout_s}s: {stage}.{func_name}") from exc
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip().splitlines()
        # Filter node warning noise; keep the real error.
        err = next((l for l in reversed(stderr) if "Warning" not in l), proc.stderr)
        raise TsBridgeError(f"TS call failed: {stage}.{func_name}: {err[:500]}")
    try:
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError) as exc:
        raise TsBridgeError(f"TS call returned non-JSON: {stage}.{func_name}: {proc.stdout[:300]}") from exc
