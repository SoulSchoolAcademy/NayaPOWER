"""Registry — the JSONL ledger of active lessons.

One JSON object per line. Each record carries the lesson's stage, its
Intelligent Block, where it is encoded in the machine, its behavioral
check, and its re-tell count — the metric of learning.

The registry is append-mostly: lessons are added and updated, never
deleted. A FAILED lesson stays visible until its bug is fixed and the
lesson re-verified — the failure is the evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import Lesson


def load(path: str | Path) -> list[Lesson]:
    p = Path(path)
    if not p.exists():
        return []
    lessons = []
    for i, line in enumerate(p.read_text().splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            lessons.append(Lesson.from_dict(json.loads(line)))
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"registry {p} line {i}: corrupt record: {e}")
    return lessons


def save(path: str | Path, lessons: list[Lesson]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        "\n".join(json.dumps(l.to_dict(), ensure_ascii=False) for l in lessons) + "\n"
    )


def find(lessons: list[Lesson], lesson_id: str) -> Lesson | None:
    for l in lessons:
        if l.lesson_id == lesson_id:
            return l
    return None


def upsert(path: str | Path, lesson: Lesson) -> None:
    """Insert or replace a lesson record, preserving file order."""
    lessons = load(path)
    for i, l in enumerate(lessons):
        if l.lesson_id == lesson.lesson_id:
            lessons[i] = lesson
            break
    else:
        lessons.append(lesson)
    save(path, lessons)
