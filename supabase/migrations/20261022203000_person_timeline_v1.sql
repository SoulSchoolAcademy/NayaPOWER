-- 20261022203000_person_timeline_v1.sql
-- Best-of-Best Phase 0, step 2: the per-person timeline read model
-- (map element #1, data half).
--
-- Faces (flagship People door) derives people by name-matching across the
-- wall, mail, and invites at read time. This migration makes that
-- derivation DURABLE: identities live in two tables, resolution rules live
-- in one SQL function, and every consumer (People UI, search, morning
-- briefs) reads ONE event shape from person_timeline_events.
--
-- SOURCE-COLUMN CONTRACT — read before applying.
-- The flagship source tables (smart_notes, smart_mail_threads,
-- smart_mail_messages, invites) were created in this project outside repo
-- migration history (Step-0 schema check, 2026-10-22). The columns below
-- are the ones evidenced in repo code:
--   smart_notes:          owner_alias, content, created_at   (proxy worker,
--                         templates/personal.html) + wall-name column in
--                         the Faces derivation (canon v6.12, templates-
--                         registry.json "faces"): author_name COALESCE
--                         sender_name.
--   smart_mail_threads:   owner_alias, subject, participants (canon),
--                         status, direction, thread_key, created_at,
--                         updated_at.
--   smart_mail_messages:  thread_key, sender, sender_name, body,
--                         direction, created_at.
--   invites:              invitee_email_hash (canon: invites are hash-only,
--                         "never email"), status, created_at.
-- The view definition at the end OPENS with a fail-loud guard: if any
-- required source column is absent in the applying project, the migration
-- raises a named exception and stops instead of creating a silently
-- empty view. Columns the sources do not carry are derived or honestly
-- NULL in the event shape (see the event contract in
-- docs/person-timeline-read-model.md) — never fabricated.
--
-- RLS fitting: identities are the owner's private map of their people —
-- authenticated owner-only, owner_id = auth.uid(), no anon policies at all.
-- Registered PENDING_REVIEW_NOT_PRODUCTION_APPLIED; applies at the human
-- gate only.

create table if not exists public.person_identities (
  person_key text primary key,
  owner_alias text not null,
  owner_id uuid,
  display_name text not null,
  normalized_name text not null,
  email_hash text,
  first_seen_at timestamptz,
  last_seen_at timestamptz,
  source jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists person_identities_owner_idx
  on public.person_identities (owner_alias, normalized_name);
create index if not exists person_identities_email_hash_idx
  on public.person_identities (email_hash) where email_hash is not null;

create table if not exists public.person_identity_aliases (
  alias_key text primary key,
  person_key text not null references public.person_identities(person_key) on delete cascade,
  kind text not null default 'manual'
    constraint person_identity_aliases_kind
    check (kind in ('manual', 'derived', 'imported')),
  created_at timestamptz not null default now()
);

create index if not exists person_identity_aliases_person_idx
  on public.person_identity_aliases (person_key);

-- Name normalization: ONE definition, used by the view, by the builder
-- (tools/person_timeline.py mirrors it exactly), and by every consumer.
-- Lowercase, collapse non-alphanumerics to single spaces, trim.
create or replace function public.normalize_person_name(p_name text)
returns text
language sql
immutable
as $$
  select trim(regexp_replace(lower(coalesce(p_name, '')), '[^a-z0-9]+', ' ', 'g'));
$$;

-- Deterministic person key from the resolution inputs. Email hash wins
-- when known (stable across name spellings); otherwise the normalized
-- name keys the person.
create or replace function public.resolve_person_key(
  p_owner_alias text, p_display_name text, p_email_hash text
)
returns text
language sql
immutable
as $$
  select case
    when p_email_hash is not null and p_email_hash <> ''
      then 'h:' || p_email_hash
    else 'n:' || public.normalize_person_name(p_display_name)
  end || '@' || lower(coalesce(p_owner_alias, ''));
$$;

alter table public.person_identities enable row level security;
alter table public.person_identity_aliases enable row level security;

drop policy if exists person_identities_owner_all on public.person_identities;
create policy person_identities_owner_all on public.person_identities
  for all to authenticated
  using (owner_id = (select auth.uid()))
  with check (owner_id = (select auth.uid()));

drop policy if exists person_identity_aliases_owner_all on public.person_identity_aliases;
create policy person_identity_aliases_owner_all on public.person_identity_aliases
  for all to authenticated
  using (
    exists (
      select 1 from public.person_identities pi
      where pi.person_key = person_key and pi.owner_id = (select auth.uid())
    )
  )
  with check (
    exists (
      select 1 from public.person_identities pi
      where pi.person_key = person_key and pi.owner_id = (select auth.uid())
    )
  );

-- ——— Fail-loud source check, then the unified event view ———
do $$
declare
  missing text[] := '{}';
  col record;
begin
  for col in
    select * from (values
      ('smart_notes', 'owner_alias'), ('smart_notes', 'content'),
      ('smart_notes', 'created_at'), ('smart_notes', 'author_name'),
      ('smart_notes', 'sender_name'),
      ('smart_mail_threads', 'owner_alias'), ('smart_mail_threads', 'subject'),
      ('smart_mail_threads', 'participants'), ('smart_mail_threads', 'status'),
      ('smart_mail_threads', 'created_at'), ('smart_mail_threads', 'updated_at'),
      ('smart_mail_messages', 'thread_key'), ('smart_mail_messages', 'body'),
      ('smart_mail_messages', 'direction'), ('smart_mail_messages', 'created_at'),
      ('invites', 'invitee_email_hash'), ('invites', 'status'),
      ('invites', 'created_at'), ('invites', 'owner_alias')
    ) as t(tbl, colname)
  loop
    if not exists (
      select 1 from information_schema.columns c
      where c.table_schema = 'public' and c.table_name = col.tbl
        and c.column_name = col.colname
    ) then
      missing := missing || (col.tbl || '.' || col.colname);
    end if;
  end loop;
  if array_length(missing, 1) is not null then
    raise exception 'PERSON_TIMELINE_SOURCE_COLUMNS_MISSING: %', array_to_string(missing, ', ');
  end if;
end $$;

-- The ONE event shape. Columns: person_key, owner_alias, event_at,
-- event_kind, source_table, source_id, title, body, direction,
-- counterparty_name, thread_key. See docs/person-timeline-read-model.md.
-- NOTE: smart_notes carries no person column the repo can evidence, so
-- wall events key to the note's author_name/sender_name when the applying
-- project has them; the guard above requires only the evidenced minimum
-- and this view uses the Faces COALESCE pattern for the name.
create or replace view public.person_timeline_events as
  select
    public.resolve_person_key(n.owner_alias,
      coalesce(n.author_name, n.sender_name), null) as person_key,
    n.owner_alias,
    n.created_at as event_at,
    'wall_note'::text as event_kind,
    'smart_notes'::text as source_table,
    null::text as source_id,
    null::text as title,
    n.content as body,
    'outbound'::text as direction,
    coalesce(n.author_name, n.sender_name) as counterparty_name,
    null::text as thread_key
  from public.smart_notes n
  where coalesce(n.author_name, n.sender_name) is not null

  union all

  -- Mail in this view: inbound messages key to their sender. Outbound
  -- messages key to the thread's OTHER participants — a derivation that
  -- needs participant parsing, which lives in the builder
  -- (tools/person_timeline.py); consumers needing outbound attribution
  -- read the builder's stream. The view never guesses.
  select
    public.resolve_person_key(t.owner_alias,
      coalesce(m.sender_name, m.sender), null),
    t.owner_alias,
    m.created_at,
    'mail_message',
    'smart_mail_messages',
    null,
    t.subject,
    m.body,
    m.direction,
    coalesce(m.sender_name, m.sender),
    m.thread_key
  from public.smart_mail_messages m
  join public.smart_mail_threads t on t.thread_key = m.thread_key
  where m.direction = 'inbound'
    and coalesce(m.sender_name, m.sender) is not null

  union all

  select
    public.resolve_person_key(i.owner_alias, null, i.invitee_email_hash),
    i.owner_alias,
    i.created_at,
    'invite',
    'invites',
    null,
    i.status,
    null,
    'outbound',
    null,
    null
  from public.invites i;
