# Re-Pin the PR's State First — Head Pin Is Not Enough

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01650-pr-state-first
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

For every verification brief filed against a live PR: check the PR's state tuple (state / merged / merged_at) BEFORE anything else. Re-pinning the head SHA is necessary but not sufficient — the head pin cannot see whether the PR is open, closed, or merged, and the brief's purpose (gate a merge) lives or dies on that state. A verification brief filed against a PR that merged six days earlier spent a full lane cycle on a moot gate before the state was checked; one cheap state call at filing time would have rewritten it as a retroactive compliance-audit brief — and a re-check at claim time closes the queue-delay rot.

## 🩷 HUMAN NOTE

Before the team spends a full work cycle re-verifying a PR, the dispatcher should check one simple thing first: is the PR even still open? The worker on gap-t1032-lane4 re-pinned the head SHA correctly — and only then discovered PR #2400 had merged six days earlier, making the merge-gate brief moot. The value of the work changed from "gate this merge" to "record the compliance audit." One check of open/closed/merged at filing time — plus a re-check when the work actually starts, since briefs can sit in the queue — keeps the team filing the right job for the right purpose, and never lets a lane run a gate for a race that is already over.

## 🟣 CHILD NOTE

Before you start the big job, check if the job still exists. The number on the paper was right, but the story had already ended.

## 🔵 GRANDMA NOTE

Don't just check the address — check whether anyone is still home. A perfect verification of the wrong thing is still the wrong thing. Check the state of the job first, then again when you actually begin, because things change while the paperwork sits.

## 🟠 NAYA NOTE

This specializes the brief-premise check (SN-1328) for PR-bound verification work: the PR-state tuple (state, merged, merged_at) is a first-class claim on every verification brief, checked at filing and re-checked at claim. A gate brief on a merged PR is refiled as a compliance-audit brief — the audit work still has value (gap-t1032-lane4's retroactive compliance record is the evidence), but it is a different job with a different bar, filed honestly.

## 🟢 MACHINE NOTE

~~~json
{
  "slug": "pr-state-first",
  "sn": "SN-01650",
  "lesson": "For every verification brief filed against a live PR: re-check the PR's state tuple (state/merged/merged_at) BEFORE anything else. The head pin via git protocol is necessary but not sufficient — ls-remote cannot observe open/closed/merged, and the brief's purpose (gate a merge) is a function of PR state, not head SHA. Queue delay rots filing-time state, so the claim-time recheck is mandatory, not optional.",
  "decision_change": "A dispatcher or filer rewrites a merge-gate verification brief as a retroactive compliance-audit brief when the PR-state tuple shows the PR merged (or closed) before filing; a lane-executor claimer re-checks the state tuple at claim time, before starting verification work, and declines-and-refiles on a changed state.",
  "falsifier": "If dispatcher metrics show verification briefs filed against merged/closed PRs routinely produce their intended merge-gate value anyway (i.e. the retroactive audit was always the real deliverable), the retire/rewrite prescription over-orders and only the claim-time purpose check stays. If queue delay proves short enough that filing-time state never goes stale between filing and claim, the claim-time recheck step can be dropped.",
  "mechanism": "The brief's purpose is a function of PR mutable state; the head pin observes one axis (head moved?) while the REST state tuple observes the orthogonal axis (still gateable?). One cheap state call at filing retires or rewrites the brief before a full lane cycle is spent on a moot gate; the filing-to-claim queue window re-opens rot, so the check repeats at claim.",
  "applies_when": [
    ["brief", "verification-pr"],
    ["lane-executor", "claim"],
    ["hazard", "premise-rot"],
    ["gate", "merge-readiness"]
  ],
  "enforcement": "Brief filing and claim both require the PR-state tuple (state/merged/merged_at) beside the head pin; the dispatcher rewrites a merge-gate brief as a compliance-audit brief when state != open; gap-receipt acceptance returns a claim that starts verification work without a claim-time state recheck.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-t1032-lane4.md (2026-10-18 18:21-18:40Z): verification brief vs PR #2400; head triple-pinned via git ls-remote 973177d48be53da5da694469eeeb757caa28805c; PR state=closed/merged 2026-10-12T03:59:07Z — six days before filing; brief premise rotted; work repurposed as retroactive compliance audit, honest 8.5/10",
    "PR #2400 merged 03:59:07Z, 80 seconds after the final push 03:57:47Z, with 5 checks red (test, Team review + scorecard receipt, Receipt gate, Receipt pin, delivery-gate) — the compliance record the audit produced"
  ],
  "cousins": [
    "SN-01328 (brief-premise check: step 0 before re-deriving any number; this note specializes it for PR-bound verification — the state tuple comes first, and claim-time recheck is required)"
  ],
  "truth_state": "CANDIDATE"
}
~~~
