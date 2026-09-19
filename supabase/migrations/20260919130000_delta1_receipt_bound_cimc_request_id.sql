-- Delta 1: receipt-bound CIMC request identity
-- Adds only the canonical request identity field. CIMC measurement identity is
-- derived from the authoritative execution receipt id and is not stored separately.

alter table public.nayanet_execution_receipts
  add column if not exists request_id text;

create index if not exists nayanet_execution_receipts_request_id_idx
  on public.nayanet_execution_receipts(request_id)
  where request_id is not null;

create or replace function public.nayanet_send_smart_mail(
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
  p_policy_decision_hash text default null
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $function$
declare
  existing_message public.v7_mail_messages%rowtype;
  v_policy public.nayanet_policy_versions;
  v_thread uuid;
  v_message uuid;
  v_receipt uuid;
  v_event uuid;
  v_correlation uuid:=gen_random_uuid();
  v_event_id text;
  v_revision bigint;
begin
  if (select auth.uid()) is null then raise exception 'AUTH_REQUIRED'; end if;
  if (select auth.uid()) <> p_sender_id then raise exception 'SENDER_IDENTITY_MISMATCH'; end if;
  perform pg_advisory_xact_lock(hashtext(p_sender_id::text || ':' || coalesce(p_project_id,'NayaNET')));

  if p_sender_id is null or p_receiver_id is null or p_sender_id=p_receiver_id then raise exception 'INVALID_PARTICIPANTS'; end if;
  if trim(coalesce(p_body,''))='' or length(p_body)>10000 then raise exception 'INVALID_BODY'; end if;
  if trim(coalesce(p_idempotency_key,''))='' then raise exception 'IDEMPOTENCY_REQUIRED'; end if;
  if p_policy_id is not null then
    select * into v_policy from public.nayanet_policy_versions where id=p_policy_id for share;
    if v_policy.id is null then raise exception 'POLICY_NOT_FOUND'; end if;
    if v_policy.user_id <> p_sender_id then raise exception 'POLICY_OWNER_MISMATCH'; end if;
    if v_policy.project_id <> coalesce(p_project_id,'NayaNET') then raise exception 'POLICY_PROJECT_MISMATCH'; end if;
    if v_policy.state not in ('CONTROLLED_TEST','OBSERVED','VERIFIED') then raise exception 'POLICY_NOT_EXECUTABLE_IN_CURRENT_STATE:%',v_policy.state; end if;
  end if;
  if p_policy_id is not null and trim(coalesce(p_experiment_case_id,''))='' then raise exception 'EXPERIMENT_CASE_ID_REQUIRED'; end if;
  if not exists(select 1 from auth.users where id=p_sender_id) or not exists(select 1 from auth.users where id=p_receiver_id) then raise exception 'USER_NOT_FOUND'; end if;

  select * into existing_message from public.v7_mail_messages
   where sender_id=p_sender_id and metadata->>'idempotency_key'=p_idempotency_key limit 1;
  if existing_message.id is not null then
    return jsonb_build_object('status','REPLAY','correlation_id',existing_message.metadata->>'correlation_id','thread_id',existing_message.thread_id,'message_id',existing_message.id,'execution_receipt_id',existing_message.metadata->>'execution_receipt_id');
  end if;

  if p_request_id is null or trim(p_request_id)='' or length(p_request_id)>128 then
    raise exception 'REQUEST_ID_REQUIRED';
  end if;

  insert into public.v7_mail_threads(created_by,kind,subject)
  values(p_sender_id,coalesce(p_kind,'direct'),coalesce(p_subject,'NayaNET controlled policy test'))
  returning id into v_thread;

  insert into public.v7_mail_members(thread_id,user_id) values(v_thread,p_sender_id),(v_thread,p_receiver_id);

  insert into public.v7_mail_messages(thread_id,sender_id,body,metadata)
  values(
    v_thread,p_sender_id,p_body,
    jsonb_build_object(
      'schema_version','NAYANET_SMART_MAIL_P1_POLICY_LINEAGE_V1',
      'correlation_id',v_correlation::text,
      'idempotency_key',p_idempotency_key,
      'sender_id',p_sender_id,
      'receiver_id',p_receiver_id,
      'policy',case when v_policy.id is null then null else jsonb_build_object('id',v_policy.id,'version',v_policy.version,'policy_key',v_policy.policy_key,'parent_policy_id',v_policy.parent_policy_id,'experiment_case_id',p_experiment_case_id) end,
      'governance',jsonb_build_object('capability','SMART_MAIL_SEND','authorization_basis','authenticated_sender_session','model_authority',false,'authority_changed',false),
      'lifecycle',jsonb_build_array('PROPOSED','INVESTIGATING','READY','AUTHORIZED','EXECUTING','EXECUTED','OBSERVED','VERIFIED')
    )
  )
  returning id into v_message;

  select coalesce(max(revision)+1,1) into v_revision
  from public.nayanet_execution_receipts
  where user_id=p_sender_id and project_id=coalesce(p_project_id,'NayaNET');

  insert into public.nayanet_execution_receipts(
    user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning,value,
    request_id,policy_id,policy_version,policy_key,policy_parent_id,experiment_case_id,policy_input_hash,policy_decision_hash
  )
  values(
    p_sender_id,coalesce(p_project_id,'NayaNET'),v_revision,'smart_mail_send',
    'Authenticated sender message is delivered to authorized receiver and remains retrievable.',
    'Controlled policy execution created thread, members and message; receipt carries immutable policy lineage.',
    'SUCCESS',
    jsonb_build_array(jsonb_build_object(
      'correlation_id',v_correlation::text,'thread_id',v_thread,'message_id',v_message,
      'sender_id',p_sender_id,'receiver_id',p_receiver_id
    )),
    jsonb_build_array(jsonb_build_object('status','captured','statement','Smart Mail controlled policy execution persisted through the canonical cognition boundary.')),
    jsonb_build_object('schema','NAYANET_RESPONSIBLE_VALUE_V1','benefit',1,'harm',0,'cost',1,'risk_adjusted_loss',0,'verified',false,'verification_method','pending receiver verification','formula','benefit - harm - cost - risk_adjusted_loss'),
    p_request_id,
    p_policy_id,
    case when v_policy.id is null then null else v_policy.version end,
    case when v_policy.id is null then null else v_policy.policy_key end,
    case when v_policy.id is null then null else v_policy.parent_policy_id end,
    p_experiment_case_id,
    p_policy_input_hash,
    p_policy_decision_hash
  )
  returning id into v_receipt;

  v_event_id:='smart-mail-proof-'||replace(v_correlation::text,'-','');
  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,type,classification,title,content,source,status,actor,confidence,tags,
    parent_event_id,source_hash,schema_version,receipt_id,metadata
  )
  values(
    p_sender_id,coalesce(p_project_id,'NayaNET'),v_event_id,'communication','observation',
    'NayaNET Smart Mail controlled policy transaction',p_body,'nayanet-smart-mail','active','human',1,
    jsonb_build_array('smart-mail','p1','policy-lineage'),
    null,'','1.0.0',v_receipt,
    jsonb_build_object(
      'correlation_id',v_correlation::text,'message_id',v_message,'receiver_id',p_receiver_id,
      'policy',case when v_policy.id is null then null else jsonb_build_object('id',v_policy.id,'version',v_policy.version,'policy_key',v_policy.policy_key,'experiment_case_id',p_experiment_case_id) end
    )
  )
  returning id into v_event;

  update public.nayanet_execution_receipts
    set evidence=evidence||jsonb_build_array(jsonb_build_object('cognition_event_id',v_event,'observed_at',now()))
    where id=v_receipt;

  update public.v7_mail_messages
    set metadata=metadata||jsonb_build_object('execution_receipt_id',v_receipt,'cognition_event_id',v_event)
    where id=v_message;

  return jsonb_build_object(
    'status','CREATED','correlation_id',v_correlation::text,'thread_id',v_thread,'message_id',v_message,
    'cognition_event_id',v_event,'execution_receipt_id',v_receipt,'authority_changed',false,
    'policy',case when v_policy.id is null then null else jsonb_build_object('id',v_policy.id,'version',v_policy.version,'policy_key',v_policy.policy_key,'experiment_case_id',p_experiment_case_id) end
  );
exception when unique_violation then
  select * into existing_message from public.v7_mail_messages where sender_id=p_sender_id and metadata->>'idempotency_key'=p_idempotency_key limit 1;
  if existing_message.id is null then raise; end if;
  return jsonb_build_object('status','REPLAY','correlation_id',existing_message.metadata->>'correlation_id','thread_id',existing_message.thread_id,'message_id',existing_message.id,'execution_receipt_id',existing_message.metadata->>'execution_receipt_id');
end;
$function$;

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
declare v_authority jsonb; v_result jsonb; v_sender uuid:=auth.uid(); v_mutual boolean;
begin
  if v_sender is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_sender<>p_sender_id then raise exception 'SENDER_IDENTITY_MISMATCH'; end if;
  select exists(
    select 1 from public.nayanet_connections a
    join public.nayanet_connections b on b.owner_member_id=p_receiver_id
      and b.connected_member_id=p_sender_id and b.status='active'
    where a.owner_member_id=p_sender_id and a.connected_member_id=p_receiver_id and a.status='active'
  ) into v_mutual;
  if not v_mutual then raise exception 'RELATIONSHIP_REQUIRED'; end if;
  v_authority:=public.nayanet_validate_authority_grant(p_authority_grant_id,'smart_mail_send',p_receiver_id::text);
  if coalesce(v_authority->>'status','BLOCKED')<>'AUTHORIZED' then
    raise exception 'AUTHORITY_REQUIRED: %',coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
  end if;
  v_result:=public.nayanet_send_smart_mail(
    p_sender_id,p_receiver_id,p_body,p_subject,p_kind,p_idempotency_key,p_project_id,p_request_id,
    p_policy_id,p_experiment_case_id,p_policy_input_hash,p_policy_decision_hash
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
  return v_result||jsonb_build_object('authority_grant_id',v_authority->>'grant_id','relationship_gate','mutual_active_connection');
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
declare v_authority jsonb; v_result jsonb; v_sender uuid:=auth.uid(); v_mutual boolean;
begin
  if v_sender is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_sender<>p_sender_id then raise exception 'SENDER_IDENTITY_MISMATCH'; end if;
  if p_policy_id is null or p_experiment_case_id is null or p_policy_input_hash is null or p_policy_decision_hash is null then
    raise exception 'POLICY_LINEAGE_REQUIRED';
  end if;
  select exists(
    select 1 from public.nayanet_connections a
    join public.nayanet_connections b on b.owner_member_id=p_receiver_id
      and b.connected_member_id=p_sender_id and b.status='active'
    where a.owner_member_id=p_sender_id and a.connected_member_id=p_receiver_id and a.status='active'
  ) into v_mutual;
  if not v_mutual then raise exception 'RELATIONSHIP_REQUIRED'; end if;
  v_authority:=public.nayanet_validate_authority_grant(p_authority_grant_id,'smart_mail_send',p_receiver_id::text);
  if coalesce(v_authority->>'status','BLOCKED')<>'AUTHORIZED' then
    raise exception 'AUTHORITY_REQUIRED: %',coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
  end if;
  select public.nayanet_send_smart_mail(
    p_sender_id,p_receiver_id,p_body,p_subject,p_kind,p_idempotency_key,p_project_id,p_request_id,
    p_policy_id,p_experiment_case_id,p_policy_input_hash,p_policy_decision_hash
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
  return v_result||jsonb_build_object('authority_grant_id',v_authority->>'grant_id','relationship_gate','mutual_active_connection');
end;
$function$;

revoke execute on function public.nayanet_send_smart_mail(uuid,uuid,text,text,text,text,text) from public,anon,authenticated,service_role;
revoke execute on function public.nayanet_send_smart_mail(uuid,uuid,text,text,text,text,text,uuid,text,text,text) from public,anon,authenticated,service_role;
grant execute on function public.nayanet_send_smart_mail(uuid,uuid,text,text,text,text,text,text,uuid,text,text,text) to authenticated,service_role;

revoke execute on function public.nayanet_send_smart_mail_authorized(uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid) from public,anon,authenticated,service_role;
grant execute on function public.nayanet_send_smart_mail_authorized(uuid,uuid,text,text,text,text,text,text,uuid,text,text,text,uuid) to authenticated,service_role;

revoke execute on function public.nayanet_send_smart_mail_policy_authorized(uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid) from public,anon,authenticated,service_role;
grant execute on function public.nayanet_send_smart_mail_policy_authorized(uuid,uuid,text,text,text,text,text,text,uuid,text,text,text,uuid) to authenticated,service_role;
