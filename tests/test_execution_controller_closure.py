#!/usr/bin/env python3
"""Execution Controller closure tests (NAYA POWER TEST #10).

The controller is the narrow state seam. EXECUTING (and everything after it) is
only reachable through the Universal Execution Gate: a gate-issued
ExecutionAuthorization bound to the exact action. Everything else REFUSED.

Safe: EXECUTION-STATE is redirected to a temp dir; the repository registry is
only READ. Temporary registries live in tempfile dirs.

Run:  python tests/test_execution_controller_closure.py
"""
from __future__ import annotations

import dataclasses
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATE_PATH = ROOT / ".naya" / "runtime" / "universal_execution_gate.py"
EC_PATH = ROOT / ".naya" / "runtime" / "execution_controller.py"

_gate_spec = importlib.util.spec_from_file_location("gblc10_universal_execution_gate", GATE_PATH)
assert _gate_spec and _gate_spec.loader
GATE = importlib.util.module_from_spec(_gate_spec)
sys.modules[GATE.__name__] = GATE
_gate_spec.loader.exec_module(GATE)

sys.path.insert(0, str(ROOT / ".naya" / "runtime"))
_ec_spec = importlib.util.spec_from_file_location("execution_controller", EC_PATH)
assert _ec_spec and _ec_spec.loader
EC = importlib.util.module_from_spec(_ec_spec)
sys.modules["execution_controller"] = EC
_ec_spec.loader.exec_module(EC)

import tempfile as _tempfile
_TMP = Path(_tempfile.mkdtemp(prefix="gblc10-"))
EC.STATE = _TMP / "EXECUTION-STATE.json"
EC.EVENTS_ROOT = _TMP / "events"
EC.INDEX_PATH = EC.EVENTS_ROOT / "INDEX.json"
EC.SESSIONS_ROOT = _TMP / "sessions"
EC.SESSIONS_INDEX_PATH = EC.SESSIONS_ROOT / "INDEX.json"

import canonical_event_store as CES  # noqa: E402
from activity_event import build_activity_event  # noqa: E402
from execution_preflight_gate import approved_preflight  # noqa: E402


def persist_activity_event(
    claim_id: str = "CL-GBLC10",
    action_id: str = "GBLC10-ACT-001",
    event_id: str = "SE-20260916-193500-gblc10-activity-gate",
    decision_id: str = "GBLC10-DEC-001",
    **overrides,
) -> str:
    overrides.setdefault("session_id", EC.load().get("session_id") if EC.STATE.exists() else None)
    event = build_activity_event(
        event_id=event_id,
        claim_id=claim_id,
        action_id=action_id,
        decision_id=decision_id,
        authority_id="HUMAN-SOULSCHOOLACADEMY-REPO-WRITE",
        actor_id="SoulSchoolAcademy",
        subject="GBLC10 activity gate",
        summary="closure test canonical Activity Feed event",
        receipt_id="RCP-GBLC10",
        next_action="continue test",
        successor="NEXT-EXECUTION-20260916-GBLC10-NEXT.md",
        evidence=["receipt:test"],
        **overrides,
    )
    result = CES.create_or_replay(event, EC.EVENTS_ROOT, EC.INDEX_PATH)
    assert result["status"] in {"CREATED", "REPLAY"}
    return event_id



def identity_for(authority):
    return {
        "schema_version": "1.0",
        "identity_id": authority.principal_id,
        "actor_class": "HUMAN",
        "who_created_or_delegated": {"creator_ref": "human-controller", "delegator_ref": None, "lineage_state": "ROOT"},
        "knowledge": [{"knowledge_id": "K-EC-CLOSURE", "claim": "Execution target is the canonical governed repository.", "source_refs": ["test:request"], "epistemic_state": "VERIFIED"}],
        "capabilities": ["repo_write"],
        "authority": {"authority_ids": [authority.authority_id]},
        "authorized_by": [{"authority_id": authority.authority_id, "authorizer_ref": "human-controller"}],
        "received_artifacts": [{"artifact_id": "ART-EC-CLOSURE", "artifact_type": "execution_request", "source_ref": "test:request", "received_at": "2026-09-19T00:00:00Z"}],
        "provenance": [{"subject_id": "ART-EC-CLOSURE", "source_ref": "test:request", "relation": "received_from"}],
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
        claim_id="CL-GBLC10",
        block_id="B-GBLC10",
        owner=owner,
        scope=["repo:SoulSchoolAcademy/NayaPOWER"],
        start_head="test-head",
    )


def write_claimed_direct():
    if EC.STATE.exists():
        EC.STATE.unlink()
    EC.STATE.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "status": "CLAIMED",
                "claim_id": "CL-DIRECT",
                "block_id": "B-DIRECT",
                "owner": "anyone",
                "scope": ["x"],
                "start_head": "head",
                "history": [],
            }
        ),
        encoding="utf-8",
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


def make_action(authority, decision_id=None, action_id="GBLC10-ACT-001", **overrides):
    values = dict(
        action_id=action_id,
        action_type="repository_write",
        target="docs/Naya",
        purpose=authority.purpose,
        authority_id=authority.authority_id,
        decision_id=decision_id or "GBLC10-DEC-001",
        actor_id=authority.principal_id,
        scope=authority.scope,
        permission="repo_write",
    )
    values.update(overrides)
    return values


def canonical_setup():
    registry = GATE.load_registry()
    authority = registry.resolve("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")
    gate = GATE.UniversalExecutionGate(registry)
    return registry, authority, gate


def registry_file_gate(payload: dict, tmpdir: Path) -> tuple:
    path = Path(tmpdir) / "authority-registry.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    gate = GATE.UniversalExecutionGate(registry_path=path)
    authority = gate._current_registry().resolve(payload["authorities"][0]["authority_id"])
    return path, gate, authority


def grant_payload(authority_id="HUMAN-T10-REVOKE", **overrides):
    authority = {
        "authority_id": authority_id,
        "principal_id": "SoulSchoolAcademy",
        "purpose": "governed maintenance and verification of NayaPOWER",
        "scope": "repo:SoulSchoolAcademy/NayaPOWER",
        "granted_actions": ["repo_write"],
        "expires_at": None,
        "revoked": False,
    }
    authority.update(overrides)
    return {"authorities": [authority]}


class TestExecutionControllerClosure(unittest.TestCase):
    def setUp(self):
        self.registry, self.authority, self.gate = canonical_setup()
        self.decision = make_decision(self.authority, "GBLC10-DEC-001")
        self.action = make_action(self.authority, self.decision.decision_id)
        self.identity = identity_for(self.authority)
        self.issued = self.gate.authorize(authority=self.authority, decision=self.decision, action=self.action, identity_envelope=self.identity, consequential=True)
        self.credential = self.issued.authorization
        self.assertIsNotNone(self.credential)

    def _refuse_transition(self, action=None, credential=None, gate=None, **extra):
        with self.assertRaises(AssertionError) as ctx:
            EC.transition(
                "EXECUTING",
                action=action if action is not None else self.action,
                execution_authorization=credential,
                gate=gate if gate is not None else self.gate,
                identity_envelope=extra.pop("identity_envelope", self.identity),
                **extra,
            )
        return str(ctx.exception)

    # 1. direct EXECUTING without credential -> REFUSED
    def test_001_direct_executing_without_credential_refused(self):
        start_claimed()
        msg = self._refuse_transition(credential=None)
        self.assertIn("requires a gate-issued", msg)

    # 2-4. model/agent approval codes are inert
    def test_002_model_approved_refused(self):
        start_claimed()
        msg = self._refuse_transition(credential=None, authorization="approved")
        self.assertIn("requires a gate-issued", msg)

    def test_003_model_authorized_refused(self):
        start_claimed()
        msg = self._refuse_transition(credential=None, model_authorized=True)
        self.assertIn("requires a gate-issued", msg)

    def test_004_agent_authorized_refused(self):
        start_claimed()
        msg = self._refuse_transition(credential=None, agent_authorized=True)
        self.assertIn("requires a gate-issued", msg)

    # 5. execution state alone -> REFUSED
    def test_005_execution_state_alone_refused(self):
        write_claimed_direct()
        msg = self._refuse_transition(credential=None, execution_status="EXECUTING", status="EXECUTING")
        self.assertIn("requires a gate-issued", msg)
        EC.STATE.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "EXECUTING",
                    "claim_id": "C",
                    "block_id": "B",
                    "owner": "x",
                    "scope": ["y"],
                    "start_head": "h",
                    "history": [],
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(AssertionError) as ctx:
            EC.validate()
        self.assertIn("no EXECUTING transition event", str(ctx.exception))

    # 6-7. claim / receipt are inert
    def test_006_claim_alone_refused(self):
        start_claimed()
        msg = self._refuse_transition(
            credential=None,
            claim={"status": "CLAIMED", "authorized": True},
            claim_id="CL-FORGED",
        )
        self.assertIn("requires a gate-issued", msg)

    def test_007_receipt_alone_refused(self):
        start_claimed()
        msg = self._refuse_transition(credential=None, receipt={"status": "verified", "authorized": True})
        self.assertIn("requires a gate-issued", msg)

    # 8. forged credential -> REFUSED
    def test_008_forged_credential_refused(self):
        start_claimed()
        never_action_id = "GBLC10-ACT-NEVER-ISSUED"
        forged_hash = hashlib.sha256(
            "|".join(
                [
                    self.credential.authority_id,
                    self.credential.decision_id,
                    never_action_id,
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
            action_id=never_action_id,
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
        action = make_action(self.authority, self.decision.decision_id, action_id=never_action_id)
        msg = self._refuse_transition(action=action, credential=forged)
        self.assertIn("was not issued by this gate", msg)

    # 9. tampered credential -> REFUSED
    def test_009_tampered_credential_refused(self):
        start_claimed()
        tampered = dataclasses.replace(self.credential, scope="repo:attacker/other")
        msg = self._refuse_transition(credential=tampered)
        self.assertIn("binding_hash does not match", msg)

    # 10-15. identity mismatches between the action and the credential
    def test_010_wrong_authority_refused(self):
        start_claimed()
        action = make_action(self.authority, None, authority_id="HUMAN-FORGED-999")
        msg = self._refuse_transition(action=action, credential=self.credential)
        self.assertIn("authority_id does not match", msg)

    def test_011_wrong_decision_refused(self):
        start_claimed()
        action = make_action(self.authority, decision_id="GBLC10-DEC-FORGED")
        msg = self._refuse_transition(action=action, credential=self.credential)
        self.assertIn("decision_id does not match", msg)

    def test_012_wrong_action_refused(self):
        start_claimed()
        action = make_action(self.authority, None, action_id="GBLC10-ACT-FORGED")
        msg = self._refuse_transition(action=action, credential=self.credential)
        self.assertIn("action_id does not match", msg)

    def test_013_wrong_actor_refused(self):
        start_claimed()
        action = make_action(self.authority, None, actor_id="someone_else")
        msg = self._refuse_transition(action=action, credential=self.credential)
        self.assertIn("actor_id does not match", msg)

    def test_014_wrong_scope_refused(self):
        start_claimed()
        action = make_action(self.authority, None, scope="repo:attacker/other")
        msg = self._refuse_transition(action=action, credential=self.credential)
        self.assertIn("scope does not match", msg)

    def test_015_wrong_permission_refused(self):
        start_claimed()
        action = make_action(self.authority, None, permission="deploy_public_runtime")
        msg = self._refuse_transition(action=action, credential=self.credential)
        self.assertIn("permission does not match", msg)

    # 16. revoked authority -> REFUSED at time of use
    def test_016_revoked_authority_refused(self):
        with tempfile.TemporaryDirectory(prefix="gblc10-revoke-") as tmp:
            path, gate, authority = registry_file_gate(grant_payload("HUMAN-T10-REVOKE"), Path(tmp))
            decision = make_decision(authority, "GBLC10-REV-DEC")
            action = make_action(authority, decision.decision_id)
            issued = gate.authorize(authority=authority, decision=decision, action=action)
            self.assertTrue(issued.allowed)

            start_claimed()
            result = EC.transition(
                "EXECUTING",
                action=action,
                execution_authorization=issued.authorization,
                gate=gate,
                preflight=approved_preflight(),
            )
            self.assertEqual(result["status"], "EXECUTING")

            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["authorities"][0]["revoked"] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            start_claimed()
            msg = self._refuse_transition(action=action, credential=issued.authorization, gate=gate)
            self.assertTrue("revoked" in msg or "no longer permits" in msg, msg)

    # 17. expired authority -> REFUSED at time of use
    def test_017_expired_authority_refused(self):
        with tempfile.TemporaryDirectory(prefix="gblc10-expire-") as tmp:
            path, gate, authority = registry_file_gate(
                grant_payload("HUMAN-T10-EXPIRE", expires_at=now_iso(-5)), Path(tmp)
            )
            decision = make_decision(authority, "GBLC10-EXP-DEC")
            action = make_action(authority, decision.decision_id)
            issued = gate.authorize(
                authority=authority,
                decision=decision,
                action=action,
                now=now_iso(-60),
            )
            self.assertTrue(issued.allowed)

            start_claimed()
            msg = self._refuse_transition(action=action, credential=issued.authorization, gate=gate)
            self.assertIn("no longer permits", msg)

    # 18. valid gate-issued credential -> EXECUTING and onward
    def test_018_valid_credential_executes(self):
        start_claimed()
        result = EC.transition(
            "EXECUTING",
            action=self.action,
            execution_authorization=self.credential,
            gate=self.gate,
            identity_envelope=self.identity,
            preflight=approved_preflight(),
        )
        self.assertEqual(result["status"], "EXECUTING")
        result = EC.transition(
            "OBSERVED",
            observation="actual runtime observation",
            execution_authorization=self.credential,
            gate=self.gate,
            identity_envelope=self.identity,
            execution_result={
                "execution_state": "COMPLETED",
                "execution_id": self.action["action_id"],
                "action": "closure test action",
                "observed_output": "actual runtime observation",
                "result": "PASS",
                "commit_sha": "test-head",
            },
        )
        self.assertEqual(result["status"], "OBSERVED")
        result = EC.transition("VERIFIED", evidence=["receipt:test"], verification={"status": "VERIFIED", "method": "test"}, next_action="continue test", successor="NEXT-EXECUTION-20260916-GBLC10-NEXT.md")
        self.assertEqual(result["status"], "VERIFIED")
        result = EC.transition("HANDED_OFF", next_action="continue test", handoff={"current_state": "VERIFIED"})
        self.assertEqual(result["status"], "HANDED_OFF")
        self.assertEqual(EC.validate()["execution_status"], "HANDED_OFF")

    # 19. previously valid credential after revocation -> REFUSED
    def test_019_prev_valid_after_revocation_refused(self):
        with tempfile.TemporaryDirectory(prefix="gblc10-prev-") as tmp:
            path, gate, authority = registry_file_gate(grant_payload("HUMAN-T10-PREV"), Path(tmp))
            decision = make_decision(authority, "GBLC10-PREV-DEC")
            action = make_action(authority, decision.decision_id)
            issued = gate.authorize(authority=authority, decision=decision, action=action)
            self.assertTrue(issued.allowed)

            start_claimed()
            result = EC.transition(
                "EXECUTING",
                action=action,
                execution_authorization=issued.authorization,
                gate=gate,
                preflight=approved_preflight(),
            )
            self.assertEqual(result["status"], "EXECUTING")

            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["authorities"][0]["revoked"] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            start_claimed()
            msg = self._refuse_transition(action=action, credential=issued.authorization, gate=gate)
            self.assertTrue("revoked" in msg or "no longer permits" in msg, msg)

    # 20. direct controller bypass (state written behind the gateway) -> REFUSED
    def test_020_direct_controller_bypass_refused(self):
        write_claimed_direct()
        msg = self._refuse_transition(credential=None)
        self.assertIn("requires a gate-issued", msg)
        write_claimed_direct()
        with self.assertRaises(AssertionError) as ctx:
            EC.transition("EXECUTING", action=self.action, update="internal", creds="issued-by-file")
        self.assertIn("requires a gate-issued", str(ctx.exception))


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestExecutionControllerClosure)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    print(f"EXECUTION_CONTROLLER_CLOSURE_TESTS={'GREEN' if result.wasSuccessful() else 'RED'} count={result.testsRun}")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())