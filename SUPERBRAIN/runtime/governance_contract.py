"""Machine-checkable governance decision contract for Naya Power.

This module consumes the canonical Authority Registry as a source of authority
metadata. It does not create a competing authority hierarchy. The registry
identifies authority; this contract enforces the constitutional pre-execution
conditions required before an action can become eligible.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


ALLOWED_RISK = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
ALLOWED_CONSEQUENCE = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


@dataclass(frozen=True)
class GovernanceDecision:
    eligible: bool
    reasons: tuple[str, ...] = ()
    authority_id: str | None = None
    authority_scope: str | None = None


@dataclass(frozen=True)
class AuthorityRegistry:
    """Read-only view of the canonical registry; never a second authority source."""

    protocol: str
    authorities: Mapping[str, Mapping[str, Any]]

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "AuthorityRegistry":
        protocol = str(data.get("protocol", ""))
        authorities = {
            str(item["authority_id"]): item
            for item in data.get("authorities", [])
            if item.get("authority_id")
        }
        return cls(protocol=protocol, authorities=authorities)

    @classmethod
    def from_file(cls, path: str | Path) -> "AuthorityRegistry":
        return cls.from_mapping(json.loads(Path(path).read_text(encoding="utf-8")))

    def resolve(self, authority_id: str) -> Mapping[str, Any] | None:
        return self.authorities.get(authority_id)


@dataclass(frozen=True)
class GovernedAction:
    """Pre-execution governance facts supplied by the host/runtime."""

    authority_id: str | None = None
    authority_scope: str | None = None
    capability_available: bool = True
    constitutional_eligible: bool = True
    objective_present: bool = True
    consequence: str = "LOW"
    reversible: bool = True
    risk: str = "LOW"
    risk_acceptable: bool = True
    evidence_ready: bool = True
    verification_required: bool = True
    stopping_condition_satisfied: bool = True
    responsible_value_eligible: bool = True
    requires_human_decision: bool = False


def evaluate_governance(
    action: GovernedAction,
    registry: AuthorityRegistry | None = None,
) -> GovernanceDecision:
    """Apply hard pre-execution governance gates.

    Invalid, unauthorized, unsafe, unverifiable, or unjustified actions are
    ineligible; they never compete as zero-value alternatives.
    """
    reasons: list[str] = []
    authority_scope = action.authority_scope

    if registry is not None:
        if not action.authority_id:
            reasons.append("authority_id is required when Authority Registry is active")
        else:
            authority = registry.resolve(action.authority_id)
            if authority is None:
                reasons.append("authority_id is not registered")
            else:
                authority_scope = str(authority.get("scope", ""))
                if authority.get("status") in {"REVOKED", "SUPERSEDED", "INACTIVE"}:
                    reasons.append("authority is not active")
                if not authority_scope.strip():
                    reasons.append("registered authority has no scope")

    if not action.capability_available:
        reasons.append("required capability unavailable")
    if not action.constitutional_eligible:
        reasons.append("constitutional eligibility failed")
    if not action.objective_present:
        reasons.append("objective is missing")
    if action.consequence not in ALLOWED_CONSEQUENCE:
        reasons.append("invalid consequence level")
    if action.consequence in {"HIGH", "CRITICAL"} and not action.reversible:
        reasons.append("high-consequence irreversible action requires escalation")
    if action.risk not in ALLOWED_RISK:
        reasons.append("invalid risk level")
    if action.risk in {"HIGH", "CRITICAL"} and not action.risk_acceptable:
        reasons.append("risk is not acceptable for execution")
    if not action.evidence_ready:
        reasons.append("required evidence is not ready")
    if not action.verification_required:
        reasons.append("verification requirement is missing")
    if not action.stopping_condition_satisfied:
        reasons.append("stopping condition requires execution to stop")
    if not action.responsible_value_eligible:
        reasons.append("responsible-value eligibility failed")
    if action.requires_human_decision:
        reasons.append("human decision is required")

    return GovernanceDecision(
        eligible=not reasons,
        reasons=tuple(reasons),
        authority_id=action.authority_id,
        authority_scope=authority_scope,
    )
