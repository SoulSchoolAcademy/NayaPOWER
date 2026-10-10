"""AER-LIVE-8: Full-State Repeatability (spec).

Shawn's law (SN-0814, ratified 2026-10-10): Repeatability requires an
inductive invariant over authority, budgets, resources, time, lifecycle,
evidence, and obligation state. Four proof obligations: entry,
invariant preservation, positive debt gain, exit availability.

Decisive CONTROL/TREATMENT pair:
- CONTROL: finite retries → reject repetition (retries exhaust)
- TREATMENT: eligible waiting consuming no retry → may remain repeatable

The invariant must cover the FULL state, not just the cycle. A cycle
that preserves debt but violates authority is not repeatable.

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FullState:
    """The full state the invariant must cover."""
    authority_valid: bool
    budget_remaining: float
    resources_available: bool
    time_valid: bool
    lifecycle_outstanding: bool
    evidence_intact: bool
    obligation_active: bool


@dataclass(frozen=True)
class RepeatabilityProof:
    """Four proof obligations for repeatability."""
    entry_established: bool      # 1. Valid entry to the invariant
    invariant_preserved: bool   # 2. Cycle preserves the full invariant
    debt_gain_positive: bool    # 3. Each cycle increases debt
    exit_available: bool         # 4. Valid exit remains reachable


def verify_repeatability(state: FullState,
                         proof: RepeatabilityProof) -> bool:
    """Verify full-state repeatability per AER-LIVE-8.

    All seven state components must hold AND all four proof obligations
    must be met. A single violation breaks repeatability.
    """
    state_ok = all([
        state.authority_valid,
        state.budget_remaining > 0,
        state.resources_available,
        state.time_valid,
        state.lifecycle_outstanding,
        state.evidence_intact,
        state.obligation_active,
    ])
    proof_ok = all([
        proof.entry_established,
        proof.invariant_preserved,
        proof.debt_gain_positive,
        proof.exit_available,
    ])
    return state_ok and proof_ok


def control_finite_retries() -> bool:
    """CONTROL: finite retries exhaust → reject repetition."""
    # Simulate 3 retries, each cycle consumes one
    retries = 3
    for _ in range(5):  # try 5 cycles
        if retries <= 0:
            return False  # cannot repeat
        retries -= 1
    return True  # unreachable


def treatment_eligible_waiting() -> bool:
    """TREATMENT: eligible waiting consumes no retry → may repeat."""
    # Waiting does not consume retries, so repetition is possible
    # (assuming other invariant components hold)
    state = FullState(
        authority_valid=True,
        budget_remaining=100.0,  # not consumed by waiting
        resources_available=True,
        time_valid=True,
        lifecycle_outstanding=True,
        evidence_intact=True,
        obligation_active=True,
    )
    proof = RepeatabilityProof(True, True, True, True)
    return verify_repeatability(state, proof)
