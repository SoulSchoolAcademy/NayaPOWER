#!/usr/bin/env python3
"""Canonical adapter for routing repository workflow mutations through NayaPOWER."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import argparse
import json
from pathlib import Path
import sys

GOVERNANCE_DIR = Path(__file__).resolve().parents[1] / "governance"
sys.path.insert(0, str(GOVERNANCE_DIR))

from governance_kernel import (  # noqa: E402
    Authority,
    DecisionObject,
    Epistemic,
    Risk,
    VerificationPlan,
    evaluate,
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
) -> dict:
    """Construct canonical governance objects and pass the canonical kernel gate."""
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

    now = datetime.now(timezone.utc)
    authority = Authority(
        authority_id=f"workflow:{actor}:{request}",
        principal_id=actor,
        purpose=purpose,
        scope=scope,
        granted_actions=frozenset({permission}),
        expires_at=(now + timedelta(hours=1)).isoformat(),
    )
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
    result = evaluate(decision, authority, now=now.isoformat())
    if not result.allowed:
        raise RuntimeError("; ".join(result.reasons))

    return {
        "status": "AUTHORIZED",
        "kernel": "NAYAPOWER-GOVERNANCE-KERNEL-V1",
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
        )
    except (ValueError, RuntimeError) as exc:
        print(f"GOVERNANCE_GATE=DENIED: {exc}")
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
