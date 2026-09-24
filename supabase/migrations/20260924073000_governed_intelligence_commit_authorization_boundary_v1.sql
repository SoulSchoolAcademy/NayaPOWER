[Reading 121 lines from start (total: 121 lines, 0 remaining)]

-- Govern the existing intelligence_commit persistence boundary with the existing authority grant model.
-- No new store or authority model. Existing calls remain compatible because the new
-- authorization argument is optional except for the canonical intelligence.capture action.

create or replace function public.nayanet_record_cognition_event(
  p_project_id text,
  p_event jsonb,
  p_action text default 'record_intelligence',
  p_expected_result text default null,
  p_observed_result text default null,
  p_learning jsonb default '[]'::jsonb,
  p_execution_authorization jsonb default null
) returns jsonb
language plpgsql
set search_path to 'public'
as $function$
declare
  v_event public.nayanet_cognition_events;
  v_state public.nayanet_project_cognition_state;
  v_receipt public.nayanet_execution_receipts;
  v_receipt_revision bigint;
  v_authority jsonb;
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;

  if p_action = 'intelligence.capture' then
    if p_execution_authorization is null then
      raise exception 'EXECUTION_AUTHORIZATION_REQUIRED';
    end if;
    v_authority := public.nayanet_validate_authority_grant(
      (p_execution_authorization->>'authority_id')::uuid,
      'intelligence_commit',
      p_project_id
    );
    if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
      raise exception 'AUTHORITY_REQUIRED: %', coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
    end if;
    if coalesce(p_execution_authorization->>'actor_id','') <> auth.uid()::text then
      raise exception 'EXECUTION_AUTHORIZATION_ACTOR_MISMATCH';
    end if;
    if coalesce(p_execution_authorization->>'permission','') <> 'intelligence_commit' then
      raise exception 'EXECUTION_AUTHORIZATION_PERMISSION_MISMATCH';
    end if;
    if coalesce(p_execution_authorization->>'governance_state','') <> 'AUTHORIZED' then
      raise exception 'EXECUTION_AUTHORIZATION_NOT_AUTHORIZED';
    end if;
  end if;

  perform pg_advisory_xact_lock(hashtext(auth.uid()::text || ':' || p_project_id));

  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata
  )
  values(
    auth.uid(),p_project_id,p_event->>'event_id',coalesce((p_event->>'created_at')::timestamptz,now()),now(),
    coalesce(p_event->>'type','intelligence'),coalesce(p_event->>'classification','observation'),p_event->>'title',
    coalesce(p_event->>'content',''),coalesce(p_event->>'source','nayanet-hub'),coalesce(p_event->>'status','active'),
    coalesce(p_event->>'actor','human'),coalesce((p_event->>'confidence')::numeric,1),coalesce(p_event->'tags','[]'::jsonb),
    p_event->>'parent_event_id',coalesce(p_event->>'source_hash',''),coalesce(p_event->>'schema_version','1.0.0'),
    coalesce(p_event->>'receipt_id',''),coalesce(p_event->'metadata','{}'::jsonb)
  )
  on conflict (user_id,project_id,event_id) do update
    set updated_at=now(),status=excluded.status,metadata=excluded.metadata
  returning * into v_event;

  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(auth.uid(),p_project_id,0,jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at,'successor',null),'READY')
  on conflict (user_id,project_id) do nothing;

  update public.nayanet_project_cognition_state
     set revision=revision+1,
         state=coalesce(state,'{}'::jsonb)||jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at),
         status='IN_PROGRESS',
         updated_at=now()
   where user_id=auth.uid() and project_id=p_project_id
   returning * into v_state;

  select coalesce(max(revision),0)+1
    into v_receipt_revision
    from public.nayanet_execution_receipts
   where user_id=auth.uid() and project_id=p_project_id;

  insert into public.nayanet_execution_receipts(
    user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning,
    authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints,
    authority_status_at_execution,authority_source_event_id,authority_validated_at
  )
  values(
    auth.uid(),p_project_id,v_receipt_revision,p_action,p_expected_result,p_observed_result,'SUCCESS',
    jsonb_build_object(
      'event_id',v_event.event_id,
      'source_hash',v_event.source_hash,
      'created_at',v_event.created_at,
      'execution_authorization',coalesce(p_execution_authorization,'null'::jsonb)
    ),
    coalesce(p_learning,'[]'::jsonb),
    case when v_authority is null then null else (v_authority->>'grant_id')::uuid end,
    case when v_authority is null then null else (v_authority->>'issuer_id')::uuid end,
    case when v_authority is null then null else v_authority->'scope' end,
    case when v_authority is null then null else v_authority->'actions' end,
    case when v_authority is null then null else v_authority->'constraints' end,
    case when v_authority is null then null else v_authority->>'grant_status' end,
    case when v_authority is null then null else v_authority->>'source_event_id' end,
    case when v_authority is null then null else clock_timestamp() end
  )
  returning * into v_receipt;

  update public.nayanet_cognition_events
     set receipt_id=v_receipt.id::text,
         updated_at=now()
   where id=v_event.id
     and user_id=auth.uid()
     and project_id=p_project_id
  returning * into v_event;

  return jsonb_build_object('event',to_jsonb(v_event),'state',to_jsonb(v_state),'receipt',to_jsonb(v_receipt));
end;
$function$;

grant execute on function public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb,jsonb) to authenticated;
revoke execute on function public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb,jsonb) from anon, public;

[executed on device: DESKTOP-OJ712N5 (97813f8c-e057-47af-82b6-89e3bc067f5c)]
-- Preserve the legacy six-argument call surface, but route it through the governed
-- seven-argument boundary so intelligence.capture cannot bypass authorization.
create or replace function public.nayanet_record_cognition_event(
  p_project_id text,
  p_event jsonb,
  p_action text default 'record_intelligence',
  p_expected_result text default null,
  p_observed_result text default null,
  p_learning jsonb default '[]'::jsonb
) returns jsonb
language sql
set search_path to 'public'
as $function$
  select public.nayanet_record_cognition_event(
    p_project_id,p_event,p_action,p_expected_result,p_observed_result,p_learning,null::jsonb
  );
$function$;

grant execute on function public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb) to authenticated;
revoke execute on function public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb) from anon, public;
