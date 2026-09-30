-- Fix Smart List membership RPC to match the composite-key membership table.
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
