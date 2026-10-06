import json
from pathlib import Path

from tools.learning_experiment_contract import validate_round2_manifest
from tools.round2_manifest_bind import blob_sha_file

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "BRAIN/12-ENGINEERING/EXPERIMENTS/R2-SN0458-NEWBATTERY-001"


def load(name):
    return json.loads((EXP / name).read_text(encoding="utf-8"))


def test_replacement_battery_is_fail_closed_until_independent_key_validation():
    manifest = load("preregistration.json")
    assert manifest["status"] == "DRAFT_AWAITING_INDEPENDENT_KEY_VALIDATION"
    assert manifest["answer_key"]["prevalidated_before_trials"] is False
    result = validate_round2_manifest(manifest)
    assert not result.ok
    assert "STATUS_MUST_BE_PREREGISTERED" in result.errors
    assert "ANSWER_KEY_PREVALIDATION_REQUIRED" in result.errors


def test_task_and_key_ids_are_exactly_one_to_one():
    tasks = load("tasks/task-pack.json")["tasks"]
    key = load("keys/answer-key.json")["answers"]
    task_ids = [t["id"] for t in tasks]
    assert len(task_ids) == 11
    assert len(set(task_ids)) == 11
    assert set(task_ids) == set(key)
    assert sum(t["kind"] == "transfer" for t in tasks) == 6
    assert sum(t["kind"] == "negative_transfer" for t in tasks) == 5


def test_all_key_actions_are_bounded_to_proceed_or_hold():
    key = load("keys/answer-key.json")["answers"]
    assert {x["action"] for x in key.values()} <= {"PROCEED", "HOLD"}
    assert sum(x["action"] == "HOLD" for x in key.values()) == 6
    assert sum(x["action"] == "PROCEED" for x in key.values()) == 5


def test_target_lesson_fixture_is_byte_identical_to_source_blob():
    assert blob_sha_file(EXP / "target-lesson-SN-0458.md") == "604d5cb88ca8cbad4f3f83ec5f549cf8e3ec1567"


def test_arm_overlays_are_separated_and_do_not_create_authority():
    control = load("arms/control.json")
    treatment = load("arms/treatment.json")
    wrong = load("arms/wrong-lesson.json")
    assert control["overlay"] is None
    assert treatment["overlay"] == "target-lesson-SN-0458.md"
    assert wrong["overlay"] == "wrong-lesson-overlay.md"
    assert all(x["authority_granted"] is False for x in (control, treatment, wrong))


def test_manifest_has_no_pretrial_outcome_leakage():
    manifest = load("preregistration.json")
    forbidden = {"results", "observed_scores", "winner", "causal_verdict"}
    assert forbidden.isdisjoint(manifest)
