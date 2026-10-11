"""
decision_discipline.py — The Decision Discipline Engine.

Implements Shawn's Naya Code intel (2026-10-11) as executable machine law:
  - Typed comparability: DOMINATES / INCOMPARABLE / UNKNOWN / PROHIBITED
  - Decision hierarchy: protect rights → eliminate dominated → improve →
    apply legitimate priorities → escalate
  - Five-way escalation routing: ACT / READ_MORE / ACT_EXPERIMENT / ASK / REFUSE
  - Evidence vs Authority separation at the LAW→ACT boundary
  - Two-requirements sequencing: authority-first / evidence-first /
    parallel / contain+escalate
  - Escalation packets: compact machine receipts

This extends the existing seams (typed_action.law11_gate, authority_gate,
value_calculus) — it does not replace them. Per the intel: "implement in the
existing LAW → ACT → VERIFY system without adding another decision engine."

Key principles (machine-enforced):
  - "Never sacrifice a meaningful difference for the convenience of a single score."
  - "Evidence never creates authority. Authority never replaces evidence."
  - "Never ask permission for what you're already authorized to do.
     Never assume permission for what you're not."
  - "INCOMPARABLE is a valid decision state, not a failure to calculate."
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .typed_action import (
    ADMISSIBLE,
    NEEDS_AUTHORITY,
    NEEDS_EVIDENCE,
    PROHIBITED,
    TypedAction,
    law11_gate,
)


# ---------------------------------------------------------------------------
# 1. TYPED COMPARABILITY
# ---------------------------------------------------------------------------

# Comparability verdicts. First-class machine results, not scores.
DOMINATES = "DOMINATES"
INCOMPARABLE = "INCOMPARABLE"
UNKNOWN = "UNKNOWN"
# PROHIBITED reused from typed_action — a hard protection violated.


@dataclass(frozen=True)
class OutcomeDimension:
    """One measurable dimension of one option, with uncertainty bounds.

    name: e.g. "speed", "accessibility", "privacy"
    # lower/upper: justified bounds on the change vs baseline (higher = better).
    #   None bound = unknown on that side (fail-open is forbidden: unknown
    #   bounds can never establish dominance).
    # evidence_quality: "measured" | "estimated" | "unknown"
    """
    name: str
    lower: float | None
    upper: float | None
    evidence_quality: str = "measured"


@dataclass(frozen=True)
class DecisionOption:
    """A candidate option with per-dimension outcomes.

    option_id: stable identifier
    dimensions: tuple of OutcomeDimension (each oriented higher=better)
    law11_action: the TypedAction for hard-gate checking (may be None for
        pure comparison tests, but production callers must supply it)
    """
    option_id: str
    dimensions: tuple[OutcomeDimension, ...] = ()
    law11_action: TypedAction | None = None
    description: str = ""


@dataclass(frozen=True)
class ComparabilityResult:
    """Outcome of comparing option A against option B."""
    verdict: str  # DOMINATES | INCOMPARABLE | UNKNOWN | PROHIBITED
    winner_id: str | None  # set when verdict == DOMINATES
    reasons: tuple[str, ...] = ()
    # Dimensions where A is strictly better / worse / unknown / tied.
    a_better: tuple[str, ...] = ()
    b_better: tuple[str, ...] = ()
    unknown_dims: tuple[str, ...] = ()


def _dimension_delta(a: OutcomeDimension | None,
                     b: OutcomeDimension | None) -> str:
    """Classify A vs B on one dimension using justified bounds.

    Returns: "a_better" | "b_better" | "tie" | "unknown"
    Dominance requires the LOWER bound of the difference to be >= 0.
    A favorable point estimate with a wide interval does NOT establish
    dominance — that is measurement laundering.
    """
    if a is None or b is None:
        return "unknown"
    if a.lower is None or a.upper is None or b.lower is None or b.upper is None:
        return "unknown"
    # Conservative difference bounds: worst case for A vs best case for B.
    diff_lower = a.lower - b.upper
    diff_upper = a.upper - b.lower
    if diff_lower > 0:
        return "a_better"
    if diff_upper < 0:
        return "b_better"
    if diff_lower == 0 and diff_upper == 0:
        return "tie"
    return "unknown"


def compare_options(a: DecisionOption, b: DecisionOption) -> ComparabilityResult:
    """Compare two options. Never invents an exchange rate between dimensions.

    Formal rule: A dominates B only if Δ_k(A,B) >= 0 for every dimension k
    (using justified lower bounds) and at least one dimension is genuinely
    better. If privacy is better under A but accessibility better under B,
    neither dominates — that is INCOMPARABLE, an honest result.

    Hard LAW check first: if either option's TypedAction is PROHIBITED,
    the comparison yields PROHIBITED regardless of apparent advantages.
    """
    # Hard gate first: prohibited options cannot win on scores.
    for opt in (a, b):
        if opt.law11_action is not None:
            verdict = law11_gate(opt.law11_action)
            if verdict.verdict == PROHIBITED:
                return ComparabilityResult(
                    verdict=PROHIBITED,
                    winner_id=None,
                    reasons=(f"PROHIBITED:{opt.option_id}:"
                             + ",".join(verdict.reasons),),
                )

    dim_names: list[str] = []
    for d in a.dimensions:
        if d.name not in dim_names:
            dim_names.append(d.name)
    for d in b.dimensions:
        if d.name not in dim_names:
            dim_names.append(d.name)

    a_map = {d.name: d for d in a.dimensions}
    b_map = {d.name: d for d in b.dimensions}

    a_better: list[str] = []
    b_better: list[str] = []
    unknown: list[str] = []

    for name in dim_names:
        outcome = _dimension_delta(a_map.get(name), b_map.get(name))
        if outcome == "a_better":
            a_better.append(name)
        elif outcome == "b_better":
            b_better.append(name)
        elif outcome == "unknown":
            unknown.append(name)
        # ties contribute to neither list

    if unknown:
        return ComparabilityResult(
            verdict=UNKNOWN,
            winner_id=None,
            reasons=(f"UNKNOWN_DIMENSIONS:{','.join(sorted(unknown))}",),
            a_better=tuple(a_better),
            b_better=tuple(b_better),
            unknown_dims=tuple(sorted(unknown)),
        )
    if a_better and not b_better:
        return ComparabilityResult(
            verdict=DOMINATES,
            winner_id=a.option_id,
            reasons=(f"DOMINATES_ON:{','.join(sorted(a_better))}",),
            a_better=tuple(sorted(a_better)),
            b_better=(),
        )
    if b_better and not a_better:
        return ComparabilityResult(
            verdict=DOMINATES,
            winner_id=b.option_id,
            reasons=(f"DOMINATES_ON:{','.join(sorted(b_better))}",),
            a_better=(),
            b_better=tuple(sorted(b_better)),
        )
    # Both have advantages, or neither does: incomparable.
    return ComparabilityResult(
        verdict=INCOMPARABLE,
        winner_id=None,
        reasons=("NO_DOMINANCE:distinct_legitimate_advantages",),
        a_better=tuple(sorted(a_better)),
        b_better=tuple(sorted(b_better)),
    )


def eliminate_dominated(options: list[DecisionOption]) -> list[DecisionOption]:
    """Remove every option dominated by another. Never invents exchange rates.

    An option survives iff no other option DOMINATES it. INCOMPARABLE and
    UNKNOWN comparisons never eliminate — uncertainty is not defeat.
    """
    survivors: list[DecisionOption] = []
    for candidate in options:
        dominated = False
        for other in options:
            if other.option_id == candidate.option_id:
                continue
            result = compare_options(other, candidate)
            if result.verdict == DOMINATES and result.winner_id == other.option_id:
                dominated = True
                break
        if not dominated:
            survivors.append(candidate)
    return survivors


# ---------------------------------------------------------------------------
# 2. EVIDENCE vs AUTHORITY — machine-enforced at the LAW→ACT boundary
# ---------------------------------------------------------------------------

# Requirement states. NEEDS_BOTH is an internal label, not a replacement
# for the four canonical LAW states (ADMISSIBLE / NEEDS_EVIDENCE /
# NEEDS_AUTHORITY / PROHIBITED).
NEEDS_BOTH = "NEEDS_BOTH"

# Independent status values.
EVIDENCE_PENDING = "pending"
EVIDENCE_SUFFICIENT = "sufficient"
EVIDENCE_STALE = "stale"

AUTHORITY_MISSING = "missing"
AUTHORITY_GRANTED = "granted"
AUTHORITY_EXPIRED = "expired"


@dataclass(frozen=True)
class RequirementAssessment:
    """Separation of evidence and authority for one proposed action."""
    state: str  # NEEDS_EVIDENCE | NEEDS_AUTHORITY | NEEDS_BOTH | PROHIBITED | ADMISSIBLE
    evidence_status: str  # pending | sufficient | stale
    authority_status: str  # missing | granted | expired
    reasons: tuple[str, ...] = ()


def assess_requirements(*,
                        evidence_status: str,
                        authority_status: str,
                        law11_action: TypedAction | None = None) -> RequirementAssessment:
    """Machine-enforce the evidence/authority separation.

    "Evidence never creates authority. Authority never replaces evidence."

    Hard LAW prohibition always wins: PROHIBITED regardless of evidence
    or authority. Otherwise the state is derived from the two independent
    statuses — sufficient evidence cannot cure missing authority, and
    granted authority cannot cure insufficient evidence.
    """
    if law11_action is not None:
        verdict = law11_gate(law11_action)
        if verdict.verdict == PROHIBITED:
            return RequirementAssessment(
                state=PROHIBITED,
                evidence_status=evidence_status,
                authority_status=authority_status,
                reasons=tuple(verdict.reasons),
            )

    evidence_ok = evidence_status == EVIDENCE_SUFFICIENT
    authority_ok = authority_status == AUTHORITY_GRANTED

    if evidence_ok and authority_ok:
        return RequirementAssessment(
            state=ADMISSIBLE,
            evidence_status=evidence_status,
            authority_status=authority_status,
            reasons=(),
        )
    if not evidence_ok and not authority_ok:
        return RequirementAssessment(
            state=NEEDS_BOTH,
            evidence_status=evidence_status,
            authority_status=authority_status,
            reasons=("MISSING_EVIDENCE", "MISSING_AUTHORITY"),
        )
    if not evidence_ok:
        return RequirementAssessment(
            state=NEEDS_EVIDENCE,
            evidence_status=evidence_status,
            authority_status=authority_status,
            reasons=("MISSING_EVIDENCE",),
        )
    return RequirementAssessment(
        state=NEEDS_AUTHORITY,
        evidence_status=evidence_status,
        authority_status=authority_status,
        reasons=("MISSING_AUTHORITY",),
    )


# ---------------------------------------------------------------------------
# 3. TWO-REQUIREMENTS SEQUENCING
# ---------------------------------------------------------------------------

# Sequence routes for NEEDS_BOTH cases.
SEQ_AUTHORITY_FIRST = "AUTHORITY_FIRST"
SEQ_EVIDENCE_FIRST = "EVIDENCE_FIRST"
SEQ_PARALLEL = "PARALLEL"
SEQ_CONTAIN_ESCALATE = "CONTAIN_ESCALATE"


@dataclass(frozen=True)
class SequenceCase:
    """Inputs for choosing the evidence/authority sequence."""
    evidence_gathering_needs_authority: bool = False
    immediate_harm_occurring: bool = False
    delay_creates_material_risk: bool = False
    parallel_safe: bool = False  # can both proceed without crossing a boundary


def choose_sequence(case: SequenceCase) -> str:
    """Choose the safest and fastest lawful order for gathering both.

    Order of checks (most urgent first):
      1. Immediate harm -> CONTAIN_ESCALATE
      2. Evidence gathering itself needs authority -> AUTHORITY_FIRST
      3. Delay is risky and parallel is safe -> PARALLEL
      4. Default -> EVIDENCE_FIRST (investigate before asking for a
         potentially unnecessary decision)
    """
    if case.immediate_harm_occurring:
        return SEQ_CONTAIN_ESCALATE
    if case.evidence_gathering_needs_authority:
        return SEQ_AUTHORITY_FIRST
    if case.delay_creates_material_risk and case.parallel_safe:
        return SEQ_PARALLEL
    return SEQ_EVIDENCE_FIRST


def execution_gate(evidence_status: str,
                   authority_status: str,
                   law11_action: TypedAction | None = None) -> RequirementAssessment:
    """The one execution gate: both requirements satisfied AND fresh.

    Stale evidence or expired authority blocks execution — approvals expire
    when the situation changes. Re-checked at the point of action.
    """
    return assess_requirements(
        evidence_status=evidence_status,
        authority_status=authority_status,
        law11_action=law11_action,
    )


# ---------------------------------------------------------------------------
# 4. FIVE-WAY ESCALATION ROUTING
# ---------------------------------------------------------------------------

# Escalation routes (feed the canonical ACT / READ_MORE / ASK / REFUSE).
ROUTE_ACT = "ACT"
ROUTE_READ_MORE = "READ_MORE"
ROUTE_ACT_EXPERIMENT = "ACT_EXPERIMENT"
ROUTE_ASK = "ASK"
ROUTE_REFUSE = "REFUSE"
# Internal non-execution condition (not a canonical outcome).
ROUTE_HOLD = "HOLD"


@dataclass(frozen=True)
class RoutingCase:
    """Inputs for the five-way routing decision."""
    violates_hard_law: bool = False
    requires_protected_authority: bool = False
    has_applicable_approved_priority: bool = False
    material_facts_missing: bool = False
    safe_evidence_path_available: bool = False
    consequential: bool = False
    authorized_bounded_experiment_available: bool = False
    unresolved_material_value_conflict: bool = False


def route_decision(case: RoutingCase) -> str:
    """Route an incomparable decision to exactly one response.

    "If evidence can answer the question, investigate. If an approved
    priority can answer it, decide. If a safe, authorized experiment can
    answer it, test. But if the decision requires choosing whose important
    interests take precedence, and no legitimate rule already settles that
    choice, escalate."

    Order (fail-closed, most severe first):
      1. Hard LAW violation -> REFUSE (human approval cannot override)
      2. Protected authority required -> ASK
      3. Approved priority applies -> ACT (authority already delegated)
      4. Material facts missing -> READ_MORE if safe path, else ASK/HOLD
      5. Authorized bounded experiment -> ACT_EXPERIMENT
      6. Unresolved material value conflict -> ASK
      7. Default -> ACT
    """
    if case.violates_hard_law:
        return ROUTE_REFUSE
    if case.requires_protected_authority:
        return ROUTE_ASK
    if case.has_applicable_approved_priority:
        return ROUTE_ACT
    if case.material_facts_missing:
        if case.safe_evidence_path_available:
            return ROUTE_READ_MORE
        return ROUTE_ASK if case.consequential else ROUTE_HOLD
    if case.authorized_bounded_experiment_available:
        return ROUTE_ACT_EXPERIMENT
    if case.unresolved_material_value_conflict:
        return ROUTE_ASK
    return ROUTE_ACT


# ---------------------------------------------------------------------------
# 5. DECISION HIERARCHY
# ---------------------------------------------------------------------------

# Hierarchy stages.
STAGE_PROTECT_RIGHTS = "protect_rights"
STAGE_ELIMINATE_DOMINATED = "eliminate_dominated"
STAGE_IMPROVE_DESIGNS = "improve_designs"
STAGE_APPLY_PRIORITIES = "apply_priorities"
STAGE_ESCALATE = "escalate"


@dataclass
class HierarchyResult:
    """Outcome of running the decision hierarchy on a set of options."""
    stage_reached: str
    survivors: list[DecisionOption]
    eliminated: list[str]  # option_ids removed with reasons
    route: str | None = None  # escalation route if STAGE_ESCALATE reached
    escalation_packet: "EscalationPacket | None" = None
    notes: tuple[str, ...] = ()


def run_decision_hierarchy(options: list[DecisionOption],
                           *,
                           approved_priority: str | None = None,
                           routing_case: RoutingCase | None = None,
                           conflict_id: str | None = None) -> HierarchyResult:
    """Run the five-stage decision hierarchy. Never invents exchange rates.

    Stage 1 — Protect rights: discard PROHIBITED options before any
        optimization. No efficiency compensates for a rights violation.
    Stage 2 — Eliminate dominated: remove options another DOMINATES.
    Stage 3 — Improve designs: recorded as a required search step — the
        caller must supply improved candidates; this stage verifies the
        search happened (via the `design_search_performed` note).
    Stage 4 — Apply legitimate priorities: if an approved priority
        resolves the remaining choice, route ACT.
    Stage 5 — Escalate: genuine unresolved conflict -> route and build
        the escalation packet.
    """
    eliminated: list[str] = []

    # Stage 1: hard gates first.
    admissible: list[DecisionOption] = []
    for opt in options:
        if opt.law11_action is not None:
            verdict = law11_gate(opt.law11_action)
            if verdict.verdict == PROHIBITED:
                eliminated.append(
                    f"{opt.option_id}:PROHIBITED:"
                    + ",".join(verdict.reasons)
                )
                continue
        admissible.append(opt)
    if not admissible:
        return HierarchyResult(
            stage_reached=STAGE_PROTECT_RIGHTS,
            survivors=[],
            eliminated=eliminated,
            route=ROUTE_REFUSE,
            notes=("ALL_OPTIONS_PROHIBITED",),
        )

    # Stage 2: eliminate dominated options.
    survivors = eliminate_dominated(admissible)
    for opt in admissible:
        if all(s.option_id != opt.option_id for s in survivors):
            eliminated.append(f"{opt.option_id}:DOMINATED")
    if len(survivors) == 1:
        return HierarchyResult(
            stage_reached=STAGE_ELIMINATE_DOMINATED,
            survivors=survivors,
            eliminated=eliminated,
            route=ROUTE_ACT,
            notes=("SINGLE_NONDOMINATED_SURVIVOR",),
        )

    # Stage 3: improve designs. The engine cannot invent better designs;
    # it enforces that the search is recorded before a trade-off is
    # declared unavoidable.
    notes = ("DESIGN_SEARCH_REQUIRED_BEFORE_TRADEOFF",)

    # Stage 4: approved priority within its legitimate scope.
    if approved_priority:
        route = route_decision(RoutingCase(
            has_applicable_approved_priority=True,
        ))
        return HierarchyResult(
            stage_reached=STAGE_APPLY_PRIORITIES,
            survivors=survivors,
            eliminated=eliminated,
            route=route,
            notes=notes + (f"PRIORITY_APPLIED:{approved_priority}",),
        )

    # Stage 5: escalate the genuine conflict.
    case = routing_case or RoutingCase(
        unresolved_material_value_conflict=True,
        consequential=True,
    )
    route = route_decision(case)
    packet = build_escalation_packet(
        survivors=survivors,
        conflict_id=conflict_id or f"conflict-{uuid.uuid4().hex[:8]}",
        route=route,
    )
    return HierarchyResult(
        stage_reached=STAGE_ESCALATE,
        survivors=survivors,
        eliminated=eliminated,
        route=route,
        escalation_packet=packet,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# 6. ESCALATION PACKETS
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EscalationPacket:
    """Compact decision packet — not an open-ended problem.

    Contains the two best options, the real trade-off, the recommendation,
    and the exact decision needed. Backed by a machine receipt.
    """
    conflict_id: str
    decision_needed: str
    option_a_id: str
    option_b_id: str
    tradeoff_summary: str
    recommendation: str
    exact_authority_sought: str
    what_we_know: tuple[str, ...] = ()
    what_we_dont_know: tuple[str, ...] = ()
    why_naya_cannot_decide: str = ""
    while_waiting: tuple[str, ...] = ()
    # Machine receipt fields.
    affected_groups: tuple[str, ...] = ()
    policy_version: str = "CURRENT"
    evidence_refs: tuple[str, ...] = ()
    deadline_utc: str = ""
    created_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


def build_escalation_packet(*,
                            survivors: list[DecisionOption],
                            conflict_id: str,
                            route: str,
                            affected_groups: tuple[str, ...] = (),
                            policy_version: str = "CURRENT",
                            evidence_refs: tuple[str, ...] = (),
                            deadline_utc: str = "") -> EscalationPacket:
    """Build the compact escalation packet for the top two survivors.

    Presents the smallest unresolved choice with analysis done — never
    dumps the whole problem on the human.
    """
    if len(survivors) >= 2:
        opt_a, opt_b = survivors[0], survivors[1]
    elif len(survivors) == 1:
        opt_a, opt_b = survivors[0], survivors[0]
    else:
        opt_a = opt_b = None

    # Derive the trade-off from the comparability assessment.
    tradeoff = "No surviving options to compare."
    know: list[str] = []
    if opt_a is not None and opt_b is not None and opt_a.option_id != opt_b.option_id:
        comp = compare_options(opt_a, opt_b)
        a_adv = ", ".join(comp.a_better) or "none"
        b_adv = ", ".join(comp.b_better) or "none"
        tradeoff = (
            f"{opt_a.option_id} is stronger on: {a_adv}. "
            f"{opt_b.option_id} is stronger on: {b_adv}. "
            f"Assessment: {comp.verdict}."
        )
        know = [
            f"Both options passed all hard LAW gates.",
            f"Comparability: {comp.verdict}.",
        ]

    return EscalationPacket(
        conflict_id=conflict_id,
        decision_needed=(
            "Choose which legitimate interest takes precedence, or authorize "
            "further design search. No approved priority covers this trade-off."
            if route == ROUTE_ASK else
            f"Routing decision: {route}."
        ),
        option_a_id=opt_a.option_id if opt_a else "none",
        option_b_id=opt_b.option_id if opt_b else "none",
        tradeoff_summary=tradeoff,
        recommendation=(
            "Select the option aligned with the authorized strategic priority; "
            "if none is authorized, request an explicit priority decision — "
            "not approval for an arbitrary score."
        ),
        exact_authority_sought=(
            "Human decision on which legitimate interest takes precedence "
            "for this consequential trade-off."
            if route == ROUTE_ASK else ""
        ),
        what_we_know=tuple(know),
        what_we_dont_know=(
            "No further material empirical question is expected to determine "
            "which legitimate interest should take precedence.",
        ),
        why_naya_cannot_decide=(
            "No approved priority covers this consequential value trade-off; "
            "inventing one would be manufacturing moral authority."
        ),
        while_waiting=(
            "Preserve the current lawful baseline.",
            "Continue work that does not depend on the unresolved choice.",
        ),
        affected_groups=affected_groups,
        policy_version=policy_version,
        evidence_refs=evidence_refs,
        deadline_utc=deadline_utc,
    )


# ---------------------------------------------------------------------------
# 7. SIMPLE OPERATING SHORTHAND
# ---------------------------------------------------------------------------

# UNDERSTAND → GATE → THINK → ACT/INVESTIGATE/TEST/ASK/REFUSE → VERIFY → LEARN
SHORTHAND_STAGES = (
    "UNDERSTAND",
    "GATE",
    "THINK",
    "DECIDE",   # ACT | INVESTIGATE | TEST | ASK | REFUSE
    "VERIFY",
    "LEARN",
)

# The five questions every Naya asks, in order.
FIVE_QUESTIONS = (
    "Is it allowed? If no, refuse.",
    "Do I understand enough? If not, investigate.",
    "Can I safely test it? If authorized, test.",
    "Does the decision belong to a human? If yes, ask.",
    "Otherwise, what is the wisest authorized action? Do it, verify, learn.",
)


def five_question_routing(*,
                          allowed: bool | None,
                          understood: bool,
                          safe_test_available: bool,
                          belongs_to_human: bool) -> str:
    """The five questions as executable routing. Fail-closed on unknown.

    allowed=None means the authority boundary is unclear -> must NOT
    assume permission (per the Genuine Ambiguity Rule).
    """
    if allowed is False:
        return ROUTE_REFUSE
    if allowed is None:
        # Ambiguous authority: escalate only that precise issue.
        return ROUTE_ASK
    if not understood:
        return ROUTE_READ_MORE
    if safe_test_available:
        return ROUTE_ACT_EXPERIMENT
    if belongs_to_human:
        return ROUTE_ASK
    return ROUTE_ACT
