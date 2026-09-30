create table if not exists public.nayanet_execution_outcomes (
  outcome_id uuid primary key default gen_random_uuid(),
  receipt_id uuid not null unique references public.nayanet_execution_receipts(id) on delete restrict,
  user_id uuid not null references auth.users(id) on delete restrict,
  project_id text not null,
  experiment_case_id text,
  outcome_type text not null,
  verifier_id uuid not null references auth.users(id) on delete restrict,
  evidence jsonb not null default '{}',
  benefit numeric not null default 0,
  harm numeric not null default 0,
  cost numeric not null default 0,
  risk_adjusted_loss numeric not null default 0,
  verified_value numeric generated always as (benefit-harm-cost-risk_adjusted_loss) stored,
  verified boolean not null default false,
  verification_method text not null,
  created_at timestamptz not null default now()
);
alter table public.nayanet_execution_outcomes enable row level security;
drop policy if exists nayanet_execution_outcomes_owner on public.nayanet_execution_outcomes;
create policy nayanet_execution_outcomes_owner on public.nayanet_execution_outcomes for select to authenticated using (user_id=auth.uid());
revoke all on table public.nayanet_execution_outcomes from anon,authenticated,public;
grant select on table public.nayanet_execution_outcomes to authenticated;
