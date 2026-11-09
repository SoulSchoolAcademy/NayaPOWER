# DESIGN BRIEF TEMPLATE — the ONLY template for design work
**Shawn's order, 2026-11-08 16:37Z — LOCK-IN-10-CONCEPTS.md, concepts 3 + 7.**
**Status:** the only template seats use for design work. Copy this file, fill in the blanks, delete nothing.
**Rule:** a brief that does not carry the laws below — embedded in full, not linked — is INCOMPLETE and does not go out. A builder who has never seen the design docs must still ship high-level work from this brief alone, because the brief carries the laws, the Factory supplies the parts, and the gate fails anything low-level.

**How to use it:** fill in every `[BRACKETED]` field. Complete §1 (activation) BEFORE any design work starts. Complete §5 (harvest sources) for EVERY element before the brief goes out — a brief without harvest sources is incomplete. The builder's handoff must answer §1's applied-laws table and §6's gate measurements (see `HANDOFF-CONTRACT.md`); without them the captain refuses to present the build.

**Standing requirements (every brief, every seat):**
- Read first: `~/workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md`, `~/workspace/team-nitro/THE-BULLSEYE.md`, `~/workspace/team-nitro/THE-NAYA-BRAND.md` — all verified on disk (`test -f`) 2026-11-08.
- §2A TONIGHT'S LAWS are checked before building and again before handoff, and reported law by law in the handoff — a law not checked is not a pass.
- The NAYA Protocol is the constitution. Where anything in this template conflicts with it, the Protocol wins.
- No deploys, merges, PRs, GitHub writes, or live edits unless the brief explicitly authorizes them. Local files only, unless stated otherwise.

---

## §0 — THE FIVE GATES (run before EVERY consequential action)
*Source: THE WISE ONE MANIFESTO (SN-0883); THE-ULTIMATE-ORIENTATION.md §9; THE-BULLSEYE.md. Verbatim, in every brief.*

Before every consequential action — every deploy, every page change, every mail sent, every agent dispatched, every claim made — run these five gates. Not as a ritual. As the decision itself. If any gate fails, STOP. No exceptions.

1. **IS IT RIGHT?** Does this serve the good of everyone it touches? Check consequences for people, privacy, trust, safety, the long-term mission. Evidence of harm or a hard stop = do not proceed. Full stop.
2. **IS IT WHAT THEY TRULY NEED?** What is the human's actual goal — beneath the words, beneath the urgency? If interpreting deeper intent, say so openly. Never silently replace their judgment with your own.
3. **IS IT MINE TO DO?** Do I have the authority? Check permission, ownership, scope, and every decision reserved for Shawn's hand. Being capable of an action never grants authority to take it. Protected gates (money, credentials, destructive, security/privacy, anything leaving the business, merges, ratification) = his hand only, always.
4. **IS NOW THE TIME?** Check readiness, dependencies, reversibility, opportunity cost. Move at nitro speed when the road is right. Do not turn judgment into delay — but never let urgency pick the road.
5. **CAN I PROVE IT?** Define what done looks like BEFORE acting. Then verify with evidence — live bytes, rendered pages, real measurements — never with claims. Receipt before report. If I can't prove it, I don't claim it.

**All five yes → act fully, at full power, no hesitation. Any gate no → stop, say why, propose the wise path.**

Brief-writer's gate check for THIS brief (fill in):
- Gate 1: [yes / no — why]
- Gate 2: [yes / no — why]
- Gate 3: [yes / no — why]
- Gate 4: [yes / no — why]
- Gate 5: [done is defined in §6 below — yes / no]

---

## §1 — ACTIVATION AS A FORCED STEP (concept 7 — NOT a suggestion)
*Before ANY design work, the builder reads all five. Reading is the first step of the work. The proof is in the handoff.*

The builder MUST read, in this order, before touching any design work:

| # | Read | Path (all verified `test -f`, 2026-11-08) | What it is |
|---|------|----------------------------------------------|------------|
| 1 | THE PLAYBOOK — the HOW | `~/workspace/team-nitro/THE-PLAYBOOK.md` | The formula, the steps, the laws. Grade 6 locked in. |
| 2 | DESIGN INTELLIGENCE REPORT — the WHY | `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` | What was got wrong, what was learned. |
| 3 | INTELLIGENT BLOCK RULES — LAW | `~/workspace/team-nitro/hub-board-edit/intelligent-block-rules-LAW-20261106.md` | Ratified 2026-11-06 by Shawn's "1000% YES!". The block rules are LAW. |
| 4 | CLARITY CONFIRMATION ACT — DRAFT | `~/workspace/team-nitro/clarity-confirmation-act-DRAFT-20261106.md` | DRAFT — official only on Shawn's word. The fingerprint, the conduct before acting, the design, all 22 elements. Do not treat as law where it conflicts with the Protocol. |
| 5 | THE NAYA BRAND | `~/workspace/team-nitro/THE-NAYA-BRAND.md` | What a Naya-designed page looks and feels like. |

**The handoff must list what was APPLIED — quote the law + the part it produced.** A handoff without this table is incomplete. Format (one row per law applied, minimum one row per read):

| Law read | Quoted (short, verbatim) | Part it produced in this build |
|----------|--------------------------|--------------------------------|
| e.g. Playbook Truth 2 | "Every element is a physical object with material, weight, and a light source." | The tier buttons: obsidian glass, 135° gradient, shadow down-right |
| [law] | [quote] | [part] |

Builder's activation sign-off (fill in before building):
- [ ] I read all five files above. Date/time read: [____]
- [ ] My handoff will carry the applied-laws table above.

**Run `python3 design-contract-gate/check-brief.py <this brief>` before dispatching — a FAIL means the brief does not go out.**

---

## §2 — THE DESIGN CONTRACT (embedded in full — the measured gate)
*Source: THE-INVENTORY.md Part 1, "THE DESIGN-CONTRACT GATE (new, 2026-11-08 — the lesson of the Pricing + PI misses)". The contract was NAMED in every brief and CHECKED in none. From now on it is a measured section in every brief and every handoff. A gate that fails is not done. A deferral ("captain's decision for later") is an open item, not a pass.*

Every build is measured against all five items. The checker is `~/workspace/team-nitro/design-contract-gate/check-gate.py` (concept-2 seat; static source-level checker — see HANDOFF-CONTRACT.md for its output format). Until it lands, measure by hand in the same format.

| Item | The law (verbatim) | How it is measured |
|------|--------------------|--------------------|
| (a) **Zero white/light backgrounds** | "ZERO white/light backgrounds anywhere on the page (every background obsidian/dark)." | Scan all CSS (inline `<style>`, `style` attributes, linked local CSS) for light background values (`#fff`, `#ffffff`, `white`, `rgb(255,255,255)`, light hex by luminance). Count = 0. Every occurrence reported with location. |
| (b) **Every element raised/elevated** | "Every element raised/elevated (real depth, real lift, real light)." | Every interactive/content element (button, card, pill, board) carries a depth stack: `box-shadow` and/or border + layered shadow. Elements missing depth are listed by location. |
| (c) **Gauges/numbers alive** | "Gauges present and alive (the speedometer language on the numbers)." | The page contains the real gauge (`#tn-tacho-mount` / `.tn-tacho-needle` / `.tn-gear-tooth`) or, for pages without a gauge, live numbers (tiled digits / orbiting orbs with numerals). The number sits on top, the gauge underneath; the needle laps the dial in sets of 500 (734 = one full lap of 500 + 234). A number without its gauge is not finished. |
| (d) **No text-in-image, no pasted document** | "NO text-in-image, NO pasted document." | Flag `<img>` elements whose alt/filename suggests text content, and embedded document-like structures (`<iframe>` to a doc, screenshot-style figures). Count = 0. |
| (e) **No bare text blocks** | "NO bare text blocks — every word lives in a board, pill, jewel, or orb." | Text nodes must live inside a board/pill/jewel/orb container (`.ph-card`, `.os-jewel`, pill classes, etc.). Bare text blocks reported with location. Count = 0. |

**The design-contract test that catches a pasted Word doc:** "Is this the max level of experience I can give the user?" — asked about the PAGE, not the briefed items. If you can see the defect by looking, fix it, don't hand it on.

**Human checks H1–H5** (what the machine cannot check — H1 stranger test · H2 perfect-words law · H3 face quality · H4 test in his head · H5 one ultimate ten) are attested per build with evidence in the handoff; all five attested PASS + machine clean = OVERALL PASS. Without them the verdict reads PASS — MACHINE ONLY, HUMAN CHECKS PENDING.

---

## §2A — TONIGHT'S LAWS — CHECK BEFORE YOU BUILD, CHECK BEFORE YOU HAND BACK (2026-11-09)
*Why these are in the template, in full, not linked: tonight proved the learning WORKS and it LEAKS. The v4 seat repeated the v49 verbatim mistake because the lesson sat in a note, not in its brief; five notes in one night hit the same bold-label defect because no brief ever said `##` sections. A lesson counts only when it changes behavior mechanically (Essence 5). These laws are therefore CHECKABLE gates in every brief — the builder checks each one before building and again before handing back, and the handoff reports each one with its test. A law not checked is not a pass. A brief that does not carry this section is INCOMPLETE and does not go out.*

| # | The law | The test (run it — don't claim it) | Source |
|---|---------|-------------------------------------|--------|
| L1 | **The stranger test.** A person who has never heard of NayaNET, never met Naya, knows nothing — does she get it, believe it, trust us enough to come in, spend time building, invest money? | Every beat/board must answer the question it raises with a mechanism, a picture, or a number she can check. No beat asks her to take our word for it. In the handoff, write the stranger test beat by beat: what would she still ask after this beat, and where in the words is it answered? Any beat that leaves her with a real question FAILS. | 2026-11-09 02:42Z · SN-2442 (The Verbatim Correction, Repeated) |
| L2 | **His words are INPUT, not output — the perfect-words law.** Scorecard his dictation against the existing words, take what's great from both, CRAFT the 10/10 version in his voice. Never paste dictation verbatim into public copy. Never put his process talk / stage directions on the page. Public copy must be professional and explain ourselves. | Read the public copy aloud as a stranger. If any line sounds like his private words posted in public ("never cash back"), it FAILS. If a claim is made without its why, it FAILS. The gate's (h) check fails the page on banned blunt phrases. | 2026-11-09 02:56Z · daily log `~/memory/2026-11-09.md` (smart note pending — next intelligence-loop run) |
| L3 | **Title + subtitle + nutshell.** The skimmable standard — what it means, what's in it for them, spelled out clear as day. No wall of text. | Every board/beat carries title + subtitle + nutshell, each non-empty. The gate's (i) check measures this on the structure. A board anyone must read end-to-end to understand FAILS. | 2026-11-09 02:54Z · SN-2448 (Title + Subtitle + Nutshell — The Skimmable Standard) |
| L4 | **Naya speaks, faces alternate.** Her first-person voice; her face beside the words, left/right switching down the page, different faces — the switch resets attention so the words land. "It's not what you say, it's how you say it." | Machine (gate (i)): consecutive boards alternate sides; every face image is a different source. Human (H3): every face looks real and high quality at render size — no pixelation, no blur. A repeated face or a pixelated face FAILS. | 2026-11-09 02:27Z (SN-2431) + 02:59Z (daily log `~/memory/2026-11-09.md`; smart note pending) |
| L5 | **The test in his head.** Is this 10-star service? Would a stranger see the value in it and trust in it? If they experienced it, would they get it? Is it obvious? Is it useful? Helpful? Is it done so clearly that it's evident what it does and what it is — and it does awesome? | Ask all six questions about the finished work, in writing, in the handoff. Any answer "no" means it is not done yet. | 2026-11-09 02:44Z · SN-2443 (The Test in His Head, Always) |
| L6 | **Smart-note format: `##` sections.** Notes use `##` sections (Hook / Nutshell / Human / Child / Grandma / Naya) — NEVER bold-inline `**Hook:**` labels as section definitions. The feed parser only sees `##` headings; a note with no `##` sections never lands. | The gate's (g) check fails any note with zero `##` sections, or whose sections are defined by bold-inline labels with zero `##` headings. Bold-inline labels quoted as examples alongside real `##` sections are reported, not failed. Run the gate on every note before filing it. | 2026-11-09 02:44Z · SN-2444 (The Parse Fix — `##` Sections or the Note Never Lands) |
| L7 | **The one ultimate ten.** One set, not two — each item is pain + solution + what's in it for them (+ who it's for). The features are valuable BECAUSE they solve the pains; they go hand in hand. Together the ten paint the picture of how the puzzle goes together and why it's extraordinary and different. | Each item names the problem, then the solution ("quite literally, this is the solution — this is how we do it"), then what's in it for them and who it's for. Two separate sets of ten FAILS. An item that only names a pain, or only claims a fix, FAILS. | 2026-11-09 03:21Z + 03:28Z · daily log `~/memory/2026-11-09.md` (smart note pending — next intelligence-loop run) |

**The handoff's gate section (§6) must report each of L1–L7 as PASS / FAIL / N-A, with the test evidence for each.** A handoff that does not report them is incomplete.

### ANTI-REPEAT — the known failure modes (every brief carries these)
*These six prohibitions are the failures tonight already paid for. A brief without them is incomplete — the brief checker fails it. The seat reads them before building and again before handing back.*
- **Never paste his dictation verbatim into public copy (v49/v4).** His words are input, not output — scorecard them, take what's great, craft the 10/10 version in his voice.
- **Never use the word "blockchain" anywhere.** Smart Ledger is a hub of intelligent blocks — a collective chain intelligent network, not the old kind of chain.
- **Never invent a component when the harvested one exists.** Harvest-first: compose, don't create. Take the shown object verbatim.
- **Never report done from scroll-0 checks alone.** Verify scroll 0 AND scrolled, desktop AND phone — a page checked at scroll 0 only is not checked.
- **Never claim without a live measurement.** Live bytes, rendered pages, real measurements — never claims. Receipt before report.
- **Never present work without a live link.** Link, don't preview — no link = not done = don't announce.

---

## §3 — THE BRAND AND THE LAWS (embedded — the standard every seat builds to)
*Sources: THE-NAYA-BRAND.md; laws/THE-REAL-OBJECT-LAW.md (canonical, all of NayaNET, forever); THE-PLAYBOOK.md; DESIGN-INTELLIGENCE-REPORT.md. Condensed here — the full files govern where this summary is silent.*

### The brand, in one paragraph
Naya is a supercharger bolted onto AI — the engine is AI, Naya makes it a supercar. NayaNET is the intelligent layer of the internet: a civilization, not an app. The feeling is ten stars: the human opens it and feels — this was made for me, this knows me, this works, this is beautiful. One click, done for you. Push-button simple on the surface; a supercomputer underneath. The human never operates the system. The AIs operate it. The human receives the finished, beautiful output — served on a platter.

### The Real Object Law (all seven principles)
1. **Everything is an object.** Every UI element exists in 3D space — volume, mass, surface, edge. A button is a physical button. An orb is a glass sphere. A board is a slab. A gauge is an instrument. Never a flat shape pretending.
2. **One light source, top-left, always.** Every gradient runs 135°. Every shadow falls down-right. Every highlight sits on the upper edge. Inconsistent lighting = fake. The light never moves.
3. **Real materials.** Obsidian glass (`#0a0a0f` to `#1a1a20`, gradient at 135° — never pure black, never flat, never grayish, never off-black), brushed metal/aluminum light (`#c8ccd6 → #9a9ea8 → #7a7e88 → #9a9ea8 → #b8bcc6`), light with volume. Gold for what matters — engraved gold on obsidian. Never neon. Never pink glow.
4. **Real shadows.** Objects sit ON the page. They cast. They have weight. No shadow = floating = fake. Depth is built from shadows, never from glow. Glow is light; shadow is mass. We build mass.
5. **Touch = physical response.** Press a button and it answers like a real thing — it depresses (scale 0.97, 0.1s), it lights, it responds. Rest raised, hover rises (`translateY(-2px)`), active presses in (`translateY(1px)`).
6. **Speak in objects.** Icons, circles, boards, buttons — minimal text. Almost no text: the page speaks in boards, buttons, jewels, orbs, gauges, pills. A paragraph of text on a bare page is the failure mode.
7. **The viewport is the stage.** The page is a world, not a document. One screen, complete on its own; the user scrolls down OR across — both, their choice, laptop and mobile.

### The Playbook truths (the HOW, Grade 6 locked in)
- **Calculate, never eyeball.** Gauge numerals sit at `angle = -135 + (value/500)*270` degrees. All six: 0, 100, 200, 300, 400, 500 — never skip 400 (81°; the bottom is 90°, there is room). If there is no formula, it is wrong.
- **8px grid** for linear layouts (8, 16, 24, 32, 48, 64, 96). Text sizes 12 / 14 / 16 / 20 / 28 / 48. Never 13px. Never 27px.
- **White text, always** (`#ffffff` or `rgba(255,255,255,0.9)`). Never colored text. Never gray below 0.6 opacity. Text never lights up, never takes color. Color lives in icon orbs, thin edge bars (2–3px), hover glow — nowhere else. Spectrum order, never random: purple `#a06bff` · blue `#3fb8ff` · green `#2fe89e` · gold `#ffbf3d` · orange `#ff9a5a` · red `#ff5e6c` · magenta `#e84fff`. At rest the system is obsidian and white; color ignites on touch, in the element's OWN color only.
- **Slow motion.** Ambient 60s–180s, active 18s–25s. Never faster than 12s — faster feels cheap. Alternate direction (CW, CCW, CW, CCW). Movement means the machine is working; if you can't say what a moving part DOES in one sentence, delete the animation.
- **One language.** Every component speaks vortex, obsidian, white text, slow motion. A button on the Dashboard feels like a button on the Profile because they are built from the same materials, same light, same principles.
- **Harvest, don't invent.** Use the parts registry. Compose, don't create. (See §4–§5.)
- **Don't touch unasked.** Working things stay working.
- **His eye wins.** Always. This document updates when he corrects us.

### The Intelligence Report lessons (the WHY — what was got wrong)
- Premium is NOT glow. "You really think that I think premium is color color glow? You gotta be kidding me." Premium is exact numbers, real materials, slow elegant motion, data so clear it hits in 2 seconds.
- Never eyeball, never skip a number, finish the edge (the bezel is what the eye hits first), don't "improve" what Shawn didn't ask to change, and my score is irrelevant — his eye is the instrument.

### The three questions (before showing Shawn)
1. Is every position calculated? (Show the formula.)
2. Does it feel like a machine? (What's moving, and why?)
3. Can you get it in 2 seconds? (What's the headline?)
If yes to all three: show him, say nothing, let his eye judge. If no to any: fix it. Don't show him yet.

### Buttons — ALL elite, no exceptions
Every button is a real object: elevated, deep, lit, with real lift and real light. No flat buttons. No grayish buttons. No button that looks cheaper than the others. The create button, the favorite button, the save button — all the same level, all the same quality, all light up the same. A button that doesn't light up like the best one on the page is a broken button. Inputs always have lots of depth. Outputs are the cleanest — broken up, scannable, the intelligent-block presentation.

### The Premium Design Algorithm — the Rubik's Cube matrix (ratified 2026-11-08)
Viewpoint by viewpoint — the unit of building is the SCREEN, not the app, always mobile optimized. One core page that morphs into all the other pages (one cube, many faces). The Trinity: Dashboard, Hub, and that page. The universal template: the same objects and functions on every page, the middle changing with the page's function. Every page introduces itself with a big beautiful hero banner. Functions pop up (click, it comes into your viewpoint; X, it goes away). The person is the atom at the centre; everything orbits them. She is Anaya.

---

## §4 — THE FACTORY (the ONLY source named in any design brief)
*Source: THE-INVENTORY.md (Parts 1–2c). The Factory is the only source named in any design brief. Every element traces to the piece index or a named harvest source.*

| Source | Path (verified `test -f`, 2026-11-08) | What it holds |
|--------|------------------------------------------|---------------|
| THE INVENTORY | `~/workspace/team-nitro/THE-INVENTORY.md` | The design laws (Part 1) + every piece with its link (Parts 2–2c) + locked-in smart blocks (Part 3). Read Part 1 before any design work. |
| THE CANONICAL PIECE INDEX | `~/workspace/smart-factory-contract/CANONICAL-PIECE-INDEX.md` (+ `.json` twin) | The master index. Truth: **571 unique IDs; 154 CANONICAL** in the working store; 416 UNVERIFIED (named but absent from the store — a harvester may NOT cite them as canonical); 1 SUPERSEDED (NAYA-INP-001 Search bar — replaced by NAYA-INP-008). "478" was builder-index-v1, a source-extraction catalog, not the canon. |
| THE WORKING STORE | `~/workspace/personal-app/pieces.json` | 155 entries: 154 canonical + 1 superseded. |
| THE LIVE CSS | `~/workspace/personal-app/factory.css` | The canonical CSS the pieces wear. |
| THE ANATOMY | `~/workspace/team-nitro/viewpoints/ANATOMY-OF-A-VIEWPORT.md` | What a viewpoint IS + the six-question test (§6). |
| THE HARVEST | `~/workspace/team-nitro/viewpoints/harvest-20261108/HARVEST.md` | The harvested pieces, laid out, with verbatim CSS. Copy VERBATIM — never restyle, never rebuild "in the style of". Change only the text inside. |

**Rules:**
- **Compose, don't create.** If a piece exists in the Factory, use it. Don't modify it. Don't "improve" it. If something close exists, adapt — don't invent. Truly doesn't exist? Build it following the Playbook, then add it to the registry.
- **Harvest-first, enforced by Law 14:** every element traces to the piece index or a named harvest source; invented chrome FAILS the build. The builder's handoff must list the harvest source for every element, or the build is rejected.
- **The 7 canonical libraries are TO-LOCATE** (no file by that name was found on disk, 2026-11-08). Do NOT guess a path. Do not cite them as a source until their paths are confirmed.
- **Known gaps (do not cite as sources):** the Hub's `.note-card` class has NO CSS rule in the Hub file — its styling could not be pinned; the mail page's `.os-savebtn` rule is cited in a comment but is not in `mail.html`. Neither is listed in the inventory until located.
- **High-end only.** No Ford parts in the Factory at all. Quarantined (below standard, 2026-10-17): NAYA-NAV-001, NAYA-NAV-007, NAYA-TYP-001, NAYA-TYP-002, NAYA-TYP-007, NAYA-TYP-008 — never use.

---

## §5 — HARVEST-SOURCE CHECKLIST (complete for EVERY element — a brief without this is incomplete)
*Rule: exact file + line, verified with `test -f` before the brief goes out. Copy VERBATIM from the source — same HTML structure, same CSS values, same JS behavior. Adapting content (menu items, labels) is allowed; restyling the component is not.*

Brief-writer: run `test -f <path>` for every row and record the result. A row with no verified source does not go out.

| # | Element (this build) | Piece ID / class | Harvest source — exact file + line | `test -f` | Verbatim or adapted (what changed) |
|---|----------------------|------------------|------------------------------------|-----------|-------------------------------------|
| 1 | [e.g. content board] | `.ph-card` | `~/workspace/team-nitro/dashboard/defectfix-v7/builder/fix9/fix9-work.html` lines 2018–2025 | OK 2026-11-08 | Verbatim CSS; only the text inside changes |
| 2 | [e.g. primary button] | `.primo` | `~/workspace/team-nitro/hub/index-2-fixed-v2.html` line 689 | OK 2026-11-08 | Verbatim; label text adapted |
| 3 | [element] | [piece ID] | [file + line] | [OK / MISSING — date] | [verbatim / adapted — what] |
| 4 | [element] | [piece ID] | [file + line] | [OK / MISSING — date] | [verbatim / adapted — what] |
| … | … | … | … | … | … |

**Every element in the build must appear in this table.** An element with no row is an invented element, and invented chrome fails the build (Law 14). **A look-alike fails too** — the 2026-11-08 16:41Z lesson (Pricing condemned a third time: a yellow "try her nine free" button that is not his button, a gauge that is not his gauge, numbers that are not his numbers — "all wannabe, low-end copycat, not done well"). A rebuilt-in-the-style-of copy of a harvested part is not a harvested part. The handoff must prove the harvest source for every element (HANDOFF-CONTRACT.md §3); a part whose source cannot be named is a look-alike, and the build is rejected.

---

## §6 — DONE, DEFINED FIRST (the Bullseye)
*Source: THE-BULLSEYE.md. No brief ships without this section. If done was never defined, the work cannot be done — it can only be "worked on."*

- **Page / viewpoint:** [which page, which viewpoint — one screen, complete on its own]
- **Exact element:** [the element, by name and location]
- **Exact behavior:** [what it does when touched/clicked/loaded]
- **Exact measurement:** [the number that proves it — e.g. first paint ≤ X ms, needle at Y°, count = Z, gate items pass]
- **What must NOT be there:** [the defect, the flat element, the white background, the bare text — named explicitly]
- **Scope boundary — do NOT touch:** [working things that stay working; Shawn did not ask to change them]

**Verification (the builder runs this before handoff — see HANDOFF-CONTRACT.md):**
- In a real browser. Phone first (390px), desktop second (1280px and wide). Scroll 0 AND scrolled.
- Every button clicked, every destination recorded. Screenshots or it did not happen.
- The design-contract gate measurements (§2) + the anatomy six-question test, both in the handoff.
- **Standard verification plan (every brief names it):** Playwright, desktop 1440 + phone 390 + true 360, zero overflow, zero console errors, named no-regressions.
- **The three-step verification is DEAD as a quality gate.** Seat scorecards (maker's self-scorecard, then a different seat's) are PREPARATION, never proof. The only verification is Shawn's eye, live, per viewpoint. The captain refuses to present a build without the gate measurements + the anatomy answers (HANDOFF-CONTRACT.md).

---

## §7 — THE WORK (fill in per brief)
- **Task:** [what to build/fix, in plain words]
- **Shawn's words (verbatim, if any):** "[quote — never paraphrase his operative words]"
- **Order / source:** [his order date, or the plan file this brief comes from]
- **Deliverable:** [exact file path(s) the work lands in]
- **Constraints:** [no deploys / merges / PRs / GitHub writes / live edits — unless explicitly authorized here]
- **Report back:** [what the parent agent needs — where the file lives, the measurements, DONE and NOT-DONE together]

---

## WORKED EXAMPLE — one filled brief section (from this template's own grounding)
*This section is an example only. Delete it when writing a real brief — or keep one filled row as the pattern.*

**§5 harvest row, filled in:** The content board for a Pricing viewpoint is `.ph-card`, harvested from `~/workspace/team-nitro/dashboard/defectfix-v7/builder/fix9/fix9-work.html` lines 2018–2025 (verified `test -f`, 2026-11-08; CSS confirmed on disk: `background:linear-gradient(180deg,#07070b,#050607); border:2px solid rgba(255,255,255,.16); border-radius:20px; padding:28px;` with the layered shadow stack and a hover that lifts −4px and glows gold `rgba(217,165,33,.6)`). It is copied VERBATIM — same structure, same CSS values — only the words inside change, because the Real Object Law (Principle 1: everything is an object; Principle 3: real materials — obsidian glass, 135° gradient) and the Playbook (Truth 2: every element is a physical object with material, weight, and a light source; Truth 4: the whole system speaks one language) demand the board be the same board on every page, and the design-contract gate (b) demands every element raised and elevated, which this board's shadow stack is. The primary action on the same viewpoint is `.primo` from `~/workspace/team-nitro/hub/index-2-fixed-v2.html` line 689 (verified `test -f`, 2026-11-08): the elite button — 16px 32px, radius 999px, 1.5px white border, obsidian gradient, sheen sweep, hover lifts −2px and glows in its own color — because the brand law is ALL buttons elite and lit the same, and a button that doesn't light up like the best one on the page is a broken button.

---

*Template written 2026-11-08 by the brief-template seat, Shawn's lock-in order 16:37Z, concepts 3 + 7. §2A TONIGHT'S LAWS added 2026-11-09 (Shawn's question: how do Nayas learn and change behavior at hyper speed without being retaught — the laws in the template and the gate are the answer). Grounded in: THE-ULTIMATE-ORIENTATION.md · THE-BULLSEYE.md · THE-NAYA-BRAND.md · THE-PLAYBOOK.md · DESIGN-INTELLIGENCE-REPORT.md · intelligent-block-rules-LAW-20261106.md · clarity-confirmation-act-DRAFT-20261106.md · ANATOMY-OF-A-VIEWPORT.md · THE-INVENTORY.md — every path verified `test -f` on 2026-11-08. §2A sources: SN-2442 · SN-2443 · SN-2444 · SN-2448 · SN-2431 · daily log `~/memory/2026-11-09.md`. If a law file moves, update this template in the same pass (concept 9 — the intelligence loop).*
