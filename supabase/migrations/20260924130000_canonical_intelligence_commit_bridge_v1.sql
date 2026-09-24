-- Stream B canonical production intelligence_commit seam V1.
-- The Edge Function is the cryptographic verifier boundary:
--   authenticated user -> gate-issued portable artifact -> Ed25519 verification
--   -> service-role-only canonical DB seam -> cognition + receipt.
--
-- Postgres deliberately does NOT pretend to verify Ed25519. The canonical DB
-- seam accepts only the service-role call made after the Edge Function has
-- verified the portable artifact, then re-checks the live production grant
-- and exact actor/action/target bindings before persistence.

create or replace function public.nayanet_canonical_intelligence_commit(
  p_project_id text,
  p_event jsonb,
  p_action text,
  p_expected_result text,
  p_observed_result text,
  p_learning jsonb default '[]'::jsonb,
  p_portable_authorization jsonb default null
) returns jsonb
language plpgsql
security invoker
set search_path to 'public'
as $function$
declare
  v_event public.nayanet_cognition_events;
  v_state public.nayanet_project_cognition_state;
  v_receipt public.nayanet_execution_receipts;
  v_receipt_revision bigint;
  v_auth jsonb;
  v_grant public.nayanet_authority_grants;
  v_grant_id uuid;
  v_actor uuid;
  v_expires timestamptz;
begin
  if coalesce(current_setting('request.jwt.claim.role', true), '') <> 'service_role' then
    raise exception 'CANONICAL_INTELLIGENCE_COMMIT_SERVICE_ROLE_REQUIRED';
  end if;
  if p_action <> 'intelligence.capture' then
    raise exception 'CANONICAL_INTELLIGENCE_COMMIT_ACTION_REQUIRED';
  end if;
  if p_portable_authorization is null
     or jsonb_typeof(p_portable_authorization) <> 'object'
     or p_portable_authorization->>'schema' <> 'naya/portable_authorization/v1'
     or jsonb_typeof(p_portable_authorization->'authorization') <> 'object'
     or jsonb_typeof(p_portable_authorization->'signature') <> 'string' then
    raise exception 'PORTABLE_AUTHORIZATION_REQUIRED';
  end if;

  -- Signature provenance is verified by the trusted Edge Function before this
  -- service-role-only seam is called. This function independently rechecks all
  -- live grant bindings so revocation/expiry cannot be bypassed after issuance.
  v_auth := p_portable_authorization->'authorization';
  if coalesce(v_auth->>'action_type','') not in ('INTELLIGENCE_COMMIT','intelligence_commit') then
    raise exception 'PORTABLE_ACTION_TYPE_MISMATCH';
  end if;
  if coalesce(v_auth->>'permission','') <> 'intelligence_commit' then
    raise exception 'PORTABLE_PERMISSION_MISMATCH';
  end if;
  if coalesce(v_auth->>'target','') <> p_project_id then
    raise exception 'PORTABLE_TARGET_MISMATCH';
  end if;
  if coalesce(v_auth->>'governance_state','') <> 'AUTHORIZED' then
    raise exception 'PORTABLE_GOVERNANCE_STATE_MISMATCH';
  end if;
  if coalesce(v_auth->>'authority_id','') = '' then
    raise exception 'PORTABLE_AUTHORITY_ID_REQUIRED';
  end if;

  begin
    v_grant_id := (v_auth->>'authority_id')::uuid;
    v_actor := (v_auth->>'actor_id')::uuid;
  exception when others then
    raise exception 'PORTABLE_PRODUCTION_GRANT_ID_INVALID';
  end;

  select * into v_grant
    from public.nayanet_authority_grants
   where grant_id = v_grant_id
     and subject_id = v_actor
     and status = 'ACTIVE'
   for update;

  if not found then
    raise exception 'PRODUCTION_AUTHORITY_GRANT_NOT_ACTIVE';
  end if;
  if v_grant.expires_at is not null and v_grant.expires_at <= clock_timestamp() then
    raise exception 'PRODUCTION_AUTHORITY_GRANT_EXPIRED';
  end if;
  if not (v_grant.actions ? 'intelligence_commit') then
    raise exception 'PRODUCTION_AUTHORITY_ACTION_NOT_GRANTED';
  end if;
  if not (
    coalesce(v_grant.scope->>'project_id','') = p_project_id
    or coalesce(v_grant.scope->>'target','') = p_project_id
  ) then
    raise exception 'PRODUCTION_AUTHORITY_TARGET_OUT_OF_SCOPE';
  end if;
  if coalesce(v_auth->>'actor_id','') <> v_grant.subject_id::text then
    raise exception 'PORTABLE_ACTOR_GRANT_MISMATCH';
  end if;
  if coalesce(v_auth->>'authority_id','') <> v_grant.grant_id::text then
    raise exception 'PORTABLE_GRANT_ID_MISMATCH';
  end if;

  -- The event must carry the same production grant identity; a legacy metadata
  -- grant cannot be substituted for the gate-issued portable artifact.
  if coalesce(p_event->'metadata'->>'authority_grant_id','') <> v_grant.grant_id::text then
    raise exception 'EVENT_AUTHORITY_GRANT_MISMATCH';
  end if;

  perform pg_advisory_xact_lock(hashtext(v_actor::text || ':' || p_project_id));

  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata
  ) values(
    v_actor,p_project_id,p_event->>'event_id',coalesce((p_event->>'created_at')::timestamptz,now()),now(),
    coalesce(p_event->>'type','intelligence'),coalesce(p_event->>'classification','observation'),p_event->>'title',
    coalesce(p_event->>'content',''),coalesce(p_event->>'source','nayanet-hub'),coalesce(p_event->>'status','active'),
    coalesce(p_event->>'actor','naya'),coalesce((p_event->>'confidence')::numeric,1),coalesce(p_event->'tags','[]'::jsonb),
    p_event->>'parent_event_id',coalesce(p_event->>'source_hash',''),coalesce(p_event->>'schema_version','1.0.0'),
    coalesce(p_event->>'receipt_id',''),coalesce(p_event->'metadata','{}'::jsonb)
  )
  on conflict (user_id,project_id,event_id) do update
    set updated_at=now(),status=excluded.status,metadata=excluded.metadata
  returning * into v_event;

  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(v_actor,p_project_id,0,jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at,'successor',null),'READY')
  on conflict (user_id,project_id) do nothing;

  update public.nayanet_project_cognition_state
     set revision=revision+1,
         state=coalesce(state,'{}'::jsonb)||jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at),
         status='IN_PROGRESS',
         updated_at=now()
   where user_id=v_actor and project_id=p_project_id
   returning * into v_state;

  select coalesce(max(revision),0)+1
    into v_receipt_revision
    from public.nayanet_execution_receipts
   where user_id=v_actor and project_id=p_project_id;

  insert into public.nayanet_execution_receipts(
    user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning,
    authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints,
    authority_status_at_execution,authority_source_event_id,authority_validated_at
  )
  values(
    v_actor,p_project_id,v_receipt_revision,p_action,p_expected_result,p_observed_result,'SUCCESS',
    jsonb_build_object(
      'event_id',v_event.event_id,
      'source_hash',v_event.source_hash,
      'created_at',v_event.created_at,
      'authorization_schema',p_portable_authorization->>'schema',
      'authorization_signature',p_portable_authorization->>'signature',
      'authority_id',v_auth->>'authority_id',
      'decision_id',v_auth->>'decision_id',
      'action_id',v_auth->>'action_id',
      'binding_hash',v_auth->>'binding_hash',
      'verification_boundary','nayanet-compound-intelligence:portable-ed25519-v1'
    ),
    coalesce(p_learning,'[]'::jsonb),
    v_grant.grant_id,v_grant.issuer_id,v_grant.scope,v_grant.actions,v_grant.constraints,
    v_grant.status,v_grant.source_event_id,clock_timestamp()
  )
  returning * into v_receipt;

  update public.nayanet_cognition_events
     set receipt_id=v_receipt.id::text,updated_at=now()
   where id=v_event.id and user_id=v_actor and project_id=p_project_id
  returning * into v_event;

  return jsonb_build_object('event',to_jsonb(v_event),'state',to_jsonb(v_state),'receipt',to_jsonb(v_receipt));
end;
$function$;

revoke all on function public.nayanet_canonical_intelligence_commit(text,jsonb,text,text,text,jsonb,jsonb) from public, anon, authenticated;
grant execute on function public.nayanet_canonical_intelligence_commit(text,jsonb,text,text,text,jsonb,jsonb) to service_role;

-- Legacy authenticated entry points remain available for non-intelligence actions,
-- but intelligence.capture can no longer bypass the canonical verifier.
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
begin
  if p_action = 'intelligence.capture' then
    raise exception 'INTELLIGENCE_CAPTURE_REQUIRES_CANONICAL_VERIFIER';
  end if;
  raise exception 'LEGACY_COGNITION_PATH_DISABLED_FOR_STREAM_B_CONVERGENCE';
end;
$function$;

revoke execute on function public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb) from public, anon, authenticated;

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
begin
  if p_action = 'intelligence.capture' then
    raise exception 'INTELLIGENCE_CAPTURE_REQUIRES_CANONICAL_VERIFIER';
  end if;
  raise exception 'LEGACY_COGNITION_PATH_DISABLED_FOR_STREAM_B_CONVERGENCE';
end;
$function$;

revoke execute on function public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb,jsonb) from public, anon, authenticated;

comment on function public.nayanet_canonical_intelligence_commit(text,jsonb,text,text,text,jsonb,jsonb)
is 'Single production intelligence_commit persistence seam. Cryptographic portable authorization is verified by the trusted Edge Function; this service-role-only function independently revalidates the live production grant and exact actor/action/target bindings before persistence.';
