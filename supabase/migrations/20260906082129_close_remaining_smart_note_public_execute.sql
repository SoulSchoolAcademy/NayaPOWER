REVOKE EXECUTE ON FUNCTION public.v7_create_smart_note(text, uuid, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, jsonb, text) FROM anon;
REVOKE EXECUTE ON FUNCTION public.v7_list_smart_note_events() FROM anon;
REVOKE EXECUTE ON FUNCTION public.verify_smart_note(uuid) FROM anon;
