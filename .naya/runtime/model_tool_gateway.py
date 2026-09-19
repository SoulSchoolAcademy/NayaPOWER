#!/usr/bin/env python3
"""Authorize consequential actions ONLY inside a claimed execution context AND
ONLY with a gate-issued ExecutionAuthorization.

The Universal Execution Gate remains responsible for authorization. This module
does NOT mint, resolve, or interpret authority. It answers exactly one question:

    Was this exact consequential action already authorized by the
    UniversalExecutionGate.authorize(...)?

Old authority-like inputs (authorization="approved", model_authorized,
agent_authorized, claimed execution state, receipts) are never consumed as
authorization. Their presence alone always terminates in REFUSED.
"""
from __future__ import annotations

import argparse
from typing import Any, Mapping

from execution_controller import load, transition
from risk_engine import classify

REQUIRED_ACTION = (
    "action_id",
    "action_type",
    "target",
    "purpose",
    "risk",
    "protected_baseline",
    "observation_target",
    "evidence_requirement",
    "verification_requirement",
    "authority_id",
    "decision_id",
    "actor_id",
    "scope",
    "permission",
)
ALLOWED_RISK = {"L1", "L2", "L3"}

_DEFAULT_GATE = None


def _default_gate():
    global _DEFAULT_GATE
    if _DEFAULT_GATE is None:
        from universal_execution_gate import UniversalExecutionGate

        _DEFAULT_GATE = UniversalExecutionGate.from_canonical()
    return _DEFAULT_GATE


def authorize(
    action: dict[str, Any],
    *,
    execution_authorization: Any = None,
    gate: Any = None,
    identity_envelope: Mapping[str, Any] | None = None,
    now: str | None = None,
    preflight: Any = None,
) -> dict[str, Any]:
    missing = [key for key in REQUIRED_ACTION if action.get(key) in (None, "", [], {})]
    if missing:
        raise AssertionError("action request missing required fields: " + ", ".join(missing))
    declared = str(action["risk"]).upper()
    if declared not in ALLOWED_RISK:
        raise AssertionError("action risk must be L1, L2, or L3")
    derived = classify(action)
    if declared != derived:
        raise AssertionError(f"declared risk {declared} does not match derived risk {derived}")
    state = load()
    if state.get("status") != "CLAIMED":
        raise AssertionError(f"action gateway requires CLAIMED execution state, got {state.get('status')}")
    for key in ("claim_id", "block_id", "owner", "scope", "start_head"):
        if state.get(key) in (None, "", [], {}):
            raise AssertionError("execution context missing " + key)
    if action["protected_baseline"] != state["start_head"]:
        raise AssertionError("protected baseline does not match claimed execution baseline")

    # The ONLY authorization credential is a gate-issued ExecutionAuthorization.
    if identity_envelope is None:
        raise AssertionError("gateway requires the governed intelligence identity envelope for consequential execution")
    if execution_authorization is None:
        raise AssertionError("gateway requires a gate-issued ExecutionAuthorization")
    issuer = gate if gate is not None else _default_gate()
    valid, reasons = issuer.verify(
        execution_authorization,
        identity_envelope,
        consequential=True,
        now=now,
    )
    if not valid:
        raise AssertionError("execution authorization refused: " + "; ".join(reasons))

    # Bind the exact action being executed to the credential.
    if action["action_id"] != execution_authorization.action_id:
        raise AssertionError("action_id does not match execution authorization")
    if action["authority_id"] != execution_authorization.authority_id:
        raise AssertionError("authority_id does not match execution authorization")
    if action["decision_id"] != execution_authorization.decision_id:
        raise AssertionError("decision_id does not match execution authorization")
    if action["actor_id"] != execution_authorization.actor_id:
        raise AssertionError("actor_id does not match execution authorization")
    if action["scope"] != execution_authorization.scope:
        raise AssertionError("scope does not match execution authorization")
    if action["permission"] != execution_authorization.permission:
        raise AssertionError("permission does not match execution authorization")
    if execution_authorization.governance_state != "AUTHORIZED":
        raise AssertionError("execution authorization governance_state is not AUTHORIZED")

    updated = transition(
        "EXECUTING",
        action=action,
        derived_risk=derived,
        execution_authorization=execution_authorization,
        gate=issuer,
        identity_envelope=identity_envelope,
        preflight=preflight,
    )
    return {
        "status": "AUTHORIZED",
        "action_id": action["action_id"],
        "execution_status": updated["status"],
        "claim_id": updated["claim_id"],
        "block_id": updated["block_id"],
        "risk": derived,
        "authority_id": execution_authorization.authority_id,
        "decision_id": execution_authorization.decision_id,
        "validated_at": execution_authorization.validated_at,
        "binding_hash": execution_authorization.binding_hash,
        "identity_id": execution_authorization.identity_id,
        "identity_fingerprint": execution_authorization.identity_fingerprint,
        "identity_binding_hash": execution_authorization.identity_binding_hash,
        "side_effect_authorized": True,
        "side_effect_executed": False,
        "proof_required_after_action": True,
    }


def self_test() -> int:
    import json
    import tempfile
    from pathlib import Path

    import execution_controller as _controller
    from execution_controller import STATE
    from universal_execution_gate import (
        DecisionObject,
        Epistemic,
        Risk,
        UniversalExecutionGate,
        VerificationPlan,
        load_registry,
    )

    original = STATE.read_text(encoding="utf-8") if STATE.exists() else None
    sessions_tmp = Path(tempfile.mkdtemp(prefix="mtg-selftest-sessions-"))
    saved_sessions = (_controller.SESSIONS_ROOT, _controller.SESSIONS_INDEX_PATH)
    try:
        _controller.SESSIONS_ROOT = sessions_tmp / "sessions"
        _controller.SESSIONS_INDEX_PATH = _controller.SESSIONS_ROOT / "INDEX.json"
        if STATE.exists():
            STATE.unlink()
        transition(
            "CLAIMED",
            claim_id="CL-TEST",
            block_id="B-TEST",
            owner="SoulSchoolAcademy",
            scope=["docs/Naya"],
            start_head="test-head",
        )

        action = {
            "action_id": "ACT-TEST-001",
            "action_type": "repository_write",
            "target": "docs/Naya",
            "purpose": "governed maintenance and verification of NayaPOWER",
            "risk": "L2",
            "protected_baseline": "test-head",
            "observation_target": "changed file state",
            "evidence_requirement": ["commit_sha"],
            "verification_requirement": ["runtime_or_ci"],
        }

        registry = load_registry()
        authority = registry.resolve("HUMAN-SOULSCHOOLACADEMY-REPO-WRITE")
        gate = UniversalExecutionGate(registry)
        decision = DecisionObject(
            decision_id="UEG-SELFTEST-DEC",
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
        bound_action = dict(
            action,
            authority_id=authority.authority_id,
            decision_id=decision.decision_id,
            actor_id=decision.actor_id,
            scope=decision.scope,
            permission=decision.action,
        )

        # 1. No credential -> REFUSED (old claim-only path is inert).
        try:
            authorize(bound_action)
        except AssertionError as exc:
            assert "ExecutionAuthorization" in str(exc)
        else:
            raise AssertionError("gateway authorized without a gate-issued credential")

        # 2. Legitimate gate-issued credential -> AUTHORIZED.
        from execution_preflight_gate import approved_preflight

        issued = gate.authorize(
            authority=authority,
            decision=decision,
            action=bound_action,
            now="2026-01-01T00:00:00+00:00",
        )
        assert issued.allowed
        result = authorize(
            bound_action,
            execution_authorization=issued.authorization,
            gate=gate,
            preflight=approved_preflight(),
        )
        assert result["status"] == "AUTHORIZED" and result["execution_status"] == "EXECUTING"

        # 3. Risk downgrade still refused.
        invalid = dict(bound_action, risk="L1")
        try:
            authorize(invalid, execution_authorization=issued.authorization, gate=gate)
        except AssertionError as exc:
            assert "does not match derived risk" in str(exc)
        else:
            raise AssertionError("gateway trusted a caller-supplied lower risk")

        # 4. Stale baseline still refused.
        if STATE.exists():
            STATE.unlink()
        transition(
            "CLAIMED",
            claim_id="CL-TEST",
            block_id="B-TEST",
            owner="SoulSchoolAcademy",
            scope=["docs/Naya"],
            start_head="test-head",
        )
        stale = dict(bound_action, protected_baseline="stale-head")
        try:
            authorize(stale, execution_authorization=issued.authorization, gate=gate)
        except AssertionError as exc:
            assert "protected baseline" in str(exc)
        else:
            raise AssertionError("gateway accepted a stale protected baseline")

        print("PASS 4/4 model tool gateway self-tests (gateway + universal gate)")
        return 0
    finally:
        _controller.SESSIONS_ROOT, _controller.SESSIONS_INDEX_PATH = saved_sessions
        import shutil

        shutil.rmtree(str(sessions_tmp), ignore_errors=True)
        if original is None:
            if STATE.exists():
                STATE.unlink()
        else:
            STATE.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["self-test"])
    args = parser.parse_args()
    raise SystemExit(self_test())