from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "supabase/migrations/20260930024000_harden_brain_relationship_semantics_v2.sql"
REPAIR = ROOT / "supabase/migrations/20260930031355_repair_graph_v2_temporal_insert_defaults.sql"
PRODUCER = ROOT / "supabase/migrations/20260928180632_fix_intelligence_commit_lineage_and_revision.sql"


def _sql(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").lower().split())


def test_graph_v2_temporal_columns_remain_required_but_gain_insert_time_defaults():
    v2 = _sql(V2)
    repair = _sql(REPAIR)
    assert "alter column observed_at set not null" in v2
    assert "alter column valid_from set not null" in v2
    assert "alter column observed_at set default now()" in repair
    assert "alter column valid_from set default now()" in repair
    assert "drop not null" not in repair


def test_existing_intelligence_commit_relationship_insert_is_compatible_without_shape_fork():
    producer = _sql(PRODUCER)
    repair = _sql(REPAIR)
    assert "insert into public.nayanet_brain_relationships" in producer
    assert "observed_at" not in producer.split("insert into public.nayanet_brain_relationships",1)[1].split("returning",1)[0]
    assert "alter table public.nayanet_brain_relationships" in repair
    assert "create table" not in repair
