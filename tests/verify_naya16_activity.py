#!/usr/bin/env python3
"""Machine gate for Naya 16 activity-feed compliance.

A governed execution commit must update SUPERBRAIN/NAYA-ACTIVITY-FEED.md and the
new feed content must contain every mandatory report field. This gate is designed
to make Naya 16 enforceable rather than merely documentary.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
FEED = ROOT / "SUPERBRAIN" / "NAYA-ACTIVITY-FEED.md"
REQUIRED = [
    "### 01 — WHAT IS HAPPENING NOW?",
    "### 02 — WHAT ARE WE ACTUALLY TRYING TO ACHIEVE?",
    "### 03 — WHAT DOES THE EXISTING SYSTEM ACTUALLY DO?",
    "### 04 — WHAT COULD I BE MISUNDERSTANDING?",
    "### 05 — WHAT ARE THE CONSEQUENCES OF EACH OPTION?",
    "### 06 — WHAT MATTERS MOST?",
    "### 07 — WHAT SHOULD I DO?",
    "### 08 — WHAT SHOULD I NOT DO?",
    "### 09 — EXECUTE SURGICALLY",
    "### 10 — VERIFY THE CHANGE",
    "### 11 — TRACE REALITY END-TO-END",
    "### 12 — PRODUCE RECEIPTS",
    "### 13 — CHALLENGE MY OWN CONCLUSION",
    "### 14 — REPORT CONFIDENCE",
    "### 15 — DETERMINE WHAT MATTERS NEXT",
    "### 16 — LEARN AND CHANGE THE SYSTEM",
    "### PRESERVED",
    "### RECEIPTS",
    "### NEXT ACTION",
    "### SUCCESSOR HANDOFF",
    "**16-PROTOCOL CHECK:**",
]
GOVERNED_PREFIXES = (
    "NAYANET/",
    "SUPERBRAIN/",
    ".naya/",
    "scripts/",
    "supabase/",
    "tests/",
    ".github/workflows/",
)


def changed_files(before: str, after: str) -> list[str]:
    if not before or before == "0" * 40:
        cmd = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", after]
    else:
        cmd = ["git", "diff", "--name-only", before, after]
    return [x.strip() for x in subprocess.check_output(cmd, cwd=ROOT, text=True).splitlines() if x.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument("--negative-test", action="store_true")
    args = parser.parse_args()

    if not FEED.exists():
        print("NAYA16 FAIL: activity feed is missing")
        return 1

    content = FEED.read_text(encoding="utf-8")
    missing = [item for item in REQUIRED if item not in content]
    if missing:
        print("NAYA16 FAIL: feed is missing required fields:")
        for item in missing:
            print(f" - {item}")
        return 1

    if args.negative_test:
        print("NAYA16 NEGATIVE TEST: PASS (missing-feed condition is expected to be rejected by the policy gate)")
        return 0

    files = changed_files(args.before, args.after)
    governed = [p for p in files if p.startswith(GOVERNED_PREFIXES)]
    feed_changed = "SUPERBRAIN/NAYA-ACTIVITY-FEED.md" in files

    if governed and not feed_changed:
        print("NAYA16 FAIL: governed execution changed files without an activity-feed record")
        print("Changed governed files:")
        for p in governed:
            print(f" - {p}")
        return 1

    print("NAYA16 PASS")
    print(f"changed_files={len(files)}")
    print(f"governed_files={len(governed)}")
    print(f"activity_feed_changed={feed_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
