create table if not exists public.smart_note_events (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null,
  subject text not null,
  event_type text not null default 'SMART_NOTE',
  source_context jsonb not null default '{}'::jsonb,
  privacy_state text not null default 'PRIVATE',
  status text not null default 'INCOMPLETE' check (status in ('INCOMPLETE','VERIFIED')),
  created_at timestamptz not null default now(),
  verified_at timestamptz
);

create table if not exists public.smart_note_artifacts (
  id uuid primary key default gen_random_uuid(),
  event_id uuid not null references public.smart_note_events(id) on delete cascade,
  artifact_type text not null check (artifact_type in ('HUMAN_NOTE','NAYA_NOTE','MACHINE_NOTE','INTELLIGENCE_FEED_NOTE')),
  content text not null,
  artifact_url text,
  created_at timestamptz not null default now(),
  unique (event_id, artifact_type)
);

create table if not exists public.smart_note_receipts (
  id uuid primary key default gen_random_uuid(),
  event_id uuid not null unique references public.smart_note_events(id) on delete cascade,
  status text not null check (status in ('VERIFIED','INCOMPLETE')),
  receipt_url text,
  verification jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create or replace function public.verify_smart_note(p_event_id uuid)
returns jsonb
language plpgsql
security definer
as $$
declare
  artifact_count integer;
  missing_types text[];
  result jsonb;
begin
  select count(*) into artifact_count
  from public.smart_note_artifacts
  where event_id = p_event_id;

  select array_agg(required_type order by required_type) into missing_types
  from (values ('HUMAN_NOTE'),('NAYA_NOTE'),('MACHINE_NOTE'),('INTELLIGENCE_FEED_NOTE')) as required(required_type)
  where not exists (
    select 1 from public.smart_note_artifacts a
    where a.event_id = p_event_id and a.artifact_type = required.required_type and a.content is not null and length(trim(a.content)) > 0
  );

  if artifact_count = 4 and coalesce(array_length(missing_types,1),0) = 0 then
    update public.smart_note_events
      set status = 'VERIFIED', verified_at = now()
      where id = p_event_id;

    insert into public.smart_note_receipts(event_id, status, verification)
    values (
      p_event_id,
      'VERIFIED',
      jsonb_build_object('four_artifacts', true, 'artifact_count', 4, 'verified_at', now())
    )
    on conflict (event_id) do update set status = 'VERIFIED', verification = excluded.verification;

    result := jsonb_build_object('status','VERIFIED','event_id',p_event_id,'artifact_count',4,'missing_types',jsonb_build_array());
  else
    update public.smart_note_events set status = 'INCOMPLETE', verified_at = null where id = p_event_id;
    result := jsonb_build_object('status','INCOMPLETE','event_id',p_event_id,'artifact_count',artifact_count,'missing_types',coalesce(to_jsonb(missing_types),'[]'::jsonb));
  end if;

  return result;
end;
$$;

comment on table public.smart_note_events is 'Constitutional Smart Note event registry. COMPLETE is permitted only after four required artifacts verify.';
comment on table public.smart_note_artifacts is 'Four required Smart Note artifact records linked to one event.';
comment on table public.smart_note_receipts is 'Evidence receipts generated only for verified Smart Note events.';
comment on function public.verify_smart_note(uuid) is 'Enforces the four-artifact Smart Note completion invariant; otherwise status remains INCOMPLETE.';
