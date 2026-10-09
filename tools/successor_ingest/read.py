"""Canonical-store reader — the ONLY network seam in this package.

Reads verified learnings from Supabase ``learning_evidence`` via the
approved read-only ``sb-api`` CLI (the CLI never handles raw keys; only
the authd surrogate leaves the machine). Read-only: the query is a bare
SELECT with explicit columns and a LIMIT — small enough to stay under the
CLI's output truncation.

Fail-closed contract:
  - CLI non-zero / bad JSON  -> IngestError("STORE_UNREACHABLE")
  - zero rows                -> handled downstream by select.eligible_lessons
    ("NO_VERIFIED_LESSONS")
  - a row is NEVER invented, defaulted, or cached-from-stale-data here.

Everything else in the package takes injected rows, so the whole core is
testable with zero network.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone

PROJECT_REF = "dahisasgpfvziswqvmvm"
SB_API = "/home/hatch/workspace/skills/supabase/bin/sb-api"

QUERY = (
    "SELECT id, target_id, level, status, provenance, verification_method, claim "
    "FROM learning_evidence "
    "WHERE level = 'E5_CAN_TEACH' AND status = 'ACTIVE' "
    "ORDER BY created_at DESC LIMIT 25"
)


class IngestError(Exception):
    """Fail-closed ingestion failure. code names the exact refusal."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def fetch_verified_rows(timeout: int = 60) -> list[dict]:
    """Read candidate-verified rows from the canonical store.

    Each returned row is stamped with retrieved_at and the exact query —
    retrieval provenance travels WITH the lesson from this point on.
    """
    try:
        proc = subprocess.run(
            [SB_API, "POST", f"/v1/projects/{PROJECT_REF}/database/query",
             json.dumps({"query": QUERY})],
            capture_output=True, text=True, timeout=timeout,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        raise IngestError("STORE_UNREACHABLE", f"sb-api failed to run: {exc}")
    if proc.returncode != 0:
        raise IngestError(
            "STORE_UNREACHABLE",
            f"sb-api exit {proc.returncode}: {proc.stderr[:200]}",
        )
    try:
        rows = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise IngestError("STORE_UNREACHABLE", f"unparseable store reply: {exc}")
    if not isinstance(rows, list):
        raise IngestError("STORE_UNREACHABLE", "store reply was not a row list")
    now = datetime.now(timezone.utc).isoformat()
    for r in rows:
        r["retrieved_at"] = now
        r["query"] = QUERY
    return rows
