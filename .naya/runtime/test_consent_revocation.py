from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
sys.path.insert(0, str(RUNTIME))
SCRIPT = RUNTIME / "consent_revocation.py"
SPEC = importlib.util.spec_from_file_location("consent_revocation", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def record(event_id: str, artifact_type: str | None, parents: list[str]) -> dict:
    row = {
        "event_id": event_id,
        "status": "ACTIVE",
        "consent_state": "EXPLICIT",
        "relationships": {"source_events": parents},
    }
    if artifact_type is not None:
        row["artifact_type"] = artifact_type
    return row


def fixture() -> tuple[dict, list[dict]]:
    revocation = {
        "revocation_id": "revocation-44",
        "authority_ref": "consent-authority-44",
        "revoked_by": "owner-1",
        "reason": "owner withdrew sharing consent",
        "evidence_refs": ["consent-evidence-1"],
        "idempotency_key": "revocation-batch-44",
        "sources": [
            {
                "intelligence_id": "ORIGINAL-A",
                "previous_consent_sha256": sha("consent-granted-A"),
                "revoked_consent_sha256": sha("consent-revoked-A"),
            }
        ],
    }
    records = [
        record("ORIGINAL-A", "ORIGINAL", []),
        record("DERIVED-D", "DERIVED", ["ORIGINAL-A"]),
        record("SUMMARY-S", "SUMMARY", ["DERIVED-D"]),
        record("COLLECTIVE-C", "COLLECTIVE_INSIGHT", ["SUMMARY-S"]),
        record("CACHE-K", "CACHE", ["ORIGINAL-A"]),
        record("EMBEDDING-V", "EMBEDDING", ["ORIGINAL-A"]),
        record("DOWNSTREAM-X", "DOWNSTREAM_CONCLUSION", ["COLLECTIVE-C"]),
    ]
    return revocation, records


class ConsentRevocationTests(unittest.TestCase):
    def test_revocation_plan_covers_every_artifact_class(self) -> None:
        revocation, records = fixture()
        plan = MODULE.plan_consent_revocation(revocation, records)
        self.assertEqual(plan["status"], "COMPLETE")
        self.assertEqual(plan["mode"], "PROPOSAL_ONLY")
        self.assertEqual(plan["original_preservation"], "PRESERVE_OWNER_ORIGINAL")
        self.assertEqual(MODULE.validate_revocation_plan(plan), [])
        actions = {item["intelligence_id"]: item["required_actions"] for item in plan["impacted_artifacts"]}
        self.assertIn("RESTRICT_DERIVED_USE", actions["DERIVED-D"])
        self.assertIn("REVALIDATE_SUMMARY", actions["SUMMARY-S"])
        self.assertIn("RECOMPUTE_COLLECTIVE_INSIGHT_IF_CONTENTS_ARE_NOT_PROVEN_ANONYMOUS", actions["COLLECTIVE-C"])
        self.assertEqual(actions["CACHE-K"], ["PROPOSE_CACHE_INVALIDATION"])
        self.assertEqual(actions["EMBEDDING-V"], ["PROPOSE_EMBEDDING_DELETION_IF_CONTENT_CONTAINS_REVOKED_SOURCE"])
        self.assertIn("REVALIDATE_DOWNSTREAM_CONCLUSION", actions["DOWNSTREAM-X"])
        self.assertEqual(plan["source_actions"][0]["preserve_original"], True)
        self.assertFalse(plan["persistence_performed"])
        self.assertFalse(plan["canonical_records_modified"])

    def test_original_is_preserved_and_never_deleted(self) -> None:
        revocation, records = fixture()
        plan = MODULE.plan_consent_revocation(revocation, records)
        original = plan["source_actions"][0]
        self.assertEqual(original["intelligence_id"], "ORIGINAL-A")
        self.assertNotIn("DELETE_ORIGINAL", json.dumps(plan, sort_keys=True))
        self.assertEqual(original["execution_performed"], False)

    def test_unknown_artifact_type_is_partial(self) -> None:
        revocation, records = fixture()
        records[1].pop("artifact_type")
        plan = MODULE.plan_consent_revocation(revocation, records)
        self.assertEqual(plan["status"], "PARTIAL")
        self.assertIn("ARTIFACT_TYPE_UNKNOWN", {item["code"] for item in plan["unresolved"]})
        derived = next(item for item in plan["impacted_artifacts"] if item["intelligence_id"] == "DERIVED-D")
        self.assertEqual(derived["artifact_type"], "UNKNOWN")
        self.assertEqual(derived["required_actions"], ["REVIEW_REQUIRED"])

    def test_missing_lineage_is_not_guessed(self) -> None:
        revocation, records = fixture()
        records[1]["relationships"]["source_events"] = ["MISSING-SOURCE"]
        plan = MODULE.plan_consent_revocation(revocation, records)
        self.assertEqual(plan["status"], "PARTIAL")
        self.assertIn("DEPENDENCY_TARGET_MISSING", {item["code"] for item in plan["unresolved"]})

    def test_no_known_dependent_is_explicit(self) -> None:
        revocation, _ = fixture()
        plan = MODULE.plan_consent_revocation(revocation, [record("ORIGINAL-A", "ORIGINAL", [])])
        self.assertEqual(plan["status"], "NO_KNOWN_DEPENDENTS")
        self.assertEqual(plan["impacted_artifacts"], [])

    def test_unauthorized_revocation_source_is_refused(self) -> None:
        revocation, records = fixture()
        with self.assertRaisesRegex(MODULE.ConsentRevocationError, "no authorized revocation source"):
            MODULE.plan_consent_revocation(revocation, records, authorized_ids={"DERIVED-D"})

    def test_equal_consent_hashes_are_refused(self) -> None:
        revocation, records = fixture()
        revocation["sources"][0]["revoked_consent_sha256"] = revocation["sources"][0]["previous_consent_sha256"]
        with self.assertRaisesRegex(MODULE.ConsentRevocationError, "hashes are equal"):
            MODULE.plan_consent_revocation(revocation, records)

    def test_missing_revocation_authority_is_refused(self) -> None:
        revocation, records = fixture()
        revocation.pop("authority_ref")
        with self.assertRaisesRegex(MODULE.ConsentRevocationError, "missing fields"):
            MODULE.plan_consent_revocation(revocation, records)

    def test_output_is_deterministic_and_input_is_not_mutated(self) -> None:
        revocation, records = fixture()
        original = copy.deepcopy(records)
        first = MODULE.plan_consent_revocation(revocation, records)
        second = MODULE.plan_consent_revocation(revocation, records)
        self.assertEqual(first, second)
        self.assertEqual(records, original)

    def test_tampered_plan_is_detected(self) -> None:
        revocation, records = fixture()
        plan = MODULE.plan_consent_revocation(revocation, records)
        plan["impacted_artifacts"][0]["execution_performed"] = True
        errors = MODULE.validate_revocation_plan(plan)
        self.assertIn("impacted artifact crosses the proposal boundary", errors)

    def test_no_actual_consent_action_is_invoked(self) -> None:
        revocation, records = fixture()
        plan = MODULE.plan_consent_revocation(revocation, records)
        serialized = json.dumps(plan, sort_keys=True)
        for action in ("DELETE_CACHE", "DELETE_EMBEDDING", "DELETE_ORIGINAL", "PERSIST_CONSENT_REVOCATION"):
            self.assertNotIn(action, serialized)
        self.assertEqual(plan["mode"], "PROPOSAL_ONLY")


if __name__ == "__main__":
    unittest.main()
