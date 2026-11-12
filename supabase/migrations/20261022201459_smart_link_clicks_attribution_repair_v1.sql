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
