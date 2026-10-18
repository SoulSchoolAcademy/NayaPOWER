# The Author Cannot Review: Check Authorship at Claim Time, Not Mid-Run

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1584-author-cannot-review-claim-time-authorship-check
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/t0801-lane11.md (Naya Clarity Narzan, Lane 11 Heart — RECUSAL receipt, 00:38Z): claimed the #2738 independent 3-pass review brief (00:14Z), discovered mid-run she is the PR's author (`Seat: Naya Clarity Narzan` in the body), recused, re-filed the brief OPEN for a non-author seat; board post #2721 comment 6243773041 (HOLD + recusal). Receipt's fix (L45): "dispatcher authorship pre-check: compare the brief assignee's seat against the PR body's Seat declaration BEFORE dispatch."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya Clarity claimed the independent-review brief for PR #2738, ran for 24 minutes, then discovered she is the PR's author and recused — the review was impossible from her seat, the run was wasted, and the brief had to be re-filed OPEN. The authorship check happened mid-run; it belongs at claim time. Rule: before a review brief is dispatched or claimed, compare the assignee's seat against the PR body's author declaration; on a match, refuse the claim and re-file for an eligible seat. A review written by the author is a false certification — the exact class the merge-receipt watch (FM#32) exists to catch. The seat's honest move was recusal + re-file (per the t0813/t0413 precedent), but the machinery should have caught it first: a gate that fires only after the run burns is a gate placed too late. (Complements SN-1581: that note is about making routing gates machine-visible at file time; this one is about the claim path checking authorship itself.)

Why this is brain-grade: review integrity is load-bearing for the whole merge protocol — one self-reviewed PR that Shawn or the team later discovers poisons trust in every scorecard. The failure mode is cheap to prevent (a string comparison at claim time) and expensive to discover late (wasted run + re-file + a false-certification near-miss). Authorship is knowable at dispatch; the check must bind to the claim, not to mid-run luck.

## 🩷 HUMAN NOTE

Shawn — a process fix from tonight's review work. I picked up a brief to independently review PR #2738, worked it for a while, and then found out I'm the one who wrote the PR. I can't independently review my own work — that would be grading my own exam — so I recused myself and put the brief back in the queue for someone eligible.

The lesson isn't the recusal (that was the right move); it's that nobody checked before I started. The rule going forward: before a review job is handed out or claimed, we compare the reviewer against the PR's author declaration. If it's the same seat, the claim is refused and the job goes back in the queue — before any work burns. The check belongs at the door, not in the middle of the room.

## 🟣 CHILD NOTE

Imagine you wrote a test at school, and then the teacher asked YOU to grade it. That's not fair to anyone — you'd want to give yourself a good grade. The rule is simple: the person who wrote it can't be the person who grades it. And the smart move is to check that before anyone starts grading, not halfway through — so nobody wastes time doing a job they were never allowed to do.

## 👵 GRANDMA NOTE

You never ask the cook to judge her own dish at the county fair — that's why there are judges. And you don't wait until she's plated it to remember. The fair has one rule that matters: check who's cooking before you hand out the judging badge. Put the check at the door, and nobody's time gets wasted.

## 🧠 NAYA NOTE

The recusal itself followed the t0813/t0413 precedent correctly — the failure was upstream: the claim path had no authorship binding. Two systemic findings ride along and stay open: (1) the gate's seat registry can't parse the lead-qualified `Seat: Naya Clarity Narzan` form, so it fails closed on the naming law — needs reconciliation (dual-form `Seat: Naya 4 — Naya Clarity Narzan` or registry extension); (2) the brief's gate-surface claim was wrong, costing a full gate-source re-derivation. The dishonest move would have been an "independent" scorecard anyway; the honest move was the 7.8 HOLD. The machinery upgrade named in the receipt — dispatcher authorship pre-check before dispatch — is the enforcement that makes this lesson load-bearing instead of advisory.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1584",
  "applies_when": ["review", "assignment", "merge", "receipt", "brief", "claim", "scorecard"],
  "enforcement": "Dispatcher/claim-path authorship pre-check (named in t0801-lane11 receipt L45): before dispatch or claim, compare the brief assignee's seat against the PR body's Seat/author declaration; on a match, the claim is refused and the brief is re-filed OPEN for a non-author seat. Recorded in the claim receipt; the merge-receipt watch (FM#32) stays as the downstream detector for any self-review that slips through.",
  "falsifier": "Scored evidence that author-reviewers produce verdicts indistinguishable from independent reviewers (no bias) would demote this from gate to advisory.",
  "mechanism": "Authorship is a stake in the outcome; review integrity requires independence; the check failed because it bound to mid-run discovery instead of the claim.",
  "decision_change": "Review briefs are never dispatched to or claimed by the authoring seat; the authorship comparison runs at claim time.",
  "related": ["SN-1575", "SN-1581"],
  "provenance": "hidden_files/twelve-lane-receipts/t0801-lane11.md (L1-5, L19-23, L45); #2721 comment 6243773041"
}
```
