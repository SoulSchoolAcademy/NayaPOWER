-- R1 writer contract: block writers stamp canonical graph edges onto blocks at
-- write time, so the edge-aware retrieval seam (know.ts selectKnowContext,
-- PR #1094) has real edges to consume.
--
-- ONE GRAPH: nayanet_brain_relationships remains the system of record for
-- graph edges. The nayanet_intelligent_blocks.connections column added here
-- is a WRITE-TIME MATERIALIZED PROJECTION of a block's outbound edges --
-- written atomically in the same transaction as the canonical edge row --
-- not a second edge store. Retrieval reads the projection from the same
-- row/snapshot as the block (no TOCTOU re-fetch); writers derive it from
-- the canonical edge at write time.
--
-- Edge shape (row projection):
--   [{"target_block_id": "<intelligent_block_id IB-*>", "relationship_type": "<22-type>"}]
-- relationship_type is drawn from the canonical 22-type vocabulary mirrored
-- in BRAIN/00-SPEC/BRAIN-MACHINE-CONTRACT-V1.schema.json $defs.relationshipType
-- and in know.ts EDGE_VOCABULARY. target_block_id is the TARGET's
-- intelligent_block_id (the key know.ts builds its byId map on), never prose.
--
-- Additive only. Existing rows backfill to '[]' (no edges), which preserves
-- the pre-existing flat retrieval behavior byte-for-byte.

-- §1. The projection column.
alter table public.nayanet_intelligent_blocks
  add column if not exists connections jsonb not null default '[]'::jsonb;

comment on column public.nayanet_intelligent_blocks.connections is
  'R1 writer contract: write-time materialized projection of this block''s outbound graph edges as [{"target_block_id":"<IB-*>","relationship_type":"<22-type>"}]. System of record is nayanet_brain_relationships (ONE GRAPH); this column is derived at write time in the same transaction. Retrieval (know.ts) consumes it from the block snapshot.';

-- §2. Write-time normalization: candidate edges -> validated projection.
-- Accepts the capture shape {type,target} and the row shape
-- {relationship_type,target_block_id}. Drops anything that is not a real
-- edge: unknown/forged relationship types, empty targets, prose targets
-- that do not resolve to an intelligent_block_id owned by p_owner_id, and
-- duplicates. Writers MUST route connections through this function; the
-- guard trigger (§3) rejects malformed shape as a backstop.
create or replace function public.nayanet_normalize_block_connections(p_candidates jsonb, p_owner_id uuid)
returns jsonb
language plpgsql stable security definer set search_path = public
as $function$
declare
  v_out jsonb := '[]'::jsonb;
  v_elem jsonb;
  v_type text;
  v_target text;
  v_resolved text;
begin
  if p_candidates is null or jsonb_typeof(p_candidates) <> 'array' then
    return '[]'::jsonb;
  end if;
  for v_elem in select * from jsonb_array_elements(p_candidates)
  loop
    if jsonb_typeof(v_elem) <> 'object' then continue; end if;
    v_type := upper(btrim(coalesce(v_elem->>'relationship_type', v_elem->>'type', '')));
    v_target := btrim(coalesce(v_elem->>'target_block_id', v_elem->>'target', ''));
    if v_type not in (
      'DERIVED_FROM','SUPPORTS','CONTRADICTS','DEPENDS_ON','IMPLEMENTS','GOVERNS',
      'AUTHORIZED_BY','USED_BY','CAUSED','RESULTED_IN','VERIFIED_BY','LEARNED_FROM',
      'SUPERSEDES','SUCCEEDS','RELATED_TO','CONTEXTUALIZES','INVALIDATES','REFINES',
      'CORRECTS','ENABLES','PRODUCES','APPLIES_TO'
    ) then
      continue;
    end if;
    if v_target = '' then continue; end if;
    -- Target must be a real intelligent_block_id in the writer's owner scope.
    -- Prose targets and foreign-owner ids never become edges (fail closed).
    select b.intelligent_block_id into v_resolved
      from public.nayanet_intelligent_blocks b
     where b.intelligent_block_id = v_target
       and b.owner_id = p_owner_id
     limit 1;
    if v_resolved is null then continue; end if;
    if exists (
      select 1 from jsonb_array_elements(v_out) o
       where o.value->>'target_block_id' = v_resolved
         and o.value->>'relationship_type' = v_type
    ) then continue; end if;
    v_out := v_out || jsonb_build_array(
      jsonb_build_object('target_block_id', v_resolved, 'relationship_type', v_type)
    );
  end loop;
  return v_out;
end;
$function$;

comment on function public.nayanet_normalize_block_connections(jsonb, uuid) is
  'R1 writer contract: normalize candidate edges to the validated connections projection. Vocabulary-checked, owner-scoped target resolution, deduplicated.';

-- §3. Backstop guard: no writer (or ad-hoc SQL) may persist a malformed
-- projection. CHECK constraints cannot contain subqueries, so this is a
-- trigger. Shape only -- target resolution stays in the writers.
create or replace function public.nayanet_intelligent_blocks_connections_guard()
returns trigger
language plpgsql set search_path = public
as $function$
declare
  v_elem jsonb;
  v_type text;
begin
  if NEW.connections is null then
    raise exception 'INTELLIGENT_BLOCK_CONNECTIONS_REQUIRED';
  end if;
  if jsonb_typeof(NEW.connections) <> 'array' then
    raise exception 'INTELLIGENT_BLOCK_CONNECTIONS_MUST_BE_ARRAY';
  end if;
  for v_elem in select * from jsonb_array_elements(NEW.connections)
  loop
    if jsonb_typeof(v_elem) <> 'object' then
      raise exception 'INTELLIGENT_BLOCK_CONNECTION_MUST_BE_OBJECT';
    end if;
    if coalesce(btrim(v_elem->>'target_block_id'), '') = '' then
      raise exception 'INTELLIGENT_BLOCK_CONNECTION_TARGET_REQUIRED';
    end if;
    v_type := upper(btrim(coalesce(v_elem->>'relationship_type', '')));
    if v_type not in (
      'DERIVED_FROM','SUPPORTS','CONTRADICTS','DEPENDS_ON','IMPLEMENTS','GOVERNS',
      'AUTHORIZED_BY','USED_BY','CAUSED','RESULTED_IN','VERIFIED_BY','LEARNED_FROM',
      'SUPERSEDES','SUCCEEDS','RELATED_TO','CONTEXTUALIZES','INVALIDATES','REFINES',
      'CORRECTS','ENABLES','PRODUCES','APPLIES_TO'
    ) then
      raise exception 'INTELLIGENT_BLOCK_CONNECTION_UNKNOWN_TYPE:%', v_elem->>'relationship_type';
    end if;
  end loop;
  return NEW;
end;
$function$;

drop trigger if exists nayanet_intelligent_blocks_connections_guard_trg
  on public.nayanet_intelligent_blocks;
create trigger nayanet_intelligent_blocks_connections_guard_trg
  before insert or update of connections on public.nayanet_intelligent_blocks
  for each row execute function public.nayanet_intelligent_blocks_connections_guard();

-- §4. Legacy Smart Note compatibility is intentionally not modified here.
-- The current canonical write seam is nayanet_intelligence_commit; this
-- migration must not depend on the retired v7_smart_note_transactions row
-- type. Existing legacy objects, where present, remain untouched.
--
-- §5. Commit writer: stamp normalized connections. New optional trailing
-- parameter keeps the existing 8-argument call sites (incl. the runtime
-- bridge) working unchanged.
--
-- NOTE: the parameter list changes (p_connections appended), so this is a
-- new function signature, not an OR REPLACE of the old one. The old 8-arg
-- signature is dropped first; otherwise the bridge's 8-argument positional
-- call would keep resolving to the stale overload and the new parameter
-- would never take effect.
drop function if exists public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text);
create function public.nayanet_intelligence_commit(
  p_event_id text, p_title text, p_content text, p_category text, p_topic text, p_target_id text,
  p_authority_grant_id uuid, p_project_id text default 'NayaNET', p_connections jsonb default null)
returns jsonb language plpgsql security definer set search_path=''
as $function$
declare
  uid uuid := auth.uid(); authority jsonb; receipt_id uuid := gen_random_uuid(); event_row uuid := gen_random_uuid();
  block_row uuid := gen_random_uuid(); intelligent_id text := 'IB-' || regexp_replace(p_event_id, '[^A-Za-z0-9_-]', '-', 'g');
  revision bigint; lineage_row uuid; index_row uuid; relationship_row uuid; state_row uuid; content_hash text;
  v_connections jsonb;
begin
  if uid is null then raise exception using errcode='42501', message='AUTH_REQUIRED'; end if;
  if coalesce(trim(p_event_id),'')='' or coalesce(trim(p_title),'')='' or coalesce(trim(p_content),'')='' or coalesce(trim(p_category),'')='' or coalesce(trim(p_topic),'')='' or coalesce(trim(p_target_id),'')='' then
    raise exception using errcode='22023', message='LESSON_FIELDS_REQUIRED';
  end if;
  authority := public.nayanet_validate_authority_grant(p_authority_grant_id,'intelligence_commit',p_project_id);
  if authority->>'status' <> 'AUTHORIZED' then raise exception using errcode='42501', message='AUTHORITY_BLOCKED:'||coalesce(authority->>'reason','UNKNOWN'); end if;
  if (authority->>'subject_id')::uuid <> uid then raise exception using errcode='42501', message='AUTHORITY_SUBJECT_MISMATCH'; end if;
  if exists(select 1 from public.nayanet_cognition_events where user_id=uid and project_id=p_project_id and event_id=p_event_id) then raise exception using errcode='23505', message='EVENT_ID_REPLAY'; end if;
  select coalesce(max(r.revision),0)+1 into revision from public.nayanet_execution_receipts r where r.user_id=uid and r.project_id=p_project_id;
  insert into public.nayanet_execution_receipts(id,user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning)
  values(receipt_id,uid,p_project_id,revision,'intelligence_commit','Persist one fresh lesson as connected canonical intelligence.','Lesson persisted as event, Intelligent Block, lineage, relationship, index, and checkpoint.','SUCCESS',
    jsonb_build_object('event_id',p_event_id,'target_id',p_target_id,'authority_grant_id',p_authority_grant_id,'authority',authority,'stage','PERSIST'),'[]'::jsonb);
  content_hash := encode(digest(p_content,'sha256'),'hex');
  insert into public.nayanet_cognition_events(id,user_id,project_id,event_id,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata)
  values(event_row,uid,p_project_id,p_event_id,'intelligence','teaching',p_title,p_content,'nayanet','active','human',1,jsonb_build_array('fresh-lesson','intelligence_commit','canonical'),null,content_hash,'1.0.0',receipt_id::text,
    jsonb_build_object('target_id',p_target_id,'authority_grant_id',p_authority_grant_id,'epistemic_state','CANDIDATE'));
  v_connections := public.nayanet_normalize_block_connections(coalesce(p_connections,'[]'::jsonb), uid);
  insert into public.nayanet_intelligent_blocks(block_id,intelligent_block_id,owner_id,subject_id,title,block_type,version,status,understanding_state,owner_scope,source_event_ids,evidence_refs,provenance,value_context,applicable_scope,content,connections,schema_version)
  values(block_row,intelligent_id,uid,p_target_id,p_title,'GOVERNED_INTELLIGENCE',1,'DURABLE','CANDIDATE','PRIVATE',array[event_row],
    jsonb_build_array(jsonb_build_object('receipt_id',receipt_id,'event_id',event_row,'source_hash',content_hash)),
    jsonb_build_object('stage','CAPTURE+PERSIST','source','nayanet','authority_grant_id',p_authority_grant_id,'source_event_id',event_row),
    jsonb_build_object('epistemic_state','CANDIDATE'),jsonb_build_object('target',p_target_id,'project_id',p_project_id),
    jsonb_build_object('lesson',p_content,'topic',p_topic,'category',p_category),v_connections,'INTELLIGENT_BLOCK_V1');
  insert into public.nayanet_intelligence_lineage(id,project_id,user_id,source_event_id,relation,target_event_id,reason,evidence_refs)
  values(gen_random_uuid(),p_project_id,uid,event_row,'CREATED_INTELLIGENT_BLOCK',block_row,'Fresh lesson became a canonical Intelligent Block through intelligence_commit.',jsonb_build_array(receipt_id,event_row,block_row))
  returning id into lineage_row;
  insert into public.nayanet_brain_relationships(relationship_id,owner_id,source_id,target_id,relationship_type,provenance,epistemic_state)
  values(gen_random_uuid(),uid,'NAYA-KERNEL-KNOW',intelligent_id,'PRODUCES',jsonb_build_object('source_event_id',event_row,'lineage_id',lineage_row,'receipt_id',receipt_id,'authority_grant_id',p_authority_grant_id,'reason','Canonical KNOW ownership of the persisted lesson.'),'CANDIDATE')
  returning relationship_id into relationship_row;
  insert into public.nayanet_intelligence_index(id,owner_id,source_table,source_id,object_type,title,event_time,status,project_id,revision,metadata)
  values(gen_random_uuid(),uid,'nayanet_intelligent_blocks',block_row,'INTELLIGENT_BLOCK',p_title,clock_timestamp(),'DURABLE',p_project_id,revision,jsonb_build_object('event_id',event_row,'intelligent_block_id',intelligent_id,'lineage_id',lineage_row,'relationship_id',relationship_row,'understanding_state','CANDIDATE','receipt_id',receipt_id))
  returning id into index_row;
  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(uid,p_project_id,revision,jsonb_build_object('checkpoint_type','COGNITIVE_CHECKPOINT','status','CANDIDATE','latest_event_id',event_row,'latest_event_key',p_event_id,'intelligent_block_id',intelligent_id,'lineage_id',lineage_row,'relationship_id',relationship_row,'index_id',index_row,'receipt_id',receipt_id,'target_id',p_target_id,'provenance_preserved',true),'READY')
  on conflict(user_id,project_id) do update set revision=excluded.revision,state=excluded.state,status=excluded.status,updated_at=clock_timestamp()
  returning id into state_row;
  update public.nayanet_execution_receipts set evidence=evidence||jsonb_build_object('event_row_id',event_row,'intelligent_block_id',intelligent_id,'block_row_id',block_row,'lineage_id',lineage_row,'relationship_id',relationship_row,'index_id',index_row,'checkpoint_id',state_row,'content_hash',content_hash) where id=receipt_id;
  return jsonb_build_object('ok',true,'schema','NAYANET_INTELLIGENCE_COMMIT_V1','receipt_id',receipt_id,'event_id',event_row,'event_key',p_event_id,'intelligent_block_id',intelligent_id,'block_row_id',block_row,'lineage_id',lineage_row,'relationship_id',relationship_row,'index_id',index_row,'checkpoint_id',state_row,'revision',revision,'understanding_state','CANDIDATE','authority_grant_id',p_authority_grant_id,'content_hash',content_hash);
end;
$function$;

-- Re-assert the original grant posture on the new signature (the DROP above
-- removed the grant attached to the old signature).
revoke all on function public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text,jsonb) from public,anon;
grant execute on function public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text,jsonb) to authenticated;

-- §6. Supersession writer promotion (from pre-production history), with the
-- intelligent_block_id hazard FIXED and connections stamped.
--
-- HAZARD (Wave 2, Worker E): the pre-production writer's INSERT omitted
-- intelligent_block_id, a live NOT NULL + UNIQUE + format-checked
-- (^IB-[0-9]{6}$) column since 20260925042110. Promoting it verbatim would
-- let superseding rows fall through to the sequence default with no
-- IB-identity chain link, silently forking the IB-* identity that know.ts
-- keys on. The Wave-2 proposal's fallback (old_id || '-v' || version) is
-- INVALID against the live schema: it violates the format check. RESOLVED
-- BRANCH (recorded here per the proposal's rule): the caller may pass an
-- explicit p_intelligent_block_id; otherwise the writer mints a FRESH
-- sequence id ('IB-' || lpad(nextval(...),6,'0')). The IB-* chain is linked
-- via supersedes_block_id (uuid FK) + provenance.supersedes_intelligent_block_id.
-- Reusing the old row's IB id would violate the unique index; the '-v<N>'
-- suffix would violate the format check. There is no third option.
--
-- Connections: the writer stamps the SUPERSEDES edge onto the OLD row's
-- projection (this is what know.ts chaseSupersession follows) and writes
-- the canonical edge row to nayanet_brain_relationships in the same
-- transaction (ONE GRAPH: table is the system of record, the projection is
-- derived). The new row carries caller-supplied normalized connections
-- (default '[]').
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
    old_row.version+1,'ACTIVE',coalesce(p_understanding_state,'CANDIDATE'),coalesce(p_owner_scope,old_row.owner_scope),p_source_event_ids,
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

-- §7. Structural hardening: linear supersession chains (was plpgsql-only).
do $$
begin
  if not exists (select 1 from pg_constraint where conname='nayanet_intelligent_blocks_no_self_supersede') then
    alter table public.nayanet_intelligent_blocks
      add constraint nayanet_intelligent_blocks_no_self_supersede
      check (supersedes_block_id is null or supersedes_block_id <> block_id);
  end if;
end $$;

create unique index if not exists nayanet_intelligent_blocks_one_superseder_idx
  on public.nayanet_intelligent_blocks (superseded_by_block_id)
  where superseded_by_block_id is not null;

create index if not exists nayanet_intelligent_blocks_supersedes_chain_idx
  on public.nayanet_intelligent_blocks (owner_id, supersedes_block_id)
  where supersedes_block_id is not null;

-- §8. Grants: invocation via edge functions only, never direct client SQL.
-- (The writers are SECURITY DEFINER with their own owner-auth checks.)
revoke all on function public.nayanet_normalize_block_connections(jsonb,uuid) from public, anon, authenticated;
revoke all on function public.nayanet_supersede_intelligent_block(uuid,uuid,uuid,text,text,text,text,text,uuid[],jsonb,jsonb,jsonb,jsonb,jsonb,text,text,text,jsonb) from public, anon, authenticated;
grant execute on function public.nayanet_normalize_block_connections(jsonb,uuid) to service_role;
grant execute on function public.nayanet_supersede_intelligent_block(uuid,uuid,uuid,text,text,text,text,text,uuid[],jsonb,jsonb,jsonb,jsonb,jsonb,text,text,text,jsonb) to service_role;

-- §9. H3 writer-seam repair: open the connections channel through the
-- runtime bridge.
--
-- FIRST BROKEN EDGE (H3, verified 2026-09-30): nayanet_intelligence_commit_runtime
-- (defined in 20260928174822_nayanet_intelligence_runtime_bridge.sql) invoked
-- nayanet_intelligence_commit with 8 positional args, so the p_connections
-- parameter added in §5 was always NULL and every committed block stamped '[]'.
-- The repair widens the BRIDGE signature only: a new optional trailing
-- p_connections (default null) is forwarded as the 9th argument to the §5
-- commit defined earlier in this migration. The Edge Function RPC calls the
-- bridge by named params; omitting p_connections preserves byte-for-byte old
-- behavior ('[]'), so this is fully backward compatible. Caller-proposed
-- candidate edges are vocabulary-checked, owner-scoped, and deduplicated by
-- nayanet_normalize_block_connections (§2); the guard trigger (§3) rejects
-- malformed projections as a backstop.
--
-- DEPENDS ON §5: requires the 9-arg nayanet_intelligence_commit with
-- p_connections jsonb defined earlier in this migration. Nothing else in
-- this migration's §§1-8 semantics is changed by this section.
--
-- NO PRODUCER YET: nothing in the executable chain derives candidate edges
-- from block content. The producer that proposes p_connections values is the
-- named next seam; this section only opens the channel.
drop function if exists public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text);
create function public.nayanet_intelligence_commit_runtime(
  p_naya_id text,p_owner_id uuid,p_runtime_jti text,p_event_id text,p_title text,p_content text,p_category text,p_topic text,p_target_id text,p_authority_grant_id uuid,p_project_id text default 'NayaNET',p_connections jsonb default null
) returns jsonb language plpgsql security definer set search_path='' as $function$
declare grant_row record; result jsonb; receipt_id uuid;
begin
 if p_naya_id <> 'NAYA-NODE-0001' then raise exception using errcode='42501',message='NAYA_ID_NOT_AUTHORIZED'; end if;
 if coalesce(trim(p_runtime_jti),'')='' then raise exception using errcode='22023',message='RUNTIME_JTI_REQUIRED'; end if;
 select * into grant_row from public.nayanet_authority_grants
 where grant_id=p_authority_grant_id and issuer_id=p_owner_id and subject_id=p_owner_id and status='ACTIVE' and revoked_at is null
 and (expires_at is null or expires_at>clock_timestamp()) and scope->>'target'=p_naya_id and actions @> '["intelligence_commit"]'::jsonb;
 if not found then raise exception using errcode='42501',message='AUTHORITY_BLOCKED'; end if;
 perform set_config('request.jwt.claim.sub',p_owner_id::text,true);
 result:=public.nayanet_intelligence_commit(p_event_id,p_title,p_content,p_category,p_topic,p_target_id,p_authority_grant_id,p_project_id,p_connections);
 receipt_id:=(result->>'receipt_id')::uuid;
 update public.nayanet_execution_receipts set evidence=evidence||jsonb_build_object('runtime_identity','naya-node-oidc','naya_id',p_naya_id,'runtime_jti',p_runtime_jti,'owner_id',p_owner_id) where id=receipt_id;
 return result||jsonb_build_object('runtime_identity','naya-node-oidc','naya_id',p_naya_id,'runtime_jti',p_runtime_jti,'owner_id',p_owner_id);
end;$function$;

-- Re-assert the original grant posture on the new signature (the DROP above
-- removed the grant attached to the old 11-arg signature).
revoke all on function public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text,jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text,jsonb) to service_role;
