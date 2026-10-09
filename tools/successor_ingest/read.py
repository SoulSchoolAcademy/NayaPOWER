"""Canonical-store reader — the ONLY network seam in this package.

Reads verified learnings from Supabase ``learning_evidence`` through a
portable transport (the full cold path is documented in
``tools/successor_ingest/COLD-RETRIEVAL.md``). The transport is RESOLVED,
never hardcoded to one machine:

    1. ``NAYA_LESSON_TRANSPORT`` — explicit path to a transport executable
    2. ``SB_API``                — the connected-connector CLI (same wire shape)
    3. ``PATH`` lookup for ``sb-api``
    4. fail closed: ``IngestError("STORE_UNREACHABLE")`` naming the
       prerequisite and how to satisfy it

Transport protocol: ``<transport> POST /v1/projects/<ref>/database/query
'{"query": "<READ-ONLY SQL>"}'`` — JSON row list on stdout.

The query is a bare SELECT with explicit columns and a LIMIT — read-only
by construction. This package NEVER issues writes; Supabase stays
read-only (capability is not authority).

Fail-closed contract:
  - transport unresolvable / non-zero / bad JSON -> IngestError("STORE_UNREACHABLE")
  - zero rows                -> handled downstream by select.eligible_lessons
    ("NO_VERIFIED_LESSONS")
  - a row is NEVER invented, defaulted, or cached-from-stale-data here.

Everything else in the package takes injected rows, so the whole core is
testable with zero network.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime, timezone

# Default canonical project (an identifier, not a secret — the connector's
# authd surrogate holds the credentials; this value only names the project).
# Overridable per runtime: NAYA_LESSON_PROJECT_REF.
DEFAULT_PROJECT_REF = "dahisasgpfvziswqvmvm"

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


def resolve_project_ref() -> str:
    """Which canonical project to read. Env override, documented default."""
    ref = os.environ.get("NAYA_LESSON_PROJECT_REF", "").strip()
    return ref or DEFAULT_PROJECT_REF


def resolve_transport() -> tuple[str, str]:
    """Find the retrieval transport. Returns (path, source_name).

    Raises IngestError("STORE_UNREACHABLE") when nothing resolves — the
    refusal names the prerequisite instead of failing on a hardcoded
    private-machine path.
    """
    explicit = os.environ.get("NAYA_LESSON_TRANSPORT", "").strip()
    if explicit:
        return explicit, "NAYA_LESSON_TRANSPORT"
    sb_api = os.environ.get("SB_API", "").strip()
    if sb_api:
        return sb_api, "SB_API"
    on_path = shutil.which("sb-api")
    if on_path:
        return on_path, "PATH"
    raise IngestError(
        "STORE_UNREACHABLE",
        "no retrieval transport resolved: set NAYA_LESSON_TRANSPORT to a "
        "transport executable (see tools/successor_ingest/COLD-RETRIEVAL.md), "
        "or make the sb-api CLI resolvable via the SB_API env var or PATH. "
        "No lesson rows were read; none were invented.",
    )


def fetch_verified_rows(
    timeout: int = 60,
    transport: "str | list[str] | None" = None,
    project_ref: str | None = None,
) -> list[dict]:
    """Read candidate-verified rows from the canonical store.

    Each returned row is stamped with retrieved_at and the exact query —
    retrieval provenance travels WITH the lesson from this point on.

    ``transport`` may be injected (path or argv prefix) for tests; when
    None it is resolved via resolve_transport().
    """
    if transport is None:
        transport, _source = resolve_transport()
        argv = [transport]
    elif isinstance(transport, str):
        argv = [transport]
    else:
        argv = list(transport)
    ref = project_ref or resolve_project_ref()
    try:
        proc = subprocess.run(
            argv + ["POST", f"/v1/projects/{ref}/database/query",
                    json.dumps({"query": QUERY})],
            capture_output=True, text=True, timeout=timeout,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        raise IngestError("STORE_UNREACHABLE", f"transport failed to run: {exc}")
    if proc.returncode != 0:
        raise IngestError(
            "STORE_UNREACHABLE",
            f"transport exit {proc.returncode}: {proc.stderr[:200]}",
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
