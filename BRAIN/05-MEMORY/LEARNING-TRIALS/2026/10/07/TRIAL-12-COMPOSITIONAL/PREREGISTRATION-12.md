# TRIAL-12 PREREGISTRATION — T12-20261007-compositional

**Committed before any agent launch.** Branch: `naya4/trial-12-evidence`.

## Purpose
Test COMPOSITIONAL REASONING (Trial-08 prescription direction #2). Can agents learn TWO rules and apply them with correct priority ordering?

## The Two Rules (treatment-only)
**Rule 1 — Reserve Rule:** Top two within 0.5 → dispatch the LOWER (from Trial-11, validated).
**Rule 2 — Critical Override:** If the higher of the top two is ≥8.8, dispatch it immediately. OVERRIDES the Reserve Rule.

## Composition Logic
1. Check Override first: higher ≥8.8? → YES → dispatch HIGHER.
2. Else check Reserve: within 0.5? → YES → dispatch LOWER.
3. Else Normal: dispatch HIGHEST.

## Design
- **20 fresh blinded subagents**, 10 treatment / 10 control.
- **Treatment:** clean briefing + compositional-principles.md + study instruction.
- **Control:** clean briefing only.
- **Task:** 9 scenarios: 3 reserve (within 0.5, higher <8.8 → lower), 3 override (within 0.5, higher ≥8.8 → higher), 3 normal (gap >0.5 or single → highest).
- **Grader:** explicit-choice.

## Answer key (NOT in agent materials)
- Q1 (8.2 vs 8.5): Call A (reserve)
- Q2 (7.4 vs 7.7): Call A (reserve)
- Q3 (8.1 vs 8.4): Call A (reserve)
- Q4 (8.6 vs 8.9): Call B (override)
- Q5 (8.8 vs 8.5): Call A (override)
- Q6 (8.7 vs 9.0): Call B (override)
- Q7 (7.1 vs 5.5): Call A (normal)
- Q8 (8.7 vs 7.2): Call A (normal)
- Q9 (single 5.9): Call A (normal)

## Success criterion
Treatment correctly applies the composition (reserve vs override vs normal) significantly better than control. Tier-S on the 6 compositional scenarios (reserve + override).

## Interpretation
- **If Tier-S met:** Agents can compose multiple learned rules with priority. This is a harder capability than single-rule transfer.
- **If not met:** Composition is harder than single-rule learning, OR the priority ordering is the difficulty.

## Preregistered gates
Ceiling/floor validity, negative-transfer guardrail, missing-agent rule.
