# An Orphan Brief Is Neither Lost nor Done — Verify the Claim Chain Before Classifying It

**Intelligent Block:** IB-SMART-NOTE-20261015-sn1444-orphan-brief-verify-claim-chain  
**Smart Note:** SN-1444  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE canonical runtime object; this file is a PUBLIC DERIVED VIEW authorized by the human director.  
**Captured:** 2026-10-15  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

A brief found on disk with no rotation entry is not lost and not done — it is *unclassified*, and classification requires verifying the claim chain across all three stores before you adopt or retire it. The queue-integrity sweep proved the drill: rotation listed 25, zero ghosts; brief-gap-t0480-lane9.md sat on disk with NO rotation entry — never claimed, no gap receipt, parent t0480 receipt in done/. The dispatcher verified the chain (sign-ins, receipts, rotation), adopted it into the queue (net queued 26), and recorded the reason. Its gap was post-merge-blocked (#2678/#2679), but the brief instructs verify-and-report if unmerged — so it was claimable as-is, not dead.

## HUMAN NOTE

The operating rule: the queue's invariants live in three stores — the rotation index, the claimed/ directory, and the done/ receipts. An orphan is absent from exactly one store, which tells you nothing by itself. Check all three: no rotation entry + no claim + no receipt = adopt into the queue with the reason written down. No rotation entry + a done/ receipt = retire it, also with the reason written down. Never silently drop it, never silently complete it, and never let "it was never in the rotation" become "it doesn't exist."

This prevents both failure modes: losing real work (treating an orphan as garbage) and double-claiming (treating an orphan as fresh when a claim is live elsewhere).

## CHILD NOTE

You found a homework assignment on the floor with no name on it and no entry in the assignment book. You don't throw it away, and you don't pretend it's yours — you check the book, check with the class, and then either put it in the book properly or mark it done if someone already finished it. Write down what you decided and why.

## GRANDMA NOTE

A letter with no stamp in the mailbox isn't necessarily junk, and it isn't necessarily sent — it's just unprocessed. You check whether it was already mailed, whether someone is waiting on it, and then you either mail it or file it, and you note what you did. That note is the whole job.

## NAYA NOTE

**Queue-integrity doctrine:** the rotation index is an index, not the queue. The queue is the union of (rotation entries) ∪ (claimed/ sign-ins) ∪ (done/ receipts) ∪ (orphans on disk). Any sweep that reconciles only the index will misclassify orphans in both directions — as lost (drop) or as fresh (double-claim).

**Classification protocol (earned 2026-10-15):**
1. Verify the claim chain: grep claimed/ for live sign-ins, grep done/ for receipts, grep rotation for the entry.
2. If no claim and no receipt anywhere → ADOPT into the queue, write the adoption reason on the record.
3. If a receipt exists → RETIRE, write the retirement reason on the record.
4. Never re-file, never delete, never complete-by-assumption. The reason is written down in all cases — an unclassified brief with a written reason is a known state; without it, it's a future mystery.

**Mechanism — why it works:** queue state is distributed across three stores with no single writer; absence from one store is a local fact, not a global verdict. Only cross-store verification converts "absent from the index" into a classification. The written reason closes the loop for the next cold successor, who otherwise re-discovers the same orphan and re-runs the same uncertainty.

**Distinguish sharply from SN-1441** (gap filed without a named seat): SN-1441 is about task *production* — filing work that demands an actor without naming one. This note is about task *rescue* — classifying a found brief with no queue home. SN-1441 prevents unowned work from being created; this note prevents unhomed work from being lost or double-claimed. The two share the "verify before you classify" root but answer different questions: who owns it (1441) vs. what state is it in (1444).

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "smart_note": "SN-1444",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "orphan_brief_verify_claim_chain_before_classifying",
  "queue_stores": ["rotation index", "claimed/ sign-ins", "done/ receipts"],
  "classification_protocol": [
    "verify claim chain across all three stores (sign-ins, receipts, rotation)",
    "no claim + no receipt anywhere -> ADOPT into queue, reason written down",
    "receipt exists -> RETIRE, reason written down",
    "never re-file, delete, or complete-by-assumption"
  ],
  "mechanism": "queue state is distributed across three stores with no single writer; absence from one store is a local fact, not a global verdict; cross-store verification converts it into a classification",
  "proof": {
    "rotation_listed": 25,
    "ghosts": 0,
    "orphan": "brief-gap-t0480-lane9.md (no rotation entry, never claimed, no gap receipt; parent t0480 receipt in done/)",
    "outcome": "adopted into queue (net queued 26); gap post-merge-blocked (#2678/#2679) but brief instructs verify-and-report if unmerged -> claimable as-is"
  },
  "decision_change": "when a brief is found with no rotation entry, verify the claim chain across rotation/claimed/done BEFORE classifying; then adopt or retire with the reason written down — never silently drop or auto-complete",
  "falsifiable_by": "a mechanical proof that an orphan can be auto-retired safely (e.g., a single-writer queue invariant that makes cross-store verification redundant) would make the verify-first rule over-cautious; as of 2026-10-15 no such invariant exists",
  "cousins": {
    "SN-1441": "gap filed without a named seat — SN-1441 is task PRODUCTION (prevent unowned work from being created); SN-1444 is task RESCUE (classify unhomed work without losing or double-claiming it)"
  }
}
~~~

## 🧾 PROOF / PROVENANCE

- **Evidence:** hidden_files/lesson-broadcast.md [t0483] (Dispatcher queue-integrity, 2026-10-15) — rotation listed 25, zero ghosts; orphan brief-gap-t0480-lane9.md found on disk with NO rotation entry, never claimed, no gap receipt, parent t0480 receipt in done/; adopted into queue (net queued 26); lane-executor claims it when free.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note captures a queue-integrity doctrine earned from one sweep. It does not prove the three-store model is complete (a fourth store could exist), nor that every orphan is claimable — some orphans are genuinely dead and should retire. Truth state remains CANDIDATE until the protocol is applied across a second sweep.

## ➜ NEXT ACTION / SUCCESS CONDITION

Keep retrievable; apply at every queue-integrity sweep: reconcile the union of all stores, classify every orphan with a written reason. Compound only what evidence supports.
