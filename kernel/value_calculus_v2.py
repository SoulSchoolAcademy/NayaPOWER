"""NayaPOWER Decision Value Calculus V2.1 — deterministic reference implementation.

Spec authority: SoulSchoolAcademy/NayaPOWER issue #1182,
"DIRECTOR-APPROVED DIRECTION — Decision Value Calculus V2.1 baseline candidate"
(OFFICIAL DIRECTION / CANDIDATE SPEC — not production-proven),
plus the R1–R6 red-team patch (candidate definitions).

Pipeline (domain-general root-core pattern):

    RESOLVE -> GATE -> SCORE -> COMPARE -> SELECT -> ACT/ESCALATE
        -> OBSERVE -> VERIFY -> LEDGER -> LEARN -> RECALIBRATE

This module covers RESOLVE through SELECT plus the OBSERVE/VERIFY/LEDGER
receipt and calibration-error math. It is intentionally dependency-free and
fully deterministic: identical inputs produce identical outputs.

Key invariants (from the spec):
  - hard boundaries precede optimization; value never creates authority
  - Q measures decision soundness ONLY — value/PV is never a Q dimension
  - value is baseline-relative: dV(a|b) = PV(a) - PV(b); dV(b|b) = 0
  - expected value never averages away catastrophic tail risk
  - one unknown critical fact cannot be averaged away by certain minor facts
  - predicted value is not actual value; verified outcomes calibrate the math
  - human worth is never reduced to a scalar score (see kernel/network_value.py)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence
import math

ENGINE_VERSION = "VALUE-CALCULUS-V2.1.0"
SPEC_VERSION = "decision-value-calculus-v2.1.0"
SPEC_REF = "SoulSchoolAcademy/NayaPOWER#1182 V2.1 baseline candidate"

# ---------------------------------------------------------------------------
# Gate states
# ---------------------------------------------------------------------------

PROHIBITED = "PROHIBITED"
NEEDS_AUTHORITY = "NEEDS_AUTHORITY"
NEEDS_EVIDENCE = "NEEDS_EVIDENCE"
ADMISSIBLE = "ADMISSIBLE"
GATE_STATES = (PROHIBITED, NEEDS_AUTHORITY, NEEDS_EVIDENCE, ADMISSIBLE)

# Strictness ordering: higher number = stricter (more blocking).
_GATE_STRICTNESS = {
    ADMISSIBLE: 0,
    NEEDS_EVIDENCE: 1,
    NEEDS_AUTHORITY: 2,
    PROHIBITED: 3,
}

# ---------------------------------------------------------------------------
# Q dimensions (decision soundness only — value magnitude is NOT a dimension)
# ---------------------------------------------------------------------------

Q_DIMS = (
    "objective_fit",
    "evidence_sufficiency",
    "applicability",
    "robustness",
    "reversibility",
    "blast_containment",
    "simplicity",
)

# Dimensions whose weakness can cap autonomous readiness regardless of mean.
Q_CRITICAL_DIMS = ("objective_fit", "evidence_sufficiency")

Q_BAND_DELIGHT = 9.5
Q_BAND_ACCEPT = 9.0
Q_BAND_BELOW = 7.0

# ---------------------------------------------------------------------------
# Versioned parameter registry (N2 fix: no silent threshold drift)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class V21Params:
    """Every weight, threshold and policy constant, versioned and ownable.

    Decision-time deviation from these values without recorded authority
    forces the outcome to BRIEF (NEEDS_AUTHORITY semantics).
    """

    version: str = SPEC_VERSION
    owner: str = "human-director"
    scope: str = "global-default"

    q_weights: Mapping[str, float] = field(default_factory=lambda: {
        "objective_fit": 0.20,
        "evidence_sufficiency": 0.20,
        "applicability": 0.15,
        "robustness": 0.15,
        "reversibility": 0.10,
        "blast_containment": 0.10,
        "simplicity": 0.10,
    })
    q_critical_cap: float = 8.9          # max Q when a critical dim scores < 7
    q_critical_min: float = 7.0

    c_agg_floor: float = 0.80           # low-risk autonomous hypothesis
    c_critical_floor: float = 0.75

    evidence_k_low: int = 5             # R6: minimum observations, low stakes
    evidence_k_consequential: int = 20  # R6: minimum observations, consequential

    dominance_margin: float = 0.25      # R1: relative margin hypothesis
    reversibility_autonomy_min: float = 0.70   # R1: below -> non-autonomous
    reversibility_consequential_min: float = 0.85

    lcb_z: float = 1.0                  # V_safe reference-method constant
    uncertainty_scale: float = 9.0      # anchor scale for confidence penalty
    material_probability: float = 1e-6  # below = modeling noise, not license

    # R4: seed tau table — max P(unacceptable harm) per scope class.
    # Candidate hypotheses; the system may never loosen them by itself.
    tau_scope: Mapping[str, float] = field(default_factory=lambda: {
        "physical_safety": 0.0,
        "rights": 0.0,
        "financial": 0.001,
        "data_loss": 0.001,
        "reputational": 0.01,
        "informational": 0.05,
        "compute_waste": 0.10,
    })

    # R5: observation windows in days, by harm category.
    windows_days: Mapping[str, float] = field(default_factory=lambda: {
        "reversible_low": 1.0,
        "financial": 7.0,
        "irreversible_third_party": 30.0,
        "physical_rights": 90.0,
    })

    calibration_learn_threshold: float = 1.0  # |dV_pred - dV_actual| -> LEARN


DEFAULT_PARAMS = V21Params()


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


# ---------------------------------------------------------------------------
# Core data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PVComponents:
    """Evidence-bound estimates: PV(a) = B - H - C - R."""
    benefit: float = 0.0
    harm: float = 0.0
    cost: float = 0.0
    risk: float = 0.0

    def total(self) -> float:
        return (_finite(self.benefit, "benefit") - _finite(self.harm, "harm")
                - _finite(self.cost, "cost") - _finite(self.risk, "risk"))


@dataclass(frozen=True)
class Option:
    """One candidate action under evaluation."""
    id: str
    label: str
    q_scores: Mapping[str, float]        # each dim in [0, 10]
    q_confidence: Mapping[str, float]    # each dim in [0, 1]
    pv: PVComponents = field(default_factory=PVComponents)
    pv_confidence: float = 0.5           # aggregate confidence on the PV estimate
    evidence_count: int = 0             # observations backing the estimates
    residual_risk: float = 0.0          # in [0, 1]
    p_unacceptable_harm: Mapping[str, float] = field(default_factory=dict)
    requires_authority: bool = False
    authority_granted: bool = False
    reversibility: float = 1.0           # in [0, 1]
    scope: str = "low"                  # "low" | "consequential"
    synthetic_baseline: bool = False    # injected mandatory candidate
    intent_ambiguous: bool = False


@dataclass(frozen=True)
class DecisionContext:
    objective: str
    baseline: Option
    stakeholders: Sequence[str] = ()
    horizon: str = "declared-per-domain"
    params: V21Params = DEFAULT_PARAMS
    param_authorized_by: Optional[str] = None
    standing_authority_contract: bool = False
    prohibited_harm_classes: Sequence[str] = ("physical_safety", "rights")


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------


def evaluate_gate(option: Option, ctx: DecisionContext) -> dict:
    """Four-state gate. Hard constraints are never scalarized."""
    p = ctx.params
    reasons = []

    # 1. Prohibited harm classes and tau policy (R4).
    for cls in option.p_unacceptable_harm:
        prob = _finite(option.p_unacceptable_harm[cls], f"p_harm[{cls}]")
        tau = p.tau_scope.get(cls)
        if tau is None:
            reasons.append(f"unknown harm class '{cls}' -> treat as PROHIBITED")
            return {"state": PROHIBITED, "reasons": reasons}
        if cls in ctx.prohibited_harm_classes and prob > p.material_probability:
            reasons.append(f"prohibited harm class '{cls}' with material P={prob}")
            return {"state": PROHIBITED, "reasons": reasons}
        if prob > tau:
            if tau == 0.0:
                reasons.append(f"zero-tolerance class '{cls}' exceeded (P={prob})")
                return {"state": PROHIBITED, "reasons": reasons}
            reasons.append(f"P(unacceptable harm|{cls})={prob} > tau={tau}")
            return {"state": NEEDS_AUTHORITY, "reasons": reasons}

    # 2. Authority.
    if option.requires_authority and not option.authority_granted:
        reasons.append("requires authority: not granted")
        return {"state": NEEDS_AUTHORITY, "reasons": reasons}

    # 3. Evidence / data floor (R6). Not rankable on V_safe -> NEEDS_EVIDENCE.
    k = p.evidence_k_consequential if option.scope == "consequential" else p.evidence_k_low
    if option.evidence_count < k:
        reasons.append(f"evidence {option.evidence_count} < k={k} for scope '{option.scope}'")
        return {"state": NEEDS_EVIDENCE, "reasons": reasons}

    reasons.append("no hard-constraint, authority, or evidence blocker")
    return {"state": ADMISSIBLE, "reasons": reasons}


# ---------------------------------------------------------------------------
# Quality (pure decision soundness — value magnitude excluded)
# ---------------------------------------------------------------------------


def score_quality(option: Option, params: V21Params = DEFAULT_PARAMS) -> dict:
    weights = params.q_weights
    if set(weights) != set(Q_DIMS):
        raise ValueError("q_weights must cover exactly the Q dimensions")
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("q_weights must sum to 1")

    dims = {}
    for d in Q_DIMS:
        raw = option.q_scores.get(d)
        if raw is None:
            raise ValueError(f"missing Q dimension '{d}' for option '{option.id}'")
        dims[d] = _finite(raw, f"q[{d}]")
        if not 0.0 <= dims[d] <= 10.0:
            raise ValueError(f"q[{d}] must be in [0, 10]")

    q = sum(weights[d] * dims[d] for d in Q_DIMS)

    # Critical proof gap caps autonomous readiness regardless of the mean.
    critical_min = min(dims[d] for d in Q_CRITICAL_DIMS)
    capped = False
    if critical_min < params.q_critical_min:
        q = min(q, params.q_critical_cap)
        capped = True

    if q >= Q_BAND_DELIGHT:
        band = "DELIGHT"
    elif q >= Q_BAND_ACCEPT:
        band = "ACCEPT"
    elif q >= Q_BAND_BELOW:
        band = "BELOW_STANDARD"
    else:
        band = "REJECT"

    return {"q": q, "band": band, "dims": dims,
            "critical_min": critical_min, "capped": capped}


def confidence(option: Option) -> dict:
    """Aggregate and critical-dimension confidence floors."""
    confs = {}
    for d in Q_DIMS:
        raw = option.q_confidence.get(d)
        if raw is None:
            raise ValueError(f"missing confidence for Q dimension '{d}'")
        confs[d] = _clamp01(_finite(raw, f"c[{d}]"))
    c_agg = sum(confs[d] for d in Q_DIMS) / len(Q_DIMS)
    c_critical = min(confs[d] for d in Q_CRITICAL_DIMS)
    return {"c_agg": c_agg, "c_critical": c_critical, "dims": confs}


# ---------------------------------------------------------------------------
# Value: PV, baseline-relative dV, conservative V_safe, D_verified
# ---------------------------------------------------------------------------


def delta_v(option: Option, baseline: Option) -> float:
    """dV(a|b) = PV(a) - PV(b). dV(b|b) = 0 by definition."""
    return option.pv.total() - baseline.pv.total()


def conservative_value(option: Option, baseline: Option,
                       params: V21Params = DEFAULT_PARAMS) -> dict:
    """V_safe = LCB(dV) - TailRiskPenalty (V2.1 reference method, versioned).

    LCB here: dV_pred - z * (1 - pv_confidence) * uncertainty_scale.
    Tail penalty: max P(unacceptable harm) * anchor scale.
    Expected value never averages away catastrophic tails: any material
    probability in a zero-tolerance class already gated PROHIBITED above;
    residual tail probability still subtracts from V_safe here.
    """
    dv = delta_v(option, baseline)
    z = params.lcb_z
    lcb = dv - z * (1.0 - _clamp01(option.pv_confidence)) * params.uncertainty_scale
    tail_p = max([0.0] + [_finite(v, "p_tail") for v in option.p_unacceptable_harm.values()])
    penalty = tail_p * params.uncertainty_scale
    v_safe = lcb - penalty
    return {"dV_pred": dv, "lcb": lcb, "tail_probability": tail_p,
            "tail_penalty": penalty, "v_safe": v_safe}


def d_verified(delta_v_actual: float) -> float:
    """R2: ladder display anchor. Raw dV is preserved in the ledger."""
    return max(-9.0, min(9.0, _finite(delta_v_actual, "dV_actual")))


def ladder_step(ladder: float, delta_v_actual: float) -> dict:
    d = d_verified(delta_v_actual)
    new_ladder = _finite(ladder, "ladder") + d
    state = "ADVANCING" if d > 0 else ("DEGRADING" if d < 0 else "NEUTRAL")
    return {"d_verified": d, "ladder": new_ladder, "state": state,
            "delta_v_actual": _finite(delta_v_actual, "dV_actual")}


# ---------------------------------------------------------------------------
# Mandatory baselines (N4 fix: the candidate set cannot rig the winner)
# ---------------------------------------------------------------------------


def _mandatory(id_: str, label: str, **kw) -> Option:
    base_q = {d: 8.0 for d in Q_DIMS}
    base_c = {d: 0.6 for d in Q_DIMS}
    base_q.update(kw.pop("q_scores", {}))
    base_c.update(kw.pop("q_confidence", {}))
    return Option(
        id=id_, label=label,
        q_scores=base_q, q_confidence=base_c,
        evidence_count=kw.pop("evidence_count", 5),
        synthetic_baseline=True, **kw,
    )


def inject_mandatory_baselines(candidates: Sequence[Option],
                               ctx: DecisionContext) -> list:
    """Ensure the brief always contains: current course, gather-evidence,
    reversible probe, rollback/revert, and human escalation."""
    ids = {o.id for o in candidates}
    out = list(candidates)
    if ctx.baseline.id not in ids:
        out.append(ctx.baseline)
        ids.add(ctx.baseline.id)
    if "mandatory:gather-evidence" not in ids:
        out.append(_mandatory(
            "mandatory:gather-evidence", "Gather more evidence before acting",
            pv=PVComponents(benefit=0.5, harm=0.0, cost=0.5, risk=0.1),
            pv_confidence=0.7, evidence_count=5, reversibility=1.0,
            q_scores={"evidence_sufficiency": 9.0}))
    if "mandatory:reversible-probe" not in ids:
        out.append(_mandatory(
            "mandatory:reversible-probe", "Run a small reversible probe",
            pv=PVComponents(benefit=1.0, harm=0.1, cost=0.5, risk=0.2),
            pv_confidence=0.6, evidence_count=5, reversibility=1.0))
    if "mandatory:rollback" not in ids:
        out.append(_mandatory(
            "mandatory:rollback", "Rollback / revert to last good state",
            pv=PVComponents(benefit=0.2, harm=0.0, cost=0.3, risk=0.1),
            pv_confidence=0.8, evidence_count=5, reversibility=1.0))
    if "mandatory:escalate" not in ids:
        out.append(_mandatory(
            "mandatory:escalate", "Escalate to human director",
            pv=PVComponents(benefit=0.0, harm=0.0, cost=0.2, risk=0.0),
            pv_confidence=0.9, evidence_count=5, reversibility=1.0,
            requires_authority=True))
    return out

# ---------------------------------------------------------------------------
# Pareto frontier + ranking + relative dominance (R1, R3)
# ---------------------------------------------------------------------------


def pareto_frontier(scored: Sequence[dict]) -> list:
    """scored: dicts with keys id, v_safe, q, residual_risk.

    a dominates b iff a >= b on all three objectives (max V_safe, max Q,
    min residual risk) and strictly better on at least one.
    Deterministic: ties broken by id.
    """
    frontier = []
    for a in scored:
        dominated = False
        for b in scored:
            if b["id"] == a["id"]:
                continue
            ge_v = b["v_safe"] >= a["v_safe"]
            ge_q = b["q"] >= a["q"]
            ge_r = b["residual_risk"] <= a["residual_risk"]
            strict = (b["v_safe"] > a["v_safe"] or b["q"] > a["q"]
                      or b["residual_risk"] < a["residual_risk"])
            if ge_v and ge_q and ge_r and strict:
                dominated = True
                break
        if not dominated:
            frontier.append(a)
    frontier.sort(key=lambda s: (-s["v_safe"], -s["q"], s["residual_risk"], s["id"]))
    return frontier


def relative_dominance(v_first: float, v_second: float, eps: float = 1e-9) -> float:
    """R1: m = (V1 - V2) / max(|V1|, eps). Parameter-free relative margin."""
    v_first = _finite(v_first, "v_first")
    v_second = _finite(v_second, "v_second")
    return (v_first - v_second) / max(abs(v_first), eps)


# ---------------------------------------------------------------------------
# The decision
# ---------------------------------------------------------------------------


def _param_deviation(ctx: DecisionContext) -> bool:
    return ctx.params != DEFAULT_PARAMS and not ctx.param_authorized_by


def decide(candidates: Sequence[Option], ctx: DecisionContext) -> dict:
    """Full V2.1 decision pass. Returns diagnostics, ranking and receipt."""
    params = ctx.params
    options = inject_mandatory_baselines(candidates, ctx)

    per_option = []
    for o in options:
        gate = evaluate_gate(o, ctx)
        q = score_quality(o, params)
        conf = confidence(o)
        cv = conservative_value(o, ctx.baseline, params)
        dv = cv["dV_pred"]
        floors = {
            "c_agg": conf["c_agg"] >= params.c_agg_floor,
            "c_critical": conf["c_critical"] >= params.c_critical_floor,
        }
        rankable = (gate["state"] == ADMISSIBLE and q["q"] >= Q_BAND_ACCEPT
                    and cv["v_safe"] > 0 and all(floors.values()))
        per_option.append({
            "id": o.id, "label": o.label,
            "gate": gate["state"], "gate_reasons": gate["reasons"],
            "q": q["q"], "q_band": q["band"], "q_capped": q["capped"],
            "c_agg": conf["c_agg"], "c_critical": conf["c_critical"],
            "floors": floors,
            "dV_pred": dv, "v_safe": cv["v_safe"],
            "lcb": cv["lcb"], "tail_penalty": cv["tail_penalty"],
            "residual_risk": _clamp01(o.residual_risk),
            "reversibility": _clamp01(o.reversibility),
            "scope": o.scope, "requires_authority": o.requires_authority,
            "synthetic_baseline": o.synthetic_baseline,
            "rankable": rankable,
        })

    # Rankable set -> Pareto frontier -> ranking. A singleton frontier still
    # passes through the full autonomy threshold: no auto-win (R3).
    rankable_opts = [s for s in per_option if s["rankable"]]
    frontier = pareto_frontier(rankable_opts)
    top3 = frontier[:3]

    ask_reasons = []
    # The injected "escalate" baseline is NEEDS_AUTHORITY by design — it is
    # the escalation path itself, not a veto on autonomous execution.
    if any(s["gate"] == NEEDS_AUTHORITY and not s["synthetic_baseline"]
           for s in per_option):
        ask_reasons.append("AuthorityRequired")
    if any(o.intent_ambiguous for o in options):
        ask_reasons.append("MaterialIntentAmbiguity")
    if top3:
        winner = top3[0]
        # Consequential + not reversible enough for scope + no standing
        # contract -> human decides (mirrors the EXECUTE reversible_enough
        # check; a standing contract plus sufficient reversibility clears it).
        if (winner["scope"] == "consequential"
                and winner["reversibility"] < params.reversibility_consequential_min
                and not ctx.standing_authority_contract):
            ask_reasons.append("ConsequentialIrreversibility")
    if top3 and not all(top3[0]["floors"].values()):
        ask_reasons.append("MaterialUncertainty")
    if len(frontier) >= 2:
        m = relative_dominance(frontier[0]["v_safe"], frontier[1]["v_safe"])
        if m < params.dominance_margin:
            ask_reasons.append("NoClearDominantOption")
    elif len(frontier) == 1:
        m = None
    else:
        m = None

    deviation = _param_deviation(ctx)

    # Outcome.
    outcome = None
    outcome_reasons = []
    selected = None
    if top3:
        w = top3[0]
        checks = {
            "admissible": w["gate"] == ADMISSIBLE,
            "q_ge_9": w["q"] >= Q_BAND_ACCEPT,
            "v_safe_positive": w["v_safe"] > 0,
            "floors": all(w["floors"].values()),
            "authority": not w["requires_authority"],
            "reversible_enough": (
                w["reversibility"] >= params.reversibility_autonomy_min
                and not (w["scope"] == "consequential"
                         and w["reversibility"] < params.reversibility_consequential_min
                         and not ctx.standing_authority_contract)
            ),
            "dominance": (m is not None and m >= params.dominance_margin),
            "no_param_deviation": not deviation,
            "consequential_contract": (
                w["scope"] != "consequential" or ctx.standing_authority_contract
            ),
        }
        failed = [k for k, v in checks.items() if not v]
        # R1: reversibility < min -> non-autonomous regardless of Priority.
        if w["reversibility"] < params.reversibility_autonomy_min:
            failed.append("reversibility_below_autonomy_min")
            failed = sorted(set(failed))
        if not failed and not ask_reasons:
            outcome = "EXECUTE"
            selected = w["id"]
        else:
            outcome = "BRIEF"
            outcome_reasons = failed + [f"ask:{r}" for r in ask_reasons]
            # recommend the winner anyway; human decides
            selected = w["id"]
    else:
        if any(s["gate"] == NEEDS_EVIDENCE for s in per_option):
            outcome = "RESEARCH"
            outcome_reasons = ["evidence_blocker_present"]
        elif any(s["gate"] == ADMISSIBLE for s in per_option):
            outcome = "REWORK"
            outcome_reasons = ["no_candidate_cleared_quality_value_bar"]
        else:
            outcome = "BRIEF"
            outcome_reasons = ["no_admissible_candidate"] + [f"ask:{r}" for r in ask_reasons]

    receipt = decision_receipt(ctx, per_option, frontier, top3, outcome,
                               selected, outcome_reasons, ask_reasons, m,
                               deviation)
    return {
        "engine_version": ENGINE_VERSION,
        "spec_version": SPEC_VERSION,
        "options": per_option,
        "frontier": [f["id"] for f in frontier],
        "top3": [t["id"] for t in top3],
        "dominance_margin": m,
        "ask_human": ask_reasons,
        "outcome": outcome,
        "selected": selected,
        "outcome_reasons": outcome_reasons,
        "param_deviation": deviation,
        "receipt": receipt,
    }


# ---------------------------------------------------------------------------
# SmartLedger typed receipts — one substrate, two streams (spec section 10)
# ---------------------------------------------------------------------------


def decision_receipt(ctx: DecisionContext, per_option: Sequence[dict],
                     frontier: Sequence[dict], top3: Sequence[dict],
                     outcome: str, selected: Optional[str],
                     outcome_reasons: Sequence[str], ask_reasons: Sequence[str],
                     dominance_margin: Optional[float],
                     param_deviation: bool) -> dict:
    """ALIGNMENT / DECISION RECEIPT (stream A)."""
    return {
        "receipt_type": "decision",
        "engine_version": ENGINE_VERSION,
        "spec_version": SPEC_VERSION,
        "spec_ref": SPEC_REF,
        "objective": ctx.objective,
        "baseline_id": ctx.baseline.id,
        "stakeholders": list(ctx.stakeholders),
        "horizon": ctx.horizon,
        "param_version": ctx.params.version,
        "param_owner": ctx.params.owner,
        "param_deviation": param_deviation,
        "param_authorized_by": ctx.param_authorized_by,
        "candidates": [
            {"id": s["id"], "label": s["label"], "gate": s["gate"],
             "gate_reasons": s["gate_reasons"], "q": s["q"], "q_band": s["q_band"],
             "c_agg": s["c_agg"], "c_critical": s["c_critical"],
             "dV_pred": s["dV_pred"], "v_safe": s["v_safe"],
             "tail_penalty": s["tail_penalty"],
             "residual_risk": s["residual_risk"],
             "reversibility": s["reversibility"],
             "rankable": s["rankable"]}
            for s in per_option
        ],
        "pareto_frontier": [f["id"] for f in frontier],
        "top3": [t["id"] for t in top3],
        "dominance_margin": dominance_margin,
        "dominance_threshold": ctx.params.dominance_margin,
        "selected": selected,
        "outcome": outcome,
        "outcome_reasons": list(outcome_reasons),
        "ask_human": list(ask_reasons),
        "verification": {"state": "PREDICTED", "window_days": None,
                         "dV_actual": None, "d_verified": None,
                         "calibration_error": None},
    }


def observation_window_days(harm_category: str,
                            params: V21Params = DEFAULT_PARAMS) -> float:
    """R5: declared observation window per harm category."""
    if harm_category not in params.windows_days:
        raise ValueError(f"unknown harm category '{harm_category}'")
    return params.windows_days[harm_category]


def record_observation(receipt: dict, dV_actual: float, harm_category: str,
                       harm_detected: bool = False,
                       params: V21Params = DEFAULT_PARAMS) -> dict:
    """OBSERVE -> VERIFY: attach the independently verified actual value.

    PASS is PROVISIONAL until the window closes with no harm detected, then
    CONFIRMED. Harm inside the window reopens the record (R5).
    """
    window = observation_window_days(harm_category, params)
    # find predicted dV for the selected option
    pred = None
    for c in receipt["candidates"]:
        if c["id"] == receipt["selected"]:
            pred = c["dV_pred"]
            break
    dV_actual = _finite(dV_actual, "dV_actual")
    d = d_verified(dV_actual)
    error = abs(pred - dV_actual) if pred is not None else None
    state = "REOPENED" if harm_detected else "PASS_PENDING_WINDOW"
    receipt = dict(receipt)
    receipt["verification"] = {
        "state": state,
        "window_days": window,
        "harm_category": harm_category,
        "dV_actual": dV_actual,
        "d_verified": d,
        "calibration_error": error,
        "learn_candidate": (error is not None
                            and error > params.calibration_learn_threshold),
    }
    return receipt


def confirm_window(receipt: dict, harm_detected: bool) -> dict:
    """Close the observation window: CONFIRMED, or REOPENED on late harm."""
    receipt = dict(receipt)
    v = dict(receipt["verification"])
    if v["state"] not in ("PASS_PENDING_WINDOW", "REOPENED"):
        raise ValueError("window can only close from a provisional state")
    v["state"] = "REOPENED" if harm_detected else "CONFIRMED"
    receipt["verification"] = v
    return receipt


# ---------------------------------------------------------------------------
# Plan-level assessment (anti action-splitting / authorization laundering)
# ---------------------------------------------------------------------------


def evaluate_plan(plan_id: str, steps: Sequence[Option], plan_pv: PVComponents,
                 ctx: DecisionContext,
                 laundering_tolerance: float = 1.0) -> dict:
    """A plan gets its own whole-plan value/risk/gate assessment.

    - every step inherits plan-level gates (a step may not be less strict
      than the plan);
    - step PVs are never simply summed into plan PV;
    - a plan whose steps look individually positive while the whole is not
      is flagged as suspected value laundering.
    """
    plan_gate: Optional[str] = None
    step_results = []
    for s in steps:
        g = evaluate_gate(s, ctx)["state"]
        step_results.append({"id": s.id, "gate": g,
                             "step_pv": s.pv.total()})
        if plan_gate is None or _GATE_STRICTNESS[g] > _GATE_STRICTNESS[plan_gate]:
            plan_gate = g

    violations = []
    for r in step_results:
        if _GATE_STRICTNESS[r["gate"]] < _GATE_STRICTNESS[plan_gate or ADMISSIBLE]:
            violations.append({"step": r["id"], "issue": "step_less_strict_than_plan",
                               "step_gate": r["gate"], "plan_gate": plan_gate})

    plan_total = plan_pv.total()
    steps_sum = sum(r["step_pv"] for r in step_results)
    laundering = (steps_sum > plan_total + laundering_tolerance
                  and plan_total <= 0)

    auth_laundering = any(
        r["gate"] == NEEDS_AUTHORITY for r in step_results)

    return {
        "plan_id": plan_id,
        "engine_version": ENGINE_VERSION,
        "plan_pv": plan_total,
        "steps_pv_sum": steps_sum,
        "plan_gate": plan_gate,
        "steps": step_results,
        "gate_inheritance_violations": violations,
        "value_laundering_suspected": laundering,
        "authorization_laundering_suspected": auth_laundering,
    }
