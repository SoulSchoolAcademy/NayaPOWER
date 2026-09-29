-- Harden Smart Connect participation replay semantics without changing the authority model.
-- Active replay is a no-op; revoked replay is a no-op.
-- Reconnect after revocation remains an explicit state transition.
create or replace function public.nayanet_smart_connect(p_door text)
returns jsonb
language plpgsql
security definer
set search_path to ''
as $function$
declare
  v_actor uuid := auth.uid();
  v_door text := lower(trim(p_door));
  v_row public.nayanet_smart_connect_participation;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_door not in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps') then
    raise exception 'SMART_CONNECT_DOOR_INVALID';
  end if;

  select *
    into v_row
    from public.nayanet_smart_connect_participation
   where member_id=v_actor and door=v_door
   for update;

  if v_row.id is not null and v_row.status='active' then
    return jsonb_build_object(
      'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
      'status','ALREADY_CONNECTED',
      'participation',to_jsonb(v_row),
      'authority','UNCHANGED',
      'publication','NOT_GRANTED',
      'identity','PRIVATE_BY_DEFAULT',
      'wisdom_sharing','DEFAULT'
    );
  end if;

  if v_row.id is null then
    insert into public.nayanet_smart_connect_participation(member_id,door)
    values(v_actor,v_door)
    returning * into v_row;
  else
    update public.nayanet_smart_connect_participation
       set status='active',
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
    'identity','PRIVATE_BY_DEFAULT',
    'wisdom_sharing','DEFAULT'
  );
end;
$function$;

create or replace function public.nayanet_smart_disconnect(p_door text)
returns jsonb
language plpgsql
security definer
set search_path to ''
as $function$
declare
  v_actor uuid := auth.uid();
  v_door text := lower(trim(p_door));
  v_row public.nayanet_smart_connect_participation;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_door not in ('github_app','mcp','rest_openapi','webhooks','sdk','a2a','mcp_apps') then
    raise exception 'SMART_CONNECT_DOOR_INVALID';
  end if;

  select *
    into v_row
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
         revoked_at=now(),
         updated_at=now()
   where id=v_row.id
   returning * into v_row;

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_PARTICIPATION_V1',
    'status','DISCONNECTED',
    'participation',to_jsonb(v_row),
    'authority','UNCHANGED'
  );
end;
$function$;

revoke all on function public.nayanet_smart_connect(text) from public;
grant execute on function public.nayanet_smart_connect(text) to authenticated;
revoke all on function public.nayanet_smart_disconnect(text) from public;
grant execute on function public.nayanet_smart_disconnect(text) to authenticated;