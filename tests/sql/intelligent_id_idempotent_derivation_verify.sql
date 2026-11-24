-- SQL-side intelligent_id idempotence verification.
--
-- EXECUTION STATUS: controls WRITTEN, not executed (no PostgreSQL in the loop
-- VM). Parse-verified under the genuine PostgreSQL parser (pglast). Live
-- execution is a reviewer-verified step before merge.
--
-- Conventions: each DO block raises on failure. P* = positive controls
-- (static catalog assertions + helper behavior, runnable on a live DB).
-- N* = negative controls (prove the test distinguishes old from new).
--
-- Reference values (from the independent-verification log at pin 692f01d9,
-- job 137765721299):
--   owned (registry) id:    IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system
--   doubled (produced) id:  IB-SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system
--   doubled p_event_id:     SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system

-- P1: helper exists, single overload, immutable, returns text.
do $$
declare c int; vol text;
begin
  select count(*) into c from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname = 'nayanet_canonical_intelligent_id';
  if c <> 1 then raise exception 'P1 FAIL: expected 1 helper overload, got %', c; end if;
  select p.provolatile into vol from pg_proc p join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname = 'nayanet_canonical_intelligent_id';
  if vol <> 'i' then raise exception 'P1 FAIL: helper is not immutable (provolatile=%)', vol; end if;
  raise notice 'P1 PASS: single immutable helper';
end $$;

-- P2: classic event id -> canonical id, byte-identical to the old derivation.
do $$
declare got text;
begin
  got := public.nayanet_canonical_intelligent_id('SMART-NOTE-20261123-sn4709-one-mind-one-living-system');
  if got <> 'IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system' then
    raise exception 'P2 FAIL: got %', got;
  end if;
  raise notice 'P2 PASS: classic input unchanged';
end $$;

-- P3: the exact doubled p_event_id from the SN-4709 failure -> the
-- registry-owned canonical id (the cure, end to end).
do $$
declare got text;
begin
  got := public.nayanet_canonical_intelligent_id('SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system');
  if got <> 'IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system' then
    raise exception 'P3 FAIL: got %', got;
  end if;
  raise notice 'P3 PASS: doubled event id cures to the registry-owned id';
end $$;

-- P4: already-prefixed event id -> same canonical id (producer-proof).
do $$
declare got text;
begin
  got := public.nayanet_canonical_intelligent_id('IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system');
  if got <> 'IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system' then
    raise exception 'P4 FAIL: got %', got;
  end if;
  raise notice 'P4 PASS: already-prefixed input converges';
end $$;

-- P5: double-doubled prefix collapses to the canonical id.
do $$
declare got text;
begin
  got := public.nayanet_canonical_intelligent_id('IB-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system');
  if got <> 'IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system' then
    raise exception 'P5 FAIL: got %', got;
  end if;
  raise notice 'P5 PASS: repeated IB- runs collapse';
end $$;

-- P6: bare stem -> 'IB-<stem>' (old behavior preserved).
do $$
declare got text;
begin
  got := public.nayanet_canonical_intelligent_id('foo');
  if got <> 'IB-foo' then raise exception 'P6 FAIL: got %', got; end if;
  raise notice 'P6 PASS: bare stem unchanged';
end $$;

-- P7: idempotency — helper(helper(x)) = helper(x) for the whole battery.
do $$
declare inp text; once text; twice text;
begin
  foreach inp in array array[
    'SMART-NOTE-20261123-sn4709-one-mind-one-living-system',
    'SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system',
    'IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system',
    'IB-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system',
    'SMART-NOTE-IB-SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system',
    'foo',
    'SMART-NOTE-my-IB-note',
    'a b/c.d'] loop
    once := public.nayanet_canonical_intelligent_id(inp);
    twice := public.nayanet_canonical_intelligent_id(once);
    if twice <> once then
      raise exception 'P7 FAIL: not idempotent for %: % -> %', inp, once, twice;
    end if;
  end loop;
  raise notice 'P7 PASS: idempotent on all 8 battery inputs';
end $$;

-- P8: the writer body calls the helper, and the old inline derivation is gone.
do $$
declare body text;
begin
  select pg_get_functiondef(oid) into body from pg_proc
    where proname = 'nayanet_intelligence_commit'
      and pg_get_function_identity_arguments(oid) =
        'text, text, text, text, text, text, uuid, text, jsonb, text[], text[]';
  if body is null then raise exception 'P8 FAIL: 11-arg writer not found'; end if;
  if body not like '%nayanet_canonical_intelligent_id(p_event_id)%' then
    raise exception 'P8 FAIL: writer does not call the helper';
  end if;
  if body like '%regexp_replace(p_event_id%' then
    raise exception 'P8 FAIL: old inline derivation still present in writer';
  end if;
  raise notice 'P8 PASS: writer single-sourced on the helper';
end $$;

-- P9: grant envelope preserved — authenticated may execute the 11-arg writer;
-- public/anon may not.
do $$
declare ok_auth boolean; ok_pub boolean;
begin
  select has_function_privilege('authenticated', 'public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text,jsonb,text[],text[])', 'execute') into ok_auth;
  select has_function_privilege('public', 'public.nayanet_intelligence_commit(text,text,text,text,text,text,uuid,text,jsonb,text[],text[])', 'execute') into ok_pub;
  if not ok_auth then raise exception 'P9 FAIL: authenticated lacks execute on writer'; end if;
  if ok_pub then raise exception 'P9 FAIL: public can execute writer'; end if;
  raise notice 'P9 PASS: grant envelope correct';
end $$;

-- N1 (non-vacuous): the OLD inline expression reproduces the exact doubled id
-- from the IV log on the failing input — the control distinguishes old/new.
do $$
declare old text;
begin
  old := 'IB-' || regexp_replace('SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system', '[^A-Za-z0-9_-]', '-', 'g');
  if old <> 'IB-SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system' then
    raise exception 'N1 FAIL: old expression did not reproduce the doubled id: %', old;
  end if;
  raise notice 'N1 PASS: old expression reproduces the doubled id (non-vacuous)';
end $$;

-- N2: the helper output for the failing input is DISTINCT from the doubled id.
do $$
declare got text;
begin
  got := public.nayanet_canonical_intelligent_id('SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system');
  if got = 'IB-SMART-NOTE-IB-SMART-NOTE-20261123-sn4709-one-mind-one-living-system' then
    raise exception 'N2 FAIL: helper still produces the doubled id';
  end if;
  raise notice 'N2 PASS: helper output differs from the doubled id';
end $$;
