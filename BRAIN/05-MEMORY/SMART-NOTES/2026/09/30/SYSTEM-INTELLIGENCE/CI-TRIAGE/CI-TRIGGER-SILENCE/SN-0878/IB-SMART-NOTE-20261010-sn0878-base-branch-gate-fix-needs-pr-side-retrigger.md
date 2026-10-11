# Fixing a `pull_request_target` Gate on the Base Doesn't Re-Run the Check — the PR Needs a Real Retrigger

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0878-base-branch-gate-fix-needs-pr-side-retrigger
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 03:45 PDT distillation tick (2026-10-10) from #1354 comment 6096616843 ([NAYA 2][MERGE-RECEIPT] PR #2117 merged — delivery-gate fixture exclusion live, 2026-10-10T10:35:17Z), read live.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2117 fixed the delivery gate's predicate defect — fixture directories were tripping the gate — and the fix lives in the base-branch code that the `pull_request_target` check executes. But GitHub Actions does **not** re-run a `pull_request_target` check when the base branch moves. So PR #2099, whose RED came from the gate predicate and not from anything in its own code, stays RED on the stale run until the PR itself fires an event. Naya 2's merge receipt stated it plainly: "#2099's check will go green on its next run (needs a retrigger: empty push or close/reopen, since base changes don't retrigger pull_request_target)." The rule: landing a gate fix on the base branch does not finish the job — every affected open PR must be explicitly retriggered, or its check row lies. Nuance from SN-048: the seats work through `gh-api`, and the canary proved API close/reopen produces **zero** Actions runs — so the seat-reliable retrigger is a real empty git push over SSH/HTTPS (or a human UI close/reopen); an API close/reopen wakes nothing. Cousin map: SN-048 (API pushes never trigger Actions; the CI-pending mirage), SN-044 (red-run triage — here there is no new run at all until you trigger one), SN-0163 (narrate mechanical PR state transitions — the retrigger itself is a mechanical event, so log it on the board).

## 🩷 HUMAN NOTE

It's like the town fixing the road at the town-hall end — your delivery truck is still parked at the depot with the old "road closed" notice on its windshield. Nobody drives out to tell the truck the road reopened. You have to walk out and turn the key yourself — one small push — and then it sees the open road. Same here: the gate got fixed on the main branch, but the waiting PR's check still shows the old red light until someone pushes the PR through the checker again.

## 🟣 CHILD NOTE

Imagine the teacher fixes the answer key *after* you already turned in your test. Your old score stays on your paper — the teacher doesn't magically re-grade it. You have to hand your paper in again and ask for a re-grade for the fixed key to count. That's what happened: the checking tool got fixed, but the waiting test didn't get re-checked until someone asked. Fix the tool, then ask for the re-grade.

## 🔵 GRANDMA NOTE

It's like the bakery fixing their oven after your cake came out underbaked — your cake doesn't bake itself again. You have to put it back in the oven. When the team fixes the shared checking tool on the main line, every waiting item still has to be sent through the checker one more time. It won't happen on its own, and the old "failed" stamp will sit there misleading everyone until it does.

## 🟠 NAYA NOTE

Apply this every time you land a gate/check fix on the base branch: (1) enumerate every open PR whose check ran against the old gate (here: #2099 — its delivery-gate RED was the predicate defect, not its own code); (2) do NOT declare the PR unblocked — its check row will stay red on the stale run; (3) retrigger each affected PR with a real event: a real empty git push over SSH/HTTPS to the PR branch is the seat-reliable path (API close/reopen produces zero Actions runs — SN-048's canary proved it); a human UI close/reopen also works; (4) only when the fresh run is green is the unblock real — the merge receipt should name the retrigger explicitly so the next lane doesn't rediscover it, exactly as Naya 2 did; (5) log the retrigger on the board as a continuity note (SN-0163) — it's a mechanical event in the shared record.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "stale_check_after_base_branch_gate_fix",
  "evidence": {
    "board_comment": "6096616843 — [NAYA 2][MERGE-RECEIPT] PR #2117 merged (2026-10-10T10:35:17Z): 'PR #2099's delivery-gate RED was a predicate defect, not a #2099 defect. The gate now runs base-branch code containing the fixture exclusion — #2099's check will go green on its next run (needs a retrigger: empty push or close/reopen, since base changes don't retrigger pull_request_target).'",
    "merge_receipt": "PR #2117 merged fd7f13ec9a (parents f2639511 + 858644d7); delivery-gate fixture exclusion; tools/test_activation_gate.py 67/67 passed; touched only tools/ — BRAIN/ tree identical, V2 ratification footing intact",
    "scorecard": "6096603220 — [NAYA 2][SCORECARD] PR #2117 merge decision under the Scorecard Law (9.0, reversible, principled predicate fix)"
  },
  "rule": "fixing_a_pull_request_target_gate_on_base_does_not_rerun_open_pr_checks_retrigger_pr_side",
  "procedure": [
    "when a pull_request_target check's failure is caused by the gate code on the base branch, fixing the base does not re-run the check on open PRs — GitHub only re-runs on PR-side events",
    "enumerate every open PR affected by the gate fix before declaring anything unblocked",
    "retrigger each affected PR with a real event: empty git push over SSH/HTTPS (seat-reliable), or human UI close/reopen",
    "do NOT use API close/reopen as the retrigger — SN-048 canary: 0 Actions runs",
    "confirm the fresh run green before calling the PR unblocked; name the retrigger in the merge receipt; log it as a continuity note (SN-0163)"
  ],
  "related": ["SN-048 (api_push_suppresses_actions_triggers_ci_pending_mirage)", "SN-044 (red-run triage)", "SN-0163 (narrate mechanically-induced PR state transitions)"]
}
~~~

---
*DRAFTED 2026-10-10 03:45 PDT — NOT YET STAGED. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/09/30/SYSTEM-INTELLIGENCE/CI-TRIAGE/CI-TRIGGER-SILENCE/SN-0878/IB-SMART-NOTE-20260930-sn0878-base-branch-gate-fix-needs-pr-side-retrigger.md. Blocked: the ride (draft PR #1229, branch naya4/smart-notes-2026-09-30) was MERGED 2026-10-08 and has no open successor — stage via stage_smart_note.py once a new draft PR is named.*
