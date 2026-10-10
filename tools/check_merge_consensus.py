#!/usr/bin/env python3
"""Merge-consensus gate: no merge without team review and a scorecard receipt.

Reads from env:
  GH_TOKEN      - GitHub token (workflow secrets.GITHUB_TOKEN)
  REPO          - owner/repo
  PR_NUMBER     - pull request number
  HEAD_SHA      - PR head SHA under test
  PR_AUTHOR     - PR author login

Requires BOTH:
  1. >=1 APPROVED review from a user who is not the PR author.
  2. A scorecard receipt: a PR comment containing '## SCORECARD', the exact
     HEAD_SHA, and an approval signal ('merge: APPROVED' or 'verdict:' >= 9).

Exit 0 = consensus present. Exit 1 = fail with a plain-words reason.
Stdlib only.
"""
import json
import os
import re
import sys
import urllib.request

API = "https://api.github.com"


def fail(msg):
    print(f"CONSENSUS GATE FAILED: {msg}")
    print("Fix: get one approving review from another seat, and post a")
    print("'## SCORECARD' comment naming the exact head SHA with a merge verdict.")
    sys.exit(1)


def api_get(path, token):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-consensus-gate/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main():
    token = os.environ.get("GH_TOKEN") or ""
    repo = os.environ.get("REPO") or ""
    pr_number = os.environ.get("PR_NUMBER") or ""
    head_sha = os.environ.get("HEAD_SHA") or ""
    pr_author = (os.environ.get("PR_AUTHOR") or "").lower()
    if not (token and repo and pr_number and head_sha):
        fail("missing GH_TOKEN/REPO/PR_NUMBER/HEAD_SHA in environment.")

    # 1. Approving review from a non-author.
    reviews = api_get(f"/repos/{repo}/pulls/{pr_number}/reviews", token)
    approvals = [r for r in reviews
                 if r.get("state") == "APPROVED"
                 and (r["user"]["login"] or "").lower() != pr_author]
    if not approvals:
        fail(f"no APPROVED review from anyone other than the author ({pr_author or 'unknown'}). "
             f"Team review is required — one seat cannot merge its own work unreviewed.")

    # 2. Scorecard receipt naming this exact head SHA.
    comments = api_get(f"/repos/{repo}/issues/{pr_number}/comments", token)
    receipt = None
    for c in comments:
        body = c.get("body") or ""
        if "## scorecard" not in body.lower():
            continue
        if head_sha not in body:
            continue
        m = re.search(r"merge:\s*APPROVED", body, re.I)
        v = re.search(r"verdict:\s*(\d+(?:\.\d+)?)", body, re.I)
        if m or (v and float(v.group(1)) >= 9.0):
            receipt = c
            break
    if not receipt:
        fail(f"no scorecard receipt found naming head SHA {head_sha[:10]}. "
             f"Post a '## SCORECARD' comment with the exact head SHA and a merge verdict.")

    print(f"CONSENSUS GATE PASSED: approval by {approvals[-1]['user']['login']}, "
          f"scorecard receipt {receipt['id']} names head {head_sha[:10]}.")


if __name__ == "__main__":
    main()
