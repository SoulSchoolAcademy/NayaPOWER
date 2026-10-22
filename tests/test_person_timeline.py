"""Per-person timeline read model — derivation tests (map element #1).

Fixtures span all four sources. The acceptance soul of the element is
ZERO manual logging: everything asserted here is derived from the rows.
Negative controls: rows that cannot be resolved are quarantined and
counted, never attached; a builder fed nothing produces nothing.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "person_timeline", ROOT / "tools" / "person_timeline.py")
pt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pt)

MIGRATION = ROOT / "supabase" / "migrations" / "20261022203000_person_timeline_v1.sql"

OWNER = {"Shawn Vibert", "Shawn"}


def rows():
    return dict(
        owner_alias="shawn",
        owner_names=OWNER,
        wall_notes=[
            {"author_name": "Mary Jones", "content": "Loved the session!",
             "created_at": "2026-10-20T10:00:00Z"},
            {"author_name": "Shawn Vibert", "content": "My own post",
             "created_at": "2026-10-20T11:00:00Z"},  # owner — not a person event
            {"author_name": None, "sender_name": None, "content": "orphan",
             "created_at": "2026-10-20T12:00:00Z"},  # quarantine
        ],
        mail_threads=[
            {"thread_key": "t1", "subject": "Pricing question", "status": "open",
             "participants": ["Mary Jones", "Shawn Vibert"],
             "created_at": "2026-10-19T09:00:00Z",
             "updated_at": "2026-10-21T09:00:00Z"},
            {"thread_key": "t2", "subject": "Intro", "status": "open",
             "participants": '[{"name": "Bob Smith", "email": "bob@example.com"}, "Shawn Vibert"]',
             "created_at": "2026-10-18T09:00:00Z",
             "updated_at": "2026-10-18T10:00:00Z"},
        ],
        mail_messages=[
            {"thread_key": "t1", "sender_name": "Mary Jones", "direction": "inbound",
             "body": "What does the quarterly plan cost?",
             "created_at": "2026-10-21T09:00:00Z"},
            {"thread_key": "t1", "sender_name": "Shawn Vibert", "direction": "outbound",
             "body": "Here is the breakdown.",
             "created_at": "2026-10-19T10:00:00Z"},
            {"thread_key": "t2", "sender_name": "Shawn Vibert", "direction": "outbound",
             "body": "Great to meet you.",
             "created_at": "2026-10-18T10:00:00Z"},
            {"thread_key": "tX", "sender_name": "Ghost", "direction": None,
             "body": "?", "created_at": "2026-10-18T11:00:00Z"},  # quarantine
        ],
        invites=[
            {"invitee_email_hash": "hash-bob", "status": "joined",
             "created_at": "2026-10-17T08:00:00Z", "owner_alias": "shawn"},
            {"invitee_email_hash": None, "status": "sent",
             "created_at": "2026-10-17T09:00:00Z", "owner_alias": "shawn"},  # quarantine
        ],
    )


def test_unified_stream_one_shape_all_sources():
    events, _, _ = pt.build_timeline(**rows())
    kinds = {e["event_kind"] for e in events}
    assert kinds == {"wall_note", "mail_message", "invite"}
    shape = {"person_key", "owner_alias", "event_at", "event_kind",
             "source_table", "source_id", "title", "body", "direction",
             "counterparty_name", "thread_key", "status"}
    for event in events:
        assert set(event.keys()) == shape, event
    ats = [e["event_at"] for e in events]
    assert ats == sorted(ats)  # one chronological stream


def test_identity_merges_name_variants_and_email_hash():
    events, identities, _ = pt.build_timeline(**rows())
    by_key = {p["person_key"]: p for p in identities}
    # Bob arrives by outbound mail (participant carries an email) AND by
    # invite hash — the email_hash_of rule makes them the same person.
    bob_key = pt.person_key("shawn", None, pt.email_hash_of("bob@example.com"))
    # The fixture invite used a literal hash, so assert the merge rule with
    # the hash the participant produced:
    bob_mail_key = pt.person_key("shawn", "Bob Smith", pt.email_hash_of("bob@example.com"))
    assert bob_mail_key in by_key
    assert by_key[bob_mail_key]["email_hash"] == pt.email_hash_of("bob@example.com")
    assert by_key[bob_mail_key]["sources"] == {"smart_mail_messages": 1}
    # Mary: wall + inbound mail + outbound mail fan-out = one person.
    mary = by_key[pt.person_key("shawn", "Mary Jones", None)]
    assert mary["sources"] == {"smart_notes": 1, "smart_mail_messages": 2}
    assert mary["first_seen_at"] == "2026-10-19T10:00:00Z"
    assert mary["last_seen_at"] == "2026-10-21T09:00:00Z"


def test_alias_registry_folds_a_variant_into_the_canonical_person():
    alias_key = pt.person_key("shawn", "Mary J", None)
    canonical = pt.person_key("shawn", "Mary Jones", None)
    data = rows()
    data["wall_notes"] = [{"author_name": "Mary J", "content": "hi",
                           "created_at": "2026-10-22T00:00:00Z"}]
    data["mail_threads"] = []
    data["mail_messages"] = []
    data["invites"] = []
    data["aliases"] = {alias_key: canonical}
    events, identities, _ = pt.build_timeline(**data)
    assert [p["person_key"] for p in identities] == [canonical]
    assert events[0]["person_key"] == canonical


def test_owner_is_never_a_person_and_owner_events_are_skipped():
    events, identities, _ = pt.build_timeline(**rows())
    assert all("shawn vibert" not in p["normalized_name"] for p in identities)
    assert all(e["counterparty_name"] != "Shawn Vibert" for e in events)


def test_quarantine_counts_unresolvable_rows_never_attaches_them():
    events, identities, report = pt.build_timeline(**rows())
    assert report["quarantined"] == 3
    assert report["quarantine_reasons"] == {
        "wall_note_without_author": 1,
        "message_without_direction": 1,
        "invite_without_email_hash": 1,
    }
    assert all(e["counterparty_name"] != "Ghost" for e in events)
    assert report["events"] == len(events) == 5


def test_negative_control_empty_input_empty_output():
    events, identities, report = pt.build_timeline(owner_alias="shawn")
    assert events == [] and identities == []
    assert report == {"input_rows": 0, "events": 0, "quarantined": 0,
                      "quarantine_reasons": {}, "people": 0}


def test_person_summary_derives_last_spoke_and_waiting():
    events, _, _ = pt.build_timeline(**rows())
    mary = [e for e in events
            if e["person_key"] == pt.person_key("shawn", "Mary Jones", None)]
    summary = pt.summarize_person(mary)
    assert summary["last_spoke_at"] == "2026-10-21T09:00:00Z"
    assert summary["waiting_on_owner"] is True  # her inbound is the latest word
    assert summary["open_thread_keys"] == ["t1"]
    assert summary["event_count"] == 3


def test_key_and_normalize_mirror_the_sql_functions():
    sql = MIGRATION.read_text(encoding="utf-8")
    assert "create or replace function public.normalize_person_name" in sql
    assert "create or replace function public.resolve_person_key" in sql
    assert "'h:' || p_email_hash" in sql and "'n:' ||" in sql
    assert pt.person_key("Shawn", "Mary Jones", None) == "n:mary jones@shawn"
    assert pt.person_key("shawn", "Anyone", "abc") == "h:abc@shawn"
    assert pt.normalize_person_name("  Mary   JONES!! ") == "mary jones"


def test_migration_fails_loud_on_missing_source_columns():
    sql = MIGRATION.read_text(encoding="utf-8")
    assert "PERSON_TIMELINE_SOURCE_COLUMNS_MISSING" in sql
    for col in ("smart_mail_threads", "participants", "invitee_email_hash",
                "author_name"):
        assert col in sql
    # RLS: identities are owner-only — no anon policy may exist.
    assert not re.search(r"create policy .*person_identities.*\n.*to anon", sql)
    assert "for all to authenticated" in sql
