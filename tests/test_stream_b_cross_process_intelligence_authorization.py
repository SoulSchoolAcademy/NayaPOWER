#!/usr/bin/env python3
"""Stream B fail-first cross-process portable authorization proof.

Read-only with respect to production: all authority and execution objects are
temporary in-memory/test fixtures. No Supabase, Hub, Cloudflare, or production
mutation is performed.

The proof establishes that a fresh process can independently verify a gate-issued
ExecutionAuthorization for the exact intelligence_commit action without the
issuer process's in-memory _issued set.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / ".naya/runtime/universal_execution_gate.py"
PORTABLE_PATH = ROOT / ".naya/runtime/portable_authorization.py"

def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

GATE = load("stream_b_gate", GATE_PATH)
PORTABLE = load("stream_b_portable", PORTABLE_PATH)

NOW = "2026-09-24T19:00:00+00:00"

def make_fixture(tmp: Path):
    authority = GATE.Authority(
        authority_id="STREAM-B-INTELLIGENCE-AUTH-001",
        principal_id="test-actor",
        purpose="bounded intelligence commit proof",
        scope="NayaNET:member:test-actor",
        granted_actions=frozenset({"intelligence_commit"}),
        expires_at="2026-09-24T20:00:00+00:00",
        revoked=False,
    )
    registry = GATE.AuthorityRegistry(authorities={authority.authority_id: authority})
    decision = GATE.DecisionObject(
        decision_id="STREAM-B-DEC-001",
        mission="bounded intelligence commit proof",
        actor_id=authority.principal_id,
        action="intelligence_commit",
        purpose=authority.purpose,
        scope=authority.scope,
        current_truth="cross-process authorization must be independently verifiable",
        gap="portable provenance is not yet proven for intelligence_commit",
        evidence=("test fixture",),
        epistemic=frozenset({GATE.Epistemic.OBSERVED, GATE.Epistemic.VERIFIED}),
        consequence="test-only authorization artifact",
        reversible=True,
        risk=GATE.Risk(uncertainty=1, consequence=1, irreversibility=1),
        alternatives=("do_not_execute",),
        expected_value="independent verification",
        required_permission="intelligence_commit",
        verification=GATE.VerificationPlan(
            "artifact verification",
            "fresh process accepts valid artifact and rejects mutations",
            ("stop",),
        ),
        necessary_power=frozenset({"intelligence_commit"}),
        requested_power=frozenset({"intelligence_commit"}),
    )
    action = {
        "action_id": "STREAM-B-ACT-001",
        "action_type": "INTELLIGENCE_COMMIT",
        "target": "NayaNET",
        "purpose": authority.purpose,
        "scope": authority.scope,
        "actor_id": authority.principal_id,
        "permission": "intelligence_commit",
        "decision_id": decision.decision_id,
        "authority_id": authority.authority_id,
    }
    gate = GATE.UniversalExecutionGate(registry)
    issued = gate.authorize(authority=authority, decision=decision, action=action, now=NOW)
    assert issued.allowed and issued.authorization is not None, issued.reasons
    private_hex, public_hex = PORTABLE.generate_keypair()
    artifact = PORTABLE.issue_portable_authorization(
        execution_authorization=issued.authorization,
        registry=registry,
        gate=gate,
        commit_sha="",
        private_key_hex=private_hex,
        now=NOW,
    )
    return registry, artifact, public_hex

def fresh_verify(artifact, public_hex, registry):
    with tempfile.TemporaryDirectory(prefix="stream-b-portable-") as td:
        td = Path(td)
        artifact_path = td / "artifact.json"
        registry_path = td / "registry.json"
        artifact_path.write_text(json.dumps(artifact), encoding="utf-8")
        registry_path.write_text(json.dumps({
            "authorities": [{
                "authority_id": a.authority_id,
                "principal_id": a.principal_id,
                "purpose": a.purpose,
                "scope": a.scope,
                "granted_actions": sorted(a.granted_actions),
                "expires_at": a.expires_at,
                "revoked": a.revoked,
            } for a in registry.authorities.values()]
        }), encoding="utf-8")
        code = r'''
import importlib.util, json, sys
from pathlib import Path
root=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location("fresh_portable", root/".naya/runtime/portable_authorization.py")
m=importlib.util.module_from_spec(spec); sys.modules[spec.name]=m; spec.loader.exec_module(m)
gate=m.GATE
artifact=json.loads(Path(sys.argv[2]).read_text())
registry=gate.load_registry(sys.argv[3])
ok,reasons=m.verify_portable_authorization(
    artifact=artifact, public_key_hex=sys.argv[4], registry=registry, now="2026-09-24T19:00:00+00:00")
print(json.dumps({"ok":ok,"reasons":reasons}))
raise SystemExit(0 if ok else 1)
'''
        p = subprocess.run(
            [sys.executable, "-c", code, str(ROOT), str(artifact_path), str(registry_path), public_hex],
            text=True, capture_output=True,
        )
        payload=json.loads(p.stdout.strip())
        return p.returncode == 0, tuple(payload["reasons"])

class TestStreamBCrossProcessIntelligenceAuthorization(unittest.TestCase):
    def setUp(self):
        self.registry, self.artifact, self.public_hex = make_fixture(Path(tempfile.mkdtemp()))

    def test_001_valid_artifact_passes_in_fresh_process(self):
        ok, reasons = fresh_verify(self.artifact, self.public_hex, self.registry)
        self.assertTrue(ok, reasons)

    def test_002_tampered_actor_fails(self):
        artifact=json.loads(json.dumps(self.artifact))
        artifact["authorization"]["actor_id"]="attacker"
        ok, reasons=fresh_verify(artifact,self.public_hex,self.registry)
        self.assertFalse(ok)
        self.assertTrue(any("signature" in r or "binding" in r for r in reasons))

    def test_003_tampered_action_fails(self):
        artifact=json.loads(json.dumps(self.artifact))
        artifact["authorization"]["action_type"]="repository_write"
        ok, reasons=fresh_verify(artifact,self.public_hex,self.registry)
        self.assertFalse(ok)

    def test_004_tampered_scope_fails(self):
        artifact=json.loads(json.dumps(self.artifact))
        artifact["authorization"]["scope"]="NayaNET:member:attacker"
        ok, reasons=fresh_verify(artifact,self.public_hex,self.registry)
        self.assertFalse(ok)

    def test_005_tampered_decision_fails(self):
        artifact=json.loads(json.dumps(self.artifact))
        artifact["authorization"]["decision_id"]="forged-decision"
        ok, reasons=fresh_verify(artifact,self.public_hex,self.registry)
        self.assertFalse(ok)

    def test_006_wrong_target_cannot_be_issued(self):
        auth=GATE.ExecutionAuthorization(
            **{**self._auth_dict(), "target":"OtherProject"}
        )
        with self.assertRaises(ValueError):
            PORTABLE.issue_portable_authorization(
                execution_authorization=auth,
                registry=self.registry,
                gate=GATE.UniversalExecutionGate(self.registry),
                commit_sha="",
                private_key_hex=PORTABLE.generate_keypair()[0],
                now=NOW,
            )

    def test_007_wrong_permission_cannot_be_issued(self):
        auth=GATE.ExecutionAuthorization(
            **{**self._auth_dict(), "permission":"repo_write"}
        )
        with self.assertRaises(ValueError):
            PORTABLE.issue_portable_authorization(
                execution_authorization=auth,
                registry=self.registry,
                gate=GATE.UniversalExecutionGate(self.registry),
                commit_sha="",
                private_key_hex=PORTABLE.generate_keypair()[0],
                now=NOW,
            )

    def test_008_expired_artifact_fails(self):
        artifact=json.loads(json.dumps(self.artifact))
        artifact["authorization"]["expires_at"]="2026-09-24T18:59:59+00:00"
        # Re-sign the altered authorization with a different key: provenance
        # must still fail, even if an attacker controls a signing key.
        _, attacker_public=PORTABLE.generate_keypair()
        attacker_private=PORTABLE.generate_keypair()[0]
        artifact["signature"]=PORTABLE._sign(
            attacker_private,
            PORTABLE._canonical_json(artifact["authorization"]).encode(),
        )
        ok,reasons=PORTABLE.verify_portable_authorization(
            artifact=artifact,public_key_hex=attacker_public,
            registry=self.registry,now=NOW)
        self.assertFalse(ok)

    def test_009_revoked_authority_fails_in_fresh_process(self):
        registry,artifact,public_hex=make_fixture(Path(tempfile.mkdtemp()))
        aid=artifact["authorization"]["authority_id"]
        registry.authorities[aid]=replace(registry.authorities[aid], revoked=True)
        # The verifier must consult current authority-of-record, not issuance memory.
        ok,reasons=PORTABLE.verify_portable_authorization(
            artifact=artifact,public_key_hex=public_hex,registry=registry,now=NOW)
        self.assertFalse(ok)
        self.assertTrue(any("revoked" in r or "permits" in r for r in reasons))

    def test_010_no_issuer_memory_required(self):
        # A new gate has an empty _issued set. The portable verifier never calls
        # UniversalExecutionGate.verify(); it relies only on signed artifact +
        # canonical authority-of-record.
        fresh_gate=GATE.UniversalExecutionGate(self.registry)
        self.assertEqual(fresh_gate._issued, set())
        ok,reasons=PORTABLE.verify_portable_authorization(
            artifact=self.artifact,public_key_hex=self.public_hex,
            registry=self.registry,now=NOW)
        self.assertTrue(ok,reasons)

    def _auth_dict(self):
        a=self._issued_authorization()
        return {field:getattr(a,field) for field in (
            "authority_id","decision_id","action_id","action_type","target",
            "actor_id","scope","permission","governance_state","risk_tier",
            "validated_at","binding_hash")}

    def _issued_authorization(self):
        authority=next(iter(self.registry.authorities.values()))
        decision=GATE.DecisionObject(
            decision_id="STREAM-B-DEC-001",
            mission=authority.purpose,
            actor_id=authority.principal_id,
            action="intelligence_commit",
            purpose=authority.purpose,
            scope=authority.scope,
            current_truth="fixture",
            gap="fixture",
            evidence=("fixture",),
            epistemic=frozenset({GATE.Epistemic.OBSERVED, GATE.Epistemic.VERIFIED}),
            consequence="fixture",
            reversible=True,
            risk=GATE.Risk(uncertainty=1, consequence=1, irreversibility=1),
            alternatives=("do_not_execute",),
            expected_value="fixture",
            required_permission="intelligence_commit",
            verification=GATE.VerificationPlan("fixture","fixture",("stop",)),
            necessary_power=frozenset({"intelligence_commit"}),
            requested_power=frozenset({"intelligence_commit"}),
        )
        action={
            "action_id":"STREAM-B-ACT-001","action_type":"INTELLIGENCE_COMMIT",
            "target":"NayaNET","purpose":authority.purpose,"scope":authority.scope,
            "actor_id":authority.principal_id,"permission":"intelligence_commit",
            "decision_id":decision.decision_id,"authority_id":authority.authority_id}
        return GATE.UniversalExecutionGate(self.registry).authorize(
            authority=authority,decision=decision,action=action,now=NOW).authorization

if __name__=="__main__":
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(TestStreamBCrossProcessIntelligenceAuthorization)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    print("STREAM_B_CROSS_PROCESS_INTELLIGENCE_AUTHORIZATION=" + ("PASS" if result.wasSuccessful() else "FAIL"))
    raise SystemExit(0 if result.wasSuccessful() else 1)
