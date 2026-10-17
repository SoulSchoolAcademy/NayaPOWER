"""AER-LIVE-8 tests: Full-State Repeatability."""
import sys
sys.path.insert(0, "drift_canary")

from aer_live8_repeatability import (
    FullState,
    RepeatabilityProof,
    control_finite_retries,
    treatment_eligible_waiting,
    verify_repeatability,
)


def good_state():
    return FullState(True, 10.0, True, True, True, True, True)


def good_proof():
    return RepeatabilityProof(True, True, True, True)


def test_full_repeatability_passes():
    assert verify_repeatability(good_state(), good_proof()) is True


def test_authority_violation_breaks():
    s = FullState(False, 10.0, True, True, True, True, True)
    assert verify_repeatability(s, good_proof()) is False


def test_zero_budget_breaks():
    s = FullState(True, 0.0, True, True, True, True, True)
    assert verify_repeatability(s, good_proof()) is False


def test_missing_proof_breaks():
    p = RepeatabilityProof(True, True, False, True)  # no debt gain
    assert verify_repeatability(good_state(), p) is False


def test_control_finite_retries_rejects():
    """CONTROL: finite retries → cannot repeat indefinitely."""
    assert control_finite_retries() is False


def test_treatment_eligible_waiting_may_repeat():
    """TREATMENT: waiting consumes no retry → repeatability possible."""
    assert treatment_eligible_waiting() is True
