-- 20261022210000_booking_v1.sql
-- Best-of-Best Wave 1: the Booking block (map element #17, build step 17).
--
-- "Your booking link lives on your app; someone picks a time, both sides
-- get reminded, and the booking lands on the person's timeline."
--
-- What this migration creates:
--   booking_pages        — one named booking page per offering. The slug
--                          is a booking link in the Smart Links shape
--                          (named, owner-scoped, same name grammar as
--                          public.smart_links). The page is the durable
--                          object; the nayanet.live/<name> redirect
--                          worker is element #3's and ships gated — this
--                          block never depends on it. The Hub surface is
--                          HUB/booking/.
--   booking_availability — the owner's windows, set once: weekday +
--                          local time range + timezone, per page.
--   bookings             — one row per booking. Double-booking is refused
--                          twice: an availability/overlap trigger (the
--                          rule, with a named error) and a partial unique
--                          index (the race-proof backstop). Cancelling
--                          frees the slot: both guards ignore cancelled
--                          rows. Visitor identity is hash-only for email
--                          (the invites pattern: never the email itself).
--
-- Reminders ride the Smart Mail store (smart_mail_threads /
-- smart_mail_messages, the evidenced columns) — written by the Hub
-- booking module at booking time for BOTH sides (owner + visitor), never
-- by external email. There is deliberately no mail table in this
-- migration: the mail store already exists and is not this block's to
-- redefine.
--
-- Timeline write: the migration EXTENDS public.person_timeline_events
-- (element #1's read model, migration 20261022203000) with a bookings
-- branch in the ONE event shape, keyed by the same
-- resolve_person_key(owner, visitor_name, visitor_email_hash) rule, so a
-- confirmed booking lands on the visitor's timeline the moment it exists.
-- A fail-loud guard refuses to apply if that read model is absent.
--
-- Calendar sync is element #21's first plug-in source and is OUT of this
-- build: booking_pages.calendar_sync_state ships as the honest
-- placeholder 'not_connected'. Nothing in this block claims a sync.
--
-- RLS fitting (mirrors Phase 0: smart_links + naya_notes):
--   - owners act as authenticated users scoped by owner_id = auth.uid().
--   - visitors are anonymous: they can do exactly three things, all
--     through SECURITY DEFINER RPCs or a guarded insert — read one page's
--     public shape + windows (RPC), read TAKEN TIME RANGES for a page
--     (RPC: times only, never who booked), insert one booking on an
--     active page (policy + trigger guards), and cancel their own
--     booking with its cancel token (RPC). There is NO anon select on
--     booking_pages, booking_availability, or bookings: availability
--     reads expose windows, never other bookings' details.
--   - service_role bypasses RLS for governed server-side writes.
-- Registered PENDING_REVIEW_NOT_PRODUCTION_APPLIED; applies at the human
-- gate only.

create table if not exists public.booking_pages (
  id uuid primary key default gen_random_uuid(),
  owner_alias text not null,
  owner_id uuid,
  slug text not null,
  title text not null,
  duration_minutes integer not null default 30
    constraint booking_pages_duration_sane
    check (duration_minutes between 5 and 480),
  active boolean not null default true,
  calendar_sync_state text not null default 'not_connected'
    constraint booking_pages_calendar_sync_state
    check (calendar_sync_state in ('not_connected', 'connected')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint booking_pages_slug_shape
    check (slug ~ '^[a-z0-9][a-z0-9-]{1,62}$'),
  constraint booking_pages_title_nonempty
    check (char_length(btrim(title)) > 0)
);

create unique index if not exists booking_pages_slug_unique
  on public.booking_pages (lower(slug));
create index if not exists booking_pages_owner_idx
  on public.booking_pages (owner_alias, created_at desc);

create table if not exists public.booking_availability (
  id uuid primary key default gen_random_uuid(),
  page_id uuid not null references public.booking_pages(id) on delete cascade,
  weekday smallint not null
    constraint booking_availability_weekday_range
    check (weekday between 0 and 6),
  start_time time not null,
  end_time time not null,
  timezone text not null default 'UTC',
  created_at timestamptz not null default now(),
  constraint booking_availability_window_sane
    check (end_time > start_time)
);

create index if not exists booking_availability_page_idx
  on public.booking_availability (page_id, weekday, start_time);

create table if not exists public.bookings (
  id uuid primary key default gen_random_uuid(),
  page_id uuid not null references public.booking_pages(id) on delete cascade,
  owner_alias text not null,
  owner_id uuid,
  visitor_name text not null,
  visitor_email_hash text,
  starts_at timestamptz not null,
  ends_at timestamptz not null,
  status text not null default 'confirmed'
    constraint bookings_status_known
    check (status in ('confirmed', 'cancelled')),
  note text,
  cancel_token uuid not null default gen_random_uuid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint bookings_span_sane check (ends_at > starts_at),
  constraint bookings_visitor_named
    check (char_length(btrim(visitor_name)) > 0)
);

-- The race-proof backstop: at most one CONFIRMED booking per page per
-- start instant, whatever path the insert took. Cancelled rows are
-- excluded — cancelling frees the slot.
create unique index if not exists bookings_one_confirmed_per_slot
  on public.bookings (page_id, starts_at)
  where status = 'confirmed';
create index if not exists bookings_owner_time_idx
  on public.bookings (owner_alias, starts_at desc);
create index if not exists bookings_page_time_idx
  on public.bookings (page_id, starts_at);

-- Owner denormalization comes from the page, never from the visitor's
-- payload: owner_alias / owner_id on a booking row are the page's.
create or replace function public.bookings_fill_owner()
returns trigger
language plpgsql
as $$
declare
  p record;
begin
  select owner_alias, owner_id into p
  from public.booking_pages where id = new.page_id;
  if not found then
    raise exception 'booking page % does not exist', new.page_id
      using errcode = 'foreign_key_violation';
  end if;
  new.owner_alias := p.owner_alias;
  new.owner_id := p.owner_id;
  return new;
end;
$$;

drop trigger if exists bookings_fill_owner on public.bookings;
create trigger bookings_fill_owner
  before insert on public.bookings
  for each row execute function public.bookings_fill_owner();

-- The availability + overlap guard. A confirmed booking must (a) fit
-- inside ONE availability window of its page, judged in that window's
-- timezone on that local weekday, and (b) not overlap any other
-- confirmed booking on the page. Both refusals carry named errors the
-- Hub module maps to plain words ('outside_availability', 'slot_taken').
create or replace function public.bookings_guard_slot()
returns trigger
language plpgsql
as $$
declare
  fits boolean;
begin
  if new.status <> 'confirmed' then
    return new;
  end if;
  select exists (
    select 1
    from public.booking_availability w
    where w.page_id = new.page_id
      and extract(dow from (new.starts_at at time zone w.timezone))::int = w.weekday
      and (new.starts_at at time zone w.timezone)::date
        = (new.ends_at at time zone w.timezone)::date
      and (new.starts_at at time zone w.timezone)::time >= w.start_time
      and (new.ends_at at time zone w.timezone)::time <= w.end_time
  ) into fits;
  if not fits then
    raise exception 'booking_outside_availability'
      using errcode = 'check_violation';
  end if;
  if exists (
    select 1
    from public.bookings b
    where b.page_id = new.page_id
      and b.status = 'confirmed'
      and (new.id is null or b.id <> new.id)
      and tstzrange(b.starts_at, b.ends_at) && tstzrange(new.starts_at, new.ends_at)
  ) then
    raise exception 'booking_slot_taken'
      using errcode = 'unique_violation';
  end if;
  return new;
end;
$$;

drop trigger if exists bookings_guard_slot on public.bookings;
create trigger bookings_guard_slot
  before insert or update of starts_at, ends_at, page_id, status
  on public.bookings
  for each row execute function public.bookings_guard_slot();

-- ——— Public reads: RPCs only (the tables are never anon-listable) ———

-- One page's public shape. No owner_id, no bookings, nothing enumerable.
create or replace function public.get_booking_page(p_slug text)
returns table (
  page_id uuid, owner_alias text, title text,
  duration_minutes integer, calendar_sync_state text
)
language sql
stable
security definer
set search_path = public
as $$
  select p.id, p.owner_alias, p.title, p.duration_minutes,
         p.calendar_sync_state
  from public.booking_pages p
  where lower(p.slug) = lower(p_slug) and p.active = true
  limit 1;
$$;

revoke all on function public.get_booking_page(text) from public;
grant execute on function public.get_booking_page(text)
  to anon, authenticated;

-- The page's availability windows (the owner's public offering).
create or replace function public.get_booking_windows(p_slug text)
returns table (
  weekday smallint, start_time time, end_time time, timezone text
)
language sql
stable
security definer
set search_path = public
as $$
  select w.weekday, w.start_time, w.end_time, w.timezone
  from public.booking_availability w
  join public.booking_pages p on p.id = w.page_id
  where lower(p.slug) = lower(p_slug) and p.active = true
  order by w.weekday, w.start_time;
$$;

revoke all on function public.get_booking_windows(text) from public;
grant execute on function public.get_booking_windows(text)
  to anon, authenticated;

-- Taken TIME RANGES for a page in a window of days. Times only — never
-- who booked, never a note, never a name. This is what a booking picker
-- greys out; it is the whole of what a stranger may learn.
create or replace function public.get_booked_starts(
  p_slug text, p_from timestamptz, p_to timestamptz
)
returns table (starts_at timestamptz, ends_at timestamptz)
language sql
stable
security definer
set search_path = public
as $$
  select b.starts_at, b.ends_at
  from public.bookings b
  join public.booking_pages p on p.id = b.page_id
  where lower(p.slug) = lower(p_slug) and p.active = true
    and b.status = 'confirmed'
    and tstzrange(b.starts_at, b.ends_at) && tstzrange(p_from, p_to)
  order by b.starts_at;
$$;

revoke all on function public.get_booked_starts(text, timestamptz, timestamptz)
  from public;
grant execute on function
  public.get_booked_starts(text, timestamptz, timestamptz)
  to anon, authenticated;

-- Visitor self-cancel: the cancel token issued at booking time is the
-- whole credential. Flips one confirmed row to cancelled (freeing the
-- slot) and reports whether it did. A wrong token changes nothing.
create or replace function public.cancel_booking(
  p_booking_id uuid, p_cancel_token uuid
)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
  flipped integer;
begin
  update public.bookings
  set status = 'cancelled', updated_at = now()
  where id = p_booking_id
    and cancel_token = p_cancel_token
    and status = 'confirmed';
  get diagnostics flipped = row_count;
  return flipped = 1;
end;
$$;

revoke all on function public.cancel_booking(uuid, uuid) from public;
grant execute on function public.cancel_booking(uuid, uuid)
  to anon, authenticated;

alter table public.booking_pages enable row level security;
alter table public.booking_availability enable row level security;
alter table public.bookings enable row level security;

-- Pages: owners manage their own. No anon policy at all — public reads
-- go through the RPCs above.
drop policy if exists booking_pages_owner_select on public.booking_pages;
create policy booking_pages_owner_select on public.booking_pages
  for select to authenticated
  using (owner_id = (select auth.uid()));
drop policy if exists booking_pages_owner_insert on public.booking_pages;
create policy booking_pages_owner_insert on public.booking_pages
  for insert to authenticated
  with check (owner_id = (select auth.uid()));
drop policy if exists booking_pages_owner_update on public.booking_pages;
create policy booking_pages_owner_update on public.booking_pages
  for update to authenticated
  using (owner_id = (select auth.uid()))
  with check (owner_id = (select auth.uid()));
drop policy if exists booking_pages_owner_delete on public.booking_pages;
create policy booking_pages_owner_delete on public.booking_pages
  for delete to authenticated
  using (owner_id = (select auth.uid()));

-- Availability: owners manage windows on their own pages only.
drop policy if exists booking_availability_owner_all
  on public.booking_availability;
create policy booking_availability_owner_all on public.booking_availability
  for all to authenticated
  using (
    exists (
      select 1 from public.booking_pages p
      where p.id = page_id and p.owner_id = (select auth.uid())
    )
  )
  with check (
    exists (
      select 1 from public.booking_pages p
      where p.id = page_id and p.owner_id = (select auth.uid())
    )
  );

-- Bookings: the owner reads and manages their own. A visitor may INSERT
-- one confirmed booking on an active page (the guard trigger + unique
-- index refuse the rest) and may never read, update, or delete rows
-- directly — cancellation goes through the token RPC.
drop policy if exists bookings_owner_select on public.bookings;
create policy bookings_owner_select on public.bookings
  for select to authenticated
  using (owner_id = (select auth.uid()));
drop policy if exists bookings_owner_insert on public.bookings;
create policy bookings_owner_insert on public.bookings
  for insert to authenticated
  with check (owner_id = (select auth.uid()));
drop policy if exists bookings_owner_update on public.bookings;
create policy bookings_owner_update on public.bookings
  for update to authenticated
  using (owner_id = (select auth.uid()))
  with check (owner_id = (select auth.uid()));
drop policy if exists bookings_owner_delete on public.bookings;
create policy bookings_owner_delete on public.bookings
  for delete to authenticated
  using (owner_id = (select auth.uid()));
drop policy if exists bookings_visitor_insert on public.bookings;
create policy bookings_visitor_insert on public.bookings
  for insert to anon, authenticated
  with check (
    status = 'confirmed'
    and exists (
      select 1 from public.booking_pages p
      where p.id = page_id and p.active = true
    )
  );

-- ——— Timeline write: bookings join the ONE event shape ———
-- Fail loud, like the read model's own source guard: if the timeline
-- (20261022203000_person_timeline_v1) has not applied, this migration
-- stops with a named exception instead of silently losing the timeline
-- half of the block.
do $$
begin
  if not exists (
    select 1 from pg_proc
    where proname = 'resolve_person_key'
  ) or not exists (
    select 1 from information_schema.views
    where table_schema = 'public' and table_name = 'person_timeline_events'
  ) then
    raise exception
      'BOOKING_TIMELINE_DEPENDENCY_MISSING: 20261022203000_person_timeline_v1 must apply first';
  end if;
end $$;

-- The view below reproduces the person_timeline_v1 branches verbatim
-- (wall_note, mail_message, invite — same columns, same order, same
-- resolution rule) and adds the bookings branch. event_at is the
-- booking's created_at: the moment the booking landed.
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
  from public.invites i

  union all

  -- Bookings: a confirmed booking is an event on the VISITOR's timeline
  -- in the owner's world — keyed by the same rule (email hash wins,
  -- else the normalized visitor name), scoped to the page's owner.
  select
    public.resolve_person_key(b.owner_alias,
      b.visitor_name, b.visitor_email_hash),
    b.owner_alias,
    b.created_at,
    'booking',
    'bookings',
    b.id::text,
    p.title,
    b.note,
    'inbound',
    b.visitor_name,
    null
  from public.bookings b
  join public.booking_pages p on p.id = b.page_id
  where b.status = 'confirmed';
