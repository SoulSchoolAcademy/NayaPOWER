-- Extend the existing Smart Connect participation seam with governed GitHub
-- installation/repository identity bindings. No second connection store is introduced.
alter table public.nayanet_smart_connect_participation
  add column if not exists external_bindings jsonb not null default '[]'::jsonb;

create index if not exists nayanet_smart_connect_participation_external_bindings_gin
  on public.nayanet_smart_connect_participation using gin (external_bindings);

create or replace function public.nayanet_smart_connect_github_bind(
  p_installation_id bigint,
  p_repository text
) returns jsonb
language plpgsql
security definer
set search_path to 'public'
as $function$
declare
  v_actor uuid := auth.uid();
  v_repository text := lower(trim(p_repository));
  v_row public.nayanet_smart_connect_participation;
  v_existing_owner uuid;
  v_bindings jsonb;
begin
  if v_actor is null then raise exception 'AUTH_REQUIRED'; end if;
  if p_installation_id is null or p_installation_id <= 0 then raise exception 'GITHUB_INSTALLATION_ID_INVALID'; end if;
  if v_repository !~ '^[^/[:space:]]+/[^/[:space:]]+$' then raise exception 'GITHUB_REPOSITORY_INVALID'; end if;

  select * into v_row
    from public.nayanet_smart_connect_participation
   where member_id=v_actor and door='github_app'
   for update;

  if v_row.id is null or v_row.status <> 'active' then
    raise exception 'GITHUB_APP_PARTICIPATION_REQUIRED';
  end if;

  select sp.member_id
    into v_existing_owner
    from public.nayanet_smart_connect_participation sp
   where sp.door='github_app'
     and sp.status='active'
     and exists (
       select 1
         from jsonb_array_elements(coalesce(sp.external_bindings,'[]'::jsonb)) b
        where b->>'provider'='github'
          and b->>'installation_id'=p_installation_id::text
          and lower(b->>'repository')=v_repository
     )
     and sp.member_id<>v_actor
   limit 1;

  if v_existing_owner is not null then
    raise exception 'GITHUB_BINDING_ALREADY_OWNED';
  end if;

  v_bindings := coalesce((
    select jsonb_agg(b)
      from jsonb_array_elements(coalesce(v_row.external_bindings,'[]'::jsonb)) b
     where not (
       b->>'provider'='github'
       and b->>'installation_id'=p_installation_id::text
       and lower(b->>'repository')=v_repository
     )
  ),'[]'::jsonb);

  v_bindings := v_bindings || jsonb_build_array(
    jsonb_build_object(
      'provider','github',
      'installation_id',p_installation_id,
      'repository',v_repository,
      'bound_at',now()
    )
  );

  update public.nayanet_smart_connect_participation
     set external_bindings=v_bindings,updated_at=now()
   where id=v_row.id
   returning * into v_row;

  return jsonb_build_object(
    'schema','NAYANET_SMART_CONNECT_GITHUB_BINDING_V1',
    'status','BOUND',
    'participation',to_jsonb(v_row),
    'identity','PRIVATE_BY_DEFAULT',
    'repository',v_repository,
    'installation_id',p_installation_id
  );
end;
$function$;

create or replace function public.nayanet_resolve_github_webhook_owner(
  p_installation_id bigint,
  p_repository text
) returns uuid
language plpgsql
security definer
set search_path to 'public'
as $function$
declare
  v_repository text := lower(trim(p_repository));
  v_count integer;
  v_owner uuid;
begin
  if p_installation_id is null or p_installation_id <= 0 then raise exception 'GITHUB_INSTALLATION_ID_INVALID'; end if;
  if v_repository !~ '^[^/[:space:]]+/[^/[:space:]]+$' then raise exception 'GITHUB_REPOSITORY_INVALID'; end if;

  select count(*), min(sp.member_id)
    into v_count, v_owner
    from public.nayanet_smart_connect_participation sp
   where sp.door='github_app'
     and sp.status='active'
     and exists (
       select 1
         from jsonb_array_elements(coalesce(sp.external_bindings,'[]'::jsonb)) b
        where b->>'provider'='github'
          and b->>'installation_id'=p_installation_id::text
          and lower(b->>'repository')=v_repository
     );

  if v_count=0 then raise exception 'GITHUB_BINDING_NOT_FOUND'; end if;
  if v_count>1 then raise exception 'GITHUB_BINDING_AMBIGUOUS'; end if;
  return v_owner;
end;
$function$;

grant execute on function public.nayanet_smart_connect_github_bind(bigint,text) to authenticated;
revoke execute on function public.nayanet_smart_connect_github_bind(bigint,text) from anon, public, service_role;

grant execute on function public.nayanet_resolve_github_webhook_owner(bigint,text) to service_role;
revoke execute on function public.nayanet_resolve_github_webhook_owner(bigint,text) from anon, authenticated, public;
