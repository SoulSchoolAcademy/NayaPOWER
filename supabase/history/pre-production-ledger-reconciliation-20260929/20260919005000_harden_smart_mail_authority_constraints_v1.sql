-- Enforce the defined no_external_side_effects constraint at the Smart Mail action boundary.
-- Legacy overloaded RPCs are retained only as fail-closed compatibility stubs.

create or replace function public.nayanet_send_smart_mail_authorized(
  p_sender_id uuid,
  p_receiver_id uuid,
  p_body text,
  p_subject text,
  p_kind text,
  p_idempotency_key text,
  p_project_id text,
  p_request_id text,
  p_policy_id uuid default null,
  p_experiment_case_id text default null,
  p_policy_input_hash text default null,
  p_policy_decision_hash text default null,
  p_authority_grant_id uuid default null
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $function$
declare
  v_authority jsonb;
  v_result jsonb;
  v_sender uuid := auth.uid();
  v_mutual boolean;
begin
  if v_sender is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_sender <> p_sender_id then raise exception 'SENDER_IDENTITY_MISMATCH'; end if;

  select exists(
    select 1 from public.nayanet_connections a
    join public.nayanet_connections b
      on b.owner_member_id=p_receiver_id
     and b.connected_member_id=p_sender_id
     and b.status='active'
    where a.owner_member_id=p_sender_id
      and a.connected_member_id=p_receiver_id
      and a.status='active'
  ) into v_mutual;
  if not v_mutual then raise exception 'RELATIONSHIP_REQUIRED'; end if;

  v_authority := public.nayanet_validate_authority_grant(
    p_authority_grant_id,'smart_mail_send',p_receiver_id::text
  );
  if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
    raise exception 'AUTHORITY_REQUIRED: %',
      coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
  end if;

  if coalesce(v_authority->'constraints'->>'no_external_side_effects','false')='true' then
    raise exception 'AUTHORITY_CONSTRAINT_CONFLICT: no_external_side_effects';
  end if;

  v_result := public.nayanet_send_smart_mail(
    p_sender_id,p_receiver_id,p_body,p_subject,p_kind,p_idempotency_key,p_project_id,
    p_request_id,p_policy_id,p_experiment_case_id,p_policy_input_hash,p_policy_decision_hash
  );

  if coalesce(v_result->>'status','')='CREATED' then
    update public.nayanet_execution_receipts
      set authority_grant_id=(v_authority->>'grant_id')::uuid,
          authority_issuer_id=(v_authority->>'issuer_id')::uuid,
          authority_scope=v_authority->'scope',
          authority_actions=v_authority->'actions',
          authority_constraints=v_authority->'constraints',
          authority_status_at_execution=v_authority->>'grant_status',
          authority_source_event_id=v_authority->>'source_event_id',
          authority_validated_at=clock_timestamp(),
          policy_id=p_policy_id,
          policy_version=(select pv.version from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          policy_key=(select pv.policy_key from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          policy_parent_id=(select pv.parent_policy_id from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          experiment_case_id=p_experiment_case_id,
          policy_input_hash=p_policy_input_hash,
          policy_decision_hash=p_policy_decision_hash
    where id=(v_result->>'execution_receipt_id')::uuid;

    update public.v7_mail_messages
      set metadata=metadata||jsonb_build_object(
        'authority_grant_id',v_authority->>'grant_id',
        'authority_source_event_id',v_authority->>'source_event_id',
        'authority_issuer_id',v_authority->>'issuer_id',
        'relationship_gate','mutual_active_connection'
      )
    where id=(v_result->>'message_id')::uuid;
  end if;

  return v_result||jsonb_build_object(
    'authority_grant_id',v_authority->>'grant_id',
    'relationship_gate','mutual_active_connection'
  );
end;
$function$;

create or replace function public.nayanet_send_smart_mail_policy_authorized(
  p_sender_id uuid,
  p_receiver_id uuid,
  p_body text,
  p_subject text,
  p_kind text,
  p_idempotency_key text,
  p_project_id text,
  p_request_id text,
  p_policy_id uuid,
  p_experiment_case_id text,
  p_policy_input_hash text,
  p_policy_decision_hash text,
  p_authority_grant_id uuid
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $function$
declare
  v_authority jsonb;
  v_result jsonb;
  v_sender uuid := auth.uid();
  v_mutual boolean;
begin
  if v_sender is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_sender <> p_sender_id then raise exception 'SENDER_IDENTITY_MISMATCH'; end if;
  if p_policy_id is null or p_experiment_case_id is null
     or p_policy_input_hash is null or p_policy_decision_hash is null then
    raise exception 'POLICY_LINEAGE_REQUIRED';
  end if;

  select exists(
    select 1 from public.nayanet_connections a
    join public.nayanet_connections b
      on b.owner_member_id=p_receiver_id
     and b.connected_member_id=p_sender_id
     and b.status='active'
    where a.owner_member_id=p_sender_id
      and a.connected_member_id=p_receiver_id
      and a.status='active'
  ) into v_mutual;
  if not v_mutual then raise exception 'RELATIONSHIP_REQUIRED'; end if;

  v_authority:=public.nayanet_validate_authority_grant(
    p_authority_grant_id,'smart_mail_send',p_receiver_id::text
  );
  if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
    raise exception 'AUTHORITY_REQUIRED: %',
      coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
  end if;

  if coalesce(v_authority->'constraints'->>'no_external_side_effects','false')='true' then
    raise exception 'AUTHORITY_CONSTRAINT_CONFLICT: no_external_side_effects';
  end if;

  select public.nayanet_send_smart_mail(
    p_sender_id,p_receiver_id,p_body,p_subject,p_kind,p_idempotency_key,p_project_id,
    p_request_id,p_policy_id,p_experiment_case_id,p_policy_input_hash,p_policy_decision_hash
  ) into v_result;

  if coalesce(v_result->>'status','')='CREATED' then
    update public.nayanet_execution_receipts
      set authority_grant_id=(v_authority->>'grant_id')::uuid,
          authority_issuer_id=(v_authority->>'issuer_id')::uuid,
          authority_scope=v_authority->'scope',
          authority_actions=v_authority->'actions',
          authority_constraints=v_authority->'constraints',
          authority_status_at_execution=v_authority->>'grant_status',
          authority_source_event_id=v_authority->>'source_event_id',
          authority_validated_at=clock_timestamp(),
          policy_id=p_policy_id,
          policy_version=(select pv.version from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          policy_key=(select pv.policy_key from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          policy_parent_id=(select pv.parent_policy_id from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          experiment_case_id=p_experiment_case_id,
          policy_input_hash=p_policy_input_hash,
          policy_decision_hash=p_policy_decision_hash
    where id=(v_result->>'execution_receipt_id')::uuid;
  end if;

  return v_result||jsonb_build_object(
    'authority_grant_id',v_authority->>'grant_id',
    'relationship_gate','mutual_active_connection'
  );
end;
$function$;

-- The deprecated overloads omit the canonical request_id lineage and must not be executable
-- by authenticated callers.
revoke all on function public.nayanet_send_smart_mail_authorized(
  uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid
) from public,anon,authenticated;

revoke all on function public.nayanet_send_smart_mail_policy_authorized(
  uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid
) from public,anon,authenticated;
