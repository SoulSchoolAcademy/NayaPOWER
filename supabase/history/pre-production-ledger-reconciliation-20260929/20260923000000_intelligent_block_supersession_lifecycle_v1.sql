-- Intelligent Block lifecycle: idempotent supersession with durable lineage.
create or replace function public.nayanet_supersede_intelligent_block(
  p_superseded_block_id uuid,p_new_block_id uuid,p_owner_id uuid,p_subject_id text,p_title text,p_block_type text,
  p_understanding_state text,p_owner_scope text,p_source_event_ids uuid[],p_evidence_refs jsonb,p_provenance jsonb,
  p_value_context jsonb,p_applicable_scope jsonb,p_content jsonb,p_schema_version text,p_idempotency_key text
) returns public.nayanet_intelligent_blocks
language plpgsql security definer set search_path = public, extensions
as $function$
declare old_row public.nayanet_intelligent_blocks; existing_row public.nayanet_intelligent_blocks; new_row public.nayanet_intelligent_blocks;
begin
  if auth.uid() is null or auth.uid() <> p_owner_id then raise exception 'INTELLIGENT_BLOCK_OWNER_AUTH_REQUIRED'; end if;
  if p_superseded_block_id is null or p_new_block_id is null then raise exception 'INTELLIGENT_BLOCK_IDS_REQUIRED'; end if;
  if p_idempotency_key is null or btrim(p_idempotency_key)='' then raise exception 'INTELLIGENT_BLOCK_IDEMPOTENCY_KEY_REQUIRED'; end if;
  select * into existing_row from public.nayanet_intelligent_blocks where block_id=p_new_block_id and owner_id=p_owner_id;
  if found then
    if coalesce(existing_row.provenance->>'idempotency_key','')<>p_idempotency_key then raise exception 'INTELLIGENT_BLOCK_IDEMPOTENCY_KEY_MISMATCH'; end if;
    return existing_row;
  end if;
  select * into old_row from public.nayanet_intelligent_blocks where block_id=p_superseded_block_id and owner_id=p_owner_id for update;
  if not found then raise exception 'INTELLIGENT_BLOCK_TO_SUPERSEDE_NOT_FOUND'; end if;
  if old_row.superseded_by_block_id is not null and old_row.superseded_by_block_id<>p_new_block_id then raise exception 'INTELLIGENT_BLOCK_ALREADY_SUPERSEDED'; end if;
  insert into public.nayanet_intelligent_blocks(
    block_id,owner_id,subject_id,title,block_type,version,status,understanding_state,owner_scope,source_event_ids,evidence_refs,
    provenance,value_context,applicable_scope,content,supersedes_block_id,superseded_by_block_id,created_at,updated_at,schema_version
  ) values (
    p_new_block_id,p_owner_id,coalesce(p_subject_id,old_row.subject_id),coalesce(p_title,old_row.title),coalesce(p_block_type,old_row.block_type),
    old_row.version+1,'ACTIVE',coalesce(p_understanding_state,'CANDIDATE'),coalesce(p_owner_scope,old_row.owner_scope),p_source_event_ids,
    coalesce(p_evidence_refs,'[]'::jsonb),coalesce(p_provenance,'{}'::jsonb)||jsonb_build_object('supersedes_block_id',old_row.block_id,'supersedes_version',old_row.version,'idempotency_key',p_idempotency_key),
    coalesce(p_value_context,old_row.value_context),coalesce(p_applicable_scope,old_row.applicable_scope),coalesce(p_content,old_row.content),
    old_row.block_id,null,now(),now(),coalesce(p_schema_version,old_row.schema_version)
  ) returning * into new_row;
  update public.nayanet_intelligent_blocks set status='SUPERSEDED',superseded_by_block_id=p_new_block_id,updated_at=now()
  where block_id=old_row.block_id and owner_id=p_owner_id;
  return new_row;
end;
$function$;
