"""Deterministic NayaPOWER value calculus. Measures declared value; never human worth."""

from dataclasses import dataclass
from math import isfinite
from typing import Mapping

class ValueCalculusError(ValueError):
    pass

@dataclass(frozen=True)
class Dimension:
    name: str
    value: float
    weight: float
    required: bool = False

@dataclass(frozen=True)
class ScoreReceipt:
    objective: str
    dimensions: tuple[Dimension, ...]
    normalized_weights: tuple[tuple[str, float], ...]
    gross_value: float
    harm_cost: float
    net_value: float
    critical_failures: tuple[str, ...]
    status: str

def _finite(value: float, label: str) -> float:
    if not isfinite(value):
        raise ValueCalculusError(f'{label} must be finite')
    return value

def normalize_weights(weights: Mapping[str, float]) -> dict[str, float]:
    if not weights:
        raise ValueCalculusError('at least one weight is required')
    cleaned = {k: _finite(float(v), f'weight[{k}]') for k, v in weights.items()}
    if any(v < 0 for v in cleaned.values()):
        raise ValueCalculusError('weights cannot be negative')
    total = sum(cleaned.values())
    if total <= 0:
        raise ValueCalculusError('weight sum must be positive')
    return {k: v / total for k, v in cleaned.items()}

def adaptive_weights(base_weights: Mapping[str, float], *, objective_multipliers=None, context_multipliers=None, risk_multipliers=None) -> dict[str, float]:
    objective_multipliers = objective_multipliers or {}
    context_multipliers = context_multipliers or {}
    risk_multipliers = risk_multipliers or {}
    effective = {}
    for name, base in base_weights.items():
        factors = (float(base), float(objective_multipliers.get(name, 1.0)), float(context_multipliers.get(name, 1.0)), float(risk_multipliers.get(name, 1.0)))
        if any(not isfinite(x) or x < 0 for x in factors):
            raise ValueCalculusError(f'invalid weight multiplier for {name}')
        effective[name] = factors[0] * factors[1] * factors[2] * factors[3]
    return normalize_weights(effective)

def score(objective: str, dimensions: Mapping[str, float], weights: Mapping[str, float], *, harm_cost: float = 0.0, critical_failures: tuple[str, ...] = (), required_dimensions: tuple[str, ...] = ()) -> ScoreReceipt:
    if not objective.strip():
        raise ValueCalculusError('objective is required')
    normalized = normalize_weights(weights)
    missing = [name for name in required_dimensions if name not in dimensions]
    if missing:
        raise ValueCalculusError(f'missing required dimensions: {", ".join(missing)}')
    values = {}
    for name in normalized:
        if name not in dimensions:
            raise ValueCalculusError(f'missing dimension: {name}')
        value = _finite(float(dimensions[name]), f'dimension[{name}]')
        if not 0.0 <= value <= 1.0:
            raise ValueCalculusError(f'dimension[{name}] must be between 0 and 1')
        values[name] = value
    harm = _finite(float(harm_cost), 'harm_cost')
    if harm < 0:
        raise ValueCalculusError('harm_cost cannot be negative')
    gross = sum(normalized[name] * values[name] for name in normalized)
    status = 'BLOCKED' if critical_failures else 'MEASURED'
    dims = tuple(Dimension(name, values[name], normalized[name], name in required_dimensions) for name in normalized)
    return ScoreReceipt(objective, dims, tuple(sorted(normalized.items())), gross, harm, gross - harm, tuple(critical_failures), status)

def mvpa(verified_value: float, resources_consumed: float) -> float:
    verified_value = _finite(float(verified_value), 'verified_value')
    resources_consumed = _finite(float(resources_consumed), 'resources_consumed')
    if resources_consumed <= 0:
        raise ValueCalculusError('resources_consumed must be positive')
    return verified_value / resources_consumed

def mvpm(verified_human_value: float, human_attention: float, human_time: float, system_cost: float) -> float:
    values = tuple(_finite(float(x), name) for x, name in ((verified_human_value, 'verified_human_value'), (human_attention, 'human_attention'), (human_time, 'human_time'), (system_cost, 'system_cost')))
    denominator = sum(values[1:])
    if denominator <= 0:
        raise ValueCalculusError('MVPM resource denominator must be positive')
    return values[0] / denominator