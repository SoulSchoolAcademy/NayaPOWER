# FACTORY STEP 6 — BUILD RECORD (2026-10-23)

**Step:** Audit §3 step 6 — "Wire the gate to the same source, visibly."
**Seat:** Naya Nitro (Team Nitro, Nu line — steps 4–5 generator line).
**Branch:** `nitro/factory-step6-gate-door-2026-10-23`. **Status: AWAITING
REVIEW — not merged by the author.**

## What was built

**A. The checker learned the design language (same source).**
`engine/check_standard_features.py` gains a design-language annex. One
function — `design_params(twin)` — extracts every rule value from the
machine twin (`NAYA-DESIGN-CONTRACT.machine.json`): the spectrum walk
order + wrap behavior, the type floor (`typography.body_px.floor` = 16),
the section/member color carriers, the SmartNote board-mapping hexes and
their board contexts, the rest exceptions, the chip marker. The checker
loads the twin beside itself, or from `origin/main` via `git show` when
it runs vendored (the `process-build-queue.py` path — verified live
below), or from the pipeline's vendored snapshot. A missing or corrupt
twin yields annex status `UNAVAILABLE` with the reason — never a faked
pass. `evaluate()` carries the annex as `design_language`; **the S1–S13
score is untouched** (regression proof below), so the annex rides every
build receipt as signal without silently moving the strict gate.

Five checks, each naming its offenders:

| Check | §10 item | Rule (all values from the twin) |
|---|---|---|
| DL-WALK | 8 | Section carriers (`--sec/--ac/--igc/--rc`) step +1 through the walk, wrap per twin, never repeat adjacently; member carriers (`--sc/--tc/--tone`) step +1 run-compressed; non-walk hues in a carrier are offenders (SmartNote board hexes exempt inside board contexts only; contents chips excluded — DL-CHIPS is their law) |
| DL-REST | 10 + 11 | Interactive rules at rest wear no spectrum color in rim properties (border/box-shadow/outline family); rest rims must be white light (neutral, min channel ≥ 192); ignition belongs to `:hover`/`:focus` |
| DL-TYPE | 17 | No font-size / font shorthand below the twin's floor, in CSS or inline styles; px/rem/pt judged, em/% counted as not-determinable and reported |
| DL-DEAD | 22 (CSS slice — Shawn's Reports-eye steer) | Interactive elements (links with href, buttons, inputs, selects, textareas, role=button, onclick) with no `:hover`/`:focus` rule setting an ignition property and no inline handler are dead, named per class signature |
| DL-CHIPS | 8 (steer) | Contents chips (chip-classed siblings) must each carry a distinct walk color; same-color clusters, missing and non-walk colors are named |

**B. The door (same checks, on the page).** The generator emits one
contiguous door region into `factory-page.generated.html`: a "Check
against the contract" section (the page's own railhead/pmodel header
grammar, near-black ground, white rims, purple ignition), a URL field +
fetch button, a paste field + check button, and a results area. The
generator embeds `design_params(twin)` — the checker's own extraction —
as a JSON block in the page; the door's in-page logic consumes exactly
that data. No rule value is hand-duplicated anywhere: corrupt the twin
and generation itself fails loud (below). The door states its own
limits on the page: checks read page bytes (inline + `<style>` CSS;
external stylesheets are outside the bytes), fetch can be blocked by
CORS (paste runs the identical checks), and the not-mechanically-
checkable §10 items are listed by name, rendered from the same embedded
data — named, never silently skipped.

## Not mechanically checkable — named (20)

§10.1 Field · §10.2 Full width · §10.3 Shapes (16:9 ratio needs layout)
· §10.4 No voids · §10.5 Twin pluses · §10.6 Smart Tabs · §10.7 Drift
(comparison across pages) · §10.9 Color jobs unmixed · §10.12 Jewel
tones (saturation judgment) · §10.13 Elevation (layered-shadow reading)
· §10.14 Wells vs buttons · §10.15 One button DNA · §10.16 Icons are
jewels · §10.18 Orbs carry people + numbers · §10.19 Living data
(behavior over time) · §10.20 Timestamps alive · §10.21 Motion has an
off switch · §10.22 functional half (a dead *handler* needs execution;
the missing-ignition half IS DL-DEAD) · §10.23 Nothing recreated
(provenance) · §10.24 Edit-only respected (provenance). Each carries its
reason in the checker's `NOT_MECHANICALLY_CHECKABLE` table, in every
report, and on the door itself.

## Evidence

- **Fixtures** (`engine/design-language-fixtures/`, 6 pages): clean →
  all PASS; each violation fixture fails exactly its own check, under
  the Python checker. The door (chrome-headless-shell, CDP) returns the
  **identical failed-check sets for all six fixtures in BOTH paste and
  fetch modes — parity 6/6 × 2**. Zero page exceptions, zero console
  errors; the door's embedded walk reads `#a06bff #3fb8ff #2fe89e
  #ffbf3d #ff9a5a #ff5e6c #e84fff` from the params block.
- **Byte discipline:** generated page minus the door region (26,456
  bytes) is **byte-identical** to the step-5 generated page on main
  (614,204 bytes). Generator `--check` exits 0: `154==154==154`,
  `12==12==12 ×2 grids`, door present and byte-stable.
- **Sabotage battery:** one appended byte → `--check` exit 1. Twin walk
  hex corrupted → checker exit 2 and generator exit 2, both naming
  `spectrum_walk.order`. Twin floor 16→99 → the clean fixture fails
  DL-TYPE (the rule value provably flows from the twin). Broken walk /
  dead board / same-color chips → flagged by checker AND door.
- **No S-score regression:** A/B against the step-5 checker on this
  branch's registry gives the identical failed set
  ([S1,S2,S3,S7,S8,S9,S10,S11,S12], 4/13 — the delta vs main's 5/13 is
  the #2978 registry state, not this change); the step-6 checker on the
  step-5 registry reproduces 5/13 exactly.
- **Processor wiring:** the checker exec'd from a bare temp path (the
  `process-build-queue.py` pattern) loads the twin from the repo clone's
  `origin/main` and passes the clean fixture — on merge, the processor
  picks this checker up from `origin/main` unchanged, so gate and door
  read the same twin by construction.
- **Live page untouched:** `nayanet.live/smartfactory` md5
  `fb7d742d6dbc570295ce0a43926f17c3` before and after. Nothing deployed;
  step 8 owns deployment.

## Honest standings (surfaced, not hidden)

- The annex on a raw template base FAILs (DL-WALK/REST/TYPE/DEAD) —
  bases are pre-customization artifacts; named here so nobody reads the
  annex as broken when a receipt shows it.
- The annex on the generated page itself FAILs: DL-WALK 564 (piece-card
  `--tc` values are per-piece identity hues — a gallery is not a
  section sequence, and bytes alone cannot tell them apart), DL-TYPE
  374 (the harvested shell's label scale runs 12–15px against the
  twin's 16px *body* floor — the strict reading the step-6 brief
  specified), DL-REST 19 (dominated by selected-state rules —
  `.naya-tab.active`, `.szpill.on`, `.btn-select.picked` wear their
  color at rest *because they are selected*; bytes cannot separate
  "selected state" from "rest"), DL-DEAD 8 signatures (`.on` variants,
  bare inputs, `a.rail-link`, `button.bh-btn` — adjudication material),
  DL-CHIPS PASS. These are contract-reading questions for Shawn/Delta,
  surfaced by name — **no harvested byte was edited to chase the
  annex** (byte discipline + the no-redesign law outrank a green
  annex). The annex is advisory until that adjudication lands.

## Self-score: 9.2 / 10

Why not 10: (1) the gray zones above are real — the twin does not
encode selected-state or gallery semantics, so the checks implement the
letter of §10 and name the gap instead of resolving it; a future twin
field could close it. (2) The door's fetch mode is CORS-bound by the
platform (named on the page; paste mode is full-parity). (3) Parity is
proven on six purpose-built fixtures plus the generated page's own
render — not yet on a corpus of arbitrary third-party pages. (4) The
factory page does not yet pass its own door; that gap is surfaced and
owned here, and closing it is an adjudication + step-8 matter, not
something this step may fake.
