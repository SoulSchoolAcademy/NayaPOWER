"""Kernel ACT pipeline: two-phase governed action execution.

Reference implementation of the ACT node contract's execution seam:

    PLAN -> re-resolve LAW -> EXECUTE

with a receipt emitted at every phase transition.

Phase 1 (PLAN): a governed LAW authority record is bound to the minimum
sufficient ActionPlan. The plan carries reversibility classification, the
expected outcome, and proof requirements. When several plan candidates are
offered, the winner is chosen through the canonical Value Calculus seam
(kernel/value_calculus) — there is no second decision engine here; ties
break toward reversible, low-stakes candidates deterministically.

DO-NO-HARM ENFORCEMENT (safety floor): before any scoring, every candidate
is run through the calculus's gate_candidate hard gates. A candidate the
calculus verdicts PROHIBITED — hard violation, any explicit unsafe flag
(LAW/RIGHTS/PRIVACY/SAFETY = False), tail risk at or above policy
threshold, or distributional harm at or above policy maximum — can never
win and can never execute: harm is zero-valued, not optional. Prohibited
candidates are excluded from selection with their governing reasons
recorded as receipt evidence; if nothing admissible remains, planning is
refused with PLAN_SAFETY_PROHIBITED. NEEDS_AUTHORITY verdicts are refused
fail-closed with PLAN_SAFETY_NEEDS_AUTHORITY: the seam binds a LAW grant
but cannot observe the human authorization the calculus demands for
consequential/irreversible plans, and it cannot ASK — so it refuses
rather than absorbing the verdict into "admissible". NEEDS_EVIDENCE
reasons are recorded as evidence without blocking (quality gates, not
harm hard stops).

Phase 2 (EXECUTE): live LAW authority is re-resolved BEFORE execution
(SN-0493: decisions expire when the tip moves; the ACT contract requires
rereading live authority even when the LAW receipt remains fresh). Any
missing, malformed, future-dated, stale, or expired authority fails closed
with an EXECUTION_REFUSED receipt — nothing executes. An injected executor
performs the action; the pipeline records execution state throughout and
emits the final receipt.

Executor claims are NEVER trusted as verification: the receipt records the
executor's claim and the observed outcome separately, and truth_state stays
UNKNOWN until the VERIFY seam closes it via apply_verify_verdict.

The ReceiptLedger is a producer-side record of emitted receipts. It is not
an authority store and grants no authority.

Canonical constants:
    MAX_LAW_AGE_SECONDS = 900  (DOOR-AI apply_retained_intelligence)
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Callable, Sequence

from kernel.value_calculus import (
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    gate_candidate,
    score_quality,
)

# Canonical max LAW age for consequential AI actions (DOOR-AI, registry V1).
MAX_LAW_AGE_SECONDS = 900

# Execution refusal codes (fail-closed).
LAW_RECEIPT_TIME_INVALID = "LAW_RECEIPT_TIME_INVALID"
LAW_AUTHORITY_TIME_INVALID = "LAW_AUTHORITY_TIME_INVALID"
LAW_AUTHORITY_EXPIRED = "LAW_AUTHORITY_EXPIRED"
LAW_AUTHORITY_STALE = "LAW_AUTHORITY_STALE"
LAW_RE_RESOLUTION_UNAVAILABLE = "LAW_RE_RESOLUTION_UNAVAILABLE"
PLAN_UNAUTHORIZED_SCOPE = "PLAN_UNAUTHORIZED_SCOPE"
PLAN_NO_CANDIDATES = "PLAN_NO_CANDIDATES"
PLAN_OUTCOME_UNDEFINED = "PLAN_OUTCOME_UNDEFINED"
PLAN_PROOF_UNDEFINED = "PLAN_PROOF_UNDEFINED"
PLAN_CANDIDATE_MISMATCH = "PLAN_CANDIDATE_MISMATCH"
PLAN_SAFETY_PROHIBITED = "PLAN_SAFETY_PROHIBITED"
PLAN_SAFETY_NEEDS_AUTHORITY = "PLAN_SAFETY_NEEDS_AUTHORITY"

_REVERSIBLE_VALUES = ("REVERSIBLE", "IRREVERSIBLE", "UNKNOWN")
_STAKE_ORDER = {"low": 0, "medium": 1, "high": 2}


class LedgerFull(Exception):
    """ReceiptLedger reached its bound — fail loud, never silently drop."""


@dataclass(frozen=True)
class LawAuthority:
    """Governed LAW decision bound to an action.

    decided_at: epoch seconds of the LAW evaluation. Must be present,
    parseable (float), and no later than the current clock.
    expires_at: epoch seconds, or None for unbounded. An expiry at or
    before the current clock is expired (per the ACT contract).
    """
    action: str
    scope: str
    decided_at: float | None
    expires_at: float | None
    grant_id: str


@dataclass(frozen=True)
class PlanCandidate:
    """One way to carry out the action. quality/confidence follow the
    Value Calculus quality-dimension contract.

    Safety fields thread the calculus do-no-harm hard gates into the
    execution seam: hard_violation, the four explicit safety flags,
    tails, and stakeholder_harms. Defaults preserve today's behavior for
    clean candidates (no flags, no tails, no harms); any PROHIBITED
    verdict excludes the candidate from selection entirely.
    """
    candidate_id: str
    action: str
    description: str
    quality: dict
    confidence: dict
    reversibility: str  # REVERSIBLE | IRREVERSIBLE | UNKNOWN
    expected_outcome: str
    proof_requirements: tuple
    stakes: str = "low"
    hard_violation: bool = False
    lawful: bool | None = None
    rights_safe: bool | None = None
    privacy_safe: bool | None = None
    safety_safe: bool | None = None
    tails: tuple = ()
    stakeholder_harms: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ActionPlan:
    plan_id: str
    action: str
    chosen: PlanCandidate
    authority: LawAuthority
    candidate_scores: tuple  # ((candidate_id, Q), ...) — the math is visible
    planned_at: float


@dataclass(frozen=True)
class ActionReceipt:
    receipt_id: str
    plan_id: str
    phase: str  # PLAN_ACCEPTED | PLAN_REFUSED | EXECUTION_STARTED |
                # EXECUTION_COMPLETED | EXECUTION_FAILED | EXECUTION_REFUSED
    executed: bool
    outcome_verified: bool  # only the VERIFY seam may set True
    truth_state: str        # UNKNOWN | BLOCKED (VERIFIED only via verdict)
    evidence: tuple = ()
    codes: tuple = ()
    observed_outcome: str | None = None
    expected_outcome: str | None = None


class ReceiptLedger:
    """Append-only, bounded producer-side receipt record."""

    def __init__(self, max_entries: int = 10_000):
        if max_entries < 1:
            raise ValueError("max_entries must be >= 1")
        self._max = max_entries
        self._entries: list[ActionReceipt] = []

    def append(self, receipt: ActionReceipt) -> None:
        if len(self._entries) >= self._max:
            raise LedgerFull(f"ledger bound reached ({self._max}); refusing silent drop")
        self._entries.append(receipt)

    def entries(self) -> tuple:
        return tuple(self._entries)


def _new_id() -> str:
    return uuid.uuid4().hex


def _validate_law_time(authority: LawAuthority, now: float,
                       max_law_age_seconds: float) -> tuple[str, ...]:
    """Return refusal codes for the authority's time fields; empty = valid."""
    decided = authority.decided_at
    if decided is None or not isinstance(decided, (int, float)):
        return (LAW_RECEIPT_TIME_INVALID,)
    if decided > now:
        return (LAW_RECEIPT_TIME_INVALID,)
    expires = authority.expires_at
    if expires is not None:
        if not isinstance(expires, (int, float)):
            return (LAW_AUTHORITY_TIME_INVALID,)
        if expires <= now:
            return (LAW_AUTHORITY_EXPIRED,)
    if now - decided > max_law_age_seconds:
        return (LAW_AUTHORITY_STALE,)
    return ()


def _candidate_to_calculus(candidate: PlanCandidate) -> Candidate:
    """Map the plan seam onto the calculus contract, including the
    do-no-harm fields. Nothing safety-relevant is dropped: harm,
    violations, tails and safety flags all reach gate_candidate.

    authorized=True is mapped, not assumed: both seams that call this
    function only run with a bound, scope-verified, time-valid
    LawAuthority — that grant IS the authority the calculus channel
    demands, so the always-on AUTHORITY_MISSING verdict is retired and
    the remaining NEEDS_AUTHORITY verdicts (consequential/irreversible
    plans, governance conflicts) are real signals. human_authorized is
    deliberately left False: the LawAuthority record carries no human
    signal, so the seam cannot claim one. When the LAW node carries
    human authorization, map it here.
    """
    return Candidate(
        candidate_id=candidate.candidate_id,
        quality=dict(candidate.quality),
        confidence=dict(candidate.confidence),
        pv=PVEstimate(B=0.0, H=0.0, C=0.0, R=0.0, confidence={}),
        authorized=True,
        stakes=candidate.stakes if candidate.stakes in _STAKE_ORDER else "high",
        reversible=candidate.reversibility == "REVERSIBLE",
        hard_violation=candidate.hard_violation,
        lawful=candidate.lawful,
        rights_safe=candidate.rights_safe,
        privacy_safe=candidate.privacy_safe,
        safety_safe=candidate.safety_safe,
        tails=tuple(candidate.tails),
        stakeholder_harms=dict(candidate.stakeholder_harms),
    )


def _select_minimum_sufficient(candidates: Sequence[PlanCandidate],
                               profile: QualityProfile) -> tuple[PlanCandidate, tuple]:
    scored = []
    for c in candidates:
        q = score_quality(_candidate_to_calculus(c), profile)["Q"]
        scored.append((c, q))
    scored.sort(key=lambda item: (
        -item[1],                                            # highest Q first
        0 if item[0].reversibility == "REVERSIBLE" else 1,   # prefer reversible
        _STAKE_ORDER.get(item[0].stakes, 2),                # prefer lower stakes
        item[0].candidate_id,                                # deterministic
    ))
    winner = scored[0][0]
    scores = tuple((c.candidate_id, round(q, 4)) for c, q in scored)
    return winner, scores


def plan_action(authority: LawAuthority,
                candidates: Sequence[PlanCandidate],
                profile: QualityProfile,
                *,
                now: float,
                risk_policy: RiskPolicy | None = None,
                ) -> tuple[ActionPlan | None, ActionReceipt]:
    """Phase 1: bind LAW authority to a minimum-sufficient plan.

    Returns (plan, receipt). On any refusal, plan is None and the receipt
    carries phase PLAN_REFUSED with the governing code. No execution happens
    here — planning never executes.

    Do-no-harm enforcement: every candidate is hard-gated through the
    calculus's gate_candidate BEFORE selection. PROHIBITED candidates are
    excluded and can never win or execute; the exclusion reasons are
    recorded as receipt evidence. NEEDS_AUTHORITY verdicts are REFUSED
    fail-closed with PLAN_SAFETY_NEEDS_AUTHORITY: this seam binds a LAW
    grant but cannot observe the human authorization the calculus
    demands for consequential/irreversible plans, and it cannot ASK —
    so it refuses rather than absorbing the verdict into "admissible".
    When nothing admissible remains the plan is refused with
    PLAN_SAFETY_PROHIBITED. NEEDS_EVIDENCE reasons are recorded as
    evidence but do not block selection (quality gates, not harm).
    """
    plan_id = _new_id()

    def refused(*codes: str, evidence: str = "") -> tuple[None, ActionReceipt]:
        return None, ActionReceipt(
            receipt_id=_new_id(), plan_id=plan_id, phase="PLAN_REFUSED",
            executed=False, outcome_verified=False, truth_state="BLOCKED",
            evidence=(evidence or f"plan refused at {now}: {', '.join(codes)}",),
            codes=codes,
        )

    if authority.scope != authority.action:
        return refused(PLAN_UNAUTHORIZED_SCOPE)
    if not candidates:
        return refused(PLAN_NO_CANDIDATES)
    for c in candidates:
        if c.action != authority.action:
            return refused(PLAN_CANDIDATE_MISMATCH)
        if c.reversibility not in _REVERSIBLE_VALUES:
            return refused(PLAN_CANDIDATE_MISMATCH)
        if not c.expected_outcome:
            return refused(PLAN_OUTCOME_UNDEFINED)
        if not c.proof_requirements:
            return refused(PLAN_PROOF_UNDEFINED)

    # --- Do-no-harm hard gate (safety floor). Fail closed: a PROHIBITED
    # candidate gets zero value — it is excluded from selection entirely.
    # A NEEDS_AUTHORITY candidate refuses the whole plan: the seam binds a
    # LAW grant but cannot observe the human authorization the calculus
    # demands for consequential/irreversible plans, so absorbing it into
    # "admissible" would be fail-open. NEEDS_EVIDENCE verdicts are recorded
    # as evidence but do not block (quality gates, not harm hard stops).
    risk = risk_policy if risk_policy is not None else RiskPolicy()
    admissible: list[PlanCandidate] = []
    excluded: list[tuple[str, list[str]]] = []  # (candidate_id, gate reasons)
    needs_auth: list[tuple[str, list[str]]] = []  # (candidate_id, gate reasons)
    evidence_notes: list[str] = []
    for c in candidates:
        gate, reasons, _q = gate_candidate(_candidate_to_calculus(c), profile, risk)
        if gate == PROHIBITED:
            excluded.append((c.candidate_id, reasons))
        elif gate == NEEDS_AUTHORITY:
            needs_auth.append((c.candidate_id, reasons))
        else:
            if gate == NEEDS_EVIDENCE and reasons:
                evidence_notes.append(
                    f"candidate {c.candidate_id} NEEDS_EVIDENCE: {', '.join(reasons)}"
                )
            admissible.append(c)
    if needs_auth:
        detail = "; ".join(f"{cid} [{', '.join(rs)}]" for cid, rs in needs_auth)
        return refused(
            PLAN_SAFETY_NEEDS_AUTHORITY,
            evidence=f"plan refused: {len(needs_auth)} candidate(s) need authority "
                     f"this seam cannot supply (fail-closed; the LAW grant binds "
                     f"scope, not human authorization for consequential/irreversible "
                     f"plans). {detail}",
        )
    if not admissible:
        detail = "; ".join(f"{cid} [{', '.join(rs)}]" for cid, rs in excluded)
        return refused(
            PLAN_SAFETY_PROHIBITED,
            evidence=f"all {len(candidates)} candidate(s) PROHIBITED by the "
                     f"do-no-harm gate; nothing admissible to execute. {detail}",
        )
    gate_evidence = tuple(evidence_notes) + tuple(
        f"candidate {cid} EXCLUDED by do-no-harm gate: {', '.join(rs)}"
        for cid, rs in excluded
    )

    chosen, scores = _select_minimum_sufficient(admissible, profile)
    plan = ActionPlan(
        plan_id=plan_id, action=authority.action, chosen=chosen,
        authority=authority, candidate_scores=scores, planned_at=now,
    )
    receipt = ActionReceipt(
        receipt_id=_new_id(), plan_id=plan_id, phase="PLAN_ACCEPTED",
        executed=False, outcome_verified=False, truth_state="UNKNOWN",
        evidence=gate_evidence
        + tuple(
            f"candidate {cid} scored Q={q}" for cid, q in scores
        ) + (f"selected {chosen.candidate_id} as minimum sufficient",),
        codes=(),
        expected_outcome=chosen.expected_outcome,
    )
    return plan, receipt


def execute_plan(plan: ActionPlan,
                 *,
                 executor: Callable[[ActionPlan], str],
                 re_resolve: Callable[[], LawAuthority | None],
                 now: float,
                 profile: QualityProfile,
                 max_law_age_seconds: float = MAX_LAW_AGE_SECONDS,
                 ledger: ReceiptLedger | None = None,
                 risk_policy: RiskPolicy | None = None) -> ActionReceipt:
    """Phase 2: re-resolve live LAW authority, re-verify the do-no-harm gate,
    then execute.

    re_resolve must return a FRESH LawAuthority read at execution time
    (SN-0493). If it returns None, or the fresh authority fails any time
    check, execution is refused and the executor is never called.

    Do-no-harm enforcement (fail-closed): the chosen candidate is re-run
    through the calculus's gate_candidate at the last responsible moment,
    immediately before the executor fires. A plan hand-crafted outside
    plan_action — or a candidate whose safety status changed after planning
    — can never reach the executor while PROHIBITED: it is refused with
    PLAN_SAFETY_PROHIBITED. A NEEDS_AUTHORITY verdict is likewise refused
    with PLAN_SAFETY_NEEDS_AUTHORITY: the seam cannot observe the human
    authorization the calculus demands for consequential/irreversible
    plans, and it cannot ASK, so it refuses rather than executing on a
    bare grant. LAW refusals keep LAW codes and precede the re-gate.
    Pass the same profile (and risk policy) used at plan time so the
    verdict is a re-verification, not a re-derivation under different math.

    Every phase transition is appended to ledger when provided.
    """
    def emit(receipt: ActionReceipt) -> ActionReceipt:
        if ledger is not None:
            ledger.append(receipt)
        return receipt

    started = ActionReceipt(
        receipt_id=_new_id(), plan_id=plan.plan_id, phase="EXECUTION_STARTED",
        executed=False, outcome_verified=False, truth_state="UNKNOWN",
        evidence=(f"execution started at {now}; re-resolving live authority",),
        codes=(),
        expected_outcome=plan.chosen.expected_outcome,
    )
    emit(started)

    def refused(*codes: str, evidence: str = "") -> ActionReceipt:
        return emit(ActionReceipt(
            receipt_id=_new_id(), plan_id=plan.plan_id, phase="EXECUTION_REFUSED",
            executed=False, outcome_verified=False, truth_state="BLOCKED",
            evidence=(evidence or f"execution refused at {now}: {', '.join(codes)}",),
            codes=codes,
            expected_outcome=plan.chosen.expected_outcome,
        ))

    fresh = re_resolve()
    if fresh is None:
        return refused(LAW_RE_RESOLUTION_UNAVAILABLE,
                       evidence="live LAW re-resolution returned no authority; refusing (SN-0493)")
    if fresh.action != plan.action or fresh.scope != plan.action:
        return refused(PLAN_UNAUTHORIZED_SCOPE,
                       evidence="re-resolved authority does not cover the planned action")
    time_codes = _validate_law_time(fresh, now, max_law_age_seconds)
    if time_codes:
        return refused(*time_codes)

    # --- Execution-time do-no-harm re-gate (safety floor). Fail closed:
    # the gate is re-verified at the last responsible moment, immediately
    # before the executor fires. A PROHIBITED chosen candidate — whether
    # hand-crafted outside plan_action or changed after planning — is
    # refused here; the executor is never called. A NEEDS_AUTHORITY verdict
    # (consequential/irreversible with no observable human authorization)
    # is refused here for the same reason: this seam cannot supply the
    # demanded authority, so it fails closed.
    risk = risk_policy if risk_policy is not None else RiskPolicy()
    gate, reasons, _q = gate_candidate(_candidate_to_calculus(plan.chosen), profile, risk)
    gate_evidence = (f"execution-time do-no-harm re-gate: candidate "
                     f"{plan.chosen.candidate_id} verdict {gate}"
                     + (f" [{', '.join(reasons)}]" if reasons else ""))
    if gate == PROHIBITED:
        return refused(PLAN_SAFETY_PROHIBITED, evidence=gate_evidence)
    if gate == NEEDS_AUTHORITY:
        return refused(PLAN_SAFETY_NEEDS_AUTHORITY, evidence=gate_evidence)

    try:
        observed = executor(plan)
    except Exception as exc:  # noqa: BLE001 — failure is evidence, not a crash
        return emit(ActionReceipt(
            receipt_id=_new_id(), plan_id=plan.plan_id, phase="EXECUTION_FAILED",
            executed=False, outcome_verified=False, truth_state="UNKNOWN",
            evidence=(f"executor raised {type(exc).__name__}: {exc}; no blind retry",),
            codes=("EXECUTION_FAILED",),
            expected_outcome=plan.chosen.expected_outcome,
        ))

    return emit(ActionReceipt(
        receipt_id=_new_id(), plan_id=plan.plan_id, phase="EXECUTION_COMPLETED",
        executed=True, outcome_verified=False, truth_state="UNKNOWN",
        evidence=(
            gate_evidence,
            f"executor completed; observed outcome recorded; "
            f"executor claim NOT trusted as verification — awaiting VERIFY verdict",
        ),
        codes=(),
        observed_outcome=observed,
        expected_outcome=plan.chosen.expected_outcome,
    ))


def apply_verify_verdict(receipt: ActionReceipt, *, verified: bool,
                         evidence: str) -> ActionReceipt:
    """VERIFY-seam handoff: close a completed receipt with an independent verdict.

    Returns a NEW receipt object with the same receipt_id — the receipt is
    closed, not replaced. Only the VERIFY seam may call this; the pipeline
    itself never sets outcome_verified=True.
    """
    if receipt.phase != "EXECUTION_COMPLETED":
        raise ValueError(f"verdict applies only to EXECUTION_COMPLETED receipts, got {receipt.phase}")
    return ActionReceipt(
        receipt_id=receipt.receipt_id, plan_id=receipt.plan_id, phase=receipt.phase,
        executed=receipt.executed, outcome_verified=verified,
        truth_state="VERIFIED" if verified else "BLOCKED",
        evidence=receipt.evidence + (f"VERIFY verdict: {evidence}",),
        codes=receipt.codes,
        observed_outcome=receipt.observed_outcome,
        expected_outcome=receipt.expected_outcome,
    )
