-- GAP-002: preserve the canonical Intelligent Block V1 envelope in the existing
-- Intelligence Index so the Hub can retrieve the same Block that persistence owns.
-- No new store or retrieval path is introduced.
create or replace function public.nayanet_intelligent_block_to_intelligence_index()
returns trigger
language plpgsql
security definer
set search_path = public, extensions
as $function$
declare
  v_block jsonb := coalesce(new.content, '{}'::jsonb);
  v_source_context jsonb := coalesce(v_block->'context', '{}'::jsonb);
  v_provenance jsonb := coalesce(new.provenance, '{}'::jsonb);
  v_event_time timestamptz := coalesce(
    nullif(v_block->'time'->>'occurred_at','')::timestamptz,
    new.created_at
  );
begin
  insert into public.nayanet_intelligence_index(
    owner_id,
    source_table,
    source_id,
    object_type,
    title,
    event_time,
    created_at,
    updated_at,
    status,
    project_id,
    revision,
    metadata
  )
  values(
    new.owner_id,
    'nayanet_intelligent_blocks',
    new.block_id,
    'INTELLIGENT_BLOCK',
    new.title,
    v_event_time,
    new.created_at,
    new.updated_at,
    new.status,
    'NayaNET',
    new.version,
    jsonb_build_object(
      'event_id', coalesce(v_block->'identity'->>'event_id', new.block_id::text),
      'object_id', coalesce(v_block->'identity'->>'object_id', 'IB:' || new.block_id::text),
      'subject_id', new.subject_id,
      'block_type', new.block_type,
      'understanding_state', new.understanding_state,
      'source_event_ids', to_jsonb(new.source_event_ids),
      'evidence_refs', new.evidence_refs,
      'schema_version', new.schema_version,
      'intelligent_block_v1', v_block,
      'intelligent_block_hash', v_block->'integrity'->>'content_hash',
      'source_context', v_source_context,
      'provenance', v_provenance,
      'privacy_state', coalesce(v_block->'context'->>'visibility', new.owner_scope),
      'verified_at', v_block->'lifecycle'->>'verified_at',
      'block_truth', v_block->'truth',
      'block_authority', v_block->'authority',
      'block_value', v_block->'value',
      'block_lifecycle', v_block->'lifecycle',
      'block_integrity', v_block->'integrity'
    )
  )
  on conflict(owner_id, source_table, source_id)
  do update set
    object_type = excluded.object_type,
    title = excluded.title,
    event_time = excluded.event_time,
    updated_at = excluded.updated_at,
    status = excluded.status,
    revision = excluded.revision,
    metadata = excluded.metadata;

  return new;
end;
$function$;

drop trigger if exists nayanet_intelligent_block_to_intelligence_index
  on public.nayanet_intelligent_blocks;

create trigger nayanet_intelligent_block_to_intelligence_index
after insert or update on public.nayanet_intelligent_blocks
for each row
execute function public.nayanet_intelligent_block_to_intelligence_index();
