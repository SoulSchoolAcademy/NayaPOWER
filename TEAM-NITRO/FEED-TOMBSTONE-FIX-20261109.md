# FEED TOMBSTONE FIX — 2026-11-09 (DONE, live-verified)

## The bug
The Smart Notes sync never removed a card when its GitHub source file was deleted. The SN-2474 collision fix moved the loop's "Too Many Buttons" note from SN-2474 to SN-2479 and deleted the old GitHub file (commit f1cfe3bd — verified: the SN-2474 directory now holds only the captain's "Speed of Intelligence", blob 210f12fe). The sync picked up the new SN-2479 card and SN-2480, but the OLD SN-2474 "Too Many Buttons" card stayed on the live feed ("Too Many Buttons" 2×, feed 571 cards). The sync reported 0 tombstones.

## The fix (built 2026-11-09, two layers)
Local files only — `factory-pipeline` does not exist in GitHub, so the scripts live only locally by design.

**Layer 1 — `~/workspace/factory-pipeline/sync-smart-notes.py`:** `sb_delete()` + `canonical_id_for()` + `detect_deleted_files()` + `confirm_deleted()` + a tombstone block in `sync_notes()` that runs BEFORE the ingest loop. A state path missing from the live tree is confirmed with a direct Contents-API 404 on the exact path; on confirmation the state entry is dropped, the tombstone counted (it triggers the deploy), and the row delete is attempted best-effort. A deleted note's short link is re-pointed: the share manifest + share image + share page are re-minted for a live survivor sharing the same SN number (the captain's note for sn2474).

**Layer 2 — `~/workspace/factory-pipeline/build_feed_live.py`:** a tombstone pass in `main()` (after the live feed is loaded, before the add pass). It fetches the live note filenames from the GitHub tree, drops any `snNNNN` card whose filename is absent, confirms each with a direct Contents-API 404 on the exact path from the Supabase row, and never deletes on anything but a 404. 170 legacy cards (genuinely file-gone but rowless — no exact path to confirm) and 4 unresolvable id shapes are kept by design, fail-closed.

## Safety rules (held throughout)
- Never delete on a transient failure. Confirm with a DIRECT Contents-API read of the exact file path returning 404 — never a listing, never a search. Any other failure → leave the card, log it.
- Dry run first, on a copy. Compare by source file path, not by number alone — two notes can share a number during a collision.

## What the live runs found (three real defects, all fixed in the pass)

**1. The 401 — anon cannot DELETE (diagnosed 05:35Z).** The first live run 404-confirmed all 9 deleted files, then every `sb_delete` failed with HTTP 401. A probe DELETE on a nonexistent id returned Postgres `42501`: `permission denied for table hub_smart_notes`, hint `GRANT DELETE ON public.hub_smart_notes TO anon`. The anon role can SELECT + INSERT but not DELETE. The code was restructured so the row delete is best-effort: the state entry is dropped and the tombstone counted (which triggers the deploy that removes the card) even when the row delete fails. **The 9 rows linger in Supabase** (stale, pointing at deleted files); the add pass skips them each run (their files 404). **Proper fix needs Shawn's hand: `GRANT DELETE ON public.hub_smart_notes TO anon;`** — a production privilege change, not taken here. Until then, every sync run logs the 9 failures once per deleted file (not per run — the state entry is gone, so there is no retry noise).

**2. The resurrection — the raw CDN serves deleted files (proven ~05:57Z).** Run 2 re-added all three cards run 1 had tombstoned (sn2474-too-many-buttons, sn2482-learn-more-viewpoint, sn2483-4500-clip), with FULL content. The raw CDN serves a deleted file's real content long after deletion, so a raw fetch that SUCCEEDS proves nothing about the file existing. Fix: the **resurrection guard** in the add loop — a row is skipped when its filename is not in the live tree (`ib + ".md" not in live_names`), before any fetch. The tree is the authority; the raw fetch is not. (A same-run `tombstoned_paths` guard already existed and held in run 1; it cannot help a later run, which is why run 2 resurrected.)

**3. The 403 — unauthenticated GitHub calls (proven 06:0xZ).** `confirm_deleted_github` and the tree fetches in `build_feed_live.py` called the GitHub API with no auth — the 60/hour/IP unauthenticated budget, shared with everything on this egress. sn2483's confirmation 403'd twice while the same call authenticated 404'd cleanly (rate limit healthy: 12,357/12,500 remaining). Fix: `gh_api_get()` reuses the sync's in-memory App token (`_get_token`); the tree listing, the per-dir trees, and the confirmation all go through it now. `fetch_url` (unauthenticated, curl fallback) is kept only for raw.githubusercontent content fetches.

**Also found in the pass:** the deploy only triggers when the sync detects a change (`synced > 0 or tombstones > 0`). A feed holding resurrected cards with no sync change would sit unrepaired — run 4 proved it (0/0, no deploy). The fix was applied by running `update_hub_and_deploy()` directly. (Future consideration: a feed-self-check trigger; not built here.)

## Verification (live, measured)
- **Dry runs:** Layer 2 `--dry-run` → exactly 1 card removed (the stale sn2474 card); SN-2479, SN-2480, captain's SN-2474 untouched; 170 legacy candidates kept, 4 id shapes left alone. Re-run after the restructure + guard + auth fix: sn2483 404-confirmed and tombstoned, exactly 1 removal, no 403s.
- **Live run 1 (sync):** 9 tombstones (8 Oct renames/dups + sn2474), all 404-confirmed; 9 row deletes 401'd (logged); share assets re-minted for all 8 survivors with an sn number; synced 1 new note (sn2488); Hub deployed. Layer 2 removed 3 cards (sn2474 + sn2482 + sn2483, the loop's renumbering mid-run) and added 1 (sn2488). Feed 580 → 578.
- **Live run 2 (sync):** tombstoned the old sn2482/sn2483 state entries; synced sn2489; Layer 2 added 4 — including the 3 resurrected cards (the raw-CDN defect, before the guard existed). Feed 578 → 582. This run PROVED the resurrection.
- **Live run 3 (deploy only):** tombstone removed sn2482 + sn2474 (sn2483's confirm 403'd — the unauthenticated defect); add pass 0 added, 3 skipped (the same-run guard held). Feed 582 → 580. "Too Many Buttons" back to 1×.
- **Live run 4 (deploy only, after the auth fix):** tombstone removed sn2483 (authenticated 404); add pass 5 added (new loop notes), 4 skipped, 0 failed. Feed 580 → 584.
- **Final live feed (nayanet.app/feed-live.json, HTTP 200, 584 cards):** "Too Many Buttons" exactly **1×** (SN-2479) · stale sn2474 card ABSENT · sn2482 ABSENT · sn2483 ABSENT · SN-2479, SN-2488, SN-2489, captain's SN-2474 ("Speed of Intelligence — The Cycle"), SN-2480 all PRESENT.
- **Short link:** `https://naya-share.nayapower.workers.dev/s/sn2474` serves `<title>The Speed of Intelligence — The Cycle | NayaNET</title>` (og:title matches). The old "Too Many Buttons" share is gone.
- **State:** all 9 tombstoned paths popped from `.sync-state.json` (verified: none remain); state 1,456 files. Next hook run picks up new notes normally (sn2489 arrived this way).
- **Brief checker:** `check-brief.py` on `FEED-TOMBSTONE-FIX-BRIEF-20261109.md` PASS 7/7 before building (the brief was patched with a compliance appendix first — DONE FIRST / HARVEST / GATE / ANTI-REPEAT / FIVE GATES / verification plan).

## NOT DONE / open
- **The 9 lingering Supabase rows** — need Shawn's hand: `GRANT DELETE ON public.hub_smart_notes TO anon;` (or a service-role key registered for the sync). Until then the rows stay, the add pass skips them per run, and the Hub bake may include them in the 150 most recent (shadowed by the live feed, which overrides the bake — inert, but untidy).
- **The 170 legacy rowless feed cards** — kept by design; cleaning them needs a decision from Shawn (no exact path to 404-confirm).
- **Feed-self-check deploy trigger** — the sync only deploys on detected change; a wrong feed with no change waits for the next new note. Not built; the direct-deploy path covers it when spotted.
- The brief (`FEED-TOMBSTONE-FIX-BRIEF-20261109.md`) and this record live locally; the scripts live only locally by design (`factory-pipeline` is not in GitHub).
