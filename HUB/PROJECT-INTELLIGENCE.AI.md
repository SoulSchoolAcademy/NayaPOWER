# 🔱 HUB BUILD INTELLIGENCE — AI BUILDER PROJECTION

**Projection of:** `HUB/PROJECT-INTELLIGENCE.md` + `HUB/DESIGN-CONTRACT.md` (canonical — they win on conflict).
**Audience:** Naya seats and builder agents. **Optimize for:** a cold builder becoming an elite Hub designer on first read.
**Standard:** one project meaning, purpose-built views — HUMAN, NAYA/NIA, AI BUILDER, MACHINE and PROOF. These are projections, not separate truth systems.

---

## INHERITED DESIGN INTELLIGENCE

Read `NAYA-ACTIVATION/DESIGN/NAYA-DESIGN-INTELLIGENCE-STANDARD-V1.md` before substantive Hub design/build work.

Companion projections:
- `PROJECT-INTELLIGENCE.HUMAN.md`
- `PROJECT-INTELLIGENCE.NAYA.md`
- `PROJECT-INTELLIGENCE.MACHINE.json`
- `PROJECT-INTELLIGENCE.FEATURES.json`
- `PROJECT-INTELLIGENCE.PROOF.md`

**Standing Team Naya law:** if you see something materially not-right, post it on Issue #554 with evidence. Do not silently bury the finding or broaden an unrelated PR to fix it without coordination.

## 0. READ THIS FIRST

### Non-negotiable architecture correction

**THE HUB IS OUTPUT, NOT THE CANONICAL INPUT OF INTELLIGENCE.**

Do not put Smart Note capture, report generation, or manual activity publishing into the Hub merely because the interface needs an action.

The three primary upstream projection classes are:
1. Smart Notes / canonical Intelligent Blocks;
2. Activity / observed operational events;
3. Intelligence Reports.

These arrive through canonical runtime/event/index seams and are projected automatically.

Read `HUB/INTELLIGENCE-PROJECTION-CONTRACT-V1.md` before implementing Feed, Today, Reports, Library, runtime adapter, privacy/collective behavior, or Smart Tabs.

A client-local card inserted into the Feed is not intelligence capture. A localStorage note is not a Smart Note. A demo report is not a report. A fake activity item is not activity.

You are building the human cockpit into a living intelligence system. Your job is not to make screens — it is to make **the most elite interface anyone has ever experienced**, where every pixel earns trust and every control does something real. The frozen visual baseline (`HUB/NAYANET INTERFACE CONCEPT.html` @ `ffedda20`) is the floor. Improve it or match it. Never flatten it.

---

## 1. DESIGNER PROGRAMMING (taste as law)

This section programs your judgment. When the spec is silent, these decide.

**Color is energy, not decoration.** The 12-color spectrum in fixed order — purple → indigo → sapphire → teal → emerald → lime → yellow → gold → orange → rich orange → red → magenta — each assigned semantically per room/board/state via tokens. Never flat decorative fills. Never overpower reading content. Primary text stays high-contrast. Full token table: MACHINE projection, `spectrum[]`.

**Depth is physical.** Every interactive object: dense obsidian/graphite surface, precise illuminated edge, subtle upper highlight, deep elevation shadow, controlled theme-colored halo. Hover: lift 2px, brighten, sharpen glow. Press: compress, darken, shrink shadow. Active: keep elevation, raise semantic energy. This is the Living Depth law — fake retro 3D and glassmorphism are both banned.

**Buttons obey the 10-point law:** obsidian material, beveled edge, elevation, theme energy, hover lift, active illumination + accent rail, press compression, accessible focus, honest disabled, disciplined motion (`.22s cubic-bezier(.16,.84,.22,1)`). A button is incomplete until it has a real causal path — visual affordance must never imply unavailable capability.

**Boards are intelligence objects, not cards.** Each of the nine boards: own icon, theme, glow, material, elevation, status, layers, actions. No two boards feel like the same card recolored.

**Icons are one faceted jewel family.** Shared geometry, facet, core, highlight, shade, edge, optical-depth rules. Unicode/emoji icons are placeholders — zero in production.

**Motion = state.** Animation communicates actual runtime state; it never manufactures it. Connected visuals only when connected. Processing effects only during processing. VERIFIED only with evidence.

**Honesty over impressiveness.** The 7-state model everywhere: LOADING / EMPTY / READY / BLOCKED / NOT_VERIFIED / VERIFIED / ERROR. No sample data. No fake mailboxes. No animated "activity" that isn't real. A false impression costs more than an empty state.

**The rail is sacred.** Single left rail, eleven rooms, search prominent. No dashboard grids. No three-column SaaS. Mobile preserves identity (rail → elite bottom bar or gesture nav), never collapses into boring cards.

---

## 2. THE EIGHT DIMENSIONS (what you score)

D1 Visual Excellence · D2 Functional Completeness · D3 Intelligence · D4 Honesty · D5 Performance · D6 Reliability & Continuity · D7 Accessibility · D8 Craft.
Full 10/10 definitions + current scores: canonical `PROJECT-INTELLIGENCE.md` §2. Current overall ~5.6/10. The game: D2/D3/D5/D7 climb while D1 never regresses.

## 3. SCORECARD INSTRUMENT (how you're measured)

1. You self-score with evidence links (screenshots, recordings, test output).
2. An **independent seat re-scores** — your self-score never closes a gate.
3. Disagreements resolve by re-reading the artifact, not debate.
4. Re-run every phase. **Scores can go DOWN.**
5. **Below 9.0 = not ready, no exceptions.** Target 10, happy with 9.5.

## 4. BUILD PHASES & GATES

Phase 0 Hygiene → Phase 1 Shell+Router → Phase 2 Tokens → Phase 3 Runtime Adapter → Phase 4 Room-by-Room → Phase 5 Identity Rebuild → Phase 6 Intelligence Layer → Phase 7 Hardening → Phase 8 The 10/10 Gate.
Gates per phase: canonical §4. Hard dependency: Phase 3+ waits on PR #1243 (persistence) merged + nine-node kernel on main. Until then, rooms render honest NOT_VERIFIED — never fake data as a substitute.

## 5. THE DOORS (Smart Connect room)

One brain. Many doors. Each door: themed elevated object, what it is, who it's for, **live status shown truthfully**, connect action with real causal path.

**Door honesty (hard rule):** the canonical registry is `BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json`. Only 2 doors are LIVE (AI Connect bounded, Supabase/Data bounded); 7 are REGISTERED_CONTRACT_ONLY. The Hub must never present a contract-only or roadmap door as live. Status per door, always — see MACHINE projection `doors_canonical[]` / `doors_roadmap[]`.

**Door authority law:** Doors expose what Naya can do. LAW decides what Naya may do. ACT does it. VERIFY checks what happened. **CONNECTED ≠ AUTHORIZED.** Connection never implies permission to act.

## 6. WORKING AGREEMENTS

- Coordinate on issue #554. Never rewrite another lane's in-flight work.
- Smallest effective change. Componentize; don't redesign the visual language.
- **Before shipping any Hub change, inventory:** PURPOSE → REQUIREMENTS → EXISTING FEATURES → PRESERVATION → INTERACTIONS → DATA → AUTHORITY → STATES → ACCESSIBILITY → RESPONSIVE → PERFORMANCE → PROOF. Then classify every existing element: **KEEP / IMPROVE / REPLACE / REMOVE.** No replacement merely because it is newer or cleaner — it must be superior in purpose, UX, visual craft, and system coherence.
- **Cold-Naya rule:** a cold Naya must be able to enter `HUB/`, understand the objective, identify what is preserved, know what is broken, and execute the next authorized step without Shawn reconstructing the vision. If not, the intelligence is incomplete.
- One shell, many rooms, one substrate. No second brains, no second databases.
- Routing law: WELCOME → IDENTITY → INTELLIGENT HUB. Identity page rebuilds in the design system; the workers.dev redirect dies.
- **Recommended first room (Phase 4): Your Intelligence Today** — it forces every meaningful seam to compose: identity → retrieval → truth state → Naya interpretation → action → honest refusal when evidence is absent.

## 7. WHEN THE SPEC IS SILENT (judgment protocol)

1. **Judgment Rule (Prime 1):** if you can see an instruction is wrong — factually, logically, or it makes the system worse — stop, explain with evidence, propose the right path. Never execute blindly.
2. **6→10 doctrine:** clear 6→10 with no plausible path to 3 → act. Plausible 6→3 or uncertain → check with Shawn. Gray zone → ask.
3. **Escalate with options + recommendation,** never bare questions.
4. Protected gates are Shawn's word only: merges, production deploys, ratification, destructive changes, privacy/consent/security/authority changes.
5. **Bring better ideas.** The spec is the floor. If you see a wiser, more powerful, more extraordinary approach — table it on #554 with reasoning. The scorecard decides, not taste. If you can beat the concept's look, do it — and prove it scores.

## 8. Full-app ownership gate

Do not optimize for “my ticket is done.”

A Hub builder is responsible for the effect of its work on the complete smart app.

Before declaring readiness:

1. restore current canonical project intelligence;
2. read the applicable room contracts;
3. inspect current implementation and deployment evidence;
4. inventory dependencies and cross-room handoffs;
5. self-score D1–D8 with evidence;
6. implement the highest-value coherent slice;
7. test browser/runtime/persistence/error/responsive/accessibility/performance behavior as applicable;
8. re-score and keep fixing known material gaps;
9. obtain independent challenge/re-score;
10. present only near-perfect work or one exact authority/external blocker.

**Target 10.0. Human Director near-perfect acceptance bar 9.5. 9.0–9.49 means continue improving rather than asking Shawn to finish the QA mentally.**

Use `HUB/SMART-APP-10-10-EXECUTION-LAW.md` as the execution protocol and `HUB/CURRENT-IMPLEMENTATION-INVENTORY.md` as the dated reality snapshot. Target contract and observed implementation must never be confused.
