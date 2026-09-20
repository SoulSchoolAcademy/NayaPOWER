"""Post-execution quality gate for the Naya Power continuous loop.

Verification answers: "Did it happen?"
Scorecard + OSCAR answer: "Is it good enough to promote and continue?"
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from naya_power_runtime import EvidenceState, MissionState


MINIMUM_RESPONSIBLE_SCORE = 9.5


@dataclass(frozen=True)
class Scorecard:
    """Quality assessment; numeric score never overrides hard constitutional gates."""

    dimensions: Mapping[str, float]
    score: float
    rationale: str = ""

    def valid(self) -> bool:
        return (
            bool(self.dimensions)
            and all(0.0 <= value <= 10.0 for value in self.dimensions.values())
            and 0.0 <= self.score <= 10.0
        )


@dataclass(frozen=True)
class OscarReview:
    """Adversarial critique before promotion."""

    blocking_defects: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    repair_actions: tuple[str, ...] = ()
    rationale: str = ""

    @property
    def passed(self) -> bool:
        return not self.blocking_defects


@dataclass(frozen=True)
class QualityDecision:
    promoted: bool
    score: float
    minimum_score: float
    oscar_passed: bool
    blocking_reasons: tuple[str, ...] = ()
    required_repairs: tuple[str, ...] = ()
    next_action: str | None = None


def evaluate_quality(
    state: MissionState,
    scorecard: Scorecard,
    oscar: OscarReview,
    next_action: str | None,
) -> QualityDecision:
    """Apply hard gates before allowing a verified result to continue."""
    reasons: list[str] = []
    repairs = list(oscar.repair_actions)

    if not scorecard.valid():
        reasons.append("invalid scorecard")
    if scorecard.score < MINIMUM_RESPONSIBLE_SCORE:
        reasons.append(f"score below {MINIMUM_RESPONSIBLE_SCORE}")
    if not oscar.passed:
        reasons.append("OSCAR found blocking defects")
    if not state.evidence:
        reasons.append("no execution evidence recorded")
    elif not any(
        evidence.state in {EvidenceState.VERIFIED, EvidenceState.LIVE_VERIFIED}
        for evidence in state.evidence
    ):
        reasons.append("no verified execution evidence recorded")

    promoted = not reasons
    return QualityDecision(
        promoted=promoted,
        score=scorecard.score,
        minimum_score=MINIMUM_RESPONSIBLE_SCORE,
        oscar_passed=oscar.passed,
        blocking_reasons=tuple(reasons),
        required_repairs=tuple(repairs),
        next_action=next_action if promoted else (repairs[0] if repairs else None),
    )


def apply_quality_decision(
    state: MissionState,
    decision: QualityDecision,
) -> MissionState:
    """Persist score/critique outcome without falsely promoting failed work."""
    state.activity.append(
        {
            "quality_gate": {
                "promoted": decision.promoted,
                "score": decision.score,
                "minimum_score": decision.minimum_score,
                "oscar_passed": decision.oscar_passed,
                "blocking_reasons": list(decision.blocking_reasons),
                "required_repairs": list(decision.required_repairs),
            }
        }
    )

    if decision.promoted:
        state.decisions.append(
            f"Quality gate passed at {decision.score:.2f}; continue mission."
        )
        state.next_action = decision.next_action
        state.next_action_reason = "Scorecard and OSCAR passed the promotion gate."
    else:
        state.blockers.extend(decision.blocking_reasons)
        state.risks.extend(decision.required_repairs)
        state.next_action = decision.next_action
        state.next_action_reason = "Repair the highest-value quality-gate failure before promotion."

    return state
