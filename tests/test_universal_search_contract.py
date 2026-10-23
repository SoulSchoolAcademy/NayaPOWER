"""Universal search service — contract tests (map element #12, step 13).

The acceptance soul of this element is ISOLATION: search returns a
person's own objects and never anyone else's. There is no live database
in the test estate, so the contract is pinned structurally on the
migrations themselves — the same standard the Phase-0 contract tests
hold: if any assertion here could silently rot (a dropped owner
predicate, a widened grant, an owner parameter creeping into the
signature), this suite fails before the dock ever sees the PR.

Negative controls are first-class: no-identity fails closed, anon holds
no grant, the query cannot widen its own LIKE match, and the flagship
source guard fails loud instead of searching an empty shape.

CURE ROUND 4 (2026-10-23) — the alias-poisoning fix. The Tier-A card
(6354152883, 8.0 NOT APPROVED) proved the original derivation unsafe:
search_universal derived the caller's alias set from free-text
owner_alias on rows the caller owns by uid, so ONE permitted insert
claiming a victim's alias leaked the victim's alias-keyed rows. The
cure, pinned below:
  * the alias set derives ONLY from the server-controlled binding
    public.owner_alias_claims (migration 20261022220000), whose final
    search_universal definition supersedes the one in 20261022214500;
  * a first-claim guard (trigger) on all three alias-source tables
    refuses any write whose alias another owner claimed first;
  * a behavioral harness, translated line-by-line from the cured SQL
    the way the VERIFY lane modeled it, proves the poisoning scenario
    returns ZERO victim rows while legitimate alias search still works.
The service's FINAL definition lives in the binding migration; tests
about the service read that definition (SVC below), never the
superseded one.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import pglast

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20261022214500_universal_search_v1.sql"
BINDING = ROOT / "supabase" / "migrations" / "20261022220000_alias_binding_v1.sql"
LEDGER = ROOT / "supabase" / "PRODUCTION-MIGRATION-LEDGER-V1.json"
MODULE = ROOT / "HUB" / "app" / "js" / "naya-search.js"
INDEX = ROOT / "HUB" / "app" / "index.html"

SQL = MIGRATION.read_text(encoding="utf-8")
SQL_LOWER = SQL.lower()
BIND = BINDING.read_text(encoding="utf-8")
# The FINAL search_universal definition: the one the binding migration
# installs last (migrations apply in version order).
SVC = BIND[BIND.index("create or replace function public.search_universal"):]


def _lf_sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode()).hexdigest()


def _ledger_entry(version: str) -> dict:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    entries = [e for e in ledger["pending"] if e["version"] == version]
    assert len(entries) == 1, f"exactly one ledger entry for {version}"
    return entries[0]


def test_migration_parses_and_ledger_entry_is_recomputed_truth():
    statements = pglast.parse_sql(SQL)
    assert len(statements) >= 5  # guard, index, score fn, service, grants
    entry = _ledger_entry("20261022214500")
    assert entry["name"] == "universal_search_v1"
    assert entry["path"] == "supabase/migrations/20261022214500_universal_search_v1.sql"
    assert entry["status"] == "PENDING_REVIEW_NOT_PRODUCTION_APPLIED"
    # Recomputed from the actual file — never copied on trust.
    assert entry["sha256"] == _lf_sha(SQL)
    assert entry["statement_count"] == len(statements)
    assert entry["bytes"] == len(MIGRATION.read_bytes())


def test_binding_migration_parses_and_ledger_entry_is_recomputed_truth():
    statements = pglast.parse_sql(BIND)
    assert len(statements) >= 15  # claims, guard, rpc, backfill, triggers, service
    entry = _ledger_entry("20261022220000")
    assert entry["name"] == "alias_binding_v1"
    assert entry["path"] == "supabase/migrations/20261022220000_alias_binding_v1.sql"
    assert entry["status"] == "PENDING_REVIEW_NOT_PRODUCTION_APPLIED"
    assert entry["sha256"] == _lf_sha(BIND)
    assert entry["statement_count"] == len(statements)
    assert entry["bytes"] == len(BINDING.read_bytes())


def test_pending_versions_are_unique_and_booking_keeps_its_version():
    # Cure round 4 renumbered universal_search off 20261022210000,
    # which main's booking migration (PR #2957) already owns. Two
    # pending migrations may never share a version again.
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    versions = [e["version"] for e in ledger["pending"]]
    assert len(versions) == len(set(versions)), "duplicate pending version"
    booking = _ledger_entry("20261022210000")
    assert booking["name"] == "booking_v1"


def test_service_signature_takes_no_owner_parameter():
    m = re.search(
        r"create or replace function public\.search_universal\((.*?)\)",
        SVC, re.S)
    assert m, "search_universal is defined (final definition)"
    params = m.group(1).lower()
    assert "p_query" in params and "p_limit" in params
    for forbidden in ("owner", "alias", "uid", "user"):
        assert forbidden not in params, (
            f"client-supplied {forbidden!r} parameter would let a caller "
            "name someone else's corpus — identity must come from auth.uid() only")


def test_identity_comes_from_auth_uid_and_fails_closed():
    assert "v_uid uuid := auth.uid()" in SVC
    # No identity -> the function returns before any source is read.
    guard = re.search(r"if v_uid is null then\s*return;", SVC)
    assert guard, "null identity must fail closed"
    first_source = SVC.index("from public.person_identities")
    assert guard.start() < first_source


def test_security_definer_with_pinned_search_path():
    m = re.search(
        r"function public\.search_universal.*?security definer\s*"
        r"set search_path = public", SVC, re.S)
    assert m, "SECURITY DEFINER requires a pinned search_path"


def test_grants_authenticated_only_never_anon():
    assert ("grant execute on function public.search_universal(text, integer)"
            "\n  to authenticated;") in SVC
    assert ("revoke all on function public.search_universal(text, integer)"
            " from public;") in SVC
    # Anon must appear nowhere near a grant on this function.
    for m in re.finditer(r"grant execute on function public\.search_universal"
                         r"\([^)]*\)\s*(?:\n\s*)?to ([^;]+);", SVC):
        assert "anon" not in m.group(1)


def test_every_source_branch_is_owner_scoped():
    # (source table, the owner predicate its branch must carry) — read
    # against the FINAL definition in the binding migration.
    branches = [
        ("public.person_identities pi", "pi.owner_id = v_uid"),
        ("public.smart_notes n", "lower(btrim(n.owner_alias)) = any (v_aliases)"),
        ("public.naya_notes nn", "nn.owner_id = v_uid"),
        ("public.smart_mail_threads t", "lower(btrim(t.owner_alias)) = any (v_aliases)"),
        ("public.smart_links l", "l.owner_id = v_uid"),
    ]
    for table, predicate in branches:
        idx = SVC.index("from " + table)
        window = SVC[idx:idx + 700]
        assert predicate in window, f"{table} branch lacks predicate {predicate!r}"


def test_alias_set_derives_from_the_binding_only():
    # The derivation block of the FINAL definition: from the alias
    # SELECT to the RETURN QUERY. It must read owner_alias_claims for
    # the caller's uid — and NONE of the three free-text source tables.
    deriv = SVC[SVC.index("select coalesce(array_agg"):SVC.index("return query")]
    assert "from public.owner_alias_claims c" in deriv
    assert "c.owner_id = v_uid" in deriv
    for table in ("public.person_identities", "public.naya_notes",
                  "public.smart_links"):
        assert f"from {table}" not in deriv, (
            f"alias derivation must never trust free-text rows in {table}")
    # The vulnerable union derivation must not survive anywhere in the
    # final definition.
    assert "select owner_alias as a" not in SVC
    assert "select owner_alias from public.naya_notes" not in SVC
    assert "select owner_alias from public.smart_links" not in SVC


def test_query_cannot_widen_its_own_match():
    # search_score escapes LIKE metacharacters in the query before any
    # pattern is built from it. (Defined in 20261022214500; the binding
    # migration does not redefine it.)
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
    # Every branch of the final definition scores through the one
    # definition.
    assert SVC.count("public.search_score(") >= 8


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
        assert f"'{kind}'" in SVC, f"action kind {kind} missing"
    for obj_type in ("person", "smart_note", "naya_note",
                     "mail_thread", "smart_link"):
        assert f"'{obj_type}'" in SVC, f"object type {obj_type} missing"


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


# ————— Cure round 4: the binding itself —————

def test_claims_table_is_server_controlled_and_write_locked():
    assert "create table if not exists public.owner_alias_claims" in BIND
    assert "alias_normalized text primary key" in BIND
    assert "owner_id uuid not null" in BIND
    assert "alter table public.owner_alias_claims enable row level security" in BIND
    # Exactly ONE policy on the claims table: select-own. No client
    # write path exists — claims are created only by definer code.
    claims_policies = re.findall(
        r"create policy (\w+)\s+on public\.owner_alias_claims", BIND)
    assert claims_policies == ["owner_alias_claims_owner_select"]
    select_policy = re.search(
        r"create policy owner_alias_claims_owner_select.*?for select"
        r" to authenticated\s*using \(owner_id = \(select auth\.uid\(\)\)\)",
        BIND, re.S)
    assert select_policy, "the one claims policy is select-own"
    # The internal claim operation is definer-run and ungranted.
    assert ("revoke all on function\n"
            "  public.bind_owner_alias_claim(text, uuid, text) from public;") in BIND


def test_first_claim_guard_arms_all_three_source_tables():
    for table in ("person_identities", "naya_notes", "smart_links"):
        pat = (r"create trigger owner_alias_bind\s+before insert or update"
               r" of owner_alias, owner_id\s+on public\." + table +
               r"\s+for each row execute function public\.bind_owner_alias\(\)")
        assert re.search(pat, BIND), f"guard trigger missing on {table}"
    guard = BIND[BIND.index("function public.bind_owner_alias()"):
                 BIND.index("function public.claim_my_alias")]
    # No owner -> no binding (null-owner rows claim nothing).
    assert "if new.owner_id is null or v_alias = '' then" in guard
    assert "return new;" in guard
    # Normalization is the same one the search match uses.
    assert "lower(btrim(coalesce(new.owner_alias, '')))" in guard
    assert "perform public.bind_owner_alias_claim(v_alias, new.owner_id," in guard
    # First-claim mechanics: insert-if-absent, then the holder must be
    # the writer's own uid or the write is refused.
    helper = BIND[BIND.index("function public.bind_owner_alias_claim"):
                  BIND.index("function public.bind_owner_alias()")]
    assert "on conflict (alias_normalized) do nothing" in helper
    assert "OWNER_ALIAS_ALREADY_CLAIMED" in helper
    assert "errcode = 'check_violation'" in helper


def test_claim_rpc_is_the_only_client_claim_path_and_fails_closed():
    start = BIND.index("function public.claim_my_alias")
    header = BIND[max(0, start - 200):start + 200]
    assert "security definer" in header
    rpc = BIND[start:]
    rpc = rpc[:rpc.index("$$;", rpc.index("begin"))]
    assert "v_uid uuid := auth.uid()" in rpc
    assert "OWNER_ALIAS_CLAIM_REQUIRES_AUTH" in rpc
    assert "if v_uid is null then" in rpc
    assert ("grant execute on function public.claim_my_alias(text)"
            " to authenticated;") in BIND
    for m in re.finditer(r"grant execute on function public\.claim_my_alias"
                         r"\([^)]*\)\s*(?:\n\s*)?to ([^;]+);", BIND):
        assert "anon" not in m.group(1)


def test_backfill_is_deterministic_first_claim_wins():
    backfill = BIND[BIND.index("insert into public.owner_alias_claims"):
                    BIND.index("drop trigger if exists owner_alias_bind")]
    assert "distinct on (x.alias_normalized)" in backfill
    assert "order by x.alias_normalized, x.created_at asc, x.owner_id asc" in backfill
    assert "'backfill'" in backfill
    for table in ("public.person_identities", "public.naya_notes",
                  "public.smart_links"):
        assert f"from {table}" in backfill


# ————— Cure round 4: the behavioral pinning harness —————
# A faithful model of the cured SQL, translated rule-by-rule the way
# the VERIFY lane modeled the original (receipt 6354152883). The
# structural tests above anchor the model to the SQL text: if the SQL
# loses the binding derivation or the guard, those tests fail, so the
# model below cannot silently diverge from what ships.

def _norm(alias: str) -> str:
    # lower(btrim(alias)) — the one normalization, used by the guard,
    # the claims table, and the flagship branch predicates.
    return alias.strip().lower()


def _score(field: str | None, query: str) -> float:
    # public.search_score's ladder on literal text (the SQL escapes
    # LIKE metacharacters so the query behaves as literal text).
    if field is None:
        return 0.0
    f, q = field.lower(), query.strip().lower()
    if q == "":
        return 0.0
    if f == q:
        return 100.0
    if f.startswith(q):
        return 80.0
    if (" " + q) in f:
        return 60.0
    if q in f:
        return 40.0
    return 0.0


class _ClaimRefused(Exception):
    pass


class _BindingModel:
    """bind_owner_alias_claim + the row guard + the cured derivation."""

    def __init__(self) -> None:
        self.claims: dict[str, str] = {}       # alias_normalized -> uid
        self.source_rows: list[dict] = []      # the three source tables
        self.smart_notes: list[dict] = []      # flagship (outside RLS)
        self.mail_threads: list[dict] = []     # flagship (outside RLS)

    def _bind(self, alias_norm: str, owner: str) -> None:
        # insert ... on conflict do nothing; then holder must be owner.
        self.claims.setdefault(alias_norm, owner)
        if self.claims[alias_norm] != owner:
            raise _ClaimRefused("OWNER_ALIAS_ALREADY_CLAIMED")

    def write_source_row(self, table: str, owner: str | None,
                         alias: str) -> None:
        # The BEFORE trigger: null owner / empty alias -> untouched;
        # otherwise the write routes through the binding FIRST (a
        # refused claim means the row is never written).
        if owner is not None and _norm(alias) != "":
            self._bind(_norm(alias), owner)
        self.source_rows.append(
            {"table": table, "owner_id": owner, "owner_alias": alias})

    def search_alias_branches(self, uid: str, query: str) -> list[dict]:
        # The cured derivation: aliases come from the claims table
        # ONLY; flagship branches match on the normalized alias.
        aliases = {a for a, o in self.claims.items() if o == uid}
        hits = []
        for n in self.smart_notes:
            if _norm(n["owner_alias"]) in aliases and max(
                    _score(n["content"], query),
                    _score(n.get("author_name"), query)) > 0:
                hits.append({"type": "smart_note", **n})
        for t in self.mail_threads:
            if _norm(t["owner_alias"]) in aliases and max(
                    _score(t["subject"], query),
                    _score(t["participants"], query)) > 0:
                hits.append({"type": "mail_thread", **t})
        return hits


def test_alias_poisoning_harness_zero_leak_and_legit_search_works():
    m = _BindingModel()
    victim, attacker = "uid-victim", "uid-attacker"
    # The victim binds their alias the ordinary way (a source row).
    m.write_source_row("naya_notes", victim, "Victim")
    # The victim's flagship rows, incl. a mixed-case alias variant.
    m.smart_notes.append({"owner_alias": "Victim",
                          "content": "VICTIM SECRET alpha payroll plans",
                          "author_name": "Victim"})
    m.mail_threads.append({"owner_alias": "victim",
                           "subject": "payroll alpha thread",
                           "participants": "victim, maria"})

    # ATTACK 1 — the card's exact scenario: one permitted insert in a
    # source table claiming the victim's alias. The guard refuses the
    # WRITE itself; the poisoned row never exists.
    try:
        m.write_source_row("naya_notes", attacker, "victim")
        raise AssertionError("guard must refuse a foreign alias claim")
    except _ClaimRefused:
        pass
    assert all(r["owner_id"] != attacker for r in m.source_rows)

    # ATTACK 2 — even if a poisoned row somehow existed in a source
    # table (a path the trigger cannot see), the cured derivation
    # reads claims only: the attacker's search still returns ZERO
    # victim rows on both alias-keyed branches.
    m.source_rows.append({"table": "smart_links", "owner_id": attacker,
                          "owner_alias": "victim"})  # bypass simulation
    for q in ("VICTIM SECRET", "alpha", "payroll"):
        hits = m.search_alias_branches(attacker, q)
        assert hits == [], f"attacker query {q!r} leaked {hits}"

    # LEGITIMATE — the victim's own search works, including the
    # case-variant flagship alias, on both alias-keyed branches.
    note_hits = m.search_alias_branches(victim, "VICTIM SECRET")
    assert [h["type"] for h in note_hits] == ["smart_note"]
    payroll = m.search_alias_branches(victim, "payroll")
    assert {h["type"] for h in payroll} == {"smart_note", "mail_thread"}

    # LEGITIMATE — the attacker binds and searches their OWN alias.
    m.write_source_row("smart_links", attacker, "attacker")
    m.smart_notes.append({"owner_alias": "Attacker",
                          "content": "attacker grocery list",
                          "author_name": "Attacker"})
    own = m.search_alias_branches(attacker, "grocery")
    assert [h["type"] for h in own] == ["smart_note"]
    # ...and the victim still cannot see the attacker's rows.
    assert m.search_alias_branches(victim, "grocery") == []
