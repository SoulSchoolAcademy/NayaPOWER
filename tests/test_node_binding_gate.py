"""Tests for the node-binding gate (GAP A enforcement)."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
GATE = ROOT / "scripts" / "check-node-bindings.py"


def run_gate(cwd: Path) -> subprocess.CompletedProcess:
    gate = cwd / "scripts" / "check-node-bindings.py"
    script = gate if gate.is_file() else GATE
    return subprocess.run(
        [sys.executable, str(script)], cwd=cwd, capture_output=True, text=True
    )


def test_gate_passes_on_current_tree():
    result = run_gate(ROOT)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "NODE-BINDING-GATE PASS" in result.stdout


def _scaffold(tmp: Path, *, drop_node: str | None = None, spec_only_without_event: bool = False):
    brain = tmp / "BRAIN" / "03-KERNEL"
    brain.mkdir(parents=True)
    nodes = [{"id": f"NAYA-KERNEL-{n}", "name": n} for n in
             ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]]
    (brain / "MANIFEST.json").write_text(json.dumps({"nodes": nodes}))
    bindings = []
    for n in ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]:
        if n == drop_node:
            continue
        b = {"node": n, "executable": f"exec-{n}", "persisted_transitions": f"store-{n}",
             "activation": "ACTIVE"}
        if n in ("LEARN", "EVOLVE"):
            b["activation"] = "SPEC_ONLY"
            if not spec_only_without_event:
                b["activation_event"] = "test event"
        bindings.append(b)
    (brain / "NODE-BINDINGS.json").write_text(json.dumps({"bindings": bindings}))
    (tmp / "scripts").mkdir(exist_ok=True)
    (tmp / "scripts" / "check-node-bindings.py").write_text(GATE.read_text())


def test_gate_fails_when_node_unbound(tmp_path):
    _scaffold(tmp_path, drop_node="VERIFY")
    result = run_gate(tmp_path)
    assert result.returncode == 1
    assert "VERIFY" in result.stdout and "no binding" in result.stdout


def test_gate_fails_when_spec_only_has_no_event(tmp_path):
    _scaffold(tmp_path, spec_only_without_event=True)
    result = run_gate(tmp_path)
    assert result.returncode == 1
    assert "activation_event" in result.stdout
