-- Citizen API v1 migration — v3 (Resolve's return patch on Power's v1,
-- 2026-10-25): adds the `family` column the v2 handler's revocation
-- cascade depends on (Power's adapter notes named this duty; the
-- migration file itself had not caught up). Everything else is
-- Power's original file, unchanged.
-- STAGING FILE ONLY. DO NOT APPLY TO PRODUCTION until: deploy hold
-- clears on Shawn's word, Nitro rendered review passes, and this
-- file is reviewed against the live schema.
-- Tables are service-role only. Enable RLS with NO public/anon policies.
-- The Edge Function uses the service-role key server-side; anon keys must
-- NEVER read or write these tables. This is the opposite of the Smart Mail
-- anon RLS break — do not repeat it.

create table if not exists citizen_notes (
  id uuid primary key default gen_random_uuid(),
  alias text not null,
  kind text not null check (kind in ('quick', 'smart')),
  title text,
  nutshell text,
  body text not null,
  key_id text not null,
  created_at timestamptz not null default now()
);

create table if not exists citizen_api_keys (
  id text primary key,
  alias text not null,
  label text not null,
  hash text not null unique,
  last4 text not null,
  revoked boolean not null default false,
  last_used timestamptz,
  requests_today integer not null default 0,
  day text not null default '',
  created_at timestamptz not null default now()
);

create table if not exists citizen_oauth_tokens (
  id text primary key,
  alias text not null,
  kind text not null check (kind in ('access', 'refresh')),
  hash text not null unique,
  family text not null,
  gen integer not null default 1,
  revoke_reason text,
  replays integer not null default 0,
  expires_at timestamptz not null,
  revoked boolean not null default false,
  last_used timestamptz,
  requests_today integer not null default 0,
  day text not null default '',
  created_at timestamptz not null default now()
);

alter table citizen_notes enable row level security;
alter table citizen_api_keys enable row level security;
alter table citizen_oauth_tokens enable row level security;
-- Intentionally NO policies for anon/authenticated. Service-role only.
-- If a future policy is added, it must be reviewed by Nitro + Shawn first,
-- with a two-owner proof, before it lands.

create index if not exists citizen_notes_alias_idx on citizen_notes (alias, created_at desc);
create index if not exists citizen_api_keys_alias_idx on citizen_api_keys (alias);
create index if not exists citizen_oauth_tokens_alias_idx on citizen_oauth_tokens (alias);
create index if not exists citizen_oauth_tokens_family_idx on citizen_oauth_tokens (family);

-- Nitro completion 2026-10-25 (packet gap closed before PR):
-- the v4 handler's E7 idempotency needs a persistent table; the v3
-- migration did not include it. Alias-scoped, matching the handler's
-- in-memory key (alias + Idempotency-Key). Same service-role-only
-- rule as the other tables: NO anon/authenticated policies.
create table if not exists citizen_idempotency_keys (
  alias text not null,
  idem_key text not null,
  body_sig text not null,
  note jsonb not null,
  created_at timestamptz not null default now(),
  primary key (alias, idem_key)
);
alter table citizen_idempotency_keys enable row level security;
-- Intentionally NO policies for anon/authenticated. Service-role only.
create index if not exists citizen_idempotency_keys_alias_idx on citizen_idempotency_keys (alias, created_at desc);
