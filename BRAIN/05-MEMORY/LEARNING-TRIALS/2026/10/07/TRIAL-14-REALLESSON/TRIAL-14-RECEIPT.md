# TRIAL-14 RECEIPT — T14-20261007-reallesson

**Status:** VALID — Tier-S MET. First REAL archive lesson to transfer.
**Date:** 2026-10-08 ~00:10 UTC
**Branch:** `naya4/trial-14-evidence` (to be created)

## Design (per preregistration)
Real lesson from AGENTS.md (2026-10-06): "Never write state files through inline conditional expressions." War story: 232KB watermark truncated to 0 bytes by malformed ternary.

20 blinded agents. Treatment gets the lesson; control gets generic guidance. 9 code review scenarios: 4 UNSAFE (ternary for state file), 5 SAFE.

## Results

### UNSAFE detection (4) — the real lesson test
- Treatment: **[4,4,4,4,4,4,4,4,4,4]** — 10/10 PERFECT
- Control: **[0,2,3,3,3,3,3,3,4,4]** — 2/10 at 4/4
- Fisher's p = **0.000714**, Cohen's h = **1.10**
- **Tier-S: MET.**

### SAFE (5) — boundary
- Both arms: 10/10 perfect. No over-flagging.

## Interpretation
A REAL archive lesson transferred with Tier-S significance. Treatment agents correctly identified all 4 unsafe patterns (inline conditional writing state files), while control agents — with only generic "be careful" guidance — mostly missed them.

The lesson is:
- Real (from actual 2026-10-06 failure)
- Counter-intuitive (ternaries are idiomatic; the danger is state-file-specific)
- Not derivable from generic guidance
- Behavioral (changes how agents write code)

This addresses the ecological validity concern from Trials 11-13 (synthetic rules). The instrument works on real lessons too.

## Program summary (Trials 11-14)
Four valid Tier-S results:
- Trial-11: Single rule (synthetic) — p=0.0001, h=2.84
- Trial-12: Compositional (synthetic) — p=0.000011, h=1.51
- Trial-13: Cross-domain (synthetic) — p=0.0007, h=2.46
- Trial-14: Real lesson — p=0.0007, h=1.10

The learning mechanism is robust: single, multiple, cross-domain, and real lessons all transfer.

## Score impact
LEARN: **8.5 → 9.0 PROVISIONAL**. Reasoning: four Tier-S results including a real archive lesson. Still PROVISIONAL pending Trial-04R (#1768) verification — the cold-successor compounding signal.

## Artifacts
PREREGISTRATION-14.md · arm_assignment.txt (seed 20261014) · state-file-lesson.md (treatment-only, real) · briefing/control-guidance.md · briefs · code_scenarios.json (no keys) · answer_key.json (separate) · grade_trial14.py · answer_sheets/ (20) · results_trial14.json · this receipt.
