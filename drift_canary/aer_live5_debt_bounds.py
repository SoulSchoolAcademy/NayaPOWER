"""AER-LIVE-5: Possible-History Fairness-Debt Bounds (spec).

Shawn's law (SN-0811, ratified 2026-10-10): Track both current debt
and historical peak across all compatible histories. A later service
reset cannot erase a possible earlier breach. Decisive test D3 catches
a final-debt-only false PASS.

Core principles:
1. Debt is tracked as (current, peak) across ALL compatible histories.
2. A service reset sets current=0 but NEVER reduces peak.
3. Verdict considers peak, not just current — a final-debt-only check
   is a false PASS if peak breached the threshold.
4. Test D3: history with peak breach but final debt 0 must FAIL.

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DebtBounds:
    """Current debt and historical peak across compatible histories."""
    current: float
    peak: float

    def __post_init__(self):
        if self.peak < self.current:
            raise ValueError("peak cannot be less than current")
        if self.current < 0 or self.peak < 0:
            raise ValueError("debt cannot be negative")


@dataclass(frozen=True)
class DebtVerdict:
    passed: bool
    # D3: True if this is a final-debt-only false PASS
    d3_false_pass: bool = False


def assess_debt(bounds: DebtBounds, threshold: float) -> DebtVerdict:
    """Assess debt against threshold using PEAK, not just current.

    A later service reset (current=0) cannot erase a possible earlier
    breach (peak > threshold).
    """
    if bounds.peak > threshold:
        # Peak breached — fail even if current is 0 (D3 catches this)
        d3 = bounds.current <= threshold
        return DebtVerdict(passed=False, d3_false_pass=d3)
    return DebtVerdict(passed=True)


def apply_service_reset(bounds: DebtBounds) -> DebtBounds:
    """Service reset: current goes to 0, peak is PRESERVED."""
    return DebtBounds(current=0.0, peak=bounds.peak)


def record_debt(bounds: DebtBounds, new_current: float) -> DebtBounds:
    """Record new debt level; peak is monotonic non-decreasing."""
    return DebtBounds(
        current=new_current,
        peak=max(bounds.peak, new_current),
    )
