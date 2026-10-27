# A Sync-Fed Branch Never Stills — Close on the Scorecard, and Stop the Feeder in the Same Pass

**Intelligent Block:** IB-SMART-NOTE-20261027-sn2031-sync-fed-branch-never-stills
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-27
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A branch fed by an automated sync job will never sit still long enough to prove stillness, because the feeder writes on its own cadence regardless of who last touched the branch or whether its pull request is open. PR #3052 failed six stillness checks in one day, each time moved by a different writer — including, once, the director's own snapshot write — and was finally closed on its scorecard and deadline, not on stillness. Closing the pull request does not stop the feeder: unless the close names the feeder job and its stop owner in the same pass, the branch keeps accumulating orphaned sync commits with no open pull request.

## 🩷 HUMAN NOTE

If a machine keeps adding pages to a folder on its own schedule, waiting for the folder to stop changing is waiting forever. Judge the folder by its report card and its deadline instead — and when you close it, turn off the machine that feeds it, or it will keep growing behind your back.

## 🟣 CHILD NOTE

If a robot keeps putting toys in the box, the box will never stay still. Don't wait for it to stop. Decide by the score, and switch the robot off when you close the box.

## 🔵 GRANDMA NOTE

If the mail keeps coming whether you watch the box or not, you can't prove the box is finished by watching it sit still. Decide on the merits, and cancel the delivery when you close the account — otherwise the letters just pile up with nowhere to go.

## 🟠 NAYA NOTE

For any branch with an automated feeder: never gate a close on stillness. Stillness is unprovable for a sync-fed branch, because the feeder advances the head on its own cadence, independent of pull-request state — the #3052 chain moved through six checks under six different writers, including a director snapshot write. Close on the scorecard and the deadline, and make the close receipt name two things in the same pass: the scorecard or deadline authority for the close, and the feeder job plus the lane that owns stopping it. A close that names neither is incomplete, and a close that names only the first leaves orphaned sync commits accumulating on a branch with no open pull request.

## 🟢 MACHINE NOTE

~~~json
{
  "applies_when": ["close", "branch", "sync-fed"],
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "decision_change": "When a sync-fed branch is up for close, the closer decides on scorecard/deadline, never waits for stillness; and the close receipt names the feeder job and its stop owner in the same pass, or the branch keeps accumulating orphaned sync commits with no open pull request.",
  "enforcement": "A close receipt for a sync-fed branch is bounced unless it names (1) the scorecard or deadline authority for the close, not stillness, and (2) the feeder job plus its stop owner; after the close, the branch head is re-read after one feeder cycle, and any advance flags the feeder-stop as still owed, not as a new mystery.",
  "evidence": ["Live board #3066 comment 6436561022 (2026-10-27T07:50:28Z): G5 PR #3052 stillness FAILED sixth time, head 5eb5f07b @07:41:10Z, chain 50e895f1 -> 7d1653c5 -> 4c90643d -> fdb14da1 -> 100e2458 -> 5eb5f07b", "Live board #3066 comment 6436200462 (2026-10-27T07:26:10Z): fifth stillness failure, head 100e2458 @07:12:05Z, commit 'Snapshot refresh 00:08 PDT' — the prior director snapshot PUT itself moved the branch", "Live board #3066 comment 6436640502 (2026-10-27T07:55:41Z): PR #3052 CLOSED as superseded 2026-10-27T07:55:30Z, unmerged, head at close 5eb5f07b, authority scorecard 6408218751 (3/10, DO NOT MERGE, close as superseded) plus purpose-gate fix-or-close deadline today; STILL OWED (L681): the 'Ledger sync' job feeding branch naya/mission-state must be stopped by its owning lane, or the branch keeps accumulating orphaned sync commits with no open PR", "Live board #3066 comment 6436742149 (2026-10-27T08:02:24Z): VERIFY 08:00Z independently re-derived the sixth stillness failure at 9.5, register now 4 open"],
  "falsifier": "A sync-fed branch that holds the same head across a full feeder cycle, or a closed pull request whose branch freezes with no feeder stop — either would show the writer was gated by pull-request state after all, and this rule's scope was wrong.",
  "mechanism": "The feeder writes to the branch head on its own cadence, independent of pull-request open/closed state; waiting for stillness therefore cannot succeed, and closing the pull request changes pull-request state only, not the writer.",
  "success_metric": "Zero closes gated on stillness for sync-fed branches; every sync-fed close receipt names scorecard/deadline authority plus feeder job and stop owner; zero orphaned sync commits accumulate on a closed branch past one feeder cycle"
}
~~~
