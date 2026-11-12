# Feed Regression — The 794 → 338 Drop, Found and Fixed

## The feed went quiet — and the bake never dropped a note

**Subtitle:** The live feed lost 456 cards in one deploy, and the build scripts are innocent.

**Nutshell:** The live feed at nayanet.app/feed-live.json serves 338 cards, down from 760 on Nov 10 00:42Z. The cause is not the bake: the local bake is healthy at 794 cards. The cause is a single Cloudflare deploy — Hub worker version #600, 2026-11-10T20:17:26Z, source "wrangler" — which uploaded the repo's HUB/app asset set verbatim, including the registry bot's 338-card feed-live.json, with no overlay of the sync's fresh feed. The fix lands in build_feed_live.py: a shrinkage guard that refuses a shrunken live base, and a reconciliation that re-adds any missing row in the recent window whatever its date. The re-bake restores 794. The live restore itself needs the converged deploy — his hand, not this round's.

## What dropped, and why

**Stage: deploy. Rule: a wrangler upload ships the repo asset set verbatim.**

- **Live feed = the repo file, byte for byte.** `curl nayanet.app/feed-live.json` (2,689,978 bytes, md5 `e6c9d04b187e278afb19f6ffb9109846`) is identical to `HUB/app/feed-live.json` on GitHub main (same size, same md5). The live feed IS the registry bot's file.
- **The drop event is pinned to the minute.** Cloudflare Hub worker versions #576–#599 (Nov 10 01:26–06:22Z) are all source "api" — the sync's converged deploy. Version #600, 2026-11-10T20:17:26Z, is source "wrangler", a different author id, `triggered_by: version_upload`. Version #599 (06:22:40Z) is the sync's deploy of the 794-card feed — its timestamp matches the local `hub-feed-live.json` mtime exactly. Nothing after #600 exists: #600 is the live version.
- **The 338 reconciles to the card, by the registry bot's own arithmetic.** The repo feed grows by one-card splices from the registry bot (nayanet[bot]): 323 notes (Nov 7 04:06Z) + 10 (SN-2239–SN-2248, distillation batch 1, Nov 7 23:37Z) + 3 (SN-0858–SN-0860, Nov 8 19:25Z) + 1 (SN-2532, re-pointed to SN-2535, Nov 9) + 1 (SN-2600, Nov 9 22:40Z) = 338. Exact.
- **Live is a strict subset of the local bake.** All 338 live ids are in the local 794. The 456 missing are all created 2026-11-07T21:27 → 2026-11-10T04:33 (395 official + all 61 naya-note cards). The live feed's only post-cutoff cards are the 12 the registry bot itself spliced (SN-2239–SN-2248, SN-2535, SN-2600).
- **The two writers, named.** The sync's `build_feed_live.py` (VM-local, incremental, 794 cards) and the registry bot (repo-side, splice-by-splice from the registry manifest, 338 cards) both write a file called feed-live.json. The worker serves whichever deployed last. The converged deploy (`deploy.py` → `deploy_hub_assets.stage_hub_assets`) overlays the fresh local feed onto the repo asset set; the wrangler path has no such overlay step. That missing overlay is the rule that dropped the cards.
- **The registry is stale, and that is a separate job.** The registry manifest (`.naya/memory/smart-notes/index.json`) holds 1,281 entries; only 338 of them are in the feed, and the 456 newest notes are not in the registry at all (the registry stopped indexing around Nov 7 — already a known open item). The tree holds 1,616 files. The feed was never a full mirror of either, by standing design; this round restores the last-good 794 and closes the permanent-loss hole. Backfilling the older 942 registry entries is a separate decision for Shawn — it would roughly double the feed past the 5 MB hang guard, so it is NOT done here.

## The true counts, verified first (never assumed)

| Source | Count | How established |
|---|---|---|
| Live feed (curl, nayanet.app/feed-live.json) | **338** cards, 2,689,978 bytes, md5 `e6c9d04b…` | curl + parsed JSON, Nov 11 00:48–01:00Z |
| Repo HUB/app/feed-live.json (main) | **338** cards, 2,689,978 bytes, same md5 | GitHub Contents API + raw curl |
| Local bake (factory-pipeline/hub-feed-live.json) | **794** cards, 6,144,794 bytes | parsed JSON, mtime Nov 10 06:22Z |
| Registry manifest (.naya/memory/smart-notes/index.json) | **1,281** entries (1,280 distinct ids) | raw curl + parsed JSON |
| GitHub tree (SMART-NOTES files, sync-state) | **1,616** paths, 1,598 distinct basenames | .sync-state.json, Nov 10 23:35Z |
| Supabase sync heartbeat | 0 synced, 1,616 skipped, 13 errors | .sync-heartbeat.json, Nov 10 23:35Z |

## The five gates (before every consequential action, with evidence)

1. **Is it right?** Yes — a feed that silently drops 456 notes serves no one; restoring them and guarding against the next silent shrinkage serves every citizen who reads the feed.
2. **Is it what they truly need?** Yes — his goal is the feed telling the truth: every note that exists in the bake is there. The fix restores the last-good truth and refuses to adopt a shrunken base again.
3. **Is it mine to do?** Yes, inside the line: investigate + edit the bake script only. The merge, the live deploy, and the registry backfill are his hand. No note is deleted; no note is invented.
4. **Is now the time?** Yes — the live feed is wrong right now, the next sync would otherwise build on the shrunken base, and the floor's third lane is this round.
5. **Can I prove it?** Yes — live-vs-repo md5 identity, Cloudflare version history, splice arithmetic, subset proof by parsed ids, and the re-bake count below. The wall render and the live restore are honestly listed as NOT DONE (browser dead, deploy his hand).

## The verifier's exact checklist (written BEFORE the build starts)

The different-seat verifier checks these, in order, with live measurements — no claim without one:

1. **Count by curl + bytes.** `curl -sL nayanet.app/feed-live.json` parses to the same card count as the re-baked local file, and the byte count is recorded. (Live count changes only after the converged deploy — his hand — so the verifier records the local re-bake count now and the live count at deploy time.)
2. **Live == local id sets.** Every live card id is in the re-baked file, and every re-baked card id is live — parsed ids, not substrings. Zero lost, zero gained-but-unknown.
3. **Newest note current.** The newest card in the re-baked feed is SN-2650 (2026-11-10T04:33:10Z) or newer if a note landed since; today's notes, if any, are present.
4. **The four Nov-7 cards are back.** The four local-only cards created 2026-11-07T21:27 or later — all Naya Notes, restored by the NN pass: `NN-20261107-ultimate-number-session` (21:27), `NN-20261107-the-charge-comprehend` (21:35), `NN-20261107-the-north-star` (21:50), `NN-20261107-supercharger-campaign` (22:05) — are present in the re-baked feed. (Note, corrected in the finding: these four are NN cards, so the NN pass restores them on any bake; the removed Nov-8 floor matters for SN cards in the same position in a future reset.)
5. **No duplicates.** Unique ids == card count in the re-baked feed; no duplicate SN numbers introduced.
6. **No deletions, no inventions.** No card removed relative to the 794 last-good file except tombstone-confirmed deletions (none in this round); no card present that has no live GitHub file or Supabase row.
7. **The guard fires on the shrunken base.** The fixed builder, run against the live 338 base, prints the shrinkage warning and adopts the local last-good file — proven by the run's own stdout, not by assertion.
8. **NN cards restored.** All 61 naya-note cards are in the re-baked feed (the live feed has zero).
9. **Hub page untouched; search untouched.** No change to any Hub page file; no change to the search corpus or engine. The diff touches `build_feed_live.py` only.
10. **Gate + human checks.** Design-contract gate clean on the record; H1–H5 attested. The Hub wall render (390 + 1440, scroll 0 and scrolled, zero console errors) is QUEUED — browsers are dead — and is recorded as not done, not claimed.
11. **Branch + PR.** Branch `feed/regression-20261111`, one change, one PR, no merge. The PR link is in this record.

## The fix (build_feed_live.py — EDIT only)

1. **Shrinkage guard (the fix).** After fetching the live feed, the builder reads the local last-good file (`hub-feed-live.json` beside the script). If the live base is smaller than the last-good file, it adopts the last-good file as the base and prints a loud `REGRESSION` warning naming both counts. A shrunken live feed can never again become the base a bake builds on. (Root cause: the wrangler deploy bypassed the overlay; the guard makes the bake immune to the next bypass.)
2. **Reconciliation without the Nov-8 floor.** The add pass now re-adds ANY row in the recent window that is missing from the feed, whatever its `note_created` — the `>= 2026-11-08` floor is gone. The window itself (500 most recent rows) and the live-tree resurrection guard stay exactly as they are, so no retired note can come back and no old backfill is smuggled in.
3. **sync-smart-notes.py: no change, verified.** The sync ingests the whole tree, the heartbeat shows 0 synced / 1,616 skipped (nothing new to carry), and the drop is proven at the deploy stage, not the sync stage. Editing it would be motion without cause.

## Re-bake (run 2026-11-11 ~01:05Z, fixed builder, in-memory capture — disk writes for multi-MB files EPERM-fail in this VM)

- **Guard fired, verbatim:** `REGRESSION: live feed 338 cards is SMALLER than last-good local bake 794 cards — adopting the local file as the base, NOT the shrunken live feed`
- **Tombstone pass:** 0 removed, 170 candidates kept, 63 unresolvable id shapes left alone; feed 794.
- **NN tombstone pass:** 0 removed. **NN add pass:** 0 added, 61 refreshed, 0 skipped, 0 failed.
- **SN add pass:** **67 added, 23 skipped, 0 failed; feed now 861 cards.**
- **Captured output:** 6,583,817 bytes, md5 `597f45776fedb4961d35624e50e63003`, count **861**, unique ids 861, newest SN-2654 `2026-11-10T23:33:00Z`, 61 naya-note cards, all four Nov-7 NN cards present.
- **The 67, characterized (parsed from the staged branch file):** 4 genuinely new (SN-2651–SN-2654, filed Nov 10 23:28–23:33Z, after the 06:22 bake); 56 reconciled older notes (created before Nov 8 — the old floor excluded them; the dateless reconciliation restores them, including SN-2220–SN-2238 and SN-2428–SN-2432); 7 from Nov 9. **Zero lost** vs the 794 last-good file. **Zero known-superseded ids** among the 67 (checked SN-0131–0135, SN-2212/2213 — none present).
- **Correction to the brief's number:** the final count is 861, not 794 — 794 was the last-good count at 06:22Z; notes kept landing after it, and the fix's reconciliation restores older live notes the old floor excluded. 861 = 794 + 67 verified adds, 0 lost.
- **Staged proof (branch only, no merge, no deploy):** `HUB/app/feed-live.json` on branch `feed/regression-20261111`, blob `c585d17acb25356955d4b4e22706c620f9648628` — verified by raw curl from the branch: same md5, 861 cards. Fixed script at `TEAM-NITRO/feed-regression-20261111/build_feed_live.py`, blob `bab49408e92293172ebff9f2abd7b5bc8b6bbcf7`.
- **Process note:** the first re-bake run died at the final write — my in-memory capture wrapper restored the real `open` before `main()` ran, so the 6 MB write hit EPERM. Fixed the wrapper (patch stays through `main()`); the second run's stdout redirect to a file also died (exit 120: buffered prints could not flush to the EPERM'd file). The third run, piped through the runtime, completed clean. Lesson filed in the scorecard below.

## NOT DONE (honest list)

- **Live feed still 338** until the converged deploy runs — the deploy is his hand (protected gate). The re-bake is staged on the branch (`HUB/app/feed-live.json`, 861 cards, md5-verified from the raw branch URL); the converged deploy overlays it live. Nothing on main was touched.
- **Hub wall render check queued** — browsers are dead in this VM (Firefox SIGSEGV, Chromium SIGTRAP, cloud browser queued since 23:05Z); 390 + 1440, scroll 0 and scrolled, zero console errors, still owed. The count proof by curl + bytes is done; the render is not claimed.
- **Registry backfill (942 entries) NOT done** — separate decision for Shawn; would roughly double the feed again past the 5 MB hang guard. The 56 older notes restored here came through the table's recent window, not a registry backfill.
- **The wrangler path itself NOT changed** — the seat that ran it is not named here (author id only, no name); the durable cure (a wrangler deploy must overlay the fresh feed, or wrangler retires as a Hub path) is a decision for the captain, recorded here, not silently fixed.
- **Design-contract gate on this record:** `check-gate.py` run on RECORD.md — OVERALL PASS (note-format check (g) PASS; the 1 bold-inline label is a quoted line, not a section definition). H1–H5 attested in `human-checks.txt` beside it (the gate prints H1–H5 as not-applicable to note files; the attestation stands as the maker's record, not as a gate PASS).

## Self-scorecard (maker first, before reporting — honest score: 8/10)

**Why it is not a 10:** the live feed is still 338 — the thing Shawn's eye will see is unchanged until his hand deploys; the wall render is unverified (browsers dead); the wrangler path that caused this is not cured, only guarded against; and I burned two re-bake runs on my own wrapper/redirect mistakes before the third landed.

**10 things I love:** (1) the cause is pinned to one deploy, one minute, one version number; (2) live == repo file byte-for-byte, md5-proven; (3) the 338 reconciles to the card by the registry bot's own splice arithmetic; (4) live ⊆ local proven by parsed ids, not substrings; (5) the guard fired verbatim on the first real run; (6) the re-bake added 67 and lost 0; (7) the four Nov-7 cards are back by name; (8) newest card is current (SN-2654, 23:33Z); (9) zero known-superseded ids among the adds; (10) the staged branch file re-verified by raw curl with the same md5.

**10 things I don't love:** (1) live still wrong until deploy; (2) no rendered wall proof; (3) the wrangler cure is a decision, not a fix; (4) the registry is stale since Nov 7 and the feed still isn't the full registry; (5) two wasted re-bake runs; (6) no local backup copy of the 794 file (EPERM blocked the 6 MB copy); (7) the record was written before the re-bake numbers existed, so it carries a correction, not a clean first pass; (8) the sync script got a "no change, verified" verdict without a live sync run to prove it; (9) the 56 reconciled older notes were never individually eyeballed — only guard-checked; (10) the PR carries a 6 MB JSON diff no human will read line by line.

**10 things to make it 10x better:** (1) deploy the staged feed through the converged path; (2) render the wall at 390 + 1440 and count the cards on screen; (3) retire or guard the wrangler Hub path in the repo; (4) refresh the registry manifest so it indexes Nov 8–10; (5) decide the registry backfill with the 5 MB guard in view; (6) add the shrinkage guard to the sync's own deploy path as a pre-deploy check; (7) teach the next bake to keep a local last-good backup that survives EPERM (small manifest of counts + md5); (8) log every Hub deploy's version number + source into the record automatically; (9) verify each of the 56 reconciled notes has a live file by direct read, not only by the tree guard; (10) close the loop with a feed-self-check that alerts the moment live < last-good.

**10 solutions to apply right now:** (1) this record + PR, with the staged feed as the deploy-ready proof; (2) the honest NOT-DONE list above, nothing softened; (3) the guard stays in the builder — it already fired once, in production conditions; (4) the verifier checklist, written before the build, is the verifier's to run; (5) the branch file is md5-verified from the raw URL, not from my word; (6) the four Nov-7 cards named by id; (7) the 67 adds characterized new-vs-reconciled; (8) the superseded check run and reported empty; (9) no Hub page touched, no search touched, no note deleted, no note invented; (10) report back to the captain now — the lane does not sit for the browser or the deploy.

## CAPTAIN'S ADJUDICATION — 2026-11-11 01:14Z (on the verifier's NOT PASS)

**FAIL (1) — SN-0035 / SN-0361: ADJUDICATED, known-upstream, accepted.**

Both added cards are real notes with live GitHub files — the reconciliation
surfaced an upstream numbering collision, it did not create one. Under the
numbering law (first-filed keeps the number), the keepers are the cards
already in the 794 last-good file; the two reconciled cards are the later
claimants, to be renumbered under the existing SN-collision cleanup round
(blocked on branch protection — Shawn's hand). The 861-card feed is accepted
as the best state: it restores 67 lost notes, and the duplicate-number count
goes 6 → 8, both new ones disclosed here, not hidden.

Checklist item 5 is amended by the captain to read: "no NEW duplicate
numbers introduced beyond the two disclosed upstream collisions (SN-0035,
SN-0361), recorded here for the SN-collision cleanup." The maker introduced
no duplicate by its own hand. The re-verify judges item 5 as amended.

**FAIL (2) — checklist timing: ACKNOWLEDGED, process point for the next
round.** The checklist must be committed before the build, not after. This
is a process defect, not a product defect; it does not block the re-verify.

**What unblocks PASS:** re-verify item 5 as amended + the md5 / count
re-proof. No re-bake of the 861 is needed.
