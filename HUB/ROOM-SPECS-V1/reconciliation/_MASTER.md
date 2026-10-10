# ROOM BLUEPRINT RECONCILIATION — MASTER

**Independent review of the two spec efforts, per Shawn's #554 directive (comment 5944571912):**
no production room building until the 11 room blueprints are independently reviewed.

- **Side A** — SPEC-FIRST pass (SN-0139): `~/workspace/room-specs-v1/<room>/SPEC.md` + `wireframe.html`
- **Side B** — Naya 3's lane (PR #1290, `naya/hub-room-functional-spec-v1 @ 5837f01f`): `~/workspace/room-specs-v1/grounding/blueprints/`
- Method: 11 independent room reviewers (one per room), adversarial toward both sides, read-only on GitHub. Per-room files: `~/workspace/room-specs-v1/reconciliation/<room>.md`.
- Review date: 2026-10-01/02. All CANDIDATE. Nothing merged, frozen, or built.

---

## 1. HEADLINE VERDICT

**0 of 11 rooms are ready to freeze. 11 of 11 NEED RESOLUTION.**

This is not a close call in any room. The blockers are real: compositional forks, self-contradictory specs, untestable predicates, and ~70 unique open taste questions. Freezing now would freeze the contradictions in.

---

## 2. THE SINGLE BIGGEST FINDING — THE TASK PREMISE WAS WRONG

The reconciliation was commissioned as "two complete specs, reconcile them." That premise does not survive contact with the files:

- **Side B's blueprints do not follow ROOM-BLUEPRINT-STANDARD-V1.** The standard demands 15 sections. The actual files are 46–92 lines each (642 lines total across all 11 rooms) — stub format. Verified section-by-section: feed, reports, library, connect, ledger, connections, lists, mail, spaces, settings, and today blueprints each omit between 5 and 8 required sections (truth states, handoffs, Naya behavior, mobile, accessibility, visual law, acceptance journey recur as the missing). Lists (`08-smart-lists.md`, 48 lines) is a fragment, not a blueprint. **Not one of the eleven is buildable-from per its own standard's definition** ("complete enough that a cold builder can reproduce the intended interface without inventing layout, controls, state, or feature scope").
- **Side A is the only buildable layer** — contract headers, component inventories, acceptance predicates, truth-state taxonomies, handoffs — but it is not freeze-ready either (see §4).

The standard itself is good. It was written and never applied — including, notably, by its own lane. The freeze path is therefore not "pick A or B." It is: **repair A, fold B's deltas in, enforce the 15-section standard as a conformance gate.** (Recommendation details in §7.)

Side B's substantive contributions are real but delta-sized, and every one of them should be preserved:
ledger's OBSERVED stage (adopts into the 4-stage chain — grounded in the Demo-1 directive, not taste); feed's title-row Space rationale; connections' panel-first behavioral law ("do not make graph the product" written into the spec); spaces' module list (closer to the Drive-notes list than A's); mail's "compose where connected" guard; library's `object_type` catch (A's card spec omits a field the projection contract's event carries); reports' instrument naming ("Time Synthesis Reader"); settings' System Health placement (out of the rail); connect's mobile full-screen detail clause; today's pulse-5th-metric correction ("reports," per the projection contract's canonical input streams).

---

## 3. PER-ROOM SCORECARD

| Room | Contradiction items | Taste Qs (unique) | Freeze verdict | Blocking items (count) |
|---|---|---|---|---|
| feed | 9 | 10 | NEEDS RESOLUTION | 7 |
| today | 13 | 5 | NEEDS RESOLUTION | 8 |
| reports | 12 | 6 | NEEDS RESOLUTION | 6 |
| library | 10 | 7 | NEEDS RESOLUTION | 8 |
| connect | 12 | 9 | NEEDS RESOLUTION | 7+ |
| ledger | 8 | 6 | NEEDS RESOLUTION | 7 |
| connections | 9 | 7 | NEEDS RESOLUTION | 7 |
| lists | 12 | 6 | NEEDS RESOLUTION | 10 |
| mail | 13 | 8 | NEEDS RESOLUTION | 6 |
| spaces | 8 | 8 | NEEDS RESOLUTION | 8+ |
| settings | 8 | 6 | NEEDS RESOLUTION | 5 |
| **TOTAL** | **~114** | **~70** | **0 / 11 ready** | **~80** |

"Contradiction items" counts A-says/B-says pairs plus internal-to-side defects; the true distinct decision points are ~80–90. Taste-question mentions total 107 across files; deduplicated ≈ 70.

---

## 4. SYSTEMATIC DEFECTS IN SIDE A (my lane — the review cut both ways)

1. **Premature "LOCKED" claims.** 9 of 11 SPEC.md files carry LOCKED / "LOCKED FOR FIDELITY BUILD" headers while holding open [NEEDS DIRECTOR TASTE] questions (ledger: 6 open; lists: 6 open). Per Shawn's law ("taste belongs at blueprint stage"), every one of these headers is false. Downgrade all to DRAFT until taste questions clear.
2. **SPEC↔wireframe drift is systematic, not incidental.** Mail's wireframe heads a section "Capture" while its SPEC mandates "Ask Naya to note this" (a No-Hub-Capture framing violation *in my own lane's wireframe*). Connect's wireframe draws a live Connect button its Predicate 2 forbids, and shows 3 doors in the bay vs 2 in the list. Today's wireframe omits the T-DETAIL/T-EVID drawer its SPEC locks. Settings' wireframe mis-files "Sign out" and "Motion preference" against its own SPEC categories, and renders System Health inside the rail its predicate excludes. Library's wireframe prejudges an open taste question (the why-strip treatment). Connections' wireframe legend preempts an undecided encoding mapping and merges sections its SPEC separates. Spaces' wireframe invents a per-portal truth badge contradicting A's own truth-state model, omits the required "Find a Space" search, and pre-decides an open section-order question. **The wireframes are not illustrations of the specs — they are independent spec surfaces, and they disagree with their specs in 7 of 11 rooms.** Freeze rule: wireframes must be regenerated *from* repaired specs, never edited independently.
3. **The signature predicate is a slogan.** "A fixture cannot improve the room's score" appears in feed, library, connections, and mail — untestable in all four (no scoring mechanism exists). Rewrite against the Sample Data Law in every spec or strike it.
4. **Ungrounded inventions inside "locked" specs.** Lists' `OpportunityState` (dangling, undefined) inside a spec claiming "no new components invented." Spaces' LEAVE-PENDING state (plausible, ungrounded). Ledger's pred 9 references a phantom "Receipts" door control. Connect's pred 2 references a "live grouping" that exists nowhere. Predicates that test nonexistent controls are defects, not gates.
5. **Vague predicates wearing mechanical clothing.** Feed's pred 2 ("observable"), pred 5 ("plain-language"), pred 12 (scroll-restore with no tolerance); today's preds 1/11/13; lists' pred 4 ("behave distinctly" — only COMPLETED has defined behavior). Every predicate must name its instrument or be rewritten.

## 5. SYSTEMATIC DEFECTS IN SIDE B (her lane)

1. **Standard non-conformance** (§2 above) — the headline defect.
2. **Internal self-contradictions.** Feed's blueprint locks manual "Load more" while flagging it taste-open (a thing cannot be both). Connect's blueprint specifies an inline detail panel while its own mobile clause demands full-screen detail.
3. **Ungrounded taxonomies.** Connections' "People | Systems | All" tabs have no data-contract referent. Settings' standalone Authority/Security/Data categories are labels with zero rows, controls, or scope law.
4. **Dropped signature elements.** Spaces' blueprint drops the gallery view its own FUNCTIONAL-SPEC requires as the signature visual. Reports' blueprint carries a highlight-card strip that contradicts its own "Time Synthesis Reader, not a grid of report cards" instrument.
5. **Compositional silence where the standard demands decisions.** B repeatedly names no primary action, no placements, no acceptance journey — the exact decisions a cold builder needs.

## 6. CROSS-ROOM CONTRADICTIONS — DECIDE ONCE, NOT PER ROOM

These are governance decisions. Resolving them room-by-room will re-create the drift the freeze is meant to end:

1. **Detail-presentation law.** Feed locks a right-overlay drawer; connect locks a slide-over; library locks full-center takeover; B variously prohibits drawers ("no second rail/drawer") and specifies inline panels. **Four different answers to the same question.** One governed detail-presentation pattern (with the mobile transformation) must be locked before any room freezes. Feed's mobile F-DETAIL is the sharpest instance: A's drawer vs B's prohibition cannot both ship.
2. **Truth-badge ownership.** Spaces' wireframe puts truth badges on Space portals; the truth-state model says truth states belong to *intelligence inside* a space. Lock: badges annotate objects, never containers.
3. **[GLOBAL SEARCH] boundary.** B's compositions plant `[GLOBAL SEARCH]` in today, ledger, mail, spaces, and connect. Is global search shell chrome or room content? One decision; rooms must not each re-answer it.
4. **Accent collisions (tokens are visual law — verified in `1278-tokens.css`).** `--accent-feed` and `--accent-connect` both resolve to `var(--green)`; `--accent-library` and `--accent-mail` both resolve to `var(--blue)`. Two rooms sharing one accent each. Tokens win over prose, but room identity deserves a director look — changing either requires a governed token edit, not a blueprint decision.
5. **The fixture-score predicate** (§4.3) — rewrite or strike everywhere.
6. **"LOCKED" header policy** (§4.1) — no spec may claim locked status with open taste questions. Mechanical rule, no taste needed.
7. **Accessibility.** Required by the blueprint standard and the room-contract gate, missing on both sides in nearly every room (reports, lists explicitly; B's stubs universally). No room freezes without it.
8. **Mode-selector consistency.** Feed's PERSONAL/COLLECTIVE/ACTIVITY modes and today's T-STREAM modes must follow one mode law (what modes exist, what switching one proves about data scope).

## 7. THE 11-VS-10 FLAG — RESOLVED, NO MISMATCH

Verified read-only via GitHub API:
- **PR #1278** (`naya2/hub-app-foundation`): `HUB/app/js/rooms/` contains **13 files — all 11 room modules present** (feed, today, reports, library, connect, ledger, connections, lists, mail, spaces, settings) plus shared `canonical.js` and `standard.js`. **Zero rooms lack a module.**
- **PR #1306** ("Hub complete-app build: 11 rooms + false-completion gate," `naya/hub-complete-app-v1 @ 44b97535`, open, 41 files): touches **all 11 room code paths**. "11 rooms" confirmed.
- **PR #1290** confirmed at the cited commit `5837f01f` (`naya/hub-room-functional-spec-v1`, open).

The count is 11 on both sides. There is no 10-vs-11 discrepancy in the code; the earlier flag is closed with evidence.

## 8. MERGED RECOMMENDATION — WHAT BECOMES THE FROZEN ROOM PACKAGE

**Base document: Side A's SPEC.md, repaired — not Side B's blueprints, and not a 50/50 merge.**

Reasons, in order of strength:
1. **Buildability is the freeze criterion**, and only A is buildable. B's stubs cannot be frozen; freezing a 48-line fragment would authorize builders to invent the missing 80%.
2. **B's review function is preserved, not discarded.** Every substantive B delta (§2) folds into A's spec as a named amendment with its grounding citation. B's role converts from "parallel spec" to "amendment source" — which is also the honest description of what it already is.
3. **The 15-section standard becomes the conformance gate it was meant to be.** Each repaired spec must demonstrate all 15 sections or mark a section N/A *with a reason a reviewer can check*. A's specs already carry most of the substance; the gate forces the missing pieces (accessibility, first-3-seconds, anti-patterns, acceptance journey) to be written rather than assumed.
4. **Wireframes are demoted to derived artifacts.** Regenerated from the repaired spec; any future wireframe edit requires a spec edit first. The 7-of-11 SPEC↔wireframe drift finding makes independent wireframe editing a proven defect source.
5. **The ~70 taste questions are the actual critical path.** They batch into themes, not rooms: layout forks (feed F-DETAIL mobile, library takeover-vs-pane, mail 3-col vs 2-col, spaces nav pattern), naming (signal console, highlight reel, context environment), scope (report-type dimension, domain rooms, T-ARC/T-STREAM), authority (settings taxonomy, mail send granularity, connect revoke gating), and visual identity (accent collisions, evidence label). **Recommend Shawn tastes them in theme batches** — one layout session answers four rooms' questions at once. Room-by-room tasting would take eleven sessions and re-split the cross-room decisions in §6.

**Concrete repair order per room** (mechanical, before any taste session):
1. Downgrade LOCKED → DRAFT on all 9 specs.
2. Fix SPEC↔wireframe drift (the named instances in each room file §2/§4).
3. Rewrite or strike untestable predicates (fixture-score slogan, phantom-control predicates, vague predicates).
4. Fold B's deltas in with citations.
5. Fill the 15-section gate (accessibility everywhere; first-3-seconds; anti-patterns; acceptance journeys).
6. Resolve the §6 cross-room governance items once.
7. Then the theme-batched taste session. Then — and only then — freeze, sequentially, room by room.

**What "frozen" will mean:** the repaired spec passes the 15-section gate, zero open taste questions, wireframe regenerated from spec, acceptance predicates all instrumented (named control, named state, named assertion). Anything less is DRAFT, and DRAFT does not authorize building.

---

*Per-room detail: [feed](sandbox://workspace/room-specs-v1/reconciliation/feed.md) · [today](sandbox://workspace/room-specs-v1/reconciliation/today.md) · [reports](sandbox://workspace/room-specs-v1/reconciliation/reports.md) · [library](sandbox://workspace/room-specs-v1/reconciliation/library.md) · [connect](sandbox://workspace/room-specs-v1/reconciliation/connect.md) · [ledger](sandbox://workspace/room-specs-v1/reconciliation/ledger.md) · [connections](sandbox://workspace/room-specs-v1/reconciliation/connections.md) · [lists](sandbox://workspace/room-specs-v1/reconciliation/lists.md) · [mail](sandbox://workspace/room-specs-v1/reconciliation/mail.md) · [spaces](sandbox://workspace/room-specs-v1/reconciliation/spaces.md) · [settings](sandbox://workspace/room-specs-v1/reconciliation/settings.md)*

---

## AMENDMENT A1 — Naya 2's five breaks accepted (2026-10-01 ~20:15 PDT, #554 5944798197 / 5944924131)

The base-side choice survived; the freeze recommendation is amended:

1. **Visuals are first-class lock artifacts, not derived.** Base = spec + visual locked
   together, two-way edits. A visual change updates the spec; a spec change re-renders
   the visual. Neither derives the other — the director reviews the image.
2. **Taste session FIRST.** New repair order: taste session → mechanical repair →
   delta fold → 15-section gate → independent freeze.
3. **Testability clause (adopted verbatim):** a predicate that cannot be instrumented
   is not a predicate. In the freeze gate definition.
4. **Independent eye as final freeze step.** Builder-repaired ≠ frozen. Freeze requires
   independent verification (Naya 2 or Naya 3 seat).
5. **Accent collisions decided now** as part of the 8 cross-room decide-once items.

Plus: checkable amendment ledger carried in the freeze package (each delta cited to its
reconciliation C-item). Producer-judges-own-work concern accepted — Naya 3's independent
read on the base-side choice still needed; her verdict defers where lanes differ.

Amended net: base = her-spec-structure + visual-first-class (two-way) + taste-first
ordering + testable-predicates + independent-freeze + 8 cross-room decisions taken once.
