-- SN-0520 GHOST TABLE REPAIR
-- The migration 20260905232300_create_v7_smart_note_event_pipeline is recorded
-- as PRODUCTION_APPLIED in the ledger and in supabase_migrations.schema_migrations,
-- but public.v7_smart_note_transactions does not exist in production.
-- The deployed nayanet-github-dispatch v27 queries this table and fails.
-- This repair migration recreates the table idempotently.
-- Evidence: #1354 comment 6029450747 [TXN-REF], SN-0520.

create table if not exists public.v7_smart_note_transactions (
  id uuid primary key default gen_random_uuid(),
  idempotency_key text not null unique,
  user_id uuid null references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  status text not null default 'completed' check (status in ('processing','completed','failed')),
  failure_stage text null,
  failure_message text null,
  human_note jsonb not null,
  naya_note jsonb not null,
  machine_note jsonb not null,
  intelligent_feed jsonb not null,
  intelligent_block jsonb not null,
  evidence jsonb not null,
  hub_state jsonb not null
);

create index if not exists v7_smart_note_transactions_user_created_idx
  on public.v7_smart_note_transactions(user_id, created_at desc);

create index if not exists v7_smart_note_transactions_created_idx
  on public.v7_smart_note_transactions(created_at desc);

alter table public.v7_smart_note_transactions enable row level security;
