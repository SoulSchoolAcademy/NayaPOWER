-- P1 receiver-response outcome extension.
-- Uses the canonical nayanet_execution_outcomes row and responsible-value formula.
create or replace function public.nayanet_record_smart_mail_response_outcome(
  p_receipt_id uuid,
  p_message_id uuid,
  p_reply_message_id uuid,
  p_expected_reply_hash text
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_user uuid := (select auth.uid());
  r public.nayanet_execution_receipts;
  m public.v7_mail_messages;
  reply public.v7_mail_messages;
  outcome public.nayanet_execution_outcomes;
  v_match boolean;
  v_benefit numeric;
begin
  if v_user is null then raise exception 'AUTH_REQUIRED'; end if;
  if p_expected_reply_hash is null or length(trim(p_expected_reply_hash)) <> 64
    or p_expected_reply_hash !~ '^[0-9a-f]{64}$'
    then raise exception 'EXPECTED_REPLY_HASH_INVALID'; end if;

  select * into r
  from public.nayanet_execution_receipts
  where id=p_receipt_id
  for share;
  if r.id is null then raise exception 'RECEIPT_NOT_FOUND'; end if;
  if r.action <> 'smart_mail_send' then raise exception 'UNSUPPORTED_OUTCOME_ACTION'; end if;
  if r.user_id = v_user then raise exception 'SENDER_CANNOT_SELF_VERIFY'; end if;

  select * into m from public.v7_mail_messages where id=p_message_id;
  if m.id is null then raise exception 'MESSAGE_NOT_FOUND'; end if;
  if m.sender_id <> r.user_id then raise exception 'MESSAGE_RECEIPT_OWNER_MISMATCH'; end if;
  if (m.metadata->>'execution_receipt_id') <> p_receipt_id::text then raise exception 'MESSAGE_RECEIPT_LINEAGE_MISMATCH'; end if;
  if not exists (
    select 1 from public.v7_mail_members
    where thread_id=m.thread_id and user_id=v_user
  ) then raise exception 'RECEIVER_NOT_AUTHORIZED'; end if;

  select * into reply from public.v7_mail_messages where id=p_reply_message_id;
  if reply.id is null then raise exception 'REPLY_MESSAGE_NOT_FOUND'; end if;
  if reply.thread_id <> m.thread_id then raise exception 'REPLY_THREAD_MISMATCH'; end if;
  if reply.sender_id <> v_user then raise exception 'REPLY_SENDER_MISMATCH'; end if;
  if reply.created_at <= m.created_at then raise exception 'REPLY_MUST_FOLLOW_ORIGINAL'; end if;
  if reply.metadata->>'reply_to_message_id' <> m.id::text then raise exception 'REPLY_LINEAGE_MISSING'; end if;

  v_match := encode(extensions.digest(coalesce(reply.body,''),'sha256'),'hex') = lower(trim(p_expected_reply_hash));
  v_benefit := case when v_match then 1 else 0 end;

  select * into outcome
  from public.nayanet_execution_outcomes
  where receipt_id=r.id
  for update;

  if outcome.outcome_id is null then raise exception 'INITIAL_OUTCOME_MISSING'; end if;
  if outcome.verifier_id <> v_user then raise exception 'OUTCOME_VERIFIER_MISMATCH'; end if;

  update public.nayanet_execution_outcomes
  set outcome_type='receiver_response_accuracy',
      evidence=coalesce(evidence,'{}'::jsonb)||jsonb_build_object(
        'response_message_id',reply.id,
        'reply_to_message_id',m.id,
        'response_sha256',encode(extensions.digest(coalesce(reply.body,''),'sha256'),'hex'),
        'expected_reply_sha256',lower(trim(p_expected_reply_hash)),
        'response_match',v_match,
        'response_verified_at',now(),
        'response_outcome_contract','NAYANET_REAL_OUTCOME_VALUE_V2'
      ),
      benefit=v_benefit,
      harm=0,
      cost=0,
      risk_adjusted_loss=0,
      verified=true,
      verification_method='authenticated receiver response + deterministic SHA-256 comparison'
  where receipt_id=r.id
  returning * into outcome;

  update public.nayanet_execution_receipts
  set value=coalesce(value,'{}'::jsonb)||jsonb_build_object(
    'schema','NAYANET_REAL_OUTCOME_VALUE_V2',
    'outcome_id',outcome.outcome_id,
    'verified',outcome.verified,
    'verified_value',outcome.verified_value,
    'verification_method',outcome.verification_method
  )
  where id=r.id;

  return jsonb_build_object(
    'status','VERIFIED',
    'outcome_id',outcome.outcome_id,
    'receipt_id',outcome.receipt_id,
    'verified_value',outcome.verified_value,
    'response_match',v_match,
    'response_message_id',reply.id,
    'verification_method',outcome.verification_method,
    'evidence',outcome.evidence
  );
end;
$$;

revoke all on function public.nayanet_record_smart_mail_response_outcome(uuid,uuid,uuid,text) from public,anon,authenticated;
grant execute on function public.nayanet_record_smart_mail_response_outcome(uuid,uuid,uuid,text) to authenticated,service_role;
