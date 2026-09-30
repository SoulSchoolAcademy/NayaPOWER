-- Restore the historical SmartLedger -> canonical intelligence-index projection.
create or replace function public.nayanet_smart_ledger_to_intelligence_index()
returns trigger language plpgsql security definer set search_path=public,extensions as $function$
begin
  insert into public.nayanet_intelligence_index(
    owner_id,source_table,source_id,object_type,title,event_time,created_at,updated_at,
    status,project_id,revision,metadata
  )
  values(
    new.owner_id,'nayanet_smart_ledger',new.ledger_event_id,'REFERENCE',
    new.event_type,new.event_at,new.created_at,new.created_at,new.status,null,null,
    jsonb_build_object(
      'source_table',new.source_table,
      'source_id',new.source_id,
      'verification',new.verification,
      'privacy_classification',new.privacy_classification,
      'assessment_state',new.metadata->>'assessment_state',
      'value_receipt_type',new.metadata->>'value_receipt_type',
      'value_receipt_hash',new.metadata->>'value_receipt_hash'
    )
  )
  on conflict(owner_id,source_table,source_id) do update set
    object_type=excluded.object_type,
    title=excluded.title,
    event_time=excluded.event_time,
    updated_at=excluded.updated_at,
    status=excluded.status,
    metadata=excluded.metadata;
  return new;
end;
$function$;
revoke all on function public.nayanet_smart_ledger_to_intelligence_index() from public,anon,authenticated;

drop trigger if exists nayanet_smart_ledger_to_intelligence_index on public.nayanet_smart_ledger;
create trigger nayanet_smart_ledger_to_intelligence_index
after insert on public.nayanet_smart_ledger
for each row execute function public.nayanet_smart_ledger_to_intelligence_index();
