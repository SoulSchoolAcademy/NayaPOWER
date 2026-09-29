ALTER FUNCTION public.verify_smart_note(uuid) SET search_path = public;
REVOKE EXECUTE ON FUNCTION public.v7_create_smart_note(text, uuid, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb) FROM anon;
REVOKE EXECUTE ON FUNCTION public.v7_create_smart_note(text, uuid, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, text) FROM anon;
REVOKE EXECUTE ON FUNCTION public.v7_list_smart_note_events() FROM anon;
REVOKE EXECUTE ON FUNCTION public.v7_list_smart_notes() FROM anon;
REVOKE EXECUTE ON FUNCTION public.verify_smart_note(uuid) FROM anon;
REVOKE ALL ON TABLE public.smart_note_events FROM anon, authenticated;
REVOKE ALL ON TABLE public.smart_note_artifacts FROM anon, authenticated;
REVOKE ALL ON TABLE public.smart_note_receipts FROM anon, authenticated;
