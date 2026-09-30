create or replace function public.v7_create_smart_note(
  p_idempotency_key text,
  p_user_id uuid,
  p_human_note jsonb,
  p_naya_note jsonb,
  p_machine_note jsonb,
  p_intelligent_feed jsonb,
  p_intelligent_block jsonb,
  p_evidence jsonb,
  p_hub_state jsonb
) returns public.v7_smart_note_transactions
language plpgsql
security definer
set search_path = public
as $$
declare
  v_row public.v7_smart_note_transactions;
begin
  if auth.uid() is null or p_user_id is distinct from auth.uid() then
    raise exception 'SMART_NOTE_USER_MISMATCH';
  end if;
  if coalesce(trim(p_idempotency_key), '') = '' then
    raise exception 'SMART_NOTE_IDEMPOTENCY_KEY_REQUIRED';
  end if;
  if p_human_note is null or p_naya_note is null or p_machine_note is null
     or p_intelligent_feed is null or p_intelligent_block is null
     or p_evidence is null or p_hub_state is null then
    raise exception 'SMART_NOTE_PIPELINE_PAYLOAD_INCOMPLETE';
  end if;

  select * into v_row
  from public.v7_smart_note_transactions
  where idempotency_key = p_idempotency_key
    and user_id = auth.uid()
  limit 1;

  if found then return v_row; end if;

  insert into public.v7_smart_note_transactions (
    idempotency_key, user_id, status,
    human_note, naya_note, machine_note,
    intelligent_feed, intelligent_block, evidence, hub_state
  ) values (
    p_idempotency_key, auth.uid(), 'completed',
    p_human_note, p_naya_note, p_machine_note,
    p_intelligent_feed, p_intelligent_block, p_evidence, p_hub_state
  )
  returning * into v_row;

  return v_row;
end;
$$;

revoke all on function public.v7_create_smart_note(text, uuid, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb) from anon, public;
grant execute on function public.v7_create_smart_note(text, uuid, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb) to authenticated;
