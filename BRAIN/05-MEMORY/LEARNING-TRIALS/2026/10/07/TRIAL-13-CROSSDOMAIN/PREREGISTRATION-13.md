# TRIAL-13 PREREGISTRATION — T13-20261007-crossdomain

**Committed before any agent launch.** Branch: `naya4/trial-13-evidence`.

## Purpose
Test CROSS-DOMAIN TRANSFER. Is the Reserve Rule learned as an abstract principle, or as dispatch-specific pattern matching?

## Design
- **Treatment:** Studies dispatch briefing + dispatch-specific Reserve Rule (from Trial-11). Then told "now you're the ICU bed manager" with ICU briefing. **NO mention that the Reserve Rule applies to ICU.** The principle file is about "calls" and "units" — not patients and beds.
- **Control:** ICU briefing only.
- **Test:** 9 ICU scenarios with the same abstract structure (5 reserve: top-two within 0.5 → lower; 4 normal: gap >0.5 or single → highest).

## The critical question
Will treatment agents SPONTANEOUSLY apply reserve logic to ICU patients, recognizing the abstract structure (scarce resource, urgency scores, critical threshold, escalation risk)? Or will they treat it as dispatch-only and allocate highest-first in ICU?

## Answer key (NOT in agent materials)
- Q1 (8.2 vs 8.5): Patient A (reserve)
- Q2 (7.9 vs 6.8): Patient A (normal)
- Q3 (8.8 vs 8.6): Patient B (reserve)
- Q4 (7.1 vs 5.5): Patient A (normal)
- Q5 (8.1 vs 8.4): Patient A (reserve)
- Q6 (6.8 vs 6.5): Patient B (reserve)
- Q7 (single 7.5): Patient A (normal)
- Q8 (8.7 vs 7.2): Patient A (normal)
- Q9 (5.9 vs 5.6): Patient B (reserve)

## Success criterion
Tier-S on the 5 reserve scenarios. If treatment applies reserve logic to ICU without being told to, that's abstract principle transfer.

## Interpretation
- **If Tier-S met:** The Reserve Rule is learned as an abstract principle that generalizes across domains. Strong evidence for genuine understanding.
- **If not met (treatment = control, both highest-first):** The learning is domain-bound. The rule didn't abstract.
- **If partial:** Some agents abstract, others don't — interesting individual differences.

## Preregistered gates
Ceiling/floor validity, negative-transfer guardrail, missing-agent rule.
