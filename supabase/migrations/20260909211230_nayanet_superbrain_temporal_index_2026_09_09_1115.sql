create table if not exists public.nayanet_intelligence_index (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  source_table text not null,
  source_id uuid not null,
  object_type text not null,
  title text,
  event_time timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  status text,
  project_id text,
  revision bigint,
  metadata jsonb not null default '{}'::jsonb,
  unique(owner_id, source_table, source_id)
);

create index if not exists nayanet_intelligence_index_owner_time_idx on public.nayanet_intelligence_index(owner_id, event_time desc nulls last, updated_at desc);
create index if not exists nayanet_intelligence_index_owner_type_idx on public.nayanet_intelligence_index(owner_id, object_type, updated_at desc);
create index if not exists nayanet_intelligence_index_project_idx on public.nayanet_intelligence_index(owner_id, project_id, updated_at desc);

alter table public.nayanet_intelligence_index enable row level security;
drop policy if exists nayanet_intelligence_index_owner on public.nayanet_intelligence_index;
create policy nayanet_intelligence_index_owner on public.nayanet_intelligence_index for select to authenticated using (owner_id = auth.uid());

create or replace function public.nayanet_index_intelligence_row() returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  j jsonb := to_jsonb(new);
  v_owner uuid;
  v_project text;
  v_revision bigint;
  v_title text;
  v_status text;
  v_type text;
  v_event timestamptz;
  v_created timestamptz;
  v_updated timestamptz;
begin
  v_owner := coalesce(nullif(j->>'user_id','')::uuid, nullif(j->>'member_id','')::uuid);
  if v_owner is null then return new; end if;
  v_project := j->>'project_id';
  v_revision := nullif(j->>'revision','')::bigint;
  v_status := j->>'status';
  v_created := coalesce(nullif(j->>'created_at','')::timestamptz, now());
  v_updated := coalesce(nullif(j->>'updated_at','')::timestamptz, v_created);
  v_event := coalesce(nullif(j->>'event_time','')::timestamptz, v_created);
  v_title := coalesce(j->>'subject', j->>'title', j->>'action', v_project, 'Intelligence event');
  v_type := case tg_table_name
    when 'nayanet_project_cognition_state' then 'STATE'
    when 'nayanet_execution_receipts' then 'RECEIPT'
    when 'nayanet_notes' then 'EVENT'
    when 'smart_note_events' then 'EVENT'
    when 'smart_note_receipts' then 'RECEIPT'
    else 'REFERENCE'
  end;
  insert into public.nayanet_intelligence_index(owner_id, source_table, source_id, object_type, title, event_time, created_at, updated_at, status, project_id, revision, metadata)
  values(v_owner, tg_table_name, new.id, v_type, v_title, v_event, v_created, v_updated, v_status, v_project, v_revision, j - 'id')
  on conflict(owner_id, source_table, source_id) do update set
    object_type=excluded.object_type,
    title=excluded.title,
    event_time=excluded.event_time,
    created_at=excluded.created_at,
    updated_at=excluded.updated_at,
    status=excluded.status,
    project_id=excluded.project_id,
    revision=excluded.revision,
    metadata=excluded.metadata;
  return new;
end;
$$;

revoke all on function public.nayanet_index_intelligence_row() from public;

 drop trigger if exists nayanet_index_cognition on public.nayanet_project_cognition_state;
 create trigger nayanet_index_cognition after insert or update on public.nayanet_project_cognition_state for each row execute function public.nayanet_index_intelligence_row();
 drop trigger if exists nayanet_index_receipt on public.nayanet_execution_receipts;
 create trigger nayanet_index_receipt after insert or update on public.nayanet_execution_receipts for each row execute function public.nayanet_index_intelligence_row();
 drop trigger if exists nayanet_index_note on public.nayanet_notes;
 create trigger nayanet_index_note after insert or update on public.nayanet_notes for each row execute function public.nayanet_index_intelligence_row();
 drop trigger if exists nayanet_index_smart_note_event on public.smart_note_events;
 create trigger nayanet_index_smart_note_event after insert or update on public.smart_note_events for each row execute function public.nayanet_index_intelligence_row();
 drop trigger if exists nayanet_index_smart_note_receipt on public.smart_note_receipts;
 create trigger nayanet_index_smart_note_receipt after insert or update on public.smart_note_receipts for each row execute function public.nayanet_index_intelligence_row();
