# TODAY — Reconciliation: Lane A (`today/SPEC.md` + `today/wireframe.html`) vs Lane B (`grounding/blueprints/02-your-intelligence-today.md`)

**Reviewer stance:** adversarial toward both sides. Identifier check: A = my lane's SPEC-FIRST spec (today/SPEC.md, today/wireframe.html). B = Naya 3's blueprint (grounding/blueprints/02-your-intelligence-today.md). Grounding cited: `INTELLIGENCE-PROJECTION-CONTRACT-V1.md` (Projection Contract), `ROOM-FUNCTIONAL-CONTRACT-V1.md` (RFC), `ROOM-BLUEPRINT-STANDARD-V1` (_STANDARD.md), `1278-tokens.css`.

Headline: the two specs agree on the room's core story (title, nutshell, honest pulse, What Changed, reflection, loops, Reports handoff, no-capture law, quiet-day sentence). They diverge on **five build-scope questions** (stream, arc, play mode, highlight duplication, pulse 5th metric), **one naming question**, and B does not actually satisfy the blueprint standard it claims to follow.

---

## 1. AGREEMENTS

Locked identically on both sides (element named, both sides confirmed):

1. **Room identity:** title **"Your Intelligence Today"**; header shows date + current Space + honest freshness. A: T-HDR locks title, date in user's timezone, current Space, freshness line. B: composition row `[Your Intelligence Today] [Date] [Space] [Freshness]`.
2. **"Today in a Nutshell":** one-sentence day summary. A: T-NUTSHELL. B: `[ TODAY IN A NUTSHELL — one sentence ]`.
3. **Today Pulse = real canonical counts, no decoration:** A locks `Intelligence events · Discoveries · Learning signals · Decisions` + clickable-to-evidence stats, zero renders as zero, "no vanity scores". B locks the same first four metrics and the "Do not" ban on giant KPI tiles as decoration. (The 5th metric conflicts — see C1.)
4. **What Changed / highlight scenes region** exists with explainable selection. A: T-CHANGED + T-REEL with per-entry selection reason. B: `[ WHAT CHANGED ] Highlight Scene 1–3` with selection logic list.
5. **Naya's Reflection, evidence-grounded.** A: T-REFLECT with evidence links per claim. B: `[ NAYA'S REFLECTION — evidence-grounded ]`.
6. **Open loops + carry-into-tomorrow content** exists. A: T-LOOPS + T-CARRY. B: `[ OPEN LOOPS / CARRY INTO TOMORROW ]`. (Separate vs combined regions conflict — see C4.)
7. **End-of-room handoff: "View this week in Reports".** A: T-END primary → `/reports/week`. B: End control "View this week in Reports". Identical label.
8. **Cross-room handoffs by canonical ID:** both lock "Open in Feed" landing on the same canonical object (A: "identity matches character-for-character (no copy)"; B's data section: same canonical objects projected), plus Evidence/Source, Save, Add to List, Ask Naya, and a Ledger path. Consistent with Projection Contract §4 (one object → many projections, never copies).
9. **No-Hub-Capture law honored:** A field 9 forbids "capture/compose controls"; B explicitly locks "No capture/follow-up Smart Note control." Neither spec implies Hub-side creation of any canonical object. A's allowed-action set (PLAY/EXPLORE, ASK_NAYA, OPEN_*, SAVE_FAVORITE, ADD_TO_LIST, VIEW_*) is all projection/organization per Projection Contract §10.
10. **No manufactured highlights:** A field 9 + predicate 6; B "Do not … do not manufacture highlights." Both lock the verbatim quiet-day sentence: *"No major changes today. Here are the two things worth remembering."*
11. **10-second comprehension goal:** A predicate 1 ("understand the day within ~10 seconds", nutshell + pulse visible without scrolling); B proof ("User understands the day in ~10 seconds and can trace every highlight to source").
12. **Mobile:** vertical full-width story flow, sticky date/actions, evidence opens as a sheet without breaking the story. A §(b) Mobile + wireframe legend; B Mobile.
13. **Date navigation:** Today / Yesterday / date picker. A: T-DATE; B: header controls. (A additionally locks "Previous meaningful day" — see Gaps.)

---

## 2. CONTRADICTIONS

**C1 — Pulse 5th metric: "Creations" (A) vs "reports" (B).**
- A says: T-PULSE's fifth stat is *"Creations: N"* (locked in §b, wireframe stat row, predicate 2).
- B says: pulse row is `events | discoveries | learning | decisions | reports`.
- Recommended resolution: **adopt "reports".** The Projection Contract §1 names three canonical Hub input streams — Smart Notes/IBs, Activity, **Reports** — and A's own data contract (field 3) lists `INTELLIGENCE_REPORT` as a consumed object. "Creations" appears nowhere in grounding and overlaps upstream creation actions the Hub must not own. B's term wins on grounding; A must change a locked value → confirm with director, but the evidence favors B.

**C2 — Space selector in the room header (B) vs Space display-only (A).**
- A says: T-HDR shows current Space as context; room is "a module against the shared shell contract" — switching chrome lives in the shell.
- B says: header controls include a "Space selector".
- Recommended resolution: **adopt A (display-only).** RFC §7 requires Space to be *visible* where it affects results; it does not mandate a per-room selector. A second Space switcher inside the room duplicates shell chrome. Remove the selector from the room composition.

**C3 — Interpretation labeling: mandatory marker (A) vs silence (B).**
- A says: T-REFLECT/T-CARRY must carry the *"Naya's interpretation — not source truth"* marker in a distinct container (predicate 5).
- B says: "NAYA'S REFLECTION — evidence-grounded", with no interpretation-vs-truth distinction locked.
- Recommended resolution: **adopt A.** RFC §8: "Naya must distinguish suggestion from fact." B's evidence-grounding does not satisfy the suggestion/fact distinction. A's marker is the compliant implementation. Not optional.

**C4 — Open loops and carry-forward: two regions (A) vs one combined region (B).**
- A says: T-LOOPS (actionable checklist) then T-CARRY (interpretation panel) as separate regions.
- B says: single region `[ OPEN LOOPS / CARRY INTO TOMORROW ]`.
- Recommended resolution: **adopt A, with a grounding argument:** RFC §2's five-layer law separates ACTION (what can I do — loops are actionable) from INTELLIGENCE (what does Naya understand — carry-forward is interpretation). Merging them collapses two semantic layers. Director can overrule on taste, but the layer law favors A.

**C5 — T-STREAM (day-scoped compact stream with Collective/Personal/Activity modes): locked by A, absent from B.**
- A says: T-STREAM is a locked region — compact single-essence card list, same IntelligenceCard anatomy as Feed, three genuine scope modes, explicitly "a *view*, not a second feed".
- B says: nothing — but its anti-pattern "do not become Feed with bigger cards" leans against any feed-like element.
- Recommended resolution: **adopt A with its fences intact.** Projection Contract §4 explicitly permits Today to project the same IB by reference; B's anti-pattern targets "bigger cards," which A's compact single-essence list avoids by construction. The fences (compact, day-scoped, genuine modes, no second-feed duplication) are the reconciliation — removing any fence re-opens the conflict. This is build-scope-changing either way → blocking until decided.

**C6 — T-ARC (day arc strip): locked by A, absent from B.**
- A says: Morning/Midday/Afternoon/Evening density strip derived from real timestamps; clicking filters T-REEL.
- B says: nothing.
- Recommended resolution: **[NEEDS DIRECTOR TASTE].** No grounding mandates or forbids it; it is additive build scope. B's silence is not a veto. If kept, A's "purely derived — no decorative shape" rule stands.

**C7 — T-CHANGED vs T-REEL duplication (internal to A; B merges the two).**
- A says: T-CHANGED shows Discovery/Learning/Decision narrative highlights (one-line + Evidence + Open in Feed) AND T-REEL shows HighlightScene cards with six fields — but never states whether these are the *same* highlights rendered twice or *different* sets.
- B says: `[ WHAT CHANGED ]` contains `Highlight Scene 1, 2, 3` — one region, scenes only.
- Recommended resolution: **[NEEDS DIRECTOR TASTE] — blocking.** A builder cannot implement this without inventing: if the sets overlap, the room shows the same highlight twice (redundant); if they differ, the spec never says what distinguishes a "Changed entry" from a "Reel scene." One of three must be locked: merge into one region, or define the partition rule. Neither grounding decides this.

**C8 — Highlight card controls: "Open Origin" (B) vs A's three-way split.**
- A says: card row = Open (drawer) · Open in Feed · Open Source/Evidence · Save · Add to List · Ask Naya.
- B says: highlight controls = Open Origin · Evidence · Ask Naya · Save/List · Open in Feed · Day in Ledger.
- Recommended resolution: **adopt A's split; drop "Open Origin" as a separate control.** For a Today highlight, the origin of the projected object *is* the Feed object — B's "Open Origin" and "Open in Feed" resolve to the same destination, which is a dead-duplicate control (violates RFC §3 "no dead button"). A's "Open Source / Evidence" names the distinct case (underlying source ≠ projected object).

**C9 — Ledger entry point: per-highlight "Day in Ledger" (B) vs day-level T-END + per-object drawer link (A).**
- A says: "View day in Ledger" (day-level, T-END); the T-DETAIL drawer adds "View in Ledger" per object where applicable.
- B says: highlight-level control "Day in Ledger".
- Recommended resolution: **adopt A.** RFC §5: "Actions are context-sensitive." A day-level ledger view from a single highlight is incoherent scope; A's split (day-level for the day, per-object only when the object is itself consequential) is the context-sensitive placement.

**C10 — "[GLOBAL SEARCH]" in B's desktop composition.**
- B says: composition opens with `[GLOBAL SEARCH]`.
- A says: room renders inside the shared shell's center workspace; rails belong to the shell.
- Recommended resolution: **adopt A — global search is shell chrome, not room composition.** Remove from the room blueprint.

**C11 — Primary instrument naming: "The Daily Intelligence Story" (B) vs highlight reel / THE HIGHLIGHT REEL (A).**
- A says: metaphor THE HIGHLIGHT REEL; T-REEL is the signature instrument.
- B says: primary instrument is "The Daily Intelligence Story".
- Recommended resolution: **[NEEDS DIRECTOR TASTE].** These may be two names for one instrument (story = reel) or two framings (reel = scenes; story = narrative arc). The blueprint must lock one name; nothing in grounding decides. Minor but blocking for naming consistency across rooms.

**C12 — Scene count: B's "Highlight Scene 1, 2, 3".**
- B says: composition lists exactly three scenes.
- A says: dynamic scene list from highlight selection.
- Recommended resolution: **adopt A's dynamic count; B's "1, 2, 3" is illustrative.** Locking exactly three scenes would manufacture or truncate highlights — contradicting both specs' no-manufacture rule.

**C13 — Data-contract naming: B's "decisions/learning/evidence".**
- B says: room consumes canonical objects "projected from: Smart Notes; Activity; Reports; decisions/learning/evidence."
- A says: `INTELLIGENT_BLOCK` / `ACTIVITY_EVENT` / `INTELLIGENCE_REPORT`, referenced by canonical ID, highlights are references never copies.
- Recommended resolution: **adopt A's naming.** Decisions/learning are *types* of intelligent blocks, not canonical object classes; "evidence" is a relationship, not a stream. Cite Projection Contract §§1, 4. B's list invites a builder to invent object classes.

---

## 3. GAPS

### Present in A, missing in B
- **T-PLAY** guided step-through overlay (Previous/Next/Close; "play = guided presentation, never video"). B has no play mode at all.
- **"Previous meaningful day"** control (most recent day with ≥1 highlight).
- **T-ARC** day arc (see C6).
- **T-STREAM** compact day-scoped stream + Collective/Personal/Activity mode selector (see C5).
- **T-DETAIL / T-EVID drawer** spec (canonical ID visible, provenance, handoffs).
- **T-QUIET** as a designed region (B names the quiet-day sentence under States but gives it no composition slot).
- **Full truth-state list:** LOADING · EMPTY/QUIET DAY · READY · OFFLINE (honest stale label) · ERROR · NOT_VERIFIED · VERIFIED · UNKNOWN · DISABLED. B locks only the quiet-day sentence.
- **Acceptance predicates** (A's 13) and any click-by-click acceptance journey.
- **Component inventory** (17 components, token notes).
- **Privacy/authority boundary:** Collective-mode highlights identity-stripped; Personal-mode may show owner context (Projection Contract §7).
- **URL/date routing** (`/today/2026-10-01`), back/forward restores day, reload preserves date + scroll.
- **Kernel responsibilities** (canonical events scoped to date+Space, real pulse counts, highlight candidates with selection reasons, grounded reflection, open-loop/carry-forward tracking).
- **Freshness honesty rule** (never "updated N min ago" when stale).
- **Wireframe** (annotated, fixture-labeled).
- **OPEN TASTE QUESTIONS** (5 flagged).

### Present in B, missing in A
- **First-3-seconds entry statement** (date+Space+freshness, nutshell, pulse, first major highlight). A's nearest equivalent is predicate 1's 10-second claim; A never specifies the literal first paint.
- **Standalone "Do not" anti-pattern section** (B: don't become Feed with bigger cards; don't manufacture highlights; no giant KPI tiles). A's field 9 covers equivalents but buries them in the contract header; a dedicated anti-patterns block is more buildable.
- Nothing else of substance: B's remaining unique elements (Space selector, Open Origin, highlight-level Day in Ledger, GLOBAL SEARCH, "reports" pulse metric) are all contradictions resolved above, not true gaps.

### Missing from both / non-conformances found adversarially
- **B does not satisfy ROOM-BLUEPRINT-STANDARD-V1 despite the task's claim it follows it.** Missing outright: §9 Naya behavior, §11 accessibility, §12 visual law, §13 acceptance journey; thin to the point of non-conformance: §6 data contract, §7 states (one sentence), §8 handoffs (controls only, no destinations/identity rules). A cold builder cannot reproduce the room from B alone.
- **A omits BLOCKED and UNAUTHORIZED** from its truth states; RFC §6 lists both as minimum runtime states. Small gap in A.
- **A's wireframe omits the T-DETAIL/T-EVID drawer** locked in SPEC §(b) — internal drift; the wireframe's claim "matches today/SPEC.md" is false on this point.
- **A's T-LOOPS checkbox has no defined causal path.** Checking a loop presumably resolves it — is that a Hub-local state change (fake) or an upstream handoff to the governed runtime (Projection Contract §3: Ask Naya hands intent upstream; §10 reserves canonical changes to upstream)? Unspecified. This is the one place in either spec that flirts with a No-Hub-Capture violation: a checkbox that silently mutates canonical loop state client-side would break §3. Must be specified as disabled-with-explanation or upstream-handoff before freeze.
- **Vague predicates in A (not actually mechanical despite the "mechanical gate" claim):** P1 "the human understands the day" is untestable; P11's "performs no client-side day synthesis presented as canonical" has no stated test; P13 ("a FIXTURE cannot satisfy predicates 1–12") is a meta-claim about the dev environment, not a room property. Recommend tightening or demoting to non-acceptance notes.
- **Wireframe styles card [Open] as primary** (`btn small primary`); SPEC §(b) never designates a primary action within the card row. Minor drift.
- **A's T-STREAM mode selector defaults to "Collective"** in the wireframe seg control while the room is personal-first ("Your Intelligence Today"); defaulting to Collective on a personal room deserves a line of justification or a change to Personal-first.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides' flagged items, deduplicated. B flags none explicitly, so this is A's five — all still open:

1. [NEEDS DIRECTOR TASTE] **Interpretation panel styling** — distinct container + micro-label is locked; the exact visual distinction (tint? border? icon?) is undecided.
2. [NEEDS DIRECTOR TASTE] **Highlight grouping** — time-of-day vs meaningful chapters; spec rule is "time grouping only when it adds meaning." Confirm.
3. [NEEDS DIRECTOR TASTE] **Day arc as Play-mode progress indicator** — undecided.
4. [NEEDS DIRECTOR TASTE] **"Previous meaningful day" threshold** — ≥1 highlight vs any pulse activity.
5. [NEEDS DIRECTOR TASTE] **T-STREAM depth** — compact single-essence cards (locked) vs full Feed card with actions/why-line. Locked compact pending this decision.

Note: contradictions C1 (pulse 5th metric), C4, C5, C6, C7, C11 above also require director input and are carried into §5 as blockers.

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION.** Blocking items by name:

1. **T-STREAM include/cut + depth** (C5 + taste question 5) — largest compositional divergence; changes the room's lower half.
2. **T-CHANGED vs T-REEL duplication** (C7) — same-highlights-twice vs partition rule must be locked; a builder will otherwise invent it.
3. **T-ARC include/cut** (C6) — additive scope; keep requires the "purely derived" rule to stay.
4. **T-PLAY include/cut** (gap in B) — A locks a full overlay mode B never contemplated.
5. **Pulse 5th metric** (C1) — recommend "reports" per Projection Contract §1; changes A's locked value, needs director confirmation.
6. **Instrument naming** (C11) — "Highlight reel" vs "Daily Intelligence Story"; lock one.
7. **T-LOOPS checkbox causal path** (§3 non-conformance) — specify disabled-with-explanation or upstream handoff; cannot freeze with a control whose result state is undefined (RFC §3) and which risks a silent No-Hub-Capture violation.
8. **"Previous meaningful day"** (gap in B + taste question 4) — include/cut + threshold definition.

Non-blocking resolutions (adopt with grounding cited; no director taste needed):
- Interpretation marker (A wins, RFC §8); Space display-only (A wins, shell contract + RFC §7); no in-room global search (A wins, shell contract); drop "Open Origin" (RFC §3 no-dead-button); day-level Ledger placement (A wins, RFC §5); dynamic scene count (both specs' no-manufacture rule); contract-aligned data naming (A wins, Projection Contract §§1, 4).
- Lane-A repairs before freeze: add T-DETAIL/T-EVID to the wireframe; add BLOCKED/UNAUTHORIZED states; tighten predicates 1, 11, 13; justify or fix the Collective-default mode selector.
- Lane-B repairs before freeze: backfill the missing blueprint-standard sections (§6 data contract, §7 states, §8 handoffs, §9 Naya behavior, §11 accessibility, §12 visual law, §13 acceptance journey) — B is currently not standard-conformant.
