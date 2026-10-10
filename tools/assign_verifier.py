#!/usr/bin/env python3
"""Automatic independent-verifier assignment for NayaPOWER PRs.

Problem it solves: independent verification used to require someone to
notice a PR, pick a verifier seat, and spawn the work. PRs stalled waiting
for verifiers; nobody owned the assignment.

How it works (triggered by .github/workflows/verifier-assignment.yml on
PR opened / reopened / labeled(needs-verification) / synchronize):
  1. Reads the author seat from the PR body ('Seat: Naya N').
  2. Deterministically assigns a verifier seat != author:
         candidates = [s for s in (2, 3, 4, 5) if s != author]
         verifier   = candidates[pr_number % len(candidates)]
     Deterministic, always independent, and rotates across PRs so no
     single seat becomes the permanent bottleneck.
  3. Idempotent per head SHA: if an assignment comment for this exact head
     SHA already exists, or a non-author seat already posted a review, it
     does nothing (no duplicate assignments, no re-assignment spam after
     the review lands; a new push -> new SHA -> fresh assignment).
  4. Posts a machine-readable assignment comment carrying the exact head
     SHA plus the 2-minute verification recipe, and applies the
     'needs-verification' label.

Gate-inert by construction: the assignment comment is written so it can
NEVER satisfy tools/check_merge_consensus.py's review detection. Seats are
written hyphenated ('Naya-4'), never in the 'Naya 4' form the gate parses,
and the comment carries an explicit "not a review" guard line. A
SELF_TEST=1 run proves this invariant against the gate's own predicate.

A missing verifier never merges silently: the label stays on and the
merge-consensus gate keeps failing until a real review lands. The PR
waits; it does not auto-merge.

Env:
  GH_TOKEN   GitHub token (workflow secrets.GITHUB_TOKEN)
  REPO       owner/repo
  PR_NUMBER  pull request number
  HEAD_SHA   PR head SHA under assignment
  DRY_RUN    '1' = read live state but print instead of writing
  SELF_TEST  '1' = run built-in integrity tests, no API calls
Stdlib only.
"""
import json
import os
import re
import sys
import urllib.request

API = "https://api.github.com"
SEAT_RE = re.compile(r"naya\s*([2345])\b", re.I)
SEATS = (2, 3, 4, 5)
LABEL = "needs-verification"
ASSIGN_MARKER = "Verifier assignment"


def fail(msg):
    print(f"VERIFIER ASSIGNMENT FAILED: {msg}")
    sys.exit(1)


def api_get(path, token):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-verifier-assignment/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def api_post(path, token, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        API + path, data=data, method="POST",
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json",
                 "User-Agent": "naya-verifier-assignment/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def seat_of(text):
    """Extract author seat number (2-5) from 'Seat: Naya N' text, or None."""
    m = SEAT_RE.search(text or "")
    return int(m.group(1)) if m else None


def pick_verifier(author_seat, pr_number):
    """Deterministic independent seat: never the author, rotates by PR."""
    candidates = [s for s in SEATS if s != author_seat]
    return candidates[pr_number % len(candidates)]


def render_assignment(pr_number, head_sha, author_seat, verifier_seat):
    """Assignment comment. Gate-inert: seats hyphenated ('Naya-4') so the
    merge-consensus gate's seat regex can never parse them; explicit guard
    line declares this is not a review."""
    short = head_sha[:10]
    return f"""## {ASSIGN_MARKER}

Independent verifier assigned: **Naya-{verifier_seat}**
PR author seat: **Naya-{author_seat}** (assignment never goes to the author's seat)
Head SHA: `{head_sha}`

> This is an assignment notice, not a review. It does not satisfy the
> merge-consensus gate. Only a `[NAYA <seat> · REVIEW]` comment from an
> independent seat satisfies the gate.

Verification recipe (exact — do not skip steps):
1. `git fetch origin {head_sha} && git checkout {head_sha}` — then confirm
   `git rev-parse HEAD` prints `{head_sha}`.
2. Run the full suite on that exact tree (the same checks repo CI runs).
3. Post your result as a PR comment in exactly this form:
   `[NAYA <your-seat> · REVIEW] APPROVED` — head `{short}`, tests <pass>/<fail>
   or
   `[NAYA <your-seat> · REVIEW] REJECTED` — head `{short}`, <reason>
4. If APPROVED, also post a `## SCORECARD` receipt naming the exact head SHA
   (the merge-consensus gate requires the scorecard too).

If you cannot complete verification, say so plainly in a comment — do not
leave the PR waiting in silence.
"""


def gate_would_accept_review(comment_body, author_seat):
    """Mirror of tools/check_merge_consensus.py Path B review detection.
    Used by self-test to prove the assignment comment is gate-inert."""
    body = comment_body or ""
    if "[NAYA" in body.upper() and "REVIEW" in body.upper() \
            and "APPROVED" in body.upper():
        s = seat_of(body)
        if s and s != author_seat:
            return True
    return False


def already_assigned(comments, head_sha):
    return any(ASSIGN_MARKER in (c.get("body") or "")
               and head_sha in (c.get("body") or "")
               for c in comments)


def already_reviewed(comments, author_seat):
    for c in comments:
        if gate_would_accept_review(c.get("body"), author_seat):
            return True
    return False


def self_test():
    # 1. Deterministic, independent, rotating selection.
    assert pick_verifier(5, 2201) == 4   # candidates [2,3,4], 2201%3==2
    assert pick_verifier(5, 2202) == 2   # 2202%3==0
    assert pick_verifier(5, 2203) == 3   # 2203%3==1
    assert pick_verifier(2, 7) == 4      # candidates [3,4,5], 7%3==1
    for author in SEATS:
        for pr in range(100):
            assert pick_verifier(author, pr) != author

    # 2. Seat parsing matches the real PR-body format.
    assert seat_of("Seat: Naya 5") == 5
    assert seat_of("seat: naya 2") == 2
    assert seat_of("no seat here") is None
    assert seat_of("Seat: Coda 1") is None  # only Naya 2-5 are seats

    # 3. THE critical invariant: the assignment comment can never satisfy
    #    the merge-consensus gate's review detection, for any author.
    for author in SEATS:
        for pr in (1, 2201, 99999):
            v = pick_verifier(author, pr)
            body = render_assignment(pr, "deadbeef" * 5, author, v)
            assert not gate_would_accept_review(body, author), \
                f"assignment comment falsely satisfies gate (author {author})"
            # ...nor for any other seat either.
            for other in SEATS:
                assert not gate_would_accept_review(body, other)

    # 4. Idempotency predicates.
    sha = "abc123"
    comments = [{"body": render_assignment(2201, sha, 5, 4)}]
    assert already_assigned(comments, sha)
    assert not already_assigned(comments, "different-sha")
    assert already_reviewed(
        [{"body": "[NAYA 4 · REVIEW] APPROVED — head abc, all green"}], 5)
    assert not already_reviewed(
        [{"body": "[NAYA 5 · REVIEW] APPROVED — own work"}], 5)

    print("VERIFIER ASSIGNMENT SELF-TEST PASSED: selection, parsing, "
          "gate-inertness, idempotency all green.")


def main():
    if os.environ.get("SELF_TEST") == "1":
        self_test()
        return

    token = os.environ.get("GH_TOKEN") or ""
    repo = os.environ.get("REPO") or ""
    pr_number = os.environ.get("PR_NUMBER") or ""
    head_sha = os.environ.get("HEAD_SHA") or ""
    dry_run = os.environ.get("DRY_RUN") == "1"
    if not (token and repo and pr_number and head_sha):
        fail("missing GH_TOKEN/REPO/PR_NUMBER/HEAD_SHA in environment.")
    pr_number = int(pr_number)

    pr = api_get(f"/repos/{repo}/pulls/{pr_number}", token)
    if pr.get("state") != "open":
        print(f"PR #{pr_number} is {pr.get('state')}; nothing to assign.")
        return
    author_seat = seat_of(pr.get("body"))
    if not author_seat:
        fail("PR body must declare the authoring seat ('Seat: Naya N'). "
             "Unattributed work cannot be assigned a verifier.")

    comments = api_get(f"/repos/{repo}/issues/{pr_number}/comments", token)
    if already_reviewed(comments, author_seat):
        print(f"PR #{pr_number}: independent review already posted; "
              f"no assignment needed.")
        return
    if already_assigned(comments, head_sha):
        print(f"PR #{pr_number}: verifier already assigned for head "
              f"{head_sha[:10]}; skipping.")
        return

    verifier = pick_verifier(author_seat, pr_number)
    body = render_assignment(pr_number, head_sha, author_seat, verifier)
    # Final guard: never emit a comment the gate could mistake for a review.
    assert not gate_would_accept_review(body, author_seat), \
        "refusing to post: assignment comment is not gate-inert"

    if dry_run:
        print(f"DRY RUN: would assign Naya-{verifier} to PR #{pr_number} "
              f"(author Naya-{author_seat}, head {head_sha[:10]}), add "
              f"label '{LABEL}', and post:\n\n{body}")
        return

    api_post(f"/repos/{repo}/issues/{pr_number}/comments", token,
             {"body": body})
    api_post(f"/repos/{repo}/issues/{pr_number}/labels", token,
             {"labels": [LABEL]})
    print(f"VERIFIER ASSIGNED: Naya-{verifier} -> PR #{pr_number} "
          f"(author Naya-{author_seat}, head {head_sha[:10]}).")


if __name__ == "__main__":
    main()
