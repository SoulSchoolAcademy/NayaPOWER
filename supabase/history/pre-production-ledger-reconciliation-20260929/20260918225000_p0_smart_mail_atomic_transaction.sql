-- P0 Smart Mail atomic transaction: receipt is created before cognition so the
-- canonical cognition row can carry its required receipt_id. The function is
-- callable only by the governed Edge Function's service role.
create or replace function public.nayanet_send_smart_mail(
  p_sender_id uuid,
  p_receiver_id uuid,
  p_body text,
  p_subject text,
  p_kind text,
  p_idempotency_key text,
  p_project_id text
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  existing_message public.v7_mail_messages%rowtype;
  v_thread uuid;
  v_message uuid;
  v_receipt uuid;
  v_event uuid;
  v_correlation uuid := gen_random_uuid();
  v_event_id text;
begin
  if p_sender_id is null or p_receiver_id is null or p_sender_id = p_receiver_id then
    raise exception 'INVALID_PARTICIPANTS';
  end if;
  if trim(coalesce(p_body,'')) = '' or length(p_body) > 10000 then
    raise exception 'INVALID_BODY';
  end if;
  if trim(coalesce(p_idempotency_key,'')) = '' then
    raise exception 'IDEMPOTENCY_REQUIRED';
  end if;
  if not exists (select 1 from auth.users where id = p_sender_id)
     or not exists (select 1 from auth.users where id = p_receiver_id) then
    raise exception 'USER_NOT_FOUND';
  end if;

  select * into existing_message
  from public.v7_mail_messages
  where sender_id = p_sender_id
    and metadata->>'idempotency_key' = p_idempotency_key
  limit 1;

  if existing_message.id is not null then
    return jsonb_build_object(
      'status','REPLAY',
      'correlation_id',existing_message.metadata->>'correlation_id',
      'thread_id',existing_message.thread_id,
      'message_id',existing_message.id,
      'execution_receipt_id',existing_message.metadata->>'execution_receipt_id'
    );
  end if;

  insert into public.v7_mail_threads(created_by,kind,subject)
  values(p_sender_id,coalesce(p_kind,'direct'),coalesce(p_subject,'NayaNET P0 communication proof'))
  returning id into v_thread;

  insert into public.v7_mail_members(thread_id,user_id)
  values(v_thread,p_sender_id),(v_thread,p_receiver_id);

  insert into public.v7_mail_messages(thread_id,sender_id,body,metadata)
  values(
    v_thread,p_sender_id,p_body,
    jsonb_build_object(
      'schema_version','NAYANET_SMART_MAIL_P0_V1',
      'correlation_id',v_correlation::text,
      'idempotency_key',p_idempotency_key,
      'sender_id',p_sender_id,
      'receiver_id',p_receiver_id,
      'governance',jsonb_build_object(
        'capability','SMART_MAIL_SEND',
        'authorization_basis','authenticated_sender_session',
        'model_authority',false,
        'authority_changed',false
      ),
      'lifecycle',jsonb_build_array('PROPOSED','INVESTIGATING','READY','AUTHORIZED','EXECUTING','EXECUTED','OBSERVED','VERIFIED')
    )
  )
  returning id into v_message;

  insert into public.nayanet_execution_receipts(
    user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning
  )
  values(
    p_sender_id,coalesce(p_project_id,'NayaNET'),1,'smart_mail_send',
    'Authenticated sender message is delivered to authorized receiver and remains retrievable.',
    'Atomic Smart Mail transaction created thread, members and message; cognition and receipt lineage were committed together.',
    'SUCCESS',
    jsonb_build_array(jsonb_build_object(
      'correlation_id',v_correlation::text,
      'thread_id',v_thread,
      'message_id',v_message,
      'sender_id',p_sender_id,
      'receiver_id',p_receiver_id
    )),
    jsonb_build_array(jsonb_build_object(
      'status','captured',
      'statement','Smart Mail P0 sender transaction persisted through the canonical cognition boundary.'
    ))
  )
  returning id into v_receipt;

  v_event_id := 'smart-mail-proof-' || replace(v_correlation::text,'-','');
  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,type,classification,title,content,source,status,actor,confidence,tags,
    parent_event_id,source_hash,schema_version,receipt_id,metadata
  )
  values(
    p_sender_id,coalesce(p_project_id,'NayaNET'),v_event_id,'communication','observation',
    'NayaNET Smart Mail P0 transaction',p_body,'nayanet-smart-mail','active','human',1,
    jsonb_build_array('smart-mail','p0','sender-receiver-proof'),
    null,'','1.0.0',v_receipt,
    jsonb_build_object('correlation_id',v_correlation::text,'message_id',v_message,'receiver_id',p_receiver_id)
  )
  returning id into v_event;

  update public.nayanet_execution_receipts
  set evidence = evidence || jsonb_build_array(jsonb_build_object(
    'cognition_event_id',v_event,
    'observed_at',now()
  ))
  where id = v_receipt;

  update public.v7_mail_messages
  set metadata = metadata || jsonb_build_object(
    'execution_receipt_id',v_receipt,
    'cognition_event_id',v_event
  )
  where id = v_message;

  return jsonb_build_object(
    'status','CREATED',
    'correlation_id',v_correlation::text,
    'thread_id',v_thread,
    'message_id',v_message,
    'cognition_event_id',v_event,
    'execution_receipt_id',v_receipt,
    'authority_changed',false
  );

exception
  when unique_violation then
    select * into existing_message
    from public.v7_mail_messages
    where sender_id = p_sender_id
      and metadata->>'idempotency_key' = p_idempotency_key
    limit 1;
    if existing_message.id is null then raise; end if;
    return jsonb_build_object(
      'status','REPLAY',
      'correlation_id',existing_message.metadata->>'correlation_id',
      'thread_id',existing_message.thread_id,
      'message_id',existing_message.id,
      'execution_receipt_id',existing_message.metadata->>'execution_receipt_id'
    );
end;
$$;

revoke execute on function public.nayanet_send_smart_mail(uuid,uuid,text,text,text,text,text) from public, anon, authenticated;
grant execute on function public.nayanet_send_smart_mail(uuid,uuid,text,text,text,text,text) to service_role;
