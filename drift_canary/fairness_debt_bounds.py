"""D60 / AER-LIVE-5: Computing Fairness-Debt Bounds Under Missing Evidence.

The possible-history debt law: calculate lower and upper fairness-debt
bounds across all independently defensible scheduling histories.

The gap it closes: D59's governor enumerates 2^k compatible histories
(fail-closed cap 2^12) and cannot bound a window with many unresolved
rounds — even when the unresolved rounds sit in short, independent
missing intervals. A 40-round window with 20 unresolved rounds in four
intervals of 5 is unassessable to D59, yet its debt bounds are exactly
computable. This module computes them.

The mechanism: exact debt-interval propagation. The reachable debt set
after each round is always a contiguous integer interval (theorem, proved
in BRAIN/01-GOVERNANCE/D60-FAIRNESS-DEBT-BOUNDS-V1.md and pinned by the
equivalence property test): every round maps an interval to an interval,
and every UNDETERMINED round takes the hull of its two branches. No
enumeration, O(N) time, exact — cross-validated against D59's brute-force
assessor on small N.

Missing intervals: maximal consecutive UNDETERMINED runs. Each interval's
added width (width_after - width_before, provably >= 0) is reported,
sorted as the reconstruction-priority order — the evidence-recovery
obligation that would most reduce uncertainty comes first, feeding D59's
open_reconstruction().

Independently defensible histories: a history is a completion of every
UNDETERMINED round to ELIGIBLE/INELIGIBLE. It is defensible iff every
settled verdict binds its completion and every UNDETERMINED round
completes both ways — completions are never asserted as fact. Settled
rounds enter only via D59's apply_settlement() with a re-proven D58
receipt; this engine takes RoundRecords and manufactures no completions.
Unknown eligibility is neither proven ineligibility nor a fairness
violation — the bounds hold the uncertainty open.

Fail-closed: a missing interval longer than MAX_MISSING_INTERVAL_ROUNDS
refuses — that is D61 (unbounded / variable-length) territory, never
approximated here. Non-BOUNDED contracts, empty round lists, duplicate
round seqs, contract/obligation mismatch — all raise.

Composes with (additive only — nothing here modifies them):
  eligibility_proof.py — ELIGIBLE / INELIGIBLE / UNDETERMINED verdicts.
  fairness.py — FairnessContract (BOUNDED: the bound), the ledger
                debt-evolution rule this module replays per history.
  unresolved_evidence.py — RoundRecord (the rounds this module bounds),
                BREACH / NO_BREACH / UNRESOLVED verdicts, the D58-receipt
                settlement path. This module never writes to a governor.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT, or
any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass

from drift_canary.eligibility_proof import (
    ELIGIBLE,
    INELIGIBLE,
    UNDETERMINED,
)
from drift_canary.fairness import FairnessContract
from drift_canary.unresolved_evidence import (
    BREACH,
    NO_BREACH,
    UNRESOLVED,
    RoundRecord,
)

# Fail-closed cap: a missing interval longer than this is D61
# (unbounded / variable-length) territory — refused, never approximated.
MAX_MISSING_INTERVAL_ROUNDS = 64


class DebtBoundError(Exception):
    """Base for fail-closed debt-bound errors."""


class MissingIntervalTooLongError(DebtBoundError):
    """A missing interval exceeds the finite cap. D61 territory. Refused."""


class UnknownObligationError(DebtBoundError):
    """Bound computation requested with no registered rounds."""


class DuplicateRoundError(DebtBoundError):
    """Two rounds with the same round_seq in one bound computation."""


class UnboundedContractError(DebtBoundError):
    """Bound computation needs a BOUNDED contract. Fail closed."""


class ContractObligationMismatchError(DebtBoundError):
    """The contract's obligation id does not match the rounds'. Fail closed."""


@dataclass(frozen=True)
class MissingInterval:
    """One maximal consecutive UNDETERMINED run and its uncertainty cost.

    added_width = width_after - width_before is provably >= 0 (each
    UNDETERMINED step is width-non-decreasing), so the priority order
    (descending added_width) is exactly the order in which recovering the
    missing evidence would shrink the bound uncertainty.
    """
    start_seq: int
    end_seq: int
    length: int
    width_before: int
    width_after: int

    def __post_init__(self):
        assert self.length >= 1, "an interval has at least one round"
        assert self.start_seq <= self.end_seq, "inverted interval"
        assert self.width_after >= self.width_before, (
            "width is non-decreasing across a missing interval — "
            "a decrease means the propagation is broken")

    @property
    def added_width(self) -> int:
        return self.width_after - self.width_before


@dataclass(frozen=True)
class DebtBoundReceipt:
    """Lower/upper fairness-debt bounds over every defensible history.

    debt_min/debt_max is the exact bound interval — proven equal to the
    min/max over the full (unenumerated) defensible-history set. The
    three-valued verdict, the witnesses attaining the extremes, and the
    missing-interval priority order make the receipt auditable. Completions
    live only inside the receipt; nothing here asserts any single
    completion as fact.
    """
    obligation_id: str
    bound: int
    debt_min: int
    debt_max: int
    verdict: str
    histories_admitted: int            # 2 ** unresolved_count, computed not enumerated
    missing_intervals: tuple           # MissingInterval, priority order
    unresolved_rounds: tuple
    breach_witness: tuple | None       # ((round_seq, eligible), ...) attaining debt_max
    clearance_witness: tuple | None    # ((round_seq, eligible), ...) attaining debt_min

    def __post_init__(self):
        assert self.verdict in (BREACH, NO_BREACH, UNRESOLVED), f"bad verdict: {self.verdict}"
        assert 0 <= self.debt_min <= self.debt_max, "inverted debt bound interval"
        assert self.histories_admitted >= 1, "at least the empty completion is admitted"
        if self.verdict == BREACH:
            assert self.debt_min > self.bound, "BREACH needs every defensible history over the bound"
            assert self.breach_witness is not None
        if self.verdict == NO_BREACH:
            assert self.debt_max <= self.bound, "NO_BREACH needs no defensible history over the bound"
            assert self.clearance_witness is not None
        if self.verdict == UNRESOLVED:
            assert self.debt_min <= self.bound < self.debt_max, "UNRESOLVED needs a straddling bound interval"


def _defensible_completions(record: RoundRecord) -> list[tuple[bool, bool]]:
    """The admissibility predicate: which (eligible, adequate_service)
    completions of one round are independently defensible.

    Settled verdicts bind their completion. UNDETERMINED completes both
    ways — the completion is a hypothesis for bound computation, never an
    asserted fact. adequate_service is always a known bool (RoundRecord
    refuses unknowns); a missing service outcome is a different unknown
    and is not completed here.
    """
    if record.verdict == ELIGIBLE:
        return [(True, record.adequate_service)]
    if record.verdict == INELIGIBLE:
        return [(False, record.adequate_service)]
    return [(True, record.adequate_service), (False, record.adequate_service)]


def _debt_after(debt: int, eligible: bool, adequate_service: bool) -> int:
    """One history step. Mirrors FairnessLedger.record_round exactly."""
    if not eligible:
        return debt
    if adequate_service:
        return 0
    return debt + 1


class DebtBoundEngine:
    """Computes exact debt bounds over defensible histories — no enumeration.

    The engine is stateless and read-only: it takes RoundRecords (as left
    by the verifier, including any D59 apply_settlement() replacements) and
    returns a DebtBoundReceipt. It manufactures no completions and writes
    to no governor, ledger, or live path.
    """

    @staticmethod
    def compute(rounds: list[RoundRecord],
                contract: FairnessContract) -> DebtBoundReceipt:
        """Lower/upper debt bounds across every defensible history."""
        if contract.standard != "BOUNDED":
            raise UnboundedContractError(
                f"bound computation needs a BOUNDED contract, got {contract.standard}")
        if not rounds:
            raise UnknownObligationError(
                "no rounds supplied — no evidence, no bounds")
        obligation_ids = {r.obligation_id for r in rounds}
        if len(obligation_ids) != 1:
            raise DebtBoundError(
                f"rounds span obligations {sorted(obligation_ids)} — "
                "bound one obligation at a time")
        obligation_id = next(iter(obligation_ids))
        if contract.obligation_id != obligation_id:
            raise ContractObligationMismatchError(
                f"contract binds {contract.obligation_id}, rounds bind "
                f"{obligation_id} — refusing to judge one obligation by "
                "another's bound")

        ordered = sorted(rounds, key=lambda r: r.round_seq)
        seqs = [r.round_seq for r in ordered]
        if len(set(seqs)) != len(seqs):
            dup = next(s for s in seqs if seqs.count(s) > 1)
            raise DuplicateRoundError(
                f"round_seq {dup} appears twice — defensible histories "
                "need unique rounds")

        bound = contract.service_bound_rounds
        if not isinstance(bound, int) or isinstance(bound, bool) or bound < 0:
            raise DebtBoundError(f"bound must be a non-negative int, got {bound!r}")

        # -- single in-order pass: exact interval propagation with ---------
        # -- witness tracking, missing-interval detection interleaved ----
        lo, hi = 0, 0
        lo_wit: tuple = ()
        hi_wit: tuple = ()
        unresolved_count = 0
        interval_reports: list[MissingInterval] = []
        i = 0
        while i < len(ordered):
            record = ordered[i]
            if record.verdict == UNDETERMINED:
                # One maximal missing interval: fail closed on D61
                # territory BEFORE propagating anything through it.
                j = i
                while j < len(ordered) and ordered[j].verdict == UNDETERMINED:
                    j += 1
                length = j - i
                if length > MAX_MISSING_INTERVAL_ROUNDS:
                    raise MissingIntervalTooLongError(
                        f"missing interval rounds {ordered[i].round_seq}.."
                        f"{ordered[j - 1].round_seq} spans {length} rounds > cap "
                        f"{MAX_MISSING_INTERVAL_ROUNDS} — unbounded-interval "
                        "territory (D61), refused, never approximated")
                width_before = hi - lo
                for k in range(i, j):
                    rec = ordered[k]
                    unresolved_count += 1
                    # Each branch: (new_lo, new_hi, new_lo_wit, new_hi_wit).
                    branches = []
                    for eligible, adequate in _defensible_completions(rec):
                        step = (rec.round_seq, eligible)
                        if not eligible:
                            branches.append((lo, hi,
                                             lo_wit + (step,), hi_wit + (step,)))
                        elif adequate:
                            branches.append((0, 0,
                                             lo_wit + (step,), lo_wit + (step,)))
                        else:
                            branches.append((lo + 1, hi + 1,
                                             lo_wit + (step,), hi_wit + (step,)))
                    # Hull of the branches. The reachable set stays a
                    # contiguous integer interval (theorem); the hull is exact.
                    # Deterministic tie-break: first branch attaining the extreme.
                    new_lo = min(b[0] for b in branches)
                    new_hi = max(b[1] for b in branches)
                    lo_wit = next(b[2] for b in branches if b[0] == new_lo)
                    hi_wit = next(b[3] for b in branches if b[1] == new_hi)
                    lo, hi = new_lo, new_hi
                width_after = hi - lo
                interval_reports.append(MissingInterval(
                    start_seq=ordered[i].round_seq,
                    end_seq=ordered[j - 1].round_seq,
                    length=length,
                    width_before=width_before,
                    width_after=width_after,
                ))
                i = j
                continue
            # Settled round: exactly one defensible completion.
            eligible, adequate = _defensible_completions(record)[0]
            step = (record.round_seq, eligible)
            if not eligible:
                lo_wit = lo_wit + (step,)
                hi_wit = hi_wit + (step,)
            elif adequate:
                # Reset collapses the interval: every history lands at 0,
                # so both extremes share one witness.
                lo, hi = 0, 0
                wit = lo_wit + (step,)
                lo_wit, hi_wit = wit, wit
            else:
                lo, hi = lo + 1, hi + 1
                lo_wit = lo_wit + (step,)
                hi_wit = hi_wit + (step,)
            i += 1

        # Sanity: propagation never leaves the non-negative integers, and
        # the interval never inverts. Both are theorem consequences; both
        # are checked, because a silent violation would manufacture bounds.
        assert 0 <= lo <= hi, f"propagation left the valid debt range: [{lo}, {hi}]"

        if lo > bound:
            verdict = BREACH
        elif hi <= bound:
            verdict = NO_BREACH
        else:
            verdict = UNRESOLVED

        # Priority order: the interval whose recovery would most shrink the
        # uncertainty comes first. Deterministic tie-break on start_seq.
        priority = tuple(sorted(
            interval_reports,
            key=lambda m: (-m.added_width, m.start_seq),
        ))

        return DebtBoundReceipt(
            obligation_id=obligation_id,
            bound=bound,
            debt_min=lo,
            debt_max=hi,
            verdict=verdict,
            histories_admitted=2 ** unresolved_count,
            missing_intervals=priority,
            unresolved_rounds=tuple(
                r.round_seq for r in ordered if r.verdict == UNDETERMINED),
            breach_witness=hi_wit if verdict != NO_BREACH else None,
            clearance_witness=lo_wit if verdict != BREACH else None,
        )
