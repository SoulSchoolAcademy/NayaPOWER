-- Live filing: membership drip/lock RPCs (Academy paywall) — 2 functions
-- Supabase filing round 2026-11-21, Seat 2 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: LIVE definitions captured first-hand 2026-11-21 via Supabase Management API
--   POST /v1/projects/dahisasgpfvziswqvmvm/database/query — pg_get_functiondef / pg_get_triggerdef.
--   Read-only capture. No live writes were made. Definitions below are verbatim live
--   bytes (CREATE OR REPLACE FUNCTION as returned by pg_get_functiondef), grouped by
--   area; only this header and per-function provenance comments were added.
-- Priority first: member_content_for / member_content_locked_for are the Academy paywall reads.
-- NOTE (scope limit, stated honestly): a fresh-apply diff against a test database is
--   NOT in scope for this round (coordinator brief). These migrations assume the
--   live-only tables they read exist — Seat 1's table filings on the same filing
--   branch supply them; apply tables first on a fresh rebuild.
-- Inventory: DATABASE.md §(b) B1/B2 + §(c); INVENTORY.md §3.2 / §3.4 (64 riders).

-- ---------------------------------------------------------------------------
-- member_content_for(p_membership_id uuid, p_token text)
--   live: public.member_content_for — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): The content this member may see — drip/published rules applied. (Membership / Academy paywall)
--   captured: pg_get_functiondef(member_content_for) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.member_content_for(p_membership_id uuid, p_token text)
 RETURNS SETOF membership_content
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT c.* FROM public.membership_content c
  LEFT JOIN public.membership_members m
    ON m.membership_id = c.membership_id
   AND m.member_alias = public.member_alias_for(p_membership_id, p_token)
   AND public.member_alias_for(p_membership_id, p_token) <> ''
  WHERE c.membership_id = p_membership_id
    AND c.published = true
    AND (
      public.is_membership_owner(p_membership_id, p_token)
      OR (
        m.member_alias IS NOT NULL
        AND m.status = 'active'
        AND (m.expires_at IS NULL OR m.expires_at > now())
        AND (c.drip_days IS NULL OR c.drip_days <= (now()::date - m.joined_at::date))
      )
    )
  ORDER BY c.position
$function$;

-- ---------------------------------------------------------------------------
-- member_content_locked_for(p_membership_id uuid, p_token text)
--   live: public.member_content_locked_for — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): The content still locked for this member — what's behind the drip. (Membership / Academy paywall)
--   captured: pg_get_functiondef(member_content_locked_for) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.member_content_locked_for(p_membership_id uuid, p_token text)
 RETURNS TABLE(id uuid, kind text, title text, drip_days integer, unlocks_at timestamp with time zone)
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT c.id, c.kind, c.title, c.drip_days,
         (m.joined_at + (c.drip_days || ' days')::interval) AS unlocks_at
  FROM public.membership_content c
  JOIN public.membership_members m
    ON m.membership_id = c.membership_id
   AND m.member_alias = public.member_alias_for(p_membership_id, p_token)
   AND public.member_alias_for(p_membership_id, p_token) <> ''
  WHERE c.membership_id = p_membership_id
    AND c.published = true
    AND m.status = 'active'
    AND (m.expires_at IS NULL OR m.expires_at > now())
    AND c.drip_days IS NOT NULL
    AND c.drip_days > (now()::date - m.joined_at::date)
  ORDER BY c.position
$function$;
