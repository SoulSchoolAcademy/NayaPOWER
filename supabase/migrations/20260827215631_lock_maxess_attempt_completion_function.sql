revoke execute on function public.complete_assessment_attempt(uuid, uuid) from public;
revoke execute on function public.complete_assessment_attempt(uuid, uuid) from anon;
grant execute on function public.complete_assessment_attempt(uuid, uuid) to authenticated;
