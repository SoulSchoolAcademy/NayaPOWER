"""Kernel ACT pipeline: two-phase governed action execution.

Reference implementation of the ACT node contract's execution seam:

    PLAN -> re-resolve LAW -> EXECUTE

with a receipt emitted at every phase transition.

Phase 1 (PLAN): a governed LAW authority record is bound to the minimum
sufficient ActionPlan. The plan carries reversibility classification, the
expected outcome, and proof requirements. When several plan candidates are
offered, the winner is chosen by the canonical Value Calculus
evaluate_candidates() path — baseline-relative value, Pareto comparison,
interval dominance. There is no second decision engine here: quality alone
never selects; only positive conservative value on the Pareto frontier wins.

DO-NO-HARM ENFORCEMENT (safety floor): before any scoring, every candidate
is run through the calculus's gate_candidate hard gates with the LAW
scope-match threaded as authorized, so unknown hard-gate flags surface as
NEEDS_EVIDENCE instead of being masked as NEEDS_AUTHORITY. A candidate the
calculus verdicts PROHIBITED — hard violation, any explicit unsafe flag
(LAW/RIGHTS/PRIVACY/SAFETY = False), tail risk at or above policy
threshold, or distributional harm at or above policy maximum — can never
win and can never execute: harm is zero-valued, not optional. A candidate
carrying unresolved critical flags (HARD_GATE_UNKNOWN / UNKNOWN_LAW /
UNKNOWN_RIGHTS / UNKNOWN_PRIVACY / UNKNOWN_SAFETY) is likewise refused
with PLAN_SAFETY_UNKNOWN: unknown safety is never treated as safe.
Prohibited candidates are excluded from selection with their governing reasons
recorded as receipt evidence; if nothing admissible remains, planning is
refused with PLAN_SAFETY_PROHIBITED (all prohibited) or PLAN_SAFETY_UNKNOWN
(any unresolved critical flags). NEEDS_AUTHORITY routing continues to
be governed by the LAW authority record (the LAW node's seam, not this
one): this seam enforces the harm hard stops, nothing else is weakened.

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
from typing import Any, Callable, Mapping, Sequence

from kernel.memory_store import MemoryStore
from kernel.value_calculus import (
    NEEDS_EVIDENCE,
    PROHIBITED,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    evaluate_candidates,
    gate_candidate,
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
PLAN_SAFETY_UNKNOWN = "PLAN_SAFETY_UNKNOWN"
PLAN_VALUE_UNDEFINED = "PLAN_VALUE_UNDEFINED"
PLAN_BASELINE_AMBIGUOUS = "PLAN_BASELINE_AMBIGUOUS"
PLAN_NEEDS_EVIDENCE = "PLAN_NEEDS_EVIDENCE"
PLAN_NEEDS_AUTHORITY = "PLAN_NEEDS_AUTHORITY"

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
    verdict excludes the candidate from selection entirely, as does any
    verdict carrying unresolved critical flags (HARD_GATE_UNKNOWN /
    UNKNOWN_LAW / UNKNOWN_RIGHTS / UNKNOWN_PRIVACY / UNKNOWN_SAFETY) —
    unknown safety is never treated as safe.

    Value fields thread the canonical value calculus into selection:
    benefit/harm/cost/risk are REQUIRED (None is refused with
    PLAN_VALUE_UNDEFINED — the pipeline never silently zeroes value
    components, per the Zero Value Law). value_confidence carries
    per-component confidence for B/H/C/R; value_evidence_count carries
    the evidence count the calculus floors check. uncertainty_penalty and
    tail_penalty feed the conservative value interval. Exactly one
    candidate per plan may carry is_baseline=True (the explicit reference
    course for baseline-relative value); when none does, the pipeline
    synthesizes the do-nothing baseline.
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
    benefit: float | None = None
    harm: float | None = None
    cost: float | None = None
    risk: float | None = None
    value_confidence: dict = field(default_factory=dict)
    value_evidence_count: int = 0
    uncertainty_penalty: float = 0.0
    tail_penalty: float = 0.0
    is_baseline: bool = False


@dataclass(frozen=True)
class ActionPlan:
    plan_id: str
    action: str
    chosen: PlanCandidate
    authority: LawAuthority
    # ((candidate_id, Q, v_safe, delta_v), ...) — the math is visible:
    # quality, conservative value, and baseline-relative value per candidate.
    candidate_scores: tuple
    planned_at: float
    # Learning-loop stub (UD-01 trial harness / miscalibration recorder link):
    # what the outcome observer needs to close the loop.
    predicted_delta_v: float | None = None
    baseline_id: str | None = None
    observation_window: dict = field(default_factory=dict)


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
    # Learning-loop stub: carried from the plan so the outcome observer can
    # reconcile predicted vs actual value (UD-01 trial harness,
    # miscalibration recorder). None = not established (never silent zero).
    predicted_delta_v: float | None = None
    baseline_id: str | None = None
    observation_window: dict = field(default_factory=dict)


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


# Gate reasons that mark unresolved critical hard-gate flags. Any one of
# these on a candidate's gate verdict is a fail-closed refusal: unknown
# LAW/RIGHTS/PRIVACY/SAFETY is never treated as safe, and never masked.
_UNKNOWN_HARD_GATE_REASONS = (
    "HARD_GATE_UNKNOWN",
    "UNKNOWN_LAW",
    "UNKNOWN_RIGHTS",
    "UNKNOWN_PRIVACY",
    "UNKNOWN_SAFETY",
)


def _has_unknown_hard_gate(reasons: Sequence[str]) -> bool:
    """True if the gate verdict carries unresolved critical hard-gate flags."""
    return any(r in _UNKNOWN_HARD_GATE_REASONS for r in reasons)


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


# Pipeline stakes (low/medium/high) mapped conservatively onto the
# calculus stake order (low/high/consequential). "medium" maps up to
# "high": understating stakes is never allowed.
_STAKE_TO_CALCULUS = {"low": "low", "medium": "high", "high": "high"}

# Id of the synthesized do-nothing baseline when the caller supplies none.
SYNTH_BASELINE_ID = "baseline:current-course"


def _candidate_to_calculus(candidate: PlanCandidate, *,
                            authorized: bool = False) -> Candidate:
    """Map the plan seam onto the calculus contract, including the
    do-no-harm fields AND the evidence-backed value estimate. Nothing
    safety-relevant is dropped: harm, violations, tails and safety flags
    all reach gate_candidate. Nothing value-relevant is zeroed: benefit,
    harm, cost, risk, per-component confidence and evidence count all
    reach the PV estimate (Zero Value Law: unknown value is never
    silently recorded as zero — missing components are refused at plan
    time with PLAN_VALUE_UNDEFINED, before this conversion runs).

    `authorized` threads the LAW scope-match into the calculus. plan_action
    passes True once authority.scope == authority.action is verified, so the
    calculus's NEEDS_EVIDENCE hard-gate-unknown verdict becomes reachable
    in-pipeline instead of being masked as NEEDS_AUTHORITY [AUTHORITY_MISSING].
    The default False preserves the LAW-governed NEEDS_AUTHORITY path: the
    execution re-gate deliberately does not thread authority, so a
    hand-crafted plan still gates NEEDS_AUTHORITY [AUTHORITY_MISSING] and
    authority stays governed by the LAW re-resolution, not the safety seam.
    """
    return Candidate(
        candidate_id=candidate.candidate_id,
        quality=dict(candidate.quality),
        confidence=dict(candidate.confidence),
        pv=PVEstimate(
            B=candidate.benefit,
            H=candidate.harm,
            C=candidate.cost,
            R=candidate.risk,
            confidence=dict(candidate.value_confidence),
            evidence_count=candidate.value_evidence_count,
        ),
        stakes=_STAKE_TO_CALCULUS.get(candidate.stakes, "high"),
        reversible=candidate.reversibility == "REVERSIBLE",
        hard_violation=candidate.hard_violation,
        authorized=authorized,
        lawful=candidate.lawful,
        rights_safe=candidate.rights_safe,
        privacy_safe=candidate.privacy_safe,
        safety_safe=candidate.safety_safe,
        tails=tuple(candidate.tails),
        stakeholder_harms=dict(candidate.stakeholder_harms),
        uncertainty_penalty=candidate.uncertainty_penalty,
        tail_penalty=candidate.tail_penalty,
        is_baseline=candidate.is_baseline,
    )


def _synth_baseline() -> Candidate:
    """The explicit do-nothing baseline: the current course, valued at
    exactly zero BY DEFINITION (baseline-relative value of the reference
    against itself). It gates ADMISSIBLE by construction — all safety
    flags explicitly True, full confidence, one evidence unit — so it
    never tips the gate logic spuriously, and its v_safe is exactly 0,
    so it can never be selected (selection requires v_safe > 0).
    """
    full_conf = {d: 1.0 for d in (
        "objective_fit", "evidence_sufficiency", "applicability",
        "robustness", "reversibility", "blast_containment", "simplicity")}
    mid_quality = {d: 5.0 for d in full_conf}
    return Candidate(
        candidate_id=SYNTH_BASELINE_ID,
        quality=mid_quality,
        confidence=full_conf,
        pv=PVEstimate(B=0.0, H=0.0, C=0.0, R=0.0,
                      confidence={"B": 1.0, "H": 1.0, "C": 1.0, "R": 1.0},
                      evidence_count=1),
        stakes="low",
        reversible=True,
        authorized=True,
        human_authorized=True,
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        is_baseline=True,
    )


def _select_by_canonical_value(converted: Sequence[Candidate],
                                  baseline_id: str,
                                  profile: QualityProfile,
                                  risk_policy: RiskPolicy) -> dict:
    """Selection through the canonical evaluate_candidates() path.

    Baseline-relative value, Pareto comparison, interval dominance —
    there is no second decision engine. The winner is the highest
    conservative value (v_safe) on the Pareto frontier; quality alone
    never selects, and negative value never wins (v_safe > 0 required).
    """
    return evaluate_candidates(converted, baseline_id, profile, risk_policy)


def _format_ranking(evaluation: Mapping) -> tuple:
    """Human-readable ranking lines for the receipt: the math is visible."""
    lines = []
    for r in evaluation["rows"]:
        if r["is_baseline"]:
            continue
        lines.append(
            f"candidate {r['candidate_id']}: gate={r['gate']} "
            f"Q={r['q']['Q']:.2f} v_safe={r['v_safe']:+.2f} "
            f"delta_v={r['delta_v']:+.2f} "
            f"interval=[{r['v_low']:+.2f},{r['v_high']:+.2f}]"
            + (f" [{','.join(r['gate_reasons'])}]" if r["gate_reasons"] else "")
        )
    return tuple(lines)


def apply_retained_intelligence(
    *,
    memory_store: MemoryStore,
    policy_store: Any | None = None,
    situation: str,
    default_behavior: str,
    now: str | None = None,
) -> dict[str, Any]:
    """Bind retained memory to the authorized-apply decision seam.

    Canonical memory→action wire (learning-loop GAP-1): serves ACTIVE,
    integrity-verified records matching `situation` from the memory store —
    QUARANTINED records are never served, SUPERSEDED/DECAYED/ARCHIVED never
    surface silently (the store's fail-closed discipline) — and combines them
    with the behavior policy's advise() decision for the same situation.

    A record matches a situation when its provenance carries the same
    `situation` key (the capture contract for actionable records).

    Precedence: integrated lesson (policy store) > retained intelligence
    (memory store, strongest verification_weight first) > caller default.
    Every decision names its `source` ("lesson:<id>", "memory:<record_id>",
    "default") so before/after transcripts prove the behavioral delta.

    Retrieval is read-only (persist_touch=False): deciding must not mutate
    the store. Raises ValueError when the store or situation is missing
    (fail closed, decide nothing).
    """
    if memory_store is None:
        raise ValueError("memory_store_required")
    if policy_store is not None and not hasattr(policy_store, "advise"):
        raise ValueError("policy_store_invalid:advise_missing")
    if not str(situation or "").strip():
        raise ValueError("situation_required")
    situation = str(situation).strip()

    def _situation_matches(record: Any) -> bool:
        provenance = getattr(record, "provenance", None)
        return isinstance(provenance, dict) and str(
            provenance.get("situation") or ""
        ).strip() == situation

    served = memory_store.serve(_situation_matches, now=now, persist_touch=False)
    candidates = sorted(
        (record for record, _label in served.items),
        key=lambda r: (
            -float(getattr(r, "verification_weight", 0.0) or 0.0),
            str(getattr(r, "last_verified_at", "") or ""),
        ),
    )

    advised = (
        policy_store.advise(situation, default_behavior)
        if policy_store is not None
        else None
    )
    policy_version = advised.get("policy_version") if advised else None

    if advised is not None and advised.get("source", "default") != "default":
        return {
            "behavior": advised["behavior"],
            "source": advised["source"],
            "situation": situation,
            "policy_version": policy_version,
            "memory_record_id": None,
            "memory_records_considered": len(candidates),
            "via": "behavior_policy",
        }
    if candidates:
        top = candidates[0]
        return {
            "behavior": top.content,
            "source": f"memory:{top.record_id}",
            "situation": situation,
            "policy_version": policy_version,
            "memory_record_id": top.record_id,
            "memory_epistemic_state": top.epistemic_state,
            "memory_verification_weight": top.verification_weight,
            "memory_records_considered": len(candidates),
            "via": "memory_store",
        }
    return {
        "behavior": default_behavior,
        "source": "default",
        "situation": situation,
        "policy_version": policy_version,
        "memory_record_id": None,
        "memory_records_considered": 0,
        "via": "default",
    }


def plan_action(authority: LawAuthority,
                candidates: Sequence[PlanCandidate],
                profile: QualityProfile,
                *,
                now: float,
                risk_policy: RiskPolicy | None = None,
                observation_window: Mapping | None = None,
                ) -> tuple[ActionPlan | None, ActionReceipt]:
    """Phase 1: bind LAW authority to a minimum-sufficient plan.

    Returns (plan, receipt). On any refusal, plan is None and the receipt
    carries phase PLAN_REFUSED with the governing code. No execution happens
    here — planning never executes.

    Do-no-harm enforcement: every candidate is hard-gated through the
    calculus's gate_candidate BEFORE selection, with the LAW scope-match
    threaded as authorized=True so unknown hard-gate flags surface as
    NEEDS_EVIDENCE instead of being masked as NEEDS_AUTHORITY. PROHIBITED
    candidates are excluded and can never win or execute; candidates
    carrying unresolved critical flags (HARD_GATE_UNKNOWN / UNKNOWN_LAW /
    UNKNOWN_RIGHTS / UNKNOWN_PRIVACY / UNKNOWN_SAFETY) are likewise
    excluded — fail closed. The exclusion reasons are recorded as receipt
    evidence. When nothing admissible remains the plan is refused with
    PLAN_SAFETY_PROHIBITED (all prohibited) or PLAN_SAFETY_UNKNOWN
    (any unresolved critical flags). NEEDS_AUTHORITY verdicts remain
    governed by the LAW authority record (the LAW node's seam): this seam
    enforces the harm hard stops only, and weakens nothing.

    Value routing: every candidate must carry evidence-backed benefit,
    harm, cost and risk (missing components are refused with
    PLAN_VALUE_UNDEFINED — the pipeline never silently zeroes value).
    Selection runs through the canonical evaluate_candidates() path
    against an explicit baseline (caller-supplied, or the synthesized
    do-nothing baseline): baseline-relative value, Pareto comparison,
    interval dominance. Only positive conservative value on the Pareto
    frontier wins; quality alone never selects. When the canonical path
    yields no selection, planning is refused with PLAN_NEEDS_EVIDENCE
    (READ_MORE), PLAN_NEEDS_AUTHORITY (ASK), or PLAN_SAFETY_PROHIBITED
    (REFUSE).

    observation_window (optional mapping, e.g. {"status": "OPEN",
    "ends_at": ...}) is recorded on the plan and receipts as the
    learning-loop stub: the outcome observer needs the predicted delta,
    the baseline id, and the window to close the loop.
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

    # --- Value-evidence contract (Zero Value Law). Fail fast: a candidate
    # without evidence-backed benefit/harm/cost/risk cannot be valued, so
    # it cannot be selected. The pipeline never silently zeroes value
    # components — unknown value is refused, not defaulted.
    for c in candidates:
        components = (("benefit", c.benefit), ("harm", c.harm),
                      ("cost", c.cost), ("risk", c.risk))
        missing = [name for name, v in components if v is None]
        negative = [name for name, v in components
                    if v is not None and v < 0]
        if missing or negative:
            detail = "; ".join(
                [f"missing {n}" for n in missing]
                + [f"negative {n}" for n in negative])
            return refused(
                PLAN_VALUE_UNDEFINED,
                evidence=f"candidate {c.candidate_id} has no evidence-backed "
                         f"value estimate ({detail}); value components are "
                         f"required — unknown value is never zeroed.",
            )

    # --- Explicit baseline. Exactly one reference course per plan.
    flagged = [c for c in candidates if c.is_baseline]
    if len(flagged) > 1:
        return refused(
            PLAN_BASELINE_AMBIGUOUS,
            evidence="more than one candidate flagged is_baseline: "
                     + ", ".join(c.candidate_id for c in flagged),
        )
    baseline_id = flagged[0].candidate_id if flagged else SYNTH_BASELINE_ID

    # --- Do-no-harm hard gate (safety floor). Fail closed: a PROHIBITED
    # candidate gets zero value — it is excluded from selection entirely.
    # A candidate carrying unresolved critical hard-gate flags
    # (HARD_GATE_UNKNOWN / UNKNOWN_LAW / UNKNOWN_RIGHTS / UNKNOWN_PRIVACY /
    # UNKNOWN_SAFETY) is likewise excluded: unknown safety is never treated
    # as safe. Authority is threaded from the LAW scope-match verified above,
    # so the calculus's NEEDS_EVIDENCE unknown-flag verdict is reachable
    # instead of being masked as NEEDS_AUTHORITY [AUTHORITY_MISSING].
    risk = risk_policy if risk_policy is not None else RiskPolicy()
    # The baseline is the reference course, not a contender: it is never
    # pre-filtered and never selected. Only contenders face the gate.
    contenders = [c for c in candidates if not c.is_baseline]
    admissible: list[PlanCandidate] = []
    excluded: list[tuple[str, list[str]]] = []  # (candidate_id, gate reasons)
    excluded_unknown: list[tuple[str, list[str]]] = []
    for c in contenders:
        gate, reasons, _q = gate_candidate(
            _candidate_to_calculus(c, authorized=True), profile, risk)
        if gate == PROHIBITED:
            excluded.append((c.candidate_id, reasons))
        elif _has_unknown_hard_gate(reasons):
            excluded_unknown.append((c.candidate_id, reasons))
        else:
            admissible.append(c)
    if not admissible:
        detail = "; ".join(f"{cid} [{', '.join(rs)}]"
                           for cid, rs in excluded + excluded_unknown)
        if excluded_unknown:
            return refused(
                PLAN_SAFETY_UNKNOWN,
                evidence=f"all {len(contenders)} candidate(s) refused by the "
                         f"do-no-harm gate: unresolved critical safety flags "
                         f"(fail closed, unknown is not safe). {detail}",
            )
        return refused(
            PLAN_SAFETY_PROHIBITED,
            evidence=f"all {len(contenders)} candidate(s) PROHIBITED by the "
                     f"do-no-harm gate; nothing admissible to execute. {detail}",
        )
    gate_evidence = tuple(
        f"candidate {cid} EXCLUDED by do-no-harm gate: {', '.join(rs)}"
        for cid, rs in excluded
    )

    # --- Canonical selection. The full converted set (survivors plus the
    # explicit baseline) goes through evaluate_candidates(): the math
    # decides. Only ADMISSIBLE candidates with Q >= q_accept and positive
    # conservative value are eligible; the winner is the highest v_safe on
    # the Pareto frontier. High quality can never disguise negative value.
    converted_all = [_candidate_to_calculus(c, authorized=True)
                     for c in admissible]
    if flagged:
        converted_all.append(_candidate_to_calculus(flagged[0], authorized=True))
    else:
        converted_all.append(_synth_baseline())
    evaluation = _select_by_canonical_value(
        converted_all, baseline_id, profile, risk)
    ranking = _format_ranking(evaluation)

    selected_id = evaluation["selected"]
    if selected_id is None:
        # The canonical path yields no winner: refuse, naming the reason.
        # The math decided there is nothing worth doing yet.
        decision = evaluation["decision"]
        if decision == "ASK":
            return refused(
                PLAN_NEEDS_AUTHORITY,
                evidence=("canonical evaluation selected no candidate: "
                          "governance must decide (ASK). " + " ".join(ranking)),
            )
        if decision == "REFUSE":
            return refused(
                PLAN_SAFETY_PROHIBITED,
                evidence=("canonical evaluation refused all candidates. "
                          + " ".join(ranking)),
            )
        return refused(
            PLAN_NEEDS_EVIDENCE,
            evidence=("canonical evaluation selected no candidate: no "
                      "candidate clears the value/evidence bar (READ_MORE). "
                      + " ".join(ranking)),
        )

    by_id = {c.candidate_id: c for c in admissible}
    chosen = by_id[selected_id]
    sel_row = next(r for r in evaluation["rows"]
                   if r["candidate_id"] == selected_id)
    scores = tuple(
        (r["candidate_id"], round(r["q"]["Q"], 4),
         round(r["v_safe"], 4), round(r["delta_v"], 4))
        for r in evaluation["rows"] if not r["is_baseline"]
    )
    window = dict(observation_window or {})
    plan = ActionPlan(
        plan_id=plan_id, action=authority.action, chosen=chosen,
        authority=authority, candidate_scores=scores, planned_at=now,
        predicted_delta_v=sel_row["delta_v"],
        baseline_id=baseline_id,
        observation_window=window,
    )
    receipt = ActionReceipt(
        receipt_id=_new_id(), plan_id=plan_id, phase="PLAN_ACCEPTED",
        executed=False, outcome_verified=False, truth_state="UNKNOWN",
        evidence=gate_evidence + ranking + (
            f"selected {chosen.candidate_id} by canonical value ranking: "
            f"highest v_safe={sel_row['v_safe']:+.2f} on the Pareto frontier "
            f"(Q={sel_row['q']['Q']:.2f}, "
            f"interval=[{sel_row['v_low']:+.2f},{sel_row['v_high']:+.2f}]); "
            f"quality alone never selects",
        ),
        codes=(),
        expected_outcome=chosen.expected_outcome,
        predicted_delta_v=sel_row["delta_v"],
        baseline_id=baseline_id,
        observation_window=window,
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
                 risk_policy: RiskPolicy | None = None,
                 on_executed: Callable[[ActionPlan, ActionReceipt], None] | None = None) -> ActionReceipt:
    """Phase 2: re-resolve live LAW authority, re-verify the do-no-harm gate,
    then execute.

    re_resolve must return a FRESH LawAuthority read at execution time
    (SN-0493). If it returns None, or the fresh authority fails any time
    check, execution is refused and the executor is never called.

    on_executed is the post-execution hook seam (WO5b): it fires exactly once,
    after the EXECUTION_COMPLETED receipt is emitted to the ledger, with
    (plan, receipt). SELF wires kernel.self_integration.make_act_experience_hook
    here so every completed action is preserved as experience. Refused or
    failed executions never reach the hook — only a completed outcome is
    recordable experience.

    Do-no-harm enforcement (fail-closed): the chosen candidate is re-run
    through the calculus's gate_candidate at the last responsible moment,
    immediately before the executor fires. A plan hand-crafted outside
    plan_action — or a candidate whose safety status changed after planning
    — can never reach the executor while PROHIBITED: it is refused with
    PLAN_SAFETY_PROHIBITED. Unresolved critical hard-gate flags
    (HARD_GATE_UNKNOWN / UNKNOWN_LAW / UNKNOWN_RIGHTS / UNKNOWN_PRIVACY /
    UNKNOWN_SAFETY) are likewise refused with PLAN_SAFETY_UNKNOWN, and any
    other NEEDS_EVIDENCE verdict is refused with PLAN_NEEDS_EVIDENCE:
    insufficiently-evidenced candidates never reach the executor.
    NEEDS_AUTHORITY verdicts stay governed by the LAW authority record
    (the LAW node's seam); this seam enforces the harm hard stops only
    and weakens nothing. Pass the same profile (and risk policy) used at
    plan time so the verdict is a re-verification, not a re-derivation
    under different math.

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
    # refused here; the executor is never called. A candidate carrying
    # unresolved critical hard-gate flags (HARD_GATE_UNKNOWN / UNKNOWN_LAW /
    # UNKNOWN_RIGHTS / UNKNOWN_PRIVACY / UNKNOWN_SAFETY) is likewise refused:
    # unknown safety is never treated as safe.
    # Authority is deliberately NOT threaded here: the re-gate preserves the
    # documented LAW-governed NEEDS_AUTHORITY [AUTHORITY_MISSING] path for
    # hand-crafted plans (authority is enforced by the LAW re-resolution
    # above, not the safety seam). The unknown-flag refusal stands as
    # defense in depth for any verdict that does carry those reasons.
    risk = risk_policy if risk_policy is not None else RiskPolicy()
    gate, reasons, _q = gate_candidate(_candidate_to_calculus(plan.chosen), profile, risk)
    gate_evidence = (f"execution-time do-no-harm re-gate: candidate "
                     f"{plan.chosen.candidate_id} verdict {gate}"
                     + (f" [{', '.join(reasons)}]" if reasons else ""))
    if gate == PROHIBITED:
        return refused(PLAN_SAFETY_PROHIBITED, evidence=gate_evidence)
    if _has_unknown_hard_gate(reasons):
        return refused(PLAN_SAFETY_UNKNOWN, evidence=gate_evidence)
    # Defense in depth: an insufficiently-evidenced chosen candidate can
    # never reach the executor either. (With authority deliberately
    # unthreaded here, the live gate_candidate masks NEEDS_EVIDENCE as
    # NEEDS_AUTHORITY [AUTHORITY_MISSING]; this branch stands for any
    # verdict that does carry NEEDS_EVIDENCE.)
    if gate == NEEDS_EVIDENCE:
        return refused(PLAN_NEEDS_EVIDENCE, evidence=gate_evidence)

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

    completed = emit(ActionReceipt(
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
        predicted_delta_v=plan.predicted_delta_v,
        baseline_id=plan.baseline_id,
        observation_window=dict(plan.observation_window),
    ))
    if on_executed is not None:
        on_executed(plan, completed)
    return completed


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
        predicted_delta_v=receipt.predicted_delta_v,
        baseline_id=receipt.baseline_id,
        observation_window=dict(receipt.observation_window),
    )
