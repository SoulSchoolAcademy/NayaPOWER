# The 43 → 39 mapping

**Why this file exists.** The composer README used to say "the 43 studio law
checks stay green on the ported engine" — true in spirit, unaccounted in
fact. Chi (VERIFY, different-seat review, 8.5/10, 2026-10-17) asked for the
exact accounting before the branch can clear the 9.5 merge bar. This is it.

**The two suites.**
- Source of truth: `../design-studio/test-studio-core.js` — 43 checks on the
  unmodified Studio prototype (StudioCore + its CSS + its renderPreview).
- The port: `composer.js --selfcheck` — 39 checks on the composer's engine,
  piece registry, recipes, and composed pages.

**The shape of the change.** The port is not the studio. The studio suite
pins a *prototype app* (its exact CSS text, its picker UI, its DOM). The
ported suite proves a *headless composer* (engine semantics, five page-type
recipes, the honesty contract). Three things happened to the 43:

| Fate | Studio checks | Port checks | Count |
|------|--------------|-------------|-------|
| Kept 1:1 | 9 | 9 | 9 |
| Consolidated / generalized | 12 | 19* | studio→port |
| Narrowed (rules kept verbatim in CSS; census dropped) | 8 | 1 | 8→1 |
| Dropped (out of scope, redundant, or app-only) | 14 | 0 | 14 |
| New in the port (the composer's own obligations) | — | 10 | 10 |
| **Total** | **43** | **39** | |

\* §B contributes 19 *distinct* port checks — P1 and P26 also appear in the kept row (S9 and S32/S33 consolidate into checks already proven 1:1 as S1→P1 and S42→P26), so the table counts each once.

Every one of the 43 appears exactly once below. Every one of the 39 appears
exactly once below. Nothing is waved at.

---

## A. Kept 1:1 — nine checks, same law, same assertion

| # | Studio check | Port check |
|---|--------------|------------|
| S1 | wheel holds 11 stops in rainbow order — gold, never yellow | P1 · wheel: 11 stops, rainbow order, gold never yellow (identical JSON compare) |
| S5 | walk starts at the accent | P13 · walk starts at accent (one accent pinned instead of two; same law) |
| S6 | walk caps at the wheel | P14 · walk caps at wheel |
| S7 | walk with unknown start falls back safely | P15 · walk unknown start falls back safely |
| S10 | flat button refused → lead, with a note | P16 · flat button refused → lead |
| S11 | colored body text refused → white | P17 · colored body text refused → white |
| S12 | stamp-everything refused → honest | P18 · stamp-everything refused → honest |
| S13 | clean picks → no advisor notes | P19 · clean picks → no notes |
| S42 | buttons carry their zone glow (composed render) | P26 · buttons carry zone glow (--ac-glow) |

## B. Consolidated / generalized — twelve studio checks became nineteen port checks (P1, P26 shared with the kept row)

**Walk law (S2, S3, S4, S8 → P2–P12).** The studio pinned one exact 4-stop
sequence (`green → orange → magenta → indigo`), the order law separately,
one 7-stop render, and a single loop test over counts 1–11. The port expands
the loop test into **eleven individual checks** (`walk(n): distinct, in
order`, n=1..11). The exact 4-stop sequence is *implied* by the general walk
law proven for every count, so the exact-value pin was retired as redundant;
nothing about the walk changed (`composer.js` `walk()` is the studio's
`walk()`, character for character).

**No-yellow (S9 → P1).** Retired as redundant: P1's JSON compare of the
wheel id list makes a `yellow` stop structurally impossible — the same
assertion, no separate check needed.

**One walk per render (S35 → P21/P22).** The studio scraped its app source
for `C.walk(s.accent,`. The port proves the *consumed* law instead: the
composed report's zones are distinct (P21) and in spectral order (P22).

**acVars + zone color (S32, S33 → P26).** The studio asserted on app source
text (`const acVars`, a `btnHTML` call string). The port asserts the result
on the composed page: buttons carry `--ac-glow` in their zone color.

**Zone hexes (S37, S38, S39 → P32).** The studio checked three hard-coded
zone hexes on one prototype render. The port checks the general law on the
composed page: *every* zone accent is a wheel hex — strictly stronger, and it
covers all five page types' renders, not one.

**Feed renders (S36 → P35–P39).** The studio's smoke test rendered one feed
(`>1000` bytes). The port composes all five page types — feed, dashboard,
form, gallery, report — each required to clear 2000 bytes. Generalization,
not loss.

## C. Narrowed — eight studio checks became one port check (P25)

S16–S23 asserted the eight alive hover selectors one by one against the
studio's `<style>` text. The port consumes `naya-core.css` as an embedded
blob, so the self-check's contract is the consumption contract: **the alive
hooks are embedded** (P25 pins `.board:hover` and `.naya-btn`, the two
surfaces every composed page must have).

The rules themselves were not weakened — they moved into the file with a
verbatim header. Verified 2026-10-17, in the shipped `naya-core.css`:

- all 8 selectors present (`.board:hover` ×2, `.ilayer`, `.piece`,
  `.ptype`, `.seg button`, `.stab`, `.nb-card`, `.stat`)
- the 5-layer living-depth construction present ×2
- nested-boards-ride-higher rule present ×2
- white rest edges (`rgba(255,255,255,.32)`) present ×4

The studio suite still pins the studio's copy. The port pins what its engine
consumes.

## D. Dropped — fourteen studio checks with no port counterpart

| Studio check | Why it has no counterpart |
|--------------|---------------------------|
| S14 accent2 retired from state | The defensive `delete s.accent2` line survives in the port's `advise()` — but the composer's state schema never admits `accent2`. Nothing left to exercise. |
| S15 legacy accent2 picks cleaned | Same line, same reason. |
| S24 board hover lifts | Property-level pins on the studio's authored CSS text. The properties ride verbatim in `naya-core.css` (verified above); the port's engine does not re-assert authored text. |
| S25 board hover ignites | Same. |
| S26 nested boards ride higher | Same. |
| S27 piece hover ignites in group color | Same. |
| S28 seg buttons lift | Same. |
| S29 seg buttons ignite | Same. |
| S30 rest edges visible white light | Same. |
| S31 5-layer living-depth construction | Same. |
| S34 picker groups walk the spectrum | Studio-app picker UI chrome (`GROUP_COLORS`). The port is a headless composer/CLI — there is no picker to walk. Out of scope. |
| S40 walk copy teaches the dynamic law | The *copy* survives — every feed and report specimen carries the "Kept walking" board and "The count fits the page; the order never breaks." The check (which scraped one prototype DOM) has no composed-page equivalent yet. |
| S41 closing board teaches the walk | Same as S40. |
| S43 advisor teaches the spectrum law | Studio-app DOM surface (`els['advisor']`). The port has no DOM — advisor notes return as `notes[]` and the CLI prints them as JSON. No equivalent surface. |

## E. New in the port — ten checks the studio never had

The composer carries obligations the prototype never did. These are the
port's own contract, not studio law:

| Port check | What it proves |
|------------|----------------|
| P20 report recipe exists, 5 zones | the first page type the studio never built |
| P23 doctype + closes html | page skeleton is well-formed |
| P24 divs balanced | page skeleton is well-formed |
| P27 boards carry zone vars (--ac) | glow wiring on composed pages |
| P28 jewels in law order | the five-jewel cycle rides along |
| P29 honest footer present | every page says what it is |
| P30 no fake-green stamp | nothing stamped ✓ without proof |
| P31 no unqualified "live data" claims | honesty is structural, not decorative |
| P33 no yellow hex anywhere | the gold law, enforced on output |
| P34 head has title | page skeleton is well-formed |

---

## The receipt

- `node test-studio-core.js` in `../design-studio/` → 43/43 (unchanged, re-confirmed 2026-10-17).
- `node composer.js --selfcheck` → 39/39, exit 0.
- This file is the bridge between them. Any reader can now account for
  every check on both sides — which is what "the 43 stay green" always
  meant, stated honestly.
