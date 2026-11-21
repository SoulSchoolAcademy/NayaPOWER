-- CHAIN REPAIR (Path A, file 174) — RESTORED PREREQUISITE, PREPENDED 2026-11-21.
-- File 174 ALTERs public.smart_links (original statement 0, add owner_id),
-- but no migration in the chain creates that table before it: its creator is
-- file 176, supabase/migrations/20261022201500_smart_links_v1.sql
--   blob 4feabd7acef26f860b9d11008f7498f6ef6f02e9, 7,986 B,
--   sha256 5c22ea369bae83df91265882a9bec2453d2b36a0fbf206bc5da12cef2b87127a
--   CREATE TABLE public.smart_links at lines 24-37, owner_id at line 27.
-- The CREATE TABLE block is reproduced VERBATIM below (14 lines, nothing else
-- from file 176). Nothing in it is invented; no GRANT exists in it — file 176's
-- single GRANT (line 171, execute on resolve_smart_link to anon, authenticated)
-- is NOT prepended: file 176 still applies it when it runs, as written.
-- WHY AMENDED IN PLACE, NOT A SEPARATE RESTORE FILE:
--   (1) File 176's true version 20261022201500 sorts AFTER file 174
--       (20261022201458) — 176th, after files 174 and 175. A filing at its true
--       version could never rescue file 174; the DAG stops at 174 first.
--   (2) A separate file would need an invented pre-174 version (there is no
--       true version between file 173 at 20261011030000 and file 174 that
--       creates this table) and would apply on production at dispatch, since
--       any invented version is unrecorded there. On THIS leg that application
--       would be a no-op in effect (CREATE TABLE IF NOT EXISTS against a table
--       production already holds — verified first-hand) — unlike file 105,
--       where a separate filing would have resurrected a reset-dropped table.
--       It is rejected anyway: it invents a version and hides provenance (the
--       file-91 leg's objection), and the amend-in-place pattern (files 87
--       and 105, both merged) keeps the repair attached to the file that needs
--       it with zero production application at all.
--   (3) File 174 IS recorded as applied on production (verified first-hand,
--       with 20261022201459 and 20261022201500), so this amended file never
--       re-applies there: production effect NONE.
--   (4) No reset/drop later in the chain affects smart_links: file 129
--       (20260927164132, the reset) sorts 129th, BEFORE file 174, and no file
--       175-197 drops the table (verified first-hand across the eight later
--       files that reference it; the only DROP touching smart_links is file 189
--       line 204, a trigger drop, not a table drop).
--   (5) File 176 still runs in full later: its CREATE TABLE IF NOT EXISTS is
--       then a no-op for the table, and its indexes, RLS, policies, trigger
--       and GRANT apply to the table as written — the replay end-state after
--       file 176 is identical to a world where file 176 ran first.
-- PRODUCTION LIVE-STATE NOTE (Divergence-3 class, recorded not resolved):
-- production's smart_links HAS owner_id (7 columns, verified first-hand) but
-- differs from file 176's CREATE: no updated_at column, and extra policies
-- smart_links_authenticated_read / smart_links_resolve_read that file 176 does
-- not define. That drift does not affect this repair — the amended file never
-- applies on production — but it belongs to the Divergence-3 investigation.
-- File 174's own statement below is UNTOUCHED, byte for byte.
--
create table if not exists public.smart_links (
  id uuid primary key default gen_random_uuid(),
  owner_alias text not null,
  owner_id uuid,
  name text not null,
  target_url text not null,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint smart_links_name_shape
    check (name ~ '^[a-z0-9][a-z0-9-]{1,62}$'),
  constraint smart_links_target_shape
    check (target_url ~ '^https?://')
);

-- 20261022201458_smart_links_owner_id_repair_v1.sql
--
-- Repair: production's public.smart_links table exists WITHOUT the
-- owner_id column that the Oct 22 migration
-- (20261022201500_smart_links_v1.sql, line 27) assumes, so that migration's
-- owner policy build (statement 18, lines 179-181) fails with ERROR 42703
-- and the migration chain stops before the 23514 fix ever runs. Failed
-- apply: governed run 43259336393, 2026-11-12 16:31:49Z.
--
-- This migration sorts one second before the attribution repair
-- (20261022201459) and the failing migration (20261022201500) and adds the
-- column first. The column definition is VERBATIM from the Oct 22 file's
-- line 27. IF NOT EXISTS makes it a no-op on any database where the column
-- already exists. Nothing else in this file.

alter table public.smart_links
  add column if not exists owner_id uuid;
