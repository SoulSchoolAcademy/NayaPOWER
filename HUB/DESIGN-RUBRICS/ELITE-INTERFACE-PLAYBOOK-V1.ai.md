# ELITE INTERFACE PLAYBOOK V1 — AI Operating Specification

**Status:** PROPOSED (truth ceiling: CANDIDATE). Awaiting Shawn Vibert's ratification.
**Scope:** every NayaNET Hub screen, room, overlay, and entry page — current and future.
**Precedence:** LAW ZERO (Canonical Design North Star) > 2026-10-04 standing color standard > this rubric > room specs.
**Companion:** `ELITE-INTERFACE-PLAYBOOK-V1.human.md` (plain language), `elite-interface-playbook-v1.machine.json` (enforceable predicates).

## Scoring procedure

1. Score each checkpoint pass(1)/fail(0). No partial credit, no "N/A".
2. Section score = x/10. Total = sum/100. Scorecard value = total/10.
3. **Ship predicate:** `total >= 90`. Below 90: name the misses, fix, re-score. Never present below 90 to Shawn.
4. Record: screen id, SHA of the code scored, date, scorer, per-checkpoint results, misses, re-score date.

## The 100 checkpoints (exact)

### §1 — Visual DNA & Color (1–12)
1. Black primary canvas (canvas = #000–#0a0a0d range; no light canvas).
2. Signature purple accent used sparingly — accent/glow only, never solid fill.
3. True black/white neutrals for text and structure (no muddy grays for body text).
4. Primary buttons black with purple edge glow, lighting up white on interaction. **(Original's white-buttons-with-purple-borders is superseded.)**
5. Glassy cards: backdrop blur 10–16px, 65–75% opacity.
6. Luxury soft shadows — layered depth, never flat black boxes.
7. High text contrast — readable at a glance, no squinting.
8. State colors used sparingly: Emerald = success; gold = warning; error = icon + text required, color TBD within allowed palette (see bound below).
9. WCAG AA contrast on all text states.
10. Semantic color tokens via CSS variables (no hardcoded hex in components).
11. Focus ring: 2px purple glow OUTSIDE the element, always visible on keyboard focus.
12. Gradients gentle and purple-family only; no rainbow. **(Original's purple↔lavender-on-white is superseded by the black canvas.)**

### §2 — Typography & Rhythm (13–22)
13. One UI family, elegant and clear (Inter in the original; principle is "elegant, clear, on-vibe" — the current stack governs the exact family).
14. Type scale: 12/14/16/18/24/32/48. Body target 17–18px, 16px floor pending Shawn's typography ruling.
15. Headlines medium/bold — clear weight contrast with body.
16. Micro-labels uppercase with letterspacing.
17. Max ~75ch line width for reading text.
18. No text over busy backgrounds — glass panels behind text, never raw art.
19. Tabular numerals for all data/numbers.
20. 8px spacing system — all spacing is a multiple of 8.
21. Tightened, consistent vertical rhythm.
22. One clear visual hierarchy per screen — the eye lands where it should.

### §3 — Layout & Structure (23–34)
23. Top command strip ≤72px, always visible.
24. Fixed, sacred primary nav order. **(Original's SmartNET-era nav names — SmartHub/SmartWorld/SmartFeeds — are dated; the principle of fixed order stands.)**
25. One-glance layout order: Metrics → Actions → Charts → Dock → Right-Now.
26. Compact hero; real content above the fold.
27. 12-column grid; 16–24px gutters.
28. Cards snap to the grid — no orphans, no overlaps.
29. "Divine 12" dock: 2–3 priority tiles larger than the rest.
30. Sticky mobile utility bar.
31. Empty states = value statement + one primary action (never a dead blank).
32. Modals light, never fullscreen takeovers.
33. Right panel 360–420px when present.
34. Full screen width used — no max-width caps on the chassis or rooms.

### §4 — Background Magic (35–44) — all gated by LAW ZERO
35. Living 3D aurora — slow, parallax, subtle. **Only if it serves meaning; decoration without meaning is out.**
36. Cursor-reactive particle sprinkles, low density.
37. Sheen layer adds depth without noise.
38. Text contrast never sacrificed to the background — glass mask behind text.
39. Animation loops 20–30s, calm cadence.
40. Background motion ≤2–3% CPU budget.
41. All ambient animation pauses when the tab is hidden.
42. CSS transforms/opacity only for ambient motion (no layout thrash).
43. GPU-friendly filters.
44. Global Low Motion toggle, respected everywhere.

### §5 — Components (45–58)
45. Primary buttons black with purple edge glow (hover: glow intensifies, lifts white). **(Superseded from original white-fill.)**
46. Primary CTA inner-glow pulse, 1200ms cycle — the single most important action only.
47. Soft-press state: scale 0.985 on press.
48. Disabled = 60% opacity + dotted border (never just grayed).
49. Inputs: dark surface; focus = purple ring (2px, outside).
50. Segmented controls preferred over dropdowns where options ≤5.
51. Metric cards: icon chip + label + big number + delta — always in that anatomy.
52. Count-up number animations ≤900ms.
53. Zebra list rows: translucent alternate tint.
54. Glass tooltips (blur, subtle border).
55. Toasts top-right, 3–4s, auto-dismiss with action retained in history.
56. Skeleton shimmer loaders — never spinners.
57. Hover glow scaled to dwell — feels alive, not twitchy.
58. One icon set, inline SVG, stroke-consistent.

### §6 — Data Viz & Insights (59–68)
59. Airy fills, ≤3 data series per chart.
60. Fixed container height — no layout jumps when data loads.
61. Smart Y-axis padding (data never kisses the frame).
62. Line-draw animations 700–900ms.
63. Tooltips lead with the big number.
64. Legends off — inline chips label series.
65. Every chart pairs an Action Panel ("Do this next").
66. Sparklines in previews only, never as the main chart.
67. Tabular numerals on all axes/labels.
68. Empty data → illustration + "Connect source" action.

### §7 — Navigation & Discovery (69–74)
69. Omnipresent search (⌘K palette) from anywhere.
70. Breadcrumbs whenever the user is deep.
71. Dock hover previews (spring, 200ms/24 stiffness).
72. Recents auto-pin — the user never re-hunts.
73. Logical Tab order matching visual order.
74. Esc always closes overlays — no trapped modals.

### §8 — Micro-Interactions & Motion (75–84)
75. Dwell-scaled hover glow.
76. Card tilt ≤6° with shadow parallax.
77. Shadow pop: 120ms down / 240ms up.
78. easeOutQuart (or cubic-bezier(.16,.84,.22,1)) as the standard ease.
79. Staggered entrances 40–60ms apart.
80. Sliding nav underline, 140ms.
81. Spring dock previews (200/24).
82. Crossfade theme toggle — no flash.
83. `prefers-reduced-motion` fully respected.
84. No animation pretends the intelligence is alive — motion communicates state.

### §9 — Accessibility & i18n (85–90)
85. WCAG AA in ALL states (hover, focus, disabled, error included).
86. Focus always visible (see checkpoint 11).
87. Alt-text discipline on every meaningful image.
88. RTL-ready layout (no hardcoded left/right assumptions in logic).
89. Safe at 120% font scaling — no clipped text, no broken grids.
90. Colorblind-safe states — **never color-alone**; every state pairs icon and/or text.

### §10 — Performance, Tech & Handoff (91–100)
91. First paint <1.5s on target hardware.
92. Non-critical JS deferred.
93. Inline SVG, single icon set (see 58).
94. CSS variable tokens for every design value (see 10).
95. Documented component library — every component has a canonical example.
96. Figma mirrors code — no design/code drift without a recorded delta.
97. Snapshot UI tests on canonical screens.
98. **One-click rule:** the screen's primary action is reachable in one click.
99. Right-Now panel = high-signal alerts only, each with a one-tap action.
100. **Consistency over novelty** — a familiar pattern beats a clever new one.

## Binding resolutions (from the six conflicts)

- **Color supersession:** checkpoints 1–4, 12, 45 encode the 2026-10-04 black-canvas standard. The original's white-canvas prescriptions are superseded and MUST NOT be followed.
- **Warn/error re-mapping (mini-scorecard, recorded):** options — (a) warn=gold, error color deferred to Shawn with mandatory icon+text pairing; (b) warn=gold, error=blue; (c) invent a red-family error. Scored: (a) wins — value 9 (unblocks 99 checkpoints honestly), risk 2 (icon+text carry the state per §9), reversibility 10 (one-token change). (b) fails semantics (blue reads as info); (c) violates the standing ban. **Decision: (a).** Error states use white/purple text + icon + label; the dedicated error color is an open question for Shawn within the allowed palette.
- **Mockup bound:** simulations/mockups are legitimate exploration tools. Every mockup is labeled MOCKUP in the artifact itself; a simulation presented as the real artifact is a misrepresentation — the boundary the onboarding voiding established.
- **Below-the-gates bias:** "default to launch/live" applies to internal readiness only. Production deploys, dispatches, and database work remain Shawn's explicit gates.
- **North-star items** (DID/soul-ID/SSO, SmartCoin, offline-by-design, SmartNET-era nav names, Inter-as-mandate): marked in the machine twin with `truth_state: NORTH_STAR`. They MUST NOT be claimed as current or presented to Shawn as shipped.

## Lineage

This rubric is the ancestor of the team's 9.0 auto-approval bar (`BRAIN/01-GOVERNANCE/0003-SYSTEM-SCORECARD-V1.md`: "9.0 is the birth threshold — nothing under 9.0 ships"). The lock-in posture: current law is the continuation of Shawn's standard, not a new process.

## Enforcement

- Today: manual — builders self-score with evidence links; the judge (Naya 1 seat) independently re-scores.
- **Follow-up (named, not faked):** CI enforcement is feasible — a `design-rubric-check` job that validates the machine.json predicates against a scored screen's declared checkpoints (score file present, total ≥ 90, superseded checkpoints not scored on the old values). Out of scope for this PR; proposed as follow-up work.
