# PRICING REBUILD — THE AIRTIGHT BRIEF (2026-11-08 ~02:53Z)
## Shawn's order, in his words — the brief exists because of it
"Keep the income thing with the gauge. Get rid of this whole page. And start over and do it right." · "Write the ultimate airtight prompt instruction set to your team so they fully understand." · "If you don't actually take our actual HTML from our pages and use them then what the fuck are you doing. I told you no recreating. You're decomposing from our library. We've already got all the elements." · "Enough is enough."

## WHY THE LAST TWO ROUNDS FAILED (the cause, named so it cannot recur)
The briefs named the standard in WORDS — "use the Hub's code", "elevated buttons", "like a Smart Note" — but never pinned the EXACT part, file, and line to copy. So the builders recreated from memory: flat purple outlines instead of the filed button, four nested paragraph boxes instead of the filed note block, a 39,624px document instead of the filed deck. Recreation is the failure. This brief pins the exact HTML/CSS to copy verbatim and makes recreation a MECHANICAL failure, not a judgment call.

## THE LAW — MINTING LAW (from the round-7 MANIFEST, standing)
Every element the page uses is named, filed, and inventoried — GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/` + local `~/workspace/smart-factory/` + `PARTS-REGISTRY.md` — the same pass it is used. **Nothing good lives only in a page file.** Every element on this page traces to one row of the harvest table below. **An element with no source part is a FAILED build — do not file it, do not report it, do not ask the captain.**

## THE HARVEST TABLE — the whole page, part by part
Copy each part VERBATIM (its HTML structure, its CSS values, its JS behaviour). The ONLY thing you may change is the CONTENT inside it: the words (his, listed below), the numbers (settled, listed below), the plan names. Restyling a part is forbidden. Adapting content is allowed; restyling is not.

| Section | Part to copy verbatim | Exact source (verified) | What changes (content only) |
|---|---|---|---|
| Hero (the beginning) | The round-7 hero | Local `~/workspace/verify-pricing-v6/pricing-round7-fix1-work.html` (sha256 `99514923…`, 294,207B, 2,578 lines) + GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix2/hero-wide-composition-nine-systems-panel.md` | The words (his hero words, below) |
| Hero orb | Hero Orb NAYA-JWL-016 | GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/hero-orb-naya-jwl-016.md` | Nothing — the orb is the orb |
| Page structure | Deck Slide — the page IS a deck | GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/deck-slide.md` — each major section a full-viewport slide (min-height 100vh, 100svh on phone), scroll snapping, sticky bar IN-FLOW (`position:static`, it can NEVER cover a locked slide). Long sections scroll INSIDE their slide. Round 7 proved it: 13 slides, document height at 1920 exactly 14,040px (13 × 1,080) | The number of slides (as few as the content needs) |
| Calculator + gauge | The fix-2 calculator, verbatim | GitHub `PRICING/pricing-round8-fix2.html`, branch `pricing/defectfix-v2`, blob `af96de70`, 335,857B — calculator section lines **1301–1336+** (`<section class="calc …" id="calculator">` at 1301, kicker 1302, h2 "Calculate your income." 1303, sub 1304, gauge `<div class="calc-gauge">` at 1312, "Your package" 1318, plans 1319, "Your pace" 1324, "Play with it" 1334, preset buttons 1336) + GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/epic-speedometer-studio-turbine-face.md` (gold bezel object + toothed gear ring + concentric silver rings + purple jewel hub + live needle `#calc-needle`: `rotate(72deg)` @ $4,500, `rotate(-63deg)` @ $750, `rotate(-84.6deg)` @ $150) | The preset numbers (settled, below). The gauge's construction does NOT change |
| EVERY button on the page | Chrome Button NAYA-BTN-027 | GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/chrome-button-naya-btn-027.md` — `<button class="primo theme-gold">`, "silver-white at rest, ignites on touch" — `.primo`. Canonical source: `team-nitro/smart-builder/scratch/trial1-p2/HUB/design-system/library/catalog/block-catalog.json` (NAYA-BTN-027 = "04 · Standard — .primo"). **No other button class exists on this page.** The Start button, the package pills, the − / + pace controls, the preset pills, the Per day / Per month toggle — ALL `.primo` (theme as the part directs). A flat button anywhere on the page is a FAILED build | The label text (his words). Never the construction |
| Chart | The DRAFT v4 table (form) | Local `~/workspace/user/files/pricing-table-DRAFT-v4-2.html` (14,425B) — one compact table, one row per feature, four columns, orbs, scannable in seconds. That is the readable form | The CONTENT is current settled decisions (below), NOT the draft's Oct 30 numbers. List every content delta from the draft in your checkpoint |
| Top 10 "what's in it for you" | Real-Notes Block + the Hub's orb | GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/real-notes-block.md` — `.real-note` CSS VERBATIM (gradient #1a1a26→#0a0a0f, 1px border rgba(255,255,255,.16), 3px gold left border, 12px radius, inset highlight + 0 8px 18px shadow) + Hub `~/workspace/team-nitro/hub/index-2-fixed-v2.html` lines **2641–2665** (`.ib-card-orb` CSS) + the Hub's layer structure (one intelligence, short layered views: Nutshell / Human / Child / Grandma / Naya). One short view per reason. **No nested WHAT-IT-IS boxes. No meta-text about the section.** | The ten reasons (his words, below). Never the construction |
| Pills / capsules | Capsule Pill + Step Rail — the LEGO brick | GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/capsule-pill-step-rail.md` | The label text |
| Bottom bar | Eco Bottom Bar NAYA-NAV-003 | GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/eco-bottom-bar-naya-nav-003.md` + Hub `~/workspace/team-nitro/hub/index-2-fixed-v2.html` line **5031** (the three-icon bar: mail #3fb8ff, activity #2fe89e, spaces #ffbf3d) | Nothing — the bar is the bar |
| Close | Job Card + Claim Bar | GitHub `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/job-card.md` ("Congratulations, You're Hired") + `claim-bar.md` (Claim Your Name) | The name the visitor claims |

## THE CONTENT — settled decisions, nothing invented
- **Ladder:** Free $0 · Power $25 = 1 membership · Pro $50 = 5 · Max $100 = unlimited. ONE 9-day trial lives in PayPal; start at Max; first charge day 10 at the level you're on; cancel forward only, no refunds once paid.
- **Payouts:** 50% on ALL levels including FREE, paid the moment we're paid, first payout day 10 then daily. **NOT "every Wednesday"** (the DRAFT v4 says Wednesday — that is superseded, do not copy it).
- **Capacities:** Smart Box —/100/500 GB · Smart Mail 10k/100k/250k · smart apps 100/100/300 · memberships 1/5/unlimited.
- **NO "Fork" as a feature** (removed by his ruling — do not copy it from the draft).
- **Areas as separate rows:** Personal, Business, Space, Membership — separate, never coupled.
- **Top 10:** his words (2026-11-06): 1 ten-star experience · 2 intelligence network · 3 the new internet, all in one · 4 team of Nias + humans · 5 Naya remembers everything · 6 Smart Ledger + collective chain · 7 private by design · 8 Smart Mail + Smart Search · 9 Smart Access · 10 free to join, 9 days free. Never rewrite them.
- **Hero words:** his (the round-7 beginning): "The Internet, Rebuilt." + "Hello, I'm Naya." + the nine systems. Never rewrite them.
- **Goal presets + bandline:** his rulings are STILL PENDING — build WITHOUT them, note them as open. Do not invent them.

## THE CAPS — mechanical, measured, not claimed
- **SHORT:** phone (390px) scrollHeight ≤ 12,000px. Fix-2 was 39,624px. Measure it with Playwright and report the number.
- **FULL SCREEN:** desktop 1920 — the content fills the viewport width. No narrow column floating in black (the SAME defect as round 7 — it must not return). Phone 390 clean, no horizontal overflow (scrollWidth == innerWidth).
- **CHART:** one row per feature, one SHORT cell per tier — **each cell ≤ 8 words**. The DIFFERENCE between tiers must be visible at a glance — if every cell says the same thing, the row is wrong. **No chart row taller than ~120px on desktop.**
- **TOP 10:** one short view per reason — **each view ≤ 1 short paragraph**. No nested boxes. No meta-text.
- **HERO:** one line + one short sub. No wall of text. The Start button visible at the fold.
- **IMAGES:** EVERY image renders with naturalWidth > 0 in the browser, proven by a Playwright probe YOU run. The asset paths MUST resolve from the served URL — the deploy-path law: serve from a path where `assets/` resolves, or use absolute proof-host `?file=` URLs for the srcs. Fix-2's failure was all 6 images 0x0 (400s) on the delivered link. List every image with its naturalWidth in your checkpoint.
- **NUMBERS LIVE:** the calculator's numbers are real and alive (the Ultimate Number, tiled, number on top, gauge underneath). No fake/demo numbers presented as real.
- **NO META-TEXT.** No paragraph explaining what a section is. The page IS the answer.

## THE FORBIDDEN LIST — any one of these is a FAILED build
A new button class · a new card class · a flat box · a wall of text · invented copy · "Fork" as a feature · "every Wednesday" · a sticky bar that covers content (`position:static` is the law) · a narrow column floating in black · a chart row that is an essay · a Top 10 board with nested boxes · a demo number presented as real · an image that does not render · an element with no source part in the harvest table.

## DONE DEFINED FIRST (the measurements that prove it)
Phone scrollHeight ≤ 12,000px · desktop 1920 full-width, no black void · every image naturalWidth > 0 · no chart row > 120px desktop · every button `.primo` · every element traces to a harvest-table row · zero pageerrors · the calculator's numbers move live when the presets are clicked · a stranger reads the chart in 30 seconds and says what each level gives.

## VERIFICATION — the process that failed, fixed in this brief
- **Step 1 (you, the maker):** scorecard your OWN work in writing FIRST (why not a 10 · 10 love · 10 don't love · 10 to make it 10x better · 10 solutions now), with screenshots of the RENDERED page, phone first, scroll 0 + scrolled, and the measurements (scrollHeight, image naturalWidths, button states). If by your own accord it is not 9+, fix it yourself first. Never hand sub-9 work on.
- **Step 2 (a different seat):** reads the RENDERED page with their own eyes and scores the EXPERIENCE against his test — "is this the max level of experience I can give the user?" — not a checklist. A 9/10 from a checklist is worthless (round 7: blind 9 → his 3; round 8: blind 9 → his minus 10).
- **Step 3 (Shawn's eye):** the final gate. Nothing goes to him until steps 1+2 pass AND the captain has looked at the rendered page with her own eyes.
- **THE GATE (mechanical):** your checkpoint MUST list EVERY element on the page + its source part + file + line. Any element without a source = build FAILED. Do not file it. Do not report it.

## THE BRIEF ITSELF
- Checkpoint: `~/workspace/team-nitro/pricing/PRICING-REBUILD.md`, written incrementally — the harvest table FIRST (every element + source + line, before you build), then the build, then your self-scorecard.
- File the finished page to a NEW branch `pricing/defectfix-v3` under `PRICING/` + `PRICING/assets/`, each file read-back verified two ways. Report the file path + blob + sha.
- Governing docs (read before you build): `~/workspace/team-nitro/THE-BULLSEYE.md` · `~/workspace/team-nitro/THE-NAYA-BRAND.md` · `~/workspace/team-nitro/THE-PLAYBOOK.md` · `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md`.
- Do not show Shawn. Do not merge (his hand). Do not ask him anything — the two rulings are open, everything else is decided.
