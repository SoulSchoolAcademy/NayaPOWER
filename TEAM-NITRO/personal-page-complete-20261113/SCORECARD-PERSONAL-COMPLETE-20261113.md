# SCORECARD — Personal page complete round (2026-11-13)

## What it is

Self-score of the seven-item Personal list against the evidence in `RECORD-PERSONAL-COMPLETE-20261113.md` and `verify-staged.json` / `verify-complete.json`. Scored per item, with the evidence named — never a bare number. The bar is the page as Shawn sees it on the staged link, phone first.

## Why it matters

A score without evidence is a claim. This scorecard says what is proven on the page, what is proven only in mechanism, and what stopped short — so the captain's double-check knows exactly where to look and what still needs a browser that can fetch.

## How to apply it

Read the per-item scores, then the gaps. The gaps are the work: live-data rendering, the points number, and the Lists render need a browser with working external fetch; the Public-query widening and the tab order need the captain's ruling.

---

## Per-item scores

| # | Item | Score | Evidence |
|---|---|---|---|
| 1 | Eight even grid buttons, Join one of them, Settings a small tool icon | **10/10** | 8 buttons equal ±0 px at 390 (110), 1440 (147), 360 (160); Join 8th with green glow, one column at phone; gear 48×48, `⚙️` only, opens `#settings` at all three widths on staged. |
| 2 | One `+` in the bottom bar on the left, exactly five items; both floating pluses gone | **10/10** | Segs `['plus','mail','activity','spaces']` at all widths; `#pluswrap`/`#os-rooms-plus`/`#os-eco-plus` `display:none`; menu exactly five in order (Make a post · Naya note · Smart note · Message · Mail). Drawer consequence named in the record. |
| 3 | The line above the bottom icons gone | **10/10** | Computed seg shadow is the A-fix (no inset white); pixel scan of staged screenshots 8.4 / 14.7 / 15.6 mean brightness vs failing baseline ~80; eye-check confirms no line. |
| 4 | Name unclipped; points pill survives + restyled (Sharpening 2) | **9/10** | Name never intersects Change cover at any width; pill present and correctly placed at all widths; restyled with the Dashboard's tiled digits + gauge line (1293 → 4 tiles + gap, fill 58.6%, digit colours live, no overlap/clipping, eye-checked wide). Minus 1: the pill shows the fallback number on staged, not the citizen's live total — the number is unproven here (points round owns it; fetch blocked). |
| 5 | Hub's exact feed system: three tabs, Smart Tabs re-filter, no composer, full-page creator, Smart Lists | **8/10** | Tabs Personal / Public / Naya Notes in order; feed line literal; composer 0; create row 3 buttons; creator opens in naya + post modes and lands a stub as a full intelligent block; ribbon re-filters (proven locally with stubs). Minus 2: Smart Lists render unproven on staged (store write proven; migration needs `slFetch()`), and the Public tab is owner-scoped by the base query (stated gap, captain to rule). |
| 6 | Smart Feed engine on real matches | **9/10** | Endpoint HTTP 200, gated, 6 matches counted by hand (48/7/4/4/4/4) with reasons; negative control passed; rail cards match the endpoint exactly; feed line literal on the page. Minus 1: the matches are staged test citizens, not real citizens — the honest framing, same as option-A. |
| 7 | Side rail, right side, mini profiles, chat in place, no scroll until overflow, seed honestly marked | **10/10** | 20 cards (6 live + 14 standing), 0 `<img>` at all widths; rail strip at 1440, stacked at phone; header "6 live matches · 14 standing"; Chat/Mail/Audio/Video in order; chat opens in place; audio/video honest status; scroll rule proven by fixture (no scroll at 3, scrolls at 25); sharpening applied (initials only, one nutshell each, live cards carry no invented nutshell). |

## Overall

**9/10 on the build; the proof is 8/10.** Every item is built and measured on the staged page as far as a browser that cannot fetch can measure it. The page itself is complete: nothing in the build is known-wrong. What is missing is not in the page — it is in the proof environment: this VM's Firefox cannot fetch any external URL, so the live wall (26 notes), the live Naya Notes (14), the points number, and the Lists render could not be seen rendering on staged. Those four sub-proofs are owed from a browser with working fetch, and the record names them rather than claiming them.

## What would make it 10/10

1. The staged link opened on a browser with working external fetch (or Shawn's phone): the 26-note wall rendering, Personal 26 / Public 26, Naya Notes 14, the pill showing the live total, and a saved note appearing in "Saved on this device".
2. The captain's ruling on the Public-query widening (owner-scoped today) and the tab order (brief order vs the 04:34Z law).
3. Zero console errors on that same browser — the 64/110/64 staged errors here are all failed external fetches, zero `pageerror`, and will clear when fetch works.

## Gates re-run (before filing)

1. **Is it right?** Yes — the seven items are the list Shawn gave; nothing extra was built, nothing live was touched, the test rows are deleted, other lanes' rows are intact.
2. **Is it what they truly need?** Yes — the whole page as he sees it, not one item alone (Checklist Law / Whole-Page Rule).
3. **Is it mine to do?** Yes — maker seat for this round, on the lane branch, staged only; no merge, no deploy, no PR, no live tap.
4. **Is now the time?** Yes — the points round landed first (sequencing §8 honored: base verified against the points record, pill + hero survive byte-for-byte); the staged rail verification happened before the test-row cleanup.
5. **Can I prove it?** Yes, except where the record says otherwise — every number above is a measurement from `verify-staged.json` / `verify-complete.json` or a service-key read, and the four unproven sub-items are named with their reason instead of claimed.
