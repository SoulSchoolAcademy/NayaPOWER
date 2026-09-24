from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().with_name("distributed_naya.py")
SPEC = importlib.util.spec_from_file_location("distributed_naya", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def envelope(target: str = "NAYANET") -> dict:
    return {
        "envelope_id": "envelope-60-1",
        "source_runtime": "LOCAL",
        "target_runtime": target,
        "subject_identity": {"subject_id": "NAYA", "binding_status": "VERIFIED", "binding_ref": "binding-1"},
        "authority": {"state": "VERIFIED", "authority_ref": "authority-1"},
        "memory": {"state": "VERIFIED", "refs": ["memory-event-1"]},
        "provenance": {"state": "VERIFIED", "refs": ["provenance-1"], "payload_sha256": "a" * 64},
        "governance": {"state": "VERIFIED", "policy_ref": "governance-policy-1"},
        "continuity": {"state": "VERIFIED", "receipt_ref": "continuity-receipt-1", "cursor": "cursor-1"},
        "consent": {"state": "ACTIVE", "revocation_plan_status": "COMPLETE"},
        "capability_registry_version": "1.0.0",
        "smart_door_lifecycle_version": "1.0.0",
    }


class DistributedNayaTests(unittest.TestCase):
    def test_all_runtime_classes_are_supported_when_dimensions_verify(self) -> None:
        for target in ("LOCAL", "CLOUD", "MOBILE", "WEB", "AI_PROVIDER", "AGENT", "NAYANET"):
            if target == "LOCAL":
                continue
            plan = MODULE.plan_distributed_continuity(envelope(target))
            self.assertEqual(plan["status"], "COMPLETE", target)
            self.assertTrue(plan["eligible_for_transport"], target)
            self.assertEqual(plan["envelope"]["target_runtime"], target)
            self.assertEqual(MODULE.validate_continuity_plan(plan), [])

    def test_naya_identity_binding_is_required(self) -> None:
        value = envelope()
        value["subject_identity"]["binding_status"] = "NOT_ESTABLISHED"
        plan = MODULE.plan_distributed_continuity(value)
        self.assertEqual(plan["status"], "BLOCKED")
        self.assertIn("NAYA_SUBJECT_BINDING_NOT_ESTABLISHED", plan["blocked_reasons"])
        self.assertFalse(plan["eligible_for_transport"])

    def test_each_required_dimension_blocks_when_missing(self) -> None:
        cases = {
            "authority": ("authority", "AUTHORITY_UNVERIFIED"),
            "memory": ("memory", "MEMORY_UNVERIFIED"),
            "provenance": ("provenance", "PROVENANCE_UNVERIFIED"),
            "governance": ("governance", "GOVERNANCE_UNVERIFIED"),
            "continuity": ("continuity", "CONTINUITY_UNVERIFIED"),
            "consent": ("consent", "CONSENT_NOT_ACTIVE"),
        }
        for field, reason in cases.values():
            value = envelope()
            value[field] = {}
            plan = MODULE.plan_distributed_continuity(value)
            self.assertEqual(plan["status"], "BLOCKED", field)
            self.assertIn(reason, plan["blocked_reasons"], field)

    def test_revoked_consent_blocks(self) -> None:
        value = envelope()
        value["consent"]["state"] = "REVOKED"
        plan = MODULE.plan_distributed_continuity(value)
        self.assertEqual(plan["status"], "BLOCKED")
        self.assertIn("CONSENT_NOT_ACTIVE", plan["blocked_reasons"])

    def test_unknown_or_same_runtime_blocks(self) -> None:
        value = envelope("UNKNOWN")
        plan = MODULE.plan_distributed_continuity(value)
        self.assertIn("TARGET_RUNTIME_UNKNOWN", plan["blocked_reasons"])
        same = MODULE.plan_distributed_continuity(envelope("LOCAL"))
        self.assertIn("SAME_RUNTIME_ROUTE_NOT_DISTRIBUTED", same["blocked_reasons"])

    def test_raw_payload_is_refused_and_never_propagated(self) -> None:
        value = envelope()
        value["payload"] = "private raw content"
        plan = MODULE.plan_distributed_continuity(value)
        self.assertIn("RAW_PAYLOAD_FIELD_FORBIDDEN:payload", plan["blocked_reasons"])
        self.assertNotIn("private raw content", json.dumps(plan, sort_keys=True))
        self.assertFalse(plan["payload_propagated"])

    def test_output_is_deterministic_and_input_is_not_mutated(self) -> None:
        value = envelope()
        original = copy.deepcopy(value)
        first = MODULE.plan_distributed_continuity(value)
        second = MODULE.plan_distributed_continuity(value)
        self.assertEqual(first, second)
        self.assertEqual(value, original)

    def test_tampered_plan_is_detected(self) -> None:
        plan = MODULE.plan_distributed_continuity(envelope())
        plan["envelope"]["authority"]["authority_ref"] = "tampered"
        errors = MODULE.validate_continuity_plan(plan)
        self.assertIn("envelope fingerprint is invalid", errors)

    def test_no_network_or_federation_boundary(self) -> None:
        plan = MODULE.plan_distributed_continuity(envelope())
        self.assertEqual(plan["mode"], "PLAN_ONLY")
        self.assertFalse(plan["execution_performed"])
        self.assertFalse(plan["network_transport_performed"])
        self.assertFalse(plan["federation_created"])
        self.assertNotIn("federation_created", plan["dimensions"])


if __name__ == "__main__":
    unittest.main()
