# SECURITY CURE NOTE — fitted mail policies completed + intake_events narrowed

**Date:** 2026-10-24 · **Builder lane:** Resolve (for the security lane's review) · **Status:** FILE ON BRANCH `resolve/security-cure-mail-intake-v1` — nothing applied; applying rides Shawn's GT-039 tap, after the security lane ratifies the one open decision ([MAIL-1] below).

**2026-11-11 technical completion proposal (unmerged and unapplied):** Read-only live Postgres policy/grant inspection found two extra surviving legacy policies: `smart_mail_threads_owner_select` and `smart_mail_messages_owner_delete`. Both still consult user-editable JWT metadata. The prepared follow-up migration now explicitly drops both and revokes direct anonymous table privileges on the legacy messages/threads tables; it leaves authenticated participant access and v7 Mail untouched. The source-level regression test `tests/test_mail_pending_policy_completion.py` checks the observed policy inventory and negative controls. Five source-level tests pass, and the 13-test focused migration suite is green. An additional 13/13 synthetic PGlite PostgreSQL permission probe passes; both deliberate legacy-policy reintroductions fail its inventory guard and expose unauthorized synthetic behavior. **These are not a Supabase branch test, real production-schema verification, independent security review, or production authorization.** The required `intake_events` and `owner_alias_claims` tables are absent from the observed production database, so the earlier migrations `20261022213000` and `20261022220000` remain mandatory dependencies. Security/DB owner must re-review the final state and receive Shawn's approval for any production deployment.

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

- **pglast parse (battery-venv):** the proposed completion migration parses clean — 17 statements (begin/commit, 3× ALTER TABLE enable-RLS, 1× CREATE FUNCTION, helper REVOKE+GRANT, legacy-table privilege REVOKE, 5× DROP POLICY, 3× CREATE POLICY). Controls also parse clean: #3018 landed cure (12), intake v1 (11), alias-binding v1 (22).
- **Spoof-source grep:** `user_metadata` and `coalesce` occur in the new file **only in header comments** (lines 34–37, 129) explaining the defect — zero occurrences in executable SQL.
- **`using (true)` grep across the surface files:** the only executable occurrence is intake v1 line 72 — the original policy this file drops and recreates scoped. Final state (apply #3018 → follow-up; intake v1 → follow-up): **no `using (true)` policy remains on `smart_mail_messages`, `smart_mail_threads`, or `intake_events`.**
- **Final-state policy inventory (drop/create simulation over the apply sequence):** exactly 5 policies survive on the two surfaces — `smart_mail_messages_participant_select` (follow-up), `smart_mail_threads_participant_select` (follow-up), `intake_events_auth_select` (follow-up, owner-scoped), and the two intake INSERT policies from v1 (`with check (true)`, public intake, by design, deliberately untouched).
- **Idempotency:** every CREATE is preceded by `drop policy if exists` / `create or replace function`; re-running the simulation sequence twice yields the identical final inventory.

## What this does NOT do

No production change of any kind; a review-only code proposal is not a production approval, and no SQL migration has been registered as applied in the production database (registration rides the authorized tap with the batch). The wider GT-039 policy set for the other pending tables (census cure 5 — `hub_smart_notes`, `project_intel_items`, Trinity page tables) still requires the gated production schema read (G3) before it can be authored truthfully; it is not in this package.

— Resolve's lane, 2026-10-24. Review owner: security lane (Nitro).


## 2026-11-11 executable synthetic RLS probe — supplementary evidence

**Files:** tests/mail_rls_synthetic_pglite.mjs and tests/fixtures/mail_rls_synthetic.sql. The synthetic schema contains no customer data or production keys and approximates only the columns and privileges necessary to exercise the two pending Smart Mail migrations. Engine: PGlite 0.5.16 (PostgreSQL compiled to WebAssembly, single-user connection with role switching); **not** a real Supabase branch or full schema rebuild. No project dependencies are added.

**Replay:** Install @electric-sql/pglite@0.5.16 into an isolated temporary directory with npm, set NAYA_PGLITE_MODULE to that package's dist/index.js absolute path, and run:
- node tests/mail_rls_synthetic_pglite.mjs candidate — **13/13 PASS, exit 0**.
- node tests/mail_rls_synthetic_pglite.mjs unsafe-thread — **expected exit 2**: omitting the new DROP POLICY smart_mail_threads_owner_select step produces one unauthorized synthetic thread read through user-editable user_metadata.smart_alias; the inventory guard fails.
- node tests/mail_rls_synthetic_pglite.mjs unsafe-delete — **expected exit 2**: omitting the new DROP POLICY smart_mail_messages_owner_delete step permits a synthetic recipient to delete another sender's message using forged user_metadata.smart_alias; the inventory guard fails.

**Trust boundary:** This is a controlled causal test of the **candidate SQL logic under a synthetic fixture**, not evidence of any real data disclosure, not an independent-seated review, not proof that all Supabase policies/functions are correct, and not proof that the four pending production migrations can be applied safely. GT-039 remains **HOLD** until a qualified security/DB owner reproduces full dependency-chain tests with authoritative metadata and synthetic identities in an approved isolated Supabase environment, then obtains exact-head independent verification and the Director's protected production authorization.


## 2026-11-11 full four-migration synthetic dependency-chain proof

**Added proof:** The same optional PGlite harness now has a full-chain mode using tests/fixtures/mail_rls_full_chain.sql. It starts with a synthetic pre-migration schema and runs these four *existing pending* migration files in chronological order:

1. 20261022213000_conversational_intake_v1.sql
2. 20261022220000_alias_binding_v1.sql
3. 20261023190000_smart_mail_legacy_rls_hardening.sql
4. 20261024194500_smart_mail_participant_completion_and_intake_scope_v1.sql

**Candidate result:** node tests/mail_rls_synthetic_pglite.mjs full-chain: **20/20 PASS, exit 0**. Additional scenarios full-chain-unsafe-thread and full-chain-unsafe-delete each exit **2 as required**; their synthetic sabotage control reproduces the respective unauthorized action and the policy inventory fails closed.

**Source-calibrated fixture:** Read-only live Supabase pg_default_acl inspection on November 11 shows public-table default ALL privileges for anon/authenticated/service_role under the postgres and supabase_admin creators. The synthetic PGlite fixture models the relevant anon/authenticated defaults. Without this setting, local INSERT / SELECT tests fail from artificial missing grants, not from production SQL policy behavior. No real production privileges were changed.

**Expanded behavior proven in the synthetic schema:** Alias-binding migration creates canonical owner_alias_claims, backfills a known Alice alias from person_identities, denies direct anonymous claim reads and RPC execution, and permits owner-bound universal search. The intake migration admits an anonymous INSERT with no RETURNING clause (the intended write-only client behavior), but rejects an anonymous INSERT ... RETURNING id and returns no rows for anonymous SELECT. Mail behavior remains as in the 13-check isolated two-script test. All synthetic identities and data are fictitious.

**Limitations / gate remains:** Full-chain *syntax and selected modeled behavior* PASS in a synthetic PostgreSQL fixture does not certify the historical 171 production migrations, the real live database's unmodeled tables/functions/policies, Supabase Auth/Data API, production API keys, revocation of stale JWTs, v7 Edge Function mail regression, independent security sign-off, or production safety. The full deployed migration history/contract and owner authorization must be independently tested in a properly scoped Supabase development environment before any GT-039 production application. No billing or production changes occurred in this proof.


## 2026-11-11 production-shape preflight (fail-closed; historical metadata only)

**New bounded technical artifact:** tools/preflight_gt039_schema.py consumes a metadata-only JSON snapshot of public table and column names, derives the required fields directly from the existing Person Timeline / Universal Search source guards and the existing Smart Links / Naya Notes CREATE TABLE contracts, and reports the first incompatible prerequisite shape without changing any database. It does not duplicate the canonical application schema, grant migrations, or add a new release engine.

**Recorded source fixture:** tests/fixtures/gt039_live_columns_20261111.json contains only table names and column names obtained by read-only Supabase information_schema.columns inspection on November 11; **no owner, customer message, or account data**. It is historical evidence, not a current/fresh pre-deployment check. Its independent replay command is:

python tools/preflight_gt039_schema.py --catalog-json tests/fixtures/gt039_live_columns_20261111.json

**Expected result:** exit 2, verdict BLOCKED_SCHEMA_DRIFT, **13 missing columns across 6 existing production tables** (the expanded CREATE TABLE check also detects smart_links.updated_at, in addition to the earlier 12 source-guard/owner-field mismatches). Invalid/incomplete metadata fails with exit 3 (UNKNOWN_FAIL_CLOSED). A shape-compatible synthetic input exits 0 but explicitly says SHAPE_COMPATIBLE_ONLY, never production approval. Run tests/test_gt039_schema_preflight.py for sabotage and missing-metadata negative controls.

**For an authorized fresh check:** First re-read the exact current production schema using the following read-only query, without touching table rows or private content:

    SELECT table_name,column_name
    FROM information_schema.columns
    WHERE table_schema='public'
      AND table_name IN ('smart_notes','smart_mail_threads','smart_mail_messages',
                         'invites','naya_notes','smart_links')
    ORDER BY table_name,ordinal_position;

Collect the results into the documented JSON shape with kind=information_schema_columns, captured_date_utc set to the *actual* UTC capture date, and tables keyed by table_name with a list of column_name strings. Run the script on that snapshot. Read-only catalog results are still NOT proof of full version history, indexes, policies, privilege reachability, services, or production approval.

**Release decision:** Existing PR #3345 remains DRAFT / HOLD. In the captured live schema, CREATE TABLE IF NOT EXISTS will not add the missing owner_id or text columns on existing tables; source guards deliberately reject other absent fields. Do not waive the guards or infer owner_id values from human-readable aliases. Security/DB plus Smart Links, Notes, Timeline/Search owners must reconcile a real schema-preserving dependency plan and obtain independent isolated runtime proof and Shawn's protected production approval.
