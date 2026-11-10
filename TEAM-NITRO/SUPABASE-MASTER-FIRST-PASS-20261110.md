# Supabase Master — First Pass (2026-11-10)

## Title: The Supabase Master — First Pass
## Subtitle: His four questions answered from the live state, the six doors re-verified shut, and every remaining fix prepared for his hand
## Nutshell: The audit scored Supabase 6 out of 10. This pass answers the
four questions Shawn asked looking at the table, re-checks the six locked
tables live, and prepares every remaining fix as a file he can run with one
paste. Nothing was deployed, nothing was changed in the database, no key
was read. What is fixed is fixed; what is prepared names its file; what is
still open names its reason.

**Project:** `dahisasgpfvziswqvmvm` (supabase-red-cable, production) ·
**Baseline:** `TEAM-NITRO/SUPABASE-AUDIT-20261110.md` (6/10, filed 2026-11-10 ~02:10Z) ·
**This pass:** 2026-11-10 ~02:56–03:30Z · **Method:** anon-key REST reads
(`sb-api`) + the audit doc + repo migrations/code (read-only). No writes,
no DDL, no service-key runs, no deploys. No keys, tokens, or passwords
appear anywhere in this report. The `seat_keys` hashes were never read.

---

## Part 1 — His Four Questions, Answered in Plain Words

### Title: The Four Questions
### Subtitle: Two empty tables, one big table with an honest unknown, and a message count that is not a member count
### Nutshell: Media notes is the voice-and-video note store with nothing in
it yet. Email tokens is the connected-email store with nothing in it yet —
and the public key cannot even see it. The 7,502 members are one row per
sign-up account, but whether they are real people, an import, or test rows
cannot be settled from the live state — this report says exactly what is
known, what points which way, and whose hand settles it. And the 1,244 is
messages, not members: 1,248 messages now, every single one sent by the
team's own three seats.

### Q1 — What is `media_notes`? (0 rows)
**Plain words:** it is the shelf where voice and video notes go. A citizen
records a spoken note in place, the recording is stored, a watcher writes
down what was said (transcript) and sums it up (summary), and the note can
be filed to a person. That is what the columns say, and the walkthrough's
own code says the same: `media_url, transcript, summary, duration_s,
kind, status, owner_alias, list_name, category, storage_path` — a recorded
note with its words written down and its owner named. The walkthrough
worker (`HUB/walk/worker.js`, NayaMedia) builds the recorder and the
`media-notes` storage bucket. **Why 0 rows:** nobody has recorded one yet.
The feature is wired; it has never been used. It is waiting to fill, not
dead. **Evidence:** schema from the live OpenAPI spec + the walkthrough
code; anon read returns `[]`, matching the audit's count of 0.

### Q2 — What is `member_email_tokens`? (0 rows)
**Plain words:** it is the drawer where a citizen's connected-email login
is kept. Columns: `alias, email, provider, refresh_token_enc, scopes` —
who it belongs to, which email, which provider (such as Gmail), the login
token kept encrypted, and what it is allowed to do. It is the store that
lets NayaNET send and read mail as the citizen, with their permission.
**Why 0 rows:** no citizen has connected an email account yet. **And one
more thing the live state proves:** the public key cannot even see this
table — an anonymous read returns 42501 "permission denied", with the
hint to grant SELECT. Unlike most tables, the public key holds no grant
here at all. The drawer is shut to strangers before it holds anything.
**Evidence:** schema from the live OpenAPI spec; anon read 42501, live
this pass; audit count 0.

### Q3 — What are the 7,502 `members` rows? (honest answer: not settled)
**Plain words first:** `members` is the list of everyone who ever signed
up. One row per sign-up account — the row's id IS the login account's id,
and a database trigger makes the row automatically the moment someone
signs up (`handle_new_user`, migration
`20260827011050_maxis_phase_1_member_and_results.sql`). Each row holds
almost nothing: an id, a display name, and two dates. There is no email,
no password, no profile in this table.
**What the live state proves:** the shape (id + display_name +
created_at + updated_at, from the live spec), the mechanism (the trigger
in the repo migration, and the Sep 27 reset migration that kept
`members` explicitly as "the existing identity bridge used by auth"),
and the count (7,502, from the audit's SQL count — the public key cannot
recount it, see below).
**What the live state does NOT prove — and this pass does not guess:**
whether the 7,502 are real people, imported from an older system, or
test rows. The public key cannot read a single member row: the table's
rules let a logged-in member see only their own row, and the public key
sees an empty list. No display name, no date, nothing to judge by. The
repo holds no seed or import script for members (searched; none found),
and no memory record states where the 7,502 came from.
**What points which way:**
- *For "real sign-ups":* the trigger has existed since Aug 27, so every
  real sign-up since then made a row automatically.
- *Against "active citizens":* almost nothing in the live database
  points at these rows. Only 1 project member and 2 space members link
  to them; member sessions, one-time codes, and email tokens are all 0;
  and the tables that would have held what members DID (assessment
  results, profiles, notes, spaces, consents) do not exist live — the
  Sep 27 reset dropped every table except `members`. The citizen-facing
  identity system the walkthrough actually uses is a different table,
  `nayanet_identities`, with 10 rows.
- *For "import or test":* nothing in the record proves it either. An
  import would have had to come through the trigger or a direct write,
  and neither is in the record.
**Whose hand settles it:** Shawn's, with a service-key read (or the Auth
dashboard count): read a sample of display names and created dates, and
compare the count with the Auth users count. If the dates cluster on one
day, it was a bulk load; if they spread across weeks, they were sign-ups;
if the names look made-up, they were tests. Until that read happens, the
honest answer is "one row per sign-up account, provenance unknown".
**Not claimed:** this pass does not call them real people, does not call
them test rows, and does not call them an import.

### Q4 — Confirm the 1,244 is messages, not members
**Confirmed, live, and stronger than asked.** `smart_mail_messages`
holds **1,248 messages** now (1,244 at the audit, +4 since — the mail is
flowing) across **1,114 threads** (1,110 at the audit, +4). The messages
are 10 days deep: oldest 2026-10-31, newest 2026-11-10 02:39Z.
**Every single message is the team's own mail.** Counted live, all 1,248,
by sender: nitro 518, resolve 554, naya-power 176. Those are the three
team seats. Nobody else has sent a message. The threads agree (nitro 484,
resolve 553, naya-power 77), and the recipients are the same family:
nitro 566, resolve 234, naya-power 215, team-naya 50, plus a handful to
individual seats. So the 1,244 was never a member count — it is the team
talking to each other, and it still is. **Evidence:** full live census
of both tables via anon REST this pass (paged, 1,248 + 1,114 rows read).

---

## Part 2 — The Before Picture, Corrected

### Title: The Off Marks Were the Before Picture
### Subtitle: The lock he ran turned RLS on and revoked the grants — re-verified live, all six
### Nutshell: The audit's screenshot showed RLS Off on the six open tables.
That screenshot was taken before Shawn ran the lock at 02:40Z. The lock
turned RLS on and took the public key's permissions away on all six. This
pass re-checked every one of them from the live state: all six answer
42501, permission denied, on an anonymous read. The door is shut.

| Table | Rows at audit | Anonymous read now |
|---|---|---|
| seat_keys | 2 | 42501 permission denied |
| ambassador_links | 7 | 42501 permission denied |
| naya_category_prototypes | 12 | 42501 permission denied |
| naya_note_filing | 19 | 42501 permission denied |
| ambassador_events | 0 | 42501 permission denied |
| seat_lane_mapping | 0 | 42501 permission denied |

No key values were read, printed, or stored — the check is the denial
itself. The audit's own spot-check (anon read of `seat_keys` returning
both rows) now returns nothing. The archive and distillation-queue locks
from Oct 22 were not re-opened by anything in this pass: neither table
was touched, and the lock file changed only the six named tables.

**Score effect:** the audit was 6/10 with −2 for the six tables. That −2
is closed by his hand and verified here. The remaining −2 is the retrieve
deploy (−1), the pages table (−0.5), and reports/delete (−0.5) — all
prepared below, all still awaiting his hand.

---

## Part 3 — What Is Prepared for His Hand

### Title: Prepared, Not Run
### Subtitle: Four SQL files and one deploy runbook — each paste-and-run, each with its verify steps
### Nutshell: Everything below is ready to fire and nothing has been fired.
Each file follows the lock file's shape (plain-words header, paste-and-run,
verify steps included) and lives on branch
`supabase/master-first-pass-20261110`, read-back verified byte-identical.

### 3.1 The missing pages table — DDL ready
**File:** `TEAM-NITRO/SUPABASE-NAYANET-PAGES-DDL-20261110.sql`
([link](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/supabase/master-first-pass-20261110/TEAM-NITRO/SUPABASE-NAYANET-PAGES-DDL-20261110.sql)) ·
blob `7eeae18e40ce690af45b22552a866c2251fc1386`
**What it does:** creates `public.nayanet_pages` — one row per citizen
page: owner alias (linked to `nayanet_identities.alias`, which is the
link because identities have no numeric id), kind (personal / business /
space / membership only), title, slug (unique per owner), body (JSONB —
the page's own blocks and settings; the template stays shared),
published flag, created/updated dates. RLS ON, public key gets SELECT
only — anyone may read a page, nobody may write one via the key; writes
go through the service role.
**Honest note:** no code anywhere in the repo writes a pages table yet
(zero references to `nayanet_pages`), so this shape is the master's
proposal from what the walkthrough needs, not a copy of an existing
writer. If the walkthrough team needs another column, add it in a second
small change; do not rebuild the table.
**Verify after running:** `rowsecurity = true`; anon holds SELECT only;
an anonymous read returns `[]` instead of PGRST205.

### 3.2 The notes DELETE grant — SQL ready, with a warning
**File:** `TEAM-NITRO/SUPABASE-HUB-SMART-NOTES-DELETE-GRANT-20261110.sql`
([link](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/supabase/master-first-pass-20261110/TEAM-NITRO/SUPABASE-HUB-SMART-NOTES-DELETE-GRANT-20261110.sql)) ·
blob `519b331c831c9c5cfb8c3e7621e711da0aae0845`
**What it does:** `GRANT DELETE ON public.hub_smart_notes TO anon` plus
a DELETE policy, so the sync's tombstone pass can actually remove rows
when a note file is deleted on GitHub.
**The warning, in plain words:** this hands DELETE on the live notes
table to anyone holding the public key. A stranger with the key could
delete any note row, not just tombstoned ones. The notes table already
lets the public key insert and rewrite any row, so this widens a door
that is already open — but it must be a conscious choice.
**The safer alternative (recommended):** run the dedupe under the
service key, which bypasses the row rules entirely — no grant needed.
The grant is only needed if the anon-key sync script itself must delete
tombstoned rows going forward.

### 3.3 The reports seed — preferred path needs no new SQL
**File:** `TEAM-NITRO/SUPABASE-REPORTS-INSERT-20261110.sql`
([link](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/supabase/master-first-pass-20261110/TEAM-NITRO/SUPABASE-REPORTS-INSERT-20261110.sql)) ·
blob `a8d8612c9fa8a0ff44cf0bd3c592defe02d03edc`
**Preferred fix (A) — service-key run, no new SQL:** the 17 missing
reports (Oct 24 – Nov 9) are already written and verified as
`~/workspace/reports-backfill-20261109/rows-seed.sql` (one INSERT, 17
rows, ON CONFLICT re-runnable; all 17 body hashes match the filed
editions; package commit `dcc885cc`). Run that file with the service
key. After it runs: 44 rows, newest 2026-11-09.
**Alternative fix (B) — the SQL in this file:** an INSERT policy for the
public key. Same warning as 3.2: it lets anyone with the public key
insert report rows, including fake ones. Run B only if that trade is
accepted. If A is the choice, leave this file unrun.
**Still open after either fix:** Nov 10 has no report yet, and no
backfill covers it — Nov 10 needs its own Daily Intelligence Report,
filed daily. And the deeper truth stands: this table is batch-fed, not
daily-fed (the Oct 9–22 rows all landed in one batch on Oct 22). The
seed closes the gap; only the daily habit keeps it closed.

### 3.4 The retrieval engine — deploy runbook ready, NOT deployed
**File:** `TEAM-NITRO/SUPABASE-RETRIEVE-DEPLOY-20261110.md`
([link](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/supabase/master-first-pass-20261110/TEAM-NITRO/SUPABASE-RETRIEVE-DEPLOY-20261110.md)) ·
blob `3f0468c7c5bf315d80cc299e3e88e7ad82859dd5`
**What it is:** `nayanet-intelligence-retrieve` — free-text question in,
ranked Intelligent Blocks out. The code is complete in the repo
(`supabase/functions/nayanet-intelligence-retrieve/`, last touched
2026-10-20) with tests. A live call today returns `NOT_FOUND`.
**Three prerequisites before the tap:** (1) the
`SUPABASE_SERVICE_ROLE_KEY` secret must be set on the project — the
function throws `SERVER_AUTH_CONFIG_MISSING` without it, and only Shawn
holds the service key; (2) a config entry is needed —
`[functions.nayanet-intelligence-retrieve] verify_jwt = false` in
`supabase/config.toml`, because the function checks identity inside its
own code (GitHub OIDC, like the governed runtimes); (3) widget-39a1bf91
is still pending — the brief names it, and no record found in this pass
says what it is or whether it gates this deploy, so it is named here so
it is not lost.
**The one tap:** `supabase functions deploy nayanet-intelligence-retrieve
--project-ref dahisasgpfvziswqvmvm`. Note: the governed deploy workflow
deploys a FIXED list of runtimes that does NOT include retrieval, so the
workflow path cannot fire this — the CLI command is the tap.
**Proof after:** the function list must show 22 ACTIVE; a probe without
credentials must stop returning `NOT_FOUND` and return an auth error
instead (`RUNTIME_IDENTITY_REQUIRED` — an auth error IS the proof, a 200
without credentials would be a defect); then the cold-successor proof
workflow confirms a real query returns ranked blocks.

### 3.5 The dedupe — 3 rows proven stale, the rest listed for review
**File:** `TEAM-NITRO/SUPABASE-DEDUP-HUB-SMART-NOTES-20261110.sql`
([link](https://github.com/SoulSchoolAcademy/NayaPOWER/blob/supabase/master-first-pass-20261110/TEAM-NITRO/SUPABASE-DEDUP-HUB-SMART-NOTES-20261110.sql)) ·
blob `1fdd660b9fd5827c11363ab72fa77c2907d6b9ed`
**Live measurement this pass (1,693 rows, up from 1,683 at the audit):**
32 note numbers are shared by two notes (one number by three) — 33 extra
rows; 26 titles appear more than once — 28 extra rows. That is bigger
than the audit's picture (20 titles, one named collision), because the
collisions kept happening while notes were filed in parallel.
**The file deletes exactly 3 rows — the only ones the record proves
stale:** the SN-2584 "Smart-Note Habit" copy (the Habit's true number is
SN-2586, and that row exists) and the SN-2632 + SN-2633 "Tune In, Then
Act" copies (the note's true number is SN-2634, and that row exists).
**Correction to the 02:58Z record:** the captain verified SN-2632/2633/
2634 are one file each on GitHub main. That is the FILES side. The TABLE
side still holds the two stale copies — this file removes them.
**What is NOT deleted:** the other 29 doubled numbers and the 26 doubled
titles are listed in the file as a review table. In most doubled-number
pairs the two rows are DIFFERENT notes that happen to share a number
(filed minutes apart by parallel seats) — the true owner is not in the
record, and guessing deletes a real note. A doubled title is not proof
of a doubled note either (e.g. "The Intelligent Block Rules", SN-2077
and SN-2304, two different days). A seat must read both notes and their
GitHub files before deleting either. The two triple-title groups ("The
Nonstop Loop" SN-0355/0589/0606; "The One-System Merge" SN-2592/2596/
2598) need their bodies read before any delete.
**Prerequisite:** run under the service key (no grant needed), OR run
the DELETE-grant file (3.2) first. Without either, every DELETE fails
with 42501 and nothing changes. After running: 1,690 rows; then re-bake
the Hub so the feed matches the table.

---

## Part 4 — The 33 Empty Tables: Waiting, Locked, or Unproven

### Title: The Empty Third
### Subtitle: 28 waiting to fill, 2 locked-empty, 3 with no known writer
### Nutshell: A third of the tables hold zero rows. Most are features that
are built but not yet used — the shape is there, the users have not
arrived. Two are empty and now locked. Three have no writer anywhere in
the repo, and this pass does not call them dead, because the repo clone is
diverged and a writer could live elsewhere — a seat must confirm before
anything is dropped.

**Waiting to fill (28)** — feature built or planned, zero use yet:
booking (availability, pages, bookings — Booking is still to be built);
memberships (content, members, invites, code prefs, member emails —
the add-on is not launched; the `memberships` table itself holds 1 row);
payments (payments, payment links, payment connections — by design the
system never sees the payment itself); citizen worlds + tiers; journal
entries (the journal habit is not running); connections (the Auto-Match
engine exists in code but its switch-on is Shawn's gate, so no matches
have ever run); media notes (wired in the walkthrough, never recorded);
member sessions / one-time codes / email tokens (those login flows were
never wired — logins go through Supabase Auth + the members trigger);
invite send log (the invite sender is live at v6, but the log is empty
while `invites` holds 4 rows); smart link joins (clicks flow — 3,899 —
joins never have); naya note categories (categories live in
`naya_category_prototypes`, 12 rows, instead); page about; products and
services; smart-connect participation; intelligence publications;
pending email sends (the mail queue sits empty; mail sends direct);
login attempts (auth logging not wired).
**Locked-empty (2)** — `ambassador_events` and `seat_lane_mapping`:
0 rows AND now locked by his hand (RLS on, grants revoked). They fill
only via the service role from here on.
**No known writer (3)** — `custom_defs`, `person_stages`,
`person_values`: no writer found in the repo clone (functions,
factory-pipeline, interfaces, Hub). Verdict: UNPROVEN, not dead. Do not
drop on this evidence alone — confirm against the live SQL and the
migration history first. If no writer and no plan is found, they are the
drop candidates.

---

## Part 5 — The Daily Watch (the Supabase master checks this every day)

### Title: The Daily Watch
### Subtitle: What the master looks at every morning, and what counts as a fault
### Nutshell: The audit is the baseline; the watch is how the 6 becomes a
10 and stays there. Every line below is a check with a number to match.
A fault is reported once, then stays silent until it changes or recovers.

1. **The six locked tables stay locked.** Anonymous read of each of the
   six must return 42501. Any other answer — rows returned, a different
   error — is a fault the same day.
2. **Row counts, top 10.** `hub_smart_notes` (1,693), `smart_mail_messages`
   (1,248), `smart_mail_threads` (1,114), `members` (7,502 — needs a SQL
   read; the public key cannot count it), `work_transitions`, `smart_link_clicks`
   (3,899), `nayanet_execution_receipts`, `hub_smart_notes_archive`,
   `distillation_queue`, `work_items`. Growth is expected for notes and
   mail; a jump of hundreds overnight, or a DROP in any count, is a fault.
3. **New tables.** Any table not in the audit's 97 is named the day it
   appears, with its RLS state and its grants. A new table with RLS off
   is a fault the same day.
4. **The 13 of 21 functions with the platform auth check off.** They
   verify identity inside their own code instead. The watch does not
   re-prove each one daily — it watches for a CHANGE: a new function
   with the check off, or a governed runtime whose deploy version moves
   without a record of why.
5. **The retrieval engine.** Until it deploys, the watch reports it
   missing every day. After it deploys, the watch probes it: no longer
   `NOT_FOUND`, auth-gated, answering real queries.
6. **The pages table.** Until the DDL runs, the watch reports it missing
   every day. After it runs, the watch counts its rows.
7. **The reports table.** Newest `report_date` must be yesterday or
   today. A gap of more than one day is a fault. (Today: newest is
   2026-10-23 — 18 days. The seed closes it to Nov 9; Nov 10 still owed.)
8. **Note-number collisions.** Any new SN number shared by two rows is
   named the day it appears. The 32 open collisions are the backlog.
9. **Duplicate titles.** New doubled titles are named; the 26 open ones
   are the backlog. Title alone never decides a delete.
10. **The 33 empty tables.** Any table leaving zero for the first time is
    news (a feature woke up). Any table in the no-known-writer three
    gaining a writer is news.
11. **The wide-open notes rules.** `hub_smart_notes` lets the public key
    insert and rewrite any row today (its rules pass everything). That is
    the standing design for the sync — but it means the public key can
    plant or rewrite notes. The watch notes it every day until the sync
    moves to a narrower rule or the service key.
12. **Repo vs live drift.** 7 live functions are not in the repo clone;
    2 repo functions are not live. The watch names any drift that grows.

---

## Part 6 — What Is Fixed, What Is Prepared, What Is Still Open

### Title: The State of the World
### Subtitle: Fixed, prepared, or open with a reason — every item named
### Nutshell: One thing is fixed and verified. Five things are prepared and
waiting for his hand. The rest is open for a named reason, not forgotten.

**FIXED (verified live this pass):**
- The six open tables are locked — all six return 42501 on an anonymous
  read (Part 2). (His hand, 02:40Z; re-verified here.)
- The audit screenshot's Off marks are explained, not open — they are the
  before picture (Part 2).

**PREPARED FOR HIS HAND (files on branch `supabase/master-first-pass-20261110`):**
- `nayanet_pages` DDL — `SUPABASE-NAYANET-PAGES-DDL-20261110.sql`
- `hub_smart_notes` DELETE grant — `SUPABASE-HUB-SMART-NOTES-DELETE-GRANT-20261110.sql`
- Reports INSERT fix — `SUPABASE-REPORTS-INSERT-20261110.sql` (service-key
  seed run preferred; the seed file already exists and is verified)
- Retrieval deploy runbook — `SUPABASE-RETRIEVE-DEPLOY-20261110.md`
- Notes dedupe — `SUPABASE-DEDUP-HUB-SMART-NOTES-20261110.sql` (3 safe
  deletes + review table)
- This report — `SUPABASE-MASTER-FIRST-PASS-20261110.md`

**STILL OPEN (with the reason):**
- Retrieve deploy — needs his tap + the service-key secret + the config
  entry + the widget-39a1bf91 question answered. Open because no deploy
  happens without his tap.
- Pages table — needs his hand on the DDL. Open because DDL is his hand.
- Reports seed — needs his hand with the service key (or his word on the
  INSERT policy). Open because the captain does not hold the service key.
- DELETE grant — needs his word (service-key dedupe is the recommended
  alternative). Open because the grant widens a door and that is his call.
- Dedupe beyond the 3 safe rows — needs a seat to read the paired notes
  and their GitHub files. Open because guessing deletes real notes.
- The 7,502 members' provenance — needs a service-key/Auth read. Open
  because the public key cannot see a single member row.
- Nov 10's Daily Intelligence Report — no report exists for today. Open
  because it must be written, not backfilled.
- The 13-of-21 auth-check-off functions — the in-code identity checks
  are the standing design, unconfirmed by this pass. Open because
  confirming them needs a code read seat.
- Repo vs live function drift + the unfilled connector doc — seat work,
  not started this pass.
- The different-seat re-run of this pass — owed; its report is the
  verification record.

---

## Verification (for the different seat)

### Title: Re-run These and Match Them
### Subtitle: Do not take this pass's word for it — run the same reads
### Nutshell: Every answer in this report traces to a live read or is
named as a gap. The re-run seat needs only this report and the anon key.

1. `seat_keys` (and the other five) — anon REST read returns 42501.
   Never read the hashes.
2. `media_notes` — anon read returns `[]`; spec columns include
   `media_url, transcript, summary, duration_s, owner_alias`.
3. `member_email_tokens` — anon read returns 42501; spec columns include
   `refresh_token_enc, provider, scopes`.
4. `members` — anon read returns `[]` (RLS hides rows from the public
   key); spec columns are `id, display_name, created_at, updated_at`.
   The 7,502 count is the audit's SQL count and cannot be re-counted
   with the anon key — say so, do not invent a recount.
5. `smart_mail_messages` — page all rows, count `from_alias`: every row
   is nitro, resolve, or naya-power. Expect ~1,248 and growing.
6. `hub_smart_notes` — newest row is SN-2637 or later; 32 numbers are
   shared by two rows; the three ib_ids in the dedupe file exist.
7. `nayanet_pages` — anon read returns PGRST205 (table does not exist).
8. `nayanet-intelligence-retrieve` — absent from the live function list;
   endpoint returns `NOT_FOUND`.
9. The five prepared files + this report exist on branch
   `supabase/master-first-pass-20261110` and read back byte-identical.

## Honest NOT-DONE list
- No deploy was made, no DDL was run, no service-key job was run, no
  database row was changed. Audit + prepare only, as briefed.
- The 7,502 members' provenance is NOT settled — it is an honest unknown
  with a named next read (service key / Auth dashboard), not a guess.
- The different-seat re-run had not been completed at filing time.
- The connector doc (`custom.supabase/CONNECTOR.md`) is still an unfilled
  template — noted, not fixed.
- widget-39a1bf91 is named as pending but its meaning was not found in
  any record searched this pass — the question is carried, not answered.
- The accompanying smart note was NOT filed by this pass. Reason: the
  captain is filing the "Supabase answers" note herself (recorded 03:11Z
  and 03:14Z Nov 10, with the World Masters and Non-Stop Method notes) —
  filing a second note with the same answers would duplicate it, and the
  noting seat was told not to duplicate those three. The pass's note text
  was drafted as SN-2640, but the number was taken between the guard run
  and the file attempt: the guard blessed SN-2640 (highest SN-2639, no
  open-PR claims, exit 0), and by the time the file-time check ran, the
  directory `SN-2640` already held another seat's note
  (`sn2640-notification-answers`). The file was correctly refused — the
  guard's blessing is only good at file time, and tonight several seats
  are filing at once. The draft is kept at
  `~/workspace/team-nitro/smart-notes/SN-2640-supabase-master-first-pass.md`
  for the captain to use or discard; the parent should confirm with her
  whether she wants this pass's text or her own.
- The live-feed verification of the captain's Supabase answers note is
  hers to confirm (feed + Box embedding, per the 03:11Z law) — it is not
  verified in this pass.
- No merge. No deploy.

---
*Supabase master, first pass — filed to GitHub `TEAM-NITRO/` on branch
`supabase/master-first-pass-20261110`. Report back to the captain with
receipts, not claims.*
