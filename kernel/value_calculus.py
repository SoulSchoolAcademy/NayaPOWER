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
    lawful: Optional[bool] = True
    rights_safe: Optional[bool] = True
    privacy_safe: Optional[bool] = True
    safety_safe: Optional[bool] = True
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


def gate_candidate(candidate: Candidate, profile: QualityProfile, risk_policy: RiskPolicy) -> tuple[str, list[str], dict]:
    q = score_quality(candidate, profile)
    reasons: list[str] = []

    if candidate.hard_violation:
        return PROHIBITED, ["HARD_VIOLATION"], q

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

    if any(v is None for v in hard_flags.values()):
        reasons.append("HARD_GATE_UNKNOWN")
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
        rows.append({
            "candidate_id": candidate.candidate_id,
            "gate": gate,
            "gate_reasons": reasons,
            "q": q,
            "pv": candidate.pv.pv(profile.uncertainty_scale),
            "delta_v": delta_value(candidate, baseline, profile),
            "v_safe": conservative_value(candidate, baseline, profile),
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
        decision = "RESEARCH" if any(r["gate"] == NEEDS_EVIDENCE for r in rows) else "BRIEF"
        if not any(r["gate"] in (NEEDS_EVIDENCE, NEEDS_AUTHORITY) for r in rows):
            decision = "REWORK"
        return {"decision": decision, "selected": None, "top3": top3, "rows": rows, "frontier": frontier}

    first = frontier[0]
    competing = [r for r in ranked_all if r["candidate_id"] != first["candidate_id"]]
    second = competing[0] if competing else None
    margin = 1.0 if second is None else relative_margin(first["v_safe"], second["v_safe"])
    by_id = {c.candidate_id: c for c in candidates}
    selected_candidate = by_id[first["candidate_id"]]
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
    )
    return {
        "decision": "EXECUTE" if can_auto else "BRIEF",
        "selected": first["candidate_id"],
        "top3": top3,
        "rows": rows,
        "frontier": frontier,
        "relative_margin": margin,
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
    legacy_to_canonical = {
        "EXECUTE": "ACT",
        "RESEARCH": "READ_MORE",
        "BRIEF": "ASK",
        "REWORK": "REFUSE",
    }
    resolution = evaluation.get("resolution")
    if resolution is None:
        resolution = legacy_to_canonical.get(evaluation.get("decision"), "ASK")
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
        "decision_resolution": resolution,
        "signed_value": evaluation.get("selected_signed_value"),
        "quality": evaluation.get("selected_quality"),
        "confidence": evaluation.get("selected_confidence"),
        "value_interval": evaluation.get("selected_value_interval"),
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



