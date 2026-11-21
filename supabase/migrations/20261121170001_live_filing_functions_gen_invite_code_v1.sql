-- Live filing: gen_invite_code() — filed early so 180000 invites.code DEFAULT resolves
-- Supabase filing round 2026-11-21, Seat 7 (FUNCTIONS). Branch: supabase/filing-20261121-functions.
-- Source: VERBATIM from the already-verified 190003 bytes
--   (supabase/migrations/20261121190003_live_filing_functions_membership_login_v1.sql,
--   blob 5228284d..., L290–L303) — copied, not re-typed; re-checked first-hand against
--   live pg_get_functiondef(public.gen_invite_code) 2026-11-21: byte-identical.
-- 190003 stays untouched: it re-defines gen_invite_code identically (idempotent).
-- Laws named: THE-NAYA-DESIGN-LAWS.md FIRST, then THE-PLAYBOOK.md,
--   DESIGN-INTELLIGENCE-REPORT.md, THE-ULTIMATE-ORIENTATION.md, THE-SET-ORIENTATION.md,
--   THE-ANATOMY-OF-A-SMART-APP-PAGE.md, THE-HEART-OF-THE-MACHINE.md, THE-OFFICIAL-PARTS.md,
--   THE-ARMY-TRAINING.md, the One-Build Law, the Eleven Laws, the Inventory Law.
-- Read-only against live: no live writes. Nothing deleted or dropped.

-- ---------------------------------------------------------------------------
-- gen_invite_code()
--   live: public.gen_invite_code — SECURITY INVOKER (default), language plpgsql, kind f, volatile v
--   purpose (DATABASE.md): Mint a new invite code. (Inviter)
--   captured: pg_get_functiondef(gen_invite_code) live, 2026-11-21
CREATE OR REPLACE FUNCTION public.gen_invite_code()
 RETURNS text
 LANGUAGE plpgsql
AS $function$
declare
  alphabet constant text := '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
  code text := '';
  i int;
begin
  for i in 1..8 loop
    code := code || substr(alphabet, (floor(random()*32))::int + 1, 1);
  end loop;
  return code;
end $function$;
