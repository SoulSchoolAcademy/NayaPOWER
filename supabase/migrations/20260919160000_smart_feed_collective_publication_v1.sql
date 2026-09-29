create table if not exists public.nayanet_intelligence_publications (
  id uuid primary key default gen_random_uuid(),
  intelligence_event_id uuid not null references public.nayanet_cognition_events(id) on delete cascade,
  owner_id uuid not null references public.members(id) on delete cascade,
  published_at timestamptz not null default now(),
  status text not null default 'published' check (status in ('published','revoked')),
  consent_state text not null default 'explicit' check (consent_state = 'explicit'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (intelligence_event_id)
);
create index if not exists nayanet_intelligence_publications_owner_idx on public.nayanet_intelligence_publications(owner_id,created_at desc);
create index if not exists nayanet_intelligence_publications_event_idx on public.nayanet_intelligence_publications(intelligence_event_id);
alter table public.nayanet_intelligence_publications enable row level security;
revoke all on table public.nayanet_intelligence_publications from anon, authenticated;
grant select on table public.nayanet_intelligence_publications to anon, authenticated;
grant insert,update,delete on table public.nayanet_intelligence_publications to authenticated;
drop policy if exists "collective_publication_read" on public.nayanet_intelligence_publications;
create policy "collective_publication_read" on public.nayanet_intelligence_publications for select to anon, authenticated using (status='published' and consent_state='explicit');
drop policy if exists "collective_publication_owner_insert" on public.nayanet_intelligence_publications;
create policy "collective_publication_owner_insert" on public.nayanet_intelligence_publications for insert to authenticated with check (owner_id=(select auth.uid()) and consent_state='explicit' and status='published' and exists (select 1 from public.nayanet_cognition_events e where e.id=intelligence_event_id and e.user_id=(select auth.uid())));
drop policy if exists "collective_publication_owner_update" on public.nayanet_intelligence_publications;
create policy "collective_publication_owner_update" on public.nayanet_intelligence_publications for update to authenticated using (owner_id=(select auth.uid())) with check (owner_id=(select auth.uid()));
drop policy if exists "collective_publication_owner_delete" on public.nayanet_intelligence_publications;
create policy "collective_publication_owner_delete" on public.nayanet_intelligence_publications for delete to authenticated using (owner_id=(select auth.uid()));