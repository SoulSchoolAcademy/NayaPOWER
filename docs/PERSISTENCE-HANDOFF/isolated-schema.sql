-- Isolated-DB setup: canonical smart-ledger foundation, adapted ONLY for the
-- missing Supabase platform pieces. Every ledger semantic (table, constraints,
-- RLS policy expression, writer idempotency, chain hash) is verbatim from
-- supabase/migrations/20260919015207_smart_ledger_foundation_v1.sql.
--
-- Adaptations (documented, test-harness only):
--   1. auth.users: minimal stub table (production: Supabase Auth managed).
--   2. auth.uid(): stub reading per-session setting app.uid (production:
--      Supabase reads the JWT; per-session identity is exactly the semantic).
--   3. extensions schema + pgcrypto for digest()/gen_random_uuid().
--   4. Smart-note trigger functions omitted (need unrelated tables).

CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS extensions;
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA extensions;

CREATE TABLE IF NOT EXISTS auth.users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid()
);

-- auth.uid() stub: per-session identity, mirroring Supabase's JWT-derived uid.
CREATE OR REPLACE FUNCTION auth.uid() RETURNS uuid
LANGUAGE sql STABLE AS $$
  SELECT NULLIF(current_setting('app.uid', true), '')::uuid
$$;

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'authenticated') THEN
    CREATE ROLE authenticated NOLOGIN;
  END IF;
END $$;

-- ===== Verbatim canonical foundation (20260919015207) =====
create table if not exists public.nayanet_smart_ledger (
  ledger_event_id uuid primary key default gen_random_uuid(),
  schema_version text not null default '1.0.0',
  owner_id uuid not null references auth.users(id),
  actor_id uuid null references auth.users(id),
  event_type text not null,
  event_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  source_table text not null,
  source_id text not null,
  parent_ledger_event_id uuid null references public.nayanet_smart_ledger(ledger_event_id),
  previous_chain_hash text null,
  event_hash text not null,
  privacy_classification text not null default 'PRIVATE',
  status text not null default 'RECORDED',
  evidence_refs jsonb not null default '[]'::jsonb,
  verification jsonb not null default '{}'::jsonb,
  value jsonb not null default '{}'::jsonb,
  outcome jsonb not null default '{}'::jsonb,
  learning_refs jsonb not null default '[]'::jsonb,
  metadata jsonb not null default '{}'::jsonb,
  supersedes_ledger_event_id uuid null references public.nayanet_smart_ledger(ledger_event_id),
  qualified_by_ledger_event_id uuid null references public.nayanet_smart_ledger(ledger_event_id),
  constraint nayanet_smart_ledger_source_unique unique(owner_id,source_table,source_id),
  constraint nayanet_smart_ledger_privacy_check check (privacy_classification in ('PRIVATE','SHARED','COLLECTIVE','PUBLIC')),
  constraint nayanet_smart_ledger_status_check check (status in ('RECORDED','VERIFIED','QUALIFIED','SUPERSEDED','BLOCKED','FAILED')),
  constraint nayanet_smart_ledger_evidence_array check (jsonb_typeof(evidence_refs)='array'),
  constraint nayanet_smart_ledger_learning_array check (jsonb_typeof(learning_refs)='array')
);
create index if not exists nayanet_smart_ledger_owner_time_idx on public.nayanet_smart_ledger(owner_id,event_at desc);
create index if not exists nayanet_smart_ledger_source_idx on public.nayanet_smart_ledger(source_table,source_id);
create index if not exists nayanet_smart_ledger_parent_idx on public.nayanet_smart_ledger(parent_ledger_event_id);
alter table public.nayanet_smart_ledger enable row level security;
drop policy if exists nayanet_smart_ledger_select_own on public.nayanet_smart_ledger;
create policy nayanet_smart_ledger_select_own on public.nayanet_smart_ledger for select to authenticated using (owner_id=auth.uid());
revoke insert,update,delete on public.nayanet_smart_ledger from anon,authenticated;

create or replace function public.nayanet_smart_ledger_hash(
 p_owner_id uuid,p_event_type text,p_event_at timestamptz,p_source_table text,p_source_id text,
 p_parent_ledger_event_id uuid,p_previous_chain_hash text,p_evidence_refs jsonb,p_metadata jsonb
) returns text language sql immutable set search_path=public,extensions as $$
 select encode(extensions.digest(
  coalesce(p_owner_id::text,'')||'|'||coalesce(p_event_type,'')||'|'||coalesce(p_event_at::text,'')||'|'||
  coalesce(p_source_table,'')||'|'||coalesce(p_source_id,'')||'|'||coalesce(p_parent_ledger_event_id::text,'')||'|'||
  coalesce(p_previous_chain_hash,'')||'|'||coalesce(p_evidence_refs::text,'')||'|'||coalesce(p_metadata::text,''),'sha256'),'hex');
$$;

create or replace function public.nayanet_record_ledger_event(
 p_owner_id uuid,p_event_type text,p_source_table text,p_source_id text,p_event_at timestamptz default now(),
 p_actor_id uuid default null,p_privacy_classification text default 'PRIVATE',p_status text default 'RECORDED',
 p_evidence_refs jsonb default '[]'::jsonb,p_verification jsonb default '{}'::jsonb,p_value jsonb default '{}'::jsonb,
 p_outcome jsonb default '{}'::jsonb,p_learning_refs jsonb default '[]'::jsonb,p_metadata jsonb default '{}'::jsonb,
 p_parent_ledger_event_id uuid default null
) returns public.nayanet_smart_ledger language plpgsql security definer set search_path=public,extensions as $$
declare v_existing public.nayanet_smart_ledger; v_previous text; v_id uuid:=gen_random_uuid(); v_hash text;
begin
 if p_owner_id is null or nullif(trim(p_event_type),'') is null or nullif(trim(p_source_table),'') is null or nullif(trim(p_source_id),'') is null then
   raise exception 'LEDGER_REQUIRED_FIELDS';
 end if;
 select * into v_existing from public.nayanet_smart_ledger where owner_id=p_owner_id and source_table=p_source_table and source_id=p_source_id limit 1;
 if found then return v_existing; end if;
 if p_parent_ledger_event_id is not null then
   select event_hash into v_previous from public.nayanet_smart_ledger where ledger_event_id=p_parent_ledger_event_id and owner_id=p_owner_id;
   if not found then raise exception 'LEDGER_PARENT_NOT_FOUND'; end if;
 else
   select event_hash into v_previous from public.nayanet_smart_ledger where owner_id=p_owner_id order by event_at desc,created_at desc limit 1;
 end if;
 v_hash:=public.nayanet_smart_ledger_hash(p_owner_id,p_event_type,p_event_at,p_source_table,p_source_id,p_parent_ledger_event_id,v_previous,coalesce(p_evidence_refs,'[]'::jsonb),coalesce(p_metadata,'{}'::jsonb));
 insert into public.nayanet_smart_ledger(ledger_event_id,schema_version,owner_id,actor_id,event_type,event_at,source_table,source_id,parent_ledger_event_id,previous_chain_hash,event_hash,privacy_classification,status,evidence_refs,verification,value,outcome,learning_refs,metadata)
 values(v_id,'1.0.0',p_owner_id,p_actor_id,p_event_type,p_event_at,p_source_table,p_source_id,p_parent_ledger_event_id,v_previous,v_hash,p_privacy_classification,p_status,coalesce(p_evidence_refs,'[]'::jsonb),coalesce(p_verification,'{}'::jsonb),coalesce(p_value,'{}'::jsonb),coalesce(p_outcome,'{}'::jsonb),coalesce(p_learning_refs,'[]'::jsonb),coalesce(p_metadata,'{}'::jsonb))
 returning * into v_existing;
 return v_existing;
exception when unique_violation then
 select * into v_existing from public.nayanet_smart_ledger where owner_id=p_owner_id and source_table=p_source_table and source_id=p_source_id limit 1;
 if found then return v_existing; end if; raise;
end; $$;
revoke execute on function public.nayanet_record_ledger_event(uuid,text,text,text,timestamptz,uuid,text,text,jsonb,jsonb,jsonb,jsonb,jsonb,jsonb,uuid) from public,anon,authenticated;

-- Test-harness grants: the harness connects as the owner roles for SELECT
-- (RLS applies) and as postgres for the writer (security definer, as in prod).
GRANT SELECT ON public.nayanet_smart_ledger TO authenticated;
GRANT USAGE ON SCHEMA public TO authenticated;
