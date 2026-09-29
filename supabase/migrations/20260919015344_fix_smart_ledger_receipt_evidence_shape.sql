create or replace function public.nayanet_execution_receipt_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
declare v_evidence jsonb;
begin
 v_evidence:=case when jsonb_typeof(coalesce(new.evidence,'{}'::jsonb))='array' then coalesce(new.evidence,'[]'::jsonb) else jsonb_build_array(coalesce(new.evidence,'{}'::jsonb)) end;
 perform public.nayanet_record_ledger_event(
  new.user_id,'EXECUTION_RECEIPT','nayanet_execution_receipts',new.id::text,new.created_at,null,'PRIVATE',
  case when new.status='SUCCESS' then 'VERIFIED' when new.status='BLOCKED' then 'BLOCKED' when new.status='FAILED' then 'FAILED' else 'RECORDED' end,
  v_evidence,jsonb_build_object('receipt_status',new.status,'authority_grant_id',new.authority_grant_id,'policy_id',new.policy_id),
  coalesce(new.value,'{}'::jsonb),jsonb_build_object('observed_result',new.observed_result),
  case when jsonb_typeof(coalesce(new.learning,'[]'::jsonb))='array' then coalesce(new.learning,'[]'::jsonb) else jsonb_build_array(new.learning) end,
  jsonb_build_object('action',new.action,'project_id',new.project_id,'revision',new.revision)
 );
 return new;
end; $$;
