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
is run through the calculus's gate_candidate hard gates with the LAW
scope-match threaded as authorized, so unknown hard-gate flags surface as
NEEDS_EVIDENCE instead of being masked as NEEDS_AUTHORITY. A candidate the
calculus verdicts PROHIBITED — hard violation, any explicit unsafe flag
(LAW/RIGHTS/PRIVACY/SAFETY = False), tail risk at or above policy
threshold, or distributional harm at or above policy maximum — can never
win and can never execute: harm is zero-valued, not optional. A candidate
the calculus verdicts NEEDS_EVIDENCE — critical safety evidence unresolved —
is likewise excluded: it can never win and can never execute until the
evidence is supplied. A candidate carrying unresolved critical flags
(HARD_GATE_UNKNOWN / UNKNOWN_LAW / UNKNOWN_RIGHTS / UNKNOWN_PRIVACY /
UNKNOWN_SAFETY) is likewise refused: unknown safety is never treated as
safe. Prohibited candidates are excluded from selection with their governing
reasons recorded as receipt evidence; if nothing admissible remains, planning
is refused with PLAN_SAFETY_PROHIBITED (hard violations),
PLAN_SAFETY_UNKNOWN (unresolved critical flags), or PLAN_SAFETY_NEEDS_EVIDENCE
(other unresolved critical safety evidence). NEEDS_AUTHORITY routing continues to
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
from typing import Any, Callable, Sequence

from kernel.memory_store import MemoryStore
from kernel.value_calculus import (
    ACT,
    ASK,
    NEEDS_EVIDENCE,
    PROHIBITED,
    QUALITY_DIMENSIONS,
    READ_MORE,
    REFUSE,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    evaluate_candidates,
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
PLAN_SAFETY_NEEDS_EVIDENCE = "PLAN_SAFETY_NEEDS_EVIDENCE"
PLAN_SAFETY_UNKNOWN = "PLAN_SAFETY_UNKNOWN"
PLAN_VALUE_UNPROVEN = "PLAN_VALUE_UNPROVEN"

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

    Value fields carry the candidate's V2.1 value-calculus estimate
    (benefit, harm, cost, risk + per-component confidence + evidence
    count). Defaults mark the estimate as NOT SUPPLIED: unknown value is
    never silently zero (Zero Value Law). A candidate without a supplied
    estimate (pv_evidence_count == 0, empty pv_confidence) cannot clear
    the calculus evidence/confidence floors and gates NEEDS_EVIDENCE
    until real data is provided. Set is_baseline=True on at most one
    candidate to declare the explicit baseline; when none is declared the
    pipeline synthesizes the do-nothing baseline.
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
    # --- V2.1 value estimate (see docstring) ---
    benefit: float = 0.0
    harm: float = 0.0
    cost: float = 0.0
    risk: float = 0.0
    pv_confidence: dict = field(default_factory=dict)
    pv_evidence_count: int = 0
    uncertainty_penalty: float = 0.0
    tail_penalty: float = 0.0
    is_baseline: bool = False


@dataclass(frozen=True)
class ActionPlan:
    plan_id: str
    action: str
    chosen: PlanCandidate
    authority: LawAuthority
    candidate_scores: tuple  # ((candidate_id, Q, v_safe), ...) — the math is visible
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


def _candidate_to_calculus(candidate: PlanCandidate, *,
                            authorized: bool = False) -> Candidate:
    """Map the plan seam onto the calculus contract, including the
    do-no-harm fields. Nothing safety-relevant is dropped: harm,
    violations, tails and safety flags all reach gate_candidate.

    `authorized` threads the LAW scope-match into the calculus. plan_action
    passes True once authority.scope == authority.action is verified, so the
    calculus's NEEDS_EVIDENCE hard-gate-unknown verdict becomes reachable
    in-pipeline instead of being masked as NEEDS_AUTHORITY [AUTHORITY_MISSING].
    The default False preserves the LAW-governed NEEDS_AUTHORITY path: the
    execution re-gate deliberately does not thread authority, so a
    hand-crafted plan still gates NEEDS_AUTHORITY [AUTHORITY_MISSING] and
    authority stays governed by the LAW re-resolution, not the safety seam.

    Value fields pass through verbatim: benefit/harm/cost/risk, per-component
    confidence, evidence count, and penalties. When the candidate carries no
    supplied estimate (pv_evidence_count == 0, empty pv_confidence) the
    calculus sees an unevidenced estimate — the gate returns NEEDS_EVIDENCE
    via the evidence/confidence floors. Unknown value is never silently zero.
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
            confidence=dict(candidate.pv_confidence),
            evidence_count=candidate.pv_evidence_count,
        ),
        uncertainty_penalty=candidate.uncertainty_penalty,
        tail_penalty=candidate.tail_penalty,
        is_baseline=candidate.is_baseline,
        stakes=candidate.stakes if candidate.stakes in _STAKE_ORDER else "high",
        reversible=candidate.reversibility == "REVERSIBLE",
        hard_violation=candidate.hard_violation,
        authorized=authorized,
        lawful=candidate.lawful,
        rights_safe=candidate.rights_safe,
        privacy_safe=candidate.privacy_safe,
        safety_safe=candidate.safety_safe,
        tails=tuple(candidate.tails),
        stakeholder_harms=dict(candidate.stakeholder_harms),
    )


_BASELINE_CANDIDATE_ID = "__baseline_do_nothing__"


def _ensure_baseline(candidates: Sequence[Candidate]) -> tuple[list[Candidate], str]:
    """Ensure exactly one explicit baseline for evaluate_candidates().

    Uses the caller's declared baseline (is_baseline=True) when present;
    otherwise synthesizes the do-nothing baseline. The synthesized baseline
    carries zero value BY DEFINITION — comparing the current course against
    itself ("baseline zero" per the Zero Value Law: definitional, not
    empirical). It gates ADMISSIBLE so it never pollutes the evaluator's
    evidence accounting, and it can never win (v_safe == 0 is not > 0).
    """
    baselines = [c for c in candidates if c.is_baseline]
    if len(baselines) > 1:
        raise ValueError("at most one baseline candidate")
    if baselines:
        return list(candidates), baselines[0].candidate_id
    baseline = Candidate(
        candidate_id=_BASELINE_CANDIDATE_ID,
        quality={d: 5.0 for d in QUALITY_DIMENSIONS},
        confidence={d: 1.0 for d in QUALITY_DIMENSIONS},
        pv=PVEstimate(
            B=0.0, H=0.0, C=0.0, R=0.0,
            confidence={"B": 1.0, "H": 1.0, "C": 1.0, "R": 1.0},
            evidence_count=1,
        ),
        authorized=True,
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        stakes="low",
        reversible=True,
        is_baseline=True,
    )
    return [baseline] + list(candidates), _BASELINE_CANDIDATE_ID


def _select_via_value_calculus(
    candidates: Sequence[PlanCandidate],
    profile: QualityProfile,
    risk_policy: RiskPolicy,
) -> tuple[PlanCandidate | None, dict]:
    """Route candidate selection through the canonical evaluate_candidates().

    This is the single decision seam: value (baseline-relative, conservative)
    determines the winner, not quality score alone. A high-Q candidate with
    negative v_safe cannot win; a candidate with unsupplied value evidence
    never reaches this function (it gates NEEDS_EVIDENCE upstream).

    Returns (winner_or_None, evaluation). The evaluation is the raw
    evaluate_candidates() result. A None winner means the calculus selected
    nothing (REFUSE, or READ_MORE with no positive-value candidate) — the
    caller must refuse planning, never fall back to quality-only ranking.
    """
    calculus_candidates = [
        _candidate_to_calculus(c, authorized=True) for c in candidates
    ]
    calculus_candidates, baseline_id = _ensure_baseline(calculus_candidates)
    evaluation = evaluate_candidates(
        calculus_candidates,
        baseline_id=baseline_id,
        profile=profile,
        risk_policy=risk_policy,
    )
    selected_id = evaluation["selected"]
    if selected_id is None:
        return None, evaluation
    by_id = {c.candidate_id: c for c in candidates}
    winner = by_id.get(selected_id)
    # The baseline can never be selected (v_safe == 0 fails the > 0
    # eligibility floor); a None here is a calculus contract violation.
    if winner is None:
        raise ValueError(
            f"evaluate_candidates selected unknown candidate {selected_id!r}"
        )
    return winner, evaluation


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
                ) -> tuple[ActionPlan | None, ActionReceipt]:
    """Phase 1: bind LAW authority to a minimum-sufficient plan.

    Returns (plan, receipt). On any refusal, plan is None and the receipt
    carries phase PLAN_REFUSED with the governing code. No execution happens
    here — planning never executes.

    Do-no-harm enforcement: every candidate is hard-gated through the
    calculus's gate_candidate BEFORE selection, with the LAW scope-match
    threaded as authorized=True so unknown hard-gate flags surface as
    NEEDS_EVIDENCE instead of being masked as NEEDS_AUTHORITY. PROHIBITED
    and NEEDS_EVIDENCE candidates are excluded and can never win or execute;
    candidates carrying unresolved critical flags (HARD_GATE_UNKNOWN /
    UNKNOWN_LAW / UNKNOWN_RIGHTS / UNKNOWN_PRIVACY / UNKNOWN_SAFETY) are
    likewise excluded — fail closed. The exclusion reasons are recorded as
    receipt evidence. When nothing admissible remains the plan is refused with
    PLAN_SAFETY_PROHIBITED (hard violations), PLAN_SAFETY_UNKNOWN
    (unresolved critical flags), or PLAN_SAFETY_NEEDS_EVIDENCE (other
    unresolved critical safety evidence). NEEDS_AUTHORITY verdicts remain
    governed by the LAW authority record (the LAW node's seam): this seam
    enforces the harm hard stops only, and weakens nothing.
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
    # A NEEDS_EVIDENCE candidate is likewise excluded: unresolved critical
    # safety evidence must never reach selection or execution. A candidate
    # carrying unresolved critical hard-gate flags (HARD_GATE_UNKNOWN /
    # UNKNOWN_LAW / UNKNOWN_RIGHTS / UNKNOWN_PRIVACY / UNKNOWN_SAFETY) is
    # likewise excluded: unknown safety is never treated as safe. Authority
    # is threaded from the LAW scope-match verified above, so the calculus's
    # NEEDS_EVIDENCE unknown-flag verdict is reachable instead of being
    # masked as NEEDS_AUTHORITY [AUTHORITY_MISSING].
    risk = risk_policy if risk_policy is not None else RiskPolicy()
    admissible: list[PlanCandidate] = []
    excluded: list[tuple[str, str, list[str]]] = []  # (candidate_id, gate verdict, gate reasons)
    for c in candidates:
        gate, reasons, _q = gate_candidate(
            _candidate_to_calculus(c, authorized=True), profile, risk)
        if gate in (PROHIBITED, NEEDS_EVIDENCE):
            excluded.append((c.candidate_id, gate, reasons))
        else:
            admissible.append(c)
    if not admissible:
        detail = "; ".join(f"{cid} [{verdict}: {', '.join(rs)}]" for cid, verdict, rs in excluded)
        has_prohibited = any(verdict == PROHIBITED for _, verdict, _ in excluded)
        has_unknown = any(_has_unknown_hard_gate(rs) for _, _, rs in excluded)
        if has_prohibited and has_unknown:
            return refused(
                PLAN_SAFETY_PROHIBITED, PLAN_SAFETY_UNKNOWN,
                evidence=f"all {len(candidates)} candidate(s) refused by the "
                         f"do-no-harm gate: hard violations present AND unresolved "
                         f"critical safety flags (fail closed, unknown is not safe). "
                         f"{detail}",
            )
        if has_prohibited:
            return refused(
                PLAN_SAFETY_PROHIBITED,
                evidence=f"all {len(candidates)} candidate(s) PROHIBITED by the "
                         f"do-no-harm gate; nothing admissible to execute. {detail}",
            )
        if has_unknown:
            return refused(
                PLAN_SAFETY_UNKNOWN,
                evidence=f"all {len(candidates)} candidate(s) refused by the "
                         f"do-no-harm gate: unresolved critical safety flags "
                         f"(fail closed, unknown is not safe). {detail}",
            )
        return refused(
            PLAN_SAFETY_NEEDS_EVIDENCE,
            evidence=f"all {len(candidates)} candidate(s) NEEDS_EVIDENCE by the "
                     f"do-no-harm gate; critical safety evidence unresolved, "
                     f"nothing admissible to execute. {detail}",
        )
    gate_evidence = tuple(
        f"candidate {cid} EXCLUDED by do-no-harm gate [{verdict}]: {', '.join(rs)}"
        for cid, verdict, rs in excluded
    )

    # --- Canonical value-calculus selection. The winner is determined by
    # evaluate_candidates(): baseline-relative conservative value (v_safe),
    # not quality score alone. A high-Q candidate with negative value cannot
    # win. When the calculus selects nothing, planning is refused — there is
    # no quality-only fallback.
    winner, evaluation = _select_via_value_calculus(admissible, profile, risk)
    decision = evaluation["decision"]
    value_rows = tuple(
        f"candidate {r['candidate_id']}: gate={r['gate']} "
        f"Q={r['q']['Q']:.2f} delta_v={r['delta_v']:.2f} v_safe={r['v_safe']:.2f}"
        + (" [BASELINE]" if r["is_baseline"] else "")
        for r in evaluation["rows"]
    )
    if winner is None:
        if decision == REFUSE:
            return refused(
                PLAN_SAFETY_PROHIBITED,
                evidence="canonical value calculus refused selection: "
                         "all non-baseline candidates PROHIBITED. "
                         + " ".join(value_rows),
            )
        return refused(
            PLAN_VALUE_UNPROVEN,
            evidence="canonical value calculus selected no candidate "
                     f"(decision={decision}): no admissible candidate demonstrates "
                     "positive conservative value vs. the do-nothing baseline; "
                     "value is unproven, not zero — supply evidence. "
                     + " ".join(value_rows),
        )
    scores = tuple(
        (r["candidate_id"], round(r["q"]["Q"], 4), round(r["v_safe"], 4))
        for r in evaluation["rows"] if not r["is_baseline"]
    )
    decision_note = (
        f"canonical evaluate_candidates decision={decision}; "
        + (
            "LAW authority governs the authorized action"
            if decision in (ASK, READ_MORE) else
            "value-confident autonomous selection"
        )
    )
    chosen = winner
    plan = ActionPlan(
        plan_id=plan_id, action=authority.action, chosen=chosen,
        authority=authority, candidate_scores=scores, planned_at=now,
    )
    receipt = ActionReceipt(
        receipt_id=_new_id(), plan_id=plan_id, phase="PLAN_ACCEPTED",
        executed=False, outcome_verified=False, truth_state="UNKNOWN",
        evidence=gate_evidence
        + value_rows
        + (f"selected {chosen.candidate_id} via canonical value calculus",
           decision_note),
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
    — can never reach the executor while PROHIBITED or NEEDS_EVIDENCE: it is
    refused with PLAN_SAFETY_PROHIBITED, PLAN_SAFETY_UNKNOWN (unresolved
    critical hard-gate flags), or PLAN_SAFETY_NEEDS_EVIDENCE respectively.
    NEEDS_AUTHORITY verdicts stay governed by the
    LAW authority record (the LAW node's seam); this seam enforces the harm
    hard stops only and weakens nothing. Pass the same profile (and risk
    policy) used at plan time so the verdict is a re-verification, not a
    re-derivation under different math.
    and weakens nothing. Pass the same profile (and risk policy) used at
    plan time so the verdict is a re-verification, not a re-derivation
    under different math.
>>>>>>> naya4/unknown-safety

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
    # refused here; the executor is never called. A NEEDS_EVIDENCE chosen
    # candidate is likewise refused: unresolved critical safety evidence
    # must never reach the executor. A candidate carrying unresolved critical
    # hard-gate flags (HARD_GATE_UNKNOWN / UNKNOWN_LAW / UNKNOWN_RIGHTS /
    # UNKNOWN_PRIVACY / UNKNOWN_SAFETY) is likewise refused: unknown safety
    # is never treated as safe.
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
    if gate == NEEDS_EVIDENCE:
        return refused(PLAN_SAFETY_NEEDS_EVIDENCE, evidence=gate_evidence)

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
    )
