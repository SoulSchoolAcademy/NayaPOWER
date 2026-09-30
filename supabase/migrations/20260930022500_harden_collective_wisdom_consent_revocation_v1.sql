-- NayaNET collective-wisdom consent/revocation hardening.
-- Extends the existing Smart Connect + derived collective-wisdom seam.
-- Does not grant cross-owner access to raw cognition events or Intelligent Blocks.
-- Production prerequisite: explicit Smart Connect consent semantics from 20260925020000.

alter table public.nayanet_collective_wisdom enable row level security;

revoke all on table public.nayanet_collective_wisdom from anon,authenticated;

grant select (
  id,
  source_event_id,
  wisdom_claim,
  topic,
  epistemic_state,
  status,
  identity_visibility,
  source_visibility,
  public_publication,
  created_at
) on public.nayanet_collective_wisdom to authenticated;

drop policy if exists nayanet_collective_wisdom_safe_read on public.nayanet_collective_wisdom;
create policy nayanet_collective_wisdom_safe_read
on public.nayanet_collective_wisdom
for select to authenticated
using (status='ACTIVE' or owner_id=auth.uid());

create or replace function public.nayanet_collective_wisdom_for_event(
  p_source_event_id uuid,
  p_owner_id uuid,
  p_wisdom_claim text,
  p_topic text,
  p_provenance jsonb
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_participation boolean;
  v_source_owned boolean;
  v_row public.nayanet_collective_wisdom;
begin
  select exists(
    select 1
    from public.nayanet_smart_connect_participation
    where member_id=p_owner_id
      and status='active'
      and consent_state='explicit'
      and wisdom_sharing='default'
  ) into v_participation;

  if not v_participation then
    raise exception 'SMART_CONNECT_EXPLICIT_CONSENT_REQUIRED';
  end if;

  select exists(
    select 1
    from public.nayanet_cognition_events e
    where e.id=p_source_event_id and e.user_id=p_owner_id
  ) into v_source_owned;

  if not v_source_owned then
    raise exception 'COLLECTIVE_WISDOM_SOURCE_OWNER_MISMATCH';
  end if;

  if nullif(trim(p_wisdom_claim),'') is null then
    raise exception 'COLLECTIVE_WISDOM_CLAIM_REQUIRED';
  end if;

  insert into public.nayanet_collective_wisdom(
    source_event_id,
    owner_id,
    wisdom_claim,
    topic,
    provenance
  )
  values(
    p_source_event_id,
    p_owner_id,
    left(trim(p_wisdom_claim),4000),
    coalesce(nullif(trim(p_topic),''),'GENERAL'),
    coalesce(p_provenance,'{}'::jsonb)-'identity'-'owner_id'-'raw_content'
  )
  on conflict(source_event_id) do update set
    wisdom_claim=excluded.wisdom_claim,
    topic=excluded.topic,
    provenance=excluded.provenance
  where nayanet_collective_wisdom.status='ACTIVE'
  returning * into v_row;

  if v_row.id is null then
    raise exception 'COLLECTIVE_WISDOM_REVOKED_REQUIRES_NEW_SOURCE_EVENT';
  end if;

  return jsonb_build_object(
    'schema','NAYANET_COLLECTIVE_WISDOM_V1',
    'status','CONTRIBUTED',
    'collective_wisdom_id',v_row.id,
    'source_event_id',v_row.source_event_id,
    'identity_visibility','private',
    'source_visibility','derived_only',
    'public_publication','separate',
    'authority','UNCHANGED'
  );
end;
$$;

revoke all on function public.nayanet_collective_wisdom_for_event(uuid,uuid,text,text,jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_collective_wisdom_for_event(uuid,uuid,text,text,jsonb) to service_role;

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

  if not exists(
    select 1
    from public.nayanet_smart_connect_participation
    where member_id=v_actor
      and status='active'
      and consent_state='explicit'
  ) then
    update public.nayanet_collective_wisdom
    set status='REVOKED'
    where owner_id=v_actor and status='ACTIVE';
  end if;

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
    'status','DISCONNECTED',
    'participation',to_jsonb(v_row),
    'authority','UNCHANGED',
    'collective_wisdom_future_use','REVOKED_WHEN_LAST_EXPLICIT_PARTICIPATION_ENDS'
  );
end;
$$;

revoke all on function public.nayanet_smart_disconnect(text) from public,anon;
grant execute on function public.nayanet_smart_disconnect(text) to authenticated;
