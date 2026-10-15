# Presence-Checking a Gate Is Theater: the Watch Must Read the Gate's Conclusion, Not the Body's Text (FM#60)

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1368-presence-checking-a-gate-is-theater-fm60
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 01:08 PDT distillation tick (2026-10-15) from #2537 comment 6186662487 (main-seat adjudication on the #2533 divergence, verified on live bytes), via the director-pass shared-state mission snapshot (2026-10-15 07:41Z). No new #1354 comments existed to read (issue capped at 2,500; commenting disabled).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The main seat withdrew the director's CLEAN verdict on PR #2533's merge. The 3-pass receipt text WAS present in the PR body — and the merge-receipt watch saw that text and called it CLEAN. But the 'Team review + scorecard receipt' branch-protection gate had FAILED three times at the merge commit, and the merge went through via the org app account anyway. The watch's defect: it verified the *presence* of receipt words in the body, never the *conclusion* of the gate at the merge commit. Presence is not outcome. Fix owed (review lane / director): the watch must read the gate's check-run conclusion at the merge commit — gate failure means RECEIPT BREACH (or NON-COMPLIANT), regardless of what the body says. Named failure mode #60: receipt-text theater. Open question carried to Shawn (morning): authorized admin bypass, or is the check advisory in practice? Cousin map: SN-097 (verify check claims against live check-runs), SN-0975 (status theater), SN-1024 (wiring a consumerless mirror is theater), tonight's post_checker census on #2568 (38/38 suite green, ZERO live call sites tree-wide — merged-not-enforced, same theater family, different seam).

## 🩷 HUMAN NOTE

It's like checking whether someone passed their driving test by reading the diary entry they wrote about it, instead of looking at the examiner's stamped score sheet. The diary can say "I passed!" in beautiful handwriting while the score sheet says FAIL three times over. You check the score sheet. That's what happened: the PR body said the receipt was there, the watch read the body's claim and called it clean — but the gate's official score sheet said FAILED. From now on: read the examiner's sheet, not the diary.

## 🟣 CHILD NOTE

Imagine the teacher keeps a big checkmark book that says who really passed the test. A kid writes in their own notebook "I passed!" — that doesn't count. Someone checking the grades has to open the teacher's book, not the kid's notebook. The team was checking the kid's notebook. The new rule: always open the teacher's book — the gate's official decision — even when the notebook looks perfect.

## 🔵 GRANDMA NOTE

It's the difference between a restaurant's own menu claiming "health score: A" and the actual health inspector's report taped to the window. You trust the inspector's report, not the menu. The team's watcher was trusting the menu — it saw the words in the PR body and called the merge clean, while the inspector (the gate) had failed it three times at the merge commit. The standing rule now: read the inspector's report every single time.

## 🟠 NAYA NOTE

Apply whenever you verify a gate, a merge receipt, or any enforcement claim: (1) never accept receipt TEXT in a PR body as proof the gate passed — the body is self-reported and unbounded; (2) read the gate's check-run CONCLUSION at the merge commit via the checks API — that is the gate's machine-recorded verdict on exact bytes; (3) gate FAILED at the merge commit → verdict is RECEIPT BREACH (formal, FM#32) or NON-COMPLIANT, regardless of what the body says; (4) when building or repairing any verification instrument, point it at the canonical machine record (check-run conclusions, call-site census), never at prose that claims the record. Name the failure mode in the verdict so the next seat doesn't rediscover it.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "presence_check_theater",
  "evidence": {
    "board_comment": "6186662487 — main-seat adjudication (verified on live bytes, 2026-10-15): director's CLEAN on PR #2533 WITHDRAWN. Receipt text present in the PR body, but the 'Team review + scorecard receipt' branch-protection gate FAILED 3x at the merge commit (406 check runs: code CI GREEN; the 3 failures are all this gate); merge went through via the org app account.",
    "named_failure_mode": "FM#60",
    "root_cause": "merge-receipt watch checks receipt TEXT in the body, not the gate check-run CONCLUSION at the merge commit — presence-checking a gate is theater",
    "fix_owed": "the watch must read the gate's check-run conclusion at the merge commit; gate failure -> RECEIPT BREACH regardless of body text (review lane / director)",
    "open_question": "authorized admin bypass, or is the check advisory in practice? (for Shawn, morning)"
  },
  "cousins": ["SN-097", "SN-0975", "SN-1024", "#2568 post_checker census (merged-not-enforced)"],
  "decision_change": "future merge-receipt verdicts read the gate's check-run conclusion at the merge commit instead of accepting body text",
  "falsifiability": "if the gate's check-run conclusion proved unreliable (false PASS) or the #2533 merge were shown valid, this is wrong",
  "mechanism": "body text is self-reported and unbounded; check-run conclusions are the gate's machine-recorded verdict on exact bytes — a watcher reading the former verifies a claim, not the gate"
}
~~~
