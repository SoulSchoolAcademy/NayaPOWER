# IB-SMART-NOTE-20260930-sn01396-merge-flow-doctrine

Intelligent Block: YES
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Author: Naya Clarity Narzan (from Shawn Vibert's direct teaching + live deep dive, 2026-10-15 ~07:00–07:30 PDT)

## IN A NUTSHELL

Merges jam for three reasons: real conflicts nobody triaged, protections that misfire, and clean PRs nobody executes. The fix: triage the merge state first (dirty/blocked/behind), keep only the load-bearing gates blocking, make everything else advisory, and give the dock one law — no clean PR sits. Protection must never cost more than the work it protects.

## HUMAN NOTE

Shawn's teaching (2026-10-15): a merge system needs balance — protection on one side, the work getting done on the other. Fourteen checks before a merge is protection theater if three failing ones block work that needs to ship. Speed and safety are always in tension; the system has to be effective AND efficient, or the bottleneck just moves.

The deep dive found all three jam classes live. First, real conflicts misdiagnosed: PR #2620 sat 5+ hours while the team chased a "check not delivered" ghost — a local test-merge proved the true blocker was merge conflicts in three generated index files. Nobody read the merge state first. Second, protections that misfire: the consensus gate re-fires on every comment, so its verdict flips as discussion happens — #2634 "failed" then "passed" 90 minutes later with zero code change because the review arrived late. It felt flaky; it was late evidence. Third, clean PRs nobody executes: #2625 sat green and mergeable for 3 hours because no one owned pressing merge. The dock didn't exist as a job, only as a word.

The doctrine. Triage order is law: read mergeable_state first — dirty means conflicts (resolve them), blocked means a required check is red (read its reason), behind means rebase. Never chase check delivery on a dirty PR. Protection balance: exactly two gates block (the receipt pin and the consensus gate — they're the load-bearing ones); the other ~14 checks stay informational and can never block. The consensus gate should judge each head SHA once, not re-litigate on every comment. Generated index files should never be committed on branches — regenerate at merge time, or the #2620 class recurs forever. And the dock's law: a clean PR merges within the hour; a sitting clean PR is the dock's failure, measured.

Proof it works: the dive resolved #2620's conflicts (branch side byte-verified, pushed, PR flipped dirty→awaiting re-score), and #2625 + #2634 merged the same hour under the protocol's own authorization (green gates = the authorization; Shawn's "unjam the merges" = the direction).

## CHILD NOTE

When a merge is stuck, look at WHY it's stuck first — is it conflicting, is a check red, or is it just sitting there? Don't guess. Keep only the important safety checks as blockers; the rest are just advice. And if a merge is ready, merge it — don't let it sit.

## GRANDMA NOTE

Locks on the door are good, but if the locks are so complicated nobody can get in and out, you've locked yourself out of your own house. Keep the two locks that matter, make the rest just warning bells, and always check whether the door is actually stuck before blaming the locks.

## NAYA NOTE

Operational procedure for the merge seam. Triage (2 minutes): `mergeable_state` → dirty: resolve conflicts (generated files: regenerate via the repo tooling, never hand-edit; verify the regenerated side's blob SHAs against branch content before taking it); blocked: identify the failing required check and read its reason (stale head pin → re-score; missing review/scorecard → collect; genuine red → fix); behind: rebase. Protection budget: REQUIRED = receipt-pin gate + consensus gate; INFORMATIONAL = everything else, never blocking. Consensus verdicts are per-head-SHA and sticky — a comment re-fire must not flip a decided head. Generated files (brain indexes, real-tree) are merge-time artifacts: branches must not commit them; the merge path regenerates. Dock SLA: clean PR merged within 1 hour of going clean; every sitting clean PR is named in the next tick with its age. Watchdog: a required check unreported 30 min after push pages the dock (distinguishes GitHub delivery failure from our failure).

## MACHINE NOTE

```json
{
  "sn": "SN-01396",
  "lesson": "merge-flow-doctrine",
  "source": "shawn-vibert-direct-teaching-2026-10-15 + live deep dive",
  "rule": "triage mergeable_state first (dirty/blocked/behind); only receipt-pin + consensus gates block; consensus verdict sticky per head SHA; generated files are merge-time artifacts; dock SLA 1h on clean PRs",
  "protection_balance": "2 blocking gates (load-bearing), ~14 informational (never blocking); a protection that costs more than the work it protects is a bug",
  "jam_classes": {
    "misdiagnosed-conflict": {"example": "#2620: 5h chasing check delivery, true cause = conflicts in 3 generated index files", "fix": "triage state first; regenerate, byte-verify, take branch side"},
    "late-evidence-flap": {"example": "#2634: gate failed then passed, same head, review arrived between", "fix": "sticky per-SHA verdicts; expect red between push and evidence"},
    "unexecuted-clean": {"example": "#2625: green 3h, nobody merged", "fix": "dock owns execution; sitting clean PR = dock failure"}
  },
  "decision_change": "before any merge debugging, read mergeable_state; before adding any new required check, name the work it protects and its cost",
  "falsifier": "a PR merges faster with more required checks; or a jam clears without triaging the merge state",
  "mechanism": "theory of constraints applied to the merge seam; protection theater vs load-bearing gates",
  "evidence": ["PR #2620 local test-merge 2026-10-15", "PR #2625/#2634 merges a9d23662/f45e41e1", "16 check runs on 6e939c5ca", "merge-consensus-gate.yml issue_comment trigger"]
}
```
