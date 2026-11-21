-- Live filing: membership owner RPCs — 10 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- Owner-side membership management + member thread read.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- mship_invite_create(p_token text, p_membership_id uuid, p_code text, p_max_uses integer, p_expires_at timestamp with time zone)
--   live: public.mship_invite_create — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner creates a membership invite. (Membership)
--   captured: pg_get_functiondef(mship_invite_create) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_invite_create(p_token text, p_membership_id uuid, p_code text, p_max_uses integer, p_expires_at timestamp with time zone)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_id uuid;
BEGIN
  IF NOT public.is_membership_owner(p_membership_id, p_token) THEN
    RAISE EXCEPTION 'not authorized';
  END IF;
  IF p_code IS NULL OR length(p_code) < 16 THEN
    RAISE EXCEPTION 'invite code must be >= 128 bits (16+ chars from a CSPRNG)';
  END IF;
  INSERT INTO public.membership_invites
    (membership_id, code_hash, max_uses, expires_at, created_by_alias)
  VALUES (p_membership_id, public._mship_hash(p_code),
          COALESCE(p_max_uses,1), p_expires_at, public.owner_alias_for(p_token))
  RETURNING id INTO v_id;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- mship_member_set_status(p_token text, p_membership_id uuid, p_member_alias text, p_status text)
--   live: public.mship_member_set_status — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner sets a member's status. (Membership)
--   captured: pg_get_functiondef(mship_member_set_status) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_member_set_status(p_token text, p_membership_id uuid, p_member_alias text, p_status text)
 RETURNS boolean
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
BEGIN
  IF NOT public.is_membership_owner(p_membership_id, p_token) THEN
    RAISE EXCEPTION 'not authorized';
  END IF;
  IF p_status NOT IN ('active','pending','cancelled','expired') THEN
    RAISE EXCEPTION 'bad status';
  END IF;
  UPDATE public.membership_members SET status = p_status, updated_at = now()
  WHERE membership_id = p_membership_id AND member_alias = p_member_alias;
  RETURN FOUND;
END $function$;

-- ---------------------------------------------------------------------------
-- mship_owner_content(p_token text, p_membership_id uuid)
--   live: public.mship_owner_content — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Owner reads their membership's content (owner view). (Membership)
--   captured: pg_get_functiondef(mship_owner_content) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_owner_content(p_token text, p_membership_id uuid)
 RETURNS SETOF membership_content
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT c.* FROM public.membership_content c
  WHERE c.membership_id = p_membership_id
    AND public.is_membership_owner(p_membership_id, p_token)
  ORDER BY c.position
$function$;

-- ---------------------------------------------------------------------------
-- mship_owner_create(p_token text, p_page_kind text, p_page_alias text, p_name text, p_slug text, p_description text, p_cover_url text, p_access_type text, p_price_cents integer, p_currency text)
--   live: public.mship_owner_create — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner creates a membership. (Membership)
--   captured: pg_get_functiondef(mship_owner_create) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_owner_create(p_token text, p_page_kind text, p_page_alias text, p_name text, p_slug text, p_description text, p_cover_url text, p_access_type text, p_price_cents integer, p_currency text)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_owner text; v_id uuid;
BEGIN
  v_owner := public.owner_alias_for(p_token);
  IF v_owner = '' THEN RAISE EXCEPTION 'not authorized'; END IF;
  IF p_access_type NOT IN ('free','paid','invite') THEN RAISE EXCEPTION 'bad access_type'; END IF;
  INSERT INTO public.memberships
    (page_kind, page_alias, owner_alias, name, slug, description, cover_url,
     access_type, price_cents, currency)
  VALUES (p_page_kind, p_page_alias, v_owner, p_name, p_slug, p_description,
          p_cover_url, p_access_type, COALESCE(p_price_cents,0), COALESCE(p_currency,'USD'))
  RETURNING id INTO v_id;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- mship_owner_delete(p_token text, p_membership_id uuid)
--   live: public.mship_owner_delete — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner deletes a membership. (Membership)
--   captured: pg_get_functiondef(mship_owner_delete) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_owner_delete(p_token text, p_membership_id uuid)
 RETURNS boolean
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
BEGIN
  IF NOT public.is_membership_owner(p_membership_id, p_token) THEN
    RAISE EXCEPTION 'not authorized';
  END IF;
  DELETE FROM public.memberships WHERE id = p_membership_id;
  RETURN FOUND;
END $function$;

-- ---------------------------------------------------------------------------
-- mship_owner_members(p_token text, p_membership_id uuid)
--   live: public.mship_owner_members — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Owner lists a membership's members. (Membership)
--   captured: pg_get_functiondef(mship_owner_members) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_owner_members(p_token text, p_membership_id uuid)
 RETURNS TABLE(member_alias text, status text, joined_at timestamp with time zone, expires_at timestamp with time zone, last_login_at timestamp with time zone)
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT m.member_alias, m.status, m.joined_at, m.expires_at, m.last_login_at
  FROM public.membership_members m
  WHERE m.membership_id = p_membership_id
    AND public.is_membership_owner(p_membership_id, p_token)
  ORDER BY m.joined_at DESC
$function$;

-- ---------------------------------------------------------------------------
-- mship_owner_tier(p_token text)
--   live: public.mship_owner_tier — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner's tier for a membership (what the tier allows). (Membership tiers)
--   captured: pg_get_functiondef(mship_owner_tier) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_owner_tier(p_token text)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_alias text;
BEGIN
  v_alias := public.owner_alias_for(p_token);
  IF v_alias IS NULL OR v_alias = '' THEN
    RETURN 'free';
  END IF;
  RETURN public.citizen_tier(v_alias);
END;
$function$;

-- ---------------------------------------------------------------------------
-- mship_owner_update(p_token text, p_membership_id uuid, p_name text, p_description text, p_cover_url text, p_price_cents integer, p_active boolean)
--   live: public.mship_owner_update — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner updates a membership. (Membership)
--   captured: pg_get_functiondef(mship_owner_update) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_owner_update(p_token text, p_membership_id uuid, p_name text, p_description text, p_cover_url text, p_price_cents integer, p_active boolean)
 RETURNS boolean
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
BEGIN
  IF NOT public.is_membership_owner(p_membership_id, p_token) THEN
    RAISE EXCEPTION 'not authorized';
  END IF;
  UPDATE public.memberships SET
    name = COALESCE(p_name, name),
    description = COALESCE(p_description, description),
    cover_url = COALESCE(p_cover_url, cover_url),
    price_cents = COALESCE(p_price_cents, price_cents),
    active = COALESCE(p_active, active),
    updated_at = now()
  WHERE id = p_membership_id;
  RETURN FOUND;
END $function$;

-- ---------------------------------------------------------------------------
-- mship_read_thread(p_token text, p_thread_id uuid, p_limit integer)
--   live: public.mship_read_thread — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Read a membership's message thread. (Membership messages)
--   captured: pg_get_functiondef(mship_read_thread) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_read_thread(p_token text, p_thread_id uuid, p_limit integer)
 RETURNS SETOF messenger_messages
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  WITH who AS (
    SELECT public.owner_alias_for(p_token) AS a
  ), me AS (
    SELECT CASE WHEN (SELECT a FROM who) <> ''
                THEN (SELECT a FROM who)
                ELSE (SELECT s.alias FROM public.member_sessions s
                      WHERE s.token_hash = public._mship_hash(p_token)
                        AND s.revoked_at IS NULL AND s.expires_at > now() LIMIT 1)
           END AS a
  )
  SELECT m.* FROM public.messenger_messages m, me
  WHERE m.thread_id = p_thread_id
    AND me.a IS NOT NULL AND me.a <> ''
    AND (m.from_alias = me.a OR m.to_alias = me.a)
  ORDER BY m.sent_at DESC
  LIMIT LEAST(COALESCE(p_limit, 50), 200)
$function$;

-- ---------------------------------------------------------------------------
-- my_membership_row(p_membership_id uuid, p_token text)
--   live: public.my_membership_row — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): The caller's own membership row (who am I here?). (Membership)
--   captured: pg_get_functiondef(my_membership_row) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.my_membership_row(p_membership_id uuid, p_token text)
 RETURNS SETOF membership_members
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT m.* FROM public.membership_members m
  WHERE m.membership_id = p_membership_id
    AND m.member_alias = public.member_alias_for(p_membership_id, p_token)
    AND public.member_alias_for(p_membership_id, p_token) <> ''
$function$;
