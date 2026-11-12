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
