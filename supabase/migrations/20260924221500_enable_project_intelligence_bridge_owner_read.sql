alter table public.nayanet_project_intelligence_bridge enable row level security;

drop policy if exists "project intelligence bridge owner read" on public.nayanet_project_intelligence_bridge;

create policy "project intelligence bridge owner read"
on public.nayanet_project_intelligence_bridge
for select
to authenticated
using ((select auth.uid()) = owner_id);
