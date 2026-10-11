"""
learning_capture.py — Machine law: every cycle must produce its lesson.

Point 8 of the Unified Operating Law: preserve provenance-bound lessons.
Failure cycles additionally require visible team communication, a root-cause
classification, a repair/blocker disposition, and a recurrence guard.

This is a fail-closed receipt validator. It does not itself post to GitHub or
prove that a lesson changed future behavior; callers must provide durable
references and later behavior requires separate retrieval/reuse evidence.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CycleLesson:
    work_description: str
    lesson: str                  # durable reusable insight — or ""
    no_lesson_reason: str = ""   # required if lesson is empty
    smart_note_id: str = ""      # canonical Smart Note ID, when captured
    provenance: str = ""         # evidence the lesson rests on
    failure_detected: bool = False
    expected_vs_actual: str = ""
    root_cause_or_unknown: str = ""
    team_share_ref: str = ""     # durable link/receipt; not a claim of dispatch by itself
    repair_or_blocker: str = ""
    regression_guard: str = ""   # test/guard reference or reason impossible yet
    canonical_lesson_ref: str = ""  # canonical durable record for the lesson


@dataclass
class LearningCaptureResult:
    passed: bool
    reasons: list = field(default_factory=list)


def _is_blank(value: object) -> bool:
    """Fail-closed presence check.

    A field is blank when it is not a string or holds only whitespace.
    Malformed (non-string) input must fail the gate with a reason — a
    fail-closed validator never crashes on a malformed receipt.
    """
    return not isinstance(value, str) or not value.strip()


def check_lesson(cycle: CycleLesson) -> LearningCaptureResult:
    reasons: list[str] = []
    if _is_blank(cycle.work_description):
        reasons.append("No work described.")

    if _is_blank(cycle.lesson):
        if _is_blank(cycle.no_lesson_reason):
            reasons.append(
                "No lesson captured and no reason given. "
                "State the lesson or state why there is none."
            )
    elif _is_blank(cycle.provenance):
        reasons.append("Lesson captured without provenance — evidence required.")

    if cycle.failure_detected:
        required = {
            "expected_vs_actual": cycle.expected_vs_actual,
            "root_cause_or_unknown": cycle.root_cause_or_unknown,
            "team_share_ref": cycle.team_share_ref,
            "repair_or_blocker": cycle.repair_or_blocker,
            "regression_guard": cycle.regression_guard,
            "canonical_lesson_ref": cycle.canonical_lesson_ref,
        }
        for field_name, value in required.items():
            if _is_blank(value):
                reasons.append(
                    f"Failure-learning gate: missing {field_name}; "
                    "failure cycles cannot silently pass."
                )
        if not _is_blank(cycle.lesson) and _is_blank(cycle.smart_note_id):
            reasons.append(
                "Failure-learning gate: reusable failure lesson requires a "
                "canonical Smart Note ID."
            )

    return LearningCaptureResult(passed=not reasons, reasons=reasons)
