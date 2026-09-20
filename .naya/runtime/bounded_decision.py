"""Vendor-neutral bounded decision contract for NayaPOWER Action 8.

This layer answers one bounded question: which candidate should be recommended?
It does not authorize, execute, or verify consequential actions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


class BoundedDecisionError(ValueError):
    pass


@dataclass(frozen=True)
class DecisionCandidate:
    candidate_id: str
    description: str
    score: float
    probability: float
    confidence: float
    eligible: bool = True

    def validate(self) -> None:
        if not self.candidate_id or not self.description:
            raise BoundedDecisionError("candidate_id and description are required")
        for name in ("score", "probability", "confidence"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise BoundedDecisionError(f"{name} must be between 0 and 1")


@dataclass(frozen=True)
class BoundedDecision:
    question_id: str
    selected_candidate: str
    score: float
    probability: float
    confidence: float
    candidate_count: int
    authority: str = "RECOMMENDATION_ONLY"

    def validate(self) -> None:
        if not self.question_id or not self.selected_candidate:
            raise BoundedDecisionError("question_id and selected_candidate are required")
        if self.authority != "RECOMMENDATION_ONLY":
            raise BoundedDecisionError("bounded decision cannot grant authority")


def choose_candidate(question_id: str, candidates: Sequence[DecisionCandidate]) -> BoundedDecision:
    """Deterministically recommend exactly one eligible candidate.

    Ranking is score first, then probability, confidence, then candidate_id.
    This is a recommendation contract only; no authorization or execution occurs.
    """
    if not question_id or not question_id.strip():
        raise BoundedDecisionError("question_id is required")
    if not candidates:
        raise BoundedDecisionError("at least one candidate is required")

    eligible: list[DecisionCandidate] = []
    for candidate in candidates:
        candidate.validate()
        if candidate.eligible:
            eligible.append(candidate)

    if not eligible:
        raise BoundedDecisionError("no eligible candidates are available")

    winner = max(
        eligible,
        key=lambda c: (c.score, c.probability, c.confidence, c.candidate_id),
    )
    decision = BoundedDecision(
        question_id=question_id,
        selected_candidate=winner.candidate_id,
        score=winner.score,
        probability=winner.probability,
        confidence=winner.confidence,
        candidate_count=len(eligible),
    )
    decision.validate()
    return decision
