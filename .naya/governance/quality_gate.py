"""Deterministic TUNE IN quality boundary for NayaPOWER.

This gate is deliberately separate from model reasoning: the model/runtime must
supply explicit predicates, and this module decides whether delivery/execution
may cross the quality boundary. No quality dimension can be averaged away.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class QualityGateInput:
    intent_understood: bool
    context_complete: bool
    material_unknowns: Tuple[str, ...]
    consequence: int
    quality_ready: bool
    evidence_ready: bool

    def __post_init__(self) -> None:
        if not isinstance(self.consequence, int) or not 0 <= self.consequence <= 10:
            raise ValueError("consequence must be an integer from 0 to 10")
        unknowns = tuple(item.strip() for item in self.material_unknowns if str(item).strip())
        object.__setattr__(self, "material_unknowns", unknowns)


@dataclass(frozen=True)
class QualityGateResult:
    allowed: bool
    state: str
    reasons: Tuple[str, ...]
    required_actions: Tuple[str, ...]


def evaluate_quality(gate: QualityGateInput, *, consequential: bool = True) -> QualityGateResult:
    """Fail closed when TUNE IN predicates are absent or materially unsatisfied."""
    reasons: list[str] = []
    required: list[str] = []

    if not gate.intent_understood:
        reasons.append("intent understanding predicate is false")
        required.append("DEEPEN: resolve actual human intent")
    if not gate.context_complete:
        reasons.append("context completeness predicate is false")
        required.append("DEEPEN: restore the relevant system/project context")
    if gate.material_unknowns:
        reasons.append("material unknowns remain")
        required.append("DEEPEN: resolve material unknowns or explicitly escalate")
    if not gate.quality_ready:
        reasons.append("quality readiness predicate is false")
        required.append("INSPECT: improve the proposed outcome before delivery/execution")
    if consequential and not gate.evidence_ready:
        reasons.append("evidence readiness predicate is false")
        required.append("DEEPEN: define how success will be observed and verified")

    if reasons:
        return QualityGateResult(
            allowed=False,
            state="DEEPEN_INSPECT_REQUIRED",
            reasons=tuple(reasons),
            required_actions=tuple(dict.fromkeys(required)),
        )

    return QualityGateResult(
        allowed=True,
        state="TUNE_IN_PASS",
        reasons=("all TUNE IN predicates satisfied",),
        required_actions=(),
    )


def evaluate_delivery(gate: QualityGateInput) -> QualityGateResult:
    """Gate consequential Naya output before it is delivered to the human."""
    return evaluate_quality(gate, consequential=True)


def evaluate_execution(gate: QualityGateInput) -> QualityGateResult:
    """Gate consequential Naya execution before an external effect is permitted."""
    return evaluate_quality(gate, consequential=True)
