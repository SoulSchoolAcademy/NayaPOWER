-- Lock the six open tables — Supabase audit 2026-11-10, Part 4.
-- Prepared for Shawn's hand in the Supabase SQL Editor (production database).
-- Paste the whole file, run it, done. No app code changes needed.
--
-- WHAT THIS DOES, IN PLAIN WORDS:
-- Each of these six tables sits with no lock on the door: anyone holding the
-- public key (which ships inside the app's own code, so anyone can find it)
-- can read, write, and delete rows in them. The audit proved it live — an
-- anonymous read of seat_keys returned both rows.
-- This file puts a lock on each table (RLS on) with NO rules underneath it,
-- which means the public key can no longer read, write, or delete anything
-- in them. Then it takes the public key's permissions away too, so even if
-- a rule is ever added by mistake, the public key has nothing to use.
-- Nothing the Hub and the feed read needs these six tables, so nothing
-- should break. If a page ever needs to read one of them, add back ONE
-- narrow read rule for that table only — never the writes.
--
-- ORDER: the keys first, the money second, the rest together.
--   seat_keys              — the keys that let the seats (agents) in. 2 rows.
--                            A stranger who writes here could add their own
--                            key and walk in as a seat, or delete the real
--                            keys and lock the team out. Most serious. First.
--   ambassador_links       — the 7 tracked links citizens share to earn
--                            their half. A stranger who writes here could
--                            point a link at their own payment, or delete
--                            links so clicks stop counting and nobody earns.
--   naya_category_prototypes — the 12 prototypes for the categories the
--                            system organizes intelligence into. A stranger
--                            who writes here scrambles the organizing system.
--   naya_note_filing       — the 19 records of Naya Notes filed. A stranger
--                            who writes here could plant fake filing records
--                            or delete the record that a note was filed.
--   ambassador_events      — 0 rows today (empty). The log of ambassador
--                            activity. Nothing to steal yet — but the door
--                            is open, so the moment the first event lands, a
--                            stranger could plant fake events or delete real
--                            ones. Lock it before it fills.
--   seat_lane_mapping      — 0 rows today (empty). Says which seat works
--                            which lane. A stranger could write fake mappings
--                            once it is used. Lock it before it fills.

ALTER TABLE public.seat_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ambassador_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.naya_category_prototypes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.naya_note_filing ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ambassador_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.seat_lane_mapping ENABLE ROW LEVEL SECURITY;

REVOKE ALL ON public.seat_keys FROM anon;
REVOKE ALL ON public.ambassador_links FROM anon;
REVOKE ALL ON public.naya_category_prototypes FROM anon;
REVOKE ALL ON public.naya_note_filing FROM anon;
REVOKE ALL ON public.ambassador_events FROM anon;
REVOKE ALL ON public.seat_lane_mapping FROM anon;

-- AFTER RUNNING, VERIFY (same SQL Editor, run these and check):
--   SELECT tablename, rowsecurity FROM pg_tables
--     WHERE schemaname = 'public'
--     AND tablename IN ('seat_keys','ambassador_links','naya_category_prototypes',
--                       'naya_note_filing','ambassador_events','seat_lane_mapping');
-- Every row should show rowsecurity = true.
-- Then re-run the audit's seat_keys check: an anonymous read should now
-- return nothing.
