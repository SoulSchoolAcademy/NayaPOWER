create table if not exists public.nayanet_project_cognition_state (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null,
  revision bigint not null default 0,
  state jsonb not null,
  status text not null default 'IN_PROGRESS' check (status in ('READY','IN_PROGRESS','BLOCKED','FAILED')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(user_id, project_id)
);

create table if not exists public.nayanet_execution_receipts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null,
  revision bigint not null,
  action text not null,
  expected_result text,
  observed_result text,
  status text not null check (status in ('SUCCESS','PARTIAL','BLOCKED','FAILED')),
  evidence jsonb not null default '[]'::jsonb,
  learning jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  unique(user_id, project_id, revision)
);

alter table public.nayanet_project_cognition_state enable row level security;
alter table public.nayanet_execution_receipts enable row level security;

drop policy if exists nayanet_cognition_owner on public.nayanet_project_cognition_state;
create policy nayanet_cognition_owner on public.nayanet_project_cognition_state for all to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists nayanet_receipts_owner on public.nayanet_execution_receipts;
create policy nayanet_receipts_owner on public.nayanet_execution_receipts for all to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());

create index if not exists nayanet_cognition_project_idx on public.nayanet_project_cognition_state(user_id, project_id);
create index if not exists nayanet_receipts_project_idx on public.nayanet_execution_receipts(user_id, project_id, created_at desc);

create or replace function public.nayanet_commit_cognition(
  p_project_id text,
  p_expected_revision bigint,
  p_state jsonb,
  p_action text,
  p_expected_result text,
  p_observed_result text,
  p_status text,
  p_evidence jsonb default '[]'::jsonb,
  p_learning jsonb default '[]'::jsonb
) returns public.nayanet_project_cognition_state
language plpgsql
security invoker
set search_path = public
as $$
declare v public.nayanet_project_cognition_state;
begin
  update public.nayanet_project_cognition_state
     set revision = revision + 1,
         state = p_state,
         status = p_status,
         updated_at = now()
   where user_id = auth.uid()
     and project_id = p_project_id
     and revision = p_expected_revision
   returning * into v;
  if not found then
    raise exception 'COGNITION_REVISION_CONFLICT';
  end if;
  insert into public.nayanet_execution_receipts(user_id, project_id, revision, action, expected_result, observed_result, status, evidence, learning)
  values(auth.uid(), p_project_id, v.revision, p_action, p_expected_result, p_observed_result, p_status, coalesce(p_evidence,'[]'::jsonb), coalesce(p_learning,'[]'::jsonb));
  return v;
end;
$$;

grant execute on function public.nayanet_commit_cognition(text,bigint,jsonb,text,text,text,text,jsonb,jsonb) to authenticated;
