"""The four-layer calibration architecture.

    Layer 1 — Hard safety floor:   LAW and authority gates. Non-negotiable.
    Layer 2 — Uncertainty-aware:   probability INTERVALS, never points.
    Layer 3 — Evidence-based:      bias-adjusted adjudication, label taxonomy.
    Layer 4 — Active learning:      review streams acquire missing evidence.

The calibration layer ADVISES the governed decision path. It never grants
authorization, never overrides LAW, and never treats absence of observed
harm as proof of safety.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Layer 2 — probability intervals, never point estimates
# ---------------------------------------------------------------------------

EVIDENCE_HIGH = "HIGH"
EVIDENCE_MEDIUM = "MEDIUM"
EVIDENCE_LOW = "LOW"
EVIDENCE_INSUFFICIENT = "INSUFFICIENT_DATA"


@dataclass(frozen=True)
class RiskInterval:
    """A plausible range for P(material error), with evidence quality.

    Display form: "0.2%–8%, evidence quality LOW". A point estimate is a
    lie with formatting when the evidence cannot support it.
    """
    low: float
    high: float
    evidence_quality: str = EVIDENCE_LOW

    def __post_init__(self):
        if not 0.0 <= self.low <= self.high <= 1.0:
            raise ValueError("require 0 <= low <= high <= 1")
        if self.evidence_quality not in (
                EVIDENCE_HIGH, EVIDENCE_MEDIUM, EVIDENCE_LOW,
                EVIDENCE_INSUFFICIENT):
            raise ValueError("unknown evidence quality")

    def display(self) -> str:
        return (f"{self.low:.1%}–{self.high:.1%}, "
                f"evidence quality {self.evidence_quality}")

    def is_actionable(self) -> bool:
        """An interval is actionable only when evidence is sufficient to
        bound it. INSUFFICIENT_DATA intervals advise caution, not action."""
        return self.evidence_quality != EVIDENCE_INSUFFICIENT


def rule_of_three_upper_bound(n_trials: int, observed_failures: int = 0) -> float:
    """95% upper bound on failure rate with zero observed failures ≈ 3/n.

    Zero failures in 100 trials does NOT justify claiming P(failure) = 0;
    it justifies claiming P(failure) < ~3% under binomial assumptions.
    Correlated or cherry-picked trials invalidate the bound — the caller
    must attest representativeness separately.
    """
    if observed_failures != 0:
        raise ValueError("rule of three applies to zero observed failures")
    if n_trials < 1:
        raise ValueError("n_trials must be >= 1")
    return 3.0 / n_trials


# ---------------------------------------------------------------------------
# Layer 3 — adjudication label taxonomy
# ---------------------------------------------------------------------------

CONFIRMED_MATERIAL_ERROR = "CONFIRMED_MATERIAL_ERROR"
CONFIRMED_VALID = "CONFIRMED_VALID"
CONTESTED = "CONTESTED"            # qualified reviewers disagree
INDETERMINATE = "INDETERMINATE"    # evidence cannot settle the case
CENSORED = "CENSORED"              # outcome prevented / unobservable
NOT_REVIEWED = "NOT_REVIEWED"      # no adequate adjudication occurred

_LABELS = (CONFIRMED_MATERIAL_ERROR, CONFIRMED_VALID, CONTESTED,
           INDETERMINATE, CENSORED, NOT_REVIEWED)


def is_negative_evidence(label: str) -> bool:
    """Only CONFIRMED_VALID counts as evidence the resolution was right.

    NOT_REVIEWED, INDETERMINATE, and CENSORED are NEVER negative evidence.
    Unreviewed cases must never automatically become 'valid' examples —
    that is how biased history becomes permanent machine law.
    """
    if label not in _LABELS:
        raise ValueError(f"unknown label {label!r}")
    return label == CONFIRMED_VALID


@dataclass(frozen=True)
class Adjudication:
    label: str
    reviewer: str
    blind: bool                     # was scoring blind to treatment?
    evidence_refs: tuple[str, ...] = ()
    disagreement_note: str = ""     # preserved when reviewers disagree


# ---------------------------------------------------------------------------
# Layer 4 — review streams (who gets reviewed, and why)
# ---------------------------------------------------------------------------

RISK_TRIGGERED = "RISK_TRIGGERED"          # 60% — consequential errors
RANDOM_AUDIT = "RANDOM_AUDIT"              # 20% — detect selection bias
UNCERTAINTY_ADVERSARIAL = "UNCERTAINTY_ADVERSARIAL"  # 20% — new failures

_STREAMS = (RISK_TRIGGERED, RANDOM_AUDIT, UNCERTAINTY_ADVERSARIAL)

# Pilot default allocation. Tunable from measured review capacity; never
# a ratified requirement.
STREAM_ALLOCATION = {
    RISK_TRIGGERED: 0.60,
    RANDOM_AUDIT: 0.20,
    UNCERTAINTY_ADVERSARIAL: 0.20,
}


@dataclass
class ReviewLedger:
    """Records WHY each challenge was or was not reviewed — the selection
    record that makes bias correction possible. Stores outcomes, never
    invents them."""
    entries: list[dict] = field(default_factory=list)

    def record(self, challenge_id: str, stream: str, reviewed: bool,
               reason: str, policy_version: str) -> None:
        if stream not in _STREAMS:
            raise ValueError(f"unknown stream {stream!r}")
        self.entries.append({
            "challenge_id": challenge_id,
            "stream": stream,
            "reviewed": reviewed,
            "reason": reason,
            "policy_version": policy_version,
        })

    def unreviewed_ids(self) -> list[str]:
        return [e["challenge_id"] for e in self.entries if not e["reviewed"]]


# ---------------------------------------------------------------------------
# Layer 1 — the hard floor (reference, not reimplementation)
# ---------------------------------------------------------------------------

def hard_floor_allows(action: str, law_verdict: str) -> bool:
    """Layer 1: LAW hard stops apply BEFORE any numeric comparison.

    A missing required authorization cannot be compensated by a low
    expected-loss score. This function is a pass-through contract: the real
    verdict always comes from LAW. Calibration output of "low risk" NEVER
    flips a LAW refusal.
    """
    if law_verdict == "REFUSE":
        return False
    if law_verdict == "ALLOW":
        return True
    raise ValueError(f"LAW verdict must be ALLOW or REFUSE, got {law_verdict!r}")
