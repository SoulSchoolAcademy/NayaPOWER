from pathlib import Path

MIGRATION = Path(__file__).parents[1] / "supabase" / "migrations" / "20260930233000_restore_smart_ledger_value_receipt_runtime_v2_1.sql"
INDEX_MIGRATION = Path(__file__).parents[1] / "supabase" / "migrations" / "20260930234500_restore_smart_ledger_intelligence_index_projection_v2_1.sql"


def test_runtime_seam_is_additive_and_single_ledger():
    sql = MIGRATION.read_text(encoding="utf-8")
    assert "alter table public.nayanet_execution_receipts add column if not exists value jsonb" in sql
    assert "create table if not exists public.nayanet_smart_ledger" in sql
    assert "create or replace function public.nayanet_record_ledger_event" in sql
    assert "create trigger nayanet_execution_receipt_to_smart_ledger" in sql
    assert "nayanet_smart_ledger_to_intelligence_index" not in sql
    assert "drop table" not in sql.lower()
    assert "delete from public.nayanet_smart_ledger" not in sql.lower()


def test_v2_1_receipt_types_and_assessment_states_are_explicit():
    sql = MIGRATION.read_text(encoding="utf-8")
    for token in (
        "ALIGNMENT_DECISION",
        "CONTRIBUTION_VALUE",
        "ASSESSED",
        "UNASSESSED",
        "VERIFIED_VALUE",
        "DECISION-VALUE-CALCULUS-V2.1",
        "value_receipt_hash",
        "VALUE_RECEIPT_POSITIVE_POINTS_REQUIRE_VERIFIED_VALUE",
    ):
        assert token in sql


def test_legacy_starting_model_is_preserved_not_reinterpreted():
    sql = MIGRATION.read_text(encoding="utf-8")
    assert "NayaNET_V1_STARTING_MODEL" in sql
    assert "legacy_provenance_preserved" in sql
    assert "base_points" not in sql


def test_authority_privacy_and_idempotency_boundaries_exist():
    sql = MIGRATION.read_text(encoding="utf-8")
    assert "LEDGER_OWNER_MISMATCH" in sql
    assert "unique(owner_id,source_table,source_id)" in sql
    assert "privacy_classification" in sql
    assert "revoke all on function public.nayanet_record_ledger_event" in sql
    assert "revoke select,insert,update,delete on public.nayanet_smart_ledger from anon,authenticated" in sql


def test_canonical_intelligence_index_projection_is_restored_separately():
    sql = INDEX_MIGRATION.read_text(encoding="utf-8")
    assert "nayanet_smart_ledger_to_intelligence_index" in sql
    assert "public.nayanet_intelligence_index" in sql
    assert "nayanet_smart_ledger" in sql
    assert "drop trigger if exists nayanet_smart_ledger_to_intelligence_index" in sql
