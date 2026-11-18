# File the Same Day — The Backlog Re-Forms Overnight

SN-3308 · OPERATIONS — THE FILING LOOP

**Filed:** Intelligence Loop filing push #2 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3284; filed as SN-3308 renumbered from provisional SN-3274.

**Created:** 2026-11-18 03:14Z (filing push COMPLETE — recorded in the daily log; drafted in run 293)

**Paired Naya Note:** NN-20261118-file-the-same-day-the-backlog-re-forms

## Hook

The filing push finished: 165 pairs filed, every one verified in-tree by blob sha, queue 165 → 0. And the queue had already refilled — runs 291–292, 22 pairs, not in this push. Filing has to keep up the same day, or the backlog re-forms.

## Nutshell

**THE PUSH COMPLETE, 03:14:30Z:** coordinator beddc203 COMPLETE. 165 pairs filed, every one verified in-tree by blob sha. Queue at start 165, at end 0. Chunks: (1) 25 renumbered SN-3225–3249; (2) 24 renumbered SN-3251–3267 + kept SN-3103–3109; (3) 25 kept SN-3110–3134; (4) 25 kept SN-3135–3159; (5) 25 kept SN-3160–3183; (6) 25 kept SN-3184–3208; (7) 15 kept SN-3209–3223. Renumbering: 43 collision pairs renumbered to SN-3225–3267; 122 free pairs kept provisional numbers; SN-3070 never filed (no draft carried it). **THE SN-3161 DUPLICATE RESOLVED:** run 280's train-the-army KEEPS SN-3161 (ORDER, blob ed68227b); run 281's on-top-of-things moved to SN-3269 (OPERATIONS, blob f23bf76e); the old OPERATIONS/SN-3161 file deleted (GET now 404). Proof the wall is down: `next-sn-number.py` exits 0, highest SN in use SN-3269 at that moment, next free SN-3270. **THE LESSON, STANDING:** filing has to keep up the same day, or the backlog re-forms — the queue already refilled with runs 291–292 (22 pairs), and the driver hardcodes `range(242, 291)`, so the next push needs it extended to 293. **THE LIVE CAVEAT, DELIVERED TO SHAWN WITH THE COUNT:** filed in GitHub + recorded for sync — NOT live on nayanet.app until the publication repair lands; do not claim any note live. **OPEN ITEMS, NAMED EXACTLY:** (1) organize hook + build_index.py STILL BLOCKED by the EPERM flake — five attempts, all Operation not permitted; INDEX.md is 0 bytes (regenerates deterministically from store/entries.jsonl — generation proved, 1,706,075 bytes, 2,087 entries); watermark intact. (2) The queue already refilled — runs 291–292, 22 pairs, not in this push.

## Human

One hundred and sixty-five pairs is a day of teaching that was sitting in drafts, not in the system — captured and distilled, but not yet working in the live system, which is exactly the gap Shawn named at 01:50Z when he said the loop must close. The push closed it: every pair verified in-tree by blob sha, the SN-3161 collision resolved with one keeper and one move, the numbering command working again. And before the ink was dry the queue had refilled, because the loop keeps drafting faster than the filing keeps up. That is the lesson, and it is a standing one: filing is not a weekly chore, it is the same day's work, or the backlog re-forms overnight and the loop is open again. Filed in GitHub is also not live on the Hub — the publication repair still stands between the tree and nayanet.app, and no note is claimed live until that repair lands.

## Child

Imagine you write down everything you learn in a day — 165 important things — but they sit in a pile on your desk instead of in your notebook. The filing push put every single one into the notebook, and checked each one is really there. But the next day you learn 22 more things, and the pile starts again. So you have to file every day, the same day, or the pile comes back. And putting it in the notebook isn't the same as putting it on the wall for everyone to see — that step still needs fixing.

## Grandma

Dear, the filing push finished, dear — 165 notes filed, every one checked and in its place, and that tangled duplicate number is all sorted out now. But the pile is already growing again, dear, because we keep learning new things every day. So the filing has to happen the same day, dear, or the pile just comes back overnight. And filed in the book isn't the same as live on the wall for everyone to see — that part still needs its fix, and we don't pretend it's done until it is.

## Naya

FILE THE SAME DAY — OR THE BACKLOG RE-FORMS OVERNIGHT. 165 PAIRS FILED, QUEUE ZERO, AND ALREADY REFILLING. FILED IN GITHUB IS NOT LIVE ON THE HUB.

## What it means

- **THE PUSH:** 165 pairs filed, blob-sha verified, queue 165 → 0 (coordinator beddc203, COMPLETE 03:14:30Z).
- **THE RESOLUTION:** SN-3161 duplicate resolved — train-the-army keeps SN-3161, on-top-of-things moved to SN-3269, old file deleted, numbering command works again.
- **THE LESSON:** filing has to keep up the same day, or the backlog re-forms — runs 291–292 already refilled it with 22 pairs, and this run adds 7 more (SN-3272–3278).
- **NUMBERING STATE, THIS RUN:** live max moved during the run — the distillation threshold batch filed SN-3270 ("The Morning List Is the Whole System") and SN-3271 ("The Whole Runs on the Law") mid-run, and has assigned provisional SN-3272–3283 to its G3–G14 composition (in flight). This run's SN-3272–3278 are provisional per `next-sn-number.py` (live max SN-3271 at run time); the filing push must renumber runs 291–293 against the fresh tree max at filing time — run 291's "renumber from SN-3270" plan is stale, SN-3270/3271 are now taken.
- **THE CAVEAT:** filed in GitHub is NOT live on nayanet.app until the publication repair lands — do not claim any note live.
- **THE OPEN ITEMS:** organize hook + build_index still EPERM-blocked (INDEX.md 0 bytes, regenerates deterministically); the next push's driver range must extend to 293.

## Why it matters

Without this note, the machine files in bursts and drifts in between — a day of teaching sits in drafts, the loop stays open, and Shawn's "the loop must close" stays a wish instead of a state. With it, the rule is mechanical: file the same day, every day, and the queue never re-forms. And the live caveat keeps the claim honest: filed is filed, live is live, and the two are not the same until the publication repair proves them the same on nayanet.app itself.

## What changes now

1. Filing runs the same day as drafting — the queue is worked to zero daily, never left to re-form.
2. The next filing push extends its driver range to cover runs 291–293 (and renumbers against the fresh tree max — run 291's "renumber from SN-3270" plan is stale; SN-3270/3271 are now taken).
3. No note is claimed live on nayanet.app until the publication repair lands and a fresh fetch proves it.
4. The organize hook + index rebuild recovery runs when the EPERM flake clears — build_index first, then the hook — never a blind retry into the flake.
5. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.
