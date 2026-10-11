#!/usr/bin/env python3
"""Build a merge-queue snapshot for the fairness scanner.

Reads the live merge queue from the mission state (#2154) and gathers the
evidence bundle for each queued PR: scorecard/review comments, check runs on
the exact head SHA, author seat. Evidence conventions mirror
tools/check_merge_consensus.py (SEAT_RE, `## SCORECARD` + head SHA, `[NAYA M .
REVIEW] APPROVED`).

Reads from env:
  GH_TOKEN - GitHub token (read-only is enough)
  REPO     - owner/repo (default SoulSchoolAcademy/NayaPOWER)

Usage:
    python3 tools/snapshot_merge_queue.py [--out queue.json] [--mission-state 2154]

The mission state's "Merge queue" section names the queue as arrow-chains of
PR numbers (e.g. "#2188 (needs his word) -> #2201 (blocked on #2188)"). The
parenthetical after each PR carries its annotation:
  - "needs his word" / "his word" -> parked (human gate, not starvation)
  - "blocked on #NNNN" / "queued behind #NNNN" -> blocked_by
  - "SUPERSEDED" / "close-unmerged" -> terminal, excluded from the queue

Known-red check exclusions come from the mission state's own standing notes
(e.g. "receipt-gate RED = the exact depth-1 bug #2188 fixes"); each exclusion
is recorded in the snapshot WITH its source so the scanner's excuse is
evidence, not hand-waving.

Stdlib only. Read-only: never posts, never mutates.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API = "https://api.github.com"
REPO = os.environ.get("REPO", "SoulSchoolAcademy/NayaPOWER")
MISSION_STATE_DEFAULT = 2154

SEAT_RE = re.compile(r"Naya\s+(\d+)", re.I)
PR_REF_RE = re.compile(r"#(\d{3,5})")
SCORECARD_RE = re.compile(r"##\s*scorecard", re.I)
HEAD_SHA_RE = re.compile(r"head\s*sha\s*[:=]\s*`?([0-9a-f]{7,40})`?", re.I)
VERDICT_RE = re.compile(r"verdict\s*[:=]\s*(\d+(?:\.\d+)?)", re.I)
MERGE_APPROVED_RE = re.compile(r"merge\s*:\s*APPROVED", re.I)
REVIEW_APPROVED_RE = re.compile(r"\[NAYA[^\]]*REVIEW[^\]]*\].*APPROVED", re.I | re.S)
FULL_SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
BRANCH_SEAT_RE = re.compile(r"^naya(\d+)/", re.I)
BLOCKED_RE = re.compile(r"(?:blocked on|blocked behind|queued behind)\s+#(\d+)", re.I)
PARKED_RE = re.compile(r"(?:needs\s+)?his word", re.I)
TERMINAL_RE = re.compile(r"SUPERSEDED|close-unmerged", re.I)
CHAIN_SPLIT_RE = re.compile(r"\s*(?:->|→)\s*")


def api_get(path: str, token: str):
    req = urllib.request.Request(
        API + path,
        headers={"Authorization": f"Bearer {token}",
                 "Accept": "application/vnd.github+json",
                 "User-Agent": "naya-merge-queue-snapshot/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"GET {path} -> HTTP {e.code}") from e


def seat_of(text: str):
    m = SEAT_RE.search(text or "")
    return f"Naya {m.group(1)}" if m else None


def extract_queue_chains(body: str):
    """Find arrow-chains of PR numbers in the 'Merge queue' section.

    Returns [(pr_number, annotation_text), ...] in queue order.
    """
    m = re.search(r"merge queue.{0,80}", body, re.I)
    section = body[m.start():] if m else body
    # Stop at the next section header or the "Merge needs:" rule sentence.
    end = re.search(r"\n#{1,3}\s|\nMerge needs:", section, re.I)
    if end:
        section = section[:end.start()]
    items = []
    # Split into candidate chains on sentence boundaries, then split chains
    # on arrows.
    for chunk in re.split(r"[.\n]", section):
        if "->" not in chunk and "→" not in chunk:
            continue
        parts = CHAIN_SPLIT_RE.split(chunk)
        chain = []
        for part in parts:
            pm = PR_REF_RE.search(part)
            if not pm:
                continue
            pr = int(pm.group(1))
            annot = part[pm.end():]
            # Annotation runs to the next PR ref or end of part.
            chain.append((pr, annot))
        items.extend(chain)
    # De-duplicate, keep order.
    seen = set()
    out = []
    for pr, annot in items:
        if pr not in seen:
            seen.add(pr)
            out.append((pr, annot))
    # Second pass: the "Parked" section names PRs awaiting Shawn's word in
    # prose outside the arrow-chains (e.g. "#2280/#2279/#2283 merges (his
    # word)"). Those are parked even without a chain-local annotation.
    parked_extra = set()
    pm = re.search(r"parked.{0,400}", body, re.I | re.S)
    if pm:
        parked_section = body[pm.start():pm.start() + 1200]
        for line in parked_section.split("\n"):
            if PARKED_RE.search(line):
                for num in PR_REF_RE.findall(line):
                    parked_extra.add(int(num))
    out = [(pr, annot + (" [parked: his word]" if pr in parked_extra and
                         "his word" not in annot.lower() else ""))
           for pr, annot in out]
    return out


def parse_evidence(pr_number: int, head_sha: str, comments, check_runs,
                   known_red: dict) -> dict:
    """Parse scorecard/review/check evidence per merge-consensus conventions."""
    scorecard = None
    review = None
    for c in comments:
        body = c.get("body") or ""
        if SCORECARD_RE.search(body) and head_sha[:12] in body:
            # Also accept the full head SHA anywhere in the comment.
            if head_sha in body or head_sha[:12] in body:
                vm = VERDICT_RE.search(body)
                scorecard = {
                    "seat": seat_of(body),
                    "head_matches": True,
                    "verdict": float(vm.group(1)) if vm else None,
                    "merge_approved": bool(MERGE_APPROVED_RE.search(body)),
                    "at": c.get("created_at"),
                    "comment_id": c.get("id"),
                }
        if REVIEW_APPROVED_RE.search(body) and head_sha[:12] in body:
            seat = seat_of(body)
            if seat and (review is None or c.get("created_at", "") > review.get("at", "")):
                review = {
                    "seat": seat,
                    "head_matches": True,
                    "at": c.get("created_at"),
                    "comment_id": c.get("id"),
                }
    runs = []
    for r in check_runs or []:
        runs.append({
            "name": r.get("name"),
            "status": r.get("status"),
            "conclusion": r.get("conclusion"),
            "completed_at": r.get("completed_at"),
        })
    return {
        "scorecard": scorecard,
        "review": review,
        "check_runs": runs,
        "checks_evidence_present": check_runs is not None,
        "known_red_checks": known_red,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build merge-queue snapshot JSON.")
    ap.add_argument("--out", default="merge_queue_snapshot.json")
    ap.add_argument("--mission-state", type=int, default=MISSION_STATE_DEFAULT)
    args = ap.parse_args(argv)
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("SNAPSHOT ERROR: GH_TOKEN not set", file=sys.stderr)
        return 2

    issue = api_get(f"/repos/{REPO}/issues/{args.mission_state}", token)
    body = issue.get("body") or ""
    tip_note = f"mission-state updated {issue.get('updated_at')}"
    chains = extract_queue_chains(body)
    print(f"queue chains from #2154: {[p for p, _ in chains]}", file=sys.stderr)

    # Known-red exclusions grounded in the mission state's own standing notes.
    known_red: dict = {}
    if re.search(r"receipt-gate RED = the exact depth-1 bug #2188 fixes", body, re.I):
        known_red["Receipt gate (evidence or it didn't happen)"] = (
            "depth-1 fetch bug fixed by PR #2188; per mission state #2154 "
            f"({tip_note}) -- not a real red on the PR"
        )

    queue = []
    for pr_number, annot in chains:
        if TERMINAL_RE.search(annot):
            print(f"  PR-{pr_number}: terminal ({annot.strip()[:60]}) -- excluded",
                  file=sys.stderr)
            continue
        pr = api_get(f"/repos/{REPO}/pulls/{pr_number}", token)
        head_sha = (pr.get("head") or {}).get("sha") or ""
        branch = ((pr.get("head") or {}).get("ref")) or ""
        state = pr.get("state")
        if state != "open":
            print(f"  PR-{pr_number}: state={state} -- excluded", file=sys.stderr)
            continue
        comments = api_get(
            f"/repos/{REPO}/issues/{pr_number}/comments?per_page=100", token)
        try:
            check_runs = api_get(
                f"/repos/{REPO}/commits/{head_sha}/check-runs?per_page=100",
                token).get("check_runs", [])
        except RuntimeError as e:
            print(f"  PR-{pr_number}: check-runs fetch failed: {e}", file=sys.stderr)
            check_runs = None

        author_seat = seat_of(pr.get("body") or "")
        if not author_seat:
            bm = BRANCH_SEAT_RE.match(branch)
            if bm:
                author_seat = f"Naya {bm.group(1)}"

        evidence = parse_evidence(pr_number, head_sha, comments, check_runs,
                                   known_red)
        blocked_by = [int(x) for x in BLOCKED_RE.findall(annot)]
        parked = None
        if PARKED_RE.search(annot):
            parked = {"reason": "awaiting Shawn's word (human gate) -- not starvation"}
        assumptions = []
        if not author_seat:
            assumptions.append("author seat undeclared; branch prefix fallback used")

        queue.append({
            "pr_number": pr_number,
            "head_sha": head_sha,
            "branch": branch,
            "author_seat": author_seat,
            "intent_recorded": True,  # present in #2154's merge queue by construction
            "blocked_by": blocked_by,
            "parked": parked,
            "assumptions": assumptions,
            "evidence": evidence,
        })
        print(f"  PR-{pr_number}: head={head_sha[:12]} author={author_seat} "
              f"scorecard={evidence['scorecard'] is not None} "
              f"review={evidence['review'] is not None} "
              f"runs={len(evidence['check_runs']) if evidence['check_runs'] else 'MISSING'} "
              f"blocked_by={blocked_by} parked={parked is not None}",
              file=sys.stderr)

    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mission_state_ref": tip_note,
        "repo": REPO,
        "queue": queue,
    }
    with open(args.out, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"wrote {args.out} with {len(queue)} queued PRs", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
