create table if not exists public.nayanet_dream_replays (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id),
  project_id text not null,
  source_event_id text not null,
  source_receipt_id uuid,
  policy_version text not null default 'DREAM-P0-V1',
  world_snapshot jsonb not null default '{}'::jsonb,
  replay_input jsonb not null default '{}'::jsonb,
  replay_output jsonb not null default '{}'::jsonb,
  status text not null default 'SIMULATED' check (status in ('SIMULATED','VERIFIED','BLOCKED','FAILED')),
  verification jsonb not null default '{}'::jsonb,
  idempotency_key text not null,
  created_at timestamptz not null default now(),
  unique(user_id, idempotency_key)
);

alter table public.nayanet_dream_replays enable row level security;

drop policy if exists "dream_replays_select_own" on public.nayanet_dream_replays;
create policy "dream_replays_select_own" on public.nayanet_dream_replays for select to authenticated using (auth.uid() = user_id);

drop policy if exists "dream_replays_insert_own" on public.nayanet_dream_replays;
create policy "dream_replays_insert_own" on public.nayanet_dream_replays for insert to authenticated with check (auth.uid() = user_id);

create index if not exists nayanet_dream_replays_source_idx on public.nayanet_dream_replays(user_id, project_id, created_at desc);

comment on table public.nayanet_dream_replays is 'P0 Dream-RSI replay ledger. Read-only against cognition/execution history; replay rows are simulations and never grant authority or mutate source history.';
