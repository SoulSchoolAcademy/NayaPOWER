**Intelligent Block:** IB-SMART-NOTE-20261025-sn1977-check-merged-pr-reviews-before-unknown
**Smart Note:** SN-1977
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-gap-t0112-lane9.md (self 9.0/10), review copies SHA-pinned in hidden_files/gap-gap-t0112-lane9/; hidden_files/CORE-PRINCIPLES.md CANDIDATE 945; hidden_files/learning-events-2026-10-25-06.md (06:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

Check a merged PR's contemporaneous reviews before declaring anything about it unknown. The "unknown" CI pytest set was already named on PR #2462 itself: two independent reviews dated the merge day — Lane 8 comment 6122317726 and Lane 10 comment 6122636824 — each name the same 7 failing tests with byte-identical tip-vs-head signatures. The answer was sitting in the PR's own review thread while the investigation called the set unknown. The rule: any future unknown-declaration about a merged PR consults that PR's own review comments first, or records that none exist.

## 🩷 HUMAN NOTE

Imagine searching the whole house for a letter that is sitting in the mailbox by the front door — and then telling everyone the letter is lost. That is what happened here: the failing-test list was already written down twice, on the very PR being investigated, by two different reviewers on the day it merged. The investigation called the set "unknown" because it never opened the PR's own reviews. The rule is a habit, not a chore: before you say "unknown" about a merged PR, open its reviews. The people who were there at the time usually already wrote the answer down.

## 🟣 CHILD NOTE

Imagine you lose your homework and tell the teacher it is gone — but it is sitting in your own backpack, where you put it yesterday. Two reviewers wrote down the failing tests on the PR itself, on the day it merged, and the later search said "unknown" without ever looking there. So the rule is: before you say "I don't know," check your own backpack first. For a merged PR, the backpack is its review comments.

## 🔵 GRANDMA NOTE

Dear, this one is about looking in the obvious place first. When something about a finished job is declared unknown, the first place to look is the notes the workers left on the job itself — the reviews written when it merged. Here two reviewers, on the merge day, had each written down the same seven failing tests, matching each other exactly. The later hunt called the set unknown because it never read those notes. The house rule: no "unknown" about a merged PR until its own reviews have been read — or until it is recorded that it has none.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it makes "unknown" a checked claim rather than a default. The mechanism is contemporaneous record: reviewers at merge time observe the artifact under its own conditions, and two independent reviewers converging on the same 7 tests with byte-identical tip-vs-head signatures is a cross-checked record, not a rumor. The falsifier is measurable: if contemporaneous reviews on a measured set of merged PRs name failing sets that byte-level re-runs contradict more often than they confirm, reviews are not a reliable source and this note is superseded. Honest hole, stated not hidden: the reviews name the 7; whether CI's set was 7 or 32 still hinges on the unproven Oct-12 branch binary — the reviews settle the named set, not the CI set.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1977",
  "title": "Check a merged PR's contemporaneous reviews before declaring anything about it unknown",
  "observation": false,
  "applies_when": ["merge", "review", "verification"],
  "enforcement": "An unknown-declaration about a merged PR is returned by the lane scorer unless it cites that PR's own review comments or records that none exist; the PR's review thread is a required source for the declaration, not an optional one.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t0112-lane9.md (self 9.0/10), review copies SHA-pinned in hidden_files/gap-gap-t0112-lane9/: PR #2462 reviews Lane 8 comment 6122317726 and Lane 10 comment 6122636824, both dated the merge day, each name the same 7 failing tests with byte-identical tip-vs-head signatures. Filed as CANDIDATE 945 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-06.md. Honest scope: reviews name the 7; whether CI's set was 7 or 32 still hinges on the unproven Oct-12 branch binary.",
  "decision_change": "Before declaring anything about a merged PR unknown, the worker reads that PR's own review comments first (or records their absence); an unknown-declaration without that step is returned as unchecked.",
  "falsifier": "If contemporaneous reviews on a measured set of merged PRs name failing sets that byte-level re-runs contradict more often than they confirm, reviews are not a reliable source and this note is superseded."
}
```
