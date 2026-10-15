# DESIGN ACTIVATION — in plain words

*For Shawn — the design entry sequence: load the laws, load the catalog, look at elite, compose, check.*

You do not design from scratch. You take the pieces and put them together beautifully. This is the design-specific sequence to complete **after** the general activation and **before** writing a single line of CSS. Skip it and you'll produce the flat-button garbage Shawn has corrected a hundred times — that pattern is now a law violation, not a mistake.

The sequence is five steps: (1) **Load the 10 load-bearing laws** from source (DESIGN-LAWS.md — Naya 5's encoding — is the full text), and name each one back before proceeding; (2) **Load the block catalog** — the official Naya Design vocabulary, 91 proven blocks across 22 categories, extracted verbatim from his approved designs — and for your task name the candidate blocks *before* writing code (if no block fits a component you need, file the gap honestly — never silently freestyle); (3) **Look at what elite looks like** — open the rendered specimen of each block, the gallery for the full set; your output must be visually indistinguishable in quality from those specimens; (4) **Compose, don't create** — assemble the page from official blocks first, custom CSS only for glue, custom components only when no block exists (and that gap gets filed so the library grows instead of the page drifting); (5) **Pre-delivery check** — the six-item checklist: every component traces to a block (or a filed gap), black ground, white text, hierarchy by size, Law-4 buttons, Law-5 purple, Law-6 accents, no number without provenance, verified the way he'll open it, passes the Usefulness Gate.

The 10 laws, compressed to what they demand: black ground (`#050507` family, no white leaking in); white text 99% of the time with hierarchy by size (24px headline / 18px body / 14px detail — never gray or colored text); no freestyle components — every class exists in the block manifest; buttons are black at heart and white in voice (black base, purple edge glow at rest, lighting up white on interaction — never colored text on buttons); purple is accent and glow, never a solid fill; one spectrum accent per item (magenta → purple → blue → green → gold) with never-crossed color jobs; self-contained delivery (one file, CSS/JS inlined, no external refs, verified from an empty folder); no number without provenance; verify through his eyes (screenshot the way he'll experience it); the Usefulness Gate — if it's not useful it can never be used, silence beats garbage.

And one law for after delivery: when he corrects your design work, the activation failed — you worked without the laws loaded or the catalog open. Write the new law down that hour. The next activation carries it.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/00-ACTIVATION/DESIGN-ACTIVATION.md`
- Paired tongues: `DESIGN-ACTIVATION.ai.md` · `design-activation.machine.json`
