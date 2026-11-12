# SECURITY CURE NOTE — fitted mail policies completed + intake_events narrowed

**Date:** 2026-10-24 · **Builder lane:** Resolve (for the security lane's review) · **Status:** FILE ON BRANCH `resolve/security-cure-mail-intake-v1` — nothing applied; applying rides Shawn's GT-039 tap, after the security lane ratifies the one open decision ([MAIL-1] below).

**The migration:** `20261024194500_smart_mail_participant_completion_and_intake_scope_v1.sql` (this directory). It is a follow-up to `20261023190000_smart_mail_legacy_rls_hardening.sql` (PR #3018), which it never edits. **Hard ordering dependency: #3018 applies first in the same GT-039 batch** — its anon-policy drops and first messages policy are the assumed base state.

**Source standard:** whole-system security census 2026-10-24 (SN-1855 instrument), Surface 1 (Smart Mail) + the `intake_events` read-all finding.

## Finding → cure → what remains gated

| # | Census finding | Exact cure in this file | Remains production-gated |
|---|---|---|---|
| MAIL-1 | `smart_mail_threads` left with RLS on and **no policy for any role** — participants can't read threads via the legacy projection | New `smart_mail_threads_participant_select`: authenticated, app_metadata alias = thread's `to_alias`, OR caller sent a message in the thread (sender leg via definer helper, below) | Security lane ratifies participant-read vs v7-only-read **before the tap** (open question, §Decisions); the GT-039 apply itself |
| MAIL-2 | Landed cure's alias source `coalesce(app_metadata, user_metadata)` — **`user_metadata` is user-writable in Supabase → alias spoof** | Messages participant policy dropped + recreated **identical in shape, app_metadata-only**; every policy and the helper in this file read `(auth.jwt() -> 'app_metadata' ->> 'smart_alias')` exclusively, with an explicit not-null guard | GT-039 apply |
| MAIL-3 | No fitted participant write policies for the legacy tables | **Resolved as a documented no-op (evidence in the migration header):** the only repo write path is the SECURITY DEFINER RPC `nayanet_send_smart_mail_authorized` → `v7_mail_*` tables, which already carry fitted member write policies (`v7_msg_member_send`, 20260918224424). No repo code writes the legacy tables; they are service-role projections. Adding authenticated INSERT/UPDATE policies would create a new direct client write path — widening, not fitting | Nothing to apply; the no-op is the cure. Any future legacy-table write path must arrive with its own fitted policies |
| INTAKE-1 | `intake_events_auth_select using (true)` (20261022213000) — **every authenticated user reads all citizens' conversational/Welcome-answer events** | Policy dropped + recreated owner-scoped: row readable only when `lower(btrim(owner_alias))` is bound to `auth.uid()` in `public.owner_alias_claims` (20261022220000 — the estate's canonical uid↔alias binding). Anon + auth INSERT policies untouched (public intake by design) | GT-039 apply (20261022213000 is itself in the pending set; this file applies after it) |

## Decisions taken (security lane: ratify or send back)

1. **[MAIL-1] Participant reads on threads, not v7-only.** Rationale: the policy cannot widen exposure beyond the two parties the messages rule already defines (addressee + senders). If production truly reads threads only via the v7 path, the policy is inert; if any reader uses the legacy projection, the tap no longer silently breaks it. The reverse choice risks an apply-time break no repo-side check can detect.
2. **[INTAKE-1] Scope via `owner_alias_claims`, not the JWT alias claim.** Proven from the DDL: `intake_events` keys rows on `owner_alias` (text, not null) and has **no uid column**. The claims table is the canonical binding (written only by definer paths, first-claim-wins); the intake migration's own header records the JWT alias claim as unavailable for this surface, and no claim-minting path exists in repo evidence. Writer impact is nil: the sole in-repo writer (`HUB/app/js/naya-intake.js`, `recordEvent`) inserts anonymously with `return=minimal` and never reads; no repo code selects from `intake_events`.
3. **Recursion-safe construction.** The landed messages policy already references `smart_mail_threads` inside its USING expression. A threads policy querying `smart_mail_messages` directly would close a policy-reference cycle (Postgres: infinite recursion in policy expansion). The threads sender leg therefore runs through `public.smart_mail_thread_sender_match(uuid)` — SECURITY DEFINER, `search_path=''`, execute revoked from public/anon and granted to authenticated only, following the estate's helper idiom.

## Schema surprises (stated plainly)

- **The legacy tables' CREATE TABLE exists in no migration.** `smart_mail_messages` / `smart_mail_threads` were created out-of-band, exactly like the `pass2_anon_*` policies — production's true shape cannot be read from the repo. The follow-up is written against exactly the columns the landed cure's own policy proves: `smart_mail_messages(from_alias, thread_id)`, `smart_mail_threads(id, to_alias)`. No other column is referenced anywhere. If the G3 production schema read (census) later shows a `from_alias` on threads, adding it to the threads policy is a one-line strengthening — not required for correctness of what's here.
- **Production thread/message reads may not touch these tables at all** (v7 path) — see decision 1; the cure is safe under both shapes.
- The intake table's own migration header half-anticipated this fix ("fitted per-table at the GT-039 gate") while shipping `using (true)` in the meantime; this file is that fitting.

## Static verification (this branch, before publish)

- **pglast parse (battery-venv):** the new migration parses clean — 14 statements (begin/commit, 3× ALTER TABLE enable-RLS, 1× CREATE FUNCTION, revoke+grant, 3× DROP POLICY, 3× CREATE POLICY). Controls also parse clean: #3018 landed cure (12), intake v1 (11), alias-binding v1 (22).
- **Spoof-source grep:** `user_metadata` and `coalesce` occur in the new file **only in header comments** (lines 34–37, 129) explaining the defect — zero occurrences in executable SQL.
- **`using (true)` grep across the surface files:** the only executable occurrence is intake v1 line 72 — the original policy this file drops and recreates scoped. Final state (apply #3018 → follow-up; intake v1 → follow-up): **no `using (true)` policy remains on `smart_mail_messages`, `smart_mail_threads`, or `intake_events`.**
- **Final-state policy inventory (drop/create simulation over the apply sequence):** exactly 5 policies survive on the two surfaces — `smart_mail_messages_participant_select` (follow-up), `smart_mail_threads_participant_select` (follow-up), `intake_events_auth_select` (follow-up, owner-scoped), and the two intake INSERT policies from v1 (`with check (true)`, public intake, by design, deliberately untouched).
- **Idempotency:** every CREATE is preceded by `drop policy if exists` / `create or replace function`; re-running the simulation sequence twice yields the identical final inventory.

## What this does NOT do

No production change of any kind; no PR opened; nothing registered in the production migration ledger (registration rides the tap with the batch). The wider GT-039 policy set for the other pending tables (census cure 5 — `hub_smart_notes`, `project_intel_items`, Trinity page tables) still requires the gated production schema read (G3) before it can be authored truthfully; it is not in this package.

— Resolve's lane, 2026-10-24. Review owner: security lane (Nitro).
