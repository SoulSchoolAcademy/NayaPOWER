# THE NAYANET BLUEPRINT V1 — AI TONGUE (build contract)

**Audience:** a cold Naya seat. Execute from this document with zero guessing. Where a value is not stated here, it is not yours to invent: escalate as a named job.
**Companions:** `.human.md` (the why) · `.machine.json` (the same truth as data — schema `nayanet-blueprint/1`).
**Status map (binding):** DESIGN_DNA = RATIFIED 2026-10-31 · VALUE_TABLE = LOCKED 2026-10-31 · THREE_MINUTE_MISSION = RULED 2026-10-31 · DREAM_TEAM = ADOPTED 2026-10-31 · WOWIE_RULE = STANDING 2026-11-01 · INTERFACE_FRAMEWORK = PROPOSED (NOT ratified) — DNA governs on any conflict until ratification.

## P0 — PHILOSOPHY AS CONSTRAINTS

- P0.1 Ten-star is holistic: dimensions = {look, feel, vibe, logic, intelligence, effectiveness, usefulness, helpfulness}. Score(screen) = min(dimensions). Any dimension < 10 ⇒ screen < 10.
- P0.2 ALIVE: a surface MUST move only on real events (ledger events, real state changes, direct touch). Decorative motion = defect. Motion not driven by data = gate failure (see G8).
- P0.3 Precious Data: every datum is presented as the most precious data in the universe. Operational form: SN-0822 (P5.1) + Vitality Law (P5.2). No bare numbers, no text walls describing life.
- P0.4 OS-for-Naya: human input ∈ {word, tap, wish}. All machinery runs agent-side. Human-facing output MUST be push-button simple; never expose process.
- P0.5 Franchise law: one canonical component per element type, imported everywhere. Local variants = defect. Approved pages (Life with Naya · certificate page) are the element library; reuse their actual elements. FIX MEANS FIX: corrections are recompositions of the existing build; authoring a substitute = failure even if it functions.

## P1 — LANGUAGE

### P1.1 Vocabulary (normative)
| Term | Definition |
|---|---|
| screen | One viewport, one complete thought; the unit of experience and of verification. |
| hero | The single element the screen exists to show. Exactly 1 per screen. |
| supporting | Context serving the hero. Count ∈ [0,3]. Never competes with hero. |
| action | A user verb on the screen. Count ∈ [1,2] primary. Bottom zone. |
| ambient | Quiet metadata at the edges. Never demands attention. |
| part | A pre-made element/function with a contract (P3.1). |
| blessed part | Part with part-level scorecard ≥ 9.0 recorded once; instances inherit proof, sample-checked. |
| recipe | A screen's build contract: slots → blessed part IDs + data bindings by contract name. |
| shell | The single chassis: Smart Bar system (P2.4). No per-app bars. |
| gate | The executable checklist (P4.4, P5.4) run on the assembled screen. Fail ⇒ no ship. |
| bullseye | The written finish line, recorded before work starts. No bullseye ⇒ no work. |
| proof | Attached evidence: render, measurement, or reconciliation. Claims without proof = UNVERIFIED. |
| done_proven | Completion state: proof verified by a checker who is not the maker. |

### P1.2 Design DNA (RATIFIED) — binding constraints
- D1 Ground: obsidian black with depth; white text; high contrast. White/light backgrounds FORBIDDEN.
- D2 Living depth: every element is layered (multi-layer borders, elevation, light held inside). Flat 2D = fail.
- D3 Ignition: elements are white at rest; on touch/hover/focus they ignite in their own color. Glow has exactly one job: ignition. Decorative glow = fail.
- D4 COLOR FLOW CYCLE (RATIFIED BY SHAWN 2026-11-01 — supersedes the PR #3141 spectrum walk): color moves in a CYCLE, not a line: [purple → indigo blue (852 Hz) → emerald green (639 Hz) → gold (528 Hz; yellow permitted in icon cases for brightness) → orange (417 Hz) → red (396 Hz) → magenta (963 Hz, the crown) → wraps back to purple]. LEAD = purple. CROWN = magenta. Weekday anchors: purple Sunday · indigo Saturday · green Thursday · gold Tuesday · orange Monday · red Friday. GROUPING LAW: richest shades only; groupings of 3 or 5 (or any consecutive run) MUST keep cycle order; long sequences repeat the pattern; NEVER double a color adjacently; NEVER random order; NEVER backtrack. High-contrast couplings encouraged (purple-green-gold; purple-blue-green). Brand dominant: purple, black, white — most surfaces and most inputs predominantly purple. One color job per element; a color means the same thing on every page, forever.
- D4-P Presentation (same ruling, 2026-11-01): bigger text over smaller; reading text is WHITE, high contrast — light pink / light grey text FORBIDDEN; minimal text, maximal visuals (an icon that says it without words beats words); everything alive and responsive on touch; never flat — always dynamic, multiple dimensions.
- D5 Geometry: boards/cards 16:9; buttons are pills; touch targets ≥ 44px; type floors: body ≥ 16px, UI labels ≥ 14px.
- D6 Law 6 (alive = answers touch): no halo/glow at rest. The jewel orb carries color as identity — solid, no halo; halo only on touch. Presence indicators breathe only while the state shown is actually live.
- D7 Honesty in every state: states = {rest, hover, pressed, selected, loading, empty, error} — all designed, all truthful. Dead buttons FORBIDDEN. SOON permitted ONLY as a non-interactive label; a tappable SOON = dead control = fail.
- D8 Family: one canonical component, imported, never copied or locally varied.
- D9 Two-second read: essence first; if a screen needs explaining, it fails.
- D10 Truth states (Law 2): gold = LIVE/shown · green = PROVEN. Use exactly; do not repurpose.
- D11 Numbers obey SN-0822 (P5.1).
- D12 Element anatomies (buttons 7 layers · boards 6 zones · icons = glyph in jewel chip · inputs sink, buttons rise · composer is ONE canonical part verbatim on every page) are specified in the ratified Anatomy (`BRAIN/10-INTERFACES/NAYA-DESIGN-ANATOMY/`); the first-stock part list is P3.4.

### P1.3 Interface Framework (PROPOSED — apply as working method; DNA wins conflicts)
- F1 Screen Principle: one screen = one viewport = one complete thought. MUST answer in ≤ 2 seconds: what am I looking at / what can I do / why am I here. Scroll reveals the NEXT screen, never the rest of the current one (subject to R2).
- F2 Layers exactly 4: hero (1, 48–72px, center zone) · supporting (∈[0,3]) · actions (∈[1,2], bottom zone) · ambient (edges). A fifth layer = fail.
- F3 Spacing scale (ONLY these values, px): 4, 8, 12, 16, 24, 32, 48, 64, 96. Any other spacing value = fail.
- F4 Type sizes per screen ≤ 3.
- F5 Viewport-fit: APP-class screens fit the viewport, no internal scroll (subject to R2).
- F6 Contrast ≥ 4.5:1 for all text.
- F7 Touch targets ≥ 44px (agrees with D5).

### P1.4 Reconciliations (PROPOSED — until ratified, implement DNA behavior; record which layer you used)
- R1 TWO COLOR LAYERS. Identity layer: each statistic owns one fixed jewel color (P5.3) — answers "which thing is this." State layer: meaning now — framework semantics {gold = score, green = positive, red = negative} and DNA truth states {gold = live/shown, green = proven}. NEVER mix layers silently: any element using a state color MUST make the layer legible (label, legend, or position convention). Identity never changes per state. SEQUENCE inside the identity layer is governed by the COLOR FLOW CYCLE (D4, RATIFIED BY SHAWN 2026-11-01); the state layer is unchanged by that ruling.
- R2 SCREEN CLASSES. Every screen declares `class ∈ {APP, READING}` in its recipe. APP: F5 viewport-fit applies. READING (Reports letters, Smart Note reading, long-form): scrolls by design; F1's "scroll reveals next screen" is satisfied by chapter/section boundaries. The gate checks the screen against its declared class.

## P2 — ARCHITECTURE (pipeline, normative order)

`PI → FACTORY → RECIPE → SHELL → GATE → ASSEMBLY → DEPLOY → VERIFY(served route)`

- P2.1 Project Intelligence (PI): single current record per app: {vision, goal, mission, bullseye, functions, recipes, alignment/connections, status}. If a fact is not in PI, it is not the plan. Stale PI ⇒ stop and refresh PI first (page zero is always PI itself).
- P2.2 Smart Factory: the single parts registry (P3). Registry = PI = live pages MUST agree; the Stockkeeper owns disagreements as named jobs.
- P2.3 Recipe: per screen. Slots MUST name blessed part IDs (never display names). Data bindings MUST reference contract names from the single bindings registry; a binding name means one thing everywhere. A recipe naming an unblessed/unknown part = STOP (hard fail, no override lane).
- P2.4 Shell: ONE chassis for all apps — the Smart Bar system: top bar = the app's own sections + related areas as quick tabs; bottom network bar = the identical 11-app bar on every page; search mounted in the chrome, one wording network-wide ("Search the network…"); one main bar — nobody makes their own. Pages differ only inside the recipe area.
- P2.5 Gate: P4.4 + P5.4 checks execute on the assembled screen (computed styles, measurements, reconciliation) — not on source claims. Output: pass/fail per check + the part or recipe line at fault.
- P2.6 Deploy + verify: done = the SERVED route returns the build AND served bytes prove content (build check and fill check are separate checklists; both must close). A compile pass is not a finish.
- P2.7 Paths: (a) CITIZEN — Trinity (Personal/Business/Space) is BORN DONE at the Welcome walk: walk answers map verbatim into the three pages' slots and seed first matches at reveal. The Factory MUST NOT create the Trinity; it is the add-on shop for extra citizen pages. Experienced time = walk + reveal. (b) TEAM — the Factory path above for the 26 apps (the training set).
- P2.8 Hosting: member pages are routes in the one estate on the network subdomain (same house as /dashboard, /personal, /business). No external hosting step exists in the pipeline.

## P3 — PARTS SYSTEM

### P3.1 Part contract (a part does not exist until all fields exist)
1. `id` — stable, registry-unique. 2. `name`. 3. Five questions, answered in writing: what it is · its purpose · how it works · why it matters · what makes it 10-star. 4. `interface` — inputs/events accepted, outputs emitted. 5. `data_contracts` — the contract names it consumes. 6. `states` — all of {rest, hover, pressed, selected, loading, empty, error} designed. 7. `anatomy_ref` — the DNA element anatomy it implements. 8. `score` + `blessing` (scorecard record: scorer, date, score) when blessed.

### P3.2 Part states (exactly three)
- BLESSED: part-level scorecard ≥ 9.0, recorded once. Instances inherit the proof; instances are sample-checked.
- EXISTS-UNPROVEN: exists; never passed a blessing. Recipes MUST NOT name it.
- MISSING: no artifact. Must be named in the Factory build queue with an owner.
- Reservation (binding honesty): proof inheritance is design, not proven. On first citizen pages, run the full gate per instance until assembly-scorecard reliability is itself proven; record when the exception is lifted.

### P3.3 Inventory truth (Parts Map v1, measured 2026-10-31)
Unique parts needed: 109 = 67 BLESSED · 32 EXISTS-UNPROVEN · 10 MISSING. Part-instances across 26 apps: 478 = 383 · 83 · 12. Factory queue: build 10, bless 32.
The 10 MISSING (build order): 1 Briefing strip (Dashboard · Intel Today · Reports) · 2 Living narrator (Dashboard) · 3 Matrix selector (Dashboard) · 4 Scheduled-send surface (Smart Mail) · 5 Nutshell guide surface (Library) · 6 Kanban column set (Projects) · 7 Reference Parts Gallery (Smart Factory — build early; it is the proving machine for all others) · 8 Affiliate/ambassador panel (Smart Growth) · 9 Screen-share surface (Smart Meet) · 10 Certificate board (Certificate/Identity).

### P3.4 First-stock canonical parts (from the ratified Anatomy, Part 8)
`.naya-btn` (signature/primary/standard/compact/jewel) · `.naya-board` (16:9 + strip + tile) · `.naya-chip-icon` (glyph set, 24-unit grid) · `.naya-composer` (verbatim, with Dictate + Schedule) · `.naya-input` · the 8 Smart Stats blocks (P5.3) · `.naya-bar` (top mount + bottom network bar) · `.naya-tabs` · `.naya-toggle` · `.naya-slider` · `.naya-face` · `.naya-sheet` · `.naya-toast` · `.naya-play-disc` · `.naya-empty-frame` · `.naya-skeleton`.

### P3.5 Shelf laws
- Imports, never copies: referencing a part MUST be by import/reference to the registry artifact. A redrawn part = defect.
- Every correction becomes a regression test: any flaw caught by a human or the gate is encoded into the gate's known-bad set permanently.
- Blessing happens in the Reference Parts Gallery: real part, real states, phone + laptop renders, measurements attached.

## P4 — SCREEN SYSTEM

### P4.1 Per-screen spec sheet (required fields; a screen without a complete sheet is not buildable)
`app` · `screen_id` · `class` (APP | READING, per R2) · `job` (one sentence) · `hero` (part ID + content source) · `supporting[]` (≤3: part ID + role) · `actions[]` (1–2 primary: label + effect) · `ambient[]` · `data_bindings` (slot → contract name) · `states` (empty/loading/error designs) · `phone_viewport` (spec first) · `laptop_viewport` (spec second) · `bullseye` (the screen's own finish line).

### P4.2 Build process (10 steps, in order — do not reorder)
1 define job → 2 choose hero → 3 place hero (center zone, display type, 48–72px) → 4 add supporting → 5 add actions (bottom zone) → 6 check fit (viewport-fit per class, both widths) → 7 check hierarchy (stranger test: hero identifiable in 2s) → 8 check beauty (DNA D1–D12, law by law) → 9 verify (gate + served-route proof) → 10 ship.

### P4.3 Mobile-first law
Design and verify phone-first. A screen failing at phone width CANNOT score 10 regardless of laptop quality. Laptop is designed second and must also be great; neither viewport is an afterthought. Fixes to a live screen are recompositions (P0.5), verified on the served route at phone width.

### P4.4 Gate checklist — design (every item must pass; evidence attached per item)
- G1 Obsidian: computed background = obsidian token; white text; no white background in the surface.
- G2 Depth: every interactive element shows layered construction (rim/elevation present via computed styles).
- G3 Ignition: rest state white/no halo; touch state ignites in the element's own color. Halo at rest = fail (orb identity exception per D6).
- G4 Color flow: every color sequence follows the D4 cycle order (purple leads, magenta crowns and wraps); no doubled color; no backtracking; groupings keep cycle order; one color job per element.
- G5 Geometry: targets ≥ 44px; boards 16:9 (strip/tile exceptions named); buttons are pills.
- G6 Type floors: body ≥ 16px; UI labels ≥ 14px; ≤ 3 type sizes on the screen (F4).
- G7 Spacing: every spacing value ∈ {4,8,12,16,24,32,48,64,96} (F3).
- G8 Motion truth: every animated element is driven by a real event/state; decorative animation = fail.
- G9 Honesty: no dead buttons; no tappable SOON; unwired features render honest frames; no fake/SAMPLE data outside labeled specimens.
- G10 State completeness: all applicable states of D7 render truthfully.
- G11 Family: every element is byte-identical to the Factory part (import check); sibling list attached (the builder names the siblings before building).
- G12 Hierarchy: layers = 4 (F2); hero count = 1; supporting ≤ 3; primary actions ≤ 2.
- G13 Viewport: APP class fits viewport at phone AND laptop widths; READING class scrolls by design with section boundaries.
- G14 Contrast: ≥ 4.5:1 all text.
- G15 The Shawn test: a reviewer can honestly check "Shawn would say 'oh yeah, that's awesome.'" If not, the screen is not done — polish and re-check.

### P4.5 The Interrogation (run per element, record answers in the screen's proof)
For each element: what does it say? what does it do? how is it saying it? is that the best way? is there a better presentation? how much real estate, and does placement/size match its value? An element that fails is cut; cuts are recorded.

## P5 — INTELLIGENCE LAYER (Smart Stats)

- P5.1 SN-0822 (binding): every number ships as magnitude + shape + direction + a human sentence — or it doesn't ship.
- P5.2 Vitality: every claim carries its graph. Every source card = living mini-graph OR honest prescriptive empty frame. Flat-data law: when Δ = 0, the chart states flatness on its face. Zero-state law: an empty state names the first action and its value, with the action present. One truth, three expressions: bar number = sentence number = ledger number.
- P5.3 ANSWER → DIAGNOSE → PRESCRIBE: every stats view answers its question, diagnoses what it sees, prescribes the one next move. Per-view bullseyes and identity colors (Shawn-locked 2026-10-31): stat identity jewels — Smart Score gold #FFB800 · Smart Notes magenta #E93FD8 · Creating amethyst #8B3DFF · Messages sapphire #2E7CF6 · Link clicks emerald #00D97E · Joins deep sapphire #2743E8 · Invites ruby #FF2E4D. Magnitude within one series uses the heat ramp (ruby → amber → gold → emerald → sapphire → deep sapphire → amethyst → magenta). Identity and magnitude are the two logics of R1 — never mixed silently.
- The 8 blocks (only stats parts that exist): Pulse Strip · Trend Panel · Mix Donut · Journey Funnel · Faces Board · Insight Feed · Heat & Streaks · Health Gauge. Per-source grammars: creating = steps · notes = constellation · likes = ripples · shares = branches · invites = funnel · sales = climb · membership = closing ring · all currents = the River. Data spine: one event ledger; event = {actor, kind, world, source, timestamp}; aggregates always derived; attribution is a field (join ← invite, click ← link/world, sale ← product/creator); until captured, insights stay honest aggregates. Placement: Dashboard = all 8 · PI = Health Gauge (filled-vs-proven as a living graph) + Trend Panel · every other door = Pulse Strip minimum.
- P5.4 Stats gate (in addition to P4.4): S1 reconciliation — displayed score == formula(displayed counts) (worked test: 75 + 4×25 + 0×35 = 175). S2 honesty — unwired metrics render honest frames; pending rows count 0 AND the surface says so. S3 matrix — WHEN {Live, Hour, 7d, 30d, All time} × WHAT {Activity, Engagement, Points, Growth, Money — one locked spectrum color each} × WHERE {This world, Pages, Rooms, Smart Link}; the resting state IS everything; no "Everything" button. S4 levels display — never a bare distance; always points-to-go + pace estimate (pace = trailing 7-day earned average).

### P5.5 VALUE TABLE (LOCKED 2026-10-31 — single source for Dashboard, Smart Ledger, canon)
birth 75 (once) · like/love 1 · comment 3 · save 5 · share_internal 5 · share_external 10 · invite_sent 25 (first per person only, in-system, anti-farm) · post 25 · smart_note 35 · membership 40 (once) · join 50 · sale 100.
FORMULA: SCORE = 75 + 25·posts + 35·notes + 5·saves + 25·invites + 50·joins + 40·membership(0|1) + 100·sales + 1·likes + 3·comments + 5·shares_internal + 10·shares_external.
Guards: harm = 0; sustained harm → negative (Law of One/no-harm); farming accounts fall together. Delta vs SN-1905 as filed: sale 50 → 100 (amendment note prepared; filing through the Smart Note door is owed — P8).

## P6 — PRODUCTION SYSTEM (Dream Team, ADOPTED 2026-10-31)

- P6.1 Principles: nobody's job is watching · making and checking are never the same hands · the queue is the clock · every seat has a bullseye, a proof, and a kill criterion.
- P6.2 Roster (guideline staffing): Builders ×3 (queue-driven; the three lead lanes Nitro 1–9 · Resolve 10–18 · Power 19–26) · Verifiers ×2 floating (same pass) · Integrator (2h landing sweep; verified ≥9.0 never waits > 2h) · Stockkeeper (daily; registry = PI = live) · Comms Runner (15m) · Judges ×2 rotating (different-seat scorecards) · Mechanic (event + daily) · Census (daily; verified outcomes per wake-up; target value ratio < 60:1) · Keeper (2h lock-in + on-finish state writes) · Director (synthesis; escalates only true gates).
- P6.3 CHAMELEON CLAUSE (binding): anyone can become anyone at any time; capability + availability decide; nobody waits on anybody; "not my job" does not exist. NEVER transfers: (a) maker ≠ checker; (b) Shawn's true gates = {money, credentials, private mail, destruction, constitutional ratification}.
- P6.4 Brief format (exact order): bullseye · exact sources · exact deliverable · proof standard · blocked move · scope fence. A brief missing any field is not dispatched.
- P6.5 Inline verification: checker ≠ maker, same pass, both named in the record. A fill closes on an inline verifier given ONLY the artifact + criteria.
- P6.6 Scorecard Law: self-score ≥ 9.0 by your own accord BEFORE requesting (the scorecard is final validation, not a drafting tool) → send to BOTH other lead seats via Smart Mail, subject prefix "SCORECARD THIS", with the live link + requirements, loud headline → also mention on board #3066 → fix and repeat until both score 9+ → only then to Shawn as the team's stamped validation. Criteria: why not 10 · what is loved · what is missing · what makes it 10× better · design-contract alignment · logic · 2-second understandability · push-button simplicity · organization · beauty. When you see a sister needs scorecarding, get it done — nobody waits for Shawn.
- P6.7 Clocks: Disposition Clock — verified ≥9.0 lands ≤ 2h; at +2h escalates to the Integrator; at +4h it is the scoreboard's named weakest point. Communication clock — named ask: respond ≤ 15m · nothing sits > 30m · > 1h = emergency named to Shawn + holder + board in the same pass. Seen ≠ answered ≠ done; a named ask closes only with an artifact, a rescope, or dated production.
- P6.8 WOWIE RULE (standing): do NOT hand Shawn an artifact until you would honestly say: "wowie — this is awesome; Shawn, you gotta check this out; this is epic; you're going to love it." Applies to links, files, pages, reports. A file the recipient cannot open and see is not a delivery.
- P6.9 Locked-In Declaration: at activation and every 2h — think, choose best, act, prove, learn; re-read the source, never the summary.
- P6.10 DELTA ONLY: state tracked once in a state file; passes read only changes. Jobs earn cadence by outcomes, never by receipts about unchanged state.

## P7 — ASSEMBLY RUNBOOK

- Stage 0 — STOCK THE FACTORY: build the 10 missing (P3.3); bless the 32 unproven in the Reference Parts Gallery. Exit criterion: 109/109 BLESSED.
- Stage 1 — WRITE THE 26 RECIPES: each lead her own apps (P6.2 split). Exit: every app has machine recipes for its screens naming only blessed IDs; every gap encountered is filed as a Factory job.
- Stage 2 — ASSEMBLER + GATE: recipe in → assembled screen on a preview route → gate report out. Assembler MUST hard-fail on unknown/unblessed IDs. Gate self-test: the gate runs against the known-bad set on every change; escapes join the set.
- Stage 3 — TIMED PILOT: one screen end-to-end; stopwatch from recipe-locked → gate-passed → sister-scorecard ≥ 9. Publish the first true number whatever it is. Compression staircase (measured, never asserted): 60 → 30 → 10 → 3 minutes; each step targets the largest logged time sink.
- Time split (steady state, per screen): mapping answers→slots: seconds (verbatim, no writing) · assembly ≈ 1m · gate ≈ 1m · render (phone + laptop) 1–2m · scorecard + landing: batchable. Target: start < 10m; goal 3m.
- Pilot standard: the director's page first, stopwatch running, in the house; nothing ships for everyone until it delights the director. Named timed pilot (design): Smart Lists. Pilot-as-Shawn's-page: SHAWN'S CALL (not seat consensus).
- Review doctrine: template scorecarded ONCE to 9+ → instances inherit proof → instances sample-checked (subject to P3.2 reservation on first citizen pages).
- Citizen acceptance bullseye: "Does Sarah finish the walk unaided?" (Sarah = ICP #1, solo service-business owner.) Her path: join free → Trinity born done → links in one place → beautiful presence → one Smart Link → real inquiry received + organized (consent + privacy controls) → Dashboard shows what happened + next move. Everybody is the market; Sarah is the door.

## P8 — STATUSES & OPEN SEAMS (do not smooth over)

- RATIFIED/LOCKED/ADOPTED: Design DNA · Value Table (sale = 100) · Three-Minute mission + two paths · Dream Team + Chameleon Clause · Wowie Rule · lane split · Parts Map v1 inventory · Color Flow cycle (Shawn, 2026-11-01; supersedes the PR #3141 walk).
- PROPOSED: Interface Framework (ratification = Shawn gate) · R1 two color layers · R2 READING class. Until ratified: DNA governs conflicts.
- CLOSED BY SHAWN'S RULING 2026-11-01: palette reconciliation (the D4 Color Flow cycle supersedes both contested spectra). STILL OWED: token-swap verification (Nitro's 65-family table is on her machine only; verification blocked until it lands in a shared store) · framework ratification · SN-1905 amendment filing (note prepared 2026-10-31; door filing owed) · Stage 3 first true number · Integrator landing pen (single-writer bottleneck is measured, not solved) · stars 6–9 names (Shawn's) · the two Shawn decisions on record (pilot-as-his-page · the annex-verification word).
- This blueprint invents nothing: every value traces to a ratified ruling, a locked table, a measured map, or an adopted design. Contested items are printed as contested.

— End of AI tongue. If any instruction here conflicts with a ratified source, the ratified source wins and the conflict is filed as a correction the same pass.
