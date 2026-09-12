#!/usr/bin/env python3
"""Canonical adapter for routing repository workflow mutations through NayaPOWER."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import argparse
import json

from governance_kernel import GovernanceKernel, GovernanceViolation


def authorize_workflow(*, actor: str, purpose: str, permission: str, request: str,
                       mission: str, uncertainty: int, consequence: int,
                       irreversibility: int, scope: dict, evidence: list[str]) -> dict:
    """Construct canonical decision/authority objects and pass the kernel gate."""
    if not actor.strip() or not purpose.strip() or not permission.strip() or not request.strip():
        raise GovernanceViolation("workflow gate identity, purpose, permission, and request are required")
    now = datetime.now(timezone.utc)
    authority = {
        "authority_id": f"workflow:{actor}:{request}",
        "issuer": f"human:{actor}",
        "holder": actor,
        "actor": actor,
        "purpose": purpose,
        "permissions": [permission],
        "scope": scope,
        "conditions": ["explicit_workflow_dispatch", "canonical_kernel_gate"],
        "issued_at": now.isoformat(),
        "expires_at": (now + timedelta(hours=1)).isoformat(),
        "revoked_at": None,
        "delegable": False,
        "delegation_scope": None,
        "evidence": evidence,
        "status": "ACTIVE",
    }
    decision = {
        "decision_id": f"workflow-decision:{actor}:{request}",
        "mission": mission,
        "actor": actor,
        "request": request,
        "purpose": purpose,
        "authority": authority,
        "scope": scope,
        "boundaries": ["workflow_scope_only", "no_implicit_delegation"],
        "evidence": evidence,
        "uncertainty": uncertainty,
        "consequence": consequence,
        "reversibility": 6 - irreversibility,
        "risk": {"irreversibility": irreversibility, "prohibited": False},
        "alternatives": ["do_not_execute"],
        "value": "authorized_repository_mutation",
        "required_permission": permission,
        "decision": "EXECUTE",
        "execution_plan": [request],
        "verification_plan": ["workflow verification", "git diff --check", "post-action repository state"],
        "stop_conditions": ["kernel denial", "scope mismatch", "verification failure", "explicit stop"],
        "receipt_requirements": ["decision", "authority", "result", "verification"],
        "learning_output": "workflow governance result",
    }
    risk = GovernanceKernel().gate(decision, authority)
    return {
        "status": "AUTHORIZED",
        "kernel": "NAYAPOWER-GOVERNANCE-KERNEL-V1",
        "risk_tier": risk.tier,
        "risk_score": risk.score,
        "actor": actor,
        "request": request,
        "authority_id": authority["authority_id"],
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
            scope=json.loads(args.scope),
            evidence=args.evidence,
        )
    except (GovernanceViolation, json.JSONDecodeError) as exc:
        print(f"GOVERNANCE_GATE=DENIED: {exc}")
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
