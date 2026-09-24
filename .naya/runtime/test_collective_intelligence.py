from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
sys.path.insert(0, str(RUNTIME))
SCRIPT = RUNTIME / "collective_intelligence.py"
SPEC = importlib.util.spec_from_file_location("collective_intelligence", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def consent_plan() -> dict:
    return {
        "schema": "NAYAPOWER_CONSENT_REVOCATION_PLAN_V1",
        "mode": "PROPOSAL_ONLY",
        "status": "COMPLETE",
        "revocation_sha256": "a" * 64,
        "persistence_performed": False,
        "impacted_artifacts": [],
        "source_actions": [],
        "unresolved": [],
    }


def item() -> dict:
    return {
        "intelligence_id": "PRIVATE-A",
        "content": "private content must not be projected",
        "visibility": "PRIVATE",
        "source_ids": ["SOURCE-A"],
        "consent": {"state": "EXPLICIT", "grant_id": "grant-1", "scope": ["COLLECTIVE"]},
        "sharing_policy": {"state": "APPROVED", "policy_ref": "policy-1", "allowed_scopes": ["COLLECTIVE"]},
        "identity_policy": {
            "state": "VERIFIED",
            "anonymization_verified": True,
            "identity_boundary": "aggregate-only",
            "identity_policy_ref": "identity-policy-1",
            "raw_owner_identity_exposed": False,
        },
        "source_authority": {"state": "VERIFIED", "authority_ref": "authority-1"},
        "contribution_provenance": [{"contribution_id": "contribution-1", "source_ref": "SOURCE-A", "provenance_hash": "b" * 64}],
        "revocation_state": "ACTIVE",
        "usage_scope": "collective intelligence only",
    }


class CollectiveIntelligenceTests(unittest.TestCase):
    def test_valid_private_item_projects_metadata_only(self) -> None:
        plan = MODULE.evaluate_collective_intelligence([item()], consent_plan())
        self.assertEqual(plan["status"], "COMPLETE")
        self.assertEqual(plan["pipeline"], list(MODULE.PIPELINE))
        self.assertEqual(plan["eligible_item_ids"], ["PRIVATE-A"])
        self.assertEqual(MODULE.validate_collective_plan(plan), [])
        proposal = plan["items"][0]["proposed_collective"]
        self.assertEqual(proposal["status"], "PROPOSED")
        self.assertEqual(proposal["visibility"], "COLLECTIVE")
        self.assertEqual(proposal["source_authority"]["authority_ref"], "authority-1")
        self.assertEqual(proposal["consent"]["grant_id"], "grant-1")
        self.assertNotIn("private content", json.dumps(proposal, sort_keys=True))
        self.assertFalse(plan["publication_performed"])

    def test_missing_consent_plan_fails_closed(self) -> None:
        with self.assertRaisesRegex(MODULE.CollectiveIntelligenceError, "System 44 consent plan"):
            MODULE.evaluate_collective_intelligence([item()])

    def test_owner_consent_is_required(self) -> None:
        value = item()
        value["consent"]["state"] = "REVOKED"
        plan = MODULE.evaluate_collective_intelligence([value], consent_plan())
        self.assertEqual(plan["status"], "BLOCKED")
        self.assertIn("OWNER_CONSENT_FOR_COLLECTIVE_REQUIRED", plan["items"][0]["reasons"])
        self.assertIsNone(plan["items"][0]["proposed_collective"])

    def test_sharing_policy_is_required(self) -> None:
        value = item()
        value["sharing_policy"]["state"] = "DENIED"
        plan = MODULE.evaluate_collective_intelligence([value], consent_plan())
        self.assertEqual(plan["status"], "BLOCKED")
        self.assertIn("SHARING_POLICY_REQUIRED", plan["items"][0]["reasons"])

    def test_anonymization_policy_is_required(self) -> None:
        value = item()
        value["identity_policy"]["anonymization_verified"] = False
        plan = MODULE.evaluate_collective_intelligence([value], consent_plan())
        self.assertEqual(plan["status"], "BLOCKED")
        self.assertIn("ANONYMIZATION_IDENTITY_POLICY_REQUIRED", plan["items"][0]["reasons"])

    def test_source_authority_and_provenance_are_required(self) -> None:
        value = item()
        value["source_authority"] = {}
        value["contribution_provenance"] = []
        plan = MODULE.evaluate_collective_intelligence([value], consent_plan())
        self.assertEqual(plan["status"], "BLOCKED")
        self.assertIn("SOURCE_AUTHORITY_REQUIRED", plan["items"][0]["reasons"])
        self.assertIn("CONTRIBUTION_PROVENANCE_REQUIRED", plan["items"][0]["reasons"])

    def test_visibility_must_begin_private(self) -> None:
        value = item()
        value["visibility"] = "COLLECTIVE"
        plan = MODULE.evaluate_collective_intelligence([value], consent_plan())
        self.assertEqual(plan["status"], "BLOCKED")
        self.assertIn("INPUT_MUST_BE_PRIVATE", plan["items"][0]["reasons"])

    def test_system44_revocation_impact_blocks_collective_proposal(self) -> None:
        plan_input = consent_plan()
        plan_input["impacted_artifacts"] = [{"intelligence_id": "SOURCE-A", "required_actions": ["RESTRICT_DERIVED_USE"]}]
        plan = MODULE.evaluate_collective_intelligence([item()], plan_input)
        self.assertEqual(plan["status"], "BLOCKED")
        self.assertIn("CONSENT_REVOCATION_REVIEW_REQUIRED", plan["items"][0]["reasons"])

    def test_partial_consent_plan_remains_partial(self) -> None:
        plan_input = consent_plan()
        plan_input["status"] = "PARTIAL"
        plan = MODULE.evaluate_collective_intelligence([item()], plan_input)
        self.assertEqual(plan["status"], "PARTIAL")
        self.assertIn("CONSENT_PLAN_NOT_COMPLETE", {item["code"] for item in plan["unresolved"]})

    def test_output_is_deterministic_and_input_is_not_mutated(self) -> None:
        value = item()
        original = copy.deepcopy(value)
        first = MODULE.evaluate_collective_intelligence([value], consent_plan())
        second = MODULE.evaluate_collective_intelligence([value], consent_plan())
        self.assertEqual(first, second)
        self.assertEqual(value, original)

    def test_no_publication_or_federation_boundary(self) -> None:
        plan = MODULE.evaluate_collective_intelligence([item()], consent_plan())
        self.assertEqual(plan["mode"], "PROPOSAL_ONLY")
        self.assertFalse(plan["execution_performed"])
        self.assertFalse(plan["publication_performed"])
        self.assertFalse(plan["persistence_performed"])
        self.assertNotIn("federation", plan)
        self.assertNotIn("published", plan["items"][0]["proposed_collective"])


if __name__ == "__main__":
    unittest.main()
