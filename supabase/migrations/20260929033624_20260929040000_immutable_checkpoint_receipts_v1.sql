create table if not exists public.nayanet_checkpoint_receipts (
  checkpoint_id uuid primary key,
  user_id uuid not null,
  project_id text not null,
  revision bigint not null,
  checkpoint_type text not null,
  status text not null,
  state jsonb not null,
  source_receipt_id uuid,
  learning_id uuid,
  event_id uuid,
  intelligent_block_id text,
  lineage_id uuid,
  relationship_id uuid,
  index_id uuid,
  content_hash text not null,
  recorded_at timestamptz not null default now()
);

create or replace function public.nayanet_checkpoint_receipts_immutable()
returns trigger language plpgsql as $$
begin
  if TG_OP <> 'INSERT' then
    raise exception 'CHECKPOINT_RECEIPT_IMMUTABLE';
  end if;
  return NEW;
end;
$$;

drop trigger if exists nayanet_checkpoint_receipts_immutable on public.nayanet_checkpoint_receipts;
create trigger nayanet_checkpoint_receipts_immutable
before update or delete on public.nayanet_checkpoint_receipts
for each row execute function public.nayanet_checkpoint_receipts_immutable();

insert into public.nayanet_checkpoint_receipts (
  checkpoint_id,user_id,project_id,revision,checkpoint_type,status,state,
  source_receipt_id,learning_id,event_id,intelligent_block_id,lineage_id,
  relationship_id,index_id,content_hash
)
select
  (r.evidence->>'checkpoint_id')::uuid,
  (r.evidence->>'owner_id')::uuid,
  r.project_id,
  r.revision,
  'COGNITIVE_CHECKPOINT',
  'LEARNED',
  jsonb_build_object(
    'checkpoint_id', r.evidence->>'checkpoint_id',
    'revision', r.revision,
    'status', 'LEARNED',
    'target_id', r.evidence->>'target_id',
    'event_id', r.evidence->>'event_row_id',
    'event_key', r.evidence->>'event_id',
    'intelligent_block_id', r.evidence->>'intelligent_block_id',
    'block_row_id', r.evidence->>'block_row_id',
    'lineage_id', r.evidence->>'lineage_id',
    'relationship_id', r.evidence->>'relationship_id',
    'index_id', r.evidence->>'index_id',
    'receipt_id', r.id,
    'learning_id', '65b93cdb-3981-4504-badd-a38861ffb971',
    'learning_claim', l.claim,
    'learning_status', l.status,
    'learning_provenance', l.provenance,
    'provenance_preserved', true,
    'causal_verification_id', 'CVO-NAYA-NODE-0001-FRESH-LEARNING-2026-09-28'
  ),
  r.id,
  l.id,
  (r.evidence->>'event_row_id')::uuid,
  r.evidence->>'intelligent_block_id',
  (r.evidence->>'lineage_id')::uuid,
  (r.evidence->>'relationship_id')::uuid,
  (r.evidence->>'index_id')::uuid,
  encode(digest(
    jsonb_build_object(
      'checkpoint_id', r.evidence->>'checkpoint_id',
      'revision', r.revision,
      'target_id', r.evidence->>'target_id',
      'event_id', r.evidence->>'event_row_id',
      'intelligent_block_id', r.evidence->>'intelligent_block_id',
      'lineage_id', r.evidence->>'lineage_id',
      'relationship_id', r.evidence->>'relationship_id',
      'index_id', r.evidence->>'index_id',
      'receipt_id', r.id,
      'learning_id', l.id,
      'learning_claim', l.claim,
      'learning_status', l.status,
      'learning_provenance', l.provenance
    )::text, 'sha256'), 'hex')
from public.nayanet_execution_receipts r
join public.learning_evidence l
  on l.id = '65b93cdb-3981-4504-badd-a38861ffb971'
where r.id = '32ff7884-e44b-46fc-84d2-682cd6f00161'
on conflict (checkpoint_id) do nothing;

create index if not exists nayanet_checkpoint_receipts_learning_idx
  on public.nayanet_checkpoint_receipts(learning_id);
