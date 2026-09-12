"""Canonical, model-agnostic NayaPOWER governance control plane.

This module is deliberately deterministic and dependency-free. It does not make
intelligence decisions for a model; it evaluates whether a proposed consequential
action has the minimum constitutional facts and authority required to proceed.

The kernel is the enforcement boundary for:
  Decision -> Authority -> Epistemic state -> Risk -> Least power -> Governance state
  -> Verification -> Receipt requirements.

Policy is fail-closed: missing or contradictory governance facts cannot silently
be promoted to AUTHORIZED or VERIFIED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
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
    """Explicit authority bound to one principal and one bounded scope."""

    authority_id: str
    principal_id: str
    purpose: str
    scope: str
    granted_actions: FrozenSet[str] = field(default_factory=frozenset)
    expires_at: Optional[str] = None
    revoked: bool = False

    def permits(self, *, actor_id: str, action: str, scope: str) -> bool:
        if self.revoked:
            return False
        if not self.authority_id or not self.principal_id or not self.purpose:
            return False
        if actor_id != self.principal_id:
            return False
        if scope != self.scope:
            return False
        return action in self.granted_actions


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


@dataclass(frozen=True)
class GovernanceResult:
    allowed: bool
    decision: Decision
    state: GovernanceState
    reasons: Tuple[str, ...]
    required_actions: Tuple[str, ...]


def _has_material_unknowns(epistemic: FrozenSet[Epistemic]) -> bool:
    return Epistemic.UNKNOWN in epistemic or Epistemic.ASSUMED in epistemic


def evaluate(
    decision: DecisionObject,
    authority: Optional[Authority],
    *,
    consequential: bool = True,
) -> GovernanceResult:
    """Evaluate one proposed action at the canonical governance boundary."""
    reasons: list[str] = []
    required: list[str] = []

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
    ):
        reasons.append("authority does not permit this actor/action/scope")
        required.append("obtain or resolve valid authority")

    if _has_material_unknowns(decision.epistemic):
        reasons.append("material epistemic uncertainty remains")
        required.append("resolve material uncertainty or escalate")

    if not decision.evidence:
        reasons.append("no evidence supplied")
        required.append("supply evidence appropriate to risk")

    if not decision.alternatives:
        reasons.append("no alternative path considered")
        required.append("consider a simpler/safer/cheaper alternative")

    if consequential and not decision.verification.complete:
        reasons.append("verification plan is incomplete")
        required.append("define observation and success criteria")

    if consequential and decision.risk.tier in {"HIGH", "CRITICAL"}:
        # High consequence requires explicit verified evidence, or escalation.
        if Epistemic.VERIFIED not in decision.epistemic:
            reasons.append("high-risk action lacks verified epistemic state")
            required.append("obtain stronger verification or escalate")

    if reasons:
        # The kernel never promotes a blocked proposal to AUTHORIZED.
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
