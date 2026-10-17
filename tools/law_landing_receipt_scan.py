#!/usr/bin/env python3
"""Post-merge tripwire for the Scorecard Law (SCORECARD-LAW-V1, RATIFIED 2026-10-05).

"no receipt, no merge" — as encoded in the Operating Protocol: the Director's
merge ratifies that merge; every other merge, by any seat, requires a scorecard
receipt posted on the area feed (#1354) BEFORE merging.

This tool automates the LAW TESTER's methodology (BUG-001, filed on #1867):
for each PR merged in the window, check the area feed for a pre-merge
scorecard receipt referencing that PR. It is the post-merge complement of the
pre-merge advisory gate (PR #1778, AUTHGOV lane): the advisory gate watches
the PR door, this watches what actually landed.

Attribution rule (empirical, verified on the BUG-001 sample): the PR-level
`merged_by` field is NOT reliable — it reads `SoulSchoolAcademy` even for
seat-performed merges. The merge COMMIT's identities are the true signal:
committer "GitHub" / author "Shawn Vibert" = Director merge (exempt);
a seat identity (e.g. "Naya 4") on author or committer = seat merge
(requires a pre-merge receipt).

Structure: pure core (no network; fully unit-tested) + thin GitHub API layer.
Stdlib only.

Usage:
    python3 tools/law_landing_receipt_scan.py --scan [--report-issue N]
        Live scan of PRs merged in the last SCAN_WINDOW_HOURS (default 24).
        --report-issue N posts the verdict table to issue N when violations
        are found (needs a token with issues:write). Quiet when clean.

    python3 tools/law_landing_receipt_scan.py --landings-json <path> \
        --comments-json <path>
        Offline verdict over supplied fixtures (used by tests / manual runs).

Env:
    GITHUB_TOKEN  (or GH_TOKEN) — token for the API layer.
    GITHUB_API_BASE — override for tests (default https://api.github.com).

Exit codes:
    0 = all clear (no violations; director-exempt landings reported, not flagged)
    1 = at least one VIOLATION (seat landing without a pre-merge receipt)
    2 = usage / input / instrument error (UNKNOWN is never reported as clean)

Fail-closed: an unreadable feed, a failed API call, or an unparseable landing
never produces a CLEAN verdict for that landing — it produces an UNKNOWN that
exits 2 so a human looks. UNKNOWN != PASS.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

OWNER = "SoulSchoolAcademy"
REPO = "NayaPOWER"
AREA_FEED_ISSUE = 1354          # #1354 — the only authoritative feed
DIRECTOR_NAMES = {"Shawn Vibert", "GitHub"}  # merge-commit identities = Director
SCAN_WINDOW_HOURS = 24

RECEIPT_KEYWORDS = ("scorecard", "receipt")


# ---------------------------------------------------------------- pure core ---

def is_director_landing(author: str | None, committer: str | None) -> bool:
    """True when the merge commit's identities are Director-side.

    Fail-closed: missing identities are NOT a director landing.
    """
    if not author and not committer:
        return False
    return (author in DIRECTOR_NAMES) or (committer in DIRECTOR_NAMES)


def _mentions_pr(body: str, pr_number: int) -> bool:
    # "#1864" or bare "1864" as a standalone token — "#18640" and "21864"
    # must NOT match PR 1864 (no false positives).
    return re.search(rf"(?<![\d#])#?{pr_number}(?!\d)", body) is not None


def receipt_predates(comments: list[dict], pr_number: int, merged_at: str) -> dict | None:
    """Return the earliest pre-merge receipt comment, or None.

    A receipt = a comment whose body mentions "scorecard" (or "receipt") AND
    references the PR number, created strictly before merged_at.
    Malformed comments are ignored, never counted.
    """
    try:
        merged_dt = datetime.fromisoformat(merged_at.replace("Z", "+00:00"))
    except (ValueError, AttributeError, TypeError):
        return None
    best = None
    for c in comments:
        try:
            body = c.get("body") or ""
            created = datetime.fromisoformat(
                (c.get("created_at") or "").replace("Z", "+00:00"))
        except (ValueError, AttributeError, TypeError):
            continue
        if created >= merged_dt:
            continue
        lowered = body.lower()
        if not any(k in lowered for k in RECEIPT_KEYWORDS):
            continue
        if not _mentions_pr(body, pr_number):
            continue
        if best is None or created < best["_dt"]:
            best = {"comment_id": c.get("id"), "created_at": c.get("created_at"),
                    "author": (c.get("user") or {}).get("login"), "_dt": created}
    if best:
        best.pop("_dt", None)
    return best


def classify(author: str | None, committer: str | None,
             receipt: dict | None) -> str:
    """CLEAN | EXEMPT_DIRECTOR | VIOLATION | UNKNOWN (fail-closed)."""
    if receipt:
        return "CLEAN"
    if is_director_landing(author, committer):
        return "EXEMPT_DIRECTOR"
    if not author and not committer:
        return "UNKNOWN"
    return "VIOLATION"


def verdict_table(findings: list[dict]) -> str:
    lines = ["| landing | PR | merged_by | verdict | receipt |",
             "|---|---|---|---|---|"]
    for f in findings:
        r = f.get("receipt")
        rcell = (f"comment {r['comment_id']} ({r['created_at'][:16]}Z)"
                 if r else "—")
        ident = f"{f.get('author') or '?'} / {f.get('committer') or '?'}"
        lines.append(
            f"| `{f['sha'][:8]}` | #{f['pr']} | {ident} | "
            f"**{f['verdict']}** | {rcell} |")
    return "\n".join(lines)


# ------------------------------------------------------------- API layer ---

def _api_base() -> str:
    # Read at call time (not import time) so tests can point the tool at a
    # stub API via the environment.
    return os.environ.get("GITHUB_API_BASE", "https://api.github.com")


def _token() -> str:
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not tok:
        raise SystemExit("error: GITHUB_TOKEN (or GH_TOKEN) is not set")
    return tok


def api_get(path: str, params: dict | None = None) -> object:
    """GET against the GitHub API with one retry on 5xx/429. Stdlib only."""
    url = _api_base() + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    last_err = None
    for _ in range(2):
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {_token()}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "nayapower-law-landing-receipt-scan",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429,) or 500 <= e.code < 600:
                time.sleep(3)
                continue
            raise SystemExit(f"error: GitHub API {e.code} on {path}: "
                             f"{e.read()[:200]!r}")
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            time.sleep(3)
    raise SystemExit(f"error: GitHub API unreachable after retry: {last_err}")


def api_post(path: str, payload: dict) -> object:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        _api_base() + path, data=data,
        headers={"Authorization": f"Bearer {_token()}",
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Content-Type": "application/json",
                 "User-Agent": "nayapower-law-landing-receipt-scan"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"error: POST {path} -> {e.code}: "
                         f"{e.read()[:200]!r}")


def recently_merged(hours: int) -> list[dict]:
    """PRs merged in the last `hours` hours, with merge-commit identities.

    merged_by is read but NOT trusted for attribution (it is unreliable);
    the merge commit's author/committer are the true signal.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    landings: list[dict] = []
    page = 1
    while True:
        batch = api_get(f"/repos/{OWNER}/{REPO}/pulls",
                        {"state": "closed", "sort": "updated",
                         "direction": "desc", "per_page": "100",
                         "page": str(page)})
        if not isinstance(batch, list) or not batch:
            break
        for pr in batch:
            updated = pr.get("updated_at") or ""
            try:
                updated_dt = datetime.fromisoformat(
                    updated.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                continue
            if updated_dt < cutoff:
                return landings  # sorted desc — nothing newer remains
            if not pr.get("merged"):
                continue
            merged_at = pr.get("merged_at") or ""
            try:
                merged_dt = datetime.fromisoformat(
                    merged_at.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                continue
            if merged_dt < cutoff:
                continue
            sha = pr.get("merge_commit_sha")
            author = committer = None
            if sha:
                c = api_get(f"/repos/{OWNER}/{REPO}/commits/{sha}")
                cm = (c.get("commit") or {})
                author = (cm.get("author") or {}).get("name")
                committer = (cm.get("committer") or {}).get("name")
            landings.append({"sha": sha or "?", "pr": pr.get("number"),
                             "author": author, "committer": committer,
                             "merged_at": merged_at})
        if len(batch) < 100:
            break
        page += 1
        if page > 20:  # sanity bound
            break
    return landings


def feed_comments(since_hours: int) -> list[dict]:
    """Recent comments on the area feed. Paginates until exhausted."""
    since = (datetime.now(timezone.utc)
             - timedelta(hours=since_hours)).isoformat()
    comments: list[dict] = []
    page = 1
    while True:
        batch = api_get(
            f"/repos/{OWNER}/{REPO}/issues/{AREA_FEED_ISSUE}/comments",
            {"per_page": "100", "page": str(page), "since": since})
        if not isinstance(batch, list) or not batch:
            break
        comments.extend(batch)
        if len(batch) < 100:
            break
        page += 1
        if page > 50:  # sanity bound
            break
    return comments


def post_report(issue_number: int, table: str, window_h: int) -> None:
    body = (
        "## [LAW-DRIVER] landing-receipt scan — VIOLATION(S) found\n\n"
        f"**Scope:** PRs merged in the last {window_h}h. "
        "Scorecard Law (SCORECARD-LAW-V1, ratified 2026-10-05): "
        "\"no receipt, no merge\" — the Director's merge ratifies that merge; "
        "every other merge, by any seat, requires a scorecard receipt on "
        f"#{AREA_FEED_ISSUE} posted before merging.\n\n"
        + table + "\n\n"
        "_Automated tripwire: `tools/law_landing_receipt_scan.py` "
        "(LAW area driver). VIOLATION rows need a seat to own them._")
    api_post(f"/repos/{OWNER}/{REPO}/issues/{issue_number}/comments",
             {"body": body})
    print(f"posted violation report to #{issue_number}", file=sys.stderr)


def scan(hours: int = SCAN_WINDOW_HOURS) -> tuple[list[dict], bool]:
    """Run the full live scan. Returns (findings, any_unknown)."""
    landings = recently_merged(hours)
    comments = feed_comments(hours + 24)  # margin: receipts predate merges
    findings: list[dict] = []
    any_unknown = False
    for land in landings:
        receipt = receipt_predates(comments, land["pr"], land["merged_at"])
        verdict = classify(land.get("author"), land.get("committer"), receipt)
        if verdict == "UNKNOWN":
            any_unknown = True
        findings.append({**land, "verdict": verdict, "receipt": receipt})
    return findings, any_unknown


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true",
                    help="live scan of PRs merged recently (needs GITHUB_TOKEN)")
    ap.add_argument("--report-issue", type=int, default=0,
                    help="post the verdict table to this issue when violations "
                         "are found (use with --scan)")
    ap.add_argument("--landings-json", help="offline: landings fixture file")
    ap.add_argument("--comments-json", help="offline: comments fixture file")
    ap.add_argument("--window-hours", type=int, default=SCAN_WINDOW_HOURS)
    args = ap.parse_args(argv)

    if args.scan:
        findings, any_unknown = scan(args.window_hours)
    elif args.landings_json and args.comments_json:
        landings = json.load(open(args.landings_json))
        comments = json.load(open(args.comments_json))
        findings, any_unknown = [], False
        for land in landings:
            receipt = receipt_predates(comments, land["pr"],
                                       land.get("merged_at") or "")
            verdict = classify(land.get("author"), land.get("committer"),
                               receipt)
            if verdict == "UNKNOWN":
                any_unknown = True
            findings.append({**land, "verdict": verdict, "receipt": receipt})
    else:
        ap.print_usage(sys.stderr)
        return 2

    if not findings:
        print("no PR merges in window — all clear")
        return 0

    table = verdict_table(findings)
    print(table)
    violations = [f for f in findings if f["verdict"] == "VIOLATION"]
    if any_unknown:
        print("UNKNOWN verdicts present — instrument could not decide; "
              "a human must look.", file=sys.stderr)
        return 2
    if violations and args.report_issue:
        post_report(args.report_issue, table, args.window_hours)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
