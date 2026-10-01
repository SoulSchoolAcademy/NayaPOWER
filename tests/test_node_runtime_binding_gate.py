"""Regression tests for the canonical nine-node runtime binding gate."""
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GATE=ROOT/"scripts/check-node-runtime-bindings.py"; REGISTRY=ROOT/"BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"; MANIFEST=ROOT/"BRAIN/03-KERNEL/MANIFEST.json"
def test_runtime_binding_gate_passes_current_tree():
    r=subprocess.run([sys.executable,str(GATE)],cwd=ROOT,capture_output=True,text=True)
    assert r.returncode==0,r.stdout+r.stderr; assert "9/9 nodes" in r.stdout
def test_runtime_registry_has_exactly_manifest_nodes():
    m=json.loads(MANIFEST.read_text()); r=json.loads(REGISTRY.read_text()); expected={n["name"] for n in m["nodes"]}; b=r["node_runtime_bindings"]
    assert expected==set(b); assert len(b)==9
    for node,x in b.items():
        assert x["entrypoint"].strip(),node; assert x["persisted_transitions"].strip(),node; assert x["proof_boundary"].strip(),node
def test_registry_truth_boundary_never_equates_binding_with_proof():
    r=json.loads(REGISTRY.read_text()); law=r["binding_truth_rule"].lower()
    assert "binding existence is not proof" in law; assert "production parity" in law
