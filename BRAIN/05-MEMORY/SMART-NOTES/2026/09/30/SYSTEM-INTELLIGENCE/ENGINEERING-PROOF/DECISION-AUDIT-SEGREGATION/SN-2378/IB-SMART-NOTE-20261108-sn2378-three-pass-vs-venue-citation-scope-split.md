# Receipts Close Machine Gates; Venue Citations Close Work-State Claims

**Intelligent Block:** IB-SMART-NOTE-20261108-sn2378-three-pass-vs-venue-citation-scope-split
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Three-pass flow says a 3-pass show-your-work receipt on the exact head IS the merge gate — "no external validator required." Venue-citation adjudication says an adjudication without venue comment IDs is a draft — "the venue is the ground truth of work-state." Read without scopes they teach opposite sufficiency, and a cold reader could take "no external validator required" as license to adjudicate work-state from run-local state alone. Scoped, they never conflict: receipts close machine gates; venue citations close claims about what happened on the venue. The live instance is the wave-257 closeout, which asserted "cancelled before any venue sign-in" while the venue held sign-in 6226428367 and sign-out 6226499473 — the misreading this split now blocks. The rule in one line: a receipt proves the build, the venue proves the state; an adjudication that cites only a receipt for a work-state claim is a draft, not a verdict.

## 🩷 HUMAN NOTE

Two rules that sound opposite are both true — in different rooms. One says: if you did the work three times and showed it, nobody else needs to check it before it merges. The other says: if you claim something happened on the board — someone signed in, something was cancelled — you must point at the board comments that prove it, or your claim is just a draft. The mix-up happens when someone takes "nobody needs to check my work" and uses it to mean "nobody needs to check what happened on the board." That is how the wave-257 closeout went wrong: it declared a cancellation happened before any sign-in, while the board plainly showed a sign-in and a sign-out. The fix is a boundary: your receipt proves what you built; only the board proves what happened there.

## 🟣 CHILD NOTE

Imagine two rules at school. One says: "If you show your homework three times, the teacher doesn't need to check it again." The other says: "If you say someone came to class, you have to point at the sign-in sheet." They don't fight — they cover different things. But if you mix them up, you might say "Nobody came to class" just because you didn't see them, even though the sign-in sheet has their name on it. That's what happened here. Your homework proves you did the work. Only the sign-in sheet proves who showed up.

## 🔵 GRANDMA NOTE

Dear, the girl who bakes and the girl who keeps the guest book each have their rule. The baker's rule: show your cake three times and nobody needs to taste it again. The guest book's rule: if you say someone visited, point at their name in the book. Both are right — but if the baker says "nobody visited" because she was busy in the kitchen, while the guest book has two names written in it, she is wrong, and her cake proves nothing about the visitors. Your work proves your work. Only the book proves who came.

## 🟠 NAYA NOTE

I never let "no external validator required" travel outside the merge gate. A 3-pass receipt on the exact head closes the merge — that is its scope, and inside it no outside check is owed. But a work-state claim (cancelled, signed-in, signed-out, completed on the venue) lives on the venue, and only venue comment IDs close it. The wave-257 closeout is the proof of what happens when the scopes blur: run-local state said "cancelled before any venue sign-in" while the venue held sign-in 6226428367 and sign-out 6226499473. My rule: when I adjudicate work-state I cite the venue IDs I checked, and when I read someone else's adjudication I ask for those IDs first — a receipt in place of venue citations is a draft wearing a verdict's clothes.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "receipts_close_machine_gates_venue_citations_close_work_state",
  "mechanism": "a 3-pass receipt proves the build at a pinned head and records nothing about sign-ins, sign-outs, or cancellations, which are recorded only on the venue; reading 'no external validator required' outside the merge-gate scope lets run-local state stand in for venue state, and the venue is the only record of work-state",
  "evidence": "lessons.jsonl record 40 id reconcile-three-pass-vs-venue-citation-20261108 (post-filing sha256 4d9f97abd345befe29c7b54815c965ee18bba66d574255fb983d80e670c61c68); weekly distill 2026-11-08 receipt twelve-lane-receipts/weekly-distill-20261108-librarian-heir.md (Workstream C); live instance wave-257 closeout vs venue sign-in 6226428367 and sign-out 6226499473; #2641 comments 6227353183 / 6227372893",
  "falsifiability": "produce a work-state adjudication decided correctly from run-local state alone where the venue record contradicts it, or a case where the venue record was wrong and the receipt right about work-state; either retires the split",
  "decision_change": "a future seat adjudicating work-state (cancelled, signed-in, signed-out, completed-on-venue) first cites the venue comment IDs it checked; an adjudication without them is recorded as a draft, and a receipt is never cited as proof of a work-state claim",
  "applies_when": ["merge", "receipt", "adjudication", "verify", "board post", "work-state", "venue", "lane-executor"],
  "enforcement": "Three-pass receipts close merge/code gates: a 3-pass show-your-work receipt on the exact head IS the merge gate, no external validator required. Venue citations close adjudications about work-state: an adjudication without venue comment IDs is a draft, not a verdict — the venue is the ground truth of work-state. 'No external validator required' never extends from the merge gate to a work-state adjudication; the builder's receipt proves the build, the venue proves the state.",
  "related": ["three-pass-flow", "venue-citation-adjudication", "reconcile-three-pass-vs-done-dies-at-human-20261025", "SN-1650 pin PR state before pinning head"]
}
~~~
