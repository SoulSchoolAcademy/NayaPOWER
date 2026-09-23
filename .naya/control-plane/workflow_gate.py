#!/usr/bin/env python3
"""Canonical adapter for routing repository workflow mutations through NayaPOWER."""
from __future__ import annotations

from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import sys

GOVERNANCE_DIR = Path(__file__).resolve().parents[1] / "governance"
sys.path.insert(0, str(GOVERNANCE_DIR))

from governance_kernel import (  # noqa: E402
    Authority,
    AuthorityRegistry,
    DecisionObject,
    Epistemic,
    Risk,
    VerificationPlan,
    evaluate,
    load_authority_registry,
    resolve_authority as resolve_registered_authority,
)

REGISTRY_PATH = GOVERNANCE_DIR / "authority-registry.json"

from quality_gate import QualityGateInput, evaluate_execution  # noqa: E402


def resolve_authority(
    registry: AuthorityRegistry,
    *,
    actor: str,
    purpose: str,
    permission: str,
    scope: str,
) -> Authority:
    """Resolve one existing grant, then bind it through the canonical resolver."""
    candidates = [
        authority
        for authority in registry.authorities.values()
        if authority.principal_id == actor
        and authority.purpose == purpose
        and permission in authority.granted_actions
        and authority.scope == scope
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            "explicit authority resolution failed: expected exactly one matching active grant, "
            f"found {len(candidates)}"
        )
    authority = candidates[0]
    return resolve_registered_authority(
        registry,
        authority_id=authority.authority_id,
        actor_id=actor,
        purpose=purpose,
        action=permission,
        scope=scope,
    )


def authorize_workflow(
    *,
    actor: str,
    purpose: str,
    permission: str,
    request: str,
    mission: str,
    uncertainty: int,
    consequence: int,
    irreversibility: int,
    scope: str,
    evidence: list[str],
    intent_understood: bool,
    context_complete: bool,
    material_unknowns: list[str],
    quality_ready: bool,
    evidence_ready: bool,
) -> dict:
    """Construct the decision and pass it through the canonical kernel."""
    required = {
        "actor": actor,
        "purpose": purpose,
        "permission": permission,
        "request": request,
        "mission": mission,
        "scope": scope,
    }
    if any(not value.strip() for value in required.values()):
        raise ValueError("workflow gate identity, purpose, permission, request, mission, and scope are required")
    if not evidence:
        raise ValueError("workflow gate requires evidence")

    quality = evaluate_execution(QualityGateInput(
        intent_understood=intent_understood,
        context_complete=context_complete,
        material_unknowns=tuple(material_unknowns),
        consequence=consequence,
        quality_ready=quality_ready,
        evidence_ready=evidence_ready,
    ))
    if not quality.allowed:
        raise RuntimeError("TUNE_IN=" + quality.state + "; " + "; ".join(quality.reasons))

    registry = load_authority_registry(REGISTRY_PATH)
    authority = resolve_authority(
        registry,
        actor=actor,
        purpose=purpose,
        permission=permission,
        scope=scope,
    )
    now = datetime.now(timezone.utc).isoformat()

    decision = DecisionObject(
        decision_id=f"workflow-decision:{actor}:{request}",
        mission=mission,
        actor_id=actor,
        action=permission,
        purpose=purpose,
        scope=scope,
        current_truth="workflow dispatch is the explicit execution request",
        gap="repository mutation requires a canonical governance decision",
        evidence=tuple(evidence),
        epistemic=frozenset({Epistemic.OBSERVED, Epistemic.VERIFIED}),
        consequence=f"workflow mutation: {request}",
        reversible=irreversibility < 10,
        risk=Risk(
            uncertainty=uncertainty,
            consequence=consequence,
            irreversibility=irreversibility,
        ),
        alternatives=("do_not_execute",),
        expected_value="authorized repository mutation under bounded governance",
        required_permission=permission,
        verification=VerificationPlan(
            observation="workflow verification and post-action repository state",
            success_criteria="requested mutation completes and repository verification passes",
            stop_conditions=("kernel denial", "scope mismatch", "verification failure", "explicit stop"),
        ),
        necessary_power=frozenset({permission}),
        requested_power=frozenset({permission}),
    )
    result = evaluate(decision, authority, now=now)
    if not result.allowed:
        raise RuntimeError("; ".join(result.reasons))

    # Mandatory consequential-execution bridge: governance eligibility alone
    # never authorizes a side effect. Every workflow mutation must receive a
    # real ExecutionAuthorization from the ONE UniversalExecutionGate.
    from universal_execution_gate import UniversalExecutionGate

    gate = UniversalExecutionGate.from_canonical()
    action = {
        "action_id": f"workflow:{actor}:{request}",
        "action_type": "workflow_mutation",
        "target": f"workflow:{request}",
        "purpose": purpose,
        "scope": scope,
        "actor_id": actor,
        "permission": permission,
        "decision_id": decision.decision_id,
        "authority_id": authority.authority_id,
    }
    issued = gate.authorize(
        authority=authority,
        decision=decision,
        action=action,
        now=now,
    )
    if not issued.allowed or issued.authorization is None:
        raise RuntimeError(
            "universal execution gate denied workflow mutation: "
            + "; ".join(issued.reasons)
        )

    authorization = issued.authorization
    return {
        "status": "AUTHORIZED",
        "kernel": "NAYAPOWER-GOVERNANCE-KERNEL-V1",
        "execution_gate": "NAYAPOWER-UNIVERSAL-EXECUTION-GATE-V1",
        "execution_authorization": {
            "authority_id": authorization.authority_id,
            "decision_id": authorization.decision_id,
            "action_id": authorization.action_id,
            "action_type": authorization.action_type,
            "target": authorization.target,
            "actor_id": authorization.actor_id,
            "scope": authorization.scope,
            "permission": authorization.permission,
            "governance_state": authorization.governance_state,
            "risk_tier": authorization.risk_tier,
            "validated_at": authorization.validated_at,
            "binding_hash": authorization.binding_hash,
        },
        "risk_tier": decision.risk.tier,
        "risk_score": decision.risk.score,
        "actor": actor,
        "request": request,
        "authority_id": authority.authority_id,
        "decision_id": decision.decision_id,
        "expires_at": authority.expires_at,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--permission", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--mission", required=True)
    parser.add_argument("--uncertainty", type=int, required=True)
    parser.add_argument("--consequence", type=int, required=True)
    parser.add_argument("--irreversibility", type=int, required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--intent-understood", action="store_true")
    parser.add_argument("--context-complete", action="store_true")
    parser.add_argument("--material-unknown", action="append", default=[])
    parser.add_argument("--quality-ready", action="store_true")
    parser.add_argument("--evidence-ready", action="store_true")
    args = parser.parse_args()
    try:
        result = authorize_workflow(
            actor=args.actor,
            purpose=args.purpose,
            permission=args.permission,
            request=args.request,
            mission=args.mission,
            uncertainty=args.uncertainty,
            consequence=args.consequence,
            irreversibility=args.irreversibility,
            scope=args.scope,
            evidence=args.evidence,
            intent_understood=args.intent_understood,
            context_complete=args.context_complete,
            material_unknowns=args.material_unknown,
            quality_ready=args.quality_ready,
            evidence_ready=args.evidence_ready,
        )
    except (ValueError, RuntimeError) as exc:
        print(f"GOVERNANCE_GATE=DENIED: {exc}")
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
