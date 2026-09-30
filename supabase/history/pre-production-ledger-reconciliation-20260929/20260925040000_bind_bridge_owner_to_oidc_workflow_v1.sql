create table if not exists public.nayanet_project_intelligence_bridge_owner_bindings (
  binding_id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references auth.users(id) on delete cascade,
  repository text not null,
  workflow_ref text not null,
  run_id text not null,
  binding_hash text not null unique,
  expires_at timestamptz not null,
  created_at timestamptz not null default now(),
  check (repository='SoulSchoolAcademy/NayaPOWER'),
  check (workflow_ref ~ '^SoulSchoolAcademy/NayaPOWER/\.github/workflows/[^[:space:]]+@refs/heads/main$'),
  check (run_id ~ '^[0-9]+$')
);

create index if not exists nayanet_bridge_owner_bindings_expiry_idx
  on public.nayanet_project_intelligence_bridge_owner_bindings(expires_at);

alter table public.nayanet_project_intelligence_bridge_owner_bindings enable row level security;
revoke all on table public.nayanet_project_intelligence_bridge_owner_bindings from anon, authenticated;

create or replace function public.nayanet_issue_bridge_owner_binding(
  p_repository text,
  p_workflow_ref text,
  p_run_id text,
  p_expires_at timestamptz
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_owner uuid := (select auth.uid());
  v_token text;
  v_hash text;
  v_row public.nayanet_project_intelligence_bridge_owner_bindings;
begin
  if v_owner is null then raise exception 'AUTH_REQUIRED'; end if;
  if p_repository <> 'SoulSchoolAcademy/NayaPOWER' then raise exception 'BRIDGE_REPOSITORY_INVALID'; end if;
  if p_workflow_ref !~ '^SoulSchoolAcademy/NayaPOWER/\.github/workflows/[^[:space:]]+@refs/heads/main$' then raise exception 'BRIDGE_WORKFLOW_REF_INVALID'; end if;
  if p_run_id !~ '^[0-9]+$' then raise exception 'BRIDGE_RUN_ID_INVALID'; end if;
  if p_expires_at is null or p_expires_at <= now() or p_expires_at > now()+interval '15 minutes' then raise exception 'BRIDGE_BINDING_EXPIRY_INVALID'; end if;

  v_token := replace(gen_random_uuid()::text,'-','')||replace(gen_random_uuid()::text,'-','');
  v_hash := encode(extensions.digest(v_token,'sha256'),'hex');
  insert into public.nayanet_project_intelligence_bridge_owner_bindings(
    owner_id,repository,workflow_ref,run_id,binding_hash,expires_at
  ) values(
    v_owner,p_repository,p_workflow_ref,p_run_id,v_hash,p_expires_at
  ) returning * into v_row;

  return jsonb_build_object(
    'status','ISSUED',
    'owner_id',v_owner,
    'repository',p_repository,
    'workflow_ref',p_workflow_ref,
    'run_id',p_run_id,
    'expires_at',v_row.expires_at,
    'owner_binding_token',v_token
  );
end;
$$;

create or replace function public.nayanet_consume_bridge_owner_binding(
  p_binding_token text,
  p_owner_id uuid,
  p_repository text,
  p_workflow_ref text,
  p_run_id text,
  p_packet_id text
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $$
declare
  v_hash text;
  v_row public.nayanet_project_intelligence_bridge_owner_bindings;
begin
  if auth.role() <> 'service_role' then raise exception 'SERVER_ROLE_REQUIRED'; end if;
  if nullif(trim(coalesce(p_binding_token,'')),'') is null then raise exception 'OWNER_BINDING_TOKEN_REQUIRED'; end if;
  if p_owner_id is null or nullif(trim(coalesce(p_packet_id,'')),'') is null then raise exception 'OWNER_BINDING_IDENTITY_REQUIRED'; end if;
  v_hash := encode(extensions.digest(p_binding_token,'sha256'),'hex');
  select * into v_row
  from public.nayanet_project_intelligence_bridge_owner_bindings
  where binding_hash=v_hash
    and owner_id=p_owner_id
    and repository=p_repository
    and workflow_ref=p_workflow_ref
    and run_id=p_run_id
    and expires_at>clock_timestamp()
  for update;
  if v_row.binding_id is null then raise exception 'OWNER_BINDING_INVALID_OR_EXPIRED'; end if;
  return jsonb_build_object(
    'status','VALID',
    'owner_id',v_row.owner_id,
    'repository',v_row.repository,
    'workflow_ref',v_row.workflow_ref,
    'run_id',v_row.run_id,
    'packet_id',p_packet_id,
    'expires_at',v_row.expires_at
  );
end;
$$;

revoke all on function public.nayanet_issue_bridge_owner_binding(text,text,text,timestamptz) from public, anon;
grant execute on function public.nayanet_issue_bridge_owner_binding(text,text,text,timestamptz) to authenticated;
revoke all on function public.nayanet_consume_bridge_owner_binding(text,uuid,text,text,text,text) from public, anon, authenticated;
grant execute on function public.nayanet_consume_bridge_owner_binding(text,uuid,text,text,text,text) to service_role;
