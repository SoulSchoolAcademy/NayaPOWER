# IB-SMART-NOTE-20260930-sn01725

**Intelligent Block:** SN-01725
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When two writers share a queue directory, the throttle-gate queue audit must read the directory, not the coordination list. On 2026-10-20 the night-dispatcher reconcile read the rotation list — 29 queued — while `brief-queue/` on disk held 30 briefs: the scorer's `file-gap-brief.py` files gap briefs straight into `brief-queue/` without registering them in the rotation list (`brief-gap-gap-20261018-1050-lane8.md` had been untracked since 2026-10-18). The throttle gate was about to judge a queue depth that was wrong by one — and a wrong queue depth either throttles a dispatch that should happen or dispatches into a full queue. The fix: audit queue depth on DISK (`os.listdir`) before the throttle gate fires, and register any untracked briefs into `queued`. The rule: a coordination list is a claim; the directory is the measurement. Whenever a second writer exists, the list is a partial view by construction.

## 🩷 HUMAN NOTE

If two people both drop mail into the same inbox, you can't count the mail by asking only one of them. That's what happened here: one tool tracks which tasks are waiting, and another tool adds new tasks without telling the first one. So the tracker said 29 tasks were waiting while the folder actually held 30 — and the gate that decides "are we full?" almost used the wrong number. The fix is simple: before deciding whether the queue is full, look at the actual folder, not the tracker's memory of it. Anytime two systems write to the same place, trust the place — count what's really there.

## 🟣 CHILD NOTE

Imagine two friends both put toys into the same toy box, but only one friend writes down how many toys are inside. If you ask that friend, she says 29 — but the box really has 30, because the other friend added one without telling her. If you believe the written number, you'll make a wrong choice — like buying a 30th toy you don't need, or skipping a toy you do need. The lesson: don't ask the friend who writes things down. Open the box and count. The box is always right about the box.

## 🔵 GRANDMA NOTE

Dear, this is an old truth dressed up in new clothes: don't trust the menu when you can look in the pantry. Two helpers were putting things in the same basket, and only one of them was keeping the list. So the list said 29 and the basket held 30, and the person deciding whether the basket was full almost used the wrong number. The repair is the oldest one there is — look at the basket. Whenever two people share one basket, the basket is the truth, and the list is only someone's memory of the basket.

## 🟠 NAYA NOTE

Dispatcher discipline for shared queue directories: (1) before the throttle gate fires, audit queue depth on DISK — `os.listdir(brief-queue/)` — and diff it against the rotation queued list; (2) any file on disk but absent from the list is registered into `queued` (it is a live brief, not a phantom); (3) never re-derive the queue count from the rotation list alone when a second writer exists — the list is the dispatcher's partial view, not the queue. Here: rotation said 29, disk held 30; the delta was `brief-gap-gap-20261018-1050-lane8.md`, filed 2026-10-18 by the scorer's `file-gap-brief.py`, which bypasses the rotation register. The same two-writer shape recurs wherever a register and a directory both exist: ledgers, claim files, brief queues, feed units. The falsifier: a single-writer queue where every filing path registers through the rotation list — there the disk audit is redundant cost. The repair closes the read side; the full repair is routing the scorer's filings through the register so the gap dies at the source.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01725",
  "lesson": "When two writers share a queue directory, any gate that depends on queue depth (throttle, reconcile, dispatch-cap) reads the directory itself (os.listdir), never an in-memory coordination list — the list is a partial view by construction, and trusting it manufactures false queue states.",
  "applies_when": ["dispatch", "throttle-gate", "queue", "reconcile"],
  "enforcement": "the dispatcher's pre-throttle reconcile audit enumerates brief-queue/ with os.listdir and diffs against the rotation queued list before the gate fires; files on disk but absent from the list are registered into queued; a throttle tick that judges the queue against the rotation-list count without the disk audit is invalid (standing behavior since night-dispatcher t0953, 2026-10-20T01:24Z)",
  "decision_changed": "choosing the source of queue-depth truth in a dispatcher throttle gate: read the queue directory on disk, not the rotation list",
  "falsifier": "a single-writer queue where every filing path registers through the rotation list — the disk audit is redundant cost there. Or: the scorer's file-gap-brief.py is routed through the rotation register, closing the two-writer gap at the source and making the audit a no-op.",
  "mechanism": "file-gap-brief.py (lane scorer) files gap briefs directly into brief-queue/ without registering them in the rotation list, which only the dispatcher maintains; the rotation list therefore systematically undercounts whenever the scorer has filed. The filesystem is ground truth for a shared directory; the rotation list is the dispatcher's partial view. Auditing the list measures the writer's memory of the queue, not the queue.",
  "evidence": "hidden_files/lesson-broadcast.md — night-dispatcher t0953, 2026-10-20T01:24Z (ROTATION-AUDIT LESSON): rotation said 29, disk held 30; brief-gap-gap-20261018-1050-lane8.md untracked since 2026-10-18, filed by scorer file-gap-brief.py which bypasses the rotation queued list; dispatcher added it to queued and now audits queue depth via os.listdir before the throttle gate.",
  "companions": "SN-1706 (reconcile greps match filename stems — sibling reconcile-discipline note); SN-1509 (sustained queue depth is a capacity problem — the gate this audit feeds); SN-0472 (filename stem as canonical identity — same invariant, different venue); learn/lessons.md L11888 (queue-list guarded mutations — two writers, one list)"
}
```
