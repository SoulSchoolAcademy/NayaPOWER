import json

import pytest

from tools.learning_experiment_contract import REQUIRED_WEIGHTS
from tools.round2_manifest_bind import (
    FROZEN_WEIGHTS,
    bind_and_validate,
    build_manifest,
    sha1_file,
    verify_fixture_binding,
)


def _hypotheses():
    return [
        "H1 diagnostic order improves",
        "H2 accuracy improves on prevalidated keys",
        "H3 value gain is not purchased by disproportionate cost",
        "H4 unrelated tasks do not suffer negative transfer",
    ]


def test_bind_valid_fixtures_passes_machine_check(tmp_path):
    f1 = tmp_path / "scenario-a.md"
    f2 = tmp_path / "answer-key.md"
    f1.write_text("transfer scenario A")
    f2.write_text("answer key A")
    manifest, result = bind_and_validate(
        "Naya 4", "Coda 2", [f1, f2], _hypotheses()
    )
    assert result.ok, result.errors
    assert manifest["scoring"]["weights"] == FROZEN_WEIGHTS
    assert set(manifest["scoring"]["weights"]) == REQUIRED_WEIGHTS


def test_bind_always_uses_frozen_weights(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("x")
    manifest = build_manifest("Naya 4", "Coda 2", [f1], _hypotheses())
    assert manifest["scoring"]["weights"] == {
        "accuracy": 0.4,
        "diagnostic_order": 0.2,
        "cost": 0.2,
        "consistency": 0.1,
        "negative_transfer_guard": 0.1,
    }


@pytest.mark.parametrize("key", [
    "schema", "status", "arms", "minimum_trials_per_arm", "negative_transfer",
    "scoring", "answer_key", "evidence_capture", "hypotheses",
])
def test_extras_cannot_override_generated_contract(tmp_path, key):
    f = tmp_path / "fixture.md"
    f.write_text("real fixture")
    with pytest.raises(ValueError, match="GENERATED_CONTRACT_OVERRIDE:" + key):
        build_manifest("builder", "verifier", [f], _hypotheses(), extras={key: {}})


def test_extras_preserve_annotation_metadata(tmp_path):
    f = tmp_path / "fixture.md"
    f.write_text("real fixture")
    manifest, result = bind_and_validate(
        "builder", "verifier", [f], _hypotheses(), extras={"annotation": "review me"}
    )
    assert result.ok
    assert manifest["annotation"] == "review me"
    assert manifest["scoring"]["weights"] == FROZEN_WEIGHTS


def test_bind_refuses_builder_self_validation(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("x")
    _, result = bind_and_validate("Naya 4", "Naya 4", [f1], _hypotheses())
    assert not result.ok
    assert "ANSWER_KEY_VERIFIER_MUST_BE_INDEPENDENT" in result.errors


def test_bind_refuses_outcome_leakage(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("x")
    with pytest.raises(ValueError, match="OUTCOME_LEAKAGE_BEFORE_TRIALS"):
        build_manifest(
            "Naya 4",
            "Coda 2",
            [f1],
            _hypotheses(),
            extras={"winner": "TREATMENT"},
        )


def test_bind_missing_fixture_refused(tmp_path):
    with pytest.raises(FileNotFoundError):
        build_manifest(
            "Naya 4", "Coda 2", [tmp_path / "absent.md"], _hypotheses()
        )


def test_bind_rejects_underpowered_design(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("x")
    _, result = bind_and_validate(
        "Naya 4",
        "Coda 2",
        [f1],
        _hypotheses(),
        minimum_trials_per_arm=4,
        negative_transfer_trials=1,
    )
    assert not result.ok
    assert "MINIMUM_FIVE_TRIALS_PER_ARM" in result.errors
    assert "MINIMUM_FIVE_NEGATIVE_TRANSFER_TRIALS" in result.errors


def test_tampered_fixture_breaks_binding(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("original bytes")
    manifest, result = bind_and_validate(
        "Naya 4", "Coda 2", [f1], _hypotheses()
    )
    assert result.ok, result.errors
    ok, _ = verify_fixture_binding(manifest, [f1])
    assert ok
    f1.write_text("original bytes + silent edit")
    ok, drifted = verify_fixture_binding(manifest, [f1])
    assert not ok
    assert drifted


def test_sha1_is_40_hex(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("probe")
    sha = sha1_file(f1)
    assert len(sha) == 40
    assert all(c in "0123456789abcdef" for c in sha)


def test_cli_rejects_leakage_and_missing(tmp_path, capsys):
    from tools.round2_manifest_bind import main

    rc = main(
        [
            "--builder",
            "Naya 4",
            "--independent-verifier",
            "Naya 4",
            "--fixture",
            str(tmp_path / "absent.md"),
            "--hypothesis",
            "H1",
            "--hypothesis",
            "H2",
            "--hypothesis",
            "H3",
            "--hypothesis",
            "H4",
        ]
    )
    assert rc == 2
    assert "BIND_REFUSED" in capsys.readouterr().out
