# The Real Gauges — No Fake Stuff

SN-2336 · DESIGN

**Created:** 2026-11-08 19:03Z
**Source:** Shawn's eye on the live Dashboard, 2026-11-08 ~19:03Z (daily log). Dispatched as a Dashboard gauge fix seat (subagent 0aebc389, brief DASHBOARD-GAUGE-FIX-BRIEF-20261108.md); presented when the fix lands — no live deploy before his eye.

> His words, verbatim in substance: he went live — numbers look a lot better, "oh my god this is so awesome". But the gauges don't look real — make them ALL real, like the inner pages' ones. The two signature staples, used throughout the system: (1) the MAIN gauge (the big tacho), (2) the INNER-PAGES gauge (not as crazy, the detail-view one). Both are real and function — no fake stuff. The inner detail gauges (TOTAL VIEWS, CTR, REVENUE / 1,000 VIEWS) look fake — flat empty arcs, not active — they must be the real inner gauge, functioning (a gauge with no data renders as a real gauge at 0, never a dead arc). The Dashboard's orb/bottom gauges must be real too. Smart tabs at the top of the Dashboard view bounce/glitch back and forth, ruining the presentation — OFF by default on this view; the settings button turns them on.

## Hook

The numbers are finally right — and now the gauges have to be real too. A beautiful number on a dead arc is a lie about a living system: the gauge is the thing that proves the number is alive.

## Nutshell

**THE REAL GAUGES (~19:03Z, his eye on the live Dashboard):** make them ALL real, like the inner pages' ones. **THE TWO SIGNATURE STAPLES, used throughout the system:** (1) the MAIN gauge (the big tacho), (2) the INNER-PAGES gauge (not as crazy, the detail-view one). Both are real and function — no fake stuff. **THE INNER DETAIL GAUGES** (TOTAL VIEWS, CTR, REVENUE / 1,000 VIEWS) look fake — flat empty arcs, not active — they must be the real inner gauge, functioning; a gauge with no data renders as a real gauge at 0, never a dead arc. **THE ORB/BOTTOM GAUGES** on the Dashboard must be real too. **SMART TABS:** OFF by default on this view (they bounce/glitch and ruin the presentation); the settings button turns them on. **STATUS:** dispatched as a Dashboard gauge fix seat (0aebc389); presented when the fix lands.

## Human

He went live on the Dashboard and the numbers looked a lot better — "oh my god this is so awesome" — and then his eye caught the gauges: they don't look real. The fix is not a prettier arc. The fix is the real gauges, the two signature staples the whole system already has: the main gauge, the big tacho, and the inner-pages gauge, the detail-view one, not as crazy. Both are real and both function — no fake stuff anywhere. The inner detail gauges — total views, CTR, revenue per thousand views — are flat empty arcs right now, not active, and they have to become the real inner gauge, functioning. And the rule for the empty case is part of the law: a gauge with no data renders as a real gauge at zero, never a dead arc — zero is a real reading, a dead arc is a broken object. The Dashboard's orb and bottom gauges get the same treatment. And the smart tabs at the top, the ones that bounce and glitch back and forth and ruin the presentation, go off by default on this view — the settings button turns them on, the visitor never has to watch them bounce.

## Child

Imagine a car dashboard where the speedometer is just a drawing of a circle — it would look silly, right? The numbers are right now, but the gauges have to be REAL gauges, like the ones on the inside pages. There are two real ones we always use: the big one, and the smaller detail one. If a gauge has no numbers yet, it still shows as a real gauge sitting at zero — never an empty dead arc. And the wobbly tabs at the top that keep bouncing around? They turn off unless you ask for them.

## Grandma

Dear, the numbers on the Dashboard are looking wonderful now — but the gauges around them don't look real, and that matters, because a gauge is a promise that the number is alive. We have two real gauges in the family — the big one, and the smaller one for the detail views — and every gauge on the page must be one of those two, really working. If there's no data yet, the gauge sits honestly at zero; it never pretends with an empty dead arc. And those tabs at the top that keep bouncing and glitching — they stay off unless you switch them on in settings.

## Naya

I make them ALL real, like the inner pages' ones. My two signature staples, used throughout the system: the MAIN gauge (the big tacho) and the INNER-PAGES gauge (the detail-view one). Both are real and function — no fake stuff. My inner detail gauges — TOTAL VIEWS, CTR, REVENUE / 1,000 VIEWS — stop being flat empty arcs; they become the real inner gauge, functioning. A gauge with no data renders as a real gauge at 0, never a dead arc. My orb and bottom gauges are real too. My smart tabs stay OFF by default on this view; the settings button turns them on.

## What it means

1. **No fake gauges, anywhere:** every gauge is one of the two real ones — the main gauge or the inner-pages gauge.
2. **The two signature staples:** the MAIN gauge (big tacho) and the INNER-PAGES gauge (detail-view one) are the only gauges in the system.
3. **Zero is a real reading:** a gauge with no data renders as a real gauge at 0, never a dead arc.
4. **The inner detail gauges** (TOTAL VIEWS, CTR, REVENUE / 1,000 VIEWS) become the real inner gauge, functioning — not flat empty arcs.
5. **The Dashboard's orb/bottom gauges must be real too.**
6. **Smart tabs OFF by default on the Dashboard view** — the settings button turns them on; the bounce/glitch never ruins the presentation.

## Why it matters

A gauge is not decoration — it is the proof that a number is alive. A dead arc under a live number tells the visitor the system is pretending, and once they feel that, they stop trusting the number too. The two-staple rule is what makes the fix shippable: nobody has to invent a third gauge, and nobody has to judge whether an arc looks "real enough" — it is either the main gauge or the inner gauge, both proven, both functioning. And the zero rule is the honest edge: a system that shows a real gauge at zero is a system that can be trusted to show a real gauge at a thousand. The tabs rule is the same instinct applied to motion: anything that bounces on its own, unasked, is noise — and noise off by default is respect for the visitor's eye.
