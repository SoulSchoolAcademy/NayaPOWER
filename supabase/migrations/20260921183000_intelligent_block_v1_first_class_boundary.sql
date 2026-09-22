-- Intelligent Block V1 first-class persistence/retrieval boundary.
-- Reuses canonical Smart Note event identity and the existing Intelligence Index.
create table if not exists public.nayanet_intelligent_blocks (
  block_id uuid primary key,
  owner_id uuid not null references auth.users(id) on delete cascade,
  subject_id text not null,
  title text not null,
  block_type text not null,
  version bigint not null default 1 check (version > 0),
  status text not null default 'ACTIVE' check (status in ('ACTIVE','DURABLE','SUPERSEDED','RELEASED','DELETED')),
  understanding_state text not null default 'CANDIDATE' check (understanding_state in ('CANDIDATE','CONTEXTUALIZED','INTERPRETED','VERIFIED','DISTILLED','APPLIED','LEARNED','SUPERSEDED')),
  owner_scope text not null default 'PRIVATE',
  source_event_ids uuid[] not null,
  evidence_refs jsonb not null default '[]'::jsonb,
  provenance jsonb not null default '{}'::jsonb,
  value_context jsonb not null default '{}'::jsonb,
  applicable_scope jsonb not null default '{}'::jsonb,
  content jsonb not null default '{}'::jsonb,
  supersedes_block_id uuid null references public.nayanet_intelligent_blocks(block_id),
  superseded_by_block_id uuid null references public.nayanet_intelligent_blocks(block_id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  schema_version text not null default 'INTELLIGENT_BLOCK_V1',
  constraint nayanet_intelligent_blocks_source_events_nonempty check (cardinality(source_event_ids) > 0),
  constraint nayanet_intelligent_blocks_evidence_array check (jsonb_typeof(evidence_refs)='array')
);
create index if not exists nayanet_intelligent_blocks_owner_updated_idx on public.nayanet_intelligent_blocks(owner_id,updated_at desc);
create index if not exists nayanet_intelligent_blocks_subject_idx on public.nayanet_intelligent_blocks(owner_id,subject_id);
create index if not exists nayanet_intelligent_blocks_source_event_idx on public.nayanet_intelligent_blocks using gin(source_event_ids);
alter table public.nayanet_intelligent_blocks enable row level security;
drop policy if exists nayanet_intelligent_blocks_owner_select on public.nayanet_intelligent_blocks;
create policy nayanet_intelligent_blocks_owner_select on public.nayanet_intelligent_blocks for select to authenticated using (owner_id=auth.uid());

create or replace function public.nayanet_upsert_intelligent_block_from_smart_note(p_transaction public.v7_smart_note_transactions)
returns public.nayanet_intelligent_blocks
language plpgsql security definer set search_path=public,extensions as $$
declare v_event_id uuid; v_block_id uuid; v_block jsonb:=coalesce(p_transaction.intelligent_block,'{}'::jsonb); v_evidence jsonb:=coalesce(p_transaction.evidence,'{}'::jsonb); v_row public.nayanet_intelligent_blocks; v_event_status text;
begin
  v_event_id:=nullif(coalesce(v_evidence->>'event_id',v_block->>'block_id',''),'')::uuid;
  if v_event_id is null then raise exception 'INTELLIGENT_BLOCK_SOURCE_EVENT_REQUIRED'; end if;
  v_block_id:=nullif(coalesce(v_block->>'block_id',v_event_id::text),'')::uuid;
  if v_block_id is null then raise exception 'INTELLIGENT_BLOCK_ID_REQUIRED'; end if;
  select status into v_event_status from public.smart_note_events where id=v_event_id;
  insert into public.nayanet_intelligent_blocks(block_id,owner_id,subject_id,title,block_type,version,status,understanding_state,owner_scope,source_event_ids,evidence_refs,provenance,value_context,applicable_scope,content,created_at,updated_at,schema_version)
  values(v_block_id,p_transaction.user_id,coalesce(nullif(v_block->>'subject',''),'Smart Note'),coalesce(nullif(v_block->>'subject',''),'Intelligent Block'),coalesce(nullif(v_block->>'type',''),'OTHER_GOVERNED'),1,case when lower(coalesce(v_block->>'status',''))='preserved' then 'DURABLE' else 'ACTIVE' end,case when v_event_status='VERIFIED' then 'VERIFIED' else 'CANDIDATE' end,coalesce(nullif(v_block->>'privacy',''),'PRIVATE'),array[v_event_id],jsonb_build_array(jsonb_build_object('source_table','smart_note_events','source_id',v_event_id::text,'receipt_id',v_evidence->>'receipt_id','verified_at',v_evidence->>'verified_at','chain',coalesce(v_evidence->'chain','[]'::jsonb))),jsonb_build_object('source','smart_note','idempotency_key',p_transaction.idempotency_key,'canonical_event_id',v_event_id,'created_from','v7_create_smart_note'),jsonb_build_object('usefulness','reusable understanding','confidence',case when v_event_status='VERIFIED' then 1 else 0 end),jsonb_build_object('privacy',coalesce(v_block->>'privacy','PRIVATE')),v_block,coalesce(nullif(v_block->>'created_at','')::timestamptz,now()),now(),'INTELLIGENT_BLOCK_V1')
  on conflict(block_id) do update set owner_id=excluded.owner_id,subject_id=excluded.subject_id,title=excluded.title,block_type=excluded.block_type,status=excluded.status,understanding_state=excluded.understanding_state,owner_scope=excluded.owner_scope,source_event_ids=excluded.source_event_ids,evidence_refs=excluded.evidence_refs,provenance=excluded.provenance,value_context=excluded.value_context,applicable_scope=excluded.applicable_scope,content=excluded.content,updated_at=now(),schema_version='INTELLIGENT_BLOCK_V1'
  returning * into v_row;
  return v_row;
end;
$$;
revoke execute on function public.nayanet_upsert_intelligent_block_from_smart_note(public.v7_smart_note_transactions) from public,anon,authenticated;

create or replace function public.nayanet_smart_note_transaction_to_intelligent_block()
returns trigger language plpgsql security definer set search_path=public,extensions as $$
begin perform public.nayanet_upsert_intelligent_block_from_smart_note(new); return new; end;
$$;
revoke execute on function public.nayanet_smart_note_transaction_to_intelligent_block() from public,anon,authenticated;
drop trigger if exists nayanet_smart_note_transaction_to_intelligent_block on public.v7_smart_note_transactions;
create trigger nayanet_smart_note_transaction_to_intelligent_block after insert or update of intelligent_block,evidence,status on public.v7_smart_note_transactions for each row execute function public.nayanet_smart_note_transaction_to_intelligent_block();

create or replace function public.nayanet_get_intelligent_block(p_block_id uuid)
returns public.nayanet_intelligent_blocks language sql stable security invoker set search_path=public as $$
select * from public.nayanet_intelligent_blocks where block_id=p_block_id and owner_id=auth.uid()
$$;

create or replace function public.nayanet_intelligent_block_to_intelligence_index()
returns trigger language plpgsql security definer set search_path=public as $$
begin
  insert into public.nayanet_intelligence_index(owner_id,source_table,source_id,object_type,title,event_time,created_at,updated_at,status,project_id,revision,metadata)
  values(new.owner_id,'nayanet_intelligent_blocks',new.block_id,'INTELLIGENT_BLOCK',new.title,new.created_at,new.created_at,new.updated_at,new.status,'NayaNET',new.version,jsonb_build_object('subject_id',new.subject_id,'block_type',new.block_type,'understanding_state',new.understanding_state,'source_event_ids',new.source_event_ids,'evidence_refs',new.evidence_refs,'schema_version',new.schema_version))
  on conflict(owner_id,source_table,source_id) do update set object_type=excluded.object_type,title=excluded.title,event_time=excluded.event_time,updated_at=excluded.updated_at,status=excluded.status,revision=excluded.revision,metadata=excluded.metadata;
  return new;
end;
$$;
drop trigger if exists nayanet_intelligent_block_to_intelligence_index on public.nayanet_intelligent_blocks;
create trigger nayanet_intelligent_block_to_intelligence_index after insert or update on public.nayanet_intelligent_blocks for each row execute function public.nayanet_intelligent_block_to_intelligence_index();
