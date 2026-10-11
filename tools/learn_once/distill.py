"""Distillation — DISTILL stage.

Raw teaching -> Intelligent Block: the essence in its smallest durable form,
seen from multiple perspectives (human / learner / machine), with an
actionable rule and a machine-checkable form.

Taught != understood. Distillation is where understanding is forced:
if you cannot state the essence, the perspectives, and the rule,
the lesson is not ready to encode.
"""

from __future__ import annotations

from .models import IntelligentBlock, Lesson, Stage


def distill(
    lesson: Lesson,
    essence: str,
    perspectives: dict,
    actionable_rule: str,
    machine_check: str,
    beneficiary_value: str = "",
) -> Lesson:
    """Distill a CAPTURED lesson into its Intelligent Block.

    Raises:
        ValueError: if the lesson is not in CAPTURED stage (stage order is law).
        ValueError: if the IB fails validation (incomplete understanding).
    """
    if lesson.stage != Stage.CAPTURED.value:
        raise ValueError(
            f"distill requires stage CAPTURED, lesson {lesson.lesson_id} "
            f"is {lesson.stage} — stages move forward only"
        )
    ib = IntelligentBlock(
        essence=essence,
        perspectives=perspectives,
        actionable_rule=actionable_rule,
        machine_check=machine_check,
        beneficiary_value=beneficiary_value,
    )
    issues = ib.validate()
    if issues:
        raise ValueError(
            f"Intelligent Block incomplete for {lesson.lesson_id}: "
            + "; ".join(issues)
        )
    lesson.ib = {
        "essence": ib.essence,
        "perspectives": ib.perspectives,
        "actionable_rule": ib.actionable_rule,
        "machine_check": ib.machine_check,
        "beneficiary_value": ib.beneficiary_value,
    }
    lesson.stage = Stage.DISTILLED.value
    lesson.log("DISTILLED to Intelligent Block")
    return lesson
