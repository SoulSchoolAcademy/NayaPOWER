# DASHBOARD PASS-4 — ONE FAMILY — WORK RECORD
- Brief: ~/workspace/team-nitro/DASHBOARD-PASS4-ONE-FAMILY-BRIEF-20261109.md (checker 7/7)
- Base: GitHub DASHBOARD/defectfix-v7/pass3/dashboard-pass3.html, blob 17195e83, branch dashboard/pass3-hero-orbs-smartlinks-20261109 (LIVE: nayanet.app/dashboard, 1,727,896B, sha256 2826dea5…)
- Gauge source: GitHub PRICING/pricing-live.html, blob a2d06d5b (v74 calculator gauge) + ~/workspace/team-nitro/pricing/rebuild/tntacho.js.html
- Evidence: fix_this_shit_4444.png / FIX_THIS_SHIT_3333.png / fix_this_mess.png (~/workspace/user/media_library/image/)
- Status: coordinator started 21:50Z Nov 9. Builder: TBD. Verifier: TBD (different seat). Deploy: TBD. No merge — Shawn's hand.

## AMENDMENT (Shawn 21:50Z — TAKE THE SHOWN OBJECT)
- Shown object: ~/workspace/user/media_library/image/image_2026-11-09_145009430.png — the pricing calculator speedometer itself. Round black dial, tick marks, $0–$10K labels, "$4.5K" bottom center, needle at value, purple-jewel center hub, purple arc segment, below "$4 500 of $10 000 — Advancing at $6 000" + digit tiles $ / 4 / 5 / 0 / 0 + "/ month".
- THIS is the mini gauge, shrunk. Rules (his words): the gauge must MATCH the stats that are there (needle/labels read the board's OWN numbers — clicks, views, CTR, revenue — scaled to that stat, never a copied $4,500); numbers VISIBLE (digit tiles under the gauge, readable at a glance); DYNAMIC (gauge follows the number); RELEVANT and REAL — a working instrument for that stat, not decoration. Do not paste $4,500/$10,000/$6,000 onto boards whose stats differ. The gauge is the object; the numbers are each board's own.
- Amendment folded into builder dispatch (builder not yet spawned at amendment time).

## BUILD — DONE (builder, 2026-11-09 ~22:00–23:30Z)
- Output: `dashboard-pass4.html` (1,763,093 bytes; patch printed 1,752,826 chars — UTF-8 multibyte; sha256 in the filing section below).
- Patches (all in this dir, all re-verified after each): `patch-pass4.py` (35 edits — the six changes), `patch-pass4b.py` (fix B), `patch-pass4c.py` + `patch-pass4c2.py` (fix C/C2, superseded), `patch-pass4c3.py` (fix C3, the keeper), `patch-pass4d.py` (fix D), `patch-pass4e.py` (fix E).
- JS: all 16 inline script blocks pass `node --check` after every patch.
- Byte-compare vs v74: `compare-pass4.py` exit 0, `PASS4-BYTE-COMPARE.md` — template diff 72 lines, numerals 32, ticks 53, **0 unexplained differing lines** (every difference is the scale parameterization or a documented retention: tnAluHub def, lapline vs bandline).

### The six changes — all done
1. Every mini = the v74 calculator speedometer (mountMiniCalc/templateCalc, byte-compared). Hero keeps the big gear gauge.
2. One presentation on all five boards (Dashboard/Personal/Business/Space/Reports): title → subtitle → nutshell → 4-cell stat row (calculator mini + tiled number + label + sub) → actions. Link cards keep their row structure with the identical 4-cell row.
3. One tile style, one color system (digit-color law; `--mc` tile overrides + the % exception deleted). 498 = [d4,d9,d8] in all three occurrences; 305 = [d3,d0,d5]; 3.2% = [d3,dot,d2,pct] in both.
4. What Naya Does REMOVED as a Dashboard board (only a removal comment remains). Your Reports is a first-class board with the same presentation (542/12/5/3 live from the spine).
5. Hero gauge VISIBLY ALIVE — needle sweeps on load (first reveal) and on every target change (1.2s easeInOut, fix D). PROVEN before/after: base snaps 8→305 in one frame (first 305 at 327ms, distinct values ['8','305']); pass-4 passes through 106 (-77.76°) (distinct ['106','305']). `hero-sweep5-pass4.json` vs `hero-sweep5-pass3base.json`.
6. "Show on gauge" buttons one gold everywhere (computed border rgb(217,165,33) on all 4 board buttons + all link-card buttons). No gray text in scope (quiet tacho number, svgsub, cap, mom-lab/next, wb-demo whitened). No DEMO pill, no visible "No numbers yet" (visible-text check: False; the textContent hit is my own script comment). Quiet boards show the honest "Quiet — nothing measured yet" state in the same presentation.

### Fixes found by self-verification (after the first build)
- **Fix B — minis read as GEAR gauges, not the shown speedometer.** Cause: the dashboard fork ADDED silver gear CSS (`.tn-gear-tooth #8a8a9c`) that the v74 pricing page never had — v74's gears render black-on-black. Proven against the live-rendered v74 gauge (`v74-gauge-truth.png`: clean black dial, white labels, needle, purple jewel/arc). Fix: mini-scoped CSS rendering the gears exactly as v74 does (black), numerals in v74's 9.5px Outfit 800 + glow, shadow texts hidden as v74 hides them. Hero gear gauge untouched.
- **Fix C/C2/C3 — stale "Show on gauge" buttons in the open all-links drill.** After a featured switch, the old holder kept disabled "On the gauge ✓" and the new holder kept "Show on gauge" (pre-existing: HERO FIX (l) re-rendered only the summary box; the drill list is a separate render, and `smartlinkViewRender` lives in an IIFE, not on window). C2's full drill re-render worked but blocked the main thread ~1s (recorder 34 ticks vs base 60, 994ms + 502ms gaps) and froze the hero sweep. C3 replaces it with an in-place swap of only the two affected buttons — verified both directions (after delta: joinus's button back; after joinus: delta's button back).
- **Fix D — the 1.2s change-sweep used easeOutQuint**, which front-loads 76% of the travel into the first 300ms and reads as a snap. Change-sweeps now use easeInOutCubic; first reveal and lap-wrap keep quint.
- **Fix E — % and $ minis silently rendered as COUNT dials.** Every caller passes symbols ('%', '$') but `calcScaleFor` only recognized the words 'pct'/'money', so '%' fell through to the count ladder (labels looked right at 0..100 by luck, but carried no %; plate showed '4' for 3.5%) and '$' the same (revenue dial 0..100, no $). Fix in `calcScaleFor` (one place): '%' → pct, '$' → money. Verified: % 3.529 → plate "3.5%", labels 0%..100%; $ 4500 → "$4.5K", labels $0..$5K; $ 0 → "$0", labels $0..$10.

### Verification — Playwright, by eye (probes in this dir)
- `probe-pass4.py` (1440/390/360, scroll 0 AND scrolled): zero horizontal overflow at all widths; only errors are the 2 Supabase CDN REQFAILs (CDN never loads from this VM — not page errors); zero pageerrors. Screenshots `p4-{hero,smartlinks,linkcards,reports,boards,bottom}-{1440,390,360}.png` — read by eye: black speedometer minis with own-scale labels, correct needles, purple hubs/arcs, digit tiles aligned, gold buttons, quiet states in-presentation, no crashes/overlaps. The 390 hero "clipped tile" in the first run was a screenshot-timing artifact — recheck at scrollY 0 puts the tiles' top at y=151, fully visible (`p4-hero390-recheck.png`; that shot also shows the honest pre-ledger loading state: "Ledger loading — your score appears when the ledger answers").
- `probe-hero-sweep5.py` (above) + `probe-hero-sweep4.py` (joinus switch with the drill buttons) + `probe-hero-sweep3.py` (lap-wrap control: both files sweep via the pre-existing wrap branch — the v5 test isolates the pass-4 branch by staying in one lap).
- Design-contract gate: **OVERALL PASS — MACHINE ONLY** (a) obsidian ✓ (b) elevation 92.3% ✓ — the 25 missing-depth items are pre-existing orb/stage divs (c) gauges alive ✓ (d) no text-in-image ✓ (e) no bare text ✓ (f) no look-alikes ✓ (h) no blunt phrases ✓ (i) N/A. Human checks H1–H5 PENDING (Shawn's eye / verifier).
- Kept, flagged: MOCK DATA toggle (labeled MOCK, opt-in, off by default); metric-strip legend (colors now live only in legend + board jewels); orb minis stay disabled per pass-3 (a); gray text in timestamps/drawer/legend rows untouched (out of scope).

### Self-scorecard (builder's own — why it is not a 10)
- Score: **9/10 by my own eye** on the rendered viewpoints at all three widths. The six changes are done and proven; the deductions are the sweep's coarseness in this VM (steps, not a glide — see NOT-DONE), the pre-existing rAF leak, and the pending human checks.
- 10 love: minis finally read as the shown speedometer · every mini wears its own scale · in-dial plate agrees with the tiles (3.2% = 3.2%) · one presentation on all five boards · tile identity (498 = [d4,d9,d8] everywhere) · gold buttons that tell the truth after a switch · hero sweep proven before/after · honest quiet state in-presentation · What Naya Does gone, Reports first-class · byte-compare 0 unexplained.
- 10 don't love: sweep coarse in this VM · 1.4MB drill list · "Open it" mostly-empty pill bars (pre-existing) · first reveal 5–15s, and a switch during it restarts the clock · mini labels ~5px at 360px · hero still the gear gauge (by design — two gauge languages on one page) · gray text left in timestamps/drawer/legend · MOCK toggle kept · legend colors no longer on gauges/tiles · orphaned rAF loops accumulate on re-renders.
- 10 to make it 10x: unmount TnTacho handles when innerHTML is replaced · faster first reveal · lazy-mount drill gauges · compact "Open it" action row · one gauge language on the page (needs Shawn's word — brief kept the gear hero) · bigger phone dial labels · whiten remaining gray text · remove MOCK toggle once the ledger is live everywhere · retire/re-derive the legend · live landed-numbers read from Shawn's seat.
- Applied now: fixes B/C3/D/E (above). The rAF lifecycle fix is too big for this pass (touches every re-render path — needs its own seat).

## NOT-DONE (honest list)
- Human checks H1–H5 (design gate) — pending Shawn's eye / the verifier. No seat scorecard is proof.
- Hero sweep glides in steps, not smoothly, in this VM: intermediate values ARE observed (8→106→305) but the main thread starves (recorder 36 ticks vs base 49 in the same window). Cause (pre-existing, found this pass): re-rendering boards/links replaces innerHTML without unmounting the old TnTacho handles — orphaned rAF loops accumulate and write to detached nodes. The mount HAS an unmount; nobody calls it on replace. Needs its own seat; not fixed here (scope + risk).
- Live landed-numbers read needs Shawn's seat (Supabase CDN never loads from this VM; all live numbers above are synthetic spine + synthetic links).
- Gray text in timestamps/drawer/legend rows; MOCK toggle + metric-strip legend kept as flagged judgment calls; orb minis still disabled per pass-3 (a).
- The drill list is 1.4MB of HTML (20 full gauge SVGs per open) — heavy; lazy-mounting is future work.
- Filing to GitHub: PENDING (next step — see below).

