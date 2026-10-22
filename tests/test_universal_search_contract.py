"""Universal search service — contract tests (map element #12, step 13).

The acceptance soul of this element is ISOLATION: search returns a
person's own objects and never anyone else's. There is no live database
in the test estate, so the contract is pinned structurally on the
migration itself — the same standard the Phase-0 contract tests hold:
if any assertion here could silently rot (a dropped owner predicate, a
widened grant, an owner parameter creeping into the signature), this
suite fails before the dock ever sees the PR.

Negative controls are first-class: no-identity fails closed, anon holds
no grant, the query cannot widen its own LIKE match, and the flagship
source guard fails loud instead of searching an empty shape.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pglast

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20261022210000_universal_search_v1.sql"
LEDGER = ROOT / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json"
MODULE = ROOT / "HUB" / "app" / "js" / "naya-search.js"
INDEX = ROOT / "HUB" / "app" / "index.html"

SQL = MIGRATION.read_text(encoding="utf-8")
SQL_LOWER = SQL.lower()


def _lf_sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode()).hexdigest()


def test_migration_parses_and_ledger_entry_is_recomputed_truth():
    statements = pglast.parse_sql(SQL)
    assert len(statements) >= 5  # guard, index, score fn, service, grants
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    entries = [e for e in ledger["pending"]
               if e["version"] == "20261022210000"]
    assert len(entries) == 1, "exactly one ledger entry for this migration"
    (entry,) = entries
    assert entry["name"] == "universal_search_v1"
    assert entry["path"] == "supabase/migrations/20261022210000_universal_search_v1.sql"
    assert entry["status"] == "PENDING_REVIEW_NOT_PRODUCTION_APPLIED"
    # Recomputed from the actual file — never copied on trust.
    assert entry["sha256"] == _lf_sha(SQL)
    assert entry["statement_count"] == len(statements)
    assert entry["bytes"] == len(MIGRATION.read_bytes())


def test_service_signature_takes_no_owner_parameter():
    m = re.search(
        r"create or replace function public\.search_universal\((.*?)\)",
        SQL, re.S)
    assert m, "search_universal is defined"
    params = m.group(1).lower()
    assert "p_query" in params and "p_limit" in params
    for forbidden in ("owner", "alias", "uid", "user"):
        assert forbidden not in params, (
            f"client-supplied {forbidden!r} parameter would let a caller "
            "name someone else's corpus — identity must come from auth.uid() only")


def test_identity_comes_from_auth_uid_and_fails_closed():
    assert "v_uid uuid := auth.uid()" in SQL
    # No identity -> the function returns before any source is read.
    guard = re.search(r"if v_uid is null then\s*return;", SQL)
    assert guard, "null identity must fail closed"
    first_source = SQL.index("from public.person_identities")
    assert guard.start() < first_source


def test_security_definer_with_pinned_search_path():
    m = re.search(
        r"function public\.search_universal.*?security definer\s*"
        r"set search_path = public", SQL, re.S)
    assert m, "SECURITY DEFINER requires a pinned search_path"


def test_grants_authenticated_only_never_anon():
    assert ("grant execute on function public.search_universal(text, integer)"
            "\n  to authenticated;") in SQL
    assert ("revoke all on function public.search_universal(text, integer)"
            " from public;") in SQL
    # Anon must appear nowhere near a grant on this function.
    for m in re.finditer(r"grant execute on function public\.search_universal"
                         r"\([^)]*\)\s*(?:\n\s*)?to ([^;]+);", SQL):
        assert "anon" not in m.group(1)


def test_every_source_branch_is_owner_scoped():
    # (source table, the owner predicate its branch must carry)
    branches = [
        ("public.person_identities pi", "pi.owner_id = v_uid"),
        ("public.smart_notes n", "n.owner_alias = any (v_aliases)"),
        ("public.naya_notes nn", "nn.owner_id = v_uid"),
        ("public.smart_mail_threads t", "t.owner_alias = any (v_aliases)"),
        ("public.smart_links l", "l.owner_id = v_uid"),
    ]
    for table, predicate in branches:
        idx = SQL.index("from " + table)
        window = SQL[idx:idx + 700]
        assert predicate in window, f"{table} branch lacks predicate {predicate!r}"
    # The alias set itself derives only from rows the caller owns by uid.
    alias_block = SQL[SQL.index("select coalesce(array_agg"):SQL.index("return query")]
    assert alias_block.count("owner_id = v_uid") == 3
    assert "p_" not in alias_block.replace("public.", ""), \
        "alias derivation must not read any function parameter"


def test_query_cannot_widen_its_own_match():
    # search_score escapes LIKE metacharacters in the query before any
    # pattern is built from it.
    score_fn = SQL[SQL.index("function public.search_score"):
                   SQL.index("function public.search_universal")]
    assert "replace(replace(replace(" in score_fn
    assert "'%', '\\%'" in score_fn and "'_', '\\_'" in score_fn
    assert "escape '\\'" in score_fn


def test_ranking_is_one_definition_with_the_documented_ladder():
    score_fn = SQL[SQL.index("function public.search_score"):
                   SQL.index("function public.search_universal")]
    for rung in ("100::double precision", "80::double precision",
                 "60::double precision", "40::double precision"):
        assert rung in score_fn, f"ranking rung {rung} missing"
    # Every branch scores through the one definition.
    assert SQL.count("public.search_score(") >= 8


def test_fail_loud_guard_covers_the_flagship_columns():
    assert "UNIVERSAL_SEARCH_SOURCE_COLUMNS_MISSING" in SQL
    for col in ("owner_alias", "content", "author_name", "sender_name",
                "subject", "participants", "thread_key", "updated_at"):
        assert f"'{col}'" in SQL, f"guard must require {col}"
    guard_end = SQL.index("end $$;")
    service_start = SQL.index("function public.search_universal")
    assert guard_end < service_start, "guard runs before the service exists"


def test_result_shape_carries_an_action_for_every_type():
    for kind in ("open_person", "open_room", "open_url"):
        assert f"'{kind}'" in SQL, f"action kind {kind} missing"
    for obj_type in ("person", "smart_note", "naya_note",
                     "mail_thread", "smart_link"):
        assert f"'{obj_type}'" in SQL, f"object type {obj_type} missing"


def test_module_and_hub_wiring_exist_and_stay_in_their_lane():
    module = MODULE.read_text(encoding="utf-8")
    for symbol in ("parseVoiceIntent", "rankResults", "createStore",
                   "mountPalette", "installHotkey", "NayaSearch"):
        assert symbol in module, f"module is missing {symbol}"
    index = INDEX.read_text(encoding="utf-8")
    assert '<script src="js/naya-search.js"></script>' in index
    assert "NayaSearch.mountPalette" in index
    assert "NayaSearch.installHotkey" in index
    # The chassis Ask-Naya box (R.search) is a different surface and is
    # NOT rewired by this build — its call site must still be intact.
    assert "R.search(searchInput.value.trim()" in index
