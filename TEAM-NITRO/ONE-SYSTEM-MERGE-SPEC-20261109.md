# THE ONE-SYSTEM MERGE SPEC — Onboarding + Smart Factory + Project Intelligence + Operation Manual + Design Law, in the Factory

**Status:** SPEC — the map for the merge, not the merge itself.
**Date:** 2026-11-09.
**Order:** Shawn, 21:39Z and 21:40Z Nov 9 — the onboarding flow, Smart Factory, Project Intelligence, and the whole operational and design law systems need to come into one.
**What this document is:** the exact detail of how five parts that live separately today come into ONE system, housed in the Factory — where each part lives, what order a Naya operates them in, and how the build flow connects them.
**What this document is not:** it does not move files, rewrite pages, or change any live system. The merge itself — moving the parts into one home — is a later build, on Shawn's word.

---

## 0. THE ONE SENTENCE

**Title:** Five parts, one home, one order.
**Subtitle:** Read the manual, fill in your intelligence, click build.
**Nutshell:** The Operation Manual, the Factory inventory, Project Intelligence, the design law, and the onboarding flow are parts of each other, and they all live in the Factory. A Naya reads the manual first, then opens Project Intelligence, then builds. A citizen answers fifteen questions — or lets Naya answer them — and clicks build, and the page comes out with everything they put in. Nothing here is a new system. It is the system that already exists, put in one home.

---

## 1. ONE SYSTEM, ONE HOME — THE FACTORY HOLDS IT ALL

**Title:** The Factory is the home, not a new app.
**Subtitle:** Five parts, each with its address.
**Nutshell:** Nothing new is built to hold this together. No new app, no new database. The Factory — the place that already holds the parts, the inventory, and the language — holds the rest too.

| # | Part | What it is | Where it lives in the Factory |
|---|---|---|---|
| 1 | **The Operation Manual** | How to operate NayaNET, in exact detail: smart notes, Naya Notes, daily reports, creating a page, Smart Mail, what every part does. The first thing a Naya reads. | `TEAM-NITRO/NAYANET-OPERATION-MANUAL.md` — the Factory's operating book, filed in GitHub, read before anything else. |
| 2 | **The Factory inventory + piece index** | The parts themselves and the canon of which parts are real. The Inventory says WHERE a part lives (file + line). The Piece Index says WHETHER it is real (canonical, verified, retired, superseded). | `TEAM-NITRO/THE-INVENTORY.md` (51,329B, current on main) and `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/CANONICAL-PIECE-INDEX.md` + `.json` (154 canonical of 571 unique IDs). |
| 3 | **Project Intelligence** | The living queue and the build input. The one list of what is directed, what is in motion, what is proven done — and the intelligence a citizen hands over to get a page built. | `~/workspace/project-intelligence/` — `ACTIVATION.md` (the discipline), `state/state.json` (the single source of truth), the Living List artifact `everything-you-directed-the-living-list`, live at nayanet.app/pi. |
| 4 | **The design law** | The laws every build follows: the Real Object Law, the Playbook (the HOW), the Intelligence Report (the WHY), the Act, the Intelligent Block Rules, the brand, and the design-contract gate that measures every check. | The law files named in §5, read in the order the Factory Activation Manual sets (§2): Playbook → Intelligence Report → Inventory → Piece Index → Real Object Law + Intelligent Block Rules. The gate itself: `~/workspace/team-nitro/design-contract-gate/check-gate.py`. |
| 5 | **The onboarding flow** | The welcome process: the 10 questions that fill in the content for a citizen's pages, ending at "you got your pages." Onboarding IS Project Intelligence — the input that builds the world. | The flow defined in §4 of this spec; its build spec is SN-2580 (the whole picture), SN-2581 (the creation flow), SN-2582 (the done-for-you house). The universal app it feeds is queued after Dashboard done-done + all pages done. |

**Why the Factory is the home:** the Factory already holds the parts and the language every Naya builds in. The Manual tells a Naya how to operate; the inventory tells her where the parts are; PI tells her what to build and with what intelligence; the design law tells her what is good enough; onboarding is the front door a citizen walks through. Putting them anywhere else would make a second system — and the one-flow law forbids that: use the system that is already there, complete the parts, sync them up.

**The Factory Activation Manual is the second book.** The Operation Manual teaches a Naya how to operate NayaNET. The Factory Activation Manual (`TEAM-NITRO/SMART-FACTORY-ACTIVATION-MANUAL-20261109.md`, 70,679B, also held in the Factory's own Smart Box — 16 blocks) teaches her how to build in the Factory, in the same language, from the same parts, alone. A Naya reads the Operation Manual first, then the Factory Activation Manual when she builds. Both live in the Factory. Neither is a separate system.

---

## 2. THE OPERATING ORDER — MANUAL FIRST, THEN PI, THEN BUILD

**Title:** The first thing a Naya does, every time.
**Subtitle:** Read, then intelligence, then build.
**Nutshell:** The order never changes. A Naya reads the Operation Manual first so she knows how everything operates. Then she opens Project Intelligence. Then she builds. Skipping the manual is how a Naya builds the wrong thing in the right language.

1. **Read the Operation Manual.** Before any operation, any note, any mail, any build. It is the activation document: how to enter a smart note, how to enter Naya Notes, how to enter daily reports, how to create a page, how to use Smart Mail, what every part does, and the daily operating loop. A citizen gets it when they connect their Muse; a Naya reads it when she wakes.
2. **Open Project Intelligence.** The Living List is the one queue: what is directed, what is in motion, what is proven done, what needs his hands. A Naya claims her item before she touches it, and lands it only with proof — a done item without proof renders as in-motion with a "proof missing" marker. Items in `needs-his-hands` move only when he moves them.
3. **Build — from the Factory, by the law.** Take the parts from the inventory and the piece index (harvest first, never invent; compose, don't create; take the shown object verbatim). Build viewpoint by viewpoint, by the Live Viewpoint Method. Run the design-contract gate (§5). Show it only when it is ready — and his eye is the final gate.

**The five gates run before every consequential action, in this order and in every seat:** Is it right? Is it what they truly need? Is it mine to do? Is now the time? Can I prove it? Any gate no — stop, say why, propose the wise path.

---

## 3. THE PI BUILD FLOW — FIFTEEN QUESTIONS, THEN CLICK BUILD

**Title:** Fill in your intelligence, click build, get your page.
**Subtitle:** Fifteen questions by default — and we answer most of them for you.
**Nutshell:** PI is connected to ALL the pages. Open any project, fill in your project intelligence, click build — and the page comes out with everything you put in. Nobody gets stuck on a question. Ever.

### 3.1 The flow, step by step

1. **Open any project.** Project Intelligence opens on the project you want to build — a Personal, a Business, a Space, a Group, a Membership page. PI is connected to all the pages; you say which page you want to build.
2. **Answer the 15 questions.** By default, PI asks fifteen questions — the same count as the MAXESS scoring engine, because fifteen is enough to know a world and few enough to finish. The questions cover what the page needs: your vision, your goal, your mission, what the page is for, what it does, who it is for, your social links, your images, your logos, and any special colors or styles you want.
3. **We fill in the rest for you.** You answer the fifteen, and the system fills in the rest — the structure, the standard blocks, the defaults — from the template.
4. **Click build.** When you are done, you click build, and it builds the page with all the intelligence you put in: vision, goal, social links, images, logos, special colors and styles — everything.

### 3.2 How a question works — three ways in, never stuck

Under every question, three ways to answer — and the question comes already answered:

- **Enter it in your own words.** Type it in, or dictate it in.
- **Click multiple choice.** Pick from the choices. No typing needed.
- **Edit what is already there.** Every question comes pre-answered in a standard template where most of it is already filled out. You just edit it: change what you want, leave the rest. A default line, a copy-paste example, a choice — always there, so nobody sits staring at a blank question wondering what to say.

**Nobody gets stuck on a question.** That is the law of this flow. If you do not know what to say, the template says it for you and you edit it. If you do not want to type, you click. If you do not want to choose, you leave the default.

### 3.3 Page by page, as much as you can — partial is fine, empty is allowed

- **Go page by page.** The questions come page by page, one screen at a time. Fill out as much as you can.
- **Partial input builds.** If you cannot fill it all out, it builds with what you gave, and you fill in the rest later. A half-filled page is a page; the rest is added when you are ready.
- **Empty is allowed.** You can go all the way through without putting anything in — we do not stop you. You just would not have much: a page with the structure and the defaults, and none of your intelligence in it. Total flexibility. We recommend answering all the questions and giving as much input as possible — but the system never blocks you for giving less.

### 3.4 Naya fills it for you — the simple ways in

Five simple ways to get your intelligence into PI, easiest first:

1. **Tell Naya.** If she is connected already, just tell her: fill out my mission and goal for this page. She does it. The whole thing can be automated — she knows you, she knows the page, she fills it in.
2. **Have Naya write your About for you.** She writes it; you edit it or accept it.
3. **Copy-paste it.** Have Naya write it somewhere else and paste it in.
4. **Type it in.** Your own words, directly.
5. **Dictate it in.** Speak it; it goes in.

A child could get a smart page up and running with their information in it. That is the bar. If a child cannot do it, the flow is not simple enough yet.

### 3.5 What the build puts in the page

The page comes out with everything the citizen put in: vision, goal, mission, what it is for, what it does, who it is for, social links, images, logos, and any special colors or styles asked for. The structure comes from the Factory's parts — the page is built from the inventoried pieces, not drawn fresh. Customization after the build uses the same parts: add a block, add a button that goes into a block, add a function — the Factory has them.

---

## 4. ONBOARDING FEEDS PI — THE FRONT DOOR

**Title:** Onboarding IS Project Intelligence.
**Subtitle:** Ten questions in, your pages out.
**Nutshell:** The welcome process and PI are the same thing. Onboarding asks the questions; PI is the answers; the build is the pages. Onboarding ends at "you got your pages."

### 4.1 The onboarding flow

- **The welcome process has 10 pages, then the pricing.** The 10 onboarding questions fill in the content for the Personal, the Business, and the Space: what they are into, what their business is, their personal goals, missions, visions — and for their space, all the information. Then you create their world.
- **Onboarding ends at "you got your pages."** When the questions are answered, the pages exist. That is the end of onboarding — not a dashboard tour, not a checklist. Your pages.
- **Creating a new Space runs the same flow.** Click to create a new Space, and it asks the questions page by page — fill it out, copy-paste from Naya, or type it in — and it automatically creates that page. Very similar each time, maybe custom for each.

### 4.2 The creation flow (SN-2581) — push-button simple

"Create whatever world you want." Goal, mission, vision, functions. Then: do you want to add any smart notes or notes? A citizen may have been working on the project and have notes related to it — boom, add them. The system analyzes the notes and the smart notes and creates the page. Then: do you want to pin the smart notes to the page and have them create your Intelligent Library?

- **Everybody gets an Intelligent Library.** PI builds the Library AND fills out the About AND creates content related to their topic or business. The Library tells a visitor all about that Space, Personal, or Business.
- **Related smart notes live in two places:** they show on the citizen's feed AND they can be pinned in the Intelligent Library.
- **The visitor, right from the start:** go to the Library, look on the feed, click About, join them, message them — everything from the first moment.

### 4.3 The done-for-you house (SN-2582) — we build it and fill it

We create the house and we fill it too, on their behalf: a done-for-you set-up business and home and community. Push-button simple for anybody to join: click connect, message them, and they show up in your connections, all organized for you. Connect with their spaces, their business, their personal feed; join their membership if you wish, or they join yours — free or paid. The system is built for the three things people want from the internet: connect with people, knowledge (intelligence), and make money. We cover all three. We simplify the whole process.

### 4.4 The universal app — what onboarding builds

There is the Hub, there is a Dashboard, and there is ONE universal intelligent app that morphs into all the interactive hub pages — Personal, Business, any Space topic, any Group topic, any Membership. They are pretty much all the same page; the only difference is the label in the front, because any of them can have a goal, a mission, a vision. Membership is not a separate page — it is a feature of the Personal, the Business and the Space, with a login. The universal app is queued after Dashboard done-done + all pages done. Onboarding is how a citizen gets it: give your Project Intelligence, click build, boom — the app exists. Then customize it with parts from the Factory.

### 4.5 The creation flow — first time and later

**Title:** Onboarding makes your original pages. The Factory makes your next ones, one at a time.
**Subtitle:** Three apps to start. One page at a time after that. It is a big circle.
**Nutshell:** The first time, onboarding creates your original pages. Later, you go to the Smart Factory, pick what kind of page, and onboarding runs again — one page, one at a time. Every page gets its own mission, goal, and vision. Anything you do not want is optional. And everything you make connects back to your world.

- **First time — onboarding creates your ORIGINAL pages.** The one-time onboarding (§4.1) creates the pages you start with: Personal, Business, Space. Three apps to start.
- **Later — the Factory creates your next page.** To create MORE pages later, you go to the Smart Factory → click "create new smart app" → it asks Personal, Business, or Space → you choose one → it triggers the onboarding process AGAIN → asks all the questions → creates that page for you.
- **Individually, not all at once.** One page at a time: do your Space, then your Personal, then your Business — one at a time. Never a batch. Never three at once.
- **Mission, goal, vision — one of each, per app.** When the flow asks for mission, goal, and vision, it asks for ONE for your Personal, ONE for your Space, ONE for your Business. We guide them through it — asking for each in turn — and it fills out all three. Each page has its own mission, goal, and vision; they are never shared across the three.
- **Optional — skip what you do not want.** No business? Choose not to answer for the business. Do not want a Space? You do not have to. We offer three spaces; use all three if you want, fewer if you do not. An unanswered app is simply not created — never a half-empty page you did not ask for.
- **Leftover slots — add another later.** Only created a Personal? Two slots are left. Go into the Smart Factory later and add another — maybe a private profile and a public profile. The slots wait for you; nothing expires.
- **It all works in the same thing — a big circle.** Smart Factory → create a smart app → what kind? → answer all the questions and input → create another space → that space or profile is connected to your profiles → it shows up in your menu, in your profile, in your business, as "in your world" — in your world tab. The page you make connects back to everything you already have. It is a big circle: the Factory makes the page, the page joins your world, your world is where you make the next page.

---

## 5. THE DESIGN LAW GATES EVERY BUILD

**Title:** Nothing ships that fails the gate.
**Subtitle:** The law is the habit, not a choice.
**Nutshell:** Every build — every page, every viewpoint, every block — follows the same law and passes the same gate. A gate that fails is not done. A deferral is an open item with a name, not a pass. And Shawn's eye is the final gate.

### 5.1 The law, in the order a Naya reads it

| # | Document | What it is | Where it lives |
|---|---|---|---|
| 1 | **THE-PLAYBOOK.md** | The HOW. The formula, the steps, the laws. | `~/workspace/team-nitro/THE-PLAYBOOK.md` · GitHub `BRAIN/10-INTERFACES/THE-PLAYBOOK.md` · SN-0844 |
| 2 | **DESIGN-INTELLIGENCE-REPORT.md** | The WHY. What was got wrong, what was learned. | `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` · GitHub `BRAIN/10-INTERFACES/DESIGN-INTELLIGENCE-REPORT.md` · SN-0843 |
| 3 | **THE-INVENTORY.md** | The PARTS. Every design law + every piece, with file + line. | `TEAM-NITRO/THE-INVENTORY.md` |
| 4 | **CANONICAL-PIECE-INDEX.md** (+ `.json`) | The CANON. The one list of which pieces are real. | GitHub `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/CANONICAL-PIECE-INDEX.md` (+ `.json`) |
| 5 | **THE-REAL-OBJECT-LAW.md** + **intelligent-block-rules-LAW-20261106.md** | The LAW. Real objects, and what an intelligent block is, section by section. | `~/workspace/team-nitro/laws/THE-REAL-OBJECT-LAW.md` · `~/workspace/team-nitro/hub-board-edit/intelligent-block-rules-LAW-20261106.md` |

Supporting law files (read when needed, not before the first build): `THE-NAYA-BRAND.md` (the brand: real objects, obsidian gloss black, ALL buttons elite and lit the same, every number alive) · the Clarity Confirmation Act (DRAFT — official only on Shawn's word) · the design laws and language files named in the Factory Activation Manual §2.

**The activation habit:** before ANY design work, read the Playbook and the Intelligence Report. Locked-in knowledge you do not read is forgotten knowledge. Then ask the three questions — is every position calculated? Does it feel like a machine? Can you get it in 2 seconds? — and only then build.

### 5.2 The Real Object Law

Every element is a real physical object. Not a flat shape with effects. Not a diagram. If it does not look touchable, it does not ship. If it does not feel real, it is not done. Seven principles: everything is an object · one light source (top-left) · real materials (obsidian glass, brushed metal, light with volume) · real shadows (objects sit ON the page) · touch = physical response · speak in objects (icons, circles, boards, buttons, minimal text) · viewport is the stage.

### 5.3 The Factory laws L1–L8

The named set that governs how a Naya writes, speaks, tests, and builds in the Factory: **L1 stranger test · L2 perfect-words law · L3 title + subtitle + nutshell · L4 Naya speaks, faces alternate** (alternation is judged on the SEQUENCE — after any move, re-check it on the new order) **· L5 the test in his head · L6 `##` note format · L7 the one ultimate ten · L8 the reusable-parts law** (every part reusable, rebuildable, clonable — clone a page, replace some parts, move some parts around; parts universal, a family of the Naya design; every part triple-A: active, living, depth, alive).

### 5.4 The design-contract gate — measured in every check, never a vibe

The machine gate (`~/workspace/team-nitro/design-contract-gate/check-gate.py`) measures the rendered page against:

- **(a)** Zero white/light backgrounds anywhere on the page — every background obsidian/dark.
- **(b)** Every element raised/elevated — real depth, real lift, real light.
- **(c)** Gauges present and alive — the speedometer language on the numbers.
- **(d)** No text-in-image, no pasted document.
- **(e)** No bare text blocks — every long text broken up, scannable, in elevated blocks that light up.
- **(f)** No look-alike buttons or boards — every element distinct in purpose and presentation.
- **(g)** Note format — smart notes in the `##` format, or they never land.
- **(h)** No dictation-blunt phrases — nothing pasted raw from dictation; the banned list holds only what Shawn flagged.
- **(i)** Title + subtitle + nutshell on every section, Naya speaking in first person, faces alternating left then right down the page, distinct faces.

Plus the human checks, attested on every verification: **H1 stranger test** (a person who has never heard of NayaNET — does she completely GET it, BELIEVE it, TRUST us enough to come in?) · **H2 perfect-words law** (the words speak to the child, the grandma, everyone, in a simple direct understandable way) · **H3 face quality** (her face, real, alternating, distinct) · **H4 the test in his head** (is this ten-star service, would somebody see value in it and trust it?) · **H5 the one ultimate ten** (one set of ten, each pain + solution + what's in it for you).

**The gate is blocking.** A gate that fails is not done. A deferral ("captain's decision for later") is an open item with a name, not a pass. Pre-existing failures that are calibration items do not block a freeze; the gate stays blocking for NEW failures. And the gate is not the final gate: **Shawn's eye is the final gate.** A seat's scorecard or verification is preparation, never proof — the only verification is his eye, on the live viewpoint, in front of him, phone first.

### 5.5 Harvest first, never invent — the build rule

Every build takes its parts from the inventory and the piece index, verbatim: same HTML structure, same CSS values, same JS behavior. Adapting content (menu items, labels, copy) is allowed; restyling the component is not. When Shawn SHOWS an object — a screenshot, a link, a page — the deliverable IS that object: same shape, same colors, same jewel, same glow, placed on the page. Recreating it "in the same spirit" is inventing. If no part exists for the job, that is a GAP — file it, do not invent it.

---

## 6. THE PUBLISHING LAW — PRIVATE AUTO LIVE, PUBLIC APPROVED

**Title:** Your page is yours the moment you make it. The network decides what goes public.
**Subtitle:** Private goes live at once. Public gets verified.
**Nutshell:** A page a citizen makes is live privately the moment it is made — no approval, no wait. It goes public on the network only after the network approves it. First we verify by hand; then a machine scans it, and if it passes the safety test, it goes live.

- **Private = auto live, immediately, no approval.** A citizen's own page, for themselves and the people they invite, goes live the moment it is built. No gate, no wait.
- **Public = approved and verified by the network.** If a citizen wants their page public on the network, it has to be approved. They ask for it; the network verifies it.
- **At first, we verify by hand.** A human (a Naya, on the network's behalf) looks at the page and checks it.
- **Then, an automated safety scan.** A process scans the page's address and looks for anything not right: errors, code that is not good, foul language, anything that should not be public. If it passes the safety test, it goes live. If it does not pass, it stays private, and the citizen is told what failed.
- **Custom is allowed; custom is not automatically public.** A citizen can custom-make their own URL or their own page the way they want — yes. But a custom page is private until it is approved, like any other page. Making a page never makes it public by itself.
- **This is not a fully-custom-pages franchise.** The model is finished pages, cloned and customized — not bespoke builds. Customization is choosing parts and editing the template; it is not a new page built from nothing.

---

## 7. ONE FLOW WITH THE REST OF THE SYSTEM

**Title:** The merge is one flow, not five systems in a trench coat.
**Subtitle:** Notes, Box, nodes, feed, Factory — one thing.
**Nutshell:** The merged system is not separate from the rest of NayaNET. It is the same one flow: notes feed the Box, the Box is the memory, the nodes are the organs, the feed is where notes are read, the Factory builds with the parts.

- **The notes and the Smart Box are one system.** The notes in GitHub and the Smart Box are one flow, not separate systems. The system operates as: understand (identity) → learn → grow → know → evolve — so Naya learns, grows, understands, retains, and the system actually works like one thing. The notes are a direct part of the Smart Box — her smart memory, her organizational system. Do not build a separate system: use the system that is already there, complete the parts, sync them up.
- **The nine nodes are the organs.** The nine Naya Nodes are the nine master contracts in GitHub `NAYANODE/` — LEARN · KNOW · ACT · LAW · VERIFY · SELF · CONNECT · EVOLVE · PROVE — with `0000-NINE-NODE-GENOME-MASTER-INDEX-V2.md` as the DNA. The canonical kernel runs SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE. The nodes are intelligence processors — the organs. The notes are the units of intelligence the organs process. A new thought does not grow a new organ.
- **The chain:** Note → Block → Feed → Box → Ledger → Dashboard → Auto-Match → Smart Link → Factory. A thought becomes a note; the note becomes an intelligent block; blocks flow into feeds; the Box stores and organizes them; the Ledger records every action in and out; the Dashboard shows the person their world; Auto-Match connects them with like minds; Smart Links carry them out into the world and track what happens; the Factory turns finished pages into templates that build the next pages. Each part is ultimate, or the promise breaks.
- **"In" means on the Smart Feed.** A smart note counts when it is ON the Smart Feed — that is when it is official, when it is in. Filing to GitHub alone is not in. Every smart note is verified live on the feed before it is reported done.
- **The end state — stop creating pages.** Get to the point where ALL the pages are already created and we are not creating pages anymore — we are just cloning them or adding a page, and we can customize that page, or leave it. Cloning is a button click, not the achievement — any system can clone a template. The achievement is the finished pages + the shared language + the inventory: the thing that lets us stop creating pages. The Factory's job is to finish the set of pages, so there is nothing left to create — just clone, customize, or leave it.
- **How multiple Nayas work the same interface.** The pages sit in GitHub — that is the single source of truth, and the collective builds from it. But GitHub is versioned files, not live co-editing: two Nayas on the same file at the same time is a conflict, resolved by merge, not live. So it is one Naya at a time per page, or different pages and branches. In the end state the question mostly disappears: everyone works on their own clone; the shared thing is the TEMPLATE — the Factory's parts — not the live page.

---

## 8. WHAT THIS SPEC DOES NOT DO

**Title:** The map, not the move.
**Subtitle:** Nothing here changes a live system.
**Nutshell:** This spec defines the merge. It does not perform it.

- It does not move any file, rewrite any page, or change any live system.
- It does not build the merged Factory, the PI build flow, or the automated safety scan. Those are later builds, each on Shawn's word, each with its own brief, each verified by his eye.
- It does not merge any pull request, deploy any worker, or change any database. Merges are his hand.
- It does not claim the merge is done. This seat writes the SPEC. The merge build is later.
- It does not invent any part, page, or component. Every part named here is harvested from a named source (§9). If a part named here does not exist yet, it is a GAP to file — not a part to invent.

---

## 9. SOURCES — EVERYTHING IN THIS SPEC COMES FROM HERE

| Source | What was taken from it |
|---|---|
| Operation Manual — `TEAM-NITRO/NAYANET-OPERATION-MANUAL.md` (blob `cdd81493`, 43,109B) | The operating order, the system in one picture, the chain, the one-flow law, the note and mail rules. |
| Factory Activation Manual — `TEAM-NITRO/SMART-FACTORY-ACTIVATION-MANUAL-20261109.md` (blob `3c026b68`, 70,679B) | The five documents to read first, the clone-build flow, the design laws L1–L8, the gate (a)–(d), the reusable-parts law. |
| The Inventory — `TEAM-NITRO/THE-INVENTORY.md` (blob `72e03613`, 51,329B) | The parts list, the design laws, the locked-in smart blocks. |
| Piece Index — `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/CANONICAL-PIECE-INDEX.md` (+ `.json`, blobs `0e63b241` / `a50ef2dd`) | The canon: 154 canonical of 571 unique IDs. |
| Project Intelligence — `~/workspace/project-intelligence/ACTIVATION.md` + nayanet.app/pi | The discipline (claim, proof, block, one queue), the refresh cycle, the state schema, the Living List. |
| Design law — `THE-NAYA-BRAND.md` · `THE-PLAYBOOK.md` · `DESIGN-INTELLIGENCE-REPORT.md` · `intelligent-block-rules-LAW-20261106.md` · `clarity-confirmation-act-DRAFT-20261106.md` | The brand, the HOW, the WHY, the block rules, the Act (DRAFT). |
| SN-2580 — The Universal App + Onboarding + Factory + PI | The whole picture: Hub + Dashboard + one universal app; onboarding is PI; the Factory is the parts. |
| SN-2581 — The Creation Flow, Push-Button Simple | Goal, mission, vision, functions; add notes; analyze; create; pin into the Intelligent Library. |
| SN-2582 — The Done-For-You House | We build the house and fill it; the three things people want: connect, knowledge, make money. |
| The one-flow law + nine nodes (Shawn, 21:07–21:18Z Nov 9) | Notes and Box are one system; the nine master contracts in `NAYANODE/`; kernel/ is the running code; BRAIN/ is the organized brain; KNOWLEDGE/ is the distilled design corpus. |
| The publishing law (Shawn, 21:31Z Nov 9) | Private auto live; public approved — manual verification first, then an automated safety scan. |
| The PI build flow (Shawn, 21:39Z Nov 9) | Fifteen questions by default; pre-filled template; own words or multiple choice; page by page; partial OK; empty OK; Naya fills it for you. |
| The merge order (Shawn, 21:39–21:40Z Nov 9) | Onboarding + Factory + PI + operational systems + design law systems come into one, housed in the Factory. |

---

## APPENDIX — THE PROOF TEST (five questions a fresh Naya must answer from this spec alone)

A fresh agent, given ONLY this spec, must be able to say:

1. **(a)** Where each of the five parts lives inside the Factory — Operation Manual, inventory + piece index, Project Intelligence, design law, onboarding flow (§1).
2. **(b)** The order a Naya operates them — manual first, then Project Intelligence, then build (§2).
3. **(c)** The 15-question PI build flow with its rules — fifteen by default, pre-filled template, own words or multiple choice, page by page, partial OK, empty OK, Naya fills it for you (§3).
4. **(d)** How onboarding feeds PI — the 10 onboarding questions fill in the content; onboarding ends at "you got your pages"; creating a Space runs the same flow; PI builds the Library, the About, and related content; the creation flow — first time (onboarding → original pages) and later (Factory → choose kind → onboarding again → one page, one at a time), per-app mission/goal/vision, optional answers, leftover slots, and the world tab where it all connects (§4.5).
5. **(e)** How the design law gates every build — the five documents in order, the Real Object Law, Factory laws L1–L8, the design-contract gate (a)–(i) + H1–H5, blocking, Shawn's eye the final gate (§5).

If a fresh Naya cannot answer all five from this spec alone, the spec is incomplete — not the Naya.
