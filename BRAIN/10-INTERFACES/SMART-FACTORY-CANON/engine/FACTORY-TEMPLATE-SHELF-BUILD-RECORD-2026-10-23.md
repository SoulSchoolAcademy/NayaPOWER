# FACTORY STEP 5 — BUILD RECORD: the template shelf, generated from the one registry

Seat: Naya Nitro (Nu line, BUILD)
Date: 2026-10-23
Branch: `nitro/factory-step5-template-shelf-2026-10-23`, based on origin/main `352ad3df46`
(canon files blob-identical to the step-4 merge `bb42d8cfc7e7`; boot gate PASS).
Plan: `~/workspace/factory-models/FACTORY-CONTRACT-HOME-AUDIT-2026-10-22.md` §3 step 5 —
"Reconcile the template shelf. One registry: page cards generated from
`templates-registry.json`; resolve Today/Smart List vs personal-hub/business-hub
(build the missing bases or drop the cards — no card without a base); annotate
each template with its named parts as they are harvested into it over time.
*Deliverable: one 12 (or N) that is the same 12 everywhere.*"

## The census (before any build)

**(a) The registry** (`engine/templates-registry.json`) — `templates` holds **12 keys**,
each with file/md5/bytes/source/base_identity: booking, business, business-hub,
community, dashboard, event, menu, personal, personal-hub, portfolio, product,
signup. Its `missing` table holds 2 more keys in the registry's own words —
today, smart-list: "No contracts.json entry, no template worker, no base file
exists." Its `alias_note` states the lookup rule: lowercase, spaces→hyphens.

**(b) The page** (`engine/factory-page-shell.html`) — the template grid exists
**twice** (`#step3-templates` and the second `<section id="step4">`), byte-identical
8,331-byte grids of **12 cards**: Personal, Today, Smart List, Business, Booking,
Product, Event, Community, Portfolio, Menu, Signup, Dashboard. (The page's third
`tgrid` is the ADD-ONS grid — `addoncard`, not the template shelf.) All 12 cards
parse to one grammar: `tcard2` + `data-t` + `--tc`, mini-gem (shape + svg),
`tbrand`, `tnut`, `tdetail` (lead + the standard ships-with suffix), VIEW button.

**(c) The bases** — `engine/templates/` in the repo and
`~/workspace/factory-pipeline/templates/` hold **exactly the registry's 12**
(same filenames both places). No base exists anywhere for today/smart-list.
The hub bases are real and buildable: `factory-pipeline/contracts.json` carries
personal-hub + business-hub with live workers (`naya-template-personal-hub`,
`naya-template-business-hub`) — they simply had no card on the shelf.

**Parts census per base** (uniform across all 12 — every base is a personal-v5
body): named in the base's own CSS comments, `NAYA-BTN-021, 023, 024, 025, 027`
(rosters `NAYA-BTN-023/024/025/021` + `NAYA-BTN-027 — chrome button`); embedded
verbatim (store `html` byte-present), `NAYA-BTN-017` (×4), `NAYA-BTN-028` (×4).
Union = **7 canonical pieces** on every base today.

## The reconciliation — one 12, the same 12 everywhere

Generated shelf (page order preserved for surviving cards; hub variants beside
their parents): **Personal · Personal Hub · Business · Business Hub · Booking ·
Product · Event · Community · Portfolio · Menu · Signup · Dashboard** — 12 cards,
one per registry template, each tracing to a registry entry AND a real base.

**OUT — Today, Smart List.** Cards existed; bases do not (registry `missing`
table is the evidence). Per the plan they come out rather than acquire invented
bases; the generator prints both exclusions on every run, so the removal is
never silent. They return the day a real base lands and the registry moves them
out of `missing` — the shelf follows the registry automatically.

**IN — Personal Hub, Business Hub.** Registry templates with real bases and
workers that the page showed no card for. Their presentation lives in the map's
new `template_overrides` section (step-4 override discipline — each entry
carries its reason): brand/nut/detail composed ONLY from the registry's own
`base_identity` (personal-hub: name "My Smart Hub", tagline "My world,
connected", about "Your personal intelligent hub. Everything you need, one
place."; business-hub: "Business Hub" / "Run your business" / "The intelligent
hub for your business. Manage everything.") in the page's card grammar; glyph =
the parent card's harvested svg (same family — the bases are personal-v5
bodies); colors = the two colors the removed cards carried (#40d3bb teal,
#ffbf3d gold), so **no new color enters the shelf** and no neighbor shares one.

**Annotation.** Every generated card carries `data-base="<registry file>"` and
`data-parts="<the base's censused canonical pieces>"`, computed from the base's
bytes at generation time (ids named incl. roster expansion ∪ verbatim-embedded
store html), in the same data-attribute dialect step 4 set for ai_label. A part
that is not canonical in the store fails the build loud — a fabricated list is
impossible by construction. Today the honest annotation is the same 7 pieces on
all 12 cards; it differentiates as parts are harvested into the bases over time,
which is exactly the plan's "as they are harvested into it over time".

## What changed (4 files)

- `engine/generate-factory-page.py` — extended, same twin discipline: loads the
  registry (every `templates` entry must have its base file — fail loud),
  harvests template cards from the shell (both grids must be byte-identical and
  tile exactly into parsed cards), resolves the reconciled shelf (registry
  `missing` ⇒ excluded; registry template with no harvested card ⇒ override
  with reason or fail loud; offered set must equal the registry set), generates
  both grids, and verifies the page. All generated regions are located on the
  original shell and applied last-to-first, so the parts shelf's bytes cannot
  shift. `--harvest` now also writes `template_order`/`template_cards` and
  preserves `template_overrides`. `--check` reports both equations.
- `engine/factory-page-presentation.json` — + `template_order`,
  `template_cards` (harvested), `template_overrides` (the 2 hub cards, with
  reasons). All step-4 harvested sections value-identical after re-harvest.
- `factory-page.generated.html` — regenerated preview: 614,204 bytes, md5
  `fdbc7841090c24d9eddff7c8914185a1`.
- This build record.

**Deliberately NOT touched:** `templates-registry.json` itself — **PR #2978**
(canon v1.3, S1 "Dark mode" → "Deep black") is open against that file and owns
its S1 edit; this branch does not edit any registry value, and the two changes
cannot conflict (disjoint files). The generator only reads the registry.

## Acceptance — proven three ways

1. **Generator verify** (every run, and `--check` exit 0): `154 canonical ==
   154 store == 154 cards; 12 registry == 12 bases == 12 template cards x2
   grids`; per-card base + parts re-verified on the generated bytes.
2. **Independent census** (a from-scratch script sharing no code with the
   generator): registry 12 == repo bases 12 == pipeline bases 12 (sets equal);
   24 annotated cards, each name exactly ×2; card keys == registry keys;
   Today/Smart List absent; every `data-base` file exists; every `data-parts`
   recomputes exactly; parts shelf 154 == canonical 154.
3. **Rendered DOM** (chrome-headless-shell, file://, external requests failed
   fast): 17/17 checks PASS at 1440px and 390px — 2 grids, 24 cards, order ==
   reconciled shelf in both grids, grids identical in the live DOM, hub card
   laid out (1160×98 desktop / 318×134 phone) with its annotation readable,
   154 pcards, **zero page exceptions / console errors**.

**Byte discipline:** the generated page minus its two template grids is
**byte-identical to the step-4 generated page** — parts shelf, carried CSS,
scripts, everything else unchanged. ADD-ONS grid intact.

**Sabotage battery** (scratch copy of the canon; exit codes per the generator's
contract): baseline `--check` exit 0 · one-byte tamper of the output → exit 1 ·
a base deleted → exit 2 naming the template ("no card without a base") · a
registry entry with no base → exit 2 · the Personal Hub override dropped from
the map → exit 2 (offered ≠ registry) · a base naming a non-canonical piece
(NAYA-BTN-099) → exit 2 · restored → exit 0.

**Live page untouched:** `https://nayanet.live/smartfactory` md5
`fb7d742d6dbc570295ce0a43926f17c3` after all work — nothing deployed (step 8).

## Named remaining divergences (not hidden, not this step's regions)

- The shell's **script** name lists — `WORLD_TABS` and the SmartTabs navigator's
  `worldNames` — still carry the old 12 names (Today/Smart List in, hubs out).
  They are app-chrome data inside shell `<script>` bytes, outside the
  generator's regions by the byte discipline; the navigator guards a missing
  card at runtime (`if (c && ...)`) so nothing breaks. Reconciling them is a
  shell change for a later step or Shawn's call at step 8.
- `engine/contracts.json` knows only the 10 shared keys; the pipeline's
  `contracts.json` has all 12. The build path that executes (pipeline) is
  complete; the canon copy's gap predates this step and is the contracts
  owner's to close.
- The shell's `window.__MISSING_TEMPLATES` guard (today/smart-list) remains —
  still true, now unreachable from the shelf, and still guarding any saved
  contract that names them.

## Self-score: 9.4/10

Why not 10: (1) −0.3 the two hub cards' copy is my composition from registry
data in the page's grammar — faithful and sourced, but unratified by Shawn's
eye (his look is step 8; step 4 took the same class of deduction for new
descriptors). (2) −0.3 the in-page script name lists above still diverge from
the reconciled shelf; I chose byte discipline over reaching outside the
generator's regions, and the choice is named rather than buried. The parts
annotation being uniform across cards is NOT a deduction: it is the true state
of the bases today, and stating it plainly is the deliverable.

## Evidence

- Census + reconciliation computed from fresh reads of the registry, shell,
  both base directories, pipeline contracts, and the store (this record §1–2).
- Generator/check/sabotage/census/render outputs as quoted above; render probe
  kept with the seat's scratch (`step5-render-probe.cjs`, 17/17 PASS).
- Live fetch of nayanet.live/smartfactory, md5 as quoted.

api_calls: 4 (2 gh-app-token fetches for clone/fetch + PR create + PR read-back).
Nothing merged, nothing deployed.
