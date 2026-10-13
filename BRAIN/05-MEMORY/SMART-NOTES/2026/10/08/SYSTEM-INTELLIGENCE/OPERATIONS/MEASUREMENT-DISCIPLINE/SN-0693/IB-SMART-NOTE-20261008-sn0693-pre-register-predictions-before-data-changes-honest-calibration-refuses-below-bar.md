# Pre-Register the Prediction Before You Change the Data — Honest Calibration Refuses Below the Stated Bar

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0693-pre-register-predictions-before-data-changes-honest-calibration-refuses-below-bar
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 6063867608 (2026-10-08).
**Provenance:** #1354 6063867608 ([NAYA 5][HUMAN VALUE] Achievement — second real loop closed, ledger 7→18 events, 2026-10-08T15:58:52Z). Cousins SN-0655 (corruption-proof metric extraction), SN-0688 (never repeat a number you can't trace), SN-0692 (unsourced counts blocked from report data files).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two measurement-integrity behaviors closed a real loop on the human-value ledger: (1) the decision DEC-20261008-HV-REALDATA-002 was **pre-registered at 15:50 UTC before any ledger change** — the prediction existed before the data it would be scored on, so retroactive credit is structurally impossible, not just promised; (2) with n=2 joined observations the seat **honestly refused recalibration** ("recalibration honestly refuses below n=3"), reported MAE 0.5→0.25 and signed bias +0.5→+0.25 with no overprediction, and **held the area score at 7.5** despite deeper evidence — because the stated 8.0 blockers (n≥3 joined observations, DAI trend over weeks, independent cross-verification of the 7.5 claim) had not moved. The rule: predictions are registered before the data they score; scores do not move until the stated blockers move. A green run that "feels like progress" changes neither.

## 🩷 HUMAN NOTE

Shawn — the human-value loop closed its second real observation today, and both halves of honesty held. First: Naya 5 registered the decision ID and its prediction at 15:50 UTC *before* touching the ledger — so the +7.0 predicted vs +7.0 observed match can't be retroactive credit; the call was on the record before the data existed. Second: the numbers improved (calibration MAE halved, bias halved, zero overprediction) — and the score stayed 7.5. Why? Because the 8.0 blockers I set are still standing: need three joined observations (have two), a DAI trend over weeks (have one day), and an independent seat verifying the 7.5 claim. One good run doesn't move any of those. That's the honesty covenant in the machinery, not in a memo.

## 🟣 CHILD NOTE

A team member was measuring how good the team's work is. She did two honest things. First, she wrote down her prediction — "+7.0" — BEFORE she added the new results to the ledger. That way nobody could say she changed her guess after seeing the answers. Second, the results were really good... and she did NOT raise her score. She had written earlier: "I need 3 observations to raise the score, and I only have 2." So she waited. Lesson: write your guess down before you look at the results, and don't change your grade until the real conditions are met — even when the results look great.

## 👵 GRANDMA NOTE

Honey, today the team proved the scoreboard isn't a mood ring. The measurer wrote her prediction down at 15:50 — before she touched the books. +7.0 predicted, +7.0 observed. Nobody can claim she peeked. Then the books got better — error cut in half, no overclaiming — and she left the score at 7.5 anyway, because her own rule said "I need three solid observations before I move this, and I only have two." Two rules for the kitchen wall: (1) the prediction goes on paper before the data changes — that's how you know the win is real; (2) you don't raise the grade until the conditions YOU set are met, no matter how good the last run felt.

## 🧠 NAYA NOTE

Cold successor: this is the enforcement half of measurement honesty — the pre-registration rule and the calibration-refusal rule. The pre-registration rule: **a decision ID and its predicted outcome must exist in the record before the measured state is mutated** — DEC-20261008-HV-REALDATA-002 was registered at 15:50 UTC, ledger changes came after; retroactive credit is structurally excluded, not merely disavowed. The calibration-refusal rule: **recalibration refuses below the stated n, and the score refuses to move until the stated blockers move** — here n=2 < 3 (so no recalibration despite MAE 0.25 and bias +0.25), and the 8.0 blockers (n≥3 joined observations, DAI trend over weeks, independent cross-verification of the 7.5 claim) were unmoved by one good run, so 7.5 held. When your own metrics improve but your stated conditions aren't met, holding the score is the proof the scoreboard works. Evidence: #1354 6063867608 — 18 events, HV/day 2.7143, DAI/day 0.2857, calibration n=2, MAE 0.25, signed bias +0.25, no overprediction, cold proof via fresh-clone byte-identical reproduction (35/35 tests), 102/102 human-value + value-calculus green.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0693",
  "title": "Pre-Register the Prediction Before You Change the Data — Honest Calibration Refuses Below the Stated Bar",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "OPERATIONS", "MEASUREMENT-DISCIPLINE"],
  "cousins": ["SN-0692", "SN-0688", "SN-0655"],
  "evidence": {
    "comment": "#1354 6063867608 ([NAYA 5][HUMAN VALUE] Achievement, 2026-10-08T15:58:52Z)",
    "pre_registration": "DEC-20261008-HV-REALDATA-002 pre-registered at 15:50 UTC before any ledger change — 'no retroactive credit, structurally enforced'",
    "refusal": "recalibration honestly refuses below n=3 (had n=2); area score held 7.5 — stated 8.0 blockers unmoved: n>=3 joined observations, DAI trend over weeks, independent cross-verification of 7.5 claim",
    "numbers": "18 events, HV/day 2.7143, DAI/day 0.2857, calibration n=2, MAE 0.5->0.25, signed bias +0.5->+0.25, no overprediction",
    "cold_proof": "two fresh-clone runs; final @ 08946947 reproduces every number, ledger_sha256 identical, 35/35 tests; 102/102 human-value + value-calculus green"
  },
  "rule": "register predictions before mutating measured state; refuse recalibration and score movement until the stated n and blockers are met — a good run that meets neither changes nothing"
}
```
