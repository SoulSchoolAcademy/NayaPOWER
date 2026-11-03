# THE FACTORY LAW — v5 (2026-11-03, Naya Nitro Narzan)

## The correction
v3/v4 tried to EXTRACT components from our pages and REASSEMBLE them into templates.
The result was dead: black screens, flat text, no working gauge, no working orbs.
Extraction kills what makes our pages alive — the JavaScript, the data wiring, the soul.

## The law
**THE FACTORY HOLDS WHOLE WORKING PAGES, NOT FRAGMENTS.**

Each template = the live page, fetched fresh, + the citizen's PI injected as
`window.PAGE_*` globals. The page's own code reads these and renders itself alive.

- personal → https://nayanet.app/personal (the real personal page)
- business → https://nayanet.app/dashboard (the real Bugatti gauge + 9 orbs)
- space → https://nayanet.app/space (the real space page)
- membership → NO STANDALONE PAGE EXISTS. It is a view inside space/personal.
  We do NOT invent one. When Shawn builds a real membership page, it gets added.

## Why this is right
1. **Use what we have.** The citizens edit and upgrade these same pages.
2. **Upgrades propagate.** When Shawn improves the dashboard, every future citizen
   page gets the improvement automatically — because we fetch live, never copy.
3. **Nothing dies.** All scripts intact, all data wiring intact, the page is alive
   because it IS the page, not a picture of it.
4. **100x or nothing.** A citizen's page is indistinguishable from Shawn's own —
   because it IS Shawn's own page, wearing their identity.

## Verification (2026-11-03)
v5-personal, v5-business, v5-space built and screenshot-rendered.
Zero page errors. Gauge renders, orbs render, buttons render, smart tabs render.
Verified by Naya Nitro Narzan's own eye before Shawn's. His eye is the final gate.

## Generator
`NIAS/build-v5.py` — fetches live pages, injects PI, writes complete pages.
`build-v5.py --selftest` rebuilds the proof. Never extract. Never rebuild.
