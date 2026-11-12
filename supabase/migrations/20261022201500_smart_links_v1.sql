-- 20261022201500_smart_links_v1.sql
-- Best-of-Best Phase 0, step 1: Smart Links data foundation (map element #3).
--
-- Creates public.smart_links + public.smart_link_clicks + the reserved-name
-- guard table for nayanet.live/<name> tracked links. The redirect worker
-- ships as code in HUB/smart-links/ (deployment is human-gated, separately).
--
-- Estate note (Step-0 schema check, 2026-10-22): the flagship tables this
-- joins (smart_notes, smart_mail_*, invites) live in this same project
-- (dahisasgpfvziswqvmvm) but were created outside repo migration history.
-- This migration follows the governed repo path instead: it is registered
-- in supabase/PRODUCTION-MIGRATION-LEDGER-V1.json as
-- PENDING_REVIEW_NOT_PRODUCTION_APPLIED and applies only at the human gate.
--
-- RLS fitting (mirrors the flagship messaging pattern + GT-039 direction):
--   - anon can do exactly two things: resolve ONE active link by name via
--     the resolve_smart_link RPC (the links table itself is never listable
--     by anon), and append a click row for an active link. Append-only:
--     no anon update, no anon delete, anywhere.
--   - owners act as authenticated users scoped by owner_id = auth.uid();
--     owner_alias is the public identity the app already keys by.
--   - service_role bypasses RLS for governed server-side writes.

create table if not exists public.smart_links (
  id uuid primary key default gen_random_uuid(),
  owner_alias text not null,
  owner_id uuid,
  name text not null,
  target_url text not null,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint smart_links_name_shape
    check (name ~ '^[a-z0-9][a-z0-9-]{1,62}$'),
  constraint smart_links_target_shape
    check (target_url ~ '^https?://')
);

create unique index if not exists smart_links_name_unique
  on public.smart_links (lower(name));
create index if not exists smart_links_owner_idx
  on public.smart_links (owner_alias, created_at desc);

create table if not exists public.smart_link_clicks (
  id uuid primary key default gen_random_uuid(),
  link_id uuid not null references public.smart_links(id) on delete cascade,
  clicked_at timestamptz not null default now(),
  referrer_class text not null default 'direct'
    constraint smart_link_clicks_referrer_class
    check (referrer_class in ('direct', 'social', 'search', 'email', 'internal', 'other')),
  referrer_host text,
  attribution_id uuid not null default gen_random_uuid()
);

create index if not exists smart_link_clicks_link_time_idx
  on public.smart_link_clicks (link_id, clicked_at desc);
create index if not exists smart_link_clicks_attribution_idx
  on public.smart_link_clicks (attribution_id);

-- Reserved names: a link name may never shadow a real route, room, file,
-- or system path on nayanet.live. This table mirrors RESERVED_NAMES in
-- HUB/smart-links/reserved-names.mjs (the single source); a contract test
-- (tests/test_smart_links_contract.py) fails if the two ever drift.
create table if not exists public.smart_link_reserved_names (
  name text primary key
);

insert into public.smart_link_reserved_names (name) values
  ('rooms'),
  ('s'),
  ('identity'),
  ('identity.html'),
  ('hub'),
  ('feed'),
  ('today'),
  ('reports'),
  ('library'),
  ('connect'),
  ('ledger'),
  ('connections'),
  ('lists'),
  ('mail'),
  ('spaces'),
  ('settings'),
  ('start'),
  ('start-here'),
  ('sn'),
  ('share-img'),
  ('sync-heartbeat'),
  ('sync-heartbeat.json'),
  ('index'),
  ('index.html'),
  ('favicon.ico'),
  ('robots.txt'),
  ('sitemap.xml'),
  ('manifest.webmanifest'),
  ('well-known'),
  ('welcome'),
  ('join'),
  ('invite'),
  ('invites'),
  ('signup'),
  ('login'),
  ('signin'),
  ('dashboard'),
  ('booking'),
  ('product'),
  ('events'),
  ('community'),
  ('profile'),
  ('menu'),
  ('factory'),
  ('growth'),
  ('api'),
  ('app'),
  ('assets'),
  ('static'),
  ('public'),
  ('admin'),
  ('support'),
  ('help'),
  ('about'),
  ('privacy'),
  ('terms'),
  ('www'),
  ('naya'),
  ('nayanet')on conflict (name) do nothing;

-- The guard: no insert or rename may take a reserved name. Enforced in the
-- database (not only in app code) so every creation path — Growth UI, API,
-- or a hand-run insert — is refused identically.
create or replace function public.smart_links_guard_reserved()
returns trigger
language plpgsql
as $$
begin
  if exists (
    select 1 from public.smart_link_reserved_names r
    where r.name = lower(new.name)
  ) then
    raise exception 'smart link name % is reserved', new.name
      using errcode = 'check_violation';
  end if;
  new.name := lower(new.name);
  return new;
end;
$$;

drop trigger if exists smart_links_guard_reserved on public.smart_links;
create trigger smart_links_guard_reserved
  before insert or update of name on public.smart_links
  for each row execute function public.smart_links_guard_reserved();

-- Resolve ONE active link by name. SECURITY DEFINER so the redirect worker
-- (anon key) can resolve without any direct SELECT grant on the table:
-- anon can never enumerate the link directory.
create or replace function public.resolve_smart_link(p_name text)
returns table (link_id uuid, target_url text)
language sql
stable
security definer
set search_path = public
as $$
  select l.id, l.target_url
  from public.smart_links l
  where lower(l.name) = lower(p_name) and l.active = true
  limit 1;
$$;

revoke all on function public.resolve_smart_link(text) from public;
grant execute on function public.resolve_smart_link(text) to anon, authenticated;

alter table public.smart_links enable row level security;
alter table public.smart_link_clicks enable row level security;
alter table public.smart_link_reserved_names enable row level security;

-- Owners: full control of their own links, as authenticated users.
drop policy if exists smart_links_owner_select on public.smart_links;
create policy smart_links_owner_select on public.smart_links
  for select to authenticated
  using (owner_id = (select auth.uid()));

drop policy if exists smart_links_owner_insert on public.smart_links;
create policy smart_links_owner_insert on public.smart_links
  for insert to authenticated
  with check (owner_id = (select auth.uid()));

drop policy if exists smart_links_owner_update on public.smart_links;
create policy smart_links_owner_update on public.smart_links
  for update to authenticated
  using (owner_id = (select auth.uid()))
  with check (owner_id = (select auth.uid()));

drop policy if exists smart_links_owner_delete on public.smart_links;
create policy smart_links_owner_delete on public.smart_links
  for delete to authenticated
  using (owner_id = (select auth.uid()));

-- Clicks: anyone may APPEND a click for an active link (that is the public
-- redirect working); nobody but the link's owner may read clicks; there is
-- deliberately NO update or delete policy for any role — clicks are an
-- append-only record.
drop policy if exists smart_link_clicks_append on public.smart_link_clicks;
create policy smart_link_clicks_append on public.smart_link_clicks
  for insert to anon, authenticated
  with check (
    exists (
      select 1 from public.smart_links l
      where l.id = link_id and l.active = true
    )
  );

drop policy if exists smart_link_clicks_owner_select on public.smart_link_clicks;
create policy smart_link_clicks_owner_select on public.smart_link_clicks
  for select to authenticated
  using (
    exists (
      select 1 from public.smart_links l
      where l.id = link_id and l.owner_id = (select auth.uid())
    )
  );

-- The reserved list is public knowledge (it mirrors live routes): readable
-- by all, writable by none (service_role only, via migration seeds).
drop policy if exists smart_link_reserved_names_read on public.smart_link_reserved_names;
create policy smart_link_reserved_names_read on public.smart_link_reserved_names
  for select to anon, authenticated
  using (true);
