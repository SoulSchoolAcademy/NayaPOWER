-- EVENT_ID_REPLAY idempotency repair.
-- Same key + same payload + complete lineage => reread original canonical result.
-- Changed payload or incomplete lineage => fail closed. No replay path writes.
-- Authority validation remains before replay reconciliation.

create or replace function public.nayanet_intelligence_commit(
  p_event_id text, p_title text, p_content text, p_category text, p_topic text, p_target_id text,
  p_authority_grant_id uuid, p_project_id text default 'NayaNET', p_connections jsonb default null,
  p_capabilities text[] default null)
returns jsonb language plpgsql security definer set search_path=''
as $function$
declare
  uid uuid := auth.uid(); authority jsonb; receipt_id uuid := gen_random_uuid(); event_row uuid := gen_random_uuid();
  block_row uuid := gen_random_uuid(); intelligent_id text := 'IB-' || regexp_replace(p_event_id, '[^A-Za-z0-9_-]', '-', 'g');
  revision bigint; lineage_row uuid; index_row uuid; relationship_row uuid; state_row uuid; content_hash text;
  v_connections jsonb;
  v_elem jsonb;
  v_capabilities text[];
  v_cap_raw text;
  v_cap_norm text;
  v_content jsonb;
  v_provenance jsonb;
  v_existing_event public.nayanet_cognition_events;
  v_existing_block public.nayanet_intelligent_blocks;
  v_existing_receipt public.nayanet_execution_receipts;
begin
  if uid is null then raise exception using errcode='42501', message='AUTH_REQUIRED'; end if;
  if coalesce(trim(p_event_id),'')='' or coalesce(trim(p_title),'')='' or coalesce(trim(p_content),'')='' or coalesce(trim(p_category),'')='' or coalesce(trim(p_topic),'')='' or coalesce(trim(p_target_id),'')='' then
    raise exception using errcode='22023', message='LESSON_FIELDS_REQUIRED';
  end if;
  -- AI1: bounded capability validation. Fail closed: any unknown or malformed
  -- entry rejects the whole commit (a typo must never silently produce an
  -- un-retrievable block, and an unknown name must never silently broaden what
  -- the selector can match). Absent or empty -> v_capabilities stays null ->
  -- the block persists byte-identical to pre-repair commits.
  v_capabilities := null;
  if p_capabilities is not null then
    if coalesce(array_length(p_capabilities, 1), 0) > 0 then
      v_capabilities := '{}';
      foreach v_cap_raw in array p_capabilities loop
        if v_cap_raw is null then
          raise exception using errcode='22023', message='CAPABILITY_MALFORMED:null-entry';
        end if;
        v_cap_norm := lower(trim(v_cap_raw));
        if v_cap_norm = '' or v_cap_norm !~ '^[a-z][a-z0-9_]*$' then
          raise exception using errcode='22023', message='CAPABILITY_MALFORMED:' || left(v_cap_raw, 64);
        end if;
        -- Bounded vocabulary mirror (canonical: capability-vocabulary.ts).
        if v_cap_norm <> all (array['governance_triage','compounding_capture']) then
          raise exception using errcode='22023', message='CAPABILITY_UNKNOWN:' || v_cap_norm;
        end if;
        if v_cap_norm <> all (v_capabilities) then
          v_capabilities := v_capabilities || v_cap_norm;
        end if;
      end loop;
      -- Deterministic persisted representation: deduped, sorted.
      select array_agg(x order by x) into v_capabilities from unnest(v_capabilities) as x;
    end if;
  end if;
  authority := public.nayanet_validate_authority_grant(p_authority_grant_id,'intelligence_commit',p_target_id);
  if authority->>'status' <> 'AUTHORIZED' then raise exception using errcode='42501', message='AUTHORITY_BLOCKED:'||coalesce(authority->>'reason','UNKNOWN'); end if;
  if (authority->>'subject_id')::uuid <> uid then raise exception using errcode='42501', message='AUTHORITY_SUBJECT_MISMATCH'; end if;
  -- Exact replay is an idempotent reread, never a second write.
  select * into v_existing_event
  from public.nayanet_cognition_events
  where user_id=uid and project_id=p_project_id and event_id=p_event_id
  limit 1;

  if found then
    content_hash := encode(extensions.digest(p_content,'sha256'),'hex');
    v_connections := public.nayanet_normalize_block_connections(coalesce(p_connections,'[]'::jsonb), uid);
    v_content := jsonb_build_object('lesson',p_content,'topic',p_topic,'category',p_category);
    if v_capabilities is not null then
      v_content := v_content || jsonb_build_object('capabilities', to_jsonb(v_capabilities));
    end if;

    if v_existing_event.source_hash is distinct from content_hash
       or v_existing_event.title is distinct from p_title
       or v_existing_event.content is distinct from p_content
       or v_existing_event.metadata->>'target_id' is distinct from p_target_id then
      raise exception using errcode='23505', message='EVENT_ID_REPLAY_PAYLOAD_MISMATCH';
    end if;

    select * into v_existing_block
    from public.nayanet_intelligent_blocks
    where owner_id=uid
      and intelligent_block_id=intelligent_id
      and v_existing_event.id = any(source_event_ids)
    limit 1;

    if not found then
      raise exception using errcode='P0001', message='EVENT_ID_REPLAY_INCOMPLETE:BLOCK_MISSING';
    end if;

    if v_existing_block.title is distinct from p_title
       or v_existing_block.subject_id is distinct from p_target_id
       or v_existing_block.content is distinct from v_content
       or coalesce(v_existing_block.connections,'[]'::jsonb) is distinct from v_connections then
      raise exception using errcode='23505', message='EVENT_ID_REPLAY_PAYLOAD_MISMATCH';
    end if;

    select * into v_existing_receipt
    from public.nayanet_execution_receipts
    where id::text=v_existing_event.receipt_id
      and user_id=uid
      and project_id=p_project_id
    limit 1;

    if not found
       or v_existing_receipt.status <> 'SUCCESS'
       or v_existing_receipt.action <> 'intelligence_commit'
       or v_existing_receipt.evidence->>'event_row_id' is distinct from v_existing_event.id::text
       or v_existing_receipt.evidence->>'content_hash' is distinct from content_hash
       or v_existing_receipt.evidence->>'intelligent_block_id' is distinct from intelligent_id
       or v_existing_receipt.evidence->>'block_row_id' is distinct from v_existing_block.block_id::text then
      raise exception using errcode='P0001', message='EVENT_ID_REPLAY_INCOMPLETE:RECEIPT_MISMATCH';
    end if;

    if coalesce(v_existing_receipt.evidence->>'lineage_id','')=''
       or coalesce(v_existing_receipt.evidence->>'relationship_id','')=''
       or coalesce(v_existing_receipt.evidence->>'index_id','')=''
       or coalesce(v_existing_receipt.evidence->>'checkpoint_id','')='' then
      raise exception using errcode='P0001', message='EVENT_ID_REPLAY_INCOMPLETE:EVIDENCE_IDS_MISSING';
    end if;

    if not exists(
      select 1 from public.nayanet_intelligence_lineage l
      where l.id=(v_existing_receipt.evidence->>'lineage_id')::uuid
        and l.user_id=uid and l.project_id=p_project_id
        and l.source_event_id=v_existing_event.id
    ) then
      raise exception using errcode='P0001', message='EVENT_ID_REPLAY_INCOMPLETE:LINEAGE_MISSING';
    end if;

    if not exists(
      select 1 from public.nayanet_brain_relationships br
      where br.relationship_id=(v_existing_receipt.evidence->>'relationship_id')::uuid
        and br.owner_id=uid and br.target_id=intelligent_id
    ) then
      raise exception using errcode='P0001', message='EVENT_ID_REPLAY_INCOMPLETE:RELATIONSHIP_MISSING';
    end if;

    if not exists(
      select 1 from public.nayanet_intelligence_index ix
      where ix.id=(v_existing_receipt.evidence->>'index_id')::uuid
        and ix.owner_id=uid and ix.project_id=p_project_id
        and ix.source_id=v_existing_block.block_id
    ) then
      raise exception using errcode='P0001', message='EVENT_ID_REPLAY_INCOMPLETE:INDEX_MISSING';
    end if;

    if not exists(
      select 1 from public.nayanet_project_cognition_state st
      where st.id=(v_existing_receipt.evidence->>'checkpoint_id')::uuid
        and st.user_id=uid and st.project_id=p_project_id
    ) then
      raise exception using errcode='P0001', message='EVENT_ID_REPLAY_INCOMPLETE:CHECKPOINT_MISSING';
    end if;

    return jsonb_build_object(
      'ok',true,'schema','NAYANET_INTELLIGENCE_COMMIT_V1',
      'receipt_id',v_existing_receipt.id,'event_id',v_existing_event.id,'event_key',p_event_id,
      'intelligent_block_id',intelligent_id,'block_row_id',v_existing_block.block_id,
      'lineage_id',(v_existing_receipt.evidence->>'lineage_id')::uuid,
      'relationship_id',(v_existing_receipt.evidence->>'relationship_id')::uuid,
      'index_id',(v_existing_receipt.evidence->>'index_id')::uuid,
      'checkpoint_id',(v_existing_receipt.evidence->>'checkpoint_id')::uuid,
      'revision',v_existing_receipt.revision,
      'understanding_state',v_existing_block.understanding_state,
      'authority_grant_id',p_authority_grant_id,'content_hash',content_hash,
      'reconciled_replay',true,'replay_status','REUSED_EXISTING_CANONICAL_LINEAGE'
    );
  end if;
  perform pg_advisory_xact_lock(hashtext(uid::text || ':' || p_project_id)::bigint);
  select coalesce(max(r.revision),0)+1 into revision from public.nayanet_execution_receipts r where r.user_id=uid and r.project_id=p_project_id;
  insert into public.nayanet_execution_receipts(id,user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning)
  values(receipt_id,uid,p_project_id,revision,'intelligence_commit','Persist one fresh lesson as connected canonical intelligence.','Lesson persisted as event, Intelligent Block, lineage, relationship, index, and checkpoint.','SUCCESS',
    jsonb_build_object('event_id',p_event_id,'target_id',p_target_id,'authority_grant_id',p_authority_grant_id,'authority',authority,'stage','PERSIST'),'[]'::jsonb);
  content_hash := encode(extensions.digest(p_content,'sha256'),'hex');
  insert into public.nayanet_cognition_events(id,user_id,project_id,event_id,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata)
  values(event_row,uid,p_project_id,p_event_id,'intelligence','teaching',p_title,p_content,'nayanet','active','human',1,jsonb_build_array('fresh-lesson','intelligence_commit','canonical'),null,content_hash,'1.0.0',receipt_id::text,
    jsonb_build_object('target_id',p_target_id,'authority_grant_id',p_authority_grant_id,'epistemic_state','CANDIDATE'));
  v_connections := public.nayanet_normalize_block_connections(coalesce(p_connections,'[]'::jsonb), uid);
  -- AI1: canonical capability storage location = content.capabilities.
  -- When no capabilities were declared, v_content is byte-identical to the
  -- pre-repair shape {lesson,topic,category}.
  v_content := jsonb_build_object('lesson',p_content,'topic',p_topic,'category',p_category);
  v_provenance := jsonb_build_object('stage','CAPTURE+PERSIST','source','nayanet','authority_grant_id',p_authority_grant_id,'source_event_id',event_row);
  if v_capabilities is not null then
    v_content := v_content || jsonb_build_object('capabilities', to_jsonb(v_capabilities));
    -- Declaration provenance: where the capability tag came from. The ONLY
    -- accepted source is the intelligence_commit capture payload.
    v_provenance := v_provenance || jsonb_build_object('capability_declaration',
      jsonb_build_object('source','intelligence_commit_capture','values',to_jsonb(v_capabilities)));
  end if;
  insert into public.nayanet_intelligent_blocks(block_id,intelligent_block_id,owner_id,subject_id,title,block_type,version,status,understanding_state,owner_scope,source_event_ids,evidence_refs,provenance,value_context,applicable_scope,content,connections,schema_version)
  values(block_row,intelligent_id,uid,p_target_id,p_title,'GOVERNED_INTELLIGENCE',1,'DURABLE','CANDIDATE','PRIVATE',array[event_row],
    jsonb_build_array(jsonb_build_object('receipt_id',receipt_id,'event_id',event_row,'source_hash',content_hash)),
    v_provenance,
    jsonb_build_object('epistemic_state','CANDIDATE'),jsonb_build_object('target',p_target_id,'project_id',p_project_id),
    v_content,v_connections,'INTELLIGENT_BLOCK_V1');
  insert into public.nayanet_intelligence_lineage(id,project_id,user_id,source_event_id,relation,target_event_id,reason,evidence_refs)
  values(gen_random_uuid(),p_project_id,uid,event_row,'CREATED_INTELLIGENT_BLOCK',event_row,'Fresh lesson became a canonical Intelligent Block through intelligence_commit.',jsonb_build_array(receipt_id,event_row,block_row))
  returning id into lineage_row;
  insert into public.nayanet_brain_relationships(relationship_id,owner_id,source_id,target_id,relationship_type,provenance,epistemic_state)
  values(gen_random_uuid(),uid,'NAYA-KERNEL-KNOW',intelligent_id,'PRODUCES',jsonb_build_object('source_event_id',event_row,'lineage_id',lineage_row,'receipt_id',receipt_id,'authority_grant_id',p_authority_grant_id,'reason','Canonical KNOW ownership of the persisted lesson.'),'CANDIDATE')
  returning relationship_id into relationship_row;
  for v_elem in select * from jsonb_array_elements(v_connections)
  loop
    insert into public.nayanet_brain_relationships(
      relationship_id,owner_id,source_id,target_id,relationship_type,provenance,epistemic_state
    )
    values(
      gen_random_uuid(),uid,intelligent_id,v_elem->>'target_block_id',upper(v_elem->>'relationship_type'),
      jsonb_build_object('source_event_id',event_row,'block_row_id',block_row,'receipt_id',receipt_id,'authority_grant_id',p_authority_grant_id,'writer','nayanet_intelligence_commit:R1_CONNECTION'),
      'CANDIDATE'
    )
    on conflict (owner_id,source_id,target_id,relationship_type) do nothing;
  end loop;
  insert into public.nayanet_intelligence_index(id,owner_id,source_table,source_id,object_type,title,event_time,status,project_id,revision,metadata)
  values(gen_random_uuid(),uid,'nayanet_intelligent_blocks',block_row,'INTELLIGENT_BLOCK',p_title,clock_timestamp(),'DURABLE',p_project_id,revision,jsonb_build_object('event_id',event_row,'intelligent_block_id',intelligent_id,'lineage_id',lineage_row,'relationship_id',relationship_row,'understanding_state','CANDIDATE','receipt_id',receipt_id))
  returning id into index_row;
  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(uid,p_project_id,revision,jsonb_build_object('checkpoint_type','COGNITIVE_CHECKPOINT','status','CANDIDATE','latest_event_id',event_row,'latest_event_key',p_event_id,'intelligent_block_id',intelligent_id,'lineage_id',lineage_row,'relationship_id',relationship_row,'index_id',index_row,'receipt_id',receipt_id,'target_id',p_target_id,'provenance_preserved',true),'READY')
  on conflict(user_id,project_id) do update set revision=excluded.revision,state=excluded.state,status=excluded.status,updated_at=clock_timestamp()
  returning id into state_row;
  -- AI1: record the declared capabilities on the immutable commit receipt so
  -- the declaration itself is historically reconstructible (#1170 anchoring).
  -- Null-safe: no capabilities -> evidence identical to pre-repair.
  update public.nayanet_execution_receipts set evidence=evidence||jsonb_build_object('event_row_id',event_row,'intelligent_block_id',intelligent_id,'block_row_id',block_row,'lineage_id',lineage_row,'relationship_id',relationship_row,'index_id',index_row,'checkpoint_id',state_row,'content_hash',content_hash)
    || case when v_capabilities is not null then jsonb_build_object('declared_capabilities', to_jsonb(v_capabilities)) else '{}'::jsonb end
    where id=receipt_id;
  return jsonb_build_object('ok',true,'schema','NAYANET_INTELLIGENCE_COMMIT_V1','receipt_id',receipt_id,'event_id',event_row,'event_key',p_event_id,'intelligent_block_id',intelligent_id,'block_row_id',block_row,'lineage_id',lineage_row,'relationship_id',relationship_row,'index_id',index_row,'checkpoint_id',state_row,'revision',revision,'understanding_state','CANDIDATE','authority_grant_id',p_authority_grant_id,'content_hash',content_hash);
end;
$function$;

revoke all on function public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text,jsonb,text[]) from public,anon;
grant execute on function public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text,jsonb,text[]) to authenticated;
