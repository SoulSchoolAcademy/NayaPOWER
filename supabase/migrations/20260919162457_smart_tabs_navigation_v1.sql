-- Canonical Smart Tabs source reconciliation.
-- This migration is already present in production under version 20260919162457.
-- It is committed here so repository source can reconstruct the deployed primitive.

create table if not exists public.nayanet_smart_tabs (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.members(id) on delete cascade,
  label text not null check (char_length(trim(label)) between 1 and 120),
  target_type text not null check (target_type in ('route','url','query','topic','category')),
  target text not null check (char_length(trim(target)) between 1 and 2000),
  scope text not null default 'private' check (scope = 'private'),
  favorite boolean not null default false,
  priority integer not null default 0,
  position integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.nayanet_smart_tabs enable row level security;

drop policy if exists "smart_tabs_owner_select" on public.nayanet_smart_tabs;
create policy "smart_tabs_owner_select" on public.nayanet_smart_tabs
  for select to authenticated using (owner_id = auth.uid());

drop policy if exists "smart_tabs_owner_insert" on public.nayanet_smart_tabs;
create policy "smart_tabs_owner_insert" on public.nayanet_smart_tabs
  for insert to authenticated with check (owner_id = auth.uid() and scope = 'private');

drop policy if exists "smart_tabs_owner_update" on public.nayanet_smart_tabs;
create policy "smart_tabs_owner_update" on public.nayanet_smart_tabs
  for update to authenticated using (owner_id = auth.uid()) with check (owner_id = auth.uid() and scope = 'private');

drop policy if exists "smart_tabs_owner_delete" on public.nayanet_smart_tabs;
create policy "smart_tabs_owner_delete" on public.nayanet_smart_tabs
  for delete to authenticated using (owner_id = auth.uid());

create index if not exists nayanet_smart_tabs_owner_position_idx
  on public.nayanet_smart_tabs(owner_id, position, created_at);
