from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "supabase" / "migrations" / "20260924175545_smart_connect_participation_collective_wisdom_v1.sql"
MIG = ROOT / "supabase" / "migrations" / "20260930023000_collective_wisdom_revocation_projection_v1.sql"


def _sql(path=MIG):
    return path.read_text(encoding="utf-8").lower()


def test_collective_feed_is_derived_only_without_direct_authenticated_base_table_read():
    sql = _sql()
    assert "security_invoker=false" in sql
    assert "security_barrier=true" in sql
    assert "revoke all on table public.nayanet_collective_wisdom from anon, authenticated" in sql
    assert "grant select on table public.nayanet_collective_wisdom_feed to authenticated" in sql
    assert "grant select on table public.nayanet_collective_wisdom to authenticated" not in sql

    view = sql.split("create or replace view public.nayanet_collective_wisdom_feed", 1)[1].split(
        "revoke all on table public.nayanet_collective_wisdom", 1
    )[0]
    assert "cw.wisdom_claim" in view
    assert "cw.topic" in view
    assert "cw.epistemic_state" in view
    assert "cw.owner_id," not in view
    assert "cw.provenance" not in view
    assert "raw_content" not in view


def test_collective_feed_requires_current_active_smart_connect_participation():
    sql = _sql()
    view = sql.split("create or replace view public.nayanet_collective_wisdom_feed", 1)[1].split(
        "revoke all on table public.nayanet_collective_wisdom", 1
    )[0]
    assert "cw.status='active'" in view
    assert "p.member_id=cw.owner_id" in view
    assert "p.status='active'" in view
    assert "p.wisdom_sharing='default'" in view


def test_disconnect_revokes_derived_wisdom_only_when_no_active_participation_remains():
    sql = _sql()
    disconnect = sql.split("create or replace function public.nayanet_smart_disconnect", 1)[1]
    assert "v_has_active_participation" in disconnect
    assert "if not v_has_active_participation then" in disconnect
    assert "update public.nayanet_collective_wisdom" in disconnect
    assert "set status='revoked'" in disconnect
    assert "where owner_id=v_actor" in disconnect
    assert "and status='active'" in disconnect
    assert "collective_wisdom_revoked_count" in disconnect


def test_reconnect_is_not_redefined_to_silently_reactivate_old_wisdom():
    sql = _sql()
    assert "create or replace function public.nayanet_smart_connect(" not in sql
    assert "set status='active'" not in sql.split(
        "create or replace function public.nayanet_smart_disconnect", 1
    )[1].split("return jsonb_build_object", 1)[0]


def test_original_private_and_contribution_boundaries_remain_present():
    base = _sql(BASE)
    assert "alter table public.nayanet_collective_wisdom enable row level security" in base
    assert "revoke all on table public.nayanet_collective_wisdom from anon,authenticated" in base
    assert "grant execute on function public.nayanet_collective_wisdom_for_event" in base
    assert "to service_role" in base
    assert "-'identity'-'owner_id'-'raw_content'" in base
