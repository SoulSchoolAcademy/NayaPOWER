"""The 11-stage chain walker — one reuse event, end to end.

    CAPTURE → PERSIST → RECEIPT → SMART LINK → COLD RETRIEVE → COMPREHEND →
    APPLY → OBSERVE → INDEPENDENTLY VERIFY → LEARN → SUCCESSOR REUSE

Stages 1–4 and 10 cite existing machinery (they are reconstruction of the
lesson’s history, not new work): the lesson row’s own provenance names the
trial; the trial result files are the capture/verification receipts; the
E5 level IS the learned state. This module does not reimplement them.

Stages 5–9 and 11 are the new machine path built here: live retrieval,
applicability, application, deterministic observation, independent
verification, and the tamper-evident reuse receipt.

The applier (the cold agent) and the reader are injected: in production
the reader is read.fetch_verified_rows and the applier is a cold
successor; in tests they are stubs. Nothing here touches the network.

SMART LINK is honestly UNINSTRUMENTED for the T11–T14 lessons: they live
in learning_evidence with no smart-note projection (the corpus gap named
in the lesson-selection criterion). The chain verdict therefore caps at
PARTIAL until the cold-retrieve lane closes that gap — visible, not hidden.
"""

from __future__ import annotations

from pathlib import Path

from .models import Applicability, ChainReport, Lesson, StageResult
from .read import IngestError, fetch_verified_rows
from .receipt import emit_reuse_receipt
from .select import SelectionError, check_applicability, eligible_lessons, match_task
from .verify import VerifyResult, verify

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[2]

# lesson target_id -> trial result file that is its capture/verify receipt
TRIAL_RECEIPTS = {
    "lesson:TIER1-2026-10-08-T11": "successor-reuse/trials/sr-p2-result.md",
    "lesson:TIER1-2026-10-08-T12": "successor-reuse/trials/sr-p6-result.md",
    "lesson:TIER1-2026-10-08-T13": "successor-reuse/trials/sr-p2-result.md",
    "lesson:TIER1-2026-10-08-T14": "successor-reuse/trials/sr-p5-result.md",
}

STAGES = (
    "CAPTURE", "PERSIST", "RECEIPT", "SMART LINK", "COLD RETRIEVE",
    "COMPREHEND", "APPLY", "OBSERVE", "INDEPENDENTLY VERIFY", "LEARN",
    "SUCCESSOR REUSE",
)


def _present(stage: str, detail: str) -> StageResult:
    return StageResult(stage, "PRESENT", detail)


def _gap(stage: str, detail: str) -> StageResult:
    return StageResult(stage, "GAP", detail)


def _uninstrumented(stage: str, detail: str) -> StageResult:
    return StageResult(stage, "UNINSTRUMENTED", detail)


def run_chain(
    task_brief: str,
    task_family: str,
    cold_agent: str,
    reader=fetch_verified_rows,
    applier=None,
    repo_root: Path = REPO_ROOT,
) -> tuple[ChainReport, dict | None]:
    """Walk the 11 stages for one reuse event.

    Returns (report, reuse_receipt). The receipt is None unless the walk
    reaches the SUCCESSOR REUSE stage. Raises IngestError / SelectionError
    fail-closed — a refused chain raises, it never returns a fake COMPLETE.
    """
    report = ChainReport(task_family=task_family)

    # ---- 5. COLD RETRIEVE (built here; runs first — nothing else is
    #      possible without the lesson) ---------------------------------
    rows = reader()  # IngestError on unreachable store
    lessons = eligible_lessons(rows)  # SelectionError when none qualify
    lesson = match_task(lessons, task_family)  # SelectionError on mismatch
    report.stages.append(_present(
        "COLD RETRIEVE",
        f"lesson {lesson.id[:8]} ({lesson.target_id}) retrieved live from "
        f"learning_evidence at {lesson.retrieved_at}",
    ))

    # ---- 1. CAPTURE / 2. PERSIST (reconstructed from the row) ----------
    report.stages.insert(0, _present(
        "CAPTURE",
        f"captured via {lesson.provenance}; "
        f"verification: {lesson.verification_method[:80]}",
    ))
    report.stages.insert(1, _present(
        "PERSIST",
        f"row {lesson.id} in canonical store learning_evidence "
        f"(level={lesson.level}, status={lesson.status})",
    ))

    # ---- 3. RECEIPT ----------------------------------------------------
    receipt_path = TRIAL_RECEIPTS.get(lesson.target_id)
    if receipt_path and (repo_root / receipt_path).exists():
        report.stages.insert(2, _present(
            "RECEIPT", f"trial receipt {receipt_path} exists in repo"))
    else:
        report.stages.insert(2, _gap(
            "RECEIPT",
            f"no trial receipt file for {lesson.target_id} (expected "
            f"{receipt_path})"))

    # ---- 4. SMART LINK -------------------------------------------------
    report.stages.insert(3, _uninstrumented(
        "SMART LINK",
        "T11–T14 lessons have no smart-note projection (corpus gap named in "
        "lesson-selection criterion); owner: cold-retrieve lane",
    ))

    # ---- 6. COMPREHEND -------------------------------------------------
    applicability = check_applicability(lesson, task_family, task_brief)
    if applicability.verdict != "APPLICABLE":
        raise SelectionError("NOT_APPLICABLE", applicability.reason)
    report.stages.append(_present("COMPREHEND", applicability.reason))

    # ---- 7. APPLY ------------------------------------------------------
    if applier is None:
        raise IngestError("NO_APPLIER", "no cold agent supplied for APPLY")
    artifact = applier(task_brief, lesson)
    if not artifact or not artifact.strip():
        raise IngestError("EMPTY_APPLICATION", "cold agent returned nothing")
    report.stages.append(_present(
        "APPLY", f"cold agent '{cold_agent}' produced an application artifact"))

    # ---- 8. OBSERVE ----------------------------------------------------
    observation = verify(task_family, artifact)
    report.stages.append(_present(
        "OBSERVE", f"observation recorded: {observation.evidence}"))

    # ---- 9. INDEPENDENTLY VERIFY ---------------------------------------
    # The verifier is a deterministic AST mechanism, separate from the
    # applier by construction — independence is structural, not claimed.
    report.stages.append(_present(
        "INDEPENDENTLY VERIFY",
        f"deterministic verifier verdict: {observation.verdict} "
        f"({observation.evidence})",
    ))

    # ---- 10. LEARN -----------------------------------------------------
    report.stages.append(_present(
        "LEARN",
        f"lesson already at {lesson.level} (independent verification on "
        f"record); promotion of NEW learnings is the Learning Lane's writ, "
        f"not this run's",
    ))

    # ---- 11. SUCCESSOR REUSE -------------------------------------------
    reused = observation.verdict == "PASS"
    receipt = emit_reuse_receipt(
        lesson=lesson,
        task_family=task_family,
        task_brief=task_brief,
        cold_agent=cold_agent,
        applicability=applicability,
        application_artifact=artifact,
        verify_result=observation,
        reused=reused,
        reuse_reason=(
            "deterministic verifier PASS: the verified law held in the "
            "successor's hands"
            if reused else
            "verifier did not PASS: reuse NOT claimed; artifact preserved "
            "as negative evidence"
        ),
    )
    report.stages.append(_present(
        "SUCCESSOR REUSE",
        f"reuse receipt {receipt['receipt_sha256'][:12]}… emitted "
        f"(reused={reused}); persistent handoff row in "
        f"nayanet_successor_handoffs is NAMED for authorization, not written",
    ))

    states = [s.state for s in report.stages]
    if any(s == "GAP" for s in states):
        report.verdict = "BROKEN"
    elif any(s in ("PENDING", "UNINSTRUMENTED") for s in states):
        report.verdict = "PARTIAL"
    else:
        report.verdict = "COMPLETE"
    return report, receipt
