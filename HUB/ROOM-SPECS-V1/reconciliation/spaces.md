# SPACES — Reconciliation: `spaces/SPEC.md` + `wireframe.html` (lane A) vs `grounding/blueprints/10-smart-spaces.md` (lane B, Naya 3)

**Reviewer:** independent pass, 2026-10-01. Read all three target files plus grounding: `INTELLIGENCE-PROJECTION-CONTRACT-V1.md`/.json (No-Hub-Capture law), `ROOM-FUNCTIONAL-CONTRACT-V1.md`, `ROOM-BLUEPRINT-STANDARD-V1` (`_STANDARD.md`), `1278-tokens.css`, canonical room package `grounding/rooms/10-smart-spaces/{FUNCTIONAL-SPEC,SPEC.AI}.md`, and `room-specs-v1/MANIFEST.md`.

**Calibration note on B:** B does not in fact follow `ROOM-BLUEPRINT-STANDARD-V1` (15 sections). It has ~7 of 15 sections — but so do all 11 sibling blueprints in `grounding/blueprints/` (46–92 lines each). B is a stub-format blueprint like its siblings, not a deficient outlier. Reconciliation below compares it as-written against A's full SPEC-FIRST spec, citing grounding as the arbiter.

---

## 1. AGREEMENTS

What both sides lock identically, verified against grounding:

1. **Room identity.** Route `/spaces`, title "Smart Spaces", metaphor THE WORLDS, accent lime (`--accent-spaces: var(--lime)` — tokens are visual law, both sides match it; FUNCTIONAL-SPEC: "Theme: lime").
2. **Human job.** A contract field 1 / header promise: "What context am I in, and what belongs together here?" — identical wording in FUNCTIONAL-SPEC ("Human question"). B's Purpose ("enter a meaningful context that changes retrieval, people, projects and intelligence") is the same job in paraphrase.
3. **Context lens, not container.** A §1 field 8: "Space is a *context lens*, not a room container... deep links with `?space=<id>`, not duplicate rooms." B Do-not: "do not create duplicate intelligence inside Space." FUNCTIONAL-SPEC: "This is a context projection of existing rooms, not a second set of databases." All three agree; this is the room's load-bearing law.
4. **No folder metaphor.** A §1 field 9 forbids the folder-only metaphor; B Do-not: "do not make Space merely a colored folder." Locked on both.
5. **Privacy levels.** A field 6: Private / Shared by choice / Collective by consent / Public by decision — identical four labels in FUNCTIONAL-SPEC ("Human language can include concepts such as..."). B does not enumerate them but does not contradict.
6. **Label ≠ enforcement.** A: "a label without enforcement is forbidden. The Hub never invents privacy guarantees." FUNCTIONAL-SPEC: "Do not turn labels into security guarantees without runtime enforcement." Identical constraint; B silent but non-contradictory.
7. **Switch changes real retrieval, one canonical ID.** A predicates 1–2 (same canonical IDs everywhere, ENTER_SPACE changes real retrieval scope via the runtime adapter, not a client filter). B Proof: "Switching Space materially changes applicable retrieval/context without changing canonical object identity." Locked identically.
8. **Persistent context + switcher; mobile compact switcher.** A: Active Space Indicator in shell on every room + Space Switcher drawer + mobile compact switcher. B controls: "switch Space." FUNCTIONAL-SPEC Mobile: "Persistent compact Space switcher." Locked.
9. **Governed actions.** A: CREATE_SPACE / INVITE_CONNECT / SET_PRIVACY_SHARING / ARCHIVE/LEAVE require governed confirmation + receipts (predicates 6, field 6). B: "invite/connect where governed", "manage Space privacy". FUNCTIONAL-SPEC: "Archive/leave with governed safeguards." Locked.
10. **No Hub-side capture.** Neither side exposes Smart Note / report / Activity capture controls. A's field 9 explicitly forbids them; B's controls contain none. Consistent with the No-Hub-Capture law (projection contract §3 and §10: forbidden producer list covers Smart Notes/reports/activity — Space creation itself is NOT in the forbidden list, and both FUNCTIONAL-SPEC and the projection contract's "choose Space/context" allowed action cover Space governance via runtime). No silent violation by either side.
11. **No fake liveness.** A forbids it and predicate 9 states "no activity is inferred from screen opens"; projection contract: "Do not infer or fabricate activity merely from the user opening a screen." B silent. Locked between A and grounding.
12. **Naya as interpretation, marked as such.** A: "Naya's read" block labeled "Naya's interpretation — not source truth" (predicate 4); matches MANIFEST locked rule #4 and FUNCTIONAL-SPEC's INTELLIGENCE layer ("Naya summarizes what matters in this Space"). B's "Ask Naya about Space" implies the same presence without the marker — no contradiction.

---

## 2. CONTRADICTIONS

**C1 — View model: two views vs one.**
- A says: two locked views — View A Space Gallery (`/spaces`) + View B Space Home (`/spaces/<space-id>`).
- B says: one view only — Space home (identity/purpose/privacy → module grid → selected module detail). No all-Spaces gallery, no Enter-from-gallery, no EMPTY-state treatment.
- **Resolution:** A's two-view model wins. FUNCTIONAL-SPEC explicitly defines both: "Signature visual: A gallery of context worlds / portals" AND a separate "Space home". B's single view drops the signature visual entirely. B must be rewritten to add the gallery view (including the EMPTY state, per FUNCTIONAL-SPEC: "Create a Space when intelligence, people and activity need a shared context.").

**C2 — Control inventory: B omits the primary actions.**
- A says: primary "＋ New Space" in the gallery header (one primary per context, per ROOM-FUNCTIONAL-CONTRACT §3); per-card Enter + overflow (Open Feed, Open Report, Members, Archive/Leave); Space-home Ask Naya (primary), Invite/Connect (secondary), overflow (Set privacy/sharing, Archive/Leave).
- B says: switch Space, open module, invite/connect where governed, manage Space privacy, Ask Naya about Space, open related intelligence. CREATE_SPACE, ENTER_SPACE, and ARCHIVE/LEAVE are entirely absent.
- **Resolution:** A's inventory wins. FUNCTIONAL-SPEC's Primary actions list opens with "Enter Space, Create Space" and includes "Archive/leave with governed safeguards"; SPEC.AI.md lists ENTER_SPACE, CREATE_SPACE, ARCHIVE_LEAVE_IF_GOVERNED. B's missing controls must be added. B also names no primary action at all, violating ROOM-FUNCTIONAL-CONTRACT §3 (primary action visually dominant, normally 1 per context).

**C3 — Space-home composition: module grid + detail drilldown vs anchored sections.**
- A says: anchored sections — Key Intelligence, Feed slice, Projects/Goals/Rules, People, Activity/Proof, Connected doors/apps. "Space Home uses anchored sections, not tabs (Space is a projection, not a sub-app with its own nav)."
- B says: module grid [ Intelligence ] [ People ] [ Projects ] [ Lists ] [ Activity ] [ Goals ] [ Rules ] [ Connections ] + "[ selected module detail ]" drilldown panel.
- **Resolution:** split. B's module coverage (Lists, Goals, Rules, Connections as named modules) is closer to FUNCTIONAL-SPEC's Drive-notes list ("Intelligence / People / Projects / Notes / Lists / Activity / Goals / Rules / Connections") than A's, which relegates Lists to an "Open in Lists" link inside the Projects/Goals/Rules table. Adopt B's module list. But B's "selected module detail" panel conflicts with A's anchored-sections law — and A's "not tabs" rule is itself ungrounded (no grounding file decides the nav pattern). **→ [NEEDS DIRECTOR TASTE]: anchored sections (A) vs module-detail drilldown (B).** Recommended default until decided: A's anchored sections, since it matches the "projection, not a sub-app" reasoning and A's handoffs already define where each module deep-links.

**C4 — Desktop composition header.**
- A says: room header (jewel + "Smart Spaces" + promise) with "＋ New Space" top-right; Active Space Indicator lives in the shell under the room header.
- B says: `[GLOBAL SEARCH]` as the first composition element, then `[Smart Spaces] [Space selector]` beside the title.
- **Resolution:** A's wins on both points. Global search is a shell element, not a Spaces-room composition decision. A's indicator placement ("belongs to the shell; the room supplies their content") is the correct shell/room boundary; B's title-adjacent selector conflates shell and room.

**C5 — State model: defined vs absent.**
- A says: Space states ACTIVE / AVAILABLE / ARCHIVED / LEAVE-PENDING + shared-model room states (LOADING · EMPTY · READY · BLOCKED · UNAUTHORIZED · NOT_VERIFIED · ERROR · OFFLINE).
- B says: nothing — no states section (also missing from all sibling stub blueprints; _STANDARD §7 requires it).
- **Resolution:** A's state model stands; B must adopt it. Caveat: LEAVE-PENDING is A's ungrounded invention (no grounding file defines it). Plausible given "governed safeguards" on leave, but flagged — see GAPS.

**C6 — Data contract precision.**
- A says: owner = NayaNET intelligence runtime (Space membership + consent law); runtime adapter seam `ENTER_SPACE / CREATE_SPACE / SET_PRIVACY_SHARING / INVITE_CONNECT / LINK_INTELLIGENCE / ARCHIVE_LEAVE`; "the Hub holds no Space store."
- B says: "Canonical Space/context relationships and scoped projections" — no owner, no seam, no store statement.
- **Resolution:** A's wins outright; _STANDARD §6 requires "what canonical data the room consumes and from whom." B must adopt A's data contract verbatim.

**C7 — Naya behavior detail.**
- A says: "Ask Naya in this Space" passes Space scope upstream, creates no local object (predicate 8); "Naya's read" interpretation block with the not-source-truth marker.
- B says: "Ask Naya about Space" as a bare control, no behavior specified.
- **Resolution:** A's wins (matches MANIFEST locked rule #4 on the interpretation marker and the projection contract's "ask Naya to explain/compare/summarize the projected intelligence" allowed action). B must adopt.

**C8 — Signature instrument naming.**
- A says: Space Gallery (portal bay of context worlds) + Space Home; FUNCTIONAL-SPEC: "A gallery of context worlds / portals."
- B says: primary instrument "Context Environment."
- **Resolution:** A's / grounding's naming wins. ROOM-FUNCTIONAL-CONTRACT §2's signature-instrument list contains "context world" and "portal bay" — B's "Context Environment" is an ungrounded synonym and should be replaced.

---

## 3. GAPS

### B has, A lacks
- **Explicit first-3-seconds entry statement.** B has it (current Space identity; purpose; key intelligence; people/projects; activity). A's journey covers gallery→home implicitly (step 1) but has no explicit entry-state section. Note B's entry state only describes Space home, not the gallery or the no-active-Space case.
- **Lists / Goals / Rules / Connections as first-class Space-home modules.** B names them; A gives Lists only an "Open in Lists" handoff inside the Projects/Goals/Rules table.

### A has, B lacks (B's stub deficit — 9 of 15 _STANDARD sections missing)
- States (see C5). Cross-room handoffs (A's `?space=<id>` deep links; B has none). Naya behavior (C7). Mobile transformation (A: gallery→home, persistent compact switcher; B: nothing). Visual law/tokens (A: lime accent, token inventory; B: nothing). Acceptance journey + mechanical predicates (A: 5-layer journey + 10 predicates; B: nothing). Data-contract precision (C6). Privacy-level enumeration (A: four levels; B: silent). Forbidden-substitutes list (A: 9 items; B: 2).

### Both lack vs grounding
- **Messages surface on Space home.** FUNCTIONAL-SPEC's Space home lists "messages"; neither A nor B includes one (A has OPEN_SPACE_MAIL among allowed actions but no region).
- **Reports surface on Space home.** FUNCTIONAL-SPEC's Space home lists "reports"; A only wires OPEN_SPACE_REPORT into the gallery card overflow; B only has "open related intelligence."
- **Important Lists as a surface.** FUNCTIONAL-SPEC lists "important Lists" in Space home; A only links out ("Open in Lists"); B names Lists as a module but specifies nothing inside it.
- **Accessibility.** _STANDARD §11 (keyboard/focus/labels/zoom) — absent from both. A's component inventory is the right home for it.
- **Canonical Space object schema.** A's taste Q6 flags it; MANIFEST lists it as grounding debt ("No canonical Space object schema — builder needs the registry field contract"). FUNCTIONAL-SPEC enumerates display fields (jewel, name/purpose, privacy, people, objectives, recent intelligence, activity, doors, health/open loops) but no registry field contract. Both sides specify against a schema that does not exist.
- **Canonical consent/privacy state schema.** A's field 3/6 and predicate 5 lean on "canonical consent law" and runtime enforcement; no such schema exists in grounding (MANIFEST gap #3). Both sides assert labels match enforcement without a checkable enforcement contract.

### A's internal inconsistencies (found adversarially)
- **Wireframe invents a per-portal-card truth badge** ("FIXTURE truth" on Space cards). SPEC §2's card fields don't list it, and per §1 field 7 truth states (CANDIDATE/VERIFIED…) belong to intelligence *inside* a Space — Spaces themselves carry ACTIVE/AVAILABLE/ARCHIVED/LEAVE-PENDING. The badge contradicts the spec's own truth-state model. Remove or replace with a Space-state indicator.
- **Wireframe omits the "Find a Space" search/filter input** required by SPEC §3 Inputs. Add it.
- **Wireframe Region 3 placement:** SPEC says the "Why spaces" strip goes "right side / below on mobile"; the wireframe stacks it full-width below the portal bay at all breakpoints. Fix desktop placement.
- **Shell boundary:** SPEC §2 says the Active Space Indicator "belongs to the shell; the room supplies their content"; the wireframe draws it inside the room content area. Either redraw it as a shell element or relax the spec.
- **CREATE_SPACE governed flow is specified (SPEC §3: name, purpose, 4-level privacy radio + enforcement note, initial members) but not wireframed** — only the triggering button is drawn. The governed confirmation flow is acceptance-relevant (predicate 6); it needs a wireframe panel.
- **Naming drift:** §1 field 2 says kernel "Register/enter/leave/archive" but field 4's seam is CREATE_SPACE; field 4 seam says `ARCHIVE_LEAVE` while fields 5/8 and predicates say `ARCHIVE/LEAVE`. One naming convention must win (recommend CREATE_SPACE / ARCHIVE_LEAVE everywhere).
- **Wireframe View B ordering:** Region 6 (Activity/Proof) sits beside Region 3 (Feed slice) in a 2-col row, above Regions 4/5/7 — different from SPEC's 2→7 sequence. SPEC's order is itself taste Q3, so this is a data point for that decision, not a violation; the wireframe's choice effectively pre-decides Q3's priority question and should be labeled as such.
- **LEAVE-PENDING** (Space truth state) is A's invention with no grounding. Keep or drop — recommend keeping only if the governed leave flow is genuinely async; otherwise drop to avoid inventing state machinery.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides' flagged items, deduplicated. (B flags none explicitly; all six below are A's, plus two reconciler additions.)

1. [NEEDS DIRECTOR TASTE] Per-Space identity jewel colors: assignable color per Space (variant/token beyond `--accent-spaces`) vs one lime identity for all Spaces with icon-only differentiation? Tokens provide a 12-color spectrum, but several spectrum colors are already room accents (green=feed/connect, blue=library/mail, purple=lists, indigo=reports, magenta=today, orange=connections, yellow=ledger) — per-Space colors risk room-identity collisions.
2. [NEEDS DIRECTOR TASTE] CREATE_SPACE authority: owner only, or any member of an existing Space? Default member roles on invite (viewer/contributor/admin)?
3. [NEEDS DIRECTOR TASTE] Space Home section order (Key Intelligence → Feed slice → Projects/Goals/Rules → People → Activity, or People first?). Note the wireframe's R3/R6 side-by-side placement already pre-decides part of this.
4. [NEEDS DIRECTOR TASTE] ARCHIVE vs LEAVE vs DELETE semantics for a Space with shared intelligence: member access + collective projections on archive; governed retention rule needed.
5. [NEEDS DIRECTOR TASTE] Per-Space notification preferences (FUNCTIONAL-SPEC mentions "Space-specific preferences" under Settings→Notifications): if yes, surface lives in Settings, this room only links.
6. [NEEDS DIRECTOR TASTE] Canonical Space object schema: grounding debt (MANIFEST gap #2). Builder-blocking later; the registry field contract must be written before any build.
7. [NEEDS DIRECTOR TASTE — added by reconciler] Space-home nav pattern: A's anchored sections vs B's module-grid + selected-module detail (C3). Grounding does not decide.
8. [NEEDS DIRECTOR TASTE — added by reconciler] Space-home scope: should important Lists / reports / messages be real regions (per FUNCTIONAL-SPEC's Space-home list) or remain deep-link handoffs (A's current choice)?

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION.** Blocking items, by name:

1. **View-model conflict (C1)** — B must adopt A's two-view model (gallery + home), or Shawn must rule otherwise. Cannot freeze two specs describing different rooms.
2. **Control inventory (C2)** — B must add ENTER_SPACE / CREATE_SPACE / ARCHIVE-LEAVE and name the primary action ("＋ New Space").
3. **Space-home nav pattern (C3 / taste Q7)** — anchored sections vs module-detail drilldown must be decided before either wireframe is final.
4. **Wireframe↔SPEC alignment (A internal)** — fix the six items in §3: remove/replace the invented portal-card truth badge, add the "Find a Space" search input, fix Region 3 desktop placement, resolve the Active Space Indicator shell-boundary mismatch, wireframe the CREATE_SPACE governed flow, unify CREATE/ARCHIVE naming. A's header claims "locked" — it isn't, until these close.
5. **Taste Q2 (CREATE authority) + Q4 (archive/leave/delete semantics)** — governed-action semantics; acceptance predicate 6 (governed confirmation + receipts) is not buildable without them.
6. **Taste Q8 (lists/reports/messages scope)** — decides Space-home region count; affects both A and B.

**Not blocking the blueprint freeze, but recorded as builder-blockers:** canonical Space object schema (Q6) and canonical consent/privacy state schema — MANIFEST already carries these as known grounding debt ("block builders later, not specs now").

**Would-be READY TO FREEZE when:** items 1–6 closed, §3's wireframe fixes landed, and the eight taste questions answered — at which point A's SPEC.md + wireframe (with B's module-coverage folded in) is the single frozen room spec, and B's stub is rewritten to match it verbatim.
