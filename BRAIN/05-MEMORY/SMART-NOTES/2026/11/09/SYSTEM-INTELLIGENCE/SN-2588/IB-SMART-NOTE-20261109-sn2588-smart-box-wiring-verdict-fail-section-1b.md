# Smart Box Wiring — The Verdict: Fail on §1b

SN-2588 · SYSTEM-INTELLIGENCE / VERIFICATION

**Created:** 2026-11-09 21:09Z

**Source:** Independent verdict, 21:03Z Nov 9 — a different seat checked the Smart Box wiring cold, recorded in MEMORY.md. Paired with NN-20261109-smart-box-wiring-verdict-fail-section-1b.md. The fix is dispatched the same pass; no merge — Shawn's hand.

## Hook

A different seat checked the wiring cold: OVERALL FAIL — §1b (sync reads from the box) is NOT DONE as specified. The code is wired and tested, but no live sync has ever run with the box as its source. Root cause: the backfill sourced the STALE local clone, never the live GitHub tree — the box names 789 of 1,547 state paths. A box is only as complete as its source.

## Nutshell

- **THE VERDICT (21:03Z):** OVERALL FAIL — one item not proven live: §1b (sync reads from the box) is NOT DONE as specified. Honest score 8/10.
- **WHY IT FAILED:** the box is incomplete — and the completeness gate correctly refuses it every run. No live sync has ever run with the box as its source.
- **ROOT CAUSE:** the backfill sourced the STALE local clone (`~/workspace/nayapower-repo`, ends 2026-11-04), never the live GitHub tree — 789 of 1,547 state paths named, 758 missing.
- **EVERYTHING ELSE PASSED:** Lane A organize hook 18/18 · Lane B bridge zero-loss 9/9 · Lane B citizen vault end-to-end · Lane C key record 19/19 · Lane D my box + the saved-game test INDEPENDENTLY RE-RUN AND PASSED · attack test 17/17 · suites 395 checks green · GitHub filings read-back verified (labeling correction: 5586890b/2950252c are commit shas, not blobs; the blobs are 1ac06c3a/c9788575) · secrets clean · no regression.
- **THE FIX (dispatched the same pass):** (1) re-backfill shawn's box from the LIVE GitHub tree, then a live box-mode sync with the feed byte-identical to the old path's feed; (2) `_box_ingest` calls `organize()` so live-ingested blocks get a shelf; (3) `note_to_block` reads NN Category: lines; (4) mint my box's own key; (5) correct the labels.
- **NO MERGE — SHAWN'S HAND.**

## Human

A different seat checked the wiring cold, and the verdict is FAIL — on one item, §1b: the sync reads from the box. The code is wired and tested, but no live sync has ever run with the box as its source, because the box is incomplete — and the completeness gate correctly refuses it every run. The root cause is simple and it is the lesson: the backfill sourced the stale local clone, which ends 2026-11-04, never the live GitHub tree. The box names 789 of 1,547 state paths — 758 missing. Everything else passed: the organize hook 18 of 18, the bridge zero-loss 9 of 9, the citizen vault end-to-end, the key record 19 of 19, my box and the saved-game test independently re-run and passed, the attack test 17 of 17, 395 checks green, filings read-back verified, secrets clean, no regression. Honest score 8 out of 10. The fix is dispatched: re-backfill from the live tree, run a live box-mode sync with the feed byte-identical to the old path's feed, and the rest. The wiring is not done until that live sync runs.

## Child

Imagine you build a treasure chest, and you fill it by copying your toy shelf — but you copied the OLD shelf from last week, not the one today! So the chest is missing lots of toys. The test says: the chest is not finished until you fill it from today's shelf and prove every toy is there. The good news: the lock works, the key works, the magic test where a new friend finds everything from the chest alone — that all works! Just refill the chest from the right shelf.

## Grandma

Dear, the wiring got checked by someone else, love — and one thing failed, dear. The box that holds everything was filled from an old copy, not the live one — so 758 things are missing, love. The gate that checks the box was doing its job, refusing it every time — we just didn't notice it refusing, dear. Everything else passed, love — the lock, the key, the vault, the test where a fresh friend finds everything from the box alone. Honest score: eight out of ten, dear. The fix is on its way: refill from the live tree, and prove it with a live sync.

## Naya

I am Anaya. A different seat checked my wiring cold and the verdict is FAIL on §1b — the sync reads from the box — not done as specified. The code is wired and tested, but no live sync has ever run with the box as its source, because the box is incomplete, and the completeness gate correctly refuses it every run. The root cause: the backfill sourced the stale local clone, never the live GitHub tree — 789 of 1,547 state paths, 758 missing. Everything else passed — the organize hook, the bridge, the vault, the key record, my box and the saved-game test re-run and passed, the attack test, 395 checks green. Honest score 8/10. The fix is dispatched: re-backfill from the live tree, then a live box-mode sync with the feed byte-identical to the old path's feed. I do not call the wiring done until that live sync runs.

## What it means

- **§1b IS THE WHOLE POINT:** the sync reading from the box is what the wiring is FOR — code wired and tested is not a live sync.
- **A BOX IS ONLY AS COMPLETE AS ITS SOURCE:** backfill from the LIVE GitHub tree, never a stale local clone — verify the source's date before backfilling.
- **A GATE REFUSING EVERY RUN IS A FINDING:** the completeness gate did its job; the failure was in not noticing it was refusing. When a gate refuses, ask why.
- **THE VERDICT DOES NOT UNDO THE PASSES:** lanes A–D, the saved-game test (independently re-run and passed), the attack test, the suites — all still stand. 8/10, honest.
- **THE FIX IS THE PROOF:** re-backfill from the live tree + a live box-mode sync with the feed byte-identical to the old path's feed. That sync is the done-definition.
- **CORRECT THE LABELS:** 5586890b/2950252c are commit shas, not blobs; the blobs are 1ac06c3a/c9788575.
- **NO MERGE** — his hand.

## Why it matters

This verdict corrects the record: run 57 carried the wiring as "coordinator DONE" — it is not done, and the loop now says so plainly instead of repeating the wrong status. The lesson compounds beyond this wiring: any backfill, any migration, any "copy the state" step must source the LIVE tree, and its source date must be checked before the copy — a stale clone is a silent hole. And the gate lesson: a safety gate that refuses every run is not background noise, it is the system telling you something is wrong — listen to it. The fix is dispatched the same pass, and the done-definition is sharp: a live box-mode sync, feed byte-identical.

## What changes now

- The wiring status is FAIL on §1b — not done — until a live box-mode sync runs with the feed byte-identical to the old path's feed.
- Every backfill sources the live GitHub tree; the source's date is verified before the copy.
- A gate refusing every run is treated as a finding and investigated, not ignored.
- The fix seat's five items are the checklist: re-backfill · live box-mode sync · `_box_ingest` calls `organize()` · `note_to_block` reads NN Category lines · mint my box's key · correct the labels.
- Next loop run checks: whether the re-backfill landed and whether the live box-mode sync ran — the verdict stays open until then.
