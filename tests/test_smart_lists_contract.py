"""Smart Lists contract tests — migration RLS shape + typed-item safety.

The store's safety claims live in the migration text: owner-only RLS on
both tables with NO anonymous path, item writes fenced to the writer's
own lists, the six typed kinds in the CHECK, and — the deletion-safety
invariant — items holding NO foreign key to any object table, so
removing an item can never delete the object it references. These tests
audit the real migration text and, as negative controls, doctored copies
that must FAIL the audit.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20261022223000_smart_lists_v1.sql"
MODULE = ROOT / "HUB" / "app" / "js" / "smart-lists.js"

TABLES = ("smart_lists", "smart_list_items")
OPS = ("select", "insert", "update", "delete")
KINDS = ("smart_note", "naya_note", "person", "mail_thread", "smart_link", "text")
OBJECT_TABLES = ("naya_notes", "smart_notes", "smart_links", "smart_mail_threads",
                 "smart_mail_messages", "person_timeline")


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def _policies(sql: str) -> list[str]:
    """Each `create policy ... ;` statement, whitespace-normalized, lowered."""
    return [
        re.sub(r"\s+", " ", m.group(0)).lower()
        for m in re.finditer(r"create policy .*?;", sql, flags=re.S | re.I)
    ]


def audit(sql: str) -> list[str]:
    """Return the list of contract violations in a smart-lists migration."""
    problems: list[str] = []
    low = sql.lower()
    policies = _policies(sql)
    for table in TABLES:
        if f"create table if not exists public.{table}" not in low:
            problems.append(f"missing table {table}")
        if f"alter table public.{table} enable row level security" not in low:
            problems.append(f"RLS not enabled on {table}")
        for op in OPS:
            name = f"{table}_owner_{op}"
            match = [p for p in policies if f"create policy {name} on public.{table}" in p]
            if not match:
                problems.append(f"missing owner {op} policy on {table}")
                continue
            stmt = match[0]
            if "to authenticated" not in stmt:
                problems.append(f"{name} is not scoped to authenticated")
            if "owner_id = (select auth.uid())" not in stmt:
                problems.append(f"{name} does not fence on owner_id = auth.uid()")
    # No anonymous or public path anywhere — lists are private, by design.
    for stmt in policies:
        if " to anon" in stmt or " to public" in stmt:
            problems.append(f"non-owner policy role present: {stmt[:80]}")
    # The six typed kinds, in the DB CHECK and in the module vocabulary.
    kind_block = re.search(r"smart_list_items_kind\s+check\s*\(\s*item_kind in \((.*?)\)\s*\)",
                           low, flags=re.S)
    if not kind_block:
        problems.append("item_kind CHECK constraint missing")
        kind_literals = ""
    else:
        kind_literals = kind_block.group(1)
    for kind in KINDS:
        if f"'{kind}'" not in kind_literals:
            problems.append(f"item kind {kind!r} missing from the migration")
    module = MODULE.read_text(encoding="utf-8")
    for kind in KINDS:
        if f"'{kind}'" not in module:
            problems.append(f"item kind {kind!r} missing from the Hub module")
    # Membership cascade: deleting a list removes its membership rows.
    if "references public.smart_lists(id) on delete cascade" not in low:
        problems.append("items->lists cascade missing")
    # Item writes must be fenced to the writer's own lists (parent guard).
    for op in ("insert", "update"):
        match = [p for p in policies
                 if f"create policy smart_list_items_owner_{op} on public.smart_list_items" in p]
        if match and "parent.owner_id = (select auth.uid())" not in match[0]:
            problems.append(f"items {op} policy lacks the parent-list owner guard")
    # Deletion safety by construction: an item references an object by
    # plain (kind, ref) text — a foreign key to any object table would put
    # the object one cascade away from a list edit.
    for table in OBJECT_TABLES:
        if f"references public.{table}" in low:
            problems.append(f"items must not hold a foreign key to {table}")
    # Text/reference coherence shape check.
    if "smart_list_items_shape" not in low:
        problems.append("item shape CHECK (text vs reference) missing")
    return problems


def test_migration_satisfies_the_contract():
    assert audit(_sql()) == []


def test_negative_control_anon_policy_fails_the_audit():
    doctored = _sql().replace(
        "create policy smart_lists_owner_select on public.smart_lists\n  for select to authenticated",
        "create policy smart_lists_owner_select on public.smart_lists\n  for select to anon",
    )
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("authenticated" in p or "anon" in p for p in problems), problems


def test_negative_control_kind_removed_fails_the_audit():
    doctored = _sql().replace("'naya_note', ", "")
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("naya_note" in p for p in problems), problems


def test_negative_control_object_foreign_key_fails_the_audit():
    doctored = _sql().replace(
        "references public.smart_lists(id) on delete cascade",
        "references public.naya_notes(id) on delete cascade",
    )
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("cascade" in p or "foreign key" in p for p in problems), problems


def test_negative_control_parent_guard_removed_fails_the_audit():
    doctored = _sql().replace("parent.owner_id = (select auth.uid())",
                              "parent.owner_id = owner_id")
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("parent-list owner guard" in p for p in problems), problems


def test_sql_parses_as_postgres():
    try:
        import pglast
    except ImportError:  # local fallback: CI installs pglast (kernel-tests)
        import pytest

        pytest.skip("pglast not installed locally")
    statements = pglast.parse_sql(_sql())
    assert len(statements) == 24
