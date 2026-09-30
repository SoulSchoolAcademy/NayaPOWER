create table if not exists public.learner_states (
  member_id uuid primary key references public.members(id) on delete cascade,
  goals jsonb not null default '[]'::jsonb check (jsonb_typeof(goals) = 'array'),
  active_target_ids jsonb not null default '[]'::jsonb check (jsonb_typeof(active_target_ids) = 'array'),
  demonstrated_capability_ids jsonb not null default '[]'::jsonb check (jsonb_typeof(demonstrated_capability_ids) = 'array'),
  current_evidence_by_target jsonb not null default '{}'::jsonb check (jsonb_typeof(current_evidence_by_target) = 'object'),
  unresolved_gap_ids jsonb not null default '[]'::jsonb check (jsonb_typeof(unresolved_gap_ids) = 'array'),
  misconception_ids jsonb not null default '[]'::jsonb check (jsonb_typeof(misconception_ids) = 'array'),
  successful_teaching_approach_ids jsonb not null default '[]'::jsonb check (jsonb_typeof(successful_teaching_approach_ids) = 'array'),
  last_meaningful_learning_at timestamptz,
  version bigint not null default 1 check (version > 0),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.learning_evidence (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references public.members(id) on delete cascade,
  target_id text not null,
  level text not null check (level in ('E0_EXPOSED','E1_UNDERSTANDS','E2_CAN_DO','E3_INDEPENDENT','E4_TRANSFER','E5_CAN_TEACH','E6_RETAINED','E7_MASTERED')),
  provenance text not null check (provenance in ('USER','SOURCE','TOOL','TEST','OBSERVATION','VERIFICATION','INFERENCE')),
  status text not null default 'ACTIVE' check (status in ('ACTIVE','STALE','SUPERSEDED','CONFLICTED','EXPIRED')),
  claim text not null check (char_length(trim(claim)) between 1 and 2000),
  observed_value jsonb not null default 'null'::jsonb,
  verification_method text not null check (char_length(trim(verification_method)) between 1 and 2000),
  source_event_id text,
  created_at timestamptz not null default now(),
  expires_at timestamptz
);

create index if not exists learning_evidence_member_target_idx on public.learning_evidence(member_id, target_id, created_at desc);
create index if not exists learning_evidence_member_status_idx on public.learning_evidence(member_id, status);

alter table public.learner_states enable row level security;
alter table public.learning_evidence enable row level security;

create policy learner_states_select_own on public.learner_states for select to authenticated using ((select auth.uid()) = member_id);
create policy learner_states_insert_own on public.learner_states for insert to authenticated with check ((select auth.uid()) = member_id);
create policy learner_states_update_own on public.learner_states for update to authenticated using ((select auth.uid()) = member_id) with check ((select auth.uid()) = member_id);

create policy learning_evidence_select_own on public.learning_evidence for select to authenticated using ((select auth.uid()) = member_id);
create policy learning_evidence_insert_own on public.learning_evidence for insert to authenticated with check ((select auth.uid()) = member_id);
create policy learning_evidence_update_own on public.learning_evidence for update to authenticated using ((select auth.uid()) = member_id) with check ((select auth.uid()) = member_id);

create or replace function public.touch_learner_state_updated_at()
returns trigger
language plpgsql
security invoker
set search_path = public
as $$
begin
  new.updated_at = now();
  new.version = old.version + 1;
  return new;
end;
$$;

drop trigger if exists learner_states_touch_updated_at on public.learner_states;
create trigger learner_states_touch_updated_at before update on public.learner_states for each row execute function public.touch_learner_state_updated_at();
