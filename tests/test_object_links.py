"""Linked everything — data-model tests (map element #14 + #19, step 14).

The acceptance soul of the element is ONE OBJECT, MANY HOMES, NO COPIES:
a note filed under a person and a list is read from its own surface, the
person's home (timeline read model from PR #2946), and the list — and
all three reads resolve the SAME store row, proven by identity and by
edit-once-read-everywhere. Negative controls: cross-owner filings and
facts are refused; unfiling removes the link and never the object; a
13th fact is refused.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ol = _load("object_links")
pt = _load("person_timeline")

MIGRATION = ROOT / "supabase" / "migrations" / "20261022211500_object_links_v1.sql"

SHAWN = {"id": "u-shawn", "alias": "shawn"}
MARIA = {"id": "u-maria", "alias": "maria"}

MARY_KEY = pt.person_key("shawn", "Mary Jones", None)     # n:mary jones@shawn
MARIA_PERSON_KEY = pt.person_key("maria", "Tom Lee", None)  # maria's own person


def store() -> "ol.LinkStore":
    return ol.LinkStore(
        naya_notes=[
            {"id": "note-1", "owner_id": SHAWN["id"], "owner_alias": "shawn",
             "text": "Mary asked about quarterly pricing", "category": "Sales",
             "list_name": None, "created_at": "2026-10-21T08:00:00Z"},
            {"id": "note-2", "owner_id": MARIA["id"], "owner_alias": "maria",
             "text": "Maria's private note", "category": "General",
             "list_name": None, "created_at": "2026-10-21T08:30:00Z"},
        ],
        smart_links=[
            {"id": "link-1", "owner_id": SHAWN["id"], "owner_alias": "shawn",
             "name": "pricing", "target_url": "https://example.com/pricing",
             "active": True},
        ],
        persons=[
            {"person_key": MARY_KEY, "owner_id": SHAWN["id"],
             "owner_alias": "shawn", "display_name": "Mary Jones"},
            {"person_key": MARIA_PERSON_KEY, "owner_id": MARIA["id"],
             "owner_alias": "maria", "display_name": "Tom Lee"},
        ],
        smart_notes=[
            {"ref": "SN-0826", "owner_alias": "shawn",
             "content": "Have each other's back"},
        ],
        mail_threads=[
            {"thread_key": "t1", "owner_alias": "shawn",
             "subject": "Pricing question"},
        ],
        lists=[
            {"name": "Launch", "owner_alias": "shawn"},
            {"name": "Launch", "owner_alias": "maria"},  # same name, other owner
        ],
    )


def mary_timeline_events():
    events, _, _ = pt.build_timeline(
        owner_alias="shawn", owner_names={"Shawn Vibert"},
        wall_notes=[], invites=[],
        mail_threads=[{"thread_key": "t1", "subject": "Pricing question",
                       "participants": ["Mary Jones", "Shawn Vibert"],
                       "created_at": "2026-10-19T09:00:00Z",
                       "updated_at": "2026-10-21T09:00:00Z"}],
        mail_messages=[{"thread_key": "t1", "sender_name": "Mary Jones",
                        "direction": "inbound",
                        "body": "What does the quarterly plan cost?",
                        "created_at": "2026-10-21T09:00:00Z"}],
    )
    return events


def file_note_under_mary_and_launch(s: "ol.LinkStore"):
    s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                 subject=("naya_note", "note-1"), target=("person", MARY_KEY),
                 at="2026-10-21T10:00:00Z")
    s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                 subject=("naya_note", "note-1"), target=("list", "Launch"),
                 at="2026-10-21T10:05:00Z")


# ── The three-homes, no-copy proof ──────────────────────────────────────

def test_one_object_readable_from_three_homes_from_one_row_each():
    s = store()
    file_note_under_mary_and_launch(s)
    assert len(s.links) == 2 and len(s.stores["naya_notes"]) == 2

    own = s.read_object(("naya_note", "note-1"))                    # home 1: its surface
    person_home = s.person_home(actor_alias="shawn", person_key=MARY_KEY,
                                timeline_events=mary_timeline_events())
    filed = [e for e in person_home if e["home_kind"] == "filed_object"]
    assert len(filed) == 1                                          # home 2: the person
    in_list = s.filed_under(actor_alias="shawn", target=("list", "Launch"))
    assert len(in_list) == 1                                        # home 3: the list

    # NO COPIES: every home resolves the very same store row.
    assert filed[0]["object"] is own
    assert in_list[0] is own
    # The person's home ALSO carries her timeline events — one stream,
    # keyed by the timeline model's own person_key.
    kinds = [e["home_kind"] for e in person_home]
    assert kinds == ["timeline_event", "filed_object"]  # chronological merge
    assert person_home[0]["event"]["person_key"] == MARY_KEY

    # Edit once in the object's own store; every home reads the edit.
    own["text"] = "Mary asked about quarterly pricing — sent the deck"
    assert s.read_object(("naya_note", "note-1"))["text"].endswith("sent the deck")
    assert s.person_home(actor_alias="shawn", person_key=MARY_KEY,
                         timeline_events=[])[0]["object"]["text"].endswith("sent the deck")
    assert s.filed_under(actor_alias="shawn",
                         target=("list", "Launch"))[0]["text"].endswith("sent the deck")


def test_file_under_is_idempotent_and_homes_are_listed():
    s = store()
    first = s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                         subject=("smart_link", "link-1"),
                         target=("person", MARY_KEY), at="2026-10-21T10:00:00Z")
    again = s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                         subject=("smart_link", "link-1"),
                         target=("person", MARY_KEY), at="2026-10-21T11:00:00Z")
    assert again["id"] == first["id"] and len(s.links) == 1
    assert s.homes_of(actor_alias="shawn", obj=("smart_link", "link-1")) == [
        ("person", MARY_KEY)]


def test_every_subject_kind_files_and_thread_targets_work():
    s = store()
    s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                 subject=("smart_note", "SN-0826"), target=("person", MARY_KEY))
    s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                 subject=("naya_note", "note-1"), target=("mail_thread", "t1"))
    s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                 subject=("person", MARY_KEY), target=("list", "Launch"))
    assert s.filed_under(actor_alias="shawn", target=("mail_thread", "t1"))[0]["id"] == "note-1"
    assert s.filed_under(actor_alias="shawn", target=("list", "Launch"))[0]["person_key"] == MARY_KEY


# ── Negative controls: ownership ────────────────────────────────────────

def test_cross_owner_subject_is_refused():
    s = store()
    with pytest.raises(ol.OwnershipError):
        s.file_under(actor_id=MARIA["id"], actor_alias="maria",
                     subject=("naya_note", "note-1"),  # shawn's note
                     target=("person", MARIA_PERSON_KEY))
    assert s.links == []


def test_cross_owner_target_person_is_refused():
    s = store()
    with pytest.raises(ol.OwnershipError):
        s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                     subject=("naya_note", "note-1"),
                     target=("person", MARIA_PERSON_KEY))  # maria's person
    assert s.links == []


def test_same_list_name_under_another_owner_is_not_yours():
    s = store()
    # Maria files her own note under HER "Launch" — resolves to her row,
    # never to shawn's same-named list; shawn's list stays empty of it.
    s.file_under(actor_id=MARIA["id"], actor_alias="maria",
                 subject=("naya_note", "note-2"), target=("list", "Launch"))
    assert s.filed_under(actor_alias="shawn", target=("list", "Launch")) == []
    assert [n["id"] for n in s.filed_under(
        actor_alias="maria", target=("list", "Launch"))] == ["note-2"]


def test_unfile_removes_the_link_never_the_object():
    s = store()
    file_note_under_mary_and_launch(s)
    assert s.unfile(actor_id=SHAWN["id"], actor_alias="shawn",
                    subject=("naya_note", "note-1"),
                    target=("person", MARY_KEY)) is True
    # The object is untouched and still readable from its own surface
    # and its remaining home.
    assert s.read_object(("naya_note", "note-1"))["text"].startswith("Mary asked")
    assert s.filed_under(actor_alias="shawn", target=("list", "Launch"))
    assert s.person_home(actor_alias="shawn", person_key=MARY_KEY,
                         timeline_events=[]) == []
    # Unfiling what is not filed is a clean False, and maria cannot
    # unfile shawn's link (it is not hers to remove).
    assert s.unfile(actor_id=SHAWN["id"], actor_alias="shawn",
                    subject=("naya_note", "note-1"),
                    target=("person", MARY_KEY)) is False
    assert s.unfile(actor_id=MARIA["id"], actor_alias="maria",
                    subject=("naya_note", "note-1"),
                    target=("list", "Launch")) is False
    assert len(s.links) == 1


def test_unknown_kinds_and_missing_objects_are_refused():
    s = store()
    with pytest.raises(ol.UnknownKindError):
        s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                     subject=("widget", "x"), target=("person", MARY_KEY))
    with pytest.raises(ol.UnknownKindError):
        s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                     subject=("naya_note", "note-1"), target=("smart_note", "SN-0826"))
    with pytest.raises(ol.ObjectNotFoundError):
        s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                     subject=("naya_note", "no-such-note"),
                     target=("person", MARY_KEY))
    with pytest.raises(ol.ObjectLinkError):
        s.file_under(actor_id=SHAWN["id"], actor_alias="shawn",
                     subject=("person", MARY_KEY), target=("person", MARY_KEY))


# ── Owner-named facts (element #19) ─────────────────────────────────────

def test_facts_ride_the_same_model_plain_and_owner_named():
    s = store()
    s.set_fact(actor_id=SHAWN["id"], actor_alias="shawn",
               obj=("person", MARY_KEY), key="Ticket Tier", value="gold")
    s.set_fact(actor_id=SHAWN["id"], actor_alias="shawn",
               obj=("person", MARY_KEY), key="dietary needs", value="none")
    facts = s.facts_for(actor_alias="shawn", obj=("person", MARY_KEY))
    assert facts == {"ticket tier": "gold", "dietary needs": "none"}
    # Upsert by normalized key: same fact, new value, still one row.
    s.set_fact(actor_id=SHAWN["id"], actor_alias="shawn",
               obj=("person", MARY_KEY), key=" ticket   tier ", value="platinum")
    assert s.facts_for(actor_alias="shawn",
                       obj=("person", MARY_KEY))["ticket tier"] == "platinum"
    assert len([f for f in s.facts if f["object_ref"] == MARY_KEY]) == 2


def test_fact_by_a_non_owner_is_refused():
    s = store()
    with pytest.raises(ol.OwnershipError):
        s.set_fact(actor_id=MARIA["id"], actor_alias="maria",
                   obj=("naya_note", "note-1"), key="stolen", value="x")
    assert s.facts == []


def test_the_thirteenth_fact_is_refused_by_name():
    s = store()
    for i in range(ol.FACT_LIMIT):
        s.set_fact(actor_id=SHAWN["id"], actor_alias="shawn",
                   obj=("naya_note", "note-1"), key=f"fact {i}", value="v")
    with pytest.raises(ol.FactLimitError):
        s.set_fact(actor_id=SHAWN["id"], actor_alias="shawn",
                   obj=("naya_note", "note-1"), key="one too many", value="v")
    # …but updating an existing fact at the limit is fine.
    s.set_fact(actor_id=SHAWN["id"], actor_alias="shawn",
               obj=("naya_note", "note-1"), key="fact 0", value="updated")
    assert s.facts_for(actor_alias="shawn",
                       obj=("naya_note", "note-1"))["fact 0"] == "updated"


# ── SQL contract audit (migration <-> module drift, RLS shape) ────────

def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def _check_kinds(sql: str, constraint: str) -> set[str]:
    block = re.search(rf"{constraint}\s+check \(\w+ in \(([^)]*)\)\)", sql)
    assert block, f"{constraint} check not found"
    return set(re.findall(r"'([^']+)'", block.group(1)))


def audit(sql: str) -> list[str]:
    """Return the list of contract violations in an object-links migration."""
    problems: list[str] = []
    low = sql.lower()
    for table in ("object_links", "object_facts"):
        if f"create table if not exists public.{table}" not in low:
            problems.append(f"missing table {table}")
        if f"alter table public.{table} enable row level security" not in low:
            problems.append(f"RLS not enabled on {table}")
        for verb in ("select", "insert", "update", "delete"):
            if f"create policy {table}_owner_{verb} on public.{table}" not in low:
                problems.append(f"owner {verb} policy missing on {table}")
    # Every owner policy must carry the owner scope in its OWN block.
    # A single global string check passes when exactly one policy is
    # weakened (VERIFY sabotage 3 on PR #2954: object_links_owner_delete
    # -> using (true) left this suite 14/14 green), so pin it per policy.
    for m in re.finditer(
            r"create policy (\w+) on public\.(object_links|object_facts)\b[^;]*;",
            low):
        block = m.group(0)
        clauses = block.count("using (") + block.count("with check (")
        scopes = block.count("owner_id = (select auth.uid())")
        if scopes < clauses:
            problems.append(
                f"policy {m.group(1)} on {m.group(2)} is not "
                "owner-scoped by auth.uid() in every clause")
    if "owner_id = (select auth.uid())" not in low:
        problems.append("policies are not owner-scoped by auth.uid()")
    # Links and facts are private: NO policy may name anon, on either table.
    for m in re.finditer(r"create policy \w+ on public\.(object_links|object_facts)\b[^;]*?to anon", low):
        problems.append(f"anon policy on {m.group(1)} is forbidden")
    if not re.search(
            r"create or replace function public\.file_object_under\(.*?security definer",
            low, re.S):
        problems.append("file_object_under security-definer operation missing")
    if "file_object_under_target_not_owned" not in low:
        problems.append("cross-owner target refusal missing")
    if "file_object_under_subject_not_owned" not in low:
        problems.append("cross-owner subject refusal missing")
    if "grant execute on function public.file_object_under" not in low:
        problems.append("authenticated execute grant missing")
    if re.search(r"grant execute on function public\.file_object_under\([^)]*\) to anon", low):
        problems.append("anon execute on file_object_under is forbidden")
    if "object_facts_guard_limit" not in low or "object_fact_limit_reached" not in low:
        problems.append("fact limit guard missing")
    if "create unique index if not exists object_links_unique" not in low:
        problems.append("link uniqueness index missing")
    if "object_links_source_tables_missing" not in low:
        problems.append("fail-loud source check missing")
    # Kind lists must match the service module exactly (drift = failure).
    if _check_kinds(sql, "object_links_subject_kind") != set(ol.SUBJECT_KINDS):
        problems.append("subject kinds drifted from tools/object_links.py")
    if _check_kinds(sql, "object_links_target_kind") != set(ol.TARGET_KINDS):
        problems.append("target kinds drifted from tools/object_links.py")
    if _check_kinds(sql, "object_facts_object_kind") != set(ol.SUBJECT_KINDS):
        problems.append("fact object kinds drifted from tools/object_links.py")
    return problems


def test_migration_satisfies_the_contract():
    assert audit(_sql()) == []


def test_negative_control_doctored_sql_fails_the_audit():
    weakened = _sql() + (
        "\ncreate policy bad on public.object_links for select to anon using (true);\n")
    assert any("anon" in p for p in audit(weakened))
    stripped = _sql().replace("security definer", "security invoker")
    assert any("security-definer" in p for p in audit(stripped))
    drifted = _sql().replace("'smart_note', 'naya_note'", "'smart_note', 'widget'")
    assert any("drifted" in p for p in audit(drifted))


def test_negative_control_single_policy_weakening_fails_the_audit():
    # VERIFY's sabotage 3 on PR #2954, as a standing control: weakening
    # ONE policy's scope must fail the audit even though the owner-scope
    # string survives in the other seven policies.
    weakened = _sql().replace(
        "create policy object_links_owner_delete on public.object_links\n"
        "  for delete to authenticated\n"
        "  using (owner_id = (select auth.uid()));",
        "create policy object_links_owner_delete on public.object_links\n"
        "  for delete to authenticated\n"
        "  using (true);")
    assert weakened != _sql()
    assert any("object_links_owner_delete" in p for p in audit(weakened))
    # An UPDATE policy carries the scope twice (using + with check);
    # weakening either single expression must also fail, by name.
    half_weakened = _sql().replace(
        "create policy object_links_owner_update on public.object_links\n"
        "  for update to authenticated\n"
        "  using (owner_id = (select auth.uid()))\n"
        "  with check (owner_id = (select auth.uid()));",
        "create policy object_links_owner_update on public.object_links\n"
        "  for update to authenticated\n"
        "  using (true)\n"
        "  with check (owner_id = (select auth.uid()));")
    assert half_weakened != _sql()
    assert any("object_links_owner_update" in p for p in audit(half_weakened))


def test_sql_parses_as_postgres_and_limit_matches():
    sql = _sql()
    assert f">= {ol.FACT_LIMIT}" in sql  # the trigger's cap mirrors the module
    try:
        import pglast
    except ImportError:  # local fallback: CI installs pglast (kernel-tests)
        import pytest as _pytest

        _pytest.skip("pglast not installed locally")
    statements = pglast.parse_sql(sql)
    assert len(statements) >= 20
