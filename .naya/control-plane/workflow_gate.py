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
)

REGISTRY_PATH = GOVERNANCE_DIR / "authority-registry.json"


def load_authority_registry() -> AuthorityRegistry:
    """Load explicit authority grants; never mint authority from a request."""
    try:
        payload = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot load authority registry: {exc}") from exc

    authorities = {}
    for raw in payload.get("authorities", []):
        authority = Authority(
            authority_id=str(raw["authority_id"]),
            principal_id=str(raw["principal_id"]),
            purpose=str(raw["purpose"]),
            scope=str(raw["scope"]),
            granted_actions=frozenset(str(item) for item in raw.get("granted_actions", [])),
            expires_at=raw.get("expires_at"),
            revoked=bool(raw.get("revoked", False)),
        )
        if authority.authority_id in authorities:
            raise RuntimeError(f"duplicate authority_id in registry: {authority.authority_id}")
        authorities[authority.authority_id] = authority
    return AuthorityRegistry(authorities=authorities)


def resolve_authority(
    registry: AuthorityRegistry,
    *,
    actor: str,
    permission: str,
    scope: str,
) -> Authority:
    """Resolve a pre-existing grant; actor/request cannot create authority."""
    candidates = [
        authority
        for authority in registry.authorities.values()
        if authority.principal_id == actor
        and permission in authority.granted_actions
        and authority.scope == scope
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            "explicit authority resolution failed: expected exactly one matching active grant, "
            f"found {len(candidates)}"
        )
    return candidates[0]


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

    registry = load_authority_registry()
    authority = resolve_authority(
        registry,
        actor=actor,
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
