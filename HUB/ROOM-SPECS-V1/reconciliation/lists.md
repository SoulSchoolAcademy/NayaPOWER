# LISTS reconciliation — independent review

**Sides:** A = my lane (`lists/SPEC.md` + `lists/wireframe.html`); B = Naya 3's lane (`grounding/blueprints/08-smart-lists.md`).
**Grounding consulted:** `INTELLIGENCE-PROJECTION-CONTRACT-V1.md` (No-Hub-Capture law), `ROOM-FUNCTIONAL-CONTRACT-V1.md` (five layers, 11-state model, universal control rules), `1278-tokens.css` (`--accent-lists`, `--fs-title`, `--fs-small`, `--muted` all verified present), `blueprints/_STANDARD.md` (ROOM-BLUEPRINT-STANDARD-V1, 15 required sections).

**Up-front correction to the task premise:** B does *not* follow ROOM-BLUEPRINT-STANDARD-V1. The file is a ~30-line stub with 8 fragmentary sections (Purpose, First 3 seconds, Desktop composition, Primary instrument, Controls, Data, Do not, Proof). It is missing 7 of the 15 required standard sections (States, Handoffs, Naya behavior, Mobile, Accessibility, Visual law, Acceptance journey). This asymmetry dominates the reconciliation: A is a buildable spec with gaps; B is an early fragment.

**No-Hub-Capture audit (both sides):** No silent violation found in either side. A's `CREATE_LIST`/`ADD_ITEM`/`PIN_REORDER`/`MOVE_LANE`/`SET_SMART_RULE` operate on *list definitions and item references* in "the governed list store" — organization actions the projection contract explicitly permits the Hub to own (§10: "add canonical object to a list" is Hub-owned). A never mints canonical IBs, reports, or activity. `ASK_NAYA_ORGANIZE` hands intent to Naya (human confirms) — the sanctioned pattern. `CONVERT_IF_REAL_OPERATION` defers to a real upstream operation or stays disabled-with-reason. B's `add/remove reference` is equally clean. One watch item: A's runtime owner names ("governed list store", "governed intelligence runtime", SPEC §a-4) are not bound to any concrete canonical seam/adapter identifier — a cold builder cannot resolve them. Not a capture violation, but an unanchored seam name (see Gaps).

---

## 1. AGREEMENTS

Both sides lock the same element, stated independently:

1. **Human job / purpose.** A §a-1: "What am I deliberately organizing, tracking or returning to?" B Purpose: "Let the human intentionally organize canonical intelligence without copying it." Same job.
2. **Reference-not-copy data model.** A §a-3: list holds `{canonical_object_id, lane, pinned, order, added_at, added_by}`; "the item payload is always the canonical object; the list holds references." B Data: "List membership references canonical object IDs." B Proof: "Same canonical object can appear in multiple lists without duplication." Identical data law; A is the detailed form of B's one-liner.
3. **Seven fixed lanes, exact labels and order.** A §b-R3: NOW · NEXT · WAITING · QUESTIONS · IDEAS · OPPORTUNITIES · COMPLETED. B desktop composition: `[ NOW ] [ NEXT ] [ WAITING ] [ QUESTIONS ] [ IDEAS ] [ OPPORTUNITIES ] [ COMPLETED ]`. Locked identically.
4. **No per-list invented state models.** B Do-not: "do not let every list invent its own state model." A: fixed seven-lane set + fixed 11-state truth model (§a-7) + per-list lane question explicitly left to the director (taste Q1) rather than letting lists improvise. Conceptual agreement.
5. **No copying canonical objects into list storage.** A §a-2, §a-9 ("forbidden local substitutes"), predicate 1. B Do-not: "do not copy object content as new truth." Identical prohibition.
6. **Signature instrument.** A: "Living Mission Table." B: "Mission Table / Smart Collection." Same instrument (and "mission table" is the Functional Contract §2 canonical instrument name for this room).
7. **Room name "Smart Lists."** Both title the room identically (directory/file names "lists" vs "08-smart-lists" are lane conventions, not a product naming disagreement).
8. **Core control set (existence, not placement).** Both specify: list selector, create list ("New list"), add/remove reference, move-lane control, open-canonical-object, and a why-here explanation (A: ambient "WHY THIS IS HERE" strip; B: "Ask Naya why here" control — substance agrees, mechanism differs; see Contradictions).
9. **No mystery auto-prioritization / no silent Naya reordering.** A §a-9 forbids "mystery auto-prioritization"; A §b-R4 "Ask Naya to organize … Naya never silently reorders." B's fragment doesn't contradict; B's Do-not set is narrower but compatible.
10. **Naya must explain membership.** A kernel responsibility §a-2: explain every smart inclusion ("WHY THIS IS HERE"). B Controls: "Ask Naya why here." Both lock explanation-of-membership as a requirement.

---

## 2. CONTRADICTIONS

**C1 — Layout: where the list selector lives.**
- A says: R2 is a left-column selector rail (search "Search lists", list rows with type badges/counts/sharing icons, "Smart starters" section); R1 header holds only title/promise left, Space chip + truth badge + "New list" right. Wireframe matches exactly.
- B says: desktop composition top row is `[Smart Lists] [List selector] [New list]` — the selector sits inline in the header row; no left rail, no context column, no R2-equivalent placement defined.
- Recommended resolution: **A wins.** A's placement is wireframe-verified and expresses the Functional Contract §1 five layers (R1 = Orientation, R2/R3 = Current State); B's fragment gives no region semantics and drops the selector rail entirely. Grounding: buildability + five-layer law. B's composition should be retired.

**C2 — Ask-Naya mechanism: ambient explanation vs on-demand control.**
- A says: explanation is ambient — the "WHY THIS IS HERE" strip is rendered on every smart-matched item (Naya-labeled, `--accent-lists` border, `--fs-small`); the interactive control is "Ask Naya to organize" (Naya proposes moves, human confirms).
- B says: the control is "Ask Naya why here" (on-demand explanation); no organize action, no ambient strip.
- Recommended resolution: **A wins on explanation** (ambient strip satisfies A's own kernel responsibility "explain every smart inclusion" and Functional Contract §8's explain behavior, without an extra click); B's "Ask Naya why here" is redundant against the strip and should be dropped. A's "Ask Naya to organize" has no B counterpart — its *scope* is already A's open taste question 6, which stands.

**C3 — Per-item "status" field.**
- A says: status is derived from lane position + `BlockerState` ("Blocked: <reason>") + smart-rule badge + completion evidence in COMPLETED. No standalone "status" field.
- B says: each item shows "status" as a distinct field, undefined.
- Recommended resolution: **A wins.** A's lane+blocker model is the concrete, testable realization of B's vague field, and B's own anti-pattern ("do not let every list invent its own state model") forbids the freeform reading of "status." Grounding: B's anti-pattern + Functional Contract §6 (fixed state vocabulary).

**C4 — Per-item "source room" display.**
- A says: origin room is reachable via the canonical ID chip ("IB-2409", click opens the object in its originating room) plus handoff "list item → open in originating room" (§a-8). The origin room is *not* shown as a labeled per-item field.
- B says: each item shows "source room" as a visible field.
- Recommended resolution: **A's mechanism satisfies the identity rule** (Functional Contract §4: one canonical ID everywhere; A predicates 1 and 7 lock identical resolution from list and origin room). B's visible-label intent is unaddressed in A — recommend the chip expose origin room on hover/at minimum the click-through, but do not treat as a freeze blocker. Small, grounded in §4; if contested, [NEEDS DIRECTOR TASTE].

**C5 — Global search placement.**
- A says: room-level search only ("Search lists" in R2); no global search element in the room spec. Wireframe shows the Hub room rail but no global search box in the room.
- B says: desktop composition opens with `[GLOBAL SEARCH]` as a room element.
- Recommended resolution: **exclude from the room spec.** Global search is a Hub-shell concern, not a room control; the room's search obligation is R2 list search. B's fragment conflates shell and room.

**C6 — Rename/archive list.**
- A says: nothing. No rename or archive control, no acceptance, not in taste questions.
- B says: Controls include "create/rename/archive list."
- Recommended resolution: **fold into A as overflow actions** ("⋯"), grounded in Functional Contract §3 (overflow = low-frequency operations). Archive semantics (soft vs hard, what happens to shared references) are unaddressed by both — flag as a minor open question for the builder/spec pass, not necessarily director taste.

**C7 — "Locked" status vs open taste questions (internal to A, affects the freeze).**
- A says: header status "SPEC-FIRST LOCKED (CANDIDATE — no build authorized)" while simultaneously carrying 6 open [NEEDS DIRECTOR TASTE] questions, one of which (lane model, Q1) is structurally load-bearing for all of R3.
- Recommended resolution: the word LOCKED is misleading as written; status should read "SPEC-FIRST DRAFT — 6 taste questions open, no build authorized" until the director answers. Not a product disagreement, but the freeze recommendation must not inherit the word "LOCKED."

**C8 — Component-invention claim (internal to A).**
- A §c says: "All components use the shared tokens (1278-tokens.css); no new tokens, no new components invented."
- The same section then inventories `ListItem`, `WhyThisIsHere`, `SmartRuleBadge`, `LaneMenu`, `PinToggle`, `SmartRuleEditor`, `NayaOrganizer`, `CompletedEvidence`, `OpportunityState` — all room-specific components.
- Recommended resolution: reword to what is actually true and verifiable: "no new *tokens*; room assembles room-specific components from shared token primitives." As written the claim is false on its face. Related: `OpportunityState` is named but never defined anywhere in the spec (dangling), and §c's "Needed-but-not-existing variants are listed under OPEN TASTE QUESTIONS" is inaccurate — the taste questions list semantic questions, not component variants.

**C9 — Predicate 4 "behave distinctly" is not testable.**
- A predicate 4: "NOW / NEXT / WAITING / QUESTIONS / IDEAS / OPPORTUNITIES / COMPLETED behave distinctly: items moved between lanes keep identity, lane moves are recorded, COMPLETED items remain inspectable with completion evidence."
- Problem: only COMPLETED has defined distinct behavior. Nothing in the spec defines what IDEAS does distinctly from OPPORTUNITIES, or WAITING from NEXT. "Behave distinctly" cannot be executed by an independent reviewer.
- Recommended resolution: either the director defines per-lane semantics ([NEEDS DIRECTOR TASTE] — this is product meaning, not spec wording), or narrow the predicate to what is actually specified (identity preservation, move recording, COMPLETED inspectability). Do not freeze with the current wording.

**C10 — Truth-state scoping and rendering (internal to A).**
- A §a-7 names all 11 Functional-Contract states, but never scopes them: does VERIFIED/NOT_VERIFIED apply to the list, the item, the room, the smart rule? Predicate 9 requires EMPTY (room + list), ERROR, OFFLINE, NOT_VERIFIED as "real rendered states," yet §b-R5 only renders EMPTY/ERROR/OFFLINE — NOT_VERIFIED has no treatment anywhere.
- Recommended resolution: spec fix before freeze — scope each state to its object (room / list / item / rule) and add the missing NOT_VERIFIED treatment, or drop it from predicate 9.

**C11 — "Convert to Space/report" scope creep (internal to A).**
- A §a-6 (authority boundary): "converting a list into a Space/report is offered only where a real operation exists." A §a-8 handoffs and §b-R4 define only "Convert to Space."
- The "/report" conversion appears nowhere else: no control, no dialog, no predicate. Dangling.
- Recommended resolution: delete "/report" or promote it to a defined control with the same disabled-with-reason treatment. One-word spec fix.

**C12 — "Drive notes" citation is unverifiable.**
- A taste Q1: "This spec implements per-list lanes per the Drive notes — confirm or correct."
- The Drive notes are not in the grounding available to this review; the citation cannot be checked. The lane model therefore rests on an unverifiable source.
- Recommended resolution: keep Q1 as [NEEDS DIRECTOR TASTE] (it already is); do not treat "per the Drive notes" as grounding. A frozen spec must not cite evidence the reviewer cannot read.

---

## 3. GAPS

**B (blueprint fragment) is missing — 7 of 15 standard sections absent:**
- Truth states (standard §7) — no states at all, despite "First 3 seconds" implying a ready state.
- Cross-room handoffs (standard §8) — no "Add to list" inbound, no open-in-origin-room, no Ledger, no Space handoff.
- Naya behavior (standard §9) — only the "Ask Naya why here" control; no behavior contract.
- Mobile transformation (standard §10) — nothing.
- Accessibility (standard §11) — nothing.
- Visual law (standard §12) — no route, no theme tokens, no metaphor, no density/hierarchy.
- Acceptance journey (standard §13) — "Proof" is a single criterion ("same canonical object in multiple lists without duplication"), not a click-by-click journey.
- Also missing within present sections: no rule-authoring/explanation UI (smart lists are central to B yet no SmartRuleEditor equivalent), no share/convert controls, no pin control, no lane-move menu, no starter-type definitions, no data-contract shape beyond one line.

**A (my lane's spec) is missing:**
- Rename/archive list controls (B has them; see C6).
- Accessibility section — A has none either. Both sides lack it; standard §11 requires keyboard/focus/labels/zoom.
- First-3-seconds entry narrative — A implies it via R1 + R5 EMPTY-room treatment but never states the entry state explicitly (B has the section; A should adopt the habit).
- Consolidated Naya behavior section — A's Naya behavior is scattered across the WHY strip (§b-R3), "Ask Naya to organize" (§b-R4), and predicate 11. No single behavior contract.
- Runtime seam binding — "the governed list store" / "governed intelligence runtime" (§a-4) name no concrete adapter/seam identifier a builder can implement against.
- Acceptance *journey* — A has 11 strong predicates but no click-by-click journey (standard §13 asks for the journey; predicates are the assertions, not the walkthrough).
- Per-lane semantics — what each of the seven lanes *means* (feeds C9).
- Visual-law prose — A names tokens and theme (all verified present in `1278-tokens.css`) but not density, depth, or hierarchy.
- Wireframe-vs-spec nit: the wireframe's COMPLETED-lane item omits the canonical ID chip, but predicate 1 requires *every* list item to display its canonical object ID. Wireframe fix.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides' flagged items, deduplicated. B flags none explicitly; all six are A's:

1. [NEEDS DIRECTOR TASTE] **Lane model** — are the seven lanes per-list or global across lists? (Load-bearing for R3; currently implemented per-list on an unverifiable "Drive notes" citation — see C12.)
2. [NEEDS DIRECTOR TASTE] **Smart rule language** — which fields and operators may rules reference, and who may author them: human only, or Naya-suggested with human approval?
3. [NEEDS DIRECTOR TASTE] **"Convert to Space"** — which real operations exist behind it? (Button correctly stays disabled-with-reason until answered.)
4. [NEEDS DIRECTOR TASTE] **List sharing governance** — who may be granted access, at what scopes, is resharing allowed?
5. [NEEDS DIRECTOR TASTE] **Ordering semantics on smart lists** — does human pin/reorder override rule ordering, or are smart lists strictly rule-ordered with pinning as overlay?
6. [NEEDS DIRECTOR TASTE] **"Ask Naya to organize" scope** — may Naya propose cross-list moves and rule changes, or only within-list lane moves?

Reviewer-added items that are *not* director taste (spec-hygiene, fix before build): C8 (component-invention reword + define or drop `OpportunityState`), C10 (scope truth states; add NOT_VERIFIED treatment), C11 (resolve "/report"), rename/archive overflow placement (C6), runtime seam binding, COMPLETED-item chip in wireframe, per-lane semantics or narrowed predicate 4 (C9 — the *wording fix* is hygiene; the *semantics* are taste).

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION** — not ready to freeze. Blocking items, in order:

1. **B's status must be resolved first.** B is a non-conforming fragment (7/15 standard sections missing), not a competing blueprint. Do not freeze two specs. Recommended path: A is the spec; fold B's deltas into A (rename/archive per C6, visible source-room consideration per C4); retire B's layout fragment (C1, C5).
2. **Lane model** (taste Q1) — structurally load-bearing; R3 cannot freeze while per-list vs global is open.
3. **Smart rule language + authorship** (taste Q2) — load-bearing for the SmartRuleEditor contract and predicate 3.
4. **Ordering semantics on smart lists** (taste Q5) — load-bearing for predicate 5 (pin/reorder path).
5. **Sharing governance** (taste Q4) — load-bearing for the R4 "Share list…" control's enabled/disabled contract.
6. **"Ask Naya to organize" scope** (taste Q6) — load-bearing for the Naya behavior contract.
7. **Convert-to-Space operations** (taste Q3) — already handled honestly (disabled-with-reason), but the control's future contract needs the answer.
8. **Predicate 4 must be made testable** (C9) — define per-lane semantics (taste) or narrow the predicate (hygiene).
9. **Truth-state scoping + NOT_VERIFIED treatment** (C10) — an 11-state claim with 4 rendered states is not freezable as written.
10. **A's "LOCKED" status line** (C7) — reword to draft-with-open-questions; the freeze must not inherit a false locked claim.

**Non-blocking before freeze, must-fix before build:** C8 (component-invention reword; define/drop `OpportunityState`; fix the needed-variants claim), C11 ("/report" dangling), runtime seam binding for "governed list store," wireframe COMPLETED-item ID chip, accessibility section (both sides lack it), click-by-click acceptance journey to complement the predicates, first-3-seconds entry statement, consolidated Naya behavior section.

**What is genuinely strong and should survive untouched:** the reference-not-copy data law (both sides, projection-contract-clean), the seven fixed lanes, the no-per-list-state-model discipline, the WHY strip with Naya/source-truth visual separation, the non-drag reorder path, disabled-with-reason instead of dead buttons, the starter-type labels, and the 11 acceptance predicates modulo C9/C10.
