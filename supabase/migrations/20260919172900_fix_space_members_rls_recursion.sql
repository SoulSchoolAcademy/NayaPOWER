-- Fix recursive SELECT policy on nayanet_space_members.
-- Use a SECURITY DEFINER membership predicate so shared-space reads do not
-- recurse through the same table's RLS policy.
create or replace function public.nayanet_is_space_member(
  p_space_id uuid,
  p_member_id uuid
) returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.nayanet_space_members m
    where m.space_id = p_space_id
      and m.member_id = p_member_id
      and m.status = 'active'
  );
$$;

revoke all on function public.nayanet_is_space_member(uuid, uuid) from public;
grant execute on function public.nayanet_is_space_member(uuid, uuid) to authenticated;

drop policy if exists nayanet_space_members_shared_read
  on public.nayanet_space_members;

create policy nayanet_space_members_shared_read
  on public.nayanet_space_members
  for select
  to authenticated
  using (
    status = 'active'
    and exists (
      select 1
      from public.nayanet_spaces s
      where s.id = nayanet_space_members.space_id
        and s.visibility = 'shared'
        and public.nayanet_is_space_member(s.id, auth.uid())
    )
  );
