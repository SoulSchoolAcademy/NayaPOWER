"""AER-LIVE-7: Minimal Pumping-Witness Integrity (spec).

Shawn's law (SN-0813, ratified 2026-10-10): An unboundedness
certificate requires reachable entry, positively debt-producing
arbitrarily repeatable cycle, valid exit after every finite repetition
count. Minimize constraints, not merely logs. Finite-token mutation
must invalidate the apparent cycle. Model-level unboundedness is not
automatically a fairness violation or physical realizability.

Certificate requirements:
1. Reachable entry: witness starts from a reachable state
2. Positive debt cycle: each traversal increases debt by > 0
3. Arbitrary repeatability: cycle can repeat any finite number of times
4. Valid exit: after N repetitions (any N), a valid exit exists

Integrity rules:
- Minimize the CONSTRAINTS, not just the log (short log with hidden
  assumptions is not minimal)
- Finite-token mutation test: if adding a finite resource bound breaks
  the cycle, it was never truly unbounded
- Model unboundedness ≠ fairness violation (may be allowed)
- Model unboundedness ≠ physical realizability (model may be wrong)

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PumpingWitness:
    """A claimed unboundedness certificate."""
    entry_reachable: bool
    debt_per_cycle: float  # must be > 0
    max_repetitions: Optional[int]  # None = arbitrary (unbounded)
    exit_valid_after_n: bool  # valid exit after every finite N
    constraints: tuple  # the minimized constraint set


@dataclass(frozen=True)
class WitnessVerdict:
    valid: bool
    reason: str = ""


def verify_witness(w: PumpingWitness) -> WitnessVerdict:
    """Verify a pumping witness per AER-LIVE-7."""
    if not w.entry_reachable:
        return WitnessVerdict(False, "entry not reachable")
    if w.debt_per_cycle <= 0:
        return WitnessVerdict(False, "cycle does not produce positive debt")
    if w.max_repetitions is not None:
        return WitnessVerdict(False, "cycle not arbitrarily repeatable")
    if not w.exit_valid_after_n:
        return WitnessVerdict(False, "no valid exit after repetitions")
    return WitnessVerdict(True, "valid pumping witness")


def finite_token_mutation_test(w: PumpingWitness,
                               token_bound: int) -> bool:
    """If a finite token bound breaks the cycle, it was never unbounded.

    Returns True if the witness SURVIVES the mutation (truly unbounded),
    False if the mutation invalidates it (was secretly bounded).
    """
    # Simulate: with finite tokens, can we still repeat arbitrarily?
    # If the witness requires unbounded tokens, it fails.
    # For spec: if max_repetitions was None but tokens are finite,
    # check if debt_per_cycle * N would exceed token capacity.
    # Simplified: a witness claiming arbitrary repetition must not
    # depend on an implicit infinite resource.
    return w.max_repetitions is None and w.debt_per_cycle > 0
    # Note: full implementation would model token consumption
