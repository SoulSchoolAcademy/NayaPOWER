"""NayaPOWER deterministic Value Calculus V1.

This module is intentionally small and dependency-free. It implements the
canonical calculation in NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Mapping, Optional, Sequence
import math

DIMENSIONS = ("U", "R", "A", "E", "C", "Re", "L", "K", "T")
ENGINE_VERSION = "VALUE-CALCULUS-V1.0"


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(value)))


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


@dataclass(frozen=True)
class Gate:
    dimension: str
    minimum: float

    def evaluate(self, dimensions: Mapping[str, float]) -> bool:
        return dimensions.get(self.dimension, 0.0) >= self.minimum


@dataclass(frozen=True)
class ValueProfile:
    profile_id: str
    version: str
    objective: str
    priorities: Mapping[str, float]
    critical_gates: Sequence[Gate] = ()
    not_applicable: Sequence[str] = ()
    sensitivity_delta: float = 0.10

    def weights(self) -> dict[str, float]:
        for d in self.priorities:
            if d not in DIMENSIONS:
                raise ValueError(f"unknown dimension: {d}")
        active = {d: max(0.0, _finite(self.priorities.get(d, 0.0), f"priority[{d}]"))
                  for d in DIMENSIONS if d not in self.not_applicable}
        total = sum(active.values())
        if total <= 0:
            raise ValueError("profile must have at least one positive active priority")
        return {d: p / total for d, p in active.items()}


@dataclass(frozen=True)
class ResourceCost:
    attention: float = 0.0
    time: float = 0.0
    compute: float = 0.0
    storage: float = 0.0
    money: float = 0.0
    complexity: float = 0.0
    risk: float = 0.0
    latency: float = 0.0
    maintenance: float = 0.0

    def total(self) -> float:
        values = [getattr(self, f) for f in self.__dataclass_fields__]
        return sum(max(0.0, _finite(v, f"resource.{f}"))
                   for f, v in zip(self.__dataclass_fields__, values))


def calculate_value(
    dimensions: Mapping[str, Optional[float]],
    profile: ValueProfile,
    harm: float = 0.0,
    verification_state: str = "ESTIMATED",
    verified_value: Optional[float] = None,
    resources: Optional[ResourceCost] = None,
    sensitivity: bool = False,
) -> dict:
    weights = profile.weights()
    normalized = {}
    missing = []
    for d in DIMENSIONS:
        if d in profile.not_applicable:
            continue
        raw = dimensions.get(d)
        if raw is None:
            missing.append(d)
            normalized[d] = 0.0
        else:
            normalized[d] = _clamp(_finite(raw, f"dimension[{d}]"))

    positive = sum(weights[d] * normalized[d] for d in weights)
    harm_n = _clamp(_finite(harm, "harm"))
    raw_score = positive - harm_n
    score = _clamp(raw_score)

    gates = [
        {"dimension": g.dimension, "minimum": g.minimum,
         "passed": g.evaluate(normalized)}
        for g in profile.critical_gates
    ]
    gate_pass = all(g["passed"] for g in gates)
    status = "PASS" if gate_pass else "BLOCKED"

    result = {
        "engine_version": ENGINE_VERSION,
        "profile": {"id": profile.profile_id, "version": profile.version,
                    "objective": profile.objective, "weights": weights},
        "dimensions": normalized,
        "missing_dimensions": missing,
        "not_applicable": list(profile.not_applicable),
        "base_score": positive,
        "harm": harm_n,
        "raw_score": raw_score,
        "normalized_score": score,
        "score_10": 10.0 * score,
        "verification_state": verification_state,
        "status": status,
        "critical_gates": gates,
        "verified_value": verified_value,
    }

    if resources is not None:
        cost = resources.total()
        result["resources"] = asdict(resources)
        result["resource_cost"] = cost
        result["mvpa"] = (verified_value / cost) if verified_value is not None and cost > 0 else None

        human_value = verified_value
        moment_cost = resources.attention + resources.time + resources.compute
        result["mvpm"] = (human_value / moment_cost) if human_value is not None and moment_cost > 0 else None

        learning_yield = normalized.get("L", 0.0)
        learning_cost = resources.attention + resources.time
        result["learning_efficiency"] = learning_yield / learning_cost if learning_cost > 0 else None

    if sensitivity:
        result["sensitivity"] = sensitivity_analysis(dimensions, profile, harm_n)

    return result


def _perturb_one_weight(weights: Mapping[str, float], dimension: str, delta: float, direction: int) -> dict[str, float]:
    """Shift one declared weight, then renormalize the complete profile."""
    shifted = dict(weights)
    shifted[dimension] = max(0.0, shifted[dimension] * (1.0 + direction * delta))
    total = sum(shifted.values())
    return {d: w / total for d, w in shifted.items()}


def sensitivity_analysis(
    dimensions: Mapping[str, Optional[float]],
    profile: ValueProfile,
    harm: float = 0.0,
) -> dict:
    base = profile.weights()
    scenarios = []
    for dimension in base:
        for direction in (-1, 1):
            w = _perturb_one_weight(base, dimension, profile.sensitivity_delta, direction)
            positive = sum(w[d] * _clamp(dimensions.get(d, 0.0) or 0.0) for d in w)
            scenarios.append({
                "dimension": dimension,
                "direction": direction,
                "score": _clamp(positive - _clamp(harm)),
            })
    baseline = _clamp(
        sum(base[d] * _clamp(dimensions.get(d, 0.0) or 0.0) for d in base)
        - _clamp(harm)
    )
    scores = [baseline, *(s["score"] for s in scenarios)]
    return {
        "delta": profile.sensitivity_delta,
        "baseline": baseline,
        "minimum": min(scores),
        "maximum": max(scores),
        "spread": max(scores) - min(scores),
        "stable_within_delta": (max(scores) - min(scores)) <= profile.sensitivity_delta,
        "scenario_scores": scenarios,
    }
