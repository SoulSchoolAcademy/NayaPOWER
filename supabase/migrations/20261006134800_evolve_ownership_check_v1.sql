-- SAFETY HARDENING: ownership check in nayanet_evolve_package_successor (Option 2 / 2026-10-06)
--
-- Context: PR #1649 (20261006133000) emergency-revoked EXECUTE on
--   public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb)
-- because it is SECURITY DEFINER and trusted p_owner_id without verifying the
-- caller. Any authenticated user who knew an owner UUID could package successor
-- handoffs as that owner. This migration is the proper heal (Option 2):
-- the function now verifies the caller IS the owner before proceeding.
--
-- The fix:
--   if auth.uid() is not null and p_owner_id is distinct from auth.uid() then
--     raise exception 'EVOLVE_CALLER_NOT_OWNER';
--   end if;
--
-- Why "is not null and ...": auth.uid() reflects the caller's JWT identity.
--   * Authenticated RPC caller (the attack path): auth.uid() is ALWAYS set by
--     PostgREST from the validated JWT. Impersonation is blocked. Airtight.
--   * service_role caller (edge functions): auth.uid() is null. service_role
--     already bypasses RLS and holds full DB privilege; the function is
--     SECURITY DEFINER precisely so trusted internal callers can write.
--     Blocking them would break the intended service path.
--   * Direct SQL (tests, admin): auth.uid() is null. Direct DB access is a
--     separate trust boundary (a holder of DB credentials needs no function).
-- There is no path by which an UNTRUSTED caller reaches this function with a
-- null auth.uid(): anon cannot execute (revoked), and authenticated RPC
-- always carries the caller's JWT.
--
-- This migration also restores the pre-#1649 grant posture (EXECUTE to
-- authenticated + service_role), which the H9-1 verification suite expects
-- (EV-G3). The restore is safe ONLY because of the ownership check above,
-- applied atomically in the same migration — there is no window where the
-- function is exposed without the check.
--
-- What this migration does NOT do:
--   - Does not change any packaging logic, VERIFY-lock gates, or the
--     hardcoded authority_inherited=false. Smallest effective change.
--   - Does not touch the trigger-function lock-down from #1649.
--   - Does not grant to anon or public.
--
-- Reversibility: re-applying 20261006133000 restores the revoked posture.
-- Idempotent: CREATE OR REPLACE + GRANT (idempotent by nature).

create or replace function public.nayanet_evolve_package_successor(
  p_owner_id uuid,
  p_parent_node_id text,
  p_successor_node_id text,
  p_mission text,
  p_intelligent_block_id uuid,
  p_relationship_ids uuid[] default '{}',
  p_context jsonb default '{}'
)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_block public.nayanet_intelligent_blocks%rowtype;
  v_rel public.nayanet_brain_relationships%rowtype;
  v_rel_id uuid;
  v_verified_rels jsonb := '[]'::jsonb;
  v_handoff_id uuid;
  v_source_events jsonb;
  v_now timestamptz := now();
begin
  if p_owner_id is null then raise exception 'EVOLVE_OWNER_REQUIRED'; end if;

  -- OWNERSHIP CHECK (2026-10-06, Option 2 heal for #1649):
  -- SECURITY DEFINER executes as the function owner, so the CALLER's identity
  -- must be verified explicitly. auth.uid() is the caller's JWT subject and is
  -- unaffected by SECURITY DEFINER. When present (authenticated RPC — the only
  -- untrusted path), the caller must BE the owner. Fail closed.
  if auth.uid() is not null and p_owner_id is distinct from auth.uid() then
    raise exception 'EVOLVE_CALLER_NOT_OWNER';
  end if;

  if p_parent_node_id is null or btrim(p_parent_node_id) = '' then raise exception 'EVOLVE_PARENT_NODE_REQUIRED'; end if;
  if p_successor_node_id is null or btrim(p_successor_node_id) = '' then raise exception 'EVOLVE_SUCCESSOR_NODE_REQUIRED'; end if;
  if p_mission is null or btrim(p_mission) = '' then raise exception 'EVOLVE_MISSION_REQUIRED'; end if;
  if p_intelligent_block_id is null then raise exception 'EVOLVE_BLOCK_REQUIRED'; end if;

  -- VERIFY-locked block only: owner-scoped, LEARNED, lock-in stamped.
  select * into v_block
  from public.nayanet_intelligent_blocks
  where block_id = p_intelligent_block_id
    and owner_id = p_owner_id;

  if v_block.block_id is null then
    raise exception 'EVOLVE_BLOCK_NOT_VERIFY_LOCKED';
  end if;
  if v_block.understanding_state <> 'LEARNED'
     or coalesce(v_block.provenance->>'learning_verification', 'false') <> 'true' then
    raise exception 'EVOLVE_BLOCK_NOT_VERIFY_LOCKED';
  end if;

  -- VERIFIED relationships only: owner-scoped, epistemic_state='VERIFIED'.
  foreach v_rel_id in array coalesce(p_relationship_ids, '{}'::uuid[]) loop
    select * into v_rel
    from public.nayanet_brain_relationships
    where relationship_id = v_rel_id
      and owner_id = p_owner_id;
    if v_rel.relationship_id is null then
      raise exception 'EVOLVE_RELATIONSHIP_NOT_VERIFIED';
    end if;
    if v_rel.epistemic_state <> 'VERIFIED' then
      raise exception 'EVOLVE_RELATIONSHIP_NOT_VERIFIED';
    end if;
    v_verified_rels := v_verified_rels || jsonb_build_object(
      'relationship_id', v_rel.relationship_id,
      'source_id', v_rel.source_id,
      'target_id', v_rel.target_id,
      'relationship_type', v_rel.relationship_type,
      'epistemic_state', v_rel.epistemic_state
    );
  end loop;

  if exists (select 1 from public.nayanet_successor_handoffs
             where successor_node_id = btrim(p_successor_node_id)) then
    raise exception 'EVOLVE_SUCCESSOR_NODE_ID_TAKEN';
  end if;

  v_source_events := to_jsonb(v_block.source_event_ids);

  insert into public.nayanet_successor_handoffs (
    parent_node_id, successor_node_id, owner_id, mission, context,
    authority_inherited, source_event_ids, proof
  ) values (
    btrim(p_parent_node_id), btrim(p_successor_node_id), p_owner_id,
    btrim(p_mission), coalesce(p_context, '{}'::jsonb),
    false, -- HARDCODED: EVOLVE never transfers authority. No parameter exists.
    v_source_events,
    jsonb_build_object(
      'schema', 'NAYANET_EVOLVE_PACKAGE_V1',
      'packaged_at', v_now,
      'verify_locked', jsonb_build_object(
        'intelligent_block_id', v_block.block_id,
        'block_title', v_block.title,
        'understanding_state', v_block.understanding_state,
        'learning_verification', true,
        'verified_relationships', v_verified_rels
      ),
      'reason_codes', jsonb_build_array('VERIFY_LOCKED_ONLY', 'NO_AUTHORITY_TRANSFER')
    )
  ) returning handoff_id into v_handoff_id;

  return jsonb_build_object(
    'schema', 'NAYANET_EVOLVE_RECEIPT_V1',
    'ok', true,
    'handoff_id', v_handoff_id,
    'successor_node_id', btrim(p_successor_node_id),
    'authority_inherited', false,
    'reason_codes', jsonb_build_array('VERIFY_LOCKED_ONLY', 'NO_AUTHORITY_TRANSFER'),
    'packaged_at', v_now
  );
end;
$$;

-- Restore the pre-#1649 grant posture. Safe ONLY because the ownership check
-- above is applied in the same migration. authenticated callers can execute
-- but only as themselves (EV-G3 expectation); service_role unchanged.
revoke all on function public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb) from public,anon;
grant execute on function public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb) to authenticated, service_role;

comment on function public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb) is
  'H9-1 EVOLVE first executable (CANDIDATE, source-only): packages one successor handoff '
  'from VERIFY-locked content only (LEARNED block + VERIFIED relationships, owner-scoped). '
  'OWNERSHIP-ENFORCED 2026-10-06: caller must be p_owner_id when auth.uid() present '
  '(EVOLVE_CALLER_NOT_OWNER). authority_inherited hardcoded false.';
