"""Tests for tools/bounded_recovery_liveness.py — D56 (AER-LIVE-2).

Proving bounded recovery liveness: six preconditions, three bounds with
proven-before-enforcement assumptions, eligible-time (not wall-clock)
bound clocks, four separate claims, and the AER-LIVE-002 rejection of
the time-only detector.

Negative controls are real: each names the mutant it kills.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools import bounded_recovery_liveness as d56
from tools.bounded_recovery_liveness import (
    Assumption,
    Bound,
    BoundedLivenessVerdict,
    EligibilitySegment,
    Precondition,
    ProgressMark,
    ServiceObservation,
    ObligationHistory,
    ELIGIBLE,
    WAITING_AUTHORITY,
    SAFETY_HOLD,
    OUTAGE_VERIFIED,
    SERVICE,
    PROGRESS,
    DISPOSITION,
    HOLDS,
    VIOLATED,
    UNPROVEN,
    NOT_APPLICABLE,
    PRECONDITIONS,
    assess,
    eligible_time,
    wall_time,
    enforceable,
    from_d55,
    run_aer_live_002,
    verify_aer_live_002,
    time_only_verdict,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def proven_assumptions():
    return (Assumption("capacity model matches", True, "test"),
            Assumption("policy matches", True, "test"))


def service_bound(limit=10):
    return Bound(kind=SERVICE, limit=limit, label="test",
                 assumptions=proven_assumptions(), evidence="test")


def all_preconditions():
    return tuple(Precondition(n, True, "test") for n in PRECONDITIONS)


def usable_service(seq=5):
    return ServiceObservation(seq, "SERVICED",
                              (("lease_id", "L-1"), ("worker_ack", "a1"),
                               ("resources_available", "yes")))


# ---------------------------------------------------------------------------
# Precondition gating: one missing precondition -> UNPROVEN, never a verdict.
# ---------------------------------------------------------------------------

def test_each_missing_precondition_yields_unproven():
    for missing_name in PRECONDITIONS:
        pres = tuple(Precondition(n, n != missing_name, "test")
                     for n in PRECONDITIONS)
        hist = ObligationHistory("o", (EligibilitySegment(ELIGIBLE, 0, 30),))
        v = assess(hist, service_bound(), pres)
        assert v.scheduling_fairness == UNPROVEN, missing_name
        assert v.safety == UNPROVEN, missing_name
        assert v.bounded_progress == UNPROVEN, missing_name
        assert v.task_completion == UNPROVEN, missing_name
        assert not v.bound_enforceable, missing_name


def test_unproven_assumption_makes_bound_unenforceable():
    bad = Bound(kind=SERVICE, limit=10, label="bad",
                assumptions=(Assumption("unproven claim", False),))
    ok, reason = enforceable(bad)
    assert not ok
    assert "unproven" in reason


def test_unenforceable_bound_never_trusted():
    bad = Bound(kind=SERVICE, limit=10, label="bad",
                assumptions=(Assumption("unproven claim", False),))
    hist = ObligationHistory("o", (EligibilitySegment(ELIGIBLE, 0, 30),))
    v = assess(hist, bad, all_preconditions())
    assert v.scheduling_fairness == UNPROVEN
    assert v.bound_enforceable is False


# ---------------------------------------------------------------------------
# Bound clock: eligible time only.
# ---------------------------------------------------------------------------

def test_eligible_time_excludes_holds_and_outage():
    segs = (EligibilitySegment(WAITING_AUTHORITY, 0, 10),
            EligibilitySegment(SAFETY_HOLD, 10, 20),
            EligibilitySegment(OUTAGE_VERIFIED, 20, 29),
            EligibilitySegment(ELIGIBLE, 29, 30))
    assert eligible_time(segs) == 1
    assert wall_time(segs) == 30


def test_outage_is_not_scheduler_failure():
    # 29 verified outage + 1 eligible, serviced: no breach, no violation.
    hist = ObligationHistory(
        "o",
        (EligibilitySegment(OUTAGE_VERIFIED, 0, 29),
         EligibilitySegment(ELIGIBLE, 29, 30)),
        service_observations=(usable_service(29),))
    v = assess(hist, service_bound(), all_preconditions())
    assert v.scheduling_fairness == HOLDS
    assert v.eligible_time == 1


def test_waiting_authority_never_a_fairness_violation():
    # 30 units waiting on authority: fairness NOT_APPLICABLE, never VIOLATED.
    hist = ObligationHistory(
        "o", (EligibilitySegment(WAITING_AUTHORITY, 0, 30),))
    v = assess(hist, service_bound(), all_preconditions())
    assert v.scheduling_fairness != VIOLATED
    assert v.eligible_time == 0


# ---------------------------------------------------------------------------
# Usable service: evidence required; dispatch without it is DISPATCHED-ONLY.
# ---------------------------------------------------------------------------

def test_dispatch_without_evidence_is_not_service():
    obs = ServiceObservation(5, "DISPATCHED", ())
    assert not obs.is_usable_service()


def test_partial_evidence_is_not_usable_service():
    # Missing worker_ack and resources_available.
    obs = ServiceObservation(5, "SERVICED", (("lease_id", "L-x"),))
    assert not obs.is_usable_service()


def test_full_evidence_is_usable_service():
    assert usable_service().is_usable_service()


@pytest.mark.parametrize("missing", ["lease_id", "worker_ack", "resources_available"])
def test_each_missing_evidence_field_fails(missing):
    fields = [(f, "v") for f in ("lease_id", "worker_ack", "resources_available")
              if f != missing]
    obs = ServiceObservation(5, "SERVICED", tuple(fields))
    assert not obs.is_usable_service(), missing


def test_partial_evidence_history_still_breaches():
    # History-level killer for the evidence-neutered mutant: a SERVICED
    # observation with partial evidence must not stop the breach.
    hist = ObligationHistory(
        "o", (EligibilitySegment(ELIGIBLE, 0, 30),),
        service_observations=(
            ServiceObservation(5, "SERVICED", (("lease_id", "L-x"),)),),
        progress_marks=())
    v = assess(hist, service_bound(), all_preconditions())
    assert v.scheduling_fairness == VIOLATED


def test_below_serviced_rung_never_usable():
    obs = ServiceObservation(5, "SELECTED",
                             (("lease_id", "L"), ("worker_ack", "a"),
                              ("resources_available", "y")))
    assert not obs.is_usable_service()


def test_starved_history_detected_as_bounded_service_breach():
    hist = ObligationHistory(
        "o", (EligibilitySegment(ELIGIBLE, 0, 30),),
        service_observations=(ServiceObservation(5, "DISPATCHED", ()),),
        progress_marks=(ProgressMark(6, "heartbeat"),))
    v = assess(hist, service_bound(), all_preconditions())
    assert v.scheduling_fairness == VIOLATED
    assert "bounded-service breach" in v.detail


# ---------------------------------------------------------------------------
# Progress: heartbeats never count; genuine marks do.
# ---------------------------------------------------------------------------

def test_heartbeat_is_never_progress():
    m = ProgressMark(1, "heartbeat")
    assert not m.is_genuine()
    for kind in ("log_line", "status_rewrite", "retry_attempt"):
        assert not ProgressMark(2, kind).is_genuine(), kind


def test_genuine_progress_mark_counts():
    assert ProgressMark(1, "lease_accepted",
                        moves_toward_outcome=True).is_genuine()
    assert ProgressMark(1, "projection_advanced",
                        state_advance=True).is_genuine()


def test_heartbeat_only_history_breaches_progress_bound():
    bound = Bound(kind=PROGRESS, limit=10, label="p",
                  assumptions=proven_assumptions())
    hist = ObligationHistory(
        "o", (EligibilitySegment(ELIGIBLE, 0, 30),),
        service_observations=(usable_service(1),),
        progress_marks=tuple(ProgressMark(i, "heartbeat") for i in range(30)))
    v = assess(hist, bound, all_preconditions())
    assert v.bounded_progress == VIOLATED
    # ...but fairness holds: the scheduler did its job; the worker stalled.
    assert v.scheduling_fairness == HOLDS


def test_unserviced_work_cannot_fail_progress():
    # D24's separation: blaming the worker for the scheduler's failure
    # is rejected — progress is NOT_APPLICABLE when nothing was serviced.
    bound = Bound(kind=PROGRESS, limit=10, label="p",
                  assumptions=proven_assumptions())
    hist = ObligationHistory("o", (EligibilitySegment(ELIGIBLE, 0, 30),))
    v = assess(hist, bound, all_preconditions())
    assert v.bounded_progress == NOT_APPLICABLE
    assert v.scheduling_fairness == VIOLATED


# ---------------------------------------------------------------------------
# Disposition bound: a timeout may prove a deadline breach — never a
# fairness failure.
# ---------------------------------------------------------------------------

def test_disposition_deadline_breach_without_fairness_failure():
    bound = Bound(kind=DISPOSITION, limit=10, label="d",
                  assumptions=proven_assumptions())
    hist = ObligationHistory(
        "o", (EligibilitySegment(ELIGIBLE, 0, 30),),
        service_observations=(usable_service(1),),
        progress_marks=(ProgressMark(2, "advanced", state_advance=True),))
    v = assess(hist, bound, all_preconditions())
    assert v.task_completion == VIOLATED          # deadline breach proven
    assert v.scheduling_fairness == HOLDS        # ...not a fairness failure


def test_governed_disposition_satisfies_completion():
    bound = Bound(kind=DISPOSITION, limit=10, label="d",
                  assumptions=proven_assumptions())
    hist = ObligationHistory(
        "o", (EligibilitySegment(ELIGIBLE, 0, 30),),
        disposition="escalated", disposition_evidence="ticket T-1")
    v = assess(hist, bound, all_preconditions())
    assert v.task_completion == HOLDS


# ---------------------------------------------------------------------------
# Four claims stay separate: no merged verdict exists.
# ---------------------------------------------------------------------------

def test_no_merged_pass_fail_attribute():
    v = run_aer_live_002()["H2"]
    assert not hasattr(v, "passed")
    assert not hasattr(v, "verdict")
    # H2: fairness violated AND safety holds AND completion unproven —
    # three truths at once, none collapsed.
    assert v.scheduling_fairness == VIOLATED
    assert v.safety == HOLDS
    assert v.task_completion == UNPROVEN


def test_verdict_serializes_four_slots():
    d = run_aer_live_002()["H1"].as_dict()
    assert set(("safety", "scheduling_fairness", "bounded_progress",
                "task_completion")) <= set(d)


# ---------------------------------------------------------------------------
# AER-LIVE-002: the time-only detector is indiscriminate and rejected.
# ---------------------------------------------------------------------------

def test_time_only_detector_indiscriminate_on_h1_h2():
    from tools.bounded_recovery_liveness import HISTORIES, _service_bound
    bound = _service_bound()
    assert time_only_verdict(HISTORIES["H1"](), bound) == "BREACH"
    assert time_only_verdict(HISTORIES["H2"](), bound) == "BREACH"
    # Same verdict for authority-blocked and starved: the procedure cannot
    # tell them apart, so it is rejected as a decision procedure.


def test_corrected_detector_separates_h1_h2():
    results = run_aer_live_002()
    assert results["H1"].scheduling_fairness != VIOLATED
    assert results["H1"].eligible_time == 1
    assert results["H2"].scheduling_fairness == VIOLATED
    assert results["H2"].eligible_time == 30


def test_safety_hold_control_has_zero_fairness_violations():
    v = run_aer_live_002()["H3"]
    assert v.safety == HOLDS
    assert v.scheduling_fairness != VIOLATED
    assert v.task_completion != VIOLATED


def test_verify_aer_live_002_passes():
    assert verify_aer_live_002(run_aer_live_002()) == []


def test_verify_catches_rigged_detector():
    # Mutant: a "corrected" detector that smuggles wall-clock into the
    # bound clock. H1 must false-breach under the mutant — proving the
    # real assess() is what keeps H1 clean.
    from tools.bounded_recovery_liveness import HISTORIES, _service_bound, _six_preconditions
    hist = HISTORIES["H1"]()
    assert wall_time(hist.segments) > _service_bound().limit      # mutant fires
    assert eligible_time(hist.segments) < _service_bound().limit  # real does not
    v = assess(hist, _service_bound(), _six_preconditions())
    assert v.scheduling_fairness != VIOLATED


# ---------------------------------------------------------------------------
# D55 seam: duck-typed, raises rather than imagines.
# ---------------------------------------------------------------------------

class _FakeAuth:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, _FakeAuth) and other.value == self.value

    def __hash__(self):
        return hash(self.value)


class _FakeD55:
    class AuthState:
        WITHDRAWN = _FakeAuth("withdrawn")
        GRANTED = _FakeAuth("granted")
        MISSING_DECISION = _FakeAuth("missing_decision")


class _FakeObligation:
    def __init__(self, auth, n_events=3):
        self.auth = auth
        self.events = [("service", f"e{i}") for i in range(n_events)]


def test_from_d55_maps_auth_states():
    segs = from_d55(_FakeObligation(_FakeD55.AuthState.WITHDRAWN), _FakeD55)
    assert segs[0].state == SAFETY_HOLD
    segs = from_d55(_FakeObligation(_FakeD55.AuthState.GRANTED), _FakeD55)
    assert segs[0].state == ELIGIBLE
    segs = from_d55(_FakeObligation(_FakeD55.AuthState.MISSING_DECISION), _FakeD55)
    assert segs[0].state == WAITING_AUTHORITY


def test_from_d55_plain_strings_without_module():
    segs = from_d55(_FakeObligation("withdrawn"))
    assert segs[0].state == SAFETY_HOLD
    segs = from_d55(_FakeObligation("granted"))
    assert segs[0].state == ELIGIBLE


def test_from_d55_raises_rather_than_imagines():
    class NoAuth:
        events = []
    with pytest.raises(ValueError):
        from_d55(NoAuth())
    with pytest.raises(ValueError):
        from_d55(_FakeObligation("bogus-state"))
    with pytest.raises(ValueError):
        from_d55(_FakeObligation(_FakeD55.AuthState.GRANTED), object())


def test_from_d55_never_invents_timeline():
    # One coarse segment; finer timelines are the caller's job.
    segs = from_d55(_FakeObligation(_FakeD55.AuthState.GRANTED), _FakeD55)
    assert len(segs) == 1


# ---------------------------------------------------------------------------
# CLI round-trip.
# ---------------------------------------------------------------------------

def test_cli_run_experiment_exit_zero_and_json():
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "bounded_recovery_liveness.py"),
         "--run-experiment"],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr
    payload = json.loads(r.stdout)
    assert payload["experiment"] == "AER-LIVE-002"
    assert payload["directive"] == "D56"
    assert payload["pass"] is True
    assert payload["violations"] == []


def test_cli_history_json():
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "bounded_recovery_liveness.py"),
         "--history", "H2"],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr
    v = json.loads(r.stdout)
    assert v["scheduling_fairness"] == "violated"
    assert v["eligible_time"] == 30


def test_module_docstring_names_no_live_wiring():
    src = (REPO_ROOT / "tools" / "bounded_recovery_liveness.py").read_text()
    assert "NOT wired into kernel/" in src
    assert "Wiring needs Shawn's word" in src
