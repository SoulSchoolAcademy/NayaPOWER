from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "smart_door_lifecycle.py"
SCHEMA_PATH = ROOT / "capabilities" / "smart-door-lifecycle.v1.schema.json"
SPEC = importlib.util.spec_from_file_location("smart_door_lifecycle", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def digest(character: str) -> str:
    return character * 64


def complete_run(capability_id: str = "pi.retrieve") -> MODULE.SmartDoorRun:
    run = MODULE.SmartDoorRun(capability_id, "request-48-1", "idempotency-48-1")
    run.record_request({"query": "current truth"}, ["project:NayaNET", "owner:authenticated_user"])
    run.record_authorization("authority-decision-1", digest("a"), "authorization-verifier-1")
    run.record_execution("executor-1", "execution-receipt-1", digest("b"))
    run.record_receive("received-artifact-1", digest("c"))
    run.record_verification("verifier-1", ["evidence-record-1"], digest("d"))
    run.record_persistence("persistence-receipt-1", "CREATED")
    run.record_index("index-receipt-1", ["canonical-event-1"])
    run.record_learning("learning-receipt-1", "CANDIDATE_ONLY")
    run.complete_run()
    return run


class SmartDoorLifecycleTests(unittest.TestCase):
    def test_exact_lifecycle_and_receipt_chain(self) -> None:
        run = complete_run()
        exported = run.export()
        self.assertEqual([receipt["state"] for receipt in exported["receipts"]], list(MODULE.LIFECYCLE))
        self.assertEqual(exported["state"], "COMPLETE")
        self.assertTrue(exported["complete"])
        self.assertEqual(MODULE.validate_run(exported), [])
        previous = None
        for receipt in exported["receipts"]:
            self.assertEqual(receipt["previous_receipt_sha256"], previous)
            previous = receipt["receipt_sha256"]
        self.assertEqual(exported["terminal_receipt_sha256"], previous)

    def test_registry_is_consumed_at_discover(self) -> None:
        run = MODULE.SmartDoorRun("pi.retrieve", "request-discover", "idempotency-discover")
        details = run.receipts[0]["details"]
        self.assertEqual(details["required_authority"], ["AUTHENTICATED_USER"])
        self.assertEqual(details["implementation_status"], "IMPLEMENTED")
        self.assertEqual(details["authority_enforcement"], "AUTHENTICATION_ONLY")
        self.assertIn("supabase/functions/nayanet-compound-intelligence/index.ts", details["source_paths"])

    def test_every_registered_capability_can_be_discovered(self) -> None:
        registry = json.loads((ROOT / "capabilities/registry.v1.json").read_text(encoding="utf-8"))
        for index, capability in enumerate(registry["capabilities"]):
            run = MODULE.SmartDoorRun(capability["id"], f"request-{index}", f"idempotency-{index}")
            self.assertEqual(run.receipts[0]["capability_id"], capability["id"])

    def test_unknown_capability_is_refused(self) -> None:
        with self.assertRaisesRegex(MODULE.SmartDoorError, "unknown capability"):
            MODULE.SmartDoorRun("unknown.capability", "request", "idempotency")

    def test_out_of_order_execution_is_refused(self) -> None:
        run = MODULE.SmartDoorRun("pi.retrieve", "request-order", "idempotency-order")
        with self.assertRaisesRegex(MODULE.SmartDoorError, "lifecycle requires REQUEST"):
            run.record_authorization("authority-1", digest("a"), "authorization-verifier-1")

    def test_scope_outside_registry_is_refused(self) -> None:
        run = MODULE.SmartDoorRun("pi.retrieve", "request-scope", "idempotency-scope")
        with self.assertRaisesRegex(MODULE.SmartDoorError, "exceeds the registered allowed_scope"):
            run.record_request({"query": "test"}, ["project:NayaNET", "repository:other"])

    def test_invalid_authority_or_execution_digest_is_refused(self) -> None:
        run = MODULE.SmartDoorRun("pi.retrieve", "request-digest", "idempotency-digest")
        run.record_request({"query": "test"}, ["project:NayaNET"])
        with self.assertRaisesRegex(MODULE.SmartDoorError, "SHA-256"):
            run.record_authorization("authority-1", "not-a-digest", "verifier-1")
        run.record_authorization("authority-1", digest("a"), "verifier-1")
        with self.assertRaisesRegex(MODULE.SmartDoorError, "SHA-256"):
            run.record_execution("executor-1", "execution-1", "not-a-digest")

    def test_executor_cannot_self_verify(self) -> None:
        run = MODULE.SmartDoorRun("pi.retrieve", "request-verify", "idempotency-verify")
        run.record_request({"query": "test"}, ["project:NayaNET"])
        run.record_authorization("authority-1", digest("a"), "authorization-verifier")
        run.record_execution("same-actor", "execution-1", digest("b"))
        run.record_receive("received-1", digest("c"))
        with self.assertRaisesRegex(MODULE.SmartDoorError, "must differ"):
            run.record_verification("same-actor", ["evidence-1"], digest("d"))

    def test_tampered_receipt_is_detected(self) -> None:
        exported = complete_run().export()
        tampered = copy.deepcopy(exported)
        tampered["receipts"][4]["details"]["verification_status"] = "BLOCKED"
        errors = MODULE.validate_run(tampered)
        self.assertTrue(any("receipt 4 digest is invalid" in error for error in errors))

    def test_incomplete_run_cannot_claim_complete(self) -> None:
        run = MODULE.SmartDoorRun("pi.retrieve", "request-incomplete", "idempotency-incomplete")
        exported = run.export()
        exported["state"] = "COMPLETE"
        exported["complete"] = True
        errors = MODULE.validate_run(exported)
        self.assertIn("complete run does not contain every lifecycle receipt", errors)

    def test_learning_cannot_promote_itself(self) -> None:
        run = MODULE.SmartDoorRun("pi.retrieve", "request-learning", "idempotency-learning")
        run.record_request({"query": "test"}, ["project:NayaNET"])
        run.record_authorization("authority-1", digest("a"), "authorization-verifier")
        run.record_execution("executor", "execution-1", digest("b"))
        run.record_receive("received-1", digest("c"))
        run.record_verification("verifier", ["evidence-1"], digest("d"))
        run.record_persistence("persistence-1", "REPLAYED")
        run.record_index("index-1", ["event-1"])
        with self.assertRaisesRegex(MODULE.SmartDoorError, "permits only"):
            run.record_learning("learning-1", "VERIFIED_ADAPTATION")
        run.record_learning("learning-1", "NO_LEARNING")
        exported = run.complete_run()
        self.assertTrue(exported["receipts"][-1]["details"]["authority_unchanged"])

    def test_lifecycle_schema_contract(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        exported = complete_run().export()
        self.assertEqual(set(exported), set(schema["required"]))
        self.assertEqual(set(exported), set(schema["properties"]))
        self.assertEqual(exported["schema"], schema["properties"]["schema"]["const"])
        self.assertEqual(len(exported["receipts"]), schema["properties"]["receipts"]["maxItems"])


if __name__ == "__main__":
    unittest.main()
