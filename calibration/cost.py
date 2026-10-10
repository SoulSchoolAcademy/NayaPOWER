"""The cost-based decision rule for reopening.

    Reopen when Br > Cr

    Br = p * L * D + learning_value   (expected harm reduction + learning)
    Cr = review_cost                   (expected cost of review incl. delay)

Where:
    p  = calibrated probability the resolution is materially wrong
         (None when uncalibrated -> INSUFFICIENT_DATA, never invented)
    L  = loss if the error is acted upon (value units)
    D  = dependency of the proposed action on the disputed resolution [0,1]
    Cr = expected review cost including delay (value units)

When p cannot be calibrated reliably, the rule falls back to conservative
scenario bounds: evaluate Br > Cr across a PLAUSIBLE RANGE of p and report
the range of conclusions. Uncertainty increases caution, never confidence.
"""

from __future__ import annotations

from dataclasses import dataclass


INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
REOPEN = "REOPEN"
DEFER = "DEFER"


@dataclass(frozen=True)
class ReviewEconomics:
    """Inputs to the cost rule. All in consistent value units."""
    p_wrong: float | None        # calibrated P(resolution materially wrong)
    p_wrong_range: tuple[float, float] | None = None  # (low, high) when set
    loss_if_wrong: float = 0.0   # L
    dependency: float = 0.0      # D in [0, 1]
    review_cost: float = 0.0     # Cr, includes delay
    learning_value: float = 0.0  # expected future learning value

    def __post_init__(self):
        if self.p_wrong is not None and not 0.0 <= self.p_wrong <= 1.0:
            raise ValueError("p_wrong must be in [0,1] or None")
        if self.p_wrong_range is not None:
            lo, hi = self.p_wrong_range
            if not 0.0 <= lo <= hi <= 1.0:
                raise ValueError("p_wrong_range must satisfy 0<=lo<=hi<=1")
        if not 0.0 <= self.dependency <= 1.0:
            raise ValueError("dependency must be in [0,1]")


@dataclass(frozen=True)
class CostDecision:
    decision: str          # REOPEN | DEFER | INSUFFICIENT_DATA
    expected_benefit: float | None   # Br (None when insufficient data)
    review_cost: float
    reasoning: str
    # When p is a range, the verdict across the range:
    range_verdict: str | None = None  # e.g. "REOPEN across full range"


def _benefit(p: float, e: ReviewEconomics) -> float:
    return p * e.loss_if_wrong * e.dependency + e.learning_value


def decide(e: ReviewEconomics) -> CostDecision:
    """Apply the cost rule. Never invents precision.

    - Calibrated p: reopen iff Br > Cr.
    - p as range: report the verdict at both bounds. Reopen only if Br > Cr
      across the FULL range (conservative); defer only if Br <= Cr across
      the full range; otherwise INSUFFICIENT_DATA with the range reported.
    - p None and no range: INSUFFICIENT_DATA — the caller must gather
      evidence or apply hard gates, never guess.
    """
    if e.p_wrong is not None:
        br = _benefit(e.p_wrong, e)
        if br > e.review_cost:
            return CostDecision(REOPEN, br, e.review_cost,
                                f"Br={br:.2f} > Cr={e.review_cost:.2f}")
        return CostDecision(DEFER, br, e.review_cost,
                            f"Br={br:.2f} <= Cr={e.review_cost:.2f}")
    if e.p_wrong_range is not None:
        lo, hi = e.p_wrong_range
        br_lo, br_hi = _benefit(lo, e), _benefit(hi, e)
        if br_lo > e.review_cost:
            return CostDecision(
                REOPEN, None, e.review_cost,
                f"Br in [{br_lo:.2f},{br_hi:.2f}] > Cr={e.review_cost:.2f} "
                f"across full plausible range",
                range_verdict=f"REOPEN across [{lo},{hi}]")
        if br_hi <= e.review_cost:
            return CostDecision(
                DEFER, None, e.review_cost,
                f"Br in [{br_lo:.2f},{br_hi:.2f}] <= Cr={e.review_cost:.2f} "
                f"across full plausible range",
                range_verdict=f"DEFER across [{lo},{hi}]")
        return CostDecision(
            INSUFFICIENT_DATA, None, e.review_cost,
            f"Br range [{br_lo:.2f},{br_hi:.2f}] straddles Cr={e.review_cost:.2f}; "
            f"gather evidence or apply hard gates — do not guess",
            range_verdict="INCONCLUSIVE across range")
    return CostDecision(
        INSUFFICIENT_DATA, None, e.review_cost,
        "p uncalibrated and no plausible range supplied: INSUFFICIENT_DATA. "
        "Use conservative scenario bounds or LAW hard gates, never a point estimate.")
