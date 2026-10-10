#!/usr/bin/env python3
"""
sweep_verify_claims.py — Automated verify-before-accept sweep for ACT area.

Scans #1354 completion comments for claimed PR numbers, builds a receipt,
and runs verify_builder_artifacts.py against the live remote.

DEPENDENCY: Requires tools/verify_builder_artifacts.py (PR #1767).
This tool is the automation layer; the verifier is the machinery.

Usage: sweep_verify_claims.py [--since-comment-id N] [--format text|json]

Exit codes: 0 = all claimed PRs verified; 1 = at least one phantom;
            2 = environment error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh-api")
REPO = "SoulSchoolAcademy/NayaPOWER"
ISSUE = "1354"
VERIFIER = Path(__file__).parent / "verify_builder_artifacts.py"

# Matches PR claims like "PR #1772", "PR1772", "#1772" in completion context
PR_RE = re.compile(r"(?:PR\s*#|PR#|pull/)(\d{4,5})", re.IGNORECASE)


def gh_api(method: str, path: str) -> dict | list:
    out = subprocess.run(
        [GH_API, method, path],
        capture_output=True, text=True, timeout=60,
    )
    if out.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path} failed: {out.stderr[:200]}")
    return json.loads(out.stdout)


def get_pr_head(pr_number: int) -> tuple[str, str]:
    """Return (full_head_sha, state) for a PR."""
    d = gh_api("GET", f"/repos/{REPO}/pulls/{pr_number}")
    return d["head"]["sha"], d["state"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since-comment-id", type=int, default=0)
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    # Get comment count, fetch last page
    issue = gh_api("GET", f"/repos/{REPO}/issues/{ISSUE}")
    count = issue.get("comments", 0)
    last_page = max(1, (count + 29) // 30)

    pr_numbers: set[int] = set()
    for page in (last_page, last_page - 1):
        if page < 1:
            continue
        comments = gh_api("GET", f"/repos/{REPO}/issues/{ISSUE}/comments?per_page=30&page={page}")
        for c in comments:
            if c["id"] <= args.since_comment_id:
                continue
            body = c.get("body", "")
            # Only completion/verification contexts
            if not re.search(r"complet|verif|open|land|merg", body, re.IGNORECASE):
                continue
            for m in PR_RE.finditer(body):
                pr_numbers.add(int(m.group(1)))

    if not pr_numbers:
        print("No PR claims found in recent #1354 comments.", file=sys.stderr)
        return 2

    artifacts = []
    for n in sorted(pr_numbers):
        try:
            head_sha, state = get_pr_head(n)
            artifacts.append({
                "kind": "pr", "number": n,
                "head": head_sha, "state": state,
            })
        except Exception as e:
            print(f"WARN: could not fetch PR #{n}: {e}", file=sys.stderr)

    if not artifacts:
        print("No verifiable PR artifacts.", file=sys.stderr)
        return 2

    receipt = {"artifacts": artifacts}
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False,
    ) as f:
        json.dump(receipt, f)
        receipt_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, str(VERIFIER), receipt_path,
             "--format", args.format],
            capture_output=True, text=True, timeout=300,
        )
        print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        return result.returncode
    finally:
        os.unlink(receipt_path)


if __name__ == "__main__":
    sys.exit(main())
