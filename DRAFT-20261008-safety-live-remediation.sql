-- ============================================================================
-- DRAFT — NOT A LIVE MIGRATION — DO NOT APPLY WITHOUT SHAWN'S EXPLICIT WORD
-- ============================================================================
-- Safety 27-warning follow-through: live remediation for the 2026-10-08
-- verified findings. Prepared by Naya 5 (safety seat) as the decision
-- vehicle for Shawn's security decision (per Naya 1, 2026-10-08: the 3
-- tables are NOT auto-fixed — live capture-path dependency must be ruled
-- on by Shawn first).
--
-- LIVE EVIDENCE (read-only, 2026-10-08, via Management API):
--   - smart_note_events / smart_note_artifacts / smart_note_receipts:
--       RLS DISABLED, ACL anon=arwdDxtm (anon has FULL read/write/delete).
--       Advisor: 3x ERROR rls_disabled_in_public.
--   - v7_create_smart_note(...): live ACL includes anon + PUBLIC EXECUTE.
--       Fail-closed inside the function (raises without JWT bound to
--       p_user_id), residual risk LOW.
--   - verify_smart_note(uuid): live ACL includes anon + PUBLIC EXECUTE.
--       SECURITY DEFINER, WRITES with NO auth check — anon can flip event
--       VERIFIED/INCOMPLETE and mint verification receipts. Residual MEDIUM.
--   - service_role bypasses RLS and is unaffected by every statement below.
--
-- WHAT THIS DRAFT DOES (mirrors repo intent already merged on main):
--   §1  Apply the owner policies from 20260906143937 (never applied live)
--       BEFORE enabling RLS — enabling RLS with no policies = deny-all.
--   §2  Enable RLS on the 3 tables (repo intent, 20260906143937).
--   §3  Revoke anon/authenticated table grants (repo intent, 20260906082117).
--   §4  Revoke anon EXECUTE on the 2 functions (repo intent, 20260906082117,
--       20260906082129). verify_smart_note is called internally by
--       v7_create_smart_note — internal calls are unaffected by EXECUTE
--       revocation; only direct REST callers lose access.
--
-- RISK NOTE (why this needs Shawn, not auto-fix):
--   If any live client calls verify_smart_note or the tables directly with
--   the anon key (rather than via service_role edge functions), it breaks.
--   Live capture was proven working 2026-10-08 (event acc612d5); the capture
--   path must be confirmed service_role-routed before applying.
--
-- TO AUTHORIZE: Shawn replies with explicit word; Naya 4 (or Naya 5 via
-- approved path) renames this into supabase/migrations/ with a timestamp
-- and it rides the deploy pipeline (deploy auth also Shawn's).
-- ============================================================================

-- §1: owner policies first (repo: 20260906143937_secure_canonical_smart_note_rls_owner_policies.sql)
DROP POLICY IF EXISTS smart_note_events_owner ON public.smart_note_events;
CREATE POLICY smart_note_events_owner ON public.smart_note_events FOR ALL TO authenticated USING (member_id = auth.uid()) WITH CHECK (member_id = auth.uid());
DROP POLICY IF EXISTS smart_note_artifacts_owner ON public.smart_note_artifacts;
CREATE POLICY smart_note_artifacts_owner ON public.smart_note_artifacts FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.smart_note_events e WHERE e.id = smart_note_artifacts.event_id AND e.member_id = auth.uid())) WITH CHECK (EXISTS (SELECT 1 FROM public.smart_note_events e WHERE e.id = smart_note_artifacts.event_id AND e.member_id = auth.uid()));
DROP POLICY IF EXISTS smart_note_receipts_owner ON public.smart_note_receipts;
CREATE POLICY smart_note_receipts_owner ON public.smart_note_receipts FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.smart_note_events e WHERE e.id = smart_note_receipts.event_id AND e.member_id = auth.uid())) WITH CHECK (EXISTS (SELECT 1 FROM public.smart_note_events e WHERE e.id = smart_note_receipts.event_id AND e.member_id = auth.uid()));

-- §2: enable RLS (policies now exist, so this cannot lock out owners)
ALTER TABLE public.smart_note_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.smart_note_artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.smart_note_receipts ENABLE ROW LEVEL SECURITY;

-- §3: revoke direct table grants (repo: 20260906082117_harden_smart_note_api_and_verifier.sql)
REVOKE ALL ON TABLE public.smart_note_events FROM anon, authenticated;
REVOKE ALL ON TABLE public.smart_note_artifacts FROM anon, authenticated;
REVOKE ALL ON TABLE public.smart_note_receipts FROM anon, authenticated;

-- §4: revoke anon EXECUTE on the two functions (repo: 20260906082117, 20260906082129)
REVOKE EXECUTE ON FUNCTION public.verify_smart_note(uuid) FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.v7_create_smart_note(text, uuid, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb) FROM anon, public;
REVOKE EXECUTE ON FUNCTION public.v7_create_smart_note(text, uuid, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, text) FROM anon, public;

-- NOT in this draft (dashboard toggles, need Shawn's click, cannot be SQL):
--   - disable anonymous sign-ins (auth config; 18x advisor WARN)
--   - enable leaked-password protection (auth config; 1x advisor WARN)
