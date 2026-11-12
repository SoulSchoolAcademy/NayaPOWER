# Uncreated flagship tables — schema evidence pack (2026-10-22)

**Purpose.** Migration `20261022203000_person_timeline_v1.sql` (PR #2946) first
REFERENCES four tables that no migration creates — `public.invites`,
`public.smart_mail_messages`, `public.smart_mail_threads`, `public.smart_notes` —
so a rebuild from empty breaks at that migration. The four tables exist in
production; they were created outside the governed migration system and the
estate has no paper for them. Post-Merge Guardian disposition on PR #2946
(comment 6352604037; post-merge verification, board #2793 comment 6352640082):
REAL ESCAPE, bookkeeping class, revert NOT recommended, cure-forward = record
the findings deliberately in `MIGRATION-COHERENCE-BASELINE.json` (done — see
`known_defect_records` there) and author create-table **baselining migrations**
as a separate governed step.

**This document is the evidence pack that step builds on. It is NOT DDL and
invents none.** Every column below is usage-grade evidence: a name a committed
file reads, writes, or requires. The repo's own extractor
(`extract-uncreated-table-evidence.py`, run 2026-10-22 against the updated
ledger) reports for all four tables: **no TYPED columns, no NAMED columns from
migration DDL** — no migration alters, inserts into, or indexes any of them.
Column types, keys, defaults, and policies live only in the production
database; the baselining step must read them there (human-gated) and must not
guess them here.

## Reference inventory (whole repo, tip c66faf7d)

| Source | Tables | What it evidences |
|---|---|---|
| `supabase/migrations/20261022203000_person_timeline_v1.sql` | all four | The only migration the coherence detector measures against all four. Its fail-loud guard requires a minimum column set per table; its view reads a wider set; its header records the Step-0 (2026-10-22) live schema check and the source-column contract. |
| `supabase/migrations/20261022201500_smart_links_v1.sql` (header) | all four (named) | Estate note: the flagship tables (`smart_notes`, `smart_mail_*`, `invites`) live in the same production project (named in that header) but were created outside repo migration history. (`'invites'` also appears in this file as a reserved URL slug — not a table reference; the detector correctly ignores it.) |
| `supabase/migrations/20261022204500_naya_notes_v1.sql` (header) | `smart_notes` (named) | Distinguishes `smart_notes` (the flagship wall/intelligence table) from `naya_notes`, `hub_smart_notes`, and `nayanet_notes` — four different objects; the baselining step must not merge them. |
| `tools/person_timeline.py` | all four | The Python builder: exact fields read per source row, participant parsing, quarantine rules. |
| `tests/test_person_timeline.py` | all four | Fixture row shapes per table (the fullest single column inventory in the repo) + the guard-column assertions. |
| `docs/person-timeline-read-model.md` | all four | The event contract: which source fields the derivation consumes; honest-null rules. |
| `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates/personal.html` (lines 2879, 2886) | `smart_notes` | Flagship wall write/read: POST body `{content, owner_alias}`; GET filtered `owner_alias=eq.<alias>`, ordered `created_at.desc`. |
| `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/naya-supabase-proxy.worker.js` | `smart_notes` | `/notes` route proxies to `/rest/v1/smart_notes` with the **anon key** — the flagship reaches this table as anon via PostgREST. |
| `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/templates-registry.json` | all four | Canon checks: flagship inserts into `smart_mail_threads`/`smart_mail_messages` (`communication-backend-insert`); `loadToday` merges wall posts, mail threads, and invites (`today-backend-source`); invites are inserted hash-only (`growth-backend-record`); the backend tables are "keyed by page alias" (`cross-page-backend-client`). |
| `supabase/history/` + all of `supabase/` (swept) | — | **Negative evidence:** no `CREATE TABLE` for any of the four exists anywhere under `supabase/`, including the pre-reconciliation lineage. |

## public.smart_notes — the flagship wall / intelligence table

Columns evidenced (grade: GUARD = required by the timeline migration's
fail-loud check; VIEW = read by its view; CODE = read/written by repo code;
FIXTURE = present in test fixtures):

| Column | Evidence | Type implication |
|---|---|---|
| `owner_alias` | GUARD, VIEW, CODE (insert body + filter in personal.html) | text-like; the page/owner key. No type stated. |
| `content` | GUARD, VIEW, CODE, FIXTURE | text-like (note body). No type stated. |
| `created_at` | GUARD, VIEW, CODE (ordered desc), FIXTURE | timestamp-like; consumed as the timeline's `event_at`. No type stated. |
| `author_name` | GUARD, VIEW, CODE, FIXTURE | text-like; Faces pattern: `author_name` COALESCE `sender_name` keys the wall event to its author. |
| `sender_name` | GUARD, VIEW, CODE, FIXTURE | text-like; fallback author name (see above). |

RLS / policy expectations stated in specs: **none for this table anywhere in
the repo.** Operational fact, not a policy statement: the flagship reads and
writes it with the anon key through the proxy worker, keyed by `owner_alias` —
production must permit that path, but whether RLS is enabled and what the
policies say is production-only knowledge.

Unknown: primary key / whether an `id` column exists (the timeline emits
`source_id = NULL` for wall notes — "when the source carries one" — and no repo
file evidences one); `updated_at` or any further columns; defaults; indexes.

## public.smart_mail_threads

| Column | Evidence | Type implication |
|---|---|---|
| `thread_key` | VIEW (join key), CODE, FIXTURE; header prose contract | text-like; the join key to messages. Uniqueness NOT evidenced. |
| `owner_alias` | GUARD, VIEW | text-like; whose mailbox. |
| `subject` | GUARD, VIEW, CODE, FIXTURE | text-like. |
| `participants` | GUARD, CODE, FIXTURE | **Type genuinely undeterminable from repo:** fixtures carry it both as a JSON array of name strings and as a JSON string of `[{"name": …, "email": …}]`; the builder deliberately tolerates a jsonb array, a JSON text string, or a delimited name string. Participant objects may carry `name`, `sender_name`, `email`, or `email_hash`. Settle from production. |
| `status` | GUARD, FIXTURE | text-like; fixture value `open`. Full value set unknown. |
| `created_at` | GUARD, FIXTURE | timestamp-like. |
| `updated_at` | GUARD, FIXTURE | timestamp-like. |
| `direction` | header prose contract ONLY | **Discrepancy to settle from production:** the migration header lists `direction` among thread columns, but the guard does not require it and the view does not use it (direction is read from messages). It may not exist on threads at all. |

RLS / policy expectations: none stated for this table. By analogy only: the
`naya_notes` header says its RLS "mirrors the flagship messaging pattern: the
owner, as an authenticated user, scoped by `owner_id = auth.uid()`" — note the
tension that everything else in the repo keys threads by `owner_alias`, not
`owner_id`; whether threads carry both is unknown.

Unknown: primary key; `owner_id` presence; FK relationships; defaults; the
full production column set.

## public.smart_mail_messages

| Column | Evidence | Type implication |
|---|---|---|
| `thread_key` | GUARD, VIEW, CODE, FIXTURE | text-like; joins to threads on equality (no FK evidenced anywhere). |
| `sender_name` | VIEW, CODE, FIXTURE | text-like; inbound events key to the sender. |
| `sender` | VIEW, CODE (fallback `sender_name` or `sender`) | text-like. Which of `sender` / `sender_name` is canonical — or whether both exist — is unknown; fixtures carry only `sender_name`. |
| `body` | GUARD, VIEW, CODE, FIXTURE | text-like. |
| `direction` | GUARD, VIEW, CODE, FIXTURE | text-like; values evidenced: `inbound`, `outbound`. |
| `created_at` | GUARD, VIEW, CODE, FIXTURE | timestamp-like; the event timestamp. |

Canon: the flagship delivers messages by inserting into the Smart Mail tables
(registry check `communication-backend-insert` covers threads and messages).

RLS / policy expectations: none stated for this table in the repo (same
flagship-messaging analogy as threads, with the same `owner_id`/`owner_alias`
open question — messages carry no owner column in any repo evidence; ownership
would derive through the thread).

Unknown: primary key / `id` (timeline emits `source_id = NULL` for mail);
any further columns; defaults; indexes.

## public.invites

| Column | Evidence | Type implication |
|---|---|---|
| `invitee_email_hash` | GUARD, VIEW, CODE, FIXTURE, CANON | text-like hash. **Hash-only by design:** canon (`growth-backend-record`) and the migration header both state the invitee's email itself is NEVER stored — "never email". The baselining migration must not add an email column. Fixtures show the value can be NULL in real rows (the builder quarantines hash-less invites). |
| `status` | GUARD, VIEW, CODE, FIXTURE | text-like; values evidenced: `sent`, `joined`. Full value set unknown. |
| `created_at` | GUARD, VIEW, FIXTURE | timestamp-like. |
| `owner_alias` | GUARD, VIEW, FIXTURE | text-like; the inviting page/owner. |

RLS / policy expectations: no policy DDL in the repo. The recorded flow is a
pre-sign-in public one — the registry evidences an invite endpoint called from
pages and an insert of the form `.from('invites').insert({invitee_email_hash…})`
in record-only mode (no email sent) — which implies anon INSERT works in
production today; the exact policy is production-only knowledge.

Unknown: primary key / `id`; expiry or accepted-at columns; `owner_id`
presence; defaults; indexes.

## Cross-cutting unknowns — what only production can answer

1. **Every column type** for all four tables (repo total: 0 types stated).
2. Primary keys, unique constraints, foreign keys, defaults, indexes.
3. Whether RLS is enabled on each table and the exact production policies.
4. The **full** production column sets — the repo evidences only the minimum
   the timeline derivation needs; production may carry more.
5. The Step-0 schema check (2026-10-22) cited by the Phase-0 migration headers
   was a live check whose full output was never committed; only its
   evidenced-minimum column lists survive, in those headers.

## Instructions to the baselining step (separate, governed)

1. At the human gate, read the live production schema for the four tables
   (`information_schema` / `pg_catalog`: columns + types, constraints,
   indexes, RLS state, policies) and preserve that dump as the step's evidence.
2. Author one baselining migration per table (or one combined migration) whose
   `CREATE TABLE IF NOT EXISTS` matches production **exactly** — types, keys,
   defaults, policies — so applying it anywhere production already has the
   tables is a no-op, and a rebuild from empty finally passes the timeline
   migration.
3. Register the migrations in `supabase/PRODUCTION-MIGRATION-LEDGER-V1.json`
   through the governed path; expect the ledger-union discipline at landing.
4. On landing, remove the four entries from
   `MIGRATION-COHERENCE-BASELINE.json` (`known_defects` +
   `known_defect_records`, with a `floor_history` entry) in the same motion —
   the baseline enforcement reports improvements loudly precisely so the
   ledger is updated deliberately, never left stale.

*Evidence grades and sources are stated inline throughout. Anything not
listed as evidenced is unknown. UNKNOWN is not PASS.*
