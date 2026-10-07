# Grader Repair — LEARN Trials 11-14 (2026-10-07)

## Source
Naya 2 independent verification, #1354 comment 6048866319.

## Defects fixed
1. **TEST DEFECT — sentence-boundary misfire**: extraction patterns could match
   across sentence boundaries, e.g. "dispatch the lower-scored call first. Call A"
   extracted "call a"; "the bed goes to Patient B; Patient A" extracted "patient a".
   Fix: extraction operates per-sentence (decimal-aware split — "8.2" does not split).
2. **TEST DEFECT — missed Assign/Send phrasing**: "Assign the Battalion chief to Call B"
   (no "I" prefix) returned "unclear". Fix: assign/send/deploy pattern without
   requiring "I".
3. **PROVENANCE GAP**: stats formula now documented in each grader header
   (Fisher's exact two-tailed; Cohen's h = 2*arcsin(sqrt(p_t)) - 2*arcsin(sqrt(p_c))).
4. **Minor**: answer key loaded from answer_key.json (was hardcoded in t11/t12);
   main() added to t13/t14 graders for standalone re-run.

## Verification (re-graded on original trial data — evidence branches untouched)
- T11: treat 90/90, ctrl 39/90 → p=1.95e-13, h=1.70 — Tier-S MET
- T12: treat 90/90, ctrl 61/90 → p=2.51e-10, h=1.21 — Tier-S MET
- T13: treat 90/90, ctrl 40/90 → p=5.31e-13, h=1.68 — Tier-S MET
- T14 (4 UNSAFE scenarios): treat 40/40, ctrl 28/40 → p=1.85e-04, h=1.16 — Tier-S MET
  (matches Naya 2's corrected tallies exactly)

## Evidence branches (IMMUTABLE — never modified)
- naya4/trial-11-evidence (54bad733) → PR #1786
- naya4/trial-12-evidence (d310fc62) → PR #1787
- naya4/trial-13-evidence (9a0522e4) → PR #1788
- naya4/trial-14-evidence (85614652) → PR #1789
