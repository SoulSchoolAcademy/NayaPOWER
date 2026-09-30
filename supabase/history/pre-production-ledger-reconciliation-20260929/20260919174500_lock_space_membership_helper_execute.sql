revoke execute on function public.nayanet_is_space_member(uuid, uuid) from anon;
revoke execute on function public.nayanet_is_space_member(uuid, uuid) from public;
grant execute on function public.nayanet_is_space_member(uuid, uuid) to authenticated;
