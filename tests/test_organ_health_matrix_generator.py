"""Smoke tests for tools/generate_organ_health_matrix.py.

Covers: happy-path emission against offline fixtures, fail-closed refusals
(bad SHA, registry/contract drift, missing envelope field), and the CI cap.
The full adversarial battery lives in the follow-up build item
``health-matrix-tests``; this file proves the generator runs correctly on the
exact bytes being pushed.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import generate_organ_health_matrix as gen  # noqa: E402

ORGANS = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
SHA = "507d34213333a38708912d343537985e619938ac"

REGISTRY = ROOT / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json"
CONTRACT = ROOT / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json"
SCHEMA = ROOT / "BRAIN/03-KERNEL/SCHEMA/ORGAN-HEALTH-MATRIX-SCHEMA.json"


@pytest.fixture()
def repo_root(tmp_path):
    dest = tmp_path / "repo" / "BRAIN" / "03-KERNEL"
    (dest / "SCHEMA").mkdir(parents=True)
    shutil.copy(REGISTRY, dest / REGISTRY.name)
    shutil.copy(CONTRACT, dest / CONTRACT.name)
    shutil.copy(SCHEMA, dest / "SCHEMA" / SCHEMA.name)
    return tmp_path / "repo"


def _fixture(path, payload):
    Path(path).write_text(json.dumps(payload), encoding="utf-8")


def _run(repo_root, tmp_path, **over):
    checks = over.get("checks", [
        {"name": "kernel-tests", "conclusion": "success", "id": 1},
        {"name": "chain-readiness-gate", "conclusion": "success", "id": 2},
        {"name": "current-truth-resolver", "conclusion": "success", "id": 3},
    ])
    runs = over.get("runs", [])
    paths = over.get("paths", ["tests/test_know_retrieval.py", "tests/test_self_identity.py"])
    _fixture(tmp_path / "checks.json", {"check_runs": checks})
    _fixture(tmp_path / "runs.json", {"workflow_runs": runs})
    _fixture(tmp_path / "tree.json", {"paths": paths})
    out = tmp_path / "matrix.json"
    argv = ["--repo", str(repo_root), "--sha", over.get("sha", SHA),
            "--out", str(out), "--evaluator", "smoke-test",
            "--check-runs", str(tmp_path / "checks.json"),
            "--workflow-runs", str(tmp_path / "runs.json"),
            "--tree-paths", str(tmp_path / "tree.json")]
    rc = gen.main(argv)
    assert rc == 0, f"generator refused unexpectedly (rc={rc})"
    return json.loads(out.read_text(encoding="utf-8"))


def test_happy_path_emits_nine_organs_in_order(repo_root, tmp_path):
    m = _run(repo_root, tmp_path)
    assert m["schema"] == "naya/organ-health-matrix/v1"
    assert m["spec_version"] == "1"
    assert m["stamped_sha"] == SHA
    assert [o["organ"] for o in m["organs"]] == ORGANS


def test_unit_proven_only_where_organ_tests_exist(repo_root, tmp_path):
    m = _run(repo_root, tmp_path)
    by_organ = {o["organ"]: o for o in m["organs"]}
    know_unit = next(e for e in by_organ["KNOW"]["rung_evidence"] if e["rung"] == "UNIT")
    self_unit = next(e for e in by_organ["SELF"]["rung_evidence"] if e["rung"] == "UNIT")
    law_unit = next(e for e in by_organ["LAW"]["rung_evidence"] if e["rung"] == "UNIT")
    assert know_unit["status"] == "PROVEN"
    assert self_unit["status"] == "PROVEN"
    assert law_unit["status"] == "UNKNOWN"  # no organ-scoped tests -> never PASS
    # INTEGRATION is still assessed on its own evidence (chain gate covers
    # all organs) but it is NOT claimed: the organ's claim is a ladder
    # prefix (spec §4.6), so the UNIT hole caps LAW's claim at CONTRACT and
    # names UNIT as the missing rung — the hole stays visible, never hidden.
    assert by_organ["LAW"]["current_rung"] == "CONTRACT"
    assert by_organ["LAW"]["missing_rung"] == "UNIT"


def test_integration_proven_from_chain_gate(repo_root, tmp_path):
    m = _run(repo_root, tmp_path)
    for o in m["organs"]:
        ev = next(e for e in o["rung_evidence"] if e["rung"] == "INTEGRATION")
        assert ev["status"] == "PROVEN", o["organ"]
    assert m["gate_coverage"] and m["gate_coverage"][0]["covers"] == ORGANS


def test_behavioral_outcome_production_successor_fail_closed(repo_root, tmp_path):
    m = _run(repo_root, tmp_path)
    by_organ = {o["organ"]: o for o in m["organs"]}
    for organ, o in by_organ.items():
        ev = {e["rung"]: e["status"] for e in o["rung_evidence"]}
        assert ev["BEHAVIORAL"] == "UNKNOWN", organ  # no live-<organ>-proof runs
        assert ev["OUTCOME"] == "UNKNOWN", organ     # no acceptance records
        assert ev["PRODUCTION"] == "UNKNOWN_NOT_DISPATCHED", organ
        assert ev["SUCCESSOR"] == "UNKNOWN_NOT_QUALIFIED", organ
    # KNOW reached INTEGRATION; its missing rung is BEHAVIORAL with a concrete proof
    assert by_organ["KNOW"]["current_rung"] == "INTEGRATION"
    assert by_organ["KNOW"]["missing_rung"] == "BEHAVIORAL"
    assert "live-know-proof" in by_organ["KNOW"]["next_proof"]


def test_failing_required_ci_caps_every_organ_at_contract(repo_root, tmp_path):
    m = _run(repo_root, tmp_path, checks=[
        {"name": "kernel-tests", "conclusion": "failure", "id": 9},
        {"name": "chain-readiness-gate", "conclusion": "success", "id": 2},
        {"name": "current-truth-resolver", "conclusion": "success", "id": 3},
    ])
    for o in m["organs"]:
        assert o["current_rung"] == "CONTRACT", o["organ"]
        above = [e for e in o["rung_evidence"] if e["rung"] not in ("STRUCTURAL", "CONTRACT")]
        assert all(e["status"] == "CAPPED_BY_CI" for e in above), o["organ"]
        assert o["missing_rung"] == "UNIT"


def test_refuses_on_malformed_sha(repo_root, tmp_path):
    rc = gen.main(["--repo", str(repo_root), "--sha", "507d3421",
                   "--out", str(tmp_path / "m.json")])
    assert rc == 2


def test_refuses_on_registry_drift(repo_root, tmp_path):
    reg = json.loads((repo_root / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").read_text())
    reg["node_order"] = ["SELF", "LAW"]  # drift
    (repo_root / "BRAIN/03-KERNEL/0003-RUNTIME-REGISTRY-V1.json").write_text(json.dumps(reg))
    rc = gen.main(["--repo", str(repo_root), "--sha", SHA,
                   "--out", str(tmp_path / "m.json")])
    assert rc == 2


def test_refuses_on_missing_envelope_field(repo_root, tmp_path):
    con = json.loads((repo_root / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json").read_text())
    del con["nodes"]["KNOW"]["success_criteria"]
    (repo_root / "BRAIN/03-KERNEL/0004-NINE-NODE-ORGANISM-CONTRACT-V1.json").write_text(json.dumps(con))
    rc = gen.main(["--repo", str(repo_root), "--sha", SHA,
                   "--out", str(tmp_path / "m.json")])
    assert rc == 2
