-- Live filing: membership core RPCs — 10 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- Membership identity, join, content owner writes, tier.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- is_active_member(p_membership_id uuid, p_token text)
--   live: public.is_active_member — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Is this session token an active member of this membership? (Membership)
--   captured: pg_get_functiondef(is_active_member) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.is_active_member(p_membership_id uuid, p_token text)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT EXISTS (
    SELECT 1
    FROM public.member_sessions s
    JOIN public.membership_members m
      ON m.membership_id = s.membership_id AND m.member_alias = s.alias
    WHERE s.kind = 'member'
      AND s.membership_id = p_membership_id
      AND s.token_hash = public._mship_hash(p_token)
      AND s.revoked_at IS NULL
      AND s.expires_at > now()
      AND m.status = 'active'
      AND (m.expires_at IS NULL OR m.expires_at > now())
  )
$function$;

-- ---------------------------------------------------------------------------
-- is_membership_owner(p_membership_id uuid, p_token text)
--   live: public.is_membership_owner — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Does this token belong to the membership owner? (Membership)
--   captured: pg_get_functiondef(is_membership_owner) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.is_membership_owner(p_membership_id uuid, p_token text)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT EXISTS (
    SELECT 1 FROM public.memberships m
    WHERE m.id = p_membership_id
      AND m.owner_alias = public.owner_alias_for(p_token)
      AND public.owner_alias_for(p_token) <> ''
  )
$function$;

-- ---------------------------------------------------------------------------
-- is_owner_session(p_token text)
--   live: public.is_owner_session — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Is this token an owner session at all? (Membership)
--   captured: pg_get_functiondef(is_owner_session) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.is_owner_session(p_token text)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT EXISTS (
    SELECT 1 FROM public.member_sessions s
    WHERE s.kind = 'owner'
      AND s.token_hash = public._mship_hash(p_token)
      AND s.revoked_at IS NULL
      AND s.expires_at > now()
  )
$function$;

-- ---------------------------------------------------------------------------
-- join_free_membership(p_membership_id uuid, p_alias text, p_email_hash text)
--   live: public.join_free_membership — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Join a free membership; returns the membership-member id. (Membership)
--   captured: pg_get_functiondef(join_free_membership) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.join_free_membership(p_membership_id uuid, p_alias text, p_email_hash text)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE v_id uuid;
BEGIN
  IF p_alias IS NULL OR p_alias = '' THEN RAISE EXCEPTION 'alias required'; END IF;
  SELECT m.id INTO v_id FROM public.memberships m
  WHERE m.id = p_membership_id AND m.active = true AND m.access_type = 'free';
  IF NOT FOUND THEN RAISE EXCEPTION 'membership not open for free join'; END IF;
  INSERT INTO public.membership_members (membership_id, member_alias, status)
  VALUES (p_membership_id, p_alias, 'active')
  ON CONFLICT (membership_id, member_alias) DO UPDATE
    SET status = 'active', updated_at = now()
    WHERE public.membership_members.status <> 'active';
  IF p_email_hash IS NOT NULL AND p_email_hash <> '' THEN
    INSERT INTO public.membership_member_emails (membership_id, member_alias, email_hash)
    VALUES (p_membership_id, p_alias, p_email_hash)
    ON CONFLICT (membership_id, member_alias) DO UPDATE SET email_hash = EXCLUDED.email_hash;
  END IF;
  SELECT id INTO v_id FROM public.membership_members
  WHERE membership_id = p_membership_id AND member_alias = p_alias;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- member_alias_for(p_membership_id uuid, p_token text)
--   live: public.member_alias_for — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Which member alias does this token stand for in this membership? (Membership)
--   captured: pg_get_functiondef(member_alias_for) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.member_alias_for(p_membership_id uuid, p_token text)
 RETURNS text
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT COALESCE((
    SELECT s.alias FROM public.member_sessions s
    JOIN public.membership_members m
      ON m.membership_id = s.membership_id AND m.member_alias = s.alias
    WHERE s.kind = 'member'
      AND s.membership_id = p_membership_id
      AND s.token_hash = public._mship_hash(p_token)
      AND s.revoked_at IS NULL
      AND s.expires_at > now()
      AND m.status = 'active'
      AND (m.expires_at IS NULL OR m.expires_at > now())
    LIMIT 1
  ), '')
$function$;

-- ---------------------------------------------------------------------------
-- membership_member_count(p_membership_id uuid)
--   live: public.membership_member_count — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): How many members does this membership have? (Membership)
--   captured: pg_get_functiondef(membership_member_count) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.membership_member_count(p_membership_id uuid)
 RETURNS integer
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT COUNT(*)::integer FROM public.membership_members
  WHERE membership_id = p_membership_id AND status = 'active'
$function$;

-- ---------------------------------------------------------------------------
-- mship_content_delete(p_token text, p_membership_id uuid, p_content_id uuid)
--   live: public.mship_content_delete — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner deletes a piece of membership content. (Membership owner)
--   captured: pg_get_functiondef(mship_content_delete) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_content_delete(p_token text, p_membership_id uuid, p_content_id uuid)
 RETURNS boolean
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
BEGIN
  IF NOT public.is_membership_owner(p_membership_id, p_token) THEN
    RAISE EXCEPTION 'not authorized';
  END IF;
  DELETE FROM public.membership_content WHERE id = p_content_id AND membership_id = p_membership_id;
  RETURN FOUND;
END $function$;

-- ---------------------------------------------------------------------------
-- mship_content_upsert(p_token text, p_membership_id uuid, p_content_id uuid, p_kind text, p_title text, p_description text, p_media_url text, p_thumbnail_url text, p_duration_seconds integer, p_position integer, p_drip_days integer, p_published boolean)
--   live: public.mship_content_upsert — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Owner creates/updates a piece of membership content. (Membership owner)
--   captured: pg_get_functiondef(mship_content_upsert) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.mship_content_upsert(p_token text, p_membership_id uuid, p_content_id uuid, p_kind text, p_title text, p_description text, p_media_url text, p_thumbnail_url text, p_duration_seconds integer, p_position integer, p_drip_days integer, p_published boolean)
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
  IF p_kind NOT IN ('video','pdf','audio','note','link') THEN RAISE EXCEPTION 'bad kind'; END IF;
  IF p_content_id IS NULL THEN
    INSERT INTO public.membership_content
      (membership_id, kind, title, description, media_url, thumbnail_url,
       duration_seconds, position, drip_days, published)
    VALUES (p_membership_id, p_kind, p_title, p_description, p_media_url,
            p_thumbnail_url, p_duration_seconds, COALESCE(p_position,0),
            p_drip_days, COALESCE(p_published,true))
    RETURNING id INTO v_id;
  ELSE
    UPDATE public.membership_content SET
      kind = p_kind, title = p_title, description = p_description,
      media_url = p_media_url, thumbnail_url = p_thumbnail_url,
      duration_seconds = p_duration_seconds, position = COALESCE(p_position, position),
      drip_days = p_drip_days, published = COALESCE(p_published, published),
      updated_at = now()
    WHERE id = p_content_id AND membership_id = p_membership_id
    RETURNING id INTO v_id;
    IF NOT FOUND THEN RAISE EXCEPTION 'content not found'; END IF;
  END IF;
  RETURN v_id;
END $function$;

-- ---------------------------------------------------------------------------
-- _mship_hash(p_token text)
--   live: public._mship_hash — SECURITY DEFINER, language sql, kind f, volatile i
--   purpose (DATABASE.md): Hash a membership token (internal helper; _ prefix marks it private). (Membership)
--   captured: pg_get_functiondef(_mship_hash) live, 2026-11-21
CREATE OR REPLACE FUNCTION public._mship_hash(p_token text)
 RETURNS text
 LANGUAGE sql
 IMMUTABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT encode(extensions.digest(p_token, 'sha256'), 'hex')
$function$;

-- ---------------------------------------------------------------------------
-- citizen_tier(p_alias text)
--   live: public.citizen_tier — SECURITY DEFINER, language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Which tier is this citizen (Power / Pro / Max / free)? (Membership tiers)
--   captured: pg_get_functiondef(citizen_tier) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.citizen_tier(p_alias text)
 RETURNS text
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
BEGIN
  RETURN COALESCE(
    (SELECT tier FROM public.citizen_tiers WHERE alias = p_alias),
    'free'
  );
END;
$function$;
