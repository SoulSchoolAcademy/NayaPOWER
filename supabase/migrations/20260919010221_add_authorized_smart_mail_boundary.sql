create or replace function public.nayanet_send_smart_mail_authorized(
  p_sender_id uuid,
  p_receiver_id uuid,
  p_body text,
  p_subject text,
  p_kind text,
  p_idempotency_key text,
  p_project_id text,
  p_policy_id uuid default null,
  p_experiment_case_id text default null,
  p_policy_input_hash text default null,
  p_policy_decision_hash text default null,
  p_authority_grant_id uuid default null
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $function$
declare
  v_authority jsonb;
  v_result jsonb;
  v_receipt_id uuid;
  v_message_id uuid;
begin
  if (select auth.uid()) is null then raise exception 'AUTH_REQUIRED'; end if;
  if (select auth.uid()) <> p_sender_id then raise exception 'SENDER_IDENTITY_MISMATCH'; end if;

  v_authority := public.nayanet_validate_authority_grant(
    p_authority_grant_id,
    'smart_mail_send',
    p_receiver_id::text
  );
  if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
    raise exception 'AUTHORITY_REQUIRED: %', coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
  end if;

  v_result := public.nayanet_send_smart_mail(
    p_sender_id,p_receiver_id,p_body,p_subject,p_kind,p_idempotency_key,p_project_id,
    p_policy_id,p_experiment_case_id,p_policy_input_hash,p_policy_decision_hash
  );

  if coalesce(v_result->>'status','') = 'CREATED' then
    v_receipt_id := (v_result->>'execution_receipt_id')::uuid;
    v_message_id := (v_result->>'message_id')::uuid;

    update public.nayanet_execution_receipts
       set authority_grant_id=(v_authority->>'grant_id')::uuid,
           authority_issuer_id=(v_authority->>'issuer_id')::uuid,
           authority_scope=v_authority->'scope',
           authority_actions=v_authority->'actions',
           authority_constraints=v_authority->'constraints',
           authority_status_at_execution=v_authority->>'grant_status',
           authority_source_event_id=v_authority->>'source_event_id',
           authority_validated_at=clock_timestamp()
     where id=v_receipt_id;

    update public.v7_mail_messages
       set metadata=metadata || jsonb_build_object(
         'authority_grant_id',v_authority->>'grant_id',
         'authority_source_event_id',v_authority->>'source_event_id',
         'authority_issuer_id',v_authority->>'issuer_id'
       )
     where id=v_message_id;

    return v_result || jsonb_build_object('authority_grant_id',v_authority->>'grant_id');
  end if;

  return v_result;
end;
$function$;

revoke execute on function public.nayanet_send_smart_mail(uuid,uuid,text,text,text,text,text) from public, anon, authenticated;
revoke execute on function public.nayanet_send_smart_mail(uuid,uuid,text,text,text,text,text,uuid,text,text,text) from public, anon, authenticated;
revoke all on function public.nayanet_send_smart_mail_authorized(uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid) from public, anon;
grant execute on function public.nayanet_send_smart_mail_authorized(uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid) to authenticated;
