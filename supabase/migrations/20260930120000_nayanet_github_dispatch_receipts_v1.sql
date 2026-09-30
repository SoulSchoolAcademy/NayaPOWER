-- nayanet-github-dispatch receipts: one row per projection idempotency key.
-- Source-present only: a human applies this migration to production. The
-- dispatch function claims a row ("processing") before touching GitHub, so a
-- concurrent duplicate either replays the completed receipt or takes over a
-- non-completed claim instead of committing twice.

create table if not exists public.nayanet_github_dispatch_receipts (
  id uuid primary key default gen_random_uuid(),
  idempotency_key text not null unique,
  transaction_id text not null,
  user_id uuid null references auth.users(id) on delete set null,
  authority_grant_id uuid null,
  intelligent_block_id text null,
  repo_path text null,
  smart_link text null,
  commit_sha text null,
  status text not null default 'processing'
    check (status in ('processing','completed','failed','blocked')),
  failure text null,
  completed_at timestamptz null,
  created_at timestamptz not null default now()
);

create index if not exists nayanet_github_dispatch_receipts_tx_idx
  on public.nayanet_github_dispatch_receipts(transaction_id);
create index if not exists nayanet_github_dispatch_receipts_user_idx
  on public.nayanet_github_dispatch_receipts(user_id, created_at desc);

alter table public.nayanet_github_dispatch_receipts enable row level security;

-- Owners can read their own dispatch receipts. Writes go through the
-- service-role client inside nayanet-github-dispatch (no insert/update
-- policy for authenticated roles).
drop policy if exists github_dispatch_receipts_select_own
  on public.nayanet_github_dispatch_receipts;
create policy github_dispatch_receipts_select_own
  on public.nayanet_github_dispatch_receipts
  for select to authenticated
  using (user_id = auth.uid());
