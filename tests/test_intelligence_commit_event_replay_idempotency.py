from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL = (ROOT / "supabase/migrations/20261006001500_reconcile_intelligence_commit_event_replay_v1.sql").read_text(encoding="utf-8")

def test_exact_replay_reuses_existing_lineage_without_second_write():
    assert "REUSED_EXISTING_CANONICAL_LINEAGE" in SQL
    assert "'reconciled_replay',true" in SQL
    replay = SQL.index("select * into v_existing_event")
    assert SQL.index("REUSED_EXISTING_CANONICAL_LINEAGE", replay) < SQL.index("insert into public.nayanet_execution_receipts", replay)

def test_changed_payload_fails_closed():
    assert "EVENT_ID_REPLAY_PAYLOAD_MISMATCH" in SQL
    assert "v_existing_event.source_hash is distinct from content_hash" in SQL
    assert "v_existing_block.content is distinct from v_content" in SQL
    assert "coalesce(v_existing_block.connections,'[]'::jsonb) is distinct from v_connections" in SQL

def test_incomplete_lineage_fails_closed():
    for marker in (
        "BLOCK_MISSING","RECEIPT_MISMATCH","EVIDENCE_IDS_MISSING",
        "LINEAGE_MISSING","RELATIONSHIP_MISSING","INDEX_MISSING","CHECKPOINT_MISSING"
    ):
        assert "EVENT_ID_REPLAY_INCOMPLETE:" + marker in SQL

def test_authority_remains_before_replay():
    assert SQL.index("nayanet_validate_authority_grant") < SQL.index("select * into v_existing_event")

def test_old_unconditional_replay_rejection_is_gone():
    assert "message='EVENT_ID_REPLAY';" not in SQL
