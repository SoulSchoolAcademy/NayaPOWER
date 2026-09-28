-- Repair Smart Connect Smart List cognition receipt overloads.
-- Existing Smart List persistence and ownership boundaries are preserved.
create or replace function public.nayanet_create_smart_list(p_name text)
returns public.nayanet_smart_lists language plpgsql security definer set search_path=public as $$
declare v_actor uuid:=auth.uid(); v_list public.nayanet_smart_lists; v_event_id text; v_event jsonb;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if trim(coalesce(p_name,''))='' then raise exception 'LIST_NAME_REQUIRED'; end if;
  select * into v_list from public.nayanet_smart_lists where owner_member_id=v_actor and name=trim(p_name) for update;
  if v_list.id is not null then return v_list; end if;
  insert into public.nayanet_smart_lists(owner_member_id,name) values(v_actor,trim(p_name)) returning * into v_list;
  v_event_id:='list-create-'||v_list.id::text;
  v_event:=jsonb_build_object('event_id',v_event_id,'type','organization','classification','observation','title','NayaNET Smart List created','content','Authenticated member created an owned Smart List.','source','nayanet-smart-list','status','active','actor','human','confidence',1,'tags',jsonb_build_array('smart-list','create'),'schema_version','NAYANET_SMART_LIST_V1','metadata',jsonb_build_object('action','create_smart_list','list_id',v_list.id,'owner_member_id',v_actor));
  perform public.nayanet_record_cognition_event('NayaNET',v_event,'smart_list_create','Owned Smart List created through the canonical Hub action boundary.','Smart List row persisted with a canonical cognition receipt.','[]'::jsonb,null::jsonb);
  return v_list;
end;
$$;
create or replace function public.nayanet_add_connection_to_list(p_list_id uuid,p_connection_id uuid)
returns jsonb language plpgsql security definer set search_path=public as $$
declare v_actor uuid:=auth.uid(); v_list public.nayanet_smart_lists; v_conn public.nayanet_connections; v_exists boolean; v_event_id text; v_event jsonb;
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
  v_event_id:='list-add-'||p_list_id::text||'-'||p_connection_id::text;
  v_event:=jsonb_build_object('event_id',v_event_id,'type','organization','classification','observation','title','NayaNET Connection added to Smart List','content','Authenticated member organized an active Connection into a Smart List.','source','nayanet-smart-list','status','active','actor','human','confidence',1,'tags',jsonb_build_array('smart-list','connection','add'),'schema_version','NAYANET_SMART_LIST_V1','metadata',jsonb_build_object('list_id',p_list_id,'connection_id',p_connection_id,'owner_member_id',v_actor));
  perform public.nayanet_record_cognition_event('NayaNET',v_event,'smart_list_add','Active Connection added to an owned Smart List.','List membership persisted.','[]'::jsonb,null::jsonb);
  return jsonb_build_object('status','ADDED','list_id',p_list_id,'connection_id',p_connection_id,'event_id',v_event_id);
end;
$$;
create or replace function public.nayanet_remove_connection_from_list(p_list_id uuid,p_connection_id uuid)
returns jsonb language plpgsql security definer set search_path=public as $$
declare v_actor uuid:=auth.uid(); v_list public.nayanet_smart_lists; v_deleted int; v_event_id text; v_event jsonb;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into v_list from public.nayanet_smart_lists where id=p_list_id for share;
  if v_list.id is null or v_list.owner_member_id<>v_actor then raise exception 'LIST_NOT_AUTHORIZED'; end if;
  delete from public.nayanet_smart_list_members where list_id=p_list_id and connection_id=p_connection_id;
  get diagnostics v_deleted=row_count;
  if v_deleted=0 then return jsonb_build_object('status','NOT_IN_LIST','list_id',p_list_id,'connection_id',p_connection_id); end if;
  v_event_id:='list-remove-'||p_list_id::text||'-'||p_connection_id::text;
  v_event:=jsonb_build_object('event_id',v_event_id,'type','organization','classification','observation','title','NayaNET Connection removed from Smart List','content','Authenticated member removed a Connection from a Smart List without revoking the Connection.','source','nayanet-smart-list','status','active','actor','human','confidence',1,'tags',jsonb_build_array('smart-list','connection','remove'),'schema_version','NAYANET_SMART_LIST_V1','metadata',jsonb_build_object('list_id',p_list_id,'connection_id',p_connection_id,'owner_member_id',v_actor));
  perform public.nayanet_record_cognition_event('NayaNET',v_event,'smart_list_remove','Connection removed from an owned Smart List.','List membership removed; Connection remains canonical.','[]'::jsonb,null::jsonb);
  return jsonb_build_object('status','REMOVED','list_id',p_list_id,'connection_id',p_connection_id,'event_id',v_event_id);
end;
$$;
revoke all on function public.nayanet_create_smart_list(text) from public;
grant execute on function public.nayanet_create_smart_list(text) to authenticated;
revoke all on function public.nayanet_add_connection_to_list(uuid,uuid) from public;
grant execute on function public.nayanet_add_connection_to_list(uuid,uuid) to authenticated;
revoke all on function public.nayanet_remove_connection_from_list(uuid,uuid) from public;
grant execute on function public.nayanet_remove_connection_from_list(uuid,uuid) to authenticated;
