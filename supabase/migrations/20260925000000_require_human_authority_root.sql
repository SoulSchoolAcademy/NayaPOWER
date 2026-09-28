create table if not exists public.nayanet_authority_roots (
  user_id uuid primary key references auth.users(id) on delete restrict,
  scope jsonb not null default '{}'::jsonb,
  actions jsonb not null default '[]'::jsonb,
  constraints jsonb not null default '{}'::jsonb,
  status text not null default 'ACTIVE' check (status in ('ACTIVE','REVOKED')),
  evidence jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  revoked_at timestamptz,
  check (jsonb_typeof(scope) = 'object'),
  check (jsonb_typeof(actions) = 'array' and jsonb_array_length(actions) > 0),
  check ((status = 'REVOKED') = (revoked_at is not null))
);

alter table public.nayanet_authority_roots enable row level security;
revoke all on table public.nayanet_authority_roots from anon, authenticated, public;
grant select on table public.nayanet_authority_roots to authenticated;
drop policy if exists "authority root visible to owner" on public.nayanet_authority_roots;
create policy "authority root visible to owner" on public.nayanet_authority_roots for select to authenticated using ((select auth.uid()) = user_id);

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
  v_root public.nayanet_authority_roots;
  v_parent public.nayanet_authority_grants;
  v_parent_id uuid;
  v_action text;
  v_issuer uuid := (select auth.uid());
begin
  if v_issuer is null then
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

  select * into v_root from public.nayanet_authority_roots where user_id = v_issuer and status = 'ACTIVE' limit 1;
  if found then
    if not (v_root.scope @> p_scope) then
      raise exception 'AUTHORITY_ROOT_SCOPE_REQUIRED';
    end if;
    for v_action in select jsonb_array_elements_text(p_actions) loop
      if not (v_root.actions ? v_action) then
        raise exception 'AUTHORITY_ROOT_ACTION_NOT_GRANTED:%', v_action;
      end if;
    end loop;
  else
    if p_parent_authority is null or jsonb_typeof(p_parent_authority) <> 'object' or (p_parent_authority ? 'grant_id') = false then
      raise exception 'AUTHORITY_ROOT_OR_PARENT_REQUIRED';
    end if;
    v_parent_id := (p_parent_authority->>'grant_id')::uuid;
    select * into v_parent from public.nayanet_authority_grants where grant_id = v_parent_id and issuer_id = v_issuer and subject_id = p_subject_id and status = 'ACTIVE' limit 1;
    if not found then
      raise exception 'AUTHORITY_PARENT_NOT_ACTIVE';
    end if;
    if v_parent.expires_at is not null and v_parent.expires_at <= clock_timestamp() then
      raise exception 'AUTHORITY_PARENT_EXPIRED';
    end if;
    if not (v_parent.scope @> p_scope) then
      raise exception 'AUTHORITY_PARENT_SCOPE_REQUIRED';
    end if;
    for v_action in select jsonb_array_elements_text(p_actions) loop
      if not (v_parent.actions ? v_action) then
        raise exception 'AUTHORITY_PARENT_ACTION_NOT_GRANTED:%', v_action;
      end if;
    end loop;
  end if;

  insert into public.nayanet_authority_grants(
    issuer_id,subject_id,source_event_id,mission_id,scope,actions,constraints,issued_at,expires_at,status,evidence,parent_authority
  ) values (
    v_issuer,p_subject_id,p_source_event_id,p_mission_id,p_scope,p_actions,coalesce(p_constraints,'{}'::jsonb),clock_timestamp(),p_expires_at,'ACTIVE',coalesce(p_evidence,'{}'::jsonb),p_parent_authority
  ) returning * into v;
  return v;
end;
$$;

grant execute on function public.nayanet_issue_authority_grant(uuid,text,text,jsonb,jsonb,jsonb,timestamptz,jsonb,jsonb) to authenticated;
revoke execute on function public.nayanet_issue_authority_grant(uuid,text,text,jsonb,jsonb,jsonb,timestamptz,jsonb,jsonb) from anon, public;
