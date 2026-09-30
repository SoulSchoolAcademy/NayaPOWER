ALTER TABLE public.smart_note_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.smart_note_artifacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.smart_note_receipts ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS smart_note_events_owner ON public.smart_note_events;
CREATE POLICY smart_note_events_owner ON public.smart_note_events FOR ALL TO authenticated USING (member_id = auth.uid()) WITH CHECK (member_id = auth.uid());
DROP POLICY IF EXISTS smart_note_artifacts_owner ON public.smart_note_artifacts;
CREATE POLICY smart_note_artifacts_owner ON public.smart_note_artifacts FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.smart_note_events e WHERE e.id = smart_note_artifacts.event_id AND e.member_id = auth.uid())) WITH CHECK (EXISTS (SELECT 1 FROM public.smart_note_events e WHERE e.id = smart_note_artifacts.event_id AND e.member_id = auth.uid()));
DROP POLICY IF EXISTS smart_note_receipts_owner ON public.smart_note_receipts;
CREATE POLICY smart_note_receipts_owner ON public.smart_note_receipts FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM public.smart_note_events e WHERE e.id = smart_note_receipts.event_id AND e.member_id = auth.uid())) WITH CHECK (EXISTS (SELECT 1 FROM public.smart_note_events e WHERE e.id = smart_note_receipts.event_id AND e.member_id = auth.uid()));
