"""Fail-closed static controls for the pending legacy Smart Mail privacy cure.

The baseline is the 2026-11-11 *policy name* census, not a data read.
These tests prove the proposed migration's final policy inventory; they do
NOT prove that production RLS is safe or that the migrations were applied.
"""
from __future__ import annotations

import re
from pathlib import Path

from pglast import parse_sql

ROOT = Path(__file__).resolve().parents[1]
FIRST = ROOT / "supabase/migrations/20261023190000_smart_mail_legacy_rls_hardening.sql"
FINISH = ROOT / "supabase/migrations/20261024194500_smart_mail_participant_completion_and_intake_scope_v1.sql"

# Name-only metadata from actual Supabase pg_policies, November 11, 2026.
OBSERVED = {
    "smart_mail_messages": {
        "pass2_anon_insert_smart_mail_messages",
        "pass2_anon_select_smart_mail_messages",
        "pass2_anon_update_smart_mail_messages",
        "smart_mail_messages_owner_delete",
        "smart_mail_messages_owner_select",
    },
    "smart_mail_threads": {
        "pass2_anon_insert_smart_mail_threads",
        "pass2_anon_select_smart_mail_threads",
        "pass2_anon_update_smart_mail_threads",
        "smart_mail_threads_owner_select",
    },
}
EXPECTED = {
    "smart_mail_messages": {"smart_mail_messages_participant_select"},
    "smart_mail_threads": {"smart_mail_threads_participant_select"},
}
DROP = re.compile(
    r"\bdrop\s+policy\s+if\s+exists\s+(\w+)\s+on\s+public\.(\w+)\s*;",
    re.IGNORECASE,
)
CREATE = re.compile(
    r"\bcreate\s+policy\s+(\w+)\s+on\s+public\.(\w+)\b",
    re.IGNORECASE,
)


def executable(sql: str) -> str:
    return re.sub(r"--[^\n]*", "", sql)


def final_mail_policies(first: str, finish: str) -> dict[str, set[str]]:
    result = {table: set(names) for table, names in OBSERVED.items()}
    for raw in (first, finish):
        sql = executable(raw)
        parse_sql(sql)  # Reject malformed SQL; no database connection or execution.
        for name, table in DROP.findall(sql):
            if table in result:
                result[table].discard(name)
        for name, table in CREATE.findall(sql):
            if table in result:
                result[table].add(name)
    return result


def test_pending_chain_closes_all_observed_legacy_mail_policies() -> None:
    actual = final_mail_policies(FIRST.read_text(encoding="utf-8"), FINISH.read_text(encoding="utf-8"))
    assert actual == EXPECTED


def test_followup_revokes_anon_table_privileges_and_avoids_user_metadata() -> None:
    sql = executable(FINISH.read_text(encoding="utf-8"))
    assert "user_metadata" not in sql.lower()
    assert re.search(
        r"\brevoke\s+all\s+privileges\s+on\s+table\s+"
        r"public\.smart_mail_messages\s*,\s*public\.smart_mail_threads\s+from\s+anon\s*;",
        sql,
        re.IGNORECASE,
    )


def test_negative_controls_catch_each_surviving_unsafe_policy() -> None:
    first = FIRST.read_text(encoding="utf-8")
    finish = FINISH.read_text(encoding="utf-8")
    for table, policy in (
        ("smart_mail_threads", "smart_mail_threads_owner_select"),
        ("smart_mail_messages", "smart_mail_messages_owner_delete"),
    ):
        statement = f"drop policy if exists {policy} on public.{table};"
        assert statement in finish
        sabotaged = finish.replace(statement, "", 1)
        assert final_mail_policies(first, sabotaged)[table] != EXPECTED[table]


def test_pending_order_has_prerequisites_in_repo() -> None:
    required = (
        "20261022213000_conversational_intake_v1.sql",
        "20261022220000_alias_binding_v1.sql",
        FIRST.name,
        FINISH.name,
    )
    assert all((ROOT / "supabase/migrations" / name).is_file() for name in required)
    assert list(required) == sorted(required)


def test_pending_ledger_metadata_matches_candidate_sql() -> None:
    import hashlib
    import json

    ledger = json.loads(
        (ROOT / "supabase/PRODUCTION-MIGRATION-LEDGER-V1.json").read_text(encoding="utf-8")
    )
    entries = [e for e in ledger["pending"] if e["version"] == "20261024194500"]
    assert len(entries) == 1
    entry = entries[0]
    source = FINISH.read_bytes()
    assert entry["status"] == "PENDING_REVIEW_NOT_PRODUCTION_APPLIED"
    assert entry["sha256"] == hashlib.sha256(source).hexdigest()
    assert entry["bytes"] == len(source)
    assert entry["statement_count"] == len(parse_sql(source.decode("utf-8")))
