-- P0 bind policy comparison to independent verified outcomes
create or replace function public.nayanet_compare_verified_policy_outcomes(
  p_baseline_policy_id uuid,
  p_candidate_policy_id uuid,
  p_baseline_receipt_id uuid,
  p_candidate_receipt_id uuid
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  bp public.nayanet_policy_versions;
  cp public.nayanet_policy_versions;
  br public.nayanet_execution_receipts;
  cr public.nayanet_execution_receipts;
  bo public.nayanet_execution_outcomes;
  co public.nayanet_execution_outcomes;
  bv numeric;
  cv numeric;
  result text;
  improvement boolean;
begin
  select * into bp from public.nayanet_policy_versions where id=p_baseline_policy_id;
  select * into cp from public.nayanet_policy_versions where id=p_candidate_policy_id;
  select * into br from public.nayanet_execution_receipts where id=p_baseline_receipt_id;
  select * into cr from public.nayanet_execution_receipts where id=p_candidate_receipt_id;
  if bp.id is null or cp.id is null then raise exception 'POLICY_NOT_FOUND'; end if;
  if br.id is null or cr.id is null then raise exception 'RECEIPT_NOT_FOUND'; end if;
  if (select auth.uid()) is null then raise exception 'AUTH_REQUIRED'; end if;
  if (select auth.uid()) <> bp.user_id then raise exception 'CALLER_NOT_POLICY_OWNER'; end if;
  if bp.user_id <> cp.user_id or bp.user_id <> br.user_id or bp.user_id <> cr.user_id then raise exception 'OWNER_LINEAGE_MISMATCH'; end if;
  if bp.project_id <> cp.project_id or bp.project_id <> br.project_id or bp.project_id <> cr.project_id then raise exception 'PROJECT_LINEAGE_MISMATCH'; end if;
  if br.policy_id is null or cr.policy_id is null then raise exception 'POLICY_RECEIPT_LINEAGE_MISSING'; end if;
  if br.policy_id <> bp.id or cr.policy_id <> cp.id then raise exception 'POLICY_RECEIPT_LINEAGE_MISMATCH'; end if;
  if br.policy_version <> bp.version or cr.policy_version <> cp.version then raise exception 'POLICY_VERSION_LINEAGE_MISMATCH'; end if;
  if br.policy_key <> bp.policy_key or cr.policy_key <> cp.policy_key then raise exception 'POLICY_KEY_LINEAGE_MISMATCH'; end if;
  if br.experiment_case_id is null or cr.experiment_case_id is null then raise exception 'EXPERIMENT_CASE_LINEAGE_MISSING'; end if;
  if br.experiment_case_id <> cr.experiment_case_id then raise exception 'EXPERIMENT_CASE_MISMATCH'; end if;
  if br.policy_input_hash is null or cr.policy_input_hash is null then raise exception 'POLICY_INPUT_HASH_MISSING'; end if;
  if br.policy_decision_hash is null or cr.policy_decision_hash is null then raise exception 'POLICY_DECISION_HASH_MISSING'; end if;
  if br.status <> 'SUCCESS' or cr.status <> 'SUCCESS' then raise exception 'OUTCOME_NOT_SUCCESS'; end if;
  select * into bo from public.nayanet_execution_outcomes where receipt_id=br.id;
  select * into co from public.nayanet_execution_outcomes where receipt_id=cr.id;
  if bo.outcome_id is null or co.outcome_id is null then raise exception 'INDEPENDENT_OUTCOME_MISSING'; end if;
  if bo.verified is not true or co.verified is not true then raise exception 'OUTCOME_NOT_VERIFIED'; end if;
  if bo.experiment_case_id <> co.experiment_case_id then raise exception 'OUTCOME_CASE_MISMATCH'; end if;
  if br.action <> cr.action or br.action <> 'smart_mail_send' then raise exception 'ACTION_MISMATCH'; end if;
  bv := bo.verified_value;
  cv := co.verified_value;
  improvement := cv > bv;
  result := case when improvement then 'POLICY_IMPROVEMENT_PROVEN' else 'POLICY_IMPROVEMENT_NOT_PROVEN' end;
  return jsonb_build_object(
    'result',result,'improvement',improvement,
    'baseline',jsonb_build_object('policy_id',bp.id,'version',bp.version,'receipt_id',br.id,'outcome_id',bo.outcome_id,'verified_value',bv,'experiment_case_id',br.experiment_case_id,'policy_input_hash',br.policy_input_hash,'policy_decision_hash',br.policy_decision_hash),
    'candidate',jsonb_build_object('policy_id',cp.id,'version',cp.version,'receipt_id',cr.id,'outcome_id',co.outcome_id,'verified_value',cv,'experiment_case_id',cr.experiment_case_id,'policy_input_hash',cr.policy_input_hash,'policy_decision_hash',cr.policy_decision_hash),
    'formula','benefit - harm - cost - risk_adjusted_loss',
    'real_observed_outcomes',true,'independent_outcome_contract',true,'verified_comparison',true,
    'policy_improvement_proven',improvement
  );
end;
$$;

revoke execute on function public.nayanet_compare_verified_policy_outcomes(uuid,uuid,uuid,uuid) from public,anon;
grant execute on function public.nayanet_compare_verified_policy_outcomes(uuid,uuid,uuid,uuid) to authenticated,service_role;
