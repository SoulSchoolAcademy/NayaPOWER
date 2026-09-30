-- 20261001040000_nayanet_value_receipts_v21_v1.sql
--
-- Typed Decision Value Calculus V2.1 receipts through the EXISTING SmartLedger.
--
-- Design constraints (Human Director):
--   * No second physical ledger. The existing public.nayanet_smart_ledger
--     table and nayanet_record_ledger_event() writer are unchanged.
--   * Typed receipts travel in the existing `value` JSONB column.
--   * Historical NayaNET_V1_STARTING_MODEL rows (assessed=false,
--     base_points 5/10) are preserved byte-identical. They are NOT rewritten
--     or reinterpreted; the assessment view classifies them as UNASSESSED.
--   * New scored records must identify: scoring engine/version, inputs,
--     evidence, verification state, value calculation, points derivation,
--     and provenance.
--   * Raw engagement never equals verified value: points_awarded > 0 is
--     rejected unless verification_state = 'VERIFIED_PASS' (evidence before
--     reward).
--   * Reputation/points never create authority: these receipts carry no
--     authority claim and no authority is derived from them.
--
-- Receipt envelope (mirrors kernel/smart_ledger_value.py):
--   receipt_type: ALIGNMENT_DECISION | CONTRIBUTION_VALUE
--   engine: DECISION-VALUE-CALCULUS-V2.1, engine_version: 2.1
--   verification_state: UNVERIFIED | PASS_PENDING_WINDOW | VERIFIED_PASS | FAIL | ESCALATE
--   inputs, evidence[], value_calculation, points_derivation, provenance{owner_id, source_table, source_id}

create or replace function public.nayanet_value_receipt_validate(p_receipt jsonb)
returns void
language plpgsql immutable
set search_path = public, extensions
as $$
declare
  v_type text;
  v_state text;
  v_points numeric;
  v_cvs numeric;
begin
  if p_receipt is null or jsonb_typeof(p_receipt) <> 'object' then
    raise exception 'VALUE_RECEIPT_INVALID: receipt must be a JSON object';
  end if;

  v_type := p_receipt ->> 'receipt_type';
  if v_type not in ('ALIGNMENT_DECISION', 'CONTRIBUTION_VALUE') then
    raise exception 'VALUE_RECEIPT_INVALID: receipt_type must be ALIGNMENT_DECISION or CONTRIBUTION_VALUE';
  end if;

  if p_receipt ->> 'engine' <> 'DECISION-VALUE-CALCULUS-V2.1' then
    raise exception 'VALUE_RECEIPT_INVALID: engine must be DECISION-VALUE-CALCULUS-V2.1';
  end if;
  if p_receipt ->> 'engine_version' <> '2.1' then
    raise exception 'VALUE_RECEIPT_INVALID: engine_version must be 2.1';
  end if;

  v_state := p_receipt ->> 'verification_state';
  if v_state not in ('UNVERIFIED', 'PASS_PENDING_WINDOW', 'VERIFIED_PASS', 'FAIL', 'ESCALATE') then
    raise exception 'VALUE_RECEIPT_INVALID: bad verification_state';
  end if;

  if jsonb_typeof(p_receipt -> 'inputs') <> 'object' or (p_receipt -> 'inputs') = '{}'::jsonb then
    raise exception 'VALUE_RECEIPT_INVALID: inputs must be a non-empty object';
  end if;
  if jsonb_typeof(p_receipt -> 'evidence') <> 'array' then
    raise exception 'VALUE_RECEIPT_INVALID: evidence must be an array';
  end if;
  if jsonb_typeof(p_receipt -> 'value_calculation') <> 'object' or (p_receipt -> 'value_calculation') = '{}'::jsonb then
    raise exception 'VALUE_RECEIPT_INVALID: value_calculation must be a non-empty object';
  end if;
  if jsonb_typeof(p_receipt -> 'points_derivation') <> 'object' then
    raise exception 'VALUE_RECEIPT_INVALID: points_derivation must be an object';
  end if;
  if jsonb_typeof(p_receipt -> 'provenance') <> 'object' then
    raise exception 'VALUE_RECEIPT_INVALID: provenance must be an object';
  end if;
  if nullif(p_receipt #>> '{provenance,owner_id}', '') is null
     or nullif(p_receipt #>> '{provenance,source_table}', '') is null
     or nullif(p_receipt #>> '{provenance,source_id}', '') is null then
    raise exception 'VALUE_RECEIPT_INVALID: provenance.owner_id/source_table/source_id are required';
  end if;
  if (p_receipt ->> 'privacy_classification') not in ('PRIVATE', 'SHARED', 'COLLECTIVE', 'PUBLIC') then
    raise exception 'VALUE_RECEIPT_INVALID: bad privacy_classification';
  end if;

  -- Evidence before reward: no points until value is verified.
  begin
    v_points := (p_receipt #>> '{points_derivation,points_awarded}')::numeric;
  exception when invalid_text_representation then
    raise exception 'VALUE_RECEIPT_INVALID: points_awarded must be numeric';
  end;
  if v_points is null or v_points < 0 then
    raise exception 'VALUE_RECEIPT_INVALID: points_awarded must be a non-negative number';
  end if;
  if v_state <> 'VERIFIED_PASS' and v_points <> 0 then
    raise exception 'VALUE_RECEIPT_INVALID: points_awarded must be 0 while verification_state=% (evidence before reward)', v_state;
  end if;

  if v_type = 'ALIGNMENT_DECISION' then
    if jsonb_typeof(p_receipt -> 'decision_receipt') <> 'object'
       or (p_receipt #>> '{decision_receipt,receipt_type}') <> 'ALIGNMENT_DECISION' then
      raise exception 'VALUE_RECEIPT_INVALID: ALIGNMENT_DECISION requires an embedded V2.1 decision_receipt';
    end if;
  else
    if nullif(p_receipt #>> '{inputs,action_class}', '') is null then
      raise exception 'VALUE_RECEIPT_INVALID: inputs.action_class is required';
    end if;
    if nullif(p_receipt #>> '{inputs,actor_id}', '') is null then
      raise exception 'VALUE_RECEIPT_INVALID: inputs.actor_id is required';
    end if;
    begin
      v_cvs := (p_receipt #>> '{value_calculation,cvs}')::numeric;
    exception when invalid_text_representation then
      raise exception 'VALUE_RECEIPT_INVALID: value_calculation.cvs must be numeric';
    end;
    if v_cvs is null or v_cvs < -9 or v_cvs > 9 then
      raise exception 'VALUE_RECEIPT_INVALID: value_calculation.cvs must be in [-9, 9]';
    end if;
    if jsonb_typeof(p_receipt #> '{value_calculation,factors}') <> 'object'
       or (p_receipt #> '{value_calculation,factors}') = '{}'::jsonb then
      raise exception 'VALUE_RECEIPT_INVALID: value_calculation.factors must be a non-empty object';
    end if;
  end if;

  return;
end;
$$;

comment on function public.nayanet_value_receipt_validate(jsonb) is
'Validates a typed V2.1 value receipt envelope. Raises VALUE_RECEIPT_INVALID with a reason on any violation. Mirrors kernel/smart_ledger_value.py.';


-- Typed writer: validates, enforces owner isolation, then records through the
-- existing nayanet_record_ledger_event(). Idempotent on
-- (owner_id, source_table, source_id): a replay returns the existing row
-- unchanged (receipts are immutable once written).
create or replace function public.nayanet_record_value_receipt(
  p_owner_id uuid,
  p_receipt jsonb,
  p_event_at timestamptz default now(),
  p_actor_id uuid default null,
  p_privacy_classification text default 'PRIVATE',
  p_qualified_by uuid default null
)
returns public.nayanet_smart_ledger
language plpgsql security definer
set search_path = public, extensions
as $$
declare
  v_row public.nayanet_smart_ledger;
  v_receipt_owner uuid;
  v_source_table text;
  v_source_id text;
  v_event_type text;
begin
  perform public.nayanet_value_receipt_validate(p_receipt);

  -- Cross-owner isolation at write time: the caller cannot record a receipt
  -- whose provenance names a different owner.
  begin
    v_receipt_owner := (p_receipt #>> '{provenance,owner_id}')::uuid;
  exception when invalid_text_representation then
    raise exception 'VALUE_RECEIPT_INVALID: provenance.owner_id must be a uuid';
  end;
  if v_receipt_owner is null or v_receipt_owner <> p_owner_id then
    raise exception 'VALUE_RECEIPT_OWNER_MISMATCH';
  end if;

  if p_privacy_classification not in ('PRIVATE', 'SHARED', 'COLLECTIVE', 'PUBLIC') then
    raise exception 'VALUE_RECEIPT_INVALID: bad privacy_classification';
  end if;

  v_event_type := p_receipt ->> 'receipt_type';
  v_source_table := p_receipt #>> '{provenance,source_table}';
  v_source_id := p_receipt #>> '{provenance,source_id}';

  v_row := public.nayanet_record_ledger_event(
    p_owner_id, v_event_type, v_source_table, v_source_id, p_event_at,
    coalesce(p_actor_id, v_receipt_owner),
    p_privacy_classification,
    case when (p_receipt ->> 'verification_state') = 'VERIFIED_PASS' then 'VERIFIED' else 'RECORDED' end,
    coalesce(p_receipt -> 'evidence', '[]'::jsonb),
    jsonb_build_object(
      'verification_state', p_receipt ->> 'verification_state',
      'receipt_schema', coalesce(p_receipt ->> 'receipt_schema', 'nayanet.value_receipt/v1')
    ),
    p_receipt,
    jsonb_build_object('engine', p_receipt ->> 'engine', 'engine_version', p_receipt ->> 'engine_version'),
    '[]'::jsonb,
    jsonb_build_object(
      'writer', 'nayanet_record_value_receipt',
      'receipt_hash_hint', left(encode(extensions.digest(p_receipt::text, 'sha256'), 'hex'), 16)
    )
  );

  -- Link back to the original assessed event when this receipt qualifies it.
  if p_qualified_by is not null and v_row.qualified_by_ledger_event_id is null then
    update public.nayanet_smart_ledger
       set qualified_by_ledger_event_id = p_qualified_by
     where ledger_event_id = v_row.ledger_event_id
    returning * into v_row;
  end if;

  return v_row;
exception
  when raise_exception then raise;
end;
$$;

revoke execute on function public.nayanet_record_value_receipt(uuid, jsonb, timestamptz, uuid, text, uuid)
  from public, anon, authenticated;

comment on function public.nayanet_record_value_receipt(uuid, jsonb, timestamptz, uuid, text, uuid) is
'Records a validated typed V2.1 value receipt (ALIGNMENT_DECISION or CONTRIBUTION_VALUE) into the existing nayanet_smart_ledger. Cross-owner writes rejected; replays return the existing immutable row.';


-- Read-time reconciliation: every ledger row classifies as
-- UNASSESSED / ASSESSED / VERIFIED_VALUE without modifying history.
-- Historical NayaNET_V1_STARTING_MODEL rows (assessed=false, base_points
-- 5/10) classify as UNASSESSED with provenance LEGACY_STARTING_MODEL.
create or replace view public.nayanet_ledger_value_assessment
with (security_invoker = true) as
select
  l.ledger_event_id,
  l.owner_id,
  l.event_type,
  l.event_at,
  l.source_table,
  l.source_id,
  l.privacy_classification,
  l.status,
  case
    when jsonb_typeof(l.value) = 'object'
         and (l.value ->> 'receipt_type') in ('ALIGNMENT_DECISION', 'CONTRIBUTION_VALUE')
         and (l.value ->> 'engine') = 'DECISION-VALUE-CALCULUS-V2.1'
         and (l.value ->> 'verification_state') = 'VERIFIED_PASS'
      then 'VERIFIED_VALUE'
    when jsonb_typeof(l.value) = 'object'
         and (l.value ->> 'receipt_type') in ('ALIGNMENT_DECISION', 'CONTRIBUTION_VALUE')
         and (l.value ->> 'engine') = 'DECISION-VALUE-CALCULUS-V2.1'
      then 'ASSESSED'
    else 'UNASSESSED'
  end as value_assessment,
  case
    when jsonb_typeof(l.value) = 'object'
         and (l.value ->> 'value_engine') = 'NayaNET_V1_STARTING_MODEL'
      then 'LEGACY_STARTING_MODEL'
    when jsonb_typeof(l.value) = 'object'
         and (l.value ->> 'receipt_type') in ('ALIGNMENT_DECISION', 'CONTRIBUTION_VALUE')
         and (l.value ->> 'engine') = 'DECISION-VALUE-CALCULUS-V2.1'
      then 'V2.1_TYPED_RECEIPT'
    else 'NONE'
  end as value_provenance
from public.nayanet_smart_ledger l;

comment on view public.nayanet_ledger_value_assessment is
'Read-time value reconciliation: UNASSESSED / ASSESSED / VERIFIED_VALUE per ledger row. Legacy NayaNET_V1_STARTING_MODEL rows are preserved untouched and classify as UNASSESSED. security_invoker so the base table RLS (owner isolation) applies.';
