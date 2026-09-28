drop policy if exists "collective_publication_owner_update" on public.nayanet_intelligence_publications;

create policy "collective_publication_owner_update"
on public.nayanet_intelligence_publications
for update to authenticated
using (owner_id = (select auth.uid()))
with check (
  owner_id = (select auth.uid())
  and exists (
    select 1
    from public.nayanet_cognition_events e
    where e.id = intelligence_event_id
      and e.user_id = (select auth.uid())
  )
);
