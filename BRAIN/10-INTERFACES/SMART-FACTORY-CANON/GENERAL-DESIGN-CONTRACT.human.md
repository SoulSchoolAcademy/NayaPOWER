> **SUPERSEDED AS A CONTRACT — 2026-10-22.** The canonical design contract is `BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md` (see MANIFEST.md, Canonical Set). This document is retained for provenance; its laws live on as the Factory law shelf. Do not cite this file as the contract.

# THE GENERAL DESIGN CONTRACT
## The Smart Factory — the one contract above every build in NayaNET

*Shawn's directive, 2026-10-21. This is the human version. Shawn checks this first; the machine version is made from it, never instead of it.*

---

## 1. WHAT THIS IS

There is one design contract in NayaNET, and this is it.

It sits **above** every per-build contract. The files in the factory pipeline (`contracts.json`, `business-contract.json`) say what one build contains — a name, a tagline, which sections. This contract says what **everything we design** must be: the laws of depth, light, motion, text, and function that no build, page, room, or component may break, no matter who asked for it or how small it is.

It lives in the **Smart Factory**, where the parts live, so that anyone who comes for parts sees the laws beside them. It binds **every Naya, every human, and every machine** that designs or builds in NayaNET. There are no exceptions for quick jobs, internal pages, or prototypes. If it ships, it obeys.

If you have not read this contract, you are not ready to design here.

---

## 2. THE READ-FIRST PROCESS — THE GATE

Before **any** design work in NayaNET — any page, room, component, polish pass, or fix — the designer does three things, in this order:

1. **Go to the Smart Factory and read this contract.** All of it. It takes five minutes.
2. **Study the exemplar gallery** (Section 4). Look at the reference pieces with your eyes, not just their names. Know what the bullseye looks like before you aim.
3. **Name your harvest in your brief.** Every build brief cites this contract and names the exact exemplars and pieces it will harvest — file, piece ID, section. 

**This is a gate, not advice.** A brief that does not cite the contract and name its exemplars **does not dispatch**. Work that arrives built from invention instead of harvest goes back, however pretty it is. Compose, don't create: the factory already holds the pieces; your job is to assemble them at the standard.

---

## 3. THE LAWS

Each law states the rule, why it exists, and how it is **checked** — because a law that cannot be checked is a wish.

### Law 1 — The Design Language (locked)
**Rule:** Every page walks the spectrum in order — purple `#a06bff` → blue `#3fb8ff` → green `#2fe89e` → gold `#ffbf3d` → orange `#ff9a5a` → red `#ff5e6c` → magenta `#e84fff` → back to purple — each section taking the **next** color, never the same color twice in a row. Elements rest white and ignite in their **own** color on hover or touch, never in someone else's. Elevation is everywhere; nothing is flat. Shapes are horizontal 16:9 rectangles, never squares (circles are for avatars and icons only). Layout is full width — no max-width cage, no wasted black margins. Only real factory pieces. A section **owns** its color: you know where you are by the color you see.
**Why:** The walk creates rhythm you can feel; color-as-identity means a person navigates by light, not by reading.
**Check:** Read the page top to bottom and name each section's color in order — any repeated neighbor, any ignition in a borrowed color, any squared-off panel or side-margin cage is a violation, visible at a glance.

### Law 2 — Dual-Depth Elevation (the master law)
**Rule:** The canonical wording of SN-0808, "Elevated, Always — The Dual-Depth Standard," quoted in full:

> **ELEVATED means: nothing is flat. Every element sits in a layered field of depth — inset highlight on its top edge, inset shadow on its bottom edge, a border that carries its own color's light, an outer glow, and a drop shadow. Direction is grammar: INPUTS ARE WELLS — their depth goes INTO the screen (strong inner shadow at the top of the well, inner light at its bottom edge, the surface sitting below the page plane). ACTIONS ARE BUTTONS — their depth comes OUT of the screen (top highlight, shadow cast down onto the page, glow outward; a physical thing a hand can press). DISPLAYS ARE LIT PANELS — they burn in their own spectrum color with bright white content. The element is alive at rest, not only when touched. This applies to every element, on every page, always — "sometimes elevated" is flat with excuses.**

Every input on every page gets the full well treatment: deep inset well, inset top highlight, inset bottom shadow, a border carrying its accent light, layered outer glow, a drop shadow — **alive at rest, stronger on focus**. One flat element beside elevated work cheapens everything around it, so "most of the page" is not compliance.
**Why:** Depth with direction teaches the hand before the mind reads a word: type into the wells, press what rises.
**Check:** Inspect the element's actual shadow stack. A well must show an inset shadow (depth going in). A button must show a drop shadow cast onto the page (depth coming out). Both must carry a border in their own color's light and an outer glow — at rest, before any interaction. Missing any layer = flat = violation.

### Law 3 — Inputs Are Wells, Actions Are Buttons
**Rule:** Depth has a direction and the direction is never decoration. Anything a person types or chooses into is carved **into** the screen. Anything a person presses rises **out of** the screen toward their hand. Never style an input like a button or a button like an input.
**Why:** In and out are meanings a hand understands instantly; the interface teaches itself.
**Check:** Cover the labels and look at the shapes alone: if you cannot tell what is typeable and what is pressable from depth direction alone, the grammar is broken.

### Law 4 — The Motion Law (the third dimension)
**Rule:** The standard has three dimensions — depth, light, and **motion**. Every interactive element carries considered micro-interactions: **hover life** (the element answers the approach of a hand), **focus travel** (on entry, light moves around the border and wells deepen), **press physics** (an outset button sinks into the screen when pressed and springs back with a precise ease), and **periodic shine sweeps** on hero surfaces. Timing and easing are deliberate and specified by name and number — never the browser default. All motion honors `prefers-reduced-motion`: reduced means a fully lit, fully elevated **static** state, never a dead one.
**Why:** "The boxes light up but they don't move" is a half-finished standard; fine precision design is alive in time as well as in space.
**Check:** The element's motion specs are named in its CSS — durations and easing curves, not defaults — and it passes **the wow test**: a reviewing designer can name *nothing* left to add. If a reviewer can say "they should have done that," it is not done.

### Law 5 — Aliveness Is Colored Light
**Rule:** Depth without light reads dead. Every content area is a living area: real elevation **plus** its own spectrum color burning in borders, glows, and lit panels, with bright white content. Flat floating text on a dark field is a defect wherever it sits. We are active intelligence; we are not dead text.
**Why:** On a black page, shadow alone is just more black — aliveness is light.
**Check:** Squint at the page from arm's length: every board should read as a lit place with its own color present. Any region that reads as gray text floating in darkness fails.

### Law 6 — The Text Law
**Rule:** Text is white or bright silver — never gray, never dimmed, never muted by opacity tricks. Hierarchy is 24px headline / 18px sub-headline / 14px small text, and where Shawn directs a hero bigger, the hero goes bigger (title block presence is part of the design, as on the certificate and the Spaces hero). Room heroes are led by the room's **name**; never invert the hierarchy with a giant tagline over a small name.
**Why:** Dim text is how a premium page quietly becomes a cheap one; hierarchy is how a page speaks clearly.
**Check:** Sample the rendered text colors: anything computing to gray or sitting under an opacity below full on body text is a violation. Measure the sizes; the order 24/18/14 must hold (or the named hero exception).

### Law 7 — Say It Once
**Rule:** The same words never appear in two layers. A name stands as the headline **or** inside a field, never both at once. A title and its description each appear exactly once on any view.
**Why:** Duplicated text is the page stuttering — it tells the person the system doesn't know what it already said.
**Check:** Read the rendered page and list every repeated string. Any repeat that is not a deliberate navigation label is removed.

### Law 8 — Text Earns Its Place
**Rule:** A line of text stays only if it is **necessary** or it **raises conversion**. Everything else is clutter and comes off — including honest-but-useless fine print on ceremonial surfaces. Text is distributed across the composition, never piled in one place.
**Why:** Every line competes with the one action the page exists for; text that doesn't work for its place taxes the lines that do.
**Check:** For each line, name its job in one sentence — necessary, or converting. A line with no job is deleted, and the page is re-read to prove nothing was lost.

### Law 9 — The Name Is Asked Once
**Rule:** A person's name is claimed **once**, at the identity page, at the door. No page, hero, hub, or settings board ever asks for it again. Everywhere else, the system greets by the claimed identity; a settings board **displays** the claimed identity (with log out where it belongs) and offers no name input. Where no identity exists, greet plainly and point to the identity page — never a prompt.
**Why:** Asking twice tells the person the system has no memory; a system with no memory cannot be trusted with anything else either.
**Check:** Grep and click: no name-entry field exists anywhere except the identity page; every greeting resolves from the claimed identity.

### Law 10 — Harvest First: Compose, Don't Create
**Rule:** Every element traces to a factory piece (by NAYA-* ID) or to a named harvest source — exact file and section, verified to exist before the brief is written. When told to "use the Hub's X," the deliverable copies the Hub's X **verbatim** — same HTML structure, same CSS values, same JS behavior; adapting content is allowed, restyling the component is not. A piece's harvest includes **all** its CSS.
**Why:** Invention drifts; the factory is the accumulated proof of what Shawn has already judged elite. Rebuilding a piece that exists is waste wearing a costume.
**Check:** The brief's harvest list is read against the shipped page, element by element. Any element with no traceable source is a violation, however good it looks.

### Law 11 — Function Law
**Rule:** Every button works. Every input is editable, every toggle toggles, every tab navigates. No dead buttons, no "coming soon," no placeholder data dressed as real. **Pretty + useless = not done.**
**Why:** A control that does nothing teaches the person that nothing on the page can be trusted.
**Check:** Click everything, in the live thing — not a screenshot. Every control produces its real result; every empty state is honest about being empty.

### Law 12 — Install Lives at the Bottom
**Rule:** Every page can be installed as an app, and the install offer sits at the **bottom** of the page — quiet, elegant, never at the top, never a shouting banner, never a veil that interrupts.
**Why:** Install is an invitation at the end of a good experience, not a toll gate at the door.
**Check:** Scroll the page: install appears once, at the bottom; nothing pops over the person's first view of the page.

### Law 13 — The Obsidian North Star
**Rule:** The aesthetic north is **beautiful glossy obsidian black** — like a glossy city at night — with awe-inspiring contrast, clarity, and quality. Every page should stop a person for a second. **Everything we do must be elite or we don't do it.** Ceremonial surfaces carry the discipline in its purest form (the certificate: true deep black, royal purple, white, and silver — the family metal is silver — real faceted artwork, restraint in text, richness in stone and depth).
**Why:** The standard is not "good for a web page"; it is the most elite system anybody has used.
**Check:** The inspector's eye at arm's length: does the surface read as polished stone with light in it — or as a dark web page? Only the first passes.

### Law 14 — Standard Chrome (the room DNA)
**Rule:** Smart Tabs are the standard navigation for all of NayaNET — bottom bar by default, scrolling and keeping position, users customize. Rooms are real smart apps sharing the system's DNA, built to the Smart App Standard (Smart Tabs, plus-button navigation, honest empty states, live data). That standard governs what a finished room is; this contract governs how everything looks and behaves — where they overlap, both hold.
**Why:** One navigation grammar everywhere means nobody relearns the building on every floor.
**Check:** The room passes the Smart App Standard's "finished" test and this contract's laws — both, not either.

### Law 15 — The Inspector Rule
**Rule:** Naya is the inspector, and so is every Naya who reads this. Whoever sees a board, input, button, or page that is flat, dead, dim, unclear, or below this contract **fixes it on sight** — first the fix, then the word to Shawn. Reporting a problem without fixing it is being part of the problem. It should be clear as day what any page, button, or input does; if it isn't, that is the defect.
**Why:** A standard nobody enforces at the moment of seeing is decoration.
**Check:** Findings are measured by what got fixed and verified, not by what got noted. An inspection that produces only a report has failed this law.

### Law 16 — The Scorecard Law
**Rule:** Everything is scored. Score it, state plainly why it is not a 10, fix that, re-score — **three passes**. Results are presented **with** their scorecard story (starting score → passes → final score → what changed), never bare. Work below ~9.5 does not ship to Shawn; it goes back for another pass first. His eye scores the feeling and the standard; our scores cover the checklist — his supersede.
**Why:** Unscored work is unproven work, and unproven work is how reservoirs of almost-done fill up.
**Check:** The scorecard exists, names the gap at each pass, and the final number is honest — verified against the live thing, not the builder's hope.

---

## 4. THE EXEMPLARS — THE BULLSEYE, IN PIECES

These are the reference pieces every design starts from. The rule for all of them is the same:

> **Copy the piece's code — all of it, HTML and CSS. Adapt the content. Never restyle the piece.**

The gallery's current state is audited in `EXEMPLAR-GAP-REPORT.md` beside this contract; where a verdict says a reference piece is still to be built, the interim harvest source named there is what you copy until the exemplar lands.

**The Reference Well (Input).** Demonstrates the full dual-depth well: depth going into the screen, border carrying its accent light, alive at rest, and **focus travel** — light moving around the border as the well deepens on entry. Every input in NayaNET is this well wearing different words.

**The Reference Button (Action).** Demonstrates the full outset stack: depth coming out of the screen, its own color burning, shine sweeping across it, and **press physics** — it sinks when pressed and springs back on a named ease. If a designer presses it and feels nothing, it is not the reference button. Current holder: the living-button family (NAYA-BTN-009) — see the audit.

**The Reference Select.** Demonstrates choosing as a physical act: a well that opens a lit panel, options that ignite in their own color as you pass over them, a chosen value that sits like a lit display. *(To be built — see the audit. Today the factory holds no elite select; that gap is named, not hidden.)*

**The Reference Section / Board.** Demonstrates how a content area lives: glossy obsidian field, border in the section's own spectrum color, layered depth, bright white text, its action riding at its head. Current holder: the feature board (NAYA-BRD-001) — see the audit for its one text repair.

**The Reference Hero.** Demonstrates the title block of a page at full presence: the dimensional glossy-obsidian field with its light source inside it, the mark, the headline at hero size, the spectrum ignition, shine sweeping the surface. *(To be built as a harvestable piece — see the audit. Today heroes exist only embedded in finished pages.)*

---

## 5. WHEN THE CONTRACT AND A REQUEST DISAGREE

**Shawn's word in the moment wins.** He is the director; the contract serves his judgment, never the reverse.

Then, the same day, one of two things happens: the exception is written into this contract as law (because it was a better rule), or it is recorded as a one-time exception with its reason. What never happens is a silent drift — a page that quietly breaks a law and teaches the next builder that the law is soft. Laws change in the open, in this document, the day they change.

The same holds for any Naya's finding: if the contract is wrong, say so plainly, bring the evidence, and the contract is updated. Until it is updated, it is obeyed.

---

*Sources read for this contract: SN-0808 "Elevated, Always" (`~/workspace/elevation-standard/SN-0808.md`) — the canonical paragraph in Law 2 is quoted verbatim; `~/AGENTS.md` — the locked Nayanet Design Language and the harvest-first law; `~/workspace/room-rollout/SMART-APP-STANDARD.md` — room DNA, Smart Tabs, install placement, hero hierarchy, aliveness, the Completion Doctrine; `~/MEMORY.md`, entries of 2026-10-21 — the input elevation law, the inspector directive, the dual-depth grammar and text discipline, the name-asked-once ruling, the aesthetic north star, the certificate discipline, the motion law; `~/workspace/factory-pipeline/contracts.json` + `business-contract.json` — the per-build contracts this contract sits above; `~/workspace/personal-app/pieces.json` + `factory.css` — the piece set and materials the exemplars are judged from.*

*Companion document: `EXEMPLAR-GAP-REPORT.md` — the audit of the gallery this contract points at.*
