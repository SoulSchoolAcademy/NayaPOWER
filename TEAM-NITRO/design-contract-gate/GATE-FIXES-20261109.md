**Context:** the v70 gap-closing verifier ran the design-contract gate and it FAILs — but three failures are measurement bugs in the gate itself, not page defects. The gate-as-blocking rule is in force (captain's decision 04:47Z), so the gate must be trustworthy: a FAIL must mean the page failed, never that the check misfired.

## Filed

- `TEAM-NITRO/design-contract-gate/check-gate.py` — blob
  **d4196c78bfa247c625d08c744a78838c22808afa**, 70,681B, commit
  `7b5d65a13c2333dd0551fe5d333d4ce6f992b991` (was blob `b114fd5d`, 56,574B).
  Read-back verified byte-identical (sha256
  `70c0488f5c7c0e038efb20be659bc1f917960b6aae4bc63234e74b018ded6265`), and the
  downloaded copy reproduces the fixed verdicts.
- Brief checker on the brief: PASS 7/7, exit 0, re-run this pass.

## The three bugs
1. **(d) Text-in-image false positives — data-URI faces.** 23 hits, all data-URI base64 face images (the 8 Naya faces + orbs). A face JPEG contains no text; a data-URI payload is opaque binary — the "doc"/"list" substrings are random base64 noise.
2. **(i) Ten shape mismatch — `.board-sub` / `.board-nut` classes.** The Ten uses `.ult-part` (why/sol/nut) + `.ult-who`, not `.board-sub` / `.board-nut`. Same family, different shape — the gate must recognize it.
3. **(c) Calculator gauge measured against the wrong standard.** The pricing calculator gauge is a different component (a calculator/speedometer, not the Dashboard needle-law gauge). Measuring it against the Dashboard gauge's standard is a category error.

## The fixes

### (d) Data-URI payloads are opaque binary, not text

`check_d` scanned every `<img>`'s `src + alt` for text signals. Fix: when
`src` starts with `data:image/`, the payload bytes are NEVER scanned; the
human-written `alt` text IS still scanned, and file/URL images are scanned
on `src + alt` as before. New count `data_uri_images_excluded` (25 on the
pricing page) and a note naming the exclusion.

### (i) The Ten is the same family in a different shape

A board carrying `.ult-card` / `.ult-part` is a TEN board and is checked
against its own shape — title + three parts (`.ult-part-why`,
`.ult-part-sol`, `.ult-part-nut`, each with at least one real bullet; a
label alone is not a nutshell) + who line (`.ult-who`). Side alternation
and face distinctness still apply to Ten boards unchanged. New count
`ten_boards` (10 on the pricing page).

### (c) The calculator gauge is not the needle-law gauge

A mount is a CALCULATOR gauge when any ancestor names the calculator
(`id="calculator"`, class `calc-gauge` / `calc-body` / `calc-...` — the
mount lives inside `#calculator`). A calculator gauge is measured against
its own standard:

1. **Number on top** — a numeric amount element (`#calc-amount` /
   `.calc-readout` with a digit) exists and shares a gauge-block ancestor
   (class containing "gauge") with the mount. Honest limit: DOM order
   cannot prove "on top" (the mount precedes the amount in source while
   the number renders above the dial) — the static check is the pairing;
   visual above/below is the live verifier's job (screenshots).
2. **Needle/dial alive** — some script builds `tn-tacho-needle`, AND some
   script mentions both the mount id and `calc-amount` (the calculator
   drives the mount when the amount changes). A gauge with no JS wiring
   is dead, not alive.
3. **Gold rim intact** — the calculator's gold token (`--gold`, a gold hex)
   is defined and is used by a calculator/tacho-scope rule (the gauge's
   number/readout wears it).

A mount anywhere else is still the Dashboard needle-law gauge, evaluated
exactly as before. `check_f` F3 is skipped only when EVERY mount is a
calculator gauge — a dead calculator gauge still FAILs (c).

## Before / after (the gate on the pricing page)

| Check | BEFORE (old gate, true v70 export — `verify-v70/gate-v70.txt`) | AFTER (fixed gate) |
|---|---|---|
| (c) | FAIL — needle law broken (CSS transition) + only 1 gear tooth | **PASS** — calculator standard: number "$4,500" paired, needle built by JS + driven, gold `--gold=#e8b64c` defined + used (counts: `calc_gauges=1`, `calc_number_paired=1`, `calc_needle_built_by_js=1`, `calc_driven_by_amount=1`, `calc_gold_defined=1`, `calc_gold_used=1`) |
| (d) | FAIL — 23 hits, all data-URI base64 false positives | **PASS** — 0 hits; 25 data-URI payloads excluded, alt still scanned |
| (f) | FAIL — F1 4 look-alike buttons + F3 fake gauge (transition + teeth) | FAIL — F1 4 look-alike buttons only; F3 skipped with note (calculator gauge) |
| (i) | FAIL — 20 missing parts (the Ten bug) + boards 17/18 both left + repeated face | FAIL — **0 missing parts** (`ten_boards=10`); only the carried debts: boards 11/12 both left + repeated face |
| (a) | FAIL — `.stone-white.lb-jewel` light gradient | FAIL — unchanged (real debt) |
| (b) | FAIL — depth 85.5% (need 90%) | FAIL — 85.6% (unchanged; 0.1% drift is the v71 board move, not the gate) |
| (e) | FAIL — contained 66% (need 80%) | FAIL — 66.1% (unchanged) |
| (h) | PASS | PASS |

OVERALL is still FAIL — as it should be: the real page debts stay failing.
The gate now fails the page for real reasons, not measurement bugs.

### A note on the "after" file (read this before comparing)

The brief's test matrix says "run the gate AFTER the fix on the SAME file"
(the v70 export). That file no longer exists on disk: the v71 build landed
on the artifact at 05:12Z — after the v70 verification (05:05Z) and during
this seat — and overwrote the export at
`~/workspace/your_files/pricing-chart-viewpoint/pricing-chart-viewpoint.html`
(v70: 4,950,955B, sha256 `cc1db9ba…`; now v71: 4,954,325B, sha256
`fdbd70a3…`). A filesystem-wide search for a 4,950,955-byte file found no
v70 copy anywhere, and restoring artifact version v70 would undo v71 work,
so it was not done. The AFTER run is therefore the fixed gate on the **v71
export**, saved as `~/workspace/team-nitro/pricing/verify-v70/gate-v71-fixed.txt`
(header inside explains this). The comparison still holds: v71 moved only
the 7 hired boards into a Learn-more viewpoint — it touched nothing the
three fixes measure. Evidence: (c) counts identical between the v70-before
and v71-after runs (mount 1, needle DOM 0, CSS 1, teeth 1, transition 1,
tiled 43, orb 0); (d) same 25 images; (i) the Ten is intact (10 boards, 0
missing parts). The only (i) difference is the side-order re-indexing
(boards 11/12 both-left in v71 vs 17/18 in v70) — the same carried
face-7/alternation debt, re-numbered by the board move.

## Test matrix

Synthetic pages in `/tmp/gate-fix-tests/` (ephemeral; rebuild from the
descriptions below if needed):

| Test | Expected | Got |
|---|---|---|
| `c-calc-good.html` — calculator gauge complete (mount in `#calculator`, amount `$4,500`, scripts build needle + drive mount, `--gold` defined + used) | (c) PASS | (c) PASS, all four sub-checks 1 |
| `c-calc-dead.html` — calculator gauge, NO scripts | (c) FAIL (dead needle + not driven; gold passes) | (c) FAIL — `C-CALC DEAD NEEDLE` + `C-CALC NOT DRIVEN`; gold passes (isolated aliveness failure) |
| `c-calc-no-gold.html` — calculator gauge wired, `--gold` removed, no gold hex | (c) FAIL (gold rim) | (c) FAIL — `C-CALC GOLD RIM MISSING`; number + alive pass |
| `c-dead-gauge.html` — mount outside calculator, needle CSS transition, 1 gear tooth | (c) FAIL needle law; (f) FAIL F3 | (c) FAIL — `C NEEDLE LAW BROKEN` + `C GEAR TEETH MISSING`; (f) FAIL — `F3 FAKE GAUGE` ×2 |
| `c-dash-good.html` — Dashboard-style mount, needle in DOM, `transition:none`, 3 teeth | (c) PASS (needle-law regression) | (c) PASS; (f) PASS |
| `d-real-doc.html` — data-URI face (alt "Naya") + file image `top10-chart.png` (alt "Top 10 reasons chart") | (d) FAIL on the file image only | (d) FAIL — 1 hit, the file image (`top10, chart, reason`); data-URI face excluded |
| `d-datauri-alt.html` — data-URI image, alt "Top 10 chart screenshot" | (d) FAIL via alt scan | (d) FAIL — `chart, screenshot` from the alt |
| `i-ten-no-nut.html` — Ten board with why + solution + who, NO `.ult-part-nut` | (i) FAIL naming the nutshell | (i) FAIL — `TEN BOARD 1 MISSING .ult-part-nut (nutshell)` (the only (i) fail) |
| `i-ten-good.html` — complete Ten board + proper hired board | (i) PASS | (i) PASS |

Regression (LOCK-IN-20261109.md evidence, reproduced with the fixed gate):

| Test | Expected | Got |
|---|---|---|
| `i-hired-bad.html` — hired board missing `.board-nut`, same side twice, same face | (i) FAIL all three | (i) FAIL — missing nut + not alternating + repeated face |
| `i-hired-good.html` — two proper hired boards, alternating, distinct faces | (i) PASS | (i) PASS |
| `g-bad-note.md` — 3 bold-inline labels, 0 `##` | (g) FAIL | (g) FAIL — `NO ## SECTIONS` |
| SN-2444 (local copy) — quotes `**Hook:**`, 9 `##` | (g) PASS | (g) PASS |
| SN-2448 (local copy) — 9 `##`, 0 labels | (g) PASS | (g) PASS |
| `h-bad-page.html` — "never cash back" in copy | (h) FAIL | (h) FAIL — `BLUNT DICTATION PHRASE` |
| Verdict wiring, all-PASS attestation on a machine-failing page | OVERALL FAIL | OVERALL FAIL |
| Verdict wiring, H3-FAIL attestation | OVERALL FAIL | OVERALL FAIL |

## Honest limitations

- **Visual "number on top" is not statically proven.** The (c) calculator
  check proves pairing + wiring + gold, not rendered above/below. The live
  verifier's screenshots remain the proof of the visual order.
- **The all-machine-pass → OVERALL PASS direction was not re-run.** No
  fully-passing page exists on disk (the LOCK-IN test page was not saved),
  so the verdict wiring was re-proven only in the FAIL directions. The
  verdict/human-checks code is untouched by this change (the diff touches
  the docstring, the calculator helpers, `check_c`, `check_d`, `check_i`,
  `check_f` F3, and the `check_c` call site — nothing else).
- **`custom_props` requires a trailing semicolon** (pre-existing gate
  behaviour, also used by check_a). A `--gold:#e8b64c` declaration without
  `;` is not collected — caught during testing (my first synthetic lacked
  the semicolon); the real page writes it with `;`, so this is a test-file
  lesson, not a gate bug. Not changed — out of scope.
- **The classifier is "any ancestor names the calculator".** Broader than
  just `id="calculator"` (also `calc-gauge` / `calc-body` / `calc-...`).
  A non-calculator gauge sitting inside an element with "calc" in its
  class would be misclassified — no such element exists on the Dashboard
  or the pricing page. If one ever appears, the discriminator should
  tighten to the `#calculator` section.

## What still fails (real page debts — NOT this build)
- (a) `.stone-white.lb-jewel` light gradient
- (b) depth 85.5–85.6% (need 90%)
- (e) contained 66% (need 80%)
- (f) 4 look-alike buttons (F1) — `.letter-all`, `.academy-btn`, `.cont-free` ×2
- (i) face-7 repeated twice + one adjacent same-side pair (boards 17/18 both
  left in v70; re-indexed to 11/12 in v71 by the board move — same debt)

## NOT DONE
- The real page debts above stay failing by design. Gate calibration vs page
  divergence is the captain's item, not this seat's.
- The "$4,500" clip decision and the v71 verification / re-freeze are
  separate seats; this seat touched neither the page nor the artifact.
- No Smart Note was filed for this fix (not ordered by the brief).
