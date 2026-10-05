from pathlib import Path

from pglast import parse_sql

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase/migrations/20261005235000_exact_event_replay_reconciliation_v1.sql"


def source() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def replay_block(sql: str) -> str:
    start = sql.index("if existing_event.id is not null then")
    end = sql.index("select coalesce(max(r.revision),0)+1 into revision", start)
    return sql[start:end]


def test_replay_migration_parses_as_postgresql():
    statements = parse_sql(source())
    assert statements


def test_current_authority_and_project_lock_precede_replay_reconciliation():
    sql = source()
    authority = sql.index("nayanet_validate_authority_grant")
    subject = sql.index("AUTHORITY_SUBJECT_MISMATCH")
    lock = sql.index("pg_advisory_xact_lock")
    lookup = sql.index("select e.* into existing_event")
    assert authority < subject < lock < lookup


def test_exact_replay_compares_the_full_normalized_commit_identity():
    block = replay_block(source())
    for required in (
        "existing_event.title is distinct from p_title",
        "existing_event.content is distinct from p_content",
        "existing_event.source_hash is distinct from content_hash",
        "existing_event.metadata->>'target_id' is distinct from p_target_id",
        "existing_block.subject_id is distinct from p_target_id",
        "existing_block.content is distinct from v_content",
        "existing_block.connections",
        "v_connections",
        "existing_event.id = any(existing_block.source_event_ids)",
    ):
        assert required in block
    assert "EVENT_ID_REPLAY_MISMATCH" in block


def test_exact_replay_requires_complete_original_receipt_and_lineage():
    block = replay_block(source())
    for required in (
        "existing_receipt.action is distinct from 'intelligence_commit'",
        "existing_receipt.status is distinct from 'SUCCESS'",
        "event_row_id",
        "block_row_id",
        "intelligent_block_id",
        "lineage_id",
        "relationship_id",
        "index_id",
        "checkpoint_id",
        "public.nayanet_intelligence_lineage",
        "public.nayanet_brain_relationships",
        "public.nayanet_intelligence_index",
        "public.nayanet_project_cognition_state",
        "EVENT_ID_REPLAY_INCOMPLETE",
    ):
        assert required in block


def test_exact_replay_is_read_only_and_returns_original_ids():
    sql = source()
    block = replay_block(sql)
    assert "insert into " not in block.lower()
    assert "update public." not in block.lower()
    assert "'idempotent_replay',true" in block
    assert "'replay_reconciled',true" in block
    for original in (
        "'receipt_id',existing_receipt.id",
        "'event_id',existing_event.id",
        "'intelligent_block_id',existing_block.intelligent_block_id",
        "'block_row_id',existing_block.block_id",
        "'lineage_id',existing_receipt.evidence->>'lineage_id'",
        "'relationship_id',existing_receipt.evidence->>'relationship_id'",
        "'index_id',existing_receipt.evidence->>'index_id'",
        "'checkpoint_id',existing_receipt.evidence->>'checkpoint_id'",
    ):
        assert original in block
    assert "message='EVENT_ID_REPLAY';" not in sql


def test_fresh_write_path_is_preserved_after_replay_branch():
    sql = source()
    start = sql.index("select coalesce(max(r.revision),0)+1 into revision")
    fresh = sql[start:]
    for table in (
        "public.nayanet_execution_receipts",
        "public.nayanet_cognition_events",
        "public.nayanet_intelligent_blocks",
        "public.nayanet_intelligence_lineage",
        "public.nayanet_brain_relationships",
        "public.nayanet_intelligence_index",
        "public.nayanet_project_cognition_state",
    ):
        assert f"insert into {table}" in fresh
    assert "nayanet_normalize_block_connections" in sql
    assert "CAPABILITY_UNKNOWN" in sql
    assert "understanding_state','CANDIDATE'" in fresh
