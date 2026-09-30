-- Durable checkpoint receipts V2
--
-- The live cognition row is intentionally mutable current state. Historical
-- proof must therefore be carried by the existing immutable checkpoint
-- evidence ledger, not by treating nayanet_project_cognition_state as history.
--
-- This migration makes the existing ledger multi-revision and records one
-- immutable snapshot whenever the canonical cognition revision advances.
-- It does not create a second state system: current state remains
-- nayanet_project_cognition_state; this table remains evidence/provenance only.

alter table public.nayanet_checkpoint_receipts
  add column if not exists checkpoint_receipt_id uuid not null default gen_random_uuid();

alter table public.nayanet_checkpoint_receipts
  drop constraint if exists nayanet_checkpoint_receipts_pkey;

do $$
begin
  if not exists (
    select 1
      from pg_constraint
     where conrelid = 'public.nayanet_checkpoint_receipts'::regclass
       and conname = 'nayanet_checkpoint_receipts_pkey'
  ) then
    alter table public.nayanet_checkpoint_receipts
      add constraint nayanet_checkpoint_receipts_pkey
      primary key (checkpoint_receipt_id);
  end if;
end
$$;

create unique index if not exists nayanet_checkpoint_receipts_owner_project_revision_uidx
  on public.nayanet_checkpoint_receipts(user_id, project_id, revision);

create index if not exists nayanet_checkpoint_receipts_checkpoint_idx
  on public.nayanet_checkpoint_receipts(checkpoint_id);

create unique index if not exists nayanet_checkpoint_receipts_source_receipt_uidx
  on public.nayanet_checkpoint_receipts(source_receipt_id)
  where source_receipt_id is not null;

create or replace function public.nayanet_record_checkpoint_receipt()
returns trigger
language plpgsql
security definer
set search_path = ''
as $function$
declare
  v_state jsonb;
  v_source_receipt_id uuid;
  v_learning_id uuid;
  v_event_id uuid;
  v_lineage_id uuid;
  v_relationship_id uuid;
  v_index_id uuid;
  v_hash text;
begin
  -- Same-revision mutations are current-state refinement, not a new checkpoint.
  -- Only a revision transition creates a durable historical checkpoint receipt.
  if TG_OP = 'UPDATE' and NEW.revision = OLD.revision then
    return NEW;
  end if;

  v_state := coalesce(NEW.state, '{}'::jsonb) || jsonb_build_object(
    'checkpoint_id', NEW.id,
    'revision', NEW.revision,
    'project_id', NEW.project_id,
    'owner_id', NEW.user_id,
    'row_status', NEW.status
  );

  v_source_receipt_id := nullif(v_state->>'receipt_id','')::uuid;
  v_learning_id := nullif(v_state->>'learning_id','')::uuid;
  v_event_id := nullif(coalesce(v_state->>'latest_event_id', v_state->>'event_id'),'')::uuid;
  v_lineage_id := nullif(v_state->>'lineage_id','')::uuid;
  v_relationship_id := nullif(v_state->>'relationship_id','')::uuid;
  v_index_id := nullif(v_state->>'index_id','')::uuid;
  v_hash := encode(extensions.digest(v_state::text, 'sha256'), 'hex');

  insert into public.nayanet_checkpoint_receipts(
    checkpoint_id,
    user_id,
    project_id,
    revision,
    checkpoint_type,
    status,
    state,
    source_receipt_id,
    learning_id,
    event_id,
    intelligent_block_id,
    lineage_id,
    relationship_id,
    index_id,
    content_hash
  )
  values(
    NEW.id,
    NEW.user_id,
    NEW.project_id,
    NEW.revision,
    coalesce(v_state->>'checkpoint_type','COGNITIVE_CHECKPOINT'),
    coalesce(v_state->>'status',NEW.status),
    v_state,
    v_source_receipt_id,
    v_learning_id,
    v_event_id,
    nullif(v_state->>'intelligent_block_id',''),
    v_lineage_id,
    v_relationship_id,
    v_index_id,
    v_hash
  )
  on conflict (user_id, project_id, revision) do nothing;

  return NEW;
end;
$function$;

drop trigger if exists nayanet_record_checkpoint_receipt_trg
  on public.nayanet_project_cognition_state;

create trigger nayanet_record_checkpoint_receipt_trg
after insert or update of revision, state, status
on public.nayanet_project_cognition_state
for each row execute function public.nayanet_record_checkpoint_receipt();

-- Record the currently authoritative revision once so the ledger begins with a
-- durable snapshot immediately on upgrade. Existing historical backfill rows
-- remain untouched.
insert into public.nayanet_checkpoint_receipts(
  checkpoint_id,user_id,project_id,revision,checkpoint_type,status,state,
  source_receipt_id,learning_id,event_id,intelligent_block_id,lineage_id,
  relationship_id,index_id,content_hash
)
select
  s.id,
  s.user_id,
  s.project_id,
  s.revision,
  coalesce(s.state->>'checkpoint_type','COGNITIVE_CHECKPOINT'),
  coalesce(s.state->>'status',s.status),
  coalesce(s.state,'{}'::jsonb) || jsonb_build_object(
    'checkpoint_id',s.id,
    'revision',s.revision,
    'project_id',s.project_id,
    'owner_id',s.user_id,
    'row_status',s.status
  ),
  nullif(s.state->>'receipt_id','')::uuid,
  nullif(s.state->>'learning_id','')::uuid,
  nullif(coalesce(s.state->>'latest_event_id',s.state->>'event_id'),'')::uuid,
  nullif(s.state->>'intelligent_block_id',''),
  nullif(s.state->>'lineage_id','')::uuid,
  nullif(s.state->>'relationship_id','')::uuid,
  nullif(s.state->>'index_id','')::uuid,
  encode(extensions.digest(
    (coalesce(s.state,'{}'::jsonb) || jsonb_build_object(
      'checkpoint_id',s.id,
      'revision',s.revision,
      'project_id',s.project_id,
      'owner_id',s.user_id,
      'row_status',s.status
    ))::text,
    'sha256'
  ),'hex')
from public.nayanet_project_cognition_state s
on conflict (user_id, project_id, revision) do nothing;

alter function public.nayanet_record_checkpoint_receipt()
  set search_path = '';

revoke execute on function public.nayanet_record_checkpoint_receipt()
  from public, anon, authenticated;

grant execute on function public.nayanet_record_checkpoint_receipt()
  to service_role;
