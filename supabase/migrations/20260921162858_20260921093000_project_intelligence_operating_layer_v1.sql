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
