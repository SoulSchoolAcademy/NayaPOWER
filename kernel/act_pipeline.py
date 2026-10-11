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
win and can never execute: harm is zero-valued, not optional. A candidate
the calculus verdicts NEEDS_EVIDENCE — critical safety evidence unresolved —
is likewise excluded: it can never win and can never execute until the
evidence is supplied. Prohibited candidates are excluded from selection with
their governing reasons recorded as receipt evidence; if nothing admissible
remains, planning is refused with PLAN_SAFETY_PROHIBITED (or
PLAN_SAFETY_NEEDS_EVIDENCE when the blockers are evidence gaps, not hard
violations). NEEDS_AUTHORITY routing continues to
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

import re
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

from kernel.memory_store import MemoryStore
from kernel.protocol.typed_action import (
    ADMISSIBLE as LAW11_ADMISSIBLE,
    INHERENTLY_PROHIBITED_OPERATIONS,
    IRREVERSIBLE as LAW11_IRREVERSIBLE,
    NEEDS_AUTHORITY as LAW11_NEEDS_AUTHORITY,
    NEEDS_EVIDENCE as LAW11_NEEDS_EVIDENCE,
    OPERATION_CAPTURE,
    OPERATION_DELETE,
    OPERATION_DEPLOY,
    OPERATION_EXECUTE,
    OPERATION_GRANT,
    OPERATION_MERGE,
    OPERATION_MIGRATE,
    OPERATION_READ,
    OPERATION_WRITE,
    PROHIBITED as LAW11_PROHIBITED,
    REVERSIBLE as LAW11_REVERSIBLE,
    REVERSIBLE_CONDITIONAL as LAW11_CONDITIONAL,
    TypedAction,
    execution_door_check,
    law11_gate,
)
from kernel.value_calculus import (
    ACT,
    ASK,
    NEEDS_EVIDENCE,
    PROHIBITED,
    READ_MORE,
    REFUSE,
    QUALITY_DIMENSIONS,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    evaluate_candidates,
    gate_candidate,
    score_quality,
)
from kernel.protocol.conflict_resolution import (
    VERDICT_PROHIBITED as CR_PROHIBITED,
    VERDICT_WORSENING as CR_WORSENING,
    VERDICT_PENDING_WINDOW as CR_PENDING,
    VERDICT_INCONCLUSIVE as CR_INCONCLUSIVE,
    COMPARE_DOMINATES,
    COMPARE_INCOMPARABLE,
    COMPARE_UNKNOWN,
    COMPARE_PROHIBITED,
    assess_no_worse_off,
    check_pareto_improvement,
    check_resolve_before_trade,
    assess_comparability,
)

# Canonical max LAW age for consequential AI actions (DOOR-AI, registry V1).
MAX_LAW_AGE_SECONDS = 900

# Execution refusal codes (fail-closed).
LAW_RECEIPT_TIME_INVALID = "LAW_RECEIPT_TIME_INVALID"
LAW_AUTHORITY_TIME_INVALID = "LAW_AUTHORITY_TIME_INVALID"
LAW_AUTHORITY_EXPIRED = "LAW_AUTHORITY_EXPIRED"
LAW_AUTHORITY_STALE = "LAW_AUTHORITY_STALE"
LAW_AUTHORITY_PROOF_STALE = "LAW_AUTHORITY_PROOF_STALE"  # Law 12: change-based expiry
LAW_RE_RESOLUTION_UNAVAILABLE = "LAW_RE_RESOLUTION_UNAVAILABLE"
PLAN_UNAUTHORIZED_SCOPE = "PLAN_UNAUTHORIZED_SCOPE"
PLAN_NO_CANDIDATES = "PLAN_NO_CANDIDATES"
PLAN_OUTCOME_UNDEFINED = "PLAN_OUTCOME_UNDEFINED"
PLAN_PROOF_UNDEFINED = "PLAN_PROOF_UNDEFINED"
PLAN_CANDIDATE_MISMATCH = "PLAN_CANDIDATE_MISMATCH"
PLAN_SAFETY_PROHIBITED = "PLAN_SAFETY_PROHIBITED"
PLAN_SAFETY_NEEDS_EVIDENCE = "PLAN_SAFETY_NEEDS_EVIDENCE"
PLAN_LAW11_NEEDS_AUTHORITY = "PLAN_LAW11_NEEDS_AUTHORITY"
PLAN_VALUE_INSUFFICIENT = "PLAN_VALUE_INSUFFICIENT"
PLAN_NEEDS_HUMAN_JUDGMENT = "PLAN_NEEDS_HUMAN_JUDGMENT"

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
    # Value estimate fields (Zero Value Law): evidence-backed benefit, harm,
    # cost, risk for the canonical value calculus. All default to None/empty,
    # meaning UNMEASURED — not zero. A candidate without value evidence cannot
    # win on value; the calculus gate verdicts NEEDS_EVIDENCE. Callers that
    # want value-based selection must supply these with real evidence.
    value_benefit: float | None = None
    value_harm: float | None = None
    value_cost: float | None = None
    value_risk: float | None = None
    value_confidence: dict = field(default_factory=dict)  # per-component B/H/C/R in [0,1]
    value_evidence_count: int = 0
    # Conflict Resolution Engine (Law of One): governed impact matrix for
    # per-group/per-dimension/per-horizon no-worse-off assessment.
    # None = not provided (phase skipped, existing behavior preserved).
    # When present, the candidate must pass the no-worse-off test and
    # anti-laundering safeguards before value scoring.
    impact_matrix: object | None = None
    # Resolve Before Trade: machine receipt showing alternative designs were
    # considered. Required when the candidate has material adverse effects.
    # None = not provided; the invariant is checked only when the impact
    # matrix shows material adverse effects (fail closed to NEEDS_EVIDENCE).
    design_search_record: object | None = None
    # Law 11 v2 (Uncertainty Handler): structured harm assessments for
    # uncertain/asymmetric/delayed/difficult-to-measure harms.
    # Tuple of HarmAssessment objects (from kernel.protocol.harm_assessment).
    # Empty = not provided (phase skipped). When present, each assessment
    # is evaluated; PROHIBITED/NEEDS_EVIDENCE/NEEDS_AUTHORITY excludes
    # the candidate.
    harm_assessments: tuple = ()


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
    do-no-harm fields and the evidence-backed value estimate.

    Nothing safety-relevant is dropped: harm, violations, tails and safety
    flags all reach gate_candidate.

    Value (Zero Value Law): when the caller supplies evidence-backed
    value_benefit/harm/cost/risk + confidence + evidence_count, those reach
    the calculus as the PVEstimate. When absent, the value is UNMEASURED —
    not zero. The PVEstimate carries placeholder zeros, but evidence_count=0
    and empty confidence force the calculus gate to verdict NEEDS_EVIDENCE,
    so unmeasured value can never determine a winner. Null is not zero.

    authorized=True: the LAW authority record (checked at plan level via
    scope matching) is the authority seam, not the per-candidate flag.
    This preserves the documented architecture: "NEEDS_AUTHORITY routing
    continues to be governed by the LAW authority record."
    """
    if (candidate.value_benefit is not None and candidate.value_harm is not None
            and candidate.value_cost is not None and candidate.value_risk is not None):
        pv = PVEstimate(
            B=candidate.value_benefit,
            H=candidate.value_harm,
            C=candidate.value_cost,
            R=candidate.value_risk,
            confidence=dict(candidate.value_confidence),
            evidence_count=candidate.value_evidence_count,
        )
    else:
        # UNMEASURED value: placeholder zeros that the gate must catch.
        # evidence_count=0 + empty confidence => NEEDS_EVIDENCE, never ADMISSIBLE.
        pv = PVEstimate(B=0.0, H=0.0, C=0.0, R=0.0, confidence={},
                        evidence_count=0)
    return Candidate(
        candidate_id=candidate.candidate_id,
        quality=dict(candidate.quality),
        confidence=dict(candidate.confidence),
        pv=pv,
        stakes=candidate.stakes if candidate.stakes in _STAKE_ORDER else "high",
        reversible=candidate.reversibility == "REVERSIBLE",
        hard_violation=candidate.hard_violation,
        lawful=candidate.lawful,
        rights_safe=candidate.rights_safe,
        privacy_safe=candidate.privacy_safe,
        safety_safe=candidate.safety_safe,
        tails=tuple(candidate.tails),
        stakeholder_harms=dict(candidate.stakeholder_harms),
        authorized=True,  # LAW record governs authority at plan level
    )


BASELINE_CANDIDATE_ID = "__baseline_do_nothing__"


# --- Law 11 typed-action mapping -------------------------------------------
# The Law 11 gate reasons about TypedActions (what is being DONE), not about
# PlanCandidates. This seam maps the pipeline's candidate representation onto
# the typed-action contract. The mapping is explicit and auditable; the
# free-text description is carried for audit only and NEVER influences the
# verdict (the gate reads typed fields, not words).
#
# Fail-closed: anything the mapping cannot determine stays unknown (None),
# and the Law 11 gate verdicts NEEDS_EVIDENCE on unknown safety dimensions
# rather than silently passing.

_OPERATION_KEYWORDS = (
    (OPERATION_DEPLOY, ("deploy",)),
    (OPERATION_MIGRATE, ("migrate",)),
    (OPERATION_DELETE, ("delete", "destroy")),
    (OPERATION_MERGE, ("merge",)),
    (OPERATION_GRANT, ("grant", "authorize", "permission")),
    (OPERATION_CAPTURE, ("capture", "smart_note", "learn")),
    (OPERATION_WRITE, ("write", "update", "apply", "modify")),
    (OPERATION_READ, ("read", "fetch", "retrieve", "query")),
)


# Character substitutions used to evade exact-string matching.
# Maps leet-speak and lookalike characters to their canonical letters.
_LEET_TRANSLATION = str.maketrans({
    "1": "i", "!": "i", "|": "i",
    "0": "o",
    "3": "e",
    "4": "a", "@": "a",
    "5": "s", "$": "s",
    "7": "t", "+": "t",
    "8": "b",
    "9": "g",
})


def _normalize_action_text(action: str) -> str:
    """Normalize free-text action names for operation inference.

    Collapses separator variations (hyphen/space/dot/slash/colon become
    underscore), leet-speak substitutions, and repeated separators, so
    that trivial respellings cannot evade prohibited-operation detection.
    """
    lowered = (action or "").lower()
    translated = lowered.translate(_LEET_TRANSLATION)
    unified = re.sub(r"[-.\s/\\:;]+", "_", translated)
    collapsed = re.sub(r"_+", "_", unified)
    return collapsed.strip("_")


# Canonical prohibited operation -> semantic stem groups.
# An action maps to the prohibited operation when (after normalization)
# it contains at least one stem from EACH group (AND across groups,
# OR within a group), order-independent. Stems catch morphological
# variants: fabricate / fabrication / fabricated all contain "fabricat".
_PROHIBITED_STEMS = (
    ("fabricate_evidence", (("fabricat",), ("evidence",))),
    ("destroy_evidence", (("destroy",), ("evidence",))),
    ("weaken_test", (("weaken",), ("test",))),
    ("break_trust", (("break",), ("trust",))),
    ("harm", (("harm",),)),
)


def _infer_operation(action: str) -> str:
    """Derive the canonical Law 11 operation from the pipeline action name.

    Inherently prohibited operations are checked FIRST so that an action
    literally named e.g. "fabricate_evidence" maps to the prohibited
    operation instead of falling through to the generic "execute".

    The check is normalization-resistant: separators (hyphen/space/dot),
    leet-speak substitutions, and morphological variants (fabricate /
    fabrication / fabricated) all resolve to the same prohibited concept.
    A respelling is not a different action.

    Otherwise the first matching keyword wins; unknown actions default to
    OPERATION_EXECUTE (a generic consequential action).
    """
    normalized = _normalize_action_text(action)
    for prohibited in INHERENTLY_PROHIBITED_OPERATIONS:
        if prohibited in normalized:
            return prohibited
    for canonical, stem_groups in _PROHIBITED_STEMS:
        if all(any(stem in normalized for stem in group) for group in stem_groups):
            return canonical
    for operation, keywords in _OPERATION_KEYWORDS:
        if any(kw in normalized for kw in keywords):
            return operation
    return OPERATION_EXECUTE


def _candidate_to_typed_action(candidate: PlanCandidate,
                               authority: LawAuthority,
                               *,
                               actor_id: str = "act_pipeline",
                               environment: str = "development") -> TypedAction:
    """Map a PlanCandidate onto the Law 11 TypedAction contract.

    actor_id: who is acting. The pipeline itself has no actor concept;
    callers that know the acting agent SHOULD pass it explicitly.
    environment: where the action would run. Defaults to "development";
    callers executing against production MUST pass environment="production"
    explicitly — the default never silently upgrades the safety posture.
    authority_ref: the LAW grant backing this plan (always present here;
    the NEEDS_AUTHORITY path is therefore governed by the LAW record).
    Safety dimensions thread straight through: True/False are evaluated,
    None stays unknown and the gate fails closed to NEEDS_EVIDENCE.
    """
    reversibility = {
        "REVERSIBLE": LAW11_REVERSIBLE,
        "IRREVERSIBLE": LAW11_IRREVERSIBLE,
    }.get(candidate.reversibility, LAW11_CONDITIONAL)
    return TypedAction(
        actor_id=actor_id,
        operation=_infer_operation(candidate.action),
        environment=environment,
        resource=authority.scope,
        authority_ref=authority.grant_id,
        policy_version="CURRENT",
        evidence_refs=tuple(candidate.proof_requirements),
        reversibility=reversibility,
        rights_safe=candidate.rights_safe,
        safety_safe=candidate.safety_safe,
        privacy_safe=candidate.privacy_safe,
        consent_obtained=None,  # unknown at this seam -> gate fails closed
        description=candidate.description,
    )


def _baseline_candidate() -> Candidate:
    """Synthesize the explicit 'do nothing' baseline for baseline-relative
    value (ΔV). The baseline is the current course: by definition ΔV=0
    against itself. It is constructed to pass the calculus gate (ADMISSIBLE)
    so it never distorts the NEEDS_EVIDENCE/PROHIBITED accounting of real
    candidates — it is the reference point, not a contender.

    Baseline zero is exact-by-definition for the ΔV calculation; it says
    nothing about whether the current course is good or harmful (Zero Value
    Law: baseline zero ≠ verified neutral).
    """
    neutral_quality = {d: 5.0 for d in QUALITY_DIMENSIONS}
    full_confidence = {d: 1.0 for d in QUALITY_DIMENSIONS}
    return Candidate(
        candidate_id=BASELINE_CANDIDATE_ID,
        quality=neutral_quality,
        confidence=full_confidence,
        pv=PVEstimate(B=0.0, H=0.0, C=0.0, R=0.0,
                      confidence={"B": 1.0, "H": 1.0, "C": 1.0, "R": 1.0},
                      evidence_count=1),
        authorized=True,
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        stakes="low",
        reversible=True,
        is_baseline=True,
    )


def _select_minimum_sufficient(
    candidates: Sequence[PlanCandidate],
    profile: QualityProfile,
    risk_policy: RiskPolicy,
) -> tuple[PlanCandidate | None, tuple, dict]:
    """Route selection through the canonical value calculus.

    Converts admissible PlanCandidates to calculus Candidates, appends the
    explicit 'do nothing' baseline, and calls evaluate_candidates() for
    baseline-relative value (ΔV), Pareto comparison, and interval dominance.
    There is no second decision engine here.

    Returns (winner_or_None, score_rows, evaluation). The evaluation dict is
    the raw evaluate_candidates() result: decision ∈ {ACT, READ_MORE, ASK,
    REFUSE}, selected candidate_id, top3, per-row gate/Q/ΔV/interval detail.

    A high quality score Q can never disguise negative baseline-relative
    value: eligibility requires v_safe > 0. Unmeasured value can never
    silently become zero: the gate verdicts NEEDS_EVIDENCE before selection.
    """
    by_id = {c.candidate_id: c for c in candidates}
    calc_candidates = [_candidate_to_calculus(c) for c in candidates]
    calc_candidates.append(_baseline_candidate())
    evaluation = evaluate_candidates(
        calc_candidates, BASELINE_CANDIDATE_ID, profile, risk_policy
    )
    selected_id = evaluation.get("selected")
    winner = by_id.get(selected_id) if selected_id else None
    # Score rows: (candidate_id, Q, delta_v, v_safe, gate) — the math is visible.
    rows = {
        r["candidate_id"]: r for r in evaluation.get("rows", [])
        if r["candidate_id"] != BASELINE_CANDIDATE_ID
    }
    scores = tuple(
        (cid,
         round(rows[cid]["q"]["Q"], 4),
         round(rows[cid]["delta_v"], 4),
         round(rows[cid]["v_safe"], 4),
         rows[cid]["gate"])
        for cid in [c.candidate_id for c in candidates]
        if cid in rows
    )
    return winner, scores, evaluation


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
                actor_id: str = "act_pipeline",
                environment: str = "development",
                ) -> tuple[ActionPlan | None, ActionReceipt]:
    """Phase 1: bind LAW authority to a minimum-sufficient plan.

    Returns (plan, receipt). On any refusal, plan is None and the receipt
    carries phase PLAN_REFUSED with the governing code. No execution happens
    here — planning never executes.

    Do-no-harm enforcement: every candidate is hard-gated through the
    calculus's gate_candidate BEFORE selection. PROHIBITED and NEEDS_EVIDENCE
    candidates are excluded and can never win or execute; the exclusion
    reasons are recorded as receipt evidence. When nothing admissible remains
    the plan is refused with PLAN_SAFETY_PROHIBITED (hard violations) or
    PLAN_SAFETY_NEEDS_EVIDENCE (unresolved critical safety evidence).
    NEEDS_AUTHORITY verdicts remain
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

    # --- Law 11 typed-action gate (the only hard law). Runs BEFORE the
    # calculus gate and BEFORE value scoring: a good calculation cannot
    # create permission. Each candidate is mapped to a TypedAction and run
    # through law11_gate():
    #   PROHIBITED -> removed, can never win or execute.
    #   NEEDS_EVIDENCE / NEEDS_AUTHORITY -> flagged, excluded from scoring.
    #   ADMISSIBLE -> proceeds to the calculus gate below.
    # Fail closed: unmapped/unknown fields -> NEEDS_EVIDENCE, never PASS.
    # The verdict and reasons are recorded as receipt evidence so the audit
    # trail shows exactly which layer excluded which candidate and why.
    law11_admissible: list[PlanCandidate] = []
    law11_excluded: list[tuple[str, str, tuple[str, ...]]] = []  # (cid, verdict, reasons)
    for c in candidates:
        typed = _candidate_to_typed_action(c, authority, actor_id=actor_id,
                                           environment=environment)
        verdict = law11_gate(typed)
        if verdict.verdict == LAW11_ADMISSIBLE:
            law11_admissible.append(c)
        else:
            law11_excluded.append((c.candidate_id, verdict.verdict, verdict.reasons))
    law11_evidence = tuple(
        f"candidate {cid} EXCLUDED by Law 11 gate [{v}]: "
        f"{', '.join(rs) if rs else 'no reason recorded'}"
        for cid, v, rs in law11_excluded
    )
    if not law11_admissible:
        detail = "; ".join(
            f"{cid} [{v}: {', '.join(rs) if rs else 'no reason recorded'}]"
            for cid, v, rs in law11_excluded
        )
        if any(v == LAW11_PROHIBITED for _, v, _ in law11_excluded):
            return refused(
                PLAN_SAFETY_PROHIBITED,
                evidence=f"all {len(candidates)} candidate(s) PROHIBITED by the "
                         f"Law 11 (do-no-harm) gate; nothing admissible to execute. "
                         f"{detail}",
            )
        if any(v == LAW11_NEEDS_AUTHORITY for _, v, _ in law11_excluded):
            return refused(
                PLAN_LAW11_NEEDS_AUTHORITY,
                evidence=f"all {len(candidates)} candidate(s) NEEDS_AUTHORITY by the "
                         f"Law 11 (do-no-harm) gate; explicit authority required, "
                         f"nothing admissible to execute. {detail}",
            )
        return refused(
            PLAN_SAFETY_NEEDS_EVIDENCE,
            evidence=f"all {len(candidates)} candidate(s) NEEDS_EVIDENCE by the "
                     f"Law 11 (do-no-harm) gate; critical safety evidence unresolved, "
                     f"nothing admissible to execute. {detail}",
        )

    # --- Law 11 v2 (Uncertainty Handler) phase. Runs AFTER Law 11 v1 hard
    # gate and BEFORE Conflict Resolution: uncertain/asymmetric/delayed/
    # difficult-to-measure harms get structured assessment. For candidates
    # carrying harm_assessments, each is evaluated via assess_uncertain_harm().
    # PROHIBITED / NEEDS_EVIDENCE / NEEDS_AUTHORITY -> excluded.
    # Candidates WITHOUT harm_assessments skip this phase (existing behavior).
    from kernel.protocol.harm_assessment import assess_uncertain_harm
    law11v2_admissible: list[PlanCandidate] = []
    law11v2_excluded: list[tuple[str, str, str]] = []  # (cid, verdict, summary)
    for c in law11_admissible:
        assessments = c.harm_assessments
        if not assessments:
            law11v2_admissible.append(c)
            continue
        # Build the typed action for this candidate (same as Law 11 v1 gate)
        typed_c = _candidate_to_typed_action(c, authority, actor_id=actor_id,
                                             environment=environment)
        result = assess_uncertain_harm(typed_c, tuple(assessments))
        if result.verdict in (LAW11_PROHIBITED, LAW11_NEEDS_EVIDENCE, LAW11_NEEDS_AUTHORITY):
            law11v2_excluded.append((
                c.candidate_id, result.verdict,
                "; ".join(result.reasons[:3]) if result.reasons else result.verdict,
            ))
        else:
            law11v2_admissible.append(c)

    # The v2 exclusions are receipt evidence: the audit trail must name
    # every layer that excluded a candidate and why (same as Law 11 v1
    # and Conflict Resolution below). This is the ONE canonical rendering:
    # refusal receipts carry the identical per-candidate strings as the
    # accepted receipt, so exclusion tuples are parseable from any phase.
    law11v2_evidence = tuple(
        f"candidate {cid} EXCLUDED by Law 11 v2 (uncertainty handler) [{v}]: "
        f"{s if s else 'no reason recorded'}"
        for cid, v, s in law11v2_excluded
    )
    law11v2_evidence_text = (
        "; ".join(law11v2_evidence) + ". " if law11v2_evidence else ""
    )

    # --- Conflict Resolution phase (Law of One). Runs AFTER Law 11 hard
    # prohibitions and BEFORE value scoring: a good calculation cannot
    # erase a group's harm. For candidates carrying a governed impact matrix,
    # the full Conflict Resolution Engine runs:
    #   1. assess_no_worse_off — no-worse-off test + anti-laundering.
    #      WORSENING / PROHIBITED -> excluded, can never win.
    #      PENDING_WINDOW / INCONCLUSIVE -> excluded (need evidence first).
    #   2. check_pareto_improvement — per-group Pareto test (recorded).
    #   3. check_resolve_before_trade — mandatory invariant: if the matrix
    #      shows material adverse effects, the decision record must show
    #      alternatives were considered, else NEEDS_EVIDENCE.
    # Candidates WITHOUT a matrix skip this phase (existing behavior preserved).
    # Fail closed: unknown bounds, failed laundering, or missing evidence
    # never support a no-worse-off claim.
    from kernel.protocol.conflict_resolution import (
        ImpactMatrix as _IM,
        DesignSearchRecord as _DSR,
    )
    cr_admissible: list[PlanCandidate] = []
    cr_excluded: list[tuple[str, str, str]] = []  # (cid, verdict, summary)
    cr_notes: list[str] = []  # informational (Pareto breakdowns, comparability)
    for c in law11v2_admissible:
        matrix = c.impact_matrix
        if matrix is None:
            cr_admissible.append(c)
            continue
        # Type safety: only ImpactMatrix instances are assessed.
        # A wrong type is a caller bug -> fail closed to NEEDS_EVIDENCE.
        if not isinstance(matrix, _IM):
            cr_excluded.append((
                c.candidate_id, "NEEDS_EVIDENCE",
                f"impact_matrix has wrong type {type(matrix).__name__}; "
                "expected ImpactMatrix.",
            ))
            continue
        assessment = assess_no_worse_off(matrix)
        if assessment.verdict in (CR_PROHIBITED, CR_WORSENING,
                                  CR_PENDING, CR_INCONCLUSIVE):
            summary = "; ".join(assessment.notes[:3]) if assessment.notes else assessment.verdict
            cr_excluded.append((c.candidate_id, assessment.verdict, summary))
            continue
        # --- Pareto improvement check (per-group, never aggregate).
        # Informational: the no-worse-off gate above already excludes
        # worsening candidates. The Pareto breakdown is recorded so the
        # receipt shows which groups are better/worse/unknown.
        pareto = check_pareto_improvement(matrix)
        if pareto.groups_worse:
            cr_notes.append(
                f"candidate {c.candidate_id} Pareto: groups worse off: "
                f"{pareto.groups_worse}."
            )
        if pareto.groups_unknown:
            cr_notes.append(
                f"candidate {c.candidate_id} Pareto: groups unknown: "
                f"{pareto.groups_unknown}."
            )
        if pareto.is_pareto_improvement:
            cr_notes.append(
                f"candidate {c.candidate_id} Pareto improvement: "
                f"{pareto.groups_improved} improved, none worse."
            )
        # --- Resolve Before Trade (mandatory invariant).
        # Detect material adverse effects from the matrix: any cell with a
        # negative point estimate or negative lower bound, or any harm
        # profile at substantial+ severity.
        has_material_adverse = False
        for cell in matrix.cells:
            d = cell.delta()
            if (d is not None and d < 0) or (
                cell.lower_bound is not None and cell.lower_bound < 0
            ):
                has_material_adverse = True
                break
        if not has_material_adverse:
            for hp in matrix.harm_profiles:
                if hp.severity in ("substantial", "injury", "rights_violation"):
                    has_material_adverse = True
                    break
        if has_material_adverse:
            record = c.design_search_record
            if record is None or not isinstance(record, _DSR):
                cr_excluded.append((
                    c.candidate_id, "NEEDS_EVIDENCE",
                    "RESOLVE_BEFORE_TRADE violated: material adverse effects "
                    "but no DesignSearchRecord provided.",
                ))
                continue
            satisfied, reason = check_resolve_before_trade(
                record, has_material_adverse_effects=True,
            )
            if not satisfied:
                cr_excluded.append((c.candidate_id, "NEEDS_EVIDENCE", reason))
                continue
            cr_notes.append(
                f"candidate {c.candidate_id} Resolve Before Trade: {reason}"
            )
        cr_admissible.append(c)
    # --- Comparability assessment (typed, never forced into one number).
    # For pairs of admissible candidates WITH matrices: if one DOMINATES
    # another, the dominated candidate is excluded (it can never be the
    # right choice). INCOMPARABLE is recorded honestly — not a failure.
    # PROHIBITED comparison -> the violating candidate is excluded.
    _matrix_candidates = [
        c for c in cr_admissible
        if isinstance(c.impact_matrix, _IM)
    ]
    _dominated: set[str] = set()
    for i in range(len(_matrix_candidates)):
        for j in range(i + 1, len(_matrix_candidates)):
            ca = _matrix_candidates[i]
            cb = _matrix_candidates[j]
            comp = assess_comparability(ca.impact_matrix, cb.impact_matrix)
            if comp.assessment == COMPARE_DOMINATES and comp.dominating:
                # comp.dominating holds the dominating matrix's action_id.
                # The other candidate is dominated -> exclude it (it can
                # never be the right choice).
                if comp.dominating == ca.impact_matrix.action_id:
                    _dominated.add(cb.candidate_id)
                    cr_notes.append(
                        f"candidate {cb.candidate_id} DOMINATED by "
                        f"{ca.candidate_id}; excluded."
                    )
                elif comp.dominating == cb.impact_matrix.action_id:
                    _dominated.add(ca.candidate_id)
                    cr_notes.append(
                        f"candidate {ca.candidate_id} DOMINATED by "
                        f"{cb.candidate_id}; excluded."
                    )
            elif comp.assessment == COMPARE_INCOMPARABLE:
                cr_notes.append(
                    f"candidates {ca.candidate_id} vs {cb.candidate_id}: "
                    f"INCOMPARABLE — {'; '.join(comp.notes[:2])}"
                )
            elif comp.assessment == COMPARE_PROHIBITED:
                cr_notes.append(
                    f"candidates {ca.candidate_id} vs {cb.candidate_id}: "
                    f"comparability PROHIBITED — {'; '.join(comp.notes[:2])}"
                )
    if _dominated:
        _kept: list[PlanCandidate] = []
        for c in cr_admissible:
            if c.candidate_id in _dominated:
                cr_excluded.append((
                    c.candidate_id, "DOMINATED",
                    "Dominated by another candidate on every dimension.",
                ))
            else:
                _kept.append(c)
        cr_admissible = _kept
    cr_evidence = law11_evidence + law11v2_evidence + tuple(
        f"candidate {cid} EXCLUDED by Conflict Resolution [{v}]: {s}"
        for cid, v, s in cr_excluded
    ) + tuple(f"Conflict Resolution note: {n}" for n in cr_notes)
    if not cr_admissible:
        detail = "; ".join(
            f"{cid} [{v}: {s}]" for cid, v, s in cr_excluded
        )
        if any(v == CR_PROHIBITED for _, v, _ in cr_excluded):
            return refused(
                PLAN_SAFETY_PROHIBITED,
                evidence=f"{law11v2_evidence_text}all {len(law11v2_admissible)} candidate(s) with impact "
                         f"matrices failed Conflict Resolution; nothing admissible. {detail}",
            )
        return refused(
            PLAN_SAFETY_NEEDS_EVIDENCE,
            evidence=f"{law11v2_evidence_text}all {len(law11v2_admissible)} candidate(s) with impact "
                     f"matrices need evidence per Conflict Resolution. {detail}",
        )

    # --- Do-no-harm hard gate (safety floor). Fail closed: a PROHIBITED
    # candidate gets zero value — it is excluded from selection entirely.
    # A NEEDS_EVIDENCE candidate is likewise excluded: unresolved critical
    # safety evidence must never reach selection or execution.
    risk = risk_policy if risk_policy is not None else RiskPolicy()
    admissible: list[PlanCandidate] = []
    excluded: list[tuple[str, str, list[str]]] = []  # (candidate_id, gate verdict, gate reasons)
    for c in cr_admissible:
        gate, reasons, _q = gate_candidate(_candidate_to_calculus(c), profile, risk)
        if gate in (PROHIBITED, NEEDS_EVIDENCE):
            excluded.append((c.candidate_id, gate, reasons))
        else:
            admissible.append(c)
    if not admissible:
        detail = "; ".join(f"{cid} [{verdict}: {', '.join(rs)}]" for cid, verdict, rs in excluded)
        law11_detail = "; ".join(
            f"{cid} [{v}: {', '.join(rs) if rs else 'no reason recorded'}]"
            for cid, v, rs in law11_excluded
        )
        prior = f"Law 11 exclusions: {law11_detail}. " if law11_detail else ""
        cr_prior = f"Conflict Resolution exclusions: {'; '.join(f'{cid} [{v}]' for cid, v, _ in cr_excluded)}. " if cr_excluded else ""
        cr_notes_text = " ".join(f"Conflict Resolution note: {n}" for n in cr_notes)
        if cr_notes_text:
            cr_prior += cr_notes_text + " "
        if any(verdict == PROHIBITED for _, verdict, _ in excluded):
            return refused(
                PLAN_SAFETY_PROHIBITED,
                evidence=f"{prior}{law11v2_evidence_text}{cr_prior}all {len(cr_admissible)} conflict-resolved candidate(s) "
                         f"PROHIBITED by the do-no-harm gate; nothing admissible to "
                         f"execute. {detail}",
            )
        return refused(
            PLAN_SAFETY_NEEDS_EVIDENCE,
            evidence=f"{prior}{law11v2_evidence_text}{cr_prior}all {len(cr_admissible)} conflict-resolved candidate(s) "
                     f"NEEDS_EVIDENCE by the do-no-harm gate; critical safety evidence "
                     f"unresolved, nothing admissible to execute. {detail}",
        )
    gate_evidence = cr_evidence + tuple(
        f"candidate {cid} EXCLUDED by do-no-harm gate [{verdict}]: {', '.join(rs)}"
        for cid, verdict, rs in excluded
    )

    # --- Canonical value-calculus selection. The winner is determined by
    # evaluate_candidates(): baseline-relative value (ΔV), Pareto comparison,
    # and interval dominance. There is no second decision engine.
    chosen, scores, evaluation = _select_minimum_sufficient(admissible, profile, risk)
    decision = evaluation.get("decision")
    calculus_evidence = tuple(
        f"candidate {cid}: Q={q}, ΔV={dv}, v_safe={vs} [{gate}]"
        for cid, q, dv, vs, gate in scores
    ) + (
        f"value-calculus decision={decision}, "
        f"selected={evaluation.get('selected')}, "
        f"baseline={BASELINE_CANDIDATE_ID}",
    )
    if decision != ACT or chosen is None:
        # The calculus did not authorize autonomous selection.
        # REFUSE: nothing admissible clears the bar (all prohibited).
        # READ_MORE: insufficient evidence — value unmeasured or uncertain.
        # ASK: consequential/irreversible — needs human judgment beyond LAW.
        if decision == REFUSE:
            return refused(
                PLAN_SAFETY_PROHIBITED,
                evidence=f"value calculus REFUSED: no admissible candidate clears "
                         f"the value bar. {'; '.join(calculus_evidence)}",
            )
        if decision == ASK:
            return refused(
                PLAN_NEEDS_HUMAN_JUDGMENT,
                evidence=f"value calculus ASK: winner is consequential or "
                         f"irreversible; human judgment required beyond the LAW "
                         f"record. {'; '.join(calculus_evidence)}",
            )
        # READ_MORE or no selection: value evidence insufficient.
        # Uncertainty never silently becomes zero — it becomes a refusal.
        return refused(
            PLAN_VALUE_INSUFFICIENT,
            evidence=f"value calculus {decision}: insufficient value evidence for "
                     f"autonomous selection. {'; '.join(calculus_evidence)}",
        )

    plan = ActionPlan(
        plan_id=plan_id, action=authority.action, chosen=chosen,
        authority=authority, candidate_scores=scores, planned_at=now,
    )
    receipt = ActionReceipt(
        receipt_id=_new_id(), plan_id=plan_id, phase="PLAN_ACCEPTED",
        executed=False, outcome_verified=False, truth_state="UNKNOWN",
        evidence=gate_evidence + calculus_evidence + (
            f"selected {chosen.candidate_id} via canonical value calculus "
            f"(baseline-relative ΔV, Pareto, interval dominance)",
        ),
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
                 on_executed: Callable[[ActionPlan, ActionReceipt], None] | None = None,
                 actor_id: str = "act_pipeline",
                 environment: str = "development",
                 law12_state: dict | None = None,
                 law12_proof_time: dict | None = None) -> ActionReceipt:
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
    refused with PLAN_SAFETY_PROHIBITED or PLAN_SAFETY_NEEDS_EVIDENCE
    respectively. NEEDS_AUTHORITY verdicts stay governed by the
    LAW authority record (the LAW node's seam); this seam enforces the harm
    hard stops only and weakens nothing. Pass the same profile (and risk
    policy) used at plan time so the verdict is a re-verification, not a
    re-derivation under different math.

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

    # --- Law 11 execution-door recheck (last responsible moment). The door
    # independently re-verifies the planning context immediately before the
    # executor fires:
    #   * authority withdrawn since planning -> PROHIBITED, STOP.
    #   * authority changed since planning -> NEEDS_AUTHORITY, STOP.
    #   * target resource changed since planning -> PROHIBITED, STOP.
    #   * Law 11 gate re-run on the current action state.
    # Any non-ADMISSIBLE verdict refuses execution; the executor is never
    # called. This is the hallway to the door: the gate exists, and now the
    # pipeline actually walks through it.
    typed_final = _candidate_to_typed_action(plan.chosen, fresh,
                                             actor_id=actor_id,
                                             environment=environment)
    door_verdict = execution_door_check(
        typed_final,
        planned_authority_ref=plan.authority.grant_id,
        current_authority_ref=fresh.grant_id,
        planned_resource=plan.authority.scope,
        current_resource=fresh.scope,
    )
    door_evidence = (
        f"Law 11 execution-door re-gate: verdict {door_verdict.verdict}"
        + (f" [{', '.join(door_verdict.reasons)}]" if door_verdict.reasons else "")
        + f" (planned grant {plan.authority.grant_id} / current grant {fresh.grant_id}; "
          f"planned scope {plan.authority.scope} / current scope {fresh.scope})"
    )
    if door_verdict.verdict == LAW11_PROHIBITED:
        return refused(PLAN_SAFETY_PROHIBITED, evidence=door_evidence)
    if door_verdict.verdict == LAW11_NEEDS_EVIDENCE:
        return refused(PLAN_SAFETY_NEEDS_EVIDENCE, evidence=door_evidence)
    if door_verdict.verdict == LAW11_NEEDS_AUTHORITY:
        return refused(PLAN_LAW11_NEEDS_AUTHORITY, evidence=door_evidence)

    # --- Law 12: change-based proof expiry (ACTIVE). The time check above
    # catches old proofs; this catches proofs whose world changed. The proof
    # being relied on is the PLAN's authority grant (plan.authority) — not
    # the fresh one. law12_proof_time holds the world values when that
    # grant was established (supplied by the caller: whoever established the
    # grant knows its world). Current state auto-resolves when not supplied,
    # so the check fires with proof-time alone — no second opt-in needed.
    # The fresh re-resolution supplies current grant standing: if the grant
    # id changed since plan time, the plan's authority basis changed.
    # (Without law12_proof_time, staleness cannot be established — the
    # check is skipped. Precise, never speculative.)
    if law12_proof_time is not None:
        from .protocol.proof_expiry import (
            proof_from_authority, validate_proof, ProofStatus,
            resolve_current_state, DEP_AUTHORITY_RECEIPT,
        )
        state = dict(law12_state) if law12_state is not None \
            else resolve_current_state()
        # The freshly re-resolved authority IS current grant standing.
        state.setdefault(DEP_AUTHORITY_RECEIPT, fresh.grant_id)
        grant_proof = proof_from_authority(
            plan.authority.grant_id,
            source_sha=law12_proof_time.get("source_sha", ""),
            policy_ref=law12_proof_time.get("policy_ref", ""),
        )
        validation = validate_proof(grant_proof, state)
        if validation.status != ProofStatus.CURRENT_UNTIL_RECHECK:
            return refused(LAW_AUTHORITY_PROOF_STALE,
                           evidence=f"Law 12: authority grant proof stale: "
                                    f"{validation.reason()}. Re-resolve authority; "
                                    f"do not execute on expired proof.")

    # --- Execution-time do-no-harm re-gate (safety floor). Fail closed:
    # the gate is re-verified at the last responsible moment, immediately
    # before the executor fires. A PROHIBITED chosen candidate — whether
    # hand-crafted outside plan_action or changed after planning — is
    # refused here; the executor is never called. A NEEDS_EVIDENCE chosen
    # candidate is likewise refused: unresolved critical safety evidence
    # must never reach the executor.
    risk = risk_policy if risk_policy is not None else RiskPolicy()
    gate, reasons, _q = gate_candidate(_candidate_to_calculus(plan.chosen), profile, risk)
    gate_evidence = (f"execution-time do-no-harm re-gate: candidate "
                     f"{plan.chosen.candidate_id} verdict {gate}"
                     + (f" [{', '.join(reasons)}]" if reasons else ""))
    if gate == PROHIBITED:
        return refused(PLAN_SAFETY_PROHIBITED, evidence=gate_evidence)
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
