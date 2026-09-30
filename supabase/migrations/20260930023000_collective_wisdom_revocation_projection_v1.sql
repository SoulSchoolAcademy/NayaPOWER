-- #1062 bounded hardening: keep private owner intelligence private while making the
-- existing derived collective projection usable only while Smart Connect consent is active.
-- This migration does not grant authenticated users direct access to the base wisdom table.

create or replace view public.nayanet_collective_wisdom_feed
with (security_invoker=false, security_barrier=true) as
select
  cw.id,
  cw.source_event_id,
  cw.wisdom_claim,
  cw.topic,
  cw.epistemic_state,
  cw.status,
  cw.identity_visibility,
  cw.source_visibility,
  cw.public_publication,
  cw.created_at
from public.nayanet_collective_wisdom as cw
where cw.status='ACTIVE'
  and exists (
    select 1
    from public.nayanet_smart_connect_participation as p
    where p.member_id=cw.owner_id
      and p.status='active'
      and p.wisdom_sharing='default'
  );

-- The safe shared surface is the derived-only view. Keep owner_id/provenance hidden
-- by preserving the direct base-table deny for authenticated and anonymous roles.
revoke all on table public.nayanet_collective_wisdom from anon, authenticated;
revoke all on table public.nayanet_collective_wisdom_feed from anon;
grant select on table public.nayanet_collective_wisdom_feed to authenticated;

create or replace function public.nayanet_smart_disconnect(p_door text)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_actor uuid:=auth.uid();
  v_door text:=lower(trim(p_door));
  v_row public.nayanet_smart_connect_participation;
  v_has_active_participation boolean:=false;
  v_revoked_wisdom_count bigint:=0;
begin
  if v_actor is null then
    raise exception 'AUTH_REQUIRED';
  end if;

  update public.nayanet_smart_connect_participation
  set status='revoked',revoked_at=now(),updated_at=now()
  where member_id=v_actor and door=v_door
  returning * into v_row;

  if v_row.id is null then
    raise exception 'SMART_CONNECT_PARTICIPATION_NOT_FOUND';
  end if;

  select exists(
    select 1
    from public.nayanet_smart_connect_participation
    where member_id=v_actor
      and status='active'
      and wisdom_sharing='default'
  ) into v_has_active_participation;

  if not v_has_active_participation then
    update public.nayanet_collective_wisdom
    set status='REVOKED'
    where owner_id=v_actor
      and status='ACTIVE';
    get diagnostics v_revoked_wisdom_count = row_count;
  end if;

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
    'status','DISCONNECTED',
    'participation',to_jsonb(v_row),
    'authority','UNCHANGED',
    'collective_wisdom_status',case when v_has_active_participation then 'ACTIVE_VIA_OTHER_PARTICIPATION' else 'REVOKED' end,
    'collective_wisdom_revoked_count',v_revoked_wisdom_count
  );
end;
$$;

revoke all on function public.nayanet_smart_disconnect(text) from public;
grant execute on function public.nayanet_smart_disconnect(text) to authenticated;
