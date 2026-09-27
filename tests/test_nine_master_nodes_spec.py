import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/".naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json"
VALIDATOR=ROOT/"scripts/verify-nine-master-nodes.py"

def run(path):
    return subprocess.run(["python3",str(VALIDATOR),str(path)],text=True,capture_output=True)

def test_manifest_passes():
    r=run(MANIFEST); assert r.returncode==0, r.stderr+r.stdout

def test_duplicate_node_fails(tmp_path):
    d=json.loads(MANIFEST.read_text())
    d["nodes"].append(d["nodes"][0])
    p=tmp_path/"bad.json"; p.write_text(json.dumps(d))
    r=run(p); assert r.returncode!=0 and "exactly 9" in r.stderr

def test_missing_contract_owner_fails(tmp_path):
    d=json.loads(MANIFEST.read_text()); d["contract_primary_ownership"].pop("26")
    p=tmp_path/"bad.json"; p.write_text(json.dumps(d))
    r=run(p); assert r.returncode!=0 and "00-26" in r.stderr

def test_safety_invariants_are_mandatory():
    d=json.loads(MANIFEST.read_text()); text=" ".join(d["global_invariants"]["must_not"]).lower()
    assert "self-authorize" in text and "self-ratify" in text and "competing canonical intelligence store" in text
