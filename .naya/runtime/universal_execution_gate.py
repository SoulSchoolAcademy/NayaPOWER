#!/usr/bin/env python3
"""Universal Execution Gate (isolated v1) for NayaPOWER.

This module is an EXECUTION BOUNDARY, not a source of power.

Its only job is to answer one question, fail-closed:

    May THIS exact action proceed, right now, under an Authority that
    originated from the human-controlled authority registry and a Decision
    Object that the canonical governance kernel independently authorized?

It deliberately:

  * does NOT replace the canonical governance kernel;
  * does NOT mint, expand, delegate, or modify authority;
  * does NOT accept model authorization ("authorization": "approved");
  * does NOT accept execution state (EXECUTION-STATE / CLAIMED / EXECUTING);
  * does NOT accept claims or receipts as authority;
  * does NOT trust caller-declared authorization of any kind.

It consumes the canonical objects directly. It introduces only a small
subordinate boundary object (ExecutionAction / ExecutionAuthorization); it does
NOT introduce another Authority model.

Integration status: this module is now bound to the canonical consequential
authorization path through the execution controller and model-tool gateway in
the source tree. Production deployment behavior is not claimed until observed
in the target runtime.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Optional, Tuple

_GOVERNANCE_DIR = Path(__file__).resolve().parents[1] / "governance"
_REGISTRY_PATH = _GOVERNANCE_DIR / "authority-registry.json"
_KERNEL_PATH = _GOVERNANCE_DIR / "governance_kernel.py"


def _load_canonical_kernel():
    """Load the one canonical governance kernel from its canonical path.

    Loaded by explicit path under a private module name so the control-plane
    self-test shim can never shadow it.
    """
    private_name = "naya_canonical_governance_kernel"
    cached = sys.modules.get(private_name)
    if cached is not None:
        return cached
    if not _KERNEL_PATH.is_file():
        raise RuntimeError("canonical governance kernel is missing")
    spec = importlib.util.spec_from_file_location(private_name, _KERNEL_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("canonical governance kernel cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[private_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(private_name, None)
        raise
    return module


KERNEL = _load_canonical_kernel()

# Re-export the canonical governance objects. This is not a second model.
Authority = KERNEL.Authority
AuthorityRegistry = KERNEL.AuthorityRegistry
DecisionObject = KERNEL.DecisionObject
Epistemic = KERNEL.Epistemic
GovernanceState = KERNEL.GovernanceState
Decision = KERNEL.Decision
Risk = KERNEL.Risk
VerificationPlan = KERNEL.VerificationPlan
CapabilityEnvelope = KERNEL.CapabilityEnvelope
ResponsibilityControl = KERNEL.ResponsibilityControl
ResponsibilityEnvelope = KERNEL.ResponsibilityEnvelope
evaluate = KERNEL.evaluate


def load_registry(path: str | Path | None = None) -> AuthorityRegistry:
    """Load grants from the human-controlled registry; never mint authority."""
    registry_path = Path(path) if path is not None else _REGISTRY_PATH
    try:
        payload = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot load authority registry: {exc}") from exc

    authorities: dict[str, Any] = {}
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


def capability_for_execution(action: "ExecutionAction") -> CapabilityEnvelope:
    """Derive the minimum observable capability envelope for this execution boundary."""
    action_type = action.action_type.lower()
    permission = action.permission.lower()
    external_write = (
        "write" in action_type
        or "deploy" in action_type
        or "mutation" in action_type
        or permission in {"repo_write", "deploy_public_runtime"}
    )
    return CapabilityEnvelope(
        autonomous_action=True,
        external_tools=True,
        external_state_write=external_write,
        persistence=action.persistence,
        inter_agent_coordination=action.inter_agent_coordination,
        delegation=action.delegated,
        third_party_impact=action.third_party_impact,
    )


def combine_capability_envelopes(
    actual: CapabilityEnvelope,
    declared: Optional[CapabilityEnvelope],
) -> CapabilityEnvelope:
    """Never allow a caller to under-declare executable capability."""
    if declared is None:
        return actual
    fields = (
        "autonomous_action",
        "external_tools",
        "external_state_write",
        "persistence",
        "inter_agent_coordination",
        "delegation",
        "third_party_impact",
    )
    return CapabilityEnvelope(**{
        name: bool(getattr(actual, name) or getattr(declared, name))
        for name in fields
    })


def responsibility_from_verified_facts(
    *,
    action: "ExecutionAction",
    decision: DecisionObject,
    authority_validated: bool,
    authority_bound: bool,
    tool_permissions_bound: bool,
    provenance_bound: bool,
) -> ResponsibilityEnvelope:
    """Build controls from facts already established by the gate's own checks."""
    controls: set[ResponsibilityControl] = set()
    if authority_validated:
        controls.add(ResponsibilityControl.IDENTITY_VERIFIED)
        controls.add(ResponsibilityControl.REVOCATION_PATH)
    if authority_bound:
        controls.add(ResponsibilityControl.AUTHORITY_BOUND)
    if tool_permissions_bound:
        controls.add(ResponsibilityControl.TOOL_PERMISSIONS_BOUND)
    if decision.evidence:
        controls.add(ResponsibilityControl.PRE_ACTION_EVIDENCE)
    if decision.verification.complete:
        controls.add(ResponsibilityControl.DURABLE_RECEIPT)
    if action.observation_target.strip() or decision.verification.observation.strip():
        controls.add(ResponsibilityControl.INDEPENDENT_OBSERVATION)
    if decision.reversible or action.recovery_plan.strip():
        controls.add(ResponsibilityControl.ROLLBACK_OR_RECOVERY)
    if provenance_bound:
        controls.add(ResponsibilityControl.PROVENANCE_BOUND)
    if action.delegated and action.delegation_chain:
        controls.add(ResponsibilityControl.DELEGATION_CHAIN_VERIFIED)
    if action.human_visible:
        controls.add(ResponsibilityControl.HUMAN_VISIBILITY)
    return ResponsibilityEnvelope(controls=frozenset(controls))


@dataclass(frozen=True)
class ExecutionAction:
    """The exact action about to execute, bound to authority/decision identity."""

    action_id: str
    action_type: str
    target: str
    purpose: str
    scope: str
    actor_id: str
    permission: str
    decision_id: str
    authority_id: str
    observation_target: str = ""
    persistence: bool = False
    inter_agent_coordination: bool = False
    delegated: bool = False
    third_party_impact: bool = False
    human_visible: bool = False
    recovery_plan: str = ""
    delegation_chain: Tuple[str, ...] = ()

    REQUIRED = (
        "action_id",
        "action_type",
        "target",
        "purpose",
        "scope",
        "actor_id",
        "permission",
        "decision_id",
        "authority_id",
    )

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "ExecutionAction":
        missing = [key for key in cls.REQUIRED if data.get(key) in (None, "", [], {})]
        if missing:
            raise ValueError("execution action missing required fields: " + ", ".join(missing))
        return cls(
            **{key: str(data[key]) for key in cls.REQUIRED},
            observation_target=str(data.get("observation_target") or ""),
            persistence=data.get("persistence") is True or data.get("persistent") is True,
            inter_agent_coordination=data.get("inter_agent_coordination") is True,
            delegated=data.get("delegated") is True or bool(data.get("delegation_chain")),
            third_party_impact=data.get("third_party_impact") is True,
            human_visible=data.get("human_visible") is True,
            recovery_plan=str(data.get("recovery_plan") or ""),
            delegation_chain=tuple(str(item) for item in (data.get("delegation_chain") or ())),
        )


@dataclass(frozen=True)
class ExecutionAuthorization:
    """Immutable identity returned when the gate ALLOWS. Not an Authority."""

    authority_id: str
    decision_id: str
    action_id: str
    action_type: str
    target: str
    actor_id: str
    scope: str
    permission: str
    governance_state: str
    risk_tier: str
    validated_at: str
    binding_hash: str


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    reasons: Tuple[str, ...]
    authorization: Optional[ExecutionAuthorization] = None


def _binding_hash(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _execution_binding_hash(
    authority_id: str,
    decision_id: str,
    action_id: str,
    action_type: str,
    target: str,
    actor_id: str,
    scope: str,
    permission: str,
) -> str:
    """Hash of every security-relevant identity field, including the exact
    action_type and target so one consequential action can never authorize a
    different one (the documented Test #8 residual is closed here)."""
    return _binding_hash(
        authority_id,
        decision_id,
        action_id,
        action_type,
        target,
        actor_id,
        scope,
        permission,
    )


def _authorization_hash(authorization: "ExecutionAuthorization") -> str:
    return _execution_binding_hash(
        authorization.authority_id,
        authorization.decision_id,
        authorization.action_id,
        authorization.action_type,
        authorization.target,
        authorization.actor_id,
        authorization.scope,
        authorization.permission,
    )


def grant_fingerprint(authority: Authority) -> str:
    """Deterministic fingerprint of a grant's security-relevant fields.

    A caller cannot change scope, permission, expiry, or revocation without
    changing the fingerprint away from the registry grant.
    """
    payload = {
        "authority_id": authority.authority_id,
        "principal_id": authority.principal_id,
        "purpose": authority.purpose,
        "scope": authority.scope,
        "granted_actions": sorted(authority.granted_actions),
        "expires_at": authority.expires_at,
        "revoked": bool(authority.revoked),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()


class UniversalExecutionGate:
    """Fail-closed checkpoint in front of a consequential action."""

    def __init__(
        self,
        registry: Optional[AuthorityRegistry] = None,
        *,
        registry_path: str | Path | None = None,
    ) -> None:
        if registry is None and registry_path is None:
            registry_path = _REGISTRY_PATH
        self._registry = registry
        self._registry_path = Path(registry_path) if registry_path is not None else None
        # Provenance: every ExecutionAuthorization this gate issued is recorded
        # here so downstream boundaries can distinguish genuine issuance from a
        # caller-constructed dataclass with identical fields. This is an
        # in-process issuance registry, not a new authority model.
        self._issued: set[str] = set()

    @classmethod
    def from_canonical(cls) -> "UniversalExecutionGate":
        """Production mode: re-read the human registry immediately before use."""
        return cls(registry_path=_REGISTRY_PATH)

    def _current_registry(self) -> AuthorityRegistry:
        if self._registry is not None:
            return self._registry
        assert self._registry_path is not None
        return load_registry(self._registry_path)

    def authorize(
        self,
        *,
        authority: Optional[Authority],
        decision: Optional[DecisionObject],
        action: Any,
        now: Optional[str] = None,
        capability: Optional[CapabilityEnvelope] = None,
        responsibility: Optional[ResponsibilityEnvelope] = None,
    ) -> GateDecision:
        """ALLOW only when provenance, validity, and all bindings hold."""
        reasons: list[str] = []
        validated_at = now or datetime.now(timezone.utc).isoformat()

        if authority is None:
            reasons.append("no authority supplied")
        if decision is None:
            reasons.append("no decision supplied")

        normalized: Optional[ExecutionAction] = None
        if action is None:
            reasons.append("no action supplied")
        elif isinstance(action, ExecutionAction):
            normalized = action
        else:
            try:
                normalized = ExecutionAction.from_mapping(action)
            except (ValueError, TypeError) as exc:
                reasons.append(str(exc))

        # 1-3. authority identity / provenance / validity
        if authority is not None:
            authority_id = getattr(authority, "authority_id", "")
            if not isinstance(authority_id, str) or not authority_id:
                reasons.append("authority_id is missing")
            else:
                resolved = self._current_registry().resolve(authority_id)
                if resolved is None:
                    reasons.append("authority_id is not present in the canonical registry")
                elif resolved is not authority and grant_fingerprint(resolved) != grant_fingerprint(authority):
                    reasons.append(
                        "authority did not originate from the canonical registry "
                        "(provenance failure: grant fingerprint mismatch)"
                    )
                elif resolved is not None and getattr(resolved, "revoked", False):
                    reasons.append("authority is revoked")
            if getattr(authority, "revoked", False):
                reasons.append("authority is revoked")

        # 4-8. decision <-> authority binding
        if authority is not None and decision is not None:
            if getattr(decision, "actor_id", None) != getattr(authority, "principal_id", None):
                reasons.append("decision actor does not match authority principal")
            if getattr(decision, "purpose", None) != getattr(authority, "purpose", None):
                reasons.append("decision purpose does not match authority purpose")
            if getattr(decision, "scope", None) != getattr(authority, "scope", None):
                reasons.append("decision scope does not match authority scope")
            if getattr(decision, "action", None) not in getattr(authority, "granted_actions", frozenset()):
                reasons.append("decision action is not granted by authority")

        # 9. action <-> authority/decision binding
        if normalized is not None and authority is not None and decision is not None:
            if normalized.authority_id != authority.authority_id:
                reasons.append("action authority_id does not match resolved authority")
            if normalized.decision_id != decision.decision_id:
                reasons.append("action decision_id does not match decision")
            if normalized.actor_id != decision.actor_id:
                reasons.append("action actor does not match decision actor")
            if normalized.purpose != decision.purpose:
                reasons.append("action purpose does not match decision purpose")
            if normalized.scope != decision.scope:
                reasons.append("action scope does not match decision scope")
            if normalized.permission != decision.action or normalized.permission != decision.required_permission:
                reasons.append("action permission does not match decision permission")

        # 10. capability -> responsibility is enforced before canonical execution authorization.
        actual_capability = capability_for_execution(normalized) if normalized is not None else None
        effective_capability = (
            combine_capability_envelopes(actual_capability, capability)
            if actual_capability is not None
            else capability
        )
        if capability is not None and not isinstance(capability, CapabilityEnvelope):
            reasons.append("invalid capability envelope")
            effective_capability = None
        if responsibility is not None and not isinstance(responsibility, ResponsibilityEnvelope):
            reasons.append("invalid responsibility envelope")
            responsibility = None

        identity_verified = False
        if authority is not None:
            resolved = self._current_registry().resolve(getattr(authority, "authority_id", ""))
            identity_verified = (
                resolved is not None
                and grant_fingerprint(resolved) == grant_fingerprint(authority)
                and not getattr(resolved, "revoked", False)
            )

        authority_bound = (
            authority is not None
            and decision is not None
            and decision.actor_id == authority.principal_id
            and decision.purpose == authority.purpose
            and decision.scope == authority.scope
            and decision.action in authority.granted_actions
        )
        tool_permissions_bound = (
            normalized is not None
            and authority_bound
            and normalized.permission == decision.action
            and normalized.permission == decision.required_permission
        )
        provenance_bound = (
            normalized is not None
            and authority is not None
            and decision is not None
            and normalized.authority_id == authority.authority_id
            and normalized.decision_id == decision.decision_id
            and normalized.actor_id == decision.actor_id
            and normalized.scope == decision.scope
            and normalized.permission == decision.action
        )
        inferred_responsibility = (
            responsibility_from_verified_facts(
                action=normalized,
                decision=decision,
                authority_validated=identity_verified,
                authority_bound=authority_bound,
                tool_permissions_bound=tool_permissions_bound,
                provenance_bound=provenance_bound,
            )
            if normalized is not None and decision is not None
            else responsibility
        )

        # 11. canonical kernel is the only authority-of-record
        kernel_result = None
        if authority is not None and decision is not None:
            kernel_result = evaluate(
                decision,
                authority,
                consequential=True,
                now=validated_at,
                capability=effective_capability,
                responsibility=inferred_responsibility,
            )
            if not kernel_result.allowed:
                reasons.extend(kernel_result.reasons)
            elif kernel_result.state != GovernanceState.AUTHORIZED or kernel_result.decision != Decision.EXECUTE:
                reasons.append(
                    "kernel result is not AUTHORIZED/EXECUTE "
                    f"(got {kernel_result.state.value}/{kernel_result.decision.value})"
                )

        reasons = list(dict.fromkeys(reasons))
        if reasons:
            return GateDecision(allowed=False, reasons=tuple(reasons))

        assert authority is not None and decision is not None and normalized is not None
        assert kernel_result is not None
        authorization = ExecutionAuthorization(
            authority_id=authority.authority_id,
            decision_id=decision.decision_id,
            action_id=normalized.action_id,
            action_type=normalized.action_type,
            target=normalized.target,
            actor_id=decision.actor_id,
            scope=decision.scope,
            permission=decision.action,
            governance_state=kernel_result.state.value,
            risk_tier=decision.risk.tier,
            validated_at=validated_at,
            binding_hash=_execution_binding_hash(
                authority.authority_id,
                decision.decision_id,
                normalized.action_id,
                normalized.action_type,
                normalized.target,
                decision.actor_id,
                decision.scope,
                decision.action,
            ),
        )
        self._issued.add(authorization.binding_hash)
        return GateDecision(allowed=True, reasons=(), authorization=authorization)

    def verify(
        self,
        authorization: Any,
        *,
        now: Optional[str] = None,
    ) -> Tuple[bool, Tuple[str, ...]]:
        """Check that an execution boundary may act on this exact authorization.

        The boundary asks: did THIS gate issue this authorization, do its
        identity fields survive integrity, and is the underlying registry grant
        still valid at time of use (revocation/expiry)?
        """
        reasons: list[str] = []
        if not isinstance(authorization, ExecutionAuthorization):
            return False, ("not a gate-issued ExecutionAuthorization",)
        validated_at = now or datetime.now(timezone.utc).isoformat()

        for field in ("authority_id", "decision_id", "action_id", "binding_hash"):
            if not getattr(authorization, field, ""):
                reasons.append(f"execution authorization missing {field}")
        if authorization.governance_state != GovernanceState.AUTHORIZED.value:
            reasons.append("governance_state is not AUTHORIZED")
        if _authorization_hash(authorization) != authorization.binding_hash:
            reasons.append("binding_hash does not match authorization fields")
        if authorization.binding_hash not in self._issued:
            reasons.append("execution authorization was not issued by this gate")

        resolved = self._current_registry().resolve(authorization.authority_id)
        if resolved is None:
            reasons.append("authority_id is not present in the canonical registry")
        else:
            if getattr(resolved, "revoked", False):
                reasons.append("authority is revoked")
            if not resolved.permits(
                actor_id=authorization.actor_id,
                action=authorization.permission,
                scope=authorization.scope,
                now=validated_at,
            ):
                reasons.append("authority no longer permits this actor/action/scope at time of use")
        return (not reasons), tuple(dict.fromkeys(reasons))


__all__ = [
    "Authority",
    "AuthorityRegistry",
    "DecisionObject",
    "Epistemic",
    "GovernanceState",
    "Decision",
    "Risk",
    "VerificationPlan",
    "evaluate",
    "load_registry",
    "ExecutionAction",
    "ExecutionAuthorization",
    "GateDecision",
    "UniversalExecutionGate",
    "CapabilityEnvelope",
    "ResponsibilityEnvelope",
    "capability_for_execution",
    "combine_capability_envelopes",
]
