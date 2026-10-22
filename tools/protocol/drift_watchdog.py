#!/usr/bin/env python3
"""Drift Watchdog — draft flag reports from recent PR / board data.

Purpose:
    The ratified Naya Protocol (PROTOCOL.md, 2026-10-20) demands
    Step 0 declaration before work, the Step 15 scorecard loop on
    every completion claim, the Value Verdict on every completion
    receipt, and independent verification by a DIFFERENT IDENTITY.
    The 2026-10-20 main-seat adjudication ruled that merges by
    nayapower-lane-agent[bot] with sole reviews from the same login
    were breaches — same-login review is not verification.

    This watchdog watches for drift from those laws in recent PR
    and board (coordination feed) data. It drafts flags for the
    director / a human reviewer to adjudicate. It never issues
    verdicts, never blocks a merge, and never posts anything on
    its own.

Inputs:
    --prs @file    JSON list of PR records in the
                   identity_separation shape PLUS a "body" text
                   field:
                       {
                         "number": 123,
                         "author_login": "...",
                         "merger_login": "...",
                         "merged": true,
                         "reviews": [{"login": "...",
                                      "state": "APPROVED|COMMENTED|..."}],
                         "body": "<PR body text>"
                       }
    --posts @file  JSON list of board posts:
                       {"id": "...", "author": "...", "body": "..."}
    --out PATH     Write the markdown report to PATH
                   (default: stdout).
    --strict       Exit 1 if any flags were drafted
                   (default: exit 0 — drafting flags is the job,
                   not a failure of the watchdog itself).

    Both inputs are optional. A missing input means that source
    is skipped, and the skip is noted in the report.

Flag types:
    IDENTITY_DRIFT
        A merged PR fails checks.identity_separation.check —
        e.g. author, reviewer(s) and merger are the same identity,
        so there was no independent verification by a different
        identity.
    UNSCORED_COMPLETION_CLAIM
        A merged PR body makes a completion claim that
        checks.scorecard_loop.scan_text flags as lacking the
        Step 15 scorecard-loop markers.
    DONE_WITHOUT_RECEIPT
        A board post claims done / complete / completed /
        shipped / merged / landed (case-insensitive) but carries
        no receipt marker: no https?:// link, no 40-hex sha, and
        neither the word "receipt" nor "evidence".
    VALIDATION_CLAIM_UNVERIFIED
        A board post contains "different seat" or
        "independently verified" (case-insensitive). Text claims
        prove nothing — identity must be checked against the PR
        data itself, so every such claim is drafted as a flag
        for a director to verify against real logins.

Honest bounds:
    These are heuristics that draft flags for a director; a flag
    is a question, not a verdict. Heuristic text matching can
    miss drift phrased differently and can flag innocent posts
    that merely mention completion. Identity flags delegate to
    the identity_separation check when it is available; the
    fallback heuristic in this file is only a stand-in until
    that check lands and is not a substitute for it. Nothing in
    this report proves a breach by itself — each flag must be
    adjudicated against the underlying PR, reviews and receipts
    by a different identity than the one that produced the work.

Cron-ready example invocation (comment only — do not schedule
anything from this file; scheduling is a director decision):

    # python3 tools/protocol/drift_watchdog.py \
    #     --prs @/tmp/recent-prs.json \
    #     --posts @/tmp/recent-posts.json \
    #     --out /tmp/drift-report.md --strict

Usage:
    python3 tools/protocol/drift_watchdog.py [--prs @file]
        [--posts @file] [--out PATH] [--strict]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Check imports — fixed interface contract
#
# Check modules are imported as:
#   sys.path.insert(0, str(Path("tools/protocol").resolve()))
#   from checks.<module> import check
# This file lives in tools/protocol/, so its own directory is that
# path regardless of the caller's cwd; insert both spellings so the
# import works from any working directory.
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
for _candidate in (_HERE, Path("tools/protocol").resolve()):
    if str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))


def _load_identity_check():
    """Return checks.identity_separation.check, or None if absent."""
    try:
        from checks.identity_separation import check as _check

        return _check
    except Exception:
        return None


def _load_scan_text():
    """Return checks.scorecard_loop.scan_text, or None if absent."""
    try:
        from checks.scorecard_loop import scan_text as _scan

        return _scan
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Fallbacks — used only while the parallel check modules have not
# landed yet. They replicate the contracted semantics narrowly so
# the watchdog still drafts honest draft flags; the real checks,
# when present, always take precedence.
# ---------------------------------------------------------------------------


def _fallback_identity_check(record):
    """Stand-in for identity_separation.check (same return shape)."""
    if not isinstance(record, dict):
        return {"pass": False, "reasons": ["record is not an object"],
                "details": {}}
    if not record.get("merged"):
        return {"pass": True,
                "reasons": ["not merged — nothing to separate"],
                "details": {}}
    author = record.get("author_login") or ""
    merger = record.get("merger_login") or ""
    reviews = record.get("reviews") or []
    reviewer_logins = []
    for rev in reviews:
        if isinstance(rev, dict):
            login = rev.get("login") or ""
            if login:
                reviewer_logins.append(login)
    independent = [
        login for login in reviewer_logins
        if login != author and login != merger
    ]
    reasons = []
    if not independent:
        reasons.append(
            "no review from an identity different from both the "
            f"author ({author!r}) and the merger ({merger!r}) — "
            "same-login review is not verification"
        )
    if merger and author and merger == author and not independent:
        reasons.append(
            f"merger {merger!r} is the author and no independent "
            "review exists — identity separation breached"
        )
    if reasons:
        return {"pass": False, "reasons": reasons, "details": {}}
    return {"pass": True,
            "reasons": ["independent review present"],
            "details": {}}


_DONE_RE = re.compile(
    r"\b(done|complete|completed|shipped|merged|landed)\b",
    re.IGNORECASE,
)
_SCORECARD_MARKERS = (
    "scorecard loop",
    "scorecard_loop",
    "why not 10",
    "why_not_10",
    "round 1",
    "round 2",
    "round 3",
    "three rounds",
    "3 rounds",
    "final_score",
    "final score",
)


def _fallback_scan_text(text):
    """Stand-in for scorecard_loop.scan_text (same return shape)."""
    body = text or ""
    if not _DONE_RE.search(body):
        return []
    lowered = body.lower()
    # A body that carries recognised loop markers is not flagged
    # by the fallback; the real check is authoritative when present.
    if "scorecard" in lowered and any(
        marker in lowered for marker in _SCORECARD_MARKERS
    ):
        return []
    if "scorecard" in lowered and "round" in lowered:
        return []
    return ["DONE_CLAIM_WITHOUT_SCORECARD_LOOP"]


# ---------------------------------------------------------------------------
# Flag collection
# ---------------------------------------------------------------------------

FLAG_TYPES = (
    "IDENTITY_DRIFT",
    "UNSCORED_COMPLETION_CLAIM",
    "DONE_WITHOUT_RECEIPT",
    "VALIDATION_CLAIM_UNVERIFIED",
)

_RECEIPT_MARKER_RE = re.compile(
    r"https?://\S+|\b[0-9a-fA-F]{40}\b|\b(receipt|evidence)\b",
    re.IGNORECASE,
)
_VALIDATION_PHRASES = ("different seat", "independently verified")


def collect_flags(prs, posts):
    """Draft flags from PR records and board posts.

    Args:
        prs:   list of PR records (identity_separation shape plus
               "body"), or None when the source was skipped.
        posts: list of board posts {"id", "author", "body"}, or
               None when the source was skipped.

    Returns:
        A list of flag dicts:
        {"source_type", "source_id", "type", "detail"}.
    """
    flags = []
    identity_check = _load_identity_check() or _fallback_identity_check
    scan_text = _load_scan_text() or _fallback_scan_text

    if prs is not None:
        for record in prs:
            if not isinstance(record, dict):
                continue
            if not record.get("merged"):
                continue
            number = record.get("number", record.get("id", "unknown"))
            source_id = f"PR #{number}"
            body = record.get("body") or ""

            # (a) Identity separation on every merged PR.
            try:
                verdict = identity_check(record)
            except Exception as exc:  # fail closed: an error is a flag
                verdict = {
                    "pass": False,
                    "reasons": [f"identity check raised: {exc}"],
                    "details": {},
                }
            if not verdict.get("pass"):
                reasons = verdict.get("reasons") or ["identity check failed"]
                flags.append({
                    "source_type": "pr",
                    "source_id": source_id,
                    "type": "IDENTITY_DRIFT",
                    "detail": "; ".join(str(r) for r in reasons),
                })

            # (b) Unscored completion claims in the PR body.
            try:
                hits = scan_text(body) if body else []
            except Exception as exc:
                hits = [f"scan_text raised: {exc}"]
            for hit in hits or []:
                flags.append({
                    "source_type": "pr",
                    "source_id": source_id,
                    "type": "UNSCORED_COMPLETION_CLAIM",
                    "detail": str(hit),
                })

    if posts is not None:
        for post in posts:
            if not isinstance(post, dict):
                continue
            post_id = post.get("id", "unknown")
            source_id = f"post {post_id}"
            body = post.get("body") or ""

            # (c) Done-claim with no receipt marker.
            if _DONE_RE.search(body) and not _RECEIPT_MARKER_RE.search(body):
                flags.append({
                    "source_type": "post",
                    "source_id": source_id,
                    "type": "DONE_WITHOUT_RECEIPT",
                    "detail": (
                        "done-claim with no receipt marker "
                        "(no link, no 40-hex sha, no receipt/evidence)"
                    ),
                })

            # (d) Validation claims in text prove nothing.
            lowered = body.lower()
            for phrase in _VALIDATION_PHRASES:
                if phrase in lowered:
                    flags.append({
                        "source_type": "post",
                        "source_id": source_id,
                        "type": "VALIDATION_CLAIM_UNVERIFIED",
                        "detail": (
                            f"post claims {phrase!r} — identity must be "
                            "checked against PR data; text claims "
                            "prove nothing"
                        ),
                    })

    return flags


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------


def build_report(flags, *, prs_provided, posts_provided,
                 prs_count=0, posts_count=0, notes=None):
    """Render the markdown draft flag report."""
    now = datetime.now(timezone.utc)
    date_line = now.strftime("%Y-%m-%d %H:%M UTC")
    counts = Counter(f["type"] for f in flags)

    lines = []
    lines.append("# Drift Watchdog — draft flag report")
    lines.append("")
    lines.append(f"Date: {date_line}")
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    if prs_provided:
        lines.append(f"- PRs: {prs_count} record(s) examined")
    else:
        lines.append("- PRs: skipped (no --prs input)")
    if posts_provided:
        lines.append(f"- Board posts: {posts_count} record(s) examined")
    else:
        lines.append("- Board posts: skipped (no --posts input)")
    for note in notes or []:
        lines.append(f"- Note: {note}")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    for flag_type in FLAG_TYPES:
        lines.append(f"- {flag_type}: {counts.get(flag_type, 0)}")
    lines.append(f"- TOTAL: {len(flags)}")
    lines.append("")
    lines.append("## Flags")
    lines.append("")
    if not flags:
        lines.append("No flags drafted.")
    else:
        for flag in flags:
            lines.append(
                f"- [{flag['type']}] {flag['source_id']}: {flag['detail']}"
            )
    lines.append("")
    lines.append("## Honest bounds")
    lines.append("")
    lines.append(
        "This report is a heuristic draft for a director. "
        "A flag is a question, not a verdict: heuristics draft "
        "flags for a director to adjudicate against the underlying "
        "PRs, reviews and receipts. Text matching can miss drift "
        "phrased differently and can flag innocent mentions of "
        "completion. Validation language in a post proves nothing "
        "about identity; only the PR data does. The watchdog "
        "issues no verdicts and blocks nothing."
    )
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _load_json_list(spec):
    """Load a JSON list from an @file spec (or a plain path).

    Returns the list. Raises ValueError/OSError on bad input;
    the caller turns that into a skipped-source note.
    """
    path_text = spec[1:] if spec.startswith("@") else spec
    text = Path(path_text).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError(f"{path_text}: top-level JSON is not a list")
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Drift watchdog: draft flag reports from recent "
            "PR / board data. Drafts flags; never issues verdicts."
        )
    )
    parser.add_argument(
        "--prs", default=None,
        help="JSON list of PR records (@file or path); optional",
    )
    parser.add_argument(
        "--posts", default=None,
        help="JSON list of board posts (@file or path); optional",
    )
    parser.add_argument(
        "--out", default=None,
        help="write the report to this path (default: stdout)",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="exit 1 if any flags were drafted (default: exit 0)",
    )
    args = parser.parse_args(argv)

    notes = []
    prs = None
    posts = None

    if args.prs is not None:
        try:
            prs = _load_json_list(args.prs)
        except Exception as exc:
            notes.append(f"PR source unreadable, skipped: {exc}")
            prs = None
    if args.posts is not None:
        try:
            posts = _load_json_list(args.posts)
        except Exception as exc:
            notes.append(f"board-post source unreadable, skipped: {exc}")
            posts = None

    flags = collect_flags(prs, posts)
    report = build_report(
        flags,
        prs_provided=prs is not None,
        posts_provided=posts is not None,
        prs_count=len(prs) if prs is not None else 0,
        posts_count=len(posts) if posts is not None else 0,
        notes=notes,
    )

    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
    else:
        print(report)

    if args.strict and flags:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
