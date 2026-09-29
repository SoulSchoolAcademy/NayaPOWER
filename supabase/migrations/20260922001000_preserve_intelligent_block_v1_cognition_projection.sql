-- NIOM: preserve the canonical Intelligent Block V1 envelope through
-- Smart Note -> Cognition projection. No new schema.
CREATE OR REPLACE FUNCTION public.nayanet_smart_note_to_cognition()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO 'public', 'extensions'
AS $function$
declare
  v_project_id text := coalesce(nullif(trim(new.source_context->>'project_id'), ''), 'NayaNET');
  v_event_id text := new.id::text;
  v_source_hash text;
  v_status text := case when new.status='VERIFIED' then 'verified' else 'active' end;
  v_content text := coalesce(nullif(trim(new.subject),''), 'Smart Note ' || new.id::text);
  v_block jsonb := case when jsonb_typeof(new.source_context->'intelligent_block_v1')='object' then new.source_context->'intelligent_block_v1' else null end;
begin
  v_source_hash := encode(extensions.digest('smart_note|' || new.id::text || '|' || new.member_id::text || '|' || coalesce(new.subject,'') || '|' || new.event_type || '|' || new.created_at::text,'sha256'),'hex');
  insert into public.nayanet_cognition_events(
    user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,
    source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata
  )
  values(
    new.member_id,v_project_id,v_event_id,new.created_at,now(),'smart_note','observation',new.subject,
    v_content,'smart_note_events',v_status,'human',1,'[]'::jsonb,null,v_source_hash,'1.0.0','',
    jsonb_build_object(
      'event_id',v_event_id,
      'canonical_source_table','smart_note_events',
      'canonical_source_id',new.id,
      'smart_note_event_id',new.id,
      'smart_note_status',new.status,
      'smart_note_privacy_state',new.privacy_state,
      'smart_note_verified_at',new.verified_at,
      'smart_note_source_context',new.source_context,
      'intelligent_block_v1',v_block,
      'intelligent_block_schema',case when v_block is not null then 'NAYANET_INTELLIGENT_BLOCK_V1' else null end,
      'intelligent_block_hash',case when v_block is not null then v_block->'integrity'->>'content_hash' else null end,
      'smart_note_receipt_id',new.source_context->>'smart_note_receipt_id'
    )
  )
  on conflict (user_id,project_id,event_id)
  do update set
    updated_at=now(),
    title=excluded.title,
    content=excluded.content,
    status=excluded.status,
    metadata=excluded.metadata,
    source_hash=excluded.source_hash;
  return new;
end;
$function$;
