#!/usr/bin/env python3
"""Merge-consensus gate: no merge without cross-seat review + scorecard receipt.

Shawn's doctrine: the protocol IS the authorization. No human click in the
pipeline. This gate is the authorization.

Reads from env:
  GH_TOKEN      - GitHub token (workflow secrets.GITHUB_TOKEN)
  REPO          - owner/repo
  PR_NUMBER     - pull request number
  HEAD_SHA      - PR head SHA under test

Seat identity: the team shares one GitHub account, so GitHub logins cannot
distinguish seats. Seats are identified by signed tags instead:
  - PR body must declare:  Seat: Naya N
  - Reviewer posts a comment:  [NAYA M · REVIEW] ... APPROVED ...
  - Scorecard receipt:  ## SCORECARD ... head: <sha> ... Seat: Naya K ...
Author seat, reviewer seat, and scorer seat must be three pairwise-distinct
seats? No — reviewer and scorer may be the same seat, but BOTH must differ
from the author seat. (The author cannot review or score their own work.)

Native GitHub APPROVED reviews from a *different login* than the PR author
also satisfy the review requirement (future-proof for distinct seat accounts).

Exit 0 = consensus present. Exit 1 = fail with a plain-words reason.
Stdlib only.
"""
import json
import os
import re
import sys
import urllib.request

API = "https://api.github.com"
SEAT_RE = re.compile(r"naya\s*([2345])\b", re.I)


def fail(msg):
    print(f"CONSENSUS GATE FAILED: {msg}")
    sys.exit(1)


def api_get(path, token):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-consensus-gate/2.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def seat_of(text):
    """Extract 'Naya N' seat tag from text, or None."""
    m = SEAT_RE.search(text or "")
    return f"Naya {m.group(1)}" if m else None


def main():
    token = os.environ.get("GH_TOKEN") or ""
    repo = os.environ.get("REPO") or ""
    pr_number = os.environ.get("PR_NUMBER") or ""
    head_sha = os.environ.get("HEAD_SHA") or ""
    if not (token and repo and pr_number and head_sha):
        fail("missing GH_TOKEN/REPO/PR_NUMBER/HEAD_SHA in environment.")

    pr = api_get(f"/repos/{repo}/pulls/{pr_number}", token)
    pr_author_login = (pr["user"]["login"] or "").lower()
    author_seat = seat_of(pr.get("body"))
    if not author_seat:
        fail("PR body must declare the authoring seat ('Seat: Naya N'). "
             "Unattributed work cannot be reviewed.")

    # --- Requirement 1: cross-seat review ---
    # The review must be FRESH: it must reference the exact head SHA being
    # merged, or have been posted after the head commit was pushed. A review
    # of an older SHA does not authorize the current code.
    reviews = api_get(f"/repos/{repo}/pulls/{pr_number}/reviews", token)
    comments = api_get(f"/repos/{repo}/issues/{pr_number}/comments", token)

    reviewer_seat = None
    review_is_fresh = False
    # Path A: native GitHub approval from a different login.
    for r in reviews:
        if (r.get("state") == "APPROVED"
                and (r["user"]["login"] or "").lower() != pr_author_login):
            reviewer_seat = seat_of(r.get("body")) or "external reviewer"
            # Freshness: approval must name the head SHA or postdate it.
            # GitHub approvals are tied to a commit via submitted_at; we
            # require the body to name the SHA explicitly for auditability.
            body = r.get("body") or ""
            if head_sha[:10] in body or head_sha in body:
                review_is_fresh = True
            break
    # Path B: seat-tagged review comment from a different seat.
    if not reviewer_seat:
        for c in comments:
            body = c.get("body") or ""
            if "[NAYA" in body.upper() and "REVIEW" in body.upper() \
                    and "APPROVED" in body.upper():
                s = seat_of(body)
                if s and s != author_seat:
                    reviewer_seat = s
                    # Freshness: the review comment must name the exact
                    # head SHA it approves. A review without a SHA is stale
                    # by default — it could approve any earlier commit.
                    if head_sha[:10] in body or head_sha in body:
                        review_is_fresh = True
                    break
    if not reviewer_seat:
        fail(f"no review from a seat other than the author ({author_seat}). "
             f"Post '[NAYA M · REVIEW] APPROVED' as a PR comment, or submit a "
             f"GitHub approving review from a different account.")
    if not review_is_fresh:
        fail(f"review from {reviewer_seat} does not name the exact head SHA "
             f"{head_sha[:10]}. Reviews must be fresh: re-review the current "
             f"head and include its SHA. Stale reviews do not authorize merges.")

    # --- Requirement 1b: no unresolved objections ---
    # If any review requested changes and was not superseded by a later
    # approval from the same seat, the PR is contested. Contested PRs do
    # not merge — the objection must be resolved or explicitly withdrawn.
    for r in reviews:
        if r.get("state") == "CHANGES_REQUESTED":
            obj_seat = seat_of(r.get("body")) or r["user"]["login"]
            # Check if this seat later approved (superseding the objection).
            superseded = any(
                x.get("state") == "APPROVED"
                and x["user"]["login"] == r["user"]["login"]
                and (x.get("submitted_at") or "") > (r.get("submitted_at") or "")
                for x in reviews
            )
            if not superseded:
                fail(f"unresolved objection from {obj_seat} "
                     f"({(r.get('body') or '')[:80]}). "
                     f"Resolve the objection or have the seat withdraw it "
                     f"before merging.")

    # --- Requirement 2: scorecard receipt naming this exact head SHA ---
    scorer_seat = None
    for c in comments:
        body = c.get("body") or ""
        if "## scorecard" not in body.lower():
            continue
        if head_sha not in body:
            continue
        m = re.search(r"merge:\s*APPROVED", body, re.I)
        v = re.search(r"verdict:\s*(\d+(?:\.\d+)?)", body, re.I)
        s = seat_of(body)
        if (m or (v and float(v.group(1)) >= 9.0)) and s and s != author_seat:
            scorer_seat = s
            break
    if not scorer_seat:
        fail(f"no scorecard receipt naming head SHA {head_sha[:10]} from a seat "
             f"other than the author ({author_seat}). Post '## SCORECARD' with "
             f"the exact head SHA, a merge verdict, and your seat tag.")

    print(f"CONSENSUS GATE PASSED: author {author_seat}, "
          f"reviewer {reviewer_seat}, scorer {scorer_seat}, head {head_sha[:10]}.")


if __name__ == "__main__":
    main()
