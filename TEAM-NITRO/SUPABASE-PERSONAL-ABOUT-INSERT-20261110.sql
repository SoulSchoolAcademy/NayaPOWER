-- Let the Personal About save land again — Personal fix-7, 2026-11-10.
-- Prepared for Shawn's hand in the Supabase SQL Editor (production database).
-- Paste the whole file, run it, done. No app code changes needed.
-- Nothing in this file has been run. Read the header first.
--
-- WHAT IS WRONG, IN PLAIN WORDS:
-- Saving the About story or motto on the Personal page writes the words
-- onto the device (that half works — a reload keeps them), then tries to
-- write the app's own copy as a row in smart_notes. That row write fails:
-- the app answers 42501, "permission denied for table
-- naya_category_prototypes", and suggests granting SELECT on that table
-- to anon. The page says so honestly in its status line instead of
-- pretending the save landed. The cross-device copy — the words following
-- you to another device — is the half that is broken.
--
-- WHAT IS PROVEN (measured, not guessed):
-- 1. The failure is real and repeatable: two real saves through the page
--    (story, then motto) both answered 401 / 42501 naming
--    naya_category_prototypes. The page's own read of smart_notes still
--    works; only the write fails, and only on that table's name.
-- 2. The same writes WORKED on Nov 9 (00:47-00:50Z): the live rows for the
--    motto, goals, vision, mission and purpose are all there. They broke
--    after the lock ran at 02:40Z on Nov 10.
-- 3. The lock changed only six tables (RLS on + REVOKE ALL FROM anon):
--    seat_keys, ambassador_links, naya_category_prototypes,
--    naya_note_filing, ambassador_events, seat_lane_mapping. Nothing else
--    in the database was touched by it.
-- 4. The page's own reads also touch the lock: the Notes and Q&A loaders
--    read smart_notes WITH the filing record joined in
--    (naya_note_filing, category_name + match_score). A read-only probe
--    just now returns 42501 "permission denied for table
--    naya_note_filing" on that joined read. So the lock broke the page's
--    read path too, not only its write path.
-- 5. The code that reads the prototypes table is NOT in the repo: zero
--    references to naya_category_prototypes in the whole repo clone. It
--    lives only in the live database, so it cannot be named from outside.
--
-- WHAT IS INFERRED (honest, not proven):
-- The reader is almost certainly a trigger on smart_notes — or a
-- write-rule function on it — that sorts each new note into a category
-- using the 12 prototypes and files the result into naya_note_filing
-- (which is why the filing rows carry category_name and match_score).
-- It runs as the anon key, so the moment the lock took anon's SELECT
-- away, the first read inside the trigger failed and the whole insert
-- failed with it. Step 0 below names the reader exactly; run it first
-- and read the names before deciding anything else.
--
-- THE FIX, IN PLAIN WORDS:
-- Give back ONE narrow read rule on each of the two tables the page
-- provably needs to read — and nothing else. The prototypes table gets
-- SELECT only (the trigger's category lookup). The filing table gets
-- SELECT only (the page's joined read). Writes stay locked on both:
-- no INSERT, no UPDATE, no DELETE grants, no write rules. A stranger
-- with the public key can read the 12 category prototypes and the
-- filing records — the page already shows the category names in the
-- open — but cannot write, change, or delete a single row in either.
-- This is the lock file's own rule: "If a page ever needs to read one
-- of them, add back ONE narrow read rule for that table only — never
-- the writes."
--
-- STEP 0 — NAME THE READER FIRST (read-only, safe, run these first):
-- These three queries only look. They tell you the trigger's name, the
-- function that reads the prototypes, and whether it runs as its owner
-- (security_definer = true) or as the anon key (false).

SELECT event_object_table AS table_name, trigger_name, event_manipulation,
       action_statement
FROM information_schema.triggers
WHERE event_object_schema = 'public'
  AND event_object_table IN ('smart_notes', 'naya_note_filing');

SELECT n.nspname AS schema_name, p.proname AS function_name,
       p.prosecdef AS runs_as_owner
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname = 'public'
  AND p.prosrc ILIKE '%naya_category_prototypes%';

SELECT policyname, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' AND tablename = 'smart_notes';

-- STEP 1 — THE NARROW FIX (run this; it is the whole fix if the re-test passes):
-- SELECT-only on the two tables. Re-runnable: the DROP lines make a
-- second run a no-op instead of an error.

GRANT SELECT ON public.naya_category_prototypes TO anon;
DROP POLICY IF EXISTS "naya_category_prototypes_select_anon" ON public.naya_category_prototypes;
CREATE POLICY "naya_category_prototypes_select_anon" ON public.naya_category_prototypes
  FOR SELECT TO anon USING (true);

GRANT SELECT ON public.naya_note_filing TO anon;
DROP POLICY IF EXISTS "naya_note_filing_select_anon" ON public.naya_note_filing;
CREATE POLICY "naya_note_filing_select_anon" ON public.naya_note_filing
  FOR SELECT TO anon USING (true);

-- AFTER RUNNING STEP 1, VERIFY (same SQL Editor, run these and check):
--   SELECT policyname, cmd FROM pg_policies
--     WHERE schemaname = 'public'
--     AND tablename IN ('naya_category_prototypes', 'naya_note_filing');
-- Two SELECT policies must now be listed, one per table, and nothing else.
--   SELECT grantee, privilege_type FROM information_schema.role_table_grants
--     WHERE table_schema = 'public'
--     AND table_name IN ('naya_category_prototypes', 'naya_note_filing')
--     AND grantee = 'anon';
-- SELECT only, on both tables. If any INSERT, UPDATE or DELETE row shows
-- up here, stop — something else changed the grants.
-- Then re-test from the page: open the Personal About, edit the story,
-- save. The status line must read "Saved — it is this app's own data
-- now." (not the "could not be written" line), and one new smart_notes
-- row with {"k":"about"} must exist for owner flagship-personal. Also
-- re-load the Notes section: the joined read must return rows instead
-- of 42501.
--
-- STEP 2 — ONLY IF THE SAVE RE-TEST STILL FAILS (do not run blind):
-- If the save still answers 42501 after Step 1, read the table it names
-- this time. If it names naya_note_filing, the trigger's filing write
-- is the next denial: the trigger writes the filing row as anon, and
-- anon still holds no INSERT there. Two ways through, in order:
-- (A) PREFERRED, if Step 0 named the trigger function: let the trigger
--     run as its owner instead of as anon, so no grant widens at all.
--     Replace <function_name> with the name Step 0 returned, and run:
--       ALTER FUNCTION public.<function_name> SECURITY DEFINER;
--     Then re-test the save. Nothing else changes; the lock stays whole.
-- (B) ONLY IF (A) does not apply (no function was named, or the reader
--     is a write rule rather than a trigger function): grant the filing
--     write narrowly. WARNING, IN PLAIN WORDS: this lets ANYONE holding
--     the public key insert filing rows — fake filing records, wrong
--     categories, anything. The public key ships inside the app's own
--     code, so anyone can find it. The page already lets the public key
--     insert smart_notes rows, so this widens a door that is already
--     open — but it must be a conscious choice. Run (B) only if you
--     accept that trade.
--       GRANT INSERT ON public.naya_note_filing TO anon;
--       DROP POLICY IF EXISTS "naya_note_filing_insert_anon" ON public.naya_note_filing;
--       CREATE POLICY "naya_note_filing_insert_anon" ON public.naya_note_filing
--         FOR INSERT TO anon WITH CHECK (true);
--     After (B), re-run the Step 1 verify queries: the grants list must
--     show SELECT + INSERT on naya_note_filing and SELECT only on
--     naya_category_prototypes — and still no UPDATE or DELETE anywhere.
