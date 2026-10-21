# EXEMPLAR GAP REPORT — What the Smart Factory Actually Holds
## Audit of the design exemplar gallery, 2026-10-21

*Companion to `GENERAL-DESIGN-CONTRACT.human.md`. Every judgment below is made from the pieces' actual CSS, not their names. Shawn's instinct — "we don't have an input proper, an output button at that level" — is tested piece by piece. He is half right, and the half he is right about is the important half.*

---

## 1. THE INVENTORY — THREE LISTS, NO SINGLE CANON

The factory's pieces live in three overlapping inventories, and they do not agree:

| Inventory | Where | Count | Claim |
|---|---|---|---|
| The personal-app piece store | `~/workspace/personal-app/pieces.json` (+ `factory.css`) | **152 pieces** | The set `AGENTS.md` calls canonical ("REAL PIECES ONLY: Every element traces to the Smart Factory (152 pieces)") |
| PIECES-INVENTORY v2 | `~/workspace/team-nitro/smart-builder/PIECES-INVENTORY-v2.json` | **155 unique** | Dated 2026-10-20; says it **supersedes** the 478-piece index; distilled from Verity's smart-builder file |
| The builder index v1 | `HUB/design-system/library/catalog/builder-index-v1.json` (repo checkouts: `nayapower-repo`, `integrator-work`) | **478 entries** | Built 2026-10-17; 459 archived / 19 unarchived sources; 6 pieces quarantined as below standard; carries a 140-entry CSS bank |

**Finding F-1 — there is no single canonical index.** `AGENTS.md` names the 152-piece set canonical *and* names the 478-piece index as a harvest source in the same breath; the v2 inventory claims to supersede the 478 while adding 3 boards the 152 set lacks. A builder following three different "canonical" lists can harvest three different pieces under one ID family. The inventories must be reconciled into one canon — the 152-piece store is the working set today (it is the one with live CSS in `factory.css`), and this audit judges from it — but the conflict itself is a defect to close in the exemplar pass.

Piece families in the working set (152): BTN 33 · BRD 27 · ICO 26 · JWL 21 · NAV 11 · ORB 8 · INP 7 · MRK 7 · OVL 5 · ROW 4 · HDR 3. Note what is absent: **no HERO family, no SELECT family.**

Supporting materials audited: `~/workspace/factory-pipeline/assets/` holds brand artwork only (diamond masters in 5 colors, a `naya-gallery` of images, samples) — no component exemplars. `contracts.json` holds the 12 build templates (name/tagline/about per template) — build recipes, not design exemplars.

The factory's own depth utilities, from `factory.css` (lines 1149–1155), are genuinely good and are the raw material exemplars should be built from:

- `.elev-1 / .elev-2 / .elev-3` — outset stack: drop shadow + 1px light ring + inset top highlight, in three strengths.
- `.carve-1 / .carve-2` — inset stack: deep inner shadow + inner bottom light ("INNER: carved into the screen," the file's own words).

The utilities know the grammar. The question is whether the *pieces* use them at elite level.

---

## 2. THE FIVE EXEMPLARS — VERDICTS

### 2.1 The Reference Well (Input) — **EXISTS-FLAT** *(needs elevation rebuild)*

Three candidates exist; none demonstrates the full well:

- **NAYA-INP-001 "Search bar"** — `.search-input` (factory.css:1237): background `rgba(255,255,255,.03)`, a 1px line border, **no shadow stack at all**. On focus it gains only a colored ring. This is precisely the "basic flat text box" Shawn's law names as the thing that wrecks a page — sitting in the factory as a piece.
- **NAYA-INP-002 "Alias field"** — `.alias-field-wrapper` (factory.css:1243): dark ground, bright 2px border, but its depth is an **outset** drop shadow (`0 8px 22px`) with a whisper of inset (`inset 0 1px 2px`). A well's depth must go *in*; this one floats. It is a handsome frame, not a well.
- **NAYA-INP-005 "Recessed field"** — the closest to a true well (factory.css:1529): real inset depth (`inset 0 3px 10px rgba(0,0,0,.9)`) on near-black `#030304`, and `:focus-within` ignites it purple. But its border is plain white at 0.72 alpha — it carries **no color light of its own**; there is no layered outer glow at rest; the label text renders `#c9c3cf` (dim — a text-law violation inside the piece itself); and there is no focus travel, only a state swap.

SN-0808 names the certificate's name input as the reference well — but that piece lives embedded in the identity page, **not in the factory store**, and Shawn judged even it "dead… not active… no depth" at rest tonight (it is being rebuilt in the certificate pass now running). **Verdict: no factory piece a designer can harvest demonstrates the elite well. EXISTS-FLAT — rebuild INP-005's recessed concept to the full dual-depth stack and crown it the reference.**

### 2.2 The Reference Button (Action) — **EXISTS-ELITE**

Shawn doubted this one exists at level. In the factory, it does:

- **NAYA-BTN-009/010/011 "Hero · living-btn"** (factory.css:472–524): a glow layer (`.btn-glow`) burning in its spectrum color at rest (opacity .55, full 1.0 on approach); hover raises the full outset stack — inset color ring, inset top highlight, inset bottom shadow, a 60px colored bloom and a deep drop shadow — while lifting `translateY(-4px) scale(1.025)`; **press physics present**: `:active` sinks it `translateY(1px) scale(.975)` on a fast .08s. This is an outset button a hand understands.
- **NAYA-BTN-004–008 "Primo" family** (factory.css:450–469): the standard-size sibling — obsidian gradient, white-hot border, a **periodic shine sweep** (`primo-sheen`, 3.5s) at rest, full ignition stack on hover, press sink `translateY(1px) scale(.985)`. This is the button the Spaces hero borrowed its sheen from.

Two honest caveats, neither disqualifying: (1) at rest the living-btn leans on its glow layer — the full shadow stack blooms on hover rather than standing at rest; the exemplar pass should stand a resting stack under it. (2) The press spring-back is a duration trick, not a named spring ease — the Motion Law now requires named specs, so the exemplar's motion should be re-specified in writing when it is crowned. **Verdict: EXISTS-ELITE — designate BTN-009 the Reference Button; no rebuild required to start, two refinements to finish.**

### 2.3 The Reference Select — **MISSING**

There is no select piece. The INP family's seven pieces are: search, alias, segmented control, toggle, jeweled checkbox, recessed field, settings row. **No dropdown, no chooser, no select of any kind carries a NAYA-* ID in any of the three inventories.** The only native `<select>` styling anywhere in the system is `.naya-tabs-pop select` (factory.css ~line 106): `border: 1px solid rgba(255,255,255,.20); background: #0a0a0e` — **zero shadow, zero depth, completely flat**, inside a settings popover where nobody looks. The segmented control (INP-003) is a tablist, not a select, and its chosen state is only modestly lit (factory.css:1520). **Verdict: MISSING — Shawn's instinct is exactly right. A designer who needs a select today must invent one, which is how flat gets in.**

### 2.4 The Reference Section / Board — **EXISTS-ELITE** *(one text repair)*

- **NAYA-BRD-001 "Feature board"** (`.board-h`, factory.css:1058): glossy obsidian gradient field, a 1.5px border in the board's **own spectrum color** (`--bc`), inset top highlight, inset bottom shadow, a colored outer glow (`0 0 30px -12px var(--bc)`), and a deep drop shadow (`0 18px 40px`). Its icon socket burns in the board's color with its own glow. This is a living section at elite depth — the board grammar the whole system already speaks.

One repair, named plainly: `.bh-text p` renders at `rgba(248,247,251,.75)` — text dimmed to 75%, a direct violation of the Text Law (white/bright silver, never dimmed) **inside the exemplar itself**. And the board's own action (`.bh-btn`) runs on a flashing-glow animation rather than the Primo/living stack — it works, but the exemplar should model the reference button, not a cousin. **Verdict: EXISTS-ELITE — crown BRD-001 the Reference Board, with the 75%-text fix as the exemplar pass's smallest and most symbolic repair: the reference piece must obey the laws it demonstrates.**

### 2.5 The Reference Hero — **MISSING** *(as a harvestable piece)*

Heroes exist — but only embedded inside finished pages: the personal app's `.hero-show` composition, the Hub's hero, the Spaces dimensional `.sp-brand-frame` treatment that became the family signature. **None of them carries a NAYA-* ID; none can be harvested; there is no HERO family in any inventory.** What the store holds are hero *ingredients*: the hero buttons (BTN-009–011), the hero orb (NAYA-JWL-016), the eyebrow (NAYA-HDR-001). A designer told to "build the hero like the standard" today has to open a finished page and reverse-engineer it — harvest by archaeology. **Verdict: MISSING — the hero must be distilled from the best living page (Spaces' dimensional frame + the glossy obsidian treatment) into one named, harvestable piece.**

---

## 3. THE BUILD LIST — THE EXEMPLAR PASS, IN PRIORITY ORDER

Each item lands as a harvestable piece in the canonical store (`pieces.json` + `factory.css`), judged against the contract's checks, and is crowned in the gallery the contract points at.

1. **NAYA-INP-008 — The Reference Well** *(rebuild of the INP-005 concept)*. Full dual-depth stack: deep inset well (carve-2 class depth) with inner light at the bottom edge; border carrying its accent color's light at rest; layered outer glow, alive at rest and stronger on focus; **focus travel** — light moves around the border on entry; label and placeholder in bright silver/white only. This is priority one: inputs are where flat hides, and Shawn has caught it three times in two nights.
2. **NAYA-INP-009 — The Reference Select** *(new)*. A well that opens a lit panel: the closed state is the Reference Well showing its chosen value as a lit display; the panel rises with elevation, options ignite in their own color on approach, the chosen option carries a jewel mark. Motion specs named; reduced-motion state fully lit and static.
3. **NAYA-HRO-001 — The Reference Hero** *(new family)*. Distilled — not invented — from the Spaces dimensional frame + glossy obsidian material in `factory.css`: full-width obsidian field with its light source inside it, the mark, headline at hero scale, spectrum ignition on its actions (Reference Buttons ride in it), a periodic shine sweep. One piece, harvestable whole.
4. **Errata on the crowned pieces** *(repairs, no new IDs)*: (a) BRD-001 — raise `.bh-text p` to full bright silver; re-seat `.bh-btn` on the Primo stack. (b) BTN-009 — stand a resting outset stack under the glow layer; write its motion specs (durations + named ease) into the piece record per the Motion Law. (c) Retire or rebuild INP-001's flat search treatment so no flat input remains harvestable under a factory ID.
5. **Reconcile the canon** *(the F-1 fix)*. One index: merge the 155-inventory's three extra boards into the working store, mark the 478-index historical, and make `AGENTS.md`, the contract, and the store name the same list. Until this is done, every brief cites piece IDs **with their source file** — which the contract's read-first gate already requires.

**Designation, no build needed:** NAYA-BTN-009 is the Reference Button and NAYA-BRD-001 is the Reference Board, effective with this report — a designer starting tomorrow harvests those two as-is while the three builds above land.

---

## 4. WHAT COULD NOT BE LOCATED

- **A single canonical piece index** — does not exist (Finding F-1). Three inventories found and named above; the "152" and the "478" are both real and both cited as sources in standing documents.
- **Any select/dropdown piece, in any inventory** — none exists.
- **Any hero piece with a NAYA-* ID** — none exists; heroes live only inside finished pages.
- The SN-0808 source file: the brief named it `SN-0808.md`; on disk it lives as `~/workspace/elevation-standard/IB-SMART-NOTE-20261021-sn0808-the-elevation-standard.md` (plus push artifacts). Same note, verified by content — the canonical paragraph was quote-checked against it verbatim for the contract.

*Sources read for this audit: `~/workspace/personal-app/pieces.json` (all 152 pieces); `~/workspace/personal-app/factory.css` (elevation utilities L1149–1155, Primo L450–469, living-btn L472–524, board-h L1058–1064, search-input L1237–1239, alias field L1241–1246, recessed field L1529–1532, tabs-pop select ~L106, segmented L1520); `~/workspace/factory-pipeline/contracts.json` + `business-contract.json`; `~/workspace/factory-pipeline/assets/` listing; `~/workspace/team-nitro/smart-builder/PIECES-INVENTORY-v2.json` (meta + families); `HUB/design-system/library/catalog/builder-index-v1.json` (meta: 478 entries); `~/workspace/elevation-standard/` (SN-0808, as filed). No live pages were edited; nothing was deployed.*
