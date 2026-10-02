-- #1136 Reading A — disconnect stops future, does not erase past.
--
-- Ratified 2026-09-30 by the Human Director (issue #1136, Reading A):
-- disconnect/revocation of a Smart Connect participation stops FUTURE
-- capture, contribution, and participation-governed access, but does NOT
-- automatically erase or disable already-distilled, anonymized collective
-- wisdom merely because the contributor disconnected.
--
-- This migration replaces the mass-revocation behavior introduced in
-- 20260930022500_harden_collective_wisdom_consent_revocation_v1.sql
-- (nayanet_smart_disconnect flipped every ACTIVE collective-wisdom row of
-- the disconnecting owner to REVOKED once their last explicit participation
-- ended). That behavior is removed PROSPECTIVELY ONLY:
--
--   * Future disconnects revoke the participation row (blocking future
--     capture/contribution, which requires status='active' AND
--     consent_state='explicit') and leave prior collective-wisdom rows
--     untouched.
--   * Rows already marked REVOKED by past disconnects are NOT resurrected.
--     No history rewrite; a separate lawful/safety/leakage removal
--     mechanism (follow-on) governs genuine suppression cases.
--
-- The COLLECTIVE_WISDOM_REVOKED_REQUIRES_NEW_SOURCE_EVENT guard is
-- unchanged: it continues to protect rows revoked through the removal
-- mechanism from silent reactivation.

create or replace function public.nayanet_smart_disconnect(p_door text)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_actor uuid := auth.uid();
  v_door text := lower(trim(p_door));
  v_row public.nayanet_smart_connect_participation;
begin
  if v_actor is null then
    raise exception 'AUTH_REQUIRED';
  end if;

  if v_door not in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps') then
    raise exception 'SMART_CONNECT_DOOR_INVALID';
  end if;

  select * into v_row
  from public.nayanet_smart_connect_participation
  where member_id=v_actor and door=v_door
  for update;

  if v_row.id is null then
    raise exception 'SMART_CONNECT_PARTICIPATION_NOT_FOUND';
  end if;

  if v_row.status='revoked' then
    return jsonb_build_object(
      'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
      'status','ALREADY_DISCONNECTED',
      'participation',to_jsonb(v_row),
      'authority','UNCHANGED'
    );
  end if;

  update public.nayanet_smart_connect_participation
  set status='revoked',
      consent_state='revoked',
      revoked_at=now(),
      updated_at=now()
  where id=v_row.id
  returning * into v_row;

  -- #1136 Reading A: no mass-revocation of prior derived wisdom.
  -- Prior ACTIVE collective-wisdom rows remain ACTIVE. Future capture and
  -- contribution are blocked by the revoked participation row itself.

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
    'status','DISCONNECTED',
    'participation',to_jsonb(v_row),
    'authority','UNCHANGED',
    'collective_wisdom_prior_rows','RETAINED_ANONYMIZED',
    'collective_wisdom_future_capture','BLOCKED_WHILE_DISCONNECTED'
  );
end;
$$;

revoke all on function public.nayanet_smart_disconnect(text) from public,anon;
grant execute on function public.nayanet_smart_disconnect(text) to authenticated;
