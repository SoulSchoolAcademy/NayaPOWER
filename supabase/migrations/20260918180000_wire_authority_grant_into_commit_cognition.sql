-- Wire Authority Grant V1 into the canonical cognition commit boundary.
-- Smallest safe change:
--   * preserve the existing 9-argument call shape via a defaulted 10th parameter;
--   * require a valid in-scope authority grant for every cognition commit that mutates
--     state and creates an execution receipt;
--   * validate before any cognition mutation;
--   * preserve authoritative grant provenance on the receipt;
--   * hold the grant row with FOR SHARE during validation so revocation cannot race
--     between authorization and receipt creation.

create or replace function public.nayanet_validate_authority_grant(
  p_grant_id uuid,
  p_action text,
  p_target text
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  g public.nayanet_authority_grants;
  uid uuid;
  reason text := 'AUTHORIZED';
begin
  uid := (select auth.uid());

  if uid is null then
    return jsonb_build_object('status','BLOCKED','reason','AUTH_REQUIRED');
  end if;

  select *
    into g
    from public.nayanet_authority_grants
   where grant_id = p_grant_id
     and (issuer_id = uid or subject_id = uid)
   for share;

  if not found then
    return jsonb_build_object(
      'status','BLOCKED',
      'reason','GRANT_NOT_FOUND_OR_NOT_OWNED',
      'grant_id',p_grant_id
    );
  end if;

  if g.subject_id <> uid then
    return jsonb_build_object('status','BLOCKED','reason','WRONG_SUBJECT','grant_id',g.grant_id);
  end if;

  if g.status = 'REVOKED' then
    return jsonb_build_object('status','BLOCKED','reason','GRANT_REVOKED','grant_id',g.grant_id,'source_event_id',g.source_event_id);
  end if;

  if g.status in ('INVALID','ISSUED') then
    return jsonb_build_object('status','BLOCKED','reason','GRANT_NOT_ACTIVE','grant_id',g.grant_id,'source_event_id',g.source_event_id);
  end if;

  if g.expires_at is not null and g.expires_at <= clock_timestamp() then
    return jsonb_build_object('status','BLOCKED','reason','GRANT_EXPIRED','grant_id',g.grant_id,'source_event_id',g.source_event_id,'expires_at',g.expires_at);
  end if;

  if not (g.actions ? p_action) then
    reason := 'ACTION_OUT_OF_SCOPE';
  elsif not (coalesce(g.scope->>'target','') = p_target or coalesce(g.scope->>'project_id','') = p_target) then
    reason := 'TARGET_OUT_OF_SCOPE';
  end if;

  if reason = 'AUTHORIZED' then
    return jsonb_build_object(
      'status','AUTHORIZED',
      'reason','VALID_IN_SCOPE_GRANT',
      'grant_id',g.grant_id,
      'issuer_id',g.issuer_id,
      'subject_id',g.subject_id,
      'mission_id',g.mission_id,
      'scope',g.scope,
      'actions',g.actions,
      'constraints',g.constraints,
      'issued_at',g.issued_at,
      'expires_at',g.expires_at,
      'grant_status','ACTIVE',
      'revoked_at',g.revoked_at,
      'evidence',g.evidence,
      'source_event_id',g.source_event_id
    );
  end if;

  return jsonb_build_object(
    'status','BLOCKED',
    'reason',reason,
    'grant_id',g.grant_id,
    'issuer_id',g.issuer_id,
    'subject_id',g.subject_id,
    'grant_status',g.status,
    'expires_at',g.expires_at,
    'revoked_at',g.revoked_at,
    'source_event_id',g.source_event_id
  );
end;
$$;

grant execute on function public.nayanet_validate_authority_grant(uuid,text,text) to authenticated;
revoke execute on function public.nayanet_validate_authority_grant(uuid,text,text) from anon, public;

drop function if exists public.nayanet_commit_cognition(
  text,bigint,jsonb,text,text,text,text,jsonb,jsonb
);

create function public.nayanet_commit_cognition(
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

  v_authority := public.nayanet_validate_authority_grant(
    p_authority_grant_id,
    p_action,
    p_project_id
  );

  if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
    raise exception 'AUTHORITY_REQUIRED: %', coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
  end if;

  update public.nayanet_project_cognition_state
     set revision = revision + 1,
         state = p_state,
         status = p_status,
         updated_at = now()
   where user_id = auth.uid()
     and project_id = p_project_id
     and revision = p_expected_revision
   returning * into v;

  if not found then
    raise exception 'COGNITION_REVISION_CONFLICT';
  end if;

  insert into public.nayanet_execution_receipts(
    user_id, project_id, revision, action, expected_result, observed_result, status,
    evidence, learning, authority_grant_id, authority_issuer_id, authority_scope,
    authority_actions, authority_constraints, authority_status_at_execution,
    authority_source_event_id, authority_validated_at
  )
  values(
    auth.uid(), p_project_id, v.revision, p_action, p_expected_result, p_observed_result, p_status,
    coalesce(p_evidence,'[]'::jsonb), coalesce(p_learning,'[]'::jsonb),
    (v_authority->>'grant_id')::uuid,
    (v_authority->>'issuer_id')::uuid,
    v_authority->'scope',
    v_authority->'actions',
    v_authority->'constraints',
    v_authority->>'grant_status',
    v_authority->>'source_event_id',
    v_authority_validated_at
  );

  return v;
end;
$function$;

grant execute on function public.nayanet_commit_cognition(
  text,bigint,jsonb,text,text,text,text,jsonb,jsonb,uuid
) to authenticated;
revoke execute on function public.nayanet_commit_cognition(
  text,bigint,jsonb,text,text,text,text,jsonb,jsonb,uuid
) from anon, public;
