#!/usr/bin/env python3
"""SN-0734 — Re-resolve PRs by topic/title, not branch prefix (Shawn ratified 2026-10-09).

When a seat disposes a pull request — closes, rejects, marks superseded —
the decision must rest on content evidence: the PR's topic/title and what
its bytes actually do. Branch-name prefixes collide across lanes
(naya5/x vs naya4/x, wave branches, repair branches); a prefix is not an
identity and never a verdict.

Validates a PR-disposition record. The hard line: a close/reject/supersede
whose basis is "branch_prefix" fails — re-resolve the PR by its topic and
title, read the bytes, then decide.

Input record:
    {
      "pr": 1998,
      "disposition": "closed" | "rejected" | "superseded" | "merged",
      "basis": "topic_title" | "content_analysis" | "branch_prefix",
      "evidence": "<what the bytes/topic actually show>"
    }

Checks:
  1. disposition closed/rejected/superseded requires basis
     "topic_title" or "content_analysis" with non-empty evidence.
  2. basis == "branch_prefix" fails closed (prefixes collide; content decides).
  3. disposition == "merged" requires basis "topic_title"/"content_analysis"
     as well — a merge by prefix is an unverified merge.

Collision note: the design-intake corpus uses SN-0734 for a different law
("never ship the same flaw twice"). This encoding follows the
merge-queue/operational definition ratified on #1354; the title above
disambiguates. If the registry collision is resolved by the Director,
renumber this entry — never silently merge the two meanings.

Usage:
    python3 tools/protocol/checks/pr_resolution.py \
        --record '{"pr": 1998, ...}' [--json]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

CONTENT_BASES = {"topic_title", "content_analysis"}
DISPOSITIONS = {"closed", "rejected", "superseded", "merged"}


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-0734", "law_status": "RATIFIED",
                     "law_title": "Re-resolve PRs by topic/title, not branch prefix"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    pr = record.get("pr")
    disposition = str(record.get("disposition") or "").strip().lower()
    basis = str(record.get("basis") or "").strip().lower()
    evidence = str(record.get("evidence") or "").strip()

    details.update({"pr": pr, "disposition": disposition, "basis": basis})

    if not pr:
        return fail("pr missing — name the pull request being disposed", details)
    if disposition not in DISPOSITIONS:
        return fail(
            f"PR #{pr}: disposition {disposition!r} — must be one of "
            f"{sorted(DISPOSITIONS)}",
            details,
        )
    reasons.append(f"PR #{pr}: disposition '{disposition}'")

    if basis == "branch_prefix":
        return fail(
            f"PR #{pr}: basis is 'branch_prefix' — branch prefixes collide "
            "across lanes and are not an identity. Re-resolve the PR by its "
            "topic/title and read its bytes before disposing it.",
            details,
        )
    if basis not in CONTENT_BASES:
        return fail(
            f"PR #{pr}: basis {basis!r} — dispositions rest on content: "
            "'topic_title' or 'content_analysis'. Nothing else decides.",
            details,
        )
    reasons.append(f"basis '{basis}' is content, not prefix")

    if not evidence:
        return fail(
            f"PR #{pr}: evidence missing — a content-basis disposition without "
            "content evidence is an assertion, not a resolution",
            details,
        )
    reasons.append("content evidence recorded")
    details["evidence"] = evidence

    reasons.append(f"PR #{pr}: honestly resolved by {basis}")
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0734 PR-resolution check")
    parser.add_argument("--record", required=True,
                        help="JSON PR-disposition record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-0734"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
