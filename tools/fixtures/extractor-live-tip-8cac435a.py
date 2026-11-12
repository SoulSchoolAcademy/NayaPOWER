#!/usr/bin/env python3
"""succession_read_before_fire.py — read-before-fire gate for feed/board succession.

A succession package is ARMED when its body is drafted; it must never FIRE
(create the successor issue) without first READING the venue issue and proving
the package's source board is still the live board. This gate mechanizes that
read: the single gh-api call below IS the venue read.

Exit codes (team convention: 0 = proven, 2 = fail-closed, 1 = usage):
  0 — venue read OK and package source board == live board. FIRE ALLOWED.
  2 — mismatch, unparseable package, or unreadable venue. DO NOT FIRE.
      A false hold costs one re-arm; a false fire posts the team's live
      coordination onto a dead board. Fail closed, always.

Usage:
  succession_read_before_fire.py --venue-issue 1599 --package <path>

The venue issue is the canonical "where is the live board" record (#1599,
the feed index). Never pass #2601 as the venue when it is director-divergent.

gh-api path: NAYA_GH_API env overrides the default; the default is the
team's quiet write path on the worker VM.
"""
import argparse
import json
import os
import re
import subprocess
import sys

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = os.environ.get("NAYA_GH_API", "/home/hatch/workspace/naya/bin/gh-api")

# Package source board: "successor to #2641" in the title/body, or "#2641 -> successor".
PKG_PATTERNS = [
    re.compile(r"\(successor to #(\d+)\)"),
    re.compile(r"#(\d+)\s*(?:→|->)\s*successor", re.IGNORECASE),
    re.compile(r"successor to #(\d+)"),
]
# Venue live-board line, e.g. "[#2721 — Team coordination feed — live board](...)".
VENUE_PATTERN = re.compile(r"#(\d+)[^\n#]{0,80}?live board", re.IGNORECASE)


def extract_package_source(text):
    for pat in PKG_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1)
    return None


def extract_live_board(body):
    m = VENUE_PATTERN.search(body)
    return m.group(1) if m else None


def read_venue_issue(number):
    try:
        out = subprocess.run(
            [GH_API, "GET", f"/repos/{REPO}/issues/{number}"],
            capture_output=True, text=True, timeout=60,
        )
    except Exception as e:
        return None, f"gh-api exec failed: {e}"
    if out.returncode != 0:
        return None, f"gh-api exit {out.returncode}: {out.stderr.strip()[:200]}"
    try:
        return json.loads(out.stdout).get("body", ""), None
    except Exception as e:
        return None, f"venue body not JSON: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--venue-issue", required=True, help="issue number of the venue record (e.g. 1599)")
    ap.add_argument("--package", required=True, help="path to the armed succession package file")
    args = ap.parse_args()

    try:
        with open(args.package, "r", encoding="utf-8") as f:
            pkg_text = f.read()
    except OSError as e:
        print(f"FAIL-CLOSED: cannot read package file: {e}", file=sys.stderr)
        return 1

    source = extract_package_source(pkg_text)
    if not source:
        print("FAIL-CLOSED: no source-board line ('successor to #NNNN') in package — do not fire", file=sys.stderr)
        return 2

    body, err = read_venue_issue(args.venue_issue)
    if err is not None:
        print(f"FAIL-CLOSED: venue issue #{args.venue_issue} unreadable ({err}) — do not fire", file=sys.stderr)
        return 2

    live = extract_live_board(body)
    if not live:
        print(f"FAIL-CLOSED: no '#NNNN ... live board' line in venue issue #{args.venue_issue} body — do not fire", file=sys.stderr)
        return 2

    if source == live:
        print(f"FIRE ALLOWED: venue #{args.venue_issue} read live; package source #{source} == live board #{live}")
        return 0
    print(f"FAIL-CLOSED: package source #{source} != live board #{live} (venue #{args.venue_issue}) — re-arm, do not fire",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
