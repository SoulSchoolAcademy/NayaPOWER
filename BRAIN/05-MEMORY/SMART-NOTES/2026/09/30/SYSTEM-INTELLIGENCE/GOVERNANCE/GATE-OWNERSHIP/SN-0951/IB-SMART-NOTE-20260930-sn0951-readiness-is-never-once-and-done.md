# Readiness Is Never Once-and-Done — Re-Evaluate Every Queued PR on Current Evidence at Merge Time

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0951-readiness-is-never-once-and-done
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [NAYA 2 WIRE LANE] sign-out, #2175 comment 6105870609 (2026-10-11T05:33:46Z); PR #2288 (branch naya2/fairness-queue-wire, stacked on #2228); tools/merge_queue_fairness.py; tools/snapshot_merge_queue.py; 25 tests + 3 negative controls; CI extended.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's wire lane signed out a merge-queue fairness instrument (PR #2288): every queued PR is modeled as a `WorkItem`, and **five merge-readiness requirements are re-evaluated against evidence only** — at merge time, on the current tip, not at queue time. That re-evaluation is the doctrine: a queue entry that was "ready" three hours ago, two tips ago, is not ready until it is ready *now*. Queues accumulate latency between the decision and the action, and every byte of that latency is decay: the tip moved (SN-0493 — a decision expires when the tip moves), the checks flipped (t2302-c's #1825 review found 4 required checks failing on an unchanged head after a CI re-run), the gate conditions changed. The fairness instrument's structural answer is that readiness has no memory — each item carries its five requirements, and the gate re-proves them against the live board, the live tip, and live check state at the moment of the merge. This is SN-0493 institutionalized: SN-0493 says re-anchor at action time; the fairness gate is the machine that forces it for queued items, where a human will never remember to. A cold Naya maintaining merge machinery months from now: never trust a queued item's readiness stamp from queue time; model queue items as WorkItems with re-evaluable requirements; the merge action must re-run every requirement against current evidence; a requirement that cannot be re-evaluated mechanically does not belong in the queue.

Why this is brain-grade: queues are where decisions die. Everything in this system learned (the hard way, on the night shift) that the gap between "we decided" and "we acted" is where corruption breeds — silent-drop merges (SN-0539), pre-merge checks trusted on post-merge trees (SN-0328), dead boards still wired into live gates (SN-0947). A queue is that gap, industrialized. The fairness wire is the first instrument that treats the gap as the threat model: re-evaluation *against evidence only* is also a fairness property — no seat's item rides on a stale approval, and no seat's item is skipped because someone's word carried more weight than the evidence. Fairness and correctness converge here: both require that the only thing evaluated is the current evidence.

## 🩷 HUMAN NOTE

Shawn — Naya 2's lane wired a fairness instrument into the merge queue tonight (PR #2288), and the pattern is worth banking. Every PR in the queue is treated as a WorkItem, and its five merge-readiness requirements get re-proved against live evidence at merge time — not trusted from when it entered the queue. Because a queue is just a long delay between the decision and the action, and everything in that delay decays: tips move, checks flip, gates change. Tonight's own reviews proved it: PR #1825's checks failed on a head that hadn't changed at all — the world moved around it. The rule: readiness has no memory. Re-evaluate every queued item on current evidence at the moment you act. That's also what makes it fair — no item rides on a stale approval, and nobody's word outranks the evidence.

## 🟣 CHILD NOTE

Imagine a line of kids waiting to ride a roller coaster. The tall-enough sign was checked when they joined the line an hour ago. But kids grow — and the ride's height rule is about *right now*, not an hour ago. So before the gate opens, the attendant measures every kid again, against the real measuring stick. That's what the fairness gate does: it doesn't trust the stamp from queue time; it measures every waiting PR against the current evidence before letting it through. Fresh measure, every time.

## 👵 GRANDMA NOTE

Think of a bakery with a take-a-number line. Your number was called at 8 AM, but you only get to the counter at noon — and the cakes you wanted might be sold out, the prices might have changed, the shop might be closed for lunch. A good bakery doesn't hand you yesterday's cake because your number was drawn yesterday. It checks what's fresh on the counter right now. The merge queue is that bakery: the number gets you to the counter, but the sale happens on today's stock. Fresh check at the counter, always.

## 💜 NAYA NOTE

Future Naya: (1) Model every queued merge as a WorkItem carrying its own re-evaluable readiness requirements — never a readiness *stamp* from queue time. (2) The merge action must re-run all requirements against current evidence: live tip, live check state, live gate conditions. Stale approvals don't ride. (3) Any requirement that cannot be re-evaluated mechanically is not a requirement — it is a promise, and promises don't belong in a queue's gate. (4) This is the fairness property too: re-evaluation *against evidence only* means no item is merged on reputation and none is skipped on rumor. (5) Pair with SN-0493 (decision expires when the tip moves — this is the queue's version), SN-0328 (re-verify on the actual merge commit), SN-0947 (gates must point at the live board, not a dead one). Evidence anchors: #2175 6105870609 (wire-lane sign-out, 2026-10-11T05:33:46Z); PR #2288 branch naya2/fairness-queue-wire; tools/merge_queue_fairness.py + snapshot_merge_queue.py; 25 tests + 3 negative controls; t2302-c's #1825 check-flip on an unchanged head is the instance that proves decay is real.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0951",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "GATE-OWNERSHIP"],
  "cousins": ["SN-0493", "SN-0328", "SN-0947"],
  "rule": "A merge queue must re-evaluate every queued PR's readiness requirements against current evidence at merge time. Readiness has no memory: the tip moves, checks flip, gates change between queue time and action time. Model queued items as WorkItems with re-evaluable requirements; the merge action re-runs them all. A requirement that cannot be mechanically re-evaluated does not belong in the queue.",
  "anti_rule": "Trusting queue-time readiness stamps at merge time; letting items ride on stale approvals; embedding requirements that only a human can re-check.",
  "evidence": {
    "wire_signout": "#2175 comment 6105870609 (2026-10-11T05:33:46Z, NAYA 2 WIRE LANE)",
    "pr": "#2288, branch naya2/fairness-queue-wire (stacked on #2228)",
    "instruments": "tools/merge_queue_fairness.py (WorkItem, five requirements re-evaluated against evidence only), tools/snapshot_merge_queue.py",
    "proof": "25 tests + 3 negative controls; CI extended",
    "decay_instance": "t2302-c: 4 required checks failing on PR #1825's unchanged head after a CI re-run — the world moves around a queued item"
  },
  "authority": "Naya 2 wire-lane sign-out observed on #2175; captured by Naya 4 distillation, CANDIDATE (auto-capture, not ratified)"
}
```
