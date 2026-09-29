-- Canonical Naya persistence restoration V1
-- Restores the canonical persistence boundary after the 2026-09-27 legacy
-- reset drift. This is restoration, not a parallel intelligence store.
create extension if not exists pgcrypto;

create table if not exists public.nayanet_project_cognition_state (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null, revision bigint not null default 0, state jsonb not null default '{}',
  status text not null default 'READY', created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(), unique(user_id,project_id)
);
create table if not exists public.nayanet_cognition_events (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null, event_id text not null, created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(), type text not null default 'intelligence',
  classification text not null default 'observation', title text, content text not null,
  source text not null default 'nayanet', status text not null default 'active',
  actor text not null default 'human', confidence numeric not null default 1,
  tags jsonb not null default '[]', parent_event_id text, source_hash text not null,
  schema_version text not null default '1.0.0', receipt_id text not null, metadata jsonb not null default '{}',
  unique(user_id,project_id,event_id)
);
create table if not exists public.nayanet_execution_receipts (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null, revision bigint not null, action text not null, expected_result text,
  observed_result text, status text not null, evidence jsonb not null default '{}',
  learning jsonb not null default '[]', created_at timestamptz not null default now(),
  unique(user_id,project_id,revision)
);
create table if not exists public.nayanet_intelligent_blocks (
  block_id uuid primary key, intelligent_block_id text, owner_id uuid not null references auth.users(id) on delete cascade,
  subject_id text not null, title text not null, block_type text not null, version bigint not null default 1,
  status text not null default 'ACTIVE', understanding_state text not null default 'CANDIDATE',
  owner_scope text not null default 'PRIVATE', source_event_ids uuid[] not null,
  evidence_refs jsonb not null default '[]', provenance jsonb not null default '{}',
  value_context jsonb not null default '{}', applicable_scope jsonb not null default '{}',
  content jsonb not null default '{}', supersedes_block_id uuid, superseded_by_block_id uuid,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now(),
  schema_version text not null default 'INTELLIGENT_BLOCK_V1'
);
create unique index if not exists nayanet_intelligent_blocks_ib_id_uidx
  on public.nayanet_intelligent_blocks(intelligent_block_id) where intelligent_block_id is not null;
create table if not exists public.nayanet_intelligence_index (
  id uuid primary key default gen_random_uuid(), owner_id uuid not null references auth.users(id) on delete cascade,
  source_table text not null, source_id uuid not null, object_type text not null, title text,
  event_time timestamptz, created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(), status text, project_id text, revision bigint,
  metadata jsonb not null default '{}', unique(owner_id,source_table,source_id)
);
create table if not exists public.nayanet_intelligence_lineage (
  id uuid primary key default gen_random_uuid(), project_id text not null,
  user_id uuid not null references auth.users(id) on delete cascade,
  source_event_id uuid not null references public.nayanet_cognition_events(id),
  relation text not null, target_event_id uuid references public.nayanet_cognition_events(id),
  reason text, evidence_refs jsonb not null default '[]', created_at timestamptz not null default now(),
  unique(source_event_id,relation,target_event_id)
);
create table if not exists public.nayanet_authority_grants (
  grant_id uuid primary key default gen_random_uuid(), issuer_id uuid not null references auth.users(id),
  subject_id uuid not null references auth.users(id), source_event_id text not null, mission_id text not null,
  scope jsonb not null default '{}', actions jsonb not null default '[]', constraints jsonb not null default '{}',
  issued_at timestamptz not null default now(), expires_at timestamptz, status text not null default 'ACTIVE',
  revoked_at timestamptz, evidence jsonb not null default '{}', parent_authority jsonb,
  schema_version text not null default '1.0.0', created_at timestamptz not null default now()
);
create table if not exists public.nayanet_successor_handoffs (
  handoff_id uuid primary key default gen_random_uuid(), parent_node_id text not null,
  successor_node_id text not null unique, owner_id uuid not null references auth.users(id) on delete cascade,
  mission text not null, context jsonb not null default '{}', authority_inherited boolean not null default false,
  source_event_ids jsonb not null default '[]', proof jsonb not null default '{}',
  created_at timestamptz not null default now()
);
create table if not exists public.nayanet_brain_relationships (
  relationship_id uuid primary key default gen_random_uuid(), owner_id uuid not null references auth.users(id) on delete cascade,
  source_id text not null, target_id text not null, relationship_type text not null,
  provenance jsonb not null default '{}', epistemic_state text not null default 'UNKNOWN',
  created_at timestamptz not null default now(), unique(owner_id,source_id,target_id,relationship_type)
);

create index if not exists nayanet_cognition_owner_time_idx on public.nayanet_cognition_events(user_id,project_id,created_at desc);
create index if not exists nayanet_block_owner_time_idx on public.nayanet_intelligent_blocks(owner_id,updated_at desc);
create index if not exists nayanet_index_owner_time_idx on public.nayanet_intelligence_index(owner_id,event_time desc nulls last,updated_at desc);
create index if not exists nayanet_authority_subject_idx on public.nayanet_authority_grants(subject_id,status,expires_at);
create index if not exists nayanet_relationship_owner_idx on public.nayanet_brain_relationships(owner_id,source_id,target_id);

alter table public.nayanet_project_cognition_state enable row level security;
alter table public.nayanet_cognition_events enable row level security;
alter table public.nayanet_execution_receipts enable row level security;
alter table public.nayanet_intelligent_blocks enable row level security;
alter table public.nayanet_intelligence_index enable row level security;
alter table public.nayanet_intelligence_lineage enable row level security;
alter table public.nayanet_authority_grants enable row level security;
alter table public.nayanet_successor_handoffs enable row level security;
alter table public.nayanet_brain_relationships enable row level security;

comment on schema public is 'Canonical Naya persistence boundary. No parallel brain store is authorized.';
