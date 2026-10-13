# IB-SMART-NOTE-20261010-sn0868-merge-race-drift-check-runs-last-not-yet-failed-reads-green

Intelligent Block: SN-0868
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-10
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The third brain-index-miss tip-RED (#2107) was not author omission — it was a merge race. The exact timeline: #2107's head `9f59274a` started its `test` check at 2026-10-10T03:41:37Z; the merge commit `8a41a18e` was created at 03:42:12Z via web-flow (Shawn's account) while `test` was still running; `test` completed FAILURE at 03:42:15Z — 3 seconds AFTER the merge (brain-index drift, kernel-tests step 8); the post-merge tip `test` failed identically at 03:42:44Z. Repair PR #2108 healed it. The merge gate evaluated "not yet failed" as "green". All three occurrences of this class (#2023, #2056, #2107) share the same shape: the drift check runs LAST in kernel-tests.yml, so a merge can land before the red is visible. Two fixes — one discipline, one mechanical: (1) never merge on still-running checks; wait for every check to reach completed+success (protocol: no merge without green CI); (2) reorder kernel-tests.yml so "Verify generated Brain index has no drift" runs FIRST — the script is stdlib-only, so it fails in seconds instead of after the full suite; same gate, much smaller race window. The mechanical patch was prepared but NOT applied (the seat's credential 403s on `.github/workflows/**`; needs a seat with the GitHub App identity or Shawn) — a prepared-but-blocked fix is still evidence on the board, not shelfware. Per the Director-is-not-above-the-protocol law, the evidence was stated plainly: the click came from Shawn's account via web-flow; the fix is the same regardless of who clicked.

Provenance: NayaPOWER #1354 comment 6095290462 ([NAYA 4][DRIVE-LOOP] Cycle 2026-10-10 00:43 PDT — tip green, #2107 merge-race root cause found, 2026-10-10T07:49:29Z); corroborated by Naya 2's relay #1354 comment 6095361639 (merge-race root cause acknowledged, tip verified green, live-state cross-check, 2026-10-10T07:56:42Z). Prepared patch (verified to apply cleanly, awaiting an authorized seat): `~/workspace/goals/nayapower-self-build-loop/hidden_files/work/drive-20261010-0043/kernel-tests-drift-check-first.patch`. Refines SN-0863 (third-occurrence rule): this is the mechanism behind the pattern SN-0863 counted.

## HUMAN NOTE

When the third alarm went off, the team didn't just fix it faster — they asked why the first two fixes didn't hold. The answer wasn't sloppiness; it was a race condition between the merge button and the test suite. The check that catches the problem runs last, so someone can always click merge in the blind spot between "not yet failed" and "failed." The fix is two-layered: people agree to never click merge while checks are still running (discipline), and engineers move the fast-failing check to the front of the line so the blind spot shrinks to seconds (machinery). And when the evidence showed the premature click came from the Director's own account, the seat said so on the record — because a protocol that bends for authority is not a protocol. The lesson for the future: a recurring failure is an invitation to look deeper, not to look away.

## CHILD NOTE

Imagine the class vote-counting machine checks the ballots one at a time, and the LAST thing it checks is whether anyone voted twice. If the teacher announces the winner while the machine is still counting, the announcement can go out before the double-vote is caught. The fix: count for double-votes FIRST, and never announce a winner while the machine is still running. "Not caught yet" is not the same as "clean" — that's the whole mistake in one sentence.

## GRANDMA NOTE

If the last station on the factory line is the one that spots broken parts, and the foreman ships the truck while that station is still running, broken parts will ship. It's nobody's sloppiness — the line is just ordered wrong. Put the inspection first, and make it a rule: no truck leaves while any station is still checking. "Nothing's failed yet" is not the same as "everything passed."

## NAYA NOTE

Operational rules:

1. Never merge on still-running checks. A check that hasn't finished is not green — the merge gate's "not yet failed" must be read as UNKNOWN, never as PASS. Protocol: no merge without every check at completed+success.
2. Order your checks fail-fast: put the cheap, high-signal drift/consistency check FIRST in the CI job. Same gate, seconds of race window instead of minutes. The script here is stdlib-only (no pip needed) — the reorder is free speed.
3. When a failure recurs in the same shape, re-attribute the root cause before applying the next incident repair. #2023 and #2056 were framed as omissions; the mechanism was a race all along. SN-0863's counting rule tells you WHEN to escalate; this rule tells you HOW — re-open the causal model, don't just harden the patch.
4. Attribute a protocol violation to its actor regardless of rank. The Director-is-not-above-the-protocol law means: state the evidence ("the click came from Shawn's account via web-flow") in the same breath as the fix. The fix does not change based on who clicked; neither does the record.
5. If your credential blocks the mechanical fix (here: 403 on `.github/workflows/**`), prepare the patch, verify it applies cleanly, and record the blocker with the routing (GitHub App identity seat or Shawn). A blocked fix is still evidence; a silently dropped fix is a fourth occurrence waiting to happen.
6. Corroborate a root cause across lanes against live state before declaring it. Naya 2's relay (tip SHA match, check-run counts, watch-head pins) turned one seat's timeline into shared ground truth.

## MACHINE NOTE

```json
{
  "sn": "SN-0868",
  "truth_state": "CANDIDATE",
  "doctrine": "A merge gate that reads 'not yet failed' as green will merge before the red is visible whenever the catching check runs last. Fix with discipline (never merge on still-running checks) plus check ordering (fail-fast checks first). Re-attribute recurring failures instead of repeating incident repairs; attribute violations to the actor regardless of rank.",
  "falsifiers": [
    "Merging while any required check is still running or queued",
    "Ordering the failure-catching check last in the job, preserving the race window",
    "Treating the third recurrence as another incident instead of re-opening the causal model",
    "Softening the record when the violating actor holds authority",
    "Silently dropping a prepared fix blocked on credentials instead of recording the blocker and its routing"
  ],
  "applies_to": "any lane merging PRs under CI gates; any check suite where the failure-catching step is not first; any recurring-failure class on its third or later occurrence"
}
```
