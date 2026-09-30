drop policy if exists collective_publication_read on public.nayanet_intelligence_publications;
create policy collective_publication_read on public.nayanet_intelligence_publications
for select to authenticated
using (
  (status = 'published' and consent_state = 'explicit')
  or owner_id = auth.uid()
);
