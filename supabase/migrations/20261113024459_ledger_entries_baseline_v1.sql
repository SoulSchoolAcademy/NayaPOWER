-- 20261113024459_ledger_entries_baseline_v1.sql
--
-- Baseline: create public.ledger_entries from live production schema evidence.
--
-- WHY THIS FILE EXISTS. The ledger_entries table exists in production (30 rows,
-- LE-20261022-001..030, chain verified 30/30 at filing of the trigger migration)
-- but no migration creates it: migration 20261113024500 only reads, locks, and
-- inserts into it. The chain-readiness gate's "Enforce no unrecorded migration
-- debt" step fails at tip 2ec4455e on exactly this one unrecorded finding
-- (run 43557983931, job chain-readiness-gate; measured 5 defects, recorded 4;
-- the 5th is UNCREATED_DEPENDENCY public.ledger_entries). This migration is
-- the prescribed cure-forward from BRAIN/12-ENGINEERING/MIGRATION-COHERENCE-
-- BASELINE.json ("how_to_lower_this_ledger"): land a create-table baselining
-- migration authored from live production schema evidence, never from guessed
-- types. No baseline-ledger change is needed: ledger_entries was never recorded
-- there, so once this lands the detector measures 4, all recorded, and the
-- enforcement step passes.
--
-- LIVE SCHEMA EVIDENCE (read-only, Supabase project dahisasgpfvziswqvmvm,
-- "supabase-red-cable", queried 2026-11-14 ~09:44-09:47Z via the Management API
-- database/query endpoint; every column, default, constraint, index, and policy
-- below is copied from that evidence, nothing guessed):
--   seq          bigint       NOT NULL  DEFAULT nextval('ledger_entries_seq_seq')
--   entry_id     text         NOT NULL  UNIQUE
--   issued_at    timestamptz  NOT NULL
--   kind         text         NOT NULL  CHECK kind IN ('execution','decision','census','signal')
--   lane         text         NOT NULL
--   title        text         NOT NULL
--   outcome      text         NOT NULL
--   nutshell     text         NOT NULL
--   proof_kind   text         NOT NULL  CHECK proof_kind IN ('url','md5','sql','file','multi')
--   proof_url    text         NULL
--   proof_detail text         NULL
--   proof_state  text         NOT NULL  DEFAULT 'VERIFIED'
--                              CHECK proof_state IN ('VERIFIED','RECORDED')
--   prev_hash    text         NOT NULL
--   entry_hash   text         NOT NULL
--   scores       jsonb        NOT NULL  DEFAULT '{}'::jsonb
--   raw          jsonb        NOT NULL  DEFAULT '{}'::jsonb
--   created_at   timestamptz  NOT NULL  DEFAULT now()
--   PRIMARY KEY (seq); UNIQUE (entry_id); indexes on issued_at DESC and lane;
--   RLS ENABLED with one policy: ledger_entries_select_anon, FOR SELECT TO anon
--   USING (true). The seq default is the bigserial expansion, reproduced here
--   as bigserial; the identity-sequence name ledger_entries_seq_seq matches live.
--   Live rows: 30, max(seq) = 31 -- seq 1 never existed (see the trigger
--   migration's header: the gap is never backfilled).
--
-- SORT. This file sorts one second before 20261113024500 (the trigger migration
-- that writes to this table), so a rebuild from empty creates the table before
-- the trigger that appends to it. Same precedent as
-- 20261022201458_smart_links_owner_id_repair_v1.sql, which sorts one second
-- before the migration it repairs. The timestamp is a sort key, not an authorship
-- claim: this file was authored 2026-11-14, after the Nov 12 deploy-failure
-- receipt (artifact 13962263565) and the Nov 14 gate failure above.
--
-- IDEMPOTENCY / PRODUCTION SAFETY. Every statement is a no-op where the object
-- already exists: CREATE TABLE IF NOT EXISTS, CREATE INDEX IF NOT EXISTS,
-- ENABLE ROW LEVEL SECURITY (idempotent), and a DO guard around the policy.
-- On production, where the table and all its objects already exist, this
-- migration changes nothing. It is NOT a production DB write in effect; the
-- governed deploy path still applies it through the normal chain.
--
-- WHAT THIS DOES NOT DO. No data backfill: live's 30 rows are history and are
-- never recreated by a migration. A rebuild starts an empty chain; the trigger's
-- GENESIS fallback (prev_hash 'GENESIS-20261022' on an empty table) handles that
-- case by design. A rebuilt sequence starts at 1 while live's effective start
-- is 2 (seq 1 never existed); seq takes no part in the hash canon, so chain
-- validity is unaffected.
--
-- RLS NOTE. The anon SELECT policy below is reproduced VERBATIM from live. It
-- is the known least-privilege exposure (anon SELECT USING (true)); the repair
-- for that class is the separate governed track GT-039 / issue #2823, awaiting
-- Shawn's word on a production DB write. This migration changes no policy and
-- must not be read as endorsing the policy -- it records the table as it is.

create table if not exists public.ledger_entries (
  seq bigserial primary key,
  entry_id text not null unique,
  issued_at timestamptz not null,
  kind text not null check (kind in ('execution', 'decision', 'census', 'signal')),
  lane text not null,
  title text not null,
  outcome text not null,
  nutshell text not null,
  proof_kind text not null check (proof_kind in ('url', 'md5', 'sql', 'file', 'multi')),
  proof_url text,
  proof_detail text,
  proof_state text not null default 'VERIFIED' check (proof_state in ('VERIFIED', 'RECORDED')),
  prev_hash text not null,
  entry_hash text not null,
  scores jsonb not null default '{}'::jsonb,
  raw jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists ledger_entries_issued_at_idx
  on public.ledger_entries (issued_at desc);

create index if not exists ledger_entries_lane_idx
  on public.ledger_entries (lane);

alter table public.ledger_entries enable row level security;

do $$
begin
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public'
      and tablename = 'ledger_entries'
      and policyname = 'ledger_entries_select_anon'
  ) then
    create policy ledger_entries_select_anon on public.ledger_entries
      for select to anon using (true);
  end if;
end
$$;
