# MAXESS Results Ignition Execution — 2026-08-22

## Purpose
Trigger and record the current `rebuild-integrated-results-final.yml` execution while preserving the current product architecture.

## North Star
ASCORE / 447 → Q15 one click → 15 responses → MAXESS_RESULT_V1 → results.nayanet.app hash → decode → validate → window.MAXESS_RESULT → E01 → E02 V3 → E03 → E04 → E05–E09 → complete Results.

## Protected
- 447 assessment scoring and questions
- existing assessment UI and Naya experience
- existing Results architecture
- E05–E09 static sections
- visual design, accessibility, responsive behavior

## Known failure history
The prior integration run failed because the builder assumed the baseline contained canonical dynamic E01–E04 sections. The current workflow uses the authoritative dynamic IDs `e01`, `maxess-e02-v3`, `e03`, and `e04` from the active Results sources.

## Current diagnostic observation
The committed `MAXESS-RESULTS-INTEGRATED-V1.html` currently visible on `main` is not evidence of the corrected build: inspection still finds the legacy `__MAXESS_RESULT_CONSUMER_V2__` bootstrap and no V5 bridge marker. Therefore it must not be shipped. The current workflow is the authority for the next build.

## Required verification
After the workflow completes, inspect the generated artifact rather than assuming the committed artifact is current. Verify one document shell, exactly E01–E09, dynamic E01–E04 from current working sources, protected E05–E09, one Results bridge, no legacy consumer, no raw YAML/Python, valid JavaScript, Q15 first-click/finalizing guard, 15-response MAXESS_RESULT_V1, five dimensions, Results navigation, hash decoding, and E01–E04 hydration.

## Status discipline
IMPLEMENTED ≠ VERIFIED ≠ LIVE VERIFIED.

Do not ship until the generated artifact itself passes the complete gate.
