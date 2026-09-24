revoke execute on function public.nayanet_smart_connect(text) from anon;
revoke execute on function public.nayanet_smart_disconnect(text) from anon;
revoke execute on function public.nayanet_collective_wisdom_for_event(uuid,uuid,text,text,jsonb) from anon, authenticated;
grant execute on function public.nayanet_smart_connect(text) to authenticated;
grant execute on function public.nayanet_smart_disconnect(text) to authenticated;
grant execute on function public.nayanet_collective_wisdom_for_event(uuid,uuid,text,text,jsonb) to service_role;