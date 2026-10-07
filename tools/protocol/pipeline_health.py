#!/usr/bin/env python3
"""Pipeline health monitor for the NayaPOWER learning pipeline.

The pipeline: CAPTURE -> PERSIST -> RECEIPT -> SMART LINK -> COLD RETRIEVE
-> COMPREHEND -> APPLY -> OBSERVE -> INDEPENDENTLY VERIFY -> LEARN
-> SUCCESSOR REUSE.

When any stage stalls, throughput drops to zero regardless of area scores.
This monitor reports pipeline flow health: GREEN (flowing), YELLOW (slowing),
RED (stalled).

Health rules:
  RED    - any CANDIDATE > 48h with no verification activity,
           OR zero pipeline movement (new rows) in 12h
  YELLOW - any CANDIDATE > 24h old, OR slowing throughput
           (current 12h volume < 50% of prior 12h volume)
  GREEN  - otherwise

Verification activity = a verification package exists for the candidate
(Tier-1/2/3 package in the packages directory, or ID listed in the
packaged-ids registry file).

READ-ONLY: this tool never writes to Supabase. It only queries.

Usage:
    python3 tools/protocol/pipeline_health.py [--json] [--packages-dir DIR]
    Output: JSON health report to stdout. Exit 0 on GREEN/YELLOW, 2 on RED.

CI: run on schedule; alert on RED.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SB_API = Path.home() / "workspace" / "skills" / "supabase" / "bin" / "sb-api"
GH_API = Path.home() / "workspace" / "naya" / "bin" / "gh-api"
PROJECT = "dahisasgpfvziswqvmvm"
DEFAULT_PACKAGES_DIR = Path.home() / "workspace" / "verification-packages-20261008"
FEEDS = {"learn": "1713", "cold_retrieve": "1714",
         "successor": "1715", "capture": "1716"}
REPO = "SoulSchoolAcademy/NayaPOWER"


def sb_query(sql: str) -> list:
    """Run a read-only query against Supabase. Returns list of rows."""
    result = subprocess.run(
        [str(SB_API), "POST",
         f"/v1/projects/{PROJECT}/database/query",
         json.dumps({"query": sql})],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"sb-api failed: {result.stdout[:200]}")
    out = result.stdout.strip()
    # sb-api wraps output; extract JSON array
    start = out.find("[")
    if start < 0:
        raise RuntimeError(f"unexpected sb-api output: {out[:200]}")
    return json.loads(out[start:])


def get_packaged_ids(packages_dir: Path) -> set:
    """Scan verification packages directory for candidate IDs (first 8 hex chars)."""
    ids = set()
    if not packages_dir.exists():
        return ids
    for f in packages_dir.glob("*-tier*.md"):
        stem = f.stem  # e.g. "07d705b0-tier1"
        cid = stem.rsplit("-tier", 1)[0]
        ids.add(cid)
    # Also check a registry file if present
    registry = packages_dir / "packaged_ids.json"
    if registry.exists():
        try:
            ids.update(json.load(open(registry)))
        except Exception:
            pass
    return ids


def get_feed_activity() -> dict:
    """Check latest comment timestamp on each pipeline feed."""
    activity = {}
    for name, num in FEEDS.items():
        try:
            result = subprocess.run(
                [str(GH_API), "GET",
                 f"/repos/{REPO}/issues/{num}/comments?per_page=1"],
                capture_output=True, text=True, timeout=30,
            )
            comments = json.loads(result.stdout)
            # gh-api returns list directly or wrapped; handle both
            if isinstance(comments, dict):
                comments = comments.get("comments", [])
            if comments:
                latest = comments[-1]["created_at"]
                activity[name] = latest
            else:
                activity[name] = None
        except Exception as e:
            activity[name] = f"error: {e}"
    return activity


def hours_ago(iso_ts: str) -> float | None:
    try:
        ts = iso_ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts)
        delta = datetime.now(timezone.utc) - dt
        return delta.total_seconds() / 3600
    except Exception:
        return None


def run_health_check(packages_dir: Path) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    issues = []

    # 1. Status counts
    rows = sb_query(
        "SELECT status, count(*) as n FROM learning_evidence GROUP BY status")
    status_counts = {r["status"]: int(r["n"]) for r in rows}

    # 2. Candidate age aggregates (avoid large result sets - sb-api truncates)
    agg = sb_query(
        "SELECT "
        "count(*) as total, "
        "count(*) FILTER (WHERE created_at < NOW() - INTERVAL '24 hours') as over_24h, "
        "count(*) FILTER (WHERE created_at < NOW() - INTERVAL '48 hours') as over_48h, "
        "MAX(EXTRACT(EPOCH FROM (NOW() - created_at))/3600) as oldest_hours "
        "FROM learning_evidence WHERE status='CANDIDATE'")[0]
    total_cands = int(agg["total"])
    n_over_24h = int(agg["over_24h"])
    n_over_48h = int(agg["over_48h"])
    oldest = float(agg["oldest_hours"] or 0)

    # 3. IDs of >48h candidates (small result set, IDs only)
    old48 = sb_query(
        "SELECT id FROM learning_evidence WHERE status='CANDIDATE' "
        "AND created_at < NOW() - INTERVAL '48 hours' ORDER BY created_at")
    old48_ids = [r["id"][:8] for r in old48]

    # 3. Verification activity for old candidates (cont.)
    packaged = get_packaged_ids(packages_dir)
    unpackaged_48h_ids = [cid for cid in old48_ids if cid not in packaged]

    # 4. Pipeline movement (new rows in last 12h vs prior 12h)
    cur12 = sb_query(
        "SELECT count(*) as n FROM learning_evidence "
        "WHERE created_at > NOW() - INTERVAL '12 hours'")[0]
    prior12 = sb_query(
        "SELECT count(*) as n FROM learning_evidence "
        "WHERE created_at <= NOW() - INTERVAL '12 hours' "
        "AND created_at > NOW() - INTERVAL '24 hours'")[0]
    new_12h = int(cur12["n"])
    new_prior_12h = int(prior12["n"])
    slowing = new_prior_12h > 0 and new_12h < (new_prior_12h * 0.5)

    # 5. Feed activity
    feeds = get_feed_activity()
    quiet_feeds = [n for n, ts in feeds.items()
                   if ts and not ts.startswith("error")
                   and (hours_ago(ts) or 0) > 24]

    # Health determination
    if unpackaged_48h_ids or new_12h == 0:
        health = "RED"
        if unpackaged_48h_ids:
            issues.append(
                f"{len(unpackaged_48h_ids)} CANDIDATE(s) >48h with no "
                f"verification package: "
                + ", ".join(unpackaged_48h_ids[:5]))
        if new_12h == 0:
            issues.append("zero pipeline movement in 12h (no new rows)")
    elif n_over_24h > 0 or slowing:
        health = "YELLOW"
        if n_over_24h > 0:
            issues.append(
                f"{n_over_24h} CANDIDATE(s) >24h old "
                f"(oldest: {oldest:.0f}h)")
        if slowing:
            issues.append(
                f"throughput slowing: {new_12h} new rows/12h vs "
                f"{new_prior_12h} prior")
    else:
        health = "GREEN"

    if quiet_feeds:
        issues.append(f"quiet feeds (>24h no activity): {', '.join(quiet_feeds)}")

    return {
        "monitor": "pipeline_health",
        "timestamp": now,
        "health": health,
        "exit_hint": 2 if health == "RED" else 0,
        "pipeline": "CAPTURE->PERSIST->RECEIPT->SMART LINK->COLD RETRIEVE"
                    "->COMPREHEND->APPLY->OBSERVE->INDEPENDENTLY VERIFY"
                    "->LEARN->SUCCESSOR REUSE",
        "status_counts": status_counts,
        "candidates": {
            "total": total_cands,
            "over_24h": n_over_24h,
            "over_48h": n_over_48h,
            "over_48h_unpackaged": len(unpackaged_48h_ids),
            "oldest_hours": round(oldest, 1),
        },
        "throughput": {
            "new_rows_12h": new_12h,
            "new_rows_prior_12h": new_prior_12h,
            "slowing": slowing,
        },
        "feeds": feeds,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="NayaPOWER pipeline health monitor")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON (default)")
    parser.add_argument("--packages-dir", default=str(DEFAULT_PACKAGES_DIR),
                        help="Verification packages directory")
    args = parser.parse_args()

    try:
        report = run_health_check(Path(args.packages_dir))
    except Exception as e:
        report = {
            "monitor": "pipeline_health",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "health": "RED",
            "exit_hint": 2,
            "issues": [f"monitor failed: {e}"],
        }

    print(json.dumps(report, indent=2))
    return report["exit_hint"]


if __name__ == "__main__":
    sys.exit(main())
