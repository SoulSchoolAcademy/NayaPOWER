"""Cold retrieval CLI — the stranger's executable door to the lesson diary.

Implements the COLD-RETRIEVAL.md path as commands, not prose:

    python3 tools/successor_ingest/retrieve.py                 # all eligible lessons
    python3 tools/successor_ingest/retrieve.py --family state_file   # one family
    python3 tools/successor_ingest/retrieve.py --jsonl         # one lesson per line

What it does, in order:
  1. resolves the transport (fail closed: STORE_UNREACHABLE)
  2. SELECTs verified rows from learning_evidence (read-only)
  3. stamps every row with retrieved_at + the exact query (provenance)
  4. filters to successor-eligible lessons (fail closed: NO_VERIFIED_LESSONS)
  5. with --family: matches one task family (fail closed: UNKNOWN_TASK_FAMILY,
     NO_APPLICABLE_LESSON)

Output: JSON on stdout — the lessons plus a "retrieval" block naming the
transport, source, project ref, query, and timestamp. Nothing is printed
when the seam refuses; the refusal code goes to stderr.

Exit codes: 0 = retrieved; 3 = REFUSED (the seam's fail-closed refusal —
a named code, never invented rows); 2 = usage error.

Run from the repo root.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from successor_ingest import read, select  # noqa: E402

REFUSAL_EXIT = 3


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Retrieve verified lessons from the canonical store."
    )
    ap.add_argument(
        "--family",
        default=None,
        help="task family to match (e.g. state_file); omit for all eligible lessons",
    )
    ap.add_argument(
        "--jsonl",
        action="store_true",
        help="emit one lesson object per line (default: one JSON document)",
    )
    ap.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="store call timeout in seconds (default: 60)",
    )
    args = ap.parse_args(argv)

    try:
        transport, source = read.resolve_transport()
    except read.IngestError as exc:
        print(f"REFUSED {exc.code}: {exc.detail}", file=sys.stderr)
        return REFUSAL_EXIT

    try:
        rows = read.fetch_verified_rows(timeout=args.timeout, transport=transport)
    except read.IngestError as exc:
        print(f"REFUSED {exc.code}: {exc.detail}", file=sys.stderr)
        return REFUSAL_EXIT

    try:
        lessons = select.eligible_lessons(rows)
        if args.family:
            lessons = [select.match_task(lessons, args.family)]
    except select.SelectionError as exc:
        print(f"REFUSED {exc.code}: {exc.detail}", file=sys.stderr)
        return REFUSAL_EXIT

    retrieval = {
        "transport": transport,
        "transport_source": source,
        "project_ref": read.resolve_project_ref(),
        "query": read.QUERY,
        "retrieved_at": rows[0]["retrieved_at"] if rows else None,
        "row_count": len(rows),
        "eligible_count": len(lessons),
    }
    payload = [
        {
            "id": le.id,
            "target_id": le.target_id,
            "level": le.level,
            "status": le.status,
            "provenance": le.provenance,
            "verification_method": le.verification_method,
            "claim_text": le.claim_text,
            "retrieved_at": le.retrieved_at,
            "query": le.query,
        }
        for le in lessons
    ]
    if args.jsonl:
        for le in payload:
            print(json.dumps(le, sort_keys=True))
    else:
        print(json.dumps({"retrieval": retrieval, "lessons": payload}, indent=2,
                         sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
