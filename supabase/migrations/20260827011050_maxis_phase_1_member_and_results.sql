create table public.members (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.maxess_results (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references public.members(id) on delete restrict,
  assessment_id text not null,
  assessment_version text not null,
  score numeric(5,2) not null check (score >= 0 and score <= 100),
  mastery_band text not null check (mastery_band in ('EMERGING','DEVELOPING','ADVANCING','MASTERING')),
  dimensions jsonb not null check (jsonb_typeof(dimensions) = 'object'),
  fingerprint text,
  report_payload jsonb,
  provenance jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

alter table public.members enable row level security;
alter table public.maxess_results enable row level security;

grant select, insert, update on public.members to authenticated;
grant select, insert on public.maxess_results to authenticated;

drop policy if exists "members_select_own" on public.members;
create policy "members_select_own" on public.members for select to authenticated using ((select auth.uid()) = id);

drop policy if exists "members_insert_own" on public.members;
create policy "members_insert_own" on public.members for insert to authenticated with check ((select auth.uid()) = id);

drop policy if exists "members_update_own" on public.members;
create policy "members_update_own" on public.members for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

drop policy if exists "results_select_own" on public.maxess_results;
create policy "results_select_own" on public.maxess_results for select to authenticated using ((select auth.uid()) = member_id);

drop policy if exists "results_insert_own" on public.maxess_results;
create policy "results_insert_own" on public.maxess_results for insert to authenticated with check ((select auth.uid()) = member_id);

create or replace function public.handle_new_user()
returns trigger
set search_path = public
language plpgsql
security definer
as $$
begin
  insert into public.members (id, display_name)
  values (new.id, coalesce(new.raw_user_meta_data->>'full_name', split_part(new.email, '@', 1)))
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();

create index if not exists maxess_results_member_created_idx on public.maxess_results(member_id, created_at desc);
