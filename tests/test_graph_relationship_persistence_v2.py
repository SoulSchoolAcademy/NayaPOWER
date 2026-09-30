from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQL = (ROOT / "supabase/migrations/20260930024000_harden_brain_relationship_semantics_v2.sql").read_text(encoding="utf-8")

def test_graph_v2_migration_is_additive_on_existing_table():
    assert "alter table public.nayanet_brain_relationships" in SQL
    assert "create table public.nayanet_brain_relationships" not in SQL.lower()
    for field in [
        "status text not null default 'ACTIVE'",
        "visibility text not null default 'PRIVATE'",
        "evidence_refs jsonb",
        "observed_at timestamptz",
        "valid_from timestamptz",
        "valid_until timestamptz",
        "supersedes_relationship_id uuid",
        "consent_ref text",
        "applicability jsonb",
        "reason_codes jsonb",
    ]:
        assert field in SQL

def test_legacy_edges_stay_unknown_applicability_not_promoted():
    assert '"state":"UNKNOWN"' in SQL
    assert "LEGACY_V1_UNCLASSIFIED" in SQL
    assert "LEGACY_V1_EDGE" in SQL
    assert "update public.nayanet_brain_relationships set epistemic_state" not in " ".join(SQL.lower().split())

def test_temporal_and_supersession_guards_fail_closed():
    compact = " ".join(SQL.split())
    assert "valid_until is null or valid_from <= valid_until" in compact
    assert "supersedes_relationship_id is null or supersedes_relationship_id <> relationship_id" in compact

def test_shared_visibility_requires_consent():
    compact = " ".join(SQL.split())
    assert "visibility <> 'DERIVED_SHARED' or consent_ref is not null" in compact

def test_applicability_is_tristate_and_structured():
    for state in ["APPLICABLE","NOT_APPLICABLE","UNKNOWN"]:
        assert state in SQL
    assert "jsonb_typeof(applicability->'task_classes') = 'array'" in SQL
    assert "jsonb_typeof(applicability->'limitations') = 'array'" in SQL

def test_migration_does_not_weaken_rls_or_create_authority():
    lowered = SQL.lower()
    assert "disable row level security" not in lowered
    assert "grant all" not in lowered
    assert "create policy" not in lowered
    assert "authority" in lowered
    assert "deliberately no update to epistemic_state" in lowered
