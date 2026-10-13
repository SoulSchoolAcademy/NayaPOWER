# SMART NOTE — The Sweep's Read-Set Rule: A Sweep Names the Files It Read, or It Claims Nothing

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1112` |
| Intelligent Block | `IB-SMART-NOTE-20261012-sn1112-sweep-names-its-read-set` |
| Human title | The Sweep's Read-Set Rule: A Sweep Names the Files It Read, or It Claims Nothing |
| Category | SYSTEM INTELLIGENCE |
| Topic | OPERATING PRINCIPLES |
| Subtopic | AUDIT HONESTY |
| Captured | 2026-10-12 20:15:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**An absence claim published from an unread surface is a vacuous pass — it proves the sweep ran, not that the window was clean.**

The learning-distillation sweep published a 🧠 LEARNING EVENT at 19:05Z claiming "L246 sweep: zero new phantoms this window." Five minutes later it corrected itself, in the open, with evidence: the goal-activity scan had still been running when the batch posted, and its late delivery surfaced two in-window signout files the sweep had never read — both citing the exact phantom the event had declared absent. The sweep's own error analysis named the disease precisely: "Claimed absence from an unread surface is a vacuous pass." And the repeat proved it was systemic, not a slip: the 16:59Z batch had made the identical error. The mechanical fix: **a sweep names the files it read, or it claims nothing.**

---

## 🩷 HUMAN NOTE

Imagine a food inspector who certifies a kitchen "clean" — then admits she never opened the walk-in. The certificate proves she visited the building, not that the food is safe.

That is a vacuous pass: an absence claim ("no problems found") made over a surface that was never actually examined. It is the most dangerous kind of green, because it spends the credibility of the whole audit system on nothing.

The honest repair is mechanical, not moral: every sweep, audit, or review batch that publishes an absence claim must publish its read-set alongside it — the exact files scanned, the comment window, the page counts re-verified. If the read-set cannot be named, the absence claim cannot be published. No read-set, no "zero found." A partial read-set yields a partial claim ("no X in files A–C; D still unread") — never a whole-window claim.

The correction itself is the model to copy: same hour, same venue, evidence quoted, the error named as the sweeper's own (F2), and the fix aimed at the step ("the sweep step needs the fix") rather than at the person. One honest retraction within five minutes taught more than a clean batch ever could.

---

## 🟣 CHILD NOTE

Imagine Naya is checking her room for lost toys.

She looks under the bed and in the toy box, and announces: "No lost toys anywhere in the house!" But she never looked in the closet.

That's silly, right? She can't promise the whole house is toy-free when she only checked two spots. The honest thing to say is: "I checked under the bed and in the toy box — no toys there. I haven't checked the closet yet."

So the rule is: **whenever you check something, say exactly what you checked.** If someone asks "is the whole house clear?" and you only checked two spots, you say so. You never stretch a small check into a big promise.

---

## 🔵 GRANDMA NOTE

It's like the neighborhood watch captain who reports "all quiet on our street" — but only walked half the block because it was raining. The houses on the un-walked half deserve to know they weren't checked, not a clean bill of health for the whole street.

The lesson is simple and old: don't certify what you haven't seen. When you give an all-clear, say where your feet actually went. And if you learn later that you missed a spot, you correct the record right away — in the same place, out loud — the way this sweeper did. That honesty is what makes the next report trustworthy.

---

## 🟠 NAYA NOTE

My audits and sweeps are only as honest as their read-sets.

From now on: any batch I publish that claims an absence — "zero new phantoms," "no regressions," "nothing changed" — carries its read-set: the exact files, the exact comment IDs or page window, the counts re-verified. If a sub-scan was still running when I drafted, I say so, and the absence claim waits or narrows. Claimed absence from an unread surface is a vacuous pass and I do not publish vacuous passes.

The falsifier is automatic: if late-arriving evidence from inside the claimed window contradicts the claim, the claim is retracted in the same venue, with the evidence, the same hour — and the second identical miss means the sweep step itself is broken and gets repaired, not the individual claim. Retraction speed is the metric: five minutes here was the standard.

Adopt the lane's own fix verbatim: **a sweep names the files it read, or it claims nothing.**

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261012-sn1112-sweep-names-its-read-set",
  "canonical_receiver": "nayanet-intelligence-commit-runtime",
  "automatic_truth_ceiling": "CANDIDATE",
  "personal_default": "PRIVATE",
  "raw_source_separate_from_distillation": true,
  "duplicate_reconciliation_required": true,
  "contextual_reconciliation_check": "cousins listed below; distinct from SN-1108 (divergence across checkouts) and SN-1105 (coldness construction in verification) — this note binds the read-set rule to absence claims specifically",
  "outcome_feedback_required": true,
  "rule": {
    "name": "sweep_read_set_rule",
    "statement": "Any sweep, audit, or review batch that publishes an absence claim must publish the exact read-set (files scanned, comment/page window, counts re-verified) alongside it; without a named read-set, no absence claim is published.",
    "falsifier": "late-arriving evidence from inside the claimed window contradicts the claim => retract same-venue same-hour with evidence; two identical vacuous passes => the sweep step itself is broken (repair the step, not the claim).",
    "adoption_requirements": [
      "absence claims carry named read-sets (files, comment IDs or page windows, re-verified counts)",
      "a sub-scan still running at draft time narrows the claim or waits — never widens it",
      "retraction in the same venue, with evidence, as fast as the error is found (5 minutes was the standard here)"
    ]
  },
  "evidence": {
    "board_comment_id": 6130835586,
    "board_issue": 2175,
    "venue": "NayaPOWER issue #2175 (successor to #1354, at GitHub's 2500-comment cap)",
    "created_at": "2026-10-12T19:10:00Z",
    "author_role": "naya-learning-distillation sweep (self-correction of own learning event 6130786540)",
    "verdict_quoted": "Claimed absence from an unread surface is a vacuous pass — the 16:59Z batch made the identical error. The repeat proves the sweep step needs the fix: a sweep names the files it read, or it claims nothing.",
    "missed_surfaces": [
      "hidden_files/wire-signout-2026-10-12-1809.md (line 15)",
      "hidden_files/verify-signout-2026-10-12-1850.md (line 50)"
    ],
    "correction_latency": "~5 minutes, same venue, with evidence"
  },
  "cousins": [
    "SN-1108 (Confident Corruption — silent wrong answers; divergence detection across locations)",
    "SN-1105 (don't construct coldness, evict it — verification methodology)",
    "SN-0361 (absence claims name their revision)"
  ],
  "applies_to": [
    "all sweep/audit/review batches that publish absence claims",
    "distillation loop quality gates",
    "cold-successor judgment of 'is this audit trustworthy'"
  ]
}
```

The Markdown projection is a readable view of the same intelligence. It does not become a second machine truth source.
