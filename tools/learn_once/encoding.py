"""Encoding — ENCODE stage.

A lesson is NOT learned when it is noted. It is learned when it lives in
the machine. The encoding checklist forces the lesson into executable
surface: law file, gate, test, cron body, or protocol manifest entry.

Hard rules:
  * The behavioral `test` target is MANDATORY — without it there is nothing
    for VERIFY to run, and the lesson cannot be proven active.
  * At least one machine target (law_file / gate / cron_body / manifest_entry)
    must be DONE. A lesson that exists only as prose is a note, not learning.
  * No target may remain TODO. Targets that genuinely do not apply must be
    marked NA with a written reason.
"""

from __future__ import annotations

from .models import MACHINE_TARGETS, EncodingRecord, EncodingTarget, Lesson, Stage


def _target_issues(t: EncodingTarget) -> list[str]:
    issues = []
    if t.status not in ("DONE", "NA", "TODO"):
        issues.append(f"{t.kind}: unknown status {t.status!r}")
    elif t.status == "TODO":
        issues.append(f"{t.kind}: still TODO — finish it or mark NA with a reason")
    elif t.status == "NA" and not (t.note or "").strip():
        issues.append(f"{t.kind}: marked NA but no reason given")
    elif t.status == "DONE" and not (t.location or "").strip():
        issues.append(f"{t.kind}: marked DONE but no location recorded")
    return issues


def checklist_issues(encoding: EncodingRecord) -> list[str]:
    """Return blocking issues. Empty list = the lesson may be encoded."""
    issues: list[str] = []
    for t in encoding.targets():
        issues.extend(_target_issues(t))
    if encoding.test.status != "DONE":
        issues.append(
            "behavioral test is mandatory: the `test` target must be DONE "
            "(VERIFY needs something to run)"
        )
    machine_done = [
        t.kind for t in encoding.targets()
        if t.kind in MACHINE_TARGETS and t.status == "DONE"
    ]
    if not machine_done:
        issues.append(
            "lesson must live in the machine: at least one of "
            "law_file / gate / cron_body / manifest_entry must be DONE — "
            "prose alone is a note, not learning"
        )
    return issues


def encode(lesson: Lesson, encoding: EncodingRecord) -> Lesson:
    """Encode a DISTILLED lesson into the machine.

    Raises:
        ValueError: wrong stage, or the checklist is incomplete.
    """
    if lesson.stage != Stage.DISTILLED.value:
        raise ValueError(
            f"encode requires stage DISTILLED, lesson {lesson.lesson_id} "
            f"is {lesson.stage} — stages move forward only"
        )
    issues = checklist_issues(encoding)
    if issues:
        raise ValueError(
            f"encoding incomplete for {lesson.lesson_id}: " + "; ".join(issues)
        )
    lesson.encoding = {
        t.kind: {
            "location": t.location,
            "status": t.status,
            "note": t.note,
        }
        for t in encoding.targets()
    }
    lesson.stage = Stage.ENCODED.value
    done = [t.kind for t in encoding.targets() if t.status == "DONE"]
    lesson.log(f"ENCODED into machine: {', '.join(done)}")
    return lesson


def make_encoding(
    test_location: str,
    law_file: str | None = None,
    gate: str | None = None,
    cron_body: str | None = None,
    manifest_entry: str | None = None,
    na_reasons: dict | None = None,
) -> EncodingRecord:
    """Convenience builder. Unspecified targets become NA (with reasons)."""
    na_reasons = na_reasons or {}
    rec = EncodingRecord()
    rec.test = EncodingTarget(
        kind="test", location=test_location, status="DONE",
        note="behavioral check proving the lesson is active",
    )
    for kind, loc in (
        ("law_file", law_file),
        ("gate", gate),
        ("cron_body", cron_body),
        ("manifest_entry", manifest_entry),
    ):
        if loc:
            setattr(rec, kind, EncodingTarget(kind=kind, location=loc, status="DONE"))
        else:
            setattr(
                rec, kind,
                EncodingTarget(
                    kind=kind, status="NA",
                    note=na_reasons.get(kind, "not applicable to this lesson"),
                ),
            )
    return rec
