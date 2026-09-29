create sequence if not exists public.nayanet_smart_note_ib_identity_seq;

alter table public.nayanet_intelligent_blocks
  add column if not exists intelligent_block_id text;

with ranked as (
  select block_id,
         2 + row_number() over(order by created_at asc, block_id asc) as n
  from public.nayanet_intelligent_blocks
)
update public.nayanet_intelligent_blocks b
set intelligent_block_id='IB-' || lpad(r.n::text,6,'0')
from ranked r
where r.block_id=b.block_id
  and b.intelligent_block_id is null;

select setval(
  'public.nayanet_smart_note_ib_identity_seq',
  greatest(
    2,
    coalesce((
      select max((substring(intelligent_block_id from 4))::bigint)
      from public.nayanet_intelligent_blocks
      where intelligent_block_id ~ '^IB-[0-9]{6}$'
    ),2)
  ),
  true
);

alter table public.nayanet_intelligent_blocks
  alter column intelligent_block_id set default ('IB-' || lpad(nextval('public.nayanet_smart_note_ib_identity_seq')::text,6,'0'));

alter table public.nayanet_intelligent_blocks
  alter column intelligent_block_id set not null;

do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname='nayanet_intelligent_blocks_intelligent_block_id_format'
  ) then
    alter table public.nayanet_intelligent_blocks
      add constraint nayanet_intelligent_blocks_intelligent_block_id_format
      check (intelligent_block_id ~ '^IB-[0-9]{6}$');
  end if;
end $$;

create unique index if not exists nayanet_intelligent_blocks_intelligent_block_id_uidx
  on public.nayanet_intelligent_blocks(intelligent_block_id);

CREATE OR REPLACE FUNCTION public.v7_create_smart_note(p_idempotency_key text, p_user_id uuid, p_human_note jsonb, p_naya_note jsonb, p_machine_note jsonb, p_intelligent_feed jsonb, p_intelligent_block jsonb, p_evidence jsonb, p_hub_state jsonb, p_subject text DEFAULT NULL::text)
 RETURNS v7_smart_note_transactions
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'extensions'
AS $function$
declare
  v_row public.v7_smart_note_transactions;
  v_event_id uuid;
  v_intelligent_block_id text;
  v_now timestamptz := now();
  v_verification jsonb;
  v_subject text;
  v_artifact_urls jsonb := coalesce(p_evidence->'artifact_urls','{}'::jsonb);
  v_receipt_url text := nullif(trim(coalesce(p_evidence->>'receipt_url','')), '');
  v_smart_note_receipt_id uuid;
  v_block_hash text;
  v_human_note jsonb;
  v_naya_note jsonb;
  v_machine_note jsonb;
  v_intelligent_feed jsonb;
  v_intelligent_block jsonb;
  v_evidence jsonb;
  v_hub_state jsonb;
begin
  if auth.uid() is null or p_user_id is distinct from auth.uid() then
    raise exception 'SMART_NOTE_USER_MISMATCH';
  end if;

  if coalesce(trim(p_idempotency_key),'')='' then
    raise exception 'SMART_NOTE_IDEMPOTENCY_KEY_REQUIRED';
  end if;

  if p_human_note is null
     or p_naya_note is null
     or p_machine_note is null
     or p_intelligent_feed is null
     or p_intelligent_block is null
     or p_evidence is null
     or p_hub_state is null then
    raise exception 'SMART_NOTE_PIPELINE_PAYLOAD_INCOMPLETE';
  end if;

  select *
    into v_row
    from public.v7_smart_note_transactions
   where idempotency_key=p_idempotency_key
     and user_id=auth.uid()
   limit 1;

  if found then
    if coalesce(trim(v_row.machine_note->>'event_id'),'') ~
       '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$' then
      perform public.verify_smart_note((v_row.machine_note->>'event_id')::uuid);
    end if;
    return v_row;
  end if;

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
    else gen_random_uuid()
  end;

  v_intelligent_block_id := 'IB-' || lpad(nextval('public.nayanet_smart_note_ib_identity_seq')::text,6,'0');

  v_human_note := p_human_note || jsonb_build_object('event_id',v_event_id);
  v_naya_note := p_naya_note || jsonb_build_object('event_id',v_event_id);
  v_machine_note := p_machine_note || jsonb_build_object('event_id',v_event_id);
  v_intelligent_feed := p_intelligent_feed || jsonb_build_object('event_id',v_event_id);
  v_intelligent_block := p_intelligent_block || jsonb_build_object(
    'block_id',v_event_id,
    'identity',coalesce(p_intelligent_block->'identity','{}'::jsonb) || jsonb_build_object(
      'object_id',v_intelligent_block_id,
      'event_id',v_event_id::text,
      'version',1,
      'namespace','nayanet',
      'schema_version','NAYANET_INTELLIGENT_BLOCK_V1',
      'intelligent_block_id',v_intelligent_block_id
    )
  );
  v_evidence := p_evidence || jsonb_build_object('event_id',v_event_id);
  v_hub_state := p_hub_state || jsonb_build_object('event_id',v_event_id);

  v_subject := nullif(trim(coalesce(p_subject,'')), '');
  if v_subject is null then
    v_subject := nullif(trim(coalesce(v_human_note->>'subject','')), '');
  end if;

  if v_subject is null then
    v_subject := left(
      regexp_replace(
        coalesce(v_human_note->>'text',v_human_note->>'content','Smart Note'),
        '\s+',
        ' ',
        'g'
      ),
      160
    );
  end if;

  insert into public.smart_note_events(
    id,member_id,subject,event_type,source_context,privacy_state,status,created_at
  )
  values(
    v_event_id,
    auth.uid(),
    v_subject,
    'SMART_NOTE',
    jsonb_build_object(
      'idempotency_key',p_idempotency_key,
      'source',coalesce(v_machine_note->>'source','naya_conversation'),
      'captured_at',v_now
    ),
    'PRIVATE',
    'INCOMPLETE',
    v_now
  );

  insert into public.smart_note_artifacts(
    event_id,artifact_type,content,artifact_url,created_at
  )
  values
    (v_event_id,'HUMAN_NOTE',coalesce(v_human_note->>'content',v_human_note->>'text',v_human_note::text),nullif(v_artifact_urls->>'human',''),v_now),
    (v_event_id,'NAYA_NOTE',coalesce(v_naya_note->>'content',v_naya_note->>'text',v_naya_note::text),nullif(v_artifact_urls->>'naya',''),v_now),
    (v_event_id,'MACHINE_NOTE',v_machine_note::text,nullif(v_artifact_urls->>'machine',''),v_now),
    (v_event_id,'INTELLIGENCE_FEED_NOTE',coalesce(v_intelligent_feed->>'summary',v_intelligent_feed->>'text',v_intelligent_feed::text),nullif(v_artifact_urls->>'feed',''),v_now);

  v_verification := public.verify_smart_note(v_event_id);

  if coalesce(v_verification->>'status','') <> 'VERIFIED' then
    raise exception 'SMART_NOTE_VERIFICATION_FAILED:%',v_verification::text;
  end if;

  insert into public.smart_note_receipts(
    event_id,status,receipt_url,verification,created_at
  )
  values(
    v_event_id,
    'VERIFIED',
    v_receipt_url,
    v_verification || jsonb_build_object('receipt_created_at',v_now),
    v_now
  )
  on conflict(event_id) do update
    set status='VERIFIED',
        receipt_url=excluded.receipt_url,
        verification=excluded.verification
  returning id into v_smart_note_receipt_id;

  -- Finalize the V1 envelope only after canonical verification and the domain
  -- receipt exist. This makes the integrity hash cover the persisted lineage.
  v_intelligent_block := jsonb_set(
    v_intelligent_block,
    '{evidence,evidence_refs}',
    jsonb_build_array(v_event_id::text,v_smart_note_receipt_id::text),
    true
  );
  v_intelligent_block := jsonb_set(
    v_intelligent_block,
    '{evidence,verification}',
    to_jsonb('Canonical Smart Note verification completed with persisted domain receipt.'::text),
    true
  );
  v_intelligent_block := jsonb_set(
    v_intelligent_block,
    '{lifecycle,stage}',
    to_jsonb('VERIFIED'::text),
    true
  );
  v_intelligent_block := jsonb_set(
    v_intelligent_block,
    '{lifecycle,verified_at}',
    to_jsonb(v_now),
    true
  );
  v_intelligent_block := jsonb_set(
    v_intelligent_block,
    '{lifecycle,updated_at}',
    to_jsonb(v_now),
    true
  );
  v_intelligent_block := jsonb_set(
    v_intelligent_block,
    '{metadata,smart_note_receipt_id}',
    to_jsonb(v_smart_note_receipt_id::text),
    true
  );
  v_intelligent_block := jsonb_set(
    v_intelligent_block,
    '{metadata,transport_finalized_at}',
    to_jsonb(v_now),
    true
  );
  v_intelligent_block := v_intelligent_block - 'integrity';
  v_block_hash := encode(extensions.digest(v_intelligent_block::text,'sha256'),'hex');
  v_intelligent_block := v_intelligent_block || jsonb_build_object(
    'integrity',
    jsonb_build_object(
      'algorithm','SHA-256',
      'content_hash',v_block_hash
    )
  );

  -- Put the finalized envelope back into the canonical Smart Note context.
  -- The existing cognition trigger then carries the same envelope into
  -- cognition/index/Hub projections. No new store is introduced.
  update public.smart_note_events
     set source_context = coalesce(source_context,'{}'::jsonb) ||
       jsonb_build_object(
         'intelligent_block_v1',v_intelligent_block,
         'intelligent_block_schema','NAYANET_INTELLIGENT_BLOCK_V1',
         'intelligent_block_hash',v_block_hash,
         'smart_note_receipt_id',v_smart_note_receipt_id::text
       )
   where id=v_event_id;

  v_evidence := v_evidence || jsonb_build_object(
    'intelligent_block_hash',v_block_hash,
    'smart_note_receipt_id',v_smart_note_receipt_id
  );
  v_hub_state := v_hub_state || jsonb_build_object(
    'intelligent_block_created',true,
    'intelligent_block_schema','NAYANET_INTELLIGENT_BLOCK_V1',
    'intelligent_block_hash',v_block_hash,
    'feed_updated',true
  );

  insert into public.v7_smart_note_transactions(
    idempotency_key,user_id,status,human_note,naya_note,machine_note,
    intelligent_feed,intelligent_block,evidence,hub_state
  )
  values(
    p_idempotency_key,
    auth.uid(),
    'completed',
    v_human_note,
    v_naya_note,
    v_machine_note,
    v_intelligent_feed,
    v_intelligent_block,
    v_evidence || jsonb_build_object('verified_at',v_now),
    v_hub_state || jsonb_build_object('last_intelligence_event_at',v_now)
  )
  returning * into v_row;

  return v_row;
end;
$function$
;

CREATE OR REPLACE FUNCTION public.nayanet_upsert_intelligent_block_from_smart_note(p_transaction v7_smart_note_transactions)
 RETURNS nayanet_intelligent_blocks
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'extensions'
AS $function$
declare
  v_event_id uuid;
  v_block_id uuid;
  v_intelligent_block_id text;
  v_block jsonb:=coalesce(p_transaction.intelligent_block,'{}'::jsonb);
  v_evidence jsonb:=coalesce(p_transaction.evidence,'{}'::jsonb);
  v_row public.nayanet_intelligent_blocks;
  v_event_status text;
begin
  v_event_id:=nullif(coalesce(v_evidence->>'event_id',v_block->>'block_id',''),'')::uuid;
  if v_event_id is null then raise exception 'INTELLIGENT_BLOCK_SOURCE_EVENT_REQUIRED'; end if;
  v_block_id:=nullif(coalesce(v_block->>'block_id',v_event_id::text),'')::uuid;
  if v_block_id is null then raise exception 'INTELLIGENT_BLOCK_ID_REQUIRED'; end if;
  v_intelligent_block_id:=nullif(coalesce(v_block->>'intelligent_block_id',v_block->'identity'->>'object_id'),'');
  select status into v_event_status from public.smart_note_events where id=v_event_id;
  insert into public.nayanet_intelligent_blocks(
    block_id,intelligent_block_id,owner_id,subject_id,title,block_type,version,status,understanding_state,owner_scope,
    source_event_ids,evidence_refs,provenance,value_context,applicable_scope,content,created_at,updated_at,schema_version)
  values(
    v_block_id,v_intelligent_block_id,p_transaction.user_id,
    coalesce(nullif(v_block->>'subject',''),'Smart Note'),
    coalesce(nullif(v_block->>'subject',''),'Intelligent Block'),
    coalesce(nullif(v_block->>'type',''),'OTHER_GOVERNED'),1,
    case when lower(coalesce(v_block->>'status',''))='preserved' then 'DURABLE' else 'ACTIVE' end,
    case when v_event_status='VERIFIED' then 'VERIFIED' else 'CANDIDATE' end,
    coalesce(nullif(v_block->>'privacy',''),'PRIVATE'),array[v_event_id],
    jsonb_build_array(jsonb_build_object('source_table','smart_note_events','source_id',v_event_id::text,'receipt_id',v_evidence->>'receipt_id','verified_at',v_evidence->>'verified_at','chain',coalesce(v_evidence->'chain','[]'::jsonb))),
    jsonb_build_object('source','smart_note','idempotency_key',p_transaction.idempotency_key,'canonical_event_id',v_event_id,'created_from','v7_create_smart_note'),
    jsonb_build_object('usefulness','reusable understanding','confidence',case when v_event_status='VERIFIED' then 1 else 0 end),
    jsonb_build_object('privacy',coalesce(v_block->>'privacy','PRIVATE')),v_block,
    coalesce(nullif(v_block->>'created_at','')::timestamptz,now()),now(),'INTELLIGENT_BLOCK_V1')
  on conflict(block_id) do update set
    owner_id=excluded.owner_id,subject_id=excluded.subject_id,title=excluded.title,block_type=excluded.block_type,
    status=excluded.status,understanding_state=excluded.understanding_state,owner_scope=excluded.owner_scope,
    source_event_ids=excluded.source_event_ids,evidence_refs=excluded.evidence_refs,provenance=excluded.provenance,
    value_context=excluded.value_context,applicable_scope=excluded.applicable_scope,content=excluded.content,
    updated_at=now(),schema_version='INTELLIGENT_BLOCK_V1',
    intelligent_block_id=coalesce(excluded.intelligent_block_id,nayanet_intelligent_blocks.intelligent_block_id)
  returning * into v_row;
  return v_row;
end;
$function$
;
