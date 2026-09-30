-- Add explicit provenance to current Space membership state.
alter table public.nayanet_space_members
  add column if not exists source_type text not null default 'direct_join',
  add column if not exists source_id uuid null;

create index if not exists nayanet_space_members_source_idx
  on public.nayanet_space_members(source_type, source_id);
