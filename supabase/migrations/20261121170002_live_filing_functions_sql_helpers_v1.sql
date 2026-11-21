-- Live filing: SQL-language helper functions, filed early so the LANGUAGE-sql
--   callers in 190000–190002 resolve on a fresh apply (Seat 8, Supabase filing
--   2026-11-21). Branch: supabase/filing-20261121-functions.
--
-- FINAL-CHECKER-VERDICT gap: six LANGUAGE-sql functions call functions not yet
--   defined at their creation point (11 call sites, 190000–190002). SQL-language
--   bodies are parsed and resolved at CREATE time, so on a strict fresh apply the
--   chain halted at 190000 member_content_for (42883) and ended at 9/11 triggers.
--   This file defines the four callees EARLY, VERBATIM from the already-verified
--   190001 / 190003 bytes (provenance comment + CREATE block copied, not re-typed;
--   each re-checked first-hand against live pg_get_functiondef 2026-11-21:
--   byte-identical, sole delta the trailing statement terminator).
--   _mship_hash        <- 190001 L211–L223
--   member_alias_for   <- 190001 L112–L136
--   owner_alias_for    <- 190003 L342–L361
--   is_membership_owner <- 190001 L41–L58
-- Order inside this file is dependency order: _mship_hash first (member_alias_for
--   and owner_alias_for call it), owner_alias_for before is_membership_owner
--   (is_membership_owner calls it). No forward reference remains inside 170002,
--   and 170002 sorts before 190000, so every sql caller below resolves.
-- 190000–190003 stay untouched: they re-define these four functions identically
--   (idempotent CREATE OR REPLACE). The eight plpgsql callers of the same later
--   functions are NOT breaks (plpgsql resolves at execution) and are untouched.
-- Laws named: THE-NAYA-DESIGN-LAWS.md FIRST, then THE-PLAYBOOK.md,
--   DESIGN-INTELLIGENCE-REPORT.md, THE-ULTIMATE-ORIENTATION.md, THE-SET-ORIENTATION.md,
--   THE-ANATOMY-OF-A-SMART-APP-PAGE.md, THE-HEART-OF-THE-MACHINE.md, THE-OFFICIAL-PARTS.md,
--   THE-ARMY-TRAINING.md, the One-Build Law, the Eleven Laws, the Inventory Law.
-- Read-only against live: no live writes. Nothing deleted or dropped.
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
-- owner_alias_for(p_token text)
--   live: public.owner_alias_for — SECURITY DEFINER, language sql, kind f, volatile s
--   purpose (DATABASE.md): Resolve the owner alias for a token/session. (Identity)
--   captured: pg_get_functiondef(owner_alias_for) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.owner_alias_for(p_token text)
 RETURNS text
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
  SELECT COALESCE((
    SELECT s.alias FROM public.member_sessions s
    WHERE s.kind = 'owner'
      AND s.token_hash = public._mship_hash(p_token)
      AND s.revoked_at IS NULL
      AND s.expires_at > now()
    LIMIT 1
  ), '')
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
