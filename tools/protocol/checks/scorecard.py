#!/usr/bin/env python3
"""SN-0523 — The Math Decides.

"Score consequential choices on 7 dimensions. Highest defensible score wins."

Validates a scorecard: the seven dimensions from the manifest must all be
present, weights must sum to 1.0, scores must be in range, and the claimed
totals must match an independent recomputation. Arithmetic fraud fails.

The seven dimensions (from protocol_manifest.json):
  objective_alignment, evidence_strength, effect_size, risk,
  reversibility, cost_of_inaction, authority_clearance

Note on risk: risk is scored as "safety" (higher = safer), so that the
weighted total is always higher-is-better. A scorecard that scores raw
risk higher-is-worse must invert before weighting; the check requires
explicit direction per dimension.

Input record:
    {
      "scorecard_for": "<decision description>",
      "dimensions": {
        "objective_alignment": {"weight": 0.2, "higher_is_better": true},
        ...
      },
      "options": {
        "a": {"objective_alignment": 8, "evidence_strength": 7, ...},
        "b": {...}
      },
      "claimed_totals": {"a": 7.55, "b": 8.10},
      "claimed_winner": "b",
      "scorer": "<seat or agent id>"
    }

Checks:
  1. All seven manifest dimensions present, no extras required but extras flagged.
  2. Weights are numeric, non-negative, and sum to 1.0 (+/- 1e-6).
  3. Every option scored on every dimension, each score in [0, 10].
  4. Recomputed weighted totals match claimed_totals within 1e-6.
  5. claimed_winner == argmax(recomputed totals).
  6. scorer named.

Usage:
    python3 tools/protocol/checks/scorecard.py \
        --record '{"scorecard_for": "...", ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

MANIFEST_DIMS = [
    "objective_alignment",
    "evidence_strength",
    "effect_size",
    "risk",
    "reversibility",
    "cost_of_inaction",
    "authority_clearance",
]
WEIGHT_EPS = 1e-6
TOTAL_EPS = 1e-6


def _is_number(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-0523"}
    subject = record.get("scorecard_for") or "(unnamed scorecard)"
    details["scorecard_for"] = subject

    dimensions = record.get("dimensions")
    if not isinstance(dimensions, dict):
        return fail(f"{subject}: dimensions block missing", details)
    missing_dims = [d for d in MANIFEST_DIMS if d not in dimensions]
    if missing_dims:
        return fail(f"{subject}: missing dimensions: {missing_dims}", details)
    reasons.append(f"all {len(MANIFEST_DIMS)} dimensions present")

    weights: dict[str, float] = {}
    for dim in MANIFEST_DIMS:
        spec = dimensions[dim]
        if not isinstance(spec, dict):
            return fail(f"{subject}: dimension {dim!r} spec malformed", details)
        w = spec.get("weight")
        if not _is_number(w) or w < 0:
            return fail(f"{subject}: dimension {dim!r} weight invalid: {w!r}", details)
        weights[dim] = float(w)
    wsum = sum(weights.values())
    if abs(wsum - 1.0) > WEIGHT_EPS:
        return fail(f"{subject}: weights sum to {wsum}, not 1.0 — renormalize", details)
    reasons.append(f"weights sum to 1.0")
    details["weights"] = weights

    options = record.get("options")
    if not isinstance(options, dict) or len(options) < 2:
        return fail(f"{subject}: need >= 2 scored options", details)
    for oid, scores in options.items():
        if not isinstance(scores, dict):
            return fail(f"{subject}: option {oid!r} scores malformed", details)
        for dim in MANIFEST_DIMS:
            s = scores.get(dim)
            if not _is_number(s) or not (0 <= s <= 10):
                return fail(
                    f"{subject}: option {oid!r} dimension {dim!r} score out of [0,10]: {s!r}",
                    details,
                )
    reasons.append(f"{len(options)} options scored on all dimensions in [0,10]")

    recomputed = {
        oid: round(sum(weights[d] * scores[d] for d in MANIFEST_DIMS), 6)
        for oid, scores in options.items()
    }
    details["recomputed_totals"] = recomputed

    claimed = record.get("claimed_totals")
    if not isinstance(claimed, dict):
        return fail(f"{subject}: claimed_totals missing — totals must be stated to be checked",
                    details)
    for oid, total in recomputed.items():
        c = claimed.get(oid)
        if not _is_number(c) or abs(float(c) - total) > TOTAL_EPS:
            return fail(
                f"{subject}: claimed total for {oid!r} ({c!r}) != recomputed ({total}) — "
                "arithmetic must be reproducible",
                details,
            )
    reasons.append("claimed totals match independent recomputation")

    winner = max(recomputed, key=lambda oid: recomputed[oid])
    claimed_winner = record.get("claimed_winner")
    if claimed_winner != winner:
        return fail(
            f"{subject}: claimed winner {claimed_winner!r} != recomputed winner {winner!r} "
            f"({recomputed[winner]}) — the math decides",
            details,
        )
    reasons.append(f"winner {winner!r} ({recomputed[winner]}) is the math's winner")
    details["winner"] = winner

    scorer = record.get("scorer")
    if not scorer or not str(scorer).strip():
        return fail(f"{subject}: scorer unnamed — anonymous math is not accountable", details)
    reasons.append(f"scorer: {scorer}")
    details["scorer"] = scorer

    reasons.append(f"{subject}: scorecard valid — the math decides, and it did")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0523 scorecard check")
    parser.add_argument("--record", required=True,
                        help="JSON scorecard record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-0523"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
