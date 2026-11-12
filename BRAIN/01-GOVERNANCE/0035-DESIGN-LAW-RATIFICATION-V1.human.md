# 0035 — DESIGN LAW RATIFICATION (PR #2742, DESIGN LAWS v2)

**NAYA HONOR. NAYA LAW. ALWAYS.**

*Governance set 0035 · Ratification record — ratified in part by Shawn Vibert, Human Director, 2026-10-22 ~00:29Z (his eight-gate decision word on GT-070: "verify the set against his design standard, ratify the matching elements on the record; any conflicting element is named and excluded, never swept in"). Three tongues, one truth: this human form carries the prose and the full verification table; the AI form is `0035-DESIGN-LAW-RATIFICATION-V1.ai.md`; the machine form is `0035-design-law-ratification-v1.machine.json`.*

*Subject set: PR #2742, "Design laws v2 — 3-pass scored 9+ for ratification", file `DESIGN/DESIGN-LAWS-V2.md`, head `17ec7e8ee36e203e3f5742f97929d8c60308237c` (branch `nitro/design-laws-v2`), merged 2026-10-21 as merge commit `a6875b7a0fd4ae9377ff50aca90fd3b01f300043`; file blob at main `4b4060098b9ebbafd52c3d67c6668cd0d268f26a`, 326 lines. Verified live 2026-10-22: main tip `3e35516787f4b1b2bf9793e9a685ad056a25265e` (ref-anchored).*

## What this record settles

The merged file carries the header "STATUS: RATIFIED BY SHAWN VIBERT — 2026-10-21" (second commit of #2742, `17ec7e8e`). Until this record, that claim was **CLAIMED-UNVERIFIED**: the original PR body (`c68c412b`) said the opposite — "DRAFT FOR RATIFICATION — the stamp is Shawn's alone; nothing here is marked ratified" — and no ratification word from Shawn was on record for it.

Shawn's actual word, 2026-10-22 ~00:29Z, is narrower and is the only ratification this set has: **the elements that match his design standard are ratified; every conflicting element is named below and excluded.** This record is that ratification. Elements marked CONFLICT are **not ratified**, whatever the merged file's header says. A cure PR against `DESIGN/DESIGN-LAWS-V2.md` is the route to ratify them later; this record does not edit that file.

## Shawn's design standard — the measuring stick (exact)

- Black / white base
- Purple / deep-purple glow
- Spectrum, in this order: `#a06bff` → `#3fb8ff` → `#2fe89e` → `#ffbf3d` → `#ff9a5a` → `#ff5e6c` → `#e84fff`
- 18px body text
- Jewel 3D
- Mobile-first
- Domain: nayanet.live

## How verdicts were given

- **MATCH** — the element states the standard's value exactly, or is a design detail consistent with every pillar of the standard and contradicting none. MATCH elements are **ratified**.
- **CONFLICT** — the element states a different value, adds a value the standard excludes, orders values differently from the standard, or a pillar of the standard has no counterpart in the set (missing rule). The exact conflict is named. CONFLICT elements are **excluded from ratification**.
- **NOT-A-DESIGN-ELEMENT** — process, governance, sourcing, or record text. It is neither ratified nor rejected as design; it stands or falls by its own process, not by this record.

Evidence is the merged file's own bytes (`DESIGN/DESIGN-LAWS-V2.md` at main, blob `4b406009`), cited by section and quoted value.

## The verification table

### Foundation and Laws 0–1

| # | Element (section) | Verdict | Evidence / exact conflict |
|---|---|---|---|
| 1 | Status header — "RATIFIED BY SHAWN VIBERT — 2026-10-21" | NOT-A-DESIGN-ELEMENT | Process claim, not a design element. Was CLAIMED-UNVERIFIED until this record; superseded by the bounded ratification below (MATCH elements only). |
| 2 | LAW 0 — audience split (builders compose / makers make / checkers check) | NOT-A-DESIGN-ELEMENT | Process / role text. |
| 3 | The Compose Ladder (compose → tweak → create) | NOT-A-DESIGN-ELEMENT | Process text. |
| 4 | Master Statement — "White light at rest, own color on touch" | MATCH | White base at rest; ignition in the element's own spectrum color. Matches black/white base + spectrum pillars. |
| 5 | LAW 1 — black ground, deep rich black `#050507`, never gray, no light background | MATCH | Black base, exact bytes `#050507`. |
| 6 | LAW 1 — white-lit edges, visible white borders 1.5px+ at rest | MATCH | White base, exact bytes "1.5px+". |
| 7 | LAW 1 — buttons rest dark: black center `#050505`, white text + icon, white rim; spectrum never worn at rest | MATCH | Black/white base, exact bytes `#050505`. |
| 8 | LAW 1 — inputs ignite purple (purple edge + purple glow on focus) | MATCH | Purple glow pillar, stated for inputs/chrome. |
| 9 | LAW 1 — hover: lift + ignite in own color, glow `0 0 26–46px`; chrome ignites purple | MATCH | Purple glow + spectrum-on-touch; deep-purple register is carried by the dark purple-tinted surfaces of LAW 3 (`#1a171f`). No value contradicts the standard. |
| 10 | LAW 1 — timing/motion (`.18s` / `.28s`, `cubic-bezier(.16,.84,.22,1)`) | MATCH | Motion detail; contradicts no pillar. |
| 11 | LAW 1 — breathing ambient motion; data as holograms (glass sheets, parallax planes) | MATCH | Dimensional / jewel-3D-consistent detail; contradicts no pillar. |

### LAW 2 — Spectrum

| # | Element (section) | Verdict | Evidence / exact conflict |
|---|---|---|---|
| 12 | LAW 2 principle — spectral order, never clumped, never random | MATCH | Same ordering/clumping principle as the standard's fixed sequence. |
| 13 | Wheel stop — purple `#a06bff` | MATCH | Exact standard hex, stop 1 of the standard. |
| 14 | Wheel stop — blue `#3fb8ff` | MATCH | Exact standard hex, stop 2 of the standard (named "blue" in the file). |
| 15 | Wheel stop — green `#2fe89e` | MATCH | Exact standard hex, stop 3 of the standard. |
| 16 | Wheel stop — gold `#ffbf3d` | MATCH | Exact standard hex, stop 4 of the standard. (A competing claim naming gold `#ffd45a` exists in a comment on #2742 and in `DESIGN/HEXES-CANONICAL.md`; it contradicts Shawn's standard as given for GT-070 and was **not** followed — see "Competing claims" below.) |
| 17 | Wheel stop — orange `#ff9a5a` | MATCH | Exact standard hex, stop 5 of the standard. |
| 18 | Wheel stop — red `#ff5e6c` | MATCH | Exact standard hex, stop 6 of the standard. |
| 19 | Wheel stop — magenta `#e84fff` (hex value only) | MATCH | Exact standard hex, stop 7 of the standard. Its placement in the file's wheel is a separate element — see #20. |
| 20 | LAW 2 wheel as a sequence — 11 stops, magenta-first, "the count is dynamic; not a law that has to be five or seven or nine" | CONFLICT | The standard fixes a 7-stop sequence in the order purple → blue → green → gold → orange → red → magenta. The file's wheel has 11 stops, starts at magenta (the standard's last stop), and expressly makes the count dynamic. Wrong count, wrong order, wrong rule. |
| 21 | Wheel stop — indigo `#6675ff` | CONFLICT | Extra stop; no counterpart in the standard's 7-stop spectrum. |
| 22 | Wheel stop — emerald `#35e0a1` | CONFLICT | Wrong value / split stop: the standard's green seat is the single hex `#2fe89e`; the file splits it into emerald `#35e0a1` plus green `#2fe89e`. `#35e0a1` is excluded. |
| 23 | Wheel stop — lime `#b8ee57` | CONFLICT | Extra stop; no counterpart in the standard's spectrum. |
| 24 | Wheel stop — pink `#ed58cd` | CONFLICT | Extra stop; no counterpart in the standard's spectrum. |
| 25 | Zone walk, three zones — purple, blue, green | MATCH | Matches the standard's stops 1–3 in order. |
| 26 | Zone walk, five zones — magenta, purple, cyan, green, gold | CONFLICT | "Cyan" is not a standard stop (the standard's blue is `#3fb8ff`); the walk starts at magenta, contradicting the standard's order. |
| 27 | The Strip — magenta-first 5 stops (magenta → purple → blue → green → gold) | CONFLICT | Order conflict: magenta is the standard's final stop, not its first; a magenta-first instrument contradicts the standard sequence. |
| 28 | Contrast rule — yellow and gold never together; the wheel carries gold, never yellow; adjacent stops must read distinct | MATCH | Consistent with the standard (gold `#ffbf3d` present, no yellow stop). |
| 29 | Three jobs of color — chrome purple / text white 99% / theme = spectrum, never mixed, never flooded | MATCH | Purple glow (chrome), white base (text), spectrum (theme). |
| 30 | Themed zones — one accent per object/zone, never a whole page in one hue | MATCH | Consistent with the spectrum pillar; contradicts no pillar. |

### Laws 3–5

| # | Element (section) | Verdict | Evidence / exact conflict |
|---|---|---|---|
| 31 | LAW 3 — elevation order Field > Board > Panel > Control > Overlay; 5-layer board shadow | MATCH | Living-depth / jewel-3D construction; contradicts no pillar. |
| 32 | LAW 3 — board body: dark gradient `#1a171f → #09090d → #030304`, 1.5px border, 24px radius | MATCH | Black base with deep-purple-tinted dark gradient (`#1a171f`); white-lit edges at rest per the same section. |
| 33 | LAW 3 — header: full width, warm front door, no max-width caps | MATCH | No pillar contradicted. (It is not a mobile-first rule — see #52.) |
| 34 | LAW 4 — bullets are jewels: rotated-square diamonds, white → tone → black gradient, own-color glow, sheen facet | MATCH | Jewel 3D, stated in construction terms. |
| 35 | LAW 4 — faceted gems: true diamond geometry (clip-path polygon), white-hot crown to deep black base, drop-shadow glow | MATCH | Jewel 3D, exact construction. |
| 36 | LAW 4 — boards wear jewels: corner orbs lit from within, glowing in board tone | MATCH | Jewel 3D + spectrum glow. |
| 37 | LAW 4 — icons drawn, native vector, readable at 16px, glyph promises its behavior | MATCH | Design detail; contradicts no pillar. |
| 38 | LAW 5 — the one button: black center `#050505`, white text + icon, white border 1.5px+, purple edge + glow on hover (chrome) | MATCH | Black/white base + purple glow, exact bytes. |
| 39 | LAW 5 — touch targets: minimum 44px, principal CTA ≥52px, liftable feel | MATCH | Touch sizing detail; contradicts no pillar. (Sizing a target is not a mobile-first layout rule — see #52.) |

### LAW 6 — Type, and the standard's missing pillars

| # | Element (section) | Verdict | Evidence / exact conflict |
|---|---|---|---|
| 40 | LAW 6 — text white 99%, never gray body text | MATCH | White base pillar. |
| 41 | LAW 6 — type scale: hierarchy 24 / 18 / 14 (kicker 24, headline 18, detail 14); full scale "Body 15–17" | CONFLICT | The standard requires **18px body text**. The file assigns 18 to the headline and sets body at 15–17px. Wrong value on the body seat — body 15–17 is excluded; the cure is body = 18px. |
| 42 | LAW 6 — headers get a voice: serif Newsreader, Georgia fallback | MATCH | Type detail; contradicts no pillar of the standard. |
| 43 | LAW 6 — text never flat (gradient, layered shadow, breathing luminosity); order visuals → voice → text | MATCH | Jewel-3D / living-depth-consistent detail; contradicts no pillar. |
| 44 | STANDARD PILLAR — mobile-first | CONFLICT | **Missing rule.** The 326-line set contains no mobile-first rule at all (no "mobile" anywhere in the file). A pillar of the standard has no counterpart element; nothing in the set is ratified as mobile-first, and the set is not ratified as a complete statement of the standard until a mobile-first law is added by cure. |
| 45 | STANDARD PILLAR — domain nayanet.live | CONFLICT | **Missing rule.** The set never names the domain nayanet.live (no occurrence in the file). Missing counterpart, same consequence as #44. |

### The Eight Source Laws

| # | Element (section) | Verdict | Evidence / exact conflict |
|---|---|---|---|
| 46 | Source Law 1 — score the experience, never the code | NOT-A-DESIGN-ELEMENT | Process / scoring rule. |
| 47 | Source Law 2 — back it or bench it (9.0+ ships) | NOT-A-DESIGN-ELEMENT | Process / ship-bar rule. |
| 48 | Source Law 3 — color has jobs, never cross them; adjacent things never share a hue | MATCH | Restates #29; consistent with the spectrum pillar. |
| 49 | Source Law 4 — white light at rest, own color on touch, 1.5px+ rims | MATCH | Restates #4/#6. |
| 50 | Source Law 5 — black heart, white voice, visible skin (`#050507`) | MATCH | Black/white base, exact bytes. |
| 51 | Source Law 6 — size separates, color doesn't; 24 / 18 / 14 | CONFLICT | Restates the #41 scale: it carries the same body-text conflict (18 assigned away from body; full scale body 15–17 vs the standard's 18px body). |
| 52 | Source Law 7 — icons are drawn, not shrunk | MATCH | Restates #37. |
| 53 | Source Law 8 — verify before claiming | NOT-A-DESIGN-ELEMENT | Process / verification rule. |

### Function Law, Forbidden List, Ship Gate, closing sections

| # | Element (section) | Verdict | Evidence / exact conflict |
|---|---|---|---|
| 54 | THE FUNCTION LAW — pretty + useless = not done; click-everything protocol | NOT-A-DESIGN-ELEMENT | Enforcement process, not a visual design element. (Valuable, and unratified *as design* — it needs no design ratification.) |
| 55 | Forbidden #1 — anything flat | MATCH | Black-base / jewel-3D prohibition form. |
| 56 | Forbidden #2 — clumped color | MATCH | Restates #12. |
| 57 | Forbidden #3 — theme color on chrome; chrome color as flood | MATCH | Restates #29. |
| 58 | Forbidden #4 — gray body text | MATCH | Restates #40. |
| 59 | Forbidden #5 — shrinking Naya to one thing (face AND energy) | MATCH | Identity design rule; contradicts no pillar. |
| 60 | Forbidden #6 — quality toggles / modes | MATCH | Design rule; contradicts no pillar. |
| 61 | Forbidden #7 — light backgrounds, zero white/light surfaces | MATCH | Black base pillar, prohibition form. |
| 62 | Forbidden #8 — a second version of something that exists | NOT-A-DESIGN-ELEMENT | Composition process rule. |
| 63 | Forbidden #9 — beautiful but inert affordances | NOT-A-DESIGN-ELEMENT | Function enforcement; see #54. |
| 64 | Forbidden #10 — transmitting an adjective instead of an image | NOT-A-DESIGN-ELEMENT | Communication / spec process rule. |
| 65 | Forbidden #11 — compliance without vision | NOT-A-DESIGN-ELEMENT | Process / judgment rule. |
| 66 | Forbidden #12 — patching the specimen; sanding down the unreasonable parts | NOT-A-DESIGN-ELEMENT | Process rule. |
| 67 | Forbidden #13 — the dead button (black button, black text, hairline border, flat, no hover) | MATCH | Visual prohibition; restates #5/#6/#38/#40. |
| 68 | Forbidden #14 — recreating instead of composing | NOT-A-DESIGN-ELEMENT | Composition process rule. |
| 69 | Ship Gate #1 — white edge light visible on every card/button at rest | MATCH | Restates #6. |
| 70 | Ship Gate #2 — themed elements ignite own color; chrome ignites purple | MATCH | Restates #9/#29. |
| 71 | Ship Gate #3 — every button: black heart, white voice, truthful icon | MATCH | Restates #38/#50. |
| 72 | Ship Gate #4 — type hierarchy follows the scale | CONFLICT | Incorporates the #41 scale by reference; the referenced scale conflicts with 18px body text, so this gate cannot be ratified as written. Cure follows the #41 cure. |
| 73 | Ship Gate #5 — copy plain enough to understand on first read | NOT-A-DESIGN-ELEMENT | Content / process check. |
| 74 | Ship Gate #6 — every interactive element performs its real behavior, verified by clicking | NOT-A-DESIGN-ELEMENT | Function enforcement; see #54. |
| 75 | Ship Gate #7 — scored the rendered working page honestly, 9+ or bench | NOT-A-DESIGN-ELEMENT | Scoring process. |
| 76 | THE FINAL LAW — Shawn's eye compiles, outranks every score/law | NOT-A-DESIGN-ELEMENT | Governance statement. This record is itself an exercise of the authority it describes, via Shawn's 2026-10-22 word. |
| 77 | THE MACHINE TWIN — pointers to `DESIGN/TOKENS.css` and `DESIGN/SPECIMENS/specimens.json` | NOT-A-DESIGN-ELEMENT | Pointer text; the pointed-to files were not part of #2742's diff (its only file was `DESIGN/DESIGN-LAWS-V2.md`) and are not verified or ratified here. |
| 78 | IMPLEMENTATION RECONCILIATIONS #1–#4 (specimen coverage, cross-file parity, voice font, strip-vs-walk) | NOT-A-DESIGN-ELEMENT | Implementation notes. Note: #2's instruction to "propagate the ratified v2 hex values" must **not** be executed for the CONFLICT hexes (#21–#24) or the wheel sequence (#20) — those values are expressly not ratified. |
| 79 | SOURCES list | NOT-A-DESIGN-ELEMENT | Provenance text. |
| 80 | 3-PASS SCORECARD record, incl. "Pass 3 — the doctrine is now ratified by Shawn on 2026-10-21" | NOT-A-DESIGN-ELEMENT | Process record. Its ratification sentence is superseded by this record: ratification is dated 2026-10-22, is MATCH-only, and comes from Shawn's eight-gate word, not from 2026-10-21. |

## The verdict, counted

- **MATCH: 47 elements — RATIFIED** — rows 4–19, 25, 28–40, 42, 43, 48–50, 52, 55–61, 67, 69–71.
- **CONFLICT: 12 elements — EXCLUDED, named** — rows 20, 21, 22, 23, 24, 26, 27, 41, 44, 45, 51, 72.
- **NOT-A-DESIGN-ELEMENT: 21 elements** — rows 1–3, 46, 47, 53, 54, 62–66, 68, 73–80: process, governance, provenance, and record text; neither ratified nor rejected as design by this record. (47 + 12 + 21 = 80 rows, counted from the table itself; the machine form carries the same three lists.)

## The ratified set (what is now law, exactly)

Everything marked MATCH above — in substance: the black/white base with white-lit rest state and own-color ignition; purple chrome/input glow; the seven standard hex values **as values** (`#a06bff`, `#3fb8ff`, `#2fe89e`, `#ffbf3d`, `#ff9a5a`, `#ff5e6c`, `#e84fff`); spectral-order / no-clumping; color's three jobs; elevation and the 5-layer board construction; jewel-3D bullets, gems, and corner orbs; the one-button DNA; white 99% text; and the visual prohibitions and ship-gate checks that restate those elements.

## The excluded set (not ratified — cures named)

1. **The 11-stop wheel and its sequence** (#20) — cure: replace with the standard's 7-stop sequence in standard order.
2. **Indigo `#6675ff`** (#21), **lime `#b8ee57`** (#23), **pink `#ed58cd`** (#24) — cure: remove as spectrum stops.
3. **Emerald `#35e0a1`** (#22) — cure: remove; the green seat is `#2fe89e` alone.
4. **Five-zone walk** (#26) and **magenta-first Strip** (#27) — cure: walks/strips follow the standard sequence and start where it starts.
5. **Type scale body 15–17 / 18-as-headline** (#41, carried into #51 and #72) — cure: body text = 18px; re-derive the rest of the scale around it.
6. **Mobile-first — missing** (#44) — cure: add a mobile-first law to the set.
7. **Domain nayanet.live — missing** (#45) — cure: name the domain in the set.

## Competing claims — settled, not followed

A comment on #2742 (2026-10-21, comment `6306410301`) and `DESIGN/HEXES-CANONICAL.md` at main assert a different "locked" spectrum: nine stops including indigo `#6675ff` and kenya teal `#40d3bb`, with gold `#ffd45a`. That set contradicts Shawn's design standard as given for GT-070 on two counts (gold hex, stop set/order) and is **not** the standard this record ratifies against. Under Shawn's 2026-10-22 word, the measuring stick is the standard stated above. Any lane holding the nine-stop set should reconcile it against this record or bring a new word from Shawn — it may not be applied as ratified on the strength of that comment.

## Authority and limits

- Ratifier: **Shawn Vibert**, Human Director — eight-gate decision, 2026-10-22 ~00:29Z (GT-070 as presented: verify against his design standard, ratify matching elements on the record, name and exclude conflicting elements).
- This record ratifies design elements only. It does not certify any interface as compliant, does not change the set's 9.5/10 draft score, and does not edit `DESIGN/DESIGN-LAWS-V2.md` — a cure PR does that, through the normal Tier A door.
- Tier: **Tier A** (governance). Merge requires a different seat's scorecard at ≥9.5 at exact head — requested on the record PR; not merged by its author.
