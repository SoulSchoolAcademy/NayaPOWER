-- schema.sql — Daily Intelligence Reports table (DRAFT for Nitro's package)
-- Proposed table name: public.hub_daily_intelligence_reports
--   Follows the existing hub_ naming pattern (hub_smart_notes_archive,
--   hub_smart_notes_personal). PROPOSED — Nitro's call if another name fits
--   her estate better; the view reads the name from one config constant.
--
-- One row per day. The view reads with the anon key, so SELECT is granted to
-- anon and writes are NOT: no insert/update/delete policy exists for anon,
-- which under RLS means anon writes are denied. Seeding and future daily
-- inserts run under service_role (which bypasses RLS) — e.g. from Nitro's
-- box or the daily learning-event lane's server-side step.
--
-- Run this first, then rows-seed.sql. Safe to re-run (if not exists / or replace).

create table if not exists public.hub_daily_intelligence_reports (
  report_date     date primary key,               -- one row per day
  report_id       text unique,                    -- DIR-NAYAPOWER-2026-10-22 (DIR-NAYANET-2026-10-03 keeps its id)
  headline        text not null,                  -- the day in one line (list view)
  lessons_summary text not null,                  -- the day's lessons + declared behavior changes (verbatim slice of the edition)
  body_md         text not null,                  -- the full filed edition, markdown, byte-identical to the repo file
  source_path     text,                           -- repo path of the filed edition (provenance)
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

alter table public.hub_daily_intelligence_reports enable row level security;

drop policy if exists "reports are publicly readable" on public.hub_daily_intelligence_reports;
create policy "reports are publicly readable"
  on public.hub_daily_intelligence_reports
  for select
  to anon
  using (true);

-- Deliberately NO anon insert/update/delete policies: the reports are
-- read-only for the public; only service_role writes (seed + daily filing).
