"""Lesson selection — pure. Decides WHAT is successor-eligible and applicable.

Eligibility law (lesson-selection criterion, 2026-10-08): a lesson is
successor-eligible iff it is independently verified, non-derivable, and
outcome-grounded. In store terms the machine-checkable floor is::

    level == 'E5_CAN_TEACH' and status == 'ACTIVE'
    and provenance == 'TRIAL_EVIDENCE'

E5 is the ladder level whose definition requires independent verification
and demonstrated transfer; TRIAL_EVIDENCE provenance names the trial that
produced it. The OBSERVATION-provenance E5 row (node fallback lesson) is a
different kind — operational note, not a verified law — and is refused
here, loudly, rather than silently admitted.

Applicability (the COMPREHEND stage) is a machine floor, not a ceiling:
it rejects obvious family mismatches (a dispatch lesson handed to a
state-file task). The agent's own applicability judgment remains the
real comprehension; this gate only stops category errors.
"""

from __future__ import annotations

from .models import Applicability, Lesson

REQUIRED_LEVEL = "E5_CAN_TEACH"
REQUIRED_STATUS = "ACTIVE"
REQUIRED_PROVENANCE = "TRIAL_EVIDENCE"

# task_family -> lesson target_id prefixes eligible for it
FAMILY_TARGETS = {
    "dispatch": ("lesson:TIER1-2026-10-08-T11", "lesson:TIER1-2026-10-08-T12"),
    "icu_allocation": ("lesson:TIER1-2026-10-08-T13",),
    "state_file": ("lesson:TIER1-2026-10-08-T14",),
}

# task_family -> trigger terms the brief must contain for APPLICABLE
FAMILY_TRIGGERS = {
    "dispatch": ("dispatch", "call", "score"),
    "icu_allocation": ("icu", "allocat", "bed", "triage"),
    "state_file": ("state",),
}


class SelectionError(Exception):
    """Fail-closed selection failure. code names the exact refusal."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def eligible_lessons(rows: list[dict]) -> list[Lesson]:
    """Filter raw store rows to successor-eligible lessons.

    Raises SelectionError("NO_VERIFIED_LESSONS") when nothing qualifies —
    the caller must surface this, never invent or weaken to a CANDIDATE.
    """
    out: list[Lesson] = []
    for r in rows:
        if (
            r.get("level") == REQUIRED_LEVEL
            and r.get("status") == REQUIRED_STATUS
            and r.get("provenance") == REQUIRED_PROVENANCE
        ):
            claim = r.get("claim")
            if isinstance(claim, dict):
                claim = claim.get("text", "")
            out.append(
                Lesson(
                    id=str(r.get("id", "")),
                    target_id=str(r.get("target_id", "")),
                    level=r["level"],
                    status=r["status"],
                    provenance=r["provenance"],
                    verification_method=str(r.get("verification_method", "")),
                    claim_text=str(claim or ""),
                    retrieved_at=str(r.get("retrieved_at", "")),
                    query=str(r.get("query", "")),
                )
            )
    if not out:
        raise SelectionError(
            "NO_VERIFIED_LESSONS",
            "canonical store returned zero rows at E5_CAN_TEACH/ACTIVE/TRIAL_EVIDENCE",
        )
    return out


def match_task(lessons: list[Lesson], task_family: str) -> Lesson:
    """Pick the lesson for a task family. Exactly one family owns a lesson.

    Raises SelectionError("UNKNOWN_TASK_FAMILY") for undeclared families
    (closed world — no fuzzy fallback) and
    SelectionError("NO_APPLICABLE_LESSON") when the family has no verified
    lesson. A lesson is never transplanted across families.
    """
    targets = FAMILY_TARGETS.get(task_family)
    if targets is None:
        raise SelectionError(
            "UNKNOWN_TASK_FAMILY",
            f"'{task_family}' is not a declared lesson family "
            f"(declared: {sorted(FAMILY_TARGETS)})",
        )
    for lesson in lessons:
        if lesson.target_id in targets:
            return lesson
    raise SelectionError(
        "NO_APPLICABLE_LESSON",
        f"no verified lesson for family '{task_family}' "
        f"(eligible targets: {[l.target_id for l in lessons]})",
    )


def check_applicability(lesson: Lesson, task_family: str, task_brief: str) -> Applicability:
    """COMPREHEND stage: machine floor for applicability.

    Verifies the lesson's family matches the task family AND the brief
    contains the family's trigger terms. This does not replace the agent's
    judgment — it stops category errors before they reach the agent.
    """
    targets = FAMILY_TARGETS.get(task_family, ())
    if lesson.target_id not in targets:
        return Applicability(
            "NOT_APPLICABLE",
            f"lesson {lesson.target_id} is not registered for family '{task_family}'",
        )
    brief = task_brief.lower()
    triggers = FAMILY_TRIGGERS.get(task_family, ())
    if triggers and not any(t in brief for t in triggers):
        return Applicability(
            "NOT_APPLICABLE",
            f"brief lacks family trigger terms {triggers} for '{task_family}'",
        )
    return Applicability(
        "APPLICABLE",
        f"lesson {lesson.target_id} registered for '{task_family}'; "
        f"brief carries trigger terms",
    )
