# DESIGN-CONTRACT GATE — TEST REPORT: alpha + live-teeth + harvest-source fixes
Seat: the gate-fix seat. Date: 2026-11-10 ~04:05–04:20Z.
Branch: `design-contract-gate/alpha-teeth-harvest-20261110`.
Fixes exactly three measurement artifacts; no threshold or rule changed, no page touched.

## What was wrong (verifier evidence, reproduced before fixing)

Personal fix-7 (blob `8e36e9b841b17292f6f96e930682418e1b22431d`,
`PERSONAL/personal-candidate-2.html`, branch `personal/fix6-20261110`,
sha256 `6b15b6d4b98b52dcc01b8c76b016deae9bf217c48f564557a3ff69de088b74ee`)
failed the gate on (a), (c), (f) — all three were gate artifacts, not page defects.
Baseline run of the unfixed gate on that blob: OVERALL FAIL.
(a) 7 hits, (c) teeth 1, (f) tg-mode x2 + F3 teeth 1. (b)(d)(e)(h)(i) already passed.

## Fix 1 — (a) alpha: parse_color drops the alpha byte of 8-digit hex

- Before: `parse_color('#ffffff14')` returned `(255, 255, 255, 1.0)`,
  `effective_lightness = 1.00`, while `rgba(255,255,255,0.08)` correctly gave `0.102`.
- After: 8-digit hex parses bytes 6-8 as alpha (`0x14/255 = 0.078`).
  `#ffffff14` -> lightness `0.100`; `#ffffff05` -> `0.043`; `#ffffff08` -> `0.054`;
  `#ffffff06` -> `0.047`; `#ffffff10` -> `0.085`. All 7 fix-7 hits
  (`#ffffff05`–`#ffffff14`, 2.0–7.8% alpha) blend to lightness 0.043–0.100
  against the 0.80 threshold — none fires. Solid `#fff` still reads 1.00.
- Diff: in `parse_color`, after the 3/6/8-digit hex match,
  `alpha = int(h[6:8], 16) / 255.0 if len(h) == 8 else 1.0`.

## Fix 2 — (c)/(f) teeth: live-evidence input overrides the static count

- Before: the gate static-counted `text.count("tn-gear-tooth")` = 1 on fix-7 —
  and that 1 occurrence is a JS template string (line 16185,
  `' Z" class="tn-gear-tooth"/>'`), while the live DOM holds 246 teeth
  inside `#tn-tacho-mount` (verify-fix7 results.json: teethInMount 246,
  teethInDoc 246, needle found, transition `none`, transform
  `rotate(-59.72deg)` -> `rotate(10.1deg)`, needleMoved true).
- After: `--live-evidence FILE` (JSON) supplies the live measurements.
  `effective_teeth()` returns the live DOM count when the evidence applies;
  (c) and (f) F3 judge the live count. The static count is now taken
  outside `<script>` blocks — a JS template string is the recipe, not a
  tooth — and is still reported (`tn_gear_tooth_occurrences_static`) beside
  the live count. Live evidence also supplies needle presence in the live
  DOM (`needle_in_dom`); a live-measured real needle transition still FAILs.
- Binding (fail-closed): when the evidence carries `page_sha256`, it applies
  ONLY to a page whose bytes hash to it; a mismatch prints
  `live evidence IGNORED — page_sha256 mismatch` and the static count stands.
  Without `page_sha256` the evidence is UNBOUND — applied on trust, and the
  output says so. The evidence file's path is cited in the gate header and in
  the (c)/(f) counts (`live_evidence_file=`) and notes.
- Input filed beside the gate: `fix7-live-evidence.json` (teeth_in_mount 246,
  teeth_in_doc 246, needle_in_dom true, needle_transition "none",
  needle_moved true, page_sha256 of the fix-7 blob).
- Diff: new `read_live_evidence()`, `live_evidence_binding()`,
  `effective_teeth()`, `strip_script_blocks()`; `check_c`/`check_f` take
  `live_evidence`/`evidence_path`/`actual_sha256`; `main` parses
  `--live-evidence FILE` (exit 2 on a malformed file).

## Fix 3 — (f) named harvest source: --harvest-sources input

- Before: the (f) docstring excused "a named harvest source with file + line"
  but the machine had no input for one — `.tg-mode` failed F1 twice.
- After: `--harvest-sources FILE` lists harvested selectors with exact source
  file + lines, one per line (`.tg-mode <file>:<lines>`; compound selectors
  like `.tg-mode.on .tg-dot` are supported — every class named is excused).
  A button class named there is excused in F1 with the cited source, noted as
  `F1 HARVESTED (named source)` and counted (`harvest_source_excused_buttons`).
  A malformed line is an error (exit 2), never silently skipped.
- Verified source (read back from GitHub main, 2026-11-10):
  `NIAS/SMART-BOX/naya-world-welcome.html` lines 4199-4215 define
  `.tg-modes` / `.tg-mode` / `.tg-dot` / `.tg-mode.on` / `.tg-mode.on .tg-dot`;
  Personal lines 13645-13656 carry the same declarations, differing only in
  flex sizing (welcome `flex:1;min-width:140px` vs Personal
  `flex:0 0 auto;min-width:0`). The toggle itself is live-verified
  (verify-fix7 tg_toggle: before `["tg-mode on","tg-mode"]`,
  after `["tg-mode","tg-mode on"]`).
- Input filed beside the gate: `fix7-harvest-sources.txt`.
- Diff: new `read_harvest_sources()`; `check_f` takes `harvest_sources`/
  `harvest_path`; `pedigree()` checks the named map after the allowlist;
  `main` parses `--harvest-sources FILE`.

## No threshold or rule changed

LIGHTNESS 0.80, teeth >= 2, depth >= 90%, containment >= 80%, and every
gate item's pass/fail rule are byte-identical in meaning. Only what is
measured changed: hex8 alpha is parsed, teeth are counted outside scripts
with a live-DOM override, and a named harvest source can now be cited.

## PASS proof — fix-7 with both inputs (fixed gate)

Command:
`python3 check-gate.py --live-evidence fix7-live-evidence.json --harvest-sources fix7-harvest-sources.txt --human-checks <verify-fix7/human-checks.txt> fix7.html`
Result: **OVERALL: PASS, exit 0.** All 8 machine items PASS; H1–H5 PASS
(attested in verify-fix7/human-checks.txt).
- (a) PASS — base canvas lum 0.002; solid_light_surfaces 0; light gradients 0.
- (b) PASS — 316/327 with depth (96.6%).
- (c) PASS — teeth 246 (live DOM count; static source holds 0);
  needle in DOM, live transition none, needle moved between samples.
- (d) PASS — 0 hits; 1 data-URI image, alt scanned.
- (e) PASS — 110/110 blocks contained (100%).
- (f) PASS — 0 look-alikes, 0 gold CTAs; 2 buttons excused by named harvest
  source (`.tg-mode` from `NIAS/SMART-BOX/naya-world-welcome.html:4199-4215`);
  teeth 246 live.
- (h) PASS — 0 banned phrases. (i) PASS — not applicable (0 story boards).

Fix-1-only control (fixed gate, NO inputs): (a) PASS, (c) FAIL (teeth static 0),
(f) FAIL (tg-mode x2 + F3 teeth 0). The alpha fix alone clears (a); (c)/(f)
need the two attested inputs, as designed.

## STILL-FAILS proof — genuinely bad page (synthetic, /tmp/gatefix/bad-page.html)

Built with all three real defects: a solid `#ffffff` panel (not a tint),
a fake gauge (mount + needle with `transition:transform 1.2s`, teeth only as
one JS template string), and an invented button (`.my-fancy-btn`, never
harvested). Dark body canvas, box-shadows present, text contained — so (b),
(d), (e), (h), (i) pass and only the real defects fail.
- No inputs: **OVERALL: FAIL, exit 1** — (a) A2 solid light surface
  `.bad-panel #ffffff (lightness 1.00)`; (c) needle transition + teeth 0;
  (f) F1 `.my-fancy-btn` look-alike + F3 transition + teeth 0.
  The JS template string counts as 0 teeth.
- WITH fix-7's live-evidence + harvest-sources inputs: **still OVERALL: FAIL,
  exit 1** — (a), (c), (f) fail identically, plus
  `live evidence IGNORED — page_sha256 mismatch` in (c) and (f):
  fix-7's evidence cannot rescue another page, and `.my-fancy-btn` is not
  in the harvest file. The inputs whitewash nothing.

## Regression — TEST-REPORT known files (fixed gate, no inputs)

- Dashboard fix-9 (known-good): FAIL (a) only — identical to TEST-REPORT.
  The single hit is still the deliberate white `.os-annot` chip.
  Teeth static 3 (was 4: the JS template string no longer counts; the 3 CSS
  rules still do) — (c) and (f) still PASS.
- Pricing fix-12 (known-bad): FAIL (a)(d)(e)(f) — (a) no dark canvas,
  (d) 2 Top 10 text-in-image hits, (e) 77% contained, (f) 5 look-alike
  buttons + 12 gold-theme CTAs, byte-identical counts to TEST-REPORT.
  NOTE, honest: TEST-REPORT (2026-11-08) also listed (c) FAIL for fix-12
  (needle transition + 1 tooth). (c) now PASSES on fix-12 — NOT because of
  this fix but because of the pre-existing 2026-11-09 calculator-gauge split
  already in the file: fix-12's mount is a calculator gauge
  (calc_gauges=1, needle_law_gauges=0), judged by the calculator standard
  (number paired, needle built by JS, gold rim intact). This seat's teeth
  change cannot affect that path — the needle-law branch is never reached
  for a calculator mount, and no live evidence was supplied.

## NOT DONE

- The fixed gate is filed to the branch, NOT merged (merge is Shawn's hand).
- The gate still does not render pages: live evidence is an attested input
  from a verifier's Playwright run, trusted and cited — the gate itself
  never re-measures the live DOM. His eye remains the final gate.
- `TEST-REPORT.md` in the gate dir is NOT updated by this seat (it describes
  the 2026-11-08 runs); this report is the record for these fixes.
- The `.os-annot` white chip on Dashboard fix-9 still fails (a) — the
  bless-or-fix decision from TEST-REPORT is still open, untouched by this fix.
