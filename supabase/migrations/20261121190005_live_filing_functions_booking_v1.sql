-- Live filing: booking RPCs — 9 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- Public booking page reads + owner booking management. (cancel_booking already has repo source in booking_v1.sql and is NOT re-filed here.)
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- booking_avail_set(p_token text, p_page_id uuid, p_rows jsonb)
--   live: public.booking_avail_set — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner sets a booking page's availability windows; returns rows written. (Booking)
--   captured: pg_get_functiondef(booking_avail_set) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.booking_avail_set(p_token text, p_page_id uuid, p_rows jsonb)
 RETURNS integer
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_owner text; r jsonb; v_n integer := 0;
  v_wd integer; v_st time; v_et time; v_tz text;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  IF NOT EXISTS (SELECT 1 FROM public.booking_pages
                 WHERE id = p_page_id AND owner_alias = v_owner) THEN
    RAISE EXCEPTION 'not authorized';
  END IF;
  IF p_rows IS NULL OR jsonb_typeof(p_rows) <> 'array' THEN
    RAISE EXCEPTION 'rows must be an array';
  END IF;

  DELETE FROM public.booking_availability WHERE page_id = p_page_id;
  FOR r IN SELECT * FROM jsonb_array_elements(p_rows) LOOP
    v_wd := (r->>'weekday')::integer;
    v_st := (r->>'start_time')::time;
    v_et := (r->>'end_time')::time;
    v_tz := COALESCE(r->>'timezone', 'UTC');
    IF v_wd < 0 OR v_wd > 6 THEN RAISE EXCEPTION 'bad weekday'; END IF;
    IF v_st >= v_et THEN RAISE EXCEPTION 'bad window'; END IF;
    INSERT INTO public.booking_availability
      (page_id, weekday, start_time, end_time, timezone)
    VALUES (p_page_id, v_wd, v_st, v_et, v_tz);
    v_n := v_n + 1;
  END LOOP;
  RETURN v_n;
END $function$;

-- ---------------------------------------------------------------------------
-- booking_create(p_page_id uuid, p_visitor_name text, p_visitor_email text, p_starts_at timestamp with time zone, p_ends_at timestamp with time zone, p_note text)
--   live: public.booking_create — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): A visitor creates a booking on a public page; returns the booking id. (Booking)
--   captured: pg_get_functiondef(booking_create) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.booking_create(p_page_id uuid, p_visitor_name text, p_visitor_email text, p_starts_at timestamp with time zone, p_ends_at timestamp with time zone, p_note text)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_page public.booking_pages%ROWTYPE;
  v_id uuid;
  v_mins double precision;
BEGIN
  IF p_visitor_name IS NULL OR p_visitor_name = '' THEN
    RAISE EXCEPTION 'name required';
  END IF;
  IF p_starts_at IS NULL OR p_ends_at IS NULL OR p_ends_at <= p_starts_at THEN
    RAISE EXCEPTION 'bad slot';
  END IF;
  IF p_starts_at < now() THEN RAISE EXCEPTION 'slot is in the past'; END IF;

  -- Lock the page row: serializes concurrent bookings for this page.
  SELECT * INTO v_page FROM public.booking_pages
  WHERE id = p_page_id AND active = true FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'page not available'; END IF;

  -- Exact duration match.
  v_mins := EXTRACT(EPOCH FROM (p_ends_at - p_starts_at)) / 60;
  IF v_mins <> v_page.duration_minutes THEN RAISE EXCEPTION 'bad slot length'; END IF;

  -- Inside owner's availability (weekday 0=Sunday, matches JS getDay()).
  IF NOT EXISTS (
    SELECT 1 FROM public.booking_availability a
    WHERE a.page_id = p_page_id
      AND a.weekday = EXTRACT(DOW FROM p_starts_at)::int
      AND a.start_time <= p_starts_at::time
      AND a.end_time >= p_ends_at::time
  ) THEN RAISE EXCEPTION 'outside availability'; END IF;

  -- No overlap with a live booking.
  IF EXISTS (
    SELECT 1 FROM public.bookings b
    WHERE b.page_id = p_page_id
      AND b.status <> 'cancelled'
      AND b.starts_at < p_ends_at AND b.ends_at > p_starts_at
  ) THEN RAISE EXCEPTION 'slot taken'; END IF;

  INSERT INTO public.bookings
    (page_id, owner_alias, owner_id, visitor_name, visitor_email_hash,
     starts_at, ends_at, status, note)
  VALUES
    (p_page_id, v_page.owner_alias, v_page.owner_id, p_visitor_name,
     CASE WHEN p_visitor_email IS NULL OR p_visitor_email = '' THEN NULL
          ELSE encode(extensions.extensions.digest(lower(trim(p_visitor_email)), 'sha256'), 'hex')
     END,
     p_starts_at, p_ends_at, 'confirmed', NULLIF(p_note,''))
  RETURNING id INTO v_id;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- booking_owner_list(p_token text, p_page_id uuid, p_from date, p_to date)
--   live: public.booking_owner_list — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Owner lists bookings on a page (date-filtered, as JSON). (Booking)
--   captured: pg_get_functiondef(booking_owner_list) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.booking_owner_list(p_token text, p_page_id uuid, p_from date, p_to date)
 RETURNS jsonb
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT COALESCE(jsonb_agg(jsonb_build_object(
      'id', b.id, 'visitor_name', b.visitor_name,
      'starts_at', b.starts_at, 'ends_at', b.ends_at,
      'status', b.status, 'note', b.note, 'created_at', b.created_at)
      ORDER BY b.starts_at), '[]'::jsonb)
  FROM public.bookings b
  WHERE b.page_id = p_page_id
    AND b.owner_alias = public.owner_alias_for(p_token)
    AND public.owner_alias_for(p_token) <> ''
    AND b.starts_at::date BETWEEN COALESCE(p_from, b.starts_at::date)
                              AND COALESCE(p_to,   b.starts_at::date)
$function$;

-- ---------------------------------------------------------------------------
-- booking_owner_pages(p_token text)
--   live: public.booking_owner_pages — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): All booking pages belonging to this owner. (Booking)
--   captured: pg_get_functiondef(booking_owner_pages) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.booking_owner_pages(p_token text)
 RETURNS SETOF booking_pages
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT p.* FROM public.booking_pages p
  WHERE p.owner_alias = public.owner_alias_for(p_token)
    AND public.owner_alias_for(p_token) <> ''
  ORDER BY p.created_at DESC
$function$;

-- ---------------------------------------------------------------------------
-- booking_owner_set_status(p_token text, p_booking_id uuid, p_status text)
--   live: public.booking_owner_set_status — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner changes a booking's status (confirm/cancel). (Booking)
--   captured: pg_get_functiondef(booking_owner_set_status) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.booking_owner_set_status(p_token text, p_booking_id uuid, p_status text)
 RETURNS boolean
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_owner text;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  IF p_status NOT IN ('confirmed','cancelled') THEN RAISE EXCEPTION 'bad status'; END IF;
  UPDATE public.bookings SET status = p_status, updated_at = now()
  WHERE id = p_booking_id AND owner_alias = v_owner;
  RETURN FOUND;
END $function$;

-- ---------------------------------------------------------------------------
-- booking_page_is_active(p_page_id uuid)
--   live: public.booking_page_is_active — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Is this booking page live? (Booking)
--   captured: pg_get_functiondef(booking_page_is_active) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.booking_page_is_active(p_page_id uuid)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$ SELECT EXISTS (SELECT 1 FROM public.booking_pages WHERE id = p_page_id AND active = true); $function$;

-- ---------------------------------------------------------------------------
-- booking_page_public(p_slug text)
--   live: public.booking_page_public — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Public view of a booking page by slug (what a visitor sees). (Booking)
--   captured: pg_get_functiondef(booking_page_public) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.booking_page_public(p_slug text)
 RETURNS jsonb
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT jsonb_build_object(
    'page', jsonb_build_object(
      'id', p.id, 'slug', p.slug, 'title', p.title,
      'duration_minutes', p.duration_minutes, 'owner_alias', p.owner_alias),
    'availability', COALESCE((
      SELECT jsonb_agg(jsonb_build_object(
        'weekday', a.weekday, 'start_time', a.start_time::text,
        'end_time', a.end_time::text, 'timezone', a.timezone)
        ORDER BY a.weekday, a.start_time)
      FROM public.booking_availability a WHERE a.page_id = p.id
    ), '[]'::jsonb),
    'booked', COALESCE((
      SELECT jsonb_agg(jsonb_build_object(
        'starts_at', b.starts_at, 'ends_at', b.ends_at)
        ORDER BY b.starts_at)
      FROM public.bookings b
      WHERE b.page_id = p.id AND b.status <> 'cancelled'
        AND b.ends_at > now()
    ), '[]'::jsonb)
  )
  FROM public.booking_pages p
  WHERE p.slug = p_slug AND p.active = true
  LIMIT 1
$function$;

-- ---------------------------------------------------------------------------
-- booking_page_upsert(p_token text, p_page_id uuid, p_slug text, p_title text, p_duration_minutes integer, p_active boolean)
--   live: public.booking_page_upsert — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner creates/updates a booking page. (Booking)
--   captured: pg_get_functiondef(booking_page_upsert) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.booking_page_upsert(p_token text, p_page_id uuid, p_slug text, p_title text, p_duration_minutes integer, p_active boolean)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_owner text; v_id uuid;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  IF p_title IS NULL OR p_title = '' THEN RAISE EXCEPTION 'title required'; END IF;
  IF p_duration_minutes IS NULL OR p_duration_minutes < 5
     OR p_duration_minutes > 480 THEN RAISE EXCEPTION 'bad duration'; END IF;

  IF p_page_id IS NULL THEN
    IF p_slug IS NULL OR p_slug = '' THEN RAISE EXCEPTION 'slug required'; END IF;
    INSERT INTO public.booking_pages
      (owner_alias, slug, title, duration_minutes, active)
    VALUES (v_owner, p_slug, p_title, p_duration_minutes, COALESCE(p_active, true))
    RETURNING id INTO v_id;
  ELSE
    UPDATE public.booking_pages SET
      slug = COALESCE(NULLIF(p_slug,''), slug),
      title = p_title,
      duration_minutes = p_duration_minutes,
      active = COALESCE(p_active, active),
      updated_at = now()
    WHERE id = p_page_id AND owner_alias = v_owner
    RETURNING id INTO v_id;
    IF NOT FOUND THEN RAISE EXCEPTION 'not authorized'; END IF;
  END IF;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- get_plugin_booking_state(p_owner_alias text)
--   live: public.get_plugin_booking_state — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Booking state for the plugin/embed view. (Booking)
--   captured: pg_get_functiondef(get_plugin_booking_state) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.get_plugin_booking_state(p_owner_alias text)
 RETURNS TABLE(pages integer, upcoming integer, next_at timestamp with time zone, next_title text, first_slug text, sync_states text[])
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select
    (select count(*)::int from public.booking_pages
      where owner_alias = p_owner_alias and active = true),
    (select count(*)::int from public.bookings
      where owner_alias = p_owner_alias and status = 'confirmed'
        and starts_at >= now()),
    (select b.starts_at from public.bookings b
      where b.owner_alias = p_owner_alias and b.status = 'confirmed'
        and b.starts_at >= now()
      order by b.starts_at asc limit 1),
    (select p.title from public.bookings b
      join public.booking_pages p on p.id = b.page_id
      where b.owner_alias = p_owner_alias and b.status = 'confirmed'
        and b.starts_at >= now()
      order by b.starts_at asc limit 1),
    (select slug from public.booking_pages
      where owner_alias = p_owner_alias and active = true
      order by created_at asc limit 1),
    (select coalesce(array_agg(distinct calendar_sync_state), '{}')
      from public.booking_pages
      where owner_alias = p_owner_alias and active = true);
$function$;
