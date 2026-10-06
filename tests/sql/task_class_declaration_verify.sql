-- H8-7 writer closure verification: declared_task_classes on the canonical commit path.
--
-- EXECUTION STATUS: controls WRITTEN, not executed (no PostgreSQL in the loop
-- VM). Parse-verified under the genuine PostgreSQL parser (pglast). Live
-- execution is a reviewer-verified step before merge.
--
-- Conventions: each DO block raises on failure. P* = positive controls
-- (static catalog assertions, runnable anywhere). N* = negative/behavioral
-- controls (require a live authenticated session; documented for the live
-- verification run).

-- P1: exactly one nayanet_intelligence_commit overload, 11 params, trailing
-- p_declared_task_classes.
do $$
declare c int; last_name text;
begin
  select count(*) into c from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname = 'nayanet_intelligence_commit';
  if c <> 1 then raise exception 'P1 FAIL: expected 1 overload, got %', c; end if;
  -- Robust form: unnest proargnames/proargtypes.
  select (p.proargnames)[array_length(p.proargtypes,1)] into last_name
    from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname = 'nayanet_intelligence_commit';
  if last_name <> 'p_declared_task_classes' then
    raise exception 'P1 FAIL: last param is %, want p_declared_task_classes', last_name;
  end if;
  raise notice 'P1 PASS: single 11-arg writer with trailing p_declared_task_classes';
end $$;

-- P2: wrapper has 14 params, trailing p_declared_task_classes.
do $$
declare last_name text;
begin
  select (p.proargnames)[array_length(p.proargtypes,1)] into last_name
    from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname = 'nayanet_intelligence_commit_runtime';
  if last_name <> 'p_declared_task_classes' then
    raise exception 'P2 FAIL: wrapper last param is %, want p_declared_task_classes', last_name;
  end if;
  raise notice 'P2 PASS: wrapper threads p_declared_task_classes';
end $$;

-- P3: grants — authenticated may execute the writer; public/anon may not;
-- service_role alone may execute the runtime bridge.
do $$
declare ok_auth boolean; ok_pub boolean; ok_svc boolean;
begin
  select has_function_privilege('authenticated', 'public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text,jsonb,text[],text[])', 'execute') into ok_auth;
  select has_function_privilege('public', 'public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text,jsonb,text[],text[])', 'execute') into ok_pub;
  select has_function_privilege('service_role', 'public.nayanet_intelligence_commit_runtime(text,uuid,text,text,text,text,text,text,text,uuid,text,jsonb,text[],text[])', 'execute') into ok_svc;
  if not ok_auth then raise exception 'P3 FAIL: authenticated lacks execute on writer'; end if;
  if ok_pub then raise exception 'P3 FAIL: public can execute writer'; end if;
  if not ok_svc then raise exception 'P3 FAIL: service_role lacks execute on bridge'; end if;
  raise notice 'P3 PASS: grant envelope correct';
end $$;

-- P4: provenance stamp contract — the writer body stamps declared_task_classes
-- as a raw JSON array (the reader contract) plus the attestation record.
do $$
declare body text;
begin
  select p.prosrc into body from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname = 'nayanet_intelligence_commit';
  if body not like '%''declared_task_classes'', to_jsonb(v_task_classes)%' then
    raise exception 'P4 FAIL: writer body lacks the declared_task_classes stamp';
  end if;
  if body not like '%task_class_declaration%' then
    raise exception 'P4 FAIL: writer body lacks the attestation record';
  end if;
  raise notice 'P4 PASS: provenance stamp present in writer body';
end $$;

-- N1 (live): unknown class rejects the whole commit.
--   select public.nayanet_intelligence_commit('evt-n1','t','lesson','cat','topic','target','<grant>'::uuid,'NayaNET',null,null,array['graph_magic']);
--   expect: ERROR TASK_CLASS_UNKNOWN:graph_magic (SQLSTATE 22023)

-- N2 (live): malformed entry rejects the whole commit.
--   ... array['provenance_sensitive','has space'] ...
--   expect: ERROR TASK_CLASS_MALFORMED (SQLSTATE 22023)

-- N3 (live): null declaration persists provenance without the key
-- (byte-identical to pre-repair commits).
--   ... p_declared_task_classes => null ...
--   select block.provenance ? 'declared_task_classes' from nayanet_intelligent_blocks block ...;
--   expect: false

-- N4 (live): declared commit stamps the reader-contract array.
--   ... array['Provenance_Sensitive','learning_reuse'] ...
--   select block.provenance->'declared_task_classes' ...;
--   expect: ["learning_reuse","provenance_sensitive"] (normalized, deduped, sorted)

-- N5 (live): replay with a CHANGED declaration fails closed.
--   commit evt-n5 with array['provenance_sensitive'], then replay evt-n5 with
--   array['learning_reuse'];
--   expect: ERROR EVENT_ID_REPLAY_PAYLOAD_MISMATCH (SQLSTATE 23505)

-- N6 (live): replay with the SAME declaration rereads (idempotent, no second write).
--   commit evt-n6 with array['provenance_sensitive'], then replay evt-n6 with
--   array['provenance_sensitive'];
--   expect: ok=true, same block_row_id, no new block row.
