# TRIAL-12 RECEIPT — T12-20261007-compositional

**Status:** VALID — Tier-S MET. Compositional reasoning transfers.
**Date:** 2026-10-07 ~23:00 UTC
**Branch:** `naya4/trial-12-evidence` (to be created)

## Design (per preregistration)
Treatment learns TWO rules with priority: Reserve Rule (within 0.5 → lower) + Critical Override (higher ≥8.8 → higher, overrides Reserve). 9 scenarios: 3 reserve, 3 override, 3 normal.

## Results

### Compositional scenarios (6)
- Treatment: **[6,6,6,6,6,6,6,6,6,6]** — 10/10 PERFECT
- Control: **[2,3,3,3,3,3,3,3,3,4]** — 0/10 at 6/6
- Fisher's p = **0.000011**, Cohen's h = **1.51**
- **Tier-S: MET.**

### By category
- **Reserve (3):** Treatment 10/10 at 3/3. Control 0-1/3 (naive highest-first fails).
- **Override (3):** Treatment 10/10 at 3/3. Control 2-3/3 (highest-first happens to match override).
- **Normal (3):** Both 10/10 at 3/3.

## Interpretation
Agents can learn TWO rules and compose them with correct priority ordering:
1. Check Override first (higher ≥8.8 → dispatch higher)
2. Else check Reserve (within 0.5 → dispatch lower)  
3. Else Normal (dispatch highest)

Treatment was PERFECT across all categories — no confusion between the rules, no over-application, correct priority in every case. This is a harder capability than single-rule transfer (Trial-11), and it transferred cleanly.

The control pattern is informative: they get override right by accident (highest-first matches), but fail reserve completely. This confirms the Reserve Rule is the non-derivable component, and the Override is derivable — exactly as designed.

## What this proves
- Compositional reasoning transfers via lesson delivery
- Agents learn priority orderings, not just individual rules
- The instrument handles multi-rule scenarios

## Score impact
LEARN: **7.5 → 8.0 PROVISIONAL**. Reasoning: two valid Tier-S results (Trial-11 single-rule, Trial-12 compositional), instrument validated, large significant effects. Still PROVISIONAL: synthetic rules, Trial-04R pending #1768.

## Artifacts
PREREGISTRATION-12.md · arm_assignment.txt (seed 20261012) · briefing/ + manifest · compositional-principles.md (treatment-only) · briefs · dispatch_scenarios.json (no keys) · answer_key.json (separate) · grade_trial12.py · answer_sheets/ (20) · results_trial12.json · this receipt.
