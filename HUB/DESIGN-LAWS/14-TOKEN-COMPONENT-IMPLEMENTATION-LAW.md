# 🧬 Token & Component Implementation Law V1

## 1. Prime law

Production craft must be reusable.

If every component hand-tunes its own color, radius, shadow, spacing and motion, NayaNET will drift.

Use tokens for shared physical laws.

Use component variants for intentional differences.

## 2. Required token families

At minimum define:

### Foundation
- canvas / obsidian levels;
- surface levels;
- primary/secondary text;
- hairline/edge;
- overlay.

### Spectrum
- purple;
- indigo;
- sapphire;
- teal;
- emerald;
- lime;
- yellow;
- gold;
- orange;
- rich orange;
- red;
- magenta.

### Typography
- font family;
- body sizes;
- label sizes;
- heading scale;
- line heights;
- weights;
- tracking.

### Spacing
Use a compact rational scale, e.g.:
`4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64`

Do not create 37 unrelated spacing values.

### Radius
Define a small family:
- tight;
- control;
- board;
- portal;
- pill.

### Elevation
Map E0–E5 from Component Physics to reusable shadow/material recipes.

### Border
- subtle;
- interactive;
- active;
- focus;
- error.

### Motion
- micro duration;
- standard duration;
- context duration;
- signature easing;
- reduced-motion replacements.

### Focus
One coherent focus system across buttons, inputs, boards and controls.

## 3. Room theming

A room exposes semantic variables such as:

`--room-accent`
`--room-accent-rgb`
`--room-glow`
`--room-edge`
`--room-field`

Components consume these variables.

Do not hard-code room colors inside every button.

## 4. Component variants

A component may vary through declared variants, e.g.:

`PowerButton(intent="primary" | "secondary" | "quiet" | "destructive")`

`IntelligenceBoard(theme, state, density)`

`Glyph(name, state, size, theme)`

Do not fork components merely to make one screen look different.

## 5. CSS/material discipline

Preferred:
- tokenized CSS variables;
- reusable classes/components;
- local composition;
- documented overrides.

Avoid:
- large inline style piles;
- repeated magic hex values;
- repeated box-shadow strings;
- one-off z-index escalation;
- global selectors repairing old selectors.

## 6. Z-index law

Define layers:
- base;
- rail/topbar;
- elevated board;
- popover;
- dialog;
- critical system overlay.

Never solve stacking bugs by increasing z-index randomly.

## 7. Focus token

Focus must be visible against all room themes.

Use:
- neutral high-contrast outer ring;
- optional semantic inner glow.

Do not use only the room color if contrast may fail.

## 8. Dark material levels

Do not use one black everywhere.

Create subtle depth through controlled values such as:
- canvas;
- recessed;
- surface;
- elevated;
- active.

Difference should be visible but restrained.

## 9. Testability

Every production component should be testable in isolation with:
- themes;
- states;
- long labels;
- translated/expanded text;
- keyboard focus;
- reduced motion;
- mobile width;
- high zoom.

Build a component gallery/story surface if the framework supports it.

## 10. Acceptance

The token system succeeds when:
- changing one semantic token updates all applicable components coherently;
- no room needs a parallel mini-design system;
- visual drift is easy to detect;
- components remain expressive without ad-hoc styling;
- a new builder can create a new room without inventing new physics.
