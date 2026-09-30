create or replace function public.nayanet_publish_intelligence(
  p_intelligence_event_id uuid,
  p_authority_grant_id uuid,
  p_consent_state text
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_user uuid := (select auth.uid());
  v_source public.nayanet_cognition_events;
  v_existing public.nayanet_intelligence_publications;
  v_publication public.nayanet_intelligence_publications;
  v_authority jsonb;
begin
  if v_user is null then raise exception 'AUTH_REQUIRED'; end if;
  if p_consent_state is distinct from 'explicit' then raise exception 'EXPLICIT_CONSENT_REQUIRED'; end if;
  if p_authority_grant_id is null then raise exception 'PUBLISH_AUTHORITY_REQUIRED'; end if;

  select * into v_source
  from public.nayanet_cognition_events
  where id=p_intelligence_event_id and user_id=v_user and project_id='NayaNET'
  for share;
  if v_source.id is null then raise exception 'SOURCE_NOT_OWNED'; end if;

  v_authority := public.nayanet_validate_authority_grant(
    p_authority_grant_id,
    'smart_feed_publish',
    p_intelligence_event_id::text
  );
  if v_authority->>'status' is distinct from 'AUTHORIZED' then
    raise exception 'PUBLISH_AUTHORITY_REQUIRED:%', coalesce(v_authority->>'reason','BLOCKED');
  end if;

  select * into v_existing
  from public.nayanet_intelligence_publications
  where intelligence_event_id=p_intelligence_event_id
  for update;
  if v_existing.id is not null and v_existing.owner_id<>v_user then
    raise exception 'PUBLICATION_OWNER_MISMATCH';
  end if;

  if v_existing.id is null then
    insert into public.nayanet_intelligence_publications(
      intelligence_event_id,owner_id,status,consent_state,published_at,updated_at
    ) values(
      p_intelligence_event_id,v_user,'published','explicit',now(),now()
    )
    returning * into v_publication;
  else
    update public.nayanet_intelligence_publications
    set status='published',consent_state='explicit',published_at=now(),updated_at=now()
    where id=v_existing.id
    returning * into v_publication;
  end if;

  return jsonb_build_object(
    'status','SHARED_BY_EXPLICIT_CONSENT',
    'publication',to_jsonb(v_publication),
    'authority',v_authority
  );
end;
$$;

create or replace function public.nayanet_revoke_intelligence_publication(p_publication_id uuid)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_user uuid := (select auth.uid());
  v_publication public.nayanet_intelligence_publications;
begin
  if v_user is null then raise exception 'AUTH_REQUIRED'; end if;
  select * into v_publication
  from public.nayanet_intelligence_publications
  where id=p_publication_id
  for update;
  if v_publication.id is null then raise exception 'PUBLICATION_NOT_FOUND'; end if;
  if v_publication.owner_id<>v_user then raise exception 'PUBLICATION_OWNER_MISMATCH'; end if;
  if v_publication.status='revoked' then
    return jsonb_build_object('status','ALREADY_REVOKED','publication',to_jsonb(v_publication));
  end if;
  update public.nayanet_intelligence_publications
  set status='revoked',updated_at=now()
  where id=v_publication.id
  returning * into v_publication;
  return jsonb_build_object('status','REVOKED','publication',to_jsonb(v_publication));
end;
$$;

revoke insert,update,delete on table public.nayanet_intelligence_publications from anon, authenticated;
revoke all on function public.nayanet_publish_intelligence(uuid,uuid,text) from public, anon;
grant execute on function public.nayanet_publish_intelligence(uuid,uuid,text) to authenticated;
revoke all on function public.nayanet_revoke_intelligence_publication(uuid) from public, anon;
grant execute on function public.nayanet_revoke_intelligence_publication(uuid) to authenticated;
