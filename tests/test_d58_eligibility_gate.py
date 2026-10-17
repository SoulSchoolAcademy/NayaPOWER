"""Tests for the D58 eligibility gate (tools/d58_eligibility_gate.py).

Real asserts, no theater. The gate binds through the REAL D58 prover
(drift_canary/eligibility_proof.py); enforcement tests skip explicitly
when the mechanism is absent on this tree (dormant-off-main design).
Dormant/broken-path tests always run.
"""
import json
import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.join(os.path.dirname(_HERE), "tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)

from d58_eligibility_gate import (  # noqa: E402
    EXIT_OK, EXIT_VIOLATION, EXIT_BROKEN, run_gate,
)


def _need_mechanism():
    try:
        from drift_canary import eligibility_proof  # noqa: F401
    except ImportError:
        pytest.skip("D58 mechanism absent on this tree — enforcement needs it")


_COMPONENTS = (
    "AUTHORIZATION",
    "OUTSTANDING_WORK",
    "READY_DEPENDENCIES",
    "SCHEDULABLE_CAPACITY",
    "APPLICABLE_OPPORTUNITY",
    "CONSISTENT_ORDERING",
)

_ORIGINS = {
    "AUTHORIZATION": "law_registry",
    "OUTSTANDING_WORK": "work_queue_snapshot",
    "READY_DEPENDENCIES": "dependency_graph",
    "SCHEDULABLE_CAPACITY": "capacity_plan",
    "APPLICABLE_OPPORTUNITY": "round_log",
    "CONSISTENT_ORDERING": "ordering_service",
}


def _comp(name, status="PROVEN", origin=None, detail=None):
    return {
        "status": status,
        "detail": detail or f"{name} checked against independent source",
        "origin": origin or _ORIGINS[name],
    }


def _entry(opp="opp-1", statuses=None, flag=True, origins=None, extra_components=None):
    statuses = statuses or {}
    origins = origins or {}
    comps = {
        c: _comp(c,
                 status=statuses.get(c, "PROVEN"),
                 origin=origins.get(c))
        for c in _COMPONENTS
    }
    if extra_components:
        comps.update(extra_components)
    e = {
        "opportunity_id": opp,
        "obligation_id": "obl-A",
        "round_seq": 12,
        "components": comps,
    }
    if flag is not None:
        e["scheduler_flag"] = flag
    return e


def _write(tmp_path, opportunities):
    p = tmp_path / "d58_eligibility_manifest.json"
    p.write_text(json.dumps({"opportunities": opportunities}), encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# Always runnable: dormancy and breakage need no mechanism.
# ---------------------------------------------------------------------------

def test_dormant_no_manifest(tmp_path):
    rc = run_gate(str(tmp_path / "does-not-exist.json"))
    assert rc == EXIT_OK


def test_dormant_empty_manifest(tmp_path, capsys):
    rc = run_gate(_write(tmp_path, []))
    out = capsys.readouterr().out
    assert rc == EXIT_OK
    assert "D58_ELIGIBILITY_GATE: DORMANT" in out


def test_dormant_mechanism_absent(tmp_path, capsys, monkeypatch):
    # Even with registered opportunities, no mechanism means no verification.
    # Both the sys.modules entry AND the package attribute must be hidden:
    # `from drift_canary import eligibility_proof` binds the already-set
    # package attribute without consulting sys.modules.
    monkeypatch.setitem(sys.modules, "drift_canary.eligibility_proof", None)
    monkeypatch.delattr("drift_canary.eligibility_proof", raising=False)
    rc = run_gate(_write(tmp_path, [_entry()]))
    out = capsys.readouterr().out
    assert rc == EXIT_OK
    assert "D58_ELIGIBILITY_GATE: DORMANT" in out
    assert "not present on this tree" in out


def test_broken_corrupt_manifest(tmp_path, capsys):
    p = tmp_path / "manifest.json"
    p.write_text("{not json", encoding="utf-8")
    rc = run_gate(str(p))
    out = capsys.readouterr().out
    assert rc == EXIT_BROKEN
    assert "D58_ELIGIBILITY_GATE: BROKEN" in out


def test_broken_wrong_shape(tmp_path, capsys):
    p = tmp_path / "manifest.json"
    p.write_text(json.dumps({"opportunities": {}}), encoding="utf-8")
    rc = run_gate(str(p))
    out = capsys.readouterr().out
    assert rc == EXIT_BROKEN
    assert "D58_ELIGIBILITY_GATE: BROKEN" in out


# ---------------------------------------------------------------------------
# Enforcement: needs the real D58 prover.
# ---------------------------------------------------------------------------

def test_violation_hidden_opportunity(tmp_path, capsys):
    """Six components PROVEN but the scheduler flagged eligible=false:
    the fairness bound under-counts — blocked."""
    _need_mechanism()
    rc = run_gate(_write(tmp_path, [_entry(flag=False)]))
    out = capsys.readouterr().out
    assert rc == EXIT_VIOLATION
    assert "HIDDEN_OPPORTUNITY" in out


def test_violation_false_claim(tmp_path, capsys):
    """One component REFUTED but the scheduler flagged eligible=true:
    the fairness bound over-counts — blocked."""
    _need_mechanism()
    rc = run_gate(_write(tmp_path, [
        _entry(statuses={"AUTHORIZATION": "REFUTED"}, flag=True)]))
    out = capsys.readouterr().out
    assert rc == EXIT_VIOLATION
    assert "FALSE_CLAIM" in out


def test_violation_undetermined_counted(tmp_path, capsys):
    """UNDETERMINED never counts: an opportunity with missing evidence
    cannot carry a fairness-bound claim — blocked, with the recovery
    obligation named."""
    _need_mechanism()
    rc = run_gate(_write(tmp_path, [
        _entry(statuses={"READY_DEPENDENCIES": "UNKNOWN"}, flag=True)]))
    out = capsys.readouterr().out
    assert rc == EXIT_VIOLATION
    assert "UNDETERMINED" in out
    assert "READY_DEPENDENCIES" in out


def test_violation_tainted_origin(tmp_path, capsys):
    """Evidence backed by the scheduler's own flag is a claim, not
    evidence — the prover refuses it and the gate blocks."""
    _need_mechanism()
    rc = run_gate(_write(tmp_path, [
        _entry(origins={"AUTHORIZATION": "scheduler_flag"}, flag=True)]))
    out = capsys.readouterr().out
    assert rc == EXIT_VIOLATION
    assert "refused" in out


def test_violation_unknown_component(tmp_path, capsys):
    """A seventh component outside the six is rejected fail-closed —
    a future 'busy -> ineligible' hack cannot slip in."""
    _need_mechanism()
    rc = run_gate(_write(tmp_path, [
        _entry(extra_components={
            "BUSYNESS": _comp("AUTHORIZATION", origin="law_registry")})]))
    out = capsys.readouterr().out
    assert rc == EXIT_VIOLATION
    assert "refused" in out


def test_violation_missing_evidence_fields(tmp_path, capsys):
    """The gate refuses to invent what the manifest does not declare."""
    _need_mechanism()
    bad = _entry()
    del bad["components"]["AUTHORIZATION"]["origin"]
    rc = run_gate(_write(tmp_path, [bad]))
    out = capsys.readouterr().out
    assert rc == EXIT_VIOLATION
    assert "refuses to invent" in out


def test_violation_second_entry_still_blocks(tmp_path, capsys):
    """One clean entry does not launder a later dirty one."""
    _need_mechanism()
    rc = run_gate(_write(tmp_path, [
        _entry(opp="opp-clean", flag=True),
        _entry(opp="opp-dirty", flag=False),
    ]))
    out = capsys.readouterr().out
    assert rc == EXIT_VIOLATION
    assert "opp-dirty" in out


def test_pass_clean(tmp_path, capsys):
    _need_mechanism()
    rc = run_gate(_write(tmp_path, [_entry(flag=True)]))
    out = capsys.readouterr().out
    assert rc == EXIT_OK
    assert "D58_ELIGIBILITY_GATE: PASS" in out
    assert "CONSISTENT" in out


def test_pass_flag_not_supplied(tmp_path, capsys):
    """No scheduler flag supplied: the verdict stands on the evidence
    alone; nothing is assessed."""
    _need_mechanism()
    rc = run_gate(_write(tmp_path, [_entry(flag=None)]))
    out = capsys.readouterr().out
    assert rc == EXIT_OK
    assert "NOT_ASSESSED" in out
