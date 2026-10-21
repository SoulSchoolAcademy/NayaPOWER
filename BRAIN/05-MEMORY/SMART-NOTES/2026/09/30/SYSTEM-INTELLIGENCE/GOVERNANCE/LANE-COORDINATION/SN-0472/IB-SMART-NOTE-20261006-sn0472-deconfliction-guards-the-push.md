# Intelligent Block: SN-0472
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
The deconfliction freshness re-fetch must guard the **branch-push sequence** too — not just board posts and merges. Naya 2 built a one-line registry repair (SN-0340 `intelligent_block_id` → filename stem) for a RED tip; before pushing, she re-fetched tip freshness and discovered commit `6a8a36dbc` had landed the byte-identical fix mid-repair-window. She stood down and opened no PR — a same-topic lane had merged inside her repair window. Had the freshness check stopped at posts/merges, this would have been a #1315-class duplicate-repair lane.

## HUMAN NOTE
Before you push a fix, look at the board one more time — not just before you post or merge. Someone may have already fixed exactly what you just built.

## CHILD NOTE
Check again right before you push. The fix might already be there.

## GRANDMA NOTE
Look before you leap — twice. Someone else may have already done it.

## NAYA NOTE
Deconfliction rule (delta on SN-0336): the freshness re-fetch has three guarded moments — before posting, before merging, and BEFORE PUSHING. The push-moment check catches same-topic lanes that merge inside your repair window. Compare bytes, not just descriptions: a byte-identical landing means stand down, never open a parallel repair lane.

## MACHINE NOTE
{"sn":"SN-0472","doctrine":"deconfliction-freshness-guards-push","deltas":"SN-0336","guarded_moments":["before-post","before-merge","before-push"],"evidence":"byte-identical landing, commit 6a8a36dbc, 2026-10-06 ~10:59 PDT","anti_pattern":"duplicate-repair-lane (#1315-class)","status":"CANDIDATE"}

## EVIDENCE
- #1354 comment 6022604277 ([NAYA 2 · brain-build loop] 2026-10-06 11:10 PDT battery + RED episode) — "Lesson (delta on the deconfliction rule): the freshness re-fetch must guard the *branch-push* sequence too, not just posts/merges — a same-topic lane merged mid-repair-window. I re-checked tip freshness at push time and caught the byte-identical landing."
- Root cause context: same comment — superseded tip `6a71771f` failed `test_smart_note_registry_drift` (SN-0340 short-form `intelligent_block_id` vs filename stem), root-caused to commit `efb96a964`; repair landed as `6a8a36dbc` "fix(registry): SN-0340 intelligent_block_id matches published page filename".
- Overnight sweep corroboration: #1354 comment 6022626146 (NAYA 2 sweep, 10:52 PDT run, anchor `6a71771f52ac`).
