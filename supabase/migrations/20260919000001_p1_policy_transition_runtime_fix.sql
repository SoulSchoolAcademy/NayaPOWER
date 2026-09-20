create or replace function public.nayanet_policy_transition(p_policy_id uuid,p_to_state text,p_evaluation jsonb default '{}')
returns jsonb language plpgsql security definer set search_path=''
as $$
declare p public.nayanet_policy_versions;
begin
 select * into p from public.nayanet_policy_versions where id=p_policy_id for update;
 if p.id is null then raise exception 'POLICY_NOT_FOUND'; end if;
 if p.user_id <> auth.uid() then raise exception 'POLICY_OWNER_REQUIRED'; end if;
 if p_to_state='PROMOTED' then
  if p.state <> 'VERIFIED' then raise exception 'PROMOTION_REQUIRES_VERIFIED'; end if;
  if coalesce((p.holdout->>'result'),'') <> 'PASS' then raise exception 'PROMOTION_REQUIRES_HOLDOUT_PASS'; end if;
  if coalesce((p.adversarial->>'result'),'') <> 'PASS' then raise exception 'PROMOTION_REQUIRES_ADVERSARIAL_PASS'; end if;
  if coalesce((p_evaluation->>'authorized'),'false') <> 'true' then raise exception 'PROMOTION_REQUIRES_AUTHORIZATION'; end if;
 end if;
 if p_to_state='CONTROLLED_TEST' and p.state <> 'AUTHORIZATION_REQUIRED' then raise exception 'CONTROLLED_TEST_REQUIRES_AUTHORIZATION_STATE'; end if;
 if p_to_state='VERIFIED' and p.state <> 'OBSERVED' then raise exception 'VERIFICATION_REQUIRES_OBSERVED'; end if;
 update public.nayanet_policy_versions set state=p_to_state,
  validation=case when p_to_state='VALIDATED' then p_evaluation else validation end,
  adversarial=case when p_to_state='ADVERSARIAL_REVIEW' then p_evaluation else adversarial end,
  holdout=case when p_to_state='HOLDOUT_PASS' then p_evaluation else holdout end,
  promotion=case when p_to_state='PROMOTED' then p_evaluation else promotion end,
  rollback=case when p_to_state='ROLLED_BACK' then p_evaluation else rollback end,
  updated_at=now() where id=p_policy_id;
 return jsonb_build_object('status','TRANSITIONED','policy_id',p_policy_id,'state',p_to_state);
end; $$;
revoke execute on function public.nayanet_policy_transition(uuid,text,jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_policy_transition(uuid,text,jsonb) to authenticated,service_role;
