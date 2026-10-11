"""
conflict_resolution.py — Law of One: Conflict Resolution Engine.

Implements Shawn's intel (2026-10-11) as machine-enforced code:
  - "No person is expendable. No serious harm disappears inside an average."
  - "Before choosing between competing harms, seek a design that removes the conflict."
  - "Never sacrifice a meaningful difference for the convenience of a single score."

This module EXTENDS the existing decision process — it does not create a
competing value engine. Law 11 hard gates run first (typed_action.py).
Value Calculus V2.1 scoring runs after (value_calculus.py). This module
sits between them as the Conflict-Resolution Search phase.

COMPONENTS:
  1. Resolve Before Trade (mandatory machine invariant):
     Before selecting an action with material adverse effects on an affected
     group, the decision record must show reasonable alternatives were considered.
  2. Pareto improvement test: ΔW_g >= 0 for ALL groups, genuine improvement
     for >= 1. Per-group, never aggregate.
  3. Third-design search: six systematic strategies for finding alternatives
     that eliminate the conflict rather than administering it.
  4. No-worse-off standard: three claims (strict Pareto / multidimensional
     no-worsening / practically no worse off). Outcome vectors Δ_{g,d,t}
     per group/dimension/horizon. Never auto-summed. Incomparability is honest.
  5. Five anti-laundering safeguards (machine-enforced):
     group-average, dimension, time-horizon, measurement, statistical-confidence.
  6. Governed impact matrix: attached to candidates and receipts.

All assessments fail closed. Unknown is not safe. Unknown is not zero.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


# ---------------------------------------------------------------------------
# Canonical constants
# ---------------------------------------------------------------------------

# No-worse-off claim levels (strongest claim the evidence supports).
CLAIM_STRICT_PARETO = "STRICT_PARETO"              # every group no worse off, >=1 better
CLAIM_MULTIDIMENSIONAL = "MULTIDIMENSIONAL"        # no important dimension deteriorates
CLAIM_PRACTICAL = "PRACTICAL"                      # deterioration below preapproved limits

# Assessment verdicts (analytical labels; do NOT replace LAW verdicts).
VERDICT_STRICT_SUPPORTED = "STRICT_NO_WORSENING_SUPPORTED"
VERDICT_PRACTICAL_SUPPORTED = "PRACTICAL_NO_WORSENING_SUPPORTED"
VERDICT_INCONCLUSIVE = "INCONCLUSIVE"
VERDICT_WORSENING = "WORSENING_SUPPORTED"
VERDICT_PENDING_WINDOW = "PENDING_WINDOW"
VERDICT_PROHIBITED = "PROHIBITED"

# Comparability assessments (feed ACT/READ_MORE/ASK/REFUSE, don't replace them).
COMPARE_DOMINATES = "DOMINATES"
COMPARE_INCOMPARABLE = "INCOMPARABLE"
COMPARE_UNKNOWN = "UNKNOWN"
COMPARE_PROHIBITED = "PROHIBITED"

# Third-design search strategies.
STRATEGY_REDESIGN = "redesign"              # remove the underlying cause
STRATEGY_DECOUPLE = "decouple"              # different technical pathways
STRATEGY_ACCOMMODATE = "accommodate"        # preserve disadvantaged users' needs
STRATEGY_REDUCE_EXPOSURE = "reduce_exposure"  # narrower scope/duration
STRATEGY_REDISTRIBUTE = "redistribute"      # additional capacity/support
STRATEGY_MITIGATE = "mitigate"              # prevention, recovery, accountability

ALL_STRATEGIES = (
    STRATEGY_REDESIGN, STRATEGY_DECOUPLE, STRATEGY_ACCOMMODATE,
    STRATEGY_REDUCE_EXPOSURE, STRATEGY_REDISTRIBUTE, STRATEGY_MITIGATE,
)

# Observation states for delayed effects.
OBS_COMPLETE = "complete"
OBS_PENDING = "pending"
OBS_INCOMPLETE = "incomplete"


# ---------------------------------------------------------------------------
# Core data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AffectedGroup:
    """A group affected by a proposed action.

    group_id: stable identifier (e.g. "screen_reader_users", "main_users")
    description: human-readable, for audit only
    size_estimate: approximate count, or None if unknown.
        NEVER used to weight harm — size informs exposure, not worth.
    is_vulnerable: True if the group has reduced ability to avoid harm
        or report it (triggers heightened scrutiny).
    """
    group_id: str
    description: str = ""
    size_estimate: int | None = None
    is_vulnerable: bool = False


@dataclass(frozen=True)
class OutcomeCell:
    """One group-dimension-horizon comparison: Δ_{g,d,t}(a).

    The atomic unit of honest measurement. Never auto-summed with other cells.

    Fields:
      group_id: which group
      dimension: outcome dimension (accessibility, privacy, speed, safety, ...)
      horizon: time horizon ("immediate", "30d", "6mo", "cumulative")
      unit: measurement unit, oriented so HIGHER IS BETTER
      baseline_value: expected outcome under declared baseline Y(b)
      action_value: expected outcome under proposed action Y(a)
      lower_bound: justified lower uncertainty bound on (action - baseline)
      upper_bound: justified upper uncertainty bound on (action - baseline)
      tolerance: preapproved max permissible deterioration (epsilon).
          Must be approved BEFORE results examined. None = zero tolerance.
      rights_protected: True if this dimension is a protected right
          (tolerance cannot make violations permissible).
      evidence_quality: "strong" | "adequate" | "weak" | "missing"
      measurement_limitations: free text describing what's unmeasured
      observation_status: complete | pending | incomplete
      tail_severity: worst credible outcome description, or None
    """
    group_id: str
    dimension: str
    horizon: str
    unit: str
    baseline_value: float | None = None
    action_value: float | None = None
    lower_bound: float | None = None
    upper_bound: float | None = None
    tolerance: float | None = None
    rights_protected: bool = False
    evidence_quality: str = "missing"
    measurement_limitations: str = ""
    observation_status: str = OBS_INCOMPLETE
    tail_severity: str | None = None

    def delta(self) -> float | None:
        """Point estimate of change. None if either value unknown."""
        if self.baseline_value is None or self.action_value is None:
            return None
        return self.action_value - self.baseline_value


@dataclass(frozen=True)
class HarmProfile:
    """H_g(a) = (S, P, I, T, U, E) — full harm profile, never compressed.

    S: severity ("inconvenience" | "substantial" | "injury" | "rights_violation")
    P: probability estimate or interval description
    I: irreversibility ("reversible" | "conditional" | "irreversible")
    T: time horizon and accumulation description
    U: uncertainty description (what's unmeasured)
    E: exposure (how many, how often, how long)
    """
    group_id: str
    severity: str
    probability: str
    irreversibility: str
    timing: str
    uncertainty: str
    exposure: str


@dataclass
class ImpactMatrix:
    """Governed impact matrix for one candidate action.

    Attached to candidates and SmartLedger receipts. One OutcomeCell per
    required group-dimension-horizon comparison.

    threshold_version: version of the governing thresholds used.
        Preserved so "negligible" can't be redefined after bad results.
    """
    action_id: str
    cells: list[OutcomeCell] = field(default_factory=list)
    harm_profiles: list[HarmProfile] = field(default_factory=list)
    threshold_version: str = "v1"
    baseline_description: str = ""

    def add_cell(self, cell: OutcomeCell) -> None:
        self.cells.append(cell)

    def cells_for_group(self, group_id: str) -> list[OutcomeCell]:
        return [c for c in self.cells if c.group_id == group_id]


# ---------------------------------------------------------------------------
# Anti-laundering safeguards (all machine-enforced, all fail closed)
# ---------------------------------------------------------------------------

@dataclass
class LaunderingCheck:
    """Result of one anti-laundering safeguard."""
    safeguard: str
    passed: bool
    reason: str


def check_no_group_average_laundering(matrix: ImpactMatrix) -> LaunderingCheck:
    """Every affected group must have its OWN cells. No group may be
    represented only through an aggregate or average.

    Fails if: any group referenced in harm_profiles lacks dedicated cells,
    or if a cell's group_id is an aggregate ("all_users") without
    corresponding per-group breakdowns.
    """
    profile_groups = {p.group_id for p in matrix.harm_profiles}
    cell_groups = {c.group_id for c in matrix.cells}
    missing = profile_groups - cell_groups
    if missing:
        return LaunderingCheck(
            "group_average", False,
            f"Groups in harm profiles lack dedicated outcome cells: {sorted(missing)}. "
            "A favorable average cannot substitute for per-group measurement.",
        )
    # Aggregate-only check: if "all_users" exists but no specific groups, flag.
    if cell_groups == {"all_users"} and len(profile_groups) > 1:
        return LaunderingCheck(
            "group_average", False,
            "Only aggregate 'all_users' cells present; per-group breakdown required.",
        )
    return LaunderingCheck("group_average", True, "All profiled groups have dedicated cells.")


def check_no_dimension_laundering(matrix: ImpactMatrix) -> LaunderingCheck:
    """Dimensions must be preserved separately. A cell may not claim that
    improvement in one dimension compensates deterioration in another.

    Fails if: any cell has empty dimension (dimension must be named), or
    if the matrix contains a synthetic "composite" or "total" dimension.
    """
    for cell in matrix.cells:
        if not cell.dimension or not cell.dimension.strip():
            return LaunderingCheck(
                "dimension", False,
                f"Cell for group {cell.group_id} has unnamed dimension. "
                "Every measured outcome must name its dimension.",
            )
        if cell.dimension.lower() in ("composite", "total", "aggregate", "overall"):
            return LaunderingCheck(
                "dimension", False,
                f"Synthetic dimension '{cell.dimension}' detected. Dimensions "
                "must be preserved separately; speed cannot compensate privacy.",
            )
    return LaunderingCheck("dimension", True, "All dimensions named and preserved separately.")


def check_no_time_horizon_laundering(matrix: ImpactMatrix) -> LaunderingCheck:
    """Immediate, cumulative, and longer-term effects must be reported.
    Short-term success cannot certify unobserved future consequences.

    Fails if: matrix has cells but ALL are "immediate" horizon while any
    harm profile mentions delayed/cumulative effects.
    """
    if not matrix.cells:
        return LaunderingCheck("time_horizon", True, "No cells; nothing to check.")
    horizons = {c.horizon for c in matrix.cells}
    delayed_mentioned = any(
        any(w in (p.timing + " " + p.uncertainty).lower()
            for w in ("delay", "cumulat", "long-term", "long term", "month", "year"))
        for p in matrix.harm_profiles
    )
    if delayed_mentioned and horizons == {"immediate"}:
        return LaunderingCheck(
            "time_horizon", False,
            "Harm profiles mention delayed/cumulative effects but all cells "
            "are 'immediate' horizon. Longer horizons required.",
        )
    return LaunderingCheck("time_horizon", True, "Horizons cover stated timing concerns.")


def check_no_measurement_laundering(matrix: ImpactMatrix) -> LaunderingCheck:
    """Missing data must stay visible. Cells with weak/missing evidence
    cannot support a no-worsening claim.

    Fails if: any cell has evidence_quality "missing" or "weak" AND
    observation_status "complete" (claiming completeness without evidence).
    """
    for cell in matrix.cells:
        if cell.evidence_quality in ("missing", "weak") and cell.observation_status == OBS_COMPLETE:
            return LaunderingCheck(
                "measurement", False,
                f"Cell {cell.group_id}/{cell.dimension}/{cell.horizon} claims "
                f"complete observation with {cell.evidence_quality} evidence. "
                "Missing data must stay visible.",
            )
    return LaunderingCheck("measurement", True, "No completeness claims on weak evidence.")


def check_no_statistical_confidence_laundering(
    matrix: ImpactMatrix,
    simultaneous_method: str | None = None,
) -> LaunderingCheck:
    """Multiple comparisons need a simultaneous method. Checking dozens of
    outcomes with separate intervals does not give simultaneous assurance.

    Fails if: more than 5 cells and no simultaneous_method declared.
    """
    if len(matrix.cells) > 5 and not simultaneous_method:
        return LaunderingCheck(
            "statistical_confidence", False,
            f"{len(matrix.cells)} comparisons without a declared simultaneous "
            "inference method. Predeclare the multiple-comparison method.",
        )
    return LaunderingCheck(
        "statistical_confidence", True,
        "Simultaneous inference handled." if simultaneous_method else "Few enough comparisons.",
    )


def run_all_laundering_checks(
    matrix: ImpactMatrix,
    simultaneous_method: str | None = None,
) -> list[LaunderingCheck]:
    """Run all five anti-laundering safeguards. All must pass."""
    return [
        check_no_group_average_laundering(matrix),
        check_no_dimension_laundering(matrix),
        check_no_time_horizon_laundering(matrix),
        check_no_measurement_laundering(matrix),
        check_no_statistical_confidence_laundering(matrix, simultaneous_method),
    ]


# ---------------------------------------------------------------------------
# No-worse-off assessment
# ---------------------------------------------------------------------------

@dataclass
class NoWorseOffAssessment:
    """Result of the no-worse-off test on an impact matrix."""
    verdict: str
    claim_level: str | None          # strongest claim supported, or None
    failed_cells: list[OutcomeCell]   # cells that violate their tolerance
    inconclusive_cells: list[OutcomeCell]  # bounds overlap meaningful deterioration
    pending_cells: list[OutcomeCell]  # observation incomplete
    laundering: list[LaunderingCheck]
    notes: list[str]


def _cell_tolerance(cell: OutcomeCell) -> float:
    """Effective tolerance. None (unapproved) means zero tolerance.
    Rights-protected dimensions always get zero tolerance."""
    if cell.rights_protected:
        return 0.0
    return cell.tolerance if cell.tolerance is not None else 0.0


def assess_no_worse_off(
    matrix: ImpactMatrix,
    simultaneous_method: str | None = None,
) -> NoWorseOffAssessment:
    """Apply the no-worse-off test: L^{sim}_{g,d,t} >= -epsilon for all cells.

    Verdict priority:
      PROHIBITED > WORSENING > PENDING_WINDOW > INCONCLUSIVE > supported claims.
    """
    notes: list[str] = []
    laundering = run_all_laundering_checks(matrix, simultaneous_method)
    failed_laundering = [c for c in laundering if not c.passed]
    for c in failed_laundering:
        notes.append(f"LAUNDERING_FAIL[{c.safeguard}]: {c.reason}")

    failed: list[OutcomeCell] = []
    inconclusive: list[OutcomeCell] = []
    pending: list[OutcomeCell] = []

    for cell in matrix.cells:
        tol = _cell_tolerance(cell)
        # Rights violations are prohibitions, not tolerances.
        if cell.rights_protected and cell.lower_bound is not None and cell.lower_bound < 0:
            notes.append(
                f"RIGHTS cell {cell.group_id}/{cell.dimension}: lower bound "
                f"{cell.lower_bound} < 0. Hard boundary — tolerance cannot apply."
            )
            failed.append(cell)
            continue
        if cell.observation_status != OBS_COMPLETE:
            pending.append(cell)
            continue
        if cell.lower_bound is None:
            # Unknown bound: cannot support no-worsening. Unknown is not zero.
            inconclusive.append(cell)
            notes.append(
                f"Cell {cell.group_id}/{cell.dimension}/{cell.horizon}: "
                "lower bound unknown — cannot support no-worsening claim."
            )
            continue
        if cell.lower_bound < -tol:
            # Taxonomy (per spec): a WIDE interval whose lower bound violates
            # tolerance is INCONCLUSIVE, not WORSENING — unless the point
            # estimate itself shows deterioration. "A study with wide
            # uncertainty centered on zero does not establish harmlessness"
            # — and it does not establish harm either. A NARROW interval
            # with a violating lower bound is meaningful evidence -> WORSENING.
            point = cell.delta()
            ub = cell.upper_bound if cell.upper_bound is not None else cell.lower_bound
            width = ub - cell.lower_bound
            # Wide if the interval spans more than twice the tolerance
            # (or more than 1.0 unit when tolerance is zero).
            is_wide = width > max(2 * tol, 1.0)
            if is_wide and (point is None or point >= -tol):
                inconclusive.append(cell)
                notes.append(
                    f"Cell {cell.group_id}/{cell.dimension}/{cell.horizon}: "
                    f"lower bound {cell.lower_bound} below tolerance {-tol}, "
                    f"but interval width {width:.2f} is wide and point estimate "
                    f"{point} does not show worsening. INCONCLUSIVE "
                    f"(cannot claim harm from uncertainty)."
                )
            else:
                failed.append(cell)
        elif cell.lower_bound < 0:
            # Within tolerance but still possibly deteriorating: note it.
            notes.append(
                f"Cell {cell.group_id}/{cell.dimension}/{cell.horizon}: "
                f"lower bound {cell.lower_bound} within tolerance {tol}."
            )

    # Determine verdict.
    if any(c.rights_protected and c in failed for c in matrix.cells):
        verdict = VERDICT_PROHIBITED
        claim = None
    elif failed_laundering:
        verdict = VERDICT_INCONCLUSIVE
        claim = None
        notes.append("Anti-laundering safeguards failed; no claim can be supported.")
    elif failed:
        verdict = VERDICT_WORSENING
        claim = None
    elif pending:
        verdict = VERDICT_PENDING_WINDOW
        claim = None
    elif inconclusive:
        verdict = VERDICT_INCONCLUSIVE
        claim = None
    else:
        # All cells pass. Determine strongest claim.
        all_zero_tol = all(_cell_tolerance(c) == 0.0 for c in matrix.cells)
        all_bounds_nonneg = all(
            c.lower_bound is not None and c.lower_bound >= 0.0 for c in matrix.cells
        )
        if all_zero_tol and all_bounds_nonneg:
            verdict = VERDICT_STRICT_SUPPORTED
            claim = CLAIM_STRICT_PARETO
        elif all_bounds_nonneg:
            verdict = VERDICT_STRICT_SUPPORTED
            claim = CLAIM_MULTIDIMENSIONAL
        else:
            verdict = VERDICT_PRACTICAL_SUPPORTED
            claim = CLAIM_PRACTICAL

    return NoWorseOffAssessment(
        verdict=verdict,
        claim_level=claim,
        failed_cells=failed,
        inconclusive_cells=inconclusive,
        pending_cells=pending,
        laundering=laundering,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Pareto improvement test (per-group, never aggregate)
# ---------------------------------------------------------------------------

@dataclass
class ParetoResult:
    """Outcome of the Pareto improvement test."""
    is_pareto_improvement: bool
    groups_no_worse: list[str]
    groups_worse: list[str]
    groups_improved: list[str]
    groups_unknown: list[str]
    notes: list[str]


def check_pareto_improvement(
    matrix: ImpactMatrix,
    welfare_dimensions: list[str] | None = None,
) -> ParetoResult:
    """Test ΔW_g >= 0 for every group, genuine improvement for >= 1.

    Uses the welfare dimensions (default: all dimensions present).
    A group is "worse" if ANY of its welfare cells has a negative point
    estimate OR a negative lower bound. A group is "improved" if any cell
    is genuinely positive (lower bound > 0). Unknown bounds -> unknown group.

    "We haven't found a Pareto improvement" != "none exists" — this test
    reports what the evidence supports, nothing more.
    """
    notes: list[str] = []
    dims = welfare_dimensions
    groups = sorted({c.group_id for c in matrix.cells})

    no_worse: list[str] = []
    worse: list[str] = []
    improved: list[str] = []
    unknown: list[str] = []

    for g in groups:
        cells = [c for c in matrix.cells if c.group_id == g]
        if dims:
            cells = [c for c in cells if c.dimension in dims]
        if not cells:
            unknown.append(g)
            continue
        has_negative = False
        has_unknown = False
        has_genuine_improvement = False
        for c in cells:
            d = c.delta()
            if c.lower_bound is None and d is None:
                has_unknown = True
            elif c.lower_bound is not None and c.lower_bound < 0:
                has_negative = True
            elif d is not None and d < 0:
                has_negative = True
            if c.lower_bound is not None and c.lower_bound > 0:
                has_genuine_improvement = True
        if has_negative:
            worse.append(g)
        elif has_unknown:
            unknown.append(g)
            notes.append(f"Group {g}: unknown bounds — cannot confirm no-worse-off.")
        else:
            no_worse.append(g)
            if has_genuine_improvement:
                improved.append(g)

    is_pareto = len(worse) == 0 and len(unknown) == 0 and len(improved) >= 1
    if worse:
        notes.append(f"Groups worse off: {worse}. Not a Pareto improvement.")
    if unknown:
        notes.append(f"Groups with unknown outcomes: {unknown}. Evidence insufficient.")
    if not improved and is_pareto:
        notes.append("No group genuinely improved; no-worse-off but not an improvement.")

    return ParetoResult(
        is_pareto_improvement=is_pareto,
        groups_no_worse=no_worse,
        groups_worse=worse,
        groups_improved=improved,
        groups_unknown=unknown,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Comparability assessment (typed, never forced into one number)
# ---------------------------------------------------------------------------

@dataclass
class ComparabilityResult:
    """Typed comparison of two candidates."""
    assessment: str
    dominating: str | None       # action_id if DOMINATES
    notes: list[str]


def assess_comparability(
    matrix_a: ImpactMatrix,
    matrix_b: ImpactMatrix,
) -> ComparabilityResult:
    """Compare two candidates cell-by-cell.

    A dominates B only if Δ_k(A,B) >= 0 for every shared (group, dimension,
    horizon) AND at least one is genuinely better (lower bound > 0).
    Otherwise INCOMPARABLE (honest) or UNKNOWN (insufficient evidence).
    PROHIBITED if either violates a hard boundary.
    """
    notes: list[str] = []

    # Hard boundary check first.
    for m, label in ((matrix_a, "A"), (matrix_b, "B")):
        for c in m.cells:
            if c.rights_protected and c.lower_bound is not None and c.lower_bound < 0:
                return ComparabilityResult(
                    COMPARE_PROHIBITED, None,
                    [f"Candidate {label} violates protected right "
                     f"({c.group_id}/{c.dimension}). REFUSE regardless of advantages."],
                )

    # Build comparable cell pairs on (group, dimension, horizon).
    def key(c: OutcomeCell) -> tuple[str, str, str]:
        return (c.group_id, c.dimension, c.horizon)

    b_map = {key(c): c for c in matrix_b.cells}
    pairs: list[tuple[OutcomeCell, OutcomeCell]] = []
    for ca in matrix_a.cells:
        cb = b_map.get(key(ca))
        if cb is not None:
            pairs.append((ca, cb))

    if not pairs:
        return ComparabilityResult(
            COMPARE_UNKNOWN, None,
            ["No shared (group, dimension, horizon) cells — cannot compare."],
        )

    # Check for unknown bounds.
    for ca, cb in pairs:
        if ca.lower_bound is None or cb.upper_bound is None:
            notes.append(
                f"Pair {key(ca)}: insufficient bounds for comparison."
            )
            return ComparabilityResult(COMPARE_UNKNOWN, None, notes)

    # Dominance: A >= B everywhere, strictly better somewhere.
    a_dominates = True
    a_strictly_better = False
    b_dominates = True
    b_strictly_better = False
    for ca, cb in pairs:
        # A vs B on this cell: A's lower - B's upper (conservative).
        diff_lo = (ca.lower_bound or 0.0) - (cb.upper_bound or 0.0)
        diff_hi = (ca.upper_bound or 0.0) - (cb.lower_bound or 0.0)
        if diff_lo < 0:
            a_dominates = False
        if diff_lo > 0:
            a_strictly_better = True
        if diff_hi > 0:
            b_dominates = False
        if diff_hi < 0:
            b_strictly_better = True

    if a_dominates and a_strictly_better:
        return ComparabilityResult(COMPARE_DOMINATES, matrix_a.action_id, notes)
    if b_dominates and b_strictly_better:
        return ComparabilityResult(COMPARE_DOMINATES, matrix_b.action_id, notes)
    notes.append(
        "Neither candidate dominates. Different legitimate advantages without "
        "an established exchange rate. INCOMPARABLE is honest — apply approved "
        "priority, seek a better design, or escalate."
    )
    return ComparabilityResult(COMPARE_INCOMPARABLE, None, notes)


# ---------------------------------------------------------------------------
# Third-design search (six strategies)
# ---------------------------------------------------------------------------

@dataclass
class AlternativeDesign:
    """A candidate alternative generated by the third-design search."""
    design_id: str
    strategy: str                  # one of ALL_STRATEGIES
    description: str
    expected_effect: str           # what conflict it removes/reduces
    evidence: str = ""             # why we believe it works
    discarded: bool = False
    discard_reason: str = ""


@dataclass
class DesignSearchRecord:
    """Machine receipt for the Resolve Before Trade invariant.

    BEFORE selecting an action with material adverse effects, this record
    must show reasonable alternatives were considered.
    """
    action_id: str
    alternatives: list[AlternativeDesign] = field(default_factory=list)
    strategies_attempted: list[str] = field(default_factory=list)
    search_budget: str = "standard"   # "light" | "standard" | "thorough"
    residual_conflict: str = ""
    pareto_found: bool = False

    def record_alternative(self, alt: AlternativeDesign) -> None:
        self.alternatives.append(alt)
        if alt.strategy not in self.strategies_attempted:
            self.strategies_attempted.append(alt.strategy)

    def alternatives_considered(self) -> bool:
        """The machine invariant: were reasonable alternatives considered?"""
        return len(self.alternatives) >= 1 and len(self.strategies_attempted) >= 1

    def uncovered_strategies(self) -> list[str]:
        return [s for s in ALL_STRATEGIES if s not in self.strategies_attempted]


def check_resolve_before_trade(
    record: DesignSearchRecord,
    has_material_adverse_effects: bool,
    severity: str = "standard",
) -> tuple[bool, str]:
    """Enforce the Resolve Before Trade machine invariant.

    Returns (satisfied, reason). Fails closed: if the action has material
    adverse effects and no alternatives were considered, the invariant is
    violated -> NEEDS_EVIDENCE.
    """
    if not has_material_adverse_effects:
        return True, "No material adverse effects; invariant does not apply."
    if not record.alternatives_considered():
        return False, (
            "RESOLVE_BEFORE_TRADE violated: action has material adverse effects "
            "but no alternative designs were considered. Decision record must show "
            "reasonable lawful, lower-harm, Pareto-improving alternatives were examined."
        )
    # Thoroughness scales with severity.
    if severity in ("severe", "irreversible") and len(record.strategies_attempted) < 3:
        return False, (
            f"RESOLVE_BEFORE_TRADE: severe/irreversible harm requires >= 3 search "
            f"strategies; only {len(record.strategies_attempted)} attempted "
            f"({record.strategies_attempted})."
        )
    return True, (
        f"Resolve Before Trade satisfied: {len(record.alternatives)} alternatives "
        f"across {len(record.strategies_attempted)} strategies."
    )


# ---------------------------------------------------------------------------
# Decision record: the complete machine receipt
# ---------------------------------------------------------------------------

@dataclass
class ConflictDecisionRecord:
    """Complete machine receipt for a conflict-resolution decision.

    Required evidence per the invariant: affected parties, baseline, candidate
    designs, subgroup impacts, unknowns, discarded options, remaining conflict,
    governing authorization.
    """
    action_id: str
    groups: list[AffectedGroup] = field(default_factory=list)
    impact_matrix: ImpactMatrix | None = None
    design_search: DesignSearchRecord | None = None
    no_worse_off: NoWorseOffAssessment | None = None
    pareto: ParetoResult | None = None
    comparability: ComparabilityResult | None = None
    authority_ref: str | None = None
    threshold_version: str = "v1"
    decision: str = "UNDECIDED"      # ADMISSIBLE | NEEDS_EVIDENCE | NEEDS_AUTHORITY | PROHIBITED
    rationale: list[str] = field(default_factory=list)

    def is_complete(self) -> tuple[bool, list[str]]:
        """Check the record has all required evidence. Returns (ok, gaps)."""
        gaps: list[str] = []
        if not self.groups:
            gaps.append("affected parties not identified")
        if self.impact_matrix is None:
            gaps.append("impact matrix missing")
        if self.design_search is None:
            gaps.append("design search record missing")
        if self.no_worse_off is None:
            gaps.append("no-worse-off assessment missing")
        return (len(gaps) == 0, gaps)
