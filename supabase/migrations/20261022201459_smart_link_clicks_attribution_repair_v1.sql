-- CHAIN REPAIR (Path A, file 175) — RESTORED PREREQUISITE, PREPENDED 2026-11-21.
-- File 175 ALTERs public.smart_link_clicks (original statement 0, add attribution_id),
-- but no migration in the chain creates that table before it: its creator is
-- file 176, supabase/migrations/20261022201500_smart_links_v1.sql
--   blob 4feabd7acef26f860b9d11008f7498f6ef6f02e9, 7,986 B,
--   sha256 5c22ea369bae83df91265882a9bec2453d2b36a0fbf206bc5da12cef2b87127a
--   CREATE TABLE public.smart_link_clicks at lines 44-53, attribution_id at line 52.
-- The CREATE TABLE block is reproduced VERBATIM below (10 lines, nothing else
-- from file 176). Nothing in it is invented; no GRANT exists in it — file 176's
-- single GRANT (line 171, execute on resolve_smart_link to anon, authenticated)
-- is NOT prepended: file 176 still applies it when it runs, as written.
-- WHY AMENDED IN PLACE, NOT A SEPARATE RESTORE FILE:
--   (1) File 176's true version 20261022201500 sorts AFTER file 175
--       (20261022201459) — 176th, after file 175. A filing at its true
--       version could never rescue file 175; the DAG stops at 175 first.
--   (2) A separate file would need an invented pre-175 version (there is no
--       true version between file 174 at 20261022201458 and file 175 that
--       creates this table) and would apply on production at dispatch, since
--       any invented version is unrecorded there. On THIS leg that application
--       would be a no-op in effect (CREATE TABLE IF NOT EXISTS against a table
--       production already holds — verified first-hand) — unlike file 105,
--       where a separate filing would have resurrected a reset-dropped table.
--       It is rejected anyway: it invents a version and hides provenance (the
--       file-91 leg's objection), and the amend-in-place pattern (files 87,
--       105 and 174, all merged) keeps the repair attached to the file that
--       needs it with zero production application at all.
--   (3) File 175 IS recorded as applied on production (verified first-hand,
--       with 20261022201458 and 20261022201500), so this amended file never
--       re-applies there: production effect NONE.
--   (4) No reset/drop later in the chain affects smart_link_clicks: file 129
--       (20260927164132, the reset) sorts 129th, BEFORE file 175, and no file
--       176-197 drops the table (verified first-hand across all 22 files;
--       the only DROPs touching it are file 176 lines 203 and 213, DROP
--       POLICY IF EXISTS before the policies are recreated — not table drops).
--   (5) The prepended CREATE carries a foreign key to public.smart_links(id)
--       (file 176 line 46). That resolves on replay because the amended file
--       174 (sort 174, already merged on main) creates public.smart_links
--       immediately before file 175 runs. This repair therefore depends on
--       the file-174 repair already being on main; without it the CREATE
--       would fail on the missing referenced table.
--   (6) File 176 still runs in full later: its CREATE TABLE IF NOT EXISTS is
--       then a no-op for the table, and its indexes, RLS, policies, trigger
--       and GRANT apply to the table as written — the replay end-state after
--       file 176 is identical to a world where file 176 ran first.
-- PRODUCTION LIVE-STATE NOTE (Divergence-3 class, recorded not resolved):
-- production's smart_link_clicks HAS attribution_id (7 columns, verified
-- first-hand) but differs from file 176's CREATE: no referrer_host column,
-- and user_agent_class + country instead, which file 176 does not define.
-- attribution_id sits last in both. That drift does not affect this repair
-- — the amended file never applies on production — but it belongs to the
-- Divergence-3 investigation.
-- File 175's own statement below is UNTOUCHED, byte for byte.
--
create table if not exists public.smart_link_clicks (
  id uuid primary key default gen_random_uuid(),
  link_id uuid not null references public.smart_links(id) on delete cascade,
  clicked_at timestamptz not null default now(),
  referrer_class text not null default 'direct'
    constraint smart_link_clicks_referrer_class
    check (referrer_class in ('direct', 'social', 'search', 'email', 'internal', 'other')),
  referrer_host text,
  attribution_id uuid not null default gen_random_uuid()
);

-- 20261022201459_smart_link_clicks_attribution_repair_v1.sql
--
-- Repair: production's public.smart_link_clicks table exists WITHOUT the
-- attribution_id column that the Oct 22 migration
-- (20261022201500_smart_links_v1.sql, line 52) assumes, so that migration's
-- index build (lines 57-58) fails with ERROR 42703 and the migration chain
-- stops before the 23514 fix ever runs. Failed apply: governed run
-- 43245735356, Supabase check run 131280011943.
--
-- This migration sorts one second before the failing migration and adds the
-- column first. The column definition is VERBATIM from the Oct 22 file's
-- line 52. IF NOT EXISTS makes it a no-op on any database where the column
-- already exists. Nothing else in this file.

alter table public.smart_link_clicks
  add column if not exists attribution_id uuid not null default gen_random_uuid();
