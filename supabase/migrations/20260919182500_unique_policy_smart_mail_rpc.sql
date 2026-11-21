-- CHAIN REPAIR (Path A, file 91) — restored from history, 2026-11-21.
-- Source: supabase/history/pre-production-ledger-reconciliation-20260929/20260919182500_unique_policy_smart_mail_rpc.sql
-- (blob bb42d13e13caa8034ad1eb2873cc4c8cf1d1a54c, 3,728 B, sha256 049614debdb4c4f9be4073812b289558fcec7cb2ac3fc128d5cb54d1b9970b85).
-- The CREATE below is byte-identical to the source file's lines 1-88: the 12-arg
-- nayanet_send_smart_mail_policy_authorized overload (no p_request_id).
-- WHY RESTORED: supabase/migrations/20260919200657_delta1_receipt_bound_cimc_request_id.sql (file 87)
-- and supabase/migrations/20260919220443_harden_smart_mail_authority_constraints_v1.sql (file 91) both
-- REVOKE this 12-arg overload. It exists on production but in no chain migration, so a from-zero replay
-- fails at file 91 with 42883 (function does not exist). This file puts the overload back in the chain
-- at its true historical version, between 20260919180321 and 20260919182648.
-- WHY THE TAIL DIFFERS FROM THE SOURCE: the source file GRANTs execute to authenticated,service_role.
-- Version 20260919182500 is NOT recorded in production's supabase_migrations (verified 2026-11-21:
-- the exact-version query returns no row), so a production dispatch WOULD apply this file. On production
-- today the 12-arg overload has NO execute grant for any app role — file 87 revoked it from
-- public,anon,authenticated,service_role and file 91 from public,anon,authenticated — and file 91's own
-- comment states the deprecated overloads "must not be executable by authenticated callers".
-- A verbatim GRANT would re-open the deprecated overload to authenticated callers on production at
-- dispatch time, and file 91 (already recorded as applied) would never re-run its REVOKE to undo it.
-- The tail therefore REVOKEs from all four roles and grants nothing, reproducing production's live
-- end state exactly. Production effect of applying this file: none (CREATE OR REPLACE of the identical
-- definition; REVOKE of already-revoked privileges).
-- P1: unique RPC surface for policy-authorized Smart Mail.
-- Supabase/PostgREST RPC does not safely support this overloaded function family;
-- the policy path gets a unique name so all lineage arguments are unambiguous.

create or replace function public.nayanet_send_smart_mail_policy_authorized(
  p_sender_id uuid,
  p_receiver_id uuid,
  p_body text,
  p_subject text,
  p_kind text,
  p_idempotency_key text,
  p_project_id text,
  p_policy_id uuid,
  p_experiment_case_id text,
  p_policy_input_hash text,
  p_policy_decision_hash text,
  p_authority_grant_id uuid
)
returns jsonb
language plpgsql
security definer
set search_path=''
as $function$
declare
  v_authority jsonb;
  v_result jsonb;
  v_sender uuid := auth.uid();
  v_mutual boolean;
begin
  if v_sender is null then raise exception 'AUTH_REQUIRED'; end if;
  if v_sender <> p_sender_id then raise exception 'SENDER_IDENTITY_MISMATCH'; end if;
  if p_policy_id is null or p_experiment_case_id is null
     or p_policy_input_hash is null or p_policy_decision_hash is null then
    raise exception 'POLICY_LINEAGE_REQUIRED';
  end if;

  select exists(
    select 1
    from public.nayanet_connections a
    join public.nayanet_connections b
      on b.owner_member_id=p_receiver_id
     and b.connected_member_id=p_sender_id
     and b.status='active'
    where a.owner_member_id=p_sender_id
      and a.connected_member_id=p_receiver_id
      and a.status='active'
  ) into v_mutual;
  if not v_mutual then raise exception 'RELATIONSHIP_REQUIRED'; end if;

  v_authority:=public.nayanet_validate_authority_grant(
    p_authority_grant_id,'smart_mail_send',p_receiver_id::text
  );
  if coalesce(v_authority->>'status','BLOCKED') <> 'AUTHORIZED' then
    raise exception 'AUTHORITY_REQUIRED: %',
      coalesce(v_authority->>'reason','AUTHORIZATION_BLOCKED');
  end if;

  select public.nayanet_send_smart_mail(
    p_sender_id,p_receiver_id,p_body,p_subject,p_kind,p_idempotency_key,p_project_id,
    p_policy_id,p_experiment_case_id,p_policy_input_hash,p_policy_decision_hash
  ) into v_result;

  if coalesce(v_result->>'status','')='CREATED' then
    update public.nayanet_execution_receipts
      set authority_grant_id=(v_authority->>'grant_id')::uuid,
          authority_issuer_id=(v_authority->>'issuer_id')::uuid,
          authority_scope=v_authority->'scope',
          authority_actions=v_authority->'actions',
          authority_constraints=v_authority->'constraints',
          authority_status_at_execution=v_authority->>'grant_status',
          authority_source_event_id=v_authority->>'source_event_id',
          authority_validated_at=clock_timestamp(),
          policy_id=p_policy_id,
          policy_version=(select pv.version from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          policy_key=(select pv.policy_key from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          policy_parent_id=(select pv.parent_policy_id from public.nayanet_policy_versions pv where pv.id=p_policy_id),
          experiment_case_id=p_experiment_case_id,
          policy_input_hash=p_policy_input_hash,
          policy_decision_hash=p_policy_decision_hash
    where id=(v_result->>'execution_receipt_id')::uuid;
  end if;

  return v_result || jsonb_build_object(
    'authority_grant_id',v_authority->>'grant_id',
    'relationship_gate','mutual_active_connection'
  );
end;
$function$;

-- The deprecated 12-arg overload must not be executable by any app role.
-- Production's live end state (files 87 + 91 revoked all four roles) is reproduced here:
-- revoke from public, anon, authenticated AND service_role; grant nothing.
revoke all on function public.nayanet_send_smart_mail_policy_authorized(
  uuid,uuid,text,text,text,text,text,uuid,text,text,text,uuid
) from public,anon,authenticated,service_role;
