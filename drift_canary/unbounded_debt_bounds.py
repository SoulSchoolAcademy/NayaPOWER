"""D61 / AER-LIVE-6: Fairness-Debt Bounds for Unbounded Missing Intervals.

The unbounded missing-history law: interpret an incomplete scheduling
interval as a constrained set of possible event sequences — including
variable-length ones — and compute current and peak debt bounds without
interchanging the three things that must never be interchanged:
unknown length, unbounded debt, proven violation.

The gap it closes: the finite debt-bound engine refuses missing intervals
longer than its cap (unbounded / variable-length territory — never
approximated there). This module is that territory. It models the gap as
a sequence language:

    U*S  =  any finite number of unserved rounds, then one service round.

U (unserved): eligible + inadequate service -> debt + 1. This is the
repeatable debt-adding cycle: reachable (the ledger's own evolution rule),
with no mandatory reset.
S (service): eligible + adequate service -> debt 0. This is the valid
exit: it terminates the language and clears the counter, not the history.

Inert rounds (ineligible -> debt unchanged) are absorbed by the language:
a history U^k I^m S attains the same peak as U^k S, so the attainable-peak
set is unchanged. The language needs no inert symbol.

THEOREM (attainability, pinned by the replay property test): for the U*S
language with entry debt d, the attainable (peak, final) pairs are exactly
{(d+k, 0) : k >= 0}. For an entry debt interval [lo, hi], the attainable
peaks are every integer >= lo — "one-to-infinity" — and the final debt is
exactly 0. The service clears the counter, not the history.

THEOREM (verdict): the verdict answers off the PEAK, never the final.
BREACH iff entry_lo > bound (the 0-U history peaks at entry_lo > bound,
and every defensible history peaks >= entry_lo). Otherwise UNRESOLVED.
NO_BREACH is unreachable without an established finite limit: with an
unbounded peak and a finite bound, the history with
k = bound - entry_lo + 1 unserved rounds always peaks above the bound.
Compliance is establishable only through a finite limit, never through
the unbounded interval itself. A later service reset never erases a
possible earlier breach.

Three proof statuses — never interchanged, even when both display infinity:
  PROVEN_UNBOUNDED            — a constructive witness is exhibited: the
                               reachable repeatable debt-adding cycle (U)
                               with no mandatory reset, demonstrated to
                               reach a valid exit (S). Sampled witness
                               histories are constructed and replayed.
  NO_FINITE_BOUND_ESTABLISHED — the unbounded upper is recognized, but only
                               within the stated evidence and model
                               assumptions, and no constructive witness is
                               exhibited (the U* language without a
                               demonstrated exit cannot carry one).
  FINITE_LIMIT_ESTABLISHED    — the finite-limit hunt succeeded: trusted
                               sequence numbers, an enforced reset
                               mechanism, or a LAW withdrawal caps the
                               unserved count. The interval is then bounded
                               territory again — the three-valued verdict on
                               the trajectory defers to the finite engine.

Circular reasoning is refused mechanically: the SLA under test can never
serve as its own enforcement evidence. A finite limit is accepted only
with a named tested-SLA reference that differs from the limit's evidence.

The independent verifier (verify_compliance_claim) rejects the AER-LIVE-006
mutation: a compliance claim that examines only the final debt and declares
NO_BREACH is refused — final-debt-only evidence cannot establish compliance
over an unbounded interval, because the peak is the controlling quantity.

Defensibility doctrine: each word of the language is a defensible history
WITHIN THE STATED MODEL ASSUMPTIONS (named on every receipt) — a hypothesis
for bound computation, never an asserted fact. This engine manufactures no
completions and writes to no governor, ledger, or live path.

Composes with (additive only — nothing here modifies them):
  fairness.py — FairnessContract (BOUNDED: the bound), the ledger
                debt-evolution rule this module's U/S steps mirror exactly.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT, or
any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from drift_canary.fairness import FairnessContract

# ---------------------------------------------------------------------------
# Vocabulary. The D58/D59/D60 line uses these same verdict names; this module
# defines its own (those modules are not on main yet) so the line composes
# when they merge — identical strings, no import coupling.
# ---------------------------------------------------------------------------
BREACH = "BREACH"
NO_BREACH = "NO_BREACH"
UNRESOLVED = "UNRESOLVED"
VERDICTS = (BREACH, NO_BREACH, UNRESOLVED)

PROVEN_UNBOUNDED = "PROVEN_UNBOUNDED"
NO_FINITE_BOUND_ESTABLISHED = "NO_FINITE_BOUND_ESTABLISHED"
FINITE_LIMIT_ESTABLISHED = "FINITE_LIMIT_ESTABLISHED"
PEAK_STATUSES = (
    PROVEN_UNBOUNDED,
    NO_FINITE_BOUND_ESTABLISHED,
    FINITE_LIMIT_ESTABLISHED,
)

# The only admissible provenances for a finite limit on the unserved count.
# Anything else — including the SLA under test — is refused.
TRUSTED_SEQUENCE_NUMBERS = "TRUSTED_SEQUENCE_NUMBERS"
ENFORCED_RESET = "ENFORCED_RESET"
LAW_WITHDRAWAL = "LAW_WITHDRAWAL"
FINITE_LIMIT_SOURCES = (
    TRUSTED_SEQUENCE_NUMBERS,
    ENFORCED_RESET,
    LAW_WITHDRAWAL,
)


class UnboundedDebtError(Exception):
    """Base for fail-closed unbounded-debt errors."""


class UnboundedContractError(UnboundedDebtError):
    """The contract is not BOUNDED. An unbounded interval under a
    non-BOUNDED contract is doubly unjudgeable — refused."""


class ContractObligationMismatchError(UnboundedDebtError):
    """The interval and the contract bind different obligations."""


class UnknownLimitSourceError(UnboundedDebtError):
    """A claimed finite limit cites a source outside the admissible three."""


class CircularEvidenceError(UnboundedDebtError):
    """The finite limit's evidence IS the SLA under test (or the tested SLA
    was not named, so circularity cannot be excluded). The SLA being tested
    can never serve as its own enforcement evidence."""


class FinalDebtOnlyClaimError(UnboundedDebtError):
    """A compliance claim that examines only the final debt. The AER-LIVE-006
    mutation: final debt 0 is not compliance — the peak is the controlling
    quantity, and a later service reset never erases a possible earlier
    breach."""


class PeakUnboundedClaimError(UnboundedDebtError):
    """A NO_BREACH claim against an unbounded peak. Compliance is
    establishable only through a finite limit, never through the unbounded
    interval itself."""


class ClaimMismatchError(UnboundedDebtError):
    """A claim inconsistent with the receipt it cites."""


# ---------------------------------------------------------------------------
# The sequence language.
# ---------------------------------------------------------------------------
# One history step, mirroring FairnessLedger.record_round exactly:
#   U: eligible + inadequate service -> debt + 1   (the repeatable cycle)
#   S: eligible + adequate service  -> debt 0      (the valid exit)
_STEP_U = "U"
_STEP_S = "S"


def _apply_step(debt: int, step: str) -> int:
    """One language step. Mirrors FairnessLedger.record_round exactly."""
    if step == _STEP_U:
        return debt + 1
    if step == _STEP_S:
        return 0
    raise UnboundedDebtError(f"unknown language step {step!r} — only U and S exist")


def witness_history(entry_debt: int, unserved_rounds: int) -> tuple[str, ...]:
    """The constructive witness history: U repeated `unserved_rounds` times,
    then the valid exit S. A hypothesis for bound computation — never an
    asserted fact."""
    if not isinstance(unserved_rounds, int) or isinstance(unserved_rounds, bool):
        raise UnboundedDebtError(
            f"unserved_rounds must be an int, got {unserved_rounds!r}")
    if unserved_rounds < 0:
        raise UnboundedDebtError(
            f"unserved_rounds must be >= 0, got {unserved_rounds}")
    return (_STEP_U,) * unserved_rounds + (_STEP_S,)


def replay_history(entry_debt: int, history: tuple[str, ...]) -> tuple[int, int]:
    """Replay a witness history: returns (peak_debt, final_debt). The replay
    — not the receipt — is the authority on what a history attains."""
    debt = entry_debt
    peak = entry_debt
    for step in history:
        debt = _apply_step(debt, step)
        peak = max(peak, debt)
    return peak, debt


@dataclass(frozen=True)
class UnboundedInterval:
    """The missing interval the finite engine refused: unbounded length,
    unknown (or untrusted) sequence numbers. entry_debt_lo/hi is the debt
    interval at the interval's start — from the finite engine's propagation
    up to the refusal point, or from the ledger."""
    obligation_id: str
    entry_debt_lo: int
    entry_debt_hi: int
    must_end_with_service: bool = True  # U*S when True, U* when False

    def __post_init__(self):
        if not self.obligation_id:
            raise UnboundedDebtError("interval needs an obligation id")
        for name, v in (("entry_debt_lo", self.entry_debt_lo),
                        ("entry_debt_hi", self.entry_debt_hi)):
            if not isinstance(v, int) or isinstance(v, bool) or v < 0:
                raise UnboundedDebtError(
                    f"{name} must be a non-negative int, got {v!r}")
        if self.entry_debt_lo > self.entry_debt_hi:
            raise UnboundedDebtError(
                f"inverted entry debt interval "
                f"[{self.entry_debt_lo}, {self.entry_debt_hi}]")


@dataclass(frozen=True)
class FiniteLimit:
    """The finite-limit hunt's result: a named, admissible source capping the
    unserved count, with an evidence reference. The tested SLA is named at
    assess() time; a limit whose evidence IS the tested SLA is refused."""
    source: str
    max_unserved_rounds: int
    evidence_ref: str

    def __post_init__(self):
        if self.source not in FINITE_LIMIT_SOURCES:
            raise UnknownLimitSourceError(
                f"finite-limit source {self.source!r} not in "
                f"{list(FINITE_LIMIT_SOURCES)} — refused")
        if (not isinstance(self.max_unserved_rounds, int)
                or isinstance(self.max_unserved_rounds, bool)
                or self.max_unserved_rounds < 0):
            raise UnboundedDebtError(
                "max_unserved_rounds must be a non-negative int, got "
                f"{self.max_unserved_rounds!r}")
        if not self.evidence_ref:
            raise UnboundedDebtError("a finite limit needs an evidence_ref")


@dataclass(frozen=True)
class UnboundednessWitness:
    """The constructive witness for PROVEN_UNBOUNDED: the reachable
    repeatable debt-adding cycle (U) with no mandatory reset, demonstrated
    to reach a valid exit (S). `demonstrated` carries sampled (k, peak,
    final) triples at `entry_debt` — constructed and replayed, not trusted."""
    entry_debt: int = 0
    cycle_step: str = (
        "U: eligible + inadequate service -> debt + 1 "
        "(repeatable; no mandatory reset; mirrors FairnessLedger.record_round)")
    exit_step: str = (
        "S: eligible + adequate service -> debt 0 "
        "(valid exit; terminates the language; clears the counter, not the history)")
    demonstrated: tuple = field(default_factory=tuple)

    def __post_init__(self):
        if not isinstance(self.entry_debt, int) or isinstance(self.entry_debt, bool) \
                or self.entry_debt < 0:
            raise UnboundedDebtError(
                f"witness entry_debt must be a non-negative int, got {self.entry_debt!r}")
        for triple in self.demonstrated:
            k, peak, final = triple
            if peak != self.entry_debt + k or final != 0:
                raise UnboundedDebtError(
                    f"witness triple {triple!r} is not a U*S replay at entry "
                    f"{self.entry_debt} (need peak == entry + k and final == 0)")


@dataclass(frozen=True)
class UnboundedDebtReceipt:
    """What the unbounded interval establishes — and what it does not.

    The verdict answers off the PEAK, never the final. final_debt is
    reported exactly (0 for U*S; None for U* without an exit, where the
    final is itself unbounded) so that no reader mistakes it for the
    verdict basis. model_assumptions names the assumptions the unbounded
    upper rests on.
    """
    obligation_id: str
    bound: int
    entry_debt_lo: int
    entry_debt_hi: int
    final_debt: int | None
    final_debt_basis: str
    peak_status: str
    peak_lower_bound: int
    peak_upper_bound: int | None  # None = unbounded
    peak_basis: str
    witness: UnboundednessWitness | None
    finite_limit: FiniteLimit | None
    verdict: str
    verdict_basis: str
    defers_to: str | None
    model_assumptions: tuple

    def __post_init__(self):
        assert self.peak_status in PEAK_STATUSES, self.peak_status
        assert self.verdict in VERDICTS, self.verdict
        assert 0 <= self.peak_lower_bound, "peak lower bound non-negative"
        assert self.model_assumptions, "unbounded uppers rest on stated assumptions"
        # The three statuses are never interchanged.
        if self.peak_status == PROVEN_UNBOUNDED:
            assert self.witness is not None, "PROVEN_UNBOUNDED needs the witness"
            assert self.finite_limit is None, "witness and finite limit exclude each other"
            assert self.peak_upper_bound is None, "proven-unbounded peak has no finite upper"
        if self.peak_status == NO_FINITE_BOUND_ESTABLISHED:
            assert self.witness is None, "no witness exhibited for this status"
            assert self.finite_limit is None, "no finite limit established for this status"
            assert self.peak_upper_bound is None, "unbounded peak has no finite upper"
        if self.peak_status == FINITE_LIMIT_ESTABLISHED:
            assert self.finite_limit is not None, "status needs the limit"
            assert self.witness is None, "finite limit supersedes the witness"
            assert self.peak_upper_bound is not None, "finite limit bounds the peak"
        # The verdict answers off the peak — never the final, never NO_BREACH
        # without a finite limit.
        if self.verdict == BREACH:
            assert self.peak_lower_bound > self.bound, \
                "BREACH needs every defensible history's peak over the bound"
        if self.verdict == NO_BREACH:
            assert self.finite_limit is not None, \
                "NO_BREACH is establishable only through a finite limit"
            assert self.peak_upper_bound is not None \
                and self.peak_upper_bound <= self.bound, \
                "NO_BREACH needs no defensible history's peak over the bound"
        if self.verdict == UNRESOLVED:
            assert not (self.peak_lower_bound > self.bound), \
                "UNRESOLVED contradicts a proven peak breach"
            assert self.finite_limit is None or self.peak_upper_bound is None \
                or self.peak_upper_bound > self.bound, \
                "UNRESOLVED contradicts a proven peak clearance"


# Sampled witness demonstrations: (k unserved rounds) — the constructive
# witness exhibits the cycle reaching the exit at each sampled length.
_WITNESS_SAMPLE_KS = (0, 1, 2, 3, 5, 8, 13, 64, 1000)

_MODEL_ASSUMPTIONS_USS = (
    "The missing interval is modeled as the sequence language U*S: any "
    "finite number of unserved rounds (eligible + inadequate service, "
    "debt + 1 each) followed by exactly one service round (debt -> 0).",
    "Each word of the language is a defensible history WITHIN THESE "
    "ASSUMPTIONS — a hypothesis for bound computation, never an asserted "
    "fact. Inert (ineligible) rounds are absorbed: U^k I^m S attains the "
    "same peak as U^k S.",
    "The unbounded upper is recognized only within the stated evidence "
    "and these model assumptions.",
)
_MODEL_ASSUMPTIONS_U_STAR = (
    "The missing interval is modeled as the language U*: an unbounded "
    "number of unserved rounds with no demonstrated exit. The final debt "
    "is itself unbounded; no constructive unboundedness witness is "
    "exhibited without a valid exit.",
    "Each word of the language is a defensible history WITHIN THESE "
    "ASSUMPTIONS — a hypothesis for bound computation, never an asserted "
    "fact.",
)


class UnboundedDebtEngine:
    """Assesses an unbounded missing interval — the territory the finite
    engine refuses. Stateless and read-only: it takes the interval, the
    contract, and optionally the finite-limit hunt's result, and returns a
    receipt. It manufactures no completions and writes to no governor,
    ledger, or live path."""

    @staticmethod
    def assess(interval: UnboundedInterval,
               contract: FairnessContract,
               finite_limit: FiniteLimit | None = None,
               tested_sla_ref: str = "") -> UnboundedDebtReceipt:
        """Bound the unbounded interval. `tested_sla_ref` names the SLA
        under test — required whenever a finite limit is supplied, so the
        circularity check can run."""
        if contract.standard != "BOUNDED":
            raise UnboundedContractError(
                f"unbounded-interval assessment needs a BOUNDED contract, "
                f"got {contract.standard!r}")
        if contract.obligation_id != interval.obligation_id:
            raise ContractObligationMismatchError(
                f"contract binds {contract.obligation_id}, interval binds "
                f"{interval.obligation_id} — refusing to judge one "
                f"obligation by another's bound")
        bound = contract.service_bound_rounds
        if not isinstance(bound, int) or isinstance(bound, bool) or bound < 0:
            raise UnboundedDebtError(f"bound must be a non-negative int, got {bound!r}")

        lo, hi = interval.entry_debt_lo, interval.entry_debt_hi

        if finite_limit is not None:
            return UnboundedDebtEngine._assess_finite_limit(
                interval, bound, lo, hi, finite_limit, tested_sla_ref)

        # -- the genuinely unbounded case ---------------------------------
        if interval.must_end_with_service:
            # U*S: the terminal service clears the counter exactly.
            final_debt: int | None = 0
            final_basis = ("terminal service S clears the counter: every word "
                           "of U*S ends with debt 0 regardless of entry debt")
            demonstrated = tuple(
                (k, lo + k, 0) for k in _WITNESS_SAMPLE_KS
            )
            # The sampled triples are constructed AND replayed at the actual
            # entry debt: replay must give (peak == entry + k, final == 0).
            for k, peak, final in demonstrated:
                r_peak, r_final = replay_history(lo, witness_history(lo, k))
                assert (r_peak, r_final) == (peak, final), \
                    f"witness construction/replay mismatch at k={k}"
                assert (r_peak, r_final) == (lo + k, 0)
            witness = UnboundednessWitness(entry_debt=lo, demonstrated=demonstrated)
            status = PROVEN_UNBOUNDED
            peak_basis = ("constructive witness exhibited: the repeatable "
                          "debt-adding cycle U (no mandatory reset) reaches "
                          "the valid exit S at every sampled length; "
                          "attainable peaks are every integer >= entry debt "
                          "(one-to-infinity)")
            assumptions = _MODEL_ASSUMPTIONS_USS
        else:
            # U* without a demonstrated exit: unbounded upper recognized
            # within the stated assumptions, but no constructive witness —
            # the witness requires a valid exit.
            final_debt = None
            final_basis = ("no demonstrated exit: the final debt is itself "
                           "unbounded over U*")
            witness = None
            status = NO_FINITE_BOUND_ESTABLISHED
            peak_basis = ("unbounded upper recognized within the stated "
                          "evidence and model assumptions; no valid exit "
                          "demonstrated, so no constructive witness is "
                          "exhibited — this status is not PROVEN_UNBOUNDED")
            assumptions = _MODEL_ASSUMPTIONS_U_STAR

        verdict, verdict_basis = UnboundedDebtEngine._peak_verdict(
            lo, bound, status)

        return UnboundedDebtReceipt(
            obligation_id=interval.obligation_id,
            bound=bound,
            entry_debt_lo=lo,
            entry_debt_hi=hi,
            final_debt=final_debt,
            final_debt_basis=final_basis,
            peak_status=status,
            peak_lower_bound=lo,
            peak_upper_bound=None,
            peak_basis=peak_basis,
            witness=witness,
            finite_limit=None,
            verdict=verdict,
            verdict_basis=verdict_basis,
            defers_to=None,
            model_assumptions=assumptions,
        )

    @staticmethod
    def _assess_finite_limit(interval: UnboundedInterval,
                             bound: int,
                             lo: int, hi: int,
                             finite_limit: FiniteLimit,
                             tested_sla_ref: str) -> UnboundedDebtReceipt:
        """The hunt succeeded: cap the unserved count and compute the
        consequence. The interval becomes bounded territory — the three-valued
        verdict on the trajectory defers to the finite engine."""
        if not tested_sla_ref:
            raise CircularEvidenceError(
                "a finite limit is accepted only with the tested SLA named "
                "— without it, circularity cannot be excluded; refusing")
        if finite_limit.evidence_ref == tested_sla_ref:
            raise CircularEvidenceError(
                f"finite-limit evidence {finite_limit.evidence_ref!r} IS the "
                f"SLA under test — the SLA being tested can never serve as "
                f"its own enforcement evidence; refusing")
        cap = finite_limit.max_unserved_rounds
        peak_upper = hi + cap
        if interval.must_end_with_service:
            final_debt: int | None = 0
            final_basis = ("terminal service S clears the counter; the "
                           "finite limit caps only the unserved count")
            assumptions = _MODEL_ASSUMPTIONS_USS + (
                f"Finite limit established via {finite_limit.source} "
                f"(evidence {finite_limit.evidence_ref}): at most {cap} "
                f"unserved rounds — the interval is bounded territory again.",
            )
        else:
            final_debt = None
            final_basis = ("no demonstrated exit; finite limit caps the "
                           "unserved count but not the final debt")
            assumptions = _MODEL_ASSUMPTIONS_U_STAR + (
                f"Finite limit established via {finite_limit.source} "
                f"(evidence {finite_limit.evidence_ref}): at most {cap} "
                f"unserved rounds.",
            )
        peak_basis = (f"finite limit {finite_limit.source}: peak in "
                      f"[{lo}, {peak_upper}]")
        if lo > bound:
            verdict, verdict_basis = (
                BREACH,
                f"peak lower bound {lo} > bound {bound}: every defensible "
                f"history's peak exceeds the bound (0-U history attains it)")
            defers_to = None
        elif peak_upper <= bound:
            verdict, verdict_basis = (
                NO_BREACH,
                f"peak upper bound {peak_upper} <= bound {bound}: no "
                f"defensible history's peak exceeds the bound — established "
                f"through the finite limit, never through the interval")
            defers_to = None
        else:
            verdict, verdict_basis = (
                UNRESOLVED,
                f"peak interval [{lo}, {peak_upper}] straddles bound {bound}: "
                f"the peak bound alone cannot settle it — the three-valued "
                f"verdict on the trajectory defers to the finite engine")
            defers_to = "D60"
        return UnboundedDebtReceipt(
            obligation_id=interval.obligation_id,
            bound=bound,
            entry_debt_lo=lo,
            entry_debt_hi=hi,
            final_debt=final_debt,
            final_debt_basis=final_basis,
            peak_status=FINITE_LIMIT_ESTABLISHED,
            peak_lower_bound=lo,
            peak_upper_bound=peak_upper,
            peak_basis=peak_basis,
            witness=None,
            finite_limit=finite_limit,
            verdict=verdict,
            verdict_basis=verdict_basis,
            defers_to=defers_to,
            model_assumptions=assumptions,
        )

    @staticmethod
    def _peak_verdict(lo: int, bound: int,
                      status: str) -> tuple[str, str]:
        """The verdict answers off the peak — never the final."""
        if lo > bound:
            return (BREACH,
                    f"peak lower bound {lo} > bound {bound}: every defensible "
                    f"history's peak exceeds the bound — proven on the peak, "
                    f"not on the final")
        return (UNRESOLVED,
                f"peak one-to-infinity above {lo} against bound {bound}: "
                f"breach histories exist (k = {bound - lo + 1} unserved "
                f"rounds peaks above the bound) and the 0-U history does not "
                f"breach — verdict held undetermined; unknown length, "
                f"unbounded debt, and proven violation are not interchanged")


def verify_compliance_claim(receipt: UnboundedDebtReceipt,
                            claimed_verdict: str,
                            evidence: dict) -> str:
    """The independent verifier: accepts or rejects a compliance claim
    against a receipt. Returns "ACCEPTED" or raises.

    evidence is a plain dict naming what the claim rests on, e.g.
    {"final_debt": 0} or {"finite_limit_source": ..., "max_unserved_rounds": ...}
    or {"peak_witness": {"entry_debt": lo, "unserved_rounds": 0}}.
    """
    if claimed_verdict not in VERDICTS:
        raise ClaimMismatchError(
            f"unknown claimed verdict {claimed_verdict!r} — not a verdict")
    if claimed_verdict == UNRESOLVED:
        # Holding undetermined is conservative and always consistent here.
        return "ACCEPTED"
    if claimed_verdict == NO_BREACH:
        if receipt.verdict != NO_BREACH:
            cites_peak = any(k in evidence for k in
                             ("peak_upper_bound", "finite_limit_source",
                              "peak_witness"))
            if not cites_peak:
                # The AER-LIVE-006 mutation: examined only the final debt,
                # declared compliance.
                raise FinalDebtOnlyClaimError(
                    f"claim cites {sorted(evidence)} — final-debt-only "
                    f"evidence cannot establish NO_BREACH over an unbounded "
                    f"interval: the peak is the controlling quantity, and a "
                    f"later service reset never erases a possible earlier "
                    f"breach; receipt verdict is {receipt.verdict}")
            raise PeakUnboundedClaimError(
                f"peak is {receipt.peak_status} (unbounded above "
                f"{receipt.peak_lower_bound}) — compliance is establishable "
                f"only through a finite limit, never through the unbounded "
                f"interval itself")
        # Receipt says NO_BREACH: the claim must point at the finite limit —
        # never at the interval.
        limit = receipt.finite_limit
        if (evidence.get("finite_limit_source") == limit.source
                and evidence.get("max_unserved_rounds")
                == limit.max_unserved_rounds
                and evidence.get("evidence_ref") == limit.evidence_ref):
            return "ACCEPTED"
        raise ClaimMismatchError(
            "a NO_BREACH claim must cite the establishing finite limit "
            f"(source, cap, evidence_ref) — got {sorted(evidence)}")
    # claimed BREACH
    if receipt.verdict != BREACH:
        raise ClaimMismatchError(
            f"receipt verdict is {receipt.verdict} — a BREACH claim needs a "
            f"BREACH receipt")
    witness = evidence.get("peak_witness") or {}
    if (witness.get("entry_debt") == receipt.entry_debt_lo
            and witness.get("unserved_rounds") == 0):
        return "ACCEPTED"
    raise ClaimMismatchError(
        "a BREACH claim must cite the peak witness (the 0-U history at "
        f"entry debt {receipt.entry_debt_lo}) — got {evidence!r}")
