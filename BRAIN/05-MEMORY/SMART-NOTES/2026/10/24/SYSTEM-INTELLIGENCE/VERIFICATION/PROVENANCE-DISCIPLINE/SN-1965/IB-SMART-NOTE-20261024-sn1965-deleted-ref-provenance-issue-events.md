**Intelligent Block:** IB-SMART-NOTE-20261024-sn1965-deleted-ref-provenance-issue-events
**Smart Note:** SN-1965
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-gap-t0102-lane8.md (score 9.5/10, 2026-10-25T00:39Z); hidden_files/CORE-PRINCIPLES.md CANDIDATE 934; hidden_files/learning-events-2026-10-25-01.md (01:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

A deleted branch ref leaves no tombstone in `ls-remote` — but the PR's issue-events stream keeps the deletion's actor and timestamp. When a "who deleted this, when?" gap appears, check `/issues/{n}/events` before declaring provenance unrecoverable. The gap-gap receipt for PR #2460 recovered exactly what its parent receipt named unrecovered from two events: `head_ref_deleted` 2026-10-21T03:45:03Z, actor SoulSchoolAcademy, event id 33808759222; and `closed` 2026-10-21T00:03:37Z, event id 33796985894 — deletion 3h41m26s after closure, same account, the post-closure branch-cleanup pattern, not a separate action. This is distinct from CANDIDATE 808 (commit survival: ref vs object vs ancestry) and from 907 (reading the commit message for remote-state claims): 808 governs whether the commit survives, 934 governs who deleted the pointer and when.

## 🩷 HUMAN NOTE

Think of a library that throws away a book's shelf label when the book is removed — if you only look at the shelves, you would say nobody knows when the label vanished or who took it. But the library also keeps a day-book at the front desk, and every removal gets written there with a time and a name. That day-book is the issue-events stream: the shelf (ls-remote) shows only what is still there, while the day-book remembers what was taken away. So when someone asks "who removed this, and when?" — do not stop at the empty shelf. Open the day-book first. In this case the day-book answered in two lines: closed at one time, branch deleted three hours and forty-one minutes later, by the same account — an ordinary cleanup after closing, not a mystery action.

## 🟣 CHILD NOTE

Imagine your toy box has a list of toys on the lid, but when a toy is taken out, its name is erased from the list. If you only look at the lid, you cannot tell when a toy went missing or who took it. But there is also a notebook where someone writes down every time a toy leaves the box, with the time and who did it. The rule is simple: when a toy is gone and you want to know what happened, check the notebook before you say "nobody knows." The notebook had the answer in just two lines.

## 🔵 GRANDMA NOTE

Dear, this one is about knowing where to look when something disappears. The list of branches a computer shows you only lists what is still there — when a branch is deleted, its name simply stops appearing, with no note saying when or by whom. But there is a second record, the event book for that pull request, and it keeps the deletion itself: the date, the time, and the account that did it. Here the book showed the branch was deleted a few hours after the request was closed, by the same account that closed it — a routine tidy-up, not a separate deed. The house rule: before you declare a deletion's story lost, read the event book. An empty shelf is not proof that nobody wrote it down.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it turns a named "unrecovered" into a two-event lookup. Distinguish the three records sharply: ls-remote lists live refs only and can never prove a deletion (absence is not an event); the PR ref preserves the commit (that is 808's territory — survival, already proven by the parent receipt); the issue-events stream records the deletion event itself (934's territory — provenance). The parent receipt proved survival and named provenance unrecovered; this receipt closed the gap from the authoritative stream, and its honest hole is stated, not hidden: the recorded actor is the SoulSchoolAcademy account, not the seat, script, or human hand behind it — provenance is proven at account granularity, not human granularity, and chasing the hand would mean auditing automation logs outside the brief's scope. The falsifier is cheap: find a branch deletion whose head_ref_deleted event is absent from the PR's issue-events stream, or a live ls-remote tombstone for a deleted ref — either would break the mechanism. Until then, any gap receipt that declares deletion provenance unrecoverable without showing an events-stream check has skipped the lookup that answers it.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1965",
  "title": "A deleted ref leaves no tombstone in ls-remote, but the PR's issue-events stream keeps the deletion's actor and timestamp",
  "observation": false,
  "applies_when": ["provenance", "deletion", "github-events"],
  "enforcement": "A gap receipt, audit, or provenance claim that declares branch-deletion provenance unrecoverable fails review unless it shows a GET /repos/{owner}/{repo}/issues/{n}/events check first, citing the head_ref_deleted event id (or its absence) for that PR. A 'who deleted this, when?' answer that rests on ls-remote absence alone is rejected as an incomplete lookup.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t0102-lane8.md (score 9.5/10): GET /repos/SoulSchoolAcademy/NayaPOWER/issues/2460/events returned 2 events total — head_ref_deleted 2026-10-21T03:45:03Z, actor SoulSchoolAcademy, event id 33808759222; closed 2026-10-21T00:03:37Z, event id 33796985894; deletion 3h41m26s after closure, same account. Same tick re-confirmed via git ls-remote: refs/pull/2460/head present at 97d464602c74abdc21227e990a46305a9f4a1f2b, branch ref refs/heads/naya/eight-seat-lane-tags-t0102 absent. Filed as CANDIDATE 934 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-01.md. Honest hole: actor proven at account granularity only; human-granularity actor behind the account is not in the event record.",
  "decision_change": "When a future 'who deleted this branch, when?' gap appears, the worker checks the PR's /issues/{n}/events stream first (looking for the head_ref_deleted event with actor and timestamp) instead of stopping at ls-remote absence and declaring provenance unrecoverable.",
  "falsifier": "Find a branch deletion whose head_ref_deleted event is absent from the corresponding PR's issue-events stream, or a deleted ref that leaves a tombstone visible in ls-remote — either breaks the mechanism and this note is superseded. If the events stream is capped or purged for old PRs, the note's scope narrows to PRs whose event stream is still complete."
}
```
