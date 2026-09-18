#!/usr/bin/env python3
"""Universal Execution Gate (v1) isolated test suite.

Safe, in-memory. No repository state is written. The only filesystem writes are
to a temporary directory (tempfile) for time-of-use revocation tests.

Run:  python tests/test_universal_execution_gate.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
WG_PATH = ROOT / ".naya" / "control-plane" / "workflow_gate.py"

_gate_spec = importlib.util.spec_from_file_location("naya_universal_execution_gate", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

_wg_spec = importlib.util.spec_from_file_location("naya_workflow_gate", WG_PATH)
assert _wg_spec and _wg_spec.loader
WG = importlib.util.module_from_spec(_wg_spec)
sys.modules[WG.__name__] = WG
_wg_spec.loader.exec_module(WG)


def now_iso(offset_seconds: int = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=offset_seconds)).isoformat()


class TestUniversalExecutionGate(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = GATE.load_registry()
        self.authority = WG.resolve_authority(
            self.registry,
            actor="SoulSchoolAcademy",
            purpose="governed maintenance and verification of NayaPOWER",
            permission="repo_write",
            scope="repo:SoulSchoolAcademy/NayaPOWER",
        )
        self.gate = GATE.UniversalExecutionGate(self.registry)
        self.decision_id = "UEG-DEC-001"
        self.action_id = "UEG-ACT-001"
        self.decision = self._decision()
        self.action = self._action()

    # ---- build helpers -------------------------------------------------
    def _decision(self, **overrides):
        values = dict(
            decision_id=self.decision_id,
            mission="NayaPOWER governed repository maintenance",
            actor_id=self.authority.principal_id,
            action="repo_write",
            purpose=self.authority.purpose,
            scope=self.authority.scope,
            current_truth="repository mutation requested",
            gap="mutation requires canonical governance decision",
            evidence=("evidence:registry-grant",),
            epistemic=frozenset({GATE.Epistemic.OBSERVED, GATE.Epistemic.VERIFIED}),
            consequence="repository write under bounded governance",
            reversible=True,
            risk=GATE.Risk(uncertainty=1, consequence=2, irreversibility=1),
            alternatives=("do_not_execute",),
            expected_value="authorized bounded mutation",
            required_permission="repo_write",
            verification=GATE.VerificationPlan("post-write state", "verification passes", ("stop",)),
            necessary_power=frozenset({"repo_write"}),
            requested_power=frozenset({"repo_write"}),
        )
        values.update(overrides)
        return GATE.DecisionObject(**values)

    def _action(self, **overrides):
        values = dict(
            action_id=self.action_id,
            action_type="repository_write",
            target="docs/Naya",
            purpose=self.authority.purpose,
            scope=self.authority.scope,
            actor_id=self.authority.principal_id,
            permission="repo_write",
            decision_id=self.decision_id,
            authority_id=self.authority.authority_id,
        )
        values.update(overrides)
        return values

    def _authority(self, **overrides):
        values = dict(
            authority_id=self.authority.authority_id,
            principal_id=self.authority.principal_id,
            purpose=self.authority.purpose,
            scope=self.authority.scope,
            granted_actions=self.authority.granted_actions,
            expires_at=self.authority.expires_at,
            revoked=False,
        )
        values.update(overrides)
        return GATE.Authority(**values)

    def _allowed(self, **kwargs):
        return self.gate.authorize(authority=self.authority, decision=self.decision, action=self.action, **kwargs)

    # ---- VALID ---------------------------------------------------------
    def test_001_valid_registry_authority_allows(self):
        result = self._allowed()
        self.assertTrue(result.allowed)
        self.assertEqual(result.authorization.authority_id, self.authority.authority_id)

    # ---- INVALID -------------------------------------------------------
    def test_101_no_authority_refused(self):
        result = self.gate.authorize(authority=None, decision=self.decision, action=self.action)
        self.assertFalse(result.allowed)
        self.assertIn("no authority supplied", result.reasons)

    def test_102_fake_authority_refused(self):
        forged = GATE.Authority(
            authority_id="HUMAN-FORGED",
            principal_id="SoulSchoolAcademy",
            purpose="governed maintenance and verification of NayaPOWER",
            scope="repo:SoulSchoolAcademy/NayaPOWER",
            granted_actions=frozenset({"repo_write"}),
        )
        result = self.gate.authorize(authority=forged, decision=self.decision, action=self.action)
        self.assertFalse(result.allowed)
        self.assertIn("not present in the canonical registry", " ".join(result.reasons))

    def test_103_forged_object_with_real_id_refused(self):
        forged = self._authority(scope="repo:attacker/other")
        result = self.gate.authorize(authority=forged, decision=self.decision, action=self.action)
        self.assertFalse(result.allowed)
        self.assertIn("provenance failure", " ".join(result.reasons))

    def test_104_revoked_authority_refused(self):
        result = self.gate.authorize(authority=self._authority(revoked=True), decision=self.decision, action=self.action)
        self.assertFalse(result.allowed)
        self.assertIn("revoked", " ".join(result.reasons))

    def test_105_expired_authority_refused(self):
        expired = self._authority(expires_at=now_iso(-60))
        result = self.gate.authorize(authority=expired, decision=self.decision, action=self.action, now=now_iso(0))
        self.assertFalse(result.allowed)

    def test_106_wrong_actor_refused(self):
        result = self.gate.authorize(
            authority=self.authority,
            decision=self._decision(actor_id="someone_else"),
            action=self._action(actor_id="someone_else"),
        )
        self.assertFalse(result.allowed)
        self.assertIn("decision actor does not match authority principal", result.reasons)

    def test_107_wrong_purpose_refused(self):
        result = self.gate.authorize(
            authority=self.authority,
            decision=self._decision(purpose="different purpose"),
            action=self._action(purpose="different purpose"),
        )
        self.assertFalse(result.allowed)
        self.assertIn("decision purpose does not match authority purpose", result.reasons)

    def test_108_wrong_scope_refused(self):
        result = self.gate.authorize(
            authority=self.authority,
            decision=self._decision(scope="repo:attacker/other"),
            action=self._action(scope="repo:attacker/other"),
        )
        self.assertFalse(result.allowed)
        self.assertIn("decision scope does not match authority scope", result.reasons)

    def test_109_wrong_permission_refused(self):
        result = self.gate.authorize(
            authority=self.authority,
            decision=self.decision,
            action=self._action(permission="deploy_public_runtime"),
        )
        self.assertFalse(result.allowed)
        self.assertIn("action permission", " ".join(result.reasons))

    def test_110_ungranted_decision_action_refused(self):
        decision = self._decision(action="deploy_public_runtime", required_permission="deploy_public_runtime")
        action = self._action(permission="deploy_public_runtime")
        result = self.gate.authorize(authority=self.authority, decision=decision, action=action)
        self.assertFalse(result.allowed)
        self.assertIn("decision action is not granted by authority", result.reasons)

    def test_111_wrong_decision_id_refused(self):
        result = self.gate.authorize(
            authority=self.authority,
            decision=self.decision,
            action=self._action(decision_id="UEG-DEC-FORGED"),
        )
        self.assertFalse(result.allowed)
        self.assertIn("action decision_id does not match decision", result.reasons)

    def test_112_wrong_action_refused(self):
        other = self._action(
            action_id="UEG-ACT-OTHER",
            permission="repo_write",
            scope="repo:SoulSchoolAcademy/NayaPOWER:path:other",
        )
        result = self.gate.authorize(authority=self.authority, decision=self.decision, action=other)
        self.assertFalse(result.allowed)
        self.assertIn("action scope does not match decision scope", result.reasons)

    def test_113_kernel_denied_refused(self):
        decision = self._decision(epistemic=frozenset({GATE.Epistemic.OBSERVED, GATE.Epistemic.UNKNOWN}))
        result = self.gate.authorize(authority=self.authority, decision=decision, action=self.action)
        self.assertFalse(result.allowed)
        self.assertIn("material epistemic uncertainty remains", result.reasons)

    # ---- MODEL / STATE / CLAIM / RECEIPT BYPASS -------------------------
    def test_201_model_authorization_alone_refused(self):
        action = {**self.action, "authorization": "approved", "model_authorized": True, "agent_authorized": True}
        result = self.gate.authorize(authority=None, decision=None, action=action)
        self.assertFalse(result.allowed)
        self.assertIn("no authority supplied", result.reasons)
        self.assertIn("no decision supplied", result.reasons)

    def test_202_model_authorization_is_irrelevant_to_valid_success(self):
        action = {**self.action, "authorization": "approved", "model_authorized": True}
        result = self.gate.authorize(authority=self.authority, decision=self.decision, action=action)
        self.assertTrue(result.allowed)

    def test_203_execution_state_alone_refused(self):
        action = {**self.action, "execution_status": "EXECUTING", "status": "EXECUTING"}
        result = self.gate.authorize(authority=None, decision=None, action=action)
        self.assertFalse(result.allowed)

    def test_204_claim_alone_refused(self):
        action = {**self.action, "claim": {"status": "CLAIMED", "authorized": True}, "claim_id": "CL-1"}
        result = self.gate.authorize(authority=None, decision=None, action=action)
        self.assertFalse(result.allowed)
        self.assertIn("no authority supplied", result.reasons)

    def test_205_receipt_alone_refused(self):
        action = {**self.action, "receipt": {"status": "verified", "authorized": True}}
        result = self.gate.authorize(authority=None, decision=None, action=action)
        self.assertFalse(result.allowed)
        self.assertIn("no authority supplied", result.reasons)

    # ---- SWAPS ---------------------------------------------------------
    def test_301_decision_swap_refused(self):
        decision = self._decision()  # D1 for repo_write
        other = self._action(
            action_id="UEG-ACT-DEPLOY",
            decision_id=self.decision_id,
            permission="deploy_public_runtime",
            scope="public-runtime:sparkling-shape-7ae5:/",
            action_type="deploy",
            target="worker",
        )
        result = self.gate.authorize(authority=self.authority, decision=decision, action=other)
        self.assertFalse(result.allowed)

    def test_302_authority_swap_refused(self):
        decision = self._decision(
            decision_id="UEG-DEC-A2",
            action="deploy_public_runtime",
            purpose="deploy the canonical 509 NayaNET Intelligent Hub public runtime",
            scope="public-runtime:sparkling-shape-7ae5:/",
            required_permission="deploy_public_runtime",
            necessary_power=frozenset({"deploy_public_runtime"}),
            requested_power=frozenset({"deploy_public_runtime"}),
        )
        action = self._action(
            action_id="UEG-ACT-A2",
            decision_id="UEG-DEC-A2",
            permission="deploy_public_runtime",
            purpose=decision.purpose,
            scope=decision.scope,
            action_type="deploy",
            target="sparkling-shape-7ae5",
        )
        result = self.gate.authorize(authority=self.authority, decision=decision, action=action)
        self.assertFalse(result.allowed)
        self.assertIn("decision action is not granted by authority", result.reasons)

    # ---- TIME OF USE ---------------------------------------------------
    def test_401_revocation_between_authorization_and_execution(self):
        with tempfile.TemporaryDirectory(prefix="ueg-test-") as tmp:
            path = Path(tmp) / "authority-registry.json"
            payload = {
                "authorities": [
                    {
                        "authority_id": self.authority.authority_id,
                        "principal_id": self.authority.principal_id,
                        "purpose": self.authority.purpose,
                        "scope": self.authority.scope,
                        "granted_actions": ["repo_write"],
                        "expires_at": None,
                        "revoked": False,
                    }
                ]
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            gate = GATE.UniversalExecutionGate(registry_path=path)
            registry = gate._current_registry()
            authority = registry.resolve(self.authority.authority_id)
            decision = self._decision()
            action = self._action(authority_id=authority.authority_id)
            t0 = gate.authorize(authority=authority, decision=decision, action=action, now=now_iso(0))
            self.assertTrue(t0.allowed)
            payload["authorities"][0]["revoked"] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            t2 = gate.authorize(authority=authority, decision=decision, action=action, now=now_iso(30))
            self.assertFalse(t2.allowed, "revocation between T0 and T2 was not detected")

    def test_402_expiry_between_authorization_and_execution(self):
        grant = self._authority(expires_at=now_iso(10))
        registry = GATE.AuthorityRegistry({grant.authority_id: grant})
        gate = GATE.UniversalExecutionGate(registry)
        t0 = gate.authorize(authority=grant, decision=self._decision(), action=self.action, now=now_iso(-1))
        self.assertTrue(t0.allowed)
        t2 = gate.authorize(authority=grant, decision=self._decision(), action=self.action, now=now_iso(20))
        self.assertFalse(t2.allowed, "expiry between T0 and T2 was not detected")

    # ---- GATE CANNOT MINT / EXPAND / OVERRIDE --------------------------
    def test_501_gate_cannot_mint_authority(self):
        for name in ("create_authority", "mint_authority", "grant", "revoke", "delegate", "extend"):
            self.assertFalse(hasattr(GATE.UniversalExecutionGate, name), f"gate exposes {name}")
        result = self._allowed()
        authorization = result.authorization
        self.assertIsNotNone(authorization)
        self.assertNotIsInstance(authorization, GATE.Authority)
        self.assertIsInstance(authorization, GATE.ExecutionAuthorization)

    def test_502_gate_cannot_expand_scope_or_permission(self):
        wider = self._action(scope="repo:SoulSchoolAcademy")
        result = self.gate.authorize(authority=self.authority, decision=self.decision, action=wider)
        self.assertFalse(result.allowed)
        escalated = self._action(permission="production_admin")
        result = self.gate.authorize(authority=self.authority, decision=self.decision, action=escalated)
        self.assertFalse(result.allowed)
        self.assertIn("action permission", " ".join(result.reasons))

    def test_503_gate_cannot_override_kernel_denial(self):
        denied = self._decision(epistemic=frozenset({GATE.Epistemic.UNKNOWN}))
        result = self.gate.authorize(authority=self.authority, decision=denied, action=self.action)
        self.assertFalse(result.allowed)
        self.assertIn("material epistemic uncertainty remains", result.reasons)

    def test_504_gate_cannot_convert_refused_to_authorized(self):
        denied = self._decision(evidence=())
        result = self.gate.authorize(authority=self.authority, decision=denied, action=self.action)
        self.assertFalse(result.allowed)
        self.assertIsNone(result.authorization)

    def test_505_expired_then_kernel_deny_not_overridden(self):
        expired = self._authority(expires_at=now_iso(-60))
        result = self.gate.authorize(authority=expired, decision=self._decision(), action=self.action, now=now_iso(0))
        self.assertFalse(result.allowed)

    # ---- IDENTITY PRESERVATION ----------------------------------------
    def test_601_identity_binding_survives(self):
        result = self._allowed()
        auth = result.authorization
        self.assertEqual(auth.authority_id, self.authority.authority_id)
        self.assertEqual(auth.decision_id, self.decision_id)
        self.assertEqual(auth.action_id, self.action_id)
        self.assertEqual(auth.actor_id, self.authority.principal_id)
        self.assertEqual(auth.scope, self.authority.scope)
        self.assertEqual(auth.permission, "repo_write")
        self.assertEqual(auth.governance_state, "AUTHORIZED")
        self.assertEqual(len(auth.binding_hash), 64)
        again = self._allowed()
        self.assertEqual(auth.binding_hash, again.authorization.binding_hash)

    def test_602_identity_changes_when_action_changes(self):
        result_a = self._allowed()
        other = self._action(action_id="UEG-ACT-999")
        decision = self._decision()
        result_b = self.gate.authorize(authority=self.authority, decision=decision, action=other)
        self.assertTrue(result_b.allowed)
        self.assertNotEqual(result_a.authorization.binding_hash, result_b.authorization.binding_hash)
        self.assertFalse(any(hasattr(result_a.authorization, f) for f in ("revoked", "expires_at")))

    def test_701_missing_recovery_control_blocks_state_write(self):
        denied = self._decision(reversible=False)
        result = self.gate.authorize(authority=self.authority, decision=denied, action=self.action)
        self.assertFalse(result.allowed)
        reasons = " ".join(result.reasons)
        self.assertIn("responsibility envelope is insufficient", reasons)
        self.assertIn("rollback_or_recovery", reasons)

    def test_702_third_party_impact_requires_human_visibility(self):
        action = self._action(third_party_impact=True)
        result = self.gate.authorize(authority=self.authority, decision=self.decision, action=action)
        self.assertFalse(result.allowed)
        reasons = " ".join(result.reasons)
        self.assertIn("human_visibility", reasons)

    def test_703_delegation_requires_verified_delegation_chain(self):
        action = self._action(delegated=True)
        result = self.gate.authorize(authority=self.authority, decision=self.decision, action=action)
        self.assertFalse(result.allowed)
        reasons = " ".join(result.reasons)
        self.assertIn("delegation_chain_verified", reasons)

    def test_704_declared_capability_cannot_understate_actual_execution_power(self):
        denied = self._decision(reversible=False)
        understated = GATE.CapabilityEnvelope(
            autonomous_action=False,
            external_tools=False,
            external_state_write=False,
        )
        result = self.gate.authorize(
            authority=self.authority,
            decision=denied,
            action=self.action,
            capability=understated,
        )
        self.assertFalse(result.allowed)
        reasons = " ".join(result.reasons)
        self.assertIn("rollback_or_recovery", reasons)

    def test_705_explicit_empty_responsibility_blocks_capable_action(self):
        responsibility = GATE.ResponsibilityEnvelope(controls=frozenset())
        result = self.gate.authorize(
            authority=self.authority,
            decision=self.decision,
            action=self.action,
            responsibility=responsibility,
        )
        self.assertFalse(result.allowed)
        reasons = " ".join(result.reasons)
        self.assertIn("responsibility envelope is insufficient", reasons)
        self.assertIn("identity_verified", reasons)

    def test_603_target_and_action_type_are_bound_fields(self):
        result_a = self._allowed()
        auth = result_a.authorization
        self.assertEqual(auth.action_type, "repository_write")
        self.assertEqual(auth.target, "docs/Naya")
        swapped = self._action(action_id="UEG-ACT-SWAP", action_type="deploy", target="worker:sparkling-shape-7ae5")
        result_b = self.gate.authorize(authority=self.authority, decision=self.decision, action=swapped)
        self.assertTrue(result_b.allowed)
        self.assertNotEqual(result_a.authorization.binding_hash, result_b.authorization.binding_hash)
        # A credential for the deploy target cannot authorize the repo-write
        # target, and vice versa: the exact action_type/target are hashed into
        # the credential and recomputed at time of use (the documented
        # Test #8 residual is CLOSED).
        self.assertNotEqual(result_a.authorization.action_type, result_b.authorization.action_type)
        self.assertNotEqual(result_a.authorization.target, result_b.authorization.target)
        ok, reasons = self.gate.verify(result_a.authorization)
        self.assertTrue(ok, reasons)
        tampered_type = replace(auth, action_type="deploy")
        ok, reasons = self.gate.verify(tampered_type)
        self.assertFalse(ok)
        self.assertIn("binding_hash does not match authorization fields", reasons)
        tampered_target = replace(auth, target="worker:other")
        ok, reasons = self.gate.verify(tampered_target)
        self.assertFalse(ok)
        self.assertIn("binding_hash does not match authorization fields", reasons)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestUniversalExecutionGate)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(f"UNIVERSAL_EXECUTION_GATE_TESTS={('GREEN' if result.wasSuccessful() else 'RED')} count={result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())