"""Adversarial acceptance tests for the failure-learning machine gate."""
from kernel.protocol.learning_capture import CycleLesson, check_lesson


def _complete_failure(**overrides):
    fields = dict(
        work_description="repaired a regression",
        lesson="a skipped behavioral job is not proof of success",
        provenance="CI run URL and exact-head failing test",
        smart_note_id="SN-TEST-FAILURE-001",
        failure_detected=True,
        expected_vs_actual="expected behavioral job to execute; it was skipped",
        root_cause_or_unknown="workflow condition excluded the required job",
        team_share_ref="https://github.com/example/repo/issues/123#issuecomment-456",
        repair_or_blocker="condition corrected on branch; merge remains gated",
        regression_guard="tests/test_failure_learning_gate.py::test_failure_requires_regression_guard",
        canonical_lesson_ref="https://github.com/example/repo/blob/main/BRAIN/lesson.md",
    )
    fields.update(overrides)
    return CycleLesson(**fields)


def test_complete_failure_receipt_passes():
    result = check_lesson(_complete_failure())
    assert result.passed, result.reasons


def test_failure_cannot_pass_silently_without_team_share():
    result = check_lesson(_complete_failure(team_share_ref=""))
    assert not result.passed
    assert any("team_share_ref" in reason for reason in result.reasons)


def test_failure_requires_root_cause_or_explicit_unknown():
    result = check_lesson(_complete_failure(root_cause_or_unknown=""))
    assert not result.passed
    assert any("root_cause_or_unknown" in reason for reason in result.reasons)


def test_failure_requires_repair_or_blocker_disposition():
    result = check_lesson(_complete_failure(repair_or_blocker=""))
    assert not result.passed
    assert any("repair_or_blocker" in reason for reason in result.reasons)


def test_failure_requires_regression_guard():
    result = check_lesson(_complete_failure(regression_guard=""))
    assert not result.passed
    assert any("regression_guard" in reason for reason in result.reasons)


def test_failure_lesson_requires_canonical_record():
    result = check_lesson(_complete_failure(canonical_lesson_ref=""))
    assert not result.passed
    assert any("canonical_lesson_ref" in reason for reason in result.reasons)


def test_failure_lesson_requires_smart_note_identity():
    result = check_lesson(_complete_failure(smart_note_id=""))
    assert not result.passed
    assert any("Smart Note ID" in reason for reason in result.reasons)


def test_non_failure_cycles_keep_existing_contract():
    # Existing non-failure behavior stays compatible; failures opt into the
    # stricter evidence-bearing contract.
    result = check_lesson(CycleLesson(
        work_description="routine dependency bump",
        lesson="",
        no_lesson_reason="no behavioral change or reusable insight",
    ))
    assert result.passed


def test_failure_with_no_lesson_still_requires_explicit_no_lesson_reason():
    result = check_lesson(_complete_failure(lesson="", no_lesson_reason=""))
    assert not result.passed
    assert any("No lesson captured" in reason for reason in result.reasons)
