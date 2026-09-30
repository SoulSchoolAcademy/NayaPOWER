from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESET = ROOT / "supabase/migrations/20260927164132_reset_legacy_nayanet_intelligence_layer.sql"
HARDEN = ROOT / "supabase/migrations/20260930022500_harden_collective_wisdom_consent_revocation_v1.sql"


def _sql(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").lower().split())


def test_collective_wisdom_hardening_restores_objects_removed_by_canonical_reset():
    reset = _sql(RESET)
    sql = _sql(HARDEN)
    assert "drop table if exists public.%i cascade" in reset
    assert "create table if not exists public.nayanet_smart_connect_participation" in sql
    assert "create table if not exists public.nayanet_collective_wisdom" in sql
    assert "consent_state text not null default 'pending'" in sql
    assert "external_bindings jsonb not null default '[]'::jsonb" in sql
    assert "nayanet_smart_connect(p_door text,p_consent_state text)" in sql
    assert "smart_connect_consent_required" in sql
    assert sql.index("create table if not exists public.nayanet_collective_wisdom") < sql.index(
        "alter table public.nayanet_collective_wisdom enable row level security"
    )


def test_restored_seam_keeps_private_defaults_and_no_anon_rpc_grant():
    sql = _sql(HARDEN)
    assert "personal_intelligence text not null default 'private'" in sql
    assert "identity_visibility text not null default 'private'" in sql
    assert "revoke all on function public.nayanet_smart_connect(text,text) from public,anon" in sql
    assert "grant execute on function public.nayanet_smart_connect(text,text) to authenticated" in sql
