# LEDGER Reconciliation — A (SPEC.md + wireframe.html, my lane) vs B (06-smart-ledger.md, Naya 3's lane)

**Date:** 2026-10-01 · **Reviewer:** Naya 4 (independent reviewer seat)
**Inputs read:** `ledger/SPEC.md`, `ledger/wireframe.html`, `grounding/blueprints/06-smart-ledger.md`,
plus grounding citations `grounding/INTELLIGENCE-PROJECTION-CONTRACT-V1.md`,
`grounding/ROOM-FUNCTIONAL-CONTRACT-V1.md`, `grounding/1278-tokens.css`.
**Convention:** "A says" = my lane's SPEC.md / wireframe.html; "B says" = Naya 3's blueprint.

---

## 1. AGREEMENTS

Both specs lock these identically; no reconciliation needed:

1. **Room purpose.** A: "What happened, under whose authority, and what proves it?" — inspect consequential activity "without reading logs." B: "Explain what actually happened and what proves it." Same job, same "not accounting, not logs" disambiguation (A says it in the R1 tagline; B's "Do not become financial dashboard" says the same).
2. **Signature instrument.** A R3 "CAUSAL TIMELINE" = B "Primary instrument: Causal Receipt Timeline." Confirmed by both.
3. **Filter vocabulary.** Both specify the exact six tabs `All | Actions | Decisions | Shares | Connections | System` in the same order (A R2; B desktop composition). Locked.
4. **Control set.** B's controls (filters, Inspect Receipt, Evidence, Open Related Intelligence, Open Actor/Connection, Ask Naya, Export proof where supported, governed recovery only when explicitly available) map 1:1 onto A's R4 action row. Naming delta only: B "Evidence" vs A "View evidence" — see §2 item 7.
5. **Header composition.** B: `[Smart Ledger] [Space] [Time] [Verification Health]` = A's R1 TrustHealthHeader + scope chips (A adds an Identity chip — see §2 item 2).
6. **Data contract.** B: "Canonical receipts/evidence/authority/outcome records." A (a-3): canonical decision/action/observation/outcome/verification receipts + persistence evidence. Same canonical-object set; both prohibit synthesized proof.
7. **Executor success ≠ verification.** B: "do not call executor success VERIFIED." A: forbidden substitute "green executor output treated as verified proof"; pred 3 "an event with no independent verification shows 'Not verified — [why]'"; wireframe shows `Executed OK (≠ verified)`. Locked, in three separate places in A.
8. **Refused/failed events are never hidden.** B: "do not hide refused/failed states." A: forbidden substitute "hidden failed/unverified events"; pred 4; wireframe keeps REFUSED/FAILED events visible with a "never hidden" note. Locked.
9. **Proof-shaped acceptance.** B's one-line proof ("Known action can be traced from request through verification") is substantively A's pred 1 ("A human can locate a known action, see who initiated it, see authority, outcome, and independent verification"). Same test in different clothes.
10. **No Hub-side canonical creation.** Neither spec implies the Hub creates canonical objects. A allows only FILTER/INSPECT/VIEW/OPEN/ASK (projection contract §10-allowed) plus EXPORT and RECOVER gated on runtime support (projection contract §10: upstream actions belong to Naya/governed runtime; the Hub may request). B has no capture control at all. **Both are clean against the No-Hub-Capture law.** (Adversarial check: A's "verb phrase" card labels are projection labeling from canonical receipts, not canonical-object minting; the source of the verb phrase is unspecified — see §3 gap 10.)
11. **Anti-patterns.** B's three "Do not" items are all covered inside A's six forbidden local substitutes. Same doctrine, A is stricter (adds proof-by-animation, synthesizing missing receipts, raw-log-dump).
12. **Tokens as visual law.** A's component inventory claims "All components reuse the locked token set (1278-tokens.css)" and "No new tokens." Adversarially verified: every token referenced (`--accent-ledger`, `--yellow`, `--rich-orange`, `--bg-raise`, `--radius-pill`, `--radius-xl`, `--fs-small`, `--fs-micro`, `--depth-deep`, `--dur-*`) exists in `1278-tokens.css`. Claim holds.

---

## 2. CONTRADICTIONS

### C1. Stage chain: 4 stages (A) vs 5 stages (B)
- **A says:** `RECEIVED → AUTHORIZED → EXECUTED → VERIFIED`, "four distinct rendered stages" (R3, pred 2); wireframe draws four nodes.
- **B says:** `RECEIVED ─ AUTHORIZED ─ EXECUTED ─ OBSERVED ─ VERIFIED`, five nodes.
- **Recommended resolution: adopt B's OBSERVED stage.** Why the stronger grounding is on B's side: (a) A's own kernel responsibilities (a-2, PROOF) list the room's proof surface as "authority, receipts, **observation**, outcome, verification" — yet A's StageChain has no place for observation to render; the spec demands observation be shown and then gives it no stage. Internal inconsistency in A. (b) Shawn's Demo-1 master directive (director statement) makes post-action observation a first-class proof component (observation + outcome + acceptance + causal limits + learning eligibility), and the nine-node runtime chain has OBSERVATION as its own node between ACT and KNOW. A 4-stage chain collapses observation into EXECUTED, which is exactly the kind of stage-collapse A itself forbids (a-7: "never collapsed"). This is not taste — it is B being consistent with both A(a-2) and director-stated doctrine.

### C2. Identity scope chip: present in A, absent in B
- **A says:** R1 scope chips `Space: [All ▾] · Identity: [Me ▾] · Time: [Last 7 days ▾]`.
- **B says:** desktop composition header `[Smart Ledger] [Space] [Time] [Verification Health]` — no Identity chip.
- **Recommended resolution: keep A's Identity chip.** Grounding wins for A: projection contract §7 makes owner-vs-collective identity scope a projection policy that the human must be able to see and control; functional contract §7 (spatial/context law) requires identity/privacy scope to be visible where it materially affects results. Identity scope materially affects receipt visibility (A a-6: receipts may reference private actors; Ledger must respect source-room privacy rules). Not a product-taste call — A is required by the privacy groundings B omits.

### C3. Search control: presupposed by both, present in neither inventory
- **A says:** pred 1 requires "A known action is findable via search/filter/scope" — but A's contract header allowed actions, component inventory, and wireframe contain **no search control**. Filter tabs + scope chips are the only findability instruments.
- **B says:** desktop composition shows `[GLOBAL SEARCH]` at the top, but B's Controls list does not include search.
- **Recommended resolution: add a search control to A (wireframe + inventory), placed in R2 next to the filter tabs, not above the room.** Why: pred 1 is untestable without a search instrument — this is an internal defect in A (a predicate that tests a control that doesn't exist). B confirms search is expected. Placement in R2: B's `[GLOBAL SEARCH]` reads as the Hub shell's global search, not a room control; A's findability controls live in R2. Adding it is a spec fix, not a product decision.

### C4. "Connect door 'Receipts'" (A pred 9) vs A's own action inventory
- **A says (pred 9):** outbound links `("Open related intelligence", "Open actor", Connect door "Receipts")` must resolve. **A says (R4 + component inventory):** the action row has `"Open actor" / "Open connection"` — there is no "Receipts" door or control defined anywhere in the spec, the wireframe, or the handoffs (a-8 says events link to "door (Connect)" — singular door, not a "Receipts" door).
- **Recommended resolution: fix pred 9 before freeze** — either rename to the defined `"Open connection"` action (which is the door link A actually specifies) or define a "Receipts" surface in R4/inventory. As written the predicate references a phantom control and is untestable. Neither side's grounding picks the rename; the fix direction (match the predicate to the inventory) is mechanical, not taste.

### C5. Room name vs forbidden metaphor (internal to A)
- **A says:** the room is literally named LEDGER (route `/ledger`, mark "Smart Ledger"), and simultaneously lists "financial-ledger metaphor" as a forbidden local substitute.
- **Not a real contradiction — but flag it:** A disambiguates in three places ("not a financial ledger" in a-1, "The truth room — not accounting, not logs" tagline, forbidden substitute). The name/metric tension is handled. Recommendation: keep the explicit disambiguation line in the build; do not drop the tagline.

### C6. "LOCKED FOR FIDELITY BUILD" (A) vs six open taste questions (A)
- **A says:** Status: LOCKED FOR FIDELITY BUILD — while carrying six [NEEDS DIRECTOR TASTE] items (actor display, health denominator, export format, timeline density, retention visibility, cross-room deep-link).
- **Resolution:** the lock claim is premature. Shawn's law: "taste belongs at blueprint stage" — these are blueprint-stage questions and a fidelity build cannot be locked against them. See §5: the header must drop to CANDIDATE/DRAFT until §4 is cleared.

### C7. B's conformance claim vs B's actual content (internal to B)
- **Claimed:** B "follows ROOM-BLUEPRINT-STANDARD-V1." **Actual file:** 8 short sections (purpose, first-3-seconds, desktop composition, primary instrument, controls, data, do-not, one-line proof). It is missing the standard's truthful-states, handoffs, Naya behavior, mobile, accessibility, visual law, and acceptance-journey sections.
- **Resolution:** treat B as a partial blueprint, not a standard-conformant one. Nothing in B contradicts A's fuller sections; B's gaps are filled by A (§3). The reconciliation direction is therefore: **A is the canonical freeze candidate; B contributes corrections (OBSERVED stage, search confirmation) — not the reverse.**

### C8. Naming micro-deltas (non-blocking, resolve mechanically)
- B "Evidence" → adopt A's "View evidence" (A is the detailed inventory; both mean the same control).
- B's proof says "traced from **request** through verification"; A's stage is **RECEIVED**. Resolve: treat "request" as the RECEIVED stage's content; no product change needed.

---

## 3. GAPS

### Present in A, missing in B
1. **Truth states.** A defines 11 room states (LOADING…DISABLED) plus the per-event stage vocabulary with refused/failed/recovered variants (a-7). B has no truth-state section at all.
2. **Cross-room handoffs.** A (a-8) defines bidirectional handoffs (Feed/Mail/Connect/Spaces → Ledger proof; Ledger → Library intelligence, Connections actor, Connect door). B is silent.
3. **Naya behavior.** A R6 specifies the inline "interpretation, not evidence" panel, explanation-only, underlying data untouched. B has the "Ask Naya" control with no behavior contract — under the projection contract §10 this label discipline is what keeps Ask Naya from becoming Hub-side capture, so its absence in B is load-bearing.
4. **Mobile law.** A: chain first, full-screen receipt detail, 4-dot StageChain with labels on tap, filters in sheet. B: no mobile section.
5. **Accessibility.** A pred 11 (tab order, Enter/Esc, screen-reader text equivalents for stage states). B: none.
6. **Visual law / component inventory.** A's full token table + "no new tokens" claim (adversarially verified, §1 item 12). B: no visual law.
7. **Acceptance journey.** A's 10 mechanical predicates. B's "Proof" is one untestable sentence. (B cannot be built/tested against as written.)
8. **Scope-requery semantics.** A: "Changing any scope changes the real retrieval scope"; "FILTER is instant and re-queries canonical receipts — no client-side filtering of a stale cache." B: silent. This is a load-bearing anti-fake-live-state rule.
9. **Privacy boundary.** A a-6 (private actors, anonymous where consent requires, never export sealed/private material). B: silent — B's controls could leak under projection-contract §6/§7 without it.
10. **Runtime owner + recovery gating.** A a-4: "Recovery actions execute only through explicitly exposed governed runtime operations"; retry/recover needs confirmation. B says "governed recovery only when explicitly available" but names no owner.

### Present in B, missing in A
1. **OBSERVED stage** (→ adopted per §2 C1; this is B's single substantive contribution).
2. **First-3-seconds entry** as a named discipline (A's R1–R3 composition implies it — scope/time, verification health, causal timeline — but never states the 3-second rule. Recommend A add the one-line entry rule for reviewer testability.)
3. **[GLOBAL SEARCH]** (→ §2 C3; belongs to the shell, but B is the only place that names search at all).

### Internal-to-A gaps found adversarially
- **Wireframe vs pred 6:** "Export proof" must be "absent with reason" where unsupported. The wireframe demonstrates presence (event 1), full absence (event 2, refused) — but never the *absent-with-reason* state. Wireframe needs one annotation showing the reason state.
- **Verb-phrase provenance:** cards show human-readable "action verb phrase" (R3 item 2) and R5 forbids "prettified into fake narrative" — but no line says where the verb phrase comes from (canonical receipt field vs runtime adapter mapping). Needs one sentence binding it to the receipt (not Hub-invented) or it risks the No-Hub-Capture law at build time.
- **Wireframe R1/R2 duplication:** both R1 ("Needs attention (3)" chip) and R2 ("Needs attention / failed verification" toggle) show the attention control. SPEC R1 says the chip "jumps to the filtered view" — coherent as shortcut, but the wireframe doesn't label which is the shortcut. Minor; annotate.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides' flagged items, deduplicated. (B flags none in the file as read; the six below are A's, all tagged [NEEDS DIRECTOR TASTE] in SPEC.md.)

1. **[NEEDS DIRECTOR TASTE] Actor identity display.** Receipts reference private actors. Should the Ledger show the real name to the owner, an opaque id, or a per-actor choice? (A's default assumption: real-name-for-owner / opaque-in-collective — confirm.)
2. **[NEEDS DIRECTOR TASTE] Verification health denominator.** "98% verified" is computed, but which events count — all, only consequential ones, a governed subset? Who defines "consequential"?
3. **[NEEDS DIRECTOR TASTE] "Export proof" format.** Receipt JSON download? Signed PDF? Expiring shareable link? Different privacy/authority implications per format.
4. **[NEEDS DIRECTOR TASTE] Timeline density.** Newest-first infinite scroll specified; should high-volume system events be collapsed/aggregated by default (e.g. "12 heartbeats")? A's conservative default: never aggregate failed/unverified — confirm the rest.
5. **[NEEDS DIRECTOR TASTE] Retention visibility.** Should the Ledger show receipt retention policy, or is that Settings-room only?
6. **[NEEDS DIRECTOR TASTE] Cross-room proof deep-link.** When Feed/Mail/Spaces link to "Ledger proof," deep-link to the single event or to the thread context? (A's default: deep-link to event, thread expandable.)

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION.** A is the canonical freeze candidate (B is a partial blueprint and its only substantive contribution is the OBSERVED stage), and A's adversarial token/visual claims verify clean. But the spec is not freeze-ready. Blocking items, by name:

1. **OBSERVED stage adoption** — fold B's 5th stage into A's StageChain (§2 C1). Recommended resolution is grounded (A's own a-2 + director-stated Demo-1 doctrine); needs the lane to accept and update R3, pred 2, the wireframe strip, and the component inventory.
2. **Search control** — pred 1 tests a control that doesn't exist (§2 C3). Add room-level search to R2 + inventory + wireframe before freeze.
3. **Pred 9 phantom "Receipts" door** — rewrite to the defined "Open connection" action or define the control (§2 C4). An untestable predicate blocks freeze.
4. **Premature lock header** — drop "LOCKED FOR FIDELITY BUILD" until §4's six taste questions are decided (§2 C6). Shawn's law: taste belongs at blueprint stage; a fidelity build cannot be locked against undecided taste.
5. **Verb-phrase provenance sentence** — bind the card's human-readable verb phrase to the canonical receipt (not Hub-invented) in a-3 or R3 (§3 internal gap).
6. **Wireframe: absent-with-reason state** — annotate one event showing "Export proof" absent *with reason* per pred 6 (§3 internal gap).
7. **The six §4 taste questions** — actor identity display, health denominator, export format, timeline density, retention visibility, deep-link behavior. All [NEEDS DIRECTOR TASTE]; items 2–4 directly affect buildable predicates (health computation, export implementation, aggregation rules).

Non-blocking (may ride along with the freeze, no director input needed): Identity chip stays (grounded, §2 C2); "Evidence" → "View evidence" naming (C8); add B's first-3-seconds one-liner to A (§3); annotate R1/R2 attention-chip vs toggle shortcut (§3).
