import unittest
from dataclasses import replace

from smart_ledger_engine import (
    calculate_value,
    create_governed_execution_event,
    create_ledger_event,
    create_smart_note,
    determine_level,
    generate_smart_link,
    run_vertical_slice,
    verify_event,
)


class SmartLedgerEngineTests(unittest.TestCase):
    def test_end_to_end_vertical_slice(self):
        result = run_vertical_slice("A useful insight", "This is durable intelligence.", cumulative_points_before=45)
        self.assertEqual(result["ledger_event"]["event_type"], "SMART_NOTE_CREATED")
        self.assertEqual(result["ledger_event"]["status"], "verified")
        self.assertEqual(result["value_event"]["points"], 5)
        self.assertEqual(result["member"]["level"], 2)
        self.assertEqual(result["member"]["name"], "Emerging Member")
        self.assertEqual(result["smart_link"]["target_type"], "ledger_event")

    def test_value_requires_verification(self):
        note = create_smart_note("Test", "Content")
        event = create_ledger_event(note)
        with self.assertRaises(ValueError):
            calculate_value(event)

    def test_verification_requires_evidence_and_integrity(self):
        note = create_smart_note("Test", "Content")
        event = create_ledger_event(note)
        verified, receipt = verify_event(event)
        self.assertEqual(verified.status, "verified")
        self.assertEqual(receipt["verification_state"], "verified")
        tampered = replace(event, object_ref="note:tampered")
        with self.assertRaises(ValueError):
            verify_event(tampered)

    def test_governed_execution_receipt_is_verifiable_and_bound(self):
        governance = {
            "receipt_id": "govrcpt_TEST_001",
            "schema_version": "1.0",
            "actor_id": "agent-001",
            "authority_id": "AUTH-001",
            "decision_id": "DEC-001",
            "action_id": "ACT-001",
            "action_type": "repo_read",
            "target": "repo:NayaPOWER",
            "scope": "repo:NayaPOWER",
            "permission": "repo_read",
            "governance_state": "AUTHORIZED",
            "risk_tier": "L1",
            "capability_envelope": {"autonomous_action": True, "external_tools": True},
            "responsibility_controls": ["authority_bound", "durable_receipt", "identity_verified"],
            "binding_hash": "binding-hash-test",
            "validated_at": "2026-09-18T00:00:00Z",
        }
        event = create_governed_execution_event(
            governance,
            evidence_ref="execution:CLM-001:evidence",
            observation_ref="execution:CLM-001:observation",
            execution_verification_ref="execution:CLM-001:verification",
        )
        verified, receipt = verify_event(event)
        self.assertEqual(verified.event_type, "GOVERNED_EXECUTION_COMPLETED")
        self.assertEqual(verified.governance_receipt_id, "govrcpt_TEST_001")
        self.assertEqual(verified.governance_receipt["authority_id"], "AUTH-001")
        self.assertEqual(verified.observation_ref, "execution:CLM-001:observation")
        self.assertEqual(verified.execution_verification_ref, "execution:CLM-001:verification")
        self.assertEqual(receipt["verification_state"], "verified")

    def test_governed_execution_receipt_tampering_fails_integrity(self):
        governance = {
            "receipt_id": "govrcpt_TEST_002",
            "schema_version": "1.0",
            "actor_id": "agent-001",
            "authority_id": "AUTH-001",
            "decision_id": "DEC-002",
            "action_id": "ACT-002",
            "capability_envelope": {"autonomous_action": True},
            "responsibility_controls": ["identity_verified"],
            "binding_hash": "binding-hash-test",
        }
        event = create_governed_execution_event(
            governance,
            evidence_ref="execution:CLM-002:evidence",
            observation_ref="execution:CLM-002:observation",
            execution_verification_ref="execution:CLM-002:verification",
        )
        tampered = replace(event, governance_receipt_id="govrcpt-ATTACKER")
        with self.assertRaises(ValueError):
            verify_event(tampered)

    def test_governed_execution_requires_all_three_runtime_references(self):
        governance = {
            "receipt_id": "govrcpt_TEST_003",
            "schema_version": "1.0",
            "actor_id": "agent-001",
            "authority_id": "AUTH-001",
            "decision_id": "DEC-003",
            "action_id": "ACT-003",
            "capability_envelope": {"external_tools": True},
            "responsibility_controls": ["authority_bound"],
            "binding_hash": "binding-hash-test",
        }
        with self.assertRaises(ValueError):
            create_governed_execution_event(
                governance,
                evidence_ref="",
                observation_ref="execution:CLM-003:observation",
                execution_verification_ref="execution:CLM-003:verification",
            )
    def test_level_boundaries(self):
        self.assertEqual(determine_level(0)["level"], 1)
        self.assertEqual(determine_level(49)["level"], 1)
        self.assertEqual(determine_level(50)["level"], 2)
        self.assertEqual(determine_level(74999)["level"], 9)
        self.assertEqual(determine_level(75000)["level"], 10)

    def test_integrity_chain_changes_when_parent_changes(self):
        first = create_smart_note("First", "One")
        first_event = create_ledger_event(first)
        second = create_smart_note("Second", "Two")
        second_event = create_ledger_event(second, previous=first_event)
        self.assertEqual(second_event.previous_integrity_hash, first_event.integrity_hash)
        self.assertNotEqual(first_event.integrity_hash, second_event.integrity_hash)

    def test_smart_link_is_safe_reference(self):
        link = generate_smart_link("ledger_event", "ledger_123", access_class="authorized")
        self.assertEqual(link["target_ref"], "ledger_123")
        self.assertNotIn("actor_ref", link)


if __name__ == "__main__":
    unittest.main()
