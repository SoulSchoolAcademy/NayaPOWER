-- 20261022223000_smart_lists_v1.sql
-- Best-of-Best Wave 1: the Smart Lists server store (map element #16,
-- build-order step 15; categories ride element #19).
--
-- WHAT THIS REPLACES: two device-local list worlds that could never agree —
--   flagship: localStorage `os.lists.<alias>` (plain-text items, one device)
--   Hub:      localStorage `naya.smartlist` ({saved:[{id,kind,title,savedAt}]})
-- This store is the ONE store both surfaces read. The flagship template
-- sources are under another lane's freeze, so the flagship keeps its local
-- lists until its step wires this store; the Hub surface ships in this PR.
--
-- SHAPE:
--   smart_lists       one row per list: owner, title, category, position.
--                     Categories are plain owner-named strings (element #19:
--                     "a handful of owner-named facts, not a field editor") —
--                     there is deliberately no category table.
--   smart_list_items  one row per membership. An item is a TYPED reference:
--                     (item_kind, item_ref) — a plain object reference, per
--                     the Wave-1 scope. Items carry NO foreign key to any
--                     object table: removing an item deletes only the
--                     membership row and can never delete the underlying
--                     Smart Note, Naya Note, person, thread, or link.
--                     The sibling link-model build (step 14) owns stored
--                     object links; this store consumes references only.
--   Naya Notes (element #15, migration 20261022204500) are first-class
--   items from day one: item_kind 'naya_note', item_ref = the note's id.
--
-- RLS mirrors the flagship messaging pattern (Phase 0): the owner, as an
-- authenticated user, scoped by owner_id = auth.uid(). NO anon policies —
-- a person's lists are never publicly readable. Item writes additionally
-- require the parent list to be the writer's own, so a caller cannot
-- inject an item into another owner's list even by guessing its id.
-- Registered PENDING_REVIEW_NOT_PRODUCTION_APPLIED; applies at the human
-- gate only.

create table if not exists public.smart_lists (
  id uuid primary key default gen_random_uuid(),
  owner_alias text not null,
  owner_id uuid,
  title text not null,
  category text not null default 'General',
  position integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint smart_lists_title_nonempty check (char_length(btrim(title)) > 0),
  constraint smart_lists_title_bounded check (char_length(title) <= 200),
  constraint smart_lists_category_bounded check (char_length(category) <= 80)
);

create index if not exists smart_lists_owner_idx
  on public.smart_lists (owner_alias, position, created_at);
create index if not exists smart_lists_owner_category_idx
  on public.smart_lists (owner_alias, category);

create table if not exists public.smart_list_items (
  id uuid primary key default gen_random_uuid(),
  list_id uuid not null references public.smart_lists(id) on delete cascade,
  owner_alias text not null,
  owner_id uuid,
  item_kind text not null
    constraint smart_list_items_kind
    check (item_kind in ('smart_note', 'naya_note', 'person', 'mail_thread', 'smart_link', 'text')),
  item_ref text,
  label text,
  text text,
  position integer not null default 0,
  created_at timestamptz not null default now(),
  constraint smart_list_items_ref_bounded check (char_length(item_ref) <= 512),
  constraint smart_list_items_label_bounded check (char_length(label) <= 300),
  constraint smart_list_items_text_bounded check (char_length(text) <= 4000),
  constraint smart_list_items_shape check (
    (item_kind = 'text' and char_length(btrim(coalesce(text, ''))) > 0)
    or (item_kind <> 'text' and char_length(btrim(coalesce(item_ref, ''))) > 0)
  )
);

create index if not exists smart_list_items_list_idx
  on public.smart_list_items (list_id, position, created_at);
create index if not exists smart_list_items_owner_idx
  on public.smart_list_items (owner_alias, created_at desc);

alter table public.smart_lists enable row level security;
alter table public.smart_list_items enable row level security;

drop policy if exists smart_lists_owner_select on public.smart_lists;
create policy smart_lists_owner_select on public.smart_lists
  for select to authenticated
  using (owner_id = (select auth.uid()));

drop policy if exists smart_lists_owner_insert on public.smart_lists;
create policy smart_lists_owner_insert on public.smart_lists
  for insert to authenticated
  with check (owner_id = (select auth.uid()));

drop policy if exists smart_lists_owner_update on public.smart_lists;
create policy smart_lists_owner_update on public.smart_lists
  for update to authenticated
  using (owner_id = (select auth.uid()))
  with check (owner_id = (select auth.uid()));

drop policy if exists smart_lists_owner_delete on public.smart_lists;
create policy smart_lists_owner_delete on public.smart_lists
  for delete to authenticated
  using (owner_id = (select auth.uid()));

drop policy if exists smart_list_items_owner_select on public.smart_list_items;
create policy smart_list_items_owner_select on public.smart_list_items
  for select to authenticated
  using (owner_id = (select auth.uid()));

drop policy if exists smart_list_items_owner_insert on public.smart_list_items;
create policy smart_list_items_owner_insert on public.smart_list_items
  for insert to authenticated
  with check (
    owner_id = (select auth.uid())
    and exists (
      select 1 from public.smart_lists parent
      where parent.id = list_id and parent.owner_id = (select auth.uid())
    )
  );

drop policy if exists smart_list_items_owner_update on public.smart_list_items;
create policy smart_list_items_owner_update on public.smart_list_items
  for update to authenticated
  using (owner_id = (select auth.uid()))
  with check (
    owner_id = (select auth.uid())
    and exists (
      select 1 from public.smart_lists parent
      where parent.id = list_id and parent.owner_id = (select auth.uid())
    )
  );

drop policy if exists smart_list_items_owner_delete on public.smart_list_items;
create policy smart_list_items_owner_delete on public.smart_list_items
  for delete to authenticated
  using (owner_id = (select auth.uid()));
