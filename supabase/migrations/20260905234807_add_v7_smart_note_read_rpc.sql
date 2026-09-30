create or replace function public.v7_list_smart_notes()
returns setof public.v7_smart_note_transactions
language sql
security definer
set search_path = public
as $$
  select * from public.v7_smart_note_transactions
  where user_id = auth.uid()
  order by created_at desc;
$$;
revoke execute on function public.v7_list_smart_notes() from anon, public;
grant execute on function public.v7_list_smart_notes() to authenticated;
