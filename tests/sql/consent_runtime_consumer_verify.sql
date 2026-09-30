-- =====================================================================
-- P4 consent runtime consumer — verification script.
--
-- Runs the REAL migration files (pending 20260930022500 + PROPOSED
-- 20260930050000) against a FRESH, EMPTY database, then executes
-- positive and negative controls. Any failed assertion raises an
-- exception and aborts. Zero output on success = ALL PASS.
--
-- Usage (from the repo root):
--   createdb consent_verify && psql consent_verify \
--     -v ON_ERROR_STOP=1 -f tests/sql/consent_runtime_consumer_verify.sql
--
-- The script is SELF-CONTAINED: it stubs the two prerequisite FK targets
-- (members, nayanet_cognition_events) and auth.uid() with the same
-- semantics Supabase provides in production. It never touches production.
-- =====================================================================

\set QUIET on
\pset footer off

-- ---------------------------------------------------------------------
-- 0. Prerequisite stubs (exact shapes the pending migration expects)
-- ---------------------------------------------------------------------
create extension if not exists pgcrypto;

create table if not exists public.members (
  id uuid primary key default gen_random_uuid()
);

create table if not exists public.nayanet_cognition_events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.members(id) on delete cascade
);

-- Minimal auth.uid() stub with production semantics:
-- reads the JWT subject claim; NULL when absent.
create schema if not exists auth;
create or replace function auth.uid() returns uuid
language sql stable
as $$ select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;

-- Test roles mirroring the Supabase grant model.
do $$
begin
  if not exists (select 1 from pg_roles where rolname='authenticated') then
    create role authenticated nologin;
  end if;
  if not exists (select 1 from pg_roles where rolname='anon') then
    create role anon nologin;
  end if;
  if not exists (select 1 from pg_roles where rolname='service_role') then
    create role service_role nologin;
  end if;
end $$;

-- ---------------------------------------------------------------------
-- 1. Apply the REAL migrations under test, in deploy order.
-- ---------------------------------------------------------------------
\ir ../../supabase/migrations/20260930022500_harden_collective_wisdom_consent_revocation_v1.sql
\ir ../../supabase/migrations/20260930050000_consent_runtime_consumer_v1.sql

-- ---------------------------------------------------------------------
-- 2. Fixtures: three members, three participation states, one wisdom row.
-- ---------------------------------------------------------------------
do $$
declare
  v_a uuid; v_b uuid; v_c uuid; v_event uuid;
begin
  insert into public.members default values returning id into v_a;  -- ACTIVE+explicit
  insert into public.members default values returning id into v_b;  -- reader, no consent
  insert into public.members default values returning id into v_c;  -- REVOKED
  insert into public.nayanet_cognition_events(user_id) values (v_a) returning id into v_event;

  -- A's live explicit participation (trigger requires consent_state='explicit').
  insert into public.nayanet_smart_connect_participation(member_id, door, consent_state)
  values (v_a, 'github_app', 'explicit');

  -- C's revoked participation (insert active+explicit, then revoke like the
  -- disconnect flow does: trigger coerces consent_state to 'revoked').
  insert into public.nayanet_smart_connect_participation(member_id, door, consent_state)
  values (v_c, 'github_app', 'explicit');
  update public.nayanet_smart_connect_participation
    set status='revoked', revoked_at=now() where member_id=v_c;

  -- One collective_wisdom row owned by A, status ACTIVE.
  insert into public.nayanet_collective_wisdom(source_event_id, owner_id, wisdom_claim, topic)
  values (v_event, v_a, 'revenue follows trust', 'GENERAL');

  perform set_config('verify.member_a', v_a::text, false);
  perform set_config('verify.member_b', v_b::text, false);
  perform set_config('verify.member_c', v_c::text, false);
end $$;

-- helper: raise on failed assertion
create or replace function verify_assert(p_name text, p_ok boolean)
returns void language plpgsql as $$
begin
  if not coalesce(p_ok, false) then
    raise exception 'VERIFY FAILED: %', p_name;
  end if;
  raise notice 'PASS: %', p_name;
end $$;

-- ---------------------------------------------------------------------
-- 3. POSITIVE controls — the consumer function
-- ---------------------------------------------------------------------
select verify_assert('P1 active+explicit participation => TRUE',
  public.nayanet_consent_is_active(current_setting('verify.member_a')::uuid) = true);

-- ---------------------------------------------------------------------
-- 4. NEGATIVE controls — the consumer function
-- ---------------------------------------------------------------------
select verify_assert('N1 revoked participation => FALSE',
  public.nayanet_consent_is_active(current_setting('verify.member_c')::uuid) = false);

select verify_assert('N2 no participation row => FALSE',
  public.nayanet_consent_is_active(current_setting('verify.member_b')::uuid) = false);

select verify_assert('N3 NULL owner => FALSE (not NULL, not error)',
  public.nayanet_consent_is_active(null) = false);

do $$
declare v_r boolean;
begin
  -- pending consent_state cannot be inserted via the trigger guard; emulate
  -- by direct insert then verify the trigger refuses:
  begin
    insert into public.nayanet_smart_connect_participation(member_id, door, consent_state)
    values (current_setting('verify.member_b')::uuid, 'mcp', 'pending');
    raise exception 'VERIFY FAILED: N4 trigger allowed active row without explicit consent';
  exception
    when raise_exception then
      if SQLERRM not like '%SMART_CONNECT_CONSENT_REQUIRED%' then raise; end if;
      raise notice 'PASS: N4 active row without explicit consent refused at write time';
  end;
end $$;

-- N5: fail-closed on internal error — hide the table inside a rolled-back
-- transaction; the function must return FALSE, never raise, never bypass.
do $$
declare v_r boolean;
begin
  begin
    alter table public.nayanet_smart_connect_participation rename to _tmp_hidden;
    v_r := public.nayanet_consent_is_active(current_setting('verify.member_a')::uuid);
    if v_r is not false then
      raise exception 'VERIFY FAILED: N5 fail-closed violated (returned %)', v_r;
    end if;
    raise notice 'PASS: N5 query error => FALSE (fail closed)';
  exception
    when others then
      -- restore the table, then re-raise only if the failure was ours
      alter table if exists public._tmp_hidden rename to nayanet_smart_connect_participation;
      if SQLERRM like 'VERIFY FAILED%' then raise; end if;
      raise exception 'VERIFY FAILED: N5 function raised instead of returning FALSE: %', SQLERRM;
  end;
  -- normal path: restore (no-op if already restored)
  begin
    alter table if exists public._tmp_hidden rename to nayanet_smart_connect_participation;
  exception when others then null;
  end;
end $$;

-- ---------------------------------------------------------------------
-- 5. RLS read-path controls (collective_wisdom, R2)
--    Run as `authenticated` with the JWT claim set, exactly like PostgREST.
-- ---------------------------------------------------------------------
set role authenticated;

-- P2: non-owner B reads A's ACTIVE row while A holds live consent => visible.
select set_config('request.jwt.claim.sub', current_setting('verify.member_b'), false);
select verify_assert('P2 live consent: non-owner reads ACTIVE row',
  (select count(*) from public.nayanet_collective_wisdom
    where owner_id = current_setting('verify.member_a')::uuid) = 1);

reset role;

-- Revoke A's participation (the disconnect flow).
update public.nayanet_smart_connect_participation
  set status='revoked', consent_state='revoked', revoked_at=now()
  where member_id = current_setting('verify.member_a')::uuid;

set role authenticated;

-- N6: same row, same non-owner B, consent now revoked => row hidden.
-- This is the gap the P4 consumer closes: the row is still status='ACTIVE'
-- (revocation of the last participation flips it only via the disconnect
-- function; a direct/active-but-revoked-consent state must deny at READ time).
select set_config('request.jwt.claim.sub', current_setting('verify.member_b'), false);
select verify_assert('N6 revoked consent: non-owner cannot read ACTIVE-status row',
  (select count(*) from public.nayanet_collective_wisdom
    where owner_id = current_setting('verify.member_a')::uuid) = 0);

-- P3: the owner still reads their own row after revocation (no self-lockout).
select set_config('request.jwt.claim.sub', current_setting('verify.member_a'), false);
select verify_assert('P3 owner reads own row regardless of consent state',
  (select count(*) from public.nayanet_collective_wisdom
    where owner_id = current_setting('verify.member_a')::uuid) = 1);

reset role;

-- ---------------------------------------------------------------------
-- 6. Grant sanity: least privilege held
-- ---------------------------------------------------------------------
select verify_assert('G1 function not executable by public/anon',
  not has_function_privilege('anon', 'public.nayanet_consent_is_active(uuid)', 'execute'));
select verify_assert('G2 function executable by authenticated',
  has_function_privilege('authenticated', 'public.nayanet_consent_is_active(uuid)', 'execute'));

-- ---------------------------------------------------------------------
-- 7. Cleanup of test scaffolding (fixtures stay; script is for scratch DBs)
-- ---------------------------------------------------------------------
drop function if exists verify_assert(text, boolean);

\echo 'ALL P4 CONSENT-CONSUMER CONTROLS PASSED'
