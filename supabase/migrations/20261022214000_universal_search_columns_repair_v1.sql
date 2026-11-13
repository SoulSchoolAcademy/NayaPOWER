-- 20261022214000_universal_search_columns_repair_v1.sql
--
-- Repair: the universal-search guard in
-- 20261022214500_universal_search_v1.sql (DO block, lines 73-103) raises
-- UNIVERSAL_SEARCH_SOURCE_COLUMNS_MISSING unless 11 columns exist on the
-- pre-existing smart_notes and smart_mail_threads tables. Five are
-- MISSING on live production (apply seat's fresh pre-check, 2026-11-13):
-- smart_notes.author_name, smart_notes.sender_name,
-- smart_mail_threads.owner_alias, smart_mail_threads.participants,
-- smart_mail_threads.thread_key.
--
-- Types are read from the file's own usage, never guessed — all five
-- text: author_name / sender_name are passed to search_score(text, text)
-- via coalesce(n.author_name, n.sender_name) (lines 211-225);
-- owner_alias is read as lower(btrim(t.owner_alias)) (line 268);
-- thread_key is selected as the mail thread's object id, a text slot
-- (line 257); participants is read as t.participants::text and scored
-- as one string (lines 264, 271), and the chain's contract test
-- (tests/test_universal_search_contract.py, lines 376-394) models it as
-- a single string ("victim, maria"). NO CREATE TABLE for
-- smart_mail_threads exists anywhere in the migration chain (verified
-- by code search + grep of every .sql file that mentions it), so there
-- is no chain definition to harvest — text is the usage-derived type.
-- The guard is NOT touched: no relaxation, no weakening, the DO block
-- stays exactly as written. Adding a column writes NO data and reads
-- NO mail. Nothing else in this file.

alter table public.smart_notes
  add column if not exists author_name text,
  add column if not exists sender_name text;
alter table public.smart_mail_threads
  add column if not exists owner_alias text,
  add column if not exists participants text,
  add column if not exists thread_key text;
