# NAYA-INP-008 RE-BASE — SCORECARD

**Date:** 2026-10-21 · **Scope:** local files only, no live deploys.
**What moved:** the Reference Well's CSS technique — from the v2.10 certificate
well (harvested 2026-10-21 in the exemplar pass) to the Smart Factory input
recipe (harvested from the live Smart Factory inputs, proven on certificate
v2.11.2 — both addresses, verified by the main seat; Shawn's verdict on
v2.11.2, 05:19Z: "the best it looks and presented yet").
**Recipe source:** `~/workspace/front-door/v211/DEPTH-RECIPE.md` + the well
section of `~/workspace/front-door/v211/SCORECARD.md`.

---

## §1 What changed — files

| File | Change |
|---|---|
| `~/workspace/personal-app/factory.css` | `.ref-well-box` rest + `:focus-within` stacks replaced with the factory recipe; the INP-008 header comment rewritten with the new provenance. 39 diff lines, INP-008 block only. Braces balanced (1187 / 1187). |
| `~/workspace/personal-app/pieces.json` | INP-008 `motion` record rewritten (it encoded the retired values: deepen .60/.66 → .50/.72, ring 3px @.22). Verified by parsed diff: **only** `NAYA-INP-008.motion` differs in the whole store; `reference: true` intact. HTML unchanged. |
| `~/workspace/smart-factory-contract/CANONICAL-PIECE-INDEX.json` | INP-008 gains a `harvest_source` note (Smart Factory inputs, live-bytes md5 `9163342c…`; re-base + pointers to this scorecard and the recipe). Status / reference untouched. |
| `~/workspace/smart-factory-contract/CANONICAL-PIECE-INDEX.md` | One Notable-entries bullet added, mirroring the JSON note + the INP-009 follow-up flag. |
| `~/workspace/smart-factory-contract/showcase/index.html` | **No edit needed** — the showcase wears `factory.css` live and the store markup is unchanged, so the re-based well simply appears. It served as the verification surface. |
| `GENERAL-DESIGN-CONTRACT.machine.json` | **NOT applied — prepared, blocked, see §6.** The real file is byte-identical to its pre-pass state (md5 `5f542025…` before and after) and the validator passes on the real tree. |
| `GENERAL-DESIGN-CONTRACT.human.md` | Untouched (per guard). |

Backups taken before editing, in `~/workspace/smart-factory-contract/backup/`:
`pieces.json.bak-20261021-inp008rebase`, `factory.css.bak-20261021-inp008rebase`.

**Old stack → new stack (`.ref-well-box`):**

| | Retired (certificate-well harvest) | Re-based (Smart Factory recipe) |
|---|---|---|
| Background | `linear-gradient(180deg,#040405,#060607)` | `#030304` — flat, one tone |
| Rest border | 1.5px solid accent @.80 | 1.5px solid `rgba(255,255,255,0.85)` silver-white rim |
| Rest shadow | 9 layers / 5 inset — deep soft shade 16px 32px @0.66, bottom light, accent inner washes, accent glows 24px @0.30 + 54px @0.14 | **3 layers / 2 inset** — `inset 0 3px 10px rgba(0,0,0,0.90)`, `inset 0 1px 2px rgba(255,255,255,0.15)`, `0 0 18px rgba(248,247,251,0.30)` |
| Focus shadow | well *deepens* (.50 / 18px 36px @0.72) + ring `0 0 0 3px` accent @0.22 + glows 30px/70px | shade + lip **kept identical**; accent ignites: `0 0 0 1.5px` accent @0.90 ring + `0 0 34px` accent @0.55 glow; border → full accent |
| Focus travel | conic ring 2.8s | **kept** — INP-008's own spec, running on the accent |
| Typed text | white | white (unchanged) |

## §2 Computed-style proof (headless Chromium, showcase page, `--wc` = #a06bff)

Probe: rest read *before* any focus; focus read after a 700ms settle (past the
.28s transition). Baseline was captured with the same probe before the edit.

**REST — before:** background `linear-gradient(rgb(4,4,5), rgb(6,6,7))`, border
`rgba(160,107,255,0.8)`, shadow 9 layers (5 inset, incl. `0px 16px 32px`
@0.66 and the 54px @0.14 glow).
**REST — after (verbatim computed):**
```
backgroundColor: rgb(3, 3, 4)            backgroundImage: none
borderTopColor:  rgba(255, 255, 255, 0.85)
boxShadow: rgba(0, 0, 0, 0.9) 0px 3px 10px 0px inset,
           rgba(255, 255, 255, 0.15) 0px 1px 2px 0px inset,
           rgba(248, 247, 251, 0.3) 0px 0px 18px 0px
input color: rgb(255, 255, 255)         placeholder: rgb(232, 232, 236) (#E8E8EC)
```
**FOCUS — after (verbatim computed):**
```
borderTopColor: rgb(160, 107, 255)      (full accent)
boxShadow: rgba(0, 0, 0, 0.9) 0px 3px 10px 0px inset,
           rgba(255, 255, 255, 0.15) 0px 1px 2px 0px inset,
           rgba(160, 107, 255, 0.9) 0px 0px 0px 1.5px,
           rgba(160, 107, 255, 0.55) 0px 0px 34px 0px
::before (travel ring): opacity 1, animation ref-well-travel, 2.8s
```
The inset pair is byte-identical between rest and focus — the shade is kept,
the well does not deepen; only the accent arrives. Every value matches the
recipe in DEPTH-RECIPE.md and the deployed certificate well in the v211
scorecard, with the accent substituted for the certificate's green.
*Measurement caveat:* this headless shell serializes `border-top-width` as
`1px` both before and after the edit (the CSS declares 1.5px in both
versions) — an environment serialization quirk, unchanged by the re-base.

## §3 Showcase harness results

**verify.mjs** (full run, after): well — `shadowHasInset: true`,
`shadowLayers: 2` (was 5), `borderColor: rgba(255, 255, 255, 0.85)`,
`focusRingAnimation: ref-well-travel`, `focusRingOpacity: 1`, placeholder
`rgb(232,232,236)`, input `rgb(255,255,255)`. Button, board, hero results
identical to the pre-pass record — BTN-009 / BRD-001 / HRO-001 untouched and
still passing. Select — see §4.
*Known artifact, not a regression:* verify.mjs reports
`focusShadowDeepened: false` — it did so in the pre-pass record too
(verify-out.json), because it samples the "focused" style at transition
start. The settled-focus probe in §2 proves the focus stack genuinely
differs from rest (accent ring + glow arrive).

**verify2.mjs** (after): `wellRest` / `wellFocus` print exactly the recipe
strings in §2; `wellDeepened: true` (its label is legacy — it measures
focus ≠ rest, which is now true by ignition, not deepening);
`chevTransformOpen` = 180° rotation (select intact);
`livingBtnActiveRuleInCSS: true`, `livingBtnRestingLayersAdded: true`.
⚠️ `wellFocusRing: false` — **stale harness literal, flagged not fixed:**
verify2.mjs asserts the retired ring (`0px 0px 0px 3px`); the ring is now
1.5px by design, and the very same run's `wellFocus` string shows it
(`0px 0px 0px 1.5px`). verify2.mjs is outside this pass's file scope; its
literal should move 3px → 1.5px in a follow-up.

**probe.mjs** (after): no light-background elements found on the page —
unchanged from its purpose (page-background sanity), no regression.

## §4 INP-009 — the Reference Select check

- **Does it consume `.ref-well-box`? No.** `.ref-select-btn` carries its OWN
  copy of the retired 9-layer stack in factory.css (its header comment says
  "same inset stack" — a copy, not a consumption). Per the brief, it is left
  untouched and the divergence is flagged here and in the canon index.
- **Proof of no change:** the select's computed closed-state shadow is
  byte-identical before and after this pass (the 9-layer stack, blue accent:
  `…rgba(63, 184, 255, 0.3) 0px 0px 24px…, rgba(63, 184, 255, 0.14) 0px 0px
  54px…`).
- **Showcase checks still pass:** verify.mjs select block — opened ✓,
  `aria-expanded: true` ✓, panel shadow inset ✓, open animation
  `ref-select-open` ✓, keyboard ArrowDown + Enter chose "Naya" with correct
  `aria-selected` flags ✓.
- **Follow-up flag (for Shawn / a later pass):** INP-009's closed state is
  now the last wearer of the retired technique in the exemplar set — accent
  rim at rest, 24px/54px accent glows, deepening focus stack. Re-basing it
  onto the same recipe (silver rim at rest, accent on focus, shade kept)
  is a small, well-defined pass whenever it's authorized.

## §5 FLAG — tension with the human contract's LAW-02 wording (for Shawn)

**Not reconciled — recorded, per the guard.** LAW-02's statement and
human_check (human contract, 2026-10-21 ~02:10Z) say a well carries, *at
rest*: "a border that carries its own color's light", "a border carrying
its accent light, layered outer glow, a drop shadow", and its canonical
quote puts "inner light at its bottom edge". LAW-02-C6 likewise expects
every element's border to carry its own color's light at rest.

The Smart Factory recipe — Shawn's own teaching, 2026-10-21 ~03:32Z, later
and more specific — says the opposite for inputs at rest: the rim is
**silver-white**, the glow is **one white 18px glow** (not layered, not
accent), there is **no drop shadow** (a recess casts none), the light line
sits on the **top lip** (there is no bottom-edge inner light), and the
field's own color ignites **only on focus**. The re-based exemplar follows
the recipe, because the recipe is proven: it is what the live factory
inputs wear, it is what certificate v2.11.2 shipped, and Shawn scored that
page up ("the best it looks and presented yet", 05:19Z).

Under the contract's own §5 (Shawn's word in the moment wins, contract
updated same day), the resolution when he chooses it is a wording pass on
LAW-02 — e.g. inputs rest in silver-white and ignite in their own color on
focus. Until he rules, the human file stands exactly as written and this
flag stands beside it.

## §6 BLOCKED — machine-contract LAW-02 checks: prepared, not applied

The LAW-02 check expectations (C1 rest stack, C3 rest border, C4 focus
stack; C2's expectation stays true verbatim and only its trace moves) were
rewritten truthfully to the re-based exemplar and tested on a scratch copy
of the contract — **everything passes except validator step 7 (numeric
trace)**, which fails on exactly three recipe numbers:

```
✗ 7. UNTRACED numeric expected value 0.15 in check LAW-02-C1
✗ 7. UNTRACED numeric expected value 0.85 in check LAW-02-C3 (×2: border_color + border_alpha)
✗ 7. UNTRACED numeric expected value 0.15 in check LAW-02-C4
✗ 7. UNTRACED numeric expected value 34   in check LAW-02-C4
```

Why: step 7 searches every numeric expected value in the human contract +
EXEMPLAR-BUILD-SCORECARD.md only. `0.15` (lip-line alpha), `0.85` (rim
alpha) and `34` (focus-glow px) appear in **neither** (verified by grep:
zero occurrences) — they are genuinely new values whose evidence lives in
`front-door/v211/DEPTH-RECIPE.md`, the v211 scorecard, and this scorecard.
Every other number in the prepared checks traces (82 traced in the test
run). Writing the values in any other form to slip past the extractor
would be gaming the gate, so it was not done.

**Remedy (one line, intent-preserving — needs a decision, not taken here):**
add this scorecard to the validator's trace sources —
in `validate-machine-contract.py`, `trace_sources = human + "\n" + scorecard`
becomes a sum that also reads `INP008-REBASE-SCORECARD.md`. The gate's rule
(every number evidenced in a governing document) is unchanged; the re-base
scorecard simply becomes one of the documents it reads. **Proven, not just
asserted:** on a scratch copy, the Appendix's prepared checks + this one-line
change return **PASS — 86 values traced, 0 untraced** (the test also caught
and the Appendix avoids a phrasing artifact: a "(LAW-04-C2)" cross-reference
inside an expected string parses as the number −4; the Appendix writes
"(Law 4)" instead). The full prepared replacement JSON for LAW-02-C1…C4 is
in the Appendix, ready to apply verbatim the moment the remedy (or a LAW-02
wording pass per §5) lands.

**State left behind:** the real `GENERAL-DESIGN-CONTRACT.machine.json` is
untouched, and `python3 validate-machine-contract.py` on the real tree
returns **PASS** (73 values traced, 0 untraced) with all of this pass's
other edits in place — canon step 5 confirms INP-008 canonical +
`reference: true` in the store. The cost of the block is named plainly: a
ship gate running today's LAW-02-C1/C3/C4 against the re-based well would
fail a correct piece, because the checks still describe the retired stack.

## §7 Screenshot read (my own eyes, desktop width 1280)

- **Rest:** bright silver-white rim as one clean line; flat black fill; a
  quiet white halo hugging the box (the 18px @0.30 glow — present, not
  loud); placeholder in bright silver. It reads as a machined computer
  input, not a glow blob. ✓ matches the factory read.
- **Focus (typed text in):** full purple rim + ring, white typed text, the
  34px glow dosed — a tight halo on the silhouette, no fog on the page;
  the travel ring's bright segment visible mid-orbit at the bottom edge.
- Side-by-side in the same frame, the unfocused INP-009 below still wears
  its blue accent rim and broader glow — the retired grammar, visibly
  different. That contrast is the §4 flag in picture form.

## §8 Scores (3-pass, honest)

- **Pass 1 — recipe fidelity: 9.8.** Computed styles match DEPTH-RECIPE.md
  layer for layer in both states, accent substituted as specified; travel
  ring kept at 2.8s. Not 10: the border-width serialization caveat in §2
  is an environment quirk I could observe but not resolve from here.
- **Pass 2 — verification depth: 9.6.** Baseline + after probes with the
  same instrument; all three showcase scripts run; select proven unchanged
  *and* still passing; screenshots read in both states; validator green on
  the real tree. Not 10: verify2.mjs carries a stale literal I flagged
  rather than fixed (scope).
- **Pass 3 — contract integration: 8.8.** Canon + store + CSS all carry the
  new provenance consistently, and the LAW-02 wording tension is flagged
  with its provenance argument. Held down by §6: the machine checks still
  describe the retired stack until the one-line remedy is approved — the
  re-base is complete everywhere this pass was authorized to complete it,
  and the one remaining move is named, prepared, and waiting on a decision.
- **Overall: 9.4.**

---

## Appendix — prepared LAW-02 check replacements (NOT applied; see §6)

```json
LAW-02-C1 expected:
{
  "inset_layers": [
    "inset 0 3px 10px rgba(0,0,0,0.90)",
    "inset 0 1px 2px rgba(255,255,255,0.15)"
  ],
  "resting_glow_layers": ["0 0 18px rgba(248,247,251,0.30)"],
  "background": "flat #030304 — one tone, no gradient",
  "verified_computed": "3 shadow layers, 2 inset"
}
LAW-02-C1 trace: "INP008-REBASE-SCORECARD.md §2 (computed-style proof);
front-door/v211/DEPTH-RECIPE.md 'THE WELL'; factory.css .ref-well-box.
Supersedes the EXEMPLAR-BUILD-SCORECARD.md §1 stack (harvested from the
rejected certificate well)."

LAW-02-C2 expected: unchanged ("offset cast-shadow layers (a recess casts none)")
LAW-02-C2 trace: "EXEMPLAR-BUILD-SCORECARD.md §1: 'no cast shadow of its own
— a recess casts none'; re-verified against the re-based stack in
INP008-REBASE-SCORECARD.md §2: the only outset layer is the 0-offset rest
glow (no offset, no cast)."

LAW-02-C3 comparator: "silver_white_rim_at_rest"
LAW-02-C3 expected:
{
  "border_width_px": 1.5,
  "border_color": "silver-white rgba(255,255,255,0.85)",
  "border_alpha": 0.85,
  "accent_arrival": "the element's own color takes the border only on focus (check C4 of this law)"
}
LAW-02-C3 trace: "INP008-REBASE-SCORECARD.md §2; front-door/v211/DEPTH-RECIPE.md
'THE WELL' (rest rim silver-white .85; accent on focus only). Supersedes
EXEMPLAR-BUILD-SCORECARD.md §1 'border 1.5px in its accent at .8'.
FLAGGED TENSION with LAW-02's general wording — see INP008-REBASE-SCORECARD.md §5."

LAW-02-C4 expected:
{
  "inset_layers": [
    "inset 0 3px 10px rgba(0,0,0,0.90)",
    "inset 0 1px 2px rgba(255,255,255,0.15)"
  ],
  "focus_ring": "0 0 0 1.5px rgba(accent,0.90)",
  "focus_glow": "0 0 34px rgba(accent,0.55)",
  "relation_to_rest": "shade and lip identical to rest (the well does not deepen); the accent ignites — border goes full accent, ring + glow added; the focus-travel conic ring orbits the border throughout (Law 4)"
}
LAW-02-C4 trace: "INP008-REBASE-SCORECARD.md §2 (computed-style proof);
front-door/v211/DEPTH-RECIPE.md 'THE WELL' (focus doses proven on
certificate v2.11.2). Supersedes EXEMPLAR-BUILD-SCORECARD.md §1 deepening
stack + 3px ring."
```

---

## ADDENDUM — remedy applied by the main seat (Naya Nitro Narzan, 2026-10-21 ~05:27Z)

The §6 block is resolved. On the main seat's authority (validator + machine checks are machine-maintenance; the human contract is untouched):

1. `validate-machine-contract.py`: `INP008-REBASE-SCORECARD.md` added to `trace_sources` (one line; backup `backup/validate-machine-contract.py.bak-20261021-inp008rebase`).
2. `GENERAL-DESIGN-CONTRACT.machine.json`: the Appendix's LAW-02-C1/C2(trace)/C3/C4 replacements applied verbatim (backup `backup/machine.json.bak-20261021-inp008rebase`).
3. Validator re-run on the real tree: **PASS — 86 values traced, 0 untraced**; statements/why/human_check still verbatim (step 3 green); INP-008 canon + reference confirmed (step 5).

Main-seat verification beyond the builder's report: factory.css `.ref-well-box` carries the exact recipe values; parsed diff of pieces.json vs its pre-pass backup shows ONLY `NAYA-INP-008.motion` changed in the whole store.

Still open, by design: the §5 LAW-02 human-wording tension (awaits Shawn's ruling — the recipe is later and more specific than the general wording) and the INP-009 select's own retired-stack copy (flagged follow-up, untouched per scope).
