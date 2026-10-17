# FEED Room Reconciliation — Lane A (`feed/`, SPEC-FIRST) vs Lane B (`grounding/blueprints/01-smart-feed.md`, Naya 3)

**Reviewer stance:** adversarial toward both sides. A = `feed/SPEC.md` + `feed/wireframe.html` (my lane). B = `grounding/blueprints/01-smart-feed.md` (Naya 3's lane). Grounding cited: INTELLIGENCE-PROJECTION-CONTRACT-V1 (IPC), ROOM-FUNCTIONAL-CONTRACT-V1 (RFC), `1278-tokens.css` (tokens, visual law).

---

## 1. AGREEMENTS

What both sides lock identically. Verified pairwise below.

- **Room identity:** title "Smart Feed", route `/feed`, human question "What is happening now?" — both agree verbatim.
- **Primary instrument = the stream.** A: F-STREAM "Intelligence stream (main column, vertically continuous)"; B: "A continuous, visually rhythmic **Intelligence Stream**." Same instrument, same role (room's reason to exist).
- **Mode control: PERSONAL · COLLECTIVE · ACTIVITY.** Same three modes, same segmented-control treatment, mode positioned above tabs because it changes the whole dataset. A: F-MODE three large buttons; B: "directly below title because mode changes the entire dataset." Both agree Collective exists as a governed, identity-stripped projection.
- **Smart Tabs row below mode.** Same five leading tabs in same order: All / Smart Notes / Reports / Highlights / Learning (A locks three more: Decisions, Discoveries, Projects; B trails off with "..."). Same rule: tabs filter the *same canonical set* by type/topic from canonical metadata — never copies, never a second query store. (A: "never a copy, never a second query store"; B: "do not duplicate objects per tab.")
- **Card anatomy agrees element-for-element:** type jewel · title/essence · "why am I seeing this" · truth state · time · source/provenance · Space tag · compact actions. A's card anatomy and B's "Each object shows" list are the same seven elements in different wording.
- **Object controls agree (modulo one naming item, see Contradictions):** Open · Ask Naya · Save(/Favorite) · Add to List · Evidence/Open Source · Share only where governed. Both list these; both agree Share is absent-not-disabled when unauthorized.
- **No capture, anywhere.** A: forbidden substitutes (no "Create Smart Note"/"Post Activity"/"Generate report", no client-side IB identity, no localStorage-as-source, acceptance predicate 6 "no capture/compose control exists in the DOM"). B: "No Smart Note capture button", "do not become social-media composer", first-3-seconds explicitly shows "no composer/capture box". Both satisfy the No-Hub-Capture law (IPC §3). Neither side violates it.
- **Ask Naya = intent handoff upstream.** A: "if the human asks to create intelligence, intent hands off upstream — the Feed creates nothing"; predicate 7. B lists Ask Naya among controls with explanatory prompts. Consistent with IPC §3/§10 (Hub may handoff intent; upstream owns execution).
- **Truth states honest; fixtures quarantined.** A: LOADING/EMPTY/OFFLINE/ERROR/NOT_VERIFIED/VERIFIED/BLOCKED/UNKNOWN/DISABLED taxonomy, "The stream is quiet." + honest reason, fixture-labeled dev placeholders excluded from production paths (predicate 14). B: "All standard states", EMPTY distinguishes no-qualifying-intelligence / empty Space / runtime unavailable, "do not show fake activity". Same doctrine; A enumerates, B summarizes.
- **Projections, not copies; canonical ID preserved cross-room.** A: contract header #3 ("Feed items are projections by canonical ID — never copies"), F-DETAIL canonical ID always visible, predicates 10/13 (same canonical ID character-for-character across rooms). B proof: "Opening the same object from Feed/Library preserves canonical ID." Both satisfy IPC §4.
- **Filter = sheet, never permanent sidebar.** A: F-FILTER overlay right, "Filters never permanently clutter the canvas"; forbidden substitutes "No permanent filter dashboard cluttering the canvas". B: "filter button — right side of Smart Tabs; opens sheet, not permanent sidebar." Same.
- **Mobile: one column, actions collapse to bottom sheet.** A: one-column full-width stream, per-card "Actions" button → bottom action sheet. B: "Objects become full-width. Actions move into bottom sheet." Same.
- **Proof predicate: mode switching changes real data.** A: predicate 2. B proof: "Switching modes changes real data." Identical.
- **Ranking is explainable, never engagement-as-truth.** A: "Ranking answers *Why is this useful to me now?* … never claiming objectivity"; forbidden "No unexplained ranking presented as objective truth". B: "do not rank by engagement as truth". Same law.
- **Theme token reconciliation stands.** A's header resolves FUNCTIONAL-SPEC "emerald" vs tokens: `--accent-feed: var(--green)` = `#55e39a`. Verified in `1278-tokens.css` (line 29 `--green: #55e39a`, line 39 `--accent-feed: var(--green)`). Tokens win as visual law. B is silent; no conflict.

---

## 2. CONTRADICTIONS

### C1. Filter control placement
- **A says:** "Search & filters" button in F-HDR right side (with freshness label and "New since last visit"), opens F-FILTER.
- **B says:** filter button on the right side of the Smart Tabs row.
- **Recommended resolution:** A's F-HDR placement. The tabs row is horizontally scrollable and semantically a refinement control; hanging a sheet-opener off a scrolling row makes its position unstable. F-HDR is the stable command surface. Not a blocker if director overrides. **[NEEDS DIRECTOR TASTE]** if B's author has a composition reason.

### C2. Mobile F-DETAIL drawer — direct contradiction
- **A says:** F-DETAIL is a locked right-overlay drawer (above stream), with header/actions/sections specified; mobile section does not address it.
- **B says (mobile):** "No second rail/drawer." Flat prohibition.
- **Recommended resolution:** neither side's grounding decides this (RFC is silent on mobile drawer). The consistent move is to extend A's own mobile pattern: the action deck already collapses into a bottom sheet on mobile — F-DETAIL should become a bottom sheet on mobile, not a right overlay. That satisfies B's "no second rail/drawer" (no *side* drawer) while keeping A's locked detail content. **[NEEDS DIRECTOR TASTE]** on the exact mobile presentation; **blocker** until resolved because A's F-DETAIL lock and B's prohibition cannot both ship.

### C3. "New since last visit" placement — three-way disagreement
- **A says:** button in F-HDR right, rendered only when ≥1 unseen item exists; clicking jumps to first unseen item. (A separately flags header-vs-float as a taste question.)
- **B says:** end-of-stream marker: `[ New since last visit / end-of-stream state ]` at the bottom of the composition.
- **Wireframe note:** A's wireframe F-MODE note references `/feed/collective` while SPEC text says `/feed/personal etc.` — trivial example inconsistency, but it shows the URL convention isn't byte-locked anywhere.
- **Recommended resolution:** A is making a finer distinction than B: F-SEAM pill (new arrivals *while in room*) vs "New since last visit" (unseen items *since last visit*) are two different mechanisms; B conflates them into one end-of-stream marker. Keep A's two-mechanism model; placement (header vs float vs end-of-stream) is **[NEEDS DIRECTOR TASTE]**. **Blocker-adjacent:** freeze can proceed with A's header placement marked as the provisional lock.

### C4. Pagination model — A is internally contradictory, B adds a third reading
- **A says:** §(b) F-STREAM locks a manual "Load more" button, "no infinite scroll, so scroll/return context stays mechanical" — and in the same paragraph marks it `[NEEDS DIRECTOR TASTE]`. A thing cannot be both locked and open.
- **B says:** primary instrument is a "continuous, visually rhythmic Intelligence Stream" — "continuous" reads like infinite scroll, which contradicts A's manual button.
- **Recommended resolution:** decide it. A's mechanical argument (scroll/return context preservation, predicate 12's reload-restore requirement) is stronger grounding than B's adjective. Recommend: manual "Load more" locked, infinite scroll rejected, and the taste flag removed. **[NEEDS DIRECTOR TASTE]** to confirm — **blocker**, because A's spec is self-contradictory on a behavioral element and predicate 12 (scroll restore) depends on the answer.

### C5. Space selector placement
- **A says:** F-MODE left — Space dropdown next to the mode segmented control.
- **B says:** Space near the room title (composition shows `[Smart Feed] [Space] [Freshness]` in the title row), rationale: "Space changes context globally."
- **Recommended resolution:** neither side's grounding wins. B's rationale is marginally stronger (Space is global scope, mode is dataset scope; grouping them invites the false reading that Space is a fourth mode). Recommend B's title-row placement, or keep A. **[NEEDS DIRECTOR TASTE]**. Non-blocking: freeze with either, recorded as provisional.

### C6. Evidence label naming
- **A says:** "Open Source" (provenance row clickable → "Open Source" evidence; predicate 4 tests clicking "Open Source").
- **B says:** "Evidence".
- **Recommended resolution:** **[NEEDS DIRECTOR TASTE]**. "Evidence" is shorter and matches the room's PROOF layer vocabulary (RFC five-layer law: "Why should I trust it?"); "Open Source" is more literal about what the click does. Non-blocking; freeze with A's lock and revisit.

### C7. Default mode — A locks it, B is silent with a suggestive ordering
- **A says:** default mode **Collective**, citing it as the Human Director's preferred default (contract header #6).
- **B says:** nothing about default; first-3-seconds and composition list PERSONAL first, which a builder could read as the default.
- **Recommended resolution:** A's lock, on the director-statement grounding A cites. If the director preference is real, B should be amended to state the default explicitly. **Confirm with director** (one-line), non-blocking for freeze — but B must not ship with PERSONAL-first ambiguity. Internal B vagueness, not a B-vs-A product disagreement.

### C8. "Why am I seeing this?" as a control vs as content
- **A says:** inline expandable link in the card body AND a tertiary action-row link AND a section in F-DETAIL.
- **B says:** per-object "why it is here" is part of the primary instrument's display, and "Why am I seeing this?" appears only under Naya prompts — it is absent from B's object-controls list.
- **Recommended resolution:** A's explicit dual placement. B already requires the content ("why it is here"); making it a tappable control is a mechanical refinement, not a new idea. Fold into freeze; not a blocker.

### C9. B's `[GLOBAL SEARCH]` at composition top — A has no global search
- **A says:** nothing; the room owns only the center workspace, shell owns the rails; room-level search lives inside F-FILTER ("Search this stream…").
- **B says:** composition opens with `[GLOBAL SEARCH]`.
- **Recommended resolution:** likely a shell-level control B assumed, not a room control. If global search is shell-owned, no contradiction; if it implies the room builds one, it contradicts A's F-FILTER model. **Gap to clarify with the shell contract**, non-blocking. Do not let the room spec absorb a shell control silently.

---

## 3. GAPS

### Present in A, missing in B (B must absorb before freeze)
1. **Acceptance predicates (A §d, 14 of them).** B has a two-line "Proof" section. No testable gate exists on B's side.
2. **10-field contract header:** kernel responsibilities, canonical data, runtime owner, allowed actions, authority/privacy boundary, forbidden substitutes. B's "Data" section is one paragraph ("Consumes projected canonical: … metadata, provenance, truth state, relationships") — no kernel contract, no explainable-ranking inputs, no privacy/collective identity-stripping rules, no privacy policies on retrieval. This is the biggest structural gap.
3. **Truth-state taxonomy.** B says "All standard states" — vague; A's enumerated set (LOADING/EMPTY/OFFLINE/ERROR/NOT_VERIFIED/VERIFIED/BLOCKED/UNKNOWN/DISABLED) is the lockable list.
4. **Cross-room handoffs.** A lists seven (Today, Library, Lists, Ledger, Connections, Mail, Spaces), all carrying canonical IDs. B lists none.
5. **F-SEAM (new-intelligence seam).** A locks a conditional pill for arrivals while in the room; B has no equivalent — B's end-of-stream marker (C3) is doing double duty.
6. **F-DETAIL drawer.** A fully specified; B has no detail view at all — yet B's proof ("opening the same object from Feed/Library preserves canonical ID") implies one.
7. **F-FILTER sheet contents.** A specifies search + six filter groups + Apply/Clear all/Close footer; B only says "opens sheet".
8. **Mode default, URL routing, freshness label, "New since last visit."** A specifies; B silent.
9. **Wireframe.** A ships an annotated wireframe matching SPEC.md region-for-region; B has none.
10. **Explicit taste-question list.** A flags five; B flags zero, leaving its own ambiguities (default mode, tab count) unlabeled.

### Present in B, missing in A (A should absorb before freeze)
1. **First-3-seconds entry.** B specifies exactly what the eye lands on; A has no entry specification. (ROOM-BLUEPRINT-STANDARD-V1 structure; A lacks the whole element.)
2. **"Do not" anti-patterns list.** B: no social-media composer, no engagement-as-truth ranking, no fake activity, no object duplication per tab. A has forbidden substitutes but lacks the engagement-ranking and per-tab-duplication prohibitions as named rules.
3. **Naya prompt list.** B: "Why am I seeing this? / What matters most here? / How does this connect? / Explain this object." A specifies Ask Naya behavior but no canonical prompt set.
4. **Space-near-title rationale** (captured under C5).

### Internal inconsistencies found within each side (adversarial pass)
- **A:** (i) Pagination locked *and* flagged taste-open (C4) — must pick one. (ii) Wireframe shows F-DETAIL "Open in Today" unconditionally; SPEC says "Open in Today **(if a highlight)**" — the conditional is missing from the wireframe. (iii) SPEC text cites URL `/feed/personal`; wireframe note cites `/feed/collective` — the URL convention example is inconsistent. (iv) Predicate 2's "observable (different item sets / counts)" is weakly testable — modes may legitimately return overlapping items; needs a dataset-level assertion, not a visual one. (v) Predicate 5's "plain-language" and predicate 12's scroll-restore have no mechanical tolerance — vague predicates. (vi) Allowed actions includes `OPEN_IN_FEED (no-op here)` — a no-op action in an action allowlist is noise; either define it or drop it.
- **B:** (i) "All standard states" is not a specification — defers to an undefined standard. (ii) Tab list trails into "..." — the initial set is never actually fixed on B's side. (iii) Data section never names the projection event or its fields (IPC §12 gives a conceptual contract B could have referenced). (iv) No acceptance journey beyond two proof lines despite the blueprint standard requiring one.

### Wireframe-vs-SPEC check (A internal)
- Wireframe matches SPEC.md region-for-region: F-HDR, F-MODE, F-TABS, F-SEAM, F-STREAM (both cards), F-STATE, F-FILTER, F-DETAIL, legend. Card action rows match SPEC's seven controls; Share-absent-on-unauthorized is demonstrated on the second card. No controls appear in the wireframe that SPEC.md doesn't define. Two deltas: the "Open in Today" conditional (above) and the URL example (above). The wireframe's FIXTURE labeling is consistent with predicate 14.

### No-Hub-Capture audit
- Neither side violates the law. A's resolution note at the top of SPEC.md (removing `CAPTURE_SMART_NOTE` per the newer projection contract) is the correct precedence call. `SAVE_FAVORITE` and `ADD_TO_LIST` are Hub-owned organization actions (IPC §10 allowed). No client-side IB minting, no localStorage-as-source, no fake liveness on either side.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides' flagged items, deduplicated, plus new ones surfaced by this reconciliation. A's original five are kept verbatim in sense; new items marked **[new]**.

1. Truth-badge color semantics: should VERIFIED render green / NOT VERIFIED yellow / errors red? (A) — deliberately not invented; tokens don't define a semantic color mapping.
2. Pagination model: manual "Load more" vs infinite scroll. (A; sharpened by C4 — B's "continuous stream" language and A's internal locked-vs-open contradiction.)
3. Activity mode visual composition: same card stream (A's lock) vs distinct treatment — timeline? grouped by project? (A; FUNCTIONAL-SPEC left it open for design refinement.)
4. "New since last visit" placement: header (A's lock) vs floating over stream (A's alternative) vs end-of-stream marker (B's composition, C3).
5. Smart Tabs auto-evolution: may the room generate tabs from canonical metadata unasked, or does a new tab need explicit approval? (A; B's "..." implies evolution but never says.)
6. **[new]** Filter control placement: F-HDR right (A) vs right of Smart Tabs row (B). (C1)
7. **[new]** Space selector placement: F-MODE row (A) vs title row (B). (C5)
8. **[new]** Evidence label: "Open Source" (A) vs "Evidence" (B). (C6)
9. **[new]** Mobile F-DETAIL: bottom sheet (recommended extension of A's pattern) vs B's "no second rail/drawer" prohibition — exact mobile detail presentation. (C2)
10. **[new]** Global search: is the `[GLOBAL SEARCH]` in B's composition a shell-owned control, or does the room own any of it? (C9)

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION.** The spec may not freeze with the following items open — each is named, with the decision needed:

1. **Pagination model (blocker).** A is self-contradictory (locked manual button + taste-open flag) and B's "continuous stream" language points the other way. Director picks: manual "Load more" (recommended — mechanical scroll/return context, supports predicate 12) or infinite scroll. Until decided, predicates 2/12 can't be finalized.
2. **Mobile F-DETAIL (blocker).** A locks a right-overlay drawer; B prohibits a second rail/drawer on mobile. Resolve as: F-DETAIL becomes a bottom sheet on mobile (recommended), and A must add a mobile clause to F-DETAIL; B's prohibition must be amended to "no *side* drawer on mobile" or the recommendation rejected with an alternative.
3. **"New since last visit" placement (blocker-adjacent).** A (header) vs B (end-of-stream) vs A's own float alternative. Freeze provisionally with A's header placement; director confirms.
4. **Default mode confirmation (one-line).** A locks Collective as the director's preferred default. Director confirms the preference is current; B then states it explicitly and drops the PERSONAL-first ordering ambiguity.
5. **B must absorb A's structural spine before freeze:** acceptance predicates, contract-header fields (kernel responsibilities, allowed actions, privacy boundary, forbidden substitutes), truth-state taxonomy, cross-room handoffs, F-SEAM, F-DETAIL, F-FILTER contents. These are gaps, not disagreements — B's blueprint standard presumably requires them.
6. **A must absorb B's structural spine before freeze:** first-3-seconds entry, the "Do not" anti-patterns (engagement-ranking, per-tab duplication), Naya prompt list.
7. **A's internal cleanups (non-blocking, do before freeze):** resolve the pagination locked-vs-open flag (item 1 covers it); add the "(if a highlight)" conditional to the wireframe's F-DETAIL; fix the `/feed/personal` vs `/feed/collective` URL example mismatch; tighten predicates 2, 5, 12 into mechanical assertions; drop or define `OPEN_IN_FEED (no-op here)`.

**Non-blocking taste items** (freeze with A's provisional locks, director may override anytime): filter placement (A's F-HDR), Space placement (recommend B's title row, C5), "Evidence" vs "Open Source" (keep A's lock), truth-badge colors, Smart Tabs evolution permission, global-search ownership (confirm shell-owned).

**What is already solid and should survive unchanged:** room identity and instrument; the mode control and its above-tabs position; the eight-tab lock; card anatomy; the full object-control set with governed-Share semantics; the No-Hub-Capture posture on both sides; canonical-ID projection discipline; filter-as-sheet; mobile action-sheet collapse; the honest-state doctrine; `#55e39a` accent per tokens.
