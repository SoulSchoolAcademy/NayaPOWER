-- Let the notes sync delete tombstoned notes — Supabase master first pass, 2026-11-10.
-- Prepared for Shawn's hand in the Supabase SQL Editor (production database).
-- Paste the whole file, run it, done. No app code changes needed.
--
-- WHAT THIS DOES, IN PLAIN WORDS:
-- When a Smart Note file is deleted on GitHub, the sync is supposed to
-- delete its row from hub_smart_notes too. Today it cannot: the public
-- key holds INSERT, SELECT, and UPDATE on that table but no DELETE, and
-- no DELETE rule exists. The sync log says so itself, and the audit
-- re-proved it live. So deleted notes stay in the table forever and the
-- feed only hides the card. This file gives the public key DELETE and
-- adds the DELETE rule, so the sync's tombstone pass can actually remove
-- rows. That unblocks the dedupe too: the 32 doubled note numbers and
-- the 26 doubled titles (measured live 2026-11-10, see the first-pass
-- report) cannot be cleaned until this lands.
--
-- WHAT IT OPENS — READ THIS BEFORE RUNNING:
-- This hands DELETE on the live notes table to anyone holding the public
-- key — and the public key ships inside the app's own code, so anyone
-- can find it. With this rule in place, a stranger with the key could
-- delete any note row, not just tombstoned ones. That is the same shape
-- of openness the notes table already has for INSERT and UPDATE today
-- (its rules pass everything), so this file does not open a new kind of
-- door — but it does widen the one that is already open, and that must
-- be a conscious choice, not a surprise.
--
-- THE SAFER ALTERNATIVE (recommended):
-- Run the cleanup under the service key instead, which bypasses the
-- row rules entirely. The dedupe file
-- (SUPABASE-DEDUP-HUB-SMART-NOTES-20261110.sql) is written so it runs
-- as-is under the service key with NO grant needed. If the dedupe is
-- done that way, this grant is only needed if the anon-key sync script
-- itself must delete tombstoned rows going forward. If the sync is ever
-- moved to the service key, this grant can be revoked again and nothing
-- is lost.
--
-- IF YOU RUN THIS FILE, the sync's tombstone pass starts working on the
-- next sync. If you do NOT run it, run the dedupe under the service key
-- and leave this file unrun.

GRANT DELETE ON public.hub_smart_notes TO anon;

DROP POLICY IF EXISTS "hub_smart_notes_delete_all" ON public.hub_smart_notes;
CREATE POLICY "hub_smart_notes_delete_all" ON public.hub_smart_notes
  FOR DELETE TO anon USING (true);

-- AFTER RUNNING, VERIFY (same SQL Editor, run these and check):
--   SELECT grantee, privilege_type FROM information_schema.role_table_grants
--     WHERE table_schema = 'public' AND table_name = 'hub_smart_notes'
--     AND grantee = 'anon';
-- DELETE must now be listed alongside INSERT, SELECT, UPDATE.
--   SELECT policyname, cmd FROM pg_policies
--     WHERE schemaname = 'public' AND tablename = 'hub_smart_notes';
-- A DELETE policy must now be listed.
-- Then watch one sync: a note deleted on GitHub should leave the table
-- (its row count drops), not just hide from the feed.
