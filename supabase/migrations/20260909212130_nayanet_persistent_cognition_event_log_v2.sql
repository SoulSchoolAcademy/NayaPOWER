create table if not exists public.nayanet_cognition_events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null,
  event_id text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  type text not null default 'intelligence',
  classification text not null default 'observation',
  title text,
  content text not null,
  source text not null default 'nayanet-hub',
  status text not null default 'active',
  actor text not null default 'human',
  confidence numeric not null default 1,
  tags jsonb not null default '[]'::jsonb,
  parent_event_id text,
  source_hash text not null,
  schema_version text not null default '1.0.0',
  receipt_id text not null,
  metadata jsonb not null default '{}'::jsonb,
  unique(user_id, project_id, event_id)
);

create index if not exists nayanet_cognition_events_user_project_time_idx on public.nayanet_cognition_events(user_id, project_id, created_at desc);
create index if not exists nayanet_cognition_events_classification_idx on public.nayanet_cognition_events(user_id, project_id, classification);
create index if not exists nayanet_cognition_events_status_idx on public.nayanet_cognition_events(user_id, project_id, status);

alter table public.nayanet_cognition_events enable row level security;
drop policy if exists nayanet_cognition_events_owner on public.nayanet_cognition_events;
create policy nayanet_cognition_events_owner on public.nayanet_cognition_events for all using (user_id = auth.uid()) with check (user_id = auth.uid());

create or replace function public.nayanet_initialize_cognition(p_project_id text, p_state jsonb default '{}'::jsonb)
returns public.nayanet_project_cognition_state
language plpgsql
security invoker
set search_path = public
as $$
declare v public.nayanet_project_cognition_state;
begin
  insert into public.nayanet_project_cognition_state(user_id, project_id, revision, state, status)
  values(auth.uid(), p_project_id, 0, coalesce(p_state,'{}'::jsonb), 'active')
  on conflict (user_id, project_id) do nothing;
  select * into v from public.nayanet_project_cognition_state where user_id=auth.uid() and project_id=p_project_id;
  return v;
end;
$$;

create or replace function public.nayanet_record_cognition_event(
  p_project_id text,
  p_event jsonb,
  p_action text default 'record_intelligence',
  p_expected_result text default null,
  p_observed_result text default null,
  p_learning jsonb default '[]'::jsonb
)
returns jsonb
language plpgsql
security invoker
set search_path = public
as $$
declare v_event public.nayanet_cognition_events; v_state public.nayanet_project_cognition_state; v_receipt public.nayanet_execution_receipts;
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;
  insert into public.nayanet_cognition_events(user_id,project_id,event_id,created_at,updated_at,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata)
  values(auth.uid(),p_project_id,p_event->>'event_id',coalesce((p_event->>'created_at')::timestamptz,now()),now(),coalesce(p_event->>'type','intelligence'),coalesce(p_event->>'classification','observation'),p_event->>'title',coalesce(p_event->>'content',''),coalesce(p_event->>'source','nayanet-hub'),coalesce(p_event->>'status','active'),coalesce(p_event->>'actor','human'),coalesce((p_event->>'confidence')::numeric,1),coalesce(p_event->'tags','[]'::jsonb),p_event->>'parent_event_id',coalesce(p_event->>'source_hash',''),coalesce(p_event->>'schema_version','1.0.0'),coalesce(p_event->>'receipt_id',''),coalesce(p_event->'metadata','{}'::jsonb))
  on conflict (user_id,project_id,event_id) do update set updated_at=now(), status=excluded.status, metadata=excluded.metadata
  returning * into v_event;

  insert into public.nayanet_project_cognition_state(user_id,project_id,revision,state,status)
  values(auth.uid(),p_project_id,0,jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at,'successor',null),'active')
  on conflict (user_id,project_id) do nothing;

  update public.nayanet_project_cognition_state set revision=revision+1, state=coalesce(state,'{}'::jsonb) || jsonb_build_object('last_event_id',v_event.event_id,'last_event_at',v_event.created_at), updated_at=now() where user_id=auth.uid() and project_id=p_project_id returning * into v_state;

  insert into public.nayanet_execution_receipts(user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning)
  values(auth.uid(),p_project_id,v_state.revision,p_action,p_expected_result,p_observed_result,'verified',jsonb_build_object('event_id',v_event.event_id,'source_hash',v_event.source_hash,'created_at',v_event.created_at),coalesce(p_learning,'[]'::jsonb)) returning * into v_receipt;

  return jsonb_build_object('event',to_jsonb(v_event),'state',to_jsonb(v_state),'receipt',to_jsonb(v_receipt));
end;
$$;

create or replace function public.nayanet_create_successor_handoff(p_project_id text, p_handoff jsonb)
returns public.nayanet_project_cognition_state
language plpgsql
security invoker
set search_path = public
as $$
declare v public.nayanet_project_cognition_state;
begin
  update public.nayanet_project_cognition_state
  set revision=revision+1,state=coalesce(state,'{}'::jsonb)||jsonb_build_object('successor',p_handoff),updated_at=now()
  where user_id=auth.uid() and project_id=p_project_id returning * into v;
  if not found then raise exception 'COGNITION_NOT_INITIALIZED'; end if;
  insert into public.nayanet_execution_receipts(user_id,project_id,revision,action,status,evidence,learning)
  values(auth.uid(),p_project_id,v.revision,'successor_handoff','verified',jsonb_build_object('handoff_id',p_handoff->>'handoff_id','last_event_id',p_handoff->>'last_event_id'),jsonb_build_array('successor state persisted'));
  return v;
end;
$$;
