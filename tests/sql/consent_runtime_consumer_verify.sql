-- Ratified #1136 consent/collective-intelligence verification.
-- Fresh scratch DB only. Applies the real pending base migration plus the
-- corrective P4 migration and proves future-contribution gating without
-- retroactive deletion of accepted identity-safe derived wisdom.
\set QUIET on
\pset footer off
create extension if not exists pgcrypto;
create table if not exists public.members (id uuid primary key default gen_random_uuid());
create table if not exists public.nayanet_cognition_events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.members(id) on delete cascade
);
create schema if not exists auth;
create or replace function auth.uid() returns uuid language sql stable
as $$ select nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;
do $$
begin
  if not exists (select 1 from pg_roles where rolname='authenticated') then create role authenticated nologin; end if;
  if not exists (select 1 from pg_roles where rolname='anon') then create role anon nologin; end if;
  if not exists (select 1 from pg_roles where rolname='service_role') then create role service_role nologin; end if;
end $$;

\ir ../../supabase/migrations/20260930022500_harden_collective_wisdom_consent_revocation_v1.sql
\ir ../../supabase/migrations/20260930052000_consent_runtime_consumer_v1.sql

create or replace function verify_assert(p_name text,p_ok boolean)
returns void language plpgsql as $$
begin
  if not coalesce(p_ok,false) then raise exception 'VERIFY FAILED: %',p_name; end if;
  raise notice 'PASS: %',p_name;
end $$;

do $$
declare a uuid; b uuid; e uuid;
begin
  insert into public.members default values returning id into a;
  insert into public.members default values returning id into b;
  insert into public.nayanet_cognition_events(user_id) values(a) returning id into e;
  insert into public.nayanet_smart_connect_participation(member_id,door,consent_state)
    values(a,'github_app','explicit');
  insert into public.nayanet_collective_wisdom(source_event_id,owner_id,wisdom_claim,topic)
    values(e,a,'identity-safe accepted lesson','GENERAL');
  perform set_config('verify.a',a::text,false);
  perform set_config('verify.b',b::text,false);
  perform set_config('verify.e',e::text,false);
end $$;

select verify_assert('P1 active explicit participation => current consent TRUE',
  public.nayanet_consent_is_active(current_setting('verify.a')::uuid)=true);

set role authenticated;
select set_config('request.jwt.claim.sub',current_setting('verify.b'),false);
select verify_assert('P2 accepted ACTIVE derived wisdom visible to non-owner',
  (select count(*) from public.nayanet_collective_wisdom where owner_id=current_setting('verify.a')::uuid)=1);
reset role;

select set_config('request.jwt.claim.sub',current_setting('verify.a'),false);
select public.nayanet_smart_disconnect('github_app');

select verify_assert('N1 disconnect => current participation FALSE',
  public.nayanet_consent_is_active(current_setting('verify.a')::uuid)=false);

select verify_assert('P3 disconnect does not retroactively revoke accepted derived wisdom',
  (select status from public.nayanet_collective_wisdom where owner_id=current_setting('verify.a')::uuid limit 1)='ACTIVE');

set role authenticated;
select set_config('request.jwt.claim.sub',current_setting('verify.b'),false);
select verify_assert('P4 prior accepted identity-safe derived wisdom remains visible after disconnect',
  (select count(*) from public.nayanet_collective_wisdom where owner_id=current_setting('verify.a')::uuid)=1);
reset role;

do $$
begin
  begin
    perform public.nayanet_collective_wisdom_for_event(
      current_setting('verify.e')::uuid,current_setting('verify.a')::uuid,
      'new contribution after disconnect','GENERAL','{}'::jsonb);
    raise exception 'VERIFY FAILED: N2 future contribution accepted after disconnect';
  exception when others then
    if SQLERRM like 'VERIFY FAILED:%' then raise; end if;
    if SQLERRM not like '%SMART_CONNECT_EXPLICIT_CONSENT_REQUIRED%' then raise; end if;
    raise notice 'PASS: N2 future contribution denied after disconnect';
  end;
end $$;

select verify_assert('N3 raw cognition table is not granted to authenticated',
  not has_table_privilege('authenticated','public.nayanet_cognition_events','select'));
select verify_assert('N4 collective wisdom does not imply public publication',
  (select bool_and(public_publication='separate') from public.nayanet_collective_wisdom));
select verify_assert('G1 live-consent function not executable by anon',
  not has_function_privilege('anon','public.nayanet_consent_is_active(uuid)','execute'));
select verify_assert('G2 live-consent function executable by service_role',
  has_function_privilege('service_role','public.nayanet_consent_is_active(uuid)','execute'));

drop function if exists verify_assert(text,boolean);
\echo 'ALL #1136 CONSENT / COLLECTIVE-INTELLIGENCE CONTROLS PASSED'
