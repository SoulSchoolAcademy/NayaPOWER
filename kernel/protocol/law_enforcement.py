"""
law_enforcement.py — the unified Law 11 + Law 12 machine API.

Per the Naya Code enforcement spec (Naya 1, 2026-10-11):

  evaluate(context, typed_action, policy_ref, evidence_refs)
      -> {PROHIBITED | NEEDS_AUTHORITY | NEEDS_EVIDENCE | ADMISSIBLE,
          reason_ids, scope, expiry, receipt_id}

Only ADMISSIBLE enters Value Calculus V2.1. Final `execute` re-checks fresh
scoped authorization, resource state, consent/revocation and the relevant
policy digest atomically where possible. Unknowns are refused and
fabricated/self-issued authority proofs are rejected.

Layering:
  evaluate() = Law 11 gate (typed_action.law11_gate) + Law 12 receipt
  binding (proof_receipt.issue_proof_receipt). The verdict is bound to the
  exact world it was earned against: source SHA, policy version/hash,
  resource state digest, scope, time, revocation.
  execute_checked() = execution-door re-gate (Law 11) + Law 12 proof
  revalidation + the executor. A stale or invalidated plan-time proof
  blocks execution even if the Law 11 re-gate passes: the proof expired
  when the world changed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from kernel.protocol.typed_action import (
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    Law11Verdict,
    TypedAction,
    execution_door_check,
    law11_gate,
)
from kernel.protocol.proof_receipt import (
    EXPIRED,
    ProofContext,
    ProofReceipt,
    UNBOUND,
    LAW_POLICY_VERSION,
    check_proof_validity,
    issue_proof_receipt,
)

# States returned by evaluate(). Identical to the Law 11 verdict vocabulary
# so the whole stack speaks one decision language.
ADMISSIBLE_STATE = ADMISSIBLE
NEEDS_AUTHORITY_STATE = NEEDS_AUTHORITY
NEEDS_EVIDENCE_STATE = NEEDS_EVIDENCE
PROHIBITED_STATE = PROHIBITED

# Reason: the execute-time re-check refused because the plan-time proof
# was invalidated by a material world change (Law 12).
PROOF_INVALIDATED = "PROOF_INVALIDATED"
EXECUTOR_NEVER_CALLED = "EXECUTOR_NEVER_CALLED"


@dataclass(frozen=True)
class EnforcementContext:
    """The world a verdict is earned against. Every bound field participates
    in Law 12 invalidation; UNBOUND fields are recorded openly and are
    non-comparable (they neither validate nor invalidate)."""
    actor_id: str
    source_sha: str = UNBOUND
    policy_version: str = UNBOUND
    policy_hash: str = UNBOUND
    resource_state_digest: str = UNBOUND
    scope: str = UNBOUND
    now: float = 0.0
    # Validity window for the issued proof, in seconds from now (None = unbounded).
    proof_ttl_seconds: float | None = None
    revocation_ref: str | None = None
    # Fresh-check inputs for execute_checked(): the current authority grant
    # and resource, compared against what evaluate() planned.
    current_authority_ref: str | None = None
    current_resource: str | None = None


@dataclass(frozen=True)
class EnforcementDecision:
    """The unified verdict. reason_ids carry the Law 11 gate's reasons;
    receipt_id names the immutable Law-12-bound proof receipt."""
    state: str  # ADMISSIBLE | NEEDS_AUTHORITY | NEEDS_EVIDENCE | PROHIBITED
    reason_ids: tuple[str, ...]
    scope: str
    expiry: float | None
    receipt_id: str
    proof: ProofReceipt

    @property
    def admissible(self) -> bool:
        return self.state == ADMISSIBLE_STATE


def evaluate(
    context: EnforcementContext,
    typed_action: TypedAction,
    policy_ref: str = LAW_POLICY_VERSION,
    evidence_refs: tuple[str, ...] = (),
) -> EnforcementDecision:
    """Run the Law 11 gate on a typed action and bind the verdict to the
    context as a Law 12 proof receipt.

    policy_ref: the governing policy/law profile reference (version string).
    Defaults to the canonical LAW_POLICY_VERSION (the Twelve Laws pin) —
    pass an explicit value only when judging under a different, named
    policy revision.
    evidence_refs: input evidence receipt IDs the verdict rests on.
    Returns an EnforcementDecision. Only ADMISSIBLE may enter V2.1.
    """
    verdict: Law11Verdict = law11_gate(typed_action)

    valid_until = (
        None
        if context.proof_ttl_seconds is None
        else context.now + context.proof_ttl_seconds
    )
    proof = issue_proof_receipt(
        actor_id=typed_action.actor_id,
        operation=typed_action.operation,
        environment=typed_action.environment,
        resource=typed_action.resource,
        law_verdict=verdict.verdict,
        reason_ids=verdict.reasons,
        policy_version=policy_ref,
        policy_hash=context.policy_hash,
        source_sha=context.source_sha,
        resource_state_digest=context.resource_state_digest,
        scope=context.scope,
        evidence_ids=tuple(evidence_refs),
        issued_at=context.now,
        valid_until=valid_until,
        revocation_ref=context.revocation_ref,
    )
    return EnforcementDecision(
        state=verdict.verdict,
        reason_ids=verdict.reasons,
        scope=context.scope,
        expiry=valid_until,
        receipt_id=proof.receipt_id,
        proof=proof,
    )


@dataclass(frozen=True)
class ExecutionOutcome:
    """Result of execute_checked(). executed=False means the executor was
    never called — the outcome carries the blocking reason, not a result."""
    executed: bool
    result: str | None
    reason_ids: tuple[str, ...]
    receipt_id: str


def execute_checked(
    plan_decision: EnforcementDecision,
    typed_action: TypedAction,
    executor: Callable[[], str],
    *,
    planned_authority_ref: str | None,
    planned_resource: str,
    fresh_context: EnforcementContext,
    revoked_refs: tuple[str, ...] = (),
) -> ExecutionOutcome:
    """Final atomic re-check at the last responsible moment, then execute.

    Order (fail-closed):
      1. Law 11 execution-door: authority withdrawn/changed or target changed
         -> blocked; the executor is never called.
      2. Law 12 proof revalidation: the plan-time proof receipt is checked
         against the fresh world. Any material move (SHA, policy, resource
         state, scope, revocation, expiry) -> PROOF_INVALIDATED; blocked.
      3. Only then: the executor fires, exactly once.

    Fabricated or self-issued authority cannot pass: the door compares the
    planned authority reference against the FRESH context, never against a
    caller-supplied "current" claim alone — and step 2 pins the proof to
    the plan-time world independently of what the caller asserts now.
    """
    # 1. Law 11 execution door.
    door = execution_door_check(
        typed_action,
        planned_authority_ref=planned_authority_ref,
        current_authority_ref=fresh_context.current_authority_ref,
        planned_resource=planned_resource,
        current_resource=(fresh_context.current_resource
                          if fresh_context.current_resource is not None
                          else planned_resource),
    )
    if door.verdict != ADMISSIBLE:
        return ExecutionOutcome(
            executed=False,
            result=None,
            reason_ids=door.reasons + (EXECUTOR_NEVER_CALLED,),
            receipt_id=plan_decision.receipt_id,
        )

    # 2. Law 12: the plan-time proof must still be valid in the fresh world.
    proof_ctx = ProofContext(
        source_sha=fresh_context.source_sha,
        policy_version=fresh_context.policy_version,
        policy_hash=fresh_context.policy_hash,
        resource_state_digest=fresh_context.resource_state_digest,
        scope=fresh_context.scope,
        now=fresh_context.now,
        revoked_refs=revoked_refs,
    )
    valid, event = check_proof_validity(plan_decision.proof, proof_ctx)
    if not valid:
        return ExecutionOutcome(
            executed=False,
            result=None,
            reason_ids=(PROOF_INVALIDATED, event or "UNKNOWN", EXECUTOR_NEVER_CALLED),
            receipt_id=plan_decision.receipt_id,
        )

    # 3. The world held: fire the executor exactly once.
    return ExecutionOutcome(
        executed=True,
        result=executor(),
        reason_ids=(),
        receipt_id=plan_decision.receipt_id,
    )
