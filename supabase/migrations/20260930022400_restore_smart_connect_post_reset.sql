-- Forward restoration of canonical Smart Connect objects after the 2026-09-27 reset.
-- The original Smart Connect migrations are already recorded as applied, so they
-- will not replay after reset. This migration restores only the canonical seam
-- required by the later consent/revocation hardening migration.
-- It does not rewrite migration history or create a second intelligence store.

create table if not exists public.nayanet_smart_connect_participation (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references public.members(id) on delete cascade,
  door text not null check (door in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps')),
  status text not null default 'active' check (status in ('active','revoked')),
  wisdom_sharing text not null default 'default' check (wisdom_sharing='default'),
  personal_intelligence text not null default 'private' check (personal_intelligence='private'),
  personal_activity text not null default 'private' check (personal_activity='private'),
  identity_visibility text not null default 'private' check (identity_visibility='private'),
  smart_spaces text not null default 'enabled' check (smart_spaces='enabled'),
  external_bindings jsonb not null default '[]'::jsonb,
  consent_state text not null default 'pending' check (consent_state in ('pending','explicit','revoked')),
  connected_at timestamptz not null default now(),
  revoked_at timestamptz null,
  updated_at timestamptz not null default now(),
  unique(member_id,door)
);

create index if not exists nayanet_smart_connect_participation_member_idx
  on public.nayanet_smart_connect_participation(member_id,status,connected_at desc);
create index if not exists nayanet_smart_connect_participation_external_bindings_gin
  on public.nayanet_smart_connect_participation using gin(external_bindings);

alter table public.nayanet_smart_connect_participation enable row level security;
revoke all on table public.nayanet_smart_connect_participation from anon,authenticated;
grant select on table public.nayanet_smart_connect_participation to authenticated;

drop policy if exists smart_connect_participation_owner_read on public.nayanet_smart_connect_participation;
create policy smart_connect_participation_owner_read
on public.nayanet_smart_connect_participation for select to authenticated
using (member_id=(select auth.uid()));

create or replace function public.nayanet_require_explicit_smart_connect_consent()
returns trigger
language plpgsql
security definer
set search_path=''
as $$
begin
  if new.status='active' and new.consent_state is distinct from 'explicit' then
    raise exception 'SMART_CONNECT_CONSENT_REQUIRED';
  end if;
  if new.status='revoked' and new.consent_state is distinct from 'revoked' then
    new.consent_state:='revoked';
  end if;
  if tg_op='UPDATE'
     and new.status='active'
     and new.external_bindings is distinct from old.external_bindings
     and new.consent_state is distinct from 'explicit' then
    raise exception 'SMART_CONNECT_BINDING_CONSENT_REQUIRED';
  end if;
  return new;
end;
$$;

drop trigger if exists nayanet_smart_connect_consent_boundary
  on public.nayanet_smart_connect_participation;
create trigger nayanet_smart_connect_consent_boundary
before insert or update on public.nayanet_smart_connect_participation
for each row execute function public.nayanet_require_explicit_smart_connect_consent();

create or replace function public.nayanet_smart_connect(p_door text)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
begin
  raise exception 'SMART_CONNECT_CONSENT_REQUIRED';
end;
$$;

create or replace function public.nayanet_smart_connect(p_door text,p_consent_state text)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_actor uuid:=auth.uid();
  v_door text:=lower(trim(p_door));
  v_consent text:=lower(trim(coalesce(p_consent_state,'')));
  v_row public.nayanet_smart_connect_participation;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_door not in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps') then
    raise exception 'SMART_CONNECT_DOOR_INVALID';
  end if;
  if v_consent is distinct from 'explicit' then
    raise exception 'SMART_CONNECT_CONSENT_REQUIRED';
  end if;

  select * into v_row
  from public.nayanet_smart_connect_participation
  where member_id=v_actor and door=v_door
  for update;

  if v_row.id is not null and v_row.status='active' then
    if v_row.consent_state is distinct from 'explicit' then
      update public.nayanet_smart_connect_participation
      set consent_state='explicit',updated_at=now()
      where id=v_row.id
      returning * into v_row;
    end if;
    return jsonb_build_object(
      'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
      'status','ALREADY_CONNECTED',
      'participation',to_jsonb(v_row),
      'authority','UNCHANGED',
      'publication','NOT_GRANTED',
      'consent_state','explicit',
      'identity','PRIVATE_BY_DEFAULT',
      'wisdom_sharing','DEFAULT'
    );
  end if;

  if v_row.id is null then
    insert into public.nayanet_smart_connect_participation(member_id,door,consent_state)
    values(v_actor,v_door,'explicit')
    returning * into v_row;
  else
    update public.nayanet_smart_connect_participation
    set status='active',
        consent_state='explicit',
        wisdom_sharing='default',
        personal_intelligence='private',
        personal_activity='private',
        identity_visibility='private',
        smart_spaces='enabled',
        revoked_at=null,
        updated_at=now()
    where id=v_row.id
    returning * into v_row;
  end if;

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
    'status','CONNECTED',
    'participation',to_jsonb(v_row),
    'authority','UNCHANGED',
    'publication','NOT_GRANTED',
    'consent_state','explicit',
    'identity','PRIVATE_BY_DEFAULT',
    'wisdom_sharing','DEFAULT'
  );
end;
$$;

revoke all on function public.nayanet_smart_connect(text) from public,anon;
grant execute on function public.nayanet_smart_connect(text) to authenticated;
revoke all on function public.nayanet_smart_connect(text,text) from public,anon;
grant execute on function public.nayanet_smart_connect(text,text) to authenticated;

create table if not exists public.nayanet_collective_wisdom (
  id uuid primary key default gen_random_uuid(),
  source_event_id uuid not null references public.nayanet_cognition_events(id) on delete cascade,
  owner_id uuid not null references public.members(id) on delete cascade,
  wisdom_claim text not null,
  topic text not null default 'GENERAL',
  provenance jsonb not null default '{}'::jsonb,
  epistemic_state text not null default 'CANDIDATE' check(epistemic_state in ('CANDIDATE','VERIFIED')),
  status text not null default 'ACTIVE' check(status in ('ACTIVE','REVOKED')),
  identity_visibility text not null default 'private' check(identity_visibility='private'),
  source_visibility text not null default 'derived_only' check(source_visibility='derived_only'),
  public_publication text not null default 'separate' check(public_publication='separate'),
  created_at timestamptz not null default now(),
  unique(source_event_id)
);

create index if not exists nayanet_collective_wisdom_topic_idx
  on public.nayanet_collective_wisdom(topic,created_at desc);
alter table public.nayanet_collective_wisdom enable row level security;
revoke all on table public.nayanet_collective_wisdom from anon,authenticated;
