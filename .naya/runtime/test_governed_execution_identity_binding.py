#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
import unittest

RUNTIME = Path(__file__).resolve().parent
sys.path.insert(0, str(RUNTIME))

from governance_kernel import DecisionObject, Epistemic, Risk, VerificationPlan
from intelligence_identity import identity_binding_fingerprint, identity_fingerprint, validate_identity_envelope
from smart_ledger_engine import record_authorized_execution, verify_event
from universal_execution_gate import (
    ExecutionAction,
    UniversalExecutionGate,
    load_registry,
)


AUTHORITY_ID = "HUMAN-SOULSCHOOLACADEMY-REPO-WRITE"
ACTOR_ID = "SoulSchoolAcademy"
PURPOSE = "governed maintenance and verification of NayaPOWER"
SCOPE = "repo:SoulSchoolAcademy/NayaPOWER"


def identity_envelope() -> dict:
    return {
        "schema_version": "1.0",
        "identity_id": ACTOR_ID,
        "actor_class": "HUMAN",
        "who_created_or_delegated": {
            "creator_ref": "human-controller",
            "delegator_ref": None,
            "lineage_state": "ROOT",
        },
        "knowledge": [{
            "knowledge_id": "K-EXEC-001",
            "claim": "The canonical NayaPOWER repository is the current execution target.",
            "source_refs": ["github:repo/SoulSchoolAcademy/NayaPOWER"],
            "epistemic_state": "VERIFIED",
        }],
        "capabilities": ["repo_write"],
        "authority": {"authority_ids": [AUTHORITY_ID]},
        "authorized_by": [{
            "authority_id": AUTHORITY_ID,
            "authorizer_ref": "human-controller",
        }],
        "received_artifacts": [{
            "artifact_id": "ART-EXEC-001",
            "artifact_type": "governed_execution_request",
            "source_ref": "request:user",
            "received_at": "2026-09-18T00:00:00Z",
        }],
        "provenance": [{
            "subject_id": "ART-EXEC-001",
            "source_ref": "request:user",
            "relation": "received_from",
        }],
        "delegation": {
            "can_delegate": False,
            "delegation_scope": [],
            "chain": [],
        },
        "actual_actions": [],
        "outcomes": [],
        "learning": [],
    }


def decision() -> DecisionObject:
    return DecisionObject(
        decision_id="DEC-EXEC-001",
        mission="Verify governed execution identity binding",
        actor_id=ACTOR_ID,
        action="repo_write",
        purpose=PURPOSE,
        scope=SCOPE,
        current_truth="The canonical execution gate exists.",
        gap="The identity envelope is not yet bound into its authorization credential.",
        evidence=("evidence:governed-execution-identity-binding",),
        epistemic=frozenset({Epistemic.VERIFIED}),
        consequence="A repository write may change governed source.",
        reversible=True,
        risk=Risk(1, 1, 1),
        alternatives=("Inspect without mutation",),
        expected_value="Cryptographically bind actor identity/provenance to the exact authorized action.",
        required_permission="repo_write",
        verification=VerificationPlan(
            observation="Observe authorization and Smart Ledger receipt carrying matching identity/action bindings.",
            success_criteria="Tampering or actor/authority mismatch is rejected.",
        ),
        necessary_power=frozenset({"repo_write"}),
        requested_power=frozenset({"repo_write"}),
    )


def action() -> ExecutionAction:
    return ExecutionAction(
        action_id="EX-EXEC-001",
        action_type="repo_write",
        target="SoulSchoolAcademy/NayaPOWER",
        purpose=PURPOSE,
        scope=SCOPE,
        actor_id=ACTOR_ID,
        permission="repo_write",
        decision_id="DEC-EXEC-001",
        authority_id=AUTHORITY_ID,
    )


class GovernedExecutionIdentityBindingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = load_registry()
        self.authority = self.registry.resolve(AUTHORITY_ID)
        self.assertIsNotNone(self.authority)
        self.gate = UniversalExecutionGate(registry=self.registry)
        self.identity = identity_envelope()

    def test_identity_and_action_are_cryptographically_bound(self):
        validation = validate_identity_envelope(self.identity, consequential=True)
        self.assertTrue(validation.valid, validation.errors)
        result = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=self.identity,
            now="2026-09-18T18:00:00Z",
        )
        self.assertTrue(result.allowed, result.reasons)
        authorization = result.authorization
        self.assertIsNotNone(authorization)
        self.assertEqual(authorization.identity_id, ACTOR_ID)
        self.assertEqual(authorization.identity_fingerprint, identity_fingerprint(self.identity))
        expected = identity_binding_fingerprint(
            self.identity,
            {
                "authority_id": AUTHORITY_ID,
                "decision_id": "DEC-EXEC-001",
                "action_id": "EX-EXEC-001",
                "action_type": "repo_write",
                "target": "SoulSchoolAcademy/NayaPOWER",
                "actor_id": ACTOR_ID,
                "scope": SCOPE,
                "permission": "repo_write",
            },
        )
        self.assertEqual(authorization.identity_binding_hash, expected)

        ok, reasons = self.gate.verify(
            authorization,
            self.identity,
            now="2026-09-18T18:00:01Z",
        )
        self.assertTrue(ok, reasons)

    def test_identity_tampering_invalidates_authorization(self):
        result = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=self.identity,
            now="2026-09-18T18:00:00Z",
        )
        self.assertTrue(result.allowed)
        tampered = dict(self.identity)
        tampered["capabilities"] = ["repo_write", "deploy_public_runtime"]
        ok, reasons = self.gate.verify(result.authorization, tampered)
        self.assertFalse(ok)
        self.assertTrue(any("fingerprint" in reason or "binding" in reason for reason in reasons))

    def test_identity_actor_mismatch_is_rejected_before_authorization(self):
        tampered = dict(self.identity)
        tampered["identity_id"] = "unrelated-actor"
        result = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=tampered,
        )
        self.assertFalse(result.allowed)
        self.assertIn("identity_id does not match action actor_id", result.reasons)

    def test_identity_must_name_the_resolved_authority(self):
        tampered = dict(self.identity)
        tampered["authority"] = {"authority_ids": []}
        result = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=tampered,
        )
        self.assertFalse(result.allowed)
        self.assertIn("identity envelope does not name the resolved authority_id", result.reasons)

    def test_forged_copy_of_authorization_is_rejected(self):
        result = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=self.identity,
        )
        self.assertTrue(result.allowed)
        clone = replace(result.authorization)
        ok, reasons = self.gate.verify(clone, self.identity)
        self.assertFalse(ok)
        self.assertIn("execution authorization was not issued by this gate instance", reasons)

    def test_authorization_identity_fields_are_integrity_bound(self):
        result = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=self.identity,
        )
        self.assertTrue(result.allowed)
        tampered = replace(result.authorization, identity_id="forged")
        ok, reasons = self.gate.verify(tampered, self.identity)
        self.assertFalse(ok)
        self.assertIn("binding_hash does not match authorization fields", reasons)

    def test_smart_ledger_receipt_carries_identity_and_action_binding(self):
        authorization = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=self.identity,
        ).authorization
        self.assertIsNotNone(authorization)
        event, receipt = record_authorized_execution(
            self.gate,
            authorization,
            self.identity,
            action_ref="github:repo-write:EX-EXEC-001",
            evidence_ref="github:evidence:EX-EXEC-001",
            outcome_ref="outcome:EX-EXEC-001",
        )
        self.assertEqual(event.identity_id, ACTOR_ID)
        self.assertEqual(event.identity_fingerprint, identity_fingerprint(self.identity))
        self.assertEqual(event.identity_binding_hash, authorization.identity_binding_hash)
        self.assertEqual(event.execution_authorization_binding_hash, authorization.binding_hash)
        self.assertEqual(receipt["identity_fingerprint"], event.identity_fingerprint)
        self.assertEqual(receipt["identity_binding_hash"], event.identity_binding_hash)
        self.assertEqual(receipt["execution_authorization_binding_hash"], authorization.binding_hash)

    def test_smart_ledger_detects_identity_receipt_tampering(self):
        authorization = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=self.identity,
        ).authorization
        event, _ = record_authorized_execution(
            self.gate,
            authorization,
            self.identity,
            action_ref="github:repo-write:EX-EXEC-001",
            evidence_ref="github:evidence:EX-EXEC-001",
            outcome_ref="outcome:EX-EXEC-001",
        )
        tampered = replace(event, identity_fingerprint="0" * 64)
        with self.assertRaisesRegex(ValueError, "integrity verification failed"):
            verify_event(tampered)

    def test_smart_ledger_rejects_forged_authorization_copy(self):
        authorization = self.gate.authorize(
            authority=self.authority,
            decision=decision(),
            action=action(),
            identity_envelope=self.identity,
        ).authorization
        forged = replace(authorization)
        with self.assertRaisesRegex(ValueError, "not issued by this gate instance"):
            record_authorized_execution(
                self.gate,
                forged,
                self.identity,
                action_ref="github:repo-write:EX-EXEC-001",
                evidence_ref="github:evidence:EX-EXEC-001",
                outcome_ref="outcome:EX-EXEC-001",
            )

    def test_binding_is_deterministic_for_same_identity_and_action(self):
        execution = {
            "authority_id": AUTHORITY_ID,
            "decision_id": "DEC-EXEC-001",
            "action_id": "EX-EXEC-001",
            "action_type": "repo_write",
            "target": "SoulSchoolAcademy/NayaPOWER",
            "actor_id": ACTOR_ID,
            "scope": SCOPE,
            "permission": "repo_write",
        }
        self.assertEqual(
            identity_binding_fingerprint(self.identity, execution),
            identity_binding_fingerprint(self.identity, execution),
        )


if __name__ == "__main__":
    unittest.main()
