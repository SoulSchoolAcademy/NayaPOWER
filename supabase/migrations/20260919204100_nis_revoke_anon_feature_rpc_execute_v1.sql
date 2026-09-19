-- NIS: explicit removal of legacy anon EXECUTE grants on user-facing feature RPCs.
revoke all on function public.nayanet_join_space(uuid) from anon;
revoke all on function public.nayanet_leave_space(uuid) from anon;
revoke all on function public.nayanet_save_connection(uuid, uuid) from anon;
revoke all on function public.nayanet_revoke_connection(uuid) from anon;
revoke all on function public.nayanet_create_smart_list(text) from anon;
revoke all on function public.nayanet_add_connection_to_list(uuid, uuid) from anon;
revoke all on function public.nayanet_remove_connection_from_list(uuid, uuid) from anon;
revoke all on function public.nayanet_is_space_member(uuid, uuid) from anon;
revoke all on function public.nayanet_space_owner_membership() from anon;
revoke all on function public.nayanet_send_smart_mail(uuid, uuid, text, text, text, text, text, text, uuid, text, text, text) from anon;
revoke all on function public.nayanet_send_smart_mail_authorized(uuid, uuid, text, text, text, text, text, text, uuid, text, text, text, uuid) from anon;
revoke all on function public.nayanet_send_smart_mail_policy_authorized(uuid, uuid, text, text, text, text, text, text, uuid, text, text, text, uuid) from anon;
