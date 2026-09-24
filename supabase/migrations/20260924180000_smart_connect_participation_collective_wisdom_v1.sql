create table if not exists public.nayanet_smart_connect_participation (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references public.members(id) on delete cascade,
  door text not null check (door in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps')),
  status text not null default 'active' check (status in ('active','revoked')),
  wisdom_sharing text not null default 'default' check (wisdom_sharing = 'default'),
  personal_intelligence text not null default 'private' check (personal_intelligence = 'private'),
  personal_activity text not null default 'private' check (personal_activity = 'private'),
  identity_visibility text not null default 'private' check (identity_visibility = 'private'),
  smart_spaces text not null default 'enabled' check (smart_spaces = 'enabled'),
  connected_at timestamptz not null default now(),
  revoked_at timestamptz null,
  updated_at timestamptz not null default now(),
  unique (member_id, door)
);
create index if not exists nayanet_smart_connect_participation_member_idx on public.nayanet_smart_connect_participation(member_id,status,connected_at desc);
alter table public.nayanet_smart_connect_participation enable row level security;
revoke all on table public.nayanet_smart_connect_participation from anon, authenticated;
grant select on public.nayanet_smart_connect_participation to authenticated;
drop policy if exists smart_connect_participation_owner_read on public.nayanet_smart_connect_participation;
create policy smart_connect_participation_owner_read on public.nayanet_smart_connect_participation for select to authenticated using (member_id=(select auth.uid()));

create or replace function public.nayanet_smart_connect(p_door text)
returns jsonb language plpgsql security definer set search_path='' as $
declare v_actor uuid:=auth.uid(); v_door text:=lower(trim(p_door)); v_row public.nayanet_smart_connect_participation;
begin
 if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
 if v_door not in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps') then raise exception 'SMART_CONNECT_DOOR_INVALID'; end if;
 insert into public.nayanet_smart_connect_participation(member_id,door) values(v_actor,v_door)
 on conflict(member_id,door) do update set status='active',wisdom_sharing='default',personal_intelligence='private',personal_activity='private',identity_visibility='private',smart_spaces='enabled',revoked_at=null,updated_at=now()
 returning * into v_row;
 return jsonb_build_object('schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1','status','CONNECTED','participation',to_jsonb(v_row),'authority','UNCHANGED','publication','NOT_GRANTED','identity','PRIVATE_BY_DEFAULT','wisdom_sharing','DEFAULT');
end; $$;
create or replace function public.nayanet_smart_disconnect(p_door text)
returns jsonb language plpgsql security definer set search_path='' as $
declare v_actor uuid:=auth.uid(); v_door text:=lower(trim(p_door)); v_row public.nayanet_smart_connect_participation;
begin
 if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
 update public.nayanet_smart_connect_participation set status='revoked',revoked_at=now(),updated_at=now() where member_id=v_actor and door=v_door returning * into v_row;
 if v_row.id is null then raise exception 'SMART_CONNECT_PARTICIPATION_NOT_FOUND'; end if;
 return jsonb_build_object('schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1','status','DISCONNECTED','participation',to_jsonb(v_row),'authority','UNCHANGED');
end; $$;
revoke all on function public.nayanet_smart_connect(text) from public; grant execute on function public.nayanet_smart_connect(text) to authenticated;
revoke all on function public.nayanet_smart_disconnect(text) from public; grant execute on function public.nayanet_smart_disconnect(text) to authenticated;

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
create index if not exists nayanet_collective_wisdom_topic_idx on public.nayanet_collective_wisdom(topic,created_at desc);
alter table public.nayanet_collective_wisdom enable row level security;
revoke all on table public.nayanet_collective_wisdom from anon,authenticated;
grant select on public.nayanet_collective_wisdom to authenticated;
drop policy if exists collective_wisdom_member_read on public.nayanet_collective_wisdom;
revoke select on public.nayanet_collective_wisdom from authenticated;
create view public.nayanet_collective_wisdom_feed with(security_invoker=true) as
select id,source_event_id,wisdom_claim,topic,epistemic_state,status,identity_visibility,source_visibility,public_publication,created_at
from public.nayanet_collective_wisdom where status='ACTIVE';
grant select on public.nayanet_collective_wisdom_feed to authenticated;

create or replace function public.nayanet_collective_wisdom_for_event(p_source_event_id uuid,p_owner_id uuid,p_wisdom_claim text,p_topic text,p_provenance jsonb)
returns jsonb language plpgsql security definer set search_path='' as $
declare v_participation boolean; v_row public.nayanet_collective_wisdom;
begin
 select exists(select 1 from public.nayanet_smart_connect_participation where member_id=p_owner_id and status='active' and wisdom_sharing='default') into v_participation;
 if not v_participation then raise exception 'SMART_CONNECT_PARTICIPATION_REQUIRED'; end if;
 if nullif(trim(p_wisdom_claim),'') is null then raise exception 'COLLECTIVE_WISDOM_CLAIM_REQUIRED'; end if;
 insert into public.nayanet_collective_wisdom(source_event_id,owner_id,wisdom_claim,topic,provenance)
 values(p_source_event_id,p_owner_id,left(trim(p_wisdom_claim),4000),coalesce(nullif(trim(p_topic),''),'GENERAL'),coalesce(p_provenance,'{}'::jsonb)-'identity'-'owner_id'-'raw_content')
 on conflict(source_event_id) do update set wisdom_claim=excluded.wisdom_claim,topic=excluded.topic,provenance=excluded.provenance returning * into v_row;
 return jsonb_build_object('schema','NAYANET_COLLECTIVE_WISDOM_V1','status','CONTRIBUTED','collective_wisdom_id',v_row.id,'source_event_id',v_row.source_event_id,'identity_visibility','private','source_visibility','derived_only','public_publication','separate');
end; $$;
revoke all on function public.nayanet_collective_wisdom_for_event(uuid,uuid,text,text,jsonb) from public;
grant execute on function public.nayanet_collective_wisdom_for_event(uuid,uuid,text,text,jsonb) to service_role;