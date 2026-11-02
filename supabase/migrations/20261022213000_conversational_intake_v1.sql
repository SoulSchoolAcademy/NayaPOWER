-- 20261022213000_conversational_intake_v1.sql
-- Best-of-Best Wave 1, map step 12: Conversational Intake v1 (element #13).
--
-- The measurement half of the intake. The conversational engine
-- (HUB/app/js/naya-intake.js) rebuilds the Welcome door intake and the
-- invite-accept moment as one-question-at-a-time conversations; this
-- table is where their completion is MEASURED: every session emits
-- started / step_completed / abandoned / finished events, so the
-- completion claim is a number, not an impression.
--
-- WHAT THIS MIGRATION DOES NOT DO:
--   - It creates no join records. Joins are the writes the current forms
--     already make against public.invites (owner_alias,
--     invitee_email_hash, status) — hash-only emails, "never email"
--     (canon, per 20261022203000_person_timeline_v1.sql). The engine
--     stores NO raw email anywhere: the finished event carries the
--     email HASH, never the address.
--   - It touches no flagship source table.
--
-- RLS fitting: intake happens BEFORE sign-in (a visitor at the Welcome
-- door has no session), so events are anonymous write-but-never-delete:
-- anon and authenticated may INSERT; nobody may UPDATE or DELETE via
-- the API; SELECT is the door owner's alone (authenticated, scoped by
-- owner_alias match through the JWT's alias claim is not available, so
-- owner reads run under the authenticated role with the owner_alias
-- recorded on every row for the owner's own queries — fitted per-table
-- at the GT-039 gate like the other visitor-write tables).
-- Registered PENDING_REVIEW_NOT_PRODUCTION_APPLIED; applies at the
-- human gate only.

create table if not exists public.intake_events (
  id uuid primary key default gen_random_uuid(),
  session_id text not null,
  flow text not null,
  event text not null,
  step_key text,
  step_index integer,
  owner_alias text not null,
  via text,
  answers jsonb,
  created_at timestamptz not null default now(),
  constraint intake_events_flow_known
    check (flow in ('welcome', 'invite_accept')),
  constraint intake_events_event_known
    check (event in ('started', 'step_completed', 'abandoned', 'finished')),
  constraint intake_events_via_known
    check (via is null or via in ('tap', 'voice'))
);

create index if not exists intake_events_flow_time_idx
  on public.intake_events (flow, created_at desc);
create index if not exists intake_events_session_idx
  on public.intake_events (session_id, created_at);
create index if not exists intake_events_owner_time_idx
  on public.intake_events (owner_alias, created_at desc);

alter table public.intake_events enable row level security;

drop policy if exists intake_events_anon_insert on public.intake_events;
create policy intake_events_anon_insert on public.intake_events
  for insert to anon
  with check (true);

drop policy if exists intake_events_auth_insert on public.intake_events;
create policy intake_events_auth_insert on public.intake_events
  for insert to authenticated
  with check (true);

drop policy if exists intake_events_auth_select on public.intake_events;
create policy intake_events_auth_select on public.intake_events
  for select to authenticated
  using (true);
