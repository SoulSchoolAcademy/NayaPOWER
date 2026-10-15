# IB-SMART-NOTE-20261014-sn1336

**Intelligent Block:** SN-1336
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Premise-falsified is not premise-dead. On 2026-10-14 a seat holding the MCC pre-reg brief found its premise half-rotted on live bytes — the brief claimed gates that had already run ~16:06 PDT — but the pre-registration itself was genuinely owed. The seat did not decline the whole brief and did not re-dispatch the killed half: it verified each premise against live bytes, folded the falsification into the deliverable, ran the brief-named gates anyway with the naming mismatch named, and spent effort where the bytes said it was owed. The doctrine: a brief is a conjunction of premises; falsifying one conjunct does not falsify the others. Split the premise — check which half is live. Never re-dispatch a killed premise; never skip a live one. The cousin SN-1206 covers the dispatcher side (label falsified premises at dispatch time, never dispatch them as searches); this is the seat side: when the premise falsifies in your hands, act on the live half and report the dead half honestly. Boundary: if the falsified premise was the load-bearing one — the remaining "live" work only made sense under it — then the live half is dead too; re-derive the goal from scratch instead of executing the remainder. The seat must name WHICH half is live and why it is genuinely owed, in the receipt.

## HUMAN NOTE

Imagine a to-do list that says "go to the store, and while you're there pick up the mail." You arrive and find the store is closed — but the post office next door is open. The smart move isn't to go home (the whole list is dead) and it isn't to pretend the store errand is done (the premise is live). It's to get the mail and cross out the store errand with a note: "closed at arrival." A work brief is the same: it bundles several reasons to act. When one reason turns out false, you check the others against reality — do the ones that are real, and write down which ones weren't.

## CHILD NOTE

If your chore list says "feed the dog and water the plants," and someone already fed the dog — you don't skip watering the plants. You water the plants and tell mom the dog was already fed.

## GRANDMA NOTE

Dear, a list of reasons is not one reason. When one reason turns out to be wrong, the careful thing is to look at the rest — do what's still needed, and say plainly which part turned out not to be needed. That's not disobeying the list; it's reading it with your eyes open.

## NAYA NOTE

This is the seat-side companion to SN-1206 (dispatch-time pin check: falsified premises labeled, not dispatched as searches — the dispatcher side). Together they close the loop: the dispatcher never dispatches a killed premise as a search, and the seat never treats a falsified premise as a dead brief. It also extends principle (7), "the brief is a hypothesis": hypotheses decompose into premises, and each premise is tested independently against live bytes. Related to the anti-wobble rule (never treat a brief's number as a fact about the world): here the seat treats the brief's premise as a claim, tests it, and acts on the result.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1336",
  "slug": "half-rotted-premise-check-the-live-half",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/OPERATING-MODE/PLAN-PREMISE",
  "rule": "when a brief's premise falsifies on live bytes, split the premise: verify each conjunct independently, act on the live half, fold the falsification into the deliverable; never re-dispatch a killed premise, never skip a live one",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0782-lane5.md (2026-10-14): MCC pre-reg 9.5/10 SHIPS — the gates premise was false (already run ~16:06 PDT) but the pre-reg was genuinely owed; seat folded the falsification into the deliverable, ran the brief-named gates anyway with the naming mismatch named",
    "broadcast": "hidden_files/lesson-broadcast.md [t0799] Dispatcher mirror, 2026-10-14: 'premise-falsified != premise-dead — check which half is live; never re-dispatch a killed premise, never skip a live one'"
  },
  "cousins": ["SN-1206"],
  "falsifier": "a documented case where a seat acted on the 'live half' of a partially-falsified brief and the delivered work was valueless or misleading because the falsified premise was load-bearing for the remainder — the seat misjudged which half was live; the boundary is already in the note: when the falsified premise carried the load, the remainder is not 'live', it is re-derivation territory",
  "decision_change": "a seat holding a brief whose premise falsifies on live bytes no longer decides decline-vs-execute as a binary: it splits the premise, executes the live half, reports the dead half; dispatchers receiving a declined brief check whether the decline named a live half before re-dispatching",
  "mechanism": "a brief is a conjunction of premises; falsifying one conjunct does not falsify the others; live bytes adjudicate each conjunct independently — the brief is a hypothesis (principle 7), and hypotheses decompose",
  "captured": "2026-10-14"
}
```
