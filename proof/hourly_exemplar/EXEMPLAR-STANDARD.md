# The Exemplar Standard — hourly report, rebuilt to the Design Contract

**Generator:** `pdf_report_exemplar.py` (this directory)
**Sample:** `~/workspace/naya-hourly-exemplar.pdf`
**Branch:** `naya5/design-contract` · **Date:** 2026-10-08
**Status:** CANDIDATE exemplar — pending Shawn living with it.

Shawn's redirect: the hourly PDF he reads every hour did not follow the
design contract. The fix is not describing the laws — it is SHOWING the
standard in the thing he reads. This document is the annotation layer:
**the exemplar IS the contract; the laws below explain WHY each choice
is the way it is**, with contract law IDs.

The reporting worktree (`naya5/automated-reporting`) was NOT modified —
the exemplar imports its data layer read-only. The hourly cron is untouched.

---

## 1. Best-of harvest — what was taken from where, and why it won

| # | Element in the exemplar | Best source | Why it won |
|---|---|---|---|
| 1 | Obsidian field `#0B0D12`, ink `#F5F7FB`, muted `#AAB2BF` | `start.html` + `index-2.html` `:root` maps (Phase-1 reader C §2, §6) | The only two pages with Code-exact field tokens; every other page approximates with literals. Ground truth, not approximation. |
| 2 | Faceted-diamond jewel bullets + header brand mark (Code-exact clip-path) | `index.html` orbital jewel field (Code-exact polygon); `reports.html` jewel bullets; `ledger.html` source jewels | index.html is the only page with the Code-exact `polygon(50% 0%, 86% 28%, 74% 82%, 50% 100%, 26% 82%, 14% 28%)`. reports.html proved jewels work as bullets; ledger proved a jewel row reads as "sources". Synthesis: exact geometry + bullet usage + white-hot core → color aura. |
| 3 | L1 elevation cards: theme glow + inset top light + deep drop shadow, 1.5pt white edge | `index-2.html` boards (L1→L2 nesting); `start.html` step cards; CD-8 numerics `0 18px 42px rgba(0,0,0,.73)` | index-2 owns the depth tokens; start owns the card construction. The exemplar's `GlowCard` draws all three formula layers — no flat surfaces anywhere. |
| 4 | Button-law bar for the single priority: `#050505` pill, white text + mark, 1.5pt white edge, purple glow | `start.html` `.btn` — "the closest implementation of the Code's Button Law anywhere in the set" (reader C §6, §10.4 D11) | The only canonical instance. Parameterized by accent in start; the exemplar fixes chrome = purple (`#9d75ff`) since the priority bar is chrome, not themed. |
| 5 | Pill chips, uppercase micro-type, per-state color (AUTH / claim) | `ledger.html` status chips (CANDIDATE→RATIFIED→…→PASS taxonomy) | Ledger proved chips carry state truthfully. AUTH = emerald ("alive and well / verified"), claim = muted outline (awaiting stamp). |
| 6 | Metrics tiles in spectrum-flow accents (magenta → purple → blue → emerald → yellow) | `reports.html` weekStrip `dayTile`s — "the spectrum-flow law applied to time" (reader C §4) | The single best demonstration of DC-041 in the wild: one tile per day, each its own spectrum color. The exemplar applies the same law to the five metrics (DC-041's 5-set). |
| 7 | Room accent indigo `#6675ff` for the report's chrome | Contract D5 repair (reports.html's `#8a5cff` corrected to index-2's `--accent-reports`) | The report IS the Reports room. The exemplar wears the repaired accent instead of repeating the drift. |
| 8 | 24/18/14 type, body 18px minimum, hierarchy by size | `start.html` presentation scale + contract DC-050/DC-051 | start is the most Code-faithful page. The old hourly PDF ran 14px body everywhere — the contract's "single most-violated rule" (D9). Closed. |
| 9 | Team-coded elements in Shawn's nine colors | `pdf_report.py` dark-edition precedent + Shawn's direct spec 2026-10-08 | His word is the ground truth the contract was waiting on (CD-14). |
| 10 | Ambient field glow ≤ 0.25, jewel brand top-left, evidence footer | `index.html` ambient orbital field; `index-2.html` `--field` radial wash; DC-061 (logo top-left, always) | Ambient light that breathes without distracting (A-LAW-10); brand lockup where the contract demands it. |

**Rejected from the harvest:** `mail.html`'s blue accent (D2 wrong-room), `spaces.html`'s purple flood (D3),
`connections.html`'s purple-as-room (D4), `index.html`'s `user-scalable=no` (D1 hard violation),
`spaces.html`'s 12px ghost buttons (D11), all seven pages' prefixed var families + hex literals (D12).

---

## 2. Law annotations — why each choice is the way it is

- **Background `#0B0D12`, never `#000000`, never light** — DC-020 (sovereign darkness; `#0B0D12`
  room default). The old PDF used pure black; the contract's ground truth is obsidian.
- **Text `#F5F7FB`; secondary `#AAB2BF` only for non-primary** (stamps, source tags, muted
  detail) — DC-034, A-LAW-07. The old PDF used pure `#ffffff` for everything incl. secondary.
- **Body 18px minimum; 24/18/14 scale; hierarchy by SIZE never color** — DC-050, DC-051, A-LAW-07.
  D9 closed: the old PDF's 14px body was the contract's most-violated rule.
- **Jewel = Code-exact clip-path** `polygon(50% 0%, 86% 28%, 74% 82%, 50% 100%, 26% 82%, 14% 28%)`,
  white-hot core → theme aura — DC-070, R-jewel-clip. Never circular "Christmas-light" marks (DC-071).
- **Depth formula on every card**: outer theme glow + `inset 0 1px #fff6` + `0 18px 42px rgba(0,0,0,.73)`
  — DC-065, CD-8. Nothing flat, ever (DC-064).
- **1.5pt white edge light, visible at rest, on every card / button / table** — A-LAW-05;
  conflict X-1 resolved briefing-governs (white 1.5px+ at rest). The old PDF's 0.5pt gray rules
  were the exact failure Shawn named: "you can't see the separation. Fix it with light."
- **Purple `#9d75ff` = glow/chrome, never solid fill** — DC-012, NC-12.2. Purple appears only as
  glow, jewel aura, and the priority bar's chrome halo.
- **Button-law bar**: `#050505` fill · white text + mark ALWAYS · pill 999px · purple glow —
  DC-072/073. No colored text on buttons, ever (A-LAW-06). No clickable-div equivalents.
- **Chips**: pill, uppercase, per-state color — DC-077 (ledger pattern).
- **Spectrum discipline**: every chromatic is a canonical token; metrics follow the DC-041 flow
  as a circular subsequence (magenta, purple, blue, emerald, yellow) — DC-030, DC-031, DC-041.
- **Room accent**: indigo `#6675ff` — DC-040 (Reports), D5 repair. Chrome ignites purple; themed
  elements burn their own color (DC-032).
- **Team colors**: Shawn's nine exact hexes for team-coded elements — his direct spec 2026-10-08,
  resolving contract CD-14 ("PENDING INPUT — not invented"). Recorded, not invented; his word
  is the pin the contract asked for. Notes: Interfaces gold `#FFD700` is near-family to token
  gold `#e8b64c`; Proving red `#FF0000` doubles as alarm semantics for the verifying team
  (contract red = alarm only, NC-2.5 — here it IS the alarm's team, never decoration).
- **Ambient ≤ 0.25 opacity; brand top-left; full width, no max-width** — CD-2, DC-061.
- **Truth**: counts from real outcomes or absent; claim vs AUTH labeled on every score;
  demo/simulated labeled (none in this window) — DC-091, NC-11.
- **Copy**: direct, distilled, invitation-voiced; scored claims; no fluff — A-LAW-08 (copy /10:
  this report scores 8 — it informs cleanly; the remaining 2 is Shawn living with it).
- **Affordances**: ◆ = jewel mark (identity, not navigation); no › (nothing here navigates);
  no decorative glyphs — DC-074.

---

## 3. Gaps closed vs the current hourly PDF (drift-register style)

| # | Gap in the old PDF | Fix in the exemplar |
|---|---|---|
| G1 | Pure-black `#000000` ground | True obsidian `#0B0D12` (DC-020) |
| G2 | Pure-white `#ffffff` text everywhere, incl. secondary | Ink `#F5F7FB`; muted `#AAB2BF` for non-primary only (DC-034) |
| G3 | 14px body everywhere — the D9 systemic violation | 18px body minimum throughout (DC-050) |
| G4 | No jewel signature marks | Code-exact diamond: header brand + every bullet (DC-070) |
| G5 | Flat panels, 0.5pt gray rules ("can't see the separation") | Depth formula + 1.5pt white edge light on every surface (DC-065, A-LAW-05) |
| G6 | No button-law construction | Black-heart pill priority bar, purple chrome glow (DC-072/073) |
| G7 | Gray boxes, no spectrum | Metrics in DC-041 spectrum flow; chips per-state colored (DC-030/031) |
| G8 | Mid-word wraps ("Engine/ering", "authoritati ve") | Breaks only at slashes in team names; short labels |
| G9 | "claim" as flat gray text | Ledger-style AUTH/claim chips — state you can see (DC-077) |
| G10 | Footer collisions | Clean footer: motto left, stamp + page right |

---

## 4. Self-audit — visual laws (the checker covers HTML/CSS; this is a PDF)

Checked against `tools/design_law/check_design.py` rule-for-rule, adapted to print:

- [x] No light backgrounds — page ground `#0B0D12` (luminance ≈ 0.006 « 0.55). No gray washes.
- [x] Body text white `#F5F7FB`; secondary `#AAB2BF` only for stamps/sources/muted detail.
- [x] Body 18px minimum — verified in `_styles()`: base/bullet/cell = 18; nothing under 14, and 14 only for detail/secondary.
- [x] No solid purple fills — purple appears only as glow/aura/chrome halo.
- [x] No amber/rose — gold/yellow are the contract's pinned spectrum members; team gold is Shawn's spec (near-family to token gold).
- [x] No non-token chromatics except Shawn's nine team colors (his direct spec; CD-14 resolution recorded in §2).
- [x] White edge light ≥1.5pt visible at rest on every card, button, table, chip.
- [x] Jewel clip-path Code-exact (fractional points copied from the contract).
- [x] Red used only as alarm/identity-of-the-verifying-team, never decoration.
- [x] Hierarchy by size (24/18/14), never by color; team colors identify, sizes rank.
- [x] Truth: every number traced to ReportData; claim/AUTH labeled; empty sections render honestly.
- [x] `user-scalable=no` — not applicable to PDF; the exemplar's HTML sibling (if ever built) must allow pinch zoom (D1).

**Gate A (the 10 pre-ship checks), scored by looking at all 8 rendered pages:**
1. Lived in the rendered pages — yes, full pass at 55dpi + spot checks. 
...[truncated 1894 chars]