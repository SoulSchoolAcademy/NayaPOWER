# MAKER REPORT — Official walkthrough FIX4: one phone per screen, Settings phone cloned verbatim

**Staged (only — nothing live, nothing to Shawn directly):** https://official-walkthrough-staging.nayapower.workers.dev/
**Portal:** 47,506,230 B, sha256 `b34e6845ed66c45d46bbe8ce22347fd7d750883e4fcba8dfb0e4d19999defd61`
**Certificate:** 306,117 B, sha256 `58574945f837c9e21c4d9767dce62911d0733ff588452924ad7e2b8242c594e1` (unchanged from fix2)
**Worker:** 47,838,705 B, sha256 `65052a3835de4f013d5250f85bff239c34d796b213e706c2df8b7b1c26e7b37d`, deployment `574d7b01…` on `official-walkthrough-staging` (HTTP 200; staged bytes == local bytes for `/` and `/identity.html`)
**Branch:** `walkthrough-official-20261127` — head now `14c7ab1a629cdcc2ac724f3ba299b86e5a3b1626` (fix4 files + rebuild inputs + evidence; the maker report rides in a second commit — see below)
**Base:** fix2 (checker PASS 9.6), via fix3 (built, staged, verified, never filed — fix3 rides in this same commit)

## The order (Shawn's voice calls, 2026-11-27 ~21:11–21:18 MST)

Fix3 scope first (ends overhaul, phone overhaul, diamond realism, cascading dropdowns), then the governing instruction: take the Settings phone verbatim and clone it for every phone; make each one move and feel alive; inputs light up around the edge as you scroll down. Then the consolidated "do it now" spec: **one phone per screen, in the frame, the whole Settings concept** — superseding the three-across grouping.

## What was harvested verbatim from Settings fix13

- **Source file:** `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO%2Fofficial-template-20261123%2Fbusiness-finish-20261123%2Fsettings-2%2Fbusiness-settings2.html&ref=settings-fix13-2026
1127&cb=f4c5bfd90b8f3a2fc90d020a69c8737cf99b5409` — fetched 2026-11-27, **3,707,782 B, sha256 `5d06172f2974a60cfccc0f3a7cc9efa21ecdc3eb3a179f242a3659b1ffeb5a93`**, saved at `/tmp/fix3-settings.html`.
- **The real N image:** `~/workspace/user/media_library/image/13/135fd495c4d6c625bb58feda8cff57056d465b7b2fc5099e2f03b43787c8f781.png` — studied (black marble centre, white serif N, brushed aluminum ring, purple arc lower-right, on graphite diamond-pattern board).
- **The ball image (the `--ball` webp):** extracted from the Settings file's `--ball:url("data:image/webp;base64,…")` — **512×512, 39,360 B, sha256 `d5890238d4093db9a0455c92b328c7d3cd79c03c7084841adb8f3b6ee3e6b477`**, filed in this commit as `media/ball-n.webp` (blob `11bd6e24…`) and embedded in the built portal as a data URI (verified by sha at build time; the build asserts its base64 prefix).
- **Cloned verbatim into the walkthrough phone:** `.stage` 393/852 with the 40px/12px dual shadow; `.inner` 7-stop brushed-aluminum chrome gradient (`#f4f6f9 0%, #c7ccd6 16%, #787d88 34%, #eef1f5 52%, #969ca7 70%, #dfe3ea 86%, #6d727c 100%`), 11px borders (28px top / 20px bottom desktop); Dynamic Island (`radial-gradient(circle at 86% 50%, #16263f 0 4px, #050607 5px)`, 104×22px); home bar (120×5px); right power + left volume side buttons; the foot graphite board (`repeating-linear-gradient` diamond cross-hatch over `#3a3a3a → #0a0a0a → #2c2c2c`); the ball ring conic (`from 210deg, #fdfdfd, #9a9a9a, #e8e8e8, #5a5a5a, #d5d5d5, #8a8a8a, #fdfdfd`); the marble sphere (`radial-gradient(circle at 32% 26%, #55555f 0%, #232329 30%, #0b0b11 58%, #050607 100%)` + the webp over it); the 62px Marcellus white N with its shadow; the top-left gloss ellipse; the 24s gem spin; the 17px letterspaced ENTER label; the 48px black arrow buttons.

## Before / after, item by item

### 1. ONE PHONE PER SCREEN (supersedes the trio)
- **Before:** 8 groups of three phones across (`#bdTrio`, `#bdGroupProg` header "Group 1 of 8 — Steps 1–3 of 23"), three ENTER balls in a row.
- **After:** one phone in `#bdSingle`, built fresh per step by `buildPhone(step, n, 23)`; no trio element, no grouping header, no "Group of 8" text anywhere (build-asserted). Put in, tap the ball, next — one screen at a time. The engine is a single-phone engine (`render()` / `advance()` / `goBack()`; `GROUPS`/`collectGroup` deleted).

### 2. THE PHONE IS THE SETTINGS PHONE, cloned verbatim
- **Before:** fix2/fix3 phone — close, but its own frame (9/16 aspect, custom bezel, SVG-facet ball centre).
- **After:** the Settings fix13 phone, values above, for every screen — step phones and the end phone share the same `.bd-phone > .bd-inner > statusbar + walkhead + .bd-stage + .bd-foot` structure, the same frame, the same depth, the same aluminum feel, the same real N, the same graphite board. Live probe: phone measures 393/852 within 2%, `--ball` var set to the webp data URI, ring is the Settings conic.

### 3. INPUTS WITH ELEVATION AND REALISM + EDGE LIGHT-UP
- **Before:** white cards (fix2), then obsidian in fix3 but a chosen field only changed border colour.
- **After:** obsidian-black inputs with depth (inset top shadow + bottom highlight + drop shadow, layered card `linear-gradient(135deg, #0d0d13, #050607 55%)`); when a field is chosen it lifts in royal purple (`.bd-chosen`: purple border, purple glow, `translateY(-2px)`) AND a 3s purple edge light-up pulses around it (`bdEdgeGlow`). Live probe + screenshot: Canada and Ontario both purple-lifted, City revealed below them.

### 4. TAP THE N / ENTER BALL — flash, then advance
- **Before:** ball revealed the picture; a separate advance was needed (fix2: ball = reveal; arrows/next advanced).
- **After:** the ball IS Enter. Tap 1 flashes the related image where the step has one (picture map unchanged — 14 pictures on motto/vision/goal/mission/love/dontlove/thing/promise/gift/benefit/unique/connect/work/pillars; 9 steps have no picture). Tap 2 moves to the next input. Picture-less steps advance on the first tap — no forced rule, image only where it makes sense. The video step's ball never advances (it just spins; the video plays) — the arrows advance there. Live probe: motto tap 1 reveals (stays, `.bd-revealed`, bgpic visible) / tap 2 moves to vision; live (no pic) tap 1 goes straight to age_lang; back arrow returns vision → motto.

### 5. CASCADING: country → province → city
- **Before (fix3):** cascade built, but the live probe caught it broken (see the bug below).
- **After:** country → province drops down → city drops down, in the obsidian inputs with the purple selection highlight; the next dropdown appears only after the previous choice; a parent with no map turns the child into a free-text input; "Other…" reveals a text input. Live probe: Canada → Ontario (14 provinces incl. Ontario) → Toronto present in the city list; screenshot shows all three stacked, chosen ones purple.

### 6. ALIVE ON TOUCH
- **Before:** phones sat still except the ball float.
- **After:** the phone lifts on hover (`translateY(-4px)`, shadow deepens) and presses in on touch (`scale(.985)`); the card lifts/presses; the ball presses (`scale(.96)`); the arrows press (`scale(.97)`); the ball floats (5.5s) and its jewel spins (24s, slowed per the icon law); the orbit arcs turn at 180s / 240s reverse (outside almost slow-motion). Nothing flat, nothing dead. (Probe note: the perpetual float makes the ball "never stable" to Playwright's click waiter — the probe force-clicks; a human tap is unaffected.)

### 7. NO GROUPING HEADER
- **Before:** "Group 1 of 8 — Steps 1–3 of 23" over each trio.
- **After:** gone. Each phone is its own separated board, the frame around the edging, one family. The step counter ("1 of 23") stays inside the phone's header, where it belongs.

### 8. ENDS OVERHAUL + DIAMOND REAL
- **Before (fix2):** flat end grid, flat diamond glyph.
- **After (fix3, carried into fix4):** raised spectrum-rim buttons (World purple wide, Hub emerald, Choose plan sapphire, Dashboard gold, Business orange, Space ruby), 8s energy pulse, Hub before Pricing, "Welcome home." + the faceted purple diamond divider. The diamond in the middle is real: the orbit jewel and the end jewel are faceted mini-diamond SVGs (table + crown facets + girdle + specular, purple with a white glint); the ball's centre is the real marble image — which **supersedes fix3's SVG facet ball** per the governing instruction ("take the same phone and use it"). The remaining 347 `&#9670;` glyphs in the shipped bytes are the untouched R5 base's deal/stage chrome, out of scope; the walk regions carry 0 flat glyphs (build-asserted).
- **Eye note (mine, from the screenshots):** the end grid is taller than one phone screen at both 390 and 1440 and scrolls inside the phone — World/Hub/Pricing are visible without scrolling. That is fix2 behaviour, not a fix4 regression.

## The cascade bug the live probe found (and fixed in this round)

The probe's Canada → Ontario → Toronto walk failed: after choosing Ontario, the city fell back to a free-text input instead of a dropdown. Root cause, two parts, both in `engine.js`:

1. **Placeholder text saved as an answer.** `fieldValue()` returned the placeholder option's TEXT (`'Choose…'`) for an unchosen select, and `collectPhone` saved it. The cascade restore then read `'Choose…'` back as a real choice: the province flipped to `'__other'` with `'Choose…'` in its text box, and the city got `pv='Choose…'` (no map entry) → text mode. Fixed: an unchosen select now saves empty (both the cascade branch — `if (!selC.value) return '';` — and the plain-select branch — `if (!el.value) return '';`), and the restore self-heals a stale `'Choose…'` save.
2. **One flag for two listeners.** `wireCascade` shared a single `_bdCascadeWired` flag for the parent-change listener and the field's own change listener — the province select is BOTH the city's parent AND a field of its own, so whichever wired first won and the city-refresh listener never attached. Fixed: separate `_bdParentWired` / `_bdOwnWired` flags; the parent listener refreshes ALL of that parent's children, so shared parents work.

Found with a capture-phase spy (province value `__other` after the country change, city mode flipping to `text` in the same millisecond) and re-proved live after the fix: Canada → Ontario → Toronto dropdowns, 24/25 probe PASS. Debug scripts in `evidence/debug-fix4*.py`.

## Verification

- **Build:** `node build-official.mjs` — **42/42 PASS** (35 carried + 7 fix4/fix3 asserts), rebuilt twice byte-identical. All 10 inline script blocks parse (`new Function`, 0 bad). 8 style blocks. `&#9670;` count 347 (fix3's count, unchanged — walk regions 0).
- **Worker:** `node build-worker-official.mjs` — worker 47,838,705 B sha `65052a38…`, rebuilt byte-identical.
- **Deploy:** `cf-worker.py put-script … official-walkthrough-staging … --meta worker-meta.json` → HTTP 200, deployment `574d7b01…`. (One deploy returned success but the staged bytes still showed the previous sha on an immediate curl — edge-cache lag; re-verified after 20s: staged == local. Named here so the checker doesn't chase it.)
- **Staged curl:** `/` HTTP 200, 47,506,230 B, sha `b34e6845…` == local; `/identity.html` HTTP 200, 306,117 B, sha `58574945…` == local.
- **Live probe** (`evidence/probe-fix4.py`, Chromium via the localhost forwarder, 390×844 + 1440×900): **24/25 PASS** — one phone only, no trio/header, 393/852 shape, real marble ball, cascade, ball flash-then-advance, video ball does not advance, arrows, end reached both widths, 0 page errors. The 1 FAIL is "0 console errors": three 503s on `agmt-b*.jpg` during the probe run — all four images return 200 on direct curl immediately after, KV binding intact; transient edge blip, not a page defect. Screenshots in `evidence/` (step1, cascade, reveal, end 390 + 1440) — read with my own eye (see items 3/4/8 above).
- **Not re-probed this round (carried from fix2, unchanged code):** certificate claim flow, deal/zoom views, remove-account modal. The fix4 diff touches only the walk section/style/script/engine — but the checker should say so if it wants them re-proven, not assume.

## Law conflicts

- **SVG facets superseded by the real image (governing instruction wins):** fix3 built a brilliant-cut SVG diamond as the ball centre; Shawn's order was to take the Settings phone whole, so the ball centre is now the harvested marble webp. The faceted diamond survives as the orbit jewel + end jewel divider. No law broken — the governing instruction is the higher law, and the result is more real, not less.
- **R5 base's 347 `&#9670;` glyphs untouched:** they are the deal/stage chrome he did not ask to touch. The walk regions carry 0. Touching the base would violate "do not touch what he did not ask to touch."
- **`finish()` still hides the end ball via the build step-6 patch** (`enterBtn.hidden = true` → comment): carried from fix2/fix3 — the end phone's ball stays because the end phone is a separate static phone whose ball is never hidden; the patch only stops `finish()` hiding the walk ball. No change.
- **Video step ball doesn't advance:** by design (his picture rule — the video is the picture; the ball plays with it, the arrows move on). Named, not hidden.

## Known gaps (carried, not fixed here)

- No citizen tap route to the deal view (only `window.__fpStage.enter()`); remove-account trigger not tap-reachable (others-list hidden by v1 ruling). Both from fix2, untouched by fix4.
- `portal.html` + `worker-consolidated.js` (47 MB each) are NOT filed in the commit — the blobs API 422s them ("input too large", proven in fix1). The rebuild inputs ARE filed (portal-v1.html unchanged since fix2, sha `88346f9d…`; build scripts; phone parts; steps.js; engine.js; all 14 pictures; NEW `media/ball-n.webp`) and the rebuild was proven byte-identical twice.
- Vault: the Vault state was read from the lane's `VAULT-NOTE.md` (the filed Vault record) before touching the page; no live Supabase read was done. Fix3 + fix4 are filed back into `VAULT-NOTE.md` in this same pass.
