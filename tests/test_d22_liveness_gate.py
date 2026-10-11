"""Tests for the D22 liveness-claims gate.

These tests run the REAL gate (subprocess, exit codes) against the REAL
drift_canary.liveness mechanism from the repo tree — no fakes, no stubs.
A sabotaged gate must fail these tests (no theater).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent


def _find_gate():
    d = TESTS_DIR
    for _ in range(6):
        cand = d / "tools" / "d22_liveness_gate.py"
        if cand.is_file():
            return cand
        d = d.parent
    raise AssertionError("d22_liveness_gate.py not found above tests dir")


GATE = _find_gate()
TOOLS_DIR = GATE.parent


def _run_gate(manifest_path, cwd=None):
    return subprocess.run(
        [sys.executable, str(GATE), "--manifest", str(manifest_path)],
        capture_output=True, text=True, cwd=cwd)


def _base_claim(**over):
    claim = {
        "id": "t-claim",
        "obligation": {
            "obligation_id": "OB-T", "revision": "r1",
            "liveness_type": "TASK_COMPLETION",
            "participants": ["KNOW", "LAW"],
            "trigger": "t", "progress_target": "done",
            "fairness_assumptions": ["weak_fairness"],
            "progress_witnesses": ["milestone-a"],
        },
        "evidence": {
            "states": {"w": {"state": "COMPLETED", "since_seq": 5}},
            "wait_for": {}, "escape_paths": {},
            "histories": {"w": [[1, "RUNNABLE"], [5, "COMPLETED"]]},
            "progress_seqs": {"w": [5]},
            "eligible_since": {"w": 1}, "opportunities": {"w": 2},
            "scheduled_others": {"w": 0},
            "fairness_holds": True,
            "witnesses": [{"workflow_id": "w", "node": "LAW",
                            "milestone": "milestone-a",
                            "evidence_ref": "ev-1", "seq": 5}],
        },
        "claimed_overall": "QUALIFIED",
    }
    claim.update(over)
    return claim


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"version": 1, "claims": claims}))
    return p


def test_seeded_manifest_passes(tmp_path):
    """The shipped manifest's claims are honest: exit 0 PASS."""
    r = _run_gate(TOOLS_DIR / "d22_liveness_claims_manifest.json")
    assert r.returncode == 0, r.stderr + r.stdout
    assert "PASS" in r.stdout


def test_pessimistic_fraud_blocked(tmp_path):
    """NOT_QUALIFIED asserted on healthy evidence is also dishonest -> 1."""
    claim = _base_claim()
    claim["claimed_overall"] = "NOT_QUALIFIED"
    # evidence is QUALIFIED-shaped: the prover disagrees -> VIOLATION
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout  # dishonest, not honest


def test_fraudulent_qualified_on_deadlock_blocked(tmp_path):
    """QUALIFIED asserted on deadlocked evidence -> exit 1 VIOLATION."""
    claim = _base_claim()
    claim["id"] = "t-fraud"
    claim["obligation"]["obligation_id"] = "OB-T-FRAUD"
    claim["obligation"]["liveness_type"] = "WORKFLOW_PROGRESS"
    claim["obligation"]["progress_witnesses"] = []
    claim["evidence"]["states"] = {
        "a": {"state": "DEADLOCK_SUSPECTED", "since_seq": 9},
        "b": {"state": "WAITING_DEPENDENCY", "since_seq": 9}}
    claim["evidence"]["wait_for"] = {"a": ["b"], "b": ["a"]}
    claim["evidence"]["histories"] = {
        "a": [[1, "RUNNABLE"], [9, "DEADLOCK_SUSPECTED"]],
        "b": [[1, "RUNNABLE"], [9, "WAITING_DEPENDENCY"]]}
    claim["evidence"]["progress_seqs"] = {"a": [], "b": []}
    claim["evidence"]["eligible_since"] = {"a": 1, "b": 1}
    claim["evidence"]["opportunities"] = {"a": 5, "b": 5}
    claim["evidence"]["scheduled_others"] = {"a": 0, "b": 0}
    claim["evidence"]["witnesses"] = []
    claim["claimed_overall"] = "QUALIFIED"  # the fraud
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


def test_witness_fraud_blocked(tmp_path):
    """QUALIFIED asserted while required witnesses are missing -> exit 1."""
    claim = _base_claim()  # requires milestone-a
    claim["evidence"]["witnesses"] = []  # ...but produces none
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout


def test_type_verdict_mismatch_blocked(tmp_path):
    """A wrong claimed_type_verdicts entry -> exit 1."""
    claim = _base_claim()
    claim["claimed_type_verdicts"] = {"TASK_COMPLETION": "VIOLATED"}
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout


def test_empty_manifest_is_dormant_not_green(tmp_path):
    """Zero claims -> exit 0 DORMANT, explicitly named (never false green)."""
    r = _run_gate(_write_manifest(tmp_path, []))
    assert r.returncode == 0, r.stderr + r.stdout
    assert "DORMANT" in r.stdout


def test_corrupt_manifest_fails_closed(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json")
    r = _run_gate(p)
    assert r.returncode == 2, r.stderr + r.stdout
    assert "BROKEN" in r.stdout


def test_unknown_state_fails_closed(tmp_path):
    claim = _base_claim()
    claim["evidence"]["states"]["w"]["state"] = "VIBING"
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_wait_for_bare_string_fails_closed(tmp_path):
    """A bare string wait_for would iterate as characters — fail closed."""
    claim = _base_claim()
    claim["evidence"]["wait_for"] = {"w": "COMPLETED"}
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_duplicate_claim_ids_fail_closed(tmp_path):
    r = _run_gate(_write_manifest(tmp_path, [_base_claim(), _base_claim()]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_mechanism_missing_fails_closed(tmp_path):
    """Gate copied to a tree without drift_canary -> exit 2, never pass."""
    bare = tmp_path / "bare" / "tools"
    bare.mkdir(parents=True)
    shutil.copy(GATE, bare / "d22_liveness_gate.py")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"version": 1, "claims": [_base_claim()]}))
    r = subprocess.run(
        [sys.executable, str(bare / "d22_liveness_gate.py"),
         "--manifest", str(manifest)],
        capture_output=True, text=True)
    assert r.returncode == 2, r.stderr + r.stdout
    assert "BROKEN" in r.stdout


def test_mechanism_missing_with_no_claims_is_dormant(tmp_path):
    """No claims + no mechanism -> DORMANT (nothing to judge), not BROKEN."""
    bare = tmp_path / "bare" / "tools"
    bare.mkdir(parents=True)
    shutil.copy(GATE, bare / "d22_liveness_gate.py")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"version": 1, "claims": []}))
    r = subprocess.run(
        [sys.executable, str(bare / "d22_liveness_gate.py"),
         "--manifest", str(manifest)],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "DORMANT" in r.stdout
