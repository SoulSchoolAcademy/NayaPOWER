-- Stream B automatic collective-wisdom projection.
-- Verified learning is the canonical semantic source for wisdom contribution.
-- This migration is SOURCE ONLY; deployment remains separately authorized.
create or replace function public.nayanet_project_verified_learning_to_collective_wisdom(
  p_learning_id uuid
) returns jsonb
language plpgsql
security definer
set search_path to ''
as $function$
declare
  v_learning public.learning_evidence;
  v_source public.nayanet_cognition_events;
  v_topic text;
  v_provenance jsonb;
  v_result jsonb;
begin
  if auth.uid() is null then
    raise exception 'AUTH_REQUIRED';
  end if;

  select * into v_learning
  from public.learning_evidence
  where id=p_learning_id and member_id=auth.uid()
  for update;

  if v_learning.id is null then raise exception 'LEARNING_NOT_FOUND'; end if;
  if v_learning.status <> 'ACTIVE' then raise exception 'VERIFIED_LEARNING_REQUIRED'; end if;
  if v_learning.source_event_id is null then raise exception 'LEARNING_SOURCE_EVENT_REQUIRED'; end if;

  select * into v_source
  from public.nayanet_cognition_events
  where event_id=v_learning.source_event_id
    and user_id=auth.uid()
    and project_id='NayaNET'
  limit 1;

  if v_source.id is null then raise exception 'SOURCE_EVENT_NOT_FOUND'; end if;

  v_topic := coalesce(
    nullif(trim(v_learning.observed_value->>'topic'),''),
    nullif(trim(v_source.metadata->>'topic'),''),
    'GENERAL'
  );

  v_provenance := jsonb_build_object(
    'schema','NAYANET_COLLECTIVE_WISDOM_PROVENANCE_V1',
    'learning_id',v_learning.id,
    'source_event_id',v_source.id,
    'source_event_key',v_source.event_id,
    'learning_level',v_learning.level,
    'verification_method',v_learning.verification_method,
    'learning_status',v_learning.status
  );

  v_result := public.nayanet_collective_wisdom_for_event(
    v_source.id,
    auth.uid(),
    v_learning.claim,
    v_topic,
    v_provenance
  );

  update public.nayanet_collective_wisdom
  set epistemic_state='VERIFIED'
  where id=(v_result->>'collective_wisdom_id')::uuid
    and owner_id=auth.uid();

  return v_result || jsonb_build_object(
    'learning_id',v_learning.id,
    'verification_status',v_learning.status,
    'epistemic_state','VERIFIED'
  );
end;
$function$;

revoke all on function public.nayanet_project_verified_learning_to_collective_wisdom(uuid)
  from public,anon;
grant execute on function public.nayanet_project_verified_learning_to_collective_wisdom(uuid)
  to authenticated,service_role;
comment on function public.nayanet_project_verified_learning_to_collective_wisdom(uuid)
is 'Automatic verified-learning projection into collective wisdom. Participation/consent governs contribution; execution authority and publication are not consulted.';
