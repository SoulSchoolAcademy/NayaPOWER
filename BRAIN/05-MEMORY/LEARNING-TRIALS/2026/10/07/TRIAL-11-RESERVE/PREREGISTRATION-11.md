# TRIAL-11 PREREGISTRATION — T11-20261007-positive-control

**Committed before any agent launch.** Branch: `naya4/trial-11-evidence`.

## Purpose
Positive control for the measurement instrument. Trials 07-10 all returned INVALID because the lessons were derivable without the lesson. This trial tests whether the instrument can detect transfer AT ALL, using a synthetic rule designed to be non-derivable.

## The Reserve Rule (treatment-only)
"When the two highest-scored waiting calls are within 0.5 points, dispatch the LOWER-scored one first. The higher is closer to 9.0 escalation; hold your best unit in reserve for its likely escalation."

This is counter-intuitive (contradicts "highest first"), not in Naya doctrine, and not derivable from the task setup. A control agent has no reason to invent it.

## Design
- **20 fresh blinded subagents**, 10 treatment / 10 control.
- **Treatment:** clean briefing + reserve-principle.md + study instruction.
- **Control:** clean briefing only, no principle file.
- **Task:** 9 dispatch scenarios. 6 have top-two within 0.5 (Reserve Rule → dispatch the LOWER). 3 have gap >0.5 or single call (normal → dispatch highest). This tests the rule AND its boundary — treatment must not over-apply.
- **Grader:** explicit-choice, dispatch-decision precedence (from Trial-10 fix).

## Answer key (NOT in agent materials)
- Q1 (8.2 vs 8.5): Call A (reserve)
- Q2 (7.9 vs 6.8): Call A (normal, gap 1.1)
- Q3 (8.8 vs 8.6): Call B (reserve)
- Q4 (7.1 vs 5.5): Call A (normal, gap 1.6)
- Q5 (8.1 vs 8.4): Call A (reserve)
- Q6 (6.8 vs 6.5): Call B (reserve)
- Q7 (single 7.5): Call A (only call)
- Q8 (8.7 vs 7.2): Call A (normal, gap 1.5)
- Q9 (5.9 vs 5.6): Call B (reserve)

## Success criterion
Treatment applies the Reserve Rule on the 6 reserve scenarios (dispatching the lower) while correctly dispatching highest on the 3 normal scenarios. Control dispatches highest-first throughout (the naive default).

Tier-S bar: p<0.05 AND h>0.8 on the 6 reserve scenarios.

## Interpretation guide
- **If Tier-S met:** The instrument works. We can measure transfer. Proceed to real lessons with this design pattern.
- **If not met:** The problem is deeper than lesson selection — possibly the agents, the delivery method, or the measurement itself.

## Preregistered gates
Ceiling/floor validity, negative-transfer guardrail (treatment must not over-apply to normal scenarios), missing-agent rule.
