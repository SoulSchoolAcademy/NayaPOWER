#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".naya" / "runtime"
sys.path.insert(0, str(RUNTIME))

from universal_execution_gate import DecisionObject, Epistemic, Risk, UniversalExecutionGate, VerificationPlan, load_registry
from execution_preflight_gate import approved_preflight
import execution_controller as EC
import model_tool_gateway as MTG


def identity_for(authority):
    return {
        "schema_version": "1.0",
        "identity_id": authority.principal_id,
        "actor_class": "HUMAN",
        "who_created_or_delegated": {"creator_ref": "human-controller", "delegator_ref": None, "lineage_state": "ROOT"},
        "knowledge": [{
            "knowledge_id": "K-E2E-001",
            "claim": "The requested action is the exact governed execution target.",
            "source_refs": ["test:request"],
            "epistemic_state": "VERIFIED",
        }],
        "capabilities": ["repo_write"],
        "authority": {"authority_ids": [authority.authority_id]},
        "authorized_by": [{"authority_id": authority.authority_id, "authorizer_ref": "human-controller"}],
        "received_artifacts": [{
            "artifact_id": "ART-E2E-001",
            "artifact_type": "execution_request",
            "source_ref": "test:request",
            "received_at": "2026-09-19T00:00:00Z",
        }],
        "provenance": [{"subject_id": "ART-E2E-001", "source_ref": "test:request", "relation": "received_from"}],
        "delegation": {"can_delegate": False, "delegation_scope": [], "chain": []},
        "actual_actions": [],
        "outcomes": [],
        "learning": [],
    }


class GovernedRuntimeIdentityLoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="naya-runtime-loop-"))
        EC.STATE = self.tmp / "EXECUTION-STATE.json"
        EC.EVENTS_ROOT = self.tmp / "events"
        EC.INDEX_PATH = EC.EVENTS_ROOT / "INDEX.json"
        EC.SESSIONS_ROOT = self.tmp / "sessions"
        EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"
        self.registry = load_registry()
        self.authority = self.registry.resolve("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")
        self.identity = identity_for(self.authority)
        self.gate = UniversalExecutionGate(self.registry)
        self.decision = DecisionObject(
            decision_id="LOOP-DEC-001",
            mission="Execute one governed repository action through the live runtime path",
            actor_id=self.authority.principal_id,
            action="repo_write",
            purpose=self.authority.purpose,
            scope=self.authority.scope,
            current_truth="The live gateway/controller path exists.",
            gap="Identity binding must survive the full execution lifecycle.",
            evidence=("test:e2e",),
            epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
            consequence="A bounded repository write may change governed source.",
            reversible=True,
            risk=Risk(1, 1, 1),
            alternatives=("do_not_execute",),
            expected_value="Preserve identity lineage through actual execution and verified receipt.",
            required_permission="repo_write",
            verification=VerificationPlan("Observe the completed test action and verify its receipt.", "Activity and Smart Ledger bindings match the authorization."),
            necessary_power=frozenset({"repo_write"}),
            requested_power=frozenset({"repo_write"}),
        )
        self.action = {
            "action_id": "LOOP-ACT-001",
            "action_type": "repository_write",
            "target": "docs/Naya",
            "purpose": self.authority.purpose,
            "risk": "L2",
            "protected_baseline": "test-head",
            "observation_target": "created temporary governed execution marker",
            "evidence_requirement": ["command_output", "commit_sha"],
            "verification_requirement": ["smart_ledger_receipt", "activity_event"],
            "authority_id": self.authority.authority_id,
            "decision_id": self.decision.decision_id,
            "actor_id": self.authority.principal_id,
            "scope": self.authority.scope,
            "permission": "repo_write",
        }
        EC.transition(
            "CLAIMED",
            claim_id="LOOP-CLAIM-001",
            block_id="LOOP-BLOCK-001",
            owner=self.authority.principal_id,
            scope=[self.authority.scope],
            start_head="test-head",
        )
        issued = self.gate.authorize(
            authority=self.authority,
            decision=self.decision,
            action=self.action,
            identity_envelope=self.identity,
            consequential=True,
            now="2026-09-19T01:05:00+00:00",
        )
        self.assertTrue(issued.allowed, issued.reasons)
        self.credential = issued.authorization

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_full_gateway_to_controller_to_ledger_to_activity(self):
        authorized = MTG.authorize(
            self.action,
            execution_authorization=self.credential,
            gate=self.gate,
            identity_envelope=self.identity,
            preflight=approved_preflight(),
        )
        self.assertEqual(authorized["status"], "AUTHORIZED")
        self.assertEqual(authorized["execution_status"], "EXECUTING")
        self.assertEqual(authorized["identity_id"], self.authority.principal_id)
        self.assertEqual(authorized["identity_fingerprint"], self.credential.identity_fingerprint)
        self.assertEqual(authorized["identity_binding_hash"], self.credential.identity_binding_hash)

        marker = self.tmp / "actual-action.txt"
        marker.write_text("REAL_TEST_ACTION_EXECUTED\n", encoding="utf-8")
        observed = EC.transition(
            "OBSERVED",
            observation="Observed the actual side effect in a temporary execution target.",
            execution_authorization=self.credential,
            gate=self.gate,
            identity_envelope=self.identity,
            execution_result={
                "execution_state": "COMPLETED",
                "execution_id": self.action["action_id"],
                "action_id": self.action["action_id"],
                "action": "write governed execution marker",
                "action_ref": "tool:filesystem:test-marker",
                "observed_output": marker.read_text(encoding="utf-8").strip(),
                "result": "PASS",
                "commit_sha": "test-head",
                "command": "write temporary execution marker",
                "environment": "windows-test",
                "source": "governed-runtime-loop-test",
                "outcome_ref": "outcome:LOOP-ACT-001",
            },
        )
        self.assertEqual(observed["status"], "OBSERVED")
        self.assertEqual(observed["smart_ledger"]["verification_receipt"]["verification_state"], "verified")
        self.assertEqual(observed["identity_binding"]["identity_id"], self.authority.principal_id)

        verified = EC.transition(
            "VERIFIED",
            evidence=[observed["execution_evidence"]["evidence_id"], observed["smart_ledger"]["ledger_event"]["ledger_event_id"]],
            verification={"status": "VERIFIED", "method": "governed-runtime-loop-test"},
            next_action="Continue with controller/tool-gateway integration verification.",
            successor="NEXT-GOVERNED-RUNTIME-IDENTITY-LOOP.md",
        )
        self.assertEqual(verified["status"], "VERIFIED")

        event_path = next(self.tmp.joinpath("events").rglob("SE-*.json"))
        event = json.loads(event_path.read_text(encoding="utf-8"))
        execution = event["execution"]
        self.assertEqual(execution["identity_id"], self.authority.principal_id)
        self.assertEqual(execution["identity_fingerprint"], self.credential.identity_fingerprint)
        self.assertEqual(execution["identity_binding_hash"], self.credential.identity_binding_hash)
        self.assertEqual(execution["execution_authorization_binding_hash"], self.credential.binding_hash)
        self.assertEqual(execution["smart_ledger_event_id"], observed["smart_ledger"]["ledger_event"]["ledger_event_id"])
        self.assertEqual(execution["smart_ledger_receipt_id"], observed["smart_ledger"]["verification_receipt"]["receipt_id"])

        checked = EC.validate()
        self.assertEqual(checked["execution_status"], "VERIFIED")

    def test_identity_tamper_at_observed_is_rejected(self):
        MTG.authorize(
            self.action,
            execution_authorization=self.credential,
            gate=self.gate,
            identity_envelope=self.identity,
            preflight=approved_preflight(),
        )
        tampered = dict(self.identity)
        tampered["capabilities"] = ["repo_write", "deploy_public_runtime"]
        with self.assertRaises(AssertionError) as ctx:
            EC.transition(
                "OBSERVED",
                observation="attempt",
                execution_authorization=self.credential,
                gate=self.gate,
                identity_envelope=tampered,
                execution_result={
                    "execution_state": "COMPLETED",
                    "execution_id": self.action["action_id"],
                    "action": "write marker",
                    "observed_output": "tamper",
                    "result": "PASS",
                    "commit_sha": "test-head",
                },
            )
        self.assertIn("authorization identity fingerprint", str(ctx.exception))

    def test_activity_binding_tamper_is_rejected_at_verification(self):
        MTG.authorize(
            self.action,
            execution_authorization=self.credential,
            gate=self.gate,
            identity_envelope=self.identity,
            preflight=approved_preflight(),
        )
        EC.transition(
            "OBSERVED",
            observation="Observed actual side effect.",
            execution_authorization=self.credential,
            gate=self.gate,
            identity_envelope=self.identity,
            execution_result={
                "execution_state": "COMPLETED",
                "execution_id": self.action["action_id"],
                "action": "write marker",
                "observed_output": "done",
                "result": "PASS",
                "commit_sha": "test-head",
            },
        )
        payload = EC.load()
        payload["identity_binding"]["identity_binding_hash"] = "0" * 64
        # No Activity event may be accepted against a tampered execution binding.
        EC.STATE.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(AssertionError) as ctx:
            EC.transition(
                "VERIFIED",
                evidence=["test"],
                verification={"status": "VERIFIED", "method": "tamper-test"},
                next_action="continue",
                successor="NEXT",
            )
        self.assertIn("identity/action binding", str(ctx.exception))

if __name__ == "__main__":
    unittest.main(verbosity=2)
