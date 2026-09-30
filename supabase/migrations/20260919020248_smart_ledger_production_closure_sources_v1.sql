
create or replace function public.nayanet_sync_ledger_source(
 p_owner_id uuid,p_source_table text,p_source_id text,p_status text default null,p_verification jsonb default null,
 p_value jsonb default null,p_outcome jsonb default null,p_learning_refs jsonb default null,p_metadata jsonb default null
) returns void language plpgsql security definer set search_path=public,extensions as $$
begin
 update public.nayanet_smart_ledger
 set status=coalesce(p_status,status),
     verification=case when p_verification is null then verification else verification||p_verification end,
     value=case when p_value is null then value else value||p_value end,
     outcome=case when p_outcome is null then outcome else outcome||p_outcome end,
     learning_refs=case when p_learning_refs is null then learning_refs else p_learning_refs end,
     metadata=case when p_metadata is null then metadata else metadata||p_metadata end
 where owner_id=p_owner_id and source_table=p_source_table and source_id=p_source_id;
end; $$;

create or replace function public.nayanet_smart_note_event_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 if tg_op='INSERT' then
  perform public.nayanet_record_ledger_event(new.member_id,'SMART_NOTE_EVENT','smart_note_events',new.id::text,new.created_at,new.member_id,
   case when new.privacy_state='SHARED' then 'SHARED' else 'PRIVATE' end,
   case when new.status='VERIFIED' then 'VERIFIED' else 'RECORDED' end,
   jsonb_build_array(jsonb_build_object('source_table','smart_note_events','source_id',new.id::text)),
   case when new.status='VERIFIED' then jsonb_build_object('status','VERIFIED','verified_at',new.verified_at) else '{}'::jsonb end,
   '{}'::jsonb,'{}'::jsonb,'[]'::jsonb,jsonb_build_object('subject',new.subject,'event_type',new.event_type));
 else
  perform public.nayanet_sync_ledger_source(new.member_id,'smart_note_events',new.id::text,
   case when new.status='VERIFIED' then 'VERIFIED' else 'RECORDED' end,
   jsonb_build_object('smart_note_status',new.status,'verified_at',new.verified_at));
 end if;
 return new;
end; $$;
drop trigger if exists nayanet_smart_note_event_to_smart_ledger on public.smart_note_events;
create trigger nayanet_smart_note_event_to_smart_ledger after insert or update on public.smart_note_events for each row execute function public.nayanet_smart_note_event_to_ledger();

create or replace function public.nayanet_smart_note_receipt_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
declare v_owner uuid;
begin
 select member_id into v_owner from public.smart_note_events where id=new.event_id;
 if v_owner is not null then
  perform public.nayanet_sync_ledger_source(v_owner,'smart_note_events',new.event_id::text,
   case when new.status='VERIFIED' then 'VERIFIED' else null end,
   jsonb_build_object('smart_note_receipt_id',new.id,'receipt_status',new.status,'verification',coalesce(new.verification,'{}'::jsonb)));
 end if;
 return new;
end; $$;
drop trigger if exists nayanet_smart_note_receipt_to_smart_ledger on public.smart_note_receipts;
create trigger nayanet_smart_note_receipt_to_smart_ledger after insert or update on public.smart_note_receipts for each row execute function public.nayanet_smart_note_receipt_to_ledger();

create or replace function public.nayanet_execution_receipt_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
declare v_evidence jsonb;
begin
 v_evidence:=case when jsonb_typeof(coalesce(new.evidence,'{}'::jsonb))='array' then coalesce(new.evidence,'[]'::jsonb) else jsonb_build_array(coalesce(new.evidence,'{}'::jsonb)) end;
 if tg_op='INSERT' then
  perform public.nayanet_record_ledger_event(new.user_id,'EXECUTION_RECEIPT','nayanet_execution_receipts',new.id::text,new.created_at,null,'PRIVATE',
   case when new.status='SUCCESS' then 'VERIFIED' when new.status='BLOCKED' then 'BLOCKED' when new.status='FAILED' then 'FAILED' else 'RECORDED' end,
   v_evidence,jsonb_build_object('receipt_status',new.status,'authority_grant_id',new.authority_grant_id,'policy_id',new.policy_id),
   coalesce(new.value,'{}'::jsonb),jsonb_build_object('observed_result',new.observed_result),
   case when jsonb_typeof(coalesce(new.learning,'[]'::jsonb))='array' then coalesce(new.learning,'[]'::jsonb) else jsonb_build_array(new.learning) end,
   jsonb_build_object('action',new.action,'project_id',new.project_id,'revision',new.revision));
 else
  perform public.nayanet_sync_ledger_source(new.user_id,'nayanet_execution_receipts',new.id::text,
   case when new.status='SUCCESS' then 'VERIFIED' when new.status='BLOCKED' then 'BLOCKED' when new.status='FAILED' then 'FAILED' else null end,
   jsonb_build_object('receipt_status',new.status,'evidence',v_evidence,'authority_grant_id',new.authority_grant_id,'policy_id',new.policy_id),
   coalesce(new.value,'{}'::jsonb),jsonb_build_object('observed_result',new.observed_result),
   case when jsonb_typeof(coalesce(new.learning,'[]'::jsonb))='array' then coalesce(new.learning,'[]'::jsonb) else jsonb_build_array(new.learning) end);
 end if;
 return new;
end; $$;
drop trigger if exists nayanet_execution_receipt_to_smart_ledger on public.nayanet_execution_receipts;
create trigger nayanet_execution_receipt_to_smart_ledger after insert or update on public.nayanet_execution_receipts for each row execute function public.nayanet_execution_receipt_to_ledger();

create or replace function public.nayanet_report_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 if tg_op='INSERT' then
  perform public.nayanet_record_ledger_event(new.user_id,'INTELLIGENCE_REPORT','v7_intelligence_reports',new.id::text,new.created_at,new.user_id,'PRIVATE','RECORDED','[]'::jsonb,jsonb_build_object('status',new.status),'{}'::jsonb,'{}'::jsonb,'[]'::jsonb,jsonb_build_object('period_type',new.period_type,'period_start',new.period_start,'period_end',new.period_end));
 else
  perform public.nayanet_sync_ledger_source(new.user_id,'v7_intelligence_reports',new.id::text,new.status,jsonb_build_object('report_status',new.status));
 end if;
 return new;
end; $$;
drop trigger if exists nayanet_report_to_smart_ledger on public.v7_intelligence_reports;
create trigger nayanet_report_to_smart_ledger after insert or update on public.v7_intelligence_reports for each row execute function public.nayanet_report_to_ledger();

create or replace function public.nayanet_learning_evidence_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 if tg_op='INSERT' then
  perform public.nayanet_record_ledger_event(new.member_id,'LEARNING_EVIDENCE','learning_evidence',new.id::text,new.created_at,new.member_id,'PRIVATE',
   case when lower(new.status)='active' then 'VERIFIED' else 'RECORDED' end,
   jsonb_build_array(jsonb_build_object('source_table','learning_evidence','source_id',new.id::text)),
   jsonb_build_object('status',new.status,'verification_method',new.verification_method,'provenance',new.provenance),'{}'::jsonb,'{}'::jsonb,'[]'::jsonb,
   jsonb_build_object('target_id',new.target_id,'level',new.level,'claim',new.claim,'source_event_id',new.source_event_id));
 else
  perform public.nayanet_sync_ledger_source(new.member_id,'learning_evidence',new.id::text,
   case when lower(new.status)='active' then 'VERIFIED' else 'RECORDED' end,
   jsonb_build_object('status',new.status,'verification_method',new.verification_method,'provenance',new.provenance));
 end if;
 return new;
end; $$;
drop trigger if exists nayanet_learning_evidence_to_smart_ledger on public.learning_evidence;
create trigger nayanet_learning_evidence_to_smart_ledger after insert or update on public.learning_evidence for each row execute function public.nayanet_learning_evidence_to_ledger();

create or replace function public.nayanet_learner_state_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 perform public.nayanet_record_ledger_event(new.member_id,'LEARNER_STATE','learner_states',new.member_id::text,coalesce(new.updated_at,now()),new.member_id,'PRIVATE','VERIFIED','[]'::jsonb,
  jsonb_build_object('learner_state_version',new.version,'last_meaningful_learning_at',new.last_meaningful_learning_at),'{}'::jsonb,'{}'::jsonb,'[]'::jsonb,
  jsonb_build_object('active_target_ids',new.active_target_ids,'demonstrated_capability_ids',new.demonstrated_capability_ids,'current_evidence_by_target',new.current_evidence_by_target));
 return new;
end; $$;
drop trigger if exists nayanet_learner_state_to_smart_ledger on public.learner_states;
create trigger nayanet_learner_state_to_smart_ledger after insert or update on public.learner_states for each row execute function public.nayanet_learner_state_to_ledger();

create or replace function public.nayanet_space_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 if tg_op='INSERT' then
  perform public.nayanet_record_ledger_event(new.owner_member_id,'SMART_SPACE','nayanet_spaces',new.id::text,new.created_at,new.owner_member_id,
   case when lower(new.visibility)='shared' then 'SHARED' else 'PRIVATE' end,'RECORDED','[]'::jsonb,'{}'::jsonb,jsonb_build_object('assessed',false,'base_points',10,'value_engine','NayaNET_V1_STARTING_MODEL'),'{}'::jsonb,'[]'::jsonb,
   jsonb_build_object('name',new.name,'purpose',new.purpose,'visibility',new.visibility));
 else
  perform public.nayanet_sync_ledger_source(new.owner_member_id,'nayanet_spaces',new.id::text,null,jsonb_build_object('visibility',new.visibility,'updated_at',new.updated_at));
 end if;
 return new;
end; $$;
drop trigger if exists nayanet_space_to_smart_ledger on public.nayanet_spaces;
create trigger nayanet_space_to_smart_ledger after insert or update on public.nayanet_spaces for each row execute function public.nayanet_space_to_ledger();
