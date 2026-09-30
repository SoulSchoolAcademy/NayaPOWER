"""CONNECT writer threading: structural verification of the SQL migration.

The migration cannot be executed against a live database from here, so this
test verifies everything that can be verified without one:
  1. the migration parses with a real PostgreSQL parser (pglast);
  2. the commit bridge forwards p_connections to the R1 commit writer;
  3. the supersede bridge exists, enforces the governed runtime checks
     (naya_id, jti, authority grant with the intelligence_commit action),
     and calls the promoted supersession writer with eligible defaults;
  4. both bridges stay service_role-only.

DB execution (deploy-time) remains the chain owner's verification step and
is disclosed as such in the PR.
"""
import re
from pathlib import Path

import pytest
from pglast import parse_sql

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20260930050000_thread_connections_through_commit_bridge.sql"


@pytest.fixture(scope="module")
def migration_text():
    return MIGRATION.read_text(encoding="utf-8")


def test_migration_file_exists():
    assert MIGRATION.exists(), "CONNECT threading migration must exist"


def test_migration_sorts_after_r1_writer_contract():
    r1 = next(ROOT.glob("supabase/migrations/*_r1_writer_connections_v1.sql"), None)
    assert r1 is not None, "R1 writer contract migration must exist"
    assert MIGRATION.name > r1.name, "threading migration must sort after the R1 contract"


def test_migration_parses_with_postgres_parser(migration_text):
    stmts = parse_sql(migration_text)
    # drop + create + revoke + grant for each bridge (8 statements total)
    assert len(stmts) == 8, f"expected 8 statements, got {len(stmts)}"


def test_commit_bridge_threads_p_connections(migration_text):
    assert re.search(
        r"create function public\.nayanet_intelligence_commit_runtime\([^;]*?p_connections jsonb default null",
        migration_text,
        re.DOTALL,
    ), "commit bridge must accept trailing p_connections"
    assert "drop function if exists public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text)" in migration_text
    assert "public.nayanet_intelligence_commit(p_event_id,p_title,p_content,p_category,p_topic,p_target_id,p_authority_grant_id,p_project_id,p_connections)" in migration_text


def test_supersede_bridge_governed(migration_text):
    assert re.search(
        r"create function public\.nayanet_supersede_intelligent_block_runtime\([^;]*?p_connections jsonb default null",
        migration_text,
        re.DOTALL,
    ), "supersede bridge must accept trailing p_connections"
    assert "NAYA_ID_NOT_AUTHORIZED" in migration_text
    assert "RUNTIME_JTI_REQUIRED" in migration_text
    assert "AUTHORITY_BLOCKED" in migration_text
    assert 'actions @> \'["intelligence_commit"]\'::jsonb' in migration_text
    assert "public.nayanet_supersede_intelligent_block(" in migration_text


def test_supersede_bridge_eligible_defaults(migration_text):
    # evidence_refs must be non-empty for the new row to stay eligible for
    # retrieval (know.ts isEligibleBlock); idempotency key travels in the
    # evidence envelope and the writer's provenance merge.
    assert "idempotency_key" in migration_text
    assert "jsonb_build_object('lesson',p_content)" in migration_text


def test_bridges_service_role_only(migration_text):
    for sig, name in [
        ("text,uuid,text,text,text,text,text,text,text,uuid,text,jsonb", "nayanet_intelligence_commit_runtime"),
        ("text,uuid,text,uuid,text,uuid,text,text,text,text,text,text,jsonb", "nayanet_supersede_intelligent_block_runtime"),
    ]:
        assert f"revoke all on function public.{name}({sig}) from public,anon,authenticated" in migration_text
        assert f"grant execute on function public.{name}({sig}) to service_role" in migration_text


def test_supersede_bridge_required_parameters_precede_defaults(migration_text):
    m = re.search(
        r"create function public\.nayanet_supersede_intelligent_block_runtime\((.*?)\) returns jsonb",
        migration_text,
        re.DOTALL | re.IGNORECASE,
    )
    assert m, "supersede runtime bridge signature must exist"
    signature = m.group(1)
    assert signature.index("p_idempotency_key text") < signature.index("p_project_id text default"), (
        "all required parameters must precede the first defaulted parameter; "
        "PostgreSQL rejects default-before-required signatures with SQLSTATE 42P13"
    )
    assert "p_superseded_block_id uuid,p_title text,p_content text,p_idempotency_key text" in signature.replace("\n", " "), (
        "required supersede inputs must stay required rather than being hidden behind nullable defaults"
    )
