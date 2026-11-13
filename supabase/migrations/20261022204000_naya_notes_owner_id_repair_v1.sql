-- 20261022204000_naya_notes_owner_id_repair_v1.sql
--
-- Repair: production's public.naya_notes table exists WITHOUT the
-- owner_id column that the Oct 22 migration
-- (20261022204500_naya_notes_v1.sql, line 26) assumes, so that migration's
-- four owner policies (lines 44-62) fail with ERROR 42703 and the chain
-- stops. The same missing column also blocks the alias-binding trigger
-- in 20261022220000_alias_binding_v1.sql (lines 198-202, BEFORE INSERT OR
-- UPDATE OF owner_alias, owner_id ON public.naya_notes) and the backfill
-- in that file (lines 167-189), which reads naya_notes.owner_id.
-- Found by the apply seat's fresh pre-check, 2026-11-13 (STOP record):
-- a dispatch now would apply 1458 + 1500 + 20261022203000 and then fail
-- at 20261022204500, leaving a partial chain on live production.
--
-- This migration sorts before the failing migration
-- (20261022204500) and adds the column first. The column definition is
-- VERBATIM from the Oct 22 file's line 26 (owner_id uuid, nullable, no
-- default). IF NOT EXISTS makes it a no-op on any database where the
-- column already exists. Nothing else in this file.

alter table public.naya_notes
  add column if not exists owner_id uuid;
