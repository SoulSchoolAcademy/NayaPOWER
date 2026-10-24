-- Ambassador System V1 — schema (Naya Power, 2026-10-24).
-- APPLIED live 2026-10-24 (~04:05Z) via the Supabase door; 9 links issued.
-- The alias IS the affiliate link. Events are the ledger; every dashboard
-- number is a derivation over ambassador_events.

create table if not exists public.ambassador_links (
  alias text primary key,
  link_url text not null,
  issued_at timestamptz not null default now(),
  status text not null default 'active'
);

create table if not exists public.ambassador_events (
  id uuid primary key default gen_random_uuid(),
  alias text not null,                       -- the ambassador credited
  kind text not null check (kind in ('click','signup','sale','refund')),
  visitor_key text,                          -- first-party visitor cookie id
  subject_ref text,                          -- order id / new citizen alias
  amount_cents integer,                      -- sale/refund events
  currency text,
  source text,                               -- stripe | paypal | groovesell
  created_at timestamptz not null default now()
);

-- Issuance: every citizen alias on record (certificate registry + seats).
insert into public.ambassador_links (alias, link_url)
select alias, 'https://nayanet.live/joinus?ref=' || alias
from public.smart_mail_aliases where kind in ('seat','member','person','citizen')
on conflict (alias) do nothing;
insert into public.ambassador_links (alias, link_url)
select distinct alias, 'https://nayanet.live/joinus?ref=' || alias
from public.nayanet_identities
on conflict (alias) do nothing;
