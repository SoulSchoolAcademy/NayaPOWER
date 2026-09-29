create or replace function public.nayanet_intelligence_commit_runtime(
  p_naya_id text,
  p_owner_id uuid,
  p_runtime_jti text,
  p_event_id text,
  p_title text,
  p_content text,
  p_category text,
  p_topic text,
  p_target_id text,
  p_authority_grant_id uuid,
  p_project_id text default 'NayaNET'
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $function$
declare
  grant_row record;
  result jsonb;
  receipt_id uuid;
begin
  if p_naya_id <> 'NAYA-NODE-0001' then
    raise exception using errcode='42501', message='NAYA_ID_NOT_AUTHORIZED';
  end if;

  if coalesce(trim(p_runtime_jti),'')='' then
    raise exception using errcode='22023', message='RUNTIME_JTI_REQUIRED';
  end if;

  select * into grant_row
  from public.nayanet_authority_grants
  where grant_id = p_authority_grant_id
    and issuer_id = p_owner_id
    and subject_id = p_owner_id
    and status = 'ACTIVE'
    and revoked_at is null
    and (expires_at is null or expires_at > clock_timestamp())
    and scope->>'target' = p_naya_id
    and actions @> '["intelligence_commit"]'::jsonb;

  if not found then
    raise exception using errcode='42501', message='AUTHORITY_BLOCKED';
  end if;

  -- Preserve the governed runtime identity through the full PostgREST/RLS claim context.
  perform set_config(
    'request.jwt.claims',
    json_build_object('sub', p_owner_id::text, 'role', 'authenticated')::text,
    true
  );
  perform set_config('request.jwt.claim.sub', p_owner_id::text, true);

  result := public.nayanet_intelligence_commit(
    p_event_id,p_title,p_content,p_category,p_topic,p_target_id,p_authority_grant_id,p_project_id
  );

  receipt_id := (result->>'receipt_id')::uuid;
  update public.nayanet_execution_receipts
    set evidence = evidence || jsonb_build_object(
      'runtime_identity','naya-node-oidc',
      'naya_id',p_naya_id,
      'runtime_jti',p_runtime_jti,
      'owner_id',p_owner_id
    )
  where id = receipt_id;

  return result || jsonb_build_object(
    'runtime_identity','naya-node-oidc',
    'naya_id',p_naya_id,
    'runtime_jti',p_runtime_jti,
    'owner_id',p_owner_id
  );
end;
$function$;

revoke all on function public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text) from public, anon, authenticated;
grant execute on function public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text) to service_role;
