"""Regression tests for the canonical nine-node runtime binding gate."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts/check-node-runtime-bindings.py"
REGISTRY = ROOT / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"
MANIFEST = ROOT / "BRAIN/03-KERNEL/MANIFEST.json"

def run_gate() -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(GATE)], cwd=ROOT, capture_output=True, text=True)

def test_runtime_binding_gate_passes_current_tree():
    result = run_gate()
    assert result.returncode == 0, result.stdout + result.stderr
    assert "9/9 nodes" in result.stdout

def test_runtime_registry_has_exactly_manifest_nodes():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    expected = {n["name"] for n in manifest["nodes"]}
    bindings = registry["node_runtime_bindings"]
    assert expected == set(bindings)
    assert len(bindings) == 9
    for node, binding in bindings.items():
        assert binding["entrypoint"].strip(), node
        assert binding["persisted_transitions"].strip(), node
        assert binding["proof_boundary"].strip(), node

def test_registry_truth_boundary_never_equates_binding_with_proof():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    law = registry["binding_truth_rule"].lower()
    assert "binding existence is not proof" in law
    assert "production parity" in law
