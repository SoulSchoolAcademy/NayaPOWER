# A Merge Watch That Counts a Window Can Report Zero While a Merge Lands on Its Edge — Anchor on Tip-SHA Continuity

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02749-merge-watch-window-zero-misses-tip-move
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Director merge-watch pass 2026-11-12 ~20:38 PST vs PR #3357 merged 2026-11-13T04:44:06Z (breach #307); memory log ~/memory/2026-11-12.md, Window DO entry 20:55 PST; TIPVERIFY-64 (pin 26b1a0e6, cycle ran 20:08-20:50 PST).

## ✦ IN A NUTSHELL

The director's merge watch reported "0 PRs merged" while PR #3357 had merged minutes earlier — no 3-pass receipt, 0 reviews, 4 check failures at the merge commit, breach #307. A watch that counts merges inside a time window can report zero while a merge lands on the window's edge: the query runs before the merge is indexed, or the window starts after the merge timestamp. The tip SHA is a single atomic fact — if it moved, something merged, and no window edge can hide it. Anchor every "0 merged" claim on tip-SHA continuity: compare the live tip to the last verified tip, and treat any movement as merges to investigate. A "0 merged" verdict without a tip-SHA check is unproven, not clean.

## 🩷 HUMAN NOTE

Shawn — the night watch reported "nothing merged" while a merge had landed minutes before the check ran. The merge (PR #3357, a learning-event doc) went to main with no receipt, no reviews, and four failing checks — and the watch missed it entirely, because it counted merges inside a time window and this one fell on the window's edge. The fix is one anchor: before any watch says "zero merged," it must compare the live tip SHA against the last verified tip. If the tip moved, something merged — full stop. A zero without that check is a guess, not a finding.

## 🟣 CHILD NOTE

Imagine you're counting how many kids came through the door between 8 and 9 o'clock, but you only look at the door at 9. A kid who slipped in at 8:59 while you were looking away doesn't get counted — your notebook says zero, but a kid is inside. The tip SHA is like checking whether anyone is in the room at all: if the room is different from the last time you looked, someone came in. Count the room, not the clock.

## 🔵 GRANDMA NOTE

Dear, it is like counting visitors by asking who knocked between lunch and tea — and missing the one who came in through the back door while you were in the kitchen. You don't count knocks; you check whether the house has changed. If a chair has moved, someone was here. The tip SHA is the chair: compare it to the last time you looked, and you will never miss a visitor again.

## 🟠 NAYA NOTE

This is the detection-side companion to SN-1066 (the disclosure side: a watcher must self-report its own missed breach) and SN-1592 (every watch needs a falsifier for its EMPTY state). Those say what a watcher must do when it misses; this says how to stop missing this way. (1) A time-window count query is not a falsifier for "0 merged" — it is blind at both edges (indexing delay at the query end, window start at the other). (2) The tip SHA is the falsifier: `git ls-remote` at run time vs the last verified tip; any delta means merges happened, and the watch must enumerate them before claiming zero. (3) The #3357 case is the worked proof: the director's run started 04:45:57Z, the merge landed 04:44:06Z, and the watch still reported zero. (4) Apply the same anchor to any "nothing changed" verdict: a count over a window is a claim about the query, not about the world.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": [
    ["merge", "watch"],
    ["claim", "empty"],
    ["watch", "empty-state"]
  ],
  "canonical_object": "INTELLIGENT_BLOCK",
  "claim_boundary": "This note governs merge-watch '0 merged' verdicts only: it does not claim window queries are useless elsewhere, only that a window-count query cannot falsify 'no merges'. It does not adjudicate breach #307 itself (that is the dock's), only the watch defect that missed it.",
  "decision_change": "Before a merge watch reports '0 merged' — or verifies such a claim — the run compares the live tip SHA (git ls-remote at run time) to the last verified tip; any movement forces a merge enumeration, and a '0 merged' claim without that check is treated as unproven.",
  "enforcement": "The merge-watch run asserts tip-SHA continuity (ls-remote tip vs last verified tip) before reporting '0 merged'; a '0 merged' claim without the tip-SHA check is rejected as evidence by the merge-watch owner / director. The check is a named verification step in the watch run, not a habit.",
  "evidence": [
    "PR #3357 ('docs(brain): learning event 2026-11-12'), merged 2026-11-13T04:44:06Z via merge commit ad608c48 by nayanet[bot]; head 26d82ac3; 0 reviews; NO 3-pass receipt in the 1,704-char PR body (verified by direct read); 4 check failures at the merge commit (test, chain-readiness-gate, promote-and-prove, resolve-current-truth). Breach #307.",
    "The director's ~20:38 PST pass (run started 04:45:57Z) reported '0 PRs merged after previous tick' while PR #3357 had merged at 04:44:06Z, ~1.8 min before the run started. The watch's window query missed a merge that landed at its edge. Memory log ~/memory/2026-11-12.md, Window DO entry 20:55 PST.",
    "TIPVERIFY-64 (pin 26b1a0e6, cycle 20:08-20:50 PST): tip moved twice after the pin (26b1a0e6 -> ceef98b7 -> ad608c48) — the tip SHA recorded the movement the window query missed."
  ],
  "falsifier": "Refuted if the #3357 miss is shown to have a different cause — e.g. the watch's query window covered 04:44:06Z and still returned zero (then the cause is a query/index error, not a window edge); or if a window-count watch provably catches every merge across a month of tip moves while a tip-SHA check adds nothing.",
  "intelligence_class": "LESSON",
  "mechanism": "GitHub merge/query results are eventually consistent and window-bounded: a merge landing near query time or just before the window start is invisible to the count. The tip SHA changes atomically with any landing, so comparing SHAs cannot miss a merge the window query can — the SHA is a single fact about the world, the window count is a fact about the query.",
  "related_notes": ["SN-1066", "SN-1592", "SN-0971"],
  "truth_state": "CANDIDATE"
}
```
