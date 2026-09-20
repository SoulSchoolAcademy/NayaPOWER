# MAXESS Results — Pre-Launch Cleanup Checklist

**Purpose:** Lock the Results experience only after each section is clean, receives authoritative runtime data, preserves its approved presentation, and passes final real-browser verification.

## Production architecture

`MAXESS Assessment → MAXESS_RESULT_V1 → window.MAXESS_RESULT → E01–E06 Results sections → final continuation`

Rules:
- `window.MAXESS_RESULT` is authoritative runtime data.
- Sections must not invent user scores.
- Demo/fallback result data must not survive in production-facing renderers.
- Preserve approved visuals and copy unless a defect requires change.
- Make the smallest coherent repair; verify after each section.

## Section checklist

### E01 — Score Reveal
- [x] Real `MAXESS_RESULT_V1` consumer present.
- [x] Reads `window.MAXESS_RESULT`.
- [x] `DEMO_SCORE=null` production safety already present.
- [ ] Browser-verified with real result after full Results integration.

**Current finding:** No source repair required at this stage. E01 is already real-data-ready.

### E02 — Five Dimensions
- [x] Reads authoritative `window.MAXESS_RESULT`.
- [x] Renders five dimension entries from result data.
- [x] Listens for `maxess:result-updated` / `MAXESS_RESULT_READY`.
- [ ] Remove any remaining demo-only content if discovered in runtime/source inspection.
- [ ] Browser-verify all five scores and names against real contract.

**Current finding:** Source is already structured as a real-data consumer; do not replace it unnecessarily.

### E03 — Personal Report
- [ ] Remove `DEMO_RESULT` fallback.
- [ ] Require valid `MAXESS_RESULT_V1` data.
- [ ] Preserve approved illuminated-letter presentation.
- [ ] Dynamically derive mastery stage, score, and narrative inputs from the real result.
- [ ] Fail safely when result is missing/invalid.
- [ ] Browser-verify with real contract.

### E04 — Capability Profile
- [ ] Remove hardcoded default `score=82`.
- [ ] Remove hardcoded Direction 82 presentation from initial markup.
- [ ] Derive Direction score from authoritative result dimensions.
- [ ] Derive stage, range, marker position, and narrative from real data.
- [ ] Fail safely if Direction data is unavailable.
- [ ] Browser-verify differentiated values.

### E05
- [ ] Inspect source for demo/fallback result data.
- [ ] Convert to authoritative `window.MAXESS_RESULT` consumption only where required.
- [ ] Preserve approved visual/interaction design.
- [ ] Browser-verify with real Profile A/B.

### E06 — Naya Supercharger
- [x] Approved visual structure preserved.
- [x] Human Maximus Codex wordmark sizing corrected to responsive max 320px.
- [ ] Remove trailing diagnostic/integrity script that Groove exposes as visible text.
- [ ] Preserve nine-system content and approved presentation.
- [ ] Browser-verify E06 boundary has no leaked code/text.

## Final Results artifact hygiene

- [ ] One canonical Results renderer.
- [ ] No obsolete V11/V12/V13/V15/V18/V20 competing renderers in production path.
- [ ] No demo 82 fallback architecture.
- [ ] One canonical final CTA/button.
- [ ] No duplicate IDs or uncontrolled mutation layers.
- [ ] PDF/Print output verified.
- [ ] Responsive verification complete.
- [ ] Accessibility verification complete.

## Integration gate

- [ ] Real 15-answer assessment produces `MAXESS_RESULT_V1`.
- [ ] Results URL receives the real contract.
- [ ] `window.MAXESS_RESULT` hydrates.
- [ ] Visible score equals contract score.
- [ ] Profile A verified.
- [ ] Profile B verified.
- [ ] All required differentiation fields differ A vs B.
- [ ] Public production URL verified.

## Release gate

Do not declare locked until all MUST-FIX items above are complete and the real browser E2E passes against the intended public Results deployment.
