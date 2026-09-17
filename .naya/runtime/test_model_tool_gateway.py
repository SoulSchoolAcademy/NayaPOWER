#!/usr/bin/env python3
"""Executable gateway boundary tests (Test #9 contract).

A gate-issued ExecutionAuthorization is now required. Claim/risk/baseline checks
remain. No credential, forged credential, and tampered credentials are refused.
"""
from __future__ import annotations

import dataclasses
import json
import tempfile
from pathlib import Path

import execution_controller as _EC
from execution_controller import STATE, transition
from model_tool_gateway import authorize
from execution_preflight_gate import approved_preflight
from universal_execution_gate import (
    DecisionObject,
    Epistemic,
    Risk,
    UniversalExecutionGate,
    VerificationPlan,
    load_registry,
)


def build_context():
    registry = load_registry()
    authority = registry.resolve("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")
    gate = UniversalExecutionGate(registry)
    decision = DecisionObject(
        decision_id="MTG-TEST-DEC",
        mission="NayaPOWER governed repository maintenance",
        actor_id=authority.principal_id,
        action="repo_write",
        purpose=authority.purpose,
        scope=authority.scope,
        current_truth="repository mutation requested",
        gap="mutation requires canonical governance decision",
        evidence=("evidence:registry-grant",),
        epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
        consequence="repository write under bounded governance",
        reversible=True,
        risk=Risk(uncertainty=1, consequence=2, irreversibility=1),
        alternatives=("do_not_execute",),
        expected_value="authorized bounded mutation",
        required_permission="repo_write",
        verification=VerificationPlan("post-write state", "verification passes", ("stop",)),
        necessary_power=frozenset({"repo_write"}),
        requested_power=frozenset({"repo_write"}),
    )
    return registry, authority, decision, gate


def action():
    return {
        "action_id": "ACT-MTG-TEST",
        "action_type": "repository_write",
        "target": "docs/Naya",
        "purpose": "governed maintenance and verification of NayaPOWER",
        "risk": "L2",
        "protected_baseline": "test-head",
        "observation_target": "changed file state",
        "evidence_requirement": ["commit_sha"],
        "verification_requirement": ["runtime_or_ci"],
    }


def _reset_claimed(owner_id: str) -> None:
    if STATE.exists():
        STATE.unlink()
    transition(
        "CLAIMED",
        claim_id="CL-TEST",
        block_id="B-TEST",
        owner=owner_id,
        scope=["docs/Naya"],
        start_head="test-head",
    )


def main() -> int:
    import hashlib

    registry, authority, decision, gate = build_context()
    bound = dict(
        action(),
        authority_id=authority.authority_id,
        decision_id=decision.decision_id,
        actor_id=decision.actor_id,
        scope=decision.scope,
        permission=decision.action,
    )
    issued = gate.authorize(authority=authority, decision=decision, action=bound)
    credential = issued.authorization

    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    sessions_tmp = Path(tempfile.mkdtemp(prefix="mtg-sessions-"))
    saved_sessions = (_EC.SESSIONS_ROOT, _EC.SESSIONS_INDEX_PATH)
    try:
        _EC.SESSIONS_ROOT = sessions_tmp / "sessions"
        _EC.SESSIONS_INDEX_PATH = _EC.SESSIONS_ROOT / "INDEX.json"
        _reset_claimed(authority.principal_id)

        # No credential -> REFUSED even with a full claim.
        try:
            authorize(bound)
        except AssertionError as exc:
            assert "ExecutionAuthorization" in str(exc)
        else:
            raise AssertionError("gateway authorized without a credential")

        # Valid credential -> AUTHORIZED.
        result = authorize(
            bound,
            execution_authorization=credential,
            gate=gate,
            preflight=approved_preflight(),
        )
        assert result["status"] == "AUTHORIZED"
        assert result["execution_status"] == "EXECUTING"
        assert result["authority_id"] == credential.authority_id
        assert result["decision_id"] == credential.decision_id

        # Forged credential (self-computed hash, never issued) -> REFUSED.
        never_action_id = "MTG-ACT-NEVER-ISSUED"
        forged_hash = hashlib.sha256(
            "|".join(
                [
                    credential.authority_id,
                    credential.decision_id,
                    never_action_id,
                    credential.action_type,
                    credential.target,
                    credential.actor_id,
                    credential.scope,
                    credential.permission,
                ]
            ).encode("utf-8")
        ).hexdigest()
        forged = credential.__class__(
            authority_id=credential.authority_id,
            decision_id=credential.decision_id,
            action_id=never_action_id,
            action_type=credential.action_type,
            target=credential.target,
            actor_id=credential.actor_id,
            scope=credential.scope,
            permission=credential.permission,
            governance_state=credential.governance_state,
            risk_tier=credential.risk_tier,
            validated_at=credential.validated_at,
            binding_hash=forged_hash,
        )
        _reset_claimed(authority.principal_id)
        forged_action = dict(bound, action_id=never_action_id)
        try:
            authorize(forged_action, execution_authorization=forged, gate=gate)
        except AssertionError as exc:
            assert "not issued by this gate" in str(exc)
        else:
            raise AssertionError("gateway accepted a caller-constructed credential")

        # Tampered scope -> REFUSED.
        tampered = dataclasses.replace(credential, scope="repo:attacker/other")
        _reset_claimed(authority.principal_id)
        try:
            authorize(bound, execution_authorization=tampered, gate=gate)
        except AssertionError as exc:
            assert "binding_hash" in str(exc) or "scope" in str(exc)
        else:
            raise AssertionError("gateway accepted a tampered credential")

        # Action/permission cross-binding -> REFUSED.
        mismatch = dict(bound, permission="deploy_public_runtime")
        _reset_claimed(authority.principal_id)
        try:
            authorize(mismatch, execution_authorization=credential, gate=gate)
        except AssertionError as exc:
            assert "permission does not match" in str(exc)
        else:
            raise AssertionError("gateway accepted an action permission outside the credential")

        # Risk downgrade still refused.
        invalid = dict(bound, risk="L1")
        _reset_claimed(authority.principal_id)
        try:
            authorize(invalid, execution_authorization=credential, gate=gate)
        except AssertionError as exc:
            assert "does not match derived risk" in str(exc)
        else:
            raise AssertionError("gateway trusted a caller-supplied lower risk")

        # Stale baseline still refused.
        stale = dict(bound, protected_baseline="stale-head")
        _reset_claimed(authority.principal_id)
        try:
            authorize(stale, execution_authorization=credential, gate=gate)
        except AssertionError as exc:
            assert "protected baseline" in str(exc)
        else:
            raise AssertionError("gateway accepted a stale protected baseline")

        print("PASS 7/7 model tool gateway boundary tests")
        return 0
    finally:
        _EC.SESSIONS_ROOT, _EC.SESSIONS_INDEX_PATH = saved_sessions
        import shutil

        shutil.rmtree(str(sessions_tmp), ignore_errors=True)
        if original is None:
            if STATE.exists():
                STATE.unlink()
        else:
            STATE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())