#!/usr/bin/env python3
"""SN-0493 — Decisions Expire When the Tip Moves.

"Re-resolve live state before every action. Stale SHA = stale decision."

Validates that a SHA a decision was made against still matches the current
origin/main tip. Any drift fails closed: the decision must be re-resolved,
not trusted.

Input record:
    {"claimed_sha": "<40-hex sha the decision was made against>"}

Checks:
  1. claimed_sha is present and well-formed (40 hex chars).
  2. origin/main tip is resolvable.
  3. claimed_sha == current tip (exact match; no grace period).

On mismatch the result reports how many commits behind the claim is,
so the agent knows the cost of re-resolution.

Usage:
    python3 kernel/protocol/checks/tip_freshness.py \
        --record '{"claimed_sha": "<sha>"}' [--json]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def current_tip() -> str | None:
    try:
        r = subprocess.run(
            ["git", "ls-remote", "origin", "main"],
            capture_output=True, text=True, timeout=30, cwd=ROOT,
        )
        if r.returncode != 0:
            return None
        sha = r.stdout.split()[0] if r.stdout.strip() else ""
        return sha if SHA_RE.match(sha) else None
    except Exception:
        return None


def commits_behind(claimed: str, tip: str) -> int | None:
    """How many commits the claim is behind tip (None if unknowable)."""
    try:
        r = subprocess.run(
            ["git", "rev-list", "--count", f"{claimed}..{tip}"],
            capture_output=True, text=True, timeout=30, cwd=ROOT,
        )
        if r.returncode != 0:
            return None
        return int(r.stdout.strip())
    except Exception:
        return None


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {}

    claimed = record.get("claimed_sha")
    if not claimed:
        return fail("claimed_sha is missing: no basis to judge freshness",
                    {"law": "SN-0493"})
    if not isinstance(claimed, str) or not SHA_RE.match(claimed):
        return fail(f"claimed_sha malformed (expected 40 hex chars): {claimed!r}",
                    {"law": "SN-0493"})

    tip = current_tip()
    if tip is None:
        return fail("cannot resolve origin/main tip: freshness unknowable, fail closed",
                    {"law": "SN-0493", "claimed_sha": claimed[:12]})

    details.update({"claimed_sha": claimed[:12], "current_tip": tip[:12], "law": "SN-0493"})

    if claimed == tip:
        reasons.append(f"claimed SHA matches current tip {tip[:12]}: decision is fresh")
        return result(True, reasons, details)

    behind = commits_behind(claimed, tip)
    details["commits_behind"] = behind
    behind_txt = f"{behind} commits behind" if behind is not None else "drift unmeasurable"
    return fail(
        f"STALE SHA: claim {claimed[:12]} vs tip {tip[:12]} ({behind_txt}). "
        "SN-0493: re-resolve live state and re-decide; do not act on the stale decision.",
        details,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0493 tip-freshness check")
    parser.add_argument("--record", required=True,
                        help="JSON decision record (or @file) with claimed_sha")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-0493"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
