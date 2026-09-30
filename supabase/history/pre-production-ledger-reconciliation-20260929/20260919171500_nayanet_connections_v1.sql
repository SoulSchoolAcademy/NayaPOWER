-- Canonical explicit Connection projection.
-- A Connection is a deliberate saved relationship, not automatic Space membership.
-- Communication authority remains separate.

create table public.nayanet_connections (
  id uuid primary key default gen_random_uuid(),
  owner_member_id uuid not null references public.members(id) on delete cascade,
  connected_member_id uuid not null references public.members(id) on delete cascade,
  status text not null default 'active' check (status in ('active','revoked')),
  source_type text not null default 'space',
  source_space_id uuid null references public.nayanet_spaces(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  revoked_at timestamptz null,
  check (owner_member_id <> connected_member_id),
  unique (owner_member_id, connected_member_id)
);

create index nayanet_connections_owner_status_idx on public.nayanet_connections(owner_member_id,status,created_at desc);
create index nayanet_connections_target_idx on public.nayanet_connections(connected_member_id,status,created_at desc);

alter table public.nayanet_connections enable row level security;

create policy nayanet_connections_owner_read
  on public.nayanet_connections for select to authenticated
  using (owner_member_id = auth.uid());

create or replace function public.nayanet_save_connection(p_target_member_id uuid,p_space_id uuid)
returns jsonb language plpgsql security definer set search_path=public as $$
declare
  v_actor uuid := auth.uid(); v_target public.members; v_space public.nayanet_spaces;
  v_shared boolean; v_conn public.nayanet_connections; v_event_id text; v_event jsonb;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if p_target_member_id is null or p_target_member_id=v_actor then raise exception 'INVALID_CONNECTION_TARGET'; end if;
  select * into v_target from public.members where id=p_target_member_id;
  if v_target.id is null then raise exception 'TARGET_MEMBER_NOT_FOUND'; end if;
  select * into v_space from public.nayanet_spaces where id=p_space_id;
  if v_space.id is null then raise exception 'SPACE_NOT_FOUND'; end if;
  select exists(
    select 1 from public.nayanet_space_members a
    join public.nayanet_space_members b on b.space_id=a.space_id
    where a.space_id=p_space_id and a.member_id=v_actor and a.status='active'
      and b.member_id=p_target_member_id and b.status='active'
  ) into v_shared;
  if not v_shared then raise exception 'CONNECTION_REQUIRES_ACTIVE_SHARED_SPACE'; end if;
  select * into v_conn from public.nayanet_connections
  where owner_member_id=v_actor and connected_member_id=p_target_member_id for update;
  if v_conn.id is not null and v_conn.status='active' then
    return jsonb_build_object('status','ALREADY_CONNECTED','connection',to_jsonb(v_conn));
  end if;
  if v_conn.id is null then
    insert into public.nayanet_connections(owner_member_id,connected_member_id,status,source_type,source_space_id)
    values(v_actor,p_target_member_id,'active','space',p_space_id) returning * into v_conn;
  else
    update public.nayanet_connections set status='active',source_type='space',source_space_id=p_space_id,revoked_at=null,updated_at=now()
    where id=v_conn.id returning * into v_conn;
  end if;
  v_event_id:='connection-save-'||v_conn.id::text||'-'||extract(epoch from v_conn.updated_at)::bigint::text;
  v_event:=jsonb_build_object('event_id',v_event_id,'type','relationship','classification','observation','title','NayaNET Connection saved','content','Authenticated member deliberately saved a person as a Connection from an active shared Space.','source','nayanet-connection','status','active','actor','human','confidence',1,'tags',jsonb_build_array('connection','save','smart-space'),'schema_version','NAYANET_CONNECTION_V1','metadata',jsonb_build_object('connection_id',v_conn.id,'owner_member_id',v_actor,'connected_member_id',p_target_member_id,'source_space_id',p_space_id,'source_type','space'));
  perform public.nayanet_record_cognition_event('NayaNET',v_event,'connection_save','Authenticated member saves a Connection from an active shared Space.','Connection persisted as active.','[]'::jsonb);
  return jsonb_build_object('status','CONNECTED','connection',to_jsonb(v_conn),'event_id',v_event_id);
end;
$$;

create or replace function public.nayanet_revoke_connection(p_target_member_id uuid)
returns jsonb language plpgsql security definer set search_path=public as $$
declare
  v_actor uuid := auth.uid(); v_conn public.nayanet_connections; v_event_id text; v_event jsonb;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into v_conn from public.nayanet_connections where owner_member_id=v_actor and connected_member_id=p_target_member_id for update;
  if v_conn.id is null then raise exception 'CONNECTION_NOT_FOUND'; end if;
  if v_conn.status='revoked' then return jsonb_build_object('status','ALREADY_REVOKED','connection',to_jsonb(v_conn)); end if;
  update public.nayanet_connections set status='revoked',revoked_at=now(),updated_at=now() where id=v_conn.id returning * into v_conn;
  v_event_id:='connection-revoke-'||v_conn.id::text||'-'||extract(epoch from v_conn.revoked_at)::bigint::text;
  v_event:=jsonb_build_object('event_id',v_event_id,'type','relationship','classification','observation','title','NayaNET Connection revoked','content','Authenticated member revoked a saved Connection.','source','nayanet-connection','status','active','actor','human','confidence',1,'tags',jsonb_build_array('connection','revoke'),'schema_version','NAYANET_CONNECTION_V1','metadata',jsonb_build_object('connection_id',v_conn.id,'owner_member_id',v_actor,'connected_member_id',p_target_member_id,'source_space_id',v_conn.source_space_id));
  perform public.nayanet_record_cognition_event('NayaNET',v_event,'connection_revoke','Authenticated member revokes a saved Connection.','Connection persisted as revoked.','[]'::jsonb);
  return jsonb_build_object('status','REVOKED','connection',to_jsonb(v_conn),'event_id',v_event_id);
end;
$$;

revoke all on function public.nayanet_save_connection(uuid,uuid) from public;
grant execute on function public.nayanet_save_connection(uuid,uuid) to authenticated;
revoke all on function public.nayanet_revoke_connection(uuid) from public;
grant execute on function public.nayanet_revoke_connection(uuid) to authenticated;
