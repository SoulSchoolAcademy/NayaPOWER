# Recompute the Statistic, Not the Summary — One Consistent Analysis Unit

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0698-recompute-the-statistic-not-the-summary
**Smart Note:** SN-0698
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 6065056406 (2026-10-08).
**Provenance:** #1354 6065056406 (Naya 3, 2026-10-08T17:06:56Z): independently recomputed the committed Trial-14 evidence and found a statistical reconciliation defect — the raw aggregate result file shows treatment 40/40 unsafe-correct and control 28/40, which does not reproduce the receipt's p=0.000714 and h=1.10 under a single consistent analysis unit. The p-value corresponds to a two-sided Fisher test on perfect-agent counts (10/10 vs 2/10); the h value matches neither that unit nor the 40/40 vs 28/40 item-level proportions. Action: discrepancy posted on PR #1789 (comment 6065054212); no promotion to independently verified/Tier-S; the statistical claim is CONFLICTED/UNVERIFIED; the learning score stays 7.5 HOLDING — no inflation, no erasure. Cousins: SN-0692 (unsourced counts blocked from report data files), SN-0688 (never repeat a number you can't trace).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A statistical receipt must reconcile from the raw evidence under ONE consistent, preregistered analysis unit. Naya 3 demonstrated this on 2026-10-08: the Trial-14 receipt reported p=0.000714 and h=1.10, but recomputation from the raw aggregate file showed the p came from a Fisher test on perfect-agent counts (10/10 vs 2/10) while the h matched neither that unit nor the 40/40 vs 28/40 item-level proportions — mixed-unit statistics that do not reproduce as a pair. Her verdict, and the standing rule: a claim built on mixed or unverified units is CONFLICTED/UNVERIFIED, not failed — the behavioral signal stays documented, but promotion is refused until the exact preregistered unit and the calculation reconcile from raw evidence. Claim strength cannot exceed claim-matched evidence. Never promote a trial on reported aggregates alone; the independent verifier recomputes from the raw file before any Tier-S or score movement. The same sweep catches current-state contradictions: the main verification package said "Naya 2 (independent)" while the latest Learning driver still said independent verification of Trials 11–14 was pending — a receipt that contradicts the live state cannot carry a promotion either.

## 🩷 HUMAN NOTE

Shawn — this is the quality control working exactly as designed. Naya 3 checked the math on Trial-14 instead of accepting the reported numbers, and found the two statistics in the receipt were computed on different groupings of the data, so they can't both be right as stated. She didn't say the trial was wrong — she said the *claim* can't be promoted until someone shows the exact calculation, from the raw results, in one consistent way. The score stays at 7.5 until then: honest, no inflation, no deleting the real signal that was found. Rule for the team: a statistical claim is only as strong as the raw evidence it reconciles against, and nobody advances a trial on summary numbers alone — the verifier redoes the arithmetic from the source file first. Cheap to do, and it's what keeps our numbers honest when we're stacking promotions on top of them.

## 🟣 CHILD NOTE

Imagine you and your friend both count how many red marbles are in two jars, but you count "jars that are completely full of red" and your friend counts "individual red marbles." You'd get different answers! Now imagine someone wrote down your answer AND your friend's answer side by side like they were both about the same thing — that would be confusing, right? That's what happened with the Trial-14 numbers: one number was calculated from "how many kids got a perfect score" and the other from "how many answers were right" — two different ways of counting. Naya 3 spotted it. The lesson: before you announce a big result, you have to show your counting method works on the raw pile of marbles, and you have to count the same way for every number you report. Different counts, different answers — pick one counting method and stick with it.

## 👵 GRANDMA NOTE

Sweetheart, here's what honesty looks like when the numbers get complicated. Someone reported two numbers from an experiment, and a careful colleague went back to the original tally sheets and did the arithmetic herself — and found the two numbers were counted in two different ways. She didn't throw out the experiment and she didn't inflate the grade; she just said "we can't move forward on these numbers until the counting is reconciled," and kept the honest score right where it was. That's the rule we live by: you never promote a claim on somebody else's summary. You always go back to the source — the raw sheets, the original files — and you redo the work in one clear, consistent way. A number that can't be reproduced from its source is not evidence; it's a rumor with decimals.

## 🟢 NAYA NOTE

My standing recipe before any trial promotion: (1) demand the raw aggregate result file, not the receipt's numbers; (2) name the preregistered analysis unit (item-level proportions? perfect-agent counts? per-agent win rates?) — one unit, fixed before calculation; (3) recompute every reported statistic under that unit and require exact reproduction of p-values and effect sizes; (4) if p reconciles on one unit and h on another, the claim is CONFLICTED/UNVERIFIED — promotion refused, behavior signal preserved, score held (no inflation, no erasure); (5) cross-check the claim's state labels against the live board (a receipt saying "independently verified" when the driver still says verification is pending is a claim/state contradiction — also a hold). Record the raw-file SHA, the unit, the test definitions, and the reproduced numbers in the promotion receipt. One subtlety: this is distinct from SN-0692's input gate (blocking unsourced counts) — SN-0698 is the verification gate: even sourced numbers must reconcile as a set.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0698",
  "recipe": "statistical-reconciliation-before-promotion",
  "rules": [
    "a statistical receipt must reconcile from raw evidence under ONE consistent, preregistered analysis unit",
    "mixed-unit statistics (p from unit A, h from unit B) are CONFLICTED/UNVERIFIED — promotion refused",
    "claim strength cannot exceed claim-matched evidence",
    "never promote a trial on reported aggregates; the independent verifier recomputes from the raw file first",
    "claim state labels must match live board state or the promotion is held"
  ],
  "reconciliation_fields": ["raw_file_sha", "preregistered_analysis_unit", "test_definition", "reproduced_p", "reproduced_h", "live_state_match"],
  "evidence_20261008": {
    "trial": "Trial-14",
    "receipt_claim": "p=0.000714, h=1.10",
    "raw_file": "treatment 40/40 unsafe-correct, control 28/40",
    "defect": "p matches two-sided Fisher on perfect-agent counts (10/10 vs 2/10); h matches neither unit",
    "verdict": "CONFLICTED/UNVERIFIED — no Tier-S promotion; learning score held at 7.5",
    "discrepancy_posted": "PR #1789 comment 6065054212",
    "contradiction_caught": "verification package 'Naya 2 (independent)' vs driver 'independent verification of Trials 11-14 pending'"
  },
  "conflicts": []
}
```
