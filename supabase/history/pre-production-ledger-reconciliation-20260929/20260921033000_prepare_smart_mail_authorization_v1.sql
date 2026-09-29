-- Canonical human Smart Mail authorization preparation.
-- Keeps communication authority separate from connection membership and send execution.
-- The caller must already have a mutual active Connection to the receiver.
create or replace function public.nayanet_prepare_smart_mail_authorization(
  p_receiver_id uuid
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $function$
declare
  v_sender uuid := auth.uid();
  v_event jsonb;
  v_event_id text;
  v_grant public.nayanet_authority_grants;
begin
  if v_sender is null then
    raise exception 'AUTH_REQUIRED';
  end if;
  if p_receiver_id is null or p_receiver_id = v_sender then
    raise exception 'INVALID_MAIL_RECIPIENT';
  end if;

  if not exists (
    select 1
    from public.nayanet_connections a
    join public.nayanet_connections b
      on b.owner_member_id = p_receiver_id
     and b.connected_member_id = v_sender
     and b.status = 'active'
    where a.owner_member_id = v_sender
      and a.connected_member_id = p_receiver_id
      and a.status = 'active'
  ) then
    raise exception 'RELATIONSHIP_REQUIRED';
  end if;

  v_event_id := 'smart-mail-authorization-' ||
    to_char(clock_timestamp(),'YYYYMMDDHH24MISSMS') || '-' ||
    substr(replace(gen_random_uuid()::text,'-',''),1,10);

  v_event := jsonb_build_object(
    'event_id', v_event_id,
    'type', 'smart_mail_authorization',
    'classification', 'authorization',
    'title', 'Smart Mail authorization',
    'content', jsonb_build_object(
      'sender_id', v_sender,
      'receiver_id', p_receiver_id,
      'authorization_type', 'explicit_human_send'
    )::text,
    'source', 'nayanet-hub.smart-mail',
    'status', 'active',
    'actor', 'human',
    'confidence', 1,
    'tags', jsonb_build_array('smart-mail','authorization','human-send'),
    'schema_version', 'NAYANET_SMART_MAIL_AUTH_V1',
    'metadata', jsonb_build_object(
      'action', 'smart_mail_authorize',
      'sender_id', v_sender,
      'receiver_id', p_receiver_id,
      'authorization_type', 'explicit_human_send',
      'relationship_gate', 'mutual_active_connection'
    )
  );

  perform public.nayanet_record_cognition_event(
    'NayaNET',
    v_event,
    'smart_mail_authorize',
    'Mutual connected sender is authorized for a bounded Smart Mail send.',
    'Smart Mail authorization event persisted.',
    jsonb_build_array(jsonb_build_object(
      'status','captured',
      'statement','Explicit human send intent crossed the mutual-connection authorization boundary.'
    ))
  );

  v_grant := public.nayanet_issue_authority_grant(
    v_sender,
    v_event_id,
    'NayaNET Smart Mail',
    jsonb_build_object(
      'project_id', 'NayaNET',
      'target', p_receiver_id::text
    ),
    jsonb_build_array('smart_mail_send'),
    jsonb_build_object(
      'receiver_user_id', p_receiver_id,
      'authorization_event_id', v_event_id,
      'relationship_gate', 'mutual_active_connection'
    ),
    clock_timestamp() + interval '10 minutes',
    jsonb_build_object(
      'authorization_type', 'explicit_human_send',
      'receiver_user_id', p_receiver_id,
      'authorization_event_id', v_event_id
    ),
    null
  );

  return jsonb_build_object(
    'status', 'AUTHORIZED',
    'authorization_event_id', v_event_id,
    'grant_id', v_grant.grant_id,
    'expires_at', v_grant.expires_at,
    'receiver_user_id', p_receiver_id,
    'relationship_gate', 'mutual_active_connection'
  );
end;
$function$;

grant execute on function public.nayanet_prepare_smart_mail_authorization(uuid) to authenticated;
revoke execute on function public.nayanet_prepare_smart_mail_authorization(uuid) from anon, public;
