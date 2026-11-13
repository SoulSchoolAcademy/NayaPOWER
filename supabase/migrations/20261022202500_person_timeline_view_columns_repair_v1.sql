-- 20261022202500_person_timeline_view_columns_repair_v1.sql
--
-- Repair: the person-timeline guard in
-- 20261022203000_person_timeline_v1.sql (view, lines 164-220) fails at
-- statement 14, the CREATE OR REPLACE VIEW public.person_timeline_events
-- (governed run 43363191852, 2026-11-13, Supabase Preview check
-- 131681769012): ERROR: column t.thread_key does not exist (SQLSTATE
-- 42703). The guard's fail-loud source check (statement 13) PASSED on
-- that run — the first repair (20261022202000, filed on main in commit
-- 26b1a0e6, blob b521db7b) applied, and the fresh pre-check of this round
-- (2026-11-13T04:21:21Z) reads all 19 guard pairs present on live
-- production, including the first repair's 8 columns. The chain stopped
-- one statement further, on columns the guard's 19 never check: the
-- view references 18 (table, column) pairs, and THREE of them are in
-- neither the guard's 19 nor the first repair — smart_mail_threads.
-- thread_key, smart_mail_messages.sender_name, smart_mail_messages.
-- sender. The fresh pre-check proves all three MISSING on live
-- production (400/42703, each beside a 200 sibling on the same table),
-- so this file adds exactly those three. The 23514 repairs, sorting
-- after the guard, are still RED — the boundary is now statement 14.
--
-- Types are read from the view's own usage, never guessed — all three
-- text: thread_key joins t.thread_key = m.thread_key (guard line 202),
-- the messages-side join key is text (first repair), the threads-side
-- key is text (repair C, 20261022214000, line 34: add column if not
-- exists thread_key text — selected as the mail thread's object id, a
-- text slot, in 20261022214500_universal_search_v1.sql line 257), and
-- the chain's test (tests/test_person_timeline.py, lines 38 and 42)
-- models "thread_key": "t1"; sender_name / sender are passed to
-- resolve_person_key(p_display_name text, guard lines 85-87) via
-- coalesce(m.sender_name, m.sender) (guard lines 190, 199, 204) and
-- selected as counterparty_name (guard line 199) — the same pattern as
-- n.author_name / n.sender_name, which are text (first repair) — and
-- the test models "sender_name": "Mary Jones" (lines 48, 51, 54) while
-- the builder (tools/person_timeline.py, line 199) reads
-- msg.get("sender_name") or msg.get("sender") as a string name. The
-- guard's header comment lists thread_key among the smart_mail_threads
-- columns and sender, sender_name among the smart_mail_messages columns
-- evidenced in repo code (guard lines 21-25). NO CREATE TABLE for
-- smart_mail_threads exists anywhere in the migration chain (the first
-- repair verified this by exact-phrase code search, 0 results), so
-- there is no chain definition to harvest — text is the usage-derived
-- type, the same precedent as the first repair's participants/status.
--
-- NOT in this file, named not silent: smart_mail_threads.direction is
-- NOT added — the guard's header comment claims the threads table
-- carries direction, but the view never references t.direction (grep:
-- zero matches in the guard file) and the guard's 19 never checks it.
-- The first repair's 8 columns are NOT re-added — they are filed on
-- main (commit 26b1a0e6) and read present on live production now. The
-- guard is NOT touched: no relaxation, no weakening, the DO block stays
-- exactly as written. Adding a column writes NO data and reads NO mail.
-- Nothing else in this file.

alter table public.smart_mail_threads
  add column if not exists thread_key text;
alter table public.smart_mail_messages
  add column if not exists sender_name text,
  add column if not exists sender text;
