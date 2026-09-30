
create or replace function public.nayanet_smart_ledger_hash(
 p_owner_id uuid,p_event_type text,p_event_at timestamptz,p_source_table text,p_source_id text,
 p_parent_ledger_event_id uuid,p_previous_chain_hash text,p_evidence_refs jsonb,p_metadata jsonb
) returns text language sql immutable set search_path=public,extensions as $$
 select encode(extensions.digest(
  coalesce(p_owner_id::text,'')||'|'||coalesce(p_event_type,'')||'|'||coalesce(p_event_at::text,'')||'|'||
  coalesce(p_source_table,'')||'|'||coalesce(p_source_id,'')||'|'||coalesce(p_parent_ledger_event_id::text,'')||'|'||
  coalesce(p_previous_chain_hash,''),
  'sha256'),'hex');
$$;

update public.nayanet_smart_ledger l
set event_hash=public.nayanet_smart_ledger_hash(l.owner_id,l.event_type,l.event_at,l.source_table,l.source_id,l.parent_ledger_event_id,l.previous_chain_hash,l.evidence_refs,l.metadata);

create or replace function public.nayanet_smart_note_receipt_to_ledger() returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin
 update public.nayanet_smart_ledger l set
  status=case when new.status='VERIFIED' then 'VERIFIED' else l.status end,
  verification=coalesce(new.verification,'{}'::jsonb)||jsonb_build_object('smart_note_receipt_id',new.id,'receipt_status',new.status)
 where l.owner_id=(select e.member_id from public.smart_note_events e where e.id=new.event_id)
   and l.source_table='smart_note_events' and l.source_id=new.event_id::text;
 return new;
end; $$;
