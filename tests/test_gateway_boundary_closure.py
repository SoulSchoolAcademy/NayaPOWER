#!/usr/bin/env python3
"""Model Tool Gateway closure tests (NAYA POWER TEST #9).

A-R matrix. Every non-gate path must terminate in REFUSED at the model-tool
execution boundary. The ONLY authorization path is:

    canonical registry -> Authority -> DecisionObject
      -> UniversalExecutionGate.authorize -> ExecutionAuthorization
      -> model_tool_gateway.authorize

Safe: no repository state is written; EXECUTION-STATE is redirected during each
test and restored. Temporary registry files live in a tempfile directory.

Run:  python tests/test_gateway_boundary_closure.py
"""
from __future__ import annotations

import dataclasses
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
WG_PATH = ROOT / ".naya" / "control-plane" / "workflow_gate.py"
MTG_PATH = ROOT / ".naya" / "runtime" / "model_tool_gateway.py"
EC_PATH = ROOT / ".naya" / "runtime" / "execution_controller.py"

_gate_spec = importlib.util.spec_from_file_location("gblc_universal_execution_gate", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

_wg_spec = importlib.util.spec_from_file_location("gblc_workflow_gate", WG_PATH)
assert _wg_spec and _wg_spec.loader
WG = importlib.util.module_from_spec(_wg_spec)
sys.modules[WG.__name__] = WG
_wg_spec.loader.exec_module(WG)

# execution_controller must be shared (by canonical name) so model_tool_gateway
# and this suite redirect the SAME STATE file to a temp location.
sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
_ec_spec = importlib.util.spec_from_file_location("execution_controller", EC_PATH)
assert _ec_spec and _ec_spec.loader
EC = importlib.util.module_from_spec(_ec_spec)
sys.modules["execution_controller"] = EC
_ec_spec.loader.exec_module(EC)

_mtg_spec = importlib.util.spec_from_file_location("gblc_model_tool_gateway", MTG_PATH)
assert _mtg_spec and _mtg_spec.loader
MTG = importlib.util.module_from_spec(_mtg_spec)
sys.modules[MTG.__name__] = MTG
_mtg_spec.loader.exec_module(MTG)

import tempfile as _tempfile
_TMP = Path(_tempfile.mkdtemp(prefix="gblc-"))
EC.STATE = _TMP / "EXECUTION-STATE.json"
EC.SESSIONS_ROOT = _TMP / "sessions"
EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"

from execution_preflight_gate import approved_preflight  # noqa: E402



def identity_for(authority):
    return {
        "schema_version": "1.0",
        "identity_id": authority.principal_id,
        "actor_class": "HUMAN",
        "who_created_or_delegated": {"creator_ref": "human-controller", "delegator_ref": None, "lineage_state": "ROOT"},
        "knowledge": [{"knowledge_id": "K-GW-CLOSURE", "claim": "Execution target is the canonical governed repository.", "source_refs": ["test:request"], "epistemic_state": "VERIFIED"}],
        "capabilities": ["repo_write"],
        "authority": {"authority_ids": [authority.authority_id]},
        "authorized_by": [{"authority_id": authority.authority_id, "authorizer_ref": "human-controller"}],
        "received_artifacts": [{"artifact_id": "ART-GW-CLOSURE", "artifact_type": "execution_request", "source_ref": "test:request", "received_at": "2026-09-19T00:00:00Z"}],
        "provenance": [{"subject_id": "ART-GW-CLOSURE", "source_ref": "test:request", "relation": "received_from"}],
        "delegation": {"can_delegate": False, "delegation_scope": [], "chain": []},
        "actual_actions": [], "outcomes": [], "learning": [],
    }

def now_iso(offset_seconds: int = 0) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=offset_seconds)).isoformat()


def start_claimed(owner: str = "SoulSchoolAcademy"):
    if EC.STATE.exists():
        EC.STATE.unlink()
    EC.transition(
        "CLAIMED",
        claim_id="CL-GBLC",
        block_id="B-GBLC",
        owner=owner,
        scope=["docs/Naya"],
        start_head="test-head",
    )


def make_decision(authority, decision_id, gate=GATE):
    return gate.DecisionObject(
        decision_id=decision_id,
        mission="NayaPOWER governed repository maintenance",
        actor_id=authority.principal_id,
        action="repo_write",
        purpose=authority.purpose,
        scope=authority.scope,
        current_truth="repository mutation requested",
        gap="mutation requires canonical governance decision",
        evidence=("evidence:registry-grant",),
        epistemic=frozenset({gate.Epistemic.OBSERVED, gate.Epistemic.VERIFIED}),
        consequence="repository write under bounded governance",
        reversible=True,
        risk=gate.Risk(uncertainty=1, consequence=2, irreversibility=1),
        alternatives=("do_not_execute",),
        expected_value="authorized bounded mutation",
        required_permission="repo_write",
        verification=gate.VerificationPlan("post-write state", "verification passes", ("stop",)),
        necessary_power=frozenset({"repo_write"}),
        requested_power=frozenset({"repo_write"}),
    )


def make_action(authority, decision_id, action_id="UEG-ACT-001", **overrides):
    values = dict(
        action_id=action_id,
        action_type="repository_write",
        target="docs/Naya",
        purpose=authority.purpose,
        risk="L2",
        protected_baseline="test-head",
        observation_target="changed file state",
        evidence_requirement=["commit_sha"],
        verification_requirement=["runtime_or_ci"],
        authority_id=authority.authority_id,
        decision_id=decision_id,
        actor_id=authority.principal_id,
        scope=authority.scope,
        permission="repo_write",
    )
    values.update(overrides)
    return values


def canonical_setup():
    registry = GATE.load_registry()
    authority = WG.resolve_authority(
        registry,
        actor="SoulSchoolAcademy",
        purpose="governed maintenance and verification of NayaPOWER",
        permission="repo_write",
        scope="repo:SoulSchoolAcademy/NayaPOWER",
    )
    gate = GATE.UniversalExecutionGate(registry)
    return registry, authority, gate


class TestGatewayBoundaryClosure(unittest.TestCase):
    def setUp(self):
        self.registry, self.authority, self.gate = canonical_setup()
        self.decision = make_decision(self.authority, "GBLC-DEC-001")
        self.action = make_action(self.authority, self.decision.decision_id)
        self.identity = identity_for(self.authority)
        self.issued = self.gate.authorize(authority=self.authority, decision=self.decision, action=self.action, identity_envelope=self.identity, consequential=True)
        self.credential = self.issued.authorization
        start_claimed()

    # ---- A: no authority / no credential -------------------------------
    def test_001_no_authority_refused(self):
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(self.action)
        self.assertIn("ExecutionAuthorization", str(ctx.exception))

    # ---- B/C/D: model / agent approval is inert ------------------------
    def test_002_model_approval_refused(self):
        start_claimed()
        action = dict(self.action, authorization="approved")
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action)
        self.assertIn("ExecutionAuthorization", str(ctx.exception))

    def test_003_model_authorized_refused(self):
        start_claimed()
        action = dict(self.action, model_authorized=True)
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action)
        self.assertIn("ExecutionAuthorization", str(ctx.exception))

    def test_004_agent_authorized_refused(self):
        start_claimed()
        action = dict(self.action, agent_authorized=True)
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action)
        self.assertIn("ExecutionAuthorization", str(ctx.exception))

    # ---- E: execution state is inert -------------------------------------
    def test_005_execution_state_refused(self):
        start_claimed()
        action = dict(self.action, execution_status="EXECUTING", status="EXECUTING")
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action)
        self.assertIn("ExecutionAuthorization", str(ctx.exception))

    # ---- F/G: claim / receipt are inert ----------------------------------
    def test_006_claim_refused(self):
        start_claimed()
        action = dict(self.action, claim={"status": "CLAIMED", "authorized": True}, claim_id="CL-FORGED")
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action)
        self.assertIn("ExecutionAuthorization", str(ctx.exception))

    def test_007_receipt_refused(self):
        start_claimed()
        action = dict(self.action, receipt={"status": "verified", "authorized": True})
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action)
        self.assertIn("ExecutionAuthorization", str(ctx.exception))

    # ---- H: forged credential -------------------------------------------
    def test_008_forged_credential_refused(self):
        import hashlib

        start_claimed()
        never_issued_action_id = "GBLC-ACT-NEVER-ISSUED"
        forged_hash = hashlib.sha256(
            "|".join(
                [
                    self.credential.authority_id,
                    self.credential.decision_id,
                    never_issued_action_id,
                    self.credential.action_type,
                    self.credential.target,
                    self.credential.actor_id,
                    self.credential.scope,
                    self.credential.permission,
                ]
            ).encode("utf-8")
        ).hexdigest()
        forged = self.credential.__class__(
            authority_id=self.credential.authority_id,
            decision_id=self.credential.decision_id,
            action_id=never_issued_action_id,
            action_type=self.credential.action_type,
            target=self.credential.target,
            actor_id=self.credential.actor_id,
            scope=self.credential.scope,
            permission=self.credential.permission,
            governance_state=self.credential.governance_state,
            risk_tier=self.credential.risk_tier,
            validated_at=self.credential.validated_at,
            binding_hash=forged_hash,
        )
        for action in (self.action, dict(self.action, action_id=never_issued_action_id)):
            start_claimed()
            with self.assertRaises(AssertionError) as ctx:
                MTG.authorize(action, execution_authorization=forged, gate=self.gate, identity_envelope=self.identity)
            self.assertIn("not issued by this gate", str(ctx.exception))

    # ---- I: valid gate-issued credential --------------------------------
    def test_009_valid_credential_allows(self):
        start_claimed()
        result = MTG.authorize(self.action, execution_authorization=self.credential, gate=self.gate, identity_envelope=self.identity, preflight=approved_preflight())
        self.assertEqual(result["status"], "AUTHORIZED")
        self.assertEqual(result["execution_status"], "EXECUTING")
        self.assertTrue(result["side_effect_authorized"])
        self.assertEqual(result["authority_id"], self.credential.authority_id)
        self.assertEqual(result["decision_id"], self.credential.decision_id)
        self.assertEqual(result["binding_hash"], self.credential.binding_hash)

    # ---- J-O: tampered credential ---------------------------------------
    def _tamper_refused(self, **replacement):
        start_claimed()
        altered = dataclasses.replace(self.credential, **replacement)
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(self.action, execution_authorization=altered, gate=self.gate, identity_envelope=self.identity)
        self.assertIn("binding_hash does not match", str(ctx.exception))

    def test_010_authority_id_mismatch_refused(self):
        self._tamper_refused(authority_id="HUMAN-FORGED")

    def test_011_decision_id_mismatch_refused(self):
        self._tamper_refused(decision_id="GBLC-DEC-FORGED")

    def test_012_action_id_mismatch_refused(self):
        self._tamper_refused(action_id="GBLC-ACT-FORGED")

    def test_013_actor_id_mismatch_refused(self):
        self._tamper_refused(actor_id="someone_else")

    def test_014_scope_mismatch_refused(self):
        self._tamper_refused(scope="repo:attacker/other")

    def test_015_permission_mismatch_refused(self):
        self._tamper_refused(permission="deploy_public_runtime")

    def test_016_binding_hash_mismatch_refused(self):
        self._tamper_refused(binding_hash="0" * 64)

    def test_017_governance_state_not_authorized_refused(self):
        start_claimed()
        altered = dataclasses.replace(self.credential, governance_state="EXECUTING")
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(self.action, execution_authorization=altered, gate=self.gate, identity_envelope=self.identity)
        message = str(ctx.exception)
        self.assertTrue(
            any(k in message for k in ("not issued by this gate", "binding_hash", "governance_state is not AUTHORIZED")),
            message,
        )

    # ---- Cross-binding (action manifest vs credential) ------------------
    def test_018_action_permission_outside_credential_refused(self):
        start_claimed()
        action = dict(self.action, permission="deploy_public_runtime")
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action, execution_authorization=self.credential, gate=self.gate, identity_envelope=self.identity)
        self.assertIn("permission does not match", str(ctx.exception))

    def test_019_action_scope_outside_credential_refused(self):
        start_claimed()
        action = dict(self.action, scope="repo:attacker/other")
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action, execution_authorization=self.credential, gate=self.gate, identity_envelope=self.identity)
        self.assertIn("scope does not match", str(ctx.exception))

    def test_020_action_actor_outside_credential_refused(self):
        start_claimed()
        action = dict(self.action, actor_id="someone_else")
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action, execution_authorization=self.credential, gate=self.gate, identity_envelope=self.identity)
        self.assertIn("actor_id does not match", str(ctx.exception))

    # ---- P: revocation between authorization and execution --------------
    def test_021_revocation_at_time_of_use_refused(self):
        with tempfile.TemporaryDirectory(prefix="gblc-revoke-") as tmp:
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
            authority = gate._current_registry().resolve(self.authority.authority_id)
            decision = make_decision(authority, "GBLC-REV-DEC")
            action = make_action(authority, decision.decision_id, action_id="GBLC-REV-ACT")
            issued = gate.authorize(
                authority=authority,
                decision=decision,
                action=action,
                identity_envelope=identity_for(authority),
                consequential=True,
            )
            self.assertTrue(issued.allowed)

            start_claimed()
            result = MTG.authorize(
                action,
                execution_authorization=issued.authorization,
                gate=gate,
                identity_envelope=identity_for(authority),
                preflight=approved_preflight(),
            )
            self.assertEqual(result["execution_status"], "EXECUTING")

            payload["authorities"][0]["revoked"] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            start_claimed()
            with self.assertRaises(AssertionError) as ctx:
                MTG.authorize(
                    action,
                    execution_authorization=issued.authorization,
                    gate=gate,
                    identity_envelope=identity_for(authority),
                )
            self.assertIn("revoked", str(ctx.exception))

    # ---- Q: expiration at time of use -----------------------------------
    def test_022_expiration_at_time_of_use_refused(self):
        grant = GATE.Authority(
            authority_id=self.authority.authority_id,
            principal_id=self.authority.principal_id,
            purpose=self.authority.purpose,
            scope=self.authority.scope,
            granted_actions=frozenset({"repo_write"}),
            expires_at=now_iso(5),
        )
        gate = GATE.UniversalExecutionGate(GATE.AuthorityRegistry({grant.authority_id: grant}))
        decision = make_decision(grant, "GBLC-EXP-DEC")
        action = make_action(grant, decision.decision_id, action_id="GBLC-EXP-ACT")
        issued = gate.authorize(
            authority=grant,
            decision=decision,
            action=action,
            identity_envelope=identity_for(grant),
            consequential=True,
            now=now_iso(-1),
        )
        self.assertTrue(issued.allowed)

        start_claimed()
        result = MTG.authorize(
            action,
            execution_authorization=issued.authorization,
            gate=gate,
            identity_envelope=identity_for(grant),
            now=now_iso(0),
            preflight=approved_preflight(),
        )
        self.assertEqual(result["execution_status"], "EXECUTING")

        start_claimed()
        with self.assertRaises(AssertionError) as ctx:
            MTG.authorize(action, execution_authorization=issued.authorization, gate=gate, identity_envelope=identity_for(grant), now=now_iso(10))
        self.assertIn("no longer permits", str(ctx.exception))


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGatewayBoundaryClosure)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(f"GATEWAY_BOUNDARY_CLOSURE_TESTS={('GREEN' if result.wasSuccessful() else 'RED')} count={result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())