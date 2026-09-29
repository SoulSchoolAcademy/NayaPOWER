-- Canonical event-driven intelligence notification bus V1
-- Source: applied to managed Supabase project dahisasgpfvziswqvmvm on 2026-09-21.
-- No cron or GitHub Actions dependency. Execution receipts trigger notification creation.

create table if not exists public.nayanet_intelligence_notifications (
  id uuid primary key default gen_random_uuid(),
  event_id text not null unique,
  source_receipt_id uuid unique,
  source_cognition_event_id uuid,
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id text not null,
  event_type text not null,
  occurred_at timestamptz not null default now(),
  source_naya_id text not null default 'NAYA_RUNTIME',
  source_surface text not null default 'NayaPOWER',
  summary text not null,
  why_it_matters text not null default '',
  what_changed text not null default '',
  who_needs_to_know jsonb not null default '[]'::jsonb,
  recommendation text not null default '',
  authority_state text not null default 'UNCHANGED',
  evidence_state text not null default 'OBSERVED',
  visibility text not null default 'PRIVATE',
  briefing jsonb not null default '{}'::jsonb,
  canonical_day date not null default current_date,
  caused_by text,
  delivery_state text not null default 'PENDING',
  propagation_state text not null default 'PENDING',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.nayanet_intelligence_notification_deliveries (
  id uuid primary key default gen_random_uuid(),
  notification_id uuid not null references public.nayanet_intelligence_notifications(id) on delete cascade,
  event_id text not null,
  recipient_type text not null,
  recipient_key text not null,
  state text not null default 'PENDING',
  attempted_at timestamptz,
  delivered_at timestamptz,
  failure_reason text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (event_id, recipient_type, recipient_key)
);

create index if not exists idx_naya_notifications_day on public.nayanet_intelligence_notifications(canonical_day, occurred_at desc);
create index if not exists idx_naya_notifications_project on public.nayanet_intelligence_notifications(project_id, occurred_at desc);
create index if not exists idx_naya_notifications_user on public.nayanet_intelligence_notifications(user_id, occurred_at desc);
create index if not exists idx_naya_notification_delivery_pending on public.nayanet_intelligence_notification_deliveries(state, created_at);
create index if not exists idx_naya_notification_delivery_event on public.nayanet_intelligence_notification_deliveries(event_id);

alter table public.nayanet_intelligence_notifications enable row level security;
alter table public.nayanet_intelligence_notification_deliveries enable row level security;

create or replace function public.nayanet_emit_intelligence_notification_from_receipt()
returns trigger
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  v_event_id text;
  v_cognition_id uuid;
  v_summary text;
  v_why text;
  v_changed text;
  v_recommendation text;
  v_evidence_state text;
  v_authority_state text;
  v_event_type text;
  v_visibility text;
  v_briefing jsonb;
  v_notification_id uuid;
begin
  v_event_id := nullif(new.evidence->>'event_id','');

  if v_event_id is not null then
    select id, content, coalesce(metadata->>'why_it_matters',''), coalesce(metadata->>'what_changed',''),
           coalesce(metadata->>'recommendation',''), type, coalesce(metadata->>'visibility','PRIVATE'),
           coalesce(metadata->>'authority_state','UNCHANGED')
      into v_cognition_id, v_summary, v_why, v_changed, v_recommendation,
           v_event_type, v_visibility, v_authority_state
      from public.nayanet_cognition_events
     where user_id = new.user_id and project_id = new.project_id and event_id = v_event_id
     order by created_at desc limit 1;
  end if;

  v_event_id := coalesce(v_event_id, 'execution-receipt:' || new.id::text);
  v_summary := coalesce(nullif(v_summary,''), coalesce(new.observed_result, new.action, 'Execution receipt recorded.'));
  v_why := coalesce(nullif(v_why,''), 'A material runtime result was recorded and must remain visible to the intelligence system.');
  v_changed := coalesce(nullif(v_changed,''), coalesce(new.observed_result, new.status, 'Runtime state recorded.'));
  v_recommendation := coalesce(v_recommendation, '');
  v_event_type := coalesce(nullif(v_event_type,''), case
    when new.status = 'SUCCESS' then 'ACTION_COMPLETED'
    when new.status = 'BLOCKED' then 'ACTION_BLOCKED'
    when new.status = 'FAILED' then 'VERIFICATION_FAILED'
    else 'ACTIVITY_CREATED' end);
  v_visibility := upper(coalesce(nullif(v_visibility,''), 'PRIVATE'));
  v_authority_state := coalesce(nullif(v_authority_state,''), 'UNCHANGED');
  v_evidence_state := case
    when new.status = 'SUCCESS' then 'VERIFIED'
    when new.status = 'BLOCKED' then 'BLOCKED'
    when new.status = 'FAILED' then 'FAILED'
    else 'OBSERVED' end;

  v_briefing := jsonb_build_object(
    'what_happened', v_summary,
    'why_it_happened', coalesce(new.action,''),
    'why_it_matters', v_why,
    'what_changed', v_changed,
    'who_needs_to_know', jsonb_build_array('LIVE_NAYAS','NEW_NAYAS','NAYANET_INTELLIGENCE_HUB','GITHUB_NAYAPOWER'),
    'recommendation', v_recommendation,
    'authority_state', v_authority_state,
    'evidence_state', v_evidence_state,
    'source_event_id', v_event_id,
    'source_receipt_id', new.id::text,
    'delivery_state', 'PENDING');

  insert into public.nayanet_intelligence_notifications (
    event_id, source_receipt_id, source_cognition_event_id, user_id, project_id,
    event_type, occurred_at, summary, why_it_matters, what_changed,
    who_needs_to_know, recommendation, authority_state, evidence_state,
    visibility, briefing, canonical_day, caused_by, metadata)
  values (
    v_event_id, new.id, v_cognition_id, new.user_id, new.project_id,
    v_event_type, new.created_at, v_summary, v_why, v_changed,
    '["LIVE_NAYAS","NEW_NAYAS","NAYANET_INTELLIGENCE_HUB","GITHUB_NAYAPOWER"]'::jsonb,
    v_recommendation, v_authority_state, v_evidence_state,
    v_visibility, v_briefing, (new.created_at at time zone 'UTC')::date,
    nullif(new.authority_source_event_id,''),
    jsonb_build_object('action',new.action,'receipt_status',new.status,'receipt_id',new.id,'revision',new.revision))
  on conflict (event_id) do nothing
  returning id into v_notification_id;

  if v_notification_id is not null then
    insert into public.nayanet_intelligence_notification_deliveries
      (notification_id,event_id,recipient_type,recipient_key)
    values
      (v_notification_id,v_event_id,'SYSTEM','LIVE_NAYAS'),
      (v_notification_id,v_event_id,'SYSTEM','NEW_NAYAS'),
      (v_notification_id,v_event_id,'SYSTEM','NAYANET_INTELLIGENCE_HUB'),
      (v_notification_id,v_event_id,'SYSTEM','GITHUB_NAYAPOWER');

    if v_visibility in ('COLLECTIVE','PUBLIC') then
      insert into public.nayanet_intelligence_notification_deliveries
        (notification_id,event_id,recipient_type,recipient_key)
      values
        (v_notification_id,v_event_id,'INTELLIGENCE','COLLECTIVE_INTELLIGENCE');
    end if;

    perform pg_notify('nayanet_intelligence', jsonb_build_object(
      'event_id',v_event_id,'notification_id',v_notification_id,
      'project_id',new.project_id,'event_type',v_event_type)::text);
  end if;
  return new;
end;
$$;

drop trigger if exists nayanet_execution_receipt_to_intelligence_notification on public.nayanet_execution_receipts;
create trigger nayanet_execution_receipt_to_intelligence_notification
after insert on public.nayanet_execution_receipts
for each row execute function public.nayanet_emit_intelligence_notification_from_receipt();

create or replace function public.nayanet_sync_intelligence_notification_delivery_state()
returns trigger
language plpgsql
security definer
set search_path = public, extensions
as $$
declare v_state text;
begin
  select case
    when count(*) = 0 then 'PENDING'
    when count(*) filter (where state='DELIVERED') = count(*) then 'DELIVERED'
    when count(*) filter (where state='DELIVERED') > 0 then 'PARTIAL'
    when count(*) filter (where state='FAILED') > 0 then 'FAILED'
    else 'PENDING' end
    into v_state
    from public.nayanet_intelligence_notification_deliveries
   where notification_id = new.notification_id;
  update public.nayanet_intelligence_notifications set delivery_state=v_state where id=new.notification_id;
  return new;
end;
$$;

drop trigger if exists nayanet_notification_delivery_state_sync on public.nayanet_intelligence_notification_deliveries;
create trigger nayanet_notification_delivery_state_sync
after insert or update on public.nayanet_intelligence_notification_deliveries
for each row execute function public.nayanet_sync_intelligence_notification_delivery_state();
