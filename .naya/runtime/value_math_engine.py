"""NayaNET Value and Math Engine V1.

CONSTITUTION -> ELIGIBILITY -> VALUE -> MVPA -> DECISION

This module deliberately keeps hard constitutional eligibility separate from
numeric value. INVALID is not the same state as value 0.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

MIN_VALUE = -9
MAX_VALUE = 9
NEUTRAL_VALUE = 0


@dataclass(frozen=True)
class ValueContext:
    objective: str
    weights: Mapping[str, float]

    def __post_init__(self) -> None:
        if not self.objective.strip():
            raise ValueError("ValueContext requires a non-empty objective.")
        if not self.weights:
            raise ValueError("ValueContext requires at least one value dimension.")
        if any(weight < 0 for weight in self.weights.values()):
            raise ValueError("Value weights cannot be negative.")
        total = sum(self.weights.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError("Value weights must sum to 1.0.")


def constitutional_eligibility(*, constitution_ok: bool, authorized: bool = True,
                                permitted: bool = True) -> str:
    """Return ELIGIBLE only when every hard gate passes."""
    return "ELIGIBLE" if constitution_ok and authorized and permitted else "INVALID"


def weighted_value(dimensions: Mapping[str, float], context: ValueContext) -> float:
    """Calculate a weighted raw value from objective-specific dimensions.

    Dimension scores must already be expressed on the bounded -9..+9 scale.
    """
    missing = set(context.weights) - set(dimensions)
    if missing:
        raise ValueError(f"Missing value dimensions: {sorted(missing)}")
    invalid = [name for name, score in dimensions.items()
               if score < MIN_VALUE or score > MAX_VALUE]
    if invalid:
        raise ValueError(f"Dimension scores must remain within -9..+9: {invalid}")
    return sum(context.weights[name] * dimensions[name] for name in context.weights)


def bounded_value(dimensions: Mapping[str, float], context: ValueContext) -> int:
    """Map a weighted assessment to the nearest bounded integer -9..+9."""
    raw = weighted_value(dimensions, context)
    return max(MIN_VALUE, min(MAX_VALUE, int(round(raw))))


def mvpa(*, verified_responsible_value: float, resource_cost: float) -> float:
    """Return value density / Max Value Per Action.

    Resource cost must be positive. The caller must supply a verified value and
    must already have passed constitutional and authority gates.
    """
    if resource_cost <= 0:
        raise ValueError("Resource cost must be greater than zero.")
    return verified_responsible_value / resource_cost


def rank_actions(actions: Sequence[Mapping[str, object]]) -> list[dict]:
    """Rank already-eligible actions by MVPA, highest first.

    Each action must provide: id, eligibility_state, verified_value,
    resource_cost. INVALID actions are excluded rather than penalized.
    """
    eligible: list[dict] = []
    for action in actions:
        if action.get("eligibility_state") != "ELIGIBLE":
            continue
        value = float(action["verified_value"])
        cost = float(action["resource_cost"])
        score = mvpa(verified_responsible_value=value, resource_cost=cost)
        eligible.append({**action, "mvpa": score})
    return sorted(eligible, key=lambda item: float(item["mvpa"]), reverse=True)


def choose_best_action(actions: Sequence[Mapping[str, object]]) -> dict:
    """Choose the highest-MVPA eligible action, or fail explicitly."""
    ranked = rank_actions(actions)
    if not ranked:
        raise ValueError("No constitutionally eligible and authorized action is available.")
    return ranked[0]
