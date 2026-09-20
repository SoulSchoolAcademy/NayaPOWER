-- Canonical Naya Dream / Replay P0 persistence.
create table if not exists public.nayanet_dream_replays (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null,
  source_event_id text not null,
  source_receipt_id uuid,
  policy_version text not null,
  world_snapshot jsonb not null,
  replay_input jsonb not null,
  replay_output jsonb not null,
  status text not null,
  verification jsonb not null,
  idempotency_key text not null,
  created_at timestamptz not null default now()
);
create unique index if not exists nayanet_dream_replays_user_id_idempotency_key_key on public.nayanet_dream_replays (user_id,idempotency_key);
create index if not exists nayanet_dream_replays_source_idx on public.nayanet_dream_replays (user_id,project_id,created_at desc);
alter table public.nayanet_dream_replays enable row level security;
drop policy if exists dream_replays_insert_own on public.nayanet_dream_replays;
create policy dream_replays_insert_own on public.nayanet_dream_replays for insert to authenticated with check (auth.uid()=user_id);
drop policy if exists dream_replays_select_own on public.nayanet_dream_replays;
create policy dream_replays_select_own on public.nayanet_dream_replays for select to authenticated using (auth.uid()=user_id);