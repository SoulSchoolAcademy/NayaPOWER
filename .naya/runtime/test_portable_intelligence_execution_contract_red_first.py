#!/usr/bin/env python3
"""RED-first execution-facing tests for portable INTELLIGENCE_COMMIT."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent
sys.path.insert(0, str(RUNTIME))
sys.path.insert(0, str(RUNTIME.parent / "governance"))

from governance_kernel import Authority, AuthorityRegistry, DecisionObject, Epistemic, Risk, VerificationPlan
from portable_authorization import (
    INTELLIGENCE_COMMIT_ACTION_TYPE,
    INTELLIGENCE_COMMIT_PERMISSION,
    INTELLIGENCE_COMMIT_TARGET,
    generate_keypair,
    issue_portable_authorization,
    portable_boundary_intelligence_commit,
)
from portable_intelligence_execution_contract import (
    receipt_evidence,
    reconstruct_receipt_evidence,
    validate_execution_envelope,
)
from universal_execution_gate import UniversalExecutionGate

NOW = "2026-01-01T00:00:00+00:00"
SHA = "d253610f8ff8f27a838294a04c8893bf71bf7d4e"
REPO = "SoulSchoolAcademy/NayaPOWER"


def fixture():
    authority = Authority(
        authority_id="execution-facing-authority",
        principal_id="execution-facing-actor",
        purpose="execution-facing portable intelligence boundary",
        scope="NayaNET",
        granted_actions=frozenset({INTELLIGENCE_COMMIT_PERMISSION}),
        expires_at="2030-01-01T00:00:00+00:00",
        revoked=False,
    )
    registry = AuthorityRegistry(authorities={authority.authority_id: authority})
    decision = DecisionObject(
        decision_id="execution-facing-decision",
        mission="execution-facing portable intelligence boundary",
        actor_id=authority.principal_id,
        action=INTELLIGENCE_COMMIT_PERMISSION,
        purpose=authority.purpose,
        scope=authority.scope,
        current_truth="bounded",
        gap="portable authorization must be mandatory at execution",
        evidence=("test",),
        epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
        consequence="persist one record",
        reversible=True,
        risk=Risk(uncertainty=1, consequence=2, irreversibility=1),
        alternatives=("do_not_execute",),
        expected_value="reconstructable",
        required_permission=INTELLIGENCE_COMMIT_PERMISSION,
        verification=VerificationPlan(observation="receipt", success_criteria="lineage"),
        necessary_power=frozenset({INTELLIGENCE_COMMIT_PERMISSION}),
        requested_power=frozenset({INTELLIGENCE_COMMIT_PERMISSION}),
    )
    action = {
        "action_id": "execution-facing-action",
        "action_type": INTELLIGENCE_COMMIT_ACTION_TYPE,
        "target": INTELLIGENCE_COMMIT_TARGET,
        "purpose": authority.purpose,
        "scope": authority.scope,
        "actor_id": authority.principal_id,
        "permission": INTELLIGENCE_COMMIT_PERMISSION,
        "decision_id": decision.decision_id,
        "authority_id": authority.authority_id,
    }
    gate = UniversalExecutionGate(registry=registry)
    issued = gate.authorize(authority=authority, decision=decision, action=action, now=NOW)
    assert issued.allowed and issued.authorization, issued.reasons
    private, public = generate_keypair()
    artifact = issue_portable_authorization(
        execution_authorization=issued.authorization,
        registry=registry,
        gate=gate,
        commit_sha=SHA,
        private_key_hex=private,
        repository=REPO,
        now=NOW,
        expires_in_seconds=60,
    )
    return authority, registry, gate, issued.authorization, artifact, public


def envelope(artifact, ordinary):
    from portable_authorization import portable_authorization_artifact_hash

    return {
        "action": "intelligence_commit",
        "execution_authorization": copy.deepcopy(ordinary),
        "portable_authorization": copy.deepcopy(artifact),
        "portable_authorization_artifact_hash": portable_authorization_artifact_hash(artifact),
    }


def check(label, artifact, public, registry, ordinary, expected=True, now=NOW, sha=SHA):
    env = envelope(artifact, ordinary)
    verified = portable_boundary_intelligence_commit(
        artifact=artifact,
        public_key_hex=public,
        registry=registry,
        commit_sha=sha,
        repository=REPO,
        now=now,
    )
    if not verified.allowed:
        allowed = False
        code = "PORTABLE_VERIFY_REJECTED"
    else:
        result = validate_execution_envelope(
            envelope=env,
            expected_actor_id=ordinary["actor_id"],
            expected_commit_sha=sha,
            expected_repository=REPO,
        )
        allowed = result["allowed"]
        code = result["code"]
    if allowed != expected:
        raise AssertionError((label, allowed, code))
    return code


authority, registry, gate, ordinary, artifact, public = fixture()

# 18 adversarial cases hit the composed execution-facing boundary.
cases = [
    ("missing artifact", None, public, registry, True, NOW, SHA),
    ("malformed artifact", {"schema": "broken"}, public, registry, True, NOW, SHA),
]

for label, bad, key, reg, _, when, sha in cases:
    if bad is None:
        ordinary_dict = {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}
        env = envelope(artifact, ordinary_dict)
        env.pop("portable_authorization")
        result = validate_execution_envelope(
            envelope=env, expected_actor_id=ordinary_dict["actor_id"],
            expected_commit_sha=sha, expected_repository=REPO,
        )
        assert result["allowed"] is False, (label, result)
    else:
        ordinary_dict = {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}
        check(label, bad, key, reg, ordinary_dict, False, when, sha)

mutations = [
    ("tampered field", lambda x: x["authorization"].__setitem__("target", "evil")),
    ("tampered signature", lambda x: x.__setitem__("signature", "00" * 64)),
    ("wrong authority", lambda x: x["authorization"].__setitem__("authority_id", "wrong")),
    ("wrong actor", lambda x: x["authorization"].__setitem__("actor_id", "wrong")),
    ("wrong decision", lambda x: x["authorization"].__setitem__("decision_id", "wrong")),
    ("wrong action", lambda x: x["authorization"].__setitem__("action_id", "wrong")),
    ("wrong target", lambda x: x["authorization"].__setitem__("target", "evil")),
    ("wrong permission", lambda x: x["authorization"].__setitem__("permission", "repo_write")),
    ("mismatched binding hash", lambda x: x["authorization"].__setitem__("binding_hash", "0" * 64)),
]
for label, mutate in mutations:
    bad = copy.deepcopy(artifact)
    mutate(bad)
    check(label, bad, public, registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, False)

check("wrong issuer key", artifact, generate_keypair()[1], registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, False)
unsigned = copy.deepcopy(artifact)
unsigned.pop("signature")
check("unsigned", unsigned, public, registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, False)
check("wrong source sha", artifact, public, registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, False, sha="0" * 40)
check("expired", artifact, public, registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, False, now="2026-01-01T00:01:01+00:00")

revoked = Authority(
    authority_id=authority.authority_id,
    principal_id=authority.principal_id,
    purpose=authority.purpose,
    scope=authority.scope,
    granted_actions=authority.granted_actions,
    expires_at=authority.expires_at,
    revoked=True,
)
revoked_registry = AuthorityRegistry(authorities={authority.authority_id: revoked})
check("revoked", artifact, public, revoked_registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, False, now="2026-01-01T00:00:30+00:00")
check("replay after expiry", artifact, public, registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, False, now="2026-01-01T00:02:00+00:00")

identical_unsigned = copy.deepcopy(artifact)
identical_unsigned.pop("signature")
check("identical unsigned credential", identical_unsigned, public, registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, False)

# Legitimate request must pass, then its exact artifact must survive receipt persistence.
check("legitimate credential", artifact, public, registry, {k: getattr(ordinary, k) for k in ("authority_id","decision_id","action_id","action_type","target","actor_id","scope","permission","governance_state","binding_hash")}, True)
from portable_authorization import portable_authorization_artifact_hash
artifact_hash = portable_authorization_artifact_hash(artifact)
receipt = {
    "id": "simulated-receipt",
    "action": "intelligence.capture",
    "status": "SUCCESS",
    "evidence": receipt_evidence(
        existing_evidence={"event_id": "intelligence:execution-facing"},
        artifact=artifact,
        artifact_hash=artifact_hash,
    ),
}
reconstructed = reconstruct_receipt_evidence(receipt)
assert reconstructed["allowed"] is True
assert reconstructed["artifact_hash"] == artifact_hash
assert reconstructed["artifact"] == artifact

print("EXECUTION_FACING_PORTABLE_INTELLIGENCE_RED_FIRST=PASS")
print("18 attacks: FAIL-CLOSED")
print("legitimate credential: PASS")
print("artifact hash: PASS")
print("simulated receipt reconstruction: PASS")
