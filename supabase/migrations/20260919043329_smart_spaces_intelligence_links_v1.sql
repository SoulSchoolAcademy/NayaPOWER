create table if not exists public.nayanet_space_intelligence (
  id uuid primary key default gen_random_uuid(),
  space_id uuid not null references public.nayanet_spaces(id) on delete cascade,
  intelligence_event_id uuid not null references public.nayanet_cognition_events(id) on delete cascade,
  owner_member_id uuid not null references public.members(id) on delete cascade,
  created_at timestamptz not null default now(),
  unique(space_id, intelligence_event_id)
);

create index if not exists nayanet_space_intelligence_space_idx
  on public.nayanet_space_intelligence(space_id, created_at desc);

create index if not exists nayanet_space_intelligence_owner_idx
  on public.nayanet_space_intelligence(owner_member_id, created_at desc);

alter table public.nayanet_space_intelligence enable row level security;

drop policy if exists nayanet_space_intelligence_owner on public.nayanet_space_intelligence;
create policy nayanet_space_intelligence_owner
on public.nayanet_space_intelligence
for all
using (owner_member_id = auth.uid())
with check (
  owner_member_id = auth.uid()
  and exists (
    select 1 from public.nayanet_spaces s
    where s.id = space_id and s.owner_member_id = auth.uid()
  )
  and exists (
    select 1 from public.nayanet_cognition_events e
    where e.id = intelligence_event_id and e.user_id = auth.uid()
  )
);
