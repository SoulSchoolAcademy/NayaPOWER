
create or replace function public.nayanet_execution_receipt_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 perform public.nayanet_record_ledger_event(
  new.user_id,'EXECUTION_RECEIPT','nayanet_execution_receipts',new.id::text,new.created_at,null,'PRIVATE',
  case when new.status='SUCCESS' then 'VERIFIED' when new.status='BLOCKED' then 'BLOCKED' when new.status='FAILED' then 'FAILED' else 'RECORDED' end,
  coalesce(new.evidence,'[]'::jsonb),jsonb_build_object('receipt_status',new.status,'authority_grant_id',new.authority_grant_id,'policy_id',new.policy_id),
  coalesce(new.value,'{}'::jsonb),jsonb_build_object('observed_result',new.observed_result),
  coalesce(new.learning,'[]'::jsonb),jsonb_build_object('action',new.action,'project_id',new.project_id,'revision',new.revision)
 );
 return new;
end; $$;
drop trigger if exists nayanet_execution_receipt_to_smart_ledger on public.nayanet_execution_receipts;
create trigger nayanet_execution_receipt_to_smart_ledger after insert on public.nayanet_execution_receipts for each row execute function public.nayanet_execution_receipt_to_ledger();

create or replace function public.nayanet_cognition_event_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 perform public.nayanet_record_ledger_event(
  new.user_id,'COGNITION_EVENT','nayanet_cognition_events',new.id::text,new.created_at,new.user_id,'PRIVATE',
  case when lower(new.status) in ('verified','success','completed','active') then 'RECORDED' else 'RECORDED' end,
  jsonb_build_array(jsonb_build_object('source_table','nayanet_cognition_events','source_id',new.id::text)),
  jsonb_build_object('status',new.status,'confidence',new.confidence,'receipt_id',new.receipt_id),
  '{}'::jsonb,'{}'::jsonb,'[]'::jsonb,
  jsonb_build_object('event_id',new.event_id,'type',new.type,'classification',new.classification,'project_id',new.project_id,'parent_event_id',new.parent_event_id)
 );
 return new;
end; $$;
drop trigger if exists nayanet_cognition_event_to_smart_ledger on public.nayanet_cognition_events;
create trigger nayanet_cognition_event_to_smart_ledger after insert on public.nayanet_cognition_events for each row execute function public.nayanet_cognition_event_to_ledger();

create or replace function public.nayanet_report_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 perform public.nayanet_record_ledger_event(
  new.user_id,'INTELLIGENCE_REPORT','v7_intelligence_reports',new.id::text,new.created_at,new.user_id,'PRIVATE',
  'RECORDED','[]'::jsonb,jsonb_build_object('status',new.status),
  '{}'::jsonb,'{}'::jsonb,'[]'::jsonb,
  jsonb_build_object('period_type',new.period_type,'period_start',new.period_start,'period_end',new.period_end)
 );
 return new;
end; $$;
drop trigger if exists nayanet_report_to_smart_ledger on public.v7_intelligence_reports;
create trigger nayanet_report_to_smart_ledger after insert on public.v7_intelligence_reports for each row execute function public.nayanet_report_to_ledger();

create or replace function public.nayanet_learning_evidence_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 perform public.nayanet_record_ledger_event(
  new.member_id,'LEARNING_EVIDENCE','learning_evidence',new.id::text,new.created_at,new.member_id,'PRIVATE',
  case when lower(new.status) in ('verified','active','accepted') then 'VERIFIED' else 'RECORDED' end,
  jsonb_build_array(jsonb_build_object('source_table','learning_evidence','source_id',new.id::text)),
  jsonb_build_object('status',new.status,'verification_method',new.verification_method,'provenance',new.provenance),
  '{}'::jsonb,'{}'::jsonb,'[]'::jsonb,
  jsonb_build_object('target_id',new.target_id,'level',new.level,'claim',new.claim,'source_event_id',new.source_event_id)
 );
 return new;
end; $$;
drop trigger if exists nayanet_learning_evidence_to_smart_ledger on public.learning_evidence;
create trigger nayanet_learning_evidence_to_smart_ledger after insert on public.learning_evidence for each row execute function public.nayanet_learning_evidence_to_ledger();

create or replace function public.nayanet_space_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 perform public.nayanet_record_ledger_event(
  new.owner_member_id,'SMART_SPACE_CREATED','nayanet_spaces',new.id::text,new.created_at,new.owner_member_id,new.visibility,
  'RECORDED','[]'::jsonb,'{}'::jsonb,
  jsonb_build_object('assessed',false,'base_points',10,'value_engine','NayaNET_V1_STARTING_MODEL'),
  '{}'::jsonb,'[]'::jsonb,
  jsonb_build_object('name',new.name,'purpose',new.purpose,'visibility',new.visibility)
 );
 return new;
end; $$;
drop trigger if exists nayanet_space_to_smart_ledger on public.nayanet_spaces;
create trigger nayanet_space_to_smart_ledger after insert on public.nayanet_spaces for each row execute function public.nayanet_space_to_ledger();
