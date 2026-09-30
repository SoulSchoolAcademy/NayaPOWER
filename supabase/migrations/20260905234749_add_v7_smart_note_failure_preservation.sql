create or replace function public.v7_preserve_smart_note_failure(p_idempotency_key text, p_user_id uuid, p_human_note jsonb, p_failure_stage text, p_failure_message text)
returns public.v7_smart_note_transactions
language plpgsql
security definer
set search_path = public
as $$
declare v_row public.v7_smart_note_transactions;
begin
  if auth.uid() is null or auth.uid() <> p_user_id then
    raise exception 'AUTHORIZATION_REQUIRED';
  end if;
  if coalesce(trim(p_idempotency_key), '') = '' then raise exception 'IDEMPOTENCY_KEY_REQUIRED'; end if;
  if p_human_note is null then raise exception 'HUMAN_NOTE_REQUIRED'; end if;
  if coalesce(trim(p_failure_stage), '') = '' then raise exception 'FAILURE_STAGE_REQUIRED'; end if;
  if coalesce(trim(p_failure_message), '') = '' then raise exception 'FAILURE_MESSAGE_REQUIRED'; end if;

  select * into v_row from public.v7_smart_note_transactions
  where idempotency_key = p_idempotency_key and user_id = p_user_id
  limit 1;
  if found then return v_row; end if;

  insert into public.v7_smart_note_transactions(
    idempotency_key,user_id,status,failure_stage,failure_message,human_note
  ) values (
    p_idempotency_key,p_user_id,'failed',p_failure_stage,p_failure_message,p_human_note
  ) returning * into v_row;
  return v_row;
end;
$$;
revoke execute on function public.v7_preserve_smart_note_failure(text,uuid,jsonb,text,text) from anon, public;
grant execute on function public.v7_preserve_smart_note_failure(text,uuid,jsonb,text,text) to authenticated;
