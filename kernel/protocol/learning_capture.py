"""
learning_capture.py — Machine law: every cycle must produce its lesson.

Point 8 of the Unified Operating Law: "Learn by preserving valuable,
provenance-bound lessons through the canonical candidate and promotion process."

A work cycle is not complete until its lesson is captured or explicitly
declared as having none. "No lesson" is allowed but must be stated —
silence is not a lesson.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CycleLesson:
    work_description: str
    lesson: str                  # the durable, reusable insight — or ""
    no_lesson_reason: str = ""   # required if lesson is empty
    smart_note_id: str = ""      # filled when captured as a Smart Note
    provenance: str = ""         # evidence the lesson rests on


@dataclass
class LearningCaptureResult:
    passed: bool
    reasons: list = field(default_factory=list)


def check_lesson(cycle: CycleLesson) -> LearningCaptureResult:
    reasons: list[str] = []
    if not cycle.work_description.strip():
        reasons.append("No work described.")
    if not cycle.lesson.strip():
        if not cycle.no_lesson_reason.strip():
            reasons.append(
                "No lesson captured and no reason given. "
                "State the lesson or state why there is none."
            )
    else:
        if not cycle.provenance.strip():
            reasons.append("Lesson captured without provenance — evidence required.")
    return LearningCaptureResult(passed=not reasons, reasons=reasons)
