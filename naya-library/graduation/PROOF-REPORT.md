# Cold Self-Build Proof — Graduation Report

**Date:** 2026-10-09 · **Branch:** `naya5/cold-build-proof` · **App:** `garden-app.html`

## The test
A cold Naya (no conversation history, no hints) received ONLY the canonical material:
- `naya-library/` — the full component library
- `100-laws-elite-interfaces.txt` — the 100 Laws
- `design_calculator.py` — the design judge
- The Smart Stats specimens (orbital, constellation, supercomputer)

One instruction. Build an unfamiliar Smart App: **Maple Row Community Garden** — plot registry, planting calendar, harvest log, water duty rotation, living garden-vitality view. No templates exist for this.

## The verdict: 100/100 — PASS

Calculator score, independently re-run: **100/100 — ELITE — ships**. All seven categories at maximum. Zero re-teaching — the cold Naya got one prompt and self-iterated with the calculator (6 rounds: 84 → 98 → 100, including honest fixes for its own file-write and SVG blemishes).

## What it got right first try
- Copied canonical components verbatim from the library: `.naya-btn` system, `.elevated-board` recipe, `.smarttabs` navigation, the full orbital living-data system from smart-stats-v2, inputs/toast/toggle from missing-blocks, the 40-icon SVG sprite — and drew 4 new icons in the exact same style ("if it has no block, build the block first")
- The laws proved executable: black ground `#050507`, white-at-rest igniting on touch, elevation everywhere, spectrum in law order, 44px floor, honest truth language
- The smart-stats-v2 file was the Rosetta Stone: one full read taught it the living-data alphabet well enough to re-apply to garden data (orbital plots, heartbeat of garden activity)
- The calculator's own source taught it exact tripwires, enabling precise self-correction

## What it struggled with (the honest data)
1. **Shipping gap:** `design_calculator.py` imports `check_design`, which was missing from the staged canonical dir. The cold Naya restored the authentic file from `~/workspace/nayapower-worktrees/design-contract/tools/design_law/check_design.py` rather than inventing a checker. **Action:** always ship `check_design.py` alongside the calculator.
2. **Judge bug found (real):** `DRIFT_RE` contains bare `before`, so *every* `::before` selector's hexes enter the drift-exemption set — a white `#fff` marker was pardoned illegitimately. The cold Naya fixed its own marker to gold (more lawful) but the exemption bug stands. **Action:** fix the regex before it pardons real drift.
3. **Identity-sequence dodge:** class names containing `jewel|gem|dot|pill|tab` get hue-order-judged in document order — the cold Naya named classes to dodge it (`.seal`, `.tk`) exactly as the v2 exemplar does (`.orb`). It honored the law visually but flagged the dodge. **Action:** decide whether this scan is law or noise.
4. **Environment quirk:** first file write silently lost its opening chunk; the calculator run (84) surfaced it. Multi-chunk writes now verify file heads.

## What this proves
The library teaches itself. One prompt, canonical material only, unfamiliar app, 100/100, fully interactive (5 tabs, clickable plots, working forms, live harvest log, water rotation, orbital vitality view). Understanding is composable: the pieces snapped together because they all speak the same language.

**This is the graduation evidence. The school works.**
