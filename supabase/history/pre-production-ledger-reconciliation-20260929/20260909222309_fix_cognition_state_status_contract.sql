-- Mirrors production migration 20260909222309_fix_cognition_state_status_contract.
create or replace function public.nayanet_initialize_cognition(p_project_id text, p_state jsonb default '{}'::jsonb)
returns public.nayanet_project_cognition_state language plpgsql set search_path to public as $$
declare v public.nayanet_project_cognition_state;
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;
  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(auth.uid(),p_project_id,0,coalesce(p_state,'{}'::jsonb),'READY')
  on conflict (user_id,project_id) do nothing;
  select * into v from public.nayanet_project_cognition_state where user_id=auth.uid() and project_id=p_project_id;
  return v;
end;
$$;

create or replace function public.nayanet_record_cognition_event(p_project_id text,p_event jsonb,p_action text default 'record_intelligence',p_expected_result text default null,p_observed_result text default null,p_learning jsonb default '[]'::jsonb)
returns jsonb language plpgsql set search_path to public as $$
declare v_event public.nayanet_cognition_events; v_state public.nayanet_project_cognition_state; v_receipt public.nayanet_execution_receipts;
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;
  insert into public.nayanet_cognition_events(user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata)
  values(auth.uid(),p_project_id,p_event->>'event_id',coalesce((p_event->>'created_at')::timestamptz,now()),now(),coalesce(p_event->>'type','intelligence'),coalesce(p_event->>'classification','observation'),p_event->>'title',coalesce(p_event->>'content',''),coalesce(p_event->>'source','nayanet-hub'),coalesce(p_event->>'status','active'),coalesce(p_event->>'actor','human'),coalesce((p_event->>'confidence')::numeric,1),coalesce(p_event->'tags','[]'::jsonb),p_event->>'parent_event_id',coalesce(p_event->>'source_hash',''),coalesce(p_event->>'schema_version','1.0.0'),coalesce(p_event->>'receipt_id',''),coalesce(p_event->'metadata','{}'::jsonb))
  on conflict (user_id,project_id,event_id) do update set updated_at=now(),status=excluded.status,metadata=excluded.metadata returning * into v_event;
  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(auth.uid(),p_project_id,0,jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at,'successor',null),'READY')
  on conflict (user_id,project_id) do nothing;
  update public.nayanet_project_cognition_state set revision=revision+1,state=coalesce(state,'{}'::jsonb)||jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at),status='IN_PROGRESS',updated_at=now() where user_id=auth.uid() and project_id=p_project_id returning * into v_state;
  insert into public.nayanet_execution_receipts(user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning)
  values(auth.uid(),p_project_id,v_state.revision,p_action,p_expected_result,p_observed_result,'SUCCESS',jsonb_build_object('event_id',v_event.event_id,'source_hash',v_event.source_hash,'created_at',v_event.created_at),coalesce(p_learning,'[]'::jsonb)) returning * into v_receipt;
  return jsonb_build_object('event',to_jsonb(v_event),'state',to_jsonb(v_state),'receipt',to_jsonb(v_receipt));
end;
$$;
