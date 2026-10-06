"""NayaPOWER Decision Value Calculus V2.1.

Deterministic, dependency-free decision math implementing the canonical
NAYANODE/0025 value-calculus seam. Value ranks only actions that governance
already permits. Scores never create authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, Sequence
import math

ENGINE_VERSION = "DECISION-VALUE-CALCULUS-V2.1"
QUALITY_DIMENSIONS = (
    "objective_fit",
    "evidence_sufficiency",
    "applicability",
    "robustness",
    "reversibility",
    "blast_containment",
    "simplicity",
)
DEFAULT_QUALITY_PRIORITIES = {
    "objective_fit": 0.20,
    "evidence_sufficiency": 0.20,
    "applicability": 0.15,
    "robustness": 0.15,
    "reversibility": 0.10,
    "blast_containment": 0.10,
    "simplicity": 0.10,
}

PROHIBITED = "PROHIBITED"
NEEDS_AUTHORITY = "NEEDS_AUTHORITY"
NEEDS_EVIDENCE = "NEEDS_EVIDENCE"
ADMISSIBLE = "ADMISSIBLE"

ACT = "ACT"
READ_MORE = "READ_MORE"
ASK = "ASK"
REFUSE = "REFUSE"

STAKE_ORDER = {"low": 0, "high": 1, "consequential": 2}


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, _finite(value, "value")))


def _norm10(value: float, name: str) -> float:
    return max(0.0, min(10.0, _finite(value, name)))


def _stake_max(*stakes: str) -> str:
    for s in stakes:
        if s not in STAKE_ORDER:
            raise ValueError(f"unknown stake: {s}")
    return max(stakes, key=lambda s: STAKE_ORDER[s])


@dataclass(frozen=True)
class PVEstimate:
    B: float
    H: float
    C: float
    R: float
    confidence: Mapping[str, float]
    evidence_count: int = 0

    def normalized(self) -> "PVEstimate":
        vals = {}
        for name in ("B", "H", "C", "R"):
            v = _finite(getattr(self, name), f"pv.{name}")
            if v < 0:
                raise ValueError(f"pv.{name} must be >= 0")
            vals[name] = v
        conf = {k: _clamp(v) for k, v in self.confidence.items()}
        return PVEstimate(**vals, confidence=conf, evidence_count=max(0, int(self.evidence_count)))

    def min_component_confidence(self) -> float:
        n = self.normalized()
        vals = [n.confidence.get(k, 0.0) for k in ("B", "H", "C", "R")]
        return min(vals) if vals else 0.0

    def effective_residual_risk(self, uncertainty_scale: float) -> float:
        n = self.normalized()
        uncertainty_floor = max(0.0, _finite(uncertainty_scale, "uncertainty_scale")) * (
            1.0 - n.min_component_confidence()
        )
        return max(n.R, uncertainty_floor)

    def pv(self, uncertainty_scale: float = 1.0) -> float:
        n = self.normalized()
        return n.B - n.H - n.C - n.effective_residual_risk(uncertainty_scale)


@dataclass(frozen=True)
class TailRisk:
    severity: float
    probability: float
    harm_class: str = "general"


@dataclass(frozen=True)
class RiskPolicy:
    severity_threshold: float = 9.0
    probability_threshold: float = 0.01
    response: str = PROHIBITED
    max_stakeholder_harm: float = 9.0

    def __post_init__(self):
        if self.response not in (PROHIBITED, NEEDS_AUTHORITY):
            raise ValueError("risk response must be PROHIBITED or NEEDS_AUTHORITY")
        _finite(self.severity_threshold, "severity_threshold")
        p = _finite(self.probability_threshold, "probability_threshold")
        if not 0 <= p <= 1:
            raise ValueError("probability_threshold must be in [0,1]")


@dataclass(frozen=True)
class QualityProfile:
    profile_id: str
    version: str
    objective: str
    priorities: Mapping[str, float] = None
    q_accept: float = 9.0
    aggregate_confidence_floor: float = 0.80
    critical_confidence_floor: float = 0.75
    critical_confidence_dimensions: Sequence[str] = (
        "objective_fit",
        "evidence_sufficiency",
        "applicability",
        "robustness",
    )
    min_evidence_count: int = 1
    relative_margin: float = 0.10
    interval_epsilon: float = 0.0
    min_reversibility_for_auto: float = 7.0
    uncertainty_scale: float = 1.0

    def weights(self) -> dict[str, float]:
        source = self.priorities or DEFAULT_QUALITY_PRIORITIES
        unknown = set(source) - set(QUALITY_DIMENSIONS)
        if unknown:
            raise ValueError(f"unknown quality dimensions: {sorted(unknown)}")
        values = {
            d: max(0.0, _finite(source.get(d, 0.0), f"priority[{d}]"))
            for d in QUALITY_DIMENSIONS
        }
        total = sum(values.values())
        if total <= 0:
            raise ValueError("quality profile requires positive priority mass")
        return {d: v / total for d, v in values.items()}


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    quality: Mapping[str, Optional[float]]
    confidence: Mapping[str, Optional[float]]
    pv: PVEstimate
    tails: Sequence[TailRisk] = ()
    stakeholder_harms: Mapping[str, float] = None
    authorized: bool = False
    human_authorized: bool = False
    hard_violation: bool = False
    lawful: Optional[bool] = None
    rights_safe: Optional[bool] = None
    privacy_safe: Optional[bool] = None
    safety_safe: Optional[bool] = None
    stakes: str = "low"
    plan_stakes: str = "low"
    reversible: bool = True
    principal_conflict: bool = False
    coordination_conflict: bool = False
    jurisdiction_conflict: bool = False
    uncertainty_penalty: float = 0.0
    tail_penalty: float = 0.0
    dependency_unlock: float = 0.0
    human_burden: float = 0.0
    is_baseline: bool = False

    def effective_stakes(self) -> str:
        return _stake_max(self.stakes, self.plan_stakes)


def score_quality(candidate: Candidate, profile: QualityProfile) -> dict:
    weights = profile.weights()
    dims: dict[str, float] = {}
    conf: dict[str, float] = {}
    missing = []
    for d in QUALITY_DIMENSIONS:
        raw = candidate.quality.get(d)
        if raw is None:
            dims[d] = 0.0
            missing.append(d)
        else:
            dims[d] = _norm10(raw, f"quality[{d}]")
        c = candidate.confidence.get(d)
        conf[d] = 0.0 if c is None else _clamp(c)
    q = sum(weights[d] * dims[d] for d in QUALITY_DIMENSIONS)
    c_agg = sum(weights[d] * conf[d] for d in QUALITY_DIMENSIONS)
    critical = {d: conf.get(d, 0.0) for d in profile.critical_confidence_dimensions}
    c_critical = min(critical.values()) if critical else 1.0
    return {
        "Q": q,
        "confidence_aggregate": c_agg,
        "confidence_critical": c_critical,
        "critical_confidences": critical,
        "dimensions": dims,
        "confidences": conf,
        "missing_dimensions": missing,
        "weights": weights,
    }


def delta_value(candidate: Candidate, baseline: Candidate, profile: QualityProfile) -> float:
    return candidate.pv.pv(profile.uncertainty_scale) - baseline.pv.pv(profile.uncertainty_scale)


def conservative_value(candidate: Candidate, baseline: Candidate, profile: QualityProfile) -> float:
    delta = delta_value(candidate, baseline, profile)
    return delta - max(0.0, _finite(candidate.uncertainty_penalty, "uncertainty_penalty")) - max(
        0.0, _finite(candidate.tail_penalty, "tail_penalty")
    )


def value_interval(candidate: Candidate, baseline: Candidate, profile: QualityProfile) -> dict[str, float]:
    """Explicit conservative value interval used for autonomous dominance.

    V_low is the existing conservative value. V_high preserves the same
    declared uncertainty/tail width on the upside. This does not invent
    confidence: callers must still satisfy the independent aggregate and
    critical confidence floors.
    """
    delta = delta_value(candidate, baseline, profile)
    width = (
        max(0.0, _finite(candidate.uncertainty_penalty, "uncertainty_penalty"))
        + max(0.0, _finite(candidate.tail_penalty, "tail_penalty"))
    )
    return {"v_low": delta - width, "v_high": delta + width, "interval_width": width}


def interval_gap(first: Mapping[str, float], second: Mapping[str, float]) -> float:
    """Positive only when the first option's lower bound clears second's upper."""
    return _finite(first["v_low"], "first.v_low") - _finite(second["v_high"], "second.v_high")


def gate_candidate(candidate: Candidate, profile: QualityProfile, risk_policy: RiskPolicy) -> tuple[str, list[str], dict]:
    q = score_quality(candidate, profile)
    reasons: list[str] = []

    if candidate.hard_violation:
        return PROHIBITED, ["JUDGMENT_RULE_HARD_STOP"], q

    hard_flags = {
        "LAW": candidate.lawful,
        "RIGHTS": candidate.rights_safe,
        "PRIVACY": candidate.privacy_safe,
        "SAFETY": candidate.safety_safe,
    }
    if any(v is False for v in hard_flags.values()):
        return PROHIBITED, [k for k, v in hard_flags.items() if v is False], q

    for tail in candidate.tails:
        sev = _finite(tail.severity, "tail.severity")
        prob = _finite(tail.probability, "tail.probability")
        if not 0 <= prob <= 1:
            raise ValueError("tail probability must be in [0,1]")
        if sev >= risk_policy.severity_threshold and prob > risk_policy.probability_threshold:
            return risk_policy.response, [f"TAIL_RISK:{tail.harm_class}"], q

    harms = candidate.stakeholder_harms or {}
    if any(_finite(v, f"stakeholder_harm[{k}]") >= risk_policy.max_stakeholder_harm for k, v in harms.items()):
        return PROHIBITED, ["DISTRIBUTIONAL_HARM"], q

    if candidate.principal_conflict or candidate.coordination_conflict or candidate.jurisdiction_conflict:
        return NEEDS_AUTHORITY, ["CONFLICT_REQUIRES_GOVERNANCE"], q

    effective_stakes = candidate.effective_stakes()
    if not candidate.authorized:
        return NEEDS_AUTHORITY, ["AUTHORITY_MISSING"], q
    if (effective_stakes == "consequential" or not candidate.reversible) and not candidate.human_authorized:
        return NEEDS_AUTHORITY, ["CONSEQUENTIAL_OR_IRREVERSIBLE"], q

    unknown_flags = [k for k, v in hard_flags.items() if v is None]
    if unknown_flags:
        reasons.append("HARD_GATE_UNKNOWN")
        reasons.extend(f"UNKNOWN_{k}" for k in unknown_flags)
    if candidate.pv.normalized().evidence_count < profile.min_evidence_count:
        reasons.append("EVIDENCE_FLOOR")
    if q["missing_dimensions"]:
        reasons.append("QUALITY_DIMENSION_MISSING")
    if q["confidence_aggregate"] < profile.aggregate_confidence_floor:
        reasons.append("AGGREGATE_CONFIDENCE_FLOOR")
    if q["confidence_critical"] < profile.critical_confidence_floor:
        reasons.append("CRITICAL_CONFIDENCE_FLOOR")
    if candidate.pv.min_component_confidence() < profile.critical_confidence_floor:
        reasons.append("PV_COMPONENT_CONFIDENCE_FLOOR")

    if reasons:
        return NEEDS_EVIDENCE, reasons, q
    return ADMISSIBLE, [], q


def _dominates(a: dict, b: dict) -> bool:
    av, aq, ar = a["v_safe"], a["q"]["Q"], a["residual_risk"]
    bv, bq, br = b["v_safe"], b["q"]["Q"], b["residual_risk"]
    return av >= bv and aq >= bq and ar <= br and (av > bv or aq > bq or ar < br)


def pareto_frontier(rows: Sequence[dict]) -> list[dict]:
    return [row for i, row in enumerate(rows) if not any(
        i != j and _dominates(other, row) for j, other in enumerate(rows)
    )]


def relative_margin(first: float, second: float, epsilon: float = 1e-9) -> float:
    return (first - second) / max(abs(first), epsilon)


def evaluate_candidates(candidates: Sequence[Candidate], baseline_id: str, profile: QualityProfile, risk_policy: RiskPolicy = RiskPolicy()) -> dict:
    baselines = [c for c in candidates if c.candidate_id == baseline_id and c.is_baseline]
    if len(baselines) != 1:
        raise ValueError("baseline_id must identify exactly one explicit baseline")
    baseline = baselines[0]

    rows = []
    for candidate in candidates:
        gate, reasons, q = gate_candidate(candidate, profile, risk_policy)
        interval = value_interval(candidate, baseline, profile)
        rows.append({
            "candidate_id": candidate.candidate_id,
            "gate": gate,
            "gate_reasons": reasons,
            "q": q,
            "pv": candidate.pv.pv(profile.uncertainty_scale),
            "delta_v": delta_value(candidate, baseline, profile),
            "v_safe": conservative_value(candidate, baseline, profile),
            "v_low": interval["v_low"],
            "v_high": interval["v_high"],
            "interval_width": interval["interval_width"],
            "residual_risk": candidate.pv.effective_residual_risk(profile.uncertainty_scale),
            "effective_stakes": candidate.effective_stakes(),
            "reversible": candidate.reversible,
            "dependency_unlock": _finite(candidate.dependency_unlock, "dependency_unlock"),
            "human_burden": max(0.0, _finite(candidate.human_burden, "human_burden")),
            "is_baseline": candidate.is_baseline,
        })

    eligible = [r for r in rows if r["gate"] == ADMISSIBLE and r["q"]["Q"] >= profile.q_accept and r["v_safe"] > 0]
    frontier = pareto_frontier(eligible)
    key = lambda r: (
        -r["v_safe"], -r["dependency_unlock"], -r["q"]["dimensions"]["reversibility"],
        r["human_burden"], -r["q"]["dimensions"]["simplicity"],
        -r["q"]["confidence_aggregate"], r["candidate_id"],
    )
    frontier.sort(key=key)
    ranked_all = sorted(eligible, key=key)
    top3 = ranked_all[:3]

    if not frontier:
        non_baseline = [r for r in rows if not r["is_baseline"]]
        if non_baseline and all(r["gate"] == PROHIBITED for r in non_baseline):
            decision = REFUSE
        elif any(r["gate"] == NEEDS_EVIDENCE for r in rows):
            decision = READ_MORE
        elif any(r["gate"] == NEEDS_AUTHORITY for r in rows):
            decision = ASK
        else:
            # Admissible candidates exist, but none yet clears Q/value.
            decision = READ_MORE
        return {
            "decision": decision, "selected": None, "top3": top3,
            "rows": rows, "frontier": frontier,
            "interval_gap": None, "relative_margin": None,
        }

    first = frontier[0]
    competing = [r for r in ranked_all if r["candidate_id"] != first["candidate_id"]]
    second = competing[0] if competing else None
    margin = 1.0 if second is None else relative_margin(first["v_safe"], second["v_safe"])
    gap = float("inf") if second is None else interval_gap(first, second)
    by_id = {c.candidate_id: c for c in candidates}
    selected_candidate = by_id[first["candidate_id"]]
    interval_dominant = second is None or gap > profile.interval_epsilon
    can_auto = (
        first["gate"] == ADMISSIBLE
        and first["q"]["Q"] >= profile.q_accept
        and first["v_safe"] > 0
        and first["q"]["confidence_aggregate"] >= profile.aggregate_confidence_floor
        and first["q"]["confidence_critical"] >= profile.critical_confidence_floor
        and first["effective_stakes"] == "low"
        and selected_candidate.reversible
        and first["q"]["dimensions"]["reversibility"] >= profile.min_reversibility_for_auto
        and margin >= profile.relative_margin
        and interval_dominant
    )
    if can_auto:
        decision = ACT
    elif first["effective_stakes"] != "low" or not selected_candidate.reversible:
        decision = ASK
    else:
        decision = READ_MORE
    return {
        "decision": decision,
        "selected": first["candidate_id"],
        "top3": top3,
        "rows": rows,
        "frontier": frontier,
        "relative_margin": margin,
        "interval_gap": None if second is None else gap,
    }


def verification_state(outcome_passed: bool, observation_window_closed: bool, delayed_harm_material: bool) -> str:
    if not outcome_passed:
        return "FAIL"
    if delayed_harm_material and not observation_window_closed:
        return "PASS_PENDING_WINDOW"
    return "VERIFIED_PASS"


def build_decision_receipt(*, decision_id: str, objective: str, baseline_id: str, stakeholders: Sequence[str], horizon: str, evaluation: Mapping, authority_basis: str, evidence_refs: Sequence[str], observation_window: Mapping[str, Optional[str]], verification: str, delta_v_actual: Optional[float] = None) -> dict:
    if verification not in ("UNVERIFIED", "PASS_PENDING_WINDOW", "VERIFIED_PASS", "FAIL", "ESCALATE"):
        raise ValueError("invalid verification state")
    predicted = None
    if evaluation.get("selected"):
        selected = next(r for r in evaluation["rows"] if r["candidate_id"] == evaluation["selected"])
        predicted = selected["delta_v"]
    error = None
    d_verified = None
    if delta_v_actual is not None:
        actual = _finite(delta_v_actual, "delta_v_actual")
        error = abs(predicted - actual) if predicted is not None else None
        d_verified = max(-10.0, min(10.0, actual))
    return {
        "receipt_type": "ALIGNMENT_DECISION",
        "schema_version": "2.1",
        "engine_version": ENGINE_VERSION,
        "decision_id": decision_id,
        "objective": objective,
        "baseline_id": baseline_id,
        "stakeholders": list(stakeholders),
        "horizon": horizon,
        "evaluation": dict(evaluation),
        "authority_basis": authority_basis,
        "evidence_refs": list(evidence_refs),
        "observation_window": dict(observation_window),
        "verification": verification,
        "delta_v_predicted": predicted,
        "delta_v_actual": delta_v_actual,
        "d_verified": d_verified,
        "calibration_error": error,
    }


def independent_recompute(receipt: Mapping, candidates: Sequence[Candidate], profile: QualityProfile, risk_policy: RiskPolicy = RiskPolicy()) -> dict:
    evaluation = evaluate_candidates(candidates, receipt["baseline_id"], profile, risk_policy)
    return {
        "matches_decision": evaluation["decision"] == receipt["evaluation"]["decision"],
        "matches_selected": evaluation["selected"] == receipt["evaluation"]["selected"],
        "recomputed": evaluation,
    }


def calibration_summary(records: Sequence[Mapping]) -> dict:
    errors = []
    signed = []
    for r in records:
        pred = r.get("delta_v_predicted")
        actual = r.get("delta_v_actual")
        if pred is None or actual is None:
            continue
        e = _finite(actual, "actual") - _finite(pred, "predicted")
        signed.append(e)
        errors.append(abs(e))
    n = len(errors)
    mae = sum(errors) / n if n else 0.0
    bias = sum(signed) / n if n else 0.0
    return {
        "n": n,
        "mean_absolute_error": mae,
        "mean_signed_error": bias,
        "overprediction_detected": n >= 3 and bias < 0,
        "confidence_multiplier": 1.0 if n == 0 else max(0.25, 1.0 / (1.0 + mae)),
    }


def build_recalibration_receipt(
    *,
    current_profile: QualityProfile,
    proposed_version: str,
    records: Sequence[Mapping],
    proposed_priorities: Optional[Mapping[str, float]] = None,
    proposed_thresholds: Optional[Mapping[str, float]] = None,
    evidence_refs: Sequence[str] = (),
) -> dict:
    """Create a versioned LEARN candidate; never mutates the active profile."""
    if not proposed_version or proposed_version == current_profile.version:
        raise ValueError("proposed_version must be a new explicit version")
    summary = calibration_summary(records)
    return {
        "receipt_type": "VALUE_RECALIBRATION",
        "schema_version": "2.1",
        "engine_version": ENGINE_VERSION,
        "profile_id": current_profile.profile_id,
        "from_version": current_profile.version,
        "proposed_version": proposed_version,
        "objective": current_profile.objective,
        "calibration_summary": summary,
        "proposed_priorities": dict(proposed_priorities or current_profile.weights()),
        "proposed_thresholds": dict(proposed_thresholds or {}),
        "evidence_refs": list(evidence_refs),
        "state": "LEARN_CANDIDATE",
        "automatic_promotion": False,
    }


def promote_recalibration(
    receipt: Mapping,
    current_profile: QualityProfile,
    *,
    verified: bool,
    authorized: bool,
) -> QualityProfile:
    """Governed LEARN→EVOLVE write-back. No silent self-ratification."""
    if receipt.get("receipt_type") != "VALUE_RECALIBRATION":
        raise ValueError("not a recalibration receipt")
    if receipt.get("from_version") != current_profile.version:
        raise ValueError("stale recalibration receipt")
    if not verified:
        raise PermissionError("recalibration must be verified before promotion")
    if not authorized:
        raise PermissionError("recalibration requires applicable authority")

    thresholds = dict(receipt.get("proposed_thresholds") or {})
    allowed_thresholds = {
        "q_accept", "aggregate_confidence_floor", "critical_confidence_floor",
        "min_evidence_count", "relative_margin", "interval_epsilon",
        "min_reversibility_for_auto", "uncertainty_scale",
    }
    unknown = set(thresholds) - allowed_thresholds
    if unknown:
        raise ValueError(f"unknown recalibration thresholds: {sorted(unknown)}")

    params = {
        "profile_id": current_profile.profile_id,
        "version": str(receipt["proposed_version"]),
        "objective": current_profile.objective,
        "priorities": dict(receipt.get("proposed_priorities") or current_profile.weights()),
        "q_accept": current_profile.q_accept,
        "aggregate_confidence_floor": current_profile.aggregate_confidence_floor,
        "critical_confidence_floor": current_profile.critical_confidence_floor,
        "critical_confidence_dimensions": current_profile.critical_confidence_dimensions,
        "min_evidence_count": current_profile.min_evidence_count,
        "relative_margin": current_profile.relative_margin,
        "interval_epsilon": current_profile.interval_epsilon,
        "min_reversibility_for_auto": current_profile.min_reversibility_for_auto,
        "uncertainty_scale": current_profile.uncertainty_scale,
    }
    params.update(thresholds)
    return QualityProfile(**params)


def contribution_value_score(*, quality: float, relevance: float, verification: float, impact: float, novelty: float, verified_delta: float) -> float:
    """Verified contribution score in [-9,+9]; human worth/authority are out of scope."""
    factors = [_clamp(quality), _clamp(relevance), _clamp(verification), _clamp(impact), _clamp(novelty)]
    if verified_delta == 0 or any(f == 0 for f in factors):
        return 0.0
    magnitude = 9.0 * math.prod(factors) ** (1.0 / len(factors))
    return magnitude if verified_delta > 0 else -magnitude


def contribution_points(cvs: float, points_per_unit: float, repeat_decay: float = 1.0) -> float:
    """Positive recognition points only; negative CVS is evidence, never automatic punishment."""
    return max(0.0, _finite(cvs, "cvs")) * max(0.0, _finite(points_per_unit, "points_per_unit")) * _clamp(repeat_decay)


def build_contribution_receipt(
    *,
    contribution_id: str,
    action_class: str,
    provenance: Mapping,
    privacy: Mapping,
    raw_activity: Mapping,
    quality: float,
    relevance: float,
    verification_strength: float,
    impact: float,
    novelty: float,
    verified_delta: Optional[float],
    scoring_profile_id: str,
    scoring_profile_version: str,
    points_per_unit: float,
    repeat_decay: float,
    evidence_refs: Sequence[str],
    explanation: str,
    verification: str = "UNVERIFIED",
) -> dict:
    """Build the canonical CONTRIBUTION_VALUE receipt.

    Positive recognition requires VERIFIED contribution evidence. Unverified or
    merely observed activity can be recorded, but receives no positive CVS/points.
    This receipt never represents human worth and never grants authority.
    """
    if verification not in ("UNVERIFIED", "OBSERVED", "VERIFIED", "FAIL", "ESCALATE"):
        raise ValueError("invalid contribution verification state")
    if not contribution_id or not action_class:
        raise ValueError("contribution_id and action_class are required")
    if not scoring_profile_id or not scoring_profile_version:
        raise ValueError("scoring profile id/version are required")

    factors = {
        "quality": _clamp(quality),
        "relevance": _clamp(relevance),
        "verification_strength": _clamp(verification_strength),
        "impact": _clamp(impact),
        "novelty": _clamp(novelty),
    }
    actual_delta = None if verified_delta is None else _finite(verified_delta, "verified_delta")
    credit_verification = factors["verification_strength"] if verification == "VERIFIED" and actual_delta is not None else 0.0
    cvs = contribution_value_score(
        quality=factors["quality"],
        relevance=factors["relevance"],
        verification=credit_verification,
        impact=factors["impact"],
        novelty=factors["novelty"],
        verified_delta=actual_delta or 0.0,
    )
    points = contribution_points(cvs, points_per_unit, repeat_decay) if verification == "VERIFIED" else 0.0

    return {
        "receipt_type": "CONTRIBUTION_VALUE",
        "schema_version": "2.1",
        "engine_version": ENGINE_VERSION,
        "contribution_id": contribution_id,
        "action_class": action_class,
        "provenance": dict(provenance),
        "privacy": dict(privacy),
        "raw_activity": dict(raw_activity),
        "factors": factors,
        "verified_delta": actual_delta,
        "cvs": cvs,
        "scoring_profile": {
            "id": scoring_profile_id,
            "version": scoring_profile_version,
            "points_per_unit": max(0.0, _finite(points_per_unit, "points_per_unit")),
            "repeat_decay": _clamp(repeat_decay),
        },
        "points_awarded": points,
        "explanation": explanation,
        "evidence_refs": list(evidence_refs),
        "verification": verification,
    }


# ---------------------------------------------------------------------------
# Operation eligibility: RETRIEVAL_ELIGIBLE / CONSEQUENTIAL_USE_ELIGIBLE
# ---------------------------------------------------------------------------
# Two machine-exact predicates (never one Boolean) that decide whether a
# retrieval (KNOW HIT serving) or a consequential use (ACT on consequential /
# irreversible operations) may proceed. Four states, evaluated in precedence
# order — hard stops first, then the indeterminate, then the determined
# negative, and only then PASS:
#   ELIGIBLE_PASS     - eligible under current evidence; may proceed.
#   ELIGIBLE_FAIL     - not eligible under current evidence; may become
#                       eligible if the evidence changes (e.g. authorized).
#   ELIGIBLE_UNKNOWN  - cannot determine from current evidence. UNKNOWN never
#                       becomes PASS: it routes to evidence gathering, never
#                       to proceed.
#   ELIGIBLE_BLOCKED  - hard stop; not eligible without intervention
#                       (safety/law violation, unauthenticated identity).
# Every decision carries its reasons and the evidence refs it rested on.
# These predicates never score human worth and never grant authority.

ELIGIBLE_PASS = "ELIGIBLE_PASS"
ELIGIBLE_FAIL = "ELIGIBLE_FAIL"
ELIGIBLE_UNKNOWN = "ELIGIBLE_UNKNOWN"
ELIGIBLE_BLOCKED = "ELIGIBLE_BLOCKED"

_ELIGIBLE_STATES = (ELIGIBLE_PASS, ELIGIBLE_FAIL, ELIGIBLE_UNKNOWN, ELIGIBLE_BLOCKED)


@dataclass(frozen=True)
class OperationRequest:
    """Evidence available about a proposed retrieval or consequential use."""
    operation_id: str
    requester_id: Optional[str] = None          # None = unauthenticated
    requester_scope: Optional[str] = None        # owner scope, e.g. "owner:<id>"
    object_scope: Optional[str] = None          # scope of the object touched
    source_canonical: Optional[bool] = None      # True/False/unknown
    authority_basis: Optional[str] = None        # consent/authority ref; None = unknown
    consequential: bool = False
    irreversible: bool = False
    human_authorized: bool = False
    hard_violation: bool = False
    hard_flags: Optional[Mapping[str, Optional[bool]]] = None  # LAW/RIGHTS/PRIVACY/SAFETY
    confidence_aggregate: Optional[float] = None
    confidence_critical: Optional[float] = None
    evidence_refs: Sequence[str] = ()


def _eligibility_receipt(predicate: str, request: OperationRequest, state: str, reasons: list) -> dict:
    assert state in _ELIGIBLE_STATES, f"invalid eligibility state: {state}"
    return {
        "predicate": predicate,
        "operation_id": request.operation_id,
        "state": state,
        "reasons": list(reasons),
        "evidence_refs": list(request.evidence_refs),
        "engine_version": ENGINE_VERSION,
    }


def _hard_flag_states(request: OperationRequest) -> dict:
    flags = request.hard_flags or {}
    return {k: flags.get(k) for k in ("LAW", "RIGHTS", "PRIVACY", "SAFETY")}


def retrieval_eligible(request: OperationRequest) -> dict:
    """Machine-exact predicate: may this KNOW retrieval be served?

    Precedence: BLOCKED (hard stops) -> UNKNOWN (indeterminate) ->
    FAIL (determined negative) -> PASS. UNKNOWN never becomes PASS.
    """
    if not request.operation_id:
        raise ValueError("operation_id is required")
    flags = _hard_flag_states(request)

    # BLOCKED: hard stops. No identity, or a law/safety violation, ends the
    # question here — these do not become eligible by gathering evidence.
    if request.requester_id is None:
        return _eligibility_receipt("RETRIEVAL_ELIGIBLE", request, ELIGIBLE_BLOCKED,
                                    ["UNAUTHENTICATED_REQUESTER"])
    if request.hard_violation:
        return _eligibility_receipt("RETRIEVAL_ELIGIBLE", request, ELIGIBLE_BLOCKED,
                                    ["JUDGMENT_RULE_HARD_STOP"])
    violated = [k for k, v in flags.items() if v is False]
    if violated:
        return _eligibility_receipt("RETRIEVAL_ELIGIBLE", request, ELIGIBLE_BLOCKED,
                                    [f"{k}_VIOLATION" for k in violated])

    # UNKNOWN: indeterminate. Each of these routes to evidence gathering;
    # none of them may resolve to PASS.
    unknown_reasons = []
    if request.requester_scope is None or request.object_scope is None:
        unknown_reasons.append("SCOPE_UNKNOWN")
    if request.source_canonical is None:
        unknown_reasons.append("SOURCE_CANONICALITY_UNKNOWN")
    if request.authority_basis is None:
        unknown_reasons.append("AUTHORITY_BASIS_UNKNOWN")
    unknown_reasons.extend(f"UNKNOWN_{k}" for k, v in flags.items() if v is None)
    if unknown_reasons:
        return _eligibility_receipt("RETRIEVAL_ELIGIBLE", request, ELIGIBLE_UNKNOWN, unknown_reasons)

    # FAIL: determined negative on complete evidence. May become eligible if
    # the evidence changes (e.g. cross-scope authority granted).
    if request.requester_scope != request.object_scope:
        return _eligibility_receipt("RETRIEVAL_ELIGIBLE", request, ELIGIBLE_FAIL,
                                    ["CROSS_SCOPE"])
    if request.source_canonical is False:
        return _eligibility_receipt("RETRIEVAL_ELIGIBLE", request, ELIGIBLE_FAIL,
                                    ["NON_CANONICAL_SOURCE"])

    return _eligibility_receipt("RETRIEVAL_ELIGIBLE", request, ELIGIBLE_PASS, [])


def consequential_use_eligible(request: OperationRequest, profile: QualityProfile) -> dict:
    """Machine-exact predicate: may this consequential/irreversible use proceed?

    Same four-state precedence as retrieval_eligible. Additionally requires
    human authorization for consequential or irreversible operations and the
    independent confidence floors from the quality profile.
    """
    if not request.operation_id:
        raise ValueError("operation_id is required")
    flags = _hard_flag_states(request)

    # BLOCKED: hard stops.
    if request.hard_violation:
        return _eligibility_receipt("CONSEQUENTIAL_USE_ELIGIBLE", request, ELIGIBLE_BLOCKED,
                                    ["JUDGMENT_RULE_HARD_STOP"])
    violated = [k for k, v in flags.items() if v is False]
    if violated:
        return _eligibility_receipt("CONSEQUENTIAL_USE_ELIGIBLE", request, ELIGIBLE_BLOCKED,
                                    [f"{k}_VIOLATION" for k in violated])

    # UNKNOWN: indeterminate — never PASS.
    unknown_reasons = [f"UNKNOWN_{k}" for k, v in flags.items() if v is None]
    if request.confidence_aggregate is None or request.confidence_critical is None:
        unknown_reasons.append("CONFIDENCE_UNKNOWN")
    if unknown_reasons:
        return _eligibility_receipt("CONSEQUENTIAL_USE_ELIGIBLE", request, ELIGIBLE_UNKNOWN,
                                    unknown_reasons)

    # FAIL: determined negative on complete evidence.
    if (request.consequential or request.irreversible) and not request.human_authorized:
        return _eligibility_receipt("CONSEQUENTIAL_USE_ELIGIBLE", request, ELIGIBLE_FAIL,
                                    ["HUMAN_AUTHORITY_REQUIRED"])
    if request.confidence_aggregate < profile.aggregate_confidence_floor:
        return _eligibility_receipt("CONSEQUENTIAL_USE_ELIGIBLE", request, ELIGIBLE_FAIL,
                                    ["AGGREGATE_CONFIDENCE_FLOOR"])
    if request.confidence_critical < profile.critical_confidence_floor:
        return _eligibility_receipt("CONSEQUENTIAL_USE_ELIGIBLE", request, ELIGIBLE_FAIL,
                                    ["CRITICAL_CONFIDENCE_FLOOR"])

    return _eligibility_receipt("CONSEQUENTIAL_USE_ELIGIBLE", request, ELIGIBLE_PASS, [])

# Next-Best-Action priority overlay. This extends the canonical Value Calculus;
# it is not a second authority, truth, gate, or ledger system.
ACTION_DIMENSIONS = (
    "mission_value",
    "human_value",
    "urgency",
    "leverage",
    "evidence",
    "risk",
    "cost",
    "dependencies",
    "reversibility",
    "compounding_continuity",
)

DEFAULT_NEXT_BEST_ACTION_WEIGHTS = {
    "mission_value": 0.18,
    "human_value": 0.18,
    "urgency": 0.08,
    "leverage": 0.12,
    "evidence": 0.14,
    "risk": 0.10,
    "cost": 0.05,
    "dependencies": 0.05,
    "reversibility": 0.04,
    "compounding_continuity": 0.06,
}


@dataclass(frozen=True)
class NextBestActionCandidate:
    """Candidate input for deterministic priority ranking after governance gating.

    All fields are 0..10. Higher is better for every dimension *except* risk and
    cost, where the input is burden (higher is worse) and is inverted for the
    combined score. Hard governance remains outside this scalar score.
    """
    candidate_id: str
    scores: Mapping[str, float]

    def normalized(self) -> dict[str, float]:
        unknown = set(self.scores) - set(ACTION_DIMENSIONS)
        missing = set(ACTION_DIMENSIONS) - set(self.scores)
        if unknown:
            raise ValueError(f"unknown action dimensions: {sorted(unknown)}")
        if missing:
            raise ValueError(f"missing action dimensions: {sorted(missing)}")
        out = {}
        for d in ACTION_DIMENSIONS:
            out[d] = _norm10(self.scores[d], f"action[{d}]")
        return out


@dataclass(frozen=True)
class NextBestActionProfile:
    profile_id: str
    version: str
    weights: Mapping[str, float]
    act_score: float = 9.0
    below_standard_score: float = 7.0
    evidence_floor: float = 8.0
    max_risk_for_auto: float = 3.0
    min_human_value_for_auto: float = 7.0
    min_reversibility_for_auto: float = 7.0
    dominance_margin: float = 0.10

    @classmethod
    def default(cls) -> "NextBestActionProfile":
        return cls(
            profile_id="NAYAPOWER-NEXT-BEST-ACTION",
            version="1.0",
            weights=DEFAULT_NEXT_BEST_ACTION_WEIGHTS,
        )

    def __post_init__(self):
        unknown = set(self.weights) - set(ACTION_DIMENSIONS)
        missing = set(ACTION_DIMENSIONS) - set(self.weights)
        if unknown:
            raise ValueError(f"unknown action dimensions: {sorted(unknown)}")
        if missing:
            raise ValueError(f"missing action dimensions: {sorted(missing)}")
        vals = {d: _finite(self.weights[d], f"weight[{d}]") for d in ACTION_DIMENSIONS}
        if any(v < 0 for v in vals.values()) or sum(vals.values()) <= 0:
            raise ValueError("action weights require non-negative positive total")
        if abs(sum(vals.values()) - 1.0) > 1e-9:
            raise ValueError("action weights must sum to 1")
        for name, value in (("act_score", self.act_score), ("below_standard_score", self.below_standard_score),
                            ("evidence_floor", self.evidence_floor), ("max_risk_for_auto", self.max_risk_for_auto),
                            ("min_human_value_for_auto", self.min_human_value_for_auto),
                            ("min_reversibility_for_auto", self.min_reversibility_for_auto),
                            ("dominance_margin", self.dominance_margin)):
            _finite(value, name)
        if not 0 <= self.dominance_margin <= 10:
            raise ValueError("dominance_margin must be in [0,10]")


def _next_best_action_favorable_score(candidate: NextBestActionCandidate, profile: NextBestActionProfile) -> float:
    scores = candidate.normalized()
    return sum(
        profile.weights[d] * (10.0 - scores[d] if d in {"risk", "cost"} else scores[d])
        for d in ACTION_DIMENSIONS
    )


def combine_next_best_action_score(candidate: NextBestActionCandidate, profile: NextBestActionProfile) -> float:
    """Return the deterministic 0..10 priority score for a candidate.

    Governance gates are deliberately not scalarized. This function only
    combines the ten prioritization dimensions after the canonical Value
    Calculus has determined the action is otherwise eligible for comparison.
    """
    return _next_best_action_favorable_score(candidate, profile)


def _next_best_action_status(candidate: NextBestActionCandidate, score: float, profile: NextBestActionProfile) -> tuple[str, str]:
    values = candidate.normalized()
    if values["risk"] > profile.max_risk_for_auto:
        return "BLOCKED", "RISK_CAP"
    if values["evidence"] < profile.evidence_floor:
        return "READ_MORE", "EVIDENCE_FLOOR"
    if score < profile.below_standard_score:
        return "BELOW_STANDARD", "QUALITY_FLOOR"
    if values["human_value"] < profile.min_human_value_for_auto:
        return "READ_MORE", "HUMAN_VALUE_FLOOR"
    if values["reversibility"] < profile.min_reversibility_for_auto:
        return "READ_MORE", "REVERSIBILITY_FLOOR"
    if score < profile.act_score:
        return "READ_MORE", "ACT_SCORE_FLOOR"
    return "ELIGIBLE", ""


@dataclass(frozen=True)
class NextBestActionResult:
    candidate_id: str
    score: float
    status: str
    reason: str


def rank_next_best_actions(candidates: Sequence[NextBestActionCandidate], profile: NextBestActionProfile | None = None) -> list[NextBestActionResult]:
    """Rank eligible actions deterministically; close leaders become READ_MORE.

    Tie-break order: combined score, evidence, human value, urgency, leverage,
    reversibility, lower risk, lower cost, then stable candidate_id. A close
    top pair is intentionally not auto-selected: uncertainty should trigger
    more evidence rather than false precision.
    """
    p = profile or NextBestActionProfile.default()
    rows = []
    for candidate in candidates:
        score = combine_next_best_action_score(candidate, p)
        status, reason = _next_best_action_status(candidate, score, p)
        values = candidate.normalized()
        rows.append((candidate, score, status, reason, values))

    rows.sort(key=lambda x: (
        -x[1], -x[4]["evidence"], -x[4]["human_value"], -x[4]["urgency"],
        -x[4]["leverage"], -x[4]["reversibility"], x[4]["risk"], x[4]["cost"], x[0].candidate_id,
    ))
    results = [NextBestActionResult(x[0].candidate_id, x[1], x[2], x[3]) for x in rows]
    eligible = [i for i, x in enumerate(rows) if x[2] == "ELIGIBLE"]
    if len(eligible) >= 2:
        first, second = eligible[0], eligible[1]
        if rows[first][1] - rows[second][1] < p.dominance_margin:
            for i in eligible:
                results[i] = NextBestActionResult(results[i].candidate_id, results[i].score, "READ_MORE", "NO_CLEAR_DOMINANT_OPTION")
    return results
