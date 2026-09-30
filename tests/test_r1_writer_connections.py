"""R1 writer contract: structural verification of the SQL migration.

The migration cannot be executed against a live database from here, so this
test verifies everything that can be verified without one:
  1. the migration parses with a real PostgreSQL parser (pglast);
  2. the vocabulary enforced by the SQL writers/guard matches the canonical
     22-type contract byte-for-byte;
  3. the intelligent_block_id hazard is fixed (Wave 2, Worker E): the
     promoted supersession writer's INSERT includes intelligent_block_id,
     mints it from the sequence when not supplied, and does NOT use the
     invalid '-v<N>' suffix the proposal suggested (it would violate the
     live ^IB-[0-9]{6}$ format check);
  4. every block-writing INSERT in the migration persists the connections
     projection.

DB execution (deploy-time) remains the chain owner's verification step and
is disclosed as such in the PR.
"""
import json
import re
from pathlib import Path

import pytest
from pglast import parse_sql

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20260930040000_r1_writer_connections_v1.sql"
SCHEMA = ROOT / "BRAIN" / "00-SPEC" / "BRAIN-MACHINE-CONTRACT-V1.schema.json"

CANONICAL_TYPES = [
    "DERIVED_FROM", "SUPPORTS", "CONTRADICTS", "DEPENDS_ON", "IMPLEMENTS", "GOVERNS",
    "AUTHORIZED_BY", "USED_BY", "CAUSED", "RESULTED_IN", "VERIFIED_BY", "LEARNED_FROM",
    "SUPERSEDES", "SUCCEEDS", "RELATED_TO", "CONTEXTUALIZES", "INVALIDATES", "REFINES",
    "CORRECTS", "ENABLES", "PRODUCES", "APPLIES_TO",
]


@pytest.fixture(scope="module")
def migration_text():
    return MIGRATION.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def schema_types():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return schema["$defs"]["relationshipType"]["enum"]


def test_migration_file_exists():
    assert MIGRATION.exists(), "R1 migration file must exist"


def test_migration_parses_with_postgres_parser(migration_text):
    stmts = parse_sql(migration_text)
    assert len(stmts) >= 15, f"expected the full migration body, got {len(stmts)} statements"


def test_vocabulary_matches_canonical_contract(schema_types):
    assert schema_types == CANONICAL_TYPES, "canonical contract must define exactly the 22 R1 types"


def _vocab_block(text):
    """Extract the IN-list vocabulary from the normalize function."""
    m = re.search(r"v_type not in \(\s*((?:'[^']+',?\s*)+)\)", text)
    assert m, "normalize function must contain a v_type not in (...) vocabulary list"
    return re.findall(r"'([^']+)'", m.group(1))


def test_normalize_function_enforces_canonical_vocabulary(migration_text, schema_types):
    assert "nayanet_normalize_block_connections" in migration_text
    assert _vocab_block(migration_text) == schema_types


def test_guard_trigger_enforces_canonical_vocabulary(migration_text, schema_types):
    assert "nayanet_intelligent_blocks_connections_guard" in migration_text
    blocks = re.findall(r"v_type not in \(\s*((?:'[^']+',?\s*)+)\)", migration_text)
    assert len(blocks) >= 2, "both normalize and guard must carry the vocabulary"
    for b in blocks:
        assert re.findall(r"'([^']+)'", b) == schema_types


def test_normalize_resolves_targets_owner_scoped(migration_text):
    assert "b.owner_id = p_owner_id" in migration_text, \
        "target resolution must be owner-scoped (prose/foreign targets fail closed)"
    assert "b.intelligent_block_id = v_target" in migration_text


def test_supersession_insert_includes_intelligent_block_id(migration_text):
    """The hazard: the pre-production writer omitted intelligent_block_id."""
    m = re.search(
        r"create or replace function public\.nayanet_supersede_intelligent_block\(.*?\)"
        r"\s*returns.*?as \$function\$(.*?)\$function\$;",
        migration_text, re.S,
    )
    assert m, "promoted supersession writer must exist"
    body = m.group(1)
    insert_cols = re.search(r"insert into public\.nayanet_intelligent_blocks\((.*?)\)\s*values", body, re.S)
    assert insert_cols, "supersession writer must INSERT the block row"
    cols = [c.strip() for c in insert_cols.group(1).split(",")]
    assert "intelligent_block_id" in cols, \
        "HAZARD NOT FIXED: supersession INSERT must include intelligent_block_id"


def test_supersession_mints_fresh_ib_id_from_sequence(migration_text):
    assert "nextval('public.nayanet_smart_note_ib_identity_seq')" in migration_text, \
        "supersession writer must mint a fresh IB id from the sequence when none is supplied"


def _strip_sql_comments(text):
    """Remove -- line comments and /* */ blocks for executable-code assertions."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"--[^\n]*", "", text)
    return text


def test_supersession_rejects_invalid_ib_id_suffix(migration_text):
    code = _strip_sql_comments(migration_text)
    assert "'-v'" not in code and '"-v"' not in code, \
        "the '-v<N>' suffix would violate the live ^IB-[0-9]{6}$ format check and must not appear in executable code"
    assert "!~ '^IB-[0-9]{6}$'" in code, \
        "explicit IB ids must be validated against the live format check"


def test_supersession_stamps_supersedes_edge_on_old_row(migration_text):
    assert "'SUPERSEDES'" in migration_text
    assert "superseded_by_block_id=p_new_block_id" in migration_text.replace(" ", "")
    assert "connections=public.nayanet_normalize_block_connections(" in migration_text.replace(" ", ""), \
        "old row update must append the SUPERSEDES edge through normalization"


def test_supersession_writes_canonical_relationship_row(migration_text):
    assert "insert into public.nayanet_brain_relationships" in migration_text, \
        "ONE GRAPH: the canonical edge row must be written atomically with the projection"


def test_upsert_writer_persists_connections(migration_text):
    m = re.search(
        r"create or replace function public\.nayanet_upsert_intelligent_block_from_smart_note\(.*?\)"
        r"\s*returns.*?as \$function\$(.*?)\$function\$;",
        migration_text, re.S,
    )
    assert m, "upsert writer replacement must exist"
    body = m.group(1)
    assert "v_connections" in body
    assert re.search(r"insert into public\.nayanet_intelligent_blocks\((.*?)\)", body, re.S).group(1).count(",") >= 16
    insert_cols = re.search(r"insert into public\.nayanet_intelligent_blocks\((.*?)\)", body, re.S).group(1)
    assert "connections" in [c.strip() for c in insert_cols.split(",")]
    assert "connections=excluded.connections" in body.replace(" ", ""), \
        "re-upsert must refresh the projection, not keep the stale one"


def test_commit_writer_persists_connections(migration_text):
    assert "p_connections jsonb default null" in migration_text.replace("  ", " "), \
        "commit writer must accept an optional trailing p_connections parameter"
    assert "drop function if exists public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text);" in migration_text, \
        "the old 8-arg signature must be dropped or the bridge keeps resolving to the stale overload"


def test_no_self_supersede_and_linear_chain_hardening(migration_text):
    assert "nayanet_intelligent_blocks_no_self_supersede" in migration_text
    assert "nayanet_intelligent_blocks_one_superseder_idx" in migration_text
    assert "nayanet_intelligent_blocks_supersedes_chain_idx" in migration_text
