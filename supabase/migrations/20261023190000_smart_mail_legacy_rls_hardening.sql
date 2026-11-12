-- Smart Mail legacy-table RLS hardening.
-- Scope: remove anonymous access to message/thread contents and permit authenticated
-- participants to read messages. The canonical nayanet-smart-mail Edge Function
-- uses the v7_mail_* transaction path; this migration does not alter that path.
-- No data is deleted. Review app callers before applying to production.

begin;

-- Anonymous access to conversation content is not acceptable.
drop policy if exists pass2_anon_insert_smart_mail_messages on public.smart_mail_messages;
drop policy if exists pass2_anon_select_smart_mail_messages on public.smart_mail_messages;
drop policy if exists pass2_anon_update_smart_mail_messages on public.smart_mail_messages;
drop policy if exists pass2_anon_insert_smart_mail_threads on public.smart_mail_threads;
drop policy if exists pass2_anon_select_smart_mail_threads on public.smart_mail_threads;
drop policy if exists pass2_anon_update_smart_mail_threads on public.smart_mail_threads;

-- Ensure row-level security is active on these legacy projection tables.
alter table public.smart_mail_messages enable row level security;
alter table public.smart_mail_threads enable row level security;

-- Authenticated users may read a message only when their signed JWT alias is
-- the sender or the recipient on its parent thread. Alias is a display/route
-- label, not a substitute for authentication; the alias must be in the JWT.
drop policy if exists smart_mail_messages_owner_select on public.smart_mail_messages;
create policy smart_mail_messages_participant_select
on public.smart_mail_messages
for select
to authenticated
using (
  from_alias = coalesce(
    (auth.jwt() -> 'app_metadata' ->> 'smart_alias'),
    (auth.jwt() -> 'user_metadata' ->> 'smart_alias')
  )
  or exists (
    select 1
    from public.smart_mail_threads t
    where t.id = smart_mail_messages.thread_id
      and t.to_alias = coalesce(
        (auth.jwt() -> 'app_metadata' ->> 'smart_alias'),
        (auth.jwt() -> 'user_metadata' ->> 'smart_alias')
      )
  )
);

commit;
