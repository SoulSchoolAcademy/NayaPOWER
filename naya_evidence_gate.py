"""Fail-closed evidence gate for Naya intelligence evaluation receipts.

This module is intentionally small and deterministic. It does not decide whether
Naya is intelligent; it decides whether a supplied proof receipt contains the
minimum evidence required for the strength of claim it makes.

A receipt is untrusted input. Human-readable labels, filenames, or status strings
never substitute for execution, evidence, causal controls, measured change, or
cold continuation.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping


LEVELS = (
    "L0_ASSERTED",
    "L1_STRUCTURALLY_PRESENT",
    "L2_EXECUTED",
    "L3_BEHAVIORALLY_OBSERVED",
    "L4_VERIFIED",
    "L5_CAUSALLY_ATTRIBUTED",
    "L6_GENERALIZED",
    "L7_COMPOUNDED",
    "L8_COLD_SUCCESSOR_PROVEN",
)


@dataclass(frozen=True)
class Verdict:
    status: str
    evidence_level: str
    reasons: tuple[str, ...]


def load_receipt(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("receipt root must be an object")
    return value


def _has(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def evaluate_receipt(receipt: Mapping[str, Any]) -> Verdict:
    reasons: list[str] = []
    level = str(receipt.get("evidence_level", "L0_ASSERTED"))

    if level not in LEVELS:
        reasons.append(f"unknown evidence level: {level}")
        level = "L0_ASSERTED"

    # Every L2+ claim must identify a real execution and reproducible evidence.
    if LEVELS.index(level) >= LEVELS.index("L2_EXECUTED"):
        if not _has(receipt.get("execution_path")):
            reasons.append("execution evidence is missing")
        reproduction = receipt.get("reproduction")
        if not isinstance(reproduction, Mapping) or not _has(reproduction.get("command")):
            reasons.append("reproduction command is missing")
        if not _has(receipt.get("source_commit")):
            reasons.append("source commit is missing")
        if not _has(receipt.get("runtime_version")):
            reasons.append("runtime version is missing")

    # L3+ must have observable evidence, not merely a claimed result.
    if LEVELS.index(level) >= LEVELS.index("L3_BEHAVIORALLY_OBSERVED"):
        if not _has(receipt.get("evidence_ids")):
            reasons.append("observable evidence IDs are missing")
        if not _has(receipt.get("expected")) or not _has(receipt.get("actual")):
            reasons.append("expected/actual outcome pair is missing")
        if receipt.get("reproduction", {}).get("result") == "ASSERTION_ONLY":
            reasons.append("assertion-only reproduction cannot establish behavior")

    # L4+ must show authority and a verified result.
    if LEVELS.index(level) >= LEVELS.index("L4_VERIFIED"):
        if receipt.get("authority_decision") != "AUTHORIZED":
            reasons.append("verified claim lacks an explicit authorized decision")
        if receipt.get("failures"):
            reasons.append("unresolved failures remain")
        if receipt.get("uncertainties"):
            reasons.append("unresolved uncertainties remain")

    freshness = receipt.get("source_freshness", "CURRENT")
    if freshness in {"STALE", "UNKNOWN"}:
        reasons.append(f"evidence source is {freshness.lower()}")

    integrity = receipt.get("evaluator_integrity")
    required_controls = (
        "positive_control",
        "negative_control",
        "mutation_control",
        "contradiction_control",
        "stale_control",
        "cold_control",
    )
    if not isinstance(integrity, Mapping):
        reasons.append("evaluator integrity controls are missing")
    else:
        for control in required_controls:
            if integrity.get(control) != "PASS":
                reasons.append(f"evaluator {control.replace('_', ' ')} is not PASS")

    # Learning is a chain, not a boolean.
    learning = receipt.get("learning")
    if isinstance(learning, Mapping) and any(
        _has(learning.get(k))
        for k in ("lesson", "persisted", "retrieved", "behavior_changed", "measured_improvement")
    ):
        for key in ("outcome_observed", "lesson", "persisted", "retrieved", "behavior_changed"):
            if not learning.get(key):
                reasons.append(f"learning step '{key}' is not proven")
        if not isinstance(learning.get("measured_improvement"), (int, float)):
            reasons.append("learning requires measured improvement")

    # Causal attribution requires a counterfactual boundary.
    causal = receipt.get("causal")
    if isinstance(causal, Mapping) and _has(causal.get("claim")):
        if not _has(causal.get("control")):
            reasons.append("causal claim requires a control run")
        if not _has(causal.get("treatment")):
            reasons.append("causal claim requires a treatment run")
        if not isinstance(causal.get("confounders"), list):
            reasons.append("causal claim requires an explicit confounder list")

    # L8 is earned only by a real cold successor that acts.
    if LEVELS.index(level) >= LEVELS.index("L8_COLD_SUCCESSOR_PROVEN"):
        successor = receipt.get("cold_successor")
        if not isinstance(successor, Mapping) or not successor.get("cold_run"):
            reasons.append("cold successor run is not proven")
        if not isinstance(successor, Mapping) or not _has(successor.get("inherited_evidence")):
            reasons.append("successor inherited evidence is missing")
        if not isinstance(successor, Mapping) or not _has(successor.get("continuation_action")):
            reasons.append("successor continuation action is missing")

    return Verdict(
        status="PASS" if not reasons else "FAIL",
        evidence_level=level,
        reasons=tuple(reasons),
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate one Naya intelligence receipt.")
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()

    verdict = evaluate_receipt(load_receipt(args.receipt))
    print(f"STATUS={verdict.status}")
    print(f"EVIDENCE_LEVEL={verdict.evidence_level}")
    for reason in verdict.reasons:
        print(f"REASON={reason}")
    return 0 if verdict.status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
