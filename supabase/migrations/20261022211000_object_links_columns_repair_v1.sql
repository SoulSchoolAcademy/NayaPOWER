-- 20261022211000_object_links_columns_repair_v1.sql
--
-- Repair: production's public.object_links table exists WITHOUT the five
-- columns that the Oct 22 migration
-- (20261022211500_object_links_v1.sql, CREATE TABLE lines 70-89) assumes:
-- owner_id (line 72), subject_kind (lines 73-76), subject_ref (line 77),
-- target_kind (lines 78-81), target_ref (line 82). The file's unique
-- index (lines 91-92) fails with ERROR 42703 on subject_kind, and its
-- four owner policies (lines 224-243) use owner_id next. Found by the
-- apply seat's fresh pre-check, 2026-11-13 (STOP record).
--
-- The repair adds the five columns NULLABLE with no default and no
-- constraints. The chain's NOT NULL / CHECK clauses live inside a
-- CREATE TABLE IF NOT EXISTS that is a no-op on production because the
-- table already exists — they never attach. A NOT NULL add would fail
-- on a populated table. That shape difference is accepted and named
-- here, not silent. Types are VERBATIM from the Oct 22 file's
-- CREATE TABLE. IF NOT EXISTS makes each add a no-op where the column
-- already exists. Nothing else in this file.

alter table public.object_links
  add column if not exists owner_id uuid,
  add column if not exists subject_kind text,
  add column if not exists subject_ref text,
  add column if not exists target_kind text,
  add column if not exists target_ref text;
