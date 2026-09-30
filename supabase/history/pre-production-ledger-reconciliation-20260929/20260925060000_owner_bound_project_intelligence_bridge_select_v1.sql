-- Allow an authenticated owner to independently reconstruct the bridge record
-- created for that owner. No cross-owner read access is introduced.
create policy "nayanet_project_intelligence_bridge_owner_select"
  on public.nayanet_project_intelligence_bridge
  for select
  to authenticated
  using ((select auth.uid()) = owner_id);