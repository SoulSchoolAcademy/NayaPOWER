-- 20261022220000_alias_binding_v1.sql
-- PR #2956 CURE ROUND 4 (2026-10-23): the alias-poisoning cure.
--
-- THE DEFECT (VERIFY Tier-A card 6354152883, score 8.0 NOT APPROVED;
-- close comment 6354197386): search_universal derived the caller's
-- alias set from rows the caller owns by uid in person_identities /
-- naya_notes / smart_links, where owner_alias is free text that no
-- RLS policy, check constraint, or trigger binds to the caller's uid.
-- ONE permitted attacker insert carrying the victim's alias made the
-- two alias-keyed branches (smart_notes, smart_mail_threads) return
-- victim rows, enumerable in ranked pages. The uid-keyed branches
-- never leaked. No production exposure ever existed: every involved
-- migration is PENDING and application is human-gated.
--
-- THE CURE — one canonical binding, enforced at write time and
-- trusted at read time:
--   1. public.owner_alias_claims is the ONLY uid<->alias binding.
--      A normalized alias (lower/btrim) belongs to exactly one uid,
--      first claim wins. The table is written by NOTHING except the
--      SECURITY DEFINER paths in this migration (the row guard, the
--      claim RPC, the one-time backfill below): RLS is enabled with a
--      select-own policy for transparency and NO write policy for
--      any client role, so free text can never become a binding by
--      being written anywhere.
--   2. A BEFORE INSERT OR UPDATE OF owner_alias, owner_id guard on
--      each of the three alias-source tables routes every write
--      through the binding: the row's alias is claimed for the row's
--      owner; if another uid claimed it first, the write is refused
--      (OWNER_ALIAS_ALREADY_CLAIMED). Pattern follows the estate's
--      existing guard-trigger precedent (smart_links_guard_reserved).
--      Rows with a NULL owner_id claim nothing and are untouched —
--      they could never enter a uid-derived alias set either.
--   3. public.claim_my_alias(p_alias) is the explicit claim path for
--      surfaces that bind an alias before any source row exists:
--      authenticated only, fails closed without an identity, same
--      first-claim rule, same refusal.
--   4. search_universal is redefined at the end of this migration
--      (its final definition; supersedes 20261022214500) to derive
--      its alias set from owner_alias_claims ONLY, matching the
--      flagship tables on the same normalization. The three source
--      tables no longer participate in the derivation at all.
-- person_identity_aliases (PR #2946) is NOT reused: it aliases
-- *people* (person_key -> name variants) inside one owner's map; it
-- is not an owner binding and keying search to it would be a second,
-- weaker mechanism for the same decision.
--
-- BACKFILL: existing uid-owned rows claim their aliases at apply
-- time, earliest created_at wins (ties broken by owner_id, so the
-- result is deterministic); later conflicting rows keep their data
-- but their alias binds to the first claimant, and any future write
-- to such a row's alias/owner columns is refused until the alias is
-- corrected. All three source tables exist by this version
-- (20261022201500 / 20261022203000 / 20261022204500).
-- Registered PENDING_REVIEW_NOT_PRODUCTION_APPLIED; applies at the
-- human gate only, in the same sitting as 20261022214500.

-- ——— The binding. One alias -> one owner, first claim wins. ———
create table if not exists public.owner_alias_claims (
  alias_normalized text primary key,
  owner_id uuid not null,
  claimed_via text not null default 'backfill'
    constraint owner_alias_claims_via
    check (claimed_via in ('person_identities', 'naya_notes',
                           'smart_links', 'claim_rpc', 'backfill')),
  claimed_at timestamptz not null default now()
);

create index if not exists owner_alias_claims_owner_idx
  on public.owner_alias_claims (owner_id);

alter table public.owner_alias_claims enable row level security;

-- Transparency only: an owner can read their own claims. There is
-- deliberately NO insert/update/delete policy for any client role —
-- claims are created solely by the definer paths below.
drop policy if exists owner_alias_claims_owner_select
  on public.owner_alias_claims;
create policy owner_alias_claims_owner_select
  on public.owner_alias_claims
  for select to authenticated
  using (owner_id = (select auth.uid()));

-- ——— The one claim operation. Every write path funnels here. ———
-- SECURITY DEFINER: it must write the claims table on behalf of a
-- caller who holds no write policy on it. Raises on a foreign claim;
-- returns silently on the caller's own (idempotent re-claim).
create or replace function public.bind_owner_alias_claim(
  p_alias_normalized text, p_owner_id uuid, p_via text
)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.owner_alias_claims
    (alias_normalized, owner_id, claimed_via)
  values (p_alias_normalized, p_owner_id, p_via)
  on conflict (alias_normalized) do nothing;
  -- After the conflict wait resolves, the row is visible (winner
  -- committed or our own insert landed). Anything but the caller's
  -- own uid holding the claim is a refusal.
  if (select c.owner_id from public.owner_alias_claims c
       where c.alias_normalized = p_alias_normalized) <> p_owner_id then
    raise exception
      'OWNER_ALIAS_ALREADY_CLAIMED: alias % is bound to another owner',
      p_alias_normalized
      using errcode = 'check_violation';
  end if;
end;
$$;

revoke all on function
  public.bind_owner_alias_claim(text, uuid, text) from public;

-- ——— The row guard on the three alias-source tables. ———
create or replace function public.bind_owner_alias()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  v_alias text := lower(btrim(coalesce(new.owner_alias, '')));
begin
  -- No owner, no binding: such rows never entered a uid-derived
  -- alias set and must not be able to pre-claim an alias either.
  if new.owner_id is null or v_alias = '' then
    return new;
  end if;
  perform public.bind_owner_alias_claim(v_alias, new.owner_id,
                                        tg_table_name);
  return new;
end;
$$;

revoke all on function public.bind_owner_alias() from public;

-- ——— The explicit claim path (bind before any source row). ———
create or replace function public.claim_my_alias(p_alias text)
returns text
language plpgsql
security definer
set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_alias text := lower(btrim(coalesce(p_alias, '')));
begin
  if v_uid is null then
    raise exception 'OWNER_ALIAS_CLAIM_REQUIRES_AUTH'
      using errcode = 'insufficient_privilege';
  end if;
  if v_alias = '' then
    raise exception 'OWNER_ALIAS_CLAIM_EMPTY'
      using errcode = 'check_violation';
  end if;
  perform public.bind_owner_alias_claim(v_alias, v_uid, 'claim_rpc');
  return v_alias;
end;
$$;

revoke all on function public.claim_my_alias(text) from public;
grant execute on function public.claim_my_alias(text) to authenticated;

-- ——— Backfill: first claim wins, deterministically. ———
insert into public.owner_alias_claims
  (alias_normalized, owner_id, claimed_via, claimed_at)
select a.alias_normalized, a.owner_id, 'backfill', a.first_at
from (
  select distinct on (x.alias_normalized)
         x.alias_normalized, x.owner_id, x.created_at as first_at
  from (
    select lower(btrim(owner_alias)) as alias_normalized,
           owner_id, created_at
      from public.person_identities
     where owner_id is not null and btrim(owner_alias) <> ''
    union all
    select lower(btrim(owner_alias)), owner_id, created_at
      from public.naya_notes
     where owner_id is not null and btrim(owner_alias) <> ''
    union all
    select lower(btrim(owner_alias)), owner_id, created_at
      from public.smart_links
     where owner_id is not null and btrim(owner_alias) <> ''
  ) x
  order by x.alias_normalized, x.created_at asc, x.owner_id asc
) a
on conflict (alias_normalized) do nothing;

-- ——— Arm the guard on all three alias-source tables. ———
drop trigger if exists owner_alias_bind on public.person_identities;
create trigger owner_alias_bind
  before insert or update of owner_alias, owner_id
  on public.person_identities
  for each row execute function public.bind_owner_alias();

drop trigger if exists owner_alias_bind on public.naya_notes;
create trigger owner_alias_bind
  before insert or update of owner_alias, owner_id
  on public.naya_notes
  for each row execute function public.bind_owner_alias();

drop trigger if exists owner_alias_bind on public.smart_links;
create trigger owner_alias_bind
  before insert or update of owner_alias, owner_id
  on public.smart_links
  for each row execute function public.bind_owner_alias();

-- ——— The service, redefined on the binding (cure round 4). ———
-- Byte-identical to 20261022214500's definition EXCEPT the alias-set
-- derivation (owner_alias_claims only) and the two flagship branch
-- predicates (normalized match). Ranking, shape, branches, grants:
-- unchanged. This is search_universal's final definition.

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

  -- The caller's own aliases: the server-controlled binding ONLY
  -- (public.owner_alias_claims, defined above in this migration).
  -- Free-text owner_alias written on caller-owned rows is NEVER a
  -- binding — deriving the set from it was the alias-poisoning defect
  -- (PR #2956 Tier-A card 6354152883). Claims are stored normalized
  -- (lower/btrim) and the alias-keyed branches below match on the
  -- same normalization, so case/whitespace variants of an owner's
  -- own alias keep working while no one else's rows can enter.
  select coalesce(array_agg(distinct c.alias_normalized), '{}')
    into v_aliases
  from public.owner_alias_claims c
  where c.owner_id = v_uid;

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
    where lower(btrim(n.owner_alias)) = any (v_aliases)
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
    where lower(btrim(t.owner_alias)) = any (v_aliases)
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
