-- 23514 FIX: supersede path must pass a non-empty source_event_ids.
--
-- Root cause (proven first-hand by the captain, 2026-11-12 ~09:3xZ):
-- every supersede call fails with SQLSTATE 23514 (check_violation) because
-- the supersede wrapper (migration 20261001000100, line 99) passes
-- '{}'::uuid[] as p_source_event_ids to the inner writer, and the table
-- CHECK (migration 20260922012715, line 22) requires
-- cardinality(source_event_ids) > 0. cardinality('{}') = 0, so the insert
-- of the new block fails deterministically on every supersede call, while
-- commits succeed (the commit writer passes a 1-element array).
--
-- Fix shape (B) -- inner-writer fallback, recommended in the gate verdict:
-- in nayanet_supersede_intelligent_block, when the caller passes an empty
-- (or NULL) source_event_ids array, fall back to old_row.source_event_ids.
-- The successor inherits the predecessor's source events, which preserves
-- lineage. This fixes it for ALL callers, not just the wrapper.
--
-- Depends on:
--   20260930040000_r1_writer_connections_v1.sql
--     (PROMOTED_V1 -- the current definition of the inner writer, verified
--     byte-identical to live main, blob 08bbc24278add67b47b588023988edec12927bb9)
--
-- This migration does exactly ONE thing: CREATE OR REPLACE the inner writer
-- with the fallback added. It changes no other function, no other migration,
-- no table, no CHECK, no workflow, no registry file, no feed file. In
-- particular it does NOT drop or relax the CHECK -- the constraint is doing
-- its job; the writer was violating it.
--
-- CREATE OR REPLACE preserves the function's existing grants, so no
-- revoke/grant lines are needed here. The comment on the function is
-- restated verbatim from PROMOTED_V1.
--
-- Proof boundary: this migration is proven correct without touching
-- production (real Postgres parse + a line-by-line diff against the live
-- PROMOTED_V1 body + a logic test of the empty-array path -- see the round
-- record). Applying it to production goes through the governed deploy path
-- and waits for Shawn's tap; the migration's success on production is the
-- final confirmation and is NOT this round's.

create or replace function public.nayanet_supersede_intelligent_block(
  p_superseded_block_id uuid,p_new_block_id uuid,p_owner_id uuid,p_subject_id text,p_title text,p_block_type text,
  p_understanding_state text,p_owner_scope text,p_source_event_ids uuid[],p_evidence_refs jsonb,p_provenance jsonb,
  p_value_context jsonb,p_applicable_scope jsonb,p_content jsonb,p_schema_version text,p_idempotency_key text,
  p_intelligent_block_id text default null,p_connections jsonb default null
) returns public.nayanet_intelligent_blocks
language plpgsql security definer set search_path = public, extensions
as $function$
declare
  old_row public.nayanet_intelligent_blocks;
  existing_row public.nayanet_intelligent_blocks;
  new_row public.nayanet_intelligent_blocks;
  v_new_ib_id text;
  v_new_connections jsonb;
  v_supersede_edge jsonb;
  v_source_event_ids uuid[];
begin
  if auth.uid() is null or auth.uid() <> p_owner_id then raise exception 'INTELLIGENT_BLOCK_OWNER_AUTH_REQUIRED'; end if;
  if p_superseded_block_id is null or p_new_block_id is null then raise exception 'INTELLIGENT_BLOCK_IDS_REQUIRED'; end if;
  if p_superseded_block_id = p_new_block_id then raise exception 'INTELLIGENT_BLOCK_SELF_SUPERSEDE_FORBIDDEN'; end if;
  if p_idempotency_key is null or btrim(p_idempotency_key)='' then raise exception 'INTELLIGENT_BLOCK_IDEMPOTENCY_KEY_REQUIRED'; end if;
  select * into existing_row from public.nayanet_intelligent_blocks where block_id=p_new_block_id and owner_id=p_owner_id;
  if found then
    if coalesce(existing_row.provenance->>'idempotency_key','')<>p_idempotency_key then raise exception 'INTELLIGENT_BLOCK_IDEMPOTENCY_KEY_MISMATCH'; end if;
    return existing_row;
  end if;
  select * into old_row from public.nayanet_intelligent_blocks where block_id=p_superseded_block_id and owner_id=p_owner_id for update;
  if not found then raise exception 'INTELLIGENT_BLOCK_TO_SUPERSEDE_NOT_FOUND'; end if;
  if old_row.superseded_by_block_id is not null and old_row.superseded_by_block_id<>p_new_block_id then raise exception 'INTELLIGENT_BLOCK_ALREADY_SUPERSEDED'; end if;

  -- 23514 FIX (shape B): inherit the old block's source events when the
  -- caller passes none. The supersede wrapper passes '{}'::uuid[] on every
  -- call, and the table CHECK requires cardinality(source_event_ids) > 0,
  -- so an empty (or NULL) array fails the insert with SQLSTATE 23514.
  -- old_row.source_event_ids is non-empty by that same CHECK on the old
  -- row, so the insert can no longer violate it through this path.
  -- A caller-supplied non-empty array is kept verbatim.
  v_source_event_ids := case
    when coalesce(array_length(p_source_event_ids, 1), 0) > 0 then p_source_event_ids
    else old_row.source_event_ids
  end;

  -- Hazard fix: explicit IB id, else fresh sequence id (see §6 header).
  v_new_ib_id := nullif(btrim(coalesce(p_intelligent_block_id,'')),'');
  if v_new_ib_id is null then
    v_new_ib_id := 'IB-' || lpad(nextval('public.nayanet_smart_note_ib_identity_seq')::text,6,'0');
  end if;
  if v_new_ib_id !~ '^IB-[0-9]{6}$' then raise exception 'INTELLIGENT_BLOCK_ID_FORMAT_INVALID'; end if;

  v_new_connections := public.nayanet_normalize_block_connections(coalesce(p_connections,'[]'::jsonb), p_owner_id);

  insert into public.nayanet_intelligent_blocks(
    block_id,intelligent_block_id,owner_id,subject_id,title,block_type,version,status,understanding_state,owner_scope,source_event_ids,evidence_refs,
    provenance,value_context,applicable_scope,content,connections,supersedes_block_id,superseded_by_block_id,created_at,updated_at,schema_version
  ) values (
    p_new_block_id,v_new_ib_id,p_owner_id,coalesce(p_subject_id,old_row.subject_id),coalesce(p_title,old_row.title),coalesce(p_block_type,old_row.block_type),
    old_row.version+1,'ACTIVE',coalesce(p_understanding_state,'CANDIDATE'),coalesce(p_owner_scope,old_row.owner_scope),v_source_event_ids,
    coalesce(p_evidence_refs,'[]'::jsonb),
    coalesce(p_provenance,'{}'::jsonb)||jsonb_build_object(
      'supersedes_block_id',old_row.block_id,
      'supersedes_intelligent_block_id',old_row.intelligent_block_id,
      'supersedes_version',old_row.version,
      'idempotency_key',p_idempotency_key,
      'supersession_writer_version','PROMOTED_V1',
      'promoted_from','supabase/history/pre-production-ledger-reconciliation-20260929/20260923000000_intelligent_block_supersession_lifecycle_v1.sql'
    ),
    coalesce(p_value_context,old_row.value_context),coalesce(p_applicable_scope,old_row.applicable_scope),coalesce(p_content,old_row.content),
    v_new_connections,
    old_row.block_id,null,now(),now(),coalesce(p_schema_version,old_row.schema_version)
  ) returning * into new_row;

  -- Canonical edge row (system of record) + old-row projection, atomically.
  insert into public.nayanet_brain_relationships(
    relationship_id,owner_id,source_id,target_id,relationship_type,provenance,epistemic_state
  ) values (
    gen_random_uuid(),p_owner_id,
    old_row.intelligent_block_id,v_new_ib_id,'SUPERSEDES',
    jsonb_build_object(
      'superseded_block_id',old_row.block_id,
      'superseding_block_id',p_new_block_id,
      'idempotency_key',p_idempotency_key,
      'writer','nayanet_supersede_intelligent_block:PROMOTED_V1'
    ),
    'CANDIDATE'
  )
  on conflict (owner_id,source_id,target_id,relationship_type) do nothing;

  v_supersede_edge := jsonb_build_array(
    jsonb_build_object('target_block_id',v_new_ib_id,'relationship_type','SUPERSEDES')
  );
  update public.nayanet_intelligent_blocks
     set status='SUPERSEDED',
         superseded_by_block_id=p_new_block_id,
         connections=public.nayanet_normalize_block_connections(
           coalesce(connections,'[]'::jsonb) || v_supersede_edge,
           p_owner_id
         ),
         updated_at=now()
   where block_id=old_row.block_id and owner_id=p_owner_id;

  return new_row;
end;
$function$;

comment on function public.nayanet_supersede_intelligent_block(uuid,uuid,uuid,text,text,text,text,text,uuid[],jsonb,jsonb,jsonb,jsonb,jsonb,text,text,text,jsonb) is
  'R1 writer contract PROMOTED_V1: idempotent block supersession with durable lineage. Hazard fix: intelligent_block_id is explicit-or-fresh-sequence (never omitted, never reused, never suffixed -- see migration header §6). Stamps the SUPERSEDES edge onto the old row connections projection and the canonical nayanet_brain_relationships row atomically (ONE GRAPH).';
