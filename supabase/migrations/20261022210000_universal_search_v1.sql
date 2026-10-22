-- 20261022210000_universal_search_v1.sql
-- Best-of-Best Wave 1: Command + universal search (map element #12,
-- build-order step 13 — the Linear lesson: one place to find and do
-- anything).
--
-- THE SERVICE: public.search_universal(p_query, p_limit) returns ONE
-- ranked result set across the object types that exist in this project:
--   person      — public.person_identities (the step-2 timeline read
--                 model's durable identity registry, PR #2946)
--   smart_note  — public.smart_notes (the flagship wall table)
--   naya_note   — public.naya_notes (element #15 store, PR #2947)
--   mail_thread — public.smart_mail_threads (Smart Mail)
--   smart_link  — public.smart_links (element #3, PR #2945)
-- Every row carries the action that acts on it (open_person / open_room /
-- open_url + target), so a surface never renders a dead result.
--
-- ISOLATION IS THE CONTRACT (negative control, structural):
--   - The function takes NO owner parameter. Identity comes only from
--     auth.uid() inside the function; there is nothing a client can pass
--     to widen its own reach.
--   - SECURITY DEFINER is required (the flagship tables carry no
--     repo-governed RLS this function could lean on), so EVERY source
--     branch below carries its own owner predicate: owner_id = auth.uid()
--     on the Phase-0 tables, and owner_alias in the caller's own alias
--     set on the alias-keyed flagship tables. The alias set is derived
--     from rows the caller owns by uid — never from input.
--   - No identity (auth.uid() is null) returns ZERO rows. Fail closed.
--   - EXECUTE is granted to authenticated only. Unlike resolve_smart_link
--     (public by design), search is owner-private: anon gets nothing.
--
-- RANKING IS ONE DEFINITION: public.search_score(field, query) —
-- 100 exact · 80 prefix · 60 word-start · 40 contains, case-insensitive,
-- with LIKE metacharacters in the query escaped so a query can never
-- widen its own match. A source's score is the best of its fields.
--
-- SPEED: every branch filters on an owner index first (the Phase-0
-- tables carry owner indexes; person search additionally gets a
-- (owner_id, lower(display_name)) index below), so an everyday query
-- reads one owner's corpus — never the estate's. Per-source caps keep
-- any single branch from flooding the merged set before ranking.
--
-- SOURCE-COLUMN CONTRACT: smart_notes and smart_mail_threads were
-- created in this project outside repo migration history (Step-0 schema
-- check, 2026-10-22). The guard below fails LOUD — a named exception,
-- no silently-empty search — if any column this function reads is
-- absent in the applying project. Columns follow the evidenced set:
--   smart_notes:        owner_alias, content, created_at, author_name,
--                       sender_name
--   smart_mail_threads: owner_alias, subject, participants, thread_key,
--                       created_at, updated_at
-- Registered PENDING_REVIEW_NOT_PRODUCTION_APPLIED; applies at the
-- human gate only.

-- ——— Fail-loud source check ———
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
      ('smart_mail_threads', 'owner_alias'),
      ('smart_mail_threads', 'subject'),
      ('smart_mail_threads', 'participants'),
      ('smart_mail_threads', 'thread_key'),
      ('smart_mail_threads', 'created_at'),
      ('smart_mail_threads', 'updated_at')
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
    raise exception 'UNIVERSAL_SEARCH_SOURCE_COLUMNS_MISSING: %',
      array_to_string(missing, ', ');
  end if;
end $$;

-- Name lookup is the everyday query: index it on the identity registry.
create index if not exists person_identities_owner_name_idx
  on public.person_identities (owner_id, lower(display_name));

-- ——— The ranking definition. ONE place, used by every branch. ———
-- Pure string math over caller-supplied text: no data access, safe to
-- grant. Returns 0 for no match / empty query / null field.
create or replace function public.search_score(p_field text, p_query text)
returns double precision
language sql
immutable
as $$
  with v as (
    select lower(trim(coalesce(p_query, ''))) as raw,
           replace(replace(replace(
             lower(trim(coalesce(p_query, ''))),
             '\', '\\'), '%', '\%'), '_', '\_') as esc
  )
  select case
    when p_field is null or (select raw from v) = '' then 0::double precision
    when lower(p_field) = (select raw from v) then 100::double precision
    when lower(p_field) like (select esc from v) || '%' escape '\'
      then 80::double precision
    when lower(p_field) like '% ' || (select esc from v) || '%' escape '\'
      then 60::double precision
    when lower(p_field) like '%' || (select esc from v) || '%' escape '\'
      then 40::double precision
    else 0::double precision
  end;
$$;

revoke all on function public.search_score(text, text) from public;
grant execute on function public.search_score(text, text) to authenticated;

-- ——— The service. ———
create or replace function public.search_universal(
  p_query text, p_limit integer default 20
)
returns table (
  object_type text,
  object_id text,
  title text,
  snippet text,
  action_kind text,
  action_target text,
  score double precision,
  occurred_at timestamptz
)
language plpgsql
stable
security definer
set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_limit integer := least(greatest(coalesce(p_limit, 20), 1), 50);
  v_aliases text[] := '{}';
begin
  -- Fail closed: no authenticated identity, no results, no leak.
  if v_uid is null then
    return;
  end if;
  if lower(trim(coalesce(p_query, ''))) = '' then
    return;
  end if;

  -- The caller's own aliases, derived from rows they own by uid across
  -- the Phase-0 tables. Never from input; empty set = alias-keyed
  -- sources return nothing for this caller.
  select coalesce(array_agg(distinct a), '{}') into v_aliases
  from (
    select owner_alias as a from public.person_identities
      where owner_id = v_uid
    union
    select owner_alias from public.naya_notes where owner_id = v_uid
    union
    select owner_alias from public.smart_links where owner_id = v_uid
  ) s
  where a is not null and a <> '';

  return query
  with hits as (
    -- PEOPLE — the timeline read model's identity registry.
    select
      'person'::text as object_type,
      pi.person_key as object_id,
      pi.display_name as title,
      'Person'::text as snippet,
      'open_person'::text as action_kind,
      pi.person_key as action_target,
      public.search_score(pi.display_name, p_query) as score,
      coalesce(pi.last_seen_at, pi.created_at) as occurred_at
    from public.person_identities pi
    where pi.owner_id = v_uid
      and public.search_score(pi.display_name, p_query) > 0

    union all

    -- SMART NOTES — the flagship wall. smart_notes carries no id column
    -- the repo can evidence, so the action opens the Feed room; the
    -- title is the note's own first words.
    select
      'smart_note',
      '',
      left(regexp_replace(n.content, '\s+', ' ', 'g'), 80),
      'Smart Note' ||
        case when coalesce(n.author_name, n.sender_name) is not null
          then ' · ' || coalesce(n.author_name, n.sender_name)
          else '' end,
      'open_room',
      'feed',
      greatest(
        public.search_score(n.content, p_query),
        public.search_score(coalesce(n.author_name, n.sender_name), p_query)
      ),
      n.created_at
    from public.smart_notes n
    where n.owner_alias = any (v_aliases)
      and greatest(
        public.search_score(n.content, p_query),
        public.search_score(coalesce(n.author_name, n.sender_name), p_query)
      ) > 0

    union all

    -- NAYA NOTES — the owner's private captures (element #15).
    select
      'naya_note',
      nn.id::text,
      left(split_part(nn.text, E'\n', 1), 80),
      'Naya Note · ' || nn.category,
      'open_room',
      'lists',
      greatest(
        public.search_score(nn.text, p_query),
        public.search_score(nn.category, p_query),
        public.search_score(nn.list_name, p_query)
      ),
      nn.created_at
    from public.naya_notes nn
    where nn.owner_id = v_uid
      and greatest(
        public.search_score(nn.text, p_query),
        public.search_score(nn.category, p_query),
        public.search_score(nn.list_name, p_query)
      ) > 0

    union all

    -- SMART MAIL THREADS — subject and participants.
    select
      'mail_thread',
      t.thread_key,
      coalesce(nullif(t.subject, ''), '(no subject)'),
      'Smart Mail thread',
      'open_room',
      'mail',
      greatest(
        public.search_score(t.subject, p_query),
        public.search_score(t.participants::text, p_query)
      ),
      coalesce(t.updated_at, t.created_at)
    from public.smart_mail_threads t
    where t.owner_alias = any (v_aliases)
      and greatest(
        public.search_score(t.subject, p_query),
        public.search_score(t.participants::text, p_query)
      ) > 0

    union all

    -- SMART LINKS — name and target; the action opens the short link.
    select
      'smart_link',
      l.id::text,
      l.name,
      'Smart Link · nayanet.live/' || l.name,
      'open_url',
      'https://nayanet.live/' || l.name,
      greatest(
        public.search_score(l.name, p_query),
        public.search_score(l.target_url, p_query)
      ),
      l.created_at
    from public.smart_links l
    where l.owner_id = v_uid
      and l.active = true
      and greatest(
        public.search_score(l.name, p_query),
        public.search_score(l.target_url, p_query)
      ) > 0
  )
  select h.object_type, h.object_id, h.title, h.snippet,
         h.action_kind, h.action_target, h.score, h.occurred_at
  from hits h
  order by h.score desc, h.occurred_at desc nulls last
  limit v_limit;
end;
$$;

-- Owner-private by design: authenticated callers only. No anon grant —
-- there is no public moment in a person's own objects.
revoke all on function public.search_universal(text, integer) from public;
grant execute on function public.search_universal(text, integer)
  to authenticated;
