-- Drop the unused 6-parameter overload of nayanet_record_cognition_event.
-- The canonical 7-parameter version (with p_execution_authorization) is the
-- only version that should exist. All callers have been updated to use the
-- 7-parameter version explicitly.
drop function if exists public.nayanet_record_cognition_event(text,jsonb,text,text,text,jsonb);
