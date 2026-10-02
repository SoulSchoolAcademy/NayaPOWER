# Reports Room Two — Scorecard v2 (Naya 4, 2026-10-02, post rip-apart)

Branch: `naya4/room-02-reports-v2` @ `0e2ae87`. Source: six canonical daily
records `BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/` (Sep 27 → Oct 2).
Verified: jsdom DOM pass — 7 tiles / 6 live + 1 todo / 6 cards newest-first /
6 boards open / 0 JS errors; Oct 1 regression (10 sections, prompt, 9-chain,
2 scores) intact; 113 points, 0 marker leaks.

## The rip-apart (Oscar mode — what I tried to break)

1. **Buttons were invisible.** Every control was `#060608` on near-black —
   Shawn caught it. Fixed per his law: silver-white luminous at rest, theme
   color on hover/focus. Specificity audited so hovers still win.
2. **Quotes rendered as bullets.** Source `>` blockquotes became jewel bullets,
   violating the "natural content forms" law. Fixed: points now carry
   `{t, q}`, quotes render as pull-quotes (section-colored bar). Also fixed
   two latent adapter bugs the work exposed: `stripQuote` failed on
   leading-newline blocks, and the thin-section extras path never stripped
   markers at all.
3. **Empty `<ul>`** on sections with nutshell+chain but no points
   (e.g. GOVERNANCE RULE). Fixed — no empty lists render.
4. **Week hardcoded?** No — dynamic, anchored to today. Saturday stays
   dim/inert; it is genuinely the future.
5. **Search** filters the archive on real content. **Provenance** footers carry
   IB ID + snapshot law on every board. **Keyboard**: real buttons,
   focus-visible styles throughout.

## Score: 9.0/10

| Deduction | Why |
|-----------|-----|
| −0.5 | **Transport ends at the room door.** `ReportsLoader.loadDaily` is built and proven (6 reports, missing day non-fatal), but no converged Hub shell calls it yet. The room is a projector the house hasn't plugged in. |
| −0.3 | **My visual verification gap.** DOM/logic verified; the screenshot pipeline failed (leased browser can't reach this VM). The silver buttons and pull-quotes are structurally correct but I have not seen them with eyes. Shawn's visual pass is the real judge. |
| −0.2 | **Source depth.** Sep 27–30 are thin (4–5 sections) next to Oct 1's ten. The room renders faithfully and must not invent depth — this is a source-side gap, noted not blamed. |

Not deducted: WEEKLY/MONTHLY/YEARLY tabs lead to honest empty states — that is
the Brain's real taxonomy (Oct 2 report), and honesty about emptiness is correct.
Not deducted: week strip + archive both show the six reports — Shawn's law, two
different jobs (orientation vs. reading).

## What closes it to 10

- Hub shell adopts `ReportsLoader.loadDaily` → +0.5
- Shawn's eyes: "the buttons feel alive" → +0.3
- A weekly report (or richer dailies) lands in the canonical home → +0.2
