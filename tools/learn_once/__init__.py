"""Learn-Once Loop — permanent protocol component.

Shawn's teaching (2026-10-08): "A lesson isn't learned when it's noted.
It's learned when behavior changes permanently without being told again.
The test of learning is silence — the teacher never repeats it."

The loop:
    CAPTURE -> DISTILL -> ENCODE -> VERIFY -> MEASURE

    1. CAPTURE — a teaching enters (from Shawn or any high-value source)
    2. DISTILL — to an Intelligent Block: essence, multiple perspectives, actionable
    3. ENCODE  — into the machine: law file, gate, test, cron body, or manifest
                 entry. NOT just a note.
    4. VERIFY  — behavioral test proving the lesson is active; fails on regression
    5. MEASURE — the metric is zero re-tells. If the teacher repeats it,
                 the loop failed — filed as a bug.

Public API:
    from tools.learn_once import LearnOnceLoop
    loop = LearnOnceLoop(registry_path="tools/learn_once/data/lessons.jsonl")
    lesson = loop.capture("...", teacher="Shawn", source="chat")
    loop.distill(lesson, essence="...", perspectives={...}, actionable_rule="...",
                 machine_check="...")
    loop.encode(lesson, encoding)
    loop.verify(lesson)          # behavioral check
    loop.record_retell("LO-0001") # teacher repeated it -> FAILED + bug
    loop.audit()                 # learned/unlearned report over the registry
"""

from .models import (
    STAGE_ORDER,
    EncodingRecord,
    EncodingTarget,
    IntelligentBlock,
    Lesson,
    Stage,
)
from .loop import LearnOnceLoop

__all__ = [
    "LearnOnceLoop",
    "Lesson",
    "Stage",
    "STAGE_ORDER",
    "IntelligentBlock",
    "EncodingRecord",
    "EncodingTarget",
]
