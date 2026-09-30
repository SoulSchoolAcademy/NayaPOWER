-- SECURITY HARDENING: immutable checkpoint evidence must not be broadly writable/readable.
-- Existing UPDATE/DELETE immutability trigger remains in force.
-- Service-role and postgres maintenance paths remain available through their privileged roles.

alter table public.nayanet_checkpoint_receipts enable row level security;

revoke all privileges on table public.nayanet_checkpoint_receipts from anon;
revoke all privileges on table public.nayanet_checkpoint_receipts from authenticated;

grant select on table public.nayanet_checkpoint_receipts to authenticated;

drop policy if exists nayanet_checkpoint_receipts_owner_read on public.nayanet_checkpoint_receipts;
create policy nayanet_checkpoint_receipts_owner_read
on public.nayanet_checkpoint_receipts
for select
to authenticated
using (user_id = auth.uid());

comment on table public.nayanet_checkpoint_receipts is
  'Immutable checkpoint evidence ledger. RLS owner-read for authenticated users; mutation is reserved to governed privileged runtime/migration paths.';
