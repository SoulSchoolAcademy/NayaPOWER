"""Naya Power Excellence by Default deterministic evaluator.

This module is intentionally conservative. It is a quality gate, not a replacement
for constitutional judgment or domain-specific verification.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Mapping, Sequence


POLICY_PATH = Path(__file__).with_name("naya_power_excellence_policy.json")


@dataclass(frozen=True)
class ExcellenceResult:
    status: str
    score: float
    threshold: float
    exceptional_target: float
    hard_gate_failures: tuple[str, ...]
    dimension_scores: dict[str, float]
    missing_evidence: tuple[str, ...]
    reasons: tuple[str, ...]

    @property
    def deliverable(self) -> bool:
        return self.status in {"PASS", "EXCEPTIONAL"}

    @property
    def exceptional(self) -> bool:
        return self.status == "EXCEPTIONAL"

    def to_dict(self) -> dict:
        return asdict(self)


def load_policy(path: Path | None = None) -> dict:
    policy_path = path or POLICY_PATH
    return json.loads(policy_path.read_text(encoding="utf-8"))


def _clamp(value: float) -> float:
    return max(0.0, min(10.0, float(value)))


def evaluate_excellence(
    dimension_scores: Mapping[str, float],
    *,
    gates: Mapping[str, bool] | None = None,
    evidence: Mapping[str, bool] | None = None,
    policy: Mapping | None = None,
) -> ExcellenceResult:
    """Evaluate an output using hard gates plus a weighted multi-objective score.

    `dimension_scores` contains 0..10 values for the dimensions present in the
    canonical policy. Missing dimensions are treated as missing evidence rather
    than silently receiving a perfect score.
    """
    policy = policy or load_policy()
    quality = policy["quality"]
    weights = quality["exceptional_dimensions"]
    threshold = float(quality["delivery_threshold"])
    exceptional_target = float(quality["exceptional_target"])

    normalized = {name: _clamp(dimension_scores[name]) for name in weights if name in dimension_scores}
    missing_dimensions = tuple(name for name in weights if name not in normalized)

    gate_failures = []
    supplied_gates = gates or {}
    for gate_name in policy["hard_gates"]:
        if supplied_gates.get(gate_name, False):
            gate_failures.append(gate_name)

    evidence = evidence or {}
    missing_evidence = tuple(name for name, present in evidence.items() if not present)

    if gate_failures:
        return ExcellenceResult(
            status="BLOCKED",
            score=0.0,
            threshold=threshold,
            exceptional_target=exceptional_target,
            hard_gate_failures=tuple(gate_failures),
            dimension_scores=normalized,
            missing_evidence=missing_evidence,
            reasons=("A hard constitutional, safety, authorization, integrity, or correctness gate failed.",),
        )

    if missing_dimensions:
        return ExcellenceResult(
            status="INSUFFICIENT_EVIDENCE",
            score=0.0,
            threshold=threshold,
            exceptional_target=exceptional_target,
            hard_gate_failures=(),
            dimension_scores=normalized,
            missing_evidence=tuple(sorted(set(missing_evidence + missing_dimensions))),
            reasons=("Required quality dimensions were not evaluated; conservative gate prevents silent passing.",),
        )

    score = round(sum(normalized[name] * float(weights[name]) for name in weights), 4)

    if missing_evidence:
        status = "INSUFFICIENT_EVIDENCE"
        reasons = ("Evidence is missing; score alone cannot establish verified completion.",)
    elif score >= exceptional_target:
        status = "EXCEPTIONAL"
        reasons = ("The result clears the exceptional target with no hard-gate failure.",)
    elif score >= threshold:
        status = "PASS"
        reasons = ("The result clears the delivery threshold with no hard-gate failure.",)
    else:
        status = "IMPROVE"
        reasons = ("The result is below the canonical delivery threshold and should be improved before delivery.",)

    return ExcellenceResult(
        status=status,
        score=score,
        threshold=threshold,
        exceptional_target=exceptional_target,
        hard_gate_failures=(),
        dimension_scores=normalized,
        missing_evidence=missing_evidence,
        reasons=reasons,
    )


def should_block_delivery(result: ExcellenceResult) -> bool:
    """Return True when the deterministic gate says the work is not ready."""
    return not result.deliverable


def render_receipt(result: ExcellenceResult) -> str:
    """Produce a compact human-readable quality receipt."""
    evidence = "complete" if not result.missing_evidence else ", ".join(result.missing_evidence)
    gates = "none" if not result.hard_gate_failures else ", ".join(result.hard_gate_failures)
    return (
        f"NAYA POWER EXCELLENCE RECEIPT\n"
        f"status={result.status}\n"
        f"score={result.score:.4f}/10\n"
        f"delivery_threshold={result.threshold:.1f}\n"
        f"exceptional_target={result.exceptional_target:.1f}\n"
        f"hard_gate_failures={gates}\n"
        f"missing_evidence={evidence}\n"
        f"deliverable={result.deliverable}"
    )


if __name__ == "__main__":
    # Smoke execution: intentionally demonstrates the evaluator without claiming
    # that a real artifact has been verified.
    sample = {name: 9.5 for name in load_policy()["quality"]["exceptional_dimensions"]}
    result = evaluate_excellence(sample, evidence={"runtime_observation": True})
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    print(render_receipt(result))
