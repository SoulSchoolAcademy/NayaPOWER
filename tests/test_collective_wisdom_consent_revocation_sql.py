from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / "supabase" / "migrations" / "20260930022500_harden_collective_wisdom_consent_revocation_v1.sql"
# #1136 Reading A (ratified 2026-09-30): disconnect stops future, does not erase past.
READING_A_MIGRATION = ROOT / "supabase" / "migrations" / "20261001030000_disconnect_stop_future_v1.sql"


def _normalize(path: Path) -> str:
    assert path.exists(), f"required migration missing: {path.name}"
    sql = " ".join(path.read_text(encoding="utf-8").split()).lower()
    sql = re.sub(r"\s*,\s*", ",", sql)
    sql = re.sub(r"\s*=\s*", "=", sql)
    sql = re.sub(r"\(\s+", "(", sql)
    sql = re.sub(r"\s+\)", ")", sql)
    return sql


def _sql() -> str:
    return _normalize(MIGRATION)


def _sql_reading_a() -> str:
    return _normalize(READING_A_MIGRATION)


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


def test_disconnect_revokes_participation_without_touching_prior_wisdom():
    # #1136 Reading A: disconnect revokes the participation row (which blocks
    # future capture/contribution) and MUST NOT mass-revoke prior derived wisdom.
    sql = _sql_reading_a()
    assert "update public.nayanet_smart_connect_participation" in sql
    assert "set status='revoked',consent_state='revoked',revoked_at=now(),updated_at=now()" in sql
    assert "update public.nayanet_collective_wisdom" not in sql


def test_disconnect_receipt_declares_prior_rows_retained():
    sql = _sql_reading_a()
    assert "'collective_wisdom_prior_rows','retained_anonymized'" in sql
    assert "'collective_wisdom_future_capture','blocked_while_disconnected'" in sql
    assert "revoked_when_last_explicit_participation_ends" not in sql


def test_disconnect_remains_prospective_no_history_rewrite():
    # Rows already REVOKED by past disconnects are not resurrected.
    sql = _sql_reading_a()
    assert "set status='active'" not in sql


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
