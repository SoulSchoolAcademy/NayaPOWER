# 05 — Visual + Responsive Map

## 1. Visual north star

The Hub is intended to feel like a premium intelligence instrument, not a generic SaaS dashboard.

**Palette:** obsidian/black base, white typography, purple intelligence accent, sapphire/green/gold semantic accents.

**Current source tokens:**
- background `#050507`
- panel `#0b0b10`
- ink `#fff`
- muted `#a9a4b1`
- green `#55e39a`
- sapphire `#55b9ee`
- indigo `#6675ff`
- magenta `#d86cff`
- gold `#e8c766`

## 2. Typography

- Font stack: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif.
- Strong display headlines use large clamp-based sizes and tight negative tracking.
- Labels use very small uppercase text with high font weight and letter spacing.
- Body text uses approximately 14–18px depending on component/layer.
- Intelligence blocks use large editorial titles and generous line-height.

## 3. Desktop shell geometry

### Sidebar
- Width: 250px.
- Sticky/fixed visual position.
- Full viewport height.
- Dark translucent surface.
- Right border and backdrop blur.

### Main
- Fluid width.
- Base horizontal padding: 40px.
- Bottom padding: 100px to account for feature-report bar.

### Topbar
- Height: 74px.
- Sticky top.
- Border bottom.
- Translucent black + backdrop blur.

## 4. Navigation styling

Sidebar buttons:
- minimum height 46px
- 14px radius
- subtle transparent border
- hover lift and shadow
- active state uses dark purple gradient, magenta border/glow and right-side active indicator

Mobile buttons:
- fixed five-item bar
- 64px height
- rounded outer container
- subtle translucent black surface
- active item receives a light surface highlight

## 5. Ecosystem link strip

- Sticky beneath topbar.
- Horizontal scrolling.
- Each link is a compact rounded button-like anchor.
- Purple default border; sapphire/green/purple/gold semantic accents by position.
- Hover lifts 2px and increases border/glow.
- No wrapping into multiple rows on narrow widths.

## 6. Feature Reports strip

Desktop:
- fixed to bottom.
- starts after 250px sidebar.
- translucent black.
- top border.
- horizontal scroll.

Mobile:
- full width.
- bottom offset above mobile nav.
- horizontal scroll.
- compact report buttons.

## 7. Home visual hierarchy

The current source has several historical layers that hide/rewrite one another. The rebuild should produce one hierarchy:

1. current-state orientation
2. search / Ask Naya
3. intelligence feed header
4. primary Intelligent Blocks
5. compounding/next-action context

The old oversized hero should not compete with the intelligence itself.

## 8. Intelligent Block visual specification

The current renderer defines the strongest usable foundation:

- vertical stack
- full-width block inside feed
- 30px-ish corner radius desktop
- dark layered gradients
- thin luminous border
- deep shadow
- vertical intelligence spine
- colored node/dot for block identity
- strong editorial heading
- readable long-form body
- perspective sections stacked vertically
- semantic accent colors

### Spine
- 1px luminous vertical line.
- Purple at upper/mid sections.
- transitions toward sapphire/gold near lower sections.
- node/dot aligns with each block.

### Block surface
- black/obsidian base.
- subtle radial color field.
- inset highlight.
- large external shadow.
- no generic white dashboard card appearance.

### Typography
- title: approximately 29–47px desktop depending on viewport.
- body: approximately 17–18px in the core feed renderer.
- perspective labels: tiny uppercase tracking.

### Interaction
- hover lifts block a few pixels.
- border/glow strengthens using block semantic tone.
- reduced-motion mode disables transitions/animation.

## 9. Perspective visual sequence

Current foundation:

1. Human
2. Naya
3. Machine
4. Intelligent Feed

Target richer board architecture:

**WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION**

The rebuild should make these layers feel like a single intelligence composition rather than independent cards.

## 10. Smart Notes visual system

- Dark memory cards.
- Strong timestamp/type header.
- Original human note is the visual source of truth.
- Perspective tabs are compact pills.
- Machine metadata uses subdued text.
- Highlight/report surfaces use green/gold truth states.

## 11. Search visual system

Current enhanced search:
- large 60–68px input.
- 18–19px radius.
- purple border/glow.
- keyboard hint `Ctrl / ⌘ K` in one implementation.
- `TALK TO NAYA` button in another implementation.

Rebuild rule: combine these into one search component rather than layering two search implementations.

## 12. Status semantics

### Good / verified
- green.
- explicit VERIFIED language.

### Pending / unknown
- muted neutral.
- explicit PENDING / NOT VERIFIED language.

### Blocked
- gold.
- explicit blocked boundary.

### Intelligence emphasis
- purple/magenta.

### Machine/evidence
- gold or neutral depending on truth state.

## 13. Buttons

Base button:
- minimum height 48px.
- 14px radius.
- dark gradient.
- 1–2px border depending on refinement layer.
- inset highlight.
- deep shadow.
- uppercase, high-weight, compact typography.
- hover lift.

Small button:
- 39–42px height.
- 8px-ish type.

Button semantic classes:
- green = verified/persistence.
- blue = report/source.
- purple = intelligence/action.
- gold = caution/feature/evidence.

## 14. Inputs

- dark near-black background.
- thin light border.
- 13–19px radius.
- white text.
- visible focus border/glow.
- generous padding.

## 15. Modal surfaces

- fixed full-screen dark translucent backdrop.
- backdrop blur.
- centered large rounded dialog.
- purple border/glow.
- scrollable within viewport.
- explicit close/cancel.

## 16. Desktop/mobile breakpoint contract

### > 1100px
- full sidebar.
- full-width main feed.
- large typography.
- multi-column informational surfaces allowed outside the main feed.

### 901–1100px
- desktop sidebar still present.
- grid layouts compress.
- flow components reduce columns.

### ≤ 900px
- sidebar hidden.
- mobile nav shown.
- topbar 64px.
- hero stacks if present.
- mail workspace becomes single column.
- metrics become 2 columns.
- grid2 becomes 1 column.
- feed block margins and padding shrink.

### ≤ 760px
- intelligence perspectives collapse toward one column.
- search remains large but compact.
- action buttons become flexible rows.
- feed block title remains large but fits with favorite/control area.

### ≤ 520px
- smallest card radius reduction.
- report grid becomes one column.
- perspective cards become one column.
- main horizontal padding becomes approximately 12px.

## 17. Accessibility requirements

- All actionable elements are buttons or anchors, not click-only decorative divs.
- Focus-visible states must be visually obvious.
- Reduced-motion preference must be honored.
- Labels and aria labels must identify icon-only controls.
- Color cannot be the only truth-state indicator; use words such as VERIFIED, BLOCKED, PENDING.
- Search and modal controls must be keyboard reachable.

## 18. Visual prohibitions for rebuild

- No generic SaaS dashboard look.
- No competing right sidebar.
- No random horizontal/two-column feed boards.
- No code/debug artifacts visible in the intelligence feed.
- No fake data presented as live.
- No rainbow palette.
- No gratuitous glassmorphism.
- No duplicate search bars.
- No duplicate feed renderers.
- No visual element whose click behavior is undefined.
