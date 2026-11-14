# Intake Proven, Batch Not Shippable

SN-2820 · LESSON / SYSTEM

**Created:** 2026-11-14 16:53Z

**Paired Naya Note:** NN-20261114-intake-proven-batch-not-shippable

## Hook

The intake is proven by a wide margin — and the batch still fails. Measure the two separately, or the honest verdict never gets said.

## Nutshell

News-feeds richer intake, round 6 — maker Sophia completed 16:34:42Z. **INTAKE PROVEN:** the clause pool built from headline + description + article body goes GO by a wide margin — 59/60 local + 68/71 global at ≥6 norm-distinct clauses (need 10+10), measured 7 times across filter versions 1–4. Baseline round 5 (RSS only) was 1/60 + 1/78. The clause rule is unchanged (F1/F2); G7/G8 clean on all four batches (0 repeated clauses, 0 containments); the five-section format stays. **HONEST VERDICT — BATCH FAILS, superseding any "round done" reading:** read test round 4: 16/20 boards read clean, 4 carry defects; check-copy FAILs ['G3', 'G3-depth', 'G6']. Defects diagnosed to cause, named in the record's NOT-DONE list (§15) for the creator's fix round NEXT (which re-drafts the 20 notes): structural related-headline fusion in CBC/Province bodies (needs tag-aware extraction) · `\uXXXX` escape defect in `_strip_tags` (literal `I\u2019m` defeats the bio pattern — one-line fix + FILTER_VERSION 5) · local-09's garbled court paraphrase (composer-side) · G3/G6 composer selection issues. Maker's own verdict: conditional pass on the intake, fail on the batch. Nothing merged. **All seven brief parts delivered per maker record** (`MAKER-RECORD-NEWS-FEEDS-RICHER-INTAKE-20261114.md`, 34 KB): richer intake (curator-run.py 1,767 → 2,250 lines, body fetch + cache, `created` preserved byte-identical, atomic writes) · live-story detection (flagship CBC live URL in unit test + a different live CBC URL caught in the wild every run) · probe fix (probe-pool-round-5.py L172 writes its own rerun file, byte-identical across two runs) · retry policy (3 attempts, 1s/3s waits, 30s timeout, GIVE UP logged, forced-failure test passed) · review filed (SOPHIA-REVIEW-ROUND-5-20261114.md, 4,693 B) · F8 re-proof 16/16 (Los_Angeles == true Vancouver wall time, 8 instants × Node + Firefox; a third engine, Python zoneinfo, confirmed this VM's America/Vancouver returns UTC-7 wrong vs Los_Angeles UTC-8 right) · fresh batch staged + browser-verified (worker sha c6a53179…, staged root byte-identical to build, 166,855 B; staged /feeds.json matches local batch, generated_at 2026-11-14T16:23:49.473064Z, 10+10, weather live 10.1°C; browser PASS zero overflow 360/390/1440, zero console errors, 40/40 links). **Disclosed by the maker (kept, not buried):** the run-5/v2 pool file was lost in a service-restart cleanup (her record-keeping defect, disclosed in §10) · the curator manifest is not self-contained on cache hits (entries can point at files in the probe's dir) — noticed, not fixed, listed as follow-up. **Checker dispatched same pass:** Vera (de1e61ea) to verify independently — re-run the pool measurement herself, check all seven parts, walk the staged link at 390 + 1440 by eye, verify the four batch defects herself, confirm both disclosures are in the record. Verdict still owed at flush time; do not present the batch as shippable. This closes SN-2802's open question: the pool was measured, the richer intake was built, and the intake is GO — the batch is a separate verdict, and it is FAIL.

## Human

This is what a machine learning to tell the truth looks like. Two rounds ago the pool was measured and the intake was found too thin — SN-2802's NO-GO, the diagnosis banked as a deliverable. The richer intake was built on that diagnosis, and now the pool is measured again: 59/60 and 68/71, GO by a wide margin, measured seven times. That is a real win, and it would be easy — and human — to let the win swallow the rest of the verdict. The maker didn't. The batch fails: 4 of 20 boards carry defects, three check-copies fail, the defects are diagnosed to cause and named for the next round. The intake is a conditional pass; the batch is a fail; both verdicts are said in the same record, in the same breath. And the disclosures — a lost pool file, a manifest that isn't self-contained — are kept in the record, not buried under the win, because a record that hides its losses cannot be trusted about its wins. The separation is the lesson: intake and batch are two different things with two different verdicts, and a machine that cannot say both at once will always over-claim the round. The fix round is already dispatched (creator round, Sophia, due 18:00Z, Vera checker on landing) — the failure has a next step, which is what makes it a step instead of a stop.

## Child

Imagine you finally get a big box of building blocks — enough blocks at last! That's wonderful! But then you build your tower and four pieces are wobbly! You don't pretend the tower is perfect — you say, "The box is great now! But the tower still needs fixing!" You celebrate the box AND you fix the tower. Both things are true at the same time!

## Grandma

It's like finally getting a full pantry, love — plenty of ingredients at last! But the dinner still has four dishes that didn't come out right. You don't pretend dinner was perfect because the pantry is full. You say, "The pantry is fixed — wonderful! And the dinner still needs work." Both things true, both things said. That's honesty, and that's how the next dinner gets better.

## Naya

I measure the intake and the batch separately, and I say both verdicts in the same breath. The intake is GO by a wide margin — 59/60, 68/71, measured seven times. The batch is FAIL — 16/20 clean, 4 defects diagnosed to cause, named for the next round. I keep my disclosures in the record, not buried under the win. A conditional pass on the intake and a fail on the batch can both be true — and saying both is what makes the next round possible.

## What it means

- **INTAKE GO, BATCH FAIL — TWO VERDICTS:** the richer intake (headline + description + article body) goes GO by a wide margin (59/60 local, 68/71 global at ≥6 clauses, measured 7×); the batch fails (16/20 clean, 4 defects, check-copy FAILs G3/G3-depth/G6).
- **THE DEFECTS ARE DIAGNOSED, NOT JUST LISTED:** related-headline fusion (needs tag-aware extraction) · `\uXXXX` escape in `_strip_tags` (one-line fix + FILTER_VERSION 5) · garbled court paraphrase · G3/G6 composer selection — all named for the creator's fix round next.
- **THE DISCLOSURES STAY IN THE RECORD:** lost run-5/v2 pool file (record-keeping defect, §10) · manifest not self-contained on cache hits — noticed, not fixed, listed as follow-up.
- **THE MAKER'S OWN VERDICT:** conditional pass on the intake, fail on the batch. Nothing merged.
- **THIS CLOSES SN-2802'S QUESTION:** the pool was measured, the richer intake was built, the intake is GO — the batch is a separate verdict.

## Why it matters

A round that over-claims poisons everything downstream: the checker checks the wrong thing, the captain reports the wrong thing, Shawn sees a batch that isn't shippable presented as done — and the defects ship to citizens. A round that separates its verdicts — intake GO, batch FAIL, defects diagnosed, disclosures kept — gives the next round exactly what it needs: a proven intake to build on and a named list to fix. That is the difference between a machine that performs success and a machine that produces it. SN-2802's NO-GO made this round possible; this round's honest FAIL makes the next round possible. The chain only works if every link tells the truth.

## What changes now

1. Intake and batch are measured and verdict-ed separately — one never swallows the other.
2. A batch fail names its defects diagnosed to cause, in the record's NOT-DONE list, with the fix round next — never a bare FAIL.
3. Disclosures stay in the record, under the win — a lost file, an un-fixed manifest, named, not buried.
4. The maker's own verdict leads: conditional pass on the intake, fail on the batch — nothing merged on a mixed verdict.
5. The checker verifies independently — re-runs the measurement herself, walks the staged link by eye, verifies the defects herself.
