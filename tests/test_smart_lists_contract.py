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
# Exact column bounds the contract promises (char_length ceilings in the
# migration's CHECK constraints). The audit compares numbers, not
# presence: a cap silently widened is a weakening, not a detail.
BOUNDS = {"title": 200, "category": 80, "item_ref": 512, "label": 300, "text": 4000}
FENCE = "owner_id = (select auth.uid())"
PARENT_GUARD = "parent.owner_id = (select auth.uid())"


def _with_check_segment(stmt: str) -> str:
    """The part of a policy statement after WITH CHECK ('' if absent)."""
    return stmt.split("with check", 1)[1] if "with check" in stmt else ""


def _using_segment(stmt: str) -> str:
    """The part of a policy statement before WITH CHECK (its USING side)."""
    return stmt.split("with check", 1)[0]


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
            # Segment-aware fence: the uid fence must sit in the clause
            # that actually enforces it. A fence that survives only in
            # the USING side of an UPDATE while its WITH CHECK is a
            # tautology fences nothing on write — presence in the
            # statement as a whole is not proof.
            if op == "insert":
                if FENCE not in _with_check_segment(stmt):
                    problems.append(f"{name} does not fence on owner_id = auth.uid() in WITH CHECK")
            elif op == "update":
                if FENCE not in _using_segment(stmt):
                    problems.append(f"{name} does not fence on owner_id = auth.uid() in USING")
                if FENCE not in _with_check_segment(stmt):
                    problems.append(f"{name} does not fence on owner_id = auth.uid() in WITH CHECK")
            elif FENCE not in stmt:
                problems.append(f"{name} does not fence on owner_id = auth.uid()")
    # No anonymous or public path anywhere — lists are private, by design.
    for stmt in policies:
        if " to anon" in stmt or " to public" in stmt:
            problems.append(f"non-owner policy role present: {stmt[:80]}")
    # The six typed kinds, in the DB CHECK and in the module vocabulary.
    # Exact-set equality on the migration side: presence checks wave a
    # seventh kind through, and a seventh kind is a new object class the
    # store never audited.
    kind_block = re.search(r"smart_list_items_kind\s+check\s*\(\s*item_kind in \((.*?)\)\s*\)",
                           low, flags=re.S)
    if not kind_block:
        problems.append("item_kind CHECK constraint missing")
    else:
        found_kinds = set(re.findall(r"'([a-z_]+)'", kind_block.group(1)))
        if found_kinds != set(KINDS):
            problems.append(
                f"item kind set {sorted(found_kinds)} != the exact six {sorted(KINDS)}")
    module = MODULE.read_text(encoding="utf-8")
    for kind in KINDS:
        if f"'{kind}'" not in module:
            problems.append(f"item kind {kind!r} missing from the Hub module")
    # Exact numeric bounds: each promised ceiling, compared as a number.
    for column, want in BOUNDS.items():
        bound = re.search(rf"char_length\({column}\)\s*<=\s*(\d+)", low)
        if not bound:
            problems.append(f"bound on {column} missing (want char_length <= {want})")
        elif int(bound.group(1)) != want:
            problems.append(f"bound on {column} is {bound.group(1)}, want exactly {want}")
    # Foreign-key census: exactly one REFERENCES in the whole migration —
    # items -> lists, on delete cascade. Anything more is a path from a
    # list edit to an object row; anything less breaks membership cleanup.
    refs = re.findall(r"references public\.(\w+)\(id\)(?: on delete (\w+))?", low)
    if refs != [("smart_lists", "cascade")]:
        problems.append(f"foreign-key census {refs} != exactly items->lists cascade")
    if "references public.smart_lists(id) on delete cascade" not in low:
        problems.append("items->lists cascade missing")
    # Item writes must be fenced to the writer's own lists (parent
    # guard), inside the WITH CHECK segment that enforces the write.
    for op in ("insert", "update"):
        match = [p for p in policies
                 if f"create policy smart_list_items_owner_{op} on public.smart_list_items" in p]
        if match and PARENT_GUARD not in _with_check_segment(match[0]):
            problems.append(f"items {op} policy lacks the parent-list owner guard in WITH CHECK")
    # Deletion safety by construction: an item references an object by
    # plain (kind, ref) text — a foreign key to any object table would put
    # the object one cascade away from a list edit.
    for table in OBJECT_TABLES:
        if f"references public.{table}" in low:
            problems.append(f"items must not hold a foreign key to {table}")
    # Text/reference coherence shape check: BOTH branches must survive —
    # the text branch proves a text item carries text; the other proves a
    # reference item carries a reference. Presence of the constraint name
    # alone proves neither.
    if "smart_list_items_shape" not in low:
        problems.append("item shape CHECK (text vs reference) missing")
    else:
        if "(item_kind = 'text' and" not in low:
            problems.append("item shape CHECK lost its text branch")
        if "(item_kind <> 'text' and" not in low:
            problems.append("item shape CHECK lost its reference branch")
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


# --- Cure round 4: the five doctored variants the presence-only audit
# passed under the Tier-A adversarial review (VERIFY card 6354210676).
# Each weakens a Tier-A invariant while leaving every string the old
# audit searched for in place. The hardened audit must flag all five.

def test_negative_control_seventh_kind_fails_the_audit():
    doctored = _sql().replace("'smart_link', 'text'", "'smart_link', 'board', 'text'")
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("kind set" in p for p in problems), problems


def test_negative_control_text_cap_widened_fails_the_audit():
    doctored = _sql().replace("char_length(text) <= 4000", "char_length(text) <= 40000")
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("bound on text" in p for p in problems), problems


def test_negative_control_shape_text_branch_removed_fails_the_audit():
    doctored = _sql().replace(
        "(item_kind = 'text' and char_length(btrim(coalesce(text, ''))) > 0)\n    or ", "")
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("text branch" in p for p in problems), problems


def test_negative_control_update_with_check_tautology_fails_the_audit():
    doctored = _sql().replace(
        "create policy smart_lists_owner_update on public.smart_lists\n"
        "  for update to authenticated\n"
        "  using (owner_id = (select auth.uid()))\n"
        "  with check (owner_id = (select auth.uid()));",
        "create policy smart_lists_owner_update on public.smart_lists\n"
        "  for update to authenticated\n"
        "  using (owner_id = (select auth.uid()))\n"
        "  with check (owner_id = owner_id);",
    )
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("WITH CHECK" in p for p in problems), problems


def test_negative_control_category_bound_dropped_fails_the_audit():
    doctored = _sql().replace(
        ",\n  constraint smart_lists_category_bounded check (char_length(category) <= 80)", "")
    assert doctored != _sql()
    problems = audit(doctored)
    assert any("bound on category" in p for p in problems), problems


def test_sql_parses_as_postgres():
    try:
        import pglast
    except ImportError:  # local fallback: CI installs pglast (kernel-tests)
        import pytest

        pytest.skip("pglast not installed locally")
    statements = pglast.parse_sql(_sql())
    assert len(statements) == 24
