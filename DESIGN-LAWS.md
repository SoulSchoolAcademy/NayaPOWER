# DESIGN LAWS — as data (Shawn's laws, encoded)

These are not suggestions. `tools/design_gate.py` enforces the structural ones
as machine law — violations fail the build. The rest are enforced by Shawn's eye,
which is the final compiler.

## Ground (machine-enforced)

1. **Black root.** `html` and `body` backgrounds are deep black (`#050507` family).
   No path for white to leak in: `<meta name="color-scheme" content="dark">` required.
2. **Never light mode.** No white/light page or panel backgrounds. Ever.
3. **Self-contained delivery.** One HTML file: all CSS/JS inlined, no external
   stylesheet or script references. Verify from an empty folder.
4. **No freestyle components.** Every component class must exist in
   `smart-blocks/manifest.json`. If no block fits, file the gap — don't invent.

## Craft (eye-enforced, gate-warned)

5. **Text is white 99%.** Hierarchy comes from size (24/18/14), never color.
6. **Buttons: silver-white at rest, identity color on interaction.** Black heart,
   white voice, visible skin. Never colored text on buttons.
7. **Color has three jobs** — chrome (actions), text (white), theme (one spectrum
   accent per item). Never cross them. Spectrum flows purple → blue → green →
   yellow → gold → orange → red → magenta.
8. **The 5-layer shadow formula** on every elevated surface: inset top highlight,
   inset bottom shade, tight glow, wide aura, deep drop shadow.
9. **Motion encodes information.** Breathe = alive, shimmer = light, press = physical.
   No decoration. No spinning/pulsing things that mean nothing.
10. **Every data instrument names what it measures.** A chart that calculates
    nothing is a screensaver.
11. **Copy is invitation, never documentation.** Score it before shipping.
12. **Icons are drawn vector geometry**, readable at 16px. No shrunk photos.
13. **Affordances tell the truth.** A chevron promises somewhere; a plus promises add.
14. **One hero CTA per page. One nav system per page. One media moment per view.**

## Delivery (machine-enforced)

15. **The Usefulness Gate.** If it's not useful, it can never be used. If you
    wouldn't give it to the world, don't give it to Shawn — don't give it to anybody.
    Silence beats garbage.
16. **No manufactured numbers.** Every number carries provenance or it doesn't ship.
17. **Verify through his eyes.** Screenshot the delivered artifact the way he'll open it.
    His experience is the test environment.
