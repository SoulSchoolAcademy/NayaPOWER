-- P1 receiver verification ownership fix
-- The sender owns the execution receipt; the authenticated receiver owns the
-- verification act. Outcome persistence must therefore require receiver identity,
-- not receipt ownership.

create or replace function public.nayanet_record_smart_mail_outcome(
  p_receipt_id uuid,
  p_message_id uuid,
  p_experiment_case_id text default null
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $function$
declare
  v_verifier uuid := (select auth.uid());
  r public.nayanet_execution_receipts;
  m public.v7_mail_messages;
  outcome public.nayanet_execution_outcomes;
begin
  if v_verifier is null then raise exception 'AUTH_REQUIRED'; end if;

  select * into r
  from public.nayanet_execution_receipts
  where id = p_receipt_id
  for share;

  if r.id is null then raise exception 'RECEIPT_NOT_FOUND'; end if;
  if r.action <> 'smart_mail_send' then raise exception 'UNSUPPORTED_OUTCOME_ACTION'; end if;
  if p_experiment_case_id is not null
     and r.experiment_case_id is not null
     and r.experiment_case_id <> p_experiment_case_id then
    raise exception 'EXPERIMENT_CASE_MISMATCH';
  end if;

  select * into m
  from public.v7_mail_messages
  where id = p_message_id;

  if m.id is null then raise exception 'MESSAGE_NOT_FOUND'; end if;
  if (m.metadata->>'execution_receipt_id') <> p_receipt_id::text then
    raise exception 'MESSAGE_RECEIPT_LINEAGE_MISMATCH';
  end if;
  if (m.metadata->>'receiver_id') <> v_verifier::text then
    raise exception 'VERIFIER_NOT_RECEIVER';
  end if;
  if not exists (
    select 1
    from public.v7_mail_members
    where thread_id = m.thread_id
      and user_id = v_verifier
  ) then
    raise exception 'RECEIVER_NOT_AUTHORIZED';
  end if;

  insert into public.nayanet_execution_outcomes(
    receipt_id,user_id,project_id,experiment_case_id,outcome_type,verifier_id,
    evidence,benefit,harm,cost,risk_adjusted_loss,verified,verification_method
  )
  values(
    r.id,r.user_id,r.project_id,r.experiment_case_id,'receiver_retrieval',v_verifier,
    jsonb_build_object(
      'message_id',m.id,
      'thread_id',m.thread_id,
      'receiver_id',v_verifier,
      'receiver_retrieved',true,
      'receiver_retrieved_at',now(),
      'source','authenticated_receiver_retrieval',
      'outcome_contract','NAYANET_REAL_OUTCOME_VALUE_V1'
    ),
    1,0,0,0,true,'authenticated receiver retrieval'
  )
  on conflict (receipt_id) do update
    set evidence=excluded.evidence,
        verifier_id=excluded.verifier_id,
        verified=true,
        verification_method=excluded.verification_method
  returning * into outcome;

  update public.nayanet_execution_receipts
    set value = coalesce(value,'{}'::jsonb)
      || jsonb_build_object(
        'schema','NAYANET_REAL_OUTCOME_VALUE_V1',
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
    'benefit',outcome.benefit,
    'harm',outcome.harm,
    'cost',outcome.cost,
    'risk_adjusted_loss',outcome.risk_adjusted_loss,
    'verification_method',outcome.verification_method,
    'evidence',outcome.evidence
  );
end;
$function$;

revoke all on function public.nayanet_record_smart_mail_outcome(uuid,uuid,text) from public,anon,authenticated;
grant execute on function public.nayanet_record_smart_mail_outcome(uuid,uuid,text) to authenticated,service_role;
