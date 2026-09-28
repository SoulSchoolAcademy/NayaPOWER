create or replace function public.nayanet_compare_verified_policy_outcomes(p_baseline_policy_id uuid,p_candidate_policy_id uuid,p_baseline_receipt_id uuid,p_candidate_receipt_id uuid)
returns jsonb language plpgsql security definer set search_path=''
as $$
declare bp public.nayanet_policy_versions; cp public.nayanet_policy_versions; br public.nayanet_execution_receipts; cr public.nayanet_execution_receipts; bv numeric; cv numeric; result text; improvement boolean;
begin
 select * into bp from public.nayanet_policy_versions where id=p_baseline_policy_id;
 select * into cp from public.nayanet_policy_versions where id=p_candidate_policy_id;
 select * into br from public.nayanet_execution_receipts where id=p_baseline_receipt_id;
 select * into cr from public.nayanet_execution_receipts where id=p_candidate_receipt_id;
 if bp.id is null or cp.id is null then raise exception 'POLICY_NOT_FOUND'; end if;
 if br.id is null or cr.id is null then raise exception 'RECEIPT_NOT_FOUND'; end if;
 if bp.user_id <> cp.user_id or bp.user_id <> br.user_id or bp.user_id <> cr.user_id then raise exception 'OWNER_LINEAGE_MISMATCH'; end if;
 if bp.project_id <> cp.project_id or bp.project_id <> br.project_id or bp.project_id <> cr.project_id then raise exception 'PROJECT_LINEAGE_MISMATCH'; end if;
 if br.status <> 'SUCCESS' or cr.status <> 'SUCCESS' then raise exception 'OUTCOME_NOT_SUCCESS'; end if;
 if coalesce((br.value->>'verified')::boolean,false) is not true or coalesce((cr.value->>'verified')::boolean,false) is not true then raise exception 'OUTCOME_NOT_VERIFIED'; end if;
 if br.action <> cr.action then raise exception 'ACTION_MISMATCH'; end if;
 if br.action <> 'smart_mail_send' then raise exception 'UNSUPPORTED_ACTION'; end if;
 bv := coalesce((br.value->>'verified_value')::numeric,(br.value->>'benefit')::numeric,0)-coalesce((br.value->>'harm')::numeric,0)-coalesce((br.value->>'cost')::numeric,0)-coalesce((br.value->>'risk_adjusted_loss')::numeric,0);
 cv := coalesce((cr.value->>'verified_value')::numeric,(cr.value->>'benefit')::numeric,0)-coalesce((cr.value->>'harm')::numeric,0)-coalesce((cr.value->>'cost')::numeric,0)-coalesce((cr.value->>'risk_adjusted_loss')::numeric,0);
 improvement := cv > bv;
 result := case when improvement then 'PASS' else 'NOT_PROVEN' end;
 return jsonb_build_object('result',result,'improvement',improvement,'baseline',jsonb_build_object('policy_id',bp.id,'version',bp.version,'receipt_id',br.id,'verified_value',bv),'candidate',jsonb_build_object('policy_id',cp.id,'version',cp.version,'receipt_id',cr.id,'verified_value',cv),'formula','benefit - harm - cost - risk_adjusted_loss','real_observed_outcomes',true,'verified_comparison',true,'policy_improvement_proven',improvement);
end; $$;
revoke execute on function public.nayanet_compare_verified_policy_outcomes(uuid,uuid,uuid,uuid) from public,anon,authenticated;
grant execute on function public.nayanet_compare_verified_policy_outcomes(uuid,uuid,uuid,uuid) to authenticated,service_role;
