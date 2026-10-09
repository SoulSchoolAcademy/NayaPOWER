#!/usr/bin/env python3
"""SN-0735 — Duplicate PRs get blob-compared against main before close/merge (Shawn ratified 2026-10-09).

The revert-bomb check. Before a pull request is closed as duplicate /
superseded, or merged, its file bytes must be compared against current
main — blob SHA to blob SHA. A PR that would move main's bytes BACKWARDS
on any path is a revert bomb: merging it silently destroys other lanes'
landed work. The comparison is the gate; without it there is no close
and no merge.

Validates a duplicate-PR resolution record. The hard lines: no
blob_comparison, no disposition; any path where the PR's bytes would
replace main's newer bytes (revert_risk) fails closed.

Input record:
    {
      "pr": 1998,
      "disposition": "closed_as_duplicate" | "closed_as_superseded" | "merged",
      "main_tip_sha": "<40-hex full SHA of main at comparison time>",
      "blob_comparison": [
        {"path": "tools/x.py", "pr_blob": "<40-hex>", "main_blob": "<40-hex>",
         "identical": true, "reverts_main": false}
      ]
    }

Checks:
  1. blob_comparison is a non-empty list; every entry has 40-hex pr_blob
     and main_blob and a boolean identical flag.
  2. identical must be consistent with pr_blob == main_blob (the math is
     checked, not trusted).
  3. Any entry with reverts_main true fails closed — the revert bomb.
  4. An entry that is non-identical, unexplained, and disposed by merge
     fails: merges need the revert direction established for every delta.

Collision note: the design-intake corpus uses SN-0735 for a different law
("copy approved code verbatim"). This encoding follows the
merge-queue/operational definition ratified on #1354; the title above
disambiguates. If the registry collision is resolved by the Director,
renumber this entry — never silently merge the two meanings.

Usage:
    python3 tools/protocol/checks/duplicate_pr_blobs.py \
        --record '{"pr": 1998, ...}' [--json]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checks import emit, fail, load_record, result  # noqa: E402

HEX40 = re.compile(r"^[0-9a-f]{40}$")
DISPOSITIONS = {"closed_as_duplicate", "closed_as_superseded", "merged"}


def _hex40(value, what: str, details: dict) -> str | None:
    v = str(value or "").strip().lower()
    if not HEX40.match(v):
        return None
    return v


def check(record: dict) -> dict:
    reasons: list[str] = []
    details: dict = {"law": "SN-0735", "law_status": "RATIFIED",
                     "law_title": "Duplicate PRs blob-compared against main (revert-bomb check)"}

    if not isinstance(record, dict):
        return fail("record is not a JSON object", details)

    pr = record.get("pr")
    disposition = str(record.get("disposition") or "").strip().lower()
    tip = _hex40(record.get("main_tip_sha"), "main_tip_sha", details)
    rows = record.get("blob_comparison")

    details.update({"pr": pr, "disposition": disposition})

    if not pr:
        return fail("pr missing — name the pull request", details)
    if disposition not in DISPOSITIONS:
        return fail(
            f"PR #{pr}: disposition {disposition!r} — must be one of "
            f"{sorted(DISPOSITIONS)}",
            details,
        )
    if not tip:
        return fail(
            f"PR #{pr}: main_tip_sha missing or not a full 40-hex SHA — "
            "the comparison is against an exact main, never 'roughly current'",
            details,
        )
    details["main_tip_sha"] = tip
    reasons.append(f"PR #{pr}: disposition '{disposition}', main pinned at {tip[:12]}")

    if not isinstance(rows, list) or not rows:
        return fail(
            f"PR #{pr}: blob_comparison empty or missing — no blob comparison, "
            "no close, no merge. The revert-bomb check is the gate.",
            details,
        )

    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            return fail(f"PR #{pr}: blob_comparison[{i}] is not an object", details)
        path = str(row.get("path") or f"<row {i}>").strip()
        pr_blob = _hex40(row.get("pr_blob"), f"{path}.pr_blob", details)
        main_blob = _hex40(row.get("main_blob"), f"{path}.main_blob", details)
        if not pr_blob or not main_blob:
            return fail(
                f"PR #{pr}: {path}: pr_blob/main_blob must both be full 40-hex "
                "blob SHAs — abbreviated SHAs are a false-acceptance path",
                details,
            )
        claimed_identical = row.get("identical")
        actual_identical = pr_blob == main_blob
        if claimed_identical is not True and claimed_identical is not False:
            return fail(
                f"PR #{pr}: {path}: 'identical' must be an explicit boolean",
                details,
            )
        if claimed_identical != actual_identical:
            return fail(
                f"PR #{pr}: {path}: claimed identical={claimed_identical} but "
                f"blob math says {actual_identical} — the math is checked, not trusted",
                details,
            )
        if row.get("reverts_main") is True:
            return fail(
                f"PR #{pr}: {path}: REVERT BOMB — this path would move main's "
                "bytes backwards. Disposition refused. Retire the branch, "
                "rebase on the new main, re-resolve.",
                details,
            )
        reasons.append(f"{path}: {'identical' if actual_identical else 'delta, no revert'}")

    details["paths_compared"] = len(rows)
    reasons.append(
        f"PR #{pr}: {len(rows)} path(s) blob-compared against main {tip[:12]} — "
        "no revert risk; disposition may proceed"
    )
    return result(True, reasons, details)


def main() -> int:
    parser = argparse.ArgumentParser(description="SN-0735 revert-bomb check")
    parser.add_argument("--record", required=True,
                        help="JSON duplicate-PR record (or @file)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    try:
        record = load_record(args.record)
    except Exception as e:
        return emit(fail(f"unparseable record: {e}", {"law": "SN-0735"}), args.json)
    return emit(check(record), args.json)


if __name__ == "__main__":
    sys.exit(main())
