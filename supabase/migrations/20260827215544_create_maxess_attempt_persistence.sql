create table if not exists public.assessment_attempts (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references public.members(id) on delete cascade,
  assessment_id text not null,
  assessment_version text not null,
  topic text,
  status text not null default 'in_progress' check (status in ('in_progress', 'completed')),
  current_question_index integer not null default 0 check (current_question_index >= 0 and current_question_index <= 15),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  completed_at timestamptz,
  result_id uuid
);
create unique index if not exists assessment_attempts_one_active on public.assessment_attempts(member_id, assessment_id, assessment_version) where status = 'in_progress';
create index if not exists assessment_attempts_member_lookup on public.assessment_attempts(member_id, updated_at desc);
create table if not exists public.assessment_responses (
  id uuid primary key default gen_random_uuid(),
  attempt_id uuid not null references public.assessment_attempts(id) on delete cascade,
  question_id text not null,
  answer_id text not null,
  answered_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (attempt_id, question_id)
);
create index if not exists assessment_responses_attempt_lookup on public.assessment_responses(attempt_id, question_id);
alter table public.maxess_results add column if not exists attempt_id uuid references public.assessment_attempts(id);
create unique index if not exists maxess_results_one_per_attempt on public.maxess_results(attempt_id) where attempt_id is not null;
alter table public.assessment_attempts add constraint assessment_attempts_result_id_fkey foreign key (result_id) references public.maxess_results(id);
alter table public.assessment_attempts enable row level security;
alter table public.assessment_responses enable row level security;
create policy "members read own attempts" on public.assessment_attempts for select using ((select auth.uid()) = member_id);
create policy "members create own attempts" on public.assessment_attempts for insert with check ((select auth.uid()) = member_id and status = 'in_progress');
create policy "members update own active attempts" on public.assessment_attempts for update using ((select auth.uid()) = member_id and status = 'in_progress') with check ((select auth.uid()) = member_id and status = 'in_progress');
create policy "members read own responses" on public.assessment_responses for select using (exists (select 1 from public.assessment_attempts a where a.id = attempt_id and a.member_id = (select auth.uid())));
create policy "members create own active responses" on public.assessment_responses for insert with check (exists (select 1 from public.assessment_attempts a where a.id = attempt_id and a.member_id = (select auth.uid()) and a.status = 'in_progress'));
create policy "members update own active responses" on public.assessment_responses for update using (exists (select 1 from public.assessment_attempts a where a.id = attempt_id and a.member_id = (select auth.uid()) and a.status = 'in_progress')) with check (exists (select 1 from public.assessment_attempts a where a.id = attempt_id and a.member_id = (select auth.uid()) and a.status = 'in_progress'));
create or replace function public.complete_assessment_attempt(p_attempt_id uuid, p_result_id uuid) returns void language plpgsql security definer set search_path = public as $$ begin update public.assessment_attempts set status = 'completed', result_id = p_result_id, completed_at = now(), updated_at = now() where id = p_attempt_id and member_id = (select auth.uid()) and status = 'in_progress'; if not found then raise exception 'Attempt is missing, not owned by the current member, or already completed'; end if; end; $$;
revoke all on function public.complete_assessment_attempt(uuid, uuid) from public;
grant execute on function public.complete_assessment_attempt(uuid, uuid) to authenticated;
