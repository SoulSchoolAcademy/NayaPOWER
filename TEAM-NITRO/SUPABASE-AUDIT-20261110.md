# Supabase Audit — Is It Set Up Right? (2026-11-10)

## Title: The Supabase Audit
## Subtitle: 21 functions live, 97 tables counted, one open door found — scored honestly 6 out of 10
## Nutshell: Supabase is the live memory of NayaNET — the notes, the mail, the ledger, the build queue all live here and the sync is flowing. But it is not 10 out of 10 yet: six tables sit with no lock on the door and anyone holding the public key can read and change them, the search engine was never deployed, the citizen-pages table still does not exist, and the daily reports have not landed in 18 days. Every gap below names whose hand fixes it.

**Project:** `dahisasgpfvziswqvmvm` (supabase-red-cable, production) · **Region:** ca-central-1 · **Status:** ACTIVE_HEALTHY · **Postgres:** 17 · **Created:** 2026-08-25
**Method:** read-only only. Management API function list + read-only SQL reads + anon-key REST reads (`sb-api`). No writes, no DDL, no policy or grant changes, no deploys. No keys, tokens, or passwords appear anywhere in this report.
**Audit time:** 2026-11-10 ~01:40–02:10Z. **Auditor seat:** Supabase auditor, under the captain.

---

## The Score — 6 out of 10

### Title: The Score
### Subtitle: Strong bones, one open door, two missing pieces
### Nutshell: The engine runs and the data flows, so this is not a failing grade. It is not a 10 because a stranger with the public key can read and rewrite the seat-keys table today, and because two pieces Shawn asked for — the search engine and the citizen-pages table — still are not there.

What is healthy (the 6 points earned):
1. All 21 edge functions are ACTIVE and responding — none down, none erroring.
2. 97 tables hold 187,175 rows; the sync is alive — the newest note in `hub_smart_notes` is SN-2629, filed today.
3. Row-level security is ON for 91 of 97 tables, and the October 22 archive fix still holds — the archive and the distillation queue are closed to the public key.
4. The build queue is idle and healthy: 194 done, 7 failed, 0 pending, 0 building.
5. All 11 Smart Match SQL functions are live (10 `sm_*` helpers + `smart_match` itself).
6. The project itself is healthy: ACTIVE_HEALTHY, Postgres 17, no outage.

What keeps it from 10 (the 4 points owed):
1. **Six tables have no lock on the door** — RLS off + full public-key grants, including the seat-keys table. (−2)
2. **The retrieval engine was never deployed** — Ask Naya and smart search have nothing to query. (−1)
3. **The citizen-pages table still does not exist** — the walkthrough has nowhere to write a page. (−0.5)
4. **The daily reports have not landed in 18 days** and the notes table cannot delete — the cleanup paths are blocked. (−0.5)

---

## Part 1 — Every Edge Function (21 live, none missed)

### Title: Every Edge Function
### Subtitle: 21 deployed, all ACTIVE — and one that exists only on paper
### Nutshell: The dashboard screenshot showed 12; the list scrolls to 21. All 21 answer. The one function that matters most for searching — the retrieval engine — is the one that is not there.

Source: Management API `GET /projects/dahisasgpfvziswqvmvm/functions`, 2026-11-10 ~01:40Z. "Version" is the deployment count (v43 = deployed 43 times). "Last deploy" is the `updated_at` stamp. Spot-probed live afterwards: `v7-smart-note-canonical`, `nayanet-smart-mail`, `nayanet-invite-sender` all answer auth-gated (exists); `nayanet-intelligence-retrieve` answers `NOT_FOUND` (does not exist).

| # | Function | Status | Deployments | Last deploy | Auth check on |
|---|---|---|---|---|---|
| 1 | naya-decision-context | ACTIVE | v17 | 2026-09-28 | Yes |
| 2 | naya-dream-replay | ACTIVE | v18 | 2026-09-19 | Yes |
| 3 | nayanet-act-runtime | ACTIVE | v72 | 2026-10-08 | No |
| 4 | nayanet-causal-learning-experiment | ACTIVE | v91 | 2026-10-08 | No |
| 5 | nayanet-causal-verify | ACTIVE | v89 | 2026-10-08 | No |
| 6 | nayanet-cold-runtime-proof | ACTIVE | v137 | 2026-10-08 | No |
| 7 | nayanet-github-build-dispatch | ACTIVE | v17 | 2026-09-12 | Yes |
| 8 | nayanet-github-dispatch | ACTIVE | v43 | 2026-10-09 | Yes |
| 9 | nayanet-github-webhook | ACTIVE | v16 | 2026-09-24 | No |
| 10 | nayanet-intelligence-commit-runtime | ACTIVE | v89 | 2026-10-08 | No |
| 11 | nayanet-invite-sender | ACTIVE | v6 | 2026-10-20 | Yes |
| 12 | nayanet-know-runtime | ACTIVE | v74 | 2026-10-08 | No |
| 13 | nayanet-law-runtime | ACTIVE | v73 | 2026-10-08 | No |
| 14 | nayanet-learning-verify | ACTIVE | v105 | 2026-10-08 | No |
| 15 | nayanet-project-intelligence-bridge | ACTIVE | v17 | 2026-09-21 | No |
| 16 | nayanet-prove-runtime | ACTIVE | v71 | 2026-10-08 | No |
| 17 | nayanet-smart-mail | ACTIVE | v34 | 2026-09-19 | Yes |
| 18 | nayanet-smart-note-viewer | ACTIVE | v13 | 2026-09-29 | No |
| 19 | nayanet-successor-handoff | ACTIVE | v15 | 2026-09-21 | Yes |
| 20 | nayanet-verified-ai-action | ACTIVE | v54 | 2026-10-08 | No |
| 21 | v7-smart-note-canonical | ACTIVE | v26 | 2026-10-07 | Yes |

**What changed since the November 3 inventory:** then it was 15 functions in the repo, 14 live. Now 21 are live — 7 more than the November 3 live list (`nayanet-github-build-dispatch`, `naya-dream-replay`, `nayanet-github-webhook`, `nayanet-smart-mail`, `nayanet-invite-sender`, `nayanet-project-intelligence-bridge`, `nayanet-successor-handoff`). The newest deploy is `nayanet-invite-sender` v6, 2026-10-20. The big governed-runtime deploy batch landed 2026-10-08 03:04Z (act, know, law, prove, commit, causal, learning, cold-proof, verified-action — all the same minute).

**NOT DEPLOYED — `nayanet-intelligence-retrieve`:** absent from the live list of 21; a live call to its endpoint returns `NOT_FOUND` / "Requested function was not found". The code is complete in the repo (`supabase/functions/nayanet-intelligence-retrieve/`, last touched 2026-10-20). This is the retrieval engine — free-text query to ranked Intelligent Blocks. Without it, Ask Naya, smart search, and every intelligence query path have nothing to call. Still open since November 3.

**Repo drift (watch item):** the local repo clone holds 16 function folders; 7 live functions are not in it, and 2 repo functions are not live (`nayanet-github-intake` and `nayanet-intelligence-retrieve`). There is no single source of truth for which functions exist.

**Auth check off (watch item):** 13 of the 21 functions run with the platform auth check off, including the governed runtimes (act, know, law, prove, commit). They verify identity inside their own code instead. That is the standing design, but it means the platform is not the guard for those doors — a seat should confirm the in-code checks, not assume them.

---

## Part 2 — Every Table (97 tables, 187,175 rows)

### Title: Every Table
### Subtitle: 97 tables counted one by one — most locked, six wide open, a third empty
### Nutshell: Nearly everything has a lock. The six tables without one are the story of this audit — and a third of the tables have never held a single row, which says which features are built and which are still waiting to be used.

Source: read-only SQL (`pg_tables`, one exact `count(*)` per table, `pg_policies`, `information_schema.role_table_grants`), 2026-11-10 ~01:45Z. Total rows: **187,175** across 97 tables. RLS on: 91 tables. RLS off: 6 tables (see Gap 1). Anon-key grants exist on 91 tables. 3 views also exist: `person_timeline_events`, `smart_link_daily_stats`, `smart_link_dimension_stats`.

**The 10 biggest tables:**

| Table | Rows | RLS | What it holds |
|---|---|---|---|
| work_transitions | 163,197 | On | Work state transitions (87% of all rows in the project) |
| members | 7,502 | On | Members |
| smart_link_clicks | 3,899 | On | Smart Link clicks |
| nayanet_execution_receipts | 1,902 | On | Governed-runtime execution receipts |
| hub_smart_notes | 1,683 | On | The Smart Notes feed table (live) |
| smart_mail_messages | 1,244 | On | Smart Mail messages |
| smart_mail_threads | 1,110 | On | Smart Mail threads |
| work_items | 732 | On | Work items |
| distillation_queue | 655 | On | Notes queued for distillation |
| hub_smart_notes_archive | 655 | On | Archived Smart Notes |

**All 97 tables with row counts** (exact `count(*)` this audit; RLS off marked ⚠️):

| Table | Rows | RLS | Table | Rows | RLS |
|---|---|---|---|---|---|
| alarms | 23 | On | nayanet_identities | 10 | On |
| ambassador_events | 0 | ⚠️ Off | nayanet_intelligence_index | 618 | On |
| ambassador_links | 7 | ⚠️ Off | nayanet_intelligence_lineage | 197 | On |
| automation_events | 3 | On | nayanet_intelligence_publications | 0 | On |
| booking_availability | 0 | On | nayanet_intelligent_blocks | 197 | On |
| booking_pages | 0 | On | nayanet_project_cognition_state | 21 | On |
| bookings | 0 | On | nayanet_smart_connect_participation | 0 | On |
| build_queue | 201 | On | nayanet_smart_ledger | 421 | On |
| census_daily | 38 | On | nayanet_successor_handoffs | 2 | On |
| citizen_tiers | 0 | On | nayanet_value_receipts | 2 | On |
| citizen_worlds | 0 | On | node_notes | 46 | On |
| connections | 0 | On | object_links | 87 | On |
| custom_defs | 0 | On | page_about | 0 | On |
| distillation_queue | 655 | On | payment_connections | 0 | On |
| hub_cost_daily | 19 | On | payment_links | 0 | On |
| hub_daily_intelligence_reports | 27 | On | payments | 0 | On |
| hub_daily_intelligence_reports_backup_20261022 | 26 | On | pending_email_sends | 0 | On |
| hub_meta | 27 | On | person_stages | 0 | On |
| hub_smart_notes | 1,683 | On | person_values | 0 | On |
| hub_smart_notes_archive | 655 | On | production_daily | 19 | On |
| invite_send_log | 0 | On | products_services | 0 | On |
| invites | 4 | On | project_intel_items | 395 | On |
| journal_entries | 0 | On | project_members | 1 | On |
| learning_evidence | 170 | On | projects | 9 | On |
| ledger_entries | 30 | On | queue_packets | 10 | On |
| login_attempts | 0 | On | scheduled_messages | 2 | On |
| media_notes | 0 | On | seat_keys | 2 | ⚠️ Off |
| member_email_tokens | 0 | On | seat_lane_mapping | 0 | ⚠️ Off |
| member_otp_codes | 0 | On | smart_link_clicks | 3,899 | On |
| member_sessions | 0 | On | smart_link_joins | 0 | On |
| members | 7,502 | On | smart_link_reserved_names | 46 | On |
| membership_code_prefs | 0 | On | smart_links | 14 | On |
| membership_content | 0 | On | smart_list_items | 78 | On |
| membership_invites | 0 | On | smart_lists | 12 | On |
| membership_member_emails | 0 | On | smart_mail_aliases | 23 | On |
| membership_members | 0 | On | smart_mail_messages | 1,244 | On |
| memberships | 1 | On | smart_mail_threads | 1,110 | On |
| messenger_messages | 4 | On | smart_note_artifacts | 188 | On |
| naya_category_prototypes | 12 | ⚠️ Off | smart_note_events | 52 | On |
| naya_note_categories | 0 | On | smart_note_receipts | 47 | On |
| naya_note_filing | 19 | ⚠️ Off | smart_notes | 39 | On |
| naya_notes | 14 | On | smart_space_members | 2 | On |
| nayanet_authority_grants | 41 | On | smart_spaces | 7 | On |
| nayanet_brain_relationships | 265 | On | user_connections | 1 | On |
| nayanet_checkpoint_receipts | 148 | On | v7_smart_note_transactions | 47 | On |
| nayanet_cognition_events | 238 | On | voice_requests | 245 | On |
| nayanet_execution_outcomes | 410 | On | work_items | 732 | On |
| nayanet_execution_receipts | 1,902 | On | work_transitions | 163,197 | On |
| nayanet_github_dispatch_receipts | 29 | On |  |  |  |

**33 tables hold zero rows** — booking (availability, pages, bookings), memberships content/members/invites, payments, journal entries, citizen worlds/tiers, connections, media notes, and more. The shapes are built; the features have not been used yet. `nayanet_pages` is not in this list at all — it does not exist (Gap 3).

**Anon-key grants — the shape to understand:** 91 tables grant the anonymous key privileges. For most tables that grant is the full set (SELECT, INSERT, UPDATE, DELETE), and the RLS policies are the only thing standing between the public key and the data. Where a policy is wide open, the public key can write: `hub_smart_notes` has anon INSERT, SELECT, and UPDATE policies that all pass everything (`qual=true`), by design for the sync — anyone holding the public key can insert or rewrite any note row. `nayanet_smart_ledger` is the exception that proves the rule: anon holds no SELECT/INSERT/UPDATE/DELETE there at all. `smart_links` is SELECT-only for anon; `smart_link_clicks` and `smart_link_joins` are INSERT-only.

---

## Part 3 — The Known Gaps, Re-Verified Live

### Title: The Known Gaps, Re-Verified
### Subtitle: Four old gaps checked again — two still open, one holding, one bigger than remembered
### Nutshell: The archive lock held. The delete gap, the missing pages table, and the blocked reports are all still exactly where they were — and the duplicate picture is now measured, not guessed.

**Gap 1 — hub_smart_notes DELETE still blocked (GRANT gap) — STILL OPEN.**
Live proof: the anon grant list for `hub_smart_notes` reads INSERT, SELECT, UPDATE — no DELETE. The policy list agrees: INSERT, SELECT, and UPDATE policies exist; no DELETE policy exists. The sync code itself says it (`sync-smart-notes.py`, tombstone pass): "the anon role has no DELETE privilege on hub_smart_notes (Postgres 42501 — GRANT DELETE needed, Shawn's hand)". Consequence: when a note file is deleted on GitHub, its row stays in the table forever; the feed only hides the card. Fix: `GRANT DELETE` + a DELETE policy — Shawn's hand (SQL Editor).

**Gap 2 — Stale duplicates + the SN-2584 collision — MEASURED, STILL OPEN.**
Live proof (exact counts, 2026-11-10): no two rows share an `ib_id` (1,683 distinct of 1,683 rows). But 20 titles appear more than once — 18 titles twice, 2 titles three times. The two triplets:
- "The Nonstop Loop — NayaPOWER Operating Code" ×3 (SN-0606, SN-0589, SN-0355 — three different numbers, one title, all filed 2026-10-22 01:41–01:42Z).
- "The One-System Merge: Onboarding, Factory, PI, Manual, Design Law, in the Factory" ×3 (SN-2592, SN-2596, SN-2598 — filed 2026-11-09 21:44–21:56Z, twelve minutes apart).
And the SN-2584 collision is real: two different notes share the number 2584 — "The NayaNET Operation Manual" (2026-11-09 21:10:57Z) and "The Smart-Note Habit" (2026-11-09 21:14:25Z). The "71 stale duplicate rows dropped at bake" in the sync logs is a different thing — those are bake-time exclusions from the Hub HTML, not rows removed from the table. Cleaning the table needs the DELETE grant from Gap 1 first, then a dedupe pass. Fix: Shawn's hand for the grant; a seat does the dedupe after.

**Gap 3 — hub_daily_intelligence_reports ingest blocked — STILL OPEN.**
Live proof: the table has exactly one policy — anon SELECT ("reports are publicly readable"). No INSERT policy exists, so an anon-key insert fails with 42501. The table holds 27 rows; the newest report is dated **2026-10-23** and the oldest 2026-09-27 — nothing has landed in 18 days. The backfill work record (2026-11-09) already named the cure: a service-key run of the seed, or an INSERT policy. Fix: Shawn's hand (he holds the service key).

**Gap 4 — nayanet_pages missing — STILL OPEN.**
Live proof: anon REST read returns `PGRST205` — "Could not find the table 'public.nayanet_pages' in the schema cache" (hint points at `nayanet_identities`). The table list of 97 confirms it is absent. `nayanet_identities` columns are still only `alias, name, device_key, created_at, cert_no` — no pages column, no JSONB. The walkthrough writes identity here (10 rows) but a citizen page has nowhere to land. Table creation needs DDL — the REST API cannot do it. Fix: Shawn's hand (SQL Editor).

**Gap 5 — Archive + distillation_queue RLS — RE-VERIFIED, STILL CLOSED (the October 22 fix holds).**
Live proof: neither table appears in the anon grant list at all, and neither has any policy — RLS is on for both. The public key cannot read or write either. Archive: 655 rows. Distillation queue: 655 rows. Certified closed by Chi on October 22; still closed today.

---

## Part 4 — The New Finding: Six Tables With No Lock

### Title: The New Finding
### Subtitle: Six tables, RLS off, full public-key access — one of them holds seat keys
### Nutshell: This is the finding the November 3 inventory could not see, because it only checked 15 tables. Six of the 97 have no row-level lock at all, and the public key holds every privilege on them — read, write, and delete.

Live proof: `pg_tables` shows `rowsecurity=false` for exactly six tables, and `pg_policies` returns zero policies for all six, and the anon grant list gives the public key DELETE, INSERT, SELECT, UPDATE (and more) on all six:

| Table | Rows | What it holds |
|---|---|---|
| seat_keys | 2 | Seat names + key hashes (seats: resolve, naya-power — neither revoked) |
| ambassador_links | 7 | Ambassador links |
| naya_category_prototypes | 12 | Category prototypes |
| naya_note_filing | 19 | Note filing records |
| ambassador_events | 0 | Ambassador events (empty today) |
| seat_lane_mapping | 0 | Seat-to-lane mapping (empty today) |

**Verified live, not just in the catalog:** an anon-key REST read of `seat_keys` returned both rows. No key values were read, printed, or stored — only the seat names and the fact that neither is revoked. The point stands on the read alone: anyone holding the public anon key — which ships in the app's client code — can read those rows today, and the grants say they can also insert, update, and delete them. The two empty tables are the same shape with no rows yet: the door is open before anything valuable moves in.

Fix: enable RLS + add policies (or revoke the anon grants) — Shawn's hand (SQL Editor). This is the single most important fix in this audit, and it is not a seat action.

---

## Part 5 — What the Hub and the Feed Actually Read

### Title: What Reads What
### Subtitle: GitHub is the memory; Supabase is the live copy the pages read
### Nutshell: The canonical notes live on GitHub. Supabase holds the live copy the Hub is baked from and the mail, links, and ledger the app reads while you use it. If GitHub vanished, the notes would survive in Supabase; if Supabase vanished, the notes would survive on GitHub — but the live app would go quiet.

- **Smart Notes:** canonical files live on GitHub main (`BRAIN/05-MEMORY/SMART-NOTES/`). `factory-pipeline/sync-smart-notes.py` upserts them into `hub_smart_notes` (anon key, `on_conflict=ib_id`) and bakes the newest notes into the Hub HTML at deploy time. The live Hub and feed show the baked copy — they do not query Supabase on every view.
- **Smart Mail, Smart Lists, Smart Links, identities, ledger:** read live from Supabase by the app pages via the anon REST key (`smart_mail_messages` 1,244 rows, `smart_mail_threads` 1,110, `smart_links` 14, `smart_link_clicks` 3,899, `nayanet_smart_ledger` 421, `nayanet_identities` 10).
- **Build queue:** the factory pipeline polls `build_queue` (194 done, 7 failed, 0 pending).
- **Reports:** `hub_daily_intelligence_reports` is read-only for the public key; nothing new has landed since 2026-10-23 (Gap 3).
- **One-system merge spec note:** `ONE-SYSTEM-MERGE-SPEC-20261109.md` contains zero mentions of Supabase — the one-system map does not yet place where Supabase sits. A seat can add that.

---

## Part 6 — What Would Make It 10 (the exact list)

### Title: What Would Make It 10
### Subtitle: Seven fixes, split by whose hand holds them
### Nutshell: Three fixes need Shawn because only he holds the service key and the SQL Editor. Four can be done by a seat once he says go. Nothing here needs a new system — it needs the locks turned on and the two missing pieces put in place.

**Shawn's hand (service key, DELETE grant, SQL Editor DDL):**
1. Lock the six open tables — enable RLS + policies (or revoke anon grants) on `seat_keys`, `ambassador_links`, `naya_category_prototypes`, `naya_note_filing`, `ambassador_events`, `seat_lane_mapping`. (Gap: Part 4 — the top fix.)
2. Grant DELETE on `hub_smart_notes` + a DELETE policy, so tombstoned notes actually leave the table. (Gap 1.)
3. Create the `nayanet_pages` table (DDL in the SQL Editor) so the walkthrough can write citizen pages. (Gap 4.)
4. Run the Reports seed under the service key (or add an INSERT policy) so daily reports land again. (Gap 3.)

**A seat can do, once Shawn says go:**
5. Deploy `nayanet-intelligence-retrieve` — code complete in the repo, never deployed. Unblocks Ask Naya and smart search.
6. Dedupe `hub_smart_notes` after the DELETE grant lands — the SN-2584 collision and the two triple-title groups, then re-bake and re-check live.
7. Reconcile repo vs live functions (7 live functions missing from the repo clone; 2 repo functions not live) and place Supabase in the one-system merge spec.

**Watch items (no fix owed, a seat confirms):**
- 13 of 21 functions run with the platform auth check off — confirm the in-code identity checks on the governed runtimes.
- The connector doc (`custom.supabase/CONNECTOR.md`) is still an unfilled template — it records nothing about how this audit actually ran (sb-api + Management API + service key). A seat should fill it in from this audit.

---

## Verification (for the different seat)

### Title: Verification
### Subtitle: Re-run these and match them
### Nutshell: Do not take this audit's word for it — run the same reads and match the numbers.

Re-run sample (3 tables + 3 functions):
1. `hub_smart_notes` — 1,683 rows; anon SELECT returns newest SN-2629; anon grants INSERT/SELECT/UPDATE, no DELETE.
2. `seat_keys` — 2 rows; RLS off; anon REST read returns both seats (read seat names only, never the hashes).
3. `hub_daily_intelligence_reports` — 27 rows; newest report_date 2026-10-23; one policy only (anon SELECT).
4. `nayanet-intelligence-retrieve` — absent from the Management function list; live endpoint returns `NOT_FOUND`.
5. `v7-smart-note-canonical` — ACTIVE v26; live endpoint answers auth-gated.
6. `nayanet_pages` — anon REST read returns `PGRST205`.

Filing: `TEAM-NITRO/SUPABASE-AUDIT-20261110.md` on branch `supabase/audit-20261110`, read-back verified byte-identical. Accompanying smart note filed in the `##` format and verified live on the feed.

## Honest NOT-DONE list
- No fix was made in this audit — read-only by design. Every gap above is still open at filing time.
- No different-seat re-run had been completed at filing time — the re-run seat's report is the verification record, and it is owed.
- The "3 stale duplicate rows" named in the brief could not be matched to one named set in the record; what the live table holds instead is measured in Gap 2 (20 duplicated titles, two triplets, one number collision).
- The connector doc is still an unfilled template (noted, not fixed — a seat task).
- No deploy, no merge, no Supabase change of any kind was made.
