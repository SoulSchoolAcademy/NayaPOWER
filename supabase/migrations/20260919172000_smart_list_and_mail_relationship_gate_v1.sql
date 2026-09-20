-- Smart List is organization over canonical Connections.
create table public.nayanet_smart_lists (
  id uuid primary key default gen_random_uuid(),
  owner_member_id uuid not null references public.members(id) on delete cascade,
  name text not null check (char_length(trim(name)) between 1 and 120),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(owner_member_id,name)
);

create table public.nayanet_smart_list_members (
  list_id uuid not null references public.nayanet_smart_lists(id) on delete cascade,
  connection_id uuid not null references public.nayanet_connections(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key(list_id,connection_id)
);

create index nayanet_smart_lists_owner_idx on public.nayanet_smart_lists(owner_member_id,created_at desc);
create index nayanet_smart_list_members_connection_idx on public.nayanet_smart_list_members(connection_id);

alter table public.nayanet_smart_lists enable row level security;
alter table public.nayanet_smart_list_members enable row level security;

create policy nayanet_smart_lists_owner_all on public.nayanet_smart_lists
  for all to authenticated using(owner_member_id=auth.uid()) with check(owner_member_id=auth.uid());

create policy nayanet_smart_list_members_owner_read on public.nayanet_smart_list_members
  for select to authenticated
  using(exists(select 1 from public.nayanet_smart_lists l where l.id=list_id and l.owner_member_id=auth.uid()));

create or replace function public.nayanet_create_smart_list(p_name text)
returns public.nayanet_smart_lists language plpgsql security definer set search_path=public as $$
declare v public.nayanet_smart_lists;
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;
  if trim(coalesce(p_name,''))='' then raise exception 'LIST_NAME_REQUIRED'; end if;
  insert into public.nayanet_smart_lists(owner_member_id,name)
  values(auth.uid(),trim(p_name))
  on conflict(owner_member_id,name) do update set updated_at=now()
  returning * into v;
  return v;
end;
$$;

create or replace function public.nayanet_add_connection_to_list(p_list_id uuid,p_connection_id uuid)
returns jsonb language plpgsql security definer set search_path=public as $$
declare v_actor uuid:=auth.uid(); v_list public.nayanet_smart_lists; v_conn public.nayanet_connections; v_exists boolean;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into v_list from public.nayanet_smart_lists where id=p_list_id for update;
  if v_list.id is null or v_list.owner_member_id<>v_actor then raise exception 'LIST_NOT_AUTHORIZED'; end if;
  select * into v_conn from public.nayanet_connections where id=p_connection_id for share;
  if v_conn.id is null or v_conn.owner_member_id<>v_actor then raise exception 'CONNECTION_NOT_OWNED'; end if;
  if v_conn.status<>'active' then raise exception 'CONNECTION_NOT_ACTIVE'; end if;
  select exists(select 1 from public.nayanet_smart_list_members where list_id=p_list_id and connection_id=p_connection_id) into v_exists;
  if v_exists then return jsonb_build_object('status','ALREADY_IN_LIST','list_id',p_list_id,'connection_id',p_connection_id); end if;
  insert into public.nayanet_smart_list_members(list_id,connection_id) values(p_list_id,p_connection_id);
  return jsonb_build_object('status','ADDED','list_id',p_list_id,'connection_id',p_connection_id);
end;
$$;

create or replace function public.nayanet_remove_connection_from_list(p_list_id uuid,p_connection_id uuid)
returns jsonb language plpgsql security definer set search_path=public as $$
declare v_actor uuid:=auth.uid(); v_list public.nayanet_smart_lists; v_deleted int;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into v_list from public.nayanet_smart_lists where id=p_list_id for share;
  if v_list.id is null or v_list.owner_member_id<>v_actor then raise exception 'LIST_NOT_AUTHORIZED'; end if;
  delete from public.nayanet_smart_list_members where list_id=p_list_id and connection_id=p_connection_id;
  get diagnostics v_deleted=row_count;
  return jsonb_build_object('status',case when v_deleted=1 then 'REMOVED' else 'NOT_IN_LIST' end,'list_id',p_list_id,'connection_id',p_connection_id);
end;
$$;

revoke all on function public.nayanet_create_smart_list(text) from public;
grant execute on function public.nayanet_create_smart_list(text) to authenticated;
revoke all on function public.nayanet_add_connection_to_list(uuid,uuid) from public;
grant execute on function public.nayanet_add_connection_to_list(uuid,uuid) to authenticated;
revoke all on function public.nayanet_remove_connection_from_list(uuid,uuid) from public;
grant execute on function public.nayanet_remove_connection_from_list(uuid,uuid) to authenticated;

-- Relationship is evaluated before authority for direct Smart Mail.
create or replace function public.nayanet_send_smart_mail_authorized(
  p_sender_id uuid,p_receiver_id uuid,p_body text,p_subject text,p_kind text,p_idempotency_key text,p_project_id text,
  p_policy_id uuid default null,p_experiment_case_id text default null,p_policy_input_hash text default null,p_policy_decision_hash text default null,p_authority_grant_id uuid default null
)
returns jsonb language plpgsql security definer set search_path='' as $$
declare v_authority jsonb; v_result jsonb; v_sender uuid:=auth.uid(); v_mutual boolean;
begin
  if v_sender is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_sender<>p_sender_id then raise exception 'SENDER_IDENTITY_MISMATCH'; end if;
  select exists(
    select 1 from public.nayanet_connections a
    join public.nayanet_connections b on b.owner_member_id=p_receiver_id and b.connected_member_id=p_sender_id and b.status='active'
    where a.owner_member_id=p_sender_id and a.connected_member_id=p_receiver_id and a.status='active'
  ) into v_mutual;
  if not v_mutual then raise exception 'RELATIONSHIP_REQUIRED'; end if;
  v_authority:=public.nayanet_validate_authority_grant(p_authority_grant_id,'smart_mail_send',p_receiver_id::text);
  if coalesce(v_authority->>'status','BLOCKED')<>'AUTHORIZED' then raise exception 'AUTHORITY_REQUIRED: %',coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED'); end if;
  v_result:=public.nayanet_send_smart_mail(p_sender_id,p_receiver_id,p_body,p_subject,p_kind,p_idempotency_key,p_project_id,p_policy_id,p_experiment_case_id,p_policy_input_hash,p_policy_decision_hash);
  if coalesce(v_result->>'status','')='CREATED' then
    update public.nayanet_execution_receipts set
      authority_grant_id=(v_authority->>'grant_id')::uuid,authority_issuer_id=(v_authority->>'issuer_id')::uuid,
      authority_scope=v_authority->'scope',authority_actions=v_authority->'actions',authority_constraints=v_authority->'constraints',
      authority_status_at_execution=v_authority->>'grant_status',authority_source_event_id=v_authority->>'source_event_id',authority_validated_at=clock_timestamp()
    where id=(v_result->>'execution_receipt_id')::uuid;
    update public.v7_mail_messages set metadata=metadata||jsonb_build_object(
      'authority_grant_id',v_authority->>'grant_id','authority_source_event_id',v_authority->>'source_event_id',
      'authority_issuer_id',v_authority->>'issuer_id','relationship_gate','mutual_active_connection')
    where id=(v_result->>'message_id')::uuid;
  end if;
  return v_result||jsonb_build_object('authority_grant_id',v_authority->>'grant_id','relationship_gate','mutual_active_connection');
end;
$$;

revoke all on function public.nayanet_send_smart_mail_authorized(uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid) from public;
grant execute on function public.nayanet_send_smart_mail_authorized(uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid) to authenticated;
