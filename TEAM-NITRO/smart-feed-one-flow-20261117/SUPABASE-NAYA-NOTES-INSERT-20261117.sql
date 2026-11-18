-- NAYA_NOTES INSERT — MEASURED STATE + IDEMPOTENT POLICY DEFINITION
-- Smart Feed / One Flow round, 2026-11-17. FILED, NOT APPLIED.
-- Applying any live database policy is Shawn's hand, always.
--
-- WHAT WAS MEASURED LIVE (2026-11-17 ~16:23Z, anon role, PostgREST):
--   POST /rest/v1/naya_notes {owner_alias:'flagship-personal', ...}
--     -> HTTP 201, row created, read back by id.
--     Row 1: id 9b88a7be-4a35-42f1-8edc-fe868bbe0d23, created 16:23:08Z
--     Row 2: id f44b3601-3c07-4b28-b56d-b2dc09dcd22a, created 16:23:18Z
--   DELETE /rest/v1/naya_notes?id=eq.<either row>
--     -> HTTP 401 {"code":"42501","message":"permission denied for table naya_notes",
--        "hint":"Grant the required privileges to the current role with:
--        GRANT DELETE ON public.naya_notes TO anon;"}
--   SELECT on naya_notes as anon returns rows (count 15 at the time).
--   The same anon role gets 42501 on nayanet_smart_ledger SELECT, so the
--   role in these receipts IS anon — the insert success is real, not a
--   service-key artifact.
--
-- CONCLUSION: the RLS 42501 refusal on naya_notes INSERT that the brief's
-- Break 3 records NO LONGER HOLDS. Anon INSERT is already permitted on the
-- live database (a permissive INSERT policy and/or GRANT INSERT already
-- exist — RLS state changed since the brief was written, exactly as the
-- brief warned it could). There is NO live 42501 INSERT receipt to file,
-- because the refusal does not happen anymore. This file therefore does
-- two things: (1) it records the policy definition that produces the
-- observed behavior, idempotently, so the permission is a named, reviewable
-- fact instead of a silent one; (2) it states the risk and the safer path.
-- DO NOT RUN THIS BLINDLY. If the policy already exists, the DO block is
-- a no-op. Running it changes nothing when the permission is already in
-- place — which the live receipts say it is.
--
-- WHAT IT OPENS — READ THIS BEFORE RUNNING:
-- A permissive anon INSERT (WITH CHECK (true)) lets anyone holding the
-- public key — which ships inside the app's own code, so anyone can find
-- it — insert a row into naya_notes as ANY owner_alias, with any title,
-- body, or category. That is impersonation + spam into every citizen's
-- personal notes list and, now that the Hub live read surfaces
-- category='Smart Note' rows, onto the public feed. The open door is the
-- same shape the notes table already has today for SELECT (anon reads all
-- rows), and the same shape hub_smart_notes already has for INSERT/SELECT/
-- UPDATE (per SUPABASE-HUB-SMART-NOTES-DELETE-GRANT-20261110.sql, the model
-- for this file). It is still a door, and opening it wider must be a
-- conscious choice, not a surprise.
--
-- THE SAFER PATH (recommended, already the composer's path):
-- The Personal composer does NOT use the direct insert. It POSTs to the
-- server save route (https://naya-save-staging.nayapower.workers.dev/api/
-- personal/save), which validated and saved the composer's acceptance note
-- live on 2026-11-17 (HTTP 200 in 0.90s, naya_note id
-- ef5e4184-c2d6-4c99-8f54-c0901e06a088). The direct anon insert is used
-- today only by the message-save paths (msgSaveNote / msgSaveSmart in the
-- Personal page bytes, lines 10123 and 10150). If the direct insert is ever
-- narrowed again, the composer keeps working through the server route.
-- The follow-on hardening is a scoped policy (WITH CHECK (owner_alias =
-- <the caller's own alias>)) once the page carries a real session — that
-- is a design decision for Shawn, not this round.
--
-- THE POLICY DEFINITION (idempotent — creates only if missing):
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE schemaname = 'public' AND tablename = 'naya_notes'
      AND policyname = 'naya_notes_insert_anon'
  ) THEN
    CREATE POLICY "naya_notes_insert_anon" ON public.naya_notes
      FOR INSERT TO anon WITH CHECK (true);
  END IF;
END $$;

GRANT INSERT ON public.naya_notes TO anon;

-- AFTER RUNNING (or after deciding not to), VERIFY in the SQL Editor:
--   SELECT policyname, cmd, roles, qual, with_check
--     FROM pg_policies
--     WHERE schemaname = 'public' AND tablename = 'naya_notes';
-- An INSERT policy for anon must be listed (or be confirmed pre-existing).
--   SELECT grantee, privilege_type FROM information_schema.role_table_grants
--     WHERE table_schema = 'public' AND table_name = 'naya_notes'
--     AND grantee = 'anon';
-- INSERT must be listed. DELETE must NOT be listed (anon DELETE is refused
-- live, 42501 — that refusal is load-bearing: it is why the two probe rows
-- below cannot be cleaned up by anon and need the service key).
--   -- The two probe rows this round created while re-proving the refusal
--   -- (they are real rows; delete under the service key when convenient):
--   --   9b88a7be-4a35-42f1-8edc-fe868bbe0d23 (2026-11-17T16:23:08Z)
--   --   f44b3601-3c07-4b28-b56d-b2dc09dcd22a (2026-11-17T16:23:18Z)
--   -- Both are titled 'ONE-FLOW VERIFICATION PROBE — maker seat 2026-11-17
--   -- (expected refusal)', owner_alias 'flagship-personal', category
--   -- 'Smart Note'. They render on the staged feed as honest artifacts.
--
-- Model: ~/workspace/team-nitro/SUPABASE-HUB-SMART-NOTES-DELETE-GRANT-20261110.sql
-- (same shape, different table and verb — NOT copied blindly: that file
-- grants DELETE on hub_smart_notes; this file defines INSERT on naya_notes,
-- and deliberately does NOT grant DELETE here.)
