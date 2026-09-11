#!/usr/bin/env python3
"""Deterministic, fail-closed Naya Power decision calculus."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "SUPERBRAIN" / "naya_power_decision_calculus.json"

EVIDENCE_RANK = {name: i for i, name in enumerate(["UNKNOWN", "IMPLEMENTED", "TESTED", "VERIFIED", "RUNTIME-PROVEN", "PRODUCTION-PROVEN"])}


@dataclass(frozen=True)
class Candidate:
    name: str
    useful_value: float
    harm_avoidance: float
    verification_strength: float
    quality: float
    reversibility: float
    cost_efficiency: float
    latency: float
    uncertainty: float
    evidence_state: str
    violates_boundary: bool = False
    consequence: float = 0.0


def load_policy() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def score(candidate: Candidate, policy: dict) -> float:
    if candidate.violates_boundary:
        return float("-inf")
    if candidate.evidence_state not in EVIDENCE_RANK:
        return float("-inf")
    d = policy["dimensions"]
    values = {
        "useful_value": candidate.useful_value,
        "harm_avoidance": candidate.harm_avoidance,
        "verification_strength": candidate.verification_strength,
        "quality": candidate.quality,
        "reversibility": candidate.reversibility,
        "cost_efficiency": candidate.cost_efficiency,
        "latency": candidate.latency,
        "uncertainty": 100.0 - candidate.uncertainty,
    }
    weighted = sum(values[k] * d[k] for k in d) / sum(d.values())
    consequence_penalty = (candidate.consequence * candidate.uncertainty) / 100.0
    return weighted - consequence_penalty


def choose(candidates: list[Candidate], policy: dict) -> Candidate | None:
    eligible = [c for c in candidates if not c.violates_boundary]
    if not eligible:
        return None
    ranked = sorted(eligible, key=lambda c: (score(c, policy), c.reversibility, EVIDENCE_RANK[c.evidence_state]), reverse=True)
    best = ranked[0]
    if EVIDENCE_RANK[best.evidence_state] < EVIDENCE_RANK[policy["minimum_delivery_evidence"]]:
        # The calculus may select a next action below delivery evidence; it may not call it verified.
        return best
    return best


def decision(candidates: list[Candidate]) -> dict:
    policy = load_policy()
    ranked = sorted(
        ((c, score(c, policy)) for c in candidates if not c.violates_boundary),
        key=lambda item: (item[1], item[0].reversibility, EVIDENCE_RANK[item[0].evidence_state]),
        reverse=True,
    )
    chosen = ranked[0][0] if ranked else None
    if chosen is not None and chosen.consequence >= 80 and chosen.uncertainty >= 60 and EVIDENCE_RANK[chosen.evidence_state] < EVIDENCE_RANK["VERIFIED"]:
        disposition = "DEFER_FOR_VERIFICATION"
    else:
        disposition = "CHOOSE" if chosen else "REJECT_ALL"
    return {
        "chosen": chosen.name if chosen else None,
        "disposition": disposition,
        "ranked": [{"name": c.name, "score": round(s, 4), "evidence_state": c.evidence_state} for c, s in ranked],
        "boundary_rejections": [c.name for c in candidates if c.violates_boundary],
        "verified_claim_allowed": bool(chosen and EVIDENCE_RANK[chosen.evidence_state] >= EVIDENCE_RANK["VERIFIED"] and disposition == "CHOOSE"),
    }


if __name__ == "__main__":
    example = [Candidate("safe_verified", 90, 95, 95, 92, 85, 80, 80, 10, "VERIFIED", consequence=20), Candidate("risky_unknown", 100, 40, 10, 90, 20, 90, 90, 80, "UNKNOWN", consequence=90)]
    print(json.dumps(decision(example), indent=2))
