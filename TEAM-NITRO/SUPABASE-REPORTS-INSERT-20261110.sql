-- Let the daily reports land again — Supabase master first pass, 2026-11-10.
-- Prepared for Shawn's hand in the Supabase SQL Editor (production database).
-- Read the header first: the preferred fix needs NO new SQL at all.
--
-- WHAT IS WRONG, IN PLAIN WORDS:
-- The daily reports table (hub_daily_intelligence_reports) holds 27 rows
-- and the newest is dated 2026-10-23 — nothing has landed in 18 days.
-- The table has exactly one rule: the public key may READ. There is no
-- INSERT rule, so an anonymous insert fails with 42501. The audit
-- re-proved it live, and the November 9 backfill seat proved it by
-- trying: one test insert, 42501, nothing written.
--
-- THE PREFERRED FIX (A) — SERVICE-KEY RUN, NO NEW SQL:
-- The 17 missing reports (Oct 24 – Nov 9) are already written, verified,
-- and waiting as a seed file: ~/workspace/reports-backfill-20261109/rows-seed.sql
-- (one INSERT, 17 rows, ON CONFLICT re-runnable; all 17 body hashes match
-- the filed editions; package commit dcc885cc). Run that file with the
-- service key — the service key bypasses the row rules, so no policy
-- change is needed. After it runs the table holds 44 rows, newest
-- 2026-11-09. One gap remains after that: Nov 10 has no report yet, and
-- no backfill covers it — Nov 10 needs its own Daily Intelligence Report
-- written and filed, not another seed. And note the deeper truth from
-- Oct 26: this table is batch-fed, not daily-fed (the Oct 9–22 rows all
-- landed in one batch on Oct 22). The seed closes the gap; only the
-- standing daily habit (a report every day, filed daily, never batched)
-- keeps it closed.
--
-- THE ALTERNATIVE FIX (B) — THE SQL BELOW, ONLY IF YOU CHOOSE IT:
-- The statements below add an INSERT rule for the public key, so the
-- anon-key path can write reports. WARNING, IN PLAIN WORDS: this lets
-- ANYONE holding the public key insert report rows — fake reports,
-- wrong dates, anything. The public key ships inside the app's own
-- code, so anyone can find it. That is a wide-open door on the reports
-- table, and it stays open until someone revokes it. Run fix B only if
-- you accept that trade. If you run fix A, DO NOT run this file.
--
-- This file is written so that running it does fix B and nothing else.
-- If fix A is the choice, leave this file unrun and run the seed file
-- instead.

GRANT INSERT ON public.hub_daily_intelligence_reports TO anon;

DROP POLICY IF EXISTS "hub_daily_intelligence_reports_insert_all" ON public.hub_daily_intelligence_reports;
CREATE POLICY "hub_daily_intelligence_reports_insert_all" ON public.hub_daily_intelligence_reports
  FOR INSERT TO anon WITH CHECK (true);

-- AFTER RUNNING FIX B, VERIFY (same SQL Editor, run these and check):
--   SELECT policyname, cmd FROM pg_policies
--     WHERE schemaname = 'public'
--     AND tablename = 'hub_daily_intelligence_reports';
-- An INSERT policy must now be listed next to the SELECT policy.
-- Then re-run the seed (rows-seed.sql) or one test insert: it must now
-- succeed instead of failing 42501. Check the row count after:
--   SELECT count(*), max(report_date) FROM public.hub_daily_intelligence_reports;
-- Expect 44 rows, newest 2026-11-09, once the seed has run.
-- AFTER RUNNING FIX A INSTEAD, VERIFY the same count query: 44 rows,
-- newest 2026-11-09, with NO policy change.
