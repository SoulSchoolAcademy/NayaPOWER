-- Enforce one canonical UUID across the entire Smart Note transaction.
-- The receiver may supply the UUID in any canonical payload; the transaction
-- boundary selects one identity and rewrites every persisted projection to it.
create or replace function public.v7_create_smart_note(
  p_idempotency_key text,
  p_user_id uuid,
  p_human_note jsonb,
  p_naya_note jsonb,
  p_machine_note jsonb,
  p_intelligent_feed jsonb,
  p_intelligent_block jsonb,
  p_evidence jsonb,
  p_hub_state jsonb,
  p_subject text default null
) returns public.v7_smart_note_transactions
language plpgsql
security definer
set search_path to 'public'
as $function$
declare
  v_row public.v7_smart_note_transactions;
  v_event_id uuid;
  v_now timestamptz := now();
  v_verification jsonb;
  v_subject text;
  v_artifact_urls jsonb := coalesce(p_evidence->'artifact_urls','{}'::jsonb);
  v_receipt_url text := nullif(trim(coalesce(p_evidence->>'receipt_url','')), '');
  v_human_note jsonb;
  v_naya_note jsonb;
  v_machine_note jsonb;
  v_intelligent_feed jsonb;
  v_intelligent_block jsonb;
  v_evidence jsonb;
  v_hub_state jsonb;
begin
  if auth.uid() is null or p_user_id is distinct from auth.uid() then raise exception 'SMART_NOTE_USER_MISMATCH'; end if;
  if coalesce(trim(p_idempotency_key),'')='' then raise exception 'SMART_NOTE_IDEMPOTENCY_KEY_REQUIRED'; end if;
  if p_human_note is null or p_naya_note is null or p_machine_note is null or p_intelligent_feed is null or p_intelligent_block is null or p_evidence is null or p_hub_state is null then
    raise exception 'SMART_NOTE_PIPELINE_PAYLOAD_INCOMPLETE';
  end if;

  select * into v_row from public.v7_smart_note_transactions
   where idempotency_key=p_idempotency_key and user_id=auth.uid() limit 1;
  if found then return v_row; end if;

  v_event_id := case
    when coalesce(trim(p_machine_note->>'event_id'),'') ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
      then (p_machine_note->>'event_id')::uuid
    when coalesce(trim(p_intelligent_feed->>'event_id'),'') ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
      then (p_intelligent_feed->>'event_id')::uuid
    when coalesce(trim(p_intelligent_block->>'block_id'),'') ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
      then (p_intelligent_block->>'block_id')::uuid
    when coalesce(trim(p_evidence->>'event_id'),'') ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
      then (p_evidence->>'event_id')::uuid
    when coalesce(trim(p_hub_state->>'event_id'),'') ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
      then (p_hub_state->>'event_id')::uuid
    when coalesce(trim(p_human_note->>'event_id'),'') ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
      then (p_human_note->>'event_id')::uuid
    when coalesce(trim(p_naya_note->>'event_id'),'') ~ '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
      then (p_naya_note->>'event_id')::uuid
    else crypto.random_uuid()
  end;

  v_human_note := p_human_note || jsonb_build_object('event_id',v_event_id);
  v_naya_note := p_naya_note || jsonb_build_object('event_id',v_event_id);
  v_machine_note := p_machine_note || jsonb_build_object('event_id',v_event_id);
  v_intelligent_feed := p_intelligent_feed || jsonb_build_object('event_id',v_event_id);
  v_intelligent_block := p_intelligent_block || jsonb_build_object('block_id',v_event_id);
  v_evidence := p_evidence || jsonb_build_object('event_id',v_event_id);
  v_hub_state := p_hub_state || jsonb_build_object('event_id',v_event_id);

  v_subject := nullif(trim(coalesce(p_subject,'')), '');
  if v_subject is null then v_subject := nullif(trim(coalesce(v_human_note->>'subject','')), ''); end if;
  if v_subject is null then
    v_subject := left(regexp_replace(coalesce(v_human_note->>'text',v_human_note->>'content','Smart Note'),'\\s+',' ','g'),160);
  end if;

  insert into public.smart_note_events(id,member_id,subject,event_type,source_context,privacy_state,status,created_at)
  values(
    v_event_id,auth.uid(),v_subject,'SMART_NOTE',
    jsonb_build_object('idempotency_key',p_idempotency_key,'source',coalesce(v_machine_note->>'source','naya_conversation'),'captured_at',v_now),
    'PRIVATE','INCOMPLETE',v_now
  );

  insert into public.smart_note_artifacts(event_id,artifact_type,content,artifact_url,created_at) values
    (v_event_id,'HUMAN_NOTE',coalesce(v_human_note->>'content',v_human_note->>'text',v_human_note::text),nullif(v_artifact_urls->>'human',''),v_now),
    (v_event_id,'NAYA_NOTE',coalesce(v_naya_note->>'content',v_naya_note->>'text',v_naya_note::text),nullif(v_artifact_urls->>'naya',''),v_now),
    (v_event_id,'MACHINE_NOTE',v_machine_note::text,nullif(v_artifact_urls->>'machine',''),v_now),
    (v_event_id,'INTELLIGENCE_FEED_NOTE',coalesce(v_intelligent_feed->>'summary',v_intelligent_feed->>'text',v_intelligent_feed::text),nullif(v_artifact_urls->>'feed',''),v_now);

  v_verification := public.verify_smart_note(v_event_id);
  if coalesce(v_verification->>'status','') <> 'VERIFIED' then
    raise exception 'SMART_NOTE_VERIFICATION_FAILED:%',v_verification::text;
  end if;

  insert into public.smart_note_receipts(event_id,status,receipt_url,verification,created_at)
  values(v_event_id,'VERIFIED',v_receipt_url,v_verification || jsonb_build_object('receipt_created_at',v_now),v_now)
  on conflict(event_id) do update set status='VERIFIED',receipt_url=excluded.receipt_url,verification=excluded.verification;

  insert into public.v7_smart_note_transactions(
    idempotency_key,user_id,status,human_note,naya_note,machine_note,intelligent_feed,intelligent_block,evidence,hub_state
  )
  values(
    p_idempotency_key,auth.uid(),'completed',v_human_note,v_naya_note,v_machine_note,v_intelligent_feed,
    v_intelligent_block,
    v_evidence || jsonb_build_object('verified_at',v_now),
    v_hub_state || jsonb_build_object('last_intelligence_event_at',v_now)
  )
  returning * into v_row;

  return v_row;
end;
$function$;