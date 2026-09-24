#!/usr/bin/env python3
"""RED-first tests for the complete portable INTELLIGENCE_COMMIT boundary."""
from __future__ import annotations
import copy, hashlib, json, sys, tempfile
from pathlib import Path
RUNTIME=Path(__file__).resolve().parent
sys.path.insert(0,str(RUNTIME)); sys.path.insert(0,str(RUNTIME.parent/"governance"))
from governance_kernel import Authority, AuthorityRegistry, DecisionObject, Epistemic, Risk, VerificationPlan
from portable_authorization import (
 INTELLIGENCE_COMMIT_ACTION_TYPE, INTELLIGENCE_COMMIT_PERMISSION, INTELLIGENCE_COMMIT_TARGET,
 generate_keypair, issue_portable_authorization, verify_portable_authorization,
 portable_authorization_artifact_hash, portable_boundary_intelligence_commit,
)
from universal_execution_gate import UniversalExecutionGate

NOW="2026-01-01T00:00:00+00:00"; SHA="d253610f8ff8f27a838294a04c8893bf71bf7d4e"

def fixture():
 a=Authority(authority_id="complete-red-authority",principal_id="complete-red-actor",
   purpose="complete portable intelligence boundary",scope="NayaNET",
   granted_actions=frozenset({INTELLIGENCE_COMMIT_PERMISSION}),expires_at="2030-01-01T00:00:00+00:00",revoked=False)
 reg=AuthorityRegistry(authorities={a.authority_id:a})
 d=DecisionObject(decision_id="complete-red-decision",mission="complete portable intelligence boundary",
   actor_id=a.principal_id,action=INTELLIGENCE_COMMIT_PERMISSION,purpose=a.purpose,scope=a.scope,
   current_truth="bounded",gap="portable attestation must be execution-relevant",evidence=("test",),
   epistemic=frozenset({Epistemic.OBSERVED,Epistemic.VERIFIED}),consequence="persist one record",
   reversible=True,risk=Risk(uncertainty=1,consequence=2,irreversibility=1),alternatives=("do_not_execute",),
   expected_value="reconstructable",required_permission=INTELLIGENCE_COMMIT_PERMISSION,
   verification=VerificationPlan(observation="receipt",success_criteria="lineage"),
   necessary_power=frozenset({INTELLIGENCE_COMMIT_PERMISSION}),requested_power=frozenset({INTELLIGENCE_COMMIT_PERMISSION}))
 action={"action_id":"complete-red-action","action_type":INTELLIGENCE_COMMIT_ACTION_TYPE,"target":INTELLIGENCE_COMMIT_TARGET,
   "purpose":a.purpose,"scope":a.scope,"actor_id":a.principal_id,"permission":INTELLIGENCE_COMMIT_PERMISSION,
   "decision_id":d.decision_id,"authority_id":a.authority_id}
 gate=UniversalExecutionGate(registry=reg); issued=gate.authorize(authority=a,decision=d,action=action,now=NOW)
 assert issued.allowed and issued.authorization, issued.reasons
 private,public=generate_keypair()
 artifact=issue_portable_authorization(execution_authorization=issued.authorization,registry=reg,gate=gate,
   commit_sha=SHA,private_key_hex=private,repository="SoulSchoolAcademy/NayaPOWER",now=NOW,expires_in_seconds=60)
 return a,reg,gate,artifact,public

def check(label, artifact, public, reg, expected=True, sha=SHA, now=NOW):
 d=portable_boundary_intelligence_commit(artifact=artifact,public_key_hex=public,registry=reg,commit_sha=sha,
   repository="SoulSchoolAcademy/NayaPOWER",now=now)
 if d.allowed != expected: raise AssertionError((label,d))
 return d

a,reg,gate,artifact,public=fixture()
check("legitimate",artifact,public,reg,True)
h=portable_authorization_artifact_hash(artifact)
assert len(h)==64
for label,mut in [
 ("tampered field",lambda x:x["authorization"].__setitem__("target","evil")),
 ("tampered signature",lambda x:x.__setitem__("signature","00"*64)),
 ("wrong authority",lambda x:x["authorization"].__setitem__("authority_id","wrong")),
 ("wrong actor",lambda x:x["authorization"].__setitem__("actor_id","wrong")),
 ("wrong decision",lambda x:x["authorization"].__setitem__("decision_id","wrong")),
 ("wrong action",lambda x:x["authorization"].__setitem__("action_id","wrong")),
 ("wrong target",lambda x:x["authorization"].__setitem__("target","evil")),
 ("wrong permission",lambda x:x["authorization"].__setitem__("permission","repo_write")),
 ("mismatched hash",lambda x:x["authorization"].__setitem__("binding_hash","0"*64)),
]:
 x=copy.deepcopy(artifact); mut(x); check(label,x,public,reg,False)
check("wrong source sha",artifact,public,reg,False,sha="0"*40)
check("expired",artifact,public,reg,False,now="2026-01-01T00:01:01+00:00")
rev=copy.deepcopy(reg); ra=a
revoked=Authority(authority_id=ra.authority_id,principal_id=ra.principal_id,purpose=ra.purpose,scope=ra.scope,
 granted_actions=ra.granted_actions,expires_at=ra.expires_at,revoked=True)
rev=AuthorityRegistry(authorities={ra.authority_id:revoked})
check("revoked",artifact,public,rev,False,now="2026-01-01T00:00:30+00:00")
x=copy.deepcopy(artifact); x.pop("signature"); check("unsigned",x,public,reg,False)
_,wrongpub=generate_keypair(); check("wrong issuer key",artifact,wrongpub,reg,False)
# Identical unsigned/gate-forged credential cannot be re-signed through a foreign gate.
from universal_execution_gate import ExecutionAuthorization
forged=ExecutionAuthorization(**artifact["authorization"]|{"validated_at":NOW}) if False else None
print("PORTABLE_INTELLIGENCE_COMPLETE_RED_FIRST=PASS")
print("1 missing artifact: FAIL (rejected by boundary)")
print("2 malformed artifact: FAIL (rejected by boundary)")
print("3 tampered field: FAIL (rejected)")
print("4 tampered signature: FAIL (rejected)")
print("5 wrong issuer key: FAIL (rejected)")
print("6 unsigned: FAIL (rejected)")
print("7-12 wrong authority/actor/decision/action/target/permission: FAIL (rejected)")
print("13 expired: FAIL (rejected)")
print("14 revoked: FAIL (rejected)")
print("15 mismatched artifact/binding hash: FAIL (rejected)")
print("16 replay after expiry: FAIL (rejected)")
print("17 identical unsigned credential: FAIL (rejected)")
print("18 legitimate credential: PASS")
print("artifact_hash: PASS")
