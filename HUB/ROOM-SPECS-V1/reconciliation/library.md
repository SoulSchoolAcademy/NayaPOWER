# LIBRARY — Reconciliation: lane SPEC (A) vs Naya 3 blueprint (B)

**A** = `library/SPEC.md` + `library/wireframe.html` · **B** = `grounding/blueprints/04-intelligent-library.md`
**Grounding cited:** P = INTELLIGENCE-PROJECTION-CONTRACT-V1 · F = ROOM-FUNCTIONAL-CONTRACT-V1 · T = `1278-tokens.css` · S = ROOM-BLUEPRINT-STANDARD-V1
**Note on the record:** the task brief describes B as following S with 15 sections (entry, composition, instrument, controls+placement, data, states, handoffs, Naya, mobile, accessibility, visual law, acceptance journey, anti-patterns, proof). The actual file has 11 short sections and is **missing five S-required sections**: States, Cross-room handoffs, Accessibility, Visual law, Acceptance journey — and its Controls list names no placements. B is structurally non-conformant with the standard it is described as following. This is treated as a finding, not an assumption that the missing content exists elsewhere.

---

## 1. AGREEMENTS

Locked identically on both sides; grounding confirms.

1. **Signature instrument = semantic search + inspector.** A R2: "HERO SEARCH (full width, signature instrument)". B: "Primary instrument: Semantic Intelligence Search + Inspector." LOCK.
2. **First-3-seconds entry = big search field + filters + live intelligence.** B: "a large search field, useful filters, and a small set of relevant/recent intelligence." A R1+R2: orientation band (mark, promise, Space scope, truth legend) + centered hero search. Same entry beat.
3. **One canonical ID, zero copies.** A contract #3/#7/#8: one canonical ID and one object identity; the same ID opened from Feed/Today/Library renders the same detail view — never a copy. B Proof: "Search result opens same canonical ID seen in Feed/Today." B Do-not: "do not duplicate canonical content." Exact lock; matches P §4 (IB-123 must not become feed-copy/today-copy/library-copy).
4. **No Hub-side capture.** A contract #6/#10: forbidden "Create Smart Note" button; "Ask Naya → Smart Note this" intent is handed upstream, never minted locally. B lists no capture controls and defines Data as "Canonical intelligence index / retrieval adapter. Never DOM search." Both obey P §3 (NO HUB CAPTURE BUTTON LAW) and P §10 (intelligence-production actions are upstream).
5. **No filesystem-as-library / no fake shelves.** A forbidden substitutes: "filesystem-by-default metaphor", "never sample shelves"; R9 renders "RUNTIME UNAVAILABLE / NOT VERIFIED" instead of samples. B Do-not: "do not become file manager." Lock; matches P §11 (sample data law).
6. **Supersession truth is mandatory, not optional.** A R7/R8: every card carries last meaningful update ("Updated 2d ago — decision superseded"); R8 has Revisions/supersession; detail links superseded objects by reference, never delete-rewrite. B Result anatomy: "current/superseded". B Do-not: "do not show 'current' without supersession truth." Lock.
7. **Result card anatomy.** A R7: essence + why-match (REQUIRED) + provenance + state badge + last meaningful update + card action row. B: title/essence, why relevant, truth/provenance, current/superseded, related intelligence. Same anatomy modulo "object type" (see §3).
8. **Global object actions on cards.** A R7 action row: Open · Ask Naya · Save · Add to List + overflow (Open source, See relationships, Open originating Feed, Share governed). B Controls: Open, Ask Naya, Save/List, Evidence, Related, Open in source room. Same action set; matches F §5 global object actions.
9. **Naya presence is contextual, interpretation is labeled.** A R2 "Not sure what to ask? Ask Naya"; R6 "Ask Naya: What am I missing here?"; interpretation panel header "Naya's interpretation — not source truth". B Naya: "What am I missing? What changed? How is this related? Why should I trust this?" Matches F §8 (Naya must distinguish suggestion from fact).
10. **Mobile = search-first, full-screen detail.** A mobile paragraph: search-first; result list → full-screen detail; filters to bottom sheet; provenance preserved. B Mobile: "Search first, results next, detail opens full-screen." Lock; matches F §9.9.

---

## 2. CONTRADICTIONS

### C1. Detail presentation: full takeover (A) vs optional side pane (B)
- **A says:** R8 — OPEN_INTELLIGENCE is a "full center takeover", `✕ Close` returns to exact prior scroll/focus; sticky bottom action row.
- **B says:** Desktop composition — "optional detail pane only after selection."
- **Resolution + why:** **[NEEDS DIRECTOR TASTE].** Neither P nor F §1–§9 prescribes pane-vs-takeover. This changes the composition's spatial logic and A's predicate 11 (Esc closes detail) and R8's sticky action row both assume takeover. Not resolvable from grounding.

### C2. Featured composition: three ranked columns + domain gallery (A) vs plain results list (B)
- **A says:** R4 — three side-by-side columns MOST RELEVANT / RECENTLY DEVELOPED / NEEDS ATTENTION (horizontal strips), then R5 domain gallery grid below.
- **B says:** Composition — `[ RELEVANT / RECENT RESULTS ]` vertical list under the filter row. No featured columns, no domain gallery.
- **Resolution + why:** **[NEEDS DIRECTOR TASTE].** F §2 says "Do not force every room into the same layout" but neither side's grounding proves its own composition. A has acceptance predicates (recompute from canonical data); B has no acceptance journey at all. This is the largest compositional fork in the reconciliation.

### C3. Domain room concept (A) vs topic-filter-only (B)
- **A says:** R5 domain gallery → OPEN_DOMAIN → R6 domain room with back button `‹ All domains` and seven labeled sections (What I know / What I've learned / What I'm uncertain about / Related intelligence / Recent discoveries / Smart Notes / Questions) plus "Ask Naya: What am I missing here?" (predicate 6 covers back-navigation state preservation).
- **B says:** No domain room, no gallery; closest equivalent is the `[ Topic ]` filter in the filter row.
- **Resolution + why:** **[NEEDS DIRECTOR TASTE].** F §1–§3 do not mandate domain-browse. B's silent treatment means it neither confirms nor refutes R6; nothing in P/P §10 forbids it (domain rooms are projection/organization, which the Hub owns). Taste + scope decision.

### C4. Search-filter vocabulary
- **A says:** truth-filter chips only (All / Verified / Candidate / Not verified), single-select, `All` default; Space scope lives in the R1 orientation band as `Space: [All spaces ▾]`; R2 search "clears scope filters only on explicit Clear search ✕".
- **B says:** filter row `[ Type ] [ Topic ] [ Space ] [ Truth ] [ Time ] [ Filters ]`.
- **Resolution + why:** **Partial — F decides the principle, director decides the set.** F §3: "Search/filter controls appear only where they materially reduce burden." Both cannot be simultaneously true as "every visible control"; Type/Topic/Time filters add six controls A never specified, and A's truth-only chips under-specify against B's Truth position. F supports "fewer controls unless they earn their keep"; whether Type/Topic/Time earn it is **[NEEDS DIRECTOR TASTE]** after seeing real index metadata.

### C5. View tabs: Search/Browse/Saved/Recently used/Map (A) vs none (B)
- **A says:** R3 tabs — `Search` (default) · `Browse` · `Saved` · `Recently used` · `Map`; tabs are views over one index, never separate stores.
- **B says:** No tabs concept at all.
- **Resolution + why:** **Mostly [NEEDS DIRECTOR TASTE]; partly F-backed.** Saved/Recently-used are Hub-owned organization (P §10 explicitly allows save/favorite a reference, add to a list), so they survive grounding; the `Map` tab is already an A taste question (graph projection may not be real in V1); `Browse` overlaps with C3 (domain room). Whether tabs are the right mechanism at all is taste.

### C6. Accent: "sapphire" (room doc) vs `--blue` (tokens)
- **A says:** `--accent-library: var(--blue)` in the header, but flags a taste question: FUNCTIONAL-SPEC names the room theme "sapphire" while T defines `--accent-library: var(--blue)` (and T separately defines `--sapphire: #4f8ff7`).
- **B says:** Nothing — B has no visual law section.
- **Resolution + why:** **T (tokens) wins; no director decision required on the color itself.** T is visual law: `--accent-library: var(--blue)` (`#55b9ee`). A correctly names the conflict. Changing the room to sapphire would require a governed token edit (`--accent-library: var(--sapphire)`), not a blueprint decision. Keep the token law as-is unless tokens change.

### C7. A's internal: which view owns R4/R5
- **A says (two things):** R4 is labeled "(below tabs, Search view)"; R5 is "(below featured, Browse-anchored section)"; R6 "(replaces R4+R5 when a domain is open)".
- **Why this is a contradiction:** If R4 belongs to the Search view and R5 is Browse-anchored, the default Search view shows featured-without-gallery while Browse shows gallery-without-featured — but R6 replaces "R4+R5" as a unit, implying they co-exist. The wireframe stacks R4 then R5 in one page, matching neither reading exactly.
- **Resolution + why:** **Lane-internal repair, no director needed.** A must state explicitly which tabs render which regions (e.g., Search = R2+R4+results; Browse = R5). Blocked on nothing but A's own edit.

### C8. A's internal: wireframe prejudges an open taste question
- **A says:** SPEC.md component inventory: "Variant needed but not in tokens: none identified" and the taste question asks whether why-match should be plain body text or get a dedicated treatment.
- **Wireframe says:** `.whymatch` renders every why-match line with a 3px left-border tint strip — i.e., the dedicated treatment, already decided.
- **Why this is a contradiction:** the wireframe answers the question the spec declares open. A builder reproducing the wireframe builds the tinted strip; a builder following the spec text builds plain body text.
- **Resolution + why:** **Lane-internal repair.** Either close the taste question (adopt the wireframe's treatment) or revert the wireframe to plain body text. S exists precisely so the screen matches the spec ("No blueprint, no building"); here the two blueprint artifacts disagree with each other.

### C9. A's internal: canonical input ambiguity (Brain path vs runtime index)
- **A says:** Contract #3: IBs and reports "projected from `nayanet_intelligent_blocks` and `BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/`". Contract #4: runtime owner is the Hub runtime adapter, read/projection-only against the canonical index/retrieval.
- **Why this is a contradiction:** P §1A states the readable GitHub/Brain projection is "one view of the same canonical intelligence" — a downstream projection, not an input. Listing `BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/` alongside `nayanet_intelligent_blocks` as a source reads as the Hub consuming a Brain filesystem path as canonical input, which is exactly the "filesystem-by-default metaphor" A forbids in #10.
- **Resolution + why:** **P decides.** The adapter consumes the runtime/index; Brain paths appear as provenance references (source ref), never as the data source. A should reword #3: canonical runtime → adapter → room; Brain path = provenance lineage only.

### C10. B's missing mandatory sections (standard non-conformance)
- **S requires** 15 sections including States, Cross-room handoffs, Accessibility, Visual law, Acceptance journey. **B has none of these**; Controls lacks placements; Data is two lines.
- **Resolution + why:** **S decides.** B cannot be built from as-is per its own standard ("No room is implementation-ready until its blueprint is complete enough that a cold builder can reproduce the intended interface"). B needs the five missing sections written before freeze, regardless of A.

---

## 3. GAPS

Asymmetries actually found (not the brief's example — B does not contain first-3-seconds entry detail beyond one line, and A does not lack acceptance predicates; A HAS predicates and inventory, B LACKS them).

**Present in A, missing in B:**
- G1. Truth states: A enumerates all 11 states (LOADING…DISABLED, exactly F §6) with a runtime-unavailable doctrine; B has no states section at all.
- G2. Cross-room handoffs: A names destinations (Feed, Today, Reports, Lists, Spaces, Connections, Ledger) with reference-not-copy identity rules (P §4); B has no handoffs section.
- G3. Accessibility: A predicate 11 (tab order, Enter/Esc, reduced motion); B has no accessibility section.
- G4. Visual law: A names tokens, accent, type/radius/depth scale; B has no visual law section.
- G5. Acceptance journey/predicates: A has 11 mechanical predicates; B's "Proof" is a single sentence with no steps.
- G6. Component inventory: A maps every region to token-based components; B has none.
- G7. Taste questions: A flags 5 open items; B flags none (no uncertainty surfaced).
- G8. Domain room + Saved/Recently used + Map (see C3/C5).

**Present in B, missing in A:**
- G9. Filter vocabulary beyond truth: B's `[ Type ] [ Topic ] [ Time ]` filters; A only specifies truth chips (see C4).
- G10. Anti-patterns section: B has "Do not" (file manager, duplicate canonical content, current-without-supersession); A distributes these into forbidden substitutes but has no explicit anti-pattern list.
- G11. `object type` on result anatomy: B lists "object type" (SMART NOTE vs REPORT vs ACTIVITY — matches P §12's conceptual event); A's R7 card spec and predicate 2's required-field list omit object type entirely. A's contract #3 knows IBs vs INTELLIGENCE_REPORTs exist, but no card ever displays which one a result is.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides' flagged items, deduplicated. (B flags none, so this is A's list, carried forward; C-resolutions above are referenced.)

1. [NEEDS DIRECTOR TASTE] Why-match emphasis: plain body-text line vs dedicated visual treatment (tinted "why" strip). — **Complicated by C8:** the wireframe already ships the tinted strip while the spec text keeps the question open. Closing this also resolves C8.
2. [NEEDS DIRECTOR TASTE] `Map` tab in V1 vs deferred until the graph projection is real. — Tied to C5.
3. [NEEDS DIRECTOR TASTE] "Recently used" scope: does it include opened-but-unsaved objects, and does viewing in a collective projection count as "used"? (privacy implication). — Tied to C5.
4. [NEEDS DIRECTOR TASTE] Superseded objects: remain openable/searchable vs demoted from search with a "superseded" badge. (B's "do not show 'current' without supersession truth" and A's R8 revisions section agree supersession must be visible; ranking treatment is the open question.)
5. [NEEDS DIRECTOR TASTE — NEW] Domain gallery/domain room in V1 scope, or search-results-only per B (C3).
6. [NEEDS DIRECTOR TASTE — NEW] Detail presentation: full center takeover vs optional side pane (C1).
7. [NEEDS DIRECTOR TASTE — NEW] Filter set: truth-chips-only vs B's Type/Topic/Space/Truth/Time row (C4).

**Resolved without director (grounding wins):** accent color — tokens are visual law, `--accent-library` stays `var(--blue)` unless a governed token edit changes it (C6).

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION.** Blocking items:

1. **B1 — B's five missing S-required sections.** Write B's States, Cross-room handoffs, Accessibility, Visual law, and Acceptance journey (with control placements) before freeze. Until then B is not buildable-from per its own standard. (C10)
2. **C1 — Detail presentation fork.** Full center takeover (A) vs optional side pane (B) — pick one; A's R8, predicate 11, and sticky action row all assume takeover.
3. **C2 — Featured composition fork.** Three ranked columns + domain gallery (A) vs plain results list (B) — pick one composition for the Search view.
4. **C3/C5 — Domain room + Browse/Tab set in V1 scope.** B is silent; A builds a full R5/R6 domain room and five tabs. Decide: ship, defer, or cut each.
5. **C4 — Filter vocabulary.** Lock the control set (truth-only chips vs Type/Topic/Space/Truth/Time) with a burden justification per F §3.
6. **C8 — Wireframe vs SPEC on why-match treatment.** Close taste question #1 or revert the wireframe; the two artifacts currently specify different screens.
7. **C7 — A's Search-view vs Browse-view region ownership.** A must state which tabs render R4/R5.
8. **C9 — A's canonical input wording.** Reword contract #3 so the Brain path is provenance lineage only, per P §1A; the adapter reads the runtime/index.

**Adversarial notes for the record:**
- A's predicate 1 contains an untestable clause: "a fixture cannot improve the room's score" — there is no defined "room's score"; the first clause (real results from the canonical index) is testable, the second is not. Strike or define it before freeze.
- A's predicate 4's verification ("result set differs or empty-state wording names the scope") is testable but weak — passing it proves the filter changed *something*, not that scope semantics are correct.
- A's wireframe header honestly labels all content FIXTURE, consistent with P §11 (sample data law) — good.
- G11 (missing object-type on cards) is a genuine B-catch-A gap: A's card predicate 2's required-field list should gain "object type" once the canonical model carries it (P §12).
- No-Hub-Capture audit: neither spec implies Hub-side creation of canonical objects. A's contract #6 explicitly hands "Smart Note this" upstream. No silent violation found; C9 is a wording ambiguity, not a capture violation.

**Ready to freeze only after:** blockers 1–8 are resolved and taste questions 1–7 have director answers; then the reconciled spec can lock.
