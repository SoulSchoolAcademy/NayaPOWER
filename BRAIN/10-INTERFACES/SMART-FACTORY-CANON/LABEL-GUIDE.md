# LABEL-GUIDE — the dual-label doctrine for Factory pieces

**Home of the labels:** `pieces.json` (the piece store). Every entry carries BOTH labels,
always, in the same entry. A piece without both labels is not finished — it does not ship,
it does not get picked, it does not get composed.

## The human label — `name`

What a person calls the piece, in a person's words.

- **Cold-stranger test:** someone who has never seen the Factory reads the name and knows
  what the thing is. "Search bar", "Smart tabs", "Countdown" pass; a CSS class, a build
  codename, or a metaphor with no plain word beside it fails.
- The name says what it **is**, never what the builder was feeling. Color or variant rides
  after a `·` ("Orb · Magenta", "Gem bullet · Gold"); the family's exemplar carries the
  word "Reference" ("Reference Hero", "Reference Well") so a picker finds the crowned one
  by eye.
- Names are unique across the store. Two pieces with one name are two pieces mislabeled.

## The AI label — `ai_label`

What a Naya calls the piece, in her words — precise, contract-grounded, machine-readable.
An object with exactly three members:

- **`purpose`** — what the piece actually is, traced from its real markup: its class or
  treatment, its content, its size. Harvest, never invent: if the class isn't in the
  piece's `html`, it isn't in the purpose.
- **`use_when`** — a directive sentence a builder can act on: "Use when…", naming the
  situation the piece belongs in — and, for exemplars, the standing rule: *copied from,
  never restyled.*
- **`laws`** — the contract laws the piece embodies, as `["Law 3", …]`. A "Law N"
  reference resolves to `LAW-NN` in the Factory law shelf
  (`GENERAL-DESIGN-CONTRACT.machine.json` → `/laws`, Laws 1–16). Every cited law must
  exist on that shelf; a reference that resolves nowhere is an orphan and fails
  validation. Cite the laws the piece *embodies*, not every law it merely obeys.

## Retired pieces

A superseded piece keeps both labels. Its `purpose` begins **RETIRED** and names the
successor by id; its `use_when` sends every builder to the successor. Provenance is
preserved; nobody rebuilds a dead piece by accident.

## The check (machine-checkable)

1. Every store entry: non-empty `name`, non-empty `html`, and an `ai_label` with
   non-empty `purpose`, non-empty `use_when`, and ≥ 1 law.
2. Every law reference resolves on the shelf (Laws 1–16).
3. No duplicate ids, no duplicate names, no duplicate `html` across the store.
4. Every `superseded_by` target exists in the store.
5. Store canonical count == index canonical count
   (`CANONICAL-PIECE-INDEX.json` → `counts.by_status.canonical`).

## Ten exemplars (quoted from the store — the pattern to copy)

**NAYA-BTN-001 — "Black Ground"**
purpose: "A foundation button in the obsidian skin (.naya-btn--foundation-obsidian,
elev-2): a diamond jewel, the title 'BLACK GROUND', and the sub-line 'Obsidian field'."
use_when: "Use when an action needs the dark obsidian foundation treatment — the
ground-state button of the family." laws: Law 2 · Law 3 · Law 11 · Law 13.

**NAYA-HRO-001 — "Reference Hero"**
purpose: "The Reference Hero: a full hero section (.ref-hero) in purple — an 'N' mark,
an eyebrow, an H2 title ('Smart Spaces'), a sub-line, a description, and a Primo purple
action button — with a named motion spec (sheen sweep and mark breathe) in the store."
use_when: "Use as the title block of a page at full presence — the crowned exemplar
every hero is copied from, never restyled." laws: Law 1 · 2 · 4 · 5 · 6 · 10 · 13.

**NAYA-ICO-001 — "Today · dual"**
purpose: "A 'dual' room icon for Today: a 54px diamond tile (rotated square) with a
magenta radial glow, a magenta border, and a white four-point star glyph."
use_when: "Use as the Today room's icon wherever rooms are listed, docked, or picked."
laws: Law 1 · Law 2 · Law 5.

**NAYA-INP-008 — "Reference Well"**
purpose: "The Reference Well: a labeled text input (.ref-well, purple accent) whose box
carries the Smart Factory input recipe (flat obsidian fill, silver-white rim, crisp
inset top shade, white rest glow) and a named focus-travel motion spec in the store."
use_when: "Use for every text entry that matters — this is the crowned exemplar all
inputs are copied from, never restyled." laws: Law 2 · 3 · 4 · 10 · 11.

**NAYA-INP-001 — "Search bar" (the retired form)**
purpose: "RETIRED: the original search bar, superseded by NAYA-INP-008 (Reference
Well). Kept in the store for provenance only."
use_when: "Do not use. Builders reaching for a search field must harvest NAYA-INP-008."
laws: Law 3 · Law 10.

**NAYA-NAV-001 — "Smart tabs"**
purpose: "The Smart Tabs bar: a .smarttabs strip (elev-1) of tab buttons — 'All',
'Start Here', '+ Add' — with the current tab in the .on state."
use_when: "Use as the standard tab navigation of a room or page — this is the Smart
Tabs chrome every smart app shares." laws: Law 2 · Law 11 · Law 14.

**NAYA-ORB-006 — "Truth orb · Verified"**
purpose: "A small truth orb for Verified: an .orb.orb-sm in green (#2fe89e) — the
truth-state orb whose green means a claim is verified."
use_when: "Use beside a claim or item whose state is verified — never as decoration;
the color is the verdict." laws: Law 1 · Law 2 · Law 5.

**NAYA-ROW-001 — "Meta row"**
purpose: "A meta row (.meta-row): three quiet inline facts in one line — 'Today',
'Evidence-based', '3 plays'."
use_when: "Use under a headline when a few facts orient the reader and none of them
deserves its own element." laws: Law 6 · Law 8.

**NAYA-MRK-007 — "Skeleton loading"**
purpose: "A skeleton loading set: stacked .naya-skel placeholder bars (headline, two
text lines, one tall rounded block) shown while real content loads."
use_when: "Use as the honest loading state of a board or card — shape first, content
when it truly arrives." laws: Law 5 · Law 11.

**NAYA-OVL-004 — "Command palette"**
purpose: "A command palette (role=dialog): a search well ('Ask Naya, or jump
somewhere…' with an esc kbd hint) above a listbox of destinations and actions with
numbered hints."
use_when: "Use as the keyboard-first jump-and-act overlay for a whole app."
laws: Law 2 · Law 3 · Law 11.

---

*Doctrine source: FACTORY-CONTRACT-HOME-AUDIT-2026-10-22, step 3 (dual-label the parts)
and its standard for canon. The step-5 shelf work inherits this pattern unchanged.*
