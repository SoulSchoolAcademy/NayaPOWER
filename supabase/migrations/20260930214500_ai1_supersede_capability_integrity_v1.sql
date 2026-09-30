-- AI1 follow-up integrity: preserve declared capabilities across the existing
-- governed supersession runtime without changing legacy callers.
--
-- Depends on:
--   20260930235959_ai1_capability_carry_v1.sql
--
-- Why: the canonical commit path now persists content.capabilities, but the
-- supersession runtime still rebuilt successor content as {lesson} only. A
-- revision through that existing writer surface could therefore silently drop
-- purpose metadata and make a previously retrievable lesson unselectable.
--
-- This migration changes ONLY the supersession runtime bridge. The underlying
-- nayanet_supersede_intelligent_block writer already accepts arbitrary content
-- JSON and owns the block/edge supersession semantics.
--
-- Backward compatibility:
-- - p_topic / p_category / p_capabilities are trailing optional parameters.
-- - existing callers that omit them persist the exact legacy {lesson} content.
-- - capability validation mirrors the canonical bounded writer vocabulary.
-- - no epistemic-state or authority semantics change.

drop function if exists public.nayanet_supersede_intelligent_block_runtime(text,uuid,text,uuid,uuid,text,text,text,text,text,text,text,jsonb);

create function public.nayanet_supersede_intelligent_block_runtime(
  p_naya_id text,p_owner_id uuid,p_runtime_jti text,p_authority_grant_id uuid,
  p_superseded_block_id uuid,p_title text,p_content text,p_idempotency_key text,
  p_project_id text default 'NayaNET',
  p_block_type text default 'GOVERNED_INTELLIGENCE',
  p_understanding_state text default 'CANDIDATE',
  p_owner_scope text default 'PRIVATE',
  p_connections jsonb default null,
  p_topic text default null,
  p_category text default null,
  p_capabilities text[] default null
) returns jsonb language plpgsql security definer set search_path='' as $function$
declare
  grant_row record;
  new_row public.nayanet_intelligent_blocks;
  v_capabilities text[];
  v_cap_raw text;
  v_cap_norm text;
  v_content jsonb;
  v_provenance jsonb;
begin
 if p_naya_id <> 'NAYA-NODE-0001' then raise exception using errcode='42501',message='NAYA_ID_NOT_AUTHORIZED'; end if;
 if coalesce(trim(p_runtime_jti),'')='' then raise exception using errcode='22023',message='RUNTIME_JTI_REQUIRED'; end if;

 v_capabilities := null;
 if p_capabilities is not null and coalesce(array_length(p_capabilities,1),0) > 0 then
   v_capabilities := '{}';
   foreach v_cap_raw in array p_capabilities loop
     if v_cap_raw is null then raise exception using errcode='22023',message='CAPABILITY_MALFORMED:null-entry'; end if;
     v_cap_norm := lower(trim(v_cap_raw));
     if v_cap_norm = '' or v_cap_norm !~ '^[a-z][a-z0-9_]*$' then
       raise exception using errcode='22023',message='CAPABILITY_MALFORMED:' || left(v_cap_raw,64);
     end if;
     if v_cap_norm <> all (array['governance_triage','compounding_capture']) then
       raise exception using errcode='22023',message='CAPABILITY_UNKNOWN:' || v_cap_norm;
     end if;
     if v_cap_norm <> all (v_capabilities) then v_capabilities := v_capabilities || v_cap_norm; end if;
   end loop;
   select array_agg(x order by x) into v_capabilities from unnest(v_capabilities) as x;
 end if;

 select * into grant_row from public.nayanet_authority_grants
 where grant_id=p_authority_grant_id and issuer_id=p_owner_id and subject_id=p_owner_id and status='ACTIVE' and revoked_at is null
 and (expires_at is null or expires_at>clock_timestamp()) and scope->>'target'=p_naya_id and actions @> '["intelligence_commit"]'::jsonb;
 if not found then raise exception using errcode='42501',message='AUTHORITY_BLOCKED'; end if;
 perform set_config('request.jwt.claim.sub',p_owner_id::text,true);

 v_content := jsonb_build_object('lesson',p_content);
 if p_topic is not null then v_content := v_content || jsonb_build_object('topic',p_topic); end if;
 if p_category is not null then v_content := v_content || jsonb_build_object('category',p_category); end if;
 if v_capabilities is not null then v_content := v_content || jsonb_build_object('capabilities',to_jsonb(v_capabilities)); end if;

 v_provenance := jsonb_build_object(
   'writer','nayanet_supersede_intelligent_block_runtime',
   'runtime_identity','naya-node-oidc',
   'runtime_jti',p_runtime_jti,
   'naya_id',p_naya_id,
   'authority_grant_id',p_authority_grant_id
 );
 if v_capabilities is not null then
   v_provenance := v_provenance || jsonb_build_object(
     'capability_declaration',
     jsonb_build_object('source','supersede_runtime_capture','values',to_jsonb(v_capabilities))
   );
 end if;

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
   jsonb_build_array(jsonb_build_object(
     'source','supersede_runtime',
     'idempotency_key',p_idempotency_key,
     'authority_grant_id',p_authority_grant_id,
     'runtime_jti',p_runtime_jti,
     'naya_id',p_naya_id,
     'declared_capabilities',coalesce(to_jsonb(v_capabilities),'[]'::jsonb)
   )),
   v_provenance,
   jsonb_build_object('epistemic_state',coalesce(p_understanding_state,'CANDIDATE')),
   jsonb_build_object('target',p_naya_id,'project_id',p_project_id),
   v_content,
   'INTELLIGENT_BLOCK_V1',
   p_idempotency_key,
   null,
   p_connections
 );

 return row_to_json(new_row)||jsonb_build_object(
   'runtime_identity','naya-node-oidc',
   'naya_id',p_naya_id,
   'runtime_jti',p_runtime_jti,
   'owner_id',p_owner_id,
   'declared_capabilities',coalesce(to_jsonb(v_capabilities),'[]'::jsonb)
 );
end;$function$;

revoke all on function public.nayanet_supersede_intelligent_block_runtime(text,uuid,text,uuid,uuid,text,text,text,text,text,text,text,jsonb,text,text,text[]) from public,anon,authenticated;
grant execute on function public.nayanet_supersede_intelligent_block_runtime(text,uuid,text,uuid,uuid,text,text,text,text,text,text,text,jsonb,text,text,text[]) to service_role;
