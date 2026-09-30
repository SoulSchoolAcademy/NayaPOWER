-- Harden the independent authority validator so its transaction-scoped row lock
-- does not require authenticated clients to receive UPDATE privileges.
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
    return jsonb_build_object('status','BLOCKED','reason','GRANT_NOT_FOUND_OR_NOT_OWNED','grant_id',p_grant_id);
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
      'status','AUTHORIZED','reason','VALID_IN_SCOPE_GRANT',
      'grant_id',g.grant_id,'issuer_id',g.issuer_id,'subject_id',g.subject_id,
      'mission_id',g.mission_id,'scope',g.scope,'actions',g.actions,
      'constraints',g.constraints,'issued_at',g.issued_at,'expires_at',g.expires_at,
      'grant_status','ACTIVE','revoked_at',g.revoked_at,'evidence',g.evidence,
      'source_event_id',g.source_event_id
    );
  end if;

  return jsonb_build_object(
    'status','BLOCKED','reason',reason,'grant_id',g.grant_id,
    'issuer_id',g.issuer_id,'subject_id',g.subject_id,'grant_status',g.status,
    'expires_at',g.expires_at,'revoked_at',g.revoked_at,'source_event_id',g.source_event_id
  );
end;
$$;

grant execute on function public.nayanet_validate_authority_grant(uuid,text,text) to authenticated;
revoke execute on function public.nayanet_validate_authority_grant(uuid,text,text) from anon, public;
