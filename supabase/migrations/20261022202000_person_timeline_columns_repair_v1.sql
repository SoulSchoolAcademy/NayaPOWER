-- 20261022202000_person_timeline_columns_repair_v1.sql
--
-- Repair: the person-timeline guard in
-- 20261022203000_person_timeline_v1.sql (DO block, lines 125-155; values
-- list, lines 131-142; raise at line 153) raises
-- PERSON_TIMELINE_SOURCE_COLUMNS_MISSING unless 19 columns exist on the
-- pre-existing smart_notes, smart_mail_threads, smart_mail_messages and
-- invites tables. Eight are MISSING on live production (governed run
-- 43357690543, 2026-11-13, Supabase Preview check 131664040369, at
-- statement 13, the fail-loud source check before the unified event
-- view): smart_notes.author_name, smart_notes.sender_name,
-- smart_mail_threads.owner_alias, smart_mail_threads.participants,
-- smart_mail_threads.status, smart_mail_messages.thread_key,
-- smart_mail_messages.direction, invites.owner_alias.
--
-- Types are read from the chain's own definitions, never guessed — all
-- eight text: author_name / sender_name are passed to
-- resolve_person_key(p_display_name text, guard line 86) via
-- coalesce(n.author_name, n.sender_name) (guard line 176) and to
-- search_score(text, text) the same way in
-- 20261022214500_universal_search_v1.sql (lines 211-225);
-- smart_mail_threads.owner_alias is passed to resolve_person_key
-- (p_owner_alias text, guard line 86) at guard lines 189 and 191 and
-- read as t.owner_alias = any (v_aliases) in the 14500 file (line 268);
-- participants is read as t.participants::text and scored as one
-- string in the 14500 file (lines 264, 271), and the chain's contract
-- test (tests/test_universal_search_contract.py, line 394) models it as
-- a single string ("victim, maria"); status is modeled as a string in
-- the chain's test (tests/test_person_timeline.py, lines 38 and 42:
-- "status": "open") — the view does NOT read t.status, the guard
-- requires it anyway, so the column is added because the guard demands
-- it; thread_key joins t.thread_key = m.thread_key (guard line 202),
-- the threads-side key is text (repair C), and the test models
-- "thread_key": "t1"; direction is compared to the string literal
-- 'inbound' (guard line 203) and selected into the view's direction
-- column (guard line 198), and the test models "direction":
-- "inbound" / "outbound"; invites.owner_alias is passed to
-- resolve_person_key (guard lines 209 and 210) and the test models
-- "owner_alias": "shawn". NO CREATE TABLE for smart_mail_threads
-- exists anywhere in the migration chain (exact-phrase code search
-- returns 0 results), so there is no chain definition to harvest for
-- participants or status — text is the usage-derived type.
--
-- OVERLAP, named not silent: four of the eight (author_name,
-- sender_name, smart_mail_threads.owner_alias,
-- smart_mail_threads.participants) are ALREADY added on main by repair C
-- (20261022214000_universal_search_columns_repair_v1.sql). By the
-- captain's decision this file adds ALL EIGHT anyway, each ADD COLUMN
-- IF NOT EXISTS, so it is self-contained — the guard at 03000 passes
-- from this file alone — and the overlap is a no-op in either
-- application order. The guard is NOT touched: no relaxation, no
-- weakening, the DO block stays exactly as written. Adding a column
-- writes NO data and reads NO mail. Nothing else in this file.

alter table public.smart_notes
  add column if not exists author_name text,
  add column if not exists sender_name text;
alter table public.smart_mail_threads
  add column if not exists owner_alias text,
  add column if not exists participants text,
  add column if not exists status text;
alter table public.smart_mail_messages
  add column if not exists thread_key text,
  add column if not exists direction text;
alter table public.invites
  add column if not exists owner_alias text;
