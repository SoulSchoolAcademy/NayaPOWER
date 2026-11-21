-- CHAIN REPAIR (Path A, file 105) — RESTORED PREREQUISITE, PREPENDED 2026-11-21.
-- File 105 ALTERs public.nayanet_intelligence_operations (original lines 9-18),
-- but no migration in the chain creates that table: it lives only in history/
--   supabase/history/pre-production-ledger-reconciliation-20260929/20260921170000_add_nayanet_intelligence_operations.sql
--   blob 91bdbc7e7df5c72cbcf01de483aeaf3cfba1eb74, 1,261 B,
--   sha256 ac54cad2566d3db65f235c13224dfd4ead334a064b4c7ae962ac92c10f387370
-- The history file is reproduced VERBATIM below (CREATE TABLE + index + RLS +
-- two owner policies). Nothing in it is invented; no GRANT exists in it.
-- WHY AMENDED IN PLACE, NOT A SEPARATE RESTORE FILE:
--   (1) The history file's true version 20260921170000 sorts AFTER file 105
--       (20260921162858) and before file 106 (20260921170155) — a filing at its
--       true version could never rescue file 105; the DAG stops at 105 first.
--   (2) A separate file would need an invented pre-105 version AND would apply
--       on production at dispatch (version 20260921170000 is NOT recorded there),
--       CREATING a table production deliberately dropped: migration
--       20260927164132 (reset_legacy_nayanet_intelligence_layer, recorded as
--       applied) drops every public table except members, and no later migration
--       recreates this one (production today: table absent, verified first-hand).
--       The replay drops it again at file 129, so a separate filing would leave
--       production holding a legacy table the replay end-state lacks — divergence.
--   (3) File 105 IS recorded as applied on production, so this amended file
--       never re-applies there: production effect NONE. Replay and production
--       end-states stay convergent (no operations table in either).
-- File 105's own statements below are UNTOUCHED, byte for byte.
--
create table if not exists public.nayanet_intelligence_operations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null default 'NayaNET',
  operation text not null,
  status text not null,
  input jsonb not null default '{}'::jsonb,
  output jsonb not null default '{}'::jsonb,
  source_event_ids text[] not null default '{}'::text[],
  source_ref text,
  created_at timestamptz not null default now()
);
create index if not exists nayanet_intelligence_operations_user_project_created
  on public.nayanet_intelligence_operations(user_id, project_id, created_at desc);
alter table public.nayanet_intelligence_operations enable row level security;
drop policy if exists "nayanet intelligence operations owner read" on public.nayanet_intelligence_operations;
create policy "nayanet intelligence operations owner read"
  on public.nayanet_intelligence_operations for select
  using (auth.uid() = user_id);
drop policy if exists "nayanet intelligence operations owner insert" on public.nayanet_intelligence_operations;
create policy "nayanet intelligence operations owner insert"
  on public.nayanet_intelligence_operations for insert
  with check (auth.uid() = user_id);

alter table public.nayanet_project_intelligence_bridge
  add column if not exists retrieved boolean not null default false,
  add column if not exists rendered boolean not null default false,
  add column if not exists retrieval_evidence jsonb not null default '[]'::jsonb,
  add column if not exists render_evidence jsonb not null default '[]'::jsonb,
  add column if not exists acknowledged_at timestamptz,
  add column if not exists verified_at timestamptz;

alter table public.nayanet_intelligence_operations
  add column if not exists model_provider text,
  add column if not exists model_name text,
  add column if not exists input_tokens bigint not null default 0,
  add column if not exists output_tokens bigint not null default 0,
  add column if not exists tool_calls integer not null default 0,
  add column if not exists latency_ms bigint,
  add column if not exists human_seconds bigint,
  add column if not exists avoided_computation jsonb not null default '{}'::jsonb,
  add column if not exists verified_value numeric;

create table if not exists public.nayanet_project_intelligence_state (
  project_id text primary key,
  version bigint not null default 1,
  canonical_source_ref text,
  status text not null default 'ACTIVE',
  mission text not null,
  vision text not null,
  north_star text not null,
  current_state jsonb not null default '{}'::jsonb,
  proven jsonb not null default '[]'::jsonb,
  unknown jsonb not null default '[]'::jsonb,
  blocked jsonb not null default '[]'::jsonb,
  protected jsonb not null default '[]'::jsonb,
  current_next_action jsonb not null default '{}'::jsonb,
  evidence_refs jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);
alter table public.nayanet_project_intelligence_state enable row level security;

create table if not exists public.nayanet_intelligence_lineage (
  id uuid primary key default gen_random_uuid(),
  project_id text not null,
  user_id uuid not null references auth.users(id),
  source_event_id uuid not null references public.nayanet_cognition_events(id),
  relation text not null,
  target_event_id uuid references public.nayanet_cognition_events(id),
  reason text,
  evidence_refs jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  unique(source_event_id, relation, target_event_id)
);
alter table public.nayanet_intelligence_lineage enable row level security;

drop policy if exists "pi_state_owner_read" on public.nayanet_project_intelligence_state;
drop policy if exists "pi_lineage_owner_read" on public.nayanet_intelligence_lineage;
create policy "pi_state_owner_read" on public.nayanet_project_intelligence_state for select using (true);
create policy "pi_lineage_owner_read" on public.nayanet_intelligence_lineage for select using (auth.uid() = user_id);

alter table public.learning_evidence drop constraint if exists learning_evidence_status_check;
alter table public.learning_evidence add constraint learning_evidence_status_check check (status = any (array['CANDIDATE','ACTIVE','STALE','SUPERSEDED','CONFLICTED','EXPIRED']));

create index if not exists nayanet_pi_bridge_retrieved_idx on public.nayanet_project_intelligence_bridge(retrieved,accepted_at desc);
create index if not exists nayanet_pi_bridge_rendered_idx on public.nayanet_project_intelligence_bridge(rendered,accepted_at desc);
create index if not exists nayanet_pi_ops_created_idx on public.nayanet_intelligence_operations(user_id,project_id,created_at desc);
create index if not exists nayanet_pi_lineage_project_idx on public.nayanet_intelligence_lineage(project_id,created_at desc);
