-- supabase/tests/nayanet_value_receipts_v21_tests.sql
--
-- Deterministic runtime tests for 20261001040000_nayanet_value_receipts_v21_v1.sql.
--
-- Run against a NON-PRODUCTION database (dev/staging) with psql:
--   psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f supabase/tests/nayanet_value_receipts_v21_tests.sql
--
-- The whole script runs inside one transaction and ROLLBACKs at the end:
-- it is non-destructive by construction. Write-path tests are skipped with a
-- NOTICE when auth.users has no row to borrow as a test owner.
--
-- Covers: validator (valid + malformed), evidence-before-reward, typed writer,
-- replay/idempotency, cross-owner isolation, privacy, legacy V1 preservation
-- and classification, qualified_by linkage.

begin;

create temp table vr_results(name text, passed boolean);

do $$
declare
  v_owner uuid;
  v_owner_b uuid;
  v_receipt jsonb;
  v_bad jsonb;
  v_row public.nayanet_smart_ledger;
  v_row2 public.nayanet_smart_ledger;
  v_legacy_id uuid;
  v_assessment text;
  v_provenance text;
begin
  select id into v_owner from auth.users order by created_at limit 1;

  -- Base valid receipt (parameterized inline where variants are needed).
  v_receipt := jsonb_build_object(
    'receipt_type', 'CONTRIBUTION_VALUE',
    'receipt_schema', 'nayanet.value_receipt/v1',
    'engine', 'DECISION-VALUE-CALCULUS-V2.1',
    'engine_version', '2.1',
    'assessment', 'ASSESSED',
    'verification_state', 'VERIFIED_PASS',
    'privacy_classification', 'PRIVATE',
    'inputs', jsonb_build_object(
      'actor_id', coalesce(v_owner, gen_random_uuid())::text,
      'action_class', 'verified_intelligence',
      'quality', 0.8, 'relevance', 0.9, 'verification', 1.0,
      'impact', 0.7, 'novelty', 0.8, 'verified_delta', 3.0,
      'repeat_count', 1, 'scoring_profile', 'contribution-profile/v1'),
    'evidence', jsonb_build_array(
      jsonb_build_object('source_table', 'smart_note_receipts', 'source_id', 'r-1')),
    'value_calculation', jsonb_build_object(
      'cvs', 7.5,
      'factors', jsonb_build_object('quality', 0.8, 'relevance', 0.9,
        'verification', 1.0, 'impact', 0.7, 'novelty', 0.8),
      'verified_delta', 3.0,
      'formula', 'sign(verified_delta)*9*(quality*relevance*verification*impact*novelty)^(1/5)'),
    'points_derivation', jsonb_build_object(
      'points_per_unit', 10.0, 'repeat_count', 1, 'repeat_decay', 1.0,
      'points_awarded', 75,
      'basis', 'positive recognition from verified value only'),
    'provenance', jsonb_build_object(
      'owner_id', coalesce(v_owner, gen_random_uuid())::text,
      'source_table', 'smart_note_events',
      'source_id', 'note-test-1',
      'actor_id', coalesce(v_owner, gen_random_uuid())::text,
      'recorded_by', coalesce(v_owner, gen_random_uuid())::text,
      'recorded_at', now()::text,
      'ledger', 'public.nayanet_smart_ledger',
      'writer', 'nayanet_record_value_receipt',
      'scoring_profile', 'contribution-profile/v1')
  );

  -- ---- validator: valid ----
  begin
    perform public.nayanet_value_receipt_validate(v_receipt);
    insert into vr_results values ('validator accepts valid CONTRIBUTION_VALUE receipt', true);
  exception when others then
    insert into vr_results values ('validator accepts valid CONTRIBUTION_VALUE receipt', false);
  end;

  -- ---- validator: malformed (each must raise VALUE_RECEIPT_INVALID) ----
  v_bad := v_receipt || '{"receipt_type":"POINTS"}';
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject bad receipt_type', false);
  exception when raise_exception then
    insert into vr_results values ('reject bad receipt_type', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := v_receipt || '{"engine":"NOPE"}';
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject bad engine', false);
  exception when raise_exception then
    insert into vr_results values ('reject bad engine', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := v_receipt || '{"engine_version":"1.0"}';
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject bad engine_version', false);
  exception when raise_exception then
    insert into vr_results values ('reject bad engine_version', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := v_receipt || '{"verification_state":"MAYBE"}';
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject bad verification_state', false);
  exception when raise_exception then
    insert into vr_results values ('reject bad verification_state', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := v_receipt || '{"inputs":{}}';
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject empty inputs', false);
  exception when raise_exception then
    insert into vr_results values ('reject empty inputs', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := v_receipt || '{"evidence":{}}';
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject non-array evidence', false);
  exception when raise_exception then
    insert into vr_results values ('reject non-array evidence', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := jsonb_set(v_receipt, '{provenance}', (v_receipt->'provenance') - 'owner_id');
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject provenance without owner_id', false);
  exception when raise_exception then
    insert into vr_results values ('reject provenance without owner_id', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := v_receipt || '{"privacy_classification":"SUPER_PUBLIC"}';
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject bad privacy_classification', false);
  exception when raise_exception then
    insert into vr_results values ('reject bad privacy_classification', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := jsonb_set(v_receipt, '{value_calculation,cvs}', '99');
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject cvs out of [-9,9]', false);
  exception when raise_exception then
    insert into vr_results values ('reject cvs out of [-9,9]', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  v_bad := jsonb_set(v_receipt, '{value_calculation,factors}', '{}');
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject empty factors', false);
  exception when raise_exception then
    insert into vr_results values ('reject empty factors', sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  -- evidence before reward: points_awarded > 0 while UNVERIFIED
  v_bad := jsonb_set(v_receipt, '{verification_state}', '"UNVERIFIED"');
  v_bad := jsonb_set(v_bad, '{points_derivation,points_awarded}', '5');
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject points_awarded>0 while UNVERIFIED', false);
  exception when raise_exception then
    insert into vr_results values ('reject points_awarded>0 while UNVERIFIED',
      sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  -- legacy V1 row is NOT a valid typed receipt (no silent reinterpretation)
  v_bad := '{"assessed":false,"base_points":5,"value_engine":"NayaNET_V1_STARTING_MODEL"}';
  begin perform public.nayanet_value_receipt_validate(v_bad);
    insert into vr_results values ('reject legacy V1 row as typed receipt', false);
  exception when raise_exception then
    insert into vr_results values ('reject legacy V1 row as typed receipt',
      sqlerrm like 'VALUE_RECEIPT_INVALID%');
  end;

  -- ---- writer path (needs a real owner) ----
  if v_owner is null then
    raise notice 'SKIP write-path tests: no auth.users row available';
  else
    v_owner_b := gen_random_uuid();

    v_row := public.nayanet_record_value_receipt(v_owner, v_receipt);
    insert into vr_results values ('writer records a valid typed receipt',
      v_row.event_type = 'CONTRIBUTION_VALUE'
      and (v_row.value ->> 'engine') = 'DECISION-VALUE-CALCULUS-V2.1'
      and v_row.privacy_classification = 'PRIVATE');

    -- replay: same (owner, source_table, source_id) returns the SAME row
    v_row2 := public.nayanet_record_value_receipt(
      v_owner, jsonb_set(v_receipt, '{points_derivation,points_awarded}', '999999'));
    insert into vr_results values ('replay is idempotent and immutable',
      v_row2.ledger_event_id = v_row.ledger_event_id
      and (v_row2.value #>> '{points_derivation,points_awarded}') = '75');

    -- cross-owner isolation
    begin
      perform public.nayanet_record_value_receipt(v_owner_b, v_receipt);
      insert into vr_results values ('cross-owner write rejected', false);
    exception when raise_exception then
      insert into vr_results values ('cross-owner write rejected',
        sqlerrm = 'VALUE_RECEIPT_OWNER_MISMATCH');
    end;

    -- legacy V1 row preserved + classified UNASSESSED (mirrors the trigger payload)
    v_row := public.nayanet_record_ledger_event(
      v_owner, 'SMART_NOTE_CREATED', 'smart_note_events', 'note-legacy-1', now(),
      v_owner, 'PRIVATE', 'RECORDED',
      '[]'::jsonb, '{}'::jsonb,
      '{"assessed":false,"base_points":5,"value_engine":"NayaNET_V1_STARTING_MODEL"}',
      '{}'::jsonb, '[]'::jsonb, '{}'::jsonb);
    v_legacy_id := v_row.ledger_event_id;
    select a.value_assessment, a.value_provenance into v_assessment, v_provenance
      from public.nayanet_ledger_value_assessment a
     where a.ledger_event_id = v_legacy_id;
    insert into vr_results values ('legacy V1 row classifies UNASSESSED/LEGACY_STARTING_MODEL',
      v_assessment = 'UNASSESSED' and v_provenance = 'LEGACY_STARTING_MODEL');
    insert into vr_results values ('legacy V1 payload preserved byte-identical',
      (select l.value from public.nayanet_smart_ledger l
        where l.ledger_event_id = v_legacy_id)
      = '{"assessed":false,"base_points":5,"value_engine":"NayaNET_V1_STARTING_MODEL"}'::jsonb);

    -- typed row classifies VERIFIED_VALUE / V2.1_TYPED_RECEIPT
    select a.value_assessment, a.value_provenance into v_assessment, v_provenance
      from public.nayanet_ledger_value_assessment a
     where a.source_table = 'smart_note_events' and a.source_id = 'note-test-1'
       and a.owner_id = v_owner;
    insert into vr_results values ('typed receipt classifies VERIFIED_VALUE/V2.1_TYPED_RECEIPT',
      v_assessment = 'VERIFIED_VALUE' and v_provenance = 'V2.1_TYPED_RECEIPT');

    -- qualified_by linkage: an assessment receipt qualifies the original event
    v_bad := jsonb_set(v_receipt, '{provenance,source_id}', '"note-legacy-1-assessed"');
    v_row2 := public.nayanet_record_value_receipt(
      v_owner, v_bad, now(), v_owner, 'PRIVATE', v_legacy_id);
    insert into vr_results values ('qualified_by links assessment to the original event',
      v_row2.qualified_by_ledger_event_id = v_legacy_id);
  end if;
end $$;

-- Report; fail the script if anything failed.
do $$
declare
  v_pass int;
  v_fail int;
  r record;
begin
  select count(*) filter (where passed), count(*) filter (where not passed)
    into v_pass, v_fail from vr_results;
  for r in select name from vr_results where not passed loop
    raise notice 'FAIL %', r.name;
  end loop;
  raise notice 'VALUE RECEIPT RUNTIME TESTS: % passed, % failed', v_pass, v_fail;
  if v_fail > 0 then
    raise exception 'VALUE_RECEIPT_TESTS_FAILED: % failures', v_fail;
  end if;
end $$;

rollback;
