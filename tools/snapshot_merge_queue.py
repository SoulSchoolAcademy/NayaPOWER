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

The mission state's "Right now (in order)" section names the queue as a
numbered list of PR items plus the morning merge order as an arrow-chain
(e.g. "#2293 → #2270 → #2188 (his word) → #2201 queues"). Annotations:
  - "his word" / "needs Shawn's word" / "Shawn pulls the trigger" -> parked
    (human gate, not starvation)
  - "blocked on #NNNN" / "queued behind #NNNN" / "sequencing after #NNNN"
    -> blocked_by
  - "SUPERSEDED" / "recommend close-unmerged" -> terminal, excluded
  - "(draft ...)" -> parked as draft (not mergeable)

If the section is missing or yields zero PR refs, the snapshot FAILS LOUD
(exit 2) -- an empty queue must never scan green (L216).

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
BLOCKED_RE = re.compile(
    r"(?:blocked on|blocked behind|queued behind|sequencing after)\s+#(\d+)",
    re.I)
PARKED_RE = re.compile(r"(?:needs\s+)?(?:his|shawn'?s)\s+word|pulls the trigger",
                       re.I)
TERMINAL_RE = re.compile(r"SUPERSEDED|close-unmerged", re.I)
DRAFT_RE = re.compile(r"\(draft\b|\bdraft\s+PR\b", re.I)
CHAIN_SPLIT_RE = re.compile(r"\s*(?:->|→)\s*")
RIGHT_NOW_RE = re.compile(r"##\s*right now", re.I)
LEAD_PR_RE = re.compile(r"\s*\*\*PR\s+#(\d+)", re.I)
VS_RE = re.compile(r"\bvs\.?\b", re.I)


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


def right_now_section(body: str):
    """Slice the mission state's '## Right now (in order)' section.

    Returns the section text, or None when the heading is absent -- that is
    format drift and the caller must fail loud (L216), never scan empty.
    """
    m = RIGHT_NOW_RE.search(body or "")
    if not m:
        return None
    section = body[m.start():]
    end = re.search(r"\n##\s", section)
    if end:
        section = section[:end.start()]
    return section


def extract_queue_chains(body: str):
    """Parse the merge queue from '## Right now (in order)'.

    Sources, in first-seen order:
      1. arrow-chains anywhere in the section (the morning merge order,
         e.g. "#2293 → #2270 → #2188 (his word) → #2201 queues");
      2. each numbered item's lead PR ("N. **PR #NNNN ...**") with the item's
         full text as its annotation;
      3. subordinate PR refs whose own clause carries an explicit queue-state
         signal (blocked / parked / terminal / draft). For "A vs B" comparison
         clauses the signal belongs to A (the subject); B is the baseline and
         is skipped.

    Returns [(pr_number, annotation_text), ...] in queue order, annotations
    merged per PR. Empty list = unparseable; callers must fail LOUD.
    """
    section = right_now_section(body)
    if section is None:
        return []
    items = []  # (pr, annot)
    parts = re.split(r"(?m)^\s*\d+\.\s+", section)
    for part in parts[1:]:  # parts[0] is the section header preamble
        lead = None
        lm = LEAD_PR_RE.match(part)
        if lm:
            lead = int(lm.group(1))
        # 1) arrow-chains anywhere in the item (morning merge order)
        for chunk in re.split(r"[.\n]", part):
            if "->" not in chunk and "→" not in chunk:
                continue
            for sub in CHAIN_SPLIT_RE.split(chunk):
                pm = PR_REF_RE.search(sub)
                if not pm:
                    continue
                items.append((int(pm.group(1)), sub[pm.end():]))
        # 3) subordinate refs with an explicit queue-state clause.
        #    Collected before the lead so the lead's annotation can be cut
        #    at the first subordinate -- subordinate terminal/parked signals
        #    must never misattribute to the lead (e.g. item 5's lead #2296
        #    is MERGE-READY; "close-unmerged" belongs to #2280, not #2296).
        sub_items = []  # (pos_in_part, pr, annot)
        for cm in re.finditer(r"[^.;\n]+", part):
            clause = cm.group(0)
            if "->" in clause or "→" in clause:
                continue  # arrow-chains handled precisely in (1); their
                          # annotations belong to the ref they follow
            for sm in PR_REF_RE.finditer(clause):
                pr = int(sm.group(1))
                if pr == lead:
                    continue  # lead already carries the item text
                before, after = clause[:sm.start()], clause[sm.end():]
                if VS_RE.search(before[-14:]):
                    continue  # "A vs B": B is the comparison baseline
                if (TERMINAL_RE.search(after) or PARKED_RE.search(after)
                        or BLOCKED_RE.search(after) or DRAFT_RE.search(after)):
                    sub_items.append((cm.start() + sm.start(), pr, after))
        # 2) the item's lead PR: its OWN clause only (up to the first
        #    subordinate queue item).
        if lead is not None:
            cut = min([pos for pos, _, _ in sub_items], default=len(part))
            items.append((lead, part[:cut]))
        items.extend((pr, annot) for _, pr, annot in sub_items)
    # Merge annotations per PR, keep first-seen order.
    merged = {}
    for pr, annot in items:
        annot = (annot or "").strip()
        if pr in merged:
            if annot and annot not in merged[pr]:
                merged[pr] += " | " + annot
        else:
            merged[pr] = annot
    return [(pr, merged[pr]) for pr in merged]


def parked_from_parked_section(body: str):
    """PRs the mission state's '## Parked' section names as awaiting Shawn.

    Those PRs are parked even without a chain-local annotation (e.g.
    "#2293 / #2270 merges (his word — morning order above)").
    """
    m = re.search(r"##\s*parked", body or "", re.I)
    if not m:
        return set()
    section = body[m.start():]
    end = re.search(r"\n##\s", section)
    if end:
        section = section[:end.start()]
    out = set()
    for line in section.split("\n"):
        if PARKED_RE.search(line):
            out.update(int(n) for n in PR_REF_RE.findall(line))
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
    chains = [(p, a) for p, a in extract_queue_chains(body)
              if p != args.mission_state]  # the mission state is never its own queue item
    if not chains:
        # L216: an empty parse is an alarm, never a clean scan.
        if right_now_section(body) is None:
            print("SNAPSHOT ERROR: queue parsed empty from #2154 -- "
                  "'Right now (in order)' section not found; format changed?",
                  file=sys.stderr)
        else:
            print("SNAPSHOT ERROR: queue parsed empty from #2154 -- section "
                  "present but zero PR refs; format changed?", file=sys.stderr)
        return 2
    parked_extra = parked_from_parked_section(body)
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
        blocked_by = list(dict.fromkeys(int(x) for x in BLOCKED_RE.findall(annot)))
        parked = None
        if PARKED_RE.search(annot) or pr_number in parked_extra:
            parked = {"reason": "awaiting Shawn's word (human gate) -- not starvation"}
        elif DRAFT_RE.search(annot):
            parked = {"reason": "draft PR -- not mergeable; parked until ready for review"}
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
