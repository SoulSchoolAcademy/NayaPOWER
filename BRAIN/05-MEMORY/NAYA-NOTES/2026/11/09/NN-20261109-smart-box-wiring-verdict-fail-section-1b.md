# Smart Box Wiring — The Verdict: Fail on §1b

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET**

**NN-20261109-smart-box-wiring-verdict-fail-section-1b · Naya Note · 2026-11-09 21:03Z**

**Category:** System — Smart Box / Verification

## What it is

An independent verdict, 21:03Z Nov 9 — a different seat checked the Smart Box wiring cold, recorded in MEMORY.md:

- **OVERALL FAIL — one item not proven live: §1b (sync reads from the box) is NOT DONE as specified.** The code is wired and tested, but no live sync has ever run with the box as its source, because the box is incomplete — and the completeness gate correctly refuses it every run.
- **Root cause:** the backfill sourced the STALE local clone (`~/workspace/nayapower-repo`, ends 2026-11-04), never the live GitHub tree — the box names 789 of 1,547 state paths (758 missing).
- **Everything else PASSED:** Lane A organize hook (18/18) · Lane B bridge zero-loss 9/9 · Lane B citizen vault end-to-end · Lane C key record 19/19 · Lane D my box + the saved-game test INDEPENDENTLY RE-RUN AND PASSED (a fresh agent recovered everything from the box alone) · attack test 17/17 · suites 395 checks green · GitHub filings read-back verified (one labeling correction: 5586890b/2950252c are commit shas, not blobs; the blobs are 1ac06c3a/c9788575) · secrets clean · no regression. Honest score 8/10.
- **What's owed (the fix, dispatched the same pass):** (1) re-backfill shawn's box from the LIVE GitHub tree, then a live box-mode sync with the feed byte-identical to the old path's feed; (2) `_box_ingest` calls `organize()` so live-ingested blocks get a shelf; (3) `note_to_block` reads NN Category: lines; (4) mint my box's own key; (5) correct the labels. No merge — Shawn's hand.

## Why it matters

The wiring was carried as "DONE" — it is not. §1b is the whole point of the wiring (the sync reads from the box), and it was never proven live because the box was built from a stale clone. The lesson is the root cause: a box is only as complete as its source — backfill from the live tree, never a stale clone. The completeness gate did its job by refusing an incomplete box every run; the failure was in not noticing the gate was refusing. The saved-game test still passed, the lanes still passed — the system is 8/10, honest — and the fix is dispatched.

## How to use it

- Do not call the wiring done until a live box-mode sync runs with the feed byte-identical to the old path's feed.
- Backfill from the LIVE GitHub tree, never a stale local clone — verify the source's date before backfilling.
- When a gate refuses every run, ask why — a gate refusing is a finding, not a routine.
- The fix: re-backfill from live tree + live box-mode sync + `_box_ingest` calls `organize()` + `note_to_block` reads NN Category lines + mint my box's key + correct the labels.
- No merge — Shawn's hand.

---

**Written by Naya for Shawn Vibert — Founder / Creator of NayaNET.**

*The independent wiring verdict — filed as a Naya Note under the official template — three outputs: what it is, why it matters, how to use it. Paired Smart Note: **SN-2588 — Smart Box Wiring — The Verdict: Fail on §1b**.*
