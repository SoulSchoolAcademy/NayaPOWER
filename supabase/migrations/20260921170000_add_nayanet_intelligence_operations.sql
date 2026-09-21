create table if not exists public.nayanet_intelligence_operations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null default 'NayaNET',
  operation text not null,
  status text not null,
  input jsonb not null default '{}'::jsonb,
  output jsonb not null default '{}'::jsonb,
  source_event_ids text[] not null default '{}'::text[],
  source_ref text,
  created_at timestamptz not null default now()
);
create index if not exists nayanet_intelligence_operations_user_project_created
  on public.nayanet_intelligence_operations(user_id, project_id, created_at desc);
alter table public.nayanet_intelligence_operations enable row level security;
drop policy if exists "nayanet intelligence operations owner read" on public.nayanet_intelligence_operations;
create policy "nayanet intelligence operations owner read"
  on public.nayanet_intelligence_operations for select
  using (auth.uid() = user_id);
drop policy if exists "nayanet intelligence operations owner insert" on public.nayanet_intelligence_operations;
create policy "nayanet intelligence operations owner insert"
  on public.nayanet_intelligence_operations for insert
  with check (auth.uid() = user_id);
