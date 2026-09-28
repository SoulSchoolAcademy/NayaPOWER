-- Project generalized Cognition events into the existing Intelligence Index.
-- Cognition remains the event identity store; Intelligence Index is a retrieval projection.
drop trigger if exists nayanet_index_cognition_event on public.nayanet_cognition_events;
create trigger nayanet_index_cognition_event after insert or update on public.nayanet_cognition_events for each row execute function public.nayanet_index_intelligence_row();
