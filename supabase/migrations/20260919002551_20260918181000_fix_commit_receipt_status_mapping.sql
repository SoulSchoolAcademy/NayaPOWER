create or replace function public.nayanet_commit_cognition(
  p_project_id text,
  p_expected_revision bigint,
  p_state jsonb,
  p_action text,
  p_expected_result text,
  p_observed_result text,
  p_status text,
  p_evidence jsonb default '[]'::jsonb,
  p_learning jsonb default '[]'::jsonb,
  p_authority_grant_id uuid default null
)
returns public.nayanet_project_cognition_state
language plpgsql
set search_path = 'public'
as $function$
declare
  v public.nayanet_project_cognition_state;
  v_authority jsonb;
  v_authority_validated_at timestamptz;
begin
  v_authority_validated_at := clock_timestamp();
  v_authority := public.nayanet_validate_authority_grant(p_authority_grant_id,p_action,p_project_id);
  if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
    raise exception 'AUTHORITY_REQUIRED: %', coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
  end if;

  update public.nayanet_project_cognition_state
     set revision = revision + 1, state = p_state, status = p_status, updated_at = now()
   where user_id = auth.uid() and project_id = p_project_id and revision = p_expected_revision
   returning * into v;
  if not found then raise exception 'COGNITION_REVISION_CONFLICT'; end if;

  insert into public.nayanet_execution_receipts(
    user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning,
    authority_grant_id,authority_issuer_id,authority_scope,authority_actions,authority_constraints,
    authority_status_at_execution,authority_source_event_id,authority_validated_at
  )
  values(
    auth.uid(),p_project_id,v.revision,p_action,p_expected_result,p_observed_result,
    case when p_status='FAILED' then 'FAILED' when p_status='BLOCKED' then 'BLOCKED' else 'SUCCESS' end,
    coalesce(p_evidence,'[]'::jsonb),coalesce(p_learning,'[]'::jsonb),
    (v_authority->>'grant_id')::uuid,(v_authority->>'issuer_id')::uuid,
    v_authority->'scope',v_authority->'actions',v_authority->'constraints',
    v_authority->>'grant_status',v_authority->>'source_event_id',v_authority_validated_at
  );
  return v;
end;
$function$;

grant execute on function public.nayanet_commit_cognition(text,bigint,jsonb,text,text,text,text,jsonb,jsonb,uuid) to authenticated;
revoke execute on function public.nayanet_commit_cognition(text,bigint,jsonb,text,text,text,text,jsonb,jsonb,uuid) from anon,public;
