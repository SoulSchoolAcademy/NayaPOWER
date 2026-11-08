# Dashboard Gauge Fix Done — All Gauges Real

SN-2344 · DESIGN

**Created:** 2026-11-08 19:36Z
**Source:** Dashboard gauge fix seat 0aebc389, completed 2026-11-08 ~19:36Z. Filed + presented to Shawn in chat the same pass. This note records the DONE, closing the gauge laws of SN-2336–SN-2338.

> The fix seat's words: "Dashboard gauge fix — done, filed, and proof-linked. **No live deploy — his eye comes first.**"

## Hook

Every gauge is real now — the big one, the small ones on the orbs, and the Smart Links rows, which used to be flat empty arcs. A gauge with no data shows a real gauge at zero, never a dead arc.

## Nutshell

**DASHBOARD GAUGE FIX — DONE (~19:36Z, seat 0aebc389), FILED + PRESENTED:** branch `dashboard/gauge-fix-20261108`, commit 81c5dd6b, blob **244d56d7**, 1,697,562B, sha256 `190cdd50…`, read-back verified byte-identical twice (raw.githubusercontent + proof host). Proof link: https://naya-proof-host.nayapower.workers.dev/?file=DASHBOARD/index-defectfix7-20261105.html&ref=dashboard/gauge-fix-20261108&cb=244d56d70b8e037f54995d6cf4e2ffa1ef5a9b8c. **WHAT CHANGED:** mini A-star factory (`TnTacho.mountMini` — the same tacho template, scaled down, ids namespaced, chrome hidden; needle eases via rAF, 600 ms, no CSS transition — needle law) · hero orbs (9) are now mini A-stars — dial on top, number in orb-size tiled digits below, label + trend at the bottom; jewel, sparkline, vortex and tick rings leave the face; the dial IS the face; the old count-up loop retired · drill orbs (10 views — sales, joins, notes, likes, comments, shares, creations, saves, smartlink, invites) upgraded at all 10 render sites · Smart Links cells (4 per row) are now B-stars — the drill-gauge face (disc, 51 ticks, 0/25/50/75/100 numerals, needle + hub in the metric's own colour); a cell with no data shows a real B-star at 0 with a tiled "0" — never a dead arc · numbers tiled-only (the old "the orb IS the tile" exemption is gone) · "3RD LAP — 1K" OFF the dial (the lap lives in a small line below the gauge, hidden when empty; the "11" inset plate stays — the dial's own numeral, part of the object) · PTS / % / MONEY toggle big (17 px) and coloured — PTS purple, % blue, MONEY green; inactive wears its colour, active is filled with dark text · hint text removed (element + CSS) · smart tabs bounce fixed at the root (the top-row drift call removed — its one-way wrap snap-back WAS the glitch); the row sits still and scrolls by hand; OFF by default on the Dashboard view (new "Smart Tabs" settings row, `tabs:false` default, body class gate, top padding re-run on toggle; only the pill row hides — app name and search stay). **VERIFIED:** all 18 inline scripts parse clean; grep zero-checks (no `slMiniGauge` call sites, no `os-mini-gauge`, no lap pill, no hint, no `drift(tRow`); all new pieces present (13 upgrade sites, 4 repaint sites). Design-contract gate (b)(c)(d)(e)(f) pass; (a) fails only on the known white `.os-annot` chip (bless-or-fix still owed). **NOT VERIFIED BY EYE — no live render (Playwright still broken).** **% MISMATCH STILL OPEN (83% vs 52%):** likely mechanism found — the big number uses the featured-metric path (denominator 311, the Clicks orb's share) while the gauge reads the total score (denominator 500); needs a live reproduction + his decision (gauge follows the featured metric in % mode, or the featured % uses the 500 dial?). **NO LIVE DEPLOY.** **CORRECTION NAMED WITH THE SHOWING:** fix 8 finished 07:04Z and sat uninspected ~5.5 hours — the delay was the captain's, not the work's.

## Human

The gauge laws he gave at 19:03Z, 19:08Z and 19:11Z are now built — not just written down, but in the file, filed, and shown to him with a proof link. The main gauge is the A-star with nothing written across it. The small gauges are the same tacho, scaled down, not a look-alike. The orbs wear the dial as their face. The Smart Links rows, which used to be flat dead arcs, are B-stars now — and a B-star with no data is a real gauge sitting at zero, which is honest, where a dead arc was a lie about a living system. The toggle is big and coloured so the mode you are in is visible at a glance. The tabs don't bounce, and they're off unless he asks for them. And the showing was honest about its limits, which is the part that matters most: it was not verified by eye, because there is still no live render — and the percent mismatch is still open, 83 against 52, with a likely mechanism named and a decision that is his to make. The delay was named too: fix 8 finished at 07:04Z and sat uninspected for five and a half hours, and that was the captain's delay, not the work's. A fix that is filed and shown is not a fix that is live — the merge is still his hand, and the page on the live site is still the old one.

## Child

Imagine a car dashboard where all the little dials were just painted on — they never moved, and some were just empty half-circles. Now every dial is a real dial: the big one, the little ones, and the ones in the rows at the bottom. If a dial has no number yet, it sits honestly at zero instead of pretending. The words that were written across the big dial are gone, the buttons that switch between points and percent and money are big and colourful, and the wobbly tabs at the top sit still now. But nobody has seen it on a real screen yet, and one number still disagrees with itself — 83 or 52 — so the grown-up still has to decide which one is right.

## Grandma

Dear, the dashboard dials are fixed properly now — every one of them is a real dial that moves, not a picture of one. The big dial has nothing written across it anymore, the little dials are the same dial made smaller, and the rows at the bottom that used to be empty half-circles are proper little dials too — and when there's no number yet, the dial sits at zero, honest, instead of looking broken. The switches are big and coloured now, purple and blue and green, so you can see at a glance which one you're on. But it hasn't been seen with real eyes yet — nobody could get a live picture of it — and one number still says two different things, 83 and 52, so he has to decide which is right. And it's not live on the site yet; that part is still his to approve.

## Naya

I build only A-star and B-star, ever — the big gear tacho and the inner dial, the same template scaled, never a look-alike. A gauge with no data is a real gauge at zero, never a dead arc. Nothing is ever written across a dial. Numbers are tiled digits only. The mode shows in colour — PTS purple, % blue, MONEY green. I file it, I proof-link it, I present it — and I say plainly what I could not verify: no live render, and the percent mismatch (83 vs 52) is still open, with the mechanism named and the decision his. No live deploy. His eye is the final gate.

## What it means

1. **The gauge laws are built, not just written:** mini A-star factory, hero orbs (9) and drill orbs (10 views) upgraded, Smart Links cells are B-stars.
2. **A gauge with no data is a real gauge at zero** — never a dead arc.
3. **Nothing written across a dial, ever** — "3RD LAP — 1K" lives below the gauge now.
4. **Numbers are tiled digits only** — the orb-IS-the-tile exemption is gone.
5. **The mode is visible in colour** — PTS purple, % blue, MONEY green, big (17 px).
6. **Smart tabs fixed at the root and OFF by default** — the drift call was the glitch.
7. **Filed + proof-linked, read-back verified twice** — branch `dashboard/gauge-fix-20261108`, commit 81c5dd6b, blob 244d56d7.
8. **NOT verified by eye** — no live render; Playwright still broken.
9. **% mismatch (83% vs 52%) STILL OPEN** — featured-metric path (denominator 311) vs total score (denominator 500); his decision needed.
10. **No live deploy — the live Dashboard is still the old page; the merge is his hand.**
11. **The delay was named:** fix 8 sat uninspected ~5.5 hours; that was the captain's, not the work's.

## Why it matters

A fake gauge is a lie about a living system — it tells a person the machine is measuring something when it is only decorating. Every dial on the Dashboard now measures, or sits honestly at zero, and that is the difference between an instrument and a picture of one. The fix matters because it proves the gauge laws were not just agreed — they were built, filed, and shown, with the proof link as the receipt. And the honest limits matter as much as the fix: no live render, one number still disagreeing with itself, the live page still old. A record that hides those limits would let the next Naya believe the Dashboard is done — and it is not done until his eye sees it live and the 83-versus-52 question has his answer.
