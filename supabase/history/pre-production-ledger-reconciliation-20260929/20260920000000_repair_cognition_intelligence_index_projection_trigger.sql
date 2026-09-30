-- Repair production drift: keep generalized cognition events projected into the existing Intelligence Index.
-- The canonical migration exists in history, but the live production trigger was observed missing.
-- No new event store or retrieval system is introduced.
drop trigger if exists nayanet_index_cognition_event on public.nayanet_cognition_events;
create trigger nayanet_index_cognition_event
after insert or update on public.nayanet_cognition_events
for each row execute function public.nayanet_index_intelligence_row();
