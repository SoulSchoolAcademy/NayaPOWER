# DESIGN LAWS — as data (Shawn's laws, encoded)

These are not suggestions. `tools/design_gate.py` enforces the structural ones
as machine law — violations fail the build. The rest are enforced by Shawn's eye,
which is the final compiler.

Sources: the 2026-10-09 canon intake (29 PDFs) — the Shawn-ratified interface
codex `naya-100-laws-elite-interfaces.pdf`, `VISION-LAWS.pdf`, the specimen card,
the Design Constitution, the mission charge, the Oscar standard, the App Factory
(proposals, unratified — marked), the superbrain architecture. Conflicts resolved
per `CONFLICTS.md`: black-first wins over the Playbook's white canvas; spectrum
by position wins over psychology mapping; 9.5 is a factory-exit proposal, 9.0
the show-Shawn floor.

## Ground (machine-enforced)

1. **Black root.** `html` and `body` backgrounds are deep black (`#050507` family).
   No path for white to leak in: `<meta name="color-scheme" content="dark">` required.
2. **Never light mode.** No white/light page or panel backgrounds. Ever.
3. **Self-contained delivery.** One HTML file: all CSS/JS inlined, no external
   stylesheet or script references. Verify from an empty folder.
4. **No freestyle components.** Every component class must exist in
   `smart-blocks/manifest.json`. If no block fits, file the gap — don't invent.
5. **Mobile is the primary canvas.** `<meta name="viewport"
   content="width=device-width, initial-scale=1">` required. Design, screenshot,
   and score the phone view first. Tap mirrors hover. 44px touch floor.
   No horizontal scroll, ever.

## Craft (eye-enforced, gate-warned)

6. **LAW ZERO — Readability Supremacy.** No effect may ever make anything harder
   to read. Effect vs readability: the effect dies. The tiebreaker for every
   craft dispute.
7. **Text is white 99%.** Hierarchy comes from size (24/18/14), never color.
8. **Buttons: silver-white at rest, identity color on interaction.** Black heart,
   white voice, visible skin. Never colored text on buttons.
9. **Spectrum by position, never by category.** Color is assigned by reading
   order; theming by category clumps color and is a serious violation.
   Once a meaning is assigned to a color, it never changes between instruments.
10. **Color has three jobs** — chrome (actions), text (white), theme (one spectrum
    accent per item). Never cross them. Spectrum flows purple → blue → green →
    yellow → gold → orange → red → magenta.
11. **Materials have names, and only names.** Obsidian, Frosted Obsidian, Jewel,
    Paper White, Silver. Inventing a new material per page is forbidden.
12. **The 5-layer shadow formula** on every elevated surface: inset top highlight,
    inset bottom shade, tight glow, wide aura, deep drop shadow.
13. **The grayscale test.** Strip the color: hierarchy, elevation, and readability
    must survive. If the page only works in color, the depth system is fake.
14. **Motion encodes information.** Breathe = alive, shimmer = light, press = physical.
    No decoration. No spinning/pulsing things that mean nothing.
15. **Light moves before words (V-4).** On state change, motion precedes text
    updates. The output is an event, not a render.
16. **No number on screen is static text (V-3).** Every displayed number breathes,
    synced to the heartbeat. "Living" is a per-element requirement, not a vibe.
17. **One universal ±9 instrument (V-11).** Needle of light, pins past ±9 with
    logarithmic comet trails, burns white-hot past 2× range. Never a second
    gauge design.
18. **Every data instrument names what it measures.** A chart that calculates
    nothing is a screensaver.
19. **Never lie visually.** Animation never pretends success. Loading states
    indicate real work. The interface never pretends to capabilities it lacks.
    Glow ≠ intelligence.
20. **Claim labeling.** Every design claim carries its evidence status: design
    preference, observed problem, verified improvement, established universal
    rule. Never present a preference as a rule.
21. **Full state matrix.** Resting, hover, focus, pressed, disabled, loading,
    success. An unspecified state is an unshipped state.
22. **Copy is invitation, never documentation.** Score it before shipping.
23. **Icons are drawn vector geometry**, readable at 16px. No shrunk photos.
24. **Affordances tell the truth.** A chevron promises somewhere; a plus promises add.
25. **One hero CTA per page. One nav system per page. One media moment per view.**
26. **Build intimacy, not addiction.** No dark patterns, no manufactured
    dependency, no engagement optimized at the expense of value.
27. **"Feel like magic — run like math."** The one-line design constitution.

## Delivery (machine-enforced)

28. **The Usefulness Gate.** If it's not useful, it can never be used. If you
    wouldn't give it to the world, don't give it to Shawn — don't give it to anybody.
    Silence beats garbage.
29. **The Binary Gate.** Useful + valuable → YES. Useless / no value → NO.
    On-brand design → YES. Off-brand → NO. Accurate → YES. Not accurate → NO.
    One NO anywhere = it does not ship. And never waste time, money, or energy
    sending anyone anything useless, valueless, or misaligned with their intent.
29. **No manufactured numbers.** Every number carries provenance or it doesn't ship.
30. **MERGED ≠ ENFORCED.** A guard merged but not wired into the canonical
    promotion/audit seam does not count. Neither does a law merged but not enforced.
31. **Copy the approved code verbatim (SN-0735).** The approved block's exact code
    becomes the block. Paraphrasing from memory reintroduces the flatness Shawn
    rejected.
32. **Never ship the same flaw twice (SN-0734).** If a rebuild goes flatter than
    what Shawn loved, revert to the loved version verbatim. No-ego reversion.
33. **Dogfood as proof.** A design document drawn entirely from the Smart Blocks
    library proves the library works. Every deliverable demonstrates its own tools.
34. **Laws ship as a machine-readable contract.** A law living only in chat will
    be broken by the next pipeline. Encode it or lose it.
35. **Verify through his eyes.** Screenshot the delivered artifact the way he'll open it.
    His experience is the test environment.

## Meta (how the canon itself works)

- **Distilled ≠ ratified.** Intake is CANDIDATE until it survives review. Never
  install an unreviewed proposal as law — including from this intake.
- **If Shawn must re-teach a law, the law or the block is incomplete (SN-0731).**
  Fix the system, not the student. Instruction-repetition is a system defect.
- **Corrections compound the same day.** Every Shawn correction is distilled
  into the document or the library within the same session.
- **Specimen governance.** One specimen per feeling; the specimen governs by
  feeling — "make everything feel like THIS." Rebuild, never patch.
- **Vision-to-Code Protocol.** Shawn's words → sharpened → atoms → pass/fail →
  lives in the specimen. Every vision law must be testable.
