from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20260930022500_harden_collective_wisdom_consent_revocation_v1.sql"


def _sql() -> str:
    assert MIGRATION.exists(), "collective-wisdom consent/revocation hardening migration is required"
    sql = " ".join(MIGRATION.read_text(encoding="utf-8").split()).lower()
    sql = re.sub(r"\s*,\s*", ",", sql)
    sql = re.sub(r"\s*=\s*", "=", sql)
    sql = re.sub(r"\(\s+", "(", sql)
    sql = re.sub(r"\s+\)", ")", sql)
    return sql


def test_collective_feed_has_safe_authenticated_read_without_raw_owner_or_provenance_grant():
    sql = _sql()
    assert "revoke all on table public.nayanet_collective_wisdom from anon,authenticated" in sql
    assert "grant select (id,source_event_id,wisdom_claim,topic,epistemic_state,status,identity_visibility,source_visibility,public_publication,created_at) on public.nayanet_collective_wisdom to authenticated" in sql
    assert "create policy nayanet_collective_wisdom_safe_read on public.nayanet_collective_wisdom for select to authenticated using (status='active' or owner_id=auth.uid())" in sql
    assert "grant select on public.nayanet_collective_wisdom to authenticated" not in sql


def test_collective_contribution_requires_explicit_consent_and_source_owner_binding():
    sql = _sql()
    assert "status='active' and consent_state='explicit' and wisdom_sharing='default'" in sql
    assert "from public.nayanet_cognition_events e where e.id=p_source_event_id and e.user_id=p_owner_id" in sql
    assert "collective_wisdom_source_owner_mismatch" in sql


def test_disconnect_revokes_derived_wisdom_only_after_last_active_explicit_participation():
    sql = _sql()
    assert "not exists(select 1 from public.nayanet_smart_connect_participation" in sql
    assert "member_id=v_actor and status='active' and consent_state='explicit'" in sql
    assert "update public.nayanet_collective_wisdom set status='revoked'" in sql
    assert "where owner_id=v_actor and status='active'" in sql


def test_recontribution_does_not_silently_reactivate_or_rewrite_revoked_wisdom():
    sql = _sql()
    expected = (
        "on conflict(source_event_id) do update set "
        "wisdom_claim=excluded.wisdom_claim,topic=excluded.topic,provenance=excluded.provenance "
        "where nayanet_collective_wisdom.status='active'"
    )
    assert expected in sql
    assert "collective_wisdom_revoked_requires_new_source_event" in sql
    assert "on conflict(source_event_id) do update set status='active'" not in sql
