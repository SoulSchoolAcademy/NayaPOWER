-- Decision Value Calculus V2.1 -> existing SmartLedger runtime seam.
-- This migration is forward-only. It does not rewrite historical ledger rows,
-- and it deliberately does not reinterpret NayaNET_V1_STARTING_MODEL base_points.
-- One ledger remains canonical; typed value receipts live in its value JSONB.

create or replace function public.nayanet_value_receipt_v2_1_state(
  p_receipt jsonb
) returns text
language plpgsql
immutable
set search_path=public,extensions
as $$
declare
  v_type text;
  v_verification text;
  v_key text;
  v_number numeric;
  v_points numeric;
begin
  if coalesce(jsonb_typeof(p_receipt),'') <> 'object' then
    raise exception 'VALUE_RECEIPT_MUST_BE_OBJECT' using errcode='22023';
  end if;

  v_type := p_receipt->>'receipt_type';
  if v_type not in ('ALIGNMENT_DECISION','CONTRIBUTION_VALUE') then
    raise exception 'VALUE_RECEIPT_TYPE_UNSUPPORTED' using errcode='22023';
  end if;

  if coalesce(p_receipt->>'schema_version','') <> '2.1' then
    raise exception 'VALUE_RECEIPT_SCHEMA_VERSION' using errcode='22023';
  end if;

  if coalesce(p_receipt->>'engine_version','') <> 'DECISION-VALUE-CALCULUS-V2.1' then
    raise exception 'VALUE_RECEIPT_ENGINE_VERSION' using errcode='22023';
  end if;

  if coalesce(jsonb_typeof(p_receipt->'evidence_refs'),'') <> 'array' then
    raise exception 'VALUE_RECEIPT_EVIDENCE_REFS' using errcode='22023';
  end if;

  if v_type = 'ALIGNMENT_DECISION' then
    if nullif(trim(coalesce(p_receipt->>'decision_id','')),'') is null
      or nullif(trim(coalesce(p_receipt->>'objective','')),'') is null
      or nullif(trim(coalesce(p_receipt->>'baseline_id','')),'') is null
      or nullif(trim(coalesce(p_receipt->>'authority_basis','')),'') is null then
      raise exception 'ALIGNMENT_DECISION_REQUIRED_FIELDS' using errcode='22023';
    end if;

    if coalesce(jsonb_typeof(p_receipt->'evaluation'),'') <> 'object'
      or coalesce(jsonb_typeof(p_receipt->'observation_window'),'') <> 'object' then
      raise exception 'ALIGNMENT_DECISION_OBJECT_FIELDS' using errcode='22023';
    end if;

    v_verification := p_receipt->>'verification';
    if v_verification not in ('UNVERIFIED','PASS_PENDING_WINDOW','VERIFIED_PASS','FAIL','ESCALATE') then
      raise exception 'ALIGNMENT_DECISION_VERIFICATION' using errcode='22023';
    end if;

    if v_verification = 'VERIFIED_PASS'
      and coalesce(jsonb_typeof(p_receipt->'delta_v_actual'),'') = 'number' then
      return 'VERIFIED_VALUE';
    end if;
    return 'ASSESSED';
  end if;

  if nullif(trim(coalesce(p_receipt->>'contribution_id','')),'') is null
    or nullif(trim(coalesce(p_receipt->>'action_class','')),'') is null then
    raise exception 'CONTRIBUTION_VALUE_REQUIRED_FIELDS' using errcode='22023';
  end if;

  if coalesce(jsonb_typeof(p_receipt->'provenance'),'') <> 'object'
    or coalesce(jsonb_typeof(p_receipt->'privacy'),'') <> 'object'
    or coalesce(jsonb_typeof(p_receipt->'raw_activity'),'') <> 'object'
    or coalesce(jsonb_typeof(p_receipt->'factors'),'') <> 'object'
    or coalesce(jsonb_typeof(p_receipt->'scoring_profile'),'') <> 'object' then
    raise exception 'CONTRIBUTION_VALUE_OBJECT_FIELDS' using errcode='22023';
  end if;

  if coalesce(p_receipt->'privacy'->>'classification','') not in ('PRIVATE','SHARED','COLLECTIVE','PUBLIC') then
    raise exception 'CONTRIBUTION_VALUE_PRIVACY' using errcode='22023';
  end if;

  foreach v_key in array array['quality','relevance','verification_strength','impact','novelty']
  loop
    if coalesce(jsonb_typeof(p_receipt->'factors'->v_key),'') <> 'number' then
      raise exception 'CONTRIBUTION_VALUE_FACTOR_TYPE:%', v_key using errcode='22023';
    end if;
    v_number := (p_receipt->'factors'->>v_key)::numeric;
    if v_number < 0 or v_number > 1 then
      raise exception 'CONTRIBUTION_VALUE_FACTOR_RANGE:%', v_key using errcode='22023';
    end if;
  end loop;

  if nullif(trim(coalesce(p_receipt->'scoring_profile'->>'id','')),'') is null
    or nullif(trim(coalesce(p_receipt->'scoring_profile'->>'version','')),'') is null then
    raise exception 'CONTRIBUTION_VALUE_PROFILE' using errcode='22023';
  end if;

  if coalesce(jsonb_typeof(p_receipt->'points_awarded'),'') <> 'number'
    or coalesce(jsonb_typeof(p_receipt->'cvs'),'') <> 'number' then
    raise exception 'CONTRIBUTION_VALUE_SCORE_TYPES' using errcode='22023';
  end if;

  v_points := (p_receipt->>'points_awarded')::numeric;
  if v_points < 0 then
    raise exception 'CONTRIBUTION_VALUE_POINTS_NEGATIVE' using errcode='22023';
  end if;

  v_number := (p_receipt->>'cvs')::numeric;
  if v_number < -9 or v_number > 9 then
    raise exception 'CONTRIBUTION_VALUE_CVS_RANGE' using errcode='22023';
  end if;

  v_verification := p_receipt->>'verification';
  if v_verification not in ('UNVERIFIED','OBSERVED','VERIFIED','FAIL','ESCALATE') then
    raise exception 'CONTRIBUTION_VALUE_VERIFICATION' using errcode='22023';
  end if;

  if v_verification <> 'VERIFIED' and v_points <> 0 then
    raise exception 'EVIDENCE_BEFORE_REWARD' using errcode='22023';
  end if;

  if v_verification = 'VERIFIED' then
    if coalesce(jsonb_typeof(p_receipt->'verified_delta'),'') <> 'number' then
      raise exception 'VERIFIED_CONTRIBUTION_REQUIRES_DELTA' using errcode='22023';
    end if;
    return 'VERIFIED_VALUE';
  end if;

  return 'ASSESSED';
end;
$$;

revoke all on function public.nayanet_value_receipt_v2_1_state(jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_value_receipt_v2_1_state(jsonb) to service_role;

create or replace function public.nayanet_execution_value_projection_v2_1(
  p_value jsonb
) returns jsonb
language plpgsql
immutable
set search_path=public,extensions
as $$
declare
  v_input jsonb := coalesce(p_value,'{}'::jsonb);
  v_state text;
begin
  if coalesce(jsonb_typeof(v_input),'') <> 'object' then
    return jsonb_build_object(
      'assessment_state','UNASSESSED',
      'value_contract_version','2.1',
      'value_engine_compat','LEGACY_UNCLASSIFIED',
      'legacy_value_payload',v_input
    );
  end if;

  if v_input ? 'receipt_type' then
    v_state := public.nayanet_value_receipt_v2_1_state(v_input);
    return v_input || jsonb_build_object(
      'assessment_state',v_state,
      'value_contract_version','2.1',
      'value_engine','DECISION-VALUE-CALCULUS-V2.1'
    );
  end if;

  return v_input || jsonb_build_object(
    'assessment_state','UNASSESSED',
    'value_contract_version','2.1',
    'value_engine_compat',
      case
        when v_input->>'value_engine' = 'NayaNET_V1_STARTING_MODEL' then 'NayaNET_V1_STARTING_MODEL'
        else 'LEGACY_UNCLASSIFIED'
      end,
    'legacy_value_preserved',
      ((v_input ? 'base_points') or v_input->>'value_engine' = 'NayaNET_V1_STARTING_MODEL')
  );
end;
$$;

revoke all on function public.nayanet_execution_value_projection_v2_1(jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_execution_value_projection_v2_1(jsonb) to service_role;

create or replace function public.nayanet_attach_value_receipt_v2_1(
  p_owner_id uuid,
  p_source_table text,
  p_source_id text,
  p_receipt jsonb
) returns public.nayanet_smart_ledger
language plpgsql
security definer
set search_path=public,extensions
as $$
declare
  v_row public.nayanet_smart_ledger;
  v_state text;
  v_existing jsonb;
begin
  if p_owner_id is null
    or nullif(trim(coalesce(p_source_table,'')),'') is null
    or nullif(trim(coalesce(p_source_id,'')),'') is null then
    raise exception 'VALUE_RECEIPT_SOURCE_REQUIRED' using errcode='22023';
  end if;

  v_state := public.nayanet_value_receipt_v2_1_state(p_receipt);

  select *
    into v_row
    from public.nayanet_smart_ledger
   where owner_id=p_owner_id
     and source_table=p_source_table
     and source_id=p_source_id
   for update;

  if not found then
    raise exception 'VALUE_RECEIPT_SOURCE_NOT_FOUND' using errcode='P0002';
  end if;

  v_existing := v_row.value->'v2_1_receipt';
  if v_existing is not null then
    if v_existing = p_receipt then
      return v_row;
    end if;
    raise exception 'VALUE_RECEIPT_ALREADY_ATTACHED' using errcode='23505';
  end if;

  update public.nayanet_smart_ledger
     set value = coalesce(value,'{}'::jsonb) || jsonb_build_object(
       'assessment_state',v_state,
       'value_contract_version','2.1',
       'value_engine','DECISION-VALUE-CALCULUS-V2.1',
       'v2_1_receipt',p_receipt,
       'legacy_value_preserved',
         ((coalesce(value,'{}'::jsonb) ? 'base_points')
           or coalesce(value->>'value_engine','') = 'NayaNET_V1_STARTING_MODEL')
     ),
     metadata = coalesce(metadata,'{}'::jsonb) || jsonb_build_object(
       'value_receipt_type',p_receipt->>'receipt_type',
       'value_assessment_state',v_state
     )
   where ledger_event_id=v_row.ledger_event_id
   returning * into v_row;

  return v_row;
end;
$$;

revoke all on function public.nayanet_attach_value_receipt_v2_1(uuid,text,text,jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_attach_value_receipt_v2_1(uuid,text,text,jsonb) to service_role;

create or replace function public.nayanet_execution_receipt_to_ledger()
returns trigger
language plpgsql
security definer
set search_path=public,extensions
as $$
declare
  v_evidence jsonb;
  v_value jsonb;
begin
  v_evidence := case
    when jsonb_typeof(coalesce(new.evidence,'{}'::jsonb))='array'
      then coalesce(new.evidence,'[]'::jsonb)
    else jsonb_build_array(coalesce(new.evidence,'{}'::jsonb))
  end;
  v_value := public.nayanet_execution_value_projection_v2_1(coalesce(new.value,'{}'::jsonb));

  if tg_op='INSERT' then
    perform public.nayanet_record_ledger_event(
      new.user_id,'EXECUTION_RECEIPT','nayanet_execution_receipts',new.id::text,new.created_at,null,'PRIVATE',
      case
        when new.status='SUCCESS' then 'VERIFIED'
        when new.status='BLOCKED' then 'BLOCKED'
        when new.status='FAILED' then 'FAILED'
        else 'RECORDED'
      end,
      v_evidence,
      jsonb_build_object(
        'receipt_status',new.status,
        'authority_grant_id',new.authority_grant_id,
        'policy_id',new.policy_id
      ),
      v_value,
      jsonb_build_object('observed_result',new.observed_result),
      case
        when jsonb_typeof(coalesce(new.learning,'[]'::jsonb))='array'
          then coalesce(new.learning,'[]'::jsonb)
        else jsonb_build_array(new.learning)
      end,
      jsonb_build_object('action',new.action,'project_id',new.project_id,'revision',new.revision)
    );
  else
    perform public.nayanet_sync_ledger_source(
      new.user_id,'nayanet_execution_receipts',new.id::text,
      case
        when new.status='SUCCESS' then 'VERIFIED'
        when new.status='BLOCKED' then 'BLOCKED'
        when new.status='FAILED' then 'FAILED'
        else null
      end,
      jsonb_build_object(
        'receipt_status',new.status,
        'evidence',v_evidence,
        'authority_grant_id',new.authority_grant_id,
        'policy_id',new.policy_id
      ),
      v_value,
      jsonb_build_object('observed_result',new.observed_result),
      case
        when jsonb_typeof(coalesce(new.learning,'[]'::jsonb))='array'
          then coalesce(new.learning,'[]'::jsonb)
        else jsonb_build_array(new.learning)
      end
    );
  end if;
  return new;
end;
$$;

revoke all on function public.nayanet_execution_receipt_to_ledger() from public,anon,authenticated;

create or replace function public.nayanet_smart_note_event_to_ledger()
returns trigger
language plpgsql
security definer
set search_path=public,extensions
as $$
begin
  if tg_op='INSERT' then
    perform public.nayanet_record_ledger_event(
      new.member_id,'SMART_NOTE_EVENT','smart_note_events',new.id::text,new.created_at,new.member_id,
      case when new.privacy_state='SHARED' then 'SHARED' else 'PRIVATE' end,
      case when new.status='VERIFIED' then 'VERIFIED' else 'RECORDED' end,
      jsonb_build_array(jsonb_build_object('source_table','smart_note_events','source_id',new.id::text)),
      case
        when new.status='VERIFIED'
          then jsonb_build_object('status','VERIFIED','verified_at',new.verified_at)
        else '{}'::jsonb
      end,
      jsonb_build_object(
        'assessment_state','UNASSESSED',
        'value_contract_version','2.1',
        'value_engine','DECISION-VALUE-CALCULUS-V2.1',
        'legacy_seed_policy','NOT_REISSUED'
      ),
      '{}'::jsonb,
      '[]'::jsonb,
      jsonb_build_object('subject',new.subject,'event_type',new.event_type)
    );
  else
    perform public.nayanet_sync_ledger_source(
      new.member_id,'smart_note_events',new.id::text,
      case when new.status='VERIFIED' then 'VERIFIED' else 'RECORDED' end,
      jsonb_build_object('smart_note_status',new.status,'verified_at',new.verified_at)
    );
  end if;
  return new;
end;
$$;

revoke all on function public.nayanet_smart_note_event_to_ledger() from public,anon,authenticated;

create or replace function public.nayanet_space_to_ledger()
returns trigger
language plpgsql
security definer
set search_path=public,extensions
as $$
begin
  if tg_op='INSERT' then
    perform public.nayanet_record_ledger_event(
      new.owner_member_id,'SMART_SPACE','nayanet_spaces',new.id::text,new.created_at,new.owner_member_id,
      case when lower(new.visibility)='shared' then 'SHARED' else 'PRIVATE' end,
      'RECORDED','[]'::jsonb,'{}'::jsonb,
      jsonb_build_object(
        'assessment_state','UNASSESSED',
        'value_contract_version','2.1',
        'value_engine','DECISION-VALUE-CALCULUS-V2.1',
        'legacy_seed_policy','NOT_REISSUED'
      ),
      '{}'::jsonb,'[]'::jsonb,
      jsonb_build_object('name',new.name,'purpose',new.purpose,'visibility',new.visibility)
    );
  else
    perform public.nayanet_sync_ledger_source(
      new.owner_member_id,'nayanet_spaces',new.id::text,null,null,null,null,null,
      jsonb_build_object('visibility',new.visibility,'updated_at',new.updated_at)
    );
  end if;
  return new;
end;
$$;

revoke all on function public.nayanet_space_to_ledger() from public,anon,authenticated;

comment on function public.nayanet_attach_value_receipt_v2_1(uuid,text,text,jsonb)
is 'Attach one immutable V2.1 ALIGNMENT_DECISION or CONTRIBUTION_VALUE receipt to an existing owner-scoped SmartLedger source row. Same-receipt replay is idempotent; conflicting replacement fails closed.';

comment on function public.nayanet_value_receipt_v2_1_state(jsonb)
is 'Validates Decision Value Calculus V2.1 typed receipts and returns ASSESSED or VERIFIED_VALUE. It never grants authority.';

-- Proof markers: no historical UPDATE/backfill occurs in this migration.
select 'DECISION_VALUE_SMART_LEDGER_V2_1_READY' as migration;
