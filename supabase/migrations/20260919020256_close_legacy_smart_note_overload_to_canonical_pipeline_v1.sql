create or replace function public.v7_create_smart_note(
 p_idempotency_key text,p_user_id uuid,p_human_note jsonb,p_naya_note jsonb,p_machine_note jsonb,
 p_intelligent_feed jsonb,p_intelligent_block jsonb,p_evidence jsonb,p_hub_state jsonb
) returns public.v7_smart_note_transactions language plpgsql security definer set search_path=public,extensions as $$
declare v public.v7_smart_note_transactions;
begin
 select * into v from public.v7_create_smart_note(p_idempotency_key,p_user_id,p_human_note,p_naya_note,p_machine_note,p_intelligent_feed,p_intelligent_block,p_evidence,p_hub_state,null::text);
 return v;
end; $$;
revoke execute on function public.v7_create_smart_note(text,uuid,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb) from public,anon,authenticated;
