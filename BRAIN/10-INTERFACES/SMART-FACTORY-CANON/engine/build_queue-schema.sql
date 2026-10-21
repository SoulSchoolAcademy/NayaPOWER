-- build_queue — LIVE SCHEMA SNAPSHOT
-- Harvested: 2026-10-21 by Nu (BUILD), Team Nitro, for PR #2849 (Step-0 engine cure).
--
-- PROVENANCE — read before trusting: NO migration or DDL file for build_queue
-- exists in the repo or in ~/workspace/factory-pipeline (both searched
-- 2026-10-21). The table was created outside any tracked migration. This
-- snapshot is reconstructed from the LIVE database — project
-- dahisasgpfvziswqvmvm, information_schema.columns + pg_constraint, read via
-- the Supabase Management API on 2026-10-21 — so the schema the engine
-- actually runs against is on the record. It is evidence of the live state,
-- NOT a migration that was executed to produce this file.
--
-- Column evidence (ordinal order): id uuid NOT NULL default gen_random_uuid();
-- contract jsonb NOT NULL; status text default 'pending'; result_url text;
-- receipt jsonb; created_at timestamptz default now(); updated_at timestamptz
-- default now(). Constraints: build_queue_pkey PRIMARY KEY (id);
-- build_queue_status_check CHECK (status IN ('pending','building','done','failed'))
-- — the status vocabulary is corroborated independently: a test row entered
-- with a non-vocabulary status was rejected by this constraint (Postgres 23514,
-- factory-r1 TEST-SCORECARD, 2026-10-21).
-- NOT captured in this snapshot: RLS state / policies on the table.

create table public.build_queue (
  id         uuid        primary key default gen_random_uuid(),
  contract   jsonb       not null,
  status     text        default 'pending',
  result_url text,
  receipt    jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  constraint build_queue_status_check
    check (status in ('pending', 'building', 'done', 'failed'))
);
