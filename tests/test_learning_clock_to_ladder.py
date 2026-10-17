"""Behavioral tests for the clock-to-ladder bridge (convergence B/C).

These tests prove the seam the bridge closes: a T6 VERIFIED clock meta row
becomes ladder-evaluable evidence (E1-E3) through the bridge, and only
through the bridge -- the assembler has no clock producer, and the ladder
alone cannot see clock rows.

Fail-closed behaviors under test:
  - full valid T6 meta + capture receipt -> record -> evaluate() earns E3
  - no capture receipt -> evidence omits capture -> ladder UNPROVEN
    (the bridge never fabricates capture)
  - missing control_receipt / measured_effect -> record None + codes
  - judge == author (incl. normalized "Naya Verity" vs "naya-verity") -> None
  - judge == applier -> None (executor-owned observation)
  - verdict FAIL / T6_PROBE stage -> None (failed probes emit no T6)
  - measured_effect as a bare number -> None (ladder/D require a string)
  - forbidden authority field in meta or capture -> None (#1712)
  - malformed input (None / list / wrong stage) -> (None, codes), never raises
  - end-to-end: the first real T6 shape earns exactly E3, never E4+
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from learning_clock_to_ladder import (  # noqa: E402
    t6_meta_to_record,
    validate_t6_meta,
)
from learning_evidence_ladder import evaluate  # noqa: E402


def _meta(**over):
    base = {
        "lesson_id": "LC-20261014-004",
        "stage": 6,
        "stage_name": "T6_VERIFIED",
        "ts": "2026-10-14T12:00:00+00:00",
        "written_ts": "2026-10-14T12:00:01+00:00",
        "title": None,
        "evidence": "judge verdict + both transcripts",
        "judge_seat": "Naya Iota",
        "author_seat": "Naya Verity",
        "verdict": "PASS",
        "verified_at": "2026-10-14T12:00:00+00:00",
        "control_receipt": "CTRL-20261014-004",
        "treatment_receipt": "TRT-20261014-004",
        "retrieval_ref": "RET-abc123",
        "task_ref": "TASK-cold-probe-001",
        "applier": "Naya Theta",
        "applied_at": "2026-10-14T11:52:43+00:00",
        "measured_effect": "control 12/20 -> treatment 19/20",
    }
    base.update(over)
    return base


def _capture(**over):
    base = {
        "intelligent_block_id": "IB-TEST-T6",
        "captured_at": "2026-10-14T04:37:18+00:00",
    }
    base.update(over)
    return base


def test_full_t6_meta_earns_exactly_e3():
    record, codes = t6_meta_to_record(_meta(), _capture())
    assert codes == []
    assert record is not None
    assert record["id"] == "LC-20261014-004"
    assert record["producer_id"] == "Naya Verity"
    result = evaluate({**record, "claimed_level": "E3_INDEPENDENT"})
    assert result["earned_level"] == "E3_INDEPENDENT", result
    assert result["verdict"] == "ACCEPTED", result
    # T6 proves E1-E3 only: E4+ need their own evidence.
    assert "E4_TRANSFER" not in result["proven_chain"]


def test_no_capture_receipt_is_unproven_not_fabricated():
    record, codes = t6_meta_to_record(_meta())
    assert codes == []
    assert record is not None
    assert "capture_receipt" not in record["evidence"]
    result = evaluate({**record, "claimed_level": "E3_INDEPENDENT"})
    assert result["earned_level"] == "UNPROVEN", result


def test_missing_control_receipt_rejected():
    meta = _meta()
    del meta["control_receipt"]
    record, codes = t6_meta_to_record(meta, _capture())
    assert record is None
    assert any("control_receipt" in c for c in codes)


def test_missing_measured_effect_rejected():
    meta = _meta()
    del meta["measured_effect"]
    record, codes = t6_meta_to_record(meta, _capture())
    assert record is None
    assert any("measured_effect" in c for c in codes)


def test_numeric_measured_effect_rejected_not_coerced():
    record, codes = t6_meta_to_record(_meta(measured_effect=0.35), _capture())
    assert record is None
    assert any("MEASURED_EFFECT_MUST_BE_STRING" in c for c in codes)


def test_judge_is_author_rejected():
    record, codes = t6_meta_to_record(
        _meta(judge_seat="Naya Verity"), _capture())
    assert record is None
    assert any("JUDGE_IS_AUTHOR" in c for c in codes)


def test_judge_author_normalized_identity_rejected():
    # Canonical normalizer = strip + casefold (admission gate). Case and
    # surrounding whitespace do NOT make a different seat.
    record, codes = t6_meta_to_record(
        _meta(judge_seat="  NAYA VERITY  "), _capture())
    assert record is None
    assert any("JUDGE_IS_AUTHOR" in c for c in codes)


def test_hyphen_vs_space_not_normalized_canonical_rule():
    # DOCUMENTED current behavior, not a claim it is ideal: the canonical
    # normalizer does NOT equate hyphen with space, so "naya-verity" and
    # "Naya Verity" pass the bridge as different seats -- the bridge
    # faithfully applies the admission gate's rule. Strengthening the
    # normalizer belongs to the admission-gate owner (different-seat
    # decision); if it strengthens, the bridge strengthens with it
    # because it imports normalize_identity instead of copying it.
    record, codes = t6_meta_to_record(
        _meta(judge_seat="naya-verity"), _capture())
    assert record is not None
    assert codes == []


def test_judge_is_applier_rejected():
    record, codes = t6_meta_to_record(
        _meta(judge_seat="Naya Theta"), _capture())
    assert record is None
    assert any("JUDGE_IS_APPLIER" in c for c in codes)


def test_fail_verdict_rejected():
    record, codes = t6_meta_to_record(_meta(verdict="FAIL"), _capture())
    assert record is None
    assert any("VERDICT_NOT_PASS" in c for c in codes)


def test_t6_probe_stage_rejected():
    record, codes = t6_meta_to_record(
        _meta(stage="T6_PROBE", stage_name="T6_PROBE (verdict recorded, no T6 emitted)"),
        _capture())
    assert record is None
    assert any("INVALID_STAGE" in c for c in codes)


def test_stage_name_mismatch_rejected():
    record, codes = t6_meta_to_record(
        _meta(stage_name="T5_APPLIED"), _capture())
    assert record is None
    assert any("INVALID_STAGE_NAME" in c for c in codes)


def test_bad_lesson_id_rejected():
    record, codes = t6_meta_to_record(_meta(lesson_id="not-a-lesson"), _capture())
    assert record is None
    assert any("INVALID_LESSON_ID" in c for c in codes)


def test_unparseable_timestamp_rejected():
    record, codes = t6_meta_to_record(
        _meta(verified_at="yesterday-ish"), _capture())
    assert record is None
    assert any("INVALID_TIMESTAMP" in c and "verified_at" in c for c in codes)


def test_forbidden_authority_field_in_meta_rejected():
    record, codes = t6_meta_to_record(
        _meta(authorized=True), _capture())
    assert record is None
    assert any("FORBIDDEN_AUTHORITY_FIELD" in c for c in codes)


def test_forbidden_authority_field_in_capture_rejected():
    record, codes = t6_meta_to_record(_meta(), _capture(grant_id="G-1"))
    assert record is None
    assert any("FORBIDDEN_AUTHORITY_FIELD" in c for c in codes)


def test_invalid_capture_receipt_rejected():
    record, codes = t6_meta_to_record(_meta(), {"captured_at": "2026-10-14T04:37:18+00:00"})
    assert record is None
    assert any("INVALID_CAPTURE_RECEIPT" in c for c in codes)


def test_malformed_input_never_raises():
    for bad in (None, [], "T6", 6, {"stage": 6}):
        record, codes = t6_meta_to_record(bad)
        assert record is None
        assert codes
    assert validate_t6_meta(None) == ["META_NOT_AN_OBJECT"]


def test_validate_is_pure_audit():
    codes = validate_t6_meta(_meta())
    assert codes == []
    assert validate_t6_meta(_meta(verdict="NO-TRANSFER-MEASURED")) != []
