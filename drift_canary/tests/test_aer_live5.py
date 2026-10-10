"""AER-LIVE-5 tests: Possible-History Fairness-Debt Bounds."""
import sys
sys.path.insert(0, "drift_canary")

from aer_live5_debt_bounds import (
    DebtBounds,
    apply_service_reset,
    assess_debt,
    record_debt,
)


def test_peak_breach_fails_despite_reset():
    """D3: peak breach + final debt 0 must FAIL (not false PASS)."""
    b = DebtBounds(current=5.0, peak=5.0)
    b = apply_service_reset(b)  # current=0, peak=5 preserved
    assert b.current == 0.0
    assert b.peak == 5.0
    verdict = assess_debt(b, threshold=3.0)
    assert verdict.passed is False
    assert verdict.d3_false_pass is True


def test_no_breach_passes():
    b = DebtBounds(current=2.0, peak=2.0)
    assert assess_debt(b, threshold=3.0).passed is True


def test_peak_monotonic():
    b = DebtBounds(current=1.0, peak=1.0)
    b = record_debt(b, 4.0)
    assert b.peak == 4.0
    b = record_debt(b, 2.0)  # current drops, peak stays
    assert b.peak == 4.0


def test_reset_preserves_peak():
    """A later service reset cannot erase a possible earlier breach."""
    b = DebtBounds(current=10.0, peak=10.0)
    b = apply_service_reset(b)
    assert b.peak == 10.0  # peak survives reset
