#!/usr/bin/env python3
from __future__ import annotations

import unittest

from intelligence_identity import identity_fingerprint, validate_identity_envelope


def valid_envelope() -> dict:
    return {
        "schema_version": "1.0",
        "identity_id": "naya:example-001",
        "actor_class": "NAYA",
        "who_created_or_delegated": {
            "creator_ref": "human:root",
            "delegator_ref": None,
            "lineage_state": "CREATED",
        },
        "knowledge": [{
            "knowledge_id": "K-001",
            "claim": "The test fixture exists.",
            "source_refs": ["source:test-fixture"],
            "epistemic_state": "VERIFIED",
        }],
        "capabilities": ["read_repo", "summarize"],
        "authority": {"authority_ids": ["AUTH-EXAMPLE-001"]},
        "authorized_by": [{
            "authority_id": "AUTH-EXAMPLE-001",
            "authorizer_ref": "human:root",
        }],
        "received_artifacts": [{
            "artifact_id": "ART-001",
            "artifact_type": "smart_note",
            "source_ref": "source:test-fixture",
            "received_at": "2026-09-18T00:00:00Z",
        }],
        "provenance": [{
            "subject_id": "ART-001",
            "source_ref": "source:test-fixture",
            "relation": "received_from",
        }],
        "delegation": {
            "can_delegate": False,
            "delegation_scope": [],
            "chain": [],
        },
        "actual_actions": [{
            "execution_id": "EX-001",
            "action_ref": "action:test",
            "receipt_ref": "receipt:EX-001",
        }],
        "outcomes": [{
            "execution_id": "EX-001",
            "outcome_ref": "outcome:EX-001",
            "evidence_refs": ["evidence:EX-001"],
            "verification_state": "VERIFIED",
        }],
        "learning": [{
            "learning_id": "L-001",
            "claim": "The identity lineage remained intact.",
            "source_refs": ["evidence:EX-001"],
            "derivation_state": "SUPPORTED",
        }],
    }


class GovernedIntelligenceIdentityTests(unittest.TestCase):
    def test_valid_identity_passes(self):
        result = validate_identity_envelope(valid_envelope(), consequential=True)
        self.assertTrue(result.valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.identity_fingerprint), 64)

    def test_unknown_identity_fails_consequentially(self):
        item = valid_envelope()
        item["actor_class"] = "UNKNOWN"
        result = validate_identity_envelope(item, consequential=True)
        self.assertFalse(result.valid)
        self.assertIn("UNKNOWN identity cannot perform consequential actions", result.errors)

    def test_delegated_identity_requires_delegator(self):
        item = valid_envelope()
        item["who_created_or_delegated"] = {
            "creator_ref": "human:root",
            "delegator_ref": None,
            "lineage_state": "DELEGATED",
        }
        result = validate_identity_envelope(item)
        self.assertFalse(result.valid)
        self.assertIn("DELEGATED identity requires delegator_ref", result.errors)

    def test_received_artifact_requires_source_and_provenance(self):
        item = valid_envelope()
        item["received_artifacts"][0]["source_ref"] = ""
        result = validate_identity_envelope(item)
        self.assertFalse(result.valid)
        self.assertIn("received_artifacts[0] requires source_ref", result.errors)

    def test_knowledge_without_sources_is_not_accepted(self):
        item = valid_envelope()
        item["knowledge"][0]["source_refs"] = []
        result = validate_identity_envelope(item)
        self.assertFalse(result.valid)
        self.assertIn("knowledge[0] requires source_refs", result.errors)

    def test_capability_does_not_create_authority(self):
        item = valid_envelope()
        item["authority"] = {"authority_ids": []}
        result = validate_identity_envelope(item)
        self.assertFalse(result.valid)
        self.assertIn("capability presence does not establish authority", result.errors)

    def test_delegation_requires_authority_and_chain(self):
        item = valid_envelope()
        item["delegation"] = {
            "can_delegate": True,
            "delegation_scope": ["read_repo"],
            "chain": [],
        }
        result = validate_identity_envelope(item)
        self.assertFalse(result.valid)
        self.assertIn("can_delegate=true requires a delegation chain", result.errors)

    def test_actual_action_requires_execution_receipt(self):
        item = valid_envelope()
        item["actual_actions"][0]["receipt_ref"] = ""
        result = validate_identity_envelope(item)
        self.assertFalse(result.valid)
        self.assertIn("actual_actions[0] requires receipt_ref", result.errors)

    def test_outcome_requires_evidence(self):
        item = valid_envelope()
        item["outcomes"][0]["evidence_refs"] = []
        result = validate_identity_envelope(item)
        self.assertFalse(result.valid)
        self.assertIn("outcomes[0] requires evidence_refs", result.errors)

    def test_learning_requires_source_refs(self):
        item = valid_envelope()
        item["learning"][0]["source_refs"] = []
        result = validate_identity_envelope(item)
        self.assertFalse(result.valid)
        self.assertIn("learning[0] requires source_refs", result.errors)

    def test_fingerprint_changes_when_identity_state_changes(self):
        item = valid_envelope()
        first = identity_fingerprint(item)
        item["capabilities"].append("external_tool")
        second = identity_fingerprint(item)
        self.assertNotEqual(first, second)

    def test_provenance_is_structurally_separate_from_identity(self):
        item = valid_envelope()
        self.assertIn("received_artifacts", item)
        self.assertIn("provenance", item)
        self.assertNotEqual(item["received_artifacts"], item["provenance"])

if __name__ == "__main__":
    unittest.main()
