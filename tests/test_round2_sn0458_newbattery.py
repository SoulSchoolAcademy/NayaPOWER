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


def test_blind_transfer_prompts_do_not_name_the_target_rule():
    tasks = load("tasks/task-pack.json")["tasks"]
    transfer_prompts = " ".join(
        t["prompt"].lower() for t in tasks if t["kind"] == "transfer"
    )
    forbidden_cues = (
        "independent",
        "second source",
        "second-source",
        "second check",
        "sn-0458",
        "target lesson",
    )
    assert all(cue not in transfer_prompts for cue in forbidden_cues)


def test_transfer_tasks_include_repeated_same_source_evidence_not_named_as_validation():
    tasks = [t for t in load("tasks/task-pack.json")["tasks"] if t["kind"] == "transfer"]
    repeated_markers = ("same", "rerun", "repeating", "repeated", "own")
    assert all(any(marker in t["prompt"].lower() for marker in repeated_markers) for t in tasks)


def test_every_preregistered_fixture_role_matches_exact_git_blob():
    manifest = load("preregistration.json")
    roles = manifest["fixture_roles"]
    actual = {path: blob_sha_file(ROOT / path) for path in roles}
    assert actual == roles
    assert sorted(manifest["answer_key"]["fixture_shas"]) == sorted(roles.values())


def test_diagnostic_brain_index_projection_matches_generator():
    import difflib
    from tools.regenerate_brain_index import (
        basis_commit,
        domain_counts,
        inventory,
        normalize_json,
        patch_brain_index,
    )
    files = inventory(ROOT)
    counts = domain_counts(files)
    basis = basis_commit(ROOT)
    expected = normalize_json(patch_brain_index(ROOT, basis, counts, "2026-10-06"))
    actual = normalize_json((ROOT / "BRAIN/NAYAPOWER-BRAIN-INDEX.json").read_text())
    assert actual == expected, "\n".join(
        difflib.unified_diff(
            actual.splitlines(), expected.splitlines(),
            fromfile="actual", tofile="expected", n=3
        )
    )
