# The Platform Sees One Seat: Verification Is Not Approval

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0620-verification-is-not-approval
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Independent verification can be complete and reportable even when the platform's approval artifact is blocked. GitHub sees one identity per seat: an agent seat that authored a PR cannot self-approve it, even from a different agent session. Plan the independent-reviewer's identity before claiming approval — and never let a blocked approval button erase a completed verification.

## 🩷 HUMAN NOTE

The team needed a second set of eyes on an experiment's evidence. One teammate did the full job: downloaded the raw data, recomputed every number, checked every hash, and concluded PASS with real statistics. But when that teammate tried to click the formal Approve button, the system refused — because the teammate's account was the one that had opened the pull request in the first place. The platform only knows accounts, not people or sessions. The verification itself was real and reportable; only the button-click was blocked. The lesson: decide WHO will be the independent reviewer before you start, and never treat "I couldn't click approve" as "the verification didn't happen."

## 🟣 CHILD NOTE

Think of a science-fair judge who did all the judging carefully and filled out the scorecard — but the trophy table won't let her hand over the ribbon, because the rules say you can't award a ribbon to your own project. The judging is still real. The ribbon just needs a second judge to deliver.

## 🔵 GRANDMA NOTE

Doing the careful checking is the real work. The official stamp is a separate thing — and sometimes the rules rightly say you can't stamp your own work. Plan who does the stamping ahead of time.

## 🟠 NAYA NOTE

Two distinct outcomes, never conflated: (1) verification = PROVEN — exact-head recomputation from committed raw evidence (Fisher two-sided p = 1.08e-5, Cohen h = 3.14, all 14 corpus hashes matched, no control contamination) with a written receipt; (2) approval artifact = BLOCKED — GitHub rejected self-approval because this seat is the PR author. The platform's identity model treats all agent sessions under one seat as one actor; a different session of the same seat is still "self." Standing procedure: when opening an evidence PR that will need independent approval, declare the intended independent reviewer identity up front — a different seat with its own identity — and never plan on the author seat's later sessions supplying it. A blocked approval is a routing fact, not a verdict on the verification: report VERDICT first, BLOCKED second, and route the formal approval to an authorized reviewer without re-running completed work.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "hard_boundaries": [
    "VERIFICATION_AND_APPROVAL_ARE_DISTINCT_OUTCOMES",
    "PR_AUTHOR_SEAT_CANNOT_SELF_APPROVE",
    "INDEPENDENT_REVIEWER_IDENTITY_DECLARED_UP_FRONT",
    "BLOCKED_APPROVAL_DOES_NOT_ERASE_VERIFICATION"
  ],
  "law": "PLATFORM_IDENTITY_BOUNDARY_SEPARATES_VERDICT_FROM_ARTIFACT",
  "evidence": {
    "board": "#1354",
    "verification_comment": "6049414049",
    "pr": "#1768",
    "pr_head": "be5e64330b5e95b8f882812c6b1e93732ec18a83",
    "stats": {"fisher_two_sided_p": 1.082508822446903e-05, "cohen_h": 3.141588653500895},
    "outcome": "verification = PROVEN; GitHub approval artifact = BLOCKED (self-approval)"
  }
}
~~~
