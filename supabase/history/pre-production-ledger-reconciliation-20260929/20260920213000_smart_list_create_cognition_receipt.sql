-- Smart List creation participates in the canonical cognition -> receipt -> ledger chain.
create or replace function public.nayanet_create_smart_list(p_name text)
returns public.nayanet_smart_lists
language plpgsql
security definer
set search_path=public
as $function$
declare
  v_actor uuid:=auth.uid();
  v_list public.nayanet_smart_lists;
  v_event_id text;
  v_event jsonb;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if trim(coalesce(p_name,''))='' then raise exception 'LIST_NAME_REQUIRED'; end if;

  select * into v_list
  from public.nayanet_smart_lists
  where owner_member_id=v_actor and name=trim(p_name)
  for update;

  if v_list.id is not null then
    return v_list;
  end if;

  insert into public.nayanet_smart_lists(owner_member_id,name)
  values(v_actor,trim(p_name))
  returning * into v_list;

  v_event_id:='list-create-'||v_list.id::text;
  v_event:=jsonb_build_object(
    'event_id',v_event_id,
    'type','organization',
    'classification','observation',
    'title','NayaNET Smart List created',
    'content','Authenticated member created an owned Smart List.',
    'source','nayanet-smart-list',
    'status','active',
    'actor','human',
    'confidence',1,
    'tags',jsonb_build_array('smart-list','create'),
    'schema_version','NAYANET_SMART_LIST_V1',
    'metadata',jsonb_build_object('action','create_smart_list','list_id',v_list.id,'owner_member_id',v_actor)
  );
  perform public.nayanet_record_cognition_event(
    'NayaNET',
    v_event,
    'smart_list_create',
    'Owned Smart List created through the canonical Hub action boundary.',
    'Smart List row persisted with a canonical cognition receipt.',
    '[]'::jsonb
  );
  return v_list;
end;
$function$;
