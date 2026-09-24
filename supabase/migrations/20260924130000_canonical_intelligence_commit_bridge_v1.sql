-- Stream B boundary correction: intelligence is an automatic flow.
-- Connection/participation consent controls whether a node's wisdom enters the network.
-- Authority is reserved for consequential execution/publication boundaries.
create or replace function public.nayanet_canonical_intelligence_capture(
  p_actor_id uuid,p_project_id text,p_event jsonb,p_expected_result text,p_observed_result text,
  p_learning jsonb default '[]'::jsonb
) returns jsonb
language plpgsql security definer set search_path to 'public'
as $function$
declare v_event public.nayanet_cognition_events; v_state public.nayanet_project_cognition_state;
  v_receipt public.nayanet_execution_receipts; v_receipt_revision bigint;
begin
  if coalesce(current_setting('request.jwt.claim.role', true), '') <> 'service_role' then
    raise exception 'CANONICAL_INTELLIGENCE_CAPTURE_SERVICE_ROLE_REQUIRED';
  end if;
  if p_actor_id is null then raise exception 'INTELLIGENCE_ACTOR_REQUIRED'; end if;
  if p_project_id is null or trim(p_project_id) = '' then raise exception 'INTELLIGENCE_PROJECT_REQUIRED'; end if;
  if p_event is null or jsonb_typeof(p_event) <> 'object' then raise exception 'INTELLIGENCE_EVENT_REQUIRED'; end if;
  perform pg_advisory_xact_lock(hashtext(p_actor_id::text || ':' || p_project_id));
  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata
  ) values(
    p_actor_id,p_project_id,p_event->>'event_id',coalesce((p_event->>'created_at')::timestamptz,now()),now(),
    coalesce(p_event->>'type','intelligence'),coalesce(p_event->>'classification','observation'),p_event->>'title',
    coalesce(p_event->>'content',''),coalesce(p_event->>'source','nayanet-hub'),coalesce(p_event->>'status','active'),
    coalesce(p_event->>'actor','naya'),coalesce((p_event->>'confidence')::numeric,1),coalesce(p_event->'tags','[]'::jsonb),
    p_event->>'parent_event_id',coalesce(p_event->>'source_hash',''),coalesce(p_event->>'schema_version','1.0.0'),
    coalesce(p_event->>'receipt_id',''),coalesce(p_event->'metadata','{}'::jsonb)
  ) on conflict (user_id,project_id,event_id) do update
    set updated_at=now(),status=excluded.status,metadata=excluded.metadata returning * into v_event;
  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(p_actor_id,p_project_id,0,jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at,'successor',null),'READY')
  on conflict (user_id,project_id) do nothing;
  update public.nayanet_project_cognition_state set revision=revision+1,
    state=coalesce(state,'{}'::jsonb)||jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at),
    status='IN_PROGRESS',updated_at=now()
    where user_id=p_actor_id and project_id=p_project_id returning * into v_state;
  select coalesce(max(revision),0)+1 into v_receipt_revision
    from public.nayanet_execution_receipts where user_id=p_actor_id and project_id=p_project_id;
  insert into public.nayanet_execution_receipts(
    user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning,
    authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints,
    authority_status_at_execution,authority_source_event_id,authority_validated_at
  ) values(
    p_actor_id,p_project_id,v_receipt_revision,'intelligence.capture',p_expected_result,p_observed_result,'SUCCESS',
    jsonb_build_object('event_id',v_event.event_id,'source_hash',v_event.source_hash,'created_at',v_event.created_at,
      'verification_boundary','automatic-intelligence-flow-v1','authority_required',false),
    coalesce(p_learning,'[]'::jsonb),null,null,null,null,null,null,null
  ) returning * into v_receipt;
  update public.nayanet_cognition_events set receipt_id=v_receipt.id::text,updated_at=now()
    where id=v_event.id and user_id=p_actor_id and project_id=p_project_id returning * into v_event;
  return jsonb_build_object('event',to_jsonb(v_event),'state',to_jsonb(v_state),'receipt',to_jsonb(v_receipt));
end;
$function$;
revoke all on function public.nayanet_canonical_intelligence_capture(uuid,text,jsonb,text,text,jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_canonical_intelligence_capture(uuid,text,jsonb,text,text,jsonb) to service_role;
comment on function public.nayanet_canonical_intelligence_capture(uuid,text,jsonb,text,text,jsonb)
is 'Automatic intelligence capture/persistence seam. It does not require execution authority. Connection/participation consent and privacy rules govern source inclusion; authority remains for consequential execution/publication boundaries.';

create or replace function public.nayanet_record_cognition_event(
  p_project_id text,p_event jsonb,p_action text default 'record_intelligence',
  p_expected_result text default null,p_observed_result text default null,p_learning jsonb default '[]'::jsonb
) returns jsonb language plpgsql set search_path to 'public'
as $function$
declare v_event public.nayanet_cognition_events; v_state public.nayanet_project_cognition_state;
  v_receipt public.nayanet_execution_receipts; v_receipt_revision bigint;
  v_authority jsonb := null; v_authority_grant_id uuid := nullif(p_event->'metadata'->>'authority_grant_id','')::uuid;
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;
  -- intelligence.capture is automatic: no grant, credential, or execution authorization.
  if p_action <> 'intelligence.capture' and v_authority_grant_id is not null then
    v_authority := public.nayanet_validate_authority_grant(v_authority_grant_id,p_action,p_project_id);
    if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
      raise exception 'AUTHORITY_REQUIRED: %',coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
    end if;
  end if;
  perform pg_advisory_xact_lock(hashtext(auth.uid()::text || ':' || p_project_id));
  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata
  ) values(
    auth.uid(),p_project_id,p_event->>'event_id',coalesce((p_event->>'created_at')::timestamptz,now()),now(),
    coalesce(p_event->>'type','intelligence'),coalesce(p_event->>'classification','observation'),p_event->>'title',
    coalesce(p_event->>'content',''),coalesce(p_event->>'source','nayanet-hub'),coalesce(p_event->>'status','active'),
    coalesce(p_event->>'actor','human'),coalesce((p_event->>'confidence')::numeric,1),coalesce(p_event->'tags','[]'::jsonb),
    p_event->>'parent_event_id',coalesce(p_event->>'source_hash',''),coalesce(p_event->>'schema_version','1.0.0'),
    coalesce(p_event->>'receipt_id',''),coalesce(p_event->'metadata','{}'::jsonb)
  ) on conflict (user_id,project_id,event_id) do update set updated_at=now(),status=excluded.status,metadata=excluded.metadata returning * into v_event;
  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(auth.uid(),p_project_id,0,jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at,'successor',null),'READY')
  on conflict (user_id,project_id) do nothing;
  update public.nayanet_project_cognition_state set revision=revision+1,
    state=coalesce(state,'{}'::jsonb)||jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at),
    status='IN_PROGRESS',updated_at=now()
    where user_id=auth.uid() and project_id=p_project_id returning * into v_state;
  select coalesce(max(revision),0)+1 into v_receipt_revision from public.nayanet_execution_receipts
    where user_id=auth.uid() and project_id=p_project_id;
  insert into public.nayanet_execution_receipts(
    user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning,
    authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints,
    authority_status_at_execution,authority_source_event_id,authority_validated_at
  ) values(
    auth.uid(),p_project_id,v_receipt_revision,p_action,p_expected_result,p_observed_result,'SUCCESS',
    jsonb_build_object('event_id',v_event.event_id,'source_hash',v_event.source_hash,'created_at',v_event.created_at,
      'verification_boundary',case when p_action='intelligence.capture' then 'automatic-intelligence-flow-v1' else 'authenticated-cognition-v1' end,
      'authority_required',p_action <> 'intelligence.capture'),
    coalesce(p_learning,'[]'::jsonb),
    case when p_action='intelligence.capture' then null when v_authority ? 'grant_id' then (v_authority->>'grant_id')::uuid else v_authority_grant_id end,
    case when p_action='intelligence.capture' then null when v_authority ? 'issuer_id' then (v_authority->>'issuer_id')::uuid else null end,
    case when p_action='intelligence.capture' then null when v_authority ? 'scope' then v_authority->'scope' else null end,
    case when p_action='intelligence.capture' then null when v_authority ? 'actions' then v_authority->'actions' else null end,
    case when p_action='intelligence.capture' then null when v_authority ? 'constraints' then v_authority->'constraints' else null end,
    case when p_action='intelligence.capture' then null when v_authority ? 'grant_status' then v_authority->>'grant_status' else null end,
    case when p_action='intelligence.capture' then null when v_authority ? 'source_event_id' then v_authority->>'source_event_id' else null end,
    case when p_action='intelligence.capture' then null else clock_timestamp() end
  ) returning * into v_receipt;
  update public.nayanet_cognition_events set receipt_id=v_receipt.id::text,updated_at=now()
    where id=v_event.id and user_id=auth.uid() and project_id=p_project_id returning * into v_event;
  return jsonb_build_object('event',to_jsonb(v_event),'state',to_jsonb(v_state),'receipt',to_jsonb(v_receipt));
end;
$function$;

create or replace function public.nayanet_record_cognition_event(
  p_project_id text,p_event jsonb,p_action text default 'record_intelligence',
  p_expected_result text default null,p_observed_result text default null,p_learning jsonb default '[]'::jsonb,
  p_execution_authorization jsonb default null
) returns jsonb language plpgsql set search_path to 'public'
as $function$
declare v_event public.nayanet_cognition_events; v_state public.nayanet_project_cognition_state;
  v_receipt public.nayanet_execution_receipts; v_receipt_revision bigint; v_authority jsonb := null;
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;
  -- intelligence.capture is automatic and deliberately ignores execution authorization.
  if p_action <> 'intelligence.capture' and p_execution_authorization is not null then
    v_authority := public.nayanet_validate_authority_grant(
      (p_execution_authorization->>'authority_id')::uuid,p_action,p_project_id);
    if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
      raise exception 'AUTHORITY_REQUIRED: %',coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
    end if;
    if coalesce(p_execution_authorization->>'actor_id','') <> auth.uid()::text then raise exception 'EXECUTION_AUTHORIZATION_ACTOR_MISMATCH'; end if;
    if coalesce(p_execution_authorization->>'permission','') <> p_action then raise exception 'EXECUTION_AUTHORIZATION_PERMISSION_MISMATCH'; end if;
    if coalesce(p_execution_authorization->>'governance_state','') <> 'AUTHORIZED' then raise exception 'EXECUTION_AUTHORIZATION_NOT_AUTHORIZED'; end if;
  end if;
  perform pg_advisory_xact_lock(hashtext(auth.uid()::text || ':' || p_project_id));
  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata
  ) values(
    auth.uid(),p_project_id,p_event->>'event_id',coalesce((p_event->>'created_at')::timestamptz,now()),now(),
    coalesce(p_event->>'type','intelligence'),coalesce(p_event->>'classification','observation'),p_event->>'title',
    coalesce(p_event->>'content',''),coalesce(p_event->>'source','nayanet-hub'),coalesce(p_event->>'status','active'),
    coalesce(p_event->>'actor','human'),coalesce((p_event->>'confidence')::numeric,1),coalesce(p_event->'tags','[]'::jsonb),
    p_event->>'parent_event_id',coalesce(p_event->>'source_hash',''),coalesce(p_event->>'schema_version','1.0.0'),
    coalesce(p_event->>'receipt_id',''),coalesce(p_event->'metadata','{}'::jsonb)
  ) on conflict (user_id,project_id,event_id) do update set updated_at=now(),status=excluded.status,metadata=excluded.metadata returning * into v_event;
  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(auth.uid(),p_project_id,0,jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at,'successor',null),'READY')
  on conflict (user_id,project_id) do nothing;
  update public.nayanet_project_cognition_state set revision=revision+1,
    state=coalesce(state,'{}'::jsonb)||jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at),
    status='IN_PROGRESS',updated_at=now()
    where user_id=auth.uid() and project_id=p_project_id returning * into v_state;
  select coalesce(max(revision),0)+1 into v_receipt_revision from public.nayanet_execution_receipts
    where user_id=auth.uid() and project_id=p_project_id;
  insert into public.nayanet_execution_receipts(
    user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning,
    authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints,
    authority_status_at_execution,authority_source_event_id,authority_validated_at
  ) values(
    auth.uid(),p_project_id,v_receipt_revision,p_action,p_expected_result,p_observed_result,'SUCCESS',
    jsonb_build_object('event_id',v_event.event_id,'source_hash',v_event.source_hash,'created_at',v_event.created_at,
      'execution_authorization',case when p_action='intelligence.capture' then null else coalesce(p_execution_authorization,'null'::jsonb) end,
      'verification_boundary',case when p_action='intelligence.capture' then 'automatic-intelligence-flow-v1' else 'authenticated-cognition-v1' end,
      'authority_required',p_action <> 'intelligence.capture'),
    coalesce(p_learning,'[]'::jsonb),
    case when p_action='intelligence.capture' then null when v_authority is null then null else (v_authority->>'grant_id')::uuid end,
    case when p_action='intelligence.capture' then null when v_authority is null then null else (v_authority->>'issuer_id')::uuid end,
    case when p_action='intelligence.capture' then null when v_authority is null then null else v_authority->'scope' end,
    case when p_action='intelligence.capture' then null when v_authority is null then null else v_authority->'actions' end,
    case when p_action='intelligence.capture' then null when v_authority is null then null else v_authority->'constraints' end,
    case when p_action='intelligence.capture' then null when v_authority is null then null else v_authority->>'grant_status' end,
    case when p_action='intelligence.capture' then null when v_authority is null then null else v_authority->>'source_event_id' end,
    case when p_action='intelligence.capture' then null else clock_timestamp() end
  ) returning * into v_receipt;
  update public.nayanet_cognition_events set receipt_id=v_receipt.id::text,updated_at=now()
    where id=v_event.id and user_id=auth.uid() and project_id=p_project_id returning * into v_event;
  return jsonb_build_object('event',to_jsonb(v_event),'state',to_jsonb(v_state),'receipt',to_jsonb(v_receipt));
end;
$function$;
