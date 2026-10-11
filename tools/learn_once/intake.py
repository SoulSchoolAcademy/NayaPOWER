"""Lesson intake — CAPTURE stage.

A teaching enters from Shawn or any high-value source. Capture is faithful:
the raw teaching is preserved verbatim; distillation happens later.
"""

from __future__ import annotations

import datetime as dt
import re

from .models import Lesson, Stage


def _utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _slug(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:40] or "untitled"


def next_lesson_id(existing_ids: list[str]) -> str:
    """LO-NNNN sequence, continuing from the highest existing number."""
    nums = []
    for lid in existing_ids:
        m = re.fullmatch(r"LO-(\d+)", lid or "")
        if m:
            nums.append(int(m.group(1)))
    return f"LO-{(max(nums) + 1) if nums else 1:04d}"


def capture(
    teaching_text: str,
    teacher: str,
    source: str,
    title: str | None = None,
    lesson_id: str | None = None,
) -> Lesson:
    """Capture a raw teaching. Returns a Lesson in CAPTURED stage.

    Raises ValueError on empty teaching/teacher — a lesson with no content
    or no attributable teacher cannot enter the loop.
    """
    if not (teaching_text or "").strip():
        raise ValueError("teaching_text must not be empty")
    if not (teacher or "").strip():
        raise ValueError("teacher must be named — unattributed teachings rot")
    title = title or _slug(teaching_text[:80])
    lesson = Lesson(
        lesson_id=lesson_id or f"LO-{dt.datetime.now(dt.timezone.utc):%Y%m%d%H%M%S}",
        title=title,
        teacher=teacher.strip(),
        source=source,
        taught_at=_utcnow(),
        raw_teaching=teaching_text.strip(),
        stage=Stage.CAPTURED.value,
    )
    lesson.log(f"CAPTURED from {source} by {teacher.strip()}")
    return lesson
