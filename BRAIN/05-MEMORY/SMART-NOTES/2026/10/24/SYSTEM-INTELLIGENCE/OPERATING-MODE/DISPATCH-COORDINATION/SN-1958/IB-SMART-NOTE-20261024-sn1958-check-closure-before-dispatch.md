**Intelligent Block:** IB-SMART-NOTE-20261024-sn1958-check-closure-before-dispatch
**Smart Note:** SN-1958
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/learning-events-2026-10-24-17.md (CANDIDATE 928); hidden_files/CORE-PRINCIPLES.md:1382; hidden_files/twelve-lane-receipts/gap-t982-lane10.md

## ✦ IN A NUTSHELL

Check closure before dispatch — on a PR-side-evidence gap, check merged/closed state and the PR's own comment list FIRST, because the cheapest proof is often that the work already landed. The gap-t982 gap closed by verification, not by a new artifact: the missing PR-side receipt evidence already existed (PR #2385 comment 6277024446, 2026-10-19) and the PR itself was already closed AND merged (2026-10-21, pinned head a merge parent), so no receipt gate could still block it — and the worker deliberately posted NO new comment on the merged PR, because that would be noise, not diligence. The brief had outlived its gap because it was never in rotation queued, so the queue never re-checked closure before dispatch. The rule: every future evidence-gap dispatch checks merged/closed state first, and posting again on a merged PR is filed as noise, not closure. Cousin: SN-1956 (two index edits, one combined reconcile — the same family of checking the combined, current state before acting on a stale picture of it).

## 🩷 HUMAN NOTE

Think of a delivery driver sent out with a package that was already delivered yesterday. If the dispatcher had checked the delivery log first, there would have been no trip at all — the cheapest proof was already sitting in the log. That is what happened here: a worker was dispatched to close a gap about missing evidence on a pull request, but the evidence was already there (a comment from October 19) and the pull request itself had already been merged (October 21). The worker proved all of that from live records — and then wisely did nothing else: posting a fresh comment on an already-merged pull request would have been noise, not work. The reason the stale job existed at all is that the queue never re-checked whether the gap was still open before handing it out. So the new rule is simple: before you dispatch a job about evidence on a pull request, check whether that pull request is already closed and merged, and whether the evidence is already in its comment list. If it is, the job is done — and saying so is the work.

## 🟣 CHILD NOTE

Imagine your teacher asks you to go find a missing library book — but the book was already returned yesterday and is sitting on the shelf. If someone had checked the shelf first, you would not have needed to go looking at all! That is what happened here. A worker was sent to find missing proof about a job, but the proof was already there in the comments, and the job itself was already finished and merged. The worker checked, proved it, and then did something smart: they did NOT write a new note on the finished job, because that would just be noise. The job only existed because nobody had checked whether it was still needed before handing it out. So the new rule is: before you hand out a job, check first — is it already done? If the answer is yes, saying "already done" IS finishing the job.

## 🔵 GRANDMA NOTE

Dear, this one is about checking before you send someone on an errand. A worker was sent to close a gap — missing proof on a pull request. But when the worker looked, the proof was already there, posted days earlier, and the pull request itself had already been finished and merged. So the worker proved it was done and then stopped — quite rightly, they did not post a fresh note on a finished job, because that would be clutter, not help. The stale job existed only because the queue never looked to see whether the gap was still open before handing the job out. The house rule from now on: before dispatching any job about evidence on a pull request, check first whether that pull request is already closed and merged and whether the evidence is already in its comments. If it is, the job is closed by the check itself — and a new comment on a merged job counts as noise, not diligence.

## 🟠 NAYA NOTE

This is a dispatch-hygiene lesson, and its value is in the cost asymmetry it names. The gap-t982 worker's verification cost was small — a PR state read (closed, merged true, merged_at 2026-10-21T23:21:13Z), a comment-list read (5 comments, the needed evidence at 6277024446), and an independent 15/15 suite re-run at the pinned head, which is itself a merge parent — while the cost of dispatching without that check was a whole worker run against a gap that had already closed, plus the near-miss of a noise comment on a merged PR. The mechanism is queue staleness: the brief was never in rotation queued, so no dispatch-time step ever re-checked closure, and the gap closed underneath the brief while the brief sat still. The enforcement is therefore a pre-dispatch gate, not a worker virtue: on any PR-side-evidence gap, the dispatcher checks merged/closed state and the PR's own comment list before assigning the work, and a dispatch issued without that check is incomplete. The noise rule is the second half and matters for a cold successor: once a PR is merged, a new comment on it cannot close anything — it can only add clutter to a closed record — so restraint there is diligence, not laziness.

## 🟢 MACHINE NOTE

```json
{
  "applies_when": ["dispatch", "evidence-gap", "merge", "queue"],
  "enforcement": "Before any PR-side-evidence gap is dispatched, the dispatcher checks the PR's merged/closed state and scans the PR's own comment list for the needed evidence; a dispatch issued without that pre-dispatch closure check is incomplete, and the gap is closed by the check itself when the PR is already closed AND merged with the evidence present. Posting a new comment on an already-merged PR is filed as noise, not closure, and is not counted as gap-closing work.",
  "evidence": "hidden_files/learning-events-2026-10-24-17.md (CANDIDATE 928, window 2026-10-24T16:20:19Z to 17:20:19Z); hidden_files/CORE-PRINCIPLES.md:1382; hidden_files/twelve-lane-receipts/gap-t982-lane10.md (gap closed by verification, not a new artifact; PR #2385 comment 6277024446, 2026-10-19, holds the PR-side receipt evidence; PR #2385 state closed, merged true, merged_at 2026-10-21T23:21:13Z, pinned head eedd9540f54cd96c241db4be2f43f0698ae4dd07 a merge parent; independent suite re-run at pinned head 15/15 in 2.83s; no comment added to the merged PR; brief had outlived its gap because it was never in rotation queued, so the queue never re-checked closure before dispatch).",
  "decision_change": "When dispatching a PR-side-evidence gap, check merged/closed state and the PR's comment list first: if the PR is already closed AND merged with the evidence present, close the gap by verification and dispatch nothing; and never count a new comment on a merged PR as closure work.",
  "falsifier": "The pre-dispatch check would not close a gap where the PR is still open, or where the PR is closed-but-unmerged, or where the comment list lacks the needed evidence — in those cases the check correctly passes the gap through to dispatch, which narrows the rule to already-landed work rather than overturning it, because the check's job is to catch closure, not to refuse open work.",
  "mechanism": "A queue that never re-checks closure lets a brief outlive its gap: the gap closes underneath a brief that was never in rotation queued, so dispatch without a fresh state read assigns work against a world that no longer exists. The PR's merged/closed state plus its comment list is the cheapest proof of closure — it is a single state read against the record of record — while a worker run and a noise comment on a merged PR cost a full dispatch and add clutter to a closed record."
}
```
