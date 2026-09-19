from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))

from self_proof import FAIL, NOT_VERIFIED, OVERALL_LIMITED, PASS, REQUIRED_CHECKS
from self_proof_collector import collect_from_records, collect_repository


COMMIT = "e512a3b80a31e78c35d16f8728b76173ef89dc4f"


def record(surface="authority", status=PASS, evidence=None, commit_sha=COMMIT, method="execution"):
    return {
        "evidence_id": f"EV-{surface}",
        "surface": surface,
        "status": status,
        "evidence": evidence if evidence is not None else [f"observed:{surface}"],
        "commit_sha": commit_sha,
        "method": method,
    }


def test_empty_repository_evidence_is_explicitly_unverified():
    result = collect_from_records([], observed_commit=COMMIT)
    assert result["proof"]["overall"] == "SELF_VERIFIED_WITH_LIMITATIONS"
    assert result["proof"]["unverified_checks"] == list(REQUIRED_CHECKS)
    assert result["accepted_records"] == []


def test_one_real_record_proves_only_its_declared_surface():
    result = collect_from_records([record("authority")], observed_commit=COMMIT)
    assert result["proof"]["checks"][7]["status"] == PASS
    assert result["proof"]["unverified_checks"] == [
        name for name in REQUIRED_CHECKS if name != "authority"
    ]


def test_source_code_or_status_without_evidence_cannot_become_pass():
    result = collect_from_records(
        [{"surface": "runtime", "status": PASS, "commit_sha": COMMIT}],
        observed_commit=COMMIT,
    )
    assert result["proof"]["checks"][4]["status"] == NOT_VERIFIED
    assert result["accepted_records"] == []


def test_wrong_commit_cannot_prove_a_surface():
    result = collect_from_records(
        [record("build", commit_sha="wrong-commit")], observed_commit=COMMIT
    )
    assert result["proof"]["checks"][2]["status"] == NOT_VERIFIED
    assert result["accepted_records"] == []


def test_forbidden_method_cannot_prove_a_surface():
    result = collect_from_records(
        [record("identity", method="model_assertion")], observed_commit=COMMIT
    )
    assert result["proof"]["checks"][0]["status"] == NOT_VERIFIED
    assert result["accepted_records"] == []


def test_failed_existing_evidence_is_preserved_as_failure():
    result = collect_from_records(
        [record("integrity", status=FAIL, evidence=["integrity-regression"])],
        observed_commit=COMMIT,
    )
    assert result["proof"]["checks"][12]["status"] == FAIL
    assert result["proof"]["overall"] == "NOT_VERIFIED"


def test_noncanonical_status_is_not_promoted():
    result = collect_from_records(
        [record("retrieval", status="PARTIAL")], observed_commit=COMMIT
    )
    assert result["proof"]["checks"][11]["status"] == NOT_VERIFIED


def test_repository_collection_is_read_only(tmp_path: Path):
    records = tmp_path / ".naya" / "evidence" / "records"
    records.mkdir(parents=True)
    source = records / "authority.json"
    source.write_text(json.dumps(record("authority")), encoding="utf-8")
    before = source.read_bytes()

    result = collect_repository(tmp_path, observed_commit=COMMIT)

    assert result["read_only"] is True
    assert result["persistence"] == "none"
    assert result["activity_changes"] is False
    assert source.read_bytes() == before
    assert result["accepted_records"] == ["EV-authority"]


def test_collector_does_not_import_or_write_activity_paths():
    result = collect_from_records([record("persistence")], observed_commit=COMMIT)
    assert result["evidence"]["persistence"]["evidence"] == ("observed:persistence",)
    assert "activity_event" not in sys.modules
    assert "canonical_event_store" not in sys.modules


def test_all_thirteen_surfaces_are_always_returned_by_the_evaluator():
    result = collect_from_records([], observed_commit=COMMIT)
    assert [check["name"] for check in result["proof"]["checks"]] == list(REQUIRED_CHECKS)
