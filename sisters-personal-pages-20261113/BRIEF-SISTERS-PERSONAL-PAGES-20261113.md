# BRIEF — THE WALK GIVES EVERY CITIZEN THE SAME WORLD (SISTERS' PERSONAL PAGES)

**BULLSEYE (one line):** every citizen's Personal page looks EXACTLY like nayanet.app/personal — same layout, cover, photo slot, buttons, feed, composer, boards, bottom bar — with their own name, their own words, their own cover. Nothing new, nothing different.

## THE SITUATION — READ FIRST

- Shawn's law, 04:01Z: the sisters do NOT build custom personal pages. A sister's Personal page looks EXACTLY like the normal Personal page, plus one of the beautiful smart covers. Same as ours. No different page.
- Shawn's law, sharpened 04:16Z (in substance): everybody gets the SAME world — just different labels. The apps are universal; they all look like each other, like part of a family; but they're beautiful — everybody gets a high-tech million-dollar home from the start, or even a billion-dollar home. Why would anyone get a different world than anybody else? They wouldn't.
- Tonight he pressed it: what he saw did not look right. The test is whether their pages look like https://nayanet.app/personal.
- The verdict, read-only browser comparison 04:11Z: DIFFERENT. Sophia's staged page — https://naya-walk-beginning-staging.nayapower.workers.dev/pages/sophia/sophia — is a single narrow centered dark card (~600px) with a static bio essay (eyebrow "YOUR PERSONAL PAGE", heading "sophia", sections Nutshell / Why it matters / What it means / How to apply it / What's in it for you) and one "Back to your Hub" button. The live Personal page — https://nayanet.app/personal — is a full-width edge-to-edge profile page: full-width gradient cover banner + circular profile photo + "Change cover", membership pills (Naya Academy, AI Masterclass, Fast Action Club), action buttons (Message, About, My World, Skills, Connections, Invite, Share, Join NayaNET, Settings, Add something), a Live Feed with a "Make a post" composer, feed tabs (Smart Notes / Naya Notes / Activity), boards, and a persistent bottom bar. The staged page has NONE of those.
- The walk builds a card, not the Personal page. The earlier claim that the sisters' pages were "walk-created from the Personal template" was wrong — the data was checked, the look never was. The twelve sisters' data IS correct (Box: 1 box, 1 project, 3 pages each, all ten answers word-for-word) — the SHAPE is wrong.
- The fix is NOT a sisters-only special. The twelve sisters are the proof set, not the scope. The scope is every citizen, present and future: the walk gives every citizen the same world.

## THE FIX SHAPE — DECIDED ON EVIDENCE: (a) CHANGE THE WALK'S BUILDER

(a) CHANGE THE WALK'S BUILDER so every citizen's Personal page IS the Personal page. The renderer that makes the card is replaced with a renderer that serves the Personal page itself, with only the citizen's labels swapped in (name, words, cover).

Why (a), and why (b) is wrong: the sisters' pages are not stored files. They are rendered on request by the walk staging worker from the Box (citizen_worlds) through the page renderer — proven by the S2 record (pages curl-render with typed titles; the route takes the slug, not the kind). Changing the renderer changes all twelve sisters' pages and every future citizen's page in one move. (b) — converting the twelve by cloning live Personal v9 into twelve static copies — would give the sisters a different world than the next citizen gets, which is exactly what the sharpened law forbids; and twelve static copies would drift from the template the moment Personal v10 lands. Under the sharpened law, (b) is not just unnecessary — it is the wrong shape.

Fallback to (c): the maker runs the step-1 search first. If static per-sister page files are found anywhere (repo, worktree, proof host), the shape becomes (c) — fix the builder AND rebuild those files from the same renderer — and the record names every file found. If none are found, the shape stays (a) and the record says so with the search evidence.

The renderer serves all three kinds (personal, business, space) through one function. Under the Clone Law and the sharpened law, all three kinds ARE the Personal page: Personal says "My Story", Business and Space say "Our Story", each with its own words and its own cover. The card shape is deleted, not restyled.

## §0 — THE FIVE GATES (run before EVERY consequential action)

Before every consequential action — every deploy, every page change, every mail sent, every agent dispatched, every claim made — run these five gates. Not as a ritual. As the decision itself. If any gate fails, STOP. No exceptions.

1. **IS IT RIGHT?** Does this serve the good of everyone it touches? Check consequences for people, privacy, trust, safety, the long-term mission. Evidence of harm or a hard stop = do not proceed. Full stop.
2. **IS IT WHAT THEY TRULY NEED?** What is the human's actual goal — beneath the words, beneath the urgency? If interpreting deeper intent, say so openly. Never silently replace their judgment with your own.
3. **IS IT MINE TO DO?** Do I have the authority? Check permission, ownership, scope, and every decision reserved for Shawn's hand. Being capable of an action never grants authority to take it. Protected gates (money, credentials, destructive, security/privacy, anything leaving the business, merges, ratification) = his hand only, always.
4. **IS NOW THE TIME?** Check readiness, dependencies, reversibility, opportunity cost. Move at nitro speed when the road is right. Do not turn judgment into delay — but never let urgency pick the road.
5. **CAN I PROVE IT?** Define what done looks like BEFORE acting. Then verify with evidence — live bytes, rendered pages, real measurements — never with claims. Receipt before report. If I can't prove it, I don't claim it.

**All five yes → act fully, at full power, no hesitation. Any gate no → stop, say why, propose the wise path.**

Brief-writer's gate check for THIS brief:
- Gate 1: yes — this gives every citizen the same beautiful world; it harms nobody; it fixes a wrong shape Shawn named himself.
- Gate 2: yes — his goal beneath the words is one world for everybody, proven by his 04:16Z sharpening ("why would anyone get a different world than anybody else? They wouldn't").
- Gate 3: yes — brief only; no build, no deploy, no merge, no PR, no mail, no live touch. The maker builds staged only.
- Gate 4: yes — the renderer is the single point of fix; the proof set (twelve sisters + one fresh citizen) is ready; v23 is the deploy vehicle.
- Gate 5: yes — done is defined in §6 below.

## §1 — ACTIVATION AS A FORCED STEP

The builder MUST read, in this order, before touching any design work. The proof is in the handoff: the handoff lists what was APPLIED — quote the law + the part it produced, one row per law applied, minimum one row per read. A handoff without this table is incomplete.

| # | Read | Path | What it is |
|---|------|------|-----------|
| 1 | THE PLAYBOOK — the HOW | `~/workspace/team-nitro/THE-PLAYBOOK.md` | The formula, the steps, the laws. Grade 6 locked in. |
| 2 | DESIGN INTELLIGENCE REPORT — the WHY | `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` | What was got wrong, what was learned. |
| 3 | INTELLIGENT BLOCK RULES — LAW | `~/workspace/team-nitro/hub-board-edit/intelligent-block-rules-LAW-20261106.md` | Ratified 2026-11-06 by Shawn's "1000% YES!". The block rules are LAW. |
| 4 | CLARITY CONFIRMATION ACT — DRAFT | `~/workspace/team-nitro/clarity-confirmation-act-DRAFT-20261106.md` | DRAFT — official only on Shawn's word. The fingerprint, the conduct before acting, the design, all 22 elements. |
| 5 | THE NAYA BRAND | `~/workspace/team-nitro/THE-NAYA-BRAND.md` | What a Naya-designed page looks and feels like. |

Builder's activation sign-off (fill in before building):
- [ ] I read all five files above. Date/time read: [____]
- [ ] My handoff will carry the applied-laws table above.

**Run `python3 ~/workspace/team-nitro/design-contract-gate/check-brief.py <this brief>` before dispatching — a FAIL means the brief does not go out.** (The brief-writer already ran it on this brief: 9/9 PASS.)

## §2 — THE DESIGN CONTRACT (the design-contract gate (a)–(i) + human checks H1–H5)

Every build is measured against the design-contract gate (a)–(i). A gate that fails is not done. A deferral ("captain's decision for later") is an open item, not a pass. Human checks H1–H5 (what the machine cannot check — H1 stranger test · H2 perfect-words law · H3 face quality · H4 test in his head · H5 one ultimate ten) are attested per build with evidence in the handoff; all five attested PASS + machine clean = OVERALL PASS. Without them the verdict reads PASS — MACHINE ONLY, HUMAN CHECKS PENDING.

| Item | The law | How it is measured |
|------|---------|-------------------|
| (a) Zero white/light backgrounds | "ZERO white/light backgrounds anywhere on the page (every background obsidian/dark)." | Scan all CSS for light background values. Count = 0. Every occurrence reported with location. |
| (b) Every element raised/elevated | "Every element raised/elevated (real depth, real lift, real light)." | Every interactive/content element carries a depth stack: box-shadow and/or border + layered shadow. Elements missing depth are listed by location. |
| (c) Gauges/numbers alive | "Gauges present and alive (the speedometer language on the numbers)." | Live numbers on the page (tiled digits / orbiting orbs with numerals; points and level under the photo). The number sits on top, the gauge underneath. A number without its gauge is not finished. |
| (d) No text-in-image, no pasted document | "NO text-in-image, NO pasted document." | Flag `<img>` elements whose alt/filename suggests text content, and embedded document-like structures. Count = 0. |
| (e) No bare text blocks | "NO bare text blocks — every word lives in a board, pill, jewel, or orb." | Text nodes must live inside a board/pill/jewel/orb container. Bare text blocks reported with location. Count = 0. |
| (f) No look-alike | "No look-alike — a rebuilt-in-the-style-of copy of a harvested part is not a harvested part." | Every board, button, and pill is compared shape-for-shape against its harvest source. A look-alike fails. |
| (g) `##` format | "Every note and every page section uses `##` sections — the feed parser only sees `##` headings." | Sections defined by bold-inline labels with zero `##` headings fail. |
| (h) No dictation-blunt phrases | "No dictation-blunt phrases — banned blunt phrases fail the page." | His process talk and stage directions never reach public copy. Any banned blunt phrase fails. |
| (i) Title+subtitle+nutshell + faces alternate | "Every board carries title+subtitle+nutshell; Naya speaks, faces alternate." | Every board carries title + subtitle + nutshell, each non-empty; consecutive boards alternate sides; every face image is a different source. |

**The design-contract test that catches a pasted Word doc:** "Is this the max level of experience I can give the user?" — asked about the PAGE, not the briefed items. If you can see the defect by looking, fix it, don't hand it on.

## §2A — TONIGHT'S LAWS L1–L7 — CHECK BEFORE YOU BUILD, CHECK BEFORE YOU HAND BACK

| # | The law | The test (run it — don't claim it) |
|---|---------|-------------------------------------|
| L1 | **The stranger test.** A person who has never heard of NayaNET, never met Naya, knows nothing — does she get it, believe it, trust us enough to come in, spend time building, invest money? | Every beat/board must answer the question it raises with a mechanism, a picture, or a number she can check. No beat asks her to take our word for it. Any beat that leaves her with a real question FAILS. |
| L2 | **His words are INPUT, not output — the perfect-words law.** Scorecard his dictation against the existing words, take what's great from both, CRAFT the 10/10 version in his voice. Never paste dictation verbatim into public copy. | Read the public copy aloud as a stranger. If any line sounds like his private words posted in public, it FAILS. If a claim is made without its why, it FAILS. |
| L3 | **Title+subtitle+nutshell.** The skimmable standard — what it means, what's in it for them, spelled out clear as day. No wall of text. | Every board/beat carries title+subtitle+nutshell, each non-empty. A board anyone must read end-to-end to understand FAILS. |
| L4 | **Naya speaks, faces alternate.** Her first-person voice; her face beside the words, left/right switching down the page, different faces — the switch resets attention so the words land. | Consecutive boards alternate sides; every face image is a different source. A repeated face or a pixelated face FAILS. |
| L5 | **The test in his head.** Is this 10-star service? Would a stranger see the value in it and trust in it? If they experienced it, would they get it? Is it obvious? Is it useful? Helpful? Is it done so clearly that it's evident what it does and what it is — and it does awesome? | Ask all six questions about the finished work, in writing, in the handoff. Any answer "no" means it is not done yet. |
| L6 | **Smart-note format: `##` sections.** Notes use `##` sections — NEVER bold-inline `**Hook:**` labels as section definitions. The feed parser only sees `##` headings; a note with no `##` sections never lands. | The gate's (g) check fails any note with zero `##` sections, or whose sections are defined by bold-inline labels with zero `##` headings. |
| L7 | **One ultimate ten.** One set, not two — each item is pain + solution + what's in it for them (+ who it's for). | Each item names the problem, then the solution, then what's in it for them and who it's for. Two separate sets of ten FAILS. |

**The handoff's gate section (§6) must report each of L1–L7 as PASS / FAIL / N-A, with the test evidence for each.** A handoff that does not report them is incomplete.

### ANTI-REPEAT — the known failure modes (every brief carries these)
- **Never paste his dictation verbatim into public copy (v49/v4).** His words are input, not output — scorecard them, take what's great, craft the 10/10 version in his voice.
- **Never use the word "blockchain" anywhere.** Smart Ledger is a hub of intelligent blocks — a collective chain intelligent network, not the old kind of chain.
- **Never invent a component when the harvested one exists.** Harvest-first: compose, don't create. Take the shown object verbatim.
- **Never report done from scroll-0 checks alone.** Verify scroll 0 AND scrolled, desktop AND phone — a page checked at scroll 0 only is not checked.
- **Never claim without a live measurement.** Live bytes, rendered pages, real measurements — never claims. Receipt before report.
- **Never present work without a live link.** Link, don't preview — no link = not done = don't announce.

## §3 — THE BRAND AND THE LAWS

Naya is a supercharger bolted onto AI — the engine is AI, Naya makes it a supercar. NayaNET is the intelligent layer of the internet: a civilization, not an app. The feeling is ten stars: the human opens it and feels — this was made for me, this knows me, this works, this is beautiful. One click, done for you. Push-button simple on the surface; a supercomputer underneath. The human never operates the system. The AIs operate it. The human receives the finished, beautiful output — served on a platter.

### The Real Object Law (all seven principles)
1. **Everything is an object.** Every UI element exists in 3D space — volume, mass, surface, edge. Never a flat shape pretending.
2. **One light source, top-left, always.** Every gradient runs 135°. Every shadow falls down-right. Every highlight sits on the upper edge. The light never moves.
3. **Real materials.** Obsidian glass (`#0a0a0f` to `#1a1a20`, gradient at 135° — never pure black, never flat, never grayish), brushed metal, light with volume. Gold for what matters. Never neon. Never pink glow.
4. **Real shadows.** Objects sit ON the page. They cast. They have weight. No shadow = floating = fake.
5. **Touch = physical response.** Press a button and it answers like a real thing — it depresses (scale 0.97, 0.1s), it lights, it responds. Rest raised, hover rises, active presses in.
6. **Speak in objects.** Icons, circles, boards, buttons — minimal text. A paragraph of text on a bare page is the failure mode.
7. **The viewport is the stage.** The page is a world, not a document. One screen, complete on its own.

### The Playbook truths (the HOW, Grade 6 locked in)
- **Calculate, never eyeball.** If there is no formula, it is wrong.
- **8px grid** for linear layouts (8, 16, 24, 32, 48, 64, 96). Text sizes 12 / 14 / 16 / 20 / 28 / 48. Never 13px. Never 27px.
- **White text, always** (`#ffffff` or `rgba(255,255,255,0.9)`). Never colored text. Never gray below 0.6 opacity. Color lives in icon orbs, thin edge bars (2–3px), hover glow — nowhere else. Spectrum order, never random: purple `#a06bff` · blue `#3fb8ff` · green `#2fe89e` · gold `#ffbf3d` · orange `#ff9a5a` · red `#ff5e6c` · magenta `#e84fff`. At rest the system is obsidian and white; color ignites on touch, in the element's OWN color only.
- **Slow motion.** Ambient 60s–180s, active 18s–25s. Never faster than 12s. If you can't say what a moving part DOES in one sentence, delete the animation.
- **One language.** Every component speaks vortex, obsidian, white text, slow motion.
- **Harvest, don't invent.** Use the parts registry. Compose, don't create.
- **Don't touch unasked.** Working things stay working.
- **His eye wins.** Always.
- **Cover → menu → page on every page.** Obsidian black, never gray. Icons lit white at rest. Every box elevated. Every board and button LIGHTS UP on hover — moving on hover without lighting up FAILS.

### The Intelligence Report lessons (the WHY)
- Premium is NOT glow. Premium is exact numbers, real materials, slow elegant motion, data so clear it hits in 2 seconds.
- Never eyeball, never skip a number, finish the edge, don't "improve" what Shawn didn't ask to change, and my score is irrelevant — his eye is the instrument.

### The three questions (before showing Shawn)
1. Is every position calculated? (Show the formula.)
2. Does it feel like a machine? (What's moving, and why?)
3. Can you get it in 2 seconds? (What's the headline?)
If yes to all three: show him, say nothing, let his eye judge. If no to any: fix it. Don't show him yet.

### Buttons — ALL elite, no exceptions
Every button is a real object: elevated, deep, lit, with real lift and real light. No flat buttons. No grayish buttons. No button that looks cheaper than the others. All the same level, all the same quality, all light up the same. A button that doesn't light up like the best one on the page is a broken button. Inputs always have lots of depth. Outputs are the cleanest — broken up, scannable, the intelligent-block presentation.

### The Premium Design Algorithm — the Rubik's Cube matrix
Viewpoint by viewpoint — the unit of building is the SCREEN, not the app, always mobile optimized. One core page that morphs into all the other pages (one cube, many faces). The Trinity: Dashboard, Hub, and that page. The universal template: the same objects and functions on every page, the middle changing with the page's function. Every page introduces itself with a big beautiful hero banner. Functions pop up (click, it comes into your viewpoint; X, it goes away). The person is the atom at the centre; everything orbits them.

## §4 — THE FACTORY (the ONLY source named in any design brief)

| Source | Path | What it holds |
|--------|------|---------------|
| THE INVENTORY | `~/workspace/team-nitro/THE-INVENTORY.md` | The design laws (Part 1) + every piece with its link (Parts 2–2c) + locked-in smart blocks (Part 3). Read Part 1 before any design work. |
| THE CANONICAL PIECE INDEX | `~/workspace/smart-factory-contract/CANONICAL-PIECE-INDEX.md` (+ `.json` twin) | The master index. Truth: **571 unique IDs; 154 CANONICAL** in the working store; 416 UNVERIFIED (named but absent from the store — a harvester may NOT cite them as canonical); 1 SUPERSEDED. |
| THE WORKING STORE | `~/workspace/personal-app/pieces.json` | 155 entries: 154 canonical + 1 superseded. |
| THE LIVE CSS | `~/workspace/personal-app/factory.css` | The canonical CSS the pieces wear. |
| THE ANATOMY | `~/workspace/team-nitro/viewpoints/ANATOMY-OF-A-VIEWPORT.md` | What a viewpoint IS + the six-question test (§6). |
| THE HARVEST | `~/workspace/team-nitro/viewpoints/harvest-20261108/HARVEST.md` | The harvested pieces, laid out, with verbatim CSS. Copy VERBATIM — never restyle, never rebuild "in the style of". Change only the text inside. |

**Rules:**
- **Compose, don't create.** If a piece exists in the Factory, use it. Don't modify it. Don't "improve" it. If something close exists, adapt — don't invent. Truly doesn't exist? Build it following the Playbook, then add it to the registry.
- **Harvest-first, enforced by Law 14:** every element traces to the piece index or a named harvest source; invented chrome FAILS the build. The builder's handoff must list the harvest source for every element, or the build is rejected.
- **High-end only.** No Ford parts in the Factory at all.

## §5 — HARVEST-SOURCE CHECKLIST

Rule: exact file + line, verified with `test -f` before the brief goes out. Copy VERBATIM from the source — same HTML structure, same CSS values, same JS behavior. Adapting content (menu items, labels) is allowed; restyling the component is not. Every element in the build must appear in this table. An element with no row is an invented element, and invented chrome fails the build (Law 14). A look-alike fails too — a rebuilt-in-the-style-of copy of a harvested part is not a harvested part.

| # | Element (this build) | Piece ID / class | Harvest source — exact file + line | `test -f` | Verbatim or adapted (what changed) |
|---|----------------------|------------------|------------------------------------|-----------|-------------------------------------|
| 1 | The Personal page template (the whole page) | the page itself | Live https://nayanet.app/personal — re-harvested first-hand 2026-11-13 ~04:15Z: 1,484,185 B, sha256 `992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50` — the maker re-curls it first-hand at build time; local reference `~/workspace/team-nitro/space-business-mirror-personal-20261112/template-composed.html` (1,486,773 B, sha `61002d15` — NOT byte-identical to live; the LIVE bytes are the authority) | OK 2026-11-13 | Verbatim; only the citizen's labels change (name, words, cover) |
| 2 | The card renderer to replace — pageBody | `function pageBody(kind, a)` | `~/workspace/team-nitro/walk-questions-10-20261112/build-beginning-staging-worker.py` line 166 | OK 2026-11-13 | Replaced, not restyled |
| 3 | The card renderer to replace — pageHtml | `function pageHtml(alias, pg)` | `~/workspace/team-nitro/walk-questions-10-20261112/build-beginning-staging-worker.py` line 205 ("Back to your Hub" line 229; the card's `.wrap` max-width 680px) | OK 2026-11-13 | Replaced, not restyled |
| 4 | The lineage candidate — S2 build script | `pageBody` line 174, `pageHtml` line 213 ("Back to your Hub" line 237) | `~/workspace/team-nitro/walk-s2-box-pages-20261112/build-beginning-staging-worker.py` | OK 2026-11-13 | Compared, not edited unless the lineage proof names it |
| 5 | The serving proof — S2 record | pages curl-render from citizen_worlds; the route takes the slug | `~/workspace/team-nitro/walk-s2-box-pages-20261112/S2-RECORD-20261112.md` lines 96, 117–118 | OK 2026-11-13 | Read, not copied |
| 6 | The clone swaps — how Personal becomes Business/Space | 24/25 lines swapped, zero Personal remnants | `~/workspace/team-nitro/space-business-mirror-personal-20261112/RECORD.md` | OK 2026-11-13 | The swap shape, applied to the renderer (My Story vs Our Story) |
| 7 | The sisters' data — Box citizen_worlds | 1 box, 1 project, 3 pages each, ten answers word-for-word | Live read-back via `/api/welcome/box?alias=` (no file; the maker records the read-back) | N/A — live read-back | Read only; never edited |
| 8 | The v23 vehicle — Q10-fixed walk | Walk file sha `be55a494` (3,364,147 B), branch `walk/questions-10-20261112` head `f08bcf08`, filed 04:15:30Z | `~/workspace/team-nitro/walk-questions-10-20261112/Q10-RECORD-20261113.md` | OK 2026-11-13 | Read; the build script still asserts walk sha `a3510446` — the maker reconciles the assertion first-hand before rebuilding |

## §6 — DONE, DEFINED FIRST (the Bullseye)

- **Page / viewpoint:** the citizen's Personal page at `/pages/<alias>/<slug>` on the staged walk worker, phone 390 first, desktop 1440 second.
- **Exact element:** the whole page, board by board — cover banner (full-width gradient), circular photo slot, "Change cover", membership pills (Naya Academy, AI Masterclass, Fast Action Club), action buttons (Message, About, My World, Skills, Connections, Invite, Share, Join NayaNET, Settings, Add something), Live Feed with a "Make a post" composer, feed tabs (Smart Notes / Naya Notes / Activity), boards, persistent bottom bar.
- **Exact change:** the card renderer (`pageBody` + `pageHtml`) is replaced with a renderer that serves the Personal page template harvested byte-for-byte from live v9, with only the citizen's labels swapped in (name, words, cover); the narrow card shape is deleted.
- **Exact measurement:** 12/12 sisters' Personal pages render the full Personal page board-by-board (cover 1, photo slot 1, pills 3, buttons 10, composer 1, feed tabs 3, boards all, bottom bar 1) with the verdict SAME against live nayanet.app/personal; 1 fresh walk-through citizen's 3 pages render the same world; Business/Space sampled on 3 sisters (one per voice A/B/C); zero overflow at 1440/390/360, zero console errors; every button clicked, every destination recorded; the sisters' Box data reads back word-for-word after the round.
- **What must NOT be there:** the narrow centered card; the static bio essay as the page; the single "Back to your Hub" button as the only action; any gray text; any invented board, button, or pill; any sisters-only special shape; any different world for any citizen.
- **Scope boundary — do NOT touch:** the sisters' Box data; the walk's ten questions, names page, end slide, Hub, claim/join flow; the live Personal page; live anything; the bottom bar's design (harvest it as it is — the bottom-icons round owns the bar).

**Verification (the builder runs this before handoff):**
- In a real browser. Phone first (390px), desktop second (1440px). Scroll 0 AND scrolled.
- Every button clicked, every destination recorded. Screenshots or it did not happen.
- The design-contract gate measurements (§2) + the anatomy six-question test, both in the handoff.
- **Standard verification plan (every brief names it):** Playwright, desktop 1440 + phone 390 + true 360, zero overflow, zero console errors, named no-regressions.
- **The Self-Check Law governs verification.** The maker checks their own work THREE TIMES (each round finding NEW things; below honest 9+ → fix it yourself), answers the seven pre-merge questions IN WRITING (`~/workspace/team-nitro/PRE-MERGE-QUESTIONS.md`), then the CAPTAIN double-checks before it reaches Shawn and before the maker merges. The maker merges their own work. Shawn's eye is the final gate for how a page LOOKS. The captain refuses to present a build without the gate measurements + the anatomy answers.
- **Named no-regressions:** the walk's ten questions; the names page; the end slide; the Hub cards list; the claim/join flow; the sisters' Business and Space pages; the sisters' Box data (byte-unchanged); the live Personal page (untouched).

**DONE MEANS COMPLETE — THE FINISHING LAW.** A page is not done until every button navigates to its real destination and works (proven by clicking each one in a real browser — a button that goes nowhere, or to a stale or wrong place, is a defect, not a polish item), all content is filled with real content (nothing half-done, nothing placeholder), and everything is synced to the real systems (the updated real Dashboard, the real feeds, the real data). The captain inspects every button herself before anything reaches Shawn's eyes.

## §7 — THE WORK

- **Task:** replace the walk's card renderer with a renderer that serves the Personal page itself, so every citizen's Personal page IS the Personal page — then prove it on all twelve sisters plus one fresh citizen.
- **Shawn's words:** his 04:01Z law and his 04:16Z sharpening, in substance, as given in the Situation section above — the sisters' pages are the Personal page exactly, and everybody gets the same world, just different labels.
- **Order / source:** his 04:01Z law; his 04:09Z press ("if your pages look like this page then we're good" — https://nayanet.app/personal); his 04:16Z sharpening; the 04:11Z browser verdict DIFFERENT.
- **Deliverable:** the fixed build script + the rebuilt worker file + record + scorecard + seven pre-merge answers, filed on branch `sisters/personal-pages-20261113` from the current main tip (re-read first-hand). Work in `team-nitro/sisters-personal-pages-20261113/`.
- **Constraints:** no deploy, no merge, no PR, no mail, no live touch, no GitHub writes to main. Staged only. The fixed worker file goes to the captain with its sha; v23 is the deploy vehicle; this round does NOT deploy.
- **Report back:** where the fixed files live, the measurements, DONE and NOT-DONE together — and the lineage proof (which build script generates the deployed bytes) stated in one line.

### BASE FILE

Base file: `~/workspace/team-nitro/walk-questions-10-20261112/build-beginning-staging-worker.py` — the maker edits this file; never rebuild. The worker `.js` is a GENERATED artifact: the build script regenerates it from its embedded template string, so editing the `.js` alone silently reverts on rebuild. The maker edits the template inside the build script, rebuilds, and verifies the generated worker file is byte-identical to the hand edit. Lineage proof first: if the step-1 proof names the S2 build script instead, that script is the base file and the record says why.

### HOST PAGE

Host page: the walk staging worker's `/pages/<alias>/<slug>` route — the page rendered there IS the Personal page, served with the citizen's own labels; it duplicates nothing, because it IS the template. Never a standalone page: this work builds no new page and no separate page; it fixes the renderer on the route that already serves every citizen's pages.

### THE STEPS (in order — do not skip step 1)

1. **PROVE THE LINEAGE + MAP THE SLOTS (before building).** Byte-compare the deployed staging worker's `/pages/` output against both candidate build scripts' renderer regions and name which script generates the deployed bytes. Read live Personal v9 first-hand and name, in the record, how the page takes identity, cover, photo, words, pills, feed, composer, bottom bar — and how the renderer supplies each from the Box answers (about → story; into/vision/mission/motto/goal → sections/boards; biz_* → Business; space → Space). The exact mapping is the maker's, stated in the record before building. Search for static per-sister page files (repo, worktree, proof host) and report the result — this is the (a)-vs-(c) trigger. Reconcile the build script's walk-sha assertion first-hand: the walk file now hashes `be55a494` (Q10 gold fix, filed 04:15:30Z) while the script asserts `a3510446`; the maker reads the walk file's sha first-hand and updates the assertion only to the bytes that are there.
2. **REBUILD THE RENDERER.** Replace `pageBody` + `pageHtml` in the base file's template with a renderer that serves the Personal page template (harvested byte-for-byte from live v9) with only the citizen's labels swapped in. All three kinds render as the Personal page: Personal says "My Story", Business and Space say "Our Story", each with its own words and its own cover. Cover rule: each sister gets her smart cover in the cover banner; the fresh citizen gets the default cover until she picks one; never empty, never a gray band. Photo rule: the initial orb by default (members are their initial by default); a face only by the citizen's own choice. Pills: the same three membership pills as live Personal; never invented, never removed. Feed: the citizen's own feed; the empty state is honest ("No posts yet" only if truly no posts — the data state, not a placeholder). Bottom bar: harvest live at build time; if the bottom-icons round's staged bar has landed first, harvest that — never build a second bar.
3. **STAGE.** Rebuild the worker, verify byte-identical, hand the fixed worker file to the captain with its sha. This round does NOT deploy.
4. **PROVE.** Playwright at desktop 1440 + phone 390 + true 360, scroll 0 AND scrolled, zero overflow, zero console errors: all twelve sisters' Personal pages board-by-board against live nayanet.app/personal (verdict SAME); one fresh citizen walked end-to-end from the login page, all 3 of her pages; Business/Space sampled on 3 sisters (one per voice A/B/C). Every button clicked, every destination recorded. The sisters' Box data reads back word-for-word after the round.
5. **RECORD + SCORECARD + SEVEN ANSWERS.** Record, scorecard, and the seven pre-merge questions answered in writing, filed on the branch. Honest score; below 9 never reaches Shawn's eyes.

---

*Brief written 2026-11-13 by the sisters' Personal-pages brief-writer seat. Grounded in: live Personal v9 re-harvested first-hand 2026-11-13 ~04:15Z (1,484,185 B, sha `992ab18c`); the card renderer read first-hand in both candidate build scripts; the S2 record; the clone record; the 04:11Z browser verdict DIFFERENT; Shawn's 04:01Z law, his 04:09Z press, and his 04:16Z sharpening (the same world, just different labels).*
