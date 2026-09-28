-- P0 Smart Mail vertical: preserve the existing mail tables while adding
-- provenance/idempotency metadata and correcting member-scoped RLS.
alter table public.v7_mail_messages
  add column if not exists metadata jsonb not null default '{}'::jsonb;

create unique index if not exists v7_mail_messages_sender_idempotency_uq
  on public.v7_mail_messages (sender_id, ((metadata->>'idempotency_key')))
  where metadata ? 'idempotency_key';

drop policy if exists v7_msg_member_read on public.v7_mail_messages;
create policy v7_msg_member_read on public.v7_mail_messages
for select to authenticated
using (
  exists (
    select 1 from public.v7_mail_members m
    where m.thread_id = v7_mail_messages.thread_id
      and m.user_id = auth.uid()
  )
);

drop policy if exists v7_msg_member_send on public.v7_mail_messages;
create policy v7_msg_member_send on public.v7_mail_messages
for insert to authenticated
with check (
  sender_id = auth.uid()
  and exists (
    select 1 from public.v7_mail_members m
    where m.thread_id = v7_mail_messages.thread_id
      and m.user_id = auth.uid()
  )
);

drop policy if exists v7_thread_member_read on public.v7_mail_threads;
create policy v7_thread_member_read on public.v7_mail_threads
for select to authenticated
using (
  exists (
    select 1 from public.v7_mail_members m
    where m.thread_id = v7_mail_threads.id
      and m.user_id = auth.uid()
  )
);

-- Receiver membership is created only by the governed mail function using service role.
-- Direct clients can add only themselves.
