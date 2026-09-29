-- Restore the governed authority-grant mutation boundary without weakening issuer ownership.
-- The grant table remains non-insertable to authenticated clients; issuance executes
-- through the SECURITY DEFINER RPC after enforcing that the source event belongs to auth.uid().

create or replace function public.nayanet_issue_authority_grant(
  p_subject_id uuid,
  p_source_event_id text,
  p_mission_id text,
  p_scope jsonb,
  p_actions jsonb,
  p_constraints jsonb default '{}'::jsonb,
  p_expires_at timestamptz default null,
  p_evidence jsonb default '{}'::jsonb,
  p_parent_authority jsonb default null
)
returns public.nayanet_authority_grants
language plpgsql
security definer
set search_path = ''
as $$
declare
  v public.nayanet_authority_grants;
begin
  if (select auth.uid()) is null then
    raise exception 'AUTH_REQUIRED';
  end if;

  if p_subject_id is null or p_source_event_id is null or btrim(p_source_event_id) = '' then
    raise exception 'AUTHORITY_GRANT_REQUIRED_FIELDS';
  end if;

  if p_mission_id is null or btrim(p_mission_id) = '' then
    raise exception 'AUTHORITY_GRANT_MISSION_REQUIRED';
  end if;

  if jsonb_typeof(p_scope) <> 'object' then
    raise exception 'AUTHORITY_GRANT_SCOPE_INVALID';
  end if;

  if jsonb_typeof(p_actions) <> 'array' or jsonb_array_length(p_actions) = 0 then
    raise exception 'AUTHORITY_GRANT_ACTIONS_REQUIRED';
  end if;

  if p_expires_at is not null and p_expires_at <= clock_timestamp() then
    raise exception 'AUTHORITY_GRANT_EXPIRES_IN_PAST';
  end if;

  if not exists (
    select 1
    from public.nayanet_cognition_events
    where event_id = p_source_event_id
      and user_id = (select auth.uid())
  ) then
    raise exception 'AUTHORITY_SOURCE_NOT_OWNED';
  end if;

  insert into public.nayanet_authority_grants(
    issuer_id,
    subject_id,
    source_event_id,
    mission_id,
    scope,
    actions,
    constraints,
    issued_at,
    expires_at,
    status,
    evidence,
    parent_authority
  )
  values (
    (select auth.uid()),
    p_subject_id,
    p_source_event_id,
    p_mission_id,
    p_scope,
    p_actions,
    coalesce(p_constraints, '{}'::jsonb),
    clock_timestamp(),
    p_expires_at,
    'ACTIVE',
    coalesce(p_evidence, '{}'::jsonb),
    p_parent_authority
  )
  returning * into v;

  return v;
end;
$$;

grant execute on function public.nayanet_issue_authority_grant(
  uuid,text,text,jsonb,jsonb,jsonb,timestamptz,jsonb,jsonb
) to authenticated;

revoke execute on function public.nayanet_issue_authority_grant(
  uuid,text,text,jsonb,jsonb,jsonb,timestamptz,jsonb,jsonb
) from anon, public;
