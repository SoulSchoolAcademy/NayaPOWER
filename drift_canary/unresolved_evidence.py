"""D59 / AER-LIVE-4: Governing Unresolved Eligibility Evidence.

The uncertainty-preservation law: missing, contradictory, stale, or
unverifiable eligibility records are unresolved evidence obligations.
Unknown eligibility is neither proven ineligibility nor a fairness
violation. Preserve every compatible history, reconstruct the missing
evidence, derive only conclusions supported across those histories.
Reconstruction deadlines may escalate — never manufacture proof,
authority, or completion.

The gap it closes: D58 (eligibility_proof.py) yields UNDETERMINED verdicts
that "trigger an evidence-recovery obligation" — but nothing governed that
obligation. An UNDETERMINED round left a hole in every fairness-debt
computation: a single debt number cannot hold uncertainty, so any system
that collapsed the hole to a number was manufacturing a conclusion. This
module is the governance D58's recovery obligation was missing.

The mechanism, in one paragraph: each round carries a D58 three-valued
verdict plus its specific defect reason. For assessment, every
UNDETERMINED round is completed BOTH ways (eligible / ineligible) —
the compatible histories — and fairness debt is evolved per history with
the FairnessLedger rule (eligible + adequate service -> 0; eligible +
inadequate -> +1; ineligible -> unchanged). The public conclusion is
three-valued over the debt RANGE: every history breaches -> BREACH; no
history breaches -> NO_BREACH; otherwise UNRESOLVED. Stronger surrounding
evidence can therefore settle a disputed conclusion without ever
recovering the missing record. Each UNDETERMINED round spawns a
reconstruction obligation with its own attempt budget AND its own
fairness contract for the repair work itself, so "can't prove starvation
because the logs are missing" can never excuse not repairing the logs.
Exhaust the budget or starve the repair -> ESCALATED with the history
preserved, inventing neither innocence nor guilt.

Composes with (additive only — nothing here modifies them):
  eligibility_proof.py — EligibilityReceipt (the verdicts this module
                governs), EligibilityProver (re-run on reconstruction),
                Evidence, TaintedOriginError (the false-ineligibility
                mutation is caught here, not manufactured around).
  fairness.py — FairnessContract (BOUNDED: the bound + capacity basis),
                the ledger debt-evolution rule this module replays per
                history. This module never writes to a FairnessLedger.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT, or
any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Mapping

from drift_canary.eligibility_proof import (
    COMPONENTS,
    ELIGIBLE,
    INELIGIBLE,
    UNDETERMINED,
    VERDICTS,
    EligibilityProver,
    EligibilityReceipt,
    Evidence,
    UnknownComponentError,
)
from drift_canary.fairness import FairnessContract

# ---------------------------------------------------------------------------
# 1. Defect kinds: WHY a round is unresolved. (D59 registration comment
#    6102368579: "missing, contradictory, stale, or unverifiable".)
# ---------------------------------------------------------------------------
MISSING = "MISSING"                # the record was never produced
CONTRADICTORY = "CONTRADICTORY"    # two sources disagree; neither wins
STALE = "STALE"                    # evidence older than its validity window
UNVERIFIABLE = "UNVERIFIABLE"      # record exists but cannot be checked
DEFECT_KINDS = (MISSING, CONTRADICTORY, STALE, UNVERIFIABLE)

# Breach conclusions: three-valued over the debt range. UNRESOLVED is not a
# soft NO_BREACH.
BREACH = "BREACH"
NO_BREACH = "NO_BREACH"
UNRESOLVED = "UNRESOLVED"
BREACH_VERDICTS = (BREACH, NO_BREACH, UNRESOLVED)

# Reconstruction-obligation states.
RECON_OPEN = "OPEN"
RECON_SETTLED = "SETTLED"
RECON_ESCALATED = "ESCALATED"

# Escalation reasons. Neither invents innocence nor guilt.
BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
REPAIR_STARVED = "REPAIR_STARVED"

# Fail-closed cap: 2^12 histories. Beyond this the module refuses rather
# than sampling — a sampled range is a manufactured range.
MAX_UNRESOLVED_ROUNDS = 12


class UnresolvedEvidenceError(Exception):
    """Base for fail-closed unresolved-evidence errors."""


class HistorySpaceTooLargeError(UnresolvedEvidenceError):
    """Too many unresolved rounds to enumerate honestly. Fail closed."""


class UnknownObligationError(UnresolvedEvidenceError):
    """Assessment requested for an obligation with no registered rounds."""


class DuplicateRoundError(UnresolvedEvidenceError):
    """Two rounds registered for the same obligation + round_seq."""


class ReconstructionStateError(UnresolvedEvidenceError):
    """Illegal reconstruction transition (attempt on settled/escalated, ...)."""


class UnboundedContractError(UnresolvedEvidenceError):
    """Breach assessment needs a BOUNDED contract. Fail closed."""


@dataclass(frozen=True)
class ComponentDefect:
    """The specific defect reason one unknown component carries.

    The undetermined verdict never travels alone: every UNKNOWN component
    names WHY it is unknown, so a later reconstructor knows what to repair
    (re-fetch a missing log vs adjudicate two disagreeing sources are
    different repairs).
    """
    component: str
    kind: str
    detail: str

    def __post_init__(self):
        assert self.component in COMPONENTS, f"bad component: {self.component}"
        assert self.kind in DEFECT_KINDS, f"bad defect kind: {self.kind}"
        assert self.detail, "a defect needs a detail note"


@dataclass(frozen=True)
class RoundRecord:
    """One scheduling round for one obligation, as the verifier left it.

    adequate_service is the COMPLETE service history (D59's case stipulates
    it is known). It must be a real bool — a missing service outcome is a
    different unknown and this module refuses to guess it.
    """
    round_seq: int
    obligation_id: str
    verdict: str
    adequate_service: bool
    defects: tuple = ()                          # ComponentDefect per unknown
    receipt: EligibilityReceipt | None = None    # the D58 receipt, if any

    def __post_init__(self):
        assert self.verdict in VERDICTS, f"bad verdict: {self.verdict}"
        assert isinstance(self.adequate_service, bool), (
            f"adequate_service must be a known bool, got {self.adequate_service!r} "
            "— unknown service outcomes are not eligibility unknowns")
        assert self.obligation_id, "round needs an obligation id"
        if self.receipt is not None:
            assert isinstance(self.receipt, EligibilityReceipt), "receipt type"
            assert self.receipt.verdict == self.verdict, "receipt/verdict mismatch"
            assert self.receipt.round_seq == self.round_seq, "receipt/seq mismatch"
        if self.verdict == UNDETERMINED:
            assert self.defects, "UNDETERMINED must carry its defect reason(s)"
            for d in self.defects:
                assert isinstance(d, ComponentDefect), "defect type"
            if self.receipt is not None:
                defect_components = {d.component for d in self.defects}
                assert defect_components == set(self.receipt.unknown), (
                    "defects must name exactly the receipt's unknown components")
        else:
            assert not self.defects, "settled verdicts carry no defects"


@dataclass(frozen=True)
class BreachAssessment:
    """The three-valued public conclusion for one obligation.

    debt_min/debt_max is the debt RANGE across every compatible history —
    a single debt number cannot hold uncertainty. breach_witness /
    clearance_witness name the completions attaining the extremes, so the
    conclusion is auditable. Completions live only inside the assessment;
    nothing here asserts any single completion as fact.
    """
    obligation_id: str
    bound: int
    verdict: str
    debt_min: int
    debt_max: int
    histories_examined: int
    unresolved_rounds: tuple
    breach_witness: tuple | None       # ((round_seq, eligible), ...) attaining debt_max
    clearance_witness: tuple | None   # ((round_seq, eligible), ...) attaining debt_min

    def __post_init__(self):
        assert self.verdict in BREACH_VERDICTS, f"bad verdict: {self.verdict}"
        assert 0 <= self.debt_min <= self.debt_max, "inverted debt range"
        if self.verdict == BREACH:
            assert self.debt_min > self.bound, "BREACH needs every history over the bound"
            assert self.breach_witness is not None
        if self.verdict == NO_BREACH:
            assert self.debt_max <= self.bound, "NO_BREACH needs no history over the bound"
            assert self.clearance_witness is not None
        if self.verdict == UNRESOLVED:
            assert self.debt_min <= self.bound < self.debt_max, "UNRESOLVED needs a straddling range"


def _debt_after(debt: int, eligible: bool, adequate_service: bool) -> int:
    """One history step. Mirrors FairnessLedger.record_round exactly."""
    if not eligible:
        return debt
    if adequate_service:
        return 0
    return debt + 1


@dataclass
class ReconstructionObligation:
    """The independent obligation to repair one unresolved round.

    D59: "Reconstruction itself becomes an independent obligation with its
    own fairness contract." The repair work is scheduled work — if the
    repair is starved (repair debt over its own bound), that starvation is
    VISIBLE as escalation, never a silent excuse.

    attempt() merges fresh verifier evidence over the original receipt's
    components and re-runs the D58 prover. Tainted origins raise
    TaintedOriginError — the false-ineligibility mutation (settling via the
    scheduler's own flag) is caught, not laundered.
    """
    repair_obligation_id: str
    target_obligation_id: str
    round_seq: int
    missing: tuple                      # components to recover
    budget_attempts: int
    repair_bound: int                   # fairness bound for the repair work
    _target_receipt: EligibilityReceipt = field(repr=False)
    attempts_used: int = 0
    repair_debt: int = 0
    status: str = RECON_OPEN
    escalation_reason: str | None = None
    settled_receipt: EligibilityReceipt | None = None

    def __post_init__(self):
        assert self._target_receipt.verdict == UNDETERMINED, "reconstruct only unresolved rounds"
        assert set(self.missing) == set(self._target_receipt.unknown), (
            "missing must name exactly the round's unknown components")
        assert self.budget_attempts > 0, "a reconstruction with no budget is not an obligation"
        assert self.repair_bound > 0, "the repair's fairness contract needs a bound"

    def attempt(self, new_evidence: Mapping[str, Evidence]) -> EligibilityReceipt:
        """One reconstruction attempt. Returns the re-proven receipt.

        Fresh evidence merges OVER the original components; anything not
        re-supplied keeps its original (possibly UNKNOWN) state. A still-
        UNDETERMINED receipt consumes budget and accrues repair debt.
        """
        if self.status != RECON_OPEN:
            raise ReconstructionStateError(
                f"attempt on {self.status} reconstruction {self.repair_obligation_id} "
                "— settled/escalated obligations take no more attempts")
        if not isinstance(new_evidence, Mapping):
            raise ReconstructionStateError("new_evidence must be a component -> Evidence mapping")
        unknown_keys = [k for k in new_evidence if k not in COMPONENTS]
        if unknown_keys:
            raise UnknownComponentError(
                f"reconstruction supplied components outside the six: {unknown_keys} "
                "— fail closed, nothing merged, no budget consumed")

        old_components = dict(self._target_receipt.components)
        merged = {c: new_evidence.get(c, old_components[c]) for c in COMPONENTS}
        prover = EligibilityProver(merged)   # unknown components / tainted origins raise here
        receipt = prover.prove(
            self._target_receipt.opportunity_id,
            self.target_obligation_id,
            self.round_seq,
            scheduler_flag=None,             # reconstruction never re-admits the flag
        )
        self.attempts_used += 1

        if receipt.verdict != UNDETERMINED:
            self.status = RECON_SETTLED
            self.settled_receipt = receipt
            self.repair_debt = 0
            return receipt

        # Still unresolved: the attempt did not repair the round.
        self.repair_debt += 1
        if self.repair_debt > self.repair_bound:
            self._escalate(REPAIR_STARVED)
        elif self.attempts_used >= self.budget_attempts:
            self._escalate(BUDGET_EXHAUSTED)
        return receipt

    def _escalate(self, reason: str) -> None:
        self.status = RECON_ESCALATED
        self.escalation_reason = reason

    def settled_round_record(self) -> RoundRecord:
        """The settled replacement round. Only callable after SETTLED."""
        if self.status != RECON_SETTLED or self.settled_receipt is None:
            raise ReconstructionStateError(
                "no settled receipt — an open/escalated reconstruction "
                "manufactures no round")
        r = self.settled_receipt
        return RoundRecord(
            round_seq=r.round_seq,
            obligation_id=r.obligation_id,
            verdict=r.verdict,
            adequate_service=self._target_receipt_adequate_service(),
            receipt=r,
        )

    def _target_receipt_adequate_service(self) -> bool:
        # Service history is complete and immutable; the settled round keeps
        # the original round's service outcome. Stored at open time.
        return self._service_outcome

    def set_service_outcome(self, adequate_service: bool) -> None:
        """Called by the governor at open time (service history is fixed)."""
        assert isinstance(adequate_service, bool)
        self._service_outcome = adequate_service


class UnresolvedEvidenceGovernor:
    """Holds rounds per obligation, assesses breach over compatible
    histories, and owns reconstruction obligations.

    The governor never asserts a completion as fact: there is no method
    that returns "round r was eligible". Settled rounds enter only via
    apply_settlement(), which requires a D58 receipt from a reconstruction
    attempt — never a bare boolean.
    """

    def __init__(self):
        self._rounds: dict[str, dict[int, RoundRecord]] = {}
        self._reconstructions: dict[str, ReconstructionObligation] = {}

    # -- registration ----------------------------------------------------
    def register_round(self, record: RoundRecord) -> None:
        seqs = self._rounds.setdefault(record.obligation_id, {})
        if record.round_seq in seqs:
            raise DuplicateRoundError(
                f"round {record.round_seq} already registered for {record.obligation_id}")
        seqs[record.round_seq] = record

    # -- assessment ------------------------------------------------------
    def assess(self, obligation_id: str, contract: FairnessContract) -> BreachAssessment:
        """Three-valued breach verdict over every compatible history."""
        if contract.standard != "BOUNDED":
            raise UnboundedContractError(
                f"breach assessment needs a BOUNDED contract, got {contract.standard}")
        seqs = self._rounds.get(obligation_id)
        if not seqs:
            raise UnknownObligationError(
                f"no rounds registered for {obligation_id} — no evidence, no verdict")
        rounds = [seqs[s] for s in sorted(seqs)]
        bound = contract.service_bound_rounds

        unresolved = [r for r in rounds if r.verdict == UNDETERMINED]
        if len(unresolved) > MAX_UNRESOLVED_ROUNDS:
            raise HistorySpaceTooLargeError(
                f"{len(unresolved)} unresolved rounds > cap {MAX_UNRESOLVED_ROUNDS} "
                "— refusing to sample; narrow the window and re-assess")

        histories = self._enumerate(rounds)
        debts = [self._final_debt(rounds, h) for h in histories]
        debt_min, debt_max = min(debts), max(debts)

        if debt_min > bound:
            verdict = BREACH
        elif debt_max <= bound:
            verdict = NO_BREACH
        else:
            verdict = UNRESOLVED

        breach_witness = histories[debts.index(debt_max)] if verdict != NO_BREACH else None
        clearance_witness = histories[debts.index(debt_min)] if verdict != BREACH else None
        return BreachAssessment(
            obligation_id=obligation_id,
            bound=bound,
            verdict=verdict,
            debt_min=debt_min,
            debt_max=debt_max,
            histories_examined=len(histories),
            unresolved_rounds=tuple(r.round_seq for r in unresolved),
            breach_witness=breach_witness,
            clearance_witness=clearance_witness,
        )

    @staticmethod
    def _enumerate(rounds: list[RoundRecord]) -> list[tuple]:
        """Every compatible history: ((round_seq, eligible_bool), ...)."""
        unresolved_idx = [i for i, r in enumerate(rounds) if r.verdict == UNDETERMINED]
        histories = []
        for bits in product((False, True), repeat=len(unresolved_idx)):
            completion = {i: b for i, b in zip(unresolved_idx, bits)}
            histories.append(tuple(
                (r.round_seq, completion[i] if r.verdict == UNDETERMINED
                 else (r.verdict == ELIGIBLE))
                for i, r in enumerate(rounds)
            ))
        return histories

    @staticmethod
    def _final_debt(rounds: list[RoundRecord], history: tuple) -> int:
        debt = 0
        for record, (_, eligible) in zip(rounds, history):
            debt = _debt_after(debt, eligible, record.adequate_service)
        return debt

    # -- reconstruction --------------------------------------------------
    def open_reconstruction(self, obligation_id: str, round_seq: int,
                            budget_attempts: int = 3,
                            repair_bound: int = 2) -> ReconstructionObligation:
        """Open the independent repair obligation for one unresolved round."""
        seqs = self._rounds.get(obligation_id, {})
        record = seqs.get(round_seq)
        if record is None or record.verdict != UNDETERMINED:
            raise ReconstructionStateError(
                f"round {round_seq} of {obligation_id} is not an unresolved round")
        if record.receipt is None:
            raise ReconstructionStateError(
                "reconstruction needs the original D58 receipt to merge against")
        repair_oid = f"reconstruct:{obligation_id}:round-{round_seq}"
        existing = self._reconstructions.get(repair_oid)
        if existing is not None and existing.status == RECON_OPEN:
            raise ReconstructionStateError(
                f"reconstruction {repair_oid} already open")
        recon = ReconstructionObligation(
            repair_obligation_id=repair_oid,
            target_obligation_id=obligation_id,
            round_seq=round_seq,
            missing=tuple(record.receipt.unknown),
            budget_attempts=budget_attempts,
            repair_bound=repair_bound,
            _target_receipt=record.receipt,
        )
        recon.set_service_outcome(record.adequate_service)
        self._reconstructions[repair_oid] = recon
        return recon

    def get_reconstruction(self, repair_obligation_id: str) -> ReconstructionObligation:
        try:
            return self._reconstructions[repair_obligation_id]
        except KeyError:
            raise ReconstructionStateError(
                f"unknown reconstruction {repair_obligation_id}") from None

    def apply_settlement(self, repair_obligation_id: str) -> RoundRecord:
        """Swap the settled round in. Requires a SETTLED reconstruction."""
        recon = self.get_reconstruction(repair_obligation_id)
        settled = recon.settled_round_record()   # raises unless SETTLED
        self._rounds[settled.obligation_id][settled.round_seq] = settled
        return settled

    def open_reconstructions(self) -> list:
        return [r for r in self._reconstructions.values() if r.status == RECON_OPEN]
