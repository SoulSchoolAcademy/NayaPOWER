-- H9-1 — EVOLVE first executable (CANDIDATE / SOURCE-ONLY).
--
-- PROPOSED / SOURCE-ONLY. Not applied to production. Not merged.
--
-- Hole: H9 / H9-1 — nayanet_successor_handoffs has no writer (EVOLVE).
-- At pin 5b68f8dc the table has exactly two repo references — the runtime
-- registry JSON and its own DDL (20260927194144); zero writers. The
-- compounding loop is unclosed: LEARN->EVOLVE and EVOLVE->SELF are ABSENT.
--
-- This migration adds the first governed writer:
--   public.nayanet_evolve_package_successor(...)
-- which packages exactly one successor handoff from VERIFY-locked content
-- ONLY:
--   * the source intelligent block must be owner-scoped,
--     understanding_state='LEARNED', with provenance.learning_verification=true
--     (the nayanet-learning-verify lock-in stamp);
--   * every referenced relationship must be owner-scoped with
--     epistemic_state='VERIFIED'.
--
-- EVOLVE's negative control is STRUCTURAL: authority_inherited is HARDCODED
-- false inside the function body. There is no parameter for it — stale
-- authority can never transfer through this path, by construction.
--
-- Invocation authority (which LAW grant authorizes a live packaging call) is
-- a runtime concern for the caller; this function enforces content governance
-- (verify-locked-only) and no-authority-transfer at the enforcement point.
--
-- Merge and any production application are the Human Director's gates.

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

revoke all on function public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb) from public,anon;
grant execute on function public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb) to authenticated, service_role;

comment on function public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb) is
  'H9-1 EVOLVE first executable (CANDIDATE, source-only): packages one successor handoff '
  'from VERIFY-locked content only (LEARNED block + VERIFIED relationships, owner-scoped). '
  'authority_inherited is hardcoded false — stale authority cannot transfer through this path.';
