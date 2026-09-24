
-- Smart Connect proof prerequisite: explicit 7-argument cognition recorder for Space join.
create or replace function public.nayanet_join_space(p_space_id uuid)
returns jsonb language plpgsql security definer set search_path=public as $$
declare
  v_member uuid := auth.uid(); v_space public.nayanet_spaces; v_row public.nayanet_space_members; v_event_id text; v_event jsonb;
begin
  if v_member is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into v_space from public.nayanet_spaces where id=p_space_id for share;
  if v_space.id is null then raise exception 'SPACE_NOT_FOUND'; end if;
  if v_space.visibility <> 'shared' and v_space.owner_member_id <> v_member then raise exception 'SPACE_JOIN_NOT_ALLOWED'; end if;
  select * into v_row from public.nayanet_space_members where space_id=p_space_id and member_id=v_member for update;
  if v_row.id is not null and v_row.status='active' then
    return jsonb_build_object('status','ALREADY_MEMBER','membership',to_jsonb(v_row),'space_id',p_space_id,'member_id',v_member);
  end if;
  if v_row.id is null then
    insert into public.nayanet_space_members(space_id,member_id,role,status,joined_at,left_at,source_type,source_id)
    values(p_space_id,v_member,'member','active',now(),null,'direct_join',p_space_id) returning * into v_row;
  else
    update public.nayanet_space_members set status='active',joined_at=now(),left_at=null,source_type='direct_join',source_id=p_space_id,updated_at=now() where id=v_row.id returning * into v_row;
  end if;
  v_event_id:='space-join-'||p_space_id::text||'-'||v_member::text||'-'||extract(epoch from v_row.joined_at)::bigint::text;
  v_event:=jsonb_build_object('event_id',v_event_id,'type','relationship','classification','observation','title','NayaNET Space membership joined','content','Authenticated member joined a shared Smart Space.','source','nayanet-space-membership','status','active','actor','human','confidence',1,'tags',jsonb_build_array('smart-space','membership','join'),'schema_version','NAYANET_SPACE_MEMBERSHIP_V1','metadata',jsonb_build_object('space_id',p_space_id,'member_id',v_member,'role',v_row.role,'status',v_row.status,'source_type',v_row.source_type,'source_id',v_row.source_id));
  perform public.nayanet_record_cognition_event('NayaNET',v_event,'space_join','Authenticated member becomes an active member of the shared Space.','Membership row persisted as active.','[]'::jsonb,null::jsonb);
  return jsonb_build_object('status','JOINED','membership',to_jsonb(v_row),'space_id',p_space_id,'member_id',v_member,'event_id',v_event_id);
end;
$$;
revoke all on function public.nayanet_join_space(uuid) from public;
grant execute on function public.nayanet_join_space(uuid) to authenticated;
