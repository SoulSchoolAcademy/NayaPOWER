"""Naya Power runtime kernel.

Pure-stdlib implementation of the canonical Mission State + Lead Mode contract.
This module deliberately does not execute arbitrary tools. It produces an authorized,
ranked action plan for a host agent/tool layer, records evidence, and preserves
continuity without becoming a second product/project source of truth.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence

from governance_contract import AuthorityRegistry, GovernedAction, evaluate_governance

RUNTIME_PROTOCOL = "naya-power-runtime/v1"


class EvidenceState(str, Enum):
    ASSUMED = "ASSUMED"
    INFERRED = "INFERRED"
    KNOWN = "KNOWN"
    OBSERVED = "OBSERVED"
    IMPLEMENTED = "IMPLEMENTED"
    VERIFIED = "VERIFIED"
    LIVE_VERIFIED = "LIVE_VERIFIED"
    UNKNOWN = "UNKNOWN"
    CONFLICTED = "CONFLICTED"
    SUPERSEDED = "SUPERSEDED"


class BlockStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    SUPERSEDED = "SUPERSEDED"


class Authority(str, Enum):
    HUMAN = "HUMAN"
    CONSTITUTION = "CONSTITUTION"
    SOURCE_OF_TRUTH = "SOURCE_OF_TRUTH"
    PROJECT_REQUIREMENTS = "PROJECT_REQUIREMENTS"
    SPECIALIZED_MODE = "SPECIALIZED_MODE"
    EXECUTION_LAYER = "EXECUTION_LAYER"
    OUTPUT = "OUTPUT"


@dataclass(frozen=True)
class ActionCandidate:
    """A candidate next move evaluated before execution."""

    action_id: str
    description: str
    value: int
    reversible: bool = True
    consequence: str = "LOW"
    executable: bool = True
    authorized: bool = True
    constitutional: bool = True
    evidence_ready: bool = True
    dependencies_clear: bool = True
    protected_scope_preserved: bool = True
    requires_human_decision: bool = False
    authority_id: str | None = None
    authority_scope: str | None = None
    risk: str = "LOW"
    risk_acceptable: bool = True
    verification_required: bool = True
    stopping_condition_satisfied: bool = True
    responsible_value_eligible: bool = True
    reason: str = ""

    def governance_decision(self, registry: AuthorityRegistry | None = None):
        """Evaluate the candidate against the canonical pre-execution contract."""
        return evaluate_governance(
            GovernedAction(
                authority_id=self.authority_id,
                authority_scope=self.authority_scope,
                capability_available=self.executable,
                constitutional_eligible=self.constitutional,
                objective_present=bool(self.description.strip()),
                consequence=self.consequence,
                reversible=self.reversible,
                risk=self.risk,
                risk_acceptable=self.risk_acceptable,
                evidence_ready=self.evidence_ready,
                verification_required=self.verification_required,
                stopping_condition_satisfied=self.stopping_condition_satisfied,
                responsible_value_eligible=self.responsible_value_eligible,
                requires_human_decision=self.requires_human_decision,
            ),
            registry,
        )

    def eligible(self, registry: AuthorityRegistry | None = None) -> bool:
        """Hard governance constraints remove an option; invalid is not zero value."""
        decision = self.governance_decision(registry)
        return (
            decision.eligible
            and self.dependencies_clear
            and self.protected_scope_preserved
            and self.authorized
        )


@dataclass
class Evidence:
    evidence_id: str
    claim: str
    state: EvidenceState
    observation: str
    source: str
    timestamp: str = field(default_factory=lambda: utc_now())
    commit: str | None = None
    deployment: str | None = None

    def can_support_verified(self) -> bool:
        return self.state in {EvidenceState.VERIFIED, EvidenceState.LIVE_VERIFIED}


@dataclass
class MissionState:
    """Portable state contract for one active consequential mission."""

    project: str
    mission: str
    vision: str
    desired_outcome: str
    repository: str | None = None
    branch: str | None = None
    current_head: str | None = None
    production_head: str | None = None
    deployment: str | None = None
    current_phase: str = "UNKNOWN"
    plan: list[str] = field(default_factory=list)
    completed_work: list[str] = field(default_factory=list)
    remaining_work: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    protected_scope: list[str] = field(default_factory=list)
    rejected_scope: list[str] = field(default_factory=list)
    standards: list[str] = field(default_factory=list)
    known: list[str] = field(default_factory=list)
    observed: list[str] = field(default_factory=list)
    verified: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    current_action: str | None = None
    next_action: str | None = None
    next_action_reason: str | None = None
    last_verified_state: str | None = None
    block_status: BlockStatus = BlockStatus.ACTIVE
    evidence: list[Evidence] = field(default_factory=list)
    activity: list[dict[str, Any]] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: utc_now())

    def validate(self) -> list[str]:
        """Return deterministic contract violations; do not silently repair them."""
        errors: list[str] = []
        if not self.project.strip():
            errors.append("project is required")
        if not self.mission.strip():
            errors.append("mission is required")
        if not self.desired_outcome.strip():
            errors.append("desired_outcome is required")
        if self.next_action is None and self.block_status == BlockStatus.ACTIVE:
            errors.append("ACTIVE mission requires exactly one next_action")
        if self.block_status == BlockStatus.VERIFIED and not self.verified:
            errors.append("VERIFIED block requires verified state evidence")
        if self.block_status == BlockStatus.VERIFIED and not any(
            e.can_support_verified() for e in self.evidence
        ):
            errors.append("VERIFIED block requires verification evidence")
        if self.next_action and self.next_action_reason is None:
            errors.append("next_action requires a reason")
        return errors

    def assert_valid(self) -> None:
        errors = self.validate()
        if errors:
            raise ValueError("MissionState invalid: " + "; ".join(errors))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["block_status"] = self.block_status.value
        payload["evidence"] = [
            {**asdict(item), "state": item.state.value} for item in self.evidence
        ]
        return payload

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "MissionState":
        evidence = [
            Evidence(
                evidence_id=item["evidence_id"],
                claim=item["claim"],
                state=EvidenceState(item["state"]),
                observation=item["observation"],
                source=item["source"],
                timestamp=item.get("timestamp", utc_now()),
                commit=item.get("commit"),
                deployment=item.get("deployment"),
            )
            for item in data.get("evidence", [])
        ]
        payload = dict(data)
        payload["block_status"] = BlockStatus(payload.get("block_status", "ACTIVE"))
        payload["evidence"] = evidence
        return cls(**payload)


@dataclass(frozen=True)
class ActionPlan:
    action: ActionCandidate
    protocol: str = RUNTIME_PROTOCOL
    authority: Authority = Authority.EXECUTION_LAYER
    verification_method: str = "Observe the actual post-action state and attach evidence."
    expected_result: str = ""


@dataclass(frozen=True)
class ExecutionReceipt:
    action_id: str
    result: str
    evidence_state: EvidenceState
    observed: str
    evidence_source: str
    verified: bool
    next_action: str | None
    timestamp: str = field(default_factory=lambda: utc_now())
    commit: str | None = None
    deployment: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rank_candidates(
    candidates: Iterable[ActionCandidate],
    registry: AuthorityRegistry | None = None,
) -> list[ActionCandidate]:
    """Rank only candidates that pass the canonical governance contract."""
    eligible = [candidate for candidate in candidates if candidate.eligible(registry)]
    return sorted(
        eligible,
        key=lambda c: (
            c.value,
            c.evidence_ready,
            c.reversible,
            c.protected_scope_preserved,
        ),
        reverse=True,
    )


def choose_next_action(
    state: MissionState,
    candidates: Sequence[ActionCandidate],
    registry: AuthorityRegistry | None = None,
) -> ActionPlan:
    """Select one highest-value executable action for the current verified state."""
    state.assert_valid()
    ranked = rank_candidates(candidates, registry)
    if not ranked:
        raise RuntimeError(
            "No eligible next action. Mission requires new evidence, authority, dependency resolution, or human decision."
        )

    winner = ranked[0]
    return ActionPlan(
        action=winner,
        expected_result=winner.description,
        verification_method=(
            "Refetch/observe the affected state, compare against the target, "
            "and record exact evidence before promoting status."
        ),
    )


def record_result(
    state: MissionState,
    plan: ActionPlan,
    receipt: ExecutionReceipt,
) -> MissionState:
    """Persist the observed result and derive the next state without false completion."""
    if receipt.action_id != plan.action.action_id:
        raise ValueError("Receipt action_id does not match planned action")

    state.current_action = plan.action.action_id
    state.activity.append(
        {
            "timestamp": receipt.timestamp,
            "action_id": receipt.action_id,
            "result": receipt.result,
            "evidence_state": receipt.evidence_state.value,
            "observed": receipt.observed,
            "evidence_source": receipt.evidence_source,
            "verified": receipt.verified,
        }
    )
    state.observed.append(receipt.observed)
    state.evidence.append(
        Evidence(
            evidence_id=f"receipt:{receipt.action_id}:{receipt.timestamp}",
            claim=receipt.result,
            state=receipt.evidence_state,
            observation=receipt.observed,
            source=receipt.evidence_source,
            timestamp=receipt.timestamp,
            commit=receipt.commit,
            deployment=receipt.deployment,
        )
    )

    if receipt.verified:
        if receipt.evidence_state not in {
            EvidenceState.VERIFIED,
            EvidenceState.LIVE_VERIFIED,
        }:
            raise ValueError("verified=True requires VERIFIED or LIVE_VERIFIED evidence state")
        state.verified.append(receipt.result)
        state.last_verified_state = receipt.observed
        state.completed_work.append(plan.action.description)
        state.block_status = BlockStatus.VERIFIED
    elif receipt.evidence_state in {EvidenceState.UNKNOWN, EvidenceState.CONFLICTED}:
        state.unknowns.append(receipt.observed)
        state.block_status = BlockStatus.BLOCKED
    else:
        state.block_status = BlockStatus.ACTIVE

    state.next_action = receipt.next_action
    state.next_action_reason = (
        "Derived from the verified/observed result and remaining mission gap."
        if receipt.next_action
        else None
    )
    state.updated_at = receipt.timestamp
    return state


def cold_start(mission: MissionState) -> dict[str, Any]:
    """Produce the minimum operational restoration surface for a fresh Naya."""
    mission.assert_valid()
    return {
        "protocol": RUNTIME_PROTOCOL,
        "project": mission.project,
        "mission": mission.mission,
        "desired_outcome": mission.desired_outcome,
        "current_state": mission.last_verified_state or "NO VERIFIED STATE RECORDED",
        "protected_scope": list(mission.protected_scope),
        "rejected_scope": list(mission.rejected_scope),
        "known": list(mission.known),
        "unknowns": list(mission.unknowns),
        "blockers": list(mission.blockers),
        "risks": list(mission.risks),
        "current_action": mission.current_action,
        "next_action": mission.next_action,
        "next_action_reason": mission.next_action_reason,
        "authority": "HUMAN > CONSTITUTION > SOURCE_OF_TRUTH > PROJECT > MODE > EXECUTION > OUTPUT",
    }


def activation_status(mission: MissionState) -> dict[str, Any]:
    """Evaluate whether the runtime can honestly call itself activated."""
    checks = {
        "knowledge_state_present": bool(mission.project and mission.mission),
        "mission_understood": bool(mission.desired_outcome),
        "current_state_restored": bool(mission.last_verified_state or mission.known),
        "next_action_determined": bool(mission.next_action),
        "protected_scope_present": bool(mission.protected_scope),
        "unknowns_explicit": mission.unknowns is not None,
        "validation_passes": not mission.validate(),
    }
    return {
        "protocol": RUNTIME_PROTOCOL,
        "active": all(checks.values()),
        "checks": checks,
        "principle": "KNOWLEDGE + ACTIVATION + EXECUTION = ACTIVE SUPERBRAIN",
    }
