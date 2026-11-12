-- 20261024194500_smart_mail_participant_completion_and_intake_scope_v1.sql
-- SECURITY CURE COMPLETION — fitted mail policies finished + intake_events
-- narrowed. Built by Resolve's lane for the security lane's review.
--
-- ORDERING DEPENDENCY (hard): this file applies AFTER
-- 20261023190000_smart_mail_legacy_rls_hardening.sql (PR #3018) in the same
-- GT-039 batch. The anon-policy drops and the first messages participant
-- policy are #3018's work and are assumed as the base state; this file
-- completes and corrects that cure, it never edits the landed file.
-- Both files are unapplied to production and unregistered in
-- supabase/PRODUCTION-MIGRATION-LEDGER-V1.json; registration rides the tap.
--
-- CENSUS FINDINGS CURED (whole-system security census, 2026-10-24,
-- SN-1855 instrument; register: security-census-2026-10-24.md):
--
-- [MAIL-1] The landed cure leaves public.smart_mail_threads with RLS
--   enabled and NO policy for any role: authenticated participants cannot
--   read threads through the legacy projection at all.
--   THE OPEN QUESTION, stated plainly: either thread reads are expected
--   to flow exclusively through the v7 path (the Edge Function's
--   v7_mail_* tables, unaltered by both files), or the thread list reads
--   these legacy tables and #3018 as landed would break it. Repo evidence
--   cannot settle which reader production uses. DECISION TAKEN HERE:
--   participant reads. REASON: a participant SELECT policy cannot widen
--   exposure beyond the two parties the messages rule already defines —
--   the thread's addressee and the senders of its messages. If production
--   reads threads only via v7, this policy is inert and correct; if any
--   reader uses the legacy projection, the tap no longer silently breaks
--   it. The v7-only alternative (leaving threads policy-less) risks a
--   silent break at apply time that no repo-side check can detect. The
--   security lane ratifies this choice before the tap.
--
-- [MAIL-2] ALIAS-CLAIM SPOOF IN THE LANDED CURE: its one policy reads the
--   caller's alias as coalesce(app_metadata.smart_alias,
--   user_metadata.smart_alias). In Supabase, user_metadata is USER-
--   WRITABLE: when app_metadata.smart_alias is absent, any signed-in user
--   can set their own user_metadata.smart_alias to a victim's alias and
--   satisfy the from_alias leg for that victim's mail. This file requires
--   the app_metadata claim EXCLUSIVELY in every policy it writes
--   (app_metadata is set only through the service/admin path, never by
--   the user). The binding that mints aliases is public.
--   owner_alias_claims (20261022220000_alias_binding_v1.sql: the estate's
--   ONLY uid<->alias binding, written solely by definer paths).
--
-- [MAIL-3] WRITE POLICIES FOR THE LEGACY TABLES — RESOLVED AS A
--   DOCUMENTED NO-OP, with evidence: the only write path in the repo is
--   public.nayanet_send_smart_mail_authorized (20260919010221), a
--   SECURITY DEFINER RPC granted to authenticated only, which writes the
--   v7_mail_* tables (execute on the inner function is revoked from all
--   client roles); the v7 tables already carry fitted member write
--   policies (20260918224424: v7_msg_member_send, sender_id = auth.uid()
--   + thread membership). NO repo code writes the legacy tables — full
--   enumeration of the mail-named migrations, supabase/functions/, and
--   the sync proxy worker finds them referenced only by the #3018 cure
--   itself. They are projections maintained out-of-band (the same
--   out-of-band hand that created the pass2_anon_* policies), i.e. by a
--   service-role writer, which bypasses RLS by design. Adding
--   authenticated INSERT/UPDATE policies here would CREATE a direct
--   client write path that is not a product path today — widening the
--   surface, not fitting it. Deliberately none are written.
--
-- [INTAKE-1] public.intake_events: 20261022213000 created
--   intake_events_auth_select using (true) — EVERY authenticated user can
--   read ALL citizens' conversational / Welcome-answer events. This file
--   replaces it with an owner-scoped select. SCOPE SOURCE, PROVEN FROM
--   THE DDL: the table keys rows on owner_alias (text, not null) and has
--   no uid column, so the caller side must resolve uid -> alias through
--   the estate's canonical binding, public.owner_alias_claims
--   (alias_normalized = lower(btrim(alias)), owner_id = auth.uid()),
--   whose own owner-select policy composes with the subquery below. The
--   JWT-claim alternative was rejected for this surface: the intake
--   migration's own header records the alias claim as unavailable in the
--   JWT here, and no claim-minting path exists in repo evidence.
--   WRITER IMPACT: the sole in-repo writer, HUB/app/js/naya-intake.js
--   (recordEvent), inserts ANONYMOUSLY with no Prefer header
--   (return=minimal) and never reads the table; no repo code selects
--   from intake_events at all. Nothing's insert path relies on the broad
--   select being narrowed. The anon + authenticated INSERT policies of
--   20261022213000 are untouched (public intake is by design).
--
-- SCHEMA NOTE (stated plainly): the CREATE TABLE for the legacy tables
-- exists in NO migration — they were created out-of-band, like the pass2
-- policies. This file is written against exactly the columns the landed
-- cure's own policy proves exist: smart_mail_messages(from_alias,
-- thread_id) and smart_mail_threads(id, to_alias). The threads
-- sender-leg runs through a SECURITY DEFINER helper because the landed
-- messages policy already references smart_mail_threads inside its USING
-- expression; a threads policy that also queried messages directly
-- would close a policy-reference cycle and Postgres raises
-- infinite-recursion in policy expansion. The reference stays
-- one-directional in policy expressions; the helper reads as owner.
--
-- WHAT REMAINS PRODUCTION-GATED: applying #3018 + this file (Shawn's
-- GT-039 tap), registering both migrations in the production ledger, and
-- the security lane's ratification of the [MAIL-1] participant-read
-- decision before the tap. This file changes nothing in production by
-- existing; it is a file on a branch until the tap.

begin;

-- Idempotent re-assert (the enabling itself is #3018's / 20261022213000's
-- work; repeating it is a no-op and keeps this file safe to review alone).
alter table public.smart_mail_messages enable row level security;
alter table public.smart_mail_threads enable row level security;
alter table public.intake_events enable row level security;

-- [MAIL-1 helper] Sender leg for the threads policy, as owner, so the two
-- tables' policies never reference each other in both directions.
create or replace function public.smart_mail_thread_sender_match(p_thread_id uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.smart_mail_messages m
    where m.thread_id = p_thread_id
      and (auth.jwt() -> 'app_metadata' ->> 'smart_alias') is not null
      and m.from_alias = (auth.jwt() -> 'app_metadata' ->> 'smart_alias')
  );
$$;

revoke all on function public.smart_mail_thread_sender_match(uuid) from public, anon;
grant execute on function public.smart_mail_thread_sender_match(uuid) to authenticated;

-- [MAIL-2] Messages participant SELECT: the landed cure's rule with the
-- alias source fixed to app_metadata ONLY (no user_metadata fallback).
drop policy if exists smart_mail_messages_participant_select on public.smart_mail_messages;
create policy smart_mail_messages_participant_select
on public.smart_mail_messages
for select
to authenticated
using (
  (auth.jwt() -> 'app_metadata' ->> 'smart_alias') is not null
  and (
    from_alias = (auth.jwt() -> 'app_metadata' ->> 'smart_alias')
    or exists (
      select 1
      from public.smart_mail_threads t
      where t.id = smart_mail_messages.thread_id
        and t.to_alias = (auth.jwt() -> 'app_metadata' ->> 'smart_alias')
    )
  )
);

-- [MAIL-1] Threads participant SELECT, mirroring the messages rule: the
-- caller participates when they are the thread's addressee (to_alias) or
-- a sender of a message in it (via the definer helper, schema note above).
drop policy if exists smart_mail_threads_participant_select on public.smart_mail_threads;
create policy smart_mail_threads_participant_select
on public.smart_mail_threads
for select
to authenticated
using (
  (auth.jwt() -> 'app_metadata' ->> 'smart_alias') is not null
  and (
    to_alias = (auth.jwt() -> 'app_metadata' ->> 'smart_alias')
    or public.smart_mail_thread_sender_match(smart_mail_threads.id)
  )
);

-- [INTAKE-1] Owner-scoped SELECT replacing using (true): a row is
-- readable only when its owner_alias is bound to the caller in
-- public.owner_alias_claims (canonical uid<->alias binding).
drop policy if exists intake_events_auth_select on public.intake_events;
create policy intake_events_auth_select
on public.intake_events
for select
to authenticated
using (
  exists (
    select 1
    from public.owner_alias_claims c
    where c.owner_id = (select auth.uid())
      and c.alias_normalized = lower(btrim(intake_events.owner_alias))
  )
);

commit;
