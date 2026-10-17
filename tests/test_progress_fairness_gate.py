"""Tests for the D23/D24/D25 progress & fairness claims gate.

These tests run the REAL gate (subprocess, exit codes) against the REAL
drift_canary progress/fairness/strong_fairness mechanisms from the repo
tree — no fakes, no stubs. A sabotaged gate must fail these tests
(no theater).
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
        cand = d / "tools" / "progress_fairness_gate.py"
        if cand.is_file():
            return cand
        d = d.parent
    raise AssertionError("progress_fairness_gate.py not found above tests dir")


GATE = _find_gate()
TOOLS_DIR = GATE.parent


def _run_gate(manifest_path, cwd=None):
    return subprocess.run(
        [sys.executable, str(GATE), "--manifest", str(manifest_path)],
        capture_output=True, text=True, cwd=cwd)


def _write_manifest(tmp_path, claims):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"version": 1, "claims": claims}))
    return p


# ---------------------------------------------------------------------------
# D23 claim builders
# ---------------------------------------------------------------------------

def _d23_claim(**over):
    claim = {
        "id": "t-d23",
        "type": "d23_progress_rank",
        "transition": {
            "kind": "DISCHARGE",
            "prev_ranks": [5],
            "next_ranks": [],
            "retries_before": 0,
            "retries_after": 0,
            "discharged": True,
        },
        "claimed": {"proof_progress": True, "termination_progress": True},
    }
    claim.update(over)
    return claim


# ---------------------------------------------------------------------------
# D24 claim builders
# ---------------------------------------------------------------------------

def _d24_event(rung, seq=1, evidence=None):
    return {
        "obligation_id": "OB-T",
        "workflow_id": "w1",
        "seq": seq,
        "rung": rung,
        "eligible": True,
        "evidence": evidence or {},
    }


_FULL_SERVICE_EVIDENCE = {
    "lease_id": "L1", "worker_ack": "A1", "resources_available": "R1",
}


def _d24_claim(**over):
    claim = {
        "id": "t-d24",
        "type": "d24_three_truths",
        "contract": {
            "obligation_id": "OB-T",
            "revision": "r1",
            "standard": "WEAK",
            "eligibility_predicate": "eligible",
            "service_predicate": "serviced",
        },
        "events": [_d24_event("SERVICED", evidence=_FULL_SERVICE_EVIDENCE)],
        "assessment": {
            "debt_threshold": 3,
            "serviced_rounds": 1,
            "advanced_rounds": 1,
            "rank_decreasing": True,
        },
        "claimed": {
            "fair_chance": True,
            "advanced_on_service": True,
            "converging": True,
            "composition": "CONDITIONAL_LIVENESS",
        },
    }
    claim.update(over)
    return claim


# ---------------------------------------------------------------------------
# D25 claim builders
# ---------------------------------------------------------------------------

def _d25_claim(**over):
    claim = {
        "id": "t-d25",
        "type": "d25_standard_selection",
        "situation": "FLICKERING_SHARED_RESOURCE",
        "claimed_standard": "STRONG",
    }
    claim.update(over)
    return claim


# ---------------------------------------------------------------------------
# Baseline: shipped manifest is DORMANT, empty manifest is DORMANT
# ---------------------------------------------------------------------------

def test_shipped_manifest_is_dormant(tmp_path):
    r = _run_gate(TOOLS_DIR / "progress_fairness_claims_manifest.json")
    assert r.returncode == 0, r.stderr + r.stdout
    assert "DORMANT" in r.stdout


def test_empty_manifest_is_dormant_not_green(tmp_path):
    r = _run_gate(_write_manifest(tmp_path, []))
    assert r.returncode == 0, r.stderr + r.stdout
    assert "DORMANT" in r.stdout


# ---------------------------------------------------------------------------
# D23 — honest claims pass
# ---------------------------------------------------------------------------

def test_d23_honest_discharge_passes(tmp_path):
    r = _run_gate(_write_manifest(tmp_path, [_d23_claim()]))
    assert r.returncode == 0, r.stderr + r.stdout
    assert "PASS" in r.stdout


def test_d23_honest_heartbeat_no_progress_passes(tmp_path):
    claim = _d23_claim()
    claim["transition"] = {
        "kind": "HEARTBEAT", "prev_ranks": [5], "next_ranks": [5],
        "retries_before": 0, "retries_after": 0, "discharged": False,
    }
    claim["claimed"] = {"proof_progress": False, "termination_progress": False}
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 0, r.stderr + r.stdout


# ---------------------------------------------------------------------------
# D23 — gaming the measure is blocked
# ---------------------------------------------------------------------------

def test_d23_heartbeat_claimed_as_proof_blocked(tmp_path):
    """The classic fraud: activity counted as progress -> exit 1."""
    claim = _d23_claim()
    claim["transition"] = {
        "kind": "HEARTBEAT", "prev_ranks": [5], "next_ranks": [5],
        "retries_before": 0, "retries_after": 0, "discharged": False,
    }
    claim["claimed"] = {"proof_progress": True, "termination_progress": False}
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


def test_d23_escalation_claimed_as_completion_blocked(tmp_path):
    """Escalation transfers responsibility; it never completes the
    original objective -> claiming proof progress is fraud, exit 1."""
    claim = _d23_claim()
    claim["transition"] = {
        "kind": "ESCALATION", "prev_ranks": [5], "next_ranks": [5],
        "retries_before": 0, "retries_after": 0, "discharged": False,
    }
    claim["claimed"] = {"proof_progress": True, "termination_progress": True}
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


def test_d23_reassignment_claimed_as_progress_blocked(tmp_path):
    claim = _d23_claim()
    claim["transition"] = {
        "kind": "REASSIGNMENT", "prev_ranks": [5], "next_ranks": [5],
        "retries_before": 0, "retries_after": 0, "discharged": False,
    }
    claim["claimed"] = {"proof_progress": True, "termination_progress": False}
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


def test_d23_pessimistic_fraud_blocked(tmp_path):
    """Denying real progress is also dishonest -> exit 1."""
    claim = _d23_claim()  # DISCHARGE, honestly (True, True)
    claim["claimed"] = {"proof_progress": False, "termination_progress": True}
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout


# ---------------------------------------------------------------------------
# D24 — honest claims pass
# ---------------------------------------------------------------------------

def test_d24_honest_conditional_liveness_passes(tmp_path):
    r = _run_gate(_write_manifest(tmp_path, [_d24_claim()]))
    assert r.returncode == 0, r.stderr + r.stdout
    assert "PASS" in r.stdout


# ---------------------------------------------------------------------------
# D24 — opportunity/accomplishment conflation is blocked
# ---------------------------------------------------------------------------

def test_d24_dispatch_only_claimed_accomplished_blocked(tmp_path):
    """DISPATCHED-only evidence asserted as advanced_on_service: the
    opportunity is not the accomplishment -> exit 1."""
    claim = _d24_claim()
    claim["events"] = [_d24_event("DISPATCHED")]  # no usable service
    claim["assessment"] = {
        "debt_threshold": 3, "serviced_rounds": 0,
        "advanced_rounds": 0, "rank_decreasing": False,
    }
    # the fraud: claiming accomplishment on selection/dispatch alone
    claim["claimed"] = {
        "fair_chance": True, "advanced_on_service": True,
        "converging": True, "composition": "CONDITIONAL_LIVENESS",
    }
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


def test_d24_served_but_stalled_claimed_liveness_blocked(tmp_path):
    """Fairly served but stalled: adequate service never produced a
    verified transition -> LIVENESS_UNPROVEN, not CONDITIONAL -> exit 1."""
    claim = _d24_claim()
    claim["assessment"] = {
        "debt_threshold": 3, "serviced_rounds": 2,
        "advanced_rounds": 0, "rank_decreasing": False,
    }
    claim["claimed"]["composition"] = "CONDITIONAL_LIVENESS"
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


def test_d24_false_starvation_claim_blocked(tmp_path):
    """fair_chance=false asserted while debt is 0 (worker failed, not the
    scheduler): the prover disagrees -> exit 1."""
    claim = _d24_claim()  # debt 0 < threshold 3 -> fair_chance True
    claim["claimed"]["fair_chance"] = False
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


# ---------------------------------------------------------------------------
# D25 — honest claims pass
# ---------------------------------------------------------------------------

def test_d25_honest_strong_for_flicker_passes(tmp_path):
    r = _run_gate(_write_manifest(tmp_path, [_d25_claim()]))
    assert r.returncode == 0, r.stderr + r.stdout
    assert "PASS" in r.stdout


def test_d25_honest_neither_for_missing_auth_passes(tmp_path):
    claim = _d25_claim()
    claim["situation"] = "HUMAN_AUTH_MISSING"
    claim["claimed_standard"] = "NEITHER"
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 0, r.stderr + r.stdout


def test_d25_honest_assumptions_passes(tmp_path):
    claim = _d25_claim()
    claim["assumptions_evidence"] = {
        a: f"evidence for {a}" for a in (
            "PERSISTENT_IDENTITY", "GENUINE_ENABLING", "RECURRING_OPPORTUNITY",
            "SCHEDULER_OBSERVABILITY", "IMPLEMENTABILITY",
            "STRONGLY_FAIR_SELECTION", "PROGRESS_AFTER_SERVICE",
            "SAFETY_PRESERVATION")
    }
    claim["claimed_assumptions_ok"] = True
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 0, r.stderr + r.stdout


# ---------------------------------------------------------------------------
# D25 — wrong standard is blocked
# ---------------------------------------------------------------------------

def test_d25_weak_where_strong_required_blocked(tmp_path):
    """FLICKERING_SHARED_RESOURCE with WEAK: weak fairness permits
    indefinite postponement of intermittently enabled work -> exit 1."""
    claim = _d25_claim()
    claim["claimed_standard"] = "WEAK"
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


def test_d25_fairness_as_permission_excuse_blocked(tmp_path):
    """HUMAN_AUTH_MISSING with STRONG: fairness never creates permission,
    LAW remains the gate -> exit 1."""
    claim = _d25_claim()
    claim["situation"] = "HUMAN_AUTH_MISSING"
    claim["claimed_standard"] = "STRONG"
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


def test_d25_missing_assumption_claimed_ok_blocked(tmp_path):
    claim = _d25_claim()
    claim["assumptions_evidence"] = {"PERSISTENT_IDENTITY": "id stable"}
    claim["claimed_assumptions_ok"] = True  # seven assumptions missing
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 1, r.stderr + r.stdout
    assert "VIOLATION" in r.stdout


# ---------------------------------------------------------------------------
# Fail-closed paths
# ---------------------------------------------------------------------------

def test_corrupt_manifest_fails_closed(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text("{not json")
    r = _run_gate(p)
    assert r.returncode == 2, r.stderr + r.stdout
    assert "BROKEN" in r.stdout


def test_unknown_claim_type_fails_closed(tmp_path):
    claim = _d23_claim()
    claim["type"] = "d99_mind_reading"
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_unknown_transition_kind_fails_closed(tmp_path):
    claim = _d23_claim()
    claim["transition"]["kind"] = "VIBING"
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_unknown_rung_fails_closed(tmp_path):
    claim = _d24_claim()
    claim["events"] = [_d24_event("TELEPORTED")]
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_unknown_situation_fails_closed(tmp_path):
    claim = _d25_claim()
    claim["situation"] = "MONDAY_MORNING"
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_unknown_assumption_id_fails_closed(tmp_path):
    claim = _d25_claim()
    claim["assumptions_evidence"] = {"GOOD_VIBES": "trust me"}
    claim["claimed_assumptions_ok"] = True
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_duplicate_claim_ids_fail_closed(tmp_path):
    r = _run_gate(_write_manifest(tmp_path, [_d23_claim(), _d23_claim()]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_mixed_obligation_events_fail_closed(tmp_path):
    claim = _d24_claim()
    ev = _d24_event("SERVICED", evidence=_FULL_SERVICE_EVIDENCE)
    ev["obligation_id"] = "OB-OTHER"  # debt belongs to the obligation id
    claim["events"] = [ev]
    r = _run_gate(_write_manifest(tmp_path, [claim]))
    assert r.returncode == 2, r.stderr + r.stdout


def test_mechanism_missing_fails_closed(tmp_path):
    """Gate copied to a tree without drift_canary -> exit 2, never pass."""
    bare = tmp_path / "bare" / "tools"
    bare.mkdir(parents=True)
    shutil.copy(GATE, bare / "progress_fairness_gate.py")
    manifest = _write_manifest(tmp_path, [_d23_claim()])
    r = subprocess.run(
        [sys.executable, str(bare / "progress_fairness_gate.py"),
         "--manifest", str(manifest)],
        capture_output=True, text=True)
    assert r.returncode == 2, r.stderr + r.stdout
    assert "BROKEN" in r.stdout


def test_mechanism_missing_with_no_claims_is_dormant(tmp_path):
    """No claims + no mechanism -> DORMANT (nothing to judge), not BROKEN."""
    bare = tmp_path / "bare" / "tools"
    bare.mkdir(parents=True)
    shutil.copy(GATE, bare / "progress_fairness_gate.py")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"version": 1, "claims": []}))
    r = subprocess.run(
        [sys.executable, str(bare / "progress_fairness_gate.py"),
         "--manifest", str(manifest)],
        capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    assert "DORMANT" in r.stdout
