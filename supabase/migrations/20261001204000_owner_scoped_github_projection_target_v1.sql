-- Owner-scoped GitHub projection target resolver.
--
-- Extends the existing Smart Connect GitHub binding registry introduced by
-- 20260924225535_harden_github_app_owner_binding_v1.sql.
--
-- A caller may name the repository it wants to project into, but the database
-- independently proves that the authenticated owner currently holds exactly
-- one active GitHub App binding for that repository. Caller input therefore
-- selects among the owner's own bindings; it cannot create ownership.
--
-- No new ownership registry is introduced.

create or replace function public.nayanet_resolve_github_projection_target(
  p_repository text
) returns jsonb
language plpgsql
security definer
set search_path to 'public'
as $function$
declare
  v_actor uuid := auth.uid();
  v_repository text := lower(trim(p_repository));
  v_count integer;
  v_installation_id bigint;
begin
  if v_actor is null then
    raise exception 'AUTH_REQUIRED';
  end if;

  if v_repository !~ '^[^/[:space:]]+/[^/[:space:]]+$' then
    raise exception 'GITHUB_REPOSITORY_INVALID';
  end if;

  select
    count(*),
    (array_agg((b->>'installation_id')::bigint))[1]
  into v_count, v_installation_id
  from public.nayanet_smart_connect_participation sp
  cross join lateral jsonb_array_elements(coalesce(sp.external_bindings, '[]'::jsonb)) b
  where sp.member_id = v_actor
    and sp.door = 'github_app'
    and sp.status = 'active'
    and b->>'provider' = 'github'
    and lower(b->>'repository') = v_repository
    and nullif(b->>'installation_id', '') is not null;

  if v_count = 0 then
    raise exception 'GITHUB_PROJECTION_TARGET_NOT_BOUND';
  end if;

  if v_count > 1 then
    raise exception 'GITHUB_PROJECTION_TARGET_AMBIGUOUS';
  end if;

  return jsonb_build_object(
    'schema', 'NAYANET_GITHUB_PROJECTION_TARGET_V1',
    'owner_id', v_actor,
    'repository', v_repository,
    'installation_id', v_installation_id,
    'binding_source', 'nayanet_smart_connect_participation',
    'status', 'BOUND'
  );
end;
$function$;

revoke all on function public.nayanet_resolve_github_projection_target(text)
  from public, anon, service_role;
grant execute on function public.nayanet_resolve_github_projection_target(text)
  to authenticated;
