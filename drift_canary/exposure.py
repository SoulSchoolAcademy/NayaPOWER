"""Exposure budgets: track how much a sealed set has been exposed to the
evaluated side. Fresh qualification required when exposure exceeds design
assumptions.

Tracked dimensions:
  adaptive_evaluations   — rounds where the builder adapted to results
  feedback_detail_bits   — cumulative detail leaked through feedback packages
  answer_bearing_disclosures — any disclosure containing answer-bearing content
  successor_retrievability   — whether a cold successor could retrieve the set
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExposureBudget:
    set_id: str
    max_adaptive_rounds: int = 3
    max_feedback_bits: int = 64
    max_answer_disclosures: int = 0
    successor_retrievable: bool = False  # design assumption: sealed = not retrievable

    adaptive_rounds_used: int = 0
    feedback_bits_used: int = 0
    answer_disclosures: int = 0

    def record_adaptive_round(self, feedback_bits: int = 0,
                              answer_disclosure: bool = False) -> None:
        self.adaptive_rounds_used += 1
        self.feedback_bits_used += feedback_bits
        if answer_disclosure:
            self.answer_disclosures += 1

    def exceeded(self) -> tuple[bool, tuple[str, ...]]:
        reasons = []
        if self.adaptive_rounds_used > self.max_adaptive_rounds:
            reasons.append(
                f"adaptive rounds {self.adaptive_rounds_used} > {self.max_adaptive_rounds}")
        if self.feedback_bits_used > self.max_feedback_bits:
            reasons.append(
                f"feedback bits {self.feedback_bits_used} > {self.max_feedback_bits}")
        if self.answer_disclosures > self.max_answer_disclosures:
            reasons.append(
                f"answer disclosures {self.answer_disclosures} > {self.max_answer_disclosures}")
        return bool(reasons), tuple(reasons)

    def requires_fresh_qualification(self) -> bool:
        return self.exceeded()[0]


# Recovery contract: is a qualification certificate still usable in context?
# Four conjuncts; verification must bind to a CONSISTENT snapshot — a
# concurrent compromise event must not leave ACT on a stale certificate.
RECOVERY_CONTRACT = """
qualification_is_usable(certificate, context):
    verify_receipt_integrity(certificate)
    AND evidence_independence_is_current(certificate, context.snapshot_id)
    AND policy_and_runtime_scope_match(certificate, context)
    AND required_independent_reviews_passed(certificate)
""".strip()


def qualification_is_usable(receipt_integrity_ok: bool,
                            independence_current: bool,
                            scope_matches: bool,
                            independent_reviews_passed: bool) -> tuple[bool, str]:
    """Evaluate the recovery contract. All four must hold."""
    checks = (
        ("receipt_integrity", receipt_integrity_ok),
        ("evidence_independence_current", independence_current),
        ("policy_and_runtime_scope_match", scope_matches),
        ("independent_reviews_passed", independent_reviews_passed),
    )
    failed = [name for name, ok in checks if not ok]
    if failed:
        return False, f"unusable: {', '.join(failed)}"
    return True, "usable: all four conjuncts hold"


# Three separately provable facts. A lesson can stay CORRECT after its test
# is compromised — correctness of the lesson, independence of the evaluation,
# and usability of the qualification are independent claims.
SEPARABLE_FACTS = (
    "was_the_lesson_correct",      # truth of the lesson itself
    "was_the_evaluation_independent",  # integrity of the evidence
    "is_the_qualification_still_usable",  # recovery contract verdict
)
