# Smart Blocks Registry — the ONE unified library (v1.0, 2026-10-09)

Shawn's directive: keep all the 9s and 9.5s, don't cut good work just to pick one, allow multiple versions. The DROP list is law.

## Status legend
- **ported** — verbatim CSS from best source, restraint fixes applied where the inventory required
- **kept-variant** — a second earned version of a component (Shawn: allow multiple versions)
- **built-new** — missing everywhere; built from scratch in the canonical language
- **recovered** — asset was missing from the DESIGN package; recovered from repo
- **dropped** — in the sources but failed the restraint/usefulness gate; reason given

---

## 01 · Buttons

| Block | Class | Source | Status |
|---|---|---|---|
| Canonical button | `.naya-btn` | N2 Building Blocks | ported (recipe; hardcoded #8d63f5 → `var(--purple)`) |
| Signature variants | `.naya-btn.lead/.machine/.prism/.proximity` (+.streak/.compact/.small) | N2 Building Blocks | kept-variant |
| Icon buttons | `.naya-btn.icon/.micro/.portal` | N2 Building Blocks | ported |
| 40 SVG icon glyphs | `#i-spark`…`#i-globe` | N2 Building Blocks | ported (`icons.svg`) |
| Ghost button | `.naya-btn--ghost` | N4 Element Set | ported |
| Danger button | `.naya-btn--danger` | N4 Element Set | ported |
| Living button | `.lv-btn` | N5 Epic Elements | ported — **tamed**: idle colored `::after` layer removed (opacity 0 at rest; wakes on hover/proximity only) |
| Hero CTA | `.living-btn` | N5 Buttons | ported — **tamed**: `.btn-glow` opacity .55→0 at rest (ignites on hover only); idle breath kept (colorless) |
| Split button | `.naya-btn.split` + `.split-orb` | N2 Building Blocks | ported |
| Segmented control | `.segmented` | N2 Building Blocks | ported |
| Toggle switch | `.naya-toggle` | N2 Building Blocks | ported |
| Room micro-controls | `.like-pill/.act-chip/.day-dot/.send-cta/.mic-btn/.fab` | N4 Button Set (background file) | promoted into library |

## 02 · Inputs

| Block | Class | Source | Status |
|---|---|---|---|
| Recessed field | `.recessed-field` | N2 Building Blocks | ported |
| Search field | `.search-field` | N2 Building Blocks | ported (wired to ⌘K palette on this page) |
| Orbiting login | `.login-card/.login-orbit` | N2 Building Blocks | ported |
| Jeweled checkbox | `.naya-check` | — | **built-new** (N4's `.gate` turned out to be display-only jeweled bullets, no checkbox — built the real one) |

## 03 · Navigation

| Block | Class | Source | Status |
|---|---|---|---|
| Top nav bar | `.nav/.nav-orb` | N2 Building Blocks | ported |
| Pill tabs | `.smarttabs/.smarttab` | N2 Building Blocks | ported (restrained; this is the canonical SmartTabs styling) |
| Favorites ribbon | `.sn-row` + `lego/smart-tabs.js` | N5 Epic (JS behavior) | **recovered** — JS rescued from `naya-ultimate/lego/smart-tabs.js`; emoji replaced with vector glyphs; CSS restyled in N2 pill language |
| App room nav | `.app-nav` | N2 Building Blocks | ported |
| Anchor TOC pills | `.toc a` | N5 Epic Elements | ported |

## 04 · Cards

| Block | Class | Source | Status |
|---|---|---|---|
| Elevated board | `.elevated-board/.board-spine/.board-corner` | N2 Building Blocks | ported |
| Spec board | `.board` | N4 Element Set | kept-variant (one spectrum color per board, corner jewel) |
| Nested cards | `.nestcard` | N4 Element Set | ported |
| Truth cards + orbs | `.truthgrid/.truth/.torb` | N4 Element Set | ported |
| Law cards | `.lawcard` | N4 Element Set | ported |
| Three-tongue law cards | `.tongue` | N4 Element Set | ported |
| Type scale cards | `.typecard` | N4 Element Set | ported |
| Metric trio | `.metric` | N2 Building Blocks | ported |
| Job cards | `.job/.jobs` | N4 Element Set | kept-variant (color-role stat cards; `.jobs` grid recovered from source) |
| World tiles | `.layer/.layer-grid` | N5 Epic Elements | ported |

## 05 · Data

| Block | Class | Source | Status |
|---|---|---|---|
| Meaning spheres | `.sphere` | N2 Building Blocks | ported — **restrained**: white-hot centers tamed (`.92→.55`, saturated ring softened) |
| Self-scorecard | `.scorecard/.score-row/.verdict` | N2 Design Elements | ported |
| Law library | `.law-group` | N2 Building Blocks | ported |
| Data table specimen | `.data-table/.trow/.status-dot` | N2 Building Blocks | ported (labeled NO LIVE DATA, as the source demands) |
| Chart specimen | `.chart-mini` | N2 Building Blocks | ported (anatomy specimen — shown in Data via table specimen; CSS kept in file) |

## 06 · Overlays

| Block | Class | Source | Status |
|---|---|---|---|
| Toast system | `NayaBlocks.toast()` + `.naya-toast` | N2 Building Blocks (behavior) | ported (JS canonical utility; CSS built in canonical language) |
| Mini modal | `.modal-mini/.modal-gem` | N2 Building Blocks | ported |
| Share sheet | `.smart-link/.share-actions/.source-rank` | N2 Building Blocks | ported |

## 07 · Media

| Block | Class | Source | Status |
|---|---|---|---|
| Media player | `.media-player` | N2 Building Blocks | ported |
| Hero vessel | `.vessel` | N2 Building Blocks | ported |

## 08 · Specialty

| Block | Class | Source | Status |
|---|---|---|---|
| Orb system | `.orb` + 8 variants | N5 Jewel Library | ported (canonical — the most restrained orb source) |
| Mini-orb | `.mini-orb` | N5 Jewel Library | ported |
| Gem bullets | `.gem-bullet` | N5 Jewel Library | ported |
| Spectrum bar | `.spectrum-bar` | N5 Epic Elements | ported (thin, disciplined 10px strip) |
| Spectrum swatches | token chips | — | built-new (from token hues; N4's ×5 chip set was display-only) |
| Interaction physics | `.physics-row` | N2 Building Blocks | ported |
| Ship-gate checklist | `.gate` | N4 Element Set | ported (restrained N4 version) |
| Code + copy | `pre.code/.code-head/.copy-btn` | N5 Epic Elements | ported |
| Section chrome | page sections | N5 Jewel Library (`.lego-section` language) | ported (kicker + voice title pattern) |
| Rule boards | `.rule-board` | N5 Epic Elements | ported |
| Anti-pattern drift demos | `.driftgrid/.drift` | N4 Element Set | ported |
| Ambient field | page `::before` | N5 Epic Elements | ported (three quiet radial washes, 24s breathe) |

## 09 · New — P0 (built-new, all)

| Block | Class | Notes |
|---|---|---|
| Page shell / app layout | `.naya-shell` | rail + sticky head + content grid + footer slot |
| ⌘K command palette | `NayaBlocks.wirePalette()` | opens on ⌘K/Ctrl-K; jumps to any library section |
| Live sortable table | `table.naya-table[data-sortable]` | click headers; type-aware |
| Empty state | `.naya-state` | invitation copy, one action |
| Error state | `.naya-state.is-error` | honest, keeps the user's words |
| Loading state | `.naya-spinner` | quiet orbital spinner = "working" |
| Skeleton loading | `.naya-skel` | jewel-aesthetic ghosts |
| Avatars | `.naya-avatar/.naya-avatar-stack` | 28/40/56px, one hue per person |
| Badges | `.naya-badge` | verified/claim/demo/danger/quiet |
| Notification drawer | `.naya-drawer` | live open/close demo |
| Real footer | `.naya-footer` | brand + map + quiet line |

## Shared JS

| File | Provides |
|---|---|
| `blocks/naya-blocks.js` | `toast()`, `copyText()`, copy-HTML delegation, tab wiring, table sort, `wirePalette()` |
| `lego/smart-tabs.js` | Recovered SmartTabs favorites ribbon (v9.0.0, vector glyphs) |

## Dropped (the DROP list — law)

| Item | Source | Why |
|---|---|---|
| Naya 2 "Ultimate Design System" (whole file) | DESIGN/ | byte-dupe of Building Blocks (3 CSS lines differ); kept Building Blocks' deeper black |
| Epic "05 Orbs" section | N5 Epic Elements | near-identical CSS dupe of Jewel orbs |
| `.board-mix` | N5 Epic Elements | 7px neon spine — gaudy |
| Epic gate widget | N5 Epic Elements | candy gradient + pulsing neon — gaudy |
| `.action-library` (as-is) | N2 Building Blocks | gaudy multi-color overload; needs redesign before porting |
| `.orbit-btn` | N2 Building Blocks | spinning ring — motion without meaning |
| N4 `smtab.active` | N4 Element Set | 26px+56px double glow — gaudy |
| N4 Lego `.cx-btn:hover` | N4 Lego Blocks | 42px hover glow — gaudy |
| N2 Elements `.truth` | N2 Design Elements | dead code (defined, zero instances) |
| Naya 4 10-hue bar | N4 Lego Blocks | borderline rainbow — kept Epic's disciplined 8-span bar instead |
| `.sw` / `.jewel` / `.jewelrow` dupes | various | gem-bullet (Jewel N5) is canonical |
| N2 Elements `.card`, Epic `.law-card` | various | lawcard (N4) is canonical |
| Orb context cards | N5 Jewel Library | dupe pattern |

## Tokens

`tokens/tokens.css` — merged superset, no conflicts: Button-Law base (14-hue spectrum, 5-layer depth, motion, shape, type) + Epic/Jewel `:root` (field/obsidian/raise/card, soul `#a06bff`, per-hue `-rgb` twins, verified/claim/demo/danger, lift/ring, radii, type scale) + N2 materials (`--surface`, `--mat-0…3`, `--shadow-soft`, `--page`).
