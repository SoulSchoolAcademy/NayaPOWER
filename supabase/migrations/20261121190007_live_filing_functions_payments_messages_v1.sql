-- Live filing: payments + messaging + page RPCs — 8 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- Payment state reads, membership messaging, mail retention, About + products/services owner writes.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- get_payment_link(p_slug text)
--   live: public.get_payment_link — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Fetch a payment link's state for checkout. (Payments)
--   captured: pg_get_functiondef(get_payment_link) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.get_payment_link(p_slug text)
 RETURNS TABLE(link_id uuid, owner_alias text, title text, description text, amount_cents integer, currency text, smart_link_name text, connection_state text)
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select l.id, l.owner_alias, l.title, l.description,
         l.amount_cents, l.currency, l.smart_link_name,
         coalesce(c.state, 'not_connected')
  from public.payment_links l
  left join public.payment_connections c
    on c.owner_alias = l.owner_alias
  where lower(l.slug) = lower(p_slug) and l.active = true
  limit 1;
$function$;

-- ---------------------------------------------------------------------------
-- get_payment_recovery_candidates(p_owner_alias text)
--   live: public.get_payment_recovery_candidates — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Find payments that need recovery (failed/abandoned). (Payments)
--   captured: pg_get_functiondef(get_payment_recovery_candidates) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.get_payment_recovery_candidates(p_owner_alias text)
 RETURNS TABLE(payment_id uuid, buyer_name text, amount_cents integer, currency text, failure_reason text, created_at timestamp with time zone, link_title text, link_slug text)
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select p.id, p.buyer_name, p.amount_cents, p.currency,
         p.failure_reason, p.created_at, l.title, l.slug
  from public.payments p
  join public.payment_links l on l.id = p.link_id
  where p.owner_alias = p_owner_alias and p.status = 'failed'
  order by p.created_at desc
  limit 25;
$function$;

-- ---------------------------------------------------------------------------
-- get_payment_state(p_owner_alias text)
--   live: public.get_payment_state — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Current state of a payment. (Payments)
--   captured: pg_get_functiondef(get_payment_state) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.get_payment_state(p_owner_alias text)
 RETURNS TABLE(connection_state text, links integer, first_slug text, first_title text, gross_cents bigint, paid_count integer, failed_count integer, best_title text, best_cents bigint, last_at timestamp with time zone)
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  select
    coalesce((select c.state from public.payment_connections c
              where c.owner_alias = p_owner_alias), 'not_connected'),
    (select count(*)::integer from public.payment_links l
      where l.owner_alias = p_owner_alias and l.active = true),
    (select l.slug from public.payment_links l
      where l.owner_alias = p_owner_alias and l.active = true
      order by l.created_at asc, l.slug asc limit 1),
    (select l.title from public.payment_links l
      where l.owner_alias = p_owner_alias and l.active = true
      order by l.created_at asc, l.slug asc limit 1),
    (select coalesce(sum(p.amount_cents), 0)::bigint from public.payments p
      where p.owner_alias = p_owner_alias and p.status = 'succeeded'),
    (select count(*)::integer from public.payments p
      where p.owner_alias = p_owner_alias and p.status = 'succeeded'),
    (select count(*)::integer from public.payments p
      where p.owner_alias = p_owner_alias and p.status = 'failed'),
    (select l.title from public.payments p
      join public.payment_links l on l.id = p.link_id
      where p.owner_alias = p_owner_alias and p.status = 'succeeded'
      group by l.title
      order by sum(p.amount_cents) desc, l.title asc limit 1),
    (select coalesce(max(s), 0)::bigint from (
       select sum(p.amount_cents) as s from public.payments p
       where p.owner_alias = p_owner_alias and p.status = 'succeeded'
       group by p.link_id) g),
    (select max(p.created_at) from public.payments p
      where p.owner_alias = p_owner_alias and p.status = 'succeeded');
$function$;

-- ---------------------------------------------------------------------------
-- mship_send_message(p_token text, p_thread_id uuid, p_body text)
--   live: public.mship_send_message — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Send a message inside a membership. (Membership messages)
--   captured: pg_get_functiondef(mship_send_message) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_send_message(p_token text, p_thread_id uuid, p_body text)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_alias text; v_id uuid; v_to text;
BEGIN
  v_alias := public.owner_alias_for(p_token);
  IF v_alias = '' THEN
    -- member sessions are per-membership; messenger is citizen-level, so
    -- accept any live member session's alias as the sender identity.
    SELECT s.alias INTO v_alias FROM public.member_sessions s
    WHERE s.token_hash = public._mship_hash(p_token)
      AND s.revoked_at IS NULL AND s.expires_at > now() LIMIT 1;
  END IF;
  IF v_alias IS NULL OR v_alias = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  IF p_body IS NULL OR p_body = '' THEN RAISE EXCEPTION 'empty message'; END IF;
  -- Resolve the other participant from thread history; sender is FORCED.
  SELECT CASE WHEN from_alias = v_alias THEN to_alias ELSE from_alias END
    INTO v_to FROM public.messenger_messages
    WHERE thread_id = p_thread_id
      AND (from_alias = v_alias OR to_alias = v_alias)
    ORDER BY sent_at DESC LIMIT 1;
  IF v_to IS NULL THEN
    -- New thread: recipient must be supplied via thread bootstrap by the
    -- caller holding a valid session; without history we cannot address it.
    RAISE EXCEPTION 'unknown thread';
  END IF;
  INSERT INTO public.messenger_messages (thread_id, from_alias, to_alias, body)
  VALUES (p_thread_id, v_alias, v_to, p_body)
  RETURNING id INTO v_id;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- purge_expired_conversations()
--   live: public.purge_expired_conversations — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Delete expired conversations (deletion by default, enforced). (Smart Mail retention)
--   captured: pg_get_functiondef(purge_expired_conversations) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.purge_expired_conversations()
 RETURNS TABLE(deleted_threads integer, deleted_messages integer)
 LANGUAGE plpgsql
AS $function$ declare v_threads integer := 0; v_messages integer := 0; begin create temp table _expired_threads on commit drop as select t.id from public.smart_mail_threads t left join public.smart_mail_messages m on m.thread_id = t.id group by t.id, t.created_at having coalesce(max(m.created_at), t.created_at) < now() - interval '7 days'; select count(*) into v_messages from public.smart_mail_messages where thread_id in (select id from _expired_threads); delete from public.smart_mail_messages where thread_id in (select id from _expired_threads); delete from public.smart_mail_threads where id in (select id from _expired_threads); get diagnostics v_threads = row_count; return query select v_threads, v_messages; end; $function$;

-- ---------------------------------------------------------------------------
-- pa_owner_upsert(p_token text, p_page_kind text, p_page_alias text, p_headline text, p_body text, p_cover_url text)
--   live: public.pa_owner_upsert — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner upsert for page-about (About per page). (About)
--   captured: pg_get_functiondef(pa_owner_upsert) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.pa_owner_upsert(p_token text, p_page_kind text, p_page_alias text, p_headline text, p_body text, p_cover_url text)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_owner text; v_id uuid;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  INSERT INTO public.page_about
    (page_kind, page_alias, owner_alias, headline, body, cover_url)
  VALUES (p_page_kind, p_page_alias, v_owner, p_headline, p_body, p_cover_url)
  ON CONFLICT (page_kind, page_alias) DO UPDATE SET
    headline = EXCLUDED.headline, body = EXCLUDED.body,
    cover_url = EXCLUDED.cover_url
    WHERE public.page_about.owner_alias = v_owner
  RETURNING id INTO v_id;
  IF NOT FOUND THEN RAISE EXCEPTION 'not authorized'; END IF;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- ps_owner_delete(p_token text, p_row_id uuid)
--   live: public.ps_owner_delete — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner delete for products/services. (Business / Space pages)
--   captured: pg_get_functiondef(ps_owner_delete) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.ps_owner_delete(p_token text, p_row_id uuid)
 RETURNS boolean
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_owner text;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  DELETE FROM public.products_services WHERE id = p_row_id AND owner_alias = v_owner;
  RETURN FOUND;
END $function$;

-- ---------------------------------------------------------------------------
-- ps_owner_upsert(p_token text, p_row_id uuid, p_page_kind text, p_page_alias text, p_kind text, p_name text, p_description text, p_cover_url text, p_price_cents integer, p_currency text, p_active boolean)
--   live: public.ps_owner_upsert — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner upsert for products/services. (Business / Space pages)
--   captured: pg_get_functiondef(ps_owner_upsert) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.ps_owner_upsert(p_token text, p_row_id uuid, p_page_kind text, p_page_alias text, p_kind text, p_name text, p_description text, p_cover_url text, p_price_cents integer, p_currency text, p_active boolean)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_owner text; v_id uuid;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  IF p_kind NOT IN ('product','service') THEN RAISE EXCEPTION 'bad kind'; END IF;
  IF p_row_id IS NULL THEN
    INSERT INTO public.products_services
      (page_kind, page_alias, owner_alias, kind, name, description, cover_url,
       price_cents, currency, active)
    VALUES (p_page_kind, p_page_alias, v_owner, p_kind, p_name, p_description,
            p_cover_url, COALESCE(p_price_cents,0), COALESCE(p_currency,'USD'),
            COALESCE(p_active,true))
    RETURNING id INTO v_id;
  ELSE
    UPDATE public.products_services SET
      kind = p_kind, name = COALESCE(p_name, name),
      description = COALESCE(p_description, description),
      cover_url = COALESCE(p_cover_url, cover_url),
      price_cents = COALESCE(p_price_cents, price_cents),
      currency = COALESCE(p_currency, currency),
      active = COALESCE(p_active, active), updated_at = now()
    WHERE id = p_row_id AND owner_alias = v_owner
    RETURNING id INTO v_id;
    IF NOT FOUND THEN RAISE EXCEPTION 'not authorized'; END IF;
  END IF;
  RETURN v_id;
END $function$;
