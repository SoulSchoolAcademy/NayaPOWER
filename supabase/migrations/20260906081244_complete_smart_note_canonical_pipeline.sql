-- Smart Note canonical pipeline
-- Applied to Supabase project supabase-red-cable on 2026-09-06.
-- Contract: ONE Smart Note event = HUMAN + NAYA + MACHINE + INTELLIGENCE_FEED artifacts.
-- Completed events are verified and receipt-backed; retrieval is chronological by event timestamp.

CREATE OR REPLACE FUNCTION public.v7_create_smart_note(
  p_idempotency_key text,
  p_user_id uuid,
  p_human_note jsonb,
  p_naya_note jsonb,
  p_machine_note jsonb,
  p_intelligent_feed jsonb,
  p_intelligent_block jsonb,
  p_evidence jsonb,
  p_hub_state jsonb,
  p_subject text DEFAULT NULL
) RETURNS public.v7_smart_note_transactions
LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public'
AS $$
DECLARE
  v_row public.v7_smart_note_transactions;
  v_event_id uuid;
  v_now timestamptz := now();
  v_verification jsonb;
  v_subject text;
  v_artifact_urls jsonb := coalesce(p_evidence->'artifact_urls','{}'::jsonb);
  v_receipt_url text := nullif(trim(coalesce(p_evidence->>'receipt_url','')), '');
BEGIN
  IF auth.uid() IS NULL OR p_user_id IS DISTINCT FROM auth.uid() THEN RAISE EXCEPTION 'SMART_NOTE_USER_MISMATCH'; END IF;
  IF coalesce(trim(p_idempotency_key),'')='' THEN RAISE EXCEPTION 'SMART_NOTE_IDEMPOTENCY_KEY_REQUIRED'; END IF;
  IF p_human_note IS NULL OR p_naya_note IS NULL OR p_machine_note IS NULL OR p_intelligent_feed IS NULL OR p_intelligent_block IS NULL OR p_evidence IS NULL OR p_hub_state IS NULL THEN
    RAISE EXCEPTION 'SMART_NOTE_PIPELINE_PAYLOAD_INCOMPLETE';
  END IF;

  SELECT * INTO v_row FROM public.v7_smart_note_transactions WHERE idempotency_key=p_idempotency_key AND user_id=auth.uid() LIMIT 1;
  IF FOUND THEN RETURN v_row; END IF;

  v_subject := nullif(trim(coalesce(p_subject,'')), '');
  IF v_subject IS NULL THEN v_subject := nullif(trim(coalesce(p_human_note->>'subject','')), ''); END IF;
  IF v_subject IS NULL THEN v_subject := left(regexp_replace(coalesce(p_human_note->>'text',p_human_note->>'content','Smart Note'),'\s+',' ','g'),160); END IF;

  v_event_id := crypto.random_uuid();
  INSERT INTO public.smart_note_events(id,member_id,subject,event_type,source_context,privacy_state,status,created_at)
  VALUES(v_event_id,auth.uid(),v_subject,'SMART_NOTE',jsonb_build_object('idempotency_key',p_idempotency_key,'source',coalesce(p_machine_note->>'source','naya_conversation'),'captured_at',v_now),'PRIVATE','INCOMPLETE',v_now);

  INSERT INTO public.smart_note_artifacts(event_id,artifact_type,content,artifact_url,created_at) VALUES
  (v_event_id,'HUMAN_NOTE',coalesce(p_human_note->>'content',p_human_note->>'text',p_human_note::text),nullif(v_artifact_urls->>'human',''),v_now),
  (v_event_id,'NAYA_NOTE',coalesce(p_naya_note->>'content',p_naya_note->>'text',p_naya_note::text),nullif(v_artifact_urls->>'naya',''),v_now),
  (v_event_id,'MACHINE_NOTE',p_machine_note::text,nullif(v_artifact_urls->>'machine',''),v_now),
  (v_event_id,'INTELLIGENCE_FEED_NOTE',coalesce(p_intelligent_feed->>'summary',p_intelligent_feed->>'text',p_intelligent_feed::text),nullif(v_artifact_urls->>'feed',''),v_now);

  v_verification := public.verify_smart_note(v_event_id);
  IF coalesce(v_verification->>'status','') <> 'VERIFIED' THEN RAISE EXCEPTION 'SMART_NOTE_VERIFICATION_FAILED:%',v_verification::text; END IF;

  INSERT INTO public.smart_note_receipts(event_id,status,receipt_url,verification,created_at)
  VALUES(v_event_id,'VERIFIED',v_receipt_url,v_verification || jsonb_build_object('receipt_created_at',v_now),v_now)
  ON CONFLICT(event_id) DO UPDATE SET status='VERIFIED',receipt_url=excluded.receipt_url,verification=excluded.verification;

  INSERT INTO public.v7_smart_note_transactions(idempotency_key,user_id,status,human_note,naya_note,machine_note,intelligent_feed,intelligent_block,evidence,hub_state)
  VALUES(p_idempotency_key,auth.uid(),'completed',p_human_note,p_naya_note,p_machine_note,p_intelligent_feed,p_intelligent_block,p_evidence || jsonb_build_object('event_id',v_event_id,'verified_at',v_now),p_hub_state || jsonb_build_object('event_id',v_event_id,'last_intelligence_event_at',v_now))
  RETURNING * INTO v_row;
  RETURN v_row;
END;
$$;

CREATE OR REPLACE FUNCTION public.v7_list_smart_note_events()
RETURNS SETOF jsonb LANGUAGE sql SECURITY DEFINER SET search_path TO 'public'
AS $$
  SELECT jsonb_build_object(
    'event_id',e.id,'subject',e.subject,'event_type',e.event_type,'privacy_state',e.privacy_state,'status',e.status,'created_at',e.created_at,
    'artifacts',coalesce((SELECT jsonb_object_agg(lower(replace(a.artifact_type,'_NOTE','')),jsonb_build_object('type',a.artifact_type,'content',a.content,'artifact_url',a.artifact_url,'created_at',a.created_at)) FROM public.smart_note_artifacts a WHERE a.event_id=e.id),'{}'::jsonb),
    'receipt',(SELECT jsonb_build_object('status',r.status,'receipt_url',r.receipt_url,'verification',r.verification,'created_at',r.created_at) FROM public.smart_note_receipts r WHERE r.event_id=e.id LIMIT 1)
  )
  FROM public.smart_note_events e WHERE e.member_id=auth.uid() ORDER BY e.created_at DESC;
$$;
