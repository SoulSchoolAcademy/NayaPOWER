-- Harden canonical cognition receipt replay semantics for event-idempotent ingress.
-- Existing cognition events are the canonical idempotency key. On an exact replay,
-- return the original event/state/receipt without creating a new receipt or advancing
-- project cognition state. No new persistence system or authority model is introduced.

create or replace function public.nayanet_record_cognition_event(
  p_project_id text,
  p_event jsonb,
  p_action text default 'record_intelligence',
  p_expected_result text default null,
  p_observed_result text default null,
  p_learning jsonb default '[]'::jsonb
) returns jsonb
language plpgsql
set search_path to 'public'
as $function$
declare
  v_event public.nayanet_cognition_events;
  v_existing_event public.nayanet_cognition_events;
  v_state public.nayanet_project_cognition_state;
  v_receipt public.nayanet_execution_receipts;
  v_existing_receipt public.nayanet_execution_receipts;
  v_receipt_revision bigint;
  v_authority jsonb := null;
  v_authority_grant_id uuid := nullif(p_event->'metadata'->>'authority_grant_id','')::uuid;
  v_authority_validated_at timestamptz := null;
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;

  if p_action = 'intelligence.capture' then
    -- The six-argument overload has no canonical ExecutionAuthorization input.
    -- It MUST NOT authorize intelligence.capture from caller-supplied metadata.
    -- All intelligence.capture calls must use the seven-argument canonical seam,
    -- which is the only overload capable of receiving the governed authorization.
    raise exception 'CANONICAL_EXECUTION_AUTHORIZATION_REQUIRED';
  elsif v_authority_grant_id is not null then
    v_authority_validated_at := clock_timestamp();
    v_authority := public.nayanet_validate_authority_grant(
      v_authority_grant_id,
      p_action,
      p_project_id
    );
    if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
      raise exception 'AUTHORITY_REQUIRED: %', coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
    end if;
  end if;

  perform pg_advisory_xact_lock(hashtext(auth.uid()::text || ':' || p_project_id));

  -- Canonical event identity is the existing unique (user_id, project_id, event_id).
  -- An existing event with its canonical receipt is an exact replay: do not mutate
  -- state, create a second receipt, or overwrite the original event lineage.
  select *
    into v_existing_event
    from public.nayanet_cognition_events
   where user_id=auth.uid()
     and project_id=p_project_id
     and event_id=p_event->>'event_id'
   limit 1;

  if v_existing_event.id is not null
     and coalesce(v_existing_event.receipt_id,'') <> '' then
    select *
      into v_existing_receipt
      from public.nayanet_execution_receipts
     where id::text=v_existing_event.receipt_id
     limit 1;

    if v_existing_receipt.id is not null then
      select *
        into v_state
        from public.nayanet_project_cognition_state
       where user_id=auth.uid()
         and project_id=p_project_id
       limit 1;

      return jsonb_build_object(
        'replayed',true,
        'event',to_jsonb(v_existing_event),
        'state',to_jsonb(v_state),
        'receipt',to_jsonb(v_existing_receipt)
      );
    end if;
  end if;

  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata
  ) values(
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
  ) values(
    auth.uid(),p_project_id,v_receipt_revision,p_action,p_expected_result,p_observed_result,'SUCCESS',
    jsonb_build_object('event_id',v_event.event_id,'source_hash',v_event.source_hash,'created_at',v_event.created_at),
    coalesce(p_learning,'[]'::jsonb),
    case when v_authority ? 'grant_id' then (v_authority->>'grant_id')::uuid else v_authority_grant_id end,
    case when v_authority ? 'issuer_id' then (v_authority->>'issuer_id')::uuid else null end,
    case when v_authority ? 'scope' then v_authority->'scope' else null end,
    case when v_authority ? 'actions' then v_authority->'actions' else null end,
    case when v_authority ? 'constraints' then v_authority->'constraints' else null end,
    case when v_authority ? 'grant_status' then v_authority->>'grant_status' else null end,
    case when v_authority ? 'source_event_id' then v_authority->>'source_event_id' else null end,
    v_authority_validated_at
  )
  returning * into v_receipt;

  update public.nayanet_cognition_events
     set receipt_id=v_receipt.id::text,
         updated_at=now()
   where id=v_event.id
     and user_id=auth.uid()
     and project_id=p_project_id
  returning * into v_event;

  return jsonb_build_object('replayed',false,'event',to_jsonb(v_event),'state',to_jsonb(v_state),'receipt',to_jsonb(v_receipt));
end;
$function$;

grant execute on function public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb) to authenticated;
revoke execute on function public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb) from anon, public;
