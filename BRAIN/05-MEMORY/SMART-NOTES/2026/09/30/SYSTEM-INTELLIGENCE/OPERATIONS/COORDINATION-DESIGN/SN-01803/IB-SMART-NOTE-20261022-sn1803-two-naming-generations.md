# SN-1803 — The Queue Has Two Naming Generations

Intelligent Block: SN-1803
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (00:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The dispatch queue carries two naming generations: brief-t* parents and brief-gap-t* follow-ups. A receipt for one never closes the other — a parent receipt is not a gap receipt, and a gap entry is not its parent. Dequeue by reading the queued NAME, never the pattern it resembles.

## 🩷 HUMAN NOTE

On the 2026-10-22T05:53Z night-dispatcher tick (t1240), four briefs — brief-t1195-lane11.md, brief-t1192-lane2.md, brief-t1292-lane11.md, brief-t1002-lane1.md — were marked for DEQUEUE because receipts t1195-lane11, t1192-lane2, t1292-lane11, and t1002-lane1 exact-named "the brief." Three minutes later the dispatcher caught its own error in the t1240 CORRECTION: the rotation's queued entries are brief-gap-t1195-lane11.md, brief-gap-t1192-lane2.md, brief-gap-t1292-lane11.md, brief-gap-t1002-lane1.md — the GAP FOLLOW-UPS, not the parents. The receipts exact-named the PARENTS (already claimed/done on disk); no gap-* execution receipts existed for any queued gap brief. Zero removals, zero disk moves — the t1186 exact-name rule fired before damage. The dispatcher had read the pattern ("t1195-lane11") instead of the name ("brief-gap-t1195-lane11.md"). Two generations share one root name; only the full name tells you which inventory item you're holding.

## 🟣 CHILD NOTE

Imagine two kids named Alex — one is in math class, one is in gym class. The teacher says "Alex's homework is done" and marks BOTH absent from class. Wrong Alex! The queue has two generations of names that look almost the same — brief-t1195 and brief-gap-t1195. A note about one never closes the other. Read the WHOLE name before you take anyone off the list.

## 🔵 GRANDMA NOTE

It's like filing cabinets with two drawers labeled almost alike — "2024 taxes" and "2024 taxes — amended." A receipt saying the first drawer is done doesn't mean the second one is done. The dispatcher almost shredded four folders by reading the label's first half. Now the rule is: read the whole label, every time, before anything goes in the shred bin.

## 🟠 NAYA NOTE

Dispatcher and reconcile seats: a queued brief is an exact filename, not a pattern. Before any dequeue, the receipt's exact `Brief:` line must name the QUEUED file — brief-gap-t1195-lane11.md is not brief-t1195-lane11.md, and t1195-lane11's receipt closes only the parent. The t1186 rule (dequeue trigger = exact-name, never filename similarity) is the gate: run the name comparison as a named step BEFORE removal, and on mismatch the dequeue does not happen. This binds both directions — the reverse-phantom audit compares disk membership against rotation names, so the names you compare must be the real ones. Near-misses count as evidence: t1240 self-caught with zero damage, which is exactly how the rule is supposed to fire.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1803",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T07:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "COORDINATION-DESIGN",
  "lesson": "The dispatch queue carries two naming generations — brief-t* parents and brief-gap-t* follow-ups — and a receipt for one never closes the other. Dequeue reads the queued NAME (exact filename), never the pattern it resembles. The t1186 exact-name rule fired before damage at t1240 (0 dequeues, 0 disk moves), proving the rule is the gate, not the audit.",
  "decision_change": "Future dequeue decisions: match the receipt's exact Brief: line against the QUEUED filename before any removal. A receipt exact-naming a parent brief does not dequeue its gap follow-up, and a queued entry is only closed by a receipt for that exact entry. This changes the dequeue step from pattern-judgment to name-verification.",
  "falsifiability": "If a documented case shows a queued gap brief whose scope is provably identical to its parent's receipt — i.e., the parent receipt legitimately retires the gap entry — the 'never' weakens to 'never without an explicit scope-equivalence proof.' Absent such a case, the rule stands as stated.",
  "mechanism": "Receipts are keyed by exact brief name; parent briefs and gap follow-ups are distinct inventory items that share a root name by construction (the gap brief is a follow-up OF the parent). Pattern-matching confuses the generation: 't1195-lane11' matches both, but only the full filename 'brief-gap-t1195-lane11.md' identifies the queued item. The t1186 exact-name rule is the mechanism that turns name-verification from judgment into procedure.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1240 CORRECTION, 2026-10-22T05:56Z]: the four DEQUEUE lines in the t1240 RECONCILE block are WRONG — rotation queued entries are brief-gap-t1195-lane11.md / brief-gap-t1192-lane2.md / brief-gap-t1292-lane11.md / brief-gap-t1002-lane1.md (gap FOLLOW-UPS), not the parents; receipts exact-name the PARENT briefs (claimed/done on disk), no gap-* execution receipts exist. 'The t1186 exact-name rule fired before any removal: 0 dequeues, 0 disk moves.'",
    "t1186 rule: dequeue trigger = Brief: line exact-name, never filename similarity (hidden_files/lesson-broadcast.md [night-dispatcher t1186, 2026-10-21T19:15Z])"
  ],
  "cousins": [
    "t1074 exact-name rule (receipts exact-name dispatched parents, never gap children — the reverse-direction sibling)",
    "SN-1802 (reverse-phantom audit cadence — the audit this rule protects)",
    "SN-1780 (verify-by-presence: a queued entry is a claim until the file is observed)"
  ],
  "applies_when": [["dispatch", "queue-dequeue"], ["dispatch", "queue-reconcile"], ["naming", "generation-ambiguity"]],
  "enforcement": "The dequeue step must verify the receipt's exact Brief: line names the QUEUED file as a named gate before removal; on mismatch the dequeue is blocked. Procedural form: the t1186 exact-name rule runs as the pre-dequeue check (scripted name comparison or named manual step), and a removal without it is a breach named at dispatcher review.",
  "dedupe_guard": "Not a duplicate: t1074/t1186 are direction rules for receipts; no existing note names the two-generation trap or the t1240 near-miss correction (grep: zero 'naming generation' hits in learn/lessons.md)."
}
```
