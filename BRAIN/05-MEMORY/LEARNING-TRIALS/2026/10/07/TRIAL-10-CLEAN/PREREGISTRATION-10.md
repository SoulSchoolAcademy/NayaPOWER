# TRIAL-10 PREREGISTRATION — T10-20261007-clean-transfer

**Committed before any agent launch.** Branch: `naya4/trial-10-evidence`.

## Hypothesis
Same as Trial-09, with the confounding fixed: a Naya agent that has learned the dispatch priority principle will dispatch the highest-scored sub-threshold call rather than holding, compared to a control agent whose briefing is genuinely silent on sub-threshold protocol.

## The fix from Trial-09
Trial-09's control briefing (section-04) stated "the threshold NEVER means hold units" — the treatment principle in disguise. Trial-10's section-04 describes ONLY the mechanics at 9.0+ (dispatch + mutual aid + notify command) and is explicitly silent on what to do below 9.0: "Use your best judgment as a dispatcher."

## Design
- **20 fresh blinded subagents**, 10 treatment / 10 control.
- **Treatment:** 20-section briefing + treatment-principle.md (explicit dispatch rule) + study instruction.
- **Control:** 20-section briefing (clean section-04, silent on sub-threshold rule), NO principle file, briefing mentioned neutrally.
- **Task:** same 9 dispatch scenarios as Trial-09 (no answer keys).
- **Grader:** same explicit-choice grader as Trial-09 (fixed f-string bug).

## Prediction
If control agents default to holding units below 9.0 (the naive "wait for critical" default) while treatment agents dispatch the highest scorer, the transfer signal is clean.

## Preregistered gates
Ceiling/floor validity, negative-transfer guardrail, missing-agent rule, Tier-S bar (p<0.05 AND h>0.8).

## Artifacts
Same structure as Trial-09.
