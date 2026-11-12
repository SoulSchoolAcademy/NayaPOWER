# EXEMPLAR BUILD SCORECARD — The Five Reference Pieces + The One Canon
## Built 2026-10-21 · Shawn's approval 02:11Z · Companion to EXEMPLAR-GAP-REPORT.md

*Every piece below was composed from named harvest sources — nothing invented. Stores touched: `~/workspace/personal-app/pieces.json` and `~/workspace/personal-app/factory.css` (backups in `~/workspace/smart-factory-contract/backup/`). No live page was deployed. The three source inventories were read, never written (mtimes verified unchanged after the pass).*

---

## 1. NAYA-INP-008 — The Reference Well 👑 *(new)*

**Harvest sources:** INP-005's recessed concept (`factory.css` `.recessed-field`) corrected; the certificate name well's proven stack (`~/workspace/front-door/identity.html` v2.8, `.alias-field-wrapper` rest + `:focus-within`) parameterized on `--wc`/`--wc-rgb`; focus-travel ring mechanism from BTN-026's `@property` conic rim (`.orbit-btn`).

**Built:** label in full-bright `#F8F7FB` (INP-005's dim `#c9c3cf` label is the defect this corrects); well box = 9-layer stack — inset top shadow `0 2px 6px rgba(0,0,0,.60)` + deep inset `0 16px 32px rgba(0,0,0,.66)`, inner bottom light, accent inner glows, page-lip hairlines, and **no cast shadow of its own — a recess casts none**; border `1.5px` in its accent at .8; layered resting glow `0 0 24px /.30 + 0 0 54px /.14` — alive at rest. Text `#fff`; placeholder `#E8E8EC` at opacity 1.

**Motion specs (named, also in the piece record):** focus travel — conic light ring (`ref-well-travel`, `--wa` 0→360deg) orbits the border **2.8s linear infinite** while `:focus-within`; well deepens on focus (inner shadow → `.50 / 0 18px 36px .72`) + static ring `0 0 0 3px` accent .22; `box-shadow .28s cubic-bezier(.16,.84,.22,1)`, `border-color .18s ease`. Reduced motion: ring animation none; the static lit focus ring holds.

**Verification (computed, headless Chromium):** rest shadow = 9 layers, 5 inset ✓ · focus shadow deepens and gains the 3px ring ✓ · `::before` animation-name `ref-well-travel`, opacity 1 on focus ✓ · placeholder computes `rgb(232,232,236)` ✓ · input text `rgb(255,255,255)` ✓.

## 2. NAYA-INP-009 — The Reference Select 👑 *(new — the family did not exist)*

**Harvest sources:** the Reference Well's stack (closed state is the well, verbatim values); the outset mini-button grammar (Primo/living inset highlight + cast shadow) for the chevron disc; BRD-001's board elevation for the panel; INP-003's Human/Naya/Machine voice set as the demonstration options.

**Pattern chosen:** button + listbox with full ARIA (`aria-haspopup="listbox"`, `aria-expanded`, `role="listbox/option"`, `aria-selected`) — chosen over a styled native `<select>` because a native select's open panel cannot be styled in any browser, and the Function Law requires the open state to be the lit panel, not an OS default. Keyboard: Enter/Space/↓ opens; ↑/↓ move; Enter chooses; Esc/Tab close; click-outside closes. The behavior contract is written into the CSS header comment so a harvester wires it, never reinvents it.

**Built:** closed = well + raised chevron disc (outset stack, own-color glow); open = lit panel (board gradient, accent border .55, inset highlight, `0 0 30px -10px` accent glow, `0 24px 50px` drop); options ignite in the select's color on hover/active; the chosen option carries a lit diamond jewel (hollow → filled + glowing when selected). Press on the button sinks `translateY(1px) scale(.99)`.

**Motion specs:** panel opens `ref-select-open .22s cubic-bezier(.16,.84,.22,1)` (opacity 0→1, translateY −4px→0, scale .98→1); chevron rotates 0→180deg `.24s` same ease; press `.08s`. Reduced motion: open animation none, chevron transition none — panel fully lit and static.

**Verification:** closed shadow contains inset ✓ · click opens (`hidden=false`, `aria-expanded=true`) ✓ · panel shadow contains inset, animation-name `ref-select-open` ✓ · chevron computes the 180° matrix when open ✓ · **keyboard end-to-end**: ↓ + Enter chose "Naya" — value text updated, `aria-selected` moved, panel closed ✓ · screenshot of the open panel read: lit panel, jewel lit on the chosen row, chevron flipped ✓.

## 3. NAYA-HRO-001 — The Reference Hero 👑 *(new family)*

**Harvest sources:** Hub hero composition (`~/workspace/user/files/index-2.html` — foundation-obsidian gloss fall `#1b1b22 → #08080c → #030304`, deepened ray-burst `#0a0910/#030304/#14111a`, Primo sheen behavior at 5s, accent border, full elevation stack, its reduced-motion rule) + Spaces' brand-frame composition (`~/workspace/user/files/spaces.html` v3 — ringed mark, title/topic slots) at the bigger hero scale the later passes set (Hub title 60px-class / Spaces v3 30/21/16).

**Built:** `.ref-hero` on `--sc`/`--sc-rgb` (the room's own color): gloss fall + accent radial at top + burst + base obsidian gradient; mark slot (84px ringed mark, Spaces values at hero scale), eyebrow (`#E8E8EC`, letterspaced), title `clamp(25px,3vw,32px)`/900 white with accent halo, sub 21px/700 `#F2F2F6`, desc 16px/700 `#E8E8EC` — no dim text anywhere; actions slot where Reference Buttons ride un-restyled. Full stack: inset top light, inset bottom pool, accent rim glow, deep drop shadow.

**Motion specs:** sheen sweep `ref-hero-sheen 5s ease-in-out infinite` (Hub-harvested timing); mark breathes `ref-hero-breathe 5.6s ease-in-out infinite` (certificate's calm rhythm). Reduced motion: both none, sheen rests at opacity .45 — lit, never dead.

**Verification:** background computes with the gloss fall AND the conic burst ✓ · border accent at .42 ✓ · mark animation `ref-hero-breathe`, sheen `ref-hero-sheen` ✓ · title computes 32px white at desktop, wraps cleanly at 390px ✓.

## 4. Errata on the crowned pieces

- **NAYA-BRD-001 (a) — text fix:** `.board-h .bh-text p` `rgba(248,247,251,.75)` → `#E8E8EC`. Verified computed: color `rgb(232,232,236)`, opacity **1** — the exemplar now obeys the Text Law it demonstrates. (The gap report's second suggestion — re-seating `.bh-btn` on the Primo stack — was **not** in this pass's errata list and was not done; the button still runs its `btn-flash` animation. Recorded as a remaining refinement, not silently absorbed.)
- **NAYA-BTN-009 (b) — resting stack + motion record:** two layers added under the glow in the `.living-btn` base stack (`0 22px 54px rgba(0,0,0,.55)` ground shadow + `0 0 30px -8px rgba(255,255,255,.22)` resting halo), and the named motion specs (breathe 4.2s, sweep 5.5s on the house ease, hover lift .28s, press sink .08s, reduced-motion behavior) written into its `pieces.json` entry. **Cascade truth, verified by computed style:** all three living-btn pieces (009/010/011) wear `elev-3`, whose utility stack computes at rest (`0 16px 40px` + ring + inset highlight) — a resting outset stack standing under the glow, as the errata requires; the strengthened base stack now governs the button wherever it is worn without the utility, and hover/press come from the living-btn rules. Press proven by a real CDP mouse press: transform `matrix(0.975, …, 0, 1)` mid-press; release springs to the hover lift.
- **NAYA-INP-001 (c) — SUPERSEDED:** `pieces.json` entry annotated `status: "superseded"`, `superseded_by: "NAYA-INP-008"`. Piece and `.search-input` CSS retained — no page referencing it breaks.

**Crowns recorded:** `reference: true` added to BTN-009 and BRD-001 in `pieces.json` (the three new pieces carry it natively). The store schema otherwise stays `{name, html}`; the annotation keys (`reference`, `motion`, `status`, `superseded_by`) are documented in the canon.

## 5. The canon — CANONICAL-PIECE-INDEX.md + .json

**Before:** three inventories, three claims — 152 (working store) / 155 (PIECES-INVENTORY v2) / 478 (builder-index-v1) — and `AGENTS.md` citing two of them as canon at once.
**After:** one index — **571 unique piece IDs** reconciled by ID across all three sources:

| Status | Count | Meaning |
|---|---|---|
| canonical | **154** | in the working store with live CSS (incl. the 3 new exemplars) |
| superseded | **1** | NAYA-INP-001 → NAYA-INP-008 |
| unverified | **416** | named in an inventory, absent from the working store — harvesters may not cite them as canon |

Findings the reconciliation surfaced: the store and v2 agree on all 152 shared names (v2 = store + 3 boards: BRD-031/032/033, unverified until they land in the store); the store and builder-index share only 65 IDs and **all 65 collide** (different name AND different HTML — the index is a source-extraction catalog, not a superset; the store governs); 413 IDs exist only in builder-index (whole families: CRD 114, LST 42, TYP 30…); the two builder-index copies on this machine have **different md5s** — the drift had already happened inside the "index" itself; 6 IDs carry builder-index quarantines (recorded per-entry; NAV-001/007 are canonical in the store as different pieces). The rule is stated on the index: **the index is the canon; pieces.json is the working store it describes; conflicts resolve to the index, then to Shawn's word.** No source inventory was deleted or rewritten.

## 6. Proof — the showcase

`~/workspace/smart-factory-contract/showcase/index.html` — all five crowns together on glossy obsidian, generated from the store's own `pieces.json` markup and wearing `factory.css` unmodified. Working, not decorative: the well takes focus and travels; the button was pressed by real mouse events; the select was opened and driven by keyboard to a different value; a Primo counter proves its wiring. Screenshots: `shot-desktop.png`, `shot-select-open-desktop.png`, `shot-phone.png` — all read by the builder. Harness: `verify.mjs` / `verify2.mjs` (raw CDP, no dependencies), output in `verify-out.json`.

**My screenshot read:** the hero reads as the family's dimensional signature — burst inside polished obsidian, mark burning purple, type bright at hero scale. The well is visibly a *well*: black depth, purple light on its rim, glow pooling under it. The open select is the strongest new piece — a lit blue panel with the chosen row's jewel burning. The board's description now reads at the same brightness as its title. At 390px everything holds; BRD-001's text column wraps tightly (its native flex in a padded container — in production it runs full-width; recorded below).

## Honest holds

1. **Motion is specified and state-verified, not film-verified.** Focus travel, press sink, panel open, and breathing were proven by computed styles in their states (rest/focus/pressed/open) — no video capture exists in this environment, so the *feel* of the 2.8s orbit and the spring back is asserted from specs, not from watching them move.
2. **BTN-009's resting stack is split-brained by design of the old store:** `elev-3` computes at rest in the crowned markup; the strengthened base stack governs without the utility. Both are outset stacks standing under the glow — but a future pass could retire the duplication by deciding which one is the button's own.
3. **BRD-001 `.bh-btn`** still animates on `btn-flash` rather than riding the Primo stack (gap-report suggestion, outside this pass's errata). Smallest known refinement left on a crowned piece.
4. **BRD-001 at phone width in a nested container** wraps its text column tightly (title 2 lines, description 3). Native piece behavior, visible in the phone screenshot; full-width production use is unaffected.
5. **416 unverified pieces remain unverified.** The canon names the truth about them; distilling the worthy ones (the v2 boards first) into the working store is future work, piece by piece — this pass did not bless them wholesale.
6. The showcase's first desktop screenshot rendered below-fold exhibits on white — diagnosed as a `background-attachment: fixed` + beyond-viewport capture artifact (probe proved no element paints white), fixed in the showcase chrome only; no piece CSS was involved.

## Scorecard — three passes

- **Pass 1 — build correctness: 9.2.** All three builds registered in the store's native form; CSS balanced (check-css PASS); canon generated from all three sources. Docked: first `pieces.json` dump changed the file's escaping form (caught and re-dumped natively — final diff is exactly the intended 31 lines).
- **Pass 2 — proof: 9.6.** Every assertion green in a real browser engine; two apparent failures (focus shadow, chevron) were proven to be harness timing, then re-verified with settled-state reads; screenshots read at both widths; the white-capture artifact was root-caused instead of shipped.
- **Pass 3 — honesty & scope: 9.6.** Errata done exactly as named (no silent extras — the `.bh-btn` re-seat was left out *and* declared); the elev-3 cascade truth is written down instead of papered over; sources untouched; holds named with their reasons.

**Final: 9.6 / 10.** What keeps it from 10: motion feel is spec-proven, not eye-proven (hold 1), and two crowned-piece refinements remain knowingly outstanding (holds 2–3) — both are one-line follow-ups, named here so the next pass starts from truth.

*Lessons consulted: none applicable from the Nitro registry — Shawn's direct approval (2026-10-21 02:11Z).*
