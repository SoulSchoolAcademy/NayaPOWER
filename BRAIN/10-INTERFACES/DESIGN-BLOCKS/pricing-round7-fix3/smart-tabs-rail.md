# Smart Tabs — Capsule-Pill Rail (Addition 21)

**Filed:** 2026-11-07 (fix3). **Source:** harvested from the capsule-pill language of Addition 5 — the glossy black capsule pills with coloured diamond/square tile inset (`MASTER-BRIEF-ROUND7.md` ~line 166: "the glossy capsule pills"; `TEAM-PREPARATION-MASTERS.md` lines 91–96 and 153: "Capsule pills with diamond tiles | Personal / Dashboard / Factory | Pills, tabs, chips across the page"). The pill itself is the Addition 5 capsule; the rail is the new composition of thirteen of them into a page-level navigator. Nothing about the pill's look was invented — the tone colours come from the page's own palette vars (`--gold #ffbf3d`, `--purple #a06bff`, `--blue #3fb8ff`, `--green #2fe89e`, `--magenta #e84fff`, `--orange #ff9a5a`).
**Where it goes:** one copy at the top of every one of the 13 slides of the pricing page (13 navs, 169 tab links), in-flow — never fixed, never covering locked content by construction. It sits ALONGSIDE the Viewport Rule: tabs move the reader between slides; the deck stays a deck.

## Why it exists

Fix2 had NO page-level tab or category navigation: no `<nav>`, no tab bar (the re-proof's §17.1 inventory: probe `nav a, .smart-tabs a, [class*=tabs] a` returned `[]`; the only `role="tablist"` was the morph widget's persona switcher inside the live slide, which is NOT page navigation). The reader navigated by "scroll and scroll wondering what you are looking at." The rail names every section, so the reader always knows where they are and can jump.

## The design

- **A real object, not flat chrome:** 24px-tall rail, glossy black capsule pills, each with a coloured diamond tile inset (`<i>` — the diamond) in the section's tone, gold ◆ mark at the rail's head. Elevated, lit from top-left, the pill lifts when active (`.is-active` — tone-coloured ring + fill).
- **The 13 tabs (label / tone):** HERO gold · DEMO purple · TIERS blue · LIVE green · SYSTEMS magenta · TOP 10 gold · CHART blue · CALC gold · 9 DAYS purple · VALUE green · HIRED orange · TRUST blue · CLOSE gold.
- **24px because the measurements said so:** every slide's top padding/margin the rail replaces is ≥24px, so no locked landmark moves. A fixed side rail was rejected by measurement (side margins 24px at 1440, 14–17px at 390 — no room); a fixed top/bottom bar was rejected because it would change the deck stops (13 × 1,080, measured by the blind re-proof); any in-flow strip taller than 24px would break the exact-fit slides.
- **Per-slide placement + compensation (net movement of locked landmarks):** hero — between banner-map (art) and banner-head, head padding-top 28→0 (net +4 measured: CTA 965–1,021, still 59px slack); demo — first child (F25 trims absorb it); tiers — first child, `.tiers` margin-bottom 40→16 (free strip net 0); live — first child (portals 1,023→996, more slack); systems — between systems-img and kicker, img margin-bottom 24→0 (net 0); Top 10 / chart / value / trust — first child, internal scroll, no comp; calc — first child, `.calc` padding-top 24→0 (net 0); nine-days — first child (972→996); hired — first child, `.hired-beat` padding-top 32→8 (net 0); close — between banner-bottom and bottom-cta, desktop no comp (button 993→1,017), phone stack trims −32 (button 790–838 → 784–832, 12px slack).
- **Hostess layering:** the rail is `position:relative; z-index:1`; the hostess is z-index:5, so she paints ABOVE the rail — her portrait is never covered, and the pill row gets `padding-right:150px` at ≥861px so no pill ever slides under her.
- **Phone:** the pill row is a horizontally scrollable container (`overflow-x:auto`) — the 13 pills do not fit 390px, so the row scrolls; Firefox tabs into the scrollable container first, then the pills (keyboard: Tab, Tab → HERO).

## Behaviour (JS, one IIFE before `</body>`)

- Tabs are `<a>` anchors (`href="#slide-id"`, `data-slide` index) — no-JS fallback navigation works.
- JS adds instant jump (preventDefault + instant scrollTo), scrollspy active tracking (wheel scroll included), roving tabindex (only the current slide's nav has tabindex 0 — 13 tabbable, never 169), and focus to the target slide (`tabindex="-1"` on all 13 slides) after a jump.
- **The morph persona tabs are untouched** — distinct markup, the page's single `role="tablist"` with its 3 tabs ("A creator" / "A business owner" / "A community builder"). They are not page navigation and must not be mistaken for it.
- New slide ids added for the anchors: `hero`, `tiers-slide`, `live-slide`, `systems`, `top10-slide`, `chart-slide`, `ninedays-slide`, `value-slide`, `hired-slide`, `trust-slide`, `close-slide` (`#demo` and `#calculator` already existed).

## Verification (self-check `r7f3x-selfcheck.py`, run 5, fix3 sha `e97815a2…`)

- Tap each tab → lands on the correct slide at the locked stop: **13/13 @1920** (pageY 0, 1080, 2160, 3241, 4320, 5400, 6480, 7560, 8640, 9720, 10800, 11880, 12960 — the 3241 is a 1px rounding of the live slide's top; cur/active correct) and **13/13 @390** (0, 844, 1688, 2532, 3376, 4220, 5064, 5908, 6752, 7596, 8440, 9284, 10128).
- Active tab tracks on wheel scroll: hero → wheel → demo active @1920 and @390.
- Coverage: **0 overlaps at every stop, both widths** (hostess figures excepted by design — she paints above the rail).
- Keyboard: fresh load, Tab → HERO, Tab → DEMO, Enter → demo @1920 (pageY 1080); @390 Tab → list container (scrollable), Tab → HERO, Tab → DEMO, Enter → demo (pageY 844).
- Roving tabindex: exactly 13 tabbable per current nav, 0 in the other 12 — verified at every tap.
- Screenshots viewed by eye: `r7f3x-1920-tabs-hero.png` (rail clean, HERO active), `r7f3x-1920-tabs-systems.png` (SYSTEMS active, hostess above the rail), `r7f3x-390-tabs-hero.png` (scrollable pill row at 390), `r7f3x-390-close.png` (rail under the art, button clear). 0 errors at all 8 widths.
