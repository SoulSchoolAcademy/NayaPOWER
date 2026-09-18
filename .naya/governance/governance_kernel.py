"""Canonical, model-agnostic NayaPOWER governance control plane.

This module is deliberately deterministic and dependency-free. It does not make
intelligence decisions for a model; it evaluates whether a proposed consequential
action has the minimum constitutional facts, valid authority, least necessary
power, and valid state transition required to proceed.

Policy is fail-closed: missing, expired, revoked, contradictory, or invalid
state-transition facts cannot silently be promoted to AUTHORIZED or VERIFIED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import json
from pathlib import Path
from typing import FrozenSet, Mapping, Optional, Tuple


class Epistemic(str, Enum):
    KNOWN = "KNOWN"
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"
    INFERRED = "INFERRED"
    ASSUMED = "ASSUMED"
    UNKNOWN = "UNKNOWN"


class GovernanceState(str, Enum):
    PROPOSED = "PROPOSED"
    INVESTIGATING = "INVESTIGATING"
    READY_FOR_DECISION = "READY_FOR_DECISION"
    AUTHORIZED = "AUTHORIZED"
    EXECUTING = "EXECUTING"
    EXECUTED = "EXECUTED"
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"
    ASK = "ASK"
    DEFERRED = "DEFERRED"
    REFUSED = "REFUSED"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    REQUIRES_REPAIR = "REQUIRES_REPAIR"


class Decision(str, Enum):
    EXECUTE = "EXECUTE"
    INVESTIGATE = "INVESTIGATE"
    VERIFY = "VERIFY"
    ASK = "ASK"
    DEFER = "DEFER"
    REFUSE = "REFUSE"
    STOP = "STOP"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class Authority:
    """Explicit authority bound to one principal, purpose, scope, and action set."""

    authority_id: str
    principal_id: str
    purpose: str
    scope: str
    granted_actions: FrozenSet[str] = field(default_factory=frozenset)
    expires_at: Optional[str] = None
    revoked: bool = False

    def permits(
        self,
        *,
        actor_id: str,
        action: str,
        scope: str,
        now: Optional[str] = None,
    ) -> bool:
        if self.revoked:
            return False
        if not self.authority_id or not self.principal_id or not self.purpose:
            return False
        if actor_id != self.principal_id or scope != self.scope:
            return False
        if action not in self.granted_actions:
            return False
        if self.expires_at:
            if not now:
                return False
            try:
                expiry = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
                current = datetime.fromisoformat(now.replace("Z", "+00:00"))
            except ValueError:
                return False
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            if current.tzinfo is None:
                current = current.replace(tzinfo=timezone.utc)
            if current >= expiry:
                return False
        return True


@dataclass(frozen=True)
class AuthorityRegistry:
    """Immutable authority registry; callers cannot invent authority by lookup."""

    authorities: Mapping[str, Authority] = field(default_factory=dict)

    def resolve(self, authority_id: str) -> Optional[Authority]:
        return self.authorities.get(authority_id)


REGISTRY_PATH = Path(__file__).with_name("authority-registry.json")


def load_authority_registry(path: Path = REGISTRY_PATH) -> AuthorityRegistry:
    """Load the canonical explicit-grant registry; never mint authority from input."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"cannot load authority registry: {exc}") from exc

    authorities: dict[str, Authority] = {}
    for raw in payload.get("authorities", []):
        try:
            authority = Authority(
                authority_id=str(raw["authority_id"]),
                principal_id=str(raw["principal_id"]),
                purpose=str(raw["purpose"]),
                scope=str(raw["scope"]),
                granted_actions=frozenset(str(item) for item in raw.get("granted_actions", [])),
                expires_at=raw.get("expires_at"),
                revoked=bool(raw.get("revoked", False)),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError(f"invalid authority registry entry: {exc}") from exc
        if authority.authority_id in authorities:
            raise RuntimeError(f"duplicate authority_id in registry: {authority.authority_id}")
        authorities[authority.authority_id] = authority
    return AuthorityRegistry(authorities=authorities)


def resolve_authority(
    registry: AuthorityRegistry,
    *,
    authority_id: str,
    actor_id: str,
    purpose: str,
    action: str,
    scope: str,
) -> Authority:
    """Resolve exactly one registry grant and verify every binding fact."""
    if not authority_id:
        raise RuntimeError("explicit authority resolution failed: authority_id is required")
    authority = registry.resolve(authority_id)
    if authority is None:
        raise RuntimeError(f"explicit authority resolution failed: unknown authority_id {authority_id}")
    if authority.principal_id != actor_id:
        raise RuntimeError("explicit authority resolution failed: actor does not match authority principal")
    if authority.purpose != purpose:
        raise RuntimeError("explicit authority resolution failed: purpose does not match authority")
    if authority.scope != scope:
        raise RuntimeError("explicit authority resolution failed: scope does not match authority")
    if action not in authority.granted_actions:
        raise RuntimeError("explicit authority resolution failed: action is not granted")
    return authority


@dataclass(frozen=True)
class Risk:
    uncertainty: int
    consequence: int
    irreversibility: int

    def __post_init__(self) -> None:
        for name, value in (
            ("uncertainty", self.uncertainty),
            ("consequence", self.consequence),
            ("irreversibility", self.irreversibility),
        ):
            if not isinstance(value, int) or not 0 <= value <= 10:
                raise ValueError(f"{name} must be an integer from 0 to 10")

    @property
    def score(self) -> int:
        return self.uncertainty * self.consequence * self.irreversibility

    @property
    def tier(self) -> str:
        if self.score >= 400:
            return "CRITICAL"
        if self.score >= 150:
            return "HIGH"
        if self.score >= 50:
            return "MODERATE"
        return "LOW"


@dataclass(frozen=True)
class VerificationPlan:
    observation: str
    success_criteria: str
    stop_conditions: Tuple[str, ...] = ()

    @property
    def complete(self) -> bool:
        return bool(self.observation.strip() and self.success_criteria.strip())


@dataclass(frozen=True)
class DecisionObject:
    decision_id: str
    mission: str
    actor_id: str
    action: str
    purpose: str
    scope: str
    current_truth: str
    gap: str
    evidence: Tuple[str, ...]
    epistemic: FrozenSet[Epistemic]
    consequence: str
    reversible: bool
    risk: Risk
    alternatives: Tuple[str, ...]
    expected_value: str
    required_permission: str
    verification: VerificationPlan
    necessary_power: FrozenSet[str] = field(default_factory=frozenset)
    requested_power: FrozenSet[str] = field(default_factory=frozenset)

    def complete_for_governance(self) -> bool:
        required = (
            self.decision_id,
            self.mission,
            self.actor_id,
            self.action,
            self.purpose,
            self.scope,
            self.current_truth,
            self.gap,
            self.consequence,
            self.expected_value,
            self.required_permission,
        )
        return all(isinstance(v, str) and v.strip() for v in required) and self.verification.complete

    def least_power_satisfied(self) -> bool:
        return self.requested_power.issubset(self.necessary_power)


@dataclass(frozen=True)
class GovernanceResult:
    allowed: bool
    decision: Decision
    state: GovernanceState
    reasons: Tuple[str, ...]
    required_actions: Tuple[str, ...]


class ResponsibilityControl(str, Enum):
    """Minimum governance controls that must accompany observable capability."""
    IDENTITY_VERIFIED = "identity_verified"
    AUTHORITY_BOUND = "authority_bound"
    TOOL_PERMISSIONS_BOUND = "tool_permissions_bound"
    PRE_ACTION_EVIDENCE = "pre_action_evidence"
    INDEPENDENT_OBSERVATION = "independent_observation"
    DURABLE_RECEIPT = "durable_receipt"
    REVOCATION_PATH = "revocation_path"
    PROVENANCE_BOUND = "provenance_bound"
    DELEGATION_CHAIN_VERIFIED = "delegation_chain_verified"
    HUMAN_VISIBILITY = "human_visibility"
    ROLLBACK_OR_RECOVERY = "rollback_or_recovery"


@dataclass(frozen=True)
class CapabilityEnvelope:
    """Observable capabilities; intelligence level is intentionally not scored."""
    autonomous_action: bool = False
    external_tools: bool = False
    external_state_write: bool = False
    persistence: bool = False
    inter_agent_coordination: bool = False
    delegation: bool = False
    third_party_impact: bool = False


@dataclass(frozen=True)
class ResponsibilityEnvelope:
    """Controls actually demonstrated for the current capability envelope."""
    controls: FrozenSet[ResponsibilityControl] = field(default_factory=frozenset)

    def satisfies(self, required: FrozenSet[ResponsibilityControl]) -> bool:
        return required.issubset(self.controls)


@dataclass(frozen=True)
class ResponsibilityGateResult:
    allowed: bool
    required_controls: FrozenSet[ResponsibilityControl]
    missing_controls: FrozenSet[ResponsibilityControl]
    reasons: Tuple[str, ...]


_CAPABILITY_RESPONSIBILITY_RULES = {
    "autonomous_action": frozenset({
        ResponsibilityControl.IDENTITY_VERIFIED,
        ResponsibilityControl.AUTHORITY_BOUND,
        ResponsibilityControl.PRE_ACTION_EVIDENCE,
        ResponsibilityControl.DURABLE_RECEIPT,
    }),
    "external_tools": frozenset({
        ResponsibilityControl.TOOL_PERMISSIONS_BOUND,
        ResponsibilityControl.AUTHORITY_BOUND,
        ResponsibilityControl.DURABLE_RECEIPT,
    }),
    "external_state_write": frozenset({
        ResponsibilityControl.PRE_ACTION_EVIDENCE,
        ResponsibilityControl.INDEPENDENT_OBSERVATION,
        ResponsibilityControl.ROLLBACK_OR_RECOVERY,
        ResponsibilityControl.DURABLE_RECEIPT,
    }),
    "persistence": frozenset({
        ResponsibilityControl.IDENTITY_VERIFIED,
        ResponsibilityControl.DURABLE_RECEIPT,
        ResponsibilityControl.REVOCATION_PATH,
    }),
    "inter_agent_coordination": frozenset({
        ResponsibilityControl.IDENTITY_VERIFIED,
        ResponsibilityControl.PROVENANCE_BOUND,
    }),
    "delegation": frozenset({
        ResponsibilityControl.AUTHORITY_BOUND,
        ResponsibilityControl.PROVENANCE_BOUND,
        ResponsibilityControl.DELEGATION_CHAIN_VERIFIED,
    }),
    "third_party_impact": frozenset({
        ResponsibilityControl.HUMAN_VISIBILITY,
        ResponsibilityControl.PRE_ACTION_EVIDENCE,
        ResponsibilityControl.INDEPENDENT_OBSERVATION,
    }),
}


def required_responsibility_controls(
    capability: CapabilityEnvelope,
) -> FrozenSet[ResponsibilityControl]:
    """Return deterministic minimum controls implied by observable capability."""
    required: set[ResponsibilityControl] = set()
    for field_name, controls in _CAPABILITY_RESPONSIBILITY_RULES.items():
        if getattr(capability, field_name):
            required.update(controls)
    return frozenset(required)


def evaluate_capability_responsibility(
    capability: CapabilityEnvelope,
    responsibility: Optional[ResponsibilityEnvelope],
) -> ResponsibilityGateResult:
    """Fail closed when a capable actor lacks its minimum responsibility controls."""
    required = required_responsibility_controls(capability)
    supplied = responsibility.controls if responsibility is not None else frozenset()
    missing = required.difference(supplied)
    if missing:
        names = tuple(sorted(control.value for control in missing))
        return ResponsibilityGateResult(
            allowed=False,
            required_controls=required,
            missing_controls=frozenset(missing),
            reasons=(
                "responsibility envelope is insufficient for the declared capability envelope",
                "missing controls: " + ", ".join(names),
                "capability does not create authority",
            ),
        )
    return ResponsibilityGateResult(
        allowed=True,
        required_controls=required,
        missing_controls=frozenset(),
        reasons=("capability envelope is covered by the supplied responsibility envelope",),
    )

_ALLOWED_TRANSITIONS = {
    GovernanceState.PROPOSED: frozenset({GovernanceState.INVESTIGATING, GovernanceState.READY_FOR_DECISION, GovernanceState.ASK, GovernanceState.DEFERRED, GovernanceState.REFUSED, GovernanceState.STOPPED}),
    GovernanceState.INVESTIGATING: frozenset({GovernanceState.READY_FOR_DECISION, GovernanceState.ASK, GovernanceState.DEFERRED, GovernanceState.REFUSED, GovernanceState.STOPPED, GovernanceState.REQUIRES_REPAIR}),
    GovernanceState.READY_FOR_DECISION: frozenset({GovernanceState.AUTHORIZED, GovernanceState.ASK, GovernanceState.DEFERRED, GovernanceState.REFUSED, GovernanceState.STOPPED}),
    GovernanceState.AUTHORIZED: frozenset({GovernanceState.EXECUTING, GovernanceState.STOPPED, GovernanceState.FAILED}),
    GovernanceState.EXECUTING: frozenset({GovernanceState.EXECUTED, GovernanceState.FAILED, GovernanceState.STOPPED, GovernanceState.REQUIRES_REPAIR}),
    GovernanceState.EXECUTED: frozenset({GovernanceState.OBSERVED, GovernanceState.FAILED, GovernanceState.REQUIRES_REPAIR}),
    GovernanceState.OBSERVED: frozenset({GovernanceState.VERIFIED, GovernanceState.FAILED, GovernanceState.REQUIRES_REPAIR}),
    GovernanceState.VERIFIED: frozenset(),
    GovernanceState.ASK: frozenset({GovernanceState.INVESTIGATING, GovernanceState.READY_FOR_DECISION, GovernanceState.STOPPED}),
    GovernanceState.DEFERRED: frozenset({GovernanceState.INVESTIGATING, GovernanceState.STOPPED}),
    GovernanceState.REFUSED: frozenset(),
    GovernanceState.STOPPED: frozenset(),
    GovernanceState.FAILED: frozenset({GovernanceState.INVESTIGATING, GovernanceState.REQUIRES_REPAIR, GovernanceState.STOPPED}),
    GovernanceState.REQUIRES_REPAIR: frozenset({GovernanceState.INVESTIGATING, GovernanceState.STOPPED}),
}


def transition(current: GovernanceState, target: GovernanceState) -> GovernanceState:
    """Return target only when it is constitutionally reachable from current."""
    if target not in _ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"invalid governance transition: {current.value} -> {target.value}")
    return target


def _has_material_unknowns(epistemic: FrozenSet[Epistemic]) -> bool:
    return Epistemic.UNKNOWN in epistemic or Epistemic.ASSUMED in epistemic


def evaluate(
    decision: DecisionObject,
    authority: Optional[Authority],
    *,
    consequential: bool = True,
    now: Optional[str] = None,
    capability: Optional[CapabilityEnvelope] = None,
    responsibility: Optional[ResponsibilityEnvelope] = None,
) -> GovernanceResult:
    """Evaluate one proposed action at the canonical governance boundary."""
    reasons: list[str] = []
    required: list[str] = []

    if capability is not None:
        responsibility_result = evaluate_capability_responsibility(capability, responsibility)
        if not responsibility_result.allowed:
            reasons.extend(responsibility_result.reasons)
            required.extend(
                f"provide responsibility control: {control.value}"
                for control in sorted(
                    responsibility_result.missing_controls,
                    key=lambda item: item.value,
                )
            )

    if not decision.complete_for_governance():
        reasons.append("decision object is incomplete")
        required.append("complete the canonical Decision Object")

    if authority is None:
        reasons.append("no authority object supplied")
        required.append("resolve explicit authority")
    elif not authority.permits(
        actor_id=decision.actor_id,
        action=decision.action,
        scope=decision.scope,
        now=now,
    ):
        reasons.append("authority does not permit this actor/action/scope")
        required.append("obtain or resolve valid active authority")

    if _has_material_unknowns(decision.epistemic):
        reasons.append("material epistemic uncertainty remains")
        required.append("resolve material uncertainty or escalate")

    if not decision.evidence:
        reasons.append("no evidence supplied")
        required.append("supply evidence appropriate to risk")

    if not decision.alternatives:
        reasons.append("no alternative path considered")
        required.append("consider a simpler/safer/cheaper alternative")

    if not decision.least_power_satisfied():
        reasons.append("requested power exceeds necessary power")
        required.append("reduce requested power to the minimum necessary")

    if consequential and not decision.verification.complete:
        reasons.append("verification plan is incomplete")
        required.append("define observation and success criteria")

    if consequential and decision.risk.tier in {"HIGH", "CRITICAL"}:
        if Epistemic.VERIFIED not in decision.epistemic:
            reasons.append("high-risk action lacks verified epistemic state")
            required.append("obtain stronger verification or escalate")

    if reasons:
        decision_state = GovernanceState.INVESTIGATING if not authority else GovernanceState.READY_FOR_DECISION
        return GovernanceResult(
            allowed=False,
            decision=Decision.INVESTIGATE,
            state=decision_state,
            reasons=tuple(reasons),
            required_actions=tuple(dict.fromkeys(required)),
        )

    return GovernanceResult(
        allowed=True,
        decision=Decision.EXECUTE,
        state=GovernanceState.AUTHORIZED,
        reasons=("all required governance gates satisfied",),
        required_actions=(),
    )


def assert_not_verified_without_observation(
    state: GovernanceState,
    *,
    observed: bool,
    verified: bool,
) -> None:
    """Enforce the constitutional separation between execution and verification."""
    if verified and not observed:
        raise AssertionError("VERIFIED requires prior OBSERVED evidence")
    if state == GovernanceState.VERIFIED and not verified:
        raise AssertionError("VERIFIED state requires verification evidence")


def receipt_requirements(result: GovernanceResult) -> Tuple[str, ...]:
    """Return the minimum receipt fields required for this governance result."""
    base = (
        "decision_id",
        "actor",
        "purpose",
        "authority",
        "scope",
        "requested_action",
        "actual_action",
        "observation",
        "verification",
        "timestamp",
        "uncertainty",
        "next_action",
    )
    if result.allowed:
        return base + ("resulting_changes",)
    return base + ("failure_or_block_reason",)
