"""AER-LIVE-4: Eligibility Uncertainty Preservation (spec).

Shawn's law (SN-0810, ratified 2026-10-10): "Don't know" is neither
eligible nor ineligible. Missing evidence creates a governed
reconstruction obligation. Fairness debt becomes a possible-history
range, not one guessed number. Deadlines escalate uncertainty; they
never manufacture proof.

Core principles:
1. UNDETERMINED is a first-class verdict, not a pending boolean.
2. Missing evidence → reconstruction obligation (governed, tracked).
3. Fairness debt under uncertainty = [min_possible, max_possible] range.
4. Deadlines increase urgency of reconstruction, never convert
   UNDETERMINED to PROVEN_TRUE or PROVEN_FALSE.

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class UncertaintyVerdict(Enum):
    PROVEN = "PROVEN"
    DISPROVEN = "DISPROVEN"
    UNDETERMINED = "UNDETERMINED"


@dataclass(frozen=True)
class ReconstructionObligation:
    """Governed obligation to reconstruct missing evidence."""
    obligation_id: str
    missing_fact: str
    created_at: str
    deadline: Optional[str] = None
    # Deadlines escalate urgency, never manufacture proof
    escalated: bool = False


@dataclass(frozen=True)
class DebtRange:
    """Fairness debt as a possible-history range, not a guessed number."""
    min_possible: float
    max_possible: float

    def __post_init__(self):
        if self.min_possible > self.max_possible:
            raise ValueError("min_possible cannot exceed max_possible")

    def is_precise(self) -> bool:
        return self.min_possible == self.max_possible


@dataclass(frozen=True)
class UncertaintyAssessment:
    verdict: UncertaintyVerdict
    reconstruction_obligations: tuple = ()
    debt_range: Optional[DebtRange] = None


def assess_with_uncertainty(
    facts_established: dict,
    facts_missing: set,
    debt_evidence: Optional[dict] = None,
    deadline_approaching: bool = False,
) -> UncertaintyAssessment:
    """Assess eligibility preserving uncertainty.

    - Any missing fact → UNDETERMINED + reconstruction obligations
    - Debt without full evidence → range, not point estimate
    - Deadline → escalate obligations, never flip verdict
    """
    obligations = tuple(
        ReconstructionObligation(
            obligation_id=f"RECON-{fact}",
            missing_fact=fact,
            created_at="now",
            escalated=deadline_approaching,
        )
        for fact in facts_missing
    )

    if facts_missing:
        debt_range = None
        if debt_evidence:
            # Possible-history range from partial evidence
            debt_range = DebtRange(
                min_possible=debt_evidence.get("min", 0.0),
                max_possible=debt_evidence.get("max", float("inf")),
            )
        return UncertaintyAssessment(
            verdict=UncertaintyVerdict.UNDETERMINED,
            reconstruction_obligations=obligations,
            debt_range=debt_range,
        )

    # All facts present — check if any disproven
    if any(not v for v in facts_established.values()):
        return UncertaintyAssessment(verdict=UncertaintyVerdict.DISPROVEN)

    return UncertaintyAssessment(verdict=UncertaintyVerdict.PROVEN)
