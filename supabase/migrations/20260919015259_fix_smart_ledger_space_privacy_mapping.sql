create or replace function public.nayanet_space_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 perform public.nayanet_record_ledger_event(
  new.owner_member_id,'SMART_SPACE_CREATED','nayanet_spaces',new.id::text,new.created_at,new.owner_member_id,
  case when lower(new.visibility)='shared' then 'SHARED' else 'PRIVATE' end,
  'RECORDED','[]'::jsonb,'{}'::jsonb,
  jsonb_build_object('assessed',false,'base_points',10,'value_engine','NayaNET_V1_STARTING_MODEL'),
  '{}'::jsonb,'[]'::jsonb,
  jsonb_build_object('name',new.name,'purpose',new.purpose,'visibility',new.visibility)
 );
 return new;
end; $$;
