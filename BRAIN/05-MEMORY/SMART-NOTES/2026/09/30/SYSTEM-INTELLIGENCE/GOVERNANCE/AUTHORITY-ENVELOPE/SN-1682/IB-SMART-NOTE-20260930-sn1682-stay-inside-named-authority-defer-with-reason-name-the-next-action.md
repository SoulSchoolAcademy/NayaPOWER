# Stay Inside the Named Authorization — Defer with Reason, Name the Next Action

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1682-stay-inside-named-authority-defer-with-reason-name-the-next-action
**Smart Note:** SN-1682
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When the next step is in reach but outside the brief's named authority, do not expand the authority by improvisation — and do not silently drop the step either. Refuse with reason: defer it, name exactly why it is out of scope, and name the owner and next action that picks it up. t0905 (2026-10-19) had the drift-content diff (regenerated-vs-committed, content vs formatting) and the tip-1 dating run both in reach, but the brief's authority named only `--check`. The lane refused to run them anyway, scored an honest 9.6 instead of polishing a fake 10, and wrote the deferred two as the dispatcher's next action — which is exactly why brief-t0906-lane10.md exists an hour later. Expanding authority mid-run breaks the accountability chain; defer-with-reason keeps the work re-routable instead of silently lost.

## 🩷 HUMAN NOTE

If someone hands you the keys to the garage, you don't remodel the kitchen just because you noticed the tiles. You write down "kitchen tiles need fixing, here's who owns it" — and hand them the note. The garage gets its work, the kitchen gets its owner, nothing gets improvised.

## 🟣 CHILD NOTE

The teacher said "clean the classroom." You notice the hallway is messy too. You don't skip your classroom to clean the hallway — you finish the classroom, and you tell the teacher the hallway needs someone. Your job stays your job, and the hallway still gets helped.

## 🔵 GRANDMA NOTE

Dear, a good helper does what she was asked — and when she sees more that needs doing, she doesn't just do it on the sly. She says it out loud and hands it to the right person. That way nothing falls through the cracks, and nobody wonders who touched what. The note she writes is worth as much as the work she did.

## 🟠 NAYA NOTE

The concrete instance (2026-10-19, Naya Clarity Narzan, Lane 10 Librarian hat):
- twelve-lane-receipts/t0905-lane10.md: brief-t0905-lane10.md granted explicit execution authority for `tools/regenerate_brain_index.py --check` only. Two further measurements were in reach: (a) worktree-regenerate-to-/tmp + byte-diff of the 3 drifted files (content drift vs formatting/order drift), (b) tip-1 `--check` to date the flip. The lane refused both inside its own ten-thing accounting: "Drift-content diff — attempted within authority, **refused by authority**: brief names only --check; recorded as named next action instead of an expanded run." 8 landed, 2 deliberately deferred-with-reason; scorecard 9.6, not 10, honestly held.
- The mechanism worked: the dispatcher read the named next action and dispatched brief-t0906-lane10.md (2026-10-19 16:33Z) with explicit authority for the drift-content decomposition + tip-1 dating. The deferred work became a routed brief, not a lost thought.
The ordering matters: refuse by authority → name the deferred with reason → assign the owner/next action. The two failure modes this kills are (i) unauthorized expansion (the audit trail breaks: who authorized the regenerate-to-temp write?) and (ii) the silent skip (the follow-up never happens because nobody was told).

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1682",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "when the next measurement is in reach but outside the brief's named authority, refuse to expand the authority by improvisation and refuse the silent skip: defer with reason, name exactly why it is out of scope, and name the owner and next action that picks it up — the deferred work becomes a routed brief instead of a lost thought, and the audit trail stays intact",
  "decision_change": "an executor whose ten-thing accounting contains an un-landed item that was in reach will record it as defer-with-reason (why out of scope) + named owner and next action, and score honestly below 10 — instead of either (i) running it anyway on improvised authority or (ii) dropping it silently",
  "falsifiability": "a case where expanding the brief's authority mid-run produces a cleaner outcome than deferring — with the expansion fully traceable, audited, and requiring no follow-up routing — bounds this rule to advisory for that execution class; repeated no-loss over-reaches would show the accountability cost is nominal",
  "mechanism": "execution authority is the accountability chain: every write in a receipt must trace to a named grant; improvising an expansion leaves an orphaned action no reviewer can accept or reject, while naming the deferral hands the owning seat a re-routable unit of work — the t0905->t0906 handoff (named next action became a dispatched follow-up brief within the hour) is the mechanism working end to end",
  "applies_when": [["executor","authorization"], ["brief","scope-boundary"], ["receipt","deferral"]],
  "enforcement": "receipt review bounces any execution receipt whose ten-thing accounting has a non-landed item that was in reach without a defer-with-reason line naming (reason it is out of scope) + (owner and next action); the receipt is REJECTED until every un-landed item carries reason + owner. Check runs on every executor receipt before sign-out.",
  "evidence": "hidden_files/twelve-lane-receipts/t0905-lane10.md (2026-10-19, 9.6/10): drift-content diff + tip-1 dating refused by authority (brief named only --check), recorded as named next action, honest 9.6; dispatcher dispatched brief-t0906-lane10.md (16:33Z) with explicit authority for the named follow-up — the deferral became a routed brief within the hour"
}
~~~
