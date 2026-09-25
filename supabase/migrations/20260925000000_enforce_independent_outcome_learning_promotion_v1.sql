create or replace function public.nayanet_require_independent_outcome_for_learning_promotion()
returns trigger
language plpgsql
security definer
set search_path=''
as $$
declare
  v_observed jsonb := coalesce(new.observed_value, '{}'::jsonb);
  v_outcome_text text;
  v_outcome_id uuid;
  v_receipt_text text;
  v_outcome public.nayanet_execution_outcomes;
begin
  if new.status is distinct from 'ACTIVE' then
    return new;
  end if;

  v_outcome_text := nullif(trim(coalesce(v_observed->>'outcome_id', v_observed->>'baseline_outcome_id', '')), '');
  if v_outcome_text is null then
    raise exception 'INDEPENDENT_OUTCOME_REQUIRED_FOR_ACTIVE_LEARNING';
  end if;
  begin
    v_outcome_id := v_outcome_text::uuid;
  exception when invalid_text_representation then
    raise exception 'INDEPENDENT_OUTCOME_ID_INVALID';
  end;

  select * into v_outcome
  from public.nayanet_execution_outcomes
  where outcome_id = v_outcome_id
    and user_id = new.member_id
    and project_id = 'NayaNET'
    and verified is true;

  if v_outcome.outcome_id is null then
    raise exception 'INDEPENDENT_OUTCOME_NOT_FOUND_OR_UNVERIFIED';
  end if;
  if v_outcome.verifier_id = new.member_id then
    raise exception 'OUTCOME_VERIFIER_MUST_BE_INDEPENDENT';
  end if;
  if v_outcome.evidence is null or jsonb_typeof(v_outcome.evidence) <> 'object' or v_outcome.evidence = '{}'::jsonb then
    raise exception 'INDEPENDENT_OUTCOME_EVIDENCE_REQUIRED';
  end if;

  v_receipt_text := nullif(trim(coalesce(v_observed->>'receipt_id', v_observed->>'baseline_receipt_id', '')), '');
  if v_receipt_text is null then
    raise exception 'INDEPENDENT_OUTCOME_RECEIPT_REQUIRED';
  end if;
  if v_receipt_text <> v_outcome.receipt_id::text then
    raise exception 'INDEPENDENT_OUTCOME_RECEIPT_MISMATCH';
  end if;

  new.observed_value := v_observed || jsonb_build_object(
    'outcome_id', v_outcome.outcome_id,
    'receipt_id', v_outcome.receipt_id,
    'source_event_id', new.source_event_id,
    'verified', true,
    'verified_value', v_outcome.verified_value,
    'outcome_verification_method', v_outcome.verification_method,
    'independent_outcome', true
  );
  new.verification_method := v_outcome.verification_method;
  return new;
end;
$$;

drop trigger if exists nayanet_independent_outcome_learning_promotion on public.learning_evidence;
create trigger nayanet_independent_outcome_learning_promotion
before insert or update on public.learning_evidence
for each row execute function public.nayanet_require_independent_outcome_for_learning_promotion();
