-- 20261022211500_object_links_v1.sql
-- Best-of-Best Wave 1, map step 14: Linked everything, the data model
-- (map elements #14 + #19).
--
-- Until now, linkage in this system was an appearance: Faces derives
-- people by name-matching at read time, lists hold device-local text, and
-- a note could not belong to a person or sit in a list as DATA. This
-- migration makes the link itself a stored row: one object, named once,
-- readable from every home it is filed under — never copied.
--
-- THE MODEL
--   object_links — one row per filing: a subject object (kind + ref)
--     filed under a target (a person, a list, or a mail thread) by its
--     owner. Kinds: smart_note, naya_note, mail_thread, smart_link,
--     person, list. Refs are the stores' own durable keys, as text:
--       naya_note  -> naya_notes.id (uuid)
--       smart_link -> smart_links.id (uuid)
--       person     -> person_identities.person_key
--       mail_thread-> smart_mail_threads.thread_key
--       smart_note -> the note's brain-estate id (alias-scoped store)
--       list       -> the list's name in owner scope (naya_notes.list_name
--                     is the standing precedent; step 15 gives lists
--                     durable ids, and text refs carry either form)
--   object_facts — element #19 on the same model: a handful of plain
--     owner-named key/value facts per object (limit 12, enforced by
--     trigger). Deliberately NOT a field editor: no types, no schema,
--     no admin surface — the owner names a fact by asking, it is stored
--     as words.
--
-- THE OPERATION
--   file_object_under(...) is the write surfaces call ("file this under
--   Mary / under Launch"). It is SECURITY DEFINER so the ownership rules
--   are enforced in the database, identically for every caller: the
--   target person must be the caller's own, and where the subject's
--   store carries owner_id (naya_notes, smart_links, person_identities)
--   the subject must be the caller's own too. Stores keyed by
--   owner_alias alone (smart_notes, mail threads, lists) cannot be
--   owner-proven in SQL; the link row is stamped with the caller's
--   owner_id and RLS confines it to the caller — the same trust shape
--   as person_identities, the owner's private map.
--
-- RLS fitting (mirrors naya_notes / the flagship messaging pattern):
-- authenticated owner-only, owner_id = auth.uid(), NO anon policies —
-- a person's links and facts are private, never publicly readable.
-- Registered PENDING_REVIEW_NOT_PRODUCTION_APPLIED; applies at the
-- human gate only, after 20261022201500 / 20261022203000 /
-- 20261022204500 (its validation reads their tables).

-- ——— Fail-loud source check: the stores this model validates against ———
do $$
declare
  missing text[] := '{}';
  tbl text;
begin
  foreach tbl in array array['person_identities', 'naya_notes', 'smart_links']
  loop
    if not exists (
      select 1 from information_schema.tables c
      where c.table_schema = 'public' and c.table_name = tbl
    ) then
      missing := missing || tbl;
    end if;
  end loop;
  if array_length(missing, 1) is not null then
    raise exception 'OBJECT_LINKS_SOURCE_TABLES_MISSING: %', array_to_string(missing, ', ');
  end if;
end $$;

create table if not exists public.object_links (
  id uuid primary key default gen_random_uuid(),
  owner_alias text not null,
  owner_id uuid,
  subject_kind text not null
    constraint object_links_subject_kind
    check (subject_kind in ('smart_note', 'naya_note', 'mail_thread', 'smart_link', 'person', 'list')),
  subject_ref text not null,
  target_kind text not null
    constraint object_links_target_kind
    check (target_kind in ('person', 'list', 'mail_thread')),
  target_ref text not null,
  relation text not null default 'filed_under'
    constraint object_links_relation
    check (relation in ('filed_under')),
  created_at timestamptz not null default now(),
  constraint object_links_subject_ref_nonempty check (char_length(btrim(subject_ref)) > 0),
  constraint object_links_target_ref_nonempty check (char_length(btrim(target_ref)) > 0),
  constraint object_links_no_self_link
    check (not (subject_kind = target_kind and subject_ref = target_ref))
);

create unique index if not exists object_links_unique
  on public.object_links (owner_alias, subject_kind, subject_ref, target_kind, target_ref);
create index if not exists object_links_target_idx
  on public.object_links (owner_alias, target_kind, target_ref);
create index if not exists object_links_subject_idx
  on public.object_links (owner_alias, subject_kind, subject_ref);

create table if not exists public.object_facts (
  id uuid primary key default gen_random_uuid(),
  owner_alias text not null,
  owner_id uuid,
  object_kind text not null
    constraint object_facts_object_kind
    check (object_kind in ('smart_note', 'naya_note', 'mail_thread', 'smart_link', 'person', 'list')),
  object_ref text not null,
  fact_key text not null
    constraint object_facts_key_shape
    check (fact_key ~ '^[a-z0-9][a-z0-9 _-]{0,63}$'),
  fact_value text not null
    constraint object_facts_value_bounded check (char_length(fact_value) <= 500),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint object_facts_ref_nonempty check (char_length(btrim(object_ref)) > 0)
);

create unique index if not exists object_facts_unique
  on public.object_facts (owner_alias, object_kind, object_ref, lower(fact_key));
create index if not exists object_facts_object_idx
  on public.object_facts (owner_alias, object_kind, object_ref);

-- A handful means a handful: at most 12 facts per object. The 13th
-- distinct key is refused by name; updating an existing fact is not an
-- insert and is never blocked by this guard.
create or replace function public.object_facts_guard_limit()
returns trigger
language plpgsql
as $$
begin
  if (select count(*) from public.object_facts f
      where f.owner_alias = new.owner_alias
        and f.object_kind = new.object_kind
        and f.object_ref = new.object_ref) >= 12 then
    raise exception 'OBJECT_FACT_LIMIT_REACHED: % % already carries 12 facts',
      new.object_kind, new.object_ref
      using errcode = 'check_violation';
  end if;
  return new;
end;
$$;

drop trigger if exists object_facts_guard_limit on public.object_facts;
create trigger object_facts_guard_limit
  before insert on public.object_facts
  for each row execute function public.object_facts_guard_limit();

-- The write operation. SECURITY DEFINER so the ownership rules below run
-- identically for every surface (tap today, voice tomorrow); the caller
-- is always auth.uid() — there is no way to file as someone else.
create or replace function public.file_object_under(
  p_owner_alias text,
  p_subject_kind text,
  p_subject_ref text,
  p_target_kind text,
  p_target_ref text
)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  v_owner uuid := (select auth.uid());
  v_id uuid;
begin
  if v_owner is null then
    raise exception 'FILE_OBJECT_UNDER_REQUIRES_AUTH'
      using errcode = 'insufficient_privilege';
  end if;

  -- The target person must be the caller's own person.
  if p_target_kind = 'person' and not exists (
    select 1 from public.person_identities pi
    where pi.person_key = p_target_ref and pi.owner_id = v_owner
  ) then
    raise exception 'FILE_OBJECT_UNDER_TARGET_NOT_OWNED: person %', p_target_ref
      using errcode = 'insufficient_privilege';
  end if;

  -- The subject must be the caller's own wherever its store can prove it.
  if p_subject_kind = 'naya_note' and not exists (
    select 1 from public.naya_notes n
    where n.id::text = p_subject_ref and n.owner_id = v_owner
  ) then
    raise exception 'FILE_OBJECT_UNDER_SUBJECT_NOT_OWNED: naya_note %', p_subject_ref
      using errcode = 'insufficient_privilege';
  elsif p_subject_kind = 'smart_link' and not exists (
    select 1 from public.smart_links l
    where l.id::text = p_subject_ref and l.owner_id = v_owner
  ) then
    raise exception 'FILE_OBJECT_UNDER_SUBJECT_NOT_OWNED: smart_link %', p_subject_ref
      using errcode = 'insufficient_privilege';
  elsif p_subject_kind = 'person' and not exists (
    select 1 from public.person_identities pi
    where pi.person_key = p_subject_ref and pi.owner_id = v_owner
  ) then
    raise exception 'FILE_OBJECT_UNDER_SUBJECT_NOT_OWNED: person %', p_subject_ref
      using errcode = 'insufficient_privilege';
  end if;

  insert into public.object_links
    (owner_alias, owner_id, subject_kind, subject_ref, target_kind, target_ref)
  values
    (p_owner_alias, v_owner, p_subject_kind, p_subject_ref, p_target_kind, p_target_ref)
  on conflict (owner_alias, subject_kind, subject_ref, target_kind, target_ref)
  do nothing
  returning id into v_id;

  if v_id is null then
    select id into v_id from public.object_links
    where owner_alias = p_owner_alias
      and subject_kind = p_subject_kind and subject_ref = p_subject_ref
      and target_kind = p_target_kind and target_ref = p_target_ref;
  end if;
  return v_id;
end;
$$;

revoke all on function public.file_object_under(text, text, text, text, text) from public;
grant execute on function public.file_object_under(text, text, text, text, text) to authenticated;

alter table public.object_links enable row level security;
alter table public.object_facts enable row level security;

drop policy if exists object_links_owner_select on public.object_links;
create policy object_links_owner_select on public.object_links
  for select to authenticated
  using (owner_id = (select auth.uid()));

drop policy if exists object_links_owner_insert on public.object_links;
create policy object_links_owner_insert on public.object_links
  for insert to authenticated
  with check (owner_id = (select auth.uid()));

drop policy if exists object_links_owner_update on public.object_links;
create policy object_links_owner_update on public.object_links
  for update to authenticated
  using (owner_id = (select auth.uid()))
  with check (owner_id = (select auth.uid()));

drop policy if exists object_links_owner_delete on public.object_links;
create policy object_links_owner_delete on public.object_links
  for delete to authenticated
  using (owner_id = (select auth.uid()));

drop policy if exists object_facts_owner_select on public.object_facts;
create policy object_facts_owner_select on public.object_facts
  for select to authenticated
  using (owner_id = (select auth.uid()));

drop policy if exists object_facts_owner_insert on public.object_facts;
create policy object_facts_owner_insert on public.object_facts
  for insert to authenticated
  with check (owner_id = (select auth.uid()));

drop policy if exists object_facts_owner_update on public.object_facts;
create policy object_facts_owner_update on public.object_facts
  for update to authenticated
  using (owner_id = (select auth.uid()))
  with check (owner_id = (select auth.uid()));

drop policy if exists object_facts_owner_delete on public.object_facts;
create policy object_facts_owner_delete on public.object_facts
  for delete to authenticated
  using (owner_id = (select auth.uid()));
