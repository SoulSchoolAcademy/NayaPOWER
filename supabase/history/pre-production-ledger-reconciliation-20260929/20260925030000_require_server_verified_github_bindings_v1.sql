create or replace function public.nayanet_smart_connect_github_bind(p_installation_id bigint,p_repository text)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
begin
  raise exception 'GITHUB_BINDING_REQUIRES_SERVER_VERIFICATION';
end;
$$;

create or replace function public.nayanet_bind_github_installation_verified(
  p_member_id uuid,
  p_installation_id bigint,
  p_repository text,
  p_delivery_id text
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_repository text := lower(trim(p_repository));
  v_delivery text := trim(p_delivery_id);
  v_row public.nayanet_smart_connect_participation;
  v_existing_owner uuid;
  v_bindings jsonb;
begin
  if auth.role() <> 'service_role' then raise exception 'SERVER_ROLE_REQUIRED'; end if;
  if p_member_id is null then raise exception 'GITHUB_MEMBER_REQUIRED'; end if;
  if p_installation_id is null or p_installation_id<=0 then raise exception 'GITHUB_INSTALLATION_ID_INVALID'; end if;
  if v_repository !~ '^[^/[:space:]]+/[^/[:space:]]+$' then raise exception 'GITHUB_REPOSITORY_INVALID'; end if;
  if v_delivery='' then raise exception 'GITHUB_DELIVERY_ID_REQUIRED'; end if;

  select * into v_row
  from public.nayanet_smart_connect_participation
  where member_id=p_member_id and door='github_app' and status='active' and consent_state='explicit'
  for update;
  if v_row.id is null then raise exception 'GITHUB_APP_PARTICIPATION_CONSENT_REQUIRED'; end if;

  select sp.member_id into v_existing_owner
  from public.nayanet_smart_connect_participation sp
  where sp.door='github_app'
    and sp.status='active'
    and sp.member_id<>p_member_id
    and exists (
      select 1
      from jsonb_array_elements(coalesce(sp.external_bindings,'[]'::jsonb)) b
      where b->>'provider'='github'
        and b->>'installation_id'=p_installation_id::text
        and lower(b->>'repository')=v_repository
    )
  limit 1;
  if v_existing_owner is not null then raise exception 'GITHUB_BINDING_ALREADY_OWNED'; end if;

  v_bindings := coalesce((
    select jsonb_agg(b)
    from jsonb_array_elements(coalesce(v_row.external_bindings,'[]'::jsonb)) b
    where not (
      b->>'provider'='github'
      and b->>'installation_id'=p_installation_id::text
      and lower(b->>'repository')=v_repository
    )
  ),'[]'::jsonb);
  v_bindings := v_bindings || jsonb_build_array(jsonb_build_object(
    'provider','github',
    'installation_id',p_installation_id,
    'repository',v_repository,
    'verification','SIGNED_GITHUB_WEBHOOK',
    'verification_method','signed GitHub webhook delivery',
    'delivery_id',v_delivery,
    'verified_at',now(),
    'bound_at',now()
  ));
  update public.nayanet_smart_connect_participation
  set external_bindings=v_bindings,updated_at=now()
  where id=v_row.id
  returning * into v_row;

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_GITHUB_BINDING_V2',
    'status','VERIFIED_BOUND',
    'participation',to_jsonb(v_row),
    'identity','PRIVATE_BY_DEFAULT',
    'repository',v_repository,
    'installation_id',p_installation_id,
    'delivery_id',v_delivery,
    'verification','SIGNED_GITHUB_WEBHOOK'
  );
end;
$$;

create or replace function public.nayanet_resolve_github_webhook_owner(
  p_installation_id bigint,
  p_repository text
)
returns uuid
language plpgsql
security definer
set search_path=''
as $$
declare
  v_repository text := lower(trim(p_repository));
  v_count integer;
  v_owner uuid;
begin
  if p_installation_id is null or p_installation_id<=0 then raise exception 'GITHUB_INSTALLATION_ID_INVALID'; end if;
  if v_repository !~ '^[^/[:space:]]+/[^/[:space:]]+$' then raise exception 'GITHUB_REPOSITORY_INVALID'; end if;
  select count(*),(array_agg(sp.member_id))[1]
    into v_count,v_owner
    from public.nayanet_smart_connect_participation sp
   where sp.door='github_app'
     and sp.status='active'
     and sp.consent_state='explicit'
     and exists (
       select 1
       from jsonb_array_elements(coalesce(sp.external_bindings,'[]'::jsonb)) b
       where b->>'provider'='github'
         and b->>'installation_id'=p_installation_id::text
         and lower(b->>'repository')=v_repository
         and b->>'verification'='SIGNED_GITHUB_WEBHOOK'
         and nullif(b->>'delivery_id','') is not null
         and nullif(b->>'verified_at','') is not null
     );
  if v_count=0 then raise exception 'GITHUB_BINDING_NOT_FOUND'; end if;
  if v_count>1 then raise exception 'GITHUB_BINDING_AMBIGUOUS'; end if;
  return v_owner;
end;
$$;

revoke all on function public.nayanet_smart_connect_github_bind(bigint,text) from public, anon, authenticated;
revoke all on function public.nayanet_bind_github_installation_verified(uuid,bigint,text,text) from public, anon, authenticated;
grant execute on function public.nayanet_bind_github_installation_verified(uuid,bigint,text,text) to service_role;
grant execute on function public.nayanet_resolve_github_webhook_owner(bigint,text) to service_role;
revoke execute on function public.nayanet_resolve_github_webhook_owner(bigint,text) from anon, authenticated, public;
