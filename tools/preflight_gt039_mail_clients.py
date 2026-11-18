#!/usr/bin/env python3
"""GT-039 mail-client/source compatibility preflight. Read only; no web/DB access.

A private-mail security migration must not silently disable the existing
visitor send or booking-reminder paths. Static source cannot prove deployment
or a replacement transport, so this tool intentionally has NO PASS verdict.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (
    "supabase/migrations/"
    "20261024194500_smart_mail_participant_completion_and_intake_scope_v1.sql"
)
CLIENT_FILES = (
    "DASHBOARD/app/index.html",
    "interfaces/walk/flagship-template.html",
    "PERSONAL/index-master-20261105.html",
)
BOOKING_FILE = "HUB/booking/booking-store.mjs"

REVOKE = re.compile(
    r"\brevoke\s+all\s+privileges\s+on\s+table\s+"
    r"public\.smart_mail_messages\s*,\s*public\.smart_mail_threads\s+from\s+anon\s*;",
    re.I,
)
ANON_CLIENT = re.compile(
    r"supabase\.createClient\(\s*(?:SB_URL|SUPABASE_URL)\s*,\s*"
    r"(?:SB_ANON|SUPABASE_ANON)\s*\)"
)
THREAD_INSERT = re.compile(r"\.from\(['\"]smart_mail_threads['\"]\)\.insert\(", re.I)
RETURNED_THREAD = re.compile(
    r"\.from\(['\"]smart_mail_threads['\"]\)\.insert\("
    r"[^;\n]*\)\.select\(\)\.single\(\)",
    re.I,
)
MESSAGE_INSERT = re.compile(r"\.from\(['\"]smart_mail_messages['\"]\)\.insert\(", re.I)
REST_THREAD = re.compile(r"fetchImpl\([^;]*?/smart_mail_threads", re.S | re.I)
REST_MESSAGE = re.compile(r"fetchImpl\([^;]*?/smart_mail_messages", re.S | re.I)


class PreflightError(ValueError):
    pass


def read(root: Path, filename: str) -> str:
    path = root / filename
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PreflightError(f"REQUIRED_SOURCE_UNAVAILABLE: {filename}: {exc}") from exc


def line_of(source: str, token: str) -> int | None:
    pos = source.find(token)
    return source.count("\n", 0, pos) + 1 if pos >= 0 else None


def evaluate(root: Path = ROOT) -> dict:
    sql = read(root, MIGRATION)
    if not REVOKE.search(sql):
        # Removing the security fix does NOT make mail client compatibility pass.
        raise PreflightError("SECURITY_REVOKE_CONTRACT_MISSING: not evidence of a safe mail path")
    direct = []
    for filename in CLIENT_FILES:
        source = read(root, filename)
        features = {
            "public_key_client": bool(ANON_CLIENT.search(source)),
            "direct_thread_insert": bool(THREAD_INSERT.search(source)),
            "requires_returned_thread_id": bool(RETURNED_THREAD.search(source)),
            "direct_message_insert": bool(MESSAGE_INSERT.search(source)),
        }
        if all(features.values()):
            direct.append({
                "path": filename,
                "thread_insert_line": line_of(source, "from('smart_mail_threads').insert("),
                "feature": "direct browser mail send",
                "features": features,
            })
    booking = read(root, BOOKING_FILE)
    reminder = REST_THREAD.search(booking) is not None and REST_MESSAGE.search(booking) is not None
    if not direct and not reminder:
        raise PreflightError("CLIENT_PATHS_NOT_FOUND: do not infer replacement/deployed PASS")
    return {
        "verdict": "BLOCKED_MAIL_CLIENT_COMPAT" if direct else "UNKNOWN_RUNTIME_COMPATIBILITY",
        "evidence_level": "committed source only; NOT proof this source is currently deployed",
        "reason": (
            "Committed visitor mail sends require direct INSERT + RETURNING "
            "on legacy tables but proposed migration revokes anonymous "
            "table grants. Without a replacement transport, an unauthenticated "
            "visitor send would fail."
            if direct else "Direct visitor path not found; replacement and deployment unverified."
        ),
        "affected_browser_sources": direct,
        "booking_reminder_rest_insert_found": reminder,
        "booking_reminder_requires_independent_functional_proof": reminder,
        "candidate_migration": MIGRATION,
        "no_release_approval": True,
    }


def main() -> int:
    try:
        result = evaluate()
    except PreflightError as exc:
        print(json.dumps({"verdict": "UNKNOWN_FAIL_CLOSED", "error": str(exc)}, sort_keys=True))
        return 3
    print(json.dumps(result, indent=2, sort_keys=True))
    return 2 if result["verdict"] == "BLOCKED_MAIL_CLIENT_COMPAT" else 3


if __name__ == "__main__":
    raise SystemExit(main())
