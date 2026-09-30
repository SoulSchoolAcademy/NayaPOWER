-- Migration: SmartLedger V2.1 typed value receipts (runtime seam)
--
-- STATUS: candidate seam for Issue #1182 (left open for production/runtime proof)
-- and Issue #1184. Authored as PENDING_REVIEW_NOT_PRODUCTION_APPLIED.
-- Not production-applied. No merge/deploy implied by this file's existence.
--
-- ENVELOPE CONTRACT (schema 2.1):
-- Typed value receipts travel in the EXISTING public.nayanet_smart_ledger.value
-- jsonb column. This migration creates NO new table and NO parallel ledger.
--
-- A V2.1 envelope MUST satisfy all of:
--   value->>'receipt_type'  in ('ALIGNMENT_DECISION','CONTRIBUTION_VALUE')
--   value->>'value_engine'  =  'DECISION-VALUE-CALCULUS-V2.1'
--   value->>'assessment'    in ('ASSESSED','VERIFIED_VALUE')
--   ALIGNMENT_DECISION additionally requires value->'receipt' whose
--     receipt->>'receipt_type' = 'ALIGNMENT_DECISION'
--     (output of kernel/value_calculus.py build_decision_receipt)
--   CONTRIBUTION_VALUE additionally requires value ?& array[
--     'inputs','value_calculation','points_derivation',
--     'verification_state','provenance']
--
-- ASSESSMENT STATES (explicit on every qualifying future action):
--   UNASSESSED     - historical NayaNET_V1_STARTING_MODEL rows, e.g.
--                    {"assessed":false,"base_points":5|10,...}. Preserved EXACTLY
--                    as historical provenance. NEVER reinterpreted, NEVER
--                    upgraded, NEVER rescored by this seam.
--   ASSESSED       - V2.1 evaluated; verification still pending
--                    (e.g. PASS_PENDING_WINDOW, or contribution scored but
--                    not yet verified).
--   VERIFIED_VALUE - outcome observed and verified; delta_v_actual recorded.
--
-- CONSTITUTIONAL INVARIANTS (do not move silently):
--   ACTIVITY != VALUE. ENGAGEMENT != VERIFICATION. REPUTATION != AUTHORITY.
--   EVIDENCE before REWARD: unverified contribution derives zero points.
--   Points never appear in authority_basis and never grant authority.
--   Human worth is outside the equation; no receipt scores a person.
--   PostgreSQL jsonb rejects NaN/Infinity at parse time, so every stored
--   envelope is strict JSON by construction.

create or replace function public.nayanet_record_value_receipt(
  p_owner_id uuid,
  p_actor_id uuid,
  p_event_type text,
  p_source_table text,
  p_source_id text,
  p_value jsonb,
  p_verification jsonb default '{}'::jsonb,
  p_evidence_refs jsonb default '[]'::jsonb,
  p_outcome jsonb default '{}'::jsonb,
  p_privacy_classification text default 'PRIVATE',
  p_status text default 'RECORDED',
  p_parent_ledger_event_id uuid default null,
  p_metadata jsonb default '{}'::jsonb,
  p_event_at timestamptz default now()
) returns public.nayanet_smart_ledger
language plpgsql security definer set search_path=public,extensions as $$
declare
  v_receipt_type text;
  v_engine text;
  v_assessment text;
begin
  if jsonb_typeof(coalesce(p_value, 'null'::jsonb)) <> 'object' then
    raise exception 'VALUE_RECEIPT_MALFORMED';
  end if;
  v_receipt_type := p_value->>'receipt_type';
  v_engine := p_value->>'value_engine';
  v_assessment := p_value->>'assessment';
  if v_receipt_type not in ('ALIGNMENT_DECISION','CONTRIBUTION_VALUE') then
    raise exception 'VALUE_RECEIPT_MALFORMED';
  end if;
  if v_engine is distinct from 'DECISION-VALUE-CALCULUS-V2.1' then
    raise exception 'VALUE_RECEIPT_UNKNOWN_ENGINE';
  end if;
  if v_assessment not in ('ASSESSED','VERIFIED_VALUE') then
    raise exception 'VALUE_RECEIPT_BAD_ASSESSMENT';
  end if;
  if v_receipt_type = 'ALIGNMENT_DECISION' then
    if not (p_value ? 'receipt')
       or coalesce(p_value->'receipt'->>'receipt_type', '') <> 'ALIGNMENT_DECISION' then
      raise exception 'VALUE_RECEIPT_MALFORMED';
    end if;
  else
    if not (p_value ?& array['inputs','value_calculation','points_derivation',
                             'verification_state','provenance']) then
      raise exception 'VALUE_RECEIPT_MALFORMED';
    end if;
  end if;
  return public.nayanet_record_ledger_event(
    p_owner_id,
    p_event_type,
    p_source_table,
    p_source_id,
    p_event_at,
    p_actor_id,
    p_privacy_classification,
    p_status,
    coalesce(p_evidence_refs, '[]'::jsonb),
    coalesce(p_verification, '{}'::jsonb),
    p_value,
    coalesce(p_outcome, '{}'::jsonb),
    '[]'::jsonb,
    coalesce(p_metadata, '{}'::jsonb),
    p_parent_ledger_event_id
  );
end; $$;

revoke execute on function public.nayanet_record_value_receipt(uuid,uuid,text,text,text,jsonb,jsonb,jsonb,jsonb,text,text,uuid,jsonb,timestamptz) from public,anon,authenticated;

comment on function public.nayanet_record_value_receipt(uuid,uuid,text,text,text,jsonb,jsonb,jsonb,jsonb,text,text,uuid,jsonb,timestamptz) is
'Validated writer for V2.1 typed value receipts (ALIGNMENT_DECISION / CONTRIBUTION_VALUE) into the existing SmartLedger. Rejects malformed envelopes, unknown engines, and bad assessment states before any write. Legacy NayaNET_V1_STARTING_MODEL rows are not writable through this path.';

-- Derived projection: score/level are COMPUTED from receipt evidence on every
-- read. No score is stored as an unexplained magic number. Legacy V1 rows are
-- excluded by the value_engine filter and preserved untouched.
create or replace view public.nayanet_value_receipt_summary with (security_invoker=true) as
select
  l.owner_id,
  count(*) filter (where l.value->>'receipt_type' = 'ALIGNMENT_DECISION')::bigint as decision_receipts,
  count(*) filter (where l.value->>'receipt_type' = 'CONTRIBUTION_VALUE')::bigint as contribution_receipts,
  coalesce(sum((l.value->'points_derivation'->>'points')::numeric)
    filter (where l.value->>'receipt_type' = 'CONTRIBUTION_VALUE'
              and l.value->>'assessment' = 'VERIFIED_VALUE'), 0) as verified_points,
  coalesce(sum((l.value->'points_derivation'->>'points')::numeric)
    filter (where l.value->>'receipt_type' = 'CONTRIBUTION_VALUE'
              and l.value->>'assessment' = 'ASSESSED'), 0) as assessed_pending_points,
  max(l.event_at) as last_receipt_at
from public.nayanet_smart_ledger l
where l.value->>'value_engine' = 'DECISION-VALUE-CALCULUS-V2.1'
group by l.owner_id;

comment on view public.nayanet_value_receipt_summary is
'Derived projection of V2.1 typed value receipts for the future Hub. Points and levels are computed from receipt evidence on every read, never stored as magic numbers. security_invoker keeps owner isolation (RLS) intact.';
