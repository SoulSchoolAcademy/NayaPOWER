create table if not exists public.nayanet_policy_versions (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references auth.users(id) on delete cascade,
 project_id text not null default 'NayaNET',
 policy_key text not null,
 version integer not null,
 parent_policy_id uuid references public.nayanet_policy_versions(id),
 state text not null check(state in ('DRAFT','VALIDATED','ADVERSARIAL_REVIEW','HOLDOUT_PASS','AUTHORIZATION_REQUIRED','CONTROLLED_TEST','OBSERVED','VERIFIED','PROMOTED','REJECTED','ROLLED_BACK')),
 policy jsonb not null default '{}',
 validation jsonb not null default '{}',
 adversarial jsonb not null default '{}',
 holdout jsonb not null default '{}',
 promotion jsonb not null default '{}',
 rollback jsonb not null default '{}',
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 unique(user_id,project_id,policy_key,version)
);
create table if not exists public.nayanet_policy_evaluations (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references auth.users(id) on delete cascade,
 policy_id uuid not null references public.nayanet_policy_versions(id) on delete cascade,
 evaluation_type text not null check(evaluation_type in ('DETERMINISTIC','COUNTERFACTUAL','ADVERSARIAL','HOLDOUT','CONTROLLED_TEST','REAL_OUTCOME')),
 dataset_hash text,
 baseline_score numeric,
 candidate_score numeric,
 responsible_value numeric,
 verified boolean not null default false,
 result text not null check(result in ('PASS','FAIL','UNKNOWN','NOT_PROVEN')),
 evidence jsonb not null default '{}',
 created_at timestamptz not null default now()
);
alter table public.nayanet_policy_versions enable row level security;
alter table public.nayanet_policy_evaluations enable row level security;
create policy policy_versions_owner on public.nayanet_policy_versions for select using(auth.uid()=user_id);
create policy policy_versions_owner_insert on public.nayanet_policy_versions for insert with check(auth.uid()=user_id);
create policy policy_evaluations_owner on public.nayanet_policy_evaluations for select using(auth.uid()=user_id);
create policy policy_evaluations_owner_insert on public.nayanet_policy_evaluations for insert with check(auth.uid()=user_id);
revoke all on public.nayanet_policy_versions,public.nayanet_policy_evaluations from anon;
grant select,insert on public.nayanet_policy_versions,public.nayanet_policy_evaluations to authenticated;
create or replace function public.nayanet_policy_transition(p_policy_id uuid,p_to_state text,p_evaluation jsonb default '{}')
returns jsonb language plpgsql security definer set search_path=''
as $$
declare p public.nayanet_policy_versions;
begin
 select * into p from public.nayanet_policy_versions where id=p_policy_id for update;
 if p.id is null then raise exception 'POLICY_NOT_FOUND'; end if;
 if p.user_id <> auth.uid() then raise exception 'POLICY_OWNER_REQUIRED'; end if;
 if p_to_state='PROMOTED' then
  if p.state <> 'VERIFIED' then raise exception 'PROMOTION_REQUIRES_VERIFIED'; end if;
  if coalesce((p.holdout->>'result'),'') <> 'PASS' then raise exception 'PROMOTION_REQUIRES_HOLDOUT_PASS'; end if;
  if coalesce((p.adversarial->>'result'),'') <> 'PASS' then raise exception 'PROMOTION_REQUIRES_ADVERSARIAL_PASS'; end if;
  if coalesce((p_evaluation->>'authorized'),'false') <> 'true' then raise exception 'PROMOTION_REQUIRES_AUTHORIZATION'; end if;
 end if;
 if p_to_state='CONTROLLED_TEST' and p.state <> 'AUTHORIZATION_REQUIRED' then raise exception 'CONTROLLED_TEST_REQUIRES_AUTHORIZATION_STATE'; end if;
 if p_to_state='VERIFIED' and p.state <> 'OBSERVED' then raise exception 'VERIFICATION_REQUIRES_OBSERVED'; end if;
 update public.nayanet_policy_versions set state=p_to_state,
  validation=case when p_to_state='VALIDATED' then p_evaluation else validation end,
  adversarial=case when p_to_state='ADVERSARIAL_REVIEW' then p_evaluation else adversarial end,
  holdout=case when p_to_state='HOLDOUT_PASS' then p_evaluation else holdout end,
  promotion=case when p_to_state='PROMOTED' then p_evaluation else promotion end,
  rollback=case when p_to_state='ROLLED_BACK' then p_evaluation else rollback end,
  updated_at=now() where id=p_policy_id;
 return jsonb_build_object('status','TRANSITIONED','policy_id',p_policy_id,'state',p_to_state);
end; $$;
revoke execute on function public.nayanet_policy_transition(uuid,text,jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_policy_transition(uuid,text,jsonb) to authenticated,service_role;
