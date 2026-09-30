-- Repair UUID owner aggregation in the canonical GitHub webhook resolver.
-- PostgreSQL has no min(uuid); preserve the existing count + owner contract using array_agg.
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
  if p_installation_id is null or p_installation_id <= 0 then
    raise exception 'GITHUB_INSTALLATION_ID_INVALID';
  end if;
  if v_repository !~ '^[^/[:space:]]+/[^/[:space:]]+$' then
    raise exception 'GITHUB_REPOSITORY_INVALID';
  end if;

  select count(*), (array_agg(sp.member_id))[1]
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

grant execute on function public.nayanet_resolve_github_webhook_owner(bigint,text) to service_role;
revoke execute on function public.nayanet_resolve_github_webhook_owner(bigint,text) from anon, authenticated, public;
