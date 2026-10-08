# THE ULTIMATE NAYA DESIGN SPEC — Synthesis Rulings
**Status:** CANDIDATE (pending Shawn's ratification + nayanet.live reconciliation)
**Date:** 2026-10-08
**Sources synthesized:** Naya_Design_Standard_Showcase.html, NayaNET_ELITE_DESIGN_STANDARD_LIVE.html, report.html, lists.html, today.html, NayaNET-Design-Code-Convergence-2026-10-08.pdf — against the existing Design Contract V1 (CANDIDATE) and Shawn's direct specs.

> nayanet.live is ground truth. Where any submission contradicts the live site, the live site wins. Live-site reconciliation is PENDING — rulings below are upload-evidence only.

---

## 1. BEST PATTERNS HARVESTED (adopted into the spec)

| # | Pattern | Source | What it is |
|---|---------|--------|------------|
| H-1 | **Truth-state visual language** | Elite | VERIFIED / DEMONSTRATION / NOT LIVE pills on everything. "Animated ≠ alive. Stored ≠ learned. Claimed ≠ proven." Honesty baked into the design system itself. |
| H-2 | **Machine-law governance posture** | Elite | `truth_states` array, `CANDIDATE_NOT_RATIFIED` status honesty, `known_conflicts: HOLD`. Design law as executable data that refuses to pretend. |
| H-3 | **Converged button recipe** | Elite + Convergence + Contract | #050505 black heart, white text + white icon, ≥1.5px white rim at rest, inset top edge light, own-spectrum-color glow on intent, lift on hover / sink on press, 44px touch floor, principal CTA ≥52px, three observable states (IDLE/HOVER/FOCUS), disabled state that cannot pretend to work. |
| H-4 | **Governance mechanics** | Showcase | 15 filterable do/don't laws, 9.0 score gate ("Back it — ship it" / "Bench it"), copyable 6-item pre-ship checklist as the last touch before ship. |
| H-5 | **Three-jobs doctrine** | Showcase | Chrome / Text / Theme never cross. A thing's color is stable everywhere it appears. |
| H-6 | **Failure posture** | Convergence | Hard check fails → do not ship. Conflicting authority → HOLD. Missing evidence → UNKNOWN. No rounding up. Beauty never overrides security/accessibility. |
| H-7 | **"Score the lived render, not CSS"** | Convergence | Design ratings are scored against rendered output, never source. (Directly answers Shawn's "you don't know how to rate design" — the rating target was wrong.) |
| H-8 | **"Every glyph promises a real behavior"** | Convergence Law 14 | Demo stays labeled demo, local stays labeled local, LIVE requires live evidence. A beautiful but inert affordance is unfinished. |
| H-9 | **Living orb mark** | report.html | 58px pure-CSS black orb, orbiting conic light ring, breathing white backlight, inset highlights. The drawn-native-mark ideal. |
| H-10 | **Faceted jewel bullets** | report.html | 26px rounded-square per-card spectrum jewels (◆✦△✧), glow via `color-mix(in srgb, var(--jewel) 55%, transparent)`. Superior to dots — adopted. |
| H-11 | **Feed restraint doctrine** | today.html | "orb · title · nutshell · why-now. No buttons, no modes, no chrome shouting over the intelligence." + "One color, one board. A board is a destination you ENTER." |
| H-12 | **SmartTabs ribbon engineering** | lists.html | Stable identity color per tab (hash so color never shifts), sticky + edge-fade chevrons, ambient drift pausing on touch, roving keyboard, focus traps, Escape global close. |
| H-13 | **Elevation grammar** | Convergence + today.html | Field > Board > Nested panel > Control > Overlay. today.html's `--depth-hi: inset 0 1px #fff6` living-depth recipe is the material base. |
| H-14 | **Release targets** | Convergence | D1=10, D2–D8 ≥9.5, every hard gate passes. No rounding up. |

---

## 2. RULINGS — what's right vs what's not

### R-1. Showcase's LIGHT MODE is disqualified.
A full `prefers-color-scheme: light` re-skin is a constitutional violation. Dark field is law, not preference. The submission's governance mechanics (H-4) are harvested; its light mode is rejected outright. (Already enforced: P-light-bg HARD.)

### R-2. Zero gray text stands — the submissions are wrong, not the law.
Elite (#C8C4D0, #AAB2BF body copy), lists.html (`--sl-dim:#a09a8a`), today.html (`--muted:#aaa4b1`) all ship gray real text. Every instance is a violation. The convergence doc's missing zero-gray law is a gap in THEIR document, not ours. Body text is white (#F5F7FB), always. (Enforced: BODYCOLOR FAIL.)

### R-3. Type scale: Shawn's direct word governs — 24 headlines, 18 body, 14 small.
All submissions violate it (82px/100px heroes; 16px/17px bodies; report.html contradicts itself three ways). The contract's CD-1 mapping (kicker 24 > headline 18) came from source readings — **Shawn's spoken spec overrides it**: 24 IS the headline size. Contract updated: `headline_px: 24`.

### R-4. Nine team colors: names are law, hexes are provisional.
Learning=magenta → Innovation=silver is Shawn's ground truth (team-coded elements in reports). The exact hexes applied in the exemplar are the builder's best-effort rendering — **not verified as Shawn's spoken values**. Recorded as provisional tokens, exempt from P-non-token-chromatic, pending his confirmation of exact values.

### R-5. Spectrum count: nine team colors ≠ twelve chromatic tokens ≠ eight-flow.
Three competing definitions across submissions (8, 10, 12). Ruling: the **nine team colors** are for team-coded elements; the **twelve chromatic tokens** are the working palette; the **eight-flow** (purple→blue→emerald→yellow→gold→orange→red→magenta, cycling) is the alternation sequence for breaking visual flow. Separate jobs, no conflation. (H-5 three-jobs doctrine.)

### R-6. Backgrounds: page root is #0B0D12, period.
Submissions ship #020202, #050507, #0a0a0e — close but drift. #010103 is the entrance variant only, not a page root. Near-blacks are not alternatives.

### R-7. No-adjacent-same-color is HARD — including lists.html's ribbon.
The lists ribbon's adjacent silver at-rest pills conflict with the alternation law. At-rest chrome may share the white/silver rest language; **active/accented** neighbors must alternate. Clarified, not weakened.

### R-8. Smart Connect vs Smart Doors: HOLD.
The convergence doc self-flags the rename. Contract keeps `smart-doors` until nayanet.live rules (ground truth for room names).

### R-9. The "16px floor" is not drift.
Convergence C02 flagged a possible 16px law drift. Verified: the contract's 16px is the **icon readability floor**, not a body-text allowance. P-body-under-18 (HARD) stands. No drift; clarified.

### R-10. Self-declared scores are rejected.
Showcase's 9.4 scores are self-declared — the 10/10 standard rejects them. Elite honestly labels itself CANDIDATE_NOT_RATIFIED. Only independently verified scores count. (This is why the exemplar's first 9.0 was wrong — scored against vibes, not the rendered laws.)

---

## 3. THE LANGUAGE — nailed words (exact, adopt verbatim)

**Brand voice (report.html / today.html harvest):**
- "Naya is black, white, and purple — with a rainbow that knows its place. Black is the night everything floats in. White is the light. Purple is the signature."
- "The laws Naya lives by — checkable, not just beautiful."
- "A claim without verification is a lie told to yourself first."
- "Proof, not promises. Every report carries its evidence and its receipts."

**Builder maxims (adopt as AI-law):**
- "Give every element one color job."
- "Light everything: white at rest, color on touch."
- "Build buttons with black hearts."
- "Size separates, color doesn't."
- "Make the header a front door."
- "No buttons, no modes, no chrome shouting over the intelligence."

**Page language (adopt verbatim):**
- "Your intelligence, filed." / "Every smart note, grouped by what it teaches."
- "When something matters, it appears here — ordered for you, never manufactured to fill the space."
- "No verified highlight was manufactured just to fill the page."
- "Everything retained, organized by what it means — not where it happened to land."
- "ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY"
- IN A NUTSHELL · SAVE TO LIST · VIEW FULL NOTE · ★ SAVED

**Human-first rule (Shawn's law):** write for a human child first. Technicals ride as evidence links, never as prose. PR numbers never appear in body text.

---

## 4. WHAT CHANGED IN THE CONTRACT (machine law)

- `type_scale.headline_px`: 18 → **24** (Shawn's override, R-3). CD-1 updated.
- `tokens.team_colors_provisional`: nine team→color mappings added, status PROVISIONAL (R-4).
- `required_patterns`: + R-truth-states (VERIFIED/DEMONSTRATION/NOT LIVE pills), + R-button-three-states, + R-feed-restraint, + R-jewel-bullets.
- `prohibited_patterns`: + P-self-declared-score (scores ≥9.0 claimed without independent verification).
- `contractor_decisions`: + CD-15…CD-21 (synthesis rulings).
- `conflicts_for_ratification`: + X-4 (team-color hexes provisional), + X-5 (Smart Connect vs Smart Doors — HOLD for live site).
- Status remains **CANDIDATE**. Live-site reconciliation pending before any ratification ask.

## 5. PENDING — nayanet.live reconciliation
- Room names and accents vs live site (main, reports, connections pages)
- Any submission-vs-live contradictions (live wins)
- Final lock only after live findings land
