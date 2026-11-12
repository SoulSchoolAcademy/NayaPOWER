# HARVEST — the pieces, laid out (2026-11-08, captain's own eyes)

Shawn's law: pages get made in three minutes because the pieces are laid out —
grab the piece, put it in the page, change the text. This file IS the lay-out.
Every piece below is copied VERBATIM from the file named. Never restyle it.
Never rebuild it "in the style of". Change only the text inside it.

Harvested from the LIVE pages with my own eyes (Playwright Firefox, 1280px,
2026-11-08 16:12Z): Smart Factory + Dashboard. Screenshots + DOM inventory in
this same directory (`smartfactory-1280.png`, `dashboard-1280.png`, `*.json`).

## 1. THE REAL GAUGE — the needle-law speedometer (ONLY gauge. The artifact's fake speedometer is DEAD.)
- Source: `~/workspace/team-nitro/dashboard/defectfix-v7/builder/fix9/fix9-work.html`
  - Mount: `<div id="tn-tacho-mount"></div>` (line 4895)
  - Needle CSS: lines 2660–2675 (`.tn-tacho-needle`, transform-origin 100px 104px,
    drop-shadow, NO CSS transition — rAF owns the motion), 2706 (`.tn-needle-body`)
  - Gear teeth: `.tn-gear-tooth` line 2687 (fill #8a8a9c, stroke #c0c0d0) — the
    gear ring around the dial. Live page: 246 teeth.
  - Helper: `~/workspace/team-nitro/pricing/rebuild/tntacho.js.html` (54,035B)
- The law: number on TOP, gauge underneath, needle laps the dial in sets of 500.
  Needle sweeps 135deg → 405deg; the bottom 90deg gap is never touched; the
  numeral sits BELOW the arc, in the dial's open bottom gap (Shawn 2026-10-31:
  the number must never block the needle's sweep).
- Live proof: Dashboard top viewport — massive gear-ringed dial 0–500, needle,
  "505" in a box at the bottom, orbiting orbs with BIG numbers around it.

## 2. THE BOARD — the elevated obsidian board (every content element is one of these)
- Source: Dashboard fix-9 file, `.ph-card`, lines 2018–2025 + 2074–2075:
```css
.ph-card{background:linear-gradient(180deg,#07070b,#050607);
  border:2px solid rgba(255,255,255,.16);border-radius:20px;padding:28px;margin-bottom:20px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.09),inset 0 -2px 8px rgba(0,0,0,.3),0 14px 36px rgba(0,0,0,.5);
  transition:all .25s;}
.ph-card:hover{border-color:rgba(217,165,33,.6);transform:translateY(-4px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 24px 56px rgba(0,0,0,.6),0 0 44px rgba(217,165,33,.25);}
.ph-card{--ac:#d9a521;}
.ph-card:hover{border-color:var(--ac);box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 24px 56px rgba(0,0,0,.6),0 0 44px var(--ac);}
```
- The accent `--ac` changes per board (gold #d9a521 default; purple, sapphire,
  emerald, magenta, teal, orange per group). Boards change color as you flow
  down, like the intelligent board.

## 3. THE JEWEL — the real jewel (icons, checks, orbs)
- Dashboard `.os-jewel`, fix-9 file lines 3916–3923 (verbatim):
```css
.os-jewel{--jc:#d9a521;display:inline-grid;place-items:center;flex:none;line-height:1;color:#fff;background:radial-gradient(circle at 32% 26%,rgba(255,255,255,.30),rgba(255,255,255,0) 48%),linear-gradient(180deg,#262633,#0b0b12 80%);border:1.5px solid var(--jc);border-radius:9px;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.55),inset 0 -3px 6px rgba(0,0,0,.6),0 5px 12px rgba(0,0,0,.55),0 0 14px -3px var(--jc);text-shadow:0 0 9px var(--jc),0 1px 2px rgba(0,0,0,.65)}
.os-jewel-lg{width:46px;height:46px;font-size:22px;border-radius:13px}
.os-jewel-md{width:36px;height:36px;font-size:17px;border-radius:11px}
.os-jewel-sm{width:23px;height:23px;font-size:12px;border-radius:7px;vertical-align:-5px;margin-right:2px}
```
- Hub `.pj-jewel` + `.pj-jewel-lg`, `~/workspace/team-nitro/hub/index-2-fixed-v2.html`
  lines 1486–1508 (26px / 44px, `--jewel` color, radial highlight, glow).
- Live proof: Dashboard nav pills carry jewels; Smart Factory top carries five
  diamond jewels (magenta, purple, sapphire, emerald, gold); Dashboard orbs
  carry a colored jewel on top of each big number.
- CHECK / X: a ✓ inside an `.os-jewel` with `--jc` green is the check jewel;
  an ✕ inside one with `--jc` grey/red is the X. The jewel is the real part;
  the glyph is content. Never a bare text ✓.

## 4. THE NUMBERS — the Dashboard's high-level numbers
- Live proof: Dashboard orbiting orbs — BIG white numerals (745 CLICKS, 50
  INVITES, 100 CREATIONS) with a colored jewel on top and the label underneath.
  Numbers are the hero, never small grey text.
- The number law (gauge law): number on top, gauge underneath; tiled digits;
  needle laps the dial in sets of 500.
- On the pricing page the numbers ARE the Dashboard numbers: tier prices,
  counts, and the World Power dial all use this treatment.

## 5. THE PILLS — glossy obsidian pills (navigation + buttons, perfectly lined up)
- Live proof: Smart Factory top bar (INTENT ◆ QUESTIONS ◆ TEMPLATES ◆ PIECES ◆
  CONTRACT) with + buttons at both corners; Dashboard top bar (Home, Dashboard,
  About, Today, Smart Notes, Connections, Message); Factory bottom row of
  piece pills (Event, Community, Portfolio, Menu, Signup, Dashboard, Hub...),
  each with a colored jewel + "..." menu.
- Factory DOM: 894 `szpill`, 152 `pcard` (piece cards, each with name/sizes/
  stage/zoom/select/notes). The Factory IS the piece library, laid out.

## 6. THE CHART-AS-BOARDS LANGUAGE (Shawn 16:12Z — the chart viewport, NEXT)
- A chart is just a bunch of boards connected together — skinny rectangles,
  collected together, all the same language, all alive, all filled.
- Separated boards with spacing between chart parts (little rectangles for
  each part of the chart) so you can see.
- Check jewel (green, in the box) for what it has; X for what it doesn't have
  — so they can clearly see what it doesn't have and what it can have.
- Boards change color as you flow down, like the intelligent board.
- The chart data (verified): `~/workspace/team-nitro/pricing/pricing-chart-rows.json`
  — 36 feature rows in 5 groups, exact words, Amendment 3 verbatim.

## 7. WHAT A VIEWPOINT IS
- ONE viewport (1280×900 and 390px). Optimized for the top of the page.
  All the buttons perfectly lined up. The quality, the elegance, the elevation,
  the color, the branding, everything alive. NOT a long text page.
- The page is built viewpoint by viewpoint: top first, his eye, lock it in as
  a smart block, then the next viewport down.

## SOURCES (verified paths — test -f before use)
- Dashboard fix-9: `~/workspace/team-nitro/dashboard/defectfix-v7/builder/fix9/fix9-work.html`
- Hub: `~/workspace/team-nitro/hub/index-2-fixed-v2.html`
- Gauge helper: `~/workspace/team-nitro/pricing/rebuild/tntacho.js.html`
- Chart rows: `~/workspace/team-nitro/pricing/pricing-chart-rows.json`
- Smart Factory live: https://nayanet.app/smartfactory (local canonical file: TO-LOCATE — see THE-INVENTORY.md)
- Family language study: `~/workspace/team-nitro/viewpoints/FAMILY-LANGUAGE-20261108.md`

## ADDENDUM (2026-11-08 16:16Z — the backgrounded find closed the TO-LOCATE)
- **Smart Factory local canonical file FOUND:** `~/workspace/finishing-sweep/proof/pages/smartfactory.html` (558,861B, Oct 23) — the full Factory page, design laws baked in. Deploy: `~/workspace/team-nitro/smart-builder/deploy-smartfactory.py` (worker `smartfactory`, custom domain smartfactory.nayanet.live). This is the file the live page is built from — harvest the Factory's pieces from HERE, not from memory.

## ADDENDUM 2 (2026-11-08 16:16Z — the intelligent block + the smart note, own eyes)
- **THE INTELLIGENT BLOCK ORB (`.ib-card-orb`, Hub lines 2641–2665):** 42px orb, THREE radial gradients (highlight 34%/26%, sheen, color `--oc` with color-mix), 6-layer shadow (inset white ring, inset top light, inset bottom dark, outer glow in its own color, wide glow, cast shadow), `::before` glow ring, `::after` FLOOR shadow (the orb sits ON the page). Playback states `.playing` / `.reading` — the orb FLOWS while Naya speaks. Alive.
- **THE ONE SET OF LAWS (Intelligent Block Rules, LAW ratified 2026-11-06):** `~/workspace/team-nitro/hub-board-edit/intelligent-block-rules-LAW-20261106.md`. Capstone (Shawn 00:14Z): "The whole thing must be a live living object, all the way through, layered on layers upon layers — because that gives the dimensional feel, the multi-dimensional in and out, the 3D real physical object effect." The laws are ONE set through every object — buttons, boards, intelligent blocks, icons, smart apps, pages, sections, gauges. Same elevation, same one light (top-left), same real shadow, same own-color light. "A button and a gauge and a board are the same laws wearing different shapes." L1 every element a real physical object (touchable or it doesn't ship) · L2 one light source top-left always · L3 real shadows and real elevation — depth is mass, not glow ("Cast shadow beneath... Depth is built from SHADOWS, never from glow. Glow is light; shadow is mass. We build mass."); the order: Field > Board > Nested panel > Control > Overlay.
- **THE SMART NOTE FORMAT (SN-2290, newest local `~/workspace/team-nitro/smart-notes/`):** Hook → Nutshell → Human → Child → Grandma → Naya. The same idea told in layers — the Hook, the nutshell, then in a human's words, a child's words, a grandma's words, Naya's words. THIS is what his 16:05Z "in a human note, a child note, a grandma note, a Naya note" meant. The elite smart note intro follows this format — each section its own board, each with its own jewel/orb.
