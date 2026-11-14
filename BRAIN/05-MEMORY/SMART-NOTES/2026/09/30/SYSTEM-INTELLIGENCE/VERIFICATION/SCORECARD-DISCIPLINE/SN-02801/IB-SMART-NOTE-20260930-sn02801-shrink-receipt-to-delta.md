# When the Evidence Stops Changing, Shrink the Receipt to the Delta — Don't Re-Litigate the Whole Queue

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02801-shrink-receipt-to-delta
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gate-stall-20261114-0318.md (Gate-stall #34, 2026-11-14 03:18 PST), 9.0/10; learning-events-2026-11-14-03.md.

## ✦ IN A NUTSHELL

Gate-stall #34 re-swept the full 31-brief claim queue for the third hour running: 29× exit 7 parent-authorship + 2× exit 2 routing-prose, 0 claimed, queue 30 → 31 on a single arrival and zero clearances. The only new facts versus the 00:28 receipt were one arrival, one unrouted shared-state item, and the ordinal — so the receipt shrank to the delta instead of re-litigating all 31 briefs. The rule: when the evidence stops changing, the receipt should shrink to the diff, not re-prove the whole queue. Unchanged evidence carries zero new information; re-printing it buries the one thing that moved.

## 🩷 HUMAN NOTE

Shawn — imagine a security guard who files a full report every hour: all thirty-one doors, every lock, every window, every time — even when nothing changed for three hours straight. By the third report nobody reads past page one, and the one new thing (a single door left open) drowns in thirty pages of "still locked." The smart guard writes one line instead: "Same as last hour, except door 12 is open." That's this lesson: when nothing moved, don't rewrite the whole report — write the difference. The reader finds the news instantly, and the full report stays on file for anyone who needs it.

## 🟣 CHILD NOTE

Imagine you count your toy cars every day to make sure none are missing. If you have thirty-one cars and nothing changed, you don't need to list every single car again — you just say "still thirty-one, same as yesterday, except one new red car arrived." Listing all thirty-one every time is boring and slow, and the new red car gets lost in the list. When nothing changes, just say what changed. That's the whole trick.

## 🔵 GRANDMA NOTE

Dear, it's like the shopping list on the fridge. If the list is the same as yesterday except you added milk, you don't rewrite the whole list — you just add "milk" at the bottom and say "same as yesterday, plus milk." Rewriting everything wastes your time and hides the milk. Reports are the same: when the news is one small change, write the one small change and point at yesterday's full list. The full list is still there whenever anyone needs it.

## 🟠 NAYA NOTE

Source: gate-stall-20261114-0318.md (Gate-stall #34, 2026-11-14 03:18 PST), 9.0/10. Full 31-brief claim sweep, 29× exit 7 parent-authorship + 2× exit 2 routing-prose, 0 claimed; queue 30 → 31 (one arrival, zero clearances across three hours). Delta vs the 00:28 PST receipt: ONE arrival, ZERO clearances; the receipt states "when the evidence stops changing, the receipt should shrink to the delta, not re-litigate the whole queue — this receipt does that, and the only new bytes are the two diffs (one arrival, shared-state unrouted) plus the ordinal." Scope note: delta-only is defined only against a cited prior full receipt — the first receipt of a series must be full, and the delta must name every changed item plus the ordinal. Cousin: SN-2795 (a check name is not a suite — a failure report names job → step → file → test; same family of receipt-precision rules, different axis: granularity of a single report vs brevity across repeated reports).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "shrink_receipt_to_delta_when_evidence_stops_changing",
  "mechanism": "unchanged evidence carries zero new information, so re-printing a full queue on every repeat sweep adds reader cost without adding signal and buries the one new fact; the diff against the last full receipt plus the ordinal is information-complete exactly when the base is stable and cited",
  "evidence": "gate-stall-20261114-0318.md (2026-11-14 03:18 PST, 9.0/10): full 31-brief claim sweep, 29x exit 7 parent-authorship + 2x exit 2 routing-prose, 0 claimed; queue 30 -> 31 (one arrival, zero clearances across three hours); delta vs the 00:28 PST receipt is ONE arrival and ZERO clearances — the only new bytes are the two diffs (one arrival, shared-state unrouted) plus the ordinal",
  "falsifiability": "if a delta-only receipt ever omits a material change (a clearance, a new failure mode, a changed verdict) that the full form would have carried, the delta was under-scoped and the rule narrows to delta-plus-explicit-unchanged-claims; if no prior full receipt exists to cite, delta-only is undefined and the receipt must be full",
  "decision_change": "a future seat writing a repeat receipt (stall sweep, hourly re-sweep, repeated claim sweep) whose evidence is unchanged writes delta-only — the diff vs the cited last full receipt plus the ordinal — instead of re-litigating the whole queue",
  "applies_when": ["receipt", "repeated-sweep", "stall"],
  "enforcement": "the receipt audit for a repeated sweep: the receipt must name its delta against the cited prior full receipt (or state 'no change' with the ordinal); a repeat receipt that re-litigates unchanged evidence without a delta fails the brevity check and is returned for a delta-only rewrite",
  "related": ["SN-2795 a check name is not a suite — failure report names job, step, file, test"]
}
~~~
