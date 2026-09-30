
create policy nayanet_notifications_owner_read
on public.nayanet_intelligence_notifications
for select to authenticated
using (user_id = auth.uid());

create policy nayanet_notification_deliveries_owner_read
on public.nayanet_intelligence_notification_deliveries
for select to authenticated
using (
  exists (
    select 1 from public.nayanet_intelligence_notifications n
    where n.id = notification_id
      and n.user_id = auth.uid()
  )
);
