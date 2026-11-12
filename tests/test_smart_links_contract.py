"""Smart Links contract tests — migration <-> code drift + RLS shape.

The reserved-name list has ONE source (HUB/smart-links/reserved-names.mjs);
the migration seed mirrors it. These tests fail if the two drift, if the
RLS shape weakens (anon update/delete, listable links table), or if the
SQL stops parsing. The audit runs against the real migration text and —
as a negative control — against a doctored copy that must FAIL the audit.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20261022201500_smart_links_v1.sql"
RESERVED_MJS = ROOT / "HUB" / "smart-links" / "reserved-names.mjs"
WORKER = ROOT / "HUB" / "smart-links" / "worker.js"


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def _reserved_names_from_mjs() -> list[str]:
    text = RESERVED_MJS.read_text(encoding="utf-8")
    block = re.search(r"RESERVED_NAMES = Object\.freeze\(\[(.*?)\]\)", text, re.S)
    assert block, "RESERVED_NAMES block not found in reserved-names.mjs"
    return re.findall(r"'([^']+)'", block.group(1))


def audit(sql: str) -> list[str]:
    """Return the list of contract violations in a smart-links migration."""
    problems: list[str] = []
    low = sql.lower()
    for table in ("smart_links", "smart_link_clicks", "smart_link_reserved_names"):
        if f"create table if not exists public.{table}" not in low:
            problems.append(f"missing table {table}")
        if f"alter table public.{table} enable row level security" not in low:
            problems.append(f"RLS not enabled on {table}")
    if "resolve_smart_link" not in low or "security definer" not in low:
        problems.append("resolve_smart_link security-definer RPC missing")
    if "smart_links_guard_reserved" not in low:
        problems.append("reserved-name guard trigger missing")
    # Append-only clicks: an insert policy for anon must exist, and NO
    # policy may grant update or delete on clicks to anyone.
    if not re.search(r"create policy \w+ on public\.smart_link_clicks\s+for insert to anon", low):
        problems.append("anon append policy on smart_link_clicks missing")
    for m in re.finditer(r"create policy \w+ on public\.smart_link_clicks\s+for (update|delete)", low):
        problems.append(f"clicks must be append-only, found a {m.group(1)} policy")
    # No anon write/delete on the links table itself.
    for m in re.finditer(r"create policy \w+ on public\.smart_links\s+for (insert|update|delete) to anon", low):
        problems.append(f"anon {m.group(1)} on smart_links is forbidden")
    # Anon must never get a direct SELECT on the links table (enumeration);
    # resolution goes through the RPC only.
    if re.search(r"create policy \w+ on public\.smart_links\s+for select to anon", low):
        problems.append("anon select on smart_links would enumerate the directory")
    # Every reserved name from the single source must be seeded.
    seed = set(re.findall(r"\('([a-z0-9.\-]+)'\)", low))
    for name in _reserved_names_from_mjs():
        if name not in seed:
            problems.append(f"reserved name {name!r} not seeded in migration")
    return problems


def test_migration_satisfies_the_contract():
    assert audit(_sql()) == []


def test_negative_control_doctored_sql_fails_the_audit():
    doctored = _sql().replace("smart_links_guard_reserved", "guard_removed")
    problems = audit(doctored)
    assert any("guard trigger" in p for p in problems), problems
    weakened = _sql() + (
        "\ncreate policy bad on public.smart_link_clicks for delete to anon using (true);\n"
    )
    problems = audit(weakened)
    assert any("append-only" in p for p in problems), problems


def test_sql_parses_as_postgres():
    try:
        import pglast
    except ImportError:  # local fallback: CI installs pglast (kernel-tests)
        import pytest

        pytest.skip("pglast not installed locally")
    statements = pglast.parse_sql(_sql())
    assert len(statements) >= 20


def test_worker_uses_the_single_reserved_source():
    worker = WORKER.read_text(encoding="utf-8")
    assert "from './reserved-names.mjs'" in worker
    assert "isReservedName" in worker
    # The worker must never await the count before redirecting.
    assert "waitUntil" in worker
