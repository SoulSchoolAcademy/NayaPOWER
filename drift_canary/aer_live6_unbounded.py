"""AER-LIVE-6: Variable-Length and Unbounded Missing Histories (spec).

Shawn's law (SN-0812, ratified 2026-10-10): A missing interval is a
language of possible event sequences, not one unknown round.
Distinguishes unknown length, unbounded debt, proven fairness
violation. Distinguishes UNBOUNDED_IN_MODEL from
NO_FINITE_UPPER_BOUND_ESTABLISHED.

Decisive U*S fixture: final debt 0, peak 1 to infinity, verdict
unresolved.

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class HistoryVerdict(Enum):
    # Proven finite bound exists
    BOUNDED = "BOUNDED"
    # Proven unbounded within the model
    UNBOUNDED_IN_MODEL = "UNBOUNDED_IN_MODEL"
    # Cannot establish any finite upper bound (weaker than proven unbounded)
    NO_FINITE_UPPER_BOUND_ESTABLISHED = "NO_FINITE_UPPER_BOUND_ESTABLISHED"
    # Proven fairness violation (not just unbounded)
    FAIRNESS_VIOLATION_PROVEN = "FAIRNESS_VIOLATION_PROVEN"
    # Cannot determine
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class MissingInterval:
    """A missing interval as a language of possible sequences."""
    # None = unknown length; int = known max length
    max_length: Optional[int]
    # Possible debt range across all compatible sequences
    debt_min: float
    # None = unbounded above
    debt_max: Optional[float]


def assess_interval(interval: MissingInterval,
                    violation_threshold: float) -> HistoryVerdict:
    """Assess a missing interval.

    Distinguishes:
    - Unknown length vs unbounded debt vs proven violation
    - UNBOUNDED_IN_MODEL (proven) vs NO_FINITE_UPPER_BOUND (unknown)
    """
    # If max debt is bounded and below threshold → bounded
    if interval.debt_max is not None:
        if interval.debt_max <= violation_threshold:
            return HistoryVerdict.BOUNDED
        # Bounded but exceeds threshold → proven violation
        return HistoryVerdict.FAIRNESS_VIOLATION_PROVEN

    # Debt unbounded above
    if interval.max_length is None:
        # Unknown length + unbounded debt → cannot establish bound,
        # but not proven unbounded in model (we don't know the sequences)
        return HistoryVerdict.NO_FINITE_UPPER_BOUND_ESTABLISHED

    # Known length but unbounded debt → model allows unbounded
    return HistoryVerdict.UNBOUNDED_IN_MODEL


def u_star_fixture() -> HistoryVerdict:
    """Decisive U*S: final debt 0, peak 1 to infinity, verdict unresolved.

    The interval allows arbitrarily many sequences; debt could be 1
    or unbounded. Final observed debt is 0 (after interval), but the
    possible history includes unbounded debt. Verdict: unresolved —
    we cannot prove bounded, unbounded, or violation.
    """
    # The U*S pattern: unknown sequences, debt in [1, inf)
    # Final debt 0 doesn't constrain the possible history
    interval = MissingInterval(
        max_length=None,  # unknown length
        debt_min=1.0,
        debt_max=None,  # unbounded
    )
    result = assess_interval(interval, violation_threshold=100.0)
    # Must be NO_FINITE_UPPER_BOUND, not UNBOUNDED_IN_MODEL
    # (we haven't proven the model allows it, we just can't bound it)
    assert result == HistoryVerdict.NO_FINITE_UPPER_BOUND_ESTABLISHED
    return HistoryVerdict.UNRESOLVED
