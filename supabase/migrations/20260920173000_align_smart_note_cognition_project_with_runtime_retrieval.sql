-- Align Smart Note cognition bridge with the runtime retrieval project.
-- The runtime retrieves canonical Smart Note cognition under project NayaNET.
-- Keep the existing bridge, identity, and ledger/index triggers unchanged.
create or replace function public.nayanet_smart_note_to_cognition()
returns trigger language plpgsql security definer set search_path=public,extensions
as $$
declare
  v_project_id text := coalesce(nullif(trim(new.source_context->>'project_id'), ''), 'NayaNET');
  v_event_id text := 'smart_note:' || new.id::text;
  v_source_hash text;
  v_status text := case when new.status='VERIFIED' then 'verified' else 'active' end;
  v_content text := coalesce(nullif(trim(new.subject),''), 'Smart Note ' || new.id::text);
begin
  v_source_hash := encode(extensions.digest('smart_note|' || new.id::text || '|' || new.member_id::text || '|' || coalesce(new.subject,'') || '|' || new.event_type || '|' || new.created_at::text,'sha256'),'hex');
  insert into public.nayanet_cognition_events(user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata)
  values(new.member_id,v_project_id,v_event_id,new.created_at,now(),'smart_note','observation',new.subject,v_content,'smart_note_events',v_status,'human',1,'[]'::jsonb,null,v_source_hash,'1.0.0','',jsonb_build_object('canonical_source_table','smart_note_events','canonical_source_id',new.id,'smart_note_event_id',new.id,'smart_note_status',new.status,'smart_note_privacy_state',new.privacy_state,'smart_note_verified_at',new.verified_at,'smart_note_source_context',new.source_context))
  on conflict (user_id,project_id,event_id) do update set updated_at=now(),title=excluded.title,content=excluded.content,status=excluded.status,metadata=excluded.metadata,source_hash=excluded.source_hash;
  return new;
end; $$;

revoke execute on function public.nayanet_smart_note_to_cognition() from public,anon,authenticated;
drop trigger if exists nayanet_smart_note_event_to_cognition on public.smart_note_events;
create trigger nayanet_smart_note_event_to_cognition after insert or update on public.smart_note_events for each row execute function public.nayanet_smart_note_to_cognition();
