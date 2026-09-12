"""Machine-checkable governance decision contract for Naya Power.

This module consumes the canonical Authority Registry as a source of authority
metadata. It does not create a competing authority hierarchy. The registry
identifies authority; this contract enforces the constitutional pre-execution
conditions required before an action can become eligible.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


ALLOWED_RISK = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
ALLOWED_CONSEQUENCE = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
ALLOWED_DECISION_STATES = {"EXECUTE", "INVESTIGATE", "VERIFY", "ASK", "DEFER", "REFUSE", "STOP"}
ACTIVE_AUTHORITY_STATUSES = {"CANONICAL", "GOVERNING", "LOCKED", "ACTIVE", "CURRENT"}


@dataclass(frozen=True)
class GovernanceDecision:
    eligible: bool
    reasons: tuple[str, ...] = ()
    checks: Mapping[str, bool] = None  # type: ignore[assignment]
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


def _scope_tokens(scope: str) -> set[str]:
    return {part.strip().casefold() for part in scope.replace(";", ",").split(",") if part.strip()}


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
    decision_state: str = "EXECUTE"


def evaluate_governance(
    action: GovernedAction,
    registry: AuthorityRegistry | None = None,
) -> GovernanceDecision:
    """Apply hard pre-execution governance gates.

    Invalid, unauthorized, unsafe, unverifiable, or unjustified actions are
    ineligible; they never compete as zero-value alternatives. The returned
    checks make the decision auditable without creating another authority layer.
    """
    reasons: list[str] = []
    checks: dict[str, bool] = {}
    resolved_scope = action.authority_scope

    checks["authority_registry_present"] = registry is not None
    if registry is not None:
        authority = registry.resolve(action.authority_id or "") if action.authority_id else None
        checks["authority_id_present"] = bool(action.authority_id)
        checks["authority_registered"] = authority is not None
        checks["authority_active"] = bool(authority and authority.get("status") in ACTIVE_AUTHORITY_STATUSES)
        resolved_scope = str(authority.get("scope", "")) if authority else None
        checks["authority_scope_registered"] = bool(resolved_scope and resolved_scope.strip())
        checks["authority_scope_matches"] = bool(
            action.authority_scope
            and resolved_scope
            and action.authority_scope.strip().casefold() in _scope_tokens(resolved_scope)
        )
        if not checks["authority_id_present"]:
            reasons.append("authority_id is required when Authority Registry is active")
        if not checks["authority_registered"]:
            reasons.append("authority_id is not registered")
        if not checks["authority_active"]:
            reasons.append("authority is not active")
        if not checks["authority_scope_registered"]:
            reasons.append("registered authority has no scope")
        if not checks["authority_scope_matches"]:
            reasons.append("requested authority scope is outside registered authority scope")
    else:
        checks["authority_id_present"] = bool(action.authority_id)
        checks["authority_registered"] = True
        checks["authority_active"] = True
        checks["authority_scope_registered"] = bool(action.authority_scope and action.authority_scope.strip())
        checks["authority_scope_matches"] = True

    checks["capability_available"] = action.capability_available
    checks["constitutional_eligible"] = action.constitutional_eligible
    checks["objective_present"] = action.objective_present
    checks["consequence_valid"] = action.consequence in ALLOWED_CONSEQUENCE
    checks["consequence_reversible"] = not (
        action.consequence in {"HIGH", "CRITICAL"} and not action.reversible
    )
    checks["risk_valid"] = action.risk in ALLOWED_RISK
    checks["risk_acceptable"] = not (
        action.risk in {"HIGH", "CRITICAL"} and not action.risk_acceptable
    )
    checks["evidence_ready"] = action.evidence_ready
    checks["verification_required"] = action.verification_required
    checks["stopping_condition_satisfied"] = action.stopping_condition_satisfied
    checks["responsible_value_eligible"] = action.responsible_value_eligible
    checks["human_decision_not_required"] = not action.requires_human_decision
    checks["decision_state_allows_execute"] = action.decision_state == "EXECUTE"

    if not checks["capability_available"]:
        reasons.append("required capability unavailable")
    if not checks["constitutional_eligible"]:
        reasons.append("constitutional eligibility failed")
    if not checks["objective_present"]:
        reasons.append("objective is missing")
    if not checks["consequence_valid"]:
        reasons.append("invalid consequence level")
    if not checks["consequence_reversible"]:
        reasons.append("high-consequence irreversible action requires escalation")
    if not checks["risk_valid"]:
        reasons.append("invalid risk level")
    if not checks["risk_acceptable"]:
        reasons.append("risk is not acceptable for execution")
    if not checks["evidence_ready"]:
        reasons.append("required evidence is not ready")
    if not checks["verification_required"]:
        reasons.append("verification requirement is missing")
    if not checks["stopping_condition_satisfied"]:
        reasons.append("stopping condition requires execution to stop")
    if not checks["responsible_value_eligible"]:
        reasons.append("responsible-value eligibility failed")
    if not checks["human_decision_not_required"]:
        reasons.append("human decision is required")
    if not checks["decision_state_allows_execute"]:
        reasons.append(f"decision state {action.decision_state!r} does not permit execution")

    return GovernanceDecision(
        eligible=not reasons,
        reasons=tuple(reasons),
        checks=checks,
        authority_id=action.authority_id,
        authority_scope=resolved_scope,
    )
