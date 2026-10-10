"""Eligibility overlay tests: risk-based quarantine, both sides.

Shawn's refinement: quarantine unsafe USES, not knowledge. Every test
asserts BOTH sides where applicable: the unsafe application is blocked
AND the safe alternative / independent knowledge still flows.
"""
import sys

import pytest

sys.path.insert(0, "/tmp/errdef-branch/error_defense")
from eligibility import (
    CONSEQUENTIAL_USES,
    L0_NORMAL, L1_OBSERVE, L2_RESTRICT, L3_QUARANTINE, L4_EMERGENCY,
    EligibilityOverlay,
    IncidentRecord,
    assess_use_risk,
    check_use_eligibility,
)


def _overlay_with(lesson_id="LESSON-A", level=L3_QUARANTINE, scope=()):
    ov = EligibilityOverlay()
    inc = IncidentRecord(incident_id="INC-001", lesson_id=lesson_id,
                         detected_at="2026-10-10T17:40:00+00:00",
                         detected_by="falsification-suite",
                         reason="seeded circular evidence")
    return ov.apply_incident(inc, level, scope=scope, at="2026-10-10T17:40:00+00:00",
                             by="error-defense-coordinator")


# --- Levels -------------------------------------------------------------------

def test_l0_allows_consequential_use():
    d = check_use_eligibility("LESSON-A", "act", "s1", _overlay_with(level=L0_NORMAL))
    assert d.allowed is True and d.level == L0_NORMAL


def test_l1_allows_but_monitored():
    d = check_use_eligibility("LESSON-A", "decide", "s1", _overlay_with(level=L1_OBSERVE))
    assert d.allowed is True and d.reason == "eligible_monitored"


def test_l2_blocks_consequential_allows_read():
    ov = _overlay_with(level=L2_RESTRICT)
    blocked = check_use_eligibility("LESSON-A", "act", "s1", ov)
    allowed = check_use_eligibility("LESSON-A", "investigate", "s1", ov)
    assert blocked.allowed is False
    assert allowed.allowed is True  # read/investigate/hypothesize still flow


def test_l3_blocks_affected_scope_only():
    ov = _overlay_with(level=L3_QUARANTINE, scope=("dispatch-priority-tie",))
    blocked = check_use_eligibility("LESSON-A", "act", "dispatch-priority-tie", ov)
    outside = check_use_eligibility("LESSON-A", "act", "other-situation", ov)
    assert blocked.allowed is False
    assert outside.allowed is True  # smallest unsafe dependency contained


def test_l4_blocks_everything_read_too():
    ov = _overlay_with(level=L4_EMERGENCY)
    assert check_use_eligibility("LESSON-A", "act", "s1", ov).allowed is False
    assert check_use_eligibility("LESSON-A", "read", "s1", ov).allowed is False
    assert "escalate" in check_use_eligibility("LESSON-A", "act", "s1", ov).reason


# --- Fail-closed ----------------------------------------------------------------

def test_missing_overlay_blocks_consequential():
    d = check_use_eligibility("LESSON-A", "act", "s1", None)
    assert d.allowed is False and d.reason == "eligibility_lookup_failure"


def test_unlisted_lesson_eligible_by_default():
    # No incident history = L0. Fail-closed is for infrastructure failure
    # (overlay unavailable), not for "no news".
    d = check_use_eligibility("LESSON-NEW", "act", "s1", EligibilityOverlay())
    assert d.allowed is True and d.reason == "no_incidents_eligible_by_default"


def test_unknown_risk_blocks_consequential():
    ov = _overlay_with(level=L0_NORMAL)
    d = check_use_eligibility("LESSON-A", "act", "s1", ov, risk="UNKNOWN")
    assert d.allowed is False and d.reason == "risk_unknown_fail_closed"


# --- Per-use risk -----------------------------------------------------------------

def test_risk_formula():
    assert assess_use_risk(0.5, 10.0, 0.8, 1.0) == pytest.approx(4.0)


def test_uncalibrated_probability_stays_unknown():
    assert assess_use_risk(None, 10.0, 0.8, 1.0) == "UNKNOWN"


def test_high_per_use_risk_blocks_even_at_l0():
    ov = _overlay_with(level=L0_NORMAL)
    d = check_use_eligibility("LESSON-A", "act", "s1", ov, risk=5.0, risk_threshold=1.0)
    assert d.allowed is False and d.reason == "per_use_risk_exceeds_threshold"


# --- Both sides: unsafe blocked, safe alternative flows ----------------------------

def test_both_sides_contaminated_blocked_independent_usable():
    """One contaminated lesson, one independently supported alternative.
    The unsafe dependent action is blocked; the independent alternative
    for the same situation is allowed. This is the first-implementation
    scenario: block one, permit one."""
    ov = _overlay_with(lesson_id="LESSON-BAD", level=L3_QUARANTINE,
                       scope=("dispatch-priority-tie",))
    # contaminated lesson blocked for the affected decision
    bad = check_use_eligibility("LESSON-BAD", "act", "dispatch-priority-tie", ov)
    # independent alternative (no incident history) still usable for the
    # same situation: the quarantine contains the smallest unsafe
    # dependency, authorized work keeps flowing
    good = check_use_eligibility("LESSON-GOOD", "act", "dispatch-priority-tie", ov)
    assert bad.allowed is False
    assert good.allowed is True


def test_false_positive_safely_restored():
    """A lesson wrongly restricted is restored via revalidation receipt.
    History preserved: version increments, incident stays in the log."""
    ov = _overlay_with(level=L2_RESTRICT)
    assert check_use_eligibility("LESSON-A", "act", "s1", ov).allowed is False
    ov2 = ov.restore("LESSON-A", revalidation_ref="REVAL-777",
                     at="2026-10-10T17:45:00+00:00", by="coda-1")
    d = check_use_eligibility("LESSON-A", "act", "s1", ov2)
    assert d.allowed is True and d.level == L0_NORMAL
    assert ov2.version == ov.version + 1
    assert len(ov2.incidents) == len(ov.incidents)  # incident history preserved
    assert ov2.get("LESSON-A").revalidation_ref == "REVAL-777"


def test_restore_requires_revalidation_ref():
    ov = _overlay_with(level=L2_RESTRICT)
    with pytest.raises(ValueError, match="revalidation_ref"):
        ov.restore("LESSON-A", revalidation_ref="")


def test_overlay_version_increments_immutable():
    ov = _overlay_with(level=L1_OBSERVE)
    v1 = ov.version
    ov2 = ov.apply_incident(
        IncidentRecord("INC-003", "LESSON-A", "2026-10-10T17:50:00+00:00",
                       "x", "escalated"), L3_QUARANTINE)
    assert ov.version == v1  # original untouched
    assert ov2.version == v1 + 1
    assert ov2.get("LESSON-A").level == L3_QUARANTINE
    assert ov.get("LESSON-A").level == L1_OBSERVE


# --- Cold successor ------------------------------------------------------------------

def test_cold_successor_honors_quarantine_continues_unrelated():
    """A fresh successor with only the overlay: honors the quarantine for
    the affected situation, continues unrelated work. No inherited context."""
    ov = _overlay_with(lesson_id="LESSON-BAD", level=L3_QUARANTINE,
                       scope=("dispatch-priority-tie",))
    # affected work: blocked
    assert check_use_eligibility("LESSON-BAD", "act", "dispatch-priority-tie", ov).allowed is False
    # unrelated work with an eligible lesson: flows
    ov2 = ov.apply_incident(
        IncidentRecord("INC-004", "LESSON-OTHER", "2026-10-10T17:40:00+00:00",
                       "falsification-suite", "verified"), L0_NORMAL)
    assert check_use_eligibility("LESSON-OTHER", "act", "unrelated-task", ov2).allowed is True
    # overlay version recorded for the ACT plan to cite
    d = check_use_eligibility("LESSON-OTHER", "act", "unrelated-task", ov2)
    assert d.overlay_version == ov2.version
