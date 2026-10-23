# Project Intelligence — First Source-Linked Content Fill Receipt

**Date:** 2026-10-23 ~20:52–21:00 UTC  
**Executor:** Naya GPT-6, collaborative project-intelligence seat  
**Human mandate:** Team Naya fills and maintains the content of `nayanet.live/projects`; Director reviews, not data-enters.  
**Target:** Existing Supabase NayaNET Projects records; no new database, Hub shell, permissions, credentials, or production deployment.  
**Truth state:** DATABASE WRITE PERFORMED AND READ BACK; LIVE AUTHENTICATED BROWSER, CONTINUOUS SYNC, AND INDEPENDENT VERIFICATION STILL PENDING.  
**Coordination:** Team board #2793; existing Project Intelligence spec SN-0839, build order SN-0840; PR #3014 and existing implementation owners.

## Problem and observations

1. Current `/projects` HTML serves HTTP 200 but its JavaScript reads `project_intel_items` by `project_id`; the newer operational queue uses `work_items`.
2. Initially 135 `work_items` and 126 `project_intel_items` were all parent-project records, so all eight sub-project Intelligence boards appeared empty.
3. During the same cycle another Team Naya seat filed/re-homed 38 canonical `work_items` across eight actual sub-projects; follow-up showed 105 work records retained at root. This seat did not duplicate or rehome those canonical work items.
4. Prior to content-projection repair, 27 child-source work keys still had their legacy display records under the parent, and 11 new child work keys had no legacy display record.

## Authorized, bounded content writes (existing tables only)

- Created **8** ordinary `naya_notes` handoffs under existing owner alias and linked each to its actual sub-project ID. Each note declares authorship, date, source links, **reported vs independently proven** distinction, honest unknowns and owner continuation. Stable idempotency key is `source_context=project-intelligence-seed-20261023:<project_uuid>`. The first-pass escaped-newline formatting issue was fixed in exactly 8 notes (captured learning).
- Created **8** `object_links` `b_kind=naya_note`, and **16** `object_links` `b_kind=url` to grounded GitHub area/implementation records. All links use the existing unique key and conflict no-op semantics. New part notes are not automatically canonical Smart Notes or approved proof.
- Performed an atomic source-keyed projection reconciliation on the existing `project_intel_items` reader table. **27** original display records were **re-homed** to the same child `project_id` as their corresponding source `work_items` (IDs preserved; original project ID/state recorded in JSON `notes` provenance); **11** genuinely missing child display records were inserted from source work items, with stable item keys and source-record ID/provenance. No canonical `work_items` records or original root-only unmatched projection records were deleted.
- Work states converted for the legacy display vocabulary only: `needs_shawn→needs-his-hands`, `in_progress→in-motion`, `queued→queued`, `blocked→blocked`, `verifying→in-motion` **with explicit verification-pending detail**, `done_proven→done-proven` only if evidence URL and distinct, nonempty maker/prover check passes. A weaker record is not shown as proven.
- **No schema, RLS, policy, deployment, auth token or workflow mutation.** The content write used the authorized connected Supabase management data-access tool; production row-level policies were not themselves demonstrated by this administrative write. A real end-user identity read/write and cross-tenant denial test remain owed.

## Source-matched post-write verification (2026-10-23 UTC)

| Existing sub-project | Canonical work rows | Current display intel rows | Source-attributed notes | Useful links |
|---|---:|---:|---:|---:|
| Ask Naya | 6 | 6 | 1 | 3 |
| Smart Mail | 2 | 2 | 1 | 3 |
| Team Nitro | 3 | 3 | 1 | 3 |
| The Mirror Program | 3 | 3 | 1 | 3 |
| The One Flow | 2 | 2 | 1 | 3 |
| The One Hub | 6 | 6 | 1 | 3 |
| The Smart Factory | 5 | 5 | 1 | 3 |
| Voice | 11 | 11 | 1 | 3 |
| **TOTAL** | **38** | **38** | **8** | **24** |

- Root now had 105 `work_items` and 99 `project_intel_items` after 27 rehomes. Root-only population differences remain a separate mapping obligation, not declared data loss.
- Post-write SQL checked child `done-proven` display records without a nonempty evidence URL: **zero**.
- Every one of eight child projects has one source-linked `naya_note` and 3 total new links.
- This is proof of a **database state**, NOT browser rendering, live sync automation or independent verification. No automatic recurrence has been demonstrated. If source `work_items` moves again, the legacy projection could drift and show stale information.

## Immediate permanent cure and acceptance

1. Existing Data/Bridge owner must build/complete **ONE** event-derived project-content adapter from canonical `work_items`, proof, GitHub/Smart Notes/part notes and other applicable sources to the live Projects payload. It must preserve source IDs, project ancestry, RLS scope, maker/prover evidence, timestamp, atomic snapshot consistency, all status variants including **verifying**, and note/feed linkage.
2. `T-CONTENT`: through the actual authorized producer, create a source item, change status, move it between projects, revoke evidence, add a note. Verify the correct item is shown in parent/child, global/part feed and permitted machine view with same snapshot ID; no manual SQL, duplicates, stale green or unauthorized leak.
3. Existing Hub/VERIFY owner must perform real browser authenticated acceptance at `https://nayanet.live/projects?p=<real-uuid>`, including each of eight children; confirm the 38 items, notes and links actually render (not only backend counts). Failure is an owned defect, not a “done.”
4. Human-facing Essence Rule: show the most useful high-level truth; deeper note history and proof one tap behind each part.
5. Reconcile the first-fill rows with the continuous derived path; retire this manual initialization mechanism after production-worthy auto-refresh is independently proven. Use the `projection_migration` JSON note metadata for rollback/reconciliation; do not blindly delete records.
6. File a reusable Smart Note **through the authorized existing door**, then verify live Smart Link, if this recovery creates a new, nonduplicate lesson. A GitHub PR or this receipt is not itself a live Smart Note.

## Next executable action

**ACT/Bridge and existing Project Intelligence integrator:** wire the real source `work_items`→existing `/projects` data read/publisher, with stable exact-source keys and `T-CONTENT` adverse tests. Keep all eight now-populated projects visible throughout a governed migration. Naya/VERIFY independently certifies the authenticated page and repeatable source update.

**Conclusion:** first material content population COMPLETE at database level; user-facing rendering and sustainable machine operation UNKNOWN; do not declare 10/10.

## Subsequent live drift falsifier — 2026-10-23T20:59:41Z

During the *same collaborative cycle*, other Team Naya workers generated further canonical `work_items` and the parent began diverging again. The source-key diagnostic in this PR — `tools/reporting/project_content_parity.sql` — was fetched back from its actual GitHub blob and executed read-only against the live Supabase project. Its exact result:

- **NayaPOWER root:** 133 canonical work records, 123 display *work* records (126 total display rows including **three non-work `production:` pseudo-records**). **Ten missing keys** and **eleven differing source/display state-or-proof cases**. Three pseudo-records disguise the missing-ten defect as a misleading gross count difference of seven.
- **Eight sub-projects:** source and display exact item-key parity in the diagnostic for all 38 assigned records, zero missing/extra keys and zero mismatched state/proof labels at this timestamp.
- Missing root classes: `journey-test-2026-10-23`, `q14-10`, and eight new `waste-...-2026-10-23` detector-generated work entries. The “waste” title is the *source claim*, not an independent finding that the watcher had zero human value; the efficiency owner must classify it correctly.

**Why this matters:** one-time manual rehoming is not continuous intelligence. An ordinary count check is also insufficient: the release gate must compare the exact source-key sets, states and evidence on every change. No claim of automatic refresh can pass while this query shows `missing_keys>0`, `stale_extra_keys>0` or `differing_state_or_proof>0`. During eventual cutover, retire the `production:` pseudo-records through the separately governed existing migration, never count them as user tasks.

Two additional *root* source links were also filed via the existing `object_links` table: the independently observed live SN-0840 master build note and the proposed implementation PR #3014; they are labeled so a reviewer can distinguish canon from proposed annex.

**Required owner action:** Connect the actual publisher so `work_items` updates are projected without further SQL intervention, wire this read-only diagnostic into the existing verified monitoring path, then have a distinct reviewer rerun the exact query and an authenticated browser journey until both source and live display are in parity. Do not reduce or disguise the mismatch by suppressing legitimate new work.
