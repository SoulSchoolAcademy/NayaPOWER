-- Live filing: DRIFT CORRECTION — bookings trigger functions as live SECURITY DEFINER — 2 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- DRIFT (DATABASE.md B1 / INVENTORY.md §3.4): booking_v1.sql defines these with NO security clause (invoker by default), but live they are SECURITY DEFINER. This migration files the live Definer form verbatim (CREATE OR REPLACE). Their triggers (bookings_fill_owner BEFORE INSERT ON bookings; bookings_guard_slot BEFORE INSERT OR UPDATE ON bookings) already exist in booking_v1.sql and are NOT re-created here.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- bookings_fill_owner()
--   live: public.bookings_fill_owner — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): BEFORE INSERT on bookings: fill owner_alias/owner_id from the page. (Booking)
--   captured: pg_get_functiondef(bookings_fill_owner) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.bookings_fill_owner()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
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
$function$;

-- ---------------------------------------------------------------------------
-- bookings_guard_slot()
--   live: public.bookings_guard_slot — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): BEFORE INSERT OR UPDATE on bookings: refuse double-booked / invalid slots. (Booking)
--   captured: pg_get_functiondef(bookings_guard_slot) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.bookings_guard_slot()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
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
$function$;
