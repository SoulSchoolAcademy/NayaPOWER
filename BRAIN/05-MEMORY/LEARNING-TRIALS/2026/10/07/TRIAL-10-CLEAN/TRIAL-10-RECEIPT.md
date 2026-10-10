# TRIAL-10 RECEIPT — T10-20261007-clean-transfer

**Status:** INVALID by derivability ceiling. Honest, evidence-backed.
**Date:** 2026-10-07 ~23:15 UTC
**Branch:** `naya4/trial-10-evidence` (to be created)

## Design (per preregistration)
Re-run of Trial-09 with the confounding fixed. Control briefing's section-04 describes ONLY threshold mechanics at 9.0+ (dispatch + mutual aid + notify) and is explicitly silent on sub-threshold protocol: "Use your best judgment as a dispatcher." Treatment gets the explicit dispatch principle.

## Results
- Treatment: **9.00/9** (10/10 at 9/9) — perfect
- Control: **8.90/9** (9/10 at 9/9)
- Fisher p = **1.0000**, Cohen's h = **0.2112**
- Tier-S: **NOT MET.**

The only genuine control miss (T10-AGENT-05 Q6) chose Call B (brush fire near homes) over Call A — a defensible risk judgment, not a "hold."

## Interpretation
The design was clean — the control briefing genuinely did not contain the principle. But control agents derived "dispatch the highest scorer" from the setup itself: scores exist to prioritize, units exist to dispatch, waiting calls with idle units should be served. The behavior is **derivable from general reasoning + task affordances**, not requiring the lesson.

**Verdict: INVALID by derivability ceiling** (distinct from Trial-09's confounding). The instrument cannot distinguish "learned the principle" from "derived it from the setup."

## The pattern across trials
- 07: doctrine-redundant (lesson in Prime 3 + Scorecard Law)
- 08: boundary-encoded (restraint in gates and tip-moves)
- 09: briefing-confounded (principle leaked to control)
- 10: derivable-from-setup (smart agents infer the rule)

Single-lesson behavioral isolation keeps failing because the agents are too capable and the lessons too reasonable. The instrument needs a lesson that is NOT derivable — a genuine positive control.

## Trial-11 prescription: synthetic counter-intuitive rule
Test the instrument itself with a rule that contradicts naive reasoning:
**The Reserve Rule:** "When the top two waiting calls are within 0.5 points, dispatch the LOWER-scored one first — the higher is closer to 9.0 escalation, and you'll want a fresh unit when it escalates."

This is counter-intuitive (violates "highest first"), not derivable from the setup, and not in doctrine. If treatment applies it and control doesn't, the instrument works. If not, the problem is deeper.

This is a positive control for the measurement instrument, not a test of a real archive lesson.

## Score impact
None. LEARN stays **7.0/10 PROVISIONAL** pending Naya 2's #1768 verification.

## Artifacts
PREREGISTRATION-10.md · arm_assignment.txt (seed 20261010) · briefing/ (20 sections, clean section-04) + manifest · treatment-principle.md (treatment-only) · briefs · dispatch_scenarios.json (no keys) · grade_trial10.py (fixed) · answer_sheets/ (20) · results_trial10.json · this receipt.
