-- Repair Smart Note verification -> universal execution receipt trigger overload resolution.
-- The production database contains both 6-argument and 7-argument
-- nayanet_record_cognition_event overloads. The trigger's 6-argument call
-- became ambiguous after the governed execution-authorization overload was added.
-- Preserve the existing trigger, receipt boundary, and authority model; only make
-- the intended 7-argument call explicit with a NULL execution-authorization value.

create or replace function public.nayanet_smart_note_receipt_to_execution_receipt()
returns trigger
language plpgsql
security definer
set search_path to 'public', 'extensions'
as $function$
declare
  v_event public.nayanet_cognition_events;
  v_member_id uuid;
  v_event_id text := new.event_id::text;
begin
  if new.status <> 'VERIFIED' then
    return new;
  end if;

  select sne.member_id into v_member_id
    from public.smart_note_events sne
   where sne.id = new.event_id limit 1;

  if v_member_id is null then
    raise exception 'SMART_NOTE_OWNER_MISSING:%', new.event_id;
  end if;

  select * into v_event
    from public.nayanet_cognition_events
   where user_id = v_member_id
     and project_id = coalesce(
       nullif(trim((select sne2.source_context->>'project_id'
                      from public.smart_note_events sne2
                     where sne2.id = new.event_id limit 1)), ''),
       'NayaNET'
     )
     and event_id = v_event_id
   order by created_at desc limit 1;

  if not found then
    raise exception 'SMART_NOTE_COGNITION_EVENT_MISSING:%', new.event_id;
  end if;

  if nullif(trim(coalesce(v_event.receipt_id, '')), '') is not null then
    return new;
  end if;

  if auth.uid() is null or auth.uid() <> v_event.user_id then
    raise exception 'AUTH_REQUIRED';
  end if;

  perform public.nayanet_record_cognition_event(
    v_event.project_id,
    to_jsonb(v_event) || jsonb_build_object(
      'metadata',
      coalesce(v_event.metadata, '{}'::jsonb) ||
      jsonb_build_object(
        'smart_note_receipt_id', new.id,
        'canonical_receipt_bridge', 'SMART_NOTE_VERIFICATION',
        'canonical_source_table', 'smart_note_events',
        'canonical_source_id', new.event_id,
        'bridge_verified_at', coalesce(new.created_at, now())
      )
    ),
    'smart_note.create',
    'Verified Smart Note persists with a universal execution receipt',
    format(
      'Smart Note %s verified; domain receipt %s persisted and universal execution receipt created.',
      new.event_id::text,
      new.id::text
    ),
    '[]'::jsonb,
    null::jsonb
  );

  return new;
end;
$function$;
