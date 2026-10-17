#!/usr/bin/env python3
"""EVOLVE meta-learning trend comparator (v1).

Compares two `evolve_meta_learning.py` evidence bundles (baseline -> current)
and emits the DELTA: is the learning system getting better at getting better?

Read-only on both input bundles; writes one trend JSON to --out. Stdlib only.
Fail-closed: exit 2 on any malformed input, with the error naming the defect.

The trend bundle deliberately carries NO score. A machine that scores its own
learning trajectory is theater; the EVOLVE area score is made by a human from
this evidence.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

ENVELOPE_VERSION = 1
REQUIRED_METRIC_BLOCKS = (
    "total_entries",
    "ingestion_velocity",
    "status_mix",
    "integration_coverage",
    "stale_unintegrated",
    "calibration_churn",
    "receipt_health",
    "authority_gate_load",
)


def _fail(msg: str) -> "NoReturn":  # noqa: F821
    print(f"evolve_meta_trend: ERROR: {msg}", file=sys.stderr)
    sys.exit(2)


def _load_bundle(path: str, label: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        _fail(f"{label} bundle not found: {path}")
    except json.JSONDecodeError as exc:
        _fail(f"{label} bundle is not valid JSON: {path} ({exc})")
    except OSError as exc:
        _fail(f"{label} bundle unreadable: {path} ({exc})")
    if not isinstance(data, dict):
        _fail(f"{label} bundle top level is not a mapping: {path}")
    if data.get("version") != ENVELOPE_VERSION:
        _fail(
            f"{label} bundle envelope version {data.get('version')!r} != "
            f"expected {ENVELOPE_VERSION}: {path} (metric semantics may differ)"
        )
    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        _fail(f"{label} bundle has no metrics mapping: {path}")
    missing = [b for b in REQUIRED_METRIC_BLOCKS if b not in metrics]
    if missing:
        _fail(f"{label} bundle missing metric blocks {missing}: {path}")
    return data


def _as_id_set(ids, label: str, bundle_label: str) -> set:
    if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
        _fail(f"{label} ids in {bundle_label} bundle are not a list of strings")
    return set(ids)


def _delta(a: float, b: float) -> float:
    return round(b - a, 6)


def build_trend(baseline: dict, current: dict) -> dict:
    bm, cm = baseline["metrics"], current["metrics"]

    # --- entries ---
    entries_delta = cm["total_entries"] - bm["total_entries"]

    # --- velocity per UTC day ---
    bv = bm["ingestion_velocity"]["per_day"]
    cv = cm["ingestion_velocity"]["per_day"]
    if not isinstance(bv, dict) or not isinstance(cv, dict):
        _fail("ingestion_velocity.per_day is not a mapping in one bundle")
    velocity_delta = {
        day: cv.get(day, 0) - bv.get(day, 0) for day in sorted(set(bv) | set(cv))
    }

    # --- status mix ---
    bc, cc = bm["status_mix"]["counts"], cm["status_mix"]["counts"]
    bf, cf = bm["status_mix"]["fractions"], cm["status_mix"]["fractions"]
    status_delta = {
        s: {
            "count_delta": cc.get(s, 0) - bc.get(s, 0),
            "fraction_delta": _delta(bf.get(s, 0.0), cf.get(s, 0.0)),
        }
        for s in sorted(set(bc) | set(cc))
    }

    # --- integration coverage (filed != adopted; the caveat rides along) ---
    coverage_delta = _delta(
        bm["integration_coverage"]["fraction"], cm["integration_coverage"]["fraction"]
    )

    # --- stale learning debt: newly-stale vs resolved ---
    b_stale = _as_id_set(bm["stale_unintegrated"]["ids"], "stale_unintegrated", "baseline")
    c_stale = _as_id_set(cm["stale_unintegrated"]["ids"], "stale_unintegrated", "current")
    stale_delta = {
        "count_delta": cm["stale_unintegrated"]["count"] - bm["stale_unintegrated"]["count"],
        "newly_stale": sorted(c_stale - b_stale),
        "resolved": sorted(b_stale - c_stale),
    }
    threshold_mismatch = (
        bm["stale_unintegrated"].get("threshold_days")
        != cm["stale_unintegrated"].get("threshold_days")
    )

    # --- calibration churn: NEW self-corrections since baseline = meta-learning happening ---
    b_churn = _as_id_set(bm["calibration_churn"]["ids"], "calibration_churn", "baseline")
    c_churn = _as_id_set(cm["calibration_churn"]["ids"], "calibration_churn", "current")
    churn_delta = {
        "count_delta": cm["calibration_churn"]["count"] - bm["calibration_churn"]["count"],
        "new_self_corrections": sorted(c_churn - b_churn),
        "note": (
            "Entries that supersede an earlier lesson since the baseline: "
            "the system correcting itself. This is the meta-learning signal."
        ),
    }

    # --- authority gate load ---
    gate_delta = {
        "flagged_delta": cm["authority_gate_load"]["flagged"]
        - bm["authority_gate_load"]["flagged"],
        "fraction_delta": _delta(
            bm["authority_gate_load"]["fraction_of_total"],
            cm["authority_gate_load"]["fraction_of_total"],
        ),
    }

    # --- receipt health ---
    b_miss = _as_id_set(bm["receipt_health"]["missing_ids"], "receipt_health", "baseline")
    c_miss = _as_id_set(cm["receipt_health"]["missing_ids"], "receipt_health", "current")
    receipt_delta = {
        "missing_delta": cm["receipt_health"]["missing"] - bm["receipt_health"]["missing"],
        "newly_missing": sorted(c_miss - b_miss),
        "recovered": sorted(b_miss - c_miss),
        "checks_pass_delta": cm["receipt_health"]["checks_pass"]
        - bm["receipt_health"]["checks_pass"],
        "checks_fail_delta": cm["receipt_health"]["checks_fail"]
        - bm["receipt_health"]["checks_fail"],
    }

    trend = {
        "tool": "evolve_meta_trend",
        "version": ENVELOPE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "baseline": {
            "generated_at": baseline.get("generated_at"),
            "total_entries": bm["total_entries"],
        },
        "current": {
            "generated_at": current.get("generated_at"),
            "total_entries": cm["total_entries"],
        },
        "threshold_mismatch": threshold_mismatch,
        "deltas": {
            "entries_delta": entries_delta,
            "ingestion_velocity_per_day": velocity_delta,
            "status_mix": status_delta,
            "integration_coverage_fraction_delta": coverage_delta,
            "stale_learning_debt": stale_delta,
            "calibration_churn": churn_delta,
            "authority_gate_load": gate_delta,
            "receipt_health": receipt_delta,
        },
        "caveats": [
            "Deltas describe the ledger's shape changing, not proof that learning improved.",
            "integration_coverage measures filing, not adoption: filed != adopted.",
            "A rising INGESTED count with flat RATIFIED is throughput, not progress.",
            "new_self_corrections is the meta-learning signal that matters most: "
            "the system correcting its own earlier lessons.",
            "Bundle generated_at values are only comparable when both bundles were "
            "produced by the same evolve_meta_learning.py version.",
        ]
        + (
            [
                "WARNING: stale threshold_days differed between bundles; "
                "stale-debt deltas are not strictly comparable."
            ]
            if threshold_mismatch
            else []
        ),
    }
    return trend


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Compare two evolve_meta_learning evidence bundles; emit the delta."
    )
    ap.add_argument("--baseline", required=True, help="baseline bundle JSON")
    ap.add_argument("--current", required=True, help="current bundle JSON")
    ap.add_argument("--out", required=True, help="where to write the trend JSON")
    args = ap.parse_args(argv)

    baseline = _load_bundle(args.baseline, "baseline")
    current = _load_bundle(args.current, "current")
    trend = build_trend(baseline, current)

    try:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(trend, fh, indent=2, sort_keys=False)
            fh.write("\n")
    except OSError as exc:
        _fail(f"cannot write trend bundle: {args.out} ({exc})")

    print(
        f"trend: {trend['baseline']['total_entries']} -> "
        f"{trend['current']['total_entries']} entries "
        f"(delta {trend['deltas']['entries_delta']}); "
        f"new self-corrections: "
        f"{len(trend['deltas']['calibration_churn']['new_self_corrections'])}; "
        f"stale debt delta: {trend['deltas']['stale_learning_debt']['count_delta']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
