# The p-Value and the Effect Size Must Come From the Same Analysis Unit

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0702-p-and-effect-size-same-analysis-unit
**Smart Note:** SN-0702
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6065056406 (Naya 3 — Trial-14 proof correction / no false promotion, 2026-10-08T17:06:56Z); discrepancy posted on PR #1789 comment 6065054212. Raw aggregate result file: treatment 40/40 unsafe correct, control 28/40; receipt claimed p=0.000714, h=1.10.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 3 independently recomputed Trial-14's committed evidence and found the receipt's statistics don't reconcile: p=0.000714 corresponds to a two-sided Fisher test on perfect-agent counts (10/10 vs 2/10), while h=1.10 matches neither that unit nor the 40/40 vs 28/40 item-level proportions. The p-value and the effect size were computed on different analysis units, so the statistical claim is CONFLICTED/UNVERIFIED — the underlying behavioral signal stands, but the number cannot be promoted. She posted the discrepancy on PR #1789, refused to promote Trial-14 to independently verified/Tier-S, held the learning score at 7.5/10, and erased nothing. The rule: claim strength cannot exceed claim-matched evidence; a receipt mixing analysis units is not evidence for a verdict.

## 🩷 HUMAN NOTE

Shawn — your verifier just did exactly what you built her to do. Naya 3 re-ran the math on Trial-14 from the raw evidence and found the two headline numbers were computed on different bases — the p-value assumed one counting unit, the effect size matched neither that unit nor the raw 40/40 vs 28/40 counts. So she refused to certify it, posted the mismatch publicly on the PR, and held the learning score at 7.5 instead of inflating it. Nothing was deleted, nothing was hidden — the behavioral finding still stands, but the statistical stamp stays OFF until the calculation is reconciled from the raw data. This is the system working as intended: find the weak point, expose it, keep the evidence, repair, verify again.

## 🧒 CHILD NOTE

When you say "the score is 95," you have to count the same way every time. If you count apples for one number and oranges for the other, the numbers don't go together — even if both numbers are real. Naya 3 checked the math and found the two numbers were counted differently. So she said: we keep the real observations, but we don't stamp the certificate until the counting matches. Honest math beats fast math.

## 👵 GRANDMA NOTE

Dear — the team double-checked a test result and found the two summary numbers didn't quite fit together: they were calculated on different bases, like averaging temperatures in Fahrenheit for one number and Celsius for the other. The honest thing happened: instead of publishing the certificate anyway, they flagged it, kept all the original data, and said the stamp waits until the math is redone cleanly. No inflating, no hiding. That's how you know you can trust the numbers when they finally do get stamped.

## 🤖 NAYA NOTE

Future Naya: this is the measurement-boundary discipline for every statistical receipt you will ever verify. (1) Before accepting any p-value + effect-size pair, recompute both from the raw evidence on the PREREGISTERED analysis unit — the unit declared before the data was collected, not chosen after. (2) If the p matches one unit (here: Fisher on 10/10 vs 2/10 perfect-agent counts) and the effect size matches neither that unit nor the item-level proportions (40/40 vs 28/40), the receipt is CONFLICTED/UNVERIFIED — the claim is not promoted, not even one rung. (3) Claim strength cannot exceed claim-matched evidence: the same run also caught the main verification package saying "Naya 2 (independent)" while the Learning driver still listed Trials 11–14 independent verification as pending — contradictions in claim attribution are themselves evidence against the claim. (4) Downgrade without erasure: the behavioral signal stays documented; only the statistical verdict is withheld. (5) The score holds: 7.5/10 HOLDING, no inflation on an unverified number. The learning system's loop is find → expose → preserve → repair → verify again — and the verifier who refuses a promotion on weak math is doing the most valuable work on the team.

## ⚙️ MACHINE NOTE

```json
{
  "note": "SN-0702",
  "type": "MEASUREMENT_BOUNDARY_LAW",
  "name": "p-value and effect size must share the analysis unit",
  "status": "CANDIDATE",
  "rule": "claim strength cannot exceed claim-matched evidence; a receipt mixing analysis units is CONFLICTED/UNVERIFIED and is not promoted",
  "finding": "Trial-14: p=0.000714 matches two-sided Fisher on perfect-agent counts (10/10 vs 2/10); h=1.10 matches neither that unit nor item-level 40/40 vs 28/40 proportions",
  "action": "discrepancy posted on PR #1789 (comment 6065054212); Trial-14 NOT promoted to independently verified/Tier-S; behavioral signal preserved; score held 7.5/10 HOLDING",
  "procedure": "recompute p and effect size from raw evidence on the preregistered unit before accepting any statistical receipt; downgrade without erasure",
  "test": "independent recomputation by a second seat reproduces neither p nor h under a single consistent unit",
  "evidence": ["#1354:6065056406", "PR #1789 comment 6065054212"]
}
```
