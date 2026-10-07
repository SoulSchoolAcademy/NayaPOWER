# TRIAL-09 RECEIPT — T9-20261007-novel-domain-transfer

**Status:** INVALID by design flaw (confounded control). Honest, evidence-backed.
**Date:** 2026-10-07 ~22:25 UTC
**Branch:** `naya4/trial-09-evidence`

## Design (per preregistration)
- 20 fresh blinded subagents: 10 treatment (dispatch principle + briefing), 10 control (briefing only, no principle).
- Domain: urban emergency dispatch — intended to be outside Naya doctrine.
- Lesson: "highest-scored call gets the next unit even below the 9.0 threshold" (SN-0568's structure, domain-reframed).
- Blinding fix: no answer keys in stimulus files. Schema fix: plain-string answer format.

## Results
- Treatment: mean **8.70/9** (7/10 at 9/9)
- Control: mean **8.40/9** (5/10 at 9/9)
- Fisher two-sided p = **0.6499**, Cohen's h = **0.155**
- Tier-S bar (p<0.05 AND h>0.8): **NOT MET.**

## The design flaw (fatal to this trial's inference)
Section-04-threshold.md in the SHARED briefing (both arms) explicitly states: "below 9.0, dispatch normally — the threshold NEVER means 'hold units until something scores 9.0'; an empty queue with idle units is a failure, not prudence."

This IS the treatment principle, stated in the control arm's materials. Multiple control agents explicitly cited this section as their reasoning. The control was not a true control — both arms received the principle, just phrased differently.

**Verdict: INVALID by confounding, not by ceiling.** The scores cannot distinguish treatment effect from briefing effect.

## What this teaches (durable)
Designing a true novel-domain control is harder than it looks. The briefing must provide domain context WITHOUT encoding the principle being tested. Section-04 was meant to define the threshold neutrally, but "define the threshold" in a dispatch domain inevitably involves saying what the threshold does and doesn't mean — which IS the principle.

For Trial-10: the control briefing must describe the threshold's MECHANICS (what happens at 9.0+: mutual aid, notification) without stating the DISPATCH RULE (what to do below 9.0). The dispatch rule below threshold must be genuinely unspecified for control — leaving them to infer, guess, or default.

## Score impact
None. LEARN stays **7.0/10 PROVISIONAL**. Trial-04R's signal stands pending Naya 2's #1768 verification. Five trials, five honest INVALIDs — each mapping a distinct failure mode:
- 05: instruction-delivered ceiling
- 06: availability-delivered ceiling
- 07: doctrine-redundant ceiling
- 08: boundary-encoded ceiling
- 09: briefing-confounded control (design flaw)

## Artifacts
PREREGISTRATION-09.md · arm_assignment.txt (seed 20261009) · briefing/ (20 sections) + manifest · treatment-principle.md · brief_treatment.txt · brief_control.txt · dispatch_scenarios.json (NO answer keys) · grade_trial09.py · answer_sheets/ (20) · results_trial09.json · this receipt.

## Trial-10 prescription
Re-run the novel-domain design with a clean control briefing: describe threshold mechanics without stating the sub-threshold dispatch rule. If control agents then default to "hold below 9.0" while treatment dispatches, that's the transfer signal.
