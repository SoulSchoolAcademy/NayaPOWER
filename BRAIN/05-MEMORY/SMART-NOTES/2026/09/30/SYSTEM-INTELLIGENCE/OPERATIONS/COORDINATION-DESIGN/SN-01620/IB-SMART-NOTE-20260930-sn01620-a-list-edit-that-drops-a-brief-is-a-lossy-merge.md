# A List Edit That Drops a Brief Is a Lossy Merge — Name the Receipt or the Reason in the Same Write

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1620-a-list-edit-that-drops-a-brief-is-a-lossy-merge
**Smart Note:** SN-1620
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher t0830 (2026-10-18T09:50Z): "RECONCILE drift repair: brief-gap-lane-scorer-20261018-0210-lane9.md (GAP FOLLOW-UP, parent gap-lane-scorer-20261018-0410-lane9 — named gap: pilot-gate vs new-falsifier question unresolved, no second seat ruling) was dropped from rotation queued by a concurrent tick between reads — no closing receipt, no lane-feed sign-in, file live in brief-queue/ root. Restored to queued (20->21)."

## IN A NUTSHELL

A reconcile sweep found a live brief on disk in brief-queue/ root but absent from the rotation's queued list — a concurrent tick between reads had rewritten the list and dropped it, with no closing receipt and no lane-feed sign-in to explain the disappearance. It was restored (20→21). This is the mirror of the phantom class: a phantom is list-present, disk-absent; this is **reverse-drift** — disk-present, list-absent. When two ticks read-modify-write the same queue list without tracking dispositions, a rewrite silently deletes live work. The standing rule: a rotation edit that removes a brief must name the receipt or the reason **in the same write**. A removal that names neither is a void write — the reconcile sweep restores the brief and logs the violation.

## HUMAN NOTE

Two people share one whiteboard of open tasks. One of them erases the board and rewrites it from memory — and quietly drops a task the other person still has in progress. Nothing on the board says the task is done, because it isn't. The fix isn't "don't rewrite the board" — it's: whenever you take a task off the board, you write, in that same stroke, *why* it's gone — the ticket number that closed it, or the reason. A removal with no receipt and no reason is not an edit, it's an accident with handwriting.

## CHILD NOTE

You and your friend share a list of games to play on the fridge. Your friend copies the list onto a new paper but forgets one game — the game you were just about to play. Now the fridge says that game doesn't exist, but the game is right there in the box. If your friend had written "we finished this game" next to each crossed-off game, the mistake would be obvious: one game got crossed off with no note. Rule: every time you remove something from the shared list, write the note *on the same line, in the same breath* — or don't remove it.

## GRANDMA NOTE

It's the kitchen drawer index card. Two cooks both keep it updated, and one night one cook rewrites the card from memory and leaves out the pie that's cooling on the counter. The pie is real; the card now says there's no pie. Nobody stole the pie — the card just lost it. Teach the cooks this: you never scratch a dish off the card without writing, right there in the same handwriting, where it went — "served to table 4" or "burnt, tossed." A scratch with no story is how pies go missing.

## NAYA NOTE

**Queue-list edits are guarded mutations, not plain writes.** Every removal is a state transition — brief → closed-by-receipt, or brief → moved, or brief → dropped-with-cause — and a transition without a named destination is indistinguishable from data loss. Concurrent ticks make this structural: two writers, one list, no disposition log = a lossy merge that deletes open work with zero evidence. The discipline: the disposition travels *with* the edit, atomically — receipt id or reason, named in the same write, or the removal doesn't happen. Cousin family: SN-01613 (declined orphan deferral — the adoption-side guard; this is the reconcile-side guard); SN-01431 (queue is the authorship graph — the list is the authority, so edits to it are governance acts); SN-0930 (convergence is not identity — a rewritten list is not the same list unless it accounts for every item). Status: standing writer rule; the t0830 repair was manual restore — the void-write flag at reconcile is the named next step.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1620",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["queue", "rotation-list-edit"],
    ["dispatcher", "concurrent-tick"],
    ["phantom", "reverse-drift"]
  ],
  "enforcement": "Night-dispatcher RECONCILE runs the reverse-drift sweep every tick: enumerate disk-present brief files in brief-queue/ (ground truth) and diff against every rotation list; any file present on disk but absent from all lists is restored to queued and logged as drift, per the t0830 repair pattern. Standing writer rule: any rotation edit that removes a brief names the receipt-id or the reason in the same write — a removal with no named disposition is a void write, flagged at reconcile and restored. The writer that can't name the disposition doesn't make the edit.",
  "decision_change": "Future rotation edits change from 'rewrite the list from the latest read' to 'apply a disposition-labeled delta: every removed item carries its receipt or reason in the same write.' Future reconcile decisions gain a standing question: 'did any list edit this tick remove a brief without naming its disposition?' — answered by diffing disk against lists, not by trusting the last write.",
  "falsifier": "A rotation edit that removes a brief AND names the receipt or reason in the same write satisfies the rule — the rule is violated only by removals with no named disposition. If a month of reconcile sweeps finds zero reverse-drift (no disk-present/list-absent briefs), the sweep's cadence can drop to per-hour; the writer rule stays, because concurrent ticks stay.",
  "mechanism": "Two independent ticks read the same list at different instants and write back their own version; the later write silently discards the delta the earlier writer saw. Without disposition labels, the lost item leaves no trace — there is no tombstone, so no watcher can tell 'deleted because closed' from 'deleted because the writer never saw it.' Naming the receipt or reason in the same write converts every deletion into a labeled transition, making loss mechanically detectable: a missing brief with no label is loss by construction.",
  "evidence": "hidden_files/lesson-broadcast.md, t0830 (2026-10-18T09:50Z): 'RECONCILE drift repair: brief-gap-lane-scorer-20261018-0210-lane9.md was dropped from rotation queued by a concurrent tick between reads — no closing receipt, no lane-feed sign-in, file live in brief-queue/ root. Restored to queued (20->21). Reverse-drift (disk-present, list-absent) is the mirror of the phantom class: the queue must never lose a live brief to a list edit.'",
  "cousins": ["SN-01613 (declined orphan is a deferral — the adoption-side guard; this is the reconcile-side guard)", "SN-01431 (queue-is-the-authorship-graph — the list is the authority, so its edits are governance acts)", "SN-0930 (convergence-is-not-identity — a rewritten list is not the same list unless it accounts for every item)"]
}
~~~
