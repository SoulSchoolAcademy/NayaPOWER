"""Booking block contract tests — migration <-> code drift + RLS shape.

The slot rules have ONE source of truth in the database (the guard
trigger + partial unique index in 20261022210000_booking_v1.sql) and a
mirror in HUB/booking/booking-core.mjs so the page can refuse kindly.
These tests fail if the two drift, if the RLS shape weakens (any anon
read of bookings or pages), if the timeline branch disappears, or if
the ledger entry stops matching the migration's real bytes. The audit
runs against the real migration text and — as a negative control —
against doctored copies that must FAIL it.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pglast

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20261022210000_booking_v1.sql"
LEDGER = ROOT / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json"
CORE = ROOT / "HUB" / "booking" / "booking-core.mjs"


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def audit(sql: str) -> list[str]:
    """Return the list of contract violations in a booking migration."""
    problems: list[str] = []
    low = sql.lower()
    for table in ("booking_pages", "booking_availability", "bookings"):
        if f"create table if not exists public.{table}" not in low:
            problems.append(f"missing table {table}")
        if f"alter table public.{table} enable row level security" not in low:
            problems.append(f"RLS not enabled on {table}")
    # Double-booking is refused twice: the named trigger + the index.
    if "bookings_guard_slot" not in low:
        problems.append("slot guard trigger missing")
    for err in ("booking_outside_availability", "booking_slot_taken"):
        if err not in low:
            problems.append(f"named refusal {err} missing")
    if not re.search(
        r"create unique index if not exists bookings_one_confirmed_per_slot"
        r"\s+on public\.bookings \(page_id, starts_at\)\s+where status = 'confirmed'",
        low,
    ):
        problems.append("partial unique index (one confirmed per slot) missing")
    # Owner fields are filled from the page, never from the payload.
    if "bookings_fill_owner" not in low:
        problems.append("owner fill trigger missing")
    # Public reads exist and are security-definer RPCs.
    for fn in ("get_booking_page", "get_booking_windows",
               "get_booked_starts", "cancel_booking"):
        if f"function public.{fn}" not in low or "security definer" not in low:
            problems.append(f"RPC {fn} missing or not security definer")
    # Anon must never read rows directly — RPCs are the only window.
    for m in re.finditer(
        r"create policy \w+ on public\.(booking_pages|booking_availability|bookings)"
        r"\s+for (select|update|delete) to anon",
        low,
    ):
        problems.append(f"anon {m.group(2)} on {m.group(1)} is forbidden")
    # The one anon write: a guarded insert on bookings.
    if not re.search(
        r"create policy \w+ on public\.bookings\s+for insert to anon", low
    ):
        problems.append("visitor insert policy on bookings missing")
    # Cross-owner detail leak: booked-starts RPC returns times only.
    rpc = re.search(
        r"function public\.get_booked_starts.*?as \$\$(.*?)\$\$",
        low, re.S,
    )
    if not rpc or "visitor" in rpc.group(1) or "note" in rpc.group(1):
        problems.append("get_booked_starts must expose times only")
    # Owner scoping present on all three tables.
    if low.count("auth.uid()") < 8:
        problems.append("owner policies are not auth.uid()-scoped")
    # Timeline: the view gains a booking branch keyed by the read
    # model's own rule, original branches intact, fail-loud guard set.
    if "create or replace view public.person_timeline_events" not in low:
        problems.append("timeline view extension missing")
    for kind in ("'wall_note'", "'mail_message'", "'invite'", "'booking'"):
        if kind not in low:
            problems.append(f"timeline event kind {kind} missing")
    if "resolve_person_key(b.owner_alias" not in low:
        problems.append("booking branch not keyed by resolve_person_key")
    if "booking_timeline_dependency_missing" not in low:
        problems.append("fail-loud timeline dependency guard missing")
    # Calendar sync is a placeholder, stated — never a built claim.
    if "'not_connected'" not in low:
        problems.append("calendar_sync_state placeholder missing")
    return problems


def test_migration_parses_and_audit_is_clean():
    sql = _sql()
    assert len(pglast.parse_sql(sql)) > 0
    assert audit(sql) == []


def test_negative_controls_doctored_sql_fails_the_audit():
    sql = _sql()
    no_index = re.sub(
        r"create unique index if not exists bookings_one_confirmed_per_slot"
        r".*?where status = 'confirmed';",
        "", sql, flags=re.S,
    )
    assert audit(no_index), "removing the slot index must fail the audit"
    leaky = sql + (
        "\ncreate policy leak on public.bookings for select to anon"
        " using (true);\n"
    )
    assert audit(leaky), "an anon select policy must fail the audit"
    no_timeline = sql.replace("'booking'", "'meeting'")
    assert audit(no_timeline), "losing the booking branch must fail the audit"


def test_ledger_entry_matches_the_migrations_real_bytes():
    raw = MIGRATION.read_bytes()
    canon = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    entries = [
        e for e in ledger["production_applied"] + ledger["pending"]
        if e["version"] == "20261022210000"
    ]
    assert len(entries) == 1, "booking_v1 must be registered exactly once"
    entry = entries[0]
    assert entry["name"] == "booking_v1"
    assert entry["path"] == "supabase/migrations/20261022210000_booking_v1.sql"
    assert entry["status"] == "PENDING_REVIEW_NOT_PRODUCTION_APPLIED"
    assert entry["sha256"] == hashlib.sha256(canon.encode("utf-8")).hexdigest()
    assert entry["bytes"] == len(raw)
    assert entry["statement_count"] == len(pglast.parse_sql(canon))


def test_core_mirror_uses_the_migrations_own_words():
    core = CORE.read_text(encoding="utf-8")
    for reason in ("outside_availability", "slot_taken"):
        assert reason in core, f"core mirror lost the {reason} refusal"
    # One slug grammar in both layers.
    assert "^[a-z0-9][a-z0-9-]{1,62}$" in _sql()
    assert "[a-z0-9][a-z0-9-]{1,62}" in core
    # The reminder thread convention is shared, not invented twice.
    assert "booking-" in core
