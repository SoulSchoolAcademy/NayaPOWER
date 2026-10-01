-- Legacy Cognition Disposition Classification V1
-- Scope: Priority #2 legacy cognition-event disposition.
-- Contract: applies explicit non-destructive disposition to the 88-event cohort.
-- Each cognition event in the legacy cohort receives one disposition row.
-- Original nayanet_cognition_events rows are NEVER modified.
-- Rationale is recorded per event for auditability.

-- Classifier function: returns disposition + rationale for a legacy cognition event.
create or replace function public.nayanet_classify_legacy_cognition_event(
  p_type text,
  p_classification text,
  p_source text
) returns record
language sql
stable
set search_path = public
as $$
  select
    case
      -- Smart Mail communication events already have execution receipts in nayanet_execution_receipts
      when p_type = 'communication' and p_classification = 'observation' and p_source = 'nayanet-smart-mail'
        then ('ALREADY_REPRESENTED_ELSEWHERE'::public.nayanet_legacy_cognition_disposition,
              'Smart Mail communication events have execution receipts in nayanet_execution_receipts; ledger would duplicate existing evidence chain.'::text)

      -- Name-First runtime proof observations are audit records, not canonical cognition for ledger
      when p_type = 'intelligence' and p_classification = 'observation' and p_source = 'nayanet-name-first-runtime-proof'
        then ('INTENTIONALLY_EXCLUDED'::public.nayanet_legacy_cognition_disposition,
              'Name-First runtime proof observations are verification/audit records; not canonical cognition requiring ledger integrity chain.'::text)

      -- Authenticated Assistant runtime proof observations are audit records
      when p_type = 'intelligence' and p_classification = 'observation' and p_source = 'nayanet-authenticated-assistant-proof'
        then ('INTENTIONALLY_EXCLUDED'::public.nayanet_legacy_cognition_disposition,
              'Authenticated Assistant runtime proof observations are verification/audit records; not canonical cognition requiring ledger integrity chain.'::text)

      -- Dream learning decision_context_test events are test scaffolding
      when p_type = 'intelligence' and p_classification = 'decision_context_test' and p_source = 'dream-learning-decision-proof'
        then ('INTENTIONALLY_EXCLUDED'::public.nayanet_legacy_cognition_disposition,
              'Dream learning decision_context_test events are test scaffolding for decision verification; not canonical cognition.'::text)

      -- Dream learning observation events are decision observation records
      when p_type = 'intelligence' and p_classification = 'observation' and p_source = 'dream-learning-decision-proof'
        then ('INTENTIONALLY_EXCLUDED'::public.nayanet_legacy_cognition_disposition,
              'Dream learning observation events are decision observation records; decision receipts already capture the verified outcome.'::text)

      -- NayaNET 10/10 readiness gate verification event
      when p_type = 'verification' and p_classification = 'authenticated_lifecycle' and p_source = 'NayaNET 10/10 readiness gate'
        then ('INTENTIONALLY_EXCLUDED'::public.nayanet_legacy_cognition_disposition,
              'Readiness gate verification event is a system health check; not canonical cognition requiring ledger integrity chain.'::text)

      -- Fallback: requires human review
      else ('NEEDS_REVIEW'::public.nayanet_legacy_cognition_disposition,
            'No automatic classification rule matched; requires explicit human review before disposition.'::text)
    end;
$$;

-- Apply classification to the exact legacy cohort (events with no Smart Ledger entry)
-- This is idempotent: safe to re-run, will not duplicate due to unique constraint on cognition_event_id.
insert into public.nayanet_legacy_cognition_disposition (
  owner_id,
  cognition_event_id,
  disposition,
  rationale,
  classified_by,
  cohort_fingerprint_sha256
)
select
  c.user_id as owner_id,
  c.id as cognition_event_id,
  cls.disposition,
  cls.rationale,
  c.user_id as classified_by,  -- classified by the event owner (system classification)
  (
    select coalesce(encode(extensions.digest(string_agg(c2.id::text, '|' order by c2.id::text), 'sha256'), 'hex'), '')
      from public.nayanet_cognition_events c2
     where not exists (
       select 1 from public.nayanet_smart_ledger sl
        where sl.source_table = 'nayanet_cognition_events'
          and sl.source_id = c2.id::text
     )
  ) as cohort_fingerprint_sha256
from public.nayanet_cognition_events c
cross join lateral public.nayanet_classify_legacy_cognition_event(c.type, c.classification, c.source) as cls(disposition, rationale)
where not exists (
  select 1 from public.nayanet_smart_ledger sl
   where sl.source_table = 'nayanet_cognition_events'
     and sl.source_id = c.id::text
)
on conflict (cognition_event_id) do nothing;

comment on function public.nayanet_classify_legacy_cognition_event(text,text,text) is 'Deterministic classification function for legacy cognition cohort. Returns (disposition, rationale). Pure function based on type/classification/source only.';