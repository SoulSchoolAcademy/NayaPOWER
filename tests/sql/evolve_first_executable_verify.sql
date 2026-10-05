-- H9-1 EVOLVE first executable verification.
-- Fresh scratch DB only. Creates stub tables matching the canonical DDL
-- (20260927194144), applies the real candidate migration, and proves:
-- VERIFY-locked-only packaging, fail-closed refusals, structural
-- no-authority-transfer, and grant posture.
--
-- CONTROLS EXECUTED 2026-10-05 (UTC) on a genuine PostgreSQL 16 scratch DB:
-- 15/15 PASS (3 positive / 6 negative / 2 structural / 4 grant). Parse-verified
-- with the genuine PostgreSQL parser (pglast). Non-vacuity proven by mutant
-- kill: block-lock removed => EV-N1 catches; rel-verified removed => EV-N3
-- catches. EV-P2 repaired 2026-10-05: the original nested the packaging call
-- inside the asserting SELECT; the outer scan uses the statement-start MVCC
-- snapshot, which predates the initplan's INSERT (0 rows => false failure).
-- The call now runs in its own statement. (TEST DEFECT in this file, not a
-- bug in the migration.)
\set QUIET on
\pset footer off
create extension if not exists pgcrypto;

-- ---- scratch identity + roles -------------------------------------------
create table if not exists public.members (id uuid primary key default gen_random_uuid());
do $$
begin
  if not exists (select 1 from pg_roles where rolname='authenticated') then create role authenticated nologin; end if;
  if not exists (select 1 from pg_roles where rolname='anon') then create role anon nologin; end if;
  if not exists (select 1 from pg_roles where rolname='service_role') then create role service_role nologin; end if;
end $$;

-- ---- stub tables: DDL-exact columns for the three tables the function touches
create table public.nayanet_intelligent_blocks (
  block_id uuid primary key,
  intelligent_block_id text,
  owner_id uuid not null references public.members(id) on delete cascade,
  subject_id text not null, title text not null, block_type text not null,
  version bigint not null default 1, status text not null default 'ACTIVE',
  understanding_state text not null default 'CANDIDATE',
  owner_scope text not null default 'PRIVATE',
  source_event_ids uuid[] not null,
  evidence_refs jsonb not null default '[]', provenance jsonb not null default '{}',
  value_context jsonb not null default '{}', applicable_scope jsonb not null default '{}',
  content jsonb not null default '{}',
  supersedes_block_id uuid, superseded_by_block_id uuid,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now(),
  schema_version text not null default 'INTELLIGENT_BLOCK_V1'
);
create table public.nayanet_brain_relationships (
  relationship_id uuid primary key default gen_random_uuid(),
  owner_id uuid not null references public.members(id) on delete cascade,
  source_id text not null, target_id text not null, relationship_type text not null,
  provenance jsonb not null default '{}',
  epistemic_state text not null default 'UNKNOWN',
  created_at timestamptz not null default now()
);
create table public.nayanet_successor_handoffs (
  handoff_id uuid primary key default gen_random_uuid(), parent_node_id text not null,
  successor_node_id text not null unique,
  owner_id uuid not null references public.members(id) on delete cascade,
  mission text not null, context jsonb not null default '{}',
  authority_inherited boolean not null default false,
  source_event_ids jsonb not null default '[]', proof jsonb not null default '{}',
  created_at timestamptz not null default now()
);

\ir ../../supabase/migrations/20261003170000_evolve_first_executable_v1.sql

create or replace function verify_assert(p_name text,p_ok boolean)
returns void language plpgsql as $$
begin
  if not coalesce(p_ok,false) then raise exception 'VERIFY FAILED: %',p_name; end if;
  raise notice 'PASS: %',p_name;
end $$;

-- ---- fixtures ------------------------------------------------------------
do $$
declare a uuid; b uuid; blk_locked uuid; blk_cand uuid; blk_unstamped uuid;
        rel_ok uuid; rel_unknown uuid; rel_foreign uuid;
begin
  insert into public.members default values returning id into a;
  insert into public.members default values returning id into b;

  insert into public.nayanet_intelligent_blocks
    (block_id, owner_id, subject_id, title, block_type, understanding_state,
     source_event_ids, provenance, content)
  values
    (gen_random_uuid(), a, 'SUBJ', 'verify-locked lesson', 'LESSON', 'LEARNED',
     array[gen_random_uuid()],
     '{"learning_verification": true, "learning_id": "L-1"}'::jsonb,
     '{"lesson": "persistence alone is memory, not proof of active intelligence"}'::jsonb)
  returning block_id into blk_locked;

  insert into public.nayanet_intelligent_blocks
    (block_id, owner_id, subject_id, title, block_type, understanding_state,
     source_event_ids, provenance, content)
  values
    (gen_random_uuid(), a, 'SUBJ', 'candidate lesson', 'LESSON', 'CANDIDATE',
     array[gen_random_uuid()], '{}'::jsonb, '{}'::jsonb)
  returning block_id into blk_cand;

  insert into public.nayanet_intelligent_blocks
    (block_id, owner_id, subject_id, title, block_type, understanding_state,
     source_event_ids, provenance, content)
  values
    (gen_random_uuid(), a, 'SUBJ', 'learned but unstamped', 'LESSON', 'LEARNED',
     array[gen_random_uuid()], '{}'::jsonb, '{}'::jsonb)
  returning block_id into blk_unstamped;

  insert into public.nayanet_brain_relationships
    (owner_id, source_id, target_id, relationship_type, epistemic_state, provenance)
  values
    (a, 'IB-1', 'IB-2', 'SUPPORTS', 'VERIFIED', '{"learning_verification": true}'::jsonb)
  returning relationship_id into rel_ok;

  insert into public.nayanet_brain_relationships
    (owner_id, source_id, target_id, relationship_type, epistemic_state)
  values
    (a, 'IB-1', 'IB-3', 'SUPPORTS', 'UNKNOWN')
  returning relationship_id into rel_unknown;

  insert into public.nayanet_brain_relationships
    (owner_id, source_id, target_id, relationship_type, epistemic_state)
  values
    (b, 'IB-9', 'IB-8', 'SUPPORTS', 'VERIFIED')
  returning relationship_id into rel_foreign;

  perform set_config('verify.a', a::text, false);
  perform set_config('verify.blk_locked', blk_locked::text, false);
  perform set_config('verify.blk_cand', blk_cand::text, false);
  perform set_config('verify.blk_unstamped', blk_unstamped::text, false);
  perform set_config('verify.rel_ok', rel_ok::text, false);
  perform set_config('verify.rel_unknown', rel_unknown::text, false);
  perform set_config('verify.rel_foreign', rel_foreign::text, false);
end $$;

-- ---- positive controls ----------------------------------------------------
select verify_assert('EV-P1 verify-locked block + verified rel => packaged, no authority transfer',
  (select r.receipt->>'ok' = 'true'
     and r.receipt->>'schema' = 'NAYANET_EVOLVE_RECEIPT_V1'
     and (r.receipt->>'authority_inherited')::boolean = false
     and r.receipt->'reason_codes' ? 'NO_AUTHORITY_TRANSFER'
     from public.nayanet_evolve_package_successor(
       current_setting('verify.a')::uuid, 'NAYA-4', 'SUCCESSOR-1',
       'continue the compounding mission',
       current_setting('verify.blk_locked')::uuid,
       array[current_setting('verify.rel_ok')::uuid],
       '{"lane":"self-build"}'::jsonb) as r(receipt)));

select verify_assert('EV-P1b exactly one handoff row, authority_inherited=false, verify-locked proof',
  (select count(*) = 1
     and bool_and(authority_inherited = false)
     and bool_and(proof->>'schema' = 'NAYANET_EVOLVE_PACKAGE_V1')
     and bool_and(proof->'verify_locked'->>'understanding_state' = 'LEARNED')
     and bool_and((proof->'verify_locked'->'verified_relationships')::text <> '[]')
   from public.nayanet_successor_handoffs));

-- EV-P2 note: the packaging call MUST run in its own statement. A call nested
-- inside the asserting SELECT cannot see its own freshly inserted row: the
-- outer scan uses the statement-start MVCC snapshot, which predates the
-- initplan's INSERT (0 rows => false failure). Separate statements see the
-- committed row.
do $$
begin
  perform public.nayanet_evolve_package_successor(
    current_setting('verify.a')::uuid, 'NAYA-4', 'SUCCESSOR-2', 'm2',
    current_setting('verify.blk_locked')::uuid);
end $$;

select verify_assert('EV-P2 locked block with no relationships => packaged, empty verified list',
  (select (proof->'verify_locked'->'verified_relationships') = '[]'::jsonb
   from public.nayanet_successor_handoffs
   where successor_node_id = 'SUCCESSOR-2'));

-- ---- negative controls ----------------------------------------------------
do $$
declare v_msg text;
begin
  begin
    perform public.nayanet_evolve_package_successor(
      current_setting('verify.a')::uuid, 'NAYA-4', 'S-N1', 'm',
      current_setting('verify.blk_cand')::uuid);
    raise exception 'VERIFY FAILED: EV-N1 candidate block packaged';
  exception when others then
    if SQLERRM like 'VERIFY FAILED:%' then raise; end if;
    if SQLERRM <> 'EVOLVE_BLOCK_NOT_VERIFY_LOCKED' then raise; end if;
    raise notice 'PASS: EV-N1 candidate block refused (EVOLVE_BLOCK_NOT_VERIFY_LOCKED)';
  end;
end $$;

do $$
begin
  begin
    perform public.nayanet_evolve_package_successor(
      current_setting('verify.a')::uuid, 'NAYA-4', 'S-N2', 'm',
      current_setting('verify.blk_unstamped')::uuid);
    raise exception 'VERIFY FAILED: EV-N2 unstamped LEARNED block packaged';
  exception when others then
    if SQLERRM like 'VERIFY FAILED:%' then raise; end if;
    if SQLERRM <> 'EVOLVE_BLOCK_NOT_VERIFY_LOCKED' then raise; end if;
    raise notice 'PASS: EV-N2 LEARNED-but-unstamped block refused (EVOLVE_BLOCK_NOT_VERIFY_LOCKED)';
  end;
end $$;

do $$
begin
  begin
    perform public.nayanet_evolve_package_successor(
      current_setting('verify.a')::uuid, 'NAYA-4', 'S-N3', 'm',
      current_setting('verify.blk_locked')::uuid,
      array[current_setting('verify.rel_unknown')::uuid]);
    raise exception 'VERIFY FAILED: EV-N3 unverified relationship packaged';
  exception when others then
    if SQLERRM like 'VERIFY FAILED:%' then raise; end if;
    if SQLERRM <> 'EVOLVE_RELATIONSHIP_NOT_VERIFIED' then raise; end if;
    raise notice 'PASS: EV-N3 UNKNOWN relationship refused (EVOLVE_RELATIONSHIP_NOT_VERIFIED)';
  end;
end $$;

do $$
begin
  begin
    perform public.nayanet_evolve_package_successor(
      current_setting('verify.a')::uuid, 'NAYA-4', 'S-N4', 'm',
      current_setting('verify.blk_locked')::uuid,
      array[current_setting('verify.rel_foreign')::uuid]);
    raise exception 'VERIFY FAILED: EV-N4 foreign-owner relationship packaged';
  exception when others then
    if SQLERRM like 'VERIFY FAILED:%' then raise; end if;
    if SQLERRM <> 'EVOLVE_RELATIONSHIP_NOT_VERIFIED' then raise; end if;
    raise notice 'PASS: EV-N4 foreign-owner relationship refused (EVOLVE_RELATIONSHIP_NOT_VERIFIED)';
  end;
end $$;

do $$
begin
  begin
    perform public.nayanet_evolve_package_successor(
      current_setting('verify.a')::uuid, 'NAYA-4', 'S-N5', '  ',
      current_setting('verify.blk_locked')::uuid);
    raise exception 'VERIFY FAILED: EV-N5 empty mission packaged';
  exception when others then
    if SQLERRM like 'VERIFY FAILED:%' then raise; end if;
    if SQLERRM <> 'EVOLVE_MISSION_REQUIRED' then raise; end if;
    raise notice 'PASS: EV-N5 empty mission refused (EVOLVE_MISSION_REQUIRED)';
  end;
end $$;

do $$
begin
  begin
    perform public.nayanet_evolve_package_successor(
      current_setting('verify.a')::uuid, 'NAYA-4', 'SUCCESSOR-1', 'm',
      current_setting('verify.blk_locked')::uuid);
    raise exception 'VERIFY FAILED: EV-N6 duplicate successor_node_id packaged';
  exception when others then
    if SQLERRM like 'VERIFY FAILED:%' then raise; end if;
    if SQLERRM <> 'EVOLVE_SUCCESSOR_NODE_ID_TAKEN' then raise; end if;
    raise notice 'PASS: EV-N6 duplicate successor_node_id refused (EVOLVE_SUCCESSOR_NODE_ID_TAKEN)';
  end;
end $$;

-- EV-N7: structural no-authority-transfer — the function exposes NO
-- authority_inherited parameter; the value is hardcoded in the body.
select verify_assert('EV-N7 no authority_inherited parameter exists on the function',
  (select count(*) = 0
   from unnest((select proargnames
                from pg_proc where proname = 'nayanet_evolve_package_successor')) as arg
   where arg = 'authority_inherited'));

select verify_assert('EV-N8 function body hardcodes authority_inherited=false (no stale transfer possible)',
  (select prosrc like '%authority_inherited%'
     and prosrc not like '%p_authority_inherited%'
     and (select bool_and(authority_inherited = false) from public.nayanet_successor_handoffs)
   from pg_proc where proname = 'nayanet_evolve_package_successor'));

-- ---- grant controls --------------------------------------------------------
select verify_assert('EV-G1 evolve packager not executable by anon',
  not has_function_privilege('anon',
    'public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb)','execute'));

select verify_assert('EV-G2 evolve packager not executable by public',
  not has_function_privilege('public',
    'public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb)','execute'));

select verify_assert('EV-G3 evolve packager executable by authenticated',
  has_function_privilege('authenticated',
    'public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb)','execute'));

select verify_assert('EV-G4 evolve packager executable by service_role',
  has_function_privilege('service_role',
    'public.nayanet_evolve_package_successor(uuid,text,text,text,uuid,uuid[],jsonb)','execute'));

drop function if exists verify_assert(text,boolean);
\echo 'ALL H9-1 EVOLVE FIRST-EXECUTABLE CONTROLS PASSED'
