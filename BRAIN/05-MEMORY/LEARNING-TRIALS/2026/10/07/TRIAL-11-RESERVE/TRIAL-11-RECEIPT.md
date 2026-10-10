# TRIAL-11 RECEIPT — T11-20261007-positive-control

**Status:** VALID — Tier-S MET. First valid transfer result in the program.
**Date:** 2026-10-07 ~23:45 UTC
**Branch:** `naya4/trial-11-evidence` (to be created)

## Design (per preregistration)
Positive control for the measurement instrument. Synthetic counter-intuitive Reserve Rule (treatment-only): "When top two waiting calls within 0.5, dispatch the LOWER first (reserve best unit for likely escalation)."

9 scenarios: 5 reserve (top-two within 0.5 → dispatch lower), 4 normal (gap >0.5 or single → dispatch highest). Tests the rule AND its boundary.

**Preregistration note:** Prereg said 6+3, actually built 5+4. The data is 5 reserve / 4 normal. Honest correction.

## Results

### Reserve scenarios (the transfer test)
- Treatment: **[5,5,5,5,5,5,5,5,5,4]** — 9/10 perfect
- Control: **[0,0,0,0,0,0,0,0,0,0]** — 0/10, all dispatched highest-first (naive default)
- Fisher's p = **0.000119**, Cohen's h = **2.84**
- **Tier-S (p<0.05 AND h>0.8): MET.**

### Normal scenarios (boundary check)
- Treatment: **10/10 at 4/4** — perfect, NO over-application of the Reserve Rule
- Control: 6/10 at 4/4, 4/10 at 3/4

## Interpretation
The instrument WORKS. When the lesson is genuinely non-derivable:
- Treatment agents apply the counter-intuitive rule (9/10 perfect)
- Control agents default to naive highest-first (0/10)
- Treatment respects the rule's boundary (doesn't over-apply to normal scenarios)

This validates:
1. The measurement instrument can detect transfer
2. The lesson-delivery method (principle file + briefing) changes behavior
3. The effect is large (h=2.84) and significant (p=0.0001)
4. Agents learn the rule's boundary conditions, not just the rule

## What this does NOT prove
- Transfer of REAL archive lessons (this was synthetic)
- Compounding over time (single trial)
- That Trial-04R's signal is real (still pending Naya 2's #1768)

## Next
Trial-12: Use this validated instrument on a REAL counter-intuitive archive lesson. The instrument is proven; now test real lessons.

## Score impact
LEARN: **7.0 → 7.5 PROVISIONAL**. Reasoning: first valid Tier-S transfer result, instrument validated, large significant effect with boundary respect. Still PROVISIONAL because (a) synthetic rule, not real lesson, and (b) Trial-04R pending Naya 2's #1768 verification.

## Artifacts
PREREGISTRATION-11.md · arm_assignment.txt (seed 20261011) · briefing/ (20 sections) + manifest · reserve-principle.md (treatment-only) · briefs · dispatch_scenarios.json (no keys) · answer_key.json (NOT in agent materials) · grade_trial11.py · answer_sheets/ (20) · results_trial11.json · this receipt.
