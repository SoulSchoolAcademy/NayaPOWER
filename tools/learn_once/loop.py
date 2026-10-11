"""LearnOnceLoop — the orchestrator.

One object owns a registry file and walks lessons through the five stages.
Stage order is law: forward only, through the loop's own methods. The only
backward moves are failure states, and they are explicit:

  * record_retell() on an encoded-or-beyond lesson -> FAILED + bug filed.
    The metric is zero re-tells. A re-tell is a loop failure, not a reminder.
  * verify() failing on a VERIFIED/ACTIVE lesson -> REGRESSED.

promote() moves VERIFIED -> ACTIVE: the lesson has held through verification
with the teacher never repeating it.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from . import distill as _distill
from . import encoding as _encoding
from . import intake as _intake
from . import registry as _registry
from . import verify as _verify
from .models import LEARNED_STAGES, Lesson, Stage


def _utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


class LearnOnceLoop:
    def __init__(self, registry_path: str | Path):
        self.registry_path = Path(registry_path)

    # ---- the five stages -------------------------------------------------

    def capture(self, teaching_text: str, teacher: str, source: str,
                title: str | None = None) -> Lesson:
        lesson_id = _intake.next_lesson_id(
            [l.lesson_id for l in _registry.load(self.registry_path)]
        )
        lesson = _intake.capture(teaching_text, teacher, source, title, lesson_id)
        _registry.upsert(self.registry_path, lesson)
        return lesson

    def distill(self, lesson: Lesson, essence: str, perspectives: dict,
                actionable_rule: str, machine_check: str,
                beneficiary_value: str = "") -> Lesson:
        lesson = _distill.distill(
            lesson, essence, perspectives, actionable_rule,
            machine_check, beneficiary_value,
        )
        _registry.upsert(self.registry_path, lesson)
        return lesson

    def encode(self, lesson: Lesson, encoding) -> Lesson:
        lesson = _encoding.encode(lesson, encoding)
        _registry.upsert(self.registry_path, lesson)
        return lesson

    def verify(self, lesson_id: str) -> tuple[bool, str]:
        """Run the lesson's behavioral check. Returns (passed, detail)."""
        lessons = _registry.load(self.registry_path)
        lesson = _registry.find(lessons, lesson_id)
        if lesson is None:
            raise ValueError(f"unknown lesson {lesson_id}")
        if lesson.stage not in (
            Stage.ENCODED.value, Stage.VERIFIED.value, Stage.ACTIVE.value,
        ):
            raise ValueError(
                f"verify requires an encoded lesson; {lesson_id} is {lesson.stage}"
            )
        passed, detail = _verify.run_check(lesson.check)
        if passed:
            if lesson.stage == Stage.ENCODED.value:
                lesson.stage = Stage.VERIFIED.value
                lesson.log(f"VERIFIED: behavioral check passing ({detail})")
            else:
                lesson.log(f"check passing on audit ({detail})")
        else:
            if lesson.stage in (Stage.VERIFIED.value, Stage.ACTIVE.value):
                lesson.stage = Stage.REGRESSED.value
                lesson.log(f"REGRESSED: {detail}")
            else:
                lesson.log(f"verification failed (still ENCODED): {detail}")
        _registry.upsert(self.registry_path, lesson)
        return passed, detail

    def promote(self, lesson_id: str) -> Lesson:
        """VERIFIED -> ACTIVE. The lesson held; the teacher never repeated it."""
        lessons = _registry.load(self.registry_path)
        lesson = _registry.find(lessons, lesson_id)
        if lesson is None:
            raise ValueError(f"unknown lesson {lesson_id}")
        if lesson.stage != Stage.VERIFIED.value:
            raise ValueError(
                f"promote requires VERIFIED; {lesson_id} is {lesson.stage}"
            )
        if lesson.re_tells > 0:
            raise ValueError(
                f"cannot promote {lesson_id}: re_tells={lesson.re_tells} — "
                "a repeated teaching is not learned"
            )
        passed, detail = _verify.run_check(lesson.check)
        if not passed:
            raise ValueError(f"cannot promote {lesson_id}: check failing: {detail}")
        lesson.stage = Stage.ACTIVE.value
        lesson.log("ACTIVE: held through verification, zero re-tells")
        _registry.upsert(self.registry_path, lesson)
        return lesson

    # ---- the metric ------------------------------------------------------

    def record_retell(self, lesson_id: str, repeated_by: str,
                      note: str = "") -> dict:
        """The teacher had to repeat a teaching. This is the loop failing.

        Returns a bug record. If the lesson is already past DISTILL, its
        stage becomes FAILED — learned behavior would not need repeating.
        Unknown teachings are routed to intake instead of failing.
        """
        lessons = _registry.load(self.registry_path)
        lesson = _registry.find(lessons, lesson_id)
        if lesson is None:
            return {
                "outcome": "UNKNOWN_TEACHING",
                "detail": f"{lesson_id} not in registry — route to capture()",
            }
        lesson.re_tells += 1
        bug = {
            "bug": f"LEARN-ONCE-FAILURE/{lesson_id}",
            "at": _utcnow(),
            "repeated_by": repeated_by,
            "note": note or "teacher repeated an already-taught lesson",
            "re_tell_count": lesson.re_tells,
        }
        lesson.bug_refs.append(bug["bug"])
        if lesson.stage in (
            Stage.DISTILLED.value, Stage.ENCODED.value,
            Stage.VERIFIED.value, Stage.ACTIVE.value,
        ):
            lesson.stage = Stage.FAILED.value
            lesson.log(
                f"FAILED: re-tell #{lesson.re_tells} by {repeated_by} — "
                "filed as loop-failure bug"
            )
            outcome = "LOOP_FAILURE"
        else:
            lesson.log(f"re-tell #{lesson.re_tells} during {lesson.stage}")
            outcome = "REPEATED_BEFORE_ENCODING"
        _registry.upsert(self.registry_path, lesson)
        return {"outcome": outcome, "bug": bug}

    def audit(self) -> dict:
        """Learned/unlearned report over the whole registry."""
        return _verify.audit(self.registry_path)

    def get(self, lesson_id: str) -> Lesson | None:
        return _registry.find(_registry.load(self.registry_path), lesson_id)
