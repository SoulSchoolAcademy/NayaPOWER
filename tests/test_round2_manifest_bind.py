import json

import pytest

from tools.learning_experiment_contract import REQUIRED_WEIGHTS
from tools.round2_manifest_bind import (
    FROZEN_WEIGHTS,
    bind_and_validate,
    blob_sha_file,
    build_manifest,
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


def test_bind_refuses_builder_self_validation(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("x")
    with pytest.raises(ValueError, match="ANSWER_KEY_VERIFIER_MUST_BE_INDEPENDENT"):
        bind_and_validate("Naya 4", "Naya 4", [f1], _hypotheses())


def test_bind_refuses_blank_identities(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("x")
    with pytest.raises(ValueError, match="BUILDER_AND_VERIFIER_REQUIRED"):
        build_manifest("  ", "Coda 2", [f1], _hypotheses())
    with pytest.raises(ValueError, match="BUILDER_AND_VERIFIER_REQUIRED"):
        build_manifest("Naya 4", "", [f1], _hypotheses())


def test_bind_refuses_weak_hypotheses(tmp_path):
    f1 = tmp_path / "s.md"
    f1.write_text("x")
    with pytest.raises(ValueError, match="FOUR_HYPOTHESES_REQUIRED"):
        build_manifest("Naya 4", "Coda 2", [f1], ["H1", "H2", "H3"])
    with pytest.raises(ValueError, match="FOUR_HYPOTHESES_REQUIRED"):
        build_manifest(
            "Naya 4", "Coda 2", [f1], ["H1", "H1", "  ", "H1"]
        )


def test_bind_refuses_empty_fixture_list():
    with pytest.raises(ValueError, match="FIXTURE_SHAS_REQUIRED"):
        build_manifest("Naya 4", "Coda 2", [], _hypotheses())


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
    with pytest.raises(ValueError, match="MINIMUM_FIVE_TRIALS_PER_ARM"):
        bind_and_validate(
            "Naya 4",
            "Coda 2",
            [f1],
            _hypotheses(),
            minimum_trials_per_arm=4,
            negative_transfer_trials=1,
        )


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


def test_blob_sha_matches_git_vectors(tmp_path):
    empty = tmp_path / "empty.md"
    empty.write_bytes(b"")
    assert blob_sha_file(empty) == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
    hello = tmp_path / "hello.md"
    hello.write_bytes(b"hello")
    assert blob_sha_file(hello) == "b6fc4c620b67d95f953a5c1c1230aaab5db5a1b0"


def test_blob_sha_differs_from_raw_sha1(tmp_path):
    # Regression: v1 bound raw sha1, which never equals a published blob SHA.
    # SN-0458 lesson bytes: blob 604d5cb8... vs raw 6e13497b... (verified live).
    import hashlib

    f1 = tmp_path / "s.md"
    f1.write_bytes(b"probe")
    assert blob_sha_file(f1) != hashlib.sha1(b"probe").hexdigest()
    assert len(blob_sha_file(f1)) == 40


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
