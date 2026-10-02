-- P4 — Consent runtime consumer reconciled to ratified #1136.
--
-- PROPOSED / SOURCE-ONLY. Not applied to production. Not merged.
--
-- RATIFIED SEMANTIC BOUNDARY (#1136):
--   * live explicit participation gates FUTURE collective contribution;
--   * disconnect/revocation stops future contribution/access governed by participation;
--   * already accepted identity-safe derived collective wisdom is NOT automatically
--     retracted merely because the contributor disconnects;
--   * raw/private source material remains owner-protected;
--   * collective/retrieved intelligence never creates authority.
--
-- This corrective migration preserves nayanet_consent_is_active(uuid) as the
-- canonical CURRENT-PARTICIPATION reader for contribution-time checks and future
-- participation-gated surfaces. It deliberately does NOT use current participation
-- to retroactively suppress already accepted derived collective wisdom.
--
-- It also overrides the pending disconnect function from 20260930022500 so that
-- disconnect no longer mass-revokes prior collective wisdom.
--
-- =========================================================================
-- 1. The live-consent consumer.
--    TRUE  iff the owner holds >= 1 participation row with
--          status='active' AND consent_state='explicit'.
--    FALSE otherwise: no row, revoked, pending, NULL owner, or ANY query
--    error. UNKNOWN -> FALSE. Fail closed, always (Art. XIV).
-- =========================================================================

create or replace function public.nayanet_consent_is_active(p_owner_id uuid)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_ok boolean := false;
begin
  if p_owner_id is null then
    return false;
  end if;
  begin
    select exists(
      select 1
      from public.nayanet_smart_connect_participation
      where member_id = p_owner_id
        and status = 'active'
        and consent_state = 'explicit'
    ) into v_ok;
  exception
    when others then
      -- Any failure of the consent check is a denial, never a bypass.
      return false;
  end;
  return coalesce(v_ok, false);
end;
$$;

comment on function public.nayanet_consent_is_active(uuid) is
  'P4 current-participation reader reconciled to ratified #1136. TRUE iff owner has >= 1 '
  'active explicit participation row. Use to gate future contribution/participation-gated '
  'operations. Do not use current participation to retroactively retract accepted identity-safe '
  'derived collective wisdom. FALSE on uncertainty/error; intelligence never creates authority.';

-- Least privilege: callable by the runtime paths that need it; not by the public.
revoke all on function public.nayanet_consent_is_active(uuid) from public, anon;
grant execute on function public.nayanet_consent_is_active(uuid) to authenticated, service_role;

-- =========================================================================
-- 2. Reconcile collective_wisdom read semantics to ratified #1136.
--    Already accepted identity-safe derived wisdom remains available while ACTIVE.
--    Current participation is NOT a retroactive read gate.
--    Raw source tables/blocks retain their separate owner/RLS protections.
-- =========================================================================

grant select on public.nayanet_collective_wisdom to authenticated;

drop policy if exists nayanet_collective_wisdom_safe_read
  on public.nayanet_collective_wisdom;

create policy nayanet_collective_wisdom_safe_read
  on public.nayanet_collective_wisdom
  for select to authenticated
  using (status = 'ACTIVE' or owner_id = auth.uid());

comment on policy nayanet_collective_wisdom_safe_read
  on public.nayanet_collective_wisdom is
  'Ratified #1136: accepted identity-safe derived collective wisdom remains readable while ACTIVE; '
  'disconnect does not itself retract history. Raw/private source access remains separately protected.';

-- =========================================================================
-- 3. Override disconnect semantics from 20260930022500.
--    Disconnect stops future participation but does not mass-revoke accepted
--    identity-safe derived collective wisdom.
-- =========================================================================

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
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_door not in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps') then
    raise exception 'SMART_CONNECT_DOOR_INVALID';
  end if;

  select * into v_row
  from public.nayanet_smart_connect_participation
  where member_id=v_actor and door=v_door
  for update;

  if v_row.id is null then raise exception 'SMART_CONNECT_PARTICIPATION_NOT_FOUND'; end if;

  if v_row.status='revoked' then
    return jsonb_build_object(
      'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
      'status','ALREADY_DISCONNECTED',
      'participation',to_jsonb(v_row),
      'authority','UNCHANGED',
      'future_collective_contribution','DENIED',
      'prior_identity_safe_collective_wisdom','UNCHANGED'
    );
  end if;

  update public.nayanet_smart_connect_participation
  set status='revoked',consent_state='revoked',revoked_at=now(),updated_at=now()
  where id=v_row.id
  returning * into v_row;

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
    'status','DISCONNECTED',
    'participation',to_jsonb(v_row),
    'authority','UNCHANGED',
    'future_collective_contribution','DENIED',
    'prior_identity_safe_collective_wisdom','UNCHANGED',
    'public_publication','NOT_GRANTED'
  );
end;
$$;

revoke all on function public.nayanet_smart_disconnect(text) from public,anon;
grant execute on function public.nayanet_smart_disconnect(text) to authenticated;

comment on function public.nayanet_smart_disconnect(text) is
  'Ratified #1136: disconnect ends future participation/contribution. It does not automatically '
  'revoke prior accepted identity-safe derived collective wisdom. Authority remains unchanged.';
