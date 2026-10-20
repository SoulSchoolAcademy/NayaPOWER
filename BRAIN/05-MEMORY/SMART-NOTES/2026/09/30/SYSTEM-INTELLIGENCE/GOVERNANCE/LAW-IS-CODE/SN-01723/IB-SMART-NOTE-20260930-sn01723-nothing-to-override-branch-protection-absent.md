# IB-SMART-NOTE-20260930-sn01723

**Intelligent Block:** SN-01723
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #2400 merged with 5 red checks and 0 reviews — and the merge mechanism is now closed with bytes: the org-owner account clicked the normal squash-merge button 80 seconds after the final push. No admin override was needed because there was nothing to override: GET /branches/main/protection returns 404 — branch protection on main is absent, so no required-status-check machinery stood in the way. The Scorecard Law gates fire correctly as check runs, but check runs are advisory; enforcement lives in branch protection settings, not in greenness. Red checks stop nobody when protection is absent.

## 🩷 HUMAN NOTE

A guard that can be walked around isn't a guard. The team had all the right gates — they checked every pull request and lit up red when the law was violated. But the door they were supposed to guard was standing open: on this repo the merge button works for anyone with push access unless the repo is configured to require green checks first. So the rules were enforced in the report but not at the door. Greenness is a measurement; protection is the enforcement. One without the other is decoration.

## 🟣 CHILD NOTE

Imagine a clubhouse with a big sign on the door that says "You may ONLY enter if the hall monitor gives you a green stamp." But the door itself has no lock — anyone can walk in. The monitor stamps red, the sign stays up, and people walk in anyway. The stamp didn't fail; the door was never locked. If you want the rule to work, you have to put a lock on the door that only opens for green stamps. The sign alone isn't enough.

## 🔵 GRANDMA NOTE

Dear, it's like hanging a "no entry" sign on a gate with no latch. The team built all the right alarms — they rang every time a bad pull request came through. But nobody connected the alarm to the door: the repo was never set to require the alarms to be quiet before the door opens. So the person with the keys walked straight through five ringing alarms, and that was allowed. A check that reports is not a check that protects — the wiring is the whole of it.

## 🟠 NAYA NOTE

When a PR merges with red checks, don't start at "who overrode the gate" — start at "was there a gate?" The enforcement chain: (1) read branch protection on main — `GET /repos/{owner}/{repo}/branches/main/protection`; a 404 means absent, no required checks exist; (2) only then read the check runs. If protection is absent, "no admin override was needed because there was nothing to override" — the merge button executes for any account with push access regardless of red runs. Compliance verdict from the byte-closure: the Scorecard Law gates are advisory check runs with no branch-protection wiring; owner merges cannot be stopped by them. Next action (dispatcher): record the enforcement-gap root cause and decide — (i) branch protection on main marking the 4 process gates + test as required, or (ii) a Shawn-gated ratification that advisory gates are the intended design. Related: SN-0631 (a guard not on the write path is a suggestion); SN-0435 (law-is-code's four links: write, wire, prove, cite).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01723",
  "lesson": "Red check runs do not stop a merge when branch protection is absent: required-status-check enforcement lives in branch protection settings, not in check-run greenness; an owner merge needed no admin override because there was nothing to override.",
  "applies_when": ["merge", "enforcement", "branch-protection", "required-checks"],
  "enforcement": "standing check: GET /repos/{owner}/{repo}/branches/main/protection must not 404 AND must list the Scorecard Law gates as required status checks; if it 404s or the required list omits the gates, the enforcement gap is back and the dispatcher's decision (branch protection vs Shawn-gated ratification that advisory is intended) must be re-opened",
  "decision_changed": "evaluating any 'merged with red checks' event: read branch protection first, check runs second; and the dispatcher's standing decision — (i) protect main with the 4 process gates + test as required, or (ii) a Shawn-gated ratification that advisory gates are the intended design",
  "falsifier": "the org audit log showing branch protection present on 2026-10-12 would falsify 'nothing to override' (the receipt marks point-in-time absence as current-state only, unproven for 2026-10-12); a future merge 405 naming a required check would prove protection is now live",
  "mechanism": "GitHub enforces merge eligibility in branch protection settings (required status checks); check runs are reports, not enforcement points. On an unprotected branch the merge button executes for any account with push access regardless of red runs — no override privilege is consulted because no requirement exists to override.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t1032-lane4.md (2026-10-20 08:38-09:05 UTC, 9.0/10, Lane 4 Mason hat): PR #2400 state=closed merged=true, merged_at=2026-10-12T03:59:07Z, merged_by=SoulSchoolAcademy (User), auto_merge=null, merge_commit_sha=597803d8c79ec256a268c4ba1c33562d3c8a0b4f (squash, single parent), 0 reviews, exactly 2 issue events (merged+closed, same actor/timestamp), final push 03:57:47Z -> merge 03:59:07Z (80s, plain squash button); GET /branches/main/protection -> 404 'Branch not protected' (current state). Compliance verdict: Scorecard Law gates are advisory check runs with no branch-protection wiring; owner merges cannot be stopped by them. Caveat: point-in-time absence on 2026-10-12 unproven (org audit log out of scope).",
  "companions": "SN-0631 (a guard not on the write path is a suggestion); SN-0435 (law-is-code four links: write, wire, prove, cite); SN-01545 (filing-gate enforcement-or-bounce)"
}
```
