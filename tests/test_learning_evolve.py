"""Proof tests for the EVOLVE node (tools/learning_evolve.py).

What these prove (and what they don't):
- PROVEN: improvement is measured honestly against the no-lesson baseline;
  verified wins are preserved; a verified failure emits a correction record
  with the SUPERSEDES edge while the original lesson is never modified;
  the supersession transition is atomic and fail-closed; unverified
  (self-attested) outcomes never count toward a verdict; the cycle summary
  aggregates by task class into admission guidance for the next cycle.
- NOT PROVEN here: production HTTP invocation (no edge function deployed);
  longitudinal compounding (that requires the calendar, not a test).
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tools"))

from learning_evolve import (  # noqa: E402
    CORRECT,
    FLAG_FOR_REVIEW,
    KEEP,
    apply_supersession,
    emit_correction_record,
    emit_cycle_summary,
    evolve_lesson,
)


def make_lesson(lesson_id="SN-EVO-001", **overrides):
    lesson = {
        "lesson_id": lesson_id,
        "claim": "Triage support tickets by severity before topic.",
        "lifecycle_state": "ACTIVE",
        "lesson_kind": "triage",
    }
    lesson.update(overrides)
    return lesson


def make_app(receipt_id, task_ref, success, verifier="naya-2", applier="naya-1",
             baseline=None, task_class="triage"):
    app = {
        "application_receipt_id": receipt_id,
        "task_ref": task_ref,
        "task_class": task_class,
        "applier": applier,
        "applied_at": "2026-10-09T10:00:00Z",
        "decision_summary": "applied lesson to %s" % task_ref,
        "outcome": {
            "success": success,
            "effect_text": "decision %s for %s" % ("succeeded" if success else "failed", task_ref),
            "observed_at": "2026-10-09T11:00:00Z",
        },
        "independent_verification": (
            {"verifier": verifier, "verified_at": "2026-10-09T12:00:00Z"}
            if verifier is not None else None
        ),
    }
    if baseline is not None:
        app["baseline_success_rate"] = baseline
    return app


# --------------------------------------------------------------------------
# 1. Improvement measurement: honest delta against the no-lesson baseline.
# --------------------------------------------------------------------------

def test_improvement_measurement_is_honest():
    lesson = make_lesson()
    apps = [
        make_app("APP-1", "ticket-1", True, baseline=0.5),
        make_app("APP-2", "ticket-2", True, baseline=0.5),
        make_app("APP-3", "ticket-3", True, baseline=0.5),
        make_app("APP-4", "ticket-4", False, baseline=0.5),
    ]
    result = evolve_lesson(lesson, apps)
    m = result.measurement
    assert m["verified_applications"] == 4
    assert m["verified_successes"] == 3
    assert m["verified_failures"] == 1
    assert m["observed_success_rate"] == pytest.approx(0.75)
    assert m["baseline_success_rate"] == pytest.approx(0.5)
    # The honest delta: +0.25 — measured, not asserted.
    assert m["delta_vs_baseline"] == pytest.approx(0.25)
    assert "4 verified applications" in m["delta_basis"]
    assert m["low_sample"] is False


def test_delta_unknown_without_baseline():
    lesson = make_lesson()
    apps = [make_app("APP-1", "ticket-1", True), make_app("APP-2", "ticket-2", True)]
    result = evolve_lesson(lesson, apps)
    assert result.measurement["delta_vs_baseline"] is None
    assert "NO_BASELINE" in result.measurement["delta_basis"]
    # Verdict is still KEEP — but the reason says the baseline is unknown.
    assert result.verdict == KEEP
    assert "NO_BASELINE" in result.verdict_reason


def test_low_sample_is_flagged():
    lesson = make_lesson()
    apps = [make_app("APP-1", "ticket-1", True, baseline=0.5)]
    result = evolve_lesson(lesson, apps)
    assert result.measurement["low_sample"] is True
    assert result.verdict == KEEP  # the verdict holds; the bound is stated


# --------------------------------------------------------------------------
# 2. The proof case: wins preserved, failure corrected, lifecycle intact.
# --------------------------------------------------------------------------

def test_failure_emits_correction_and_preserves_wins():
    lesson = make_lesson()
    apps = [
        make_app("APP-1", "ticket-1", True, baseline=0.5),
        make_app("APP-2", "ticket-2", True, baseline=0.5),
        make_app("APP-3", "ticket-3", True, baseline=0.5),
        make_app("APP-4", "ticket-4", False, baseline=0.5),
    ]
    result = evolve_lesson(lesson, apps)

    assert result.verdict == CORRECT
    assert "FALSIFIED_IN_APPLICATION" in result.verdict_reason
    assert len(result.correction_records) == 1

    correction = result.correction_records[0]
    # The correction carries the SUPERSEDES edge and the reason.
    assert correction["supersedes_lesson_id"] == "SN-EVO-001"
    assert correction["supersession_reason"]
    assert "APP-4" in correction["supersession_reason"]
    # The original claim is preserved verbatim — nothing was overwritten.
    assert correction["original_claim"] == lesson["claim"]
    # The corrected claim narrows the scope and marks itself a candidate.
    assert correction["corrected_claim"] != lesson["claim"]
    assert "Correction candidate" in correction["corrected_claim"]
    # The falsifying evidence is named, with its verifier.
    assert correction["falsifying_evidence"]["application_receipt_id"] == "APP-4"
    assert correction["falsifying_evidence"]["verifier"] == "naya-2"
    # The wins are preserved as evidence, carried forward.
    preserved = correction["preserved_evidence"]["successful_application_receipt_ids"]
    assert sorted(preserved) == ["APP-1", "APP-2", "APP-3"]
    # The correction waits for admission — it is NOT active by fiat.
    assert correction["lifecycle_state"] == "PENDING_ADMISSION"
    # The original lesson is untouched: still ACTIVE, no supersession fields.
    assert lesson["lifecycle_state"] == "ACTIVE"
    assert "superseded_by_lesson_id" not in lesson


def test_correction_ids_are_deterministic():
    lesson = make_lesson()
    app = make_app("APP-9", "ticket-9", False)
    c1 = emit_correction_record(lesson, app, [])
    c2 = emit_correction_record(lesson, app, [])
    assert c1["correction_id"] == c2["correction_id"]
    assert c1["correction_id"].startswith("COR-")


def test_evolve_refuses_non_active_lesson():
    lesson = make_lesson(lifecycle_state="SUPERSEDED")
    with pytest.raises(ValueError, match="LESSON_NOT_ACTIVE"):
        evolve_lesson(lesson, [])


# --------------------------------------------------------------------------
# 3. Supersession: atomic, fail-closed, history preserved.
# --------------------------------------------------------------------------

def test_apply_supersession_transitions_atomically():
    lesson = make_lesson()
    app = make_app("APP-4", "ticket-4", False)
    correction = emit_correction_record(lesson, app, ["APP-1"])
    correction["admitted_at"] = "2026-10-09T13:00:00Z"
    correction["admitted_by"] = "naya-2"

    superseded, active = apply_supersession(lesson, correction)

    assert superseded["lifecycle_state"] == "SUPERSEDED"
    assert superseded["superseded_by_lesson_id"] == correction["correction_id"]
    assert superseded["supersession_reason"] == correction["supersession_reason"]
    assert superseded["superseded_at"]
    # The original claim survives on the superseded record — history intact.
    assert superseded["claim"] == lesson["claim"]
    assert active["lifecycle_state"] == "ACTIVE"
    assert active["activated_at"]
    # Inputs were never mutated.
    assert lesson["lifecycle_state"] == "ACTIVE"
    assert correction["lifecycle_state"] == "PENDING_ADMISSION"


def test_supersession_fails_closed():
    lesson = make_lesson()
    app = make_app("APP-4", "ticket-4", False)
    good = emit_correction_record(lesson, app, ["APP-1"])
    good["admitted_at"] = "2026-10-09T13:00:00Z"

    # Correction not admitted → no transition.
    unadmitted = dict(good)
    del unadmitted["admitted_at"]
    with pytest.raises(ValueError, match="not been admitted"):
        apply_supersession(lesson, unadmitted)

    # Wrong lifecycle on the correction.
    wrong_state = dict(good)
    wrong_state["lifecycle_state"] = "ACTIVE"
    with pytest.raises(ValueError, match="not PENDING_ADMISSION"):
        apply_supersession(lesson, wrong_state)

    # Edge points at the wrong lesson.
    wrong_edge = dict(good)
    wrong_edge["supersedes_lesson_id"] = "SN-OTHER"
    with pytest.raises(ValueError, match="does not point at original"):
        apply_supersession(lesson, wrong_edge)

    # Original already superseded.
    dead = dict(lesson)
    dead["lifecycle_state"] = "SUPERSEDED"
    with pytest.raises(ValueError, match="not ACTIVE"):
        apply_supersession(dead, good)

    # Corrected claim identical to the original — corrects nothing.
    same_claim = dict(good)
    same_claim["corrected_claim"] = lesson["claim"]
    with pytest.raises(ValueError, match="must correct something"):
        apply_supersession(lesson, same_claim)

    # Empty reason.
    no_reason = dict(good)
    no_reason["supersession_reason"] = "  "
    with pytest.raises(ValueError, match="supersession_reason"):
        apply_supersession(lesson, no_reason)


# --------------------------------------------------------------------------
# 4. No verified outcomes → FLAG_FOR_REVIEW, never KEEP on self-attestation.
# --------------------------------------------------------------------------

def test_self_attested_outcomes_never_count():
    lesson = make_lesson()
    # Verifier == applier: self-attestation, recorded honestly, not counted.
    apps = [
        make_app("APP-1", "ticket-1", True, verifier="naya-1", applier="naya-1"),
        make_app("APP-2", "ticket-2", True, verifier=None),
    ]
    result = evolve_lesson(lesson, apps)
    assert result.verdict == FLAG_FOR_REVIEW
    assert "NO_VERIFIED_OUTCOMES" in result.verdict_reason
    assert result.measurement["verified_applications"] == 0
    assert len(result.measurement["unverified_application_reasons"]) == 2
    assert result.correction_records == ()


def test_empty_history_is_flagged():
    result = evolve_lesson(make_lesson(), [])
    assert result.verdict == FLAG_FOR_REVIEW
    assert "NO_VERIFIED_OUTCOMES" in result.verdict_reason


# --------------------------------------------------------------------------
# 5. KEEP when every verified application succeeded.
# --------------------------------------------------------------------------

def test_all_wins_verdict_keep():
    lesson = make_lesson()
    apps = [
        make_app("APP-1", "ticket-1", True, baseline=0.4),
        make_app("APP-2", "ticket-2", True, baseline=0.4),
        make_app("APP-3", "ticket-3", True, baseline=0.4),
    ]
    result = evolve_lesson(lesson, apps)
    assert result.verdict == KEEP
    assert result.correction_records == ()
    assert result.measurement["delta_vs_baseline"] == pytest.approx(0.6)


# --------------------------------------------------------------------------
# 6. The compounding loop: cycle summary → sharper next admission.
# --------------------------------------------------------------------------

def test_cycle_summary_guides_next_admission():
    triage = evolve_lesson(
        make_lesson("SN-TRIAGE"),
        [make_app("A1", "t-1", True, baseline=0.5), make_app("A2", "t-2", True, baseline=0.5),
         make_app("A3", "t-3", False, baseline=0.5)],
    ).measurement
    routing = evolve_lesson(
        make_lesson("SN-ROUTE"),
        [make_app("B1", "r-1", True, baseline=0.3, task_class="routing"),
         make_app("B2", "r-2", True, baseline=0.3, task_class="routing")],
        baseline_success_rate=0.3,
    ).measurement

    summary = emit_cycle_summary([triage, routing])
    assert summary["schema"] == "NAYANET_LEARNING_CYCLE_SUMMARY_V1"
    assert summary["lesson_count"] == 2
    assert summary["cycle_id"].startswith("CYC-")

    by_class = summary["by_task_class"]
    assert by_class["triage"]["observed_success_rate"] == pytest.approx(2 / 3)
    assert by_class["triage"]["corrections_emitted"] == 1
    assert by_class["routing"]["mean_delta_vs_baseline"] == pytest.approx(0.7)

    guidance = " ".join(summary["admission_guidance"])
    # The next cycle's admission reads this: prefer what improved decisions,
    # treat falsification-prone classes with care.
    assert "routing" in guidance
    assert "triage" in guidance


def test_cycle_summary_deterministic_id():
    m1 = evolve_lesson(make_lesson("SN-A"), [make_app("A1", "t-1", True)]).measurement
    s1 = emit_cycle_summary([m1])
    s2 = emit_cycle_summary([m1])
    assert s1["cycle_id"] == s2["cycle_id"]


# --------------------------------------------------------------------------
# 7. Orchestrator binding: EVOLVE executes as a real stage.
# --------------------------------------------------------------------------

def test_evolve_bound_in_orchestrator():
    from orchestrator import NodeOrchestrator, RunStatus, StageStatus
    from orchestrator.executors import LocalExecutor
    from orchestrator.stages import STAGE_CONTRACTS, StageId

    assert STAGE_CONTRACTS[StageId.EVOLVE].implemented is True
    assert STAGE_CONTRACTS[StageId.EVOLVE].not_implemented_reason == ""

    executor = LocalExecutor(continuity_dir="/tmp/evolve-bind-continuity")
    out = executor.execute(
        StageId.EVOLVE,
        {
            "lesson": make_lesson(),
            "applications": [
                make_app("APP-1", "ticket-1", True, baseline=0.5),
                make_app("APP-2", "ticket-2", True, baseline=0.5),
                make_app("APP-3", "ticket-3", True, baseline=0.5),
                make_app("APP-4", "ticket-4", False, baseline=0.5),
            ],
        },
        "corr-evolve-bind",
    )
    assert out.ok is True
    assert out.result["verdict"] == CORRECT
    assert len(out.result["correction_records"]) == 1
    assert out.result["correlation_id"] == "corr-evolve-bind"
    assert "EVOLVE verdict: CORRECT" in out.summary


def test_evolve_stage_fails_closed_without_inputs():
    from orchestrator.executors import LocalExecutor
    from orchestrator.stages import StageId

    executor = LocalExecutor(continuity_dir="/tmp/evolve-bind-continuity")
    out = executor.execute(StageId.EVOLVE, {}, "corr-x")
    assert out.ok is False
    assert "no lesson supplied" in out.summary

    out = executor.execute(StageId.EVOLVE, {"lesson": make_lesson()}, "corr-x")
    assert out.ok is False
    assert "no application history supplied" in out.summary


def test_full_run_now_has_seven_implemented_stages(tmp_path):
    """The run ceiling rises: only CONNECT/LEARN remain NOT_IMPLEMENTED."""
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    from learning_admission_gate import ADMISSION_SCHEMA  # noqa: E402
    from orchestrator import NodeOrchestrator, RunStatus, StageStatus  # noqa: E402
    from orchestrator.executors import LocalExecutor  # noqa: E402

    orch = NodeOrchestrator(
        LocalExecutor(continuity_dir=tmp_path / "continuity"),
        store_root=tmp_path / "orchestrator",
    )
    capture = {
        "lesson_id": "SN-EVO-RUN",
        "owner_id": "owner-1",
        "naya_id": "naya-1",
        "identity": {"actor_id": "naya-1", "system_id": "nayapower", "role": "learner"},
        "mission": "prove the learning loop",
        "objective": "execute the nine-node pipeline for one capture",
        "candidate": {
            "schema": ADMISSION_SCHEMA,
            "claim": "The EVOLVE stage executes on the lesson's application history.",
            "falsification_condition": "If the EVOLVE stage does not execute, the claim is wrong.",
            "task": "evolve-binding-proof-run",
            "lesson_id": "SN-EVO-RUN",
            "success_criterion": "EVOLVE stage COMPLETED with a verdict.",
            "criterion_independent_of_lesson": True,
            "criterion_registered_at": "2026-10-09T09:00:00Z",
            "doer": "naya-5",
            "scorer": "naya-2",
            "measurement": {"method": "machine", "detail": "stage record inspection"},
            "arms": {
                "treatment": {"observable": "evolve runs", "measured_at": "2026-10-09T10:00:00Z"},
                "control": {"observable": "no evolve", "measured_at": "2026-10-09T10:05:00Z"},
            },
            "asserts_behavioral_change": True,
            "behavioral_measure": "evolve verdict",
            "outcome": "pending",
        },
        "lesson": make_lesson("SN-EVO-RUN"),
        "applications": [
            make_app("APP-1", "ticket-1", True, baseline=0.5),
            make_app("APP-2", "ticket-2", True, baseline=0.5),
            make_app("APP-3", "ticket-3", True, baseline=0.5),
            make_app("APP-4", "ticket-4", False, baseline=0.5),
        ],
    }
    event_id = orch.commit_capture(capture["lesson_id"], "evolve-binding-fingerprint")
    record = orch.run(event_id, capture)

    # Only CONNECT and LEARN remain unimplemented — EVOLVE now executes.
    assert record.status == RunStatus.INCOMPLETE.value
    for stage in ["SELF", "LAW", "ACT", "KNOW", "PROVE", "VERIFY", "EVOLVE"]:
        assert record.stages[stage].status == StageStatus.COMPLETED.value, stage
    for stage in ["CONNECT", "LEARN"]:
        assert record.stages[stage].status == StageStatus.NOT_IMPLEMENTED.value, stage
    evolve_result = record.stages["EVOLVE"]
    assert "EVOLVE verdict: CORRECT" in evolve_result.output_summary
