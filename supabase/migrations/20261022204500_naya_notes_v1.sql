-- 20261022204500_naya_notes_v1.sql
-- Best-of-Best Phase 0, step 3: the Naya Notes store (map element #15).
--
-- THE SEPARATION IS ABSOLUTE (element #15 spec ruling):
--   naya_notes      = THIS table. A person's own quick captures — private,
--                     never fed to the brain, never posted to any wall.
--   smart_notes     = the flagship wall/intelligence table. Different
--                     object, different life.
--   hub_smart_notes = the brain's note store. Different object.
--   nayanet_notes   = the intelligence-estate table. Different object.
-- Nothing in this migration reads, writes, copies, or syncs any of those.
--
-- Shape follows the spec's note object: owner, text, category, list,
-- created_at. The list column is named list_name (a bare "list" invites
-- breakage in query builders); the app layer presents it as "List".
--
-- RLS mirrors the flagship messaging pattern: the owner, as an
-- authenticated user, scoped by owner_id = auth.uid(). There are NO anon
-- policies — a personal capture store is never publicly readable.
-- Registered PENDING_REVIEW_NOT_PRODUCTION_APPLIED; applies at the human
-- gate only.

create table if not exists public.naya_notes (
  id uuid primary key default gen_random_uuid(),
  owner_alias text not null,
  owner_id uuid,
  text text not null,
  category text not null default 'General',
  list_name text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint naya_notes_text_nonempty check (char_length(btrim(text)) > 0),
  constraint naya_notes_text_bounded check (char_length(text) <= 4000)
);

create index if not exists naya_notes_owner_time_idx
  on public.naya_notes (owner_alias, created_at desc);
create index if not exists naya_notes_owner_category_idx
  on public.naya_notes (owner_alias, category);

alter table public.naya_notes enable row level security;

drop policy if exists naya_notes_owner_select on public.naya_notes;
create policy naya_notes_owner_select on public.naya_notes
  for select to authenticated
  using (owner_id = (select auth.uid()));

drop policy if exists naya_notes_owner_insert on public.naya_notes;
create policy naya_notes_owner_insert on public.naya_notes
  for insert to authenticated
  with check (owner_id = (select auth.uid()));

drop policy if exists naya_notes_owner_update on public.naya_notes;
create policy naya_notes_owner_update on public.naya_notes
  for update to authenticated
  using (owner_id = (select auth.uid()))
  with check (owner_id = (select auth.uid()));

drop policy if exists naya_notes_owner_delete on public.naya_notes;
create policy naya_notes_owner_delete on public.naya_notes
  for delete to authenticated
  using (owner_id = (select auth.uid()));
