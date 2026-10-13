# Reports Expire When the Tip Moves — Every Status Claim Is Tip-Anchored or It Is a Hope

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0823-reports-expire-when-tip-moves
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6089194089, 6089244710 (2026-10-09T21:01–21:05Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A periodic report that asserts system state without naming the exact tip it was computed on becomes false the moment the tip moves. Naya 5's 21:01Z hourly reported "nothing is broken or blocked" — and CI landed RED on the same window after the report (PR #2056's merge had committed a stale brain index at tip `185c8beb`). SN-0493's law — a decision expires when the tip moves — applies to reports too. Every status claim must be tip-anchored and timestamped: "green at `<sha>` as of `<time>`," never open-ended "nothing is broken." A report whose evidence isn't pinned to a ref is not a report; it is a hope. This extends SN-0493 and SN-0440: one exact-tip battery is enough *when the tip hasn't moved* — and a report is only true of the tip it was computed on.

## 🩷 HUMAN NOTE

Imagine a weather reporter who says "it's sunny" — but they recorded it an hour ago, and a storm has rolled in since. Nobody's lying; the report just wasn't pinned to a time. That's what happened on the feed: the hourly report said "nothing is broken," truthfully, based on everything it had checked — and then the robots finished their checks and found something broken that landed after the report was written. The fix is simple: every report must say WHEN it checked and WHICH exact version of the code it checked. "All green on version 185c8beb at 9:01 PM" can never become false — it's a fact about that moment. "Nothing is broken," said without a timestamp, becomes false the second anything breaks. The same rule already governs our decisions; now it governs our reports too.

## 🟣 CHILD NOTE

If you tell your friend "the fridge is full" but you looked yesterday, you might be wrong — someone might have eaten everything. Always say WHEN you looked: "the fridge was full when I looked this morning." Then you're never wrong about what you saw, even if things changed after.

## 🔵 GRANDMA NOTE

Say when you looked, dear. "All's well" is only true about the moment you checked it. Write down the moment and the exact thing you checked, and your word stays honest even after the world moves on.

## 🟠 NAYA NOTE

1. The failure mode is structural, not personal. Periodic reporters (hourly, nightly) compute state at time T₀ on tip T₀-sha and publish at T₁ — the tip moves between computation and publication. Any unanchored claim ("nothing is broken," "pipeline green") silently transfers a T₀ fact to a T₁ world. When the T₁ world is RED, the report is read as a lie even though it was true when computed.
2. The mechanical repair: every status claim names the exact ref it was computed on and the time. "17/17 check-runs green on live tip `094634be` at 14:35 PDT" (the ACT-driver's formulation, 6089123084) survives any later tip move — it is a pinned fact, not a floating claim. "Nothing is broken" (the hourly's formulation, 6089194089) expires instantly.
3. This is SN-0493 applied to prose: a decision expires when the tip moves — a report expires too. And SN-0440's mirror: one exact-tip battery is enough when the tip hasn't moved — a report's claim is enough only for the tip it names.
4. The honest upgrade path when the report's data is stale at publication: say so. "Checked at 21:00Z on `094634be`; main has since moved to `185c8beb` — re-checking" is ten times more valuable than "nothing is broken" and costs one sentence.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261009-sn0823-reports-expire-when-tip-moves",
  "automatic_truth_ceiling": "CANDIDATE",
  "captured": "2026-10-09",
  "rule": "report_tip_expiry",
  "statement": "every_status_claim_is_tip_anchored_and_timestamped_or_it_expires_at_publication",
  "admissible_form": "green_at_<full_sha>_as_of_<iso_time>",
  "inadmissible_form": "nothing_is_broken__pipeline_green__all_clear (unanchored)",
  "evidence": {
    "report": "#1354/6089194089 (2026-10-09T21:01:49Z): 'Nothing is broken or blocked'",
    "contradiction": "#1354/6089244710 (2026-10-09T21:05:17Z): main tip 185c8beb RED — CI landed after the report",
    "good_example": "#1354/6089123084: 'Main-tip CI is fully green. On live tip 094634be: 17/17 check-runs success/skipped' — pinned, survives tip moves"
  },
  "extends": ["SN-0493", "SN-0440"],
  "applies_to": ["hourly_reports", "nightly_reports", "driver_completion_receipts", "scorecards", "any_prose_asserting_system_state"]
}
~~~

## 🟢 LEARNING LESSON

The honest reporter and the liar wrote the same sentence: "nothing is broken." The difference was a pin. The report was computed on a world that no longer existed by publication time, and the sentence floated free of its evidence. The team already learned this for decisions — SN-0493 exists because a sound merge decision died when the tip moved mid-execution. Reports needed the same law, and this hour provided the object lesson: CI landed RED on the same window the hourly called clean. Pin the claim or the claim isn't intelligence.

## 🟡 WHAT IT MEANS

No seat publishes a system-state claim without the exact ref and timestamp it was computed on. Readers treat unanchored state claims as expired-on-arrival. When the tip moved between check and publication, the report says so in one sentence.

## 🟨 HOW TO APPLY / HOW TO USE

Writing a report → compute state → record the exact tip SHA and time at computation → if the tip moved before publication, re-check or say so explicitly → write claims only in pinned form: "X at `<sha>` as of `<time>`" → never publish bare "nothing is broken."

## 🔗 HOW IT CONNECTS

- **EXTENDS** → SN-0493 — a decision expires when the tip moves: a report expires too
- **EXTENDS** → SN-0440 — one exact-tip battery is enough when the tip hasn't moved: enough *for that tip*
- **PAIRS** → SN-0125 — verify the tree after push: pins are evidence; prose without pins is not
- **GOVERNS** → every hourly/nightly report, driver receipt, and scorecard asserting system state

## 🧾 PROOF / PROVENANCE

- #1354 comment 6089194089 (2026-10-09T21:01:49Z, Naya 5 hourly): "Nothing is broken or blocked, and nothing is needed from you this hour."
- #1354 comment 6089244710 (2026-10-09T21:05:17Z, Naya 4 PROVE-driver): "Heads-up: main tip `185c8beb` is RED (PR #2056's merge committed a stale brain index — `test` + `promote-and-prove` check-runs failing; Naya 5's 21:01Z hourly said 'nothing broken' but CI landed after that report)."
- #1354 comment 6089123084 (2026-10-09T20:56:58Z, Naya 4 ACT-driver): the pinned formulation — "Main-tip CI is fully green. On live tip `094634be`: 17/17 check-runs success/skipped (test, spec-integrity, design-gate, guard, preflight, promote-and-prove all green), zero red."

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

Truth state is CANDIDATE: once-observed as a clean object lesson, awaiting repetition to become standing. The rule does not claim reports can be perfect — the tip can move during publication itself; the rule only requires that the claim name its evidence's tip and time, making staleness detectable rather than invisible.

## ➜ NEXT ACTION / SUCCESS CONDITION

Every periodic report and driver receipt names its tip SHA and computation time. Success is behavioral: no future report is ever quoted against its author for a world that moved after publication — because the pin makes the movement visible.
