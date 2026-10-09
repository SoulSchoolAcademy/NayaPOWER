#!/usr/bin/env python3
"""EVOLVE meta-learning health instrument — measure whether the system is
getting better at getting better.

The EVOLVE area is defined as "the system getting better at getting better:
self-improvement discipline, meta-learning (optimizing how we learn), RSI
hygiene, compounding intelligence across generations". The LEARN machinery
ingests Smart Notes into a ledger (ledger.json), integrates them into doctrine
files, and promotes some to RATIFIED. But nothing measures whether the
LEARNING ITSELF is improving — velocity, promotion rate, calibration churn,
learning debt. This tool computes those meta-metrics from a learn-state root.

It deliberately never emits a score. A machine that scores its own learning
is theater; the EVOLVE area score is made by a human from this evidence.
(Honesty boundary, shared with tools/evolve_receipt.py.)

Inputs (--learn-root):
  ledger.json — {"version", "branch", "branch_sha_at_scan", "updated_at",
                 "entries": {"<SN-ID>": {...}}}
    entry: {"ingested_at": "<ISO-8601>", "status": "<STATUS>",
            "classification": "<CLASS>", "integrations": [{"anchor", "target"}],
            "receipt": "<path>", "supersedes": <null|str|list>,
            "blob_sha", "content_sha256", "repo_path", "run_id"}
  receipts/   — optional; <SN-ID>.json per entry with "checks": [{"check", "result"}]

Metrics (all measured, none scored):
  ingestion_velocity   — entries per calendar day (UTC) across the observed window
  status_mix           — counts and fractions per ledger status
  integration_coverage — fraction of non-duplicate entries with >= 1 integration
                         (learning that landed somewhere vs. learning merely filed)
  integration_targets  — counter of integration target files (where learning lands)
  stale_unintegrated   — INGESTED entries older than --stale-days with zero
                         integrations: learning debt
  calibration_churn    — entries with non-empty "supersedes": the system
                         correcting its own earlier lessons (the meta-learning
                         signal that matters most)
  receipt_health       — receipts found vs. missing; check PASS/FAIL counts
  authority_gate_load  — FLAGGED_AUTHORITY count and fraction (the admission
                         gate's current queue)

Fail-closed contract:
  exit 0 — the bundle was written.
  exit 2 — fail-closed: --learn-root missing, ledger.json unreadable or
           malformed, entries not a mapping. The error names the defect.
           (exit 1 is reserved for operational refusals; a read-only scan has none.)

Every bundle carries an explicit caveats block: these metrics describe the
ledger's shape, not proof that learning improved. Integration != behavioral
adoption. A high RATIFIED fraction reflects gate state, not value.

Stdlib only. --learn-root is never written to; --out may be anywhere.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL = "evolve_meta_learning"
VERSION = 1

DUPLICATE_STATUS = "DUPLICATE_OF"
INGESTED_STATUS = "INGESTED"
AUTHORITY_STATUS = "FLAGGED_AUTHORITY"


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _parse_ts(raw: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp; None when unparseable."""
    if not isinstance(raw, str) or not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def _as_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _load_ledger(learn_root: Path) -> dict:
    if not learn_root.is_dir():
        raise ScanError(f"learn-root is not a directory: {learn_root}")
    ledger_path = learn_root / "ledger.json"
    if not ledger_path.is_file():
        raise ScanError(f"ledger.json not found under learn-root: {learn_root}")
    try:
        raw = ledger_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ScanError(f"ledger.json unreadable: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ScanError(f"ledger.json is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ScanError("ledger.json top level must be an object")
    entries = data.get("entries")
    if not isinstance(entries, dict):
        raise ScanError("ledger.json must contain an 'entries' mapping")
    return data


class ScanError(Exception):
    """Fail-closed input defect; maps to exit 2."""


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def _fraction(part: int, whole: int) -> float | None:
    return round(part / whole, 4) if whole else None


def compute_metrics(entries: dict, receipts_dir: Path, stale_days: int,
                    now: datetime) -> dict:
    total = len(entries)
    status_mix = Counter()
    dates: list[datetime] = []
    integrated_ids: list[str] = []
    targets: Counter = Counter()
    stale_ids: list[str] = []
    churn_ids: list[str] = []
    learnable_total = 0  # entries that represent real learning attempts

    for sn_id, entry in entries.items():
        if not isinstance(entry, dict):
            continue
        status = entry.get("status")
        status_mix[status if isinstance(status, str) else "UNKNOWN"] += 1

        ts = _parse_ts(entry.get("ingested_at"))
        if ts is not None:
            dates.append(ts)

        integrations = entry.get("integrations")
        integrations = integrations if isinstance(integrations, list) else []
        is_duplicate = status == DUPLICATE_STATUS
        if not is_duplicate:
            learnable_total += 1
        if integrations:
            integrated_ids.append(sn_id)
            for item in integrations:
                if isinstance(item, dict) and isinstance(item.get("target"), str):
                    targets[item["target"]] += 1

        if (status == INGESTED_STATUS and not integrations and ts is not None
                and (now - ts).days > stale_days):
            stale_ids.append(sn_id)

        if _as_list(entry.get("supersedes")):
            churn_ids.append(sn_id)

    # Velocity: entries per UTC calendar day across the observed window.
    velocity: dict[str, int] = {}
    if dates:
        lo = min(dates).date()
        hi = max(dates).date()
        day = lo
        while day <= hi:
            velocity[day.isoformat()] = 0
            day = day.fromordinal(day.toordinal() + 1)
        for d in dates:
            velocity[d.date().isoformat()] += 1

    status_counts = dict(status_mix)
    status_fractions = {
        s: _fraction(c, total) for s, c in status_counts.items()
    }

    # Receipt health: a missing receipt means ingestion without a verification artifact.
    receipt_health: dict[str, Any] = {"receipts_dir_present": receipts_dir.is_dir(),
                                      "found": 0, "missing": 0,
                                      "checks_pass": 0, "checks_fail": 0,
                                      "missing_ids": []}
    if receipts_dir.is_dir():
        for sn_id in entries:
            rp = receipts_dir / f"{sn_id}.json"
            if not rp.is_file():
                receipt_health["missing"] += 1
                receipt_health["missing_ids"].append(sn_id)
                continue
            receipt_health["found"] += 1
            try:
                receipt = json.loads(rp.read_text(encoding="utf-8"))
                checks = receipt.get("checks") if isinstance(receipt, dict) else None
                for check in checks if isinstance(checks, list) else []:
                    result = check.get("result") if isinstance(check, dict) else None
                    if result == "PASS":
                        receipt_health["checks_pass"] += 1
                    elif result == "FAIL":
                        receipt_health["checks_fail"] += 1
            except (OSError, json.JSONDecodeError, UnicodeDecodeError):
                receipt_health["missing"] += 1
                receipt_health["found"] -= 1
                receipt_health["missing_ids"].append(sn_id)

    return {
        "total_entries": total,
        "learnable_entries": learnable_total,
        "ingestion_velocity": {
            "per_day": velocity,
            "days_covered": len(velocity),
            "peak_day": max(velocity, key=velocity.get) if velocity else None,
        },
        "status_mix": {"counts": status_counts, "fractions": status_fractions},
        "integration_coverage": {
            "integrated": len(integrated_ids),
            "denominator": learnable_total,
            "fraction": _fraction(len(integrated_ids), learnable_total),
            "note": "DUPLICATE_OF entries excluded from the denominator; "
                    "they are not real learning attempts.",
        },
        "integration_targets": dict(targets),
        "stale_unintegrated": {
            "threshold_days": stale_days,
            "count": len(stale_ids),
            "ids": sorted(stale_ids),
            "note": "INGESTED, zero integrations, older than the threshold: "
                    "learning debt — observed but never applied.",
        },
        "calibration_churn": {
            "count": len(churn_ids),
            "fraction_of_total": _fraction(len(churn_ids), total),
            "ids": sorted(churn_ids),
            "note": "Entries that supersede an earlier lesson: the system "
                    "correcting itself. The meta-learning signal that matters most.",
        },
        "receipt_health": receipt_health,
        "authority_gate_load": {
            "flagged": status_counts.get(AUTHORITY_STATUS, 0),
            "fraction_of_total": _fraction(status_counts.get(AUTHORITY_STATUS, 0), total),
            "note": "FLAGGED_AUTHORITY is the admission gate's queue: lessons "
                    "held for authority review, not yet integrated.",
        },
    }


CAVEATS = [
    "These metrics describe the ledger's shape, not proof that learning improved.",
    "An integration target (e.g. learn/lessons.md) records that a lesson was "
    "filed, not that behavior changed. Filed != adopted.",
    "A high RATIFIED fraction reflects gate state, not value delivered.",
    "Velocity spikes may reflect batch backfill, not faster learning.",
    "This bundle deliberately carries no score. A machine that scores its own "
    "learning is theater; the EVOLVE area score is made by a human from evidence.",
]


def scan(learn_root: Path, out: Path, stale_days: int,
         now: datetime | None = None) -> dict:
    """Run the scan; write the bundle; return it. Raises ScanError (exit 2)."""
    ledger = _load_ledger(learn_root)
    entries = ledger["entries"]
    now = now or datetime.now(timezone.utc)
    metrics = compute_metrics(entries, learn_root / "receipts", stale_days, now)
    bundle = {
        "tool": TOOL,
        "version": VERSION,
        "generated_at": now.isoformat(),
        "learn_root": str(learn_root),
        "ledger": {
            "version": ledger.get("version"),
            "branch": ledger.get("branch"),
            "branch_sha_at_scan": ledger.get("branch_sha_at_scan"),
            "updated_at": ledger.get("updated_at"),
        },
        "metrics": metrics,
        "caveats": CAVEATS,
    }
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise ScanError(f"cannot write bundle to {out}: {exc}") from exc
    return bundle


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="EVOLVE meta-learning health instrument: measure whether "
                    "the system is getting better at getting better. Read-only "
                    "on --learn-root; writes the evidence bundle to --out."
    )
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("scan", help="scan a learn-state root and write the bundle")
    s.add_argument("--learn-root", required=True,
                   help="directory containing ledger.json (+ optional receipts/)")
    s.add_argument("--out", required=True, help="where to write the JSON bundle")
    s.add_argument("--stale-days", type=int, default=7,
                   help="age in days after which an unintegrated INGESTED entry "
                        "counts as learning debt (default 7)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "scan":
        if args.stale_days < 0:
            print("error: --stale-days must be >= 0", file=sys.stderr)
            return 2
        try:
            bundle = scan(Path(args.learn_root), Path(args.out), args.stale_days)
        except ScanError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        m = bundle["metrics"]
        print(f"scanned {m['total_entries']} entries -> {args.out}")
        print(f"  integration coverage: {m['integration_coverage']['fraction']}")
        print(f"  stale (learning debt): {m['stale_unintegrated']['count']}")
        print(f"  calibration churn: {m['calibration_churn']['count']}")
        print(f"  authority gate load: {m['authority_gate_load']['flagged']}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
