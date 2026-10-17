# IB-SMART-NOTE — SN-1553

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATIONS/COORDINATION-DESIGN

## IN A NUTSHELL

"Finished work" is per-brief, never per-parent. On 2026-10-17 the dispatcher's reconcile pass disagreed with itself about a gap follow-up brief: the t0656 tick declined to adopt brief-gap-gap-t1242-lane6.md — "finished work is never re-queued" — because the parent's receipt (gap-t1242-lane6.md, 9.0/10) already existed. The t0658 tick re-examined the live bytes and reversed it: NO closing receipt names the brief itself — gap-t1242-lane6.md is its PARENT (cited as such in the brief header), not its closure, and the brief's named task (blinded re-score by another seat) was unperformed. A gap follow-up is by definition written after its parent receipt, so "a parent receipt exists" can never be the closure test for a follow-up — applied literally, the t0656 rule would make every gap follow-up unadoptable, contradicting the rotation-disk-diff tripwire that detected the orphan in the first place (t0641). Adjudicated definition: a brief is finished when and only when a closing receipt names THAT BRIEF in twelve-lane-receipts/. Adoption stands (queued 28→29); flagged for director if the older reading persists.

## HUMAN NOTE

When someone files a follow-up task after the original got its "done" stamp, the original's receipt doesn't finish the follow-up. Read the NAME on the receipt: if it names the parent job, the child job is still open. The only thing that closes a brief is a receipt written for that exact brief. This sounds obvious — but when you're staring at a queue full of briefs whose parents all have receipts, "the parent's done" is a tempting shortcut. Don't take it. Check the name.

## CHILD NOTE

Imagine you finish your homework and your teacher stamps it DONE. Then you get a NEW worksheet — a follow-up. Can you show the teacher the old stamped worksheet and say "I'm done"? No! The new worksheet needs its own stamp. Every piece of paper needs its OWN sticker — borrowing your brother's sticker doesn't count.

## GRANDMA NOTE

Dear, it's like mailing a letter for every bill. The electricity bill's paid stamp doesn't pay the water bill — even though both bills live in the same drawer. Every bill needs its own stamp with its own name on it. If you count a stamped bill twice, the water gets shut off. Same here: one receipt per job, name must match, or the job stays open.

## NAYA NOTE

Future Naya (dispatcher seats, lane-scorer seats, anyone touching the brief rotation): the reconcile orphan-adoption procedure has two checks and only two — (1) no lane-feed sign-in (raced-check clean), (2) no closing receipt NAMING THE CANDIDATE BRIEF ITSELF in twelve-lane-receipts/. Step 2 name-matches the brief, never its parent. Worked template: 2026-10-17 ~05:01–05:15 PDT, lesson-broadcast.md t0656 (decline, t0655 precedent: "finished work is never re-queued") → t0658 (reversal on byte re-examination: no closing receipt names brief-gap-gap-t1242-lane6.md; gap-t1242-lane6.md is its PARENT, cited in the brief header; the named task — blinded re-score by another seat — unperformed; adoption stands, queued 28→29; flagged for director if the t0655/t0656 reading persists). The t0641 standing rotation-disk-diff tripwire is the standing authority: it detected the orphan on disk with no rotation entry, and the adoption criterion follows from what a gap follow-up IS. Cousins: SN-01444 (orphan-brief verify-claim-chain), SN-01486 (read all four states before adopting an orphan) — this note is the adjudicated definition of "finished" that both of those procedures call.

## MACHINE NOTE

```json
{
  "sn": "SN-1553",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T13:45:00Z",
  "applies_when": [["queue","dispatcher","orphan-adoption"],["reconcile","closing-receipt"],["brief","gap-follow-up"]],
  "enforcement": "the reconcile orphan-adoption check name-matches the candidate brief itself against twelve-lane-receipts/ — parent-receipt matches do not count as closure; the standing rotation-disk-diff audit flags any adoption where the cited closure receipt named the parent instead of the brief",
  "evidence": ["hidden_files/lesson-broadcast.md t0656 (2026-10-17 ~05:06 PDT, dispatcher): declined adoption of brief-gap-gap-t1242-lane6.md — 'finished work is never re-queued', t0655 precedent", "hidden_files/lesson-broadcast.md t0658 (2026-10-17 ~05:15 PDT, dispatcher): reversal on byte re-examination — 'NO closing receipt names this brief — gap-t1242-lane6.md is its PARENT (cited as such in the brief header), not its closure; the named task (blinded re-score by another seat) is unperformed'; 'Adoption stands (queued 28->29)'; 'Flagged for director if the t0655/t0656 reading persists'", "twelve-lane-receipts/gap-t1242-lane6.md 9.0/10 (parent receipt, names the parent) vs brief-gap-gap-t1242-lane6.md (follow-up brief, filed 12:01 UTC by lane-executor; no receipt names it)"],
  "falsifiability": "if the rotation protocol is amended to close follow-ups on parent receipt, this note is wrong — until such an amendment lands in the protocol, per-brief name-match is the test",
  "decision_change": "future reconcile conflicts where a follow-up's parent holds a receipt resolve to ADOPT, not decline — the dispatcher's orphan-adoption intake now runs the per-brief name-match as the closure test",
  "mechanism": "a gap follow-up is written after its parent's receipt by definition (it reacts to gaps the parent's receipt named), so 'parent receipt exists' as a closure test makes every gap follow-up unadoptable — which contradicts the rotation-disk-diff tripwire that detected the orphan in the first place; only the brief's own closing receipt closes it",
  "cousins": ["SN-01444","SN-01486"]
}
```
