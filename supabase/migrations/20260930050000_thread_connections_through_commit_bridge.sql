-- CONNECT writer threading: expose the R1 connections contract through the
-- governed runtime bridges so the CONNECT live proof (and any future
-- governed caller) can write edges through the runtime instead of raw SQL.
--
-- PREREQUISITE: migration 20260930040000_r1_writer_connections_v1.sql
-- (R1 writer contract) must be deployed first. This migration threads the
-- already-merged writers' p_connections parameters through the
-- SECURITY DEFINER runtime bridges.
--
-- ONE GRAPH: nayanet_brain_relationships remains the system of record.
-- The bridges do not create a second graph; they forward candidate edges
-- to the writers, which normalize them into the connections projection
-- and the canonical edge rows atomically (fail closed on forged types,
-- prose targets, and cross-owner targets).
--
-- Additive only. Existing callers of nayanet_intelligence_commit_runtime
-- keep working unchanged (p_connections defaults to null -> normalized
-- to '[]' by the writer).

-- §1. Commit bridge: thread p_connections to the R1 commit writer.
--
-- The previous bridge signature (20260928174822) cannot be altered with
-- CREATE OR REPLACE (PostgreSQL forbids changing a function's argument
-- list), so it is dropped and recreated with the appended trailing
-- parameter, following the same pattern as the R1 migration itself.
drop function if exists public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text);

create function public.nayanet_intelligence_commit_runtime(
  p_naya_id text,p_owner_id uuid,p_runtime_jti text,p_event_id text,p_title text,p_content text,p_category text,p_topic text,p_target_id text,p_authority_grant_id uuid,p_project_id text default 'NayaNET',p_connections jsonb default null
) returns jsonb language plpgsql security definer set search_path='' as $function$
declare grant_row record; result jsonb; receipt_id uuid;
begin
 if p_naya_id <> 'NAYA-NODE-0001' then raise exception using errcode='42501',message='NAYA_ID_NOT_AUTHORIZED'; end if;
 if coalesce(trim(p_runtime_jti),'')='' then raise exception using errcode='22023',message='RUNTIME_JTI_REQUIRED'; end if;
 select * into grant_row from public.nayanet_authority_grants
 where grant_id=p_authority_grant_id and issuer_id=p_owner_id and subject_id=p_owner_id and status='ACTIVE' and revoked_at is null
 and (expires_at is null or expires_at>clock_timestamp()) and scope->>'target'=p_naya_id and actions @> '["intelligence_commit"]'::jsonb;
 if not found then raise exception using errcode='42501',message='AUTHORITY_BLOCKED'; end if;
 perform set_config('request.jwt.claim.sub',p_owner_id::text,true);
 result:=public.nayanet_intelligence_commit(p_event_id,p_title,p_content,p_category,p_topic,p_target_id,p_authority_grant_id,p_project_id,p_connections);
 receipt_id:=(result->>'receipt_id')::uuid;
 update public.nayanet_execution_receipts set evidence=evidence||jsonb_build_object('runtime_identity','naya-node-oidc','naya_id',p_naya_id,'runtime_jti',p_runtime_jti,'owner_id',p_owner_id) where id=receipt_id;
 return result||jsonb_build_object('runtime_identity','naya-node-oidc','naya_id',p_naya_id,'runtime_jti',p_runtime_jti,'owner_id',p_owner_id);
end;$function$;
revoke all on function public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text,jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text,jsonb) to service_role;

-- §2. Supersession bridge: governed runtime exposure of the promoted
-- supersession writer (20260930040000 §6). The writer itself is
-- SECURITY DEFINER + service_role-only with no edge-function exposure;
-- this bridge adds the OIDC runtime identity + jti + authority-grant
-- checks that the commit bridge applies, then calls the writer with
-- sensible governed defaults for the remaining parameters.
--
-- Note: the trailing parameters after p_project_id carry defaults but
-- later parameters (p_superseded_block_id, p_idempotency_key) do not, so
-- callers must use named notation for those (the edge function does).
-- Re-runnable: drop the previous bridge signature first (same pattern as §1;
-- PostgreSQL cannot CREATE OR REPLACE across an argument-list change).
drop function if exists public.nayanet_supersede_intelligent_block_runtime(text,uuid,text,uuid,text,uuid,text,text,text,text,text,text,jsonb);

create function public.nayanet_supersede_intelligent_block_runtime(
  p_naya_id text,p_owner_id uuid,p_runtime_jti text,p_authority_grant_id uuid,
  p_project_id text default 'NayaNET',
  p_superseded_block_id uuid default null,p_title text default null,p_content text default null,
  p_block_type text default 'GOVERNED_INTELLIGENCE',
  p_understanding_state text default 'CANDIDATE',
  p_owner_scope text default 'PRIVATE',
  p_idempotency_key text default null,
  p_connections jsonb default null
) returns jsonb language plpgsql security definer set search_path='' as $function$
declare grant_row record; new_row public.nayanet_intelligent_blocks;
begin
 if p_naya_id <> 'NAYA-NODE-0001' then raise exception using errcode='42501',message='NAYA_ID_NOT_AUTHORIZED'; end if;
 if coalesce(trim(p_runtime_jti),'')='' then raise exception using errcode='22023',message='RUNTIME_JTI_REQUIRED'; end if;
 select * into grant_row from public.nayanet_authority_grants
 where grant_id=p_authority_grant_id and issuer_id=p_owner_id and subject_id=p_owner_id and status='ACTIVE' and revoked_at is null
 and (expires_at is null or expires_at>clock_timestamp()) and scope->>'target'=p_naya_id and actions @> '["intelligence_commit"]'::jsonb;
 if not found then raise exception using errcode='42501',message='AUTHORITY_BLOCKED'; end if;
 perform set_config('request.jwt.claim.sub',p_owner_id::text,true);
 -- Defaults: evidence_refs carries the runtime + authority envelope so the
 -- new row stays eligible for retrieval (evidence_refs must be non-empty);
 -- content is the governed lesson shape the commit writer uses; the
 -- intelligent_block_id is minted fresh from the sequence by the writer
 -- (never reused, never suffixed -- see 20260930040000 §6 hazard fix).
 select * into new_row from public.nayanet_supersede_intelligent_block(
   p_superseded_block_id,
   gen_random_uuid(),
   p_owner_id,
   p_naya_id,
   p_title,
   p_block_type,
   p_understanding_state,
   p_owner_scope,
   '{}'::uuid[],
   jsonb_build_array(jsonb_build_object('source','supersede_runtime','idempotency_key',p_idempotency_key,'authority_grant_id',p_authority_grant_id,'runtime_jti',p_runtime_jti,'naya_id',p_naya_id)),
   jsonb_build_object('writer','nayanet_supersede_intelligent_block_runtime','runtime_identity','naya-node-oidc','runtime_jti',p_runtime_jti,'naya_id',p_naya_id,'authority_grant_id',p_authority_grant_id),
   jsonb_build_object('epistemic_state',coalesce(p_understanding_state,'CANDIDATE')),
   jsonb_build_object('target',p_naya_id,'project_id',p_project_id),
   jsonb_build_object('lesson',p_content),
   'INTELLIGENT_BLOCK_V1',
   p_idempotency_key,
   null,
   p_connections
 );
 return row_to_json(new_row)||jsonb_build_object('runtime_identity','naya-node-oidc','naya_id',p_naya_id,'runtime_jti',p_runtime_jti,'owner_id',p_owner_id);
end;$function$;
revoke all on function public.nayanet_supersede_intelligent_block_runtime(text,uuid,text,uuid,text,uuid,text,text,text,text,text,text,jsonb) from public,anon,authenticated;
grant execute on function public.nayanet_supersede_intelligent_block_runtime(text,uuid,text,uuid,text,uuid,text,text,text,text,text,text,jsonb) to service_role;
