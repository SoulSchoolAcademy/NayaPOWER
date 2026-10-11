"""
quality_gate.py — Machine law: enforce the 9.0 delivery floor.

No deliverable below 9/10 reaches Shawn. This gate validates a
delivery scorecard BEFORE delivery. Missing scorecard = no delivery.
"""
from __future__ import annotations

from dataclasses import dataclass, field


DELIVERY_FLOOR = 9.0
AAA_TARGET = 9.5


@dataclass
class Scorecard:
    """A delivery scorecard. All fields required — no partial scorecards."""
    what: str                      # what was delivered
    evidence: str                  # proof it works (links, SHAs, test counts)
    scores: dict                   # dimension -> 0-10 score
    weights: dict                  # dimension -> weight (must sum to 1.0)
    weakest_point: str             # honest: what is not a 10 and why
    verified_by: str               # who/what verified (independent of builder)

    def weighted_total(self) -> float:
        if abs(sum(self.weights.values()) - 1.0) > 0.001:
            raise ValueError("weights must sum to 1.0")
        if set(self.scores) != set(self.weights):
            raise ValueError("scores and weights must cover the same dimensions")
        return sum(self.scores[d] * self.weights[d] for d in self.scores)

    def min_dimension(self) -> float:
        return min(self.scores.values())


@dataclass
class QualityResult:
    passed: bool
    total: float
    floor: float
    reasons: list = field(default_factory=list)


def check_delivery(scorecard: Scorecard | None, builder_id: str,
                   law12_state: dict | None = None,
                   law12_proof_time: dict | None = None) -> QualityResult:
    reasons: list[str] = []
    if scorecard is None:
        return QualityResult(False, 0.0, DELIVERY_FLOOR,
                             ["No scorecard. No receipt, no delivery."])
    # Law 12 (ACTIVE): a scorecard is a proof about specific code under a
    # specific rubric. law12_proof_time holds the world values when the
    # scorecard was made (supplied by whoever scored). Current state
    # auto-resolves when not supplied, so the check fires with proof-time
    # alone — no second opt-in. If the scored code moved, the scorecard is
    # STALE — rescore, don't deliver on history.
    # (Without law12_proof_time, staleness cannot be established — the check
    # is skipped. Precise, never speculative.)
    if law12_proof_time is not None:
        from .proof_expiry import (
            proof_from_scorecard, validate_proof, resolve_current_state,
        )
        if law12_state is None:
            law12_state = resolve_current_state()
        proof = proof_from_scorecard(
            scorecard,
            source_sha=law12_proof_time.get("source_sha", ""),
            policy_ref=law12_proof_time.get("policy_ref", ""),
        )
        validation = validate_proof(proof, law12_state)
        if not validation.is_current:
            reasons.append(
                f"Law 12: scorecard stale — {validation.reason()}. "
                "Rescore against current code; do not deliver on expired proof."
            )
            return QualityResult(False, 0.0, DELIVERY_FLOOR, reasons)
    try:
        total = scorecard.weighted_total()
    except ValueError as e:
        return QualityResult(False, 0.0, DELIVERY_FLOOR, [f"Invalid scorecard: {e}"])
    if not scorecard.evidence.strip():
        reasons.append("No evidence cited.")
    if not scorecard.weakest_point.strip():
        reasons.append("No weakest point named — dishonest scorecard.")
    if scorecard.verified_by.strip().lower() == builder_id.strip().lower():
        reasons.append("Builder cannot be the sole verifier — independent verification required.")
    # Nine-floor doctrine: per-dimension minimum, never averaged.
    low = [d for d, s in scorecard.scores.items() if s < DELIVERY_FLOOR]
    if low:
        reasons.append(f"Dimensions below floor {DELIVERY_FLOOR}: {low}. A 10 never covers a 7.")
    if total < DELIVERY_FLOOR:
        reasons.append(f"Total {total:.2f} below delivery floor {DELIVERY_FLOOR}. Goes back for repair.")
    return QualityResult(passed=not reasons, total=total,
                         floor=DELIVERY_FLOOR, reasons=reasons)
