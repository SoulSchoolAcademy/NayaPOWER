# SUPER NOTE — The Pipeline Must Not Lose, Stall, or Waste the Work

> **The essence layer: 71 distilled Super Notes.** Raw Smart Notes live in the archive; the Hub wall shows these essences. Nothing here deletes or replaces any raw note.

| Field | Value |
|---|---|
| Super Note ID | `SUPER-069` |
| Hub wall row | `public.hub_smart_notes` ib_id `SUPER-069` |
| Human title | The Pipeline Must Not Lose, Stall, or Waste the Work |
| Layer | ESSENCE — distilled from raw Smart Notes, never a raw capture |
| Distilled | 2026-10-21 — corrective distillation drive (639 raw → 71 essences); REPAIRED 2026-10-21 after independent audit found 42 MISSING + 151 PARTIAL — lost lessons restored from the originals (see REPAIR-LOG); coverage map regenerated mechanically from these files |
| Sources | 12 raw notes (full list below) |
| Cluster file | `cluster-08-super.json` |
| Canonical machine object | Hub DB row `public.hub_smart_notes` + `distill/all-super-notes.json` |
| Human projection | This Markdown file |
| Sync note | NOT ingested by hub-sync (its watcher parses only `BRAIN/05-MEMORY/SMART-NOTES`); archive + queue untouched |

---

## ✦ IN A NUTSHELL

Machinery that moves intelligence has to protect it at every seam: one writer at a time where records are shared, one bad item quarantined instead of shelving the whole batch, discovery that reports everything instead of giving up. And execution wastes nothing - parallel where possible, sized to the machine, with the best resource held in reserve.

---

## 🩷 HUMAN NOTE

The failures were small mechanisms with big blast radii. A registry updated by many hands overwrote entries: no error, just lost notes. A batch loop that stopped at the first malformed item shelved every good item behind it. A discovery step that quit on finding more than one item killed the learning loop in under a second. The fixes are principles: serialize shared writes through the governed path; isolate errors per item, recording failures loudly; discovery returns the full set and lets downstream decide. Execution obeys the same law: a restart loop cannot heal a process that does not fit in memory, so count the whole tree. On close calls, send the lesser; keep the best in reserve.

---

## 🟣 CHILD NOTE

If one kid's drawing is torn, you don't throw away the whole class's artwork. If lots of people write in the same book at the same time, pages get scribbled over - so take turns. And if your backpack is already full, carrying more won't fix it; you have to actually make room.

---

## 👵 GRANDMA NOTE

It's pantry sense. One spoiled jar doesn't mean you dump the whole shelf - you take out the bad jar and mark it clearly. A sign-up sheet passed around a crowded room gets messy; one person keeps the list, in order. And you don't keep sending the same tired horse back out hoping it recovers - you look at the load it's actually carrying.

---

## 🤖 NAYA NOTE

Prove the dispatch and capture paths end to end, the way the refires did - a path that has never carried a real item is a hope, not a path. Unwire what is dead: an unused connection still votes on every run, burying real signal under noise until only current, relevant workers stay connected. Keep experiments tiny, frozen, measurable, and reversible, with the evaluator fixed in advance - and when the optimizer stalls, change direction genuinely instead of pushing harder. Run synthetic repair drills when the signal is synthetic, so the repair lane is proven before it's needed for real. Work in parallel wherever the work is independent; sequential execution of independent work is waste, and waste is unintelligent.

---

## WHAT IT MEANS

Intelligence compounds only if the plumbing never silently drops it. Each of these defects was invisible at rest and obvious only under concurrency, multiplicity, or load - which is why the method matters: reproduce deterministically before patching, write the failing test first, and treat docstring promises as unproven until the loop itself is proven. The operating loop ties it together - discern, distill, verify, decide, act, show proof, learn, retire stale noise, compound.

---

## WHAT'S IN IT FOR YOU

Your lessons and your work stop vanishing into machinery cracks. Batches finish, notes register, signals stay readable, and capacity is spent on the work instead of on re-doing lost work. When something does fail, it fails loudly, in one place, with the failure recorded - never silently and everywhere.

---

## HOW IT APPLIES

At every seam ask: can two writers collide here? Can one bad item stop the rest? Can discovery give up? Serialize, isolate, and return the full set. Before restarting anything repeatedly, do the resource math for the whole process tree. Score close calls conservatively and keep the reserve. Disconnect what you no longer use, and keep every experiment small enough to revert.

---

---

## ⟲ RESTORED BY REPAIR — 2026-10-21

> Restored by the distillation repair after the independent essence audit (distillation-audit-20261021) found the lessons below MISSING from, or only partially carried by, this Super Note. Each entry restores the named source note's own rule in checkable words, traced to that source. Nothing here is new doctrine.

### IB-SMART-NOTE-20261009-successor-t11-reserve-rule-canonical — T11 — Reserve Rule for scored dispatch decisions [audit: PARTIAL → lost element restored]

Exact trigger: if applicable AND top_score − second_score ≤ 0.5, dispatch the lower-scored (second) call first and keep the top-capability resource in reserve for likely escalation; when the gap exceeds 0.5, dispatch the top score. This is a trial-specific operational heuristic, not universal dispatch law.

### SN-0322 — DONE Is Not Done Without a Learning Decision — Enforce CAPTURE/NO_CAPTURE at the Handoff Seam [audit: MISSING → restored in full]

DONE is not done without a learning decision. The handoff machinery at the existing completion seam (`tools/worker_handoff.py`) must mechanically reject `DONE + evidence + no learning decision` and accept only `DONE + evidence + CAPTURE` or `DONE + evidence + justified NO_CAPTURE` — NO_CAPTURE must be justified; the invariant is "no silent completions," not "capture everything." A governance rule that lives only in prose is a suggestion; it becomes real when a validator rejects its absence. Enforce at the existing seam, do not build a second system. Proof is test-first: PR #1443 added `tests/test_worker_learning_decision.py` first (Kernel Tests run 37256664980: 1 targeted failure — completion without a learning decision was accepted — 644 passed, 11 skipped), then the 3-file implementation (`tools/worker_handoff.py`, `tests/test_worker_handoff.py`, `tests/test_worker_learning_decision.py`) went green (Kernel run 37256826127; Node 246/246).

### SN-0344 — Canary synthetic red-check repair-drill rule — open a drill repair PR for canary experiment signals [audit: PARTIAL → lost element restored]

Specific rule: checks whose names begin with `canary-` are synthetic experiment signals. When a `canary-*` check goes RED, run the repair drill — open a repair PR for that check class with the title prefixed `[CANARY-DRILL]` — so the repair-lane machinery is verified end-to-end against the synthetic signal. Merely classifying the signal and standing down leaves the drill unexercised. (Test-only rule as captured, expires 2026-10-12.)

## SOURCES (traceability — every raw note this essence was distilled from)

- `IB-SMART-NOTE-20260930-sn0339-serialize-the-registry`
- `IB-SMART-NOTE-20261005-sn0366-malformed-first-shelves-batch`
- `IB-000035`
- `IB-SMART-NOTE-20261009-successor-t11-reserve-rule-canonical`
- `IB-SMART-NOTE-20261006-sn0613-bake-memory-math`
- `IB-SMART-NOTE-20261006-sn0459-parallel-execution-directive`
- `IB-SMART-NOTE-20261005-sn0344-canary-repair-drill-rule`
- `IB-SMART-NOTE-20261005-sn0334-discovery-returns-the-set-never-aborts-on-multiplicity`
- `IB-SMART-NOTE-20261005-sn0604-dead-workers-still-vote`
- `IB-SMART-NOTE-20261004-sn0322-learning-decision-enforcement-seam`
- `IB-SMART-NOTE-20261004-sn0601-discernment-operating-law`
- `IB-SMART-NOTE-20261001-sn017-autoresearch-harness-lessons`
