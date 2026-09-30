create or replace function public.nayanet_policy_transition(p_policy_id uuid, p_to_state text, p_evaluation jsonb default '{}'::jsonb)
returns jsonb
language plpgsql
security definer
set search_path to ''
as $function$
declare
  p public.nayanet_policy_versions;
  v_authority jsonb;
  v_grant_id uuid;
begin
  if (select auth.uid()) is null then raise exception 'AUTH_REQUIRED'; end if;

  select * into p from public.nayanet_policy_versions where id=p_policy_id for update;
  if p.id is null then raise exception 'POLICY_NOT_FOUND'; end if;
  if p.user_id <> auth.uid() then raise exception 'POLICY_OWNER_REQUIRED'; end if;

  if p_to_state='PROMOTED' then
    if p.state <> 'VERIFIED' then raise exception 'PROMOTION_REQUIRES_VERIFIED'; end if;
    if coalesce((p.holdout->>'result'),'') <> 'PASS' then raise exception 'PROMOTION_REQUIRES_HOLDOUT_PASS'; end if;
    if coalesce((p.adversarial->>'result'),'') <> 'PASS' then raise exception 'PROMOTION_REQUIRES_ADVERSARIAL_PASS'; end if;
    if coalesce((p_evaluation->>'authorized'),'false') <> 'true' then raise exception 'PROMOTION_REQUIRES_AUTHORIZATION'; end if;
  end if;

  if p_to_state='CONTROLLED_TEST' then
    if p.state <> 'AUTHORIZATION_REQUIRED' then raise exception 'CONTROLLED_TEST_REQUIRES_AUTHORIZATION_STATE'; end if;
    if coalesce((p_evaluation->>'authorized'),'false') <> 'true' then raise exception 'CONTROLLED_TEST_REQUIRES_AUTHORIZATION'; end if;
    v_grant_id := nullif(p_evaluation->>'authority_grant_id','')::uuid;
    if v_grant_id is null then raise exception 'CONTROLLED_TEST_REQUIRES_AUTHORITY_GRANT'; end if;
    v_authority := public.nayanet_validate_authority_grant(v_grant_id,'policy.controlled_test',p_policy_id::text);
    if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
      raise exception 'CONTROLLED_TEST_AUTHORITY_BLOCKED:%', coalesce(v_authority->>'reason','UNKNOWN');
    end if;
    if coalesce(v_authority->>'subject_id','') <> (select auth.uid())::text then
      raise exception 'CONTROLLED_TEST_AUTHORITY_SUBJECT_MISMATCH';
    end if;
  end if;

  if p_to_state='VERIFIED' and p.state <> 'OBSERVED' then raise exception 'VERIFICATION_REQUIRES_OBSERVED'; end if;

  update public.nayanet_policy_versions set state=p_to_state,
    validation=case when p_to_state='VALIDATED' then p_evaluation else validation end,
    adversarial=case when p_to_state='ADVERSARIAL_REVIEW' then p_evaluation else adversarial end,
    holdout=case when p_to_state='HOLDOUT_PASS' then p_evaluation else holdout end,
    promotion=case when p_to_state='PROMOTED' then p_evaluation else promotion end,
    rollback=case when p_to_state='ROLLED_BACK' then p_evaluation else rollback end,
    updated_at=now() where id=p_policy_id;

  return jsonb_build_object('status','TRANSITIONED','policy_id',p_policy_id,'state',p_to_state,
    'authority_grant_id',case when p_to_state='CONTROLLED_TEST' then v_grant_id else null end);
end; $function$;
