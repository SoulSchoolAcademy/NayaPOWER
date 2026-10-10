# CONNECT — Room Spec Reconciliation V1

**Scope:** my lane `connect/` (SPEC.md + wireframe.html = "A") vs Naya 3's `grounding/blueprints/05-smart-connect.md` ("B").
**Grounding consulted:** INTELLIGENCE-PROJECTION-CONTRACT-V1.md, ROOM-FUNCTIONAL-CONTRACT-V1.md, `1278-tokens.css` (`--accent-connect: var(--green)`, `--teal`/`--emerald` also defined).
**Reviewer stance:** adversarial to both sides; internal inconsistencies listed in CONTRADICTIONS where they block freeze.

---

## 1. AGREEMENTS

Both sides lock these identically (element named, both sides confirmed):

1. **Room identity + privacy promise.** A (SPEC R1 + wireframe): "Smart Connect — The Portal Bay" with promise line `"Connect your intelligence — your intelligence stays yours. Connect only what you choose."` B (composition): `[ CONNECT YOUR INTELLIGENCE ] Your intelligence stays yours. Connect only what you choose.` — same promise, near-identical wording.
2. **R1 health summary control.** A: `Connection health: [HEALTHY / n degraded / OFFLINE]` as a link button `"View connection health"` → health detail. B: `[Connection Health]` element next to the room mark. Same element, same placement.
3. **Per-door instruments as the room's core set.** B: 2×3 grid of `[ Door instrument ]`. A: portal bay of DoorPortal cards (radial, with explicit grid fallback). Both agree the room is a collection of per-door instruments, not a list of links.
4. **Full per-door control vocabulary.** B lists: Connect/Authenticate · Configure · Test · Capabilities · Required Authority · Revoke/Disconnect · Receipts. A locks exactly the same seven (primary Connect/Authenticate/Configure by state; secondary Capabilities/Authority/Test/Receipts; destructive Disconnect/revoke in authority sheet). (Label exactness differs — see CONTRADICTIONS 4.)
5. **Four-state non-collapse.** B verbatim: `CONNECTED ≠ AUTHENTICATED ≠ AUTHORIZED ≠ HEALTHY`. A: connection, authentication, authorization, health as four separate labeled states ("four separate states, never collapsed"), plus the authority boundary `CONNECTED ≠ AUTHORIZED` in (a)(6).
6. **Data contract: canonical registry + live runtime state.** B: "Canonical Smart Door registry + live auth/health state." A (a)(3)–(4): Smart Door objects from `BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json` + governed runtime health/auth state; "connect/authenticate actions execute through the governed runtime — never mocked in the room."
7. **Roadmap doors never presented as live.** B: "do not present roadmap doors as live." A: R4 Roadmap Horizon band, `ROADMAP` badge, no connect button, plus forbidden substitute "roadmap door presented as live." Rule identical; A adds the visual treatment.
8. **Connection never implies authority.** B: "do not imply connection grants authority." A: (a)(6) `CONNECTED ≠ AUTHORIZED`; authority sheet as the authority surface; advice is never a permission grant.
9. **Proof = runtime-observed result.** B: "Door status matches canonical registry/runtime and a connect operation has an observable result." A: DoorStatusStack "badges update from real runtime state only"; "on success the DoorStatusStack re-reads from runtime"; predicate 4 (no dead buttons), predicate 10.
10. **Test only where supported; otherwise absent.** A: `"Test"` rendered "only if the door supports it; otherwise absent, not dead" (wireframe door 2 omits Test correctly). B lists Test as a control without the qualifier — the qualifier is implied by the functional contract's no-dead-button rule, and nothing in B requires rendering it unconditionally. Agreed in substance.
11. **Mobile: detail becomes a full-screen overlay; doors stack.** B: "detail opens full-screen." A: sheets full-screen on small screens; portal reduces to vertical cards; list view default on small screens. Same pattern.

---

## 2. CONTRADICTIONS

### C1. Detail presentation: B's inline panel vs A's slide-over — B is internally inconsistent
- **A says:** capability/authority detail opens as a slide-over sheet (R6); wireframe R6 shows the sheet.
- **B says:** `[ Selected Door Detail ] capability | identity | auth | authority | health | receipts` as an inline panel below the door grid — but B's own mobile clause says "detail opens full-screen," which contradicts B's desktop inline panel.
- **Recommended resolution:** A's slide-over (detail as overlay). B's mobile clause already assumes detail is an overlay, not an inline page section; the functional contract's five-layer law favors a signature composition that doesn't permanently reserve screen for detail that may not be selected. A's R6 wins; B should drop the inline detail panel.

### C2. "Receipts": inline tab (B) vs Ledger handoff (A)
- **A says:** `"Receipts"` hands to the **Ledger**, pre-filtered to the door — predicate 6: "same canonical events, not a copy."
- **B says:** `receipts` as one of six facets inside the selected-door detail (inline tab).
- **Recommended resolution:** A. The projection contract's one-object-many-projections law (§4): the Ledger is the canonical receipts surface; a door detail that re-hosts receipts risks copies (`feed-copy-123` problem). B's six-facet list should reduce to five; "receipts" becomes the handoff A specifies.

### C3. Primary action labels: exact per-state labels (A) vs merged "Connect/Authenticate" (B)
- **A says:** primary button labeled exactly per state — `"Connect"` (never-connected) / `"Authenticate"` (connected, unauthenticated) / `"Configure"` (live).
- **B says:** controls list "Connect/Authenticate" as one merged item plus "Configure," with no state-to-label mapping.
- **Recommended resolution:** A. The four-state non-collapse law (agreed by both) requires distinct labels for distinct states; a merged "Connect/Authenticate" label blurs the connection-vs-authentication boundary both sides claim to lock. A's state mapping wins.

### C4. Revoke/Disconnect placement and gating
- **A says:** destructive zone *inside the authority sheet*; rendered only when the runtime permits; always requires a confirmation naming the door and scopes (predicate 10).
- **B says:** "Revoke/Disconnect" as a plain per-door control in the controls list, no gating specified.
- **Recommended resolution:** A. Functional contract §3: "Dangerous/consequential actions surface authority/confirmation as required." A top-level per-door revoke without gating violates the conservative authority boundary both sides endorse (see agreement 8). B should adopt A's placement + runtime-permission gate + confirmation.

### C5. Global search
- **A says:** no search control anywhere (not in SPEC.md or wireframe).
- **B says:** `[GLOBAL SEARCH]` at the top of the desktop composition, no justification.
- **Recommended resolution:** omit for V1. Functional contract §3: "Search/filter controls appear only where they materially reduce burden." A door inventory (single-digit items per the registry model) does not meet the burden test. If `[GLOBAL SEARCH]` is intended as Hub-global chrome rather than room content, it should not appear in the room composition — [NEEDS DIRECTOR TASTE] to confirm whether global search is room-level or Hub chrome.

### C6. Accent token: A's own internal tension (FUNCTIONAL-SPEC prose vs token law)
- **A says (OPEN TASTE QUESTIONS):** FUNCTIONAL-SPEC names the room theme "teal / emerald" but `1278-tokens.css` defines `--accent-connect: var(--green)`.
- **B says:** nothing.
- **Recommended resolution:** keep `--green`. Tokens are visual law; prose in the functional contract does not override the locked token file. Recorded here because A flagged it — but this is decided by grounding hierarchy, not taste. (--teal `#40d3bb` and --emerald `#35e0a1` exist in tokens but are not the room accent.)

### C7. BLOCKER — Predicate 2 contradicts R2 + wireframe ("live connect button" for REGISTERED_CONTRACT_ONLY doors)
- **A's acceptance predicate 2 says:** "Contract-only (`REGISTERED_CONTRACT_ONLY`) and `ROADMAP` doors **never render a live connect button**."
- **A's R2 says:** primary button per state: `"Connect"` (never-connected) — and the wireframe renders a primary `"Connect"` button on the REGISTERED_CONTRACT_ONLY door card.
- **The parse is ambiguous and both parses are bad:** if "live connect button" = [live][connect button] (a button implying live connectivity), the phrase is undefined — no such button exists in the spec. If it means [a connect button that is functional/live], it directly contradicts R2 and the wireframe's Connect button on the contract-only door.
- **Recommended resolution:** rewrite predicate 2 as: "`REGISTERED_CONTRACT_ONLY` doors render `"Connect"` (initiate connection), never a button labeled as if already live; `ROADMAP` doors render no connect-class button at all." The current wording cannot be tested.

### C8. BLOCKER — Wireframe R5 violates R5 parity (missing door)
- **A's SPEC R5 says:** "The list is the accessibility-equivalent of the portal bay — **same data, same actions, same order of doors**." Predicate 5 locks parity.
- **Wireframe R2 shows 3 doors** (LIVE/AUTHENTICATED/GRANTED/HEALTHY; CONNECTED/UNAUTHENTICATED/NOT GRANTED/UNKNOWN; REGISTERED_CONTRACT_ONLY). **Wireframe R5 shows only 2** (LIVE and REGISTERED_CONTRACT_ONLY) — the CONNECTED/UNAUTHENTICATED door is missing from the list.
- **Recommended resolution:** fix the wireframe to include all three doors in registry order before freeze. This is an artifact defect, not a spec disagreement.

### C9. BLOCKER — Predicate 2 references an undefined "live grouping"
- **Predicate 2:** contract-only and ROADMAP doors "never appear in the portal bay's **'live' grouping**."
- **No "live grouping" exists in SPEC.md.** The portal bay is specified as radial around the core (grid fallback); no grouping by liveness is defined anywhere.
- **Recommended resolution:** either define a live-grouping concept (and its sort rule — which is already A's open taste question about ordering by state) or delete the phrase. As written the predicate is untestable.

### C10. BLOCKER — Wireframe invents badge labels absent from the door-state vocabulary
- **A's (a)(7) door machine vocabulary:** LIVE · CONNECTED · AUTHENTICATING · REGISTERED_CONTRACT_ONLY · ROADMAP · DEGRADED · BLOCKED · UNAUTHORIZED · ERROR · DISCONNECTED.
- **Wireframe door 2 renders:** Auth: `UNAUTHENTICATED`, Authority: `NOT GRANTED`, Health: `UNKNOWN` — none of which appear in the vocabulary, and the SPEC component table's badge inventory only colors LIVE/CONNECTED/AUTHENTICATING/REGISTERED_CONTRACT_ONLY/ROADMAP/DEGRADED/BLOCKED/ERROR/UNAUTHORIZED/DISCONNECTED (plus GRANTED/LIMITED for authority).
- **Recommended resolution:** extend the vocabulary to name the Auth row values (`AUTHENTICATED` / `UNAUTHENTICATED` / `—`) and Authority row values (`GRANTED` / `LIMITED` / `NOT_GRANTED` / `—`) explicitly in (a)(7), and bind them to badge colors. Wireframe shows dashes for inapplicable rows on door 3 but UNAUTHENTICATED/NOT GRANTED on door 2 — the rule for when a row shows a value vs `—` is undefined. Define it.

### C11. Naming drift: CONNECT_AUTHENTICATE vs "Authorize"
- **A's allowed actions (a)(5):** `CONNECT_AUTHENTICATED`… i.e. `CONNECT_AUTHENTICATE`; primary buttons are `"Connect"`/`"Authenticate"`.
- **A's R7 modal confirm button:** `"Authorize [scope summary]"` — "Authorize" matches neither the allowed-action verb nor any primary button label.
- **Recommended resolution:** reconcile the modal button to the state machine: the modal is the *authenticate* flow, so the confirm should be `"Connect"` or `"Authenticate [scopes]"` per the door's state, not a third verb "Authorize." Minor but it undermines the exact-labeling discipline A locks elsewhere (C3).

### C12. "Request card" orphan in the component inventory
- **Component inventory row:** "Request card + modal form | R3 `"Request a new door"`".
- **SPEC R3 defines only a secondary button** `"Request a new door"` opening a modal form — there is no "Request card" component defined in any region.
- **Recommended resolution:** drop "Request card" from the inventory (the button + modal form is fully specified) or define what a request card is. An inventory entry with no blueprint region is a dead reference.

---

## 3. GAPS

Verified asymmetries (not the task's example — checked both files):

**Substantive elements A has that B lacks:**
- **Cross-room handoffs.** A (a)(8): Connections · Spaces · Ledger · Mail · Settings. B: none.
- **Acceptance predicates.** A: 11 mechanical predicates (d). B: one "Proof" paragraph.
- **Component inventory with token basis.** A: full table bound to `1278-tokens.css`. B: none (no visual law at all).
- **Door-state machine vocabulary.** A (a)(7): 10-state room vocabulary + 10-state door vocabulary. B: only the four-way distinction line.
- **Truthful states (room-level).** A: LOADING/EMPTY/READY/BLOCKED/UNAUTHORIZED/NOT_VERIFIED/VERIFIED/ERROR/OFFLINE/UNKNOWN/DISABLED + honest empty/registry-unavailable renderings. B: no state list, no empty/error renderings.
- **Naya behavior.** A: `"Ask Naya: Which door should I use?"` as R3 global primary, advice = labeled suggestion, never a permission grant. B: no Naya behavior section at all (violates its own ROOM-BLUEPRINT-STANDARD-V1 outline).
- **Roadmap treatment.** A: R4 band, muted/grayscale, dashed border, `ROADMAP` badge, `"View proposal"` only, example inventory (REST/Webhooks/SDK/A2A/MCP Apps). B: only the prohibition rule.
- **Accessible door list parity.** A: R5 list view + toggle + predicate 5 parity + keyboard/AT requirements (predicate 11). B: no accessibility section (also violates its own blueprint standard).
- **Registry ordering rule.** A predicate 1: doors match the registry exactly, same order. B: silent.
- **Authority sheet contents.** A R6: permitted verbs, scopes, rate/retention limits, who granted, expiry, disconnect/revoke zone. B: "Required Authority" as a control name only.
- **Governed connect/auth flow.** A R7: scopes shown, identity shown, `"Authorize [scope summary]"` confirm, `"Not now"` cancel, no fake success animation. B: no flow.
- **"Request a new door" workflow.** A: R3 secondary + predicate 7 (governed request receipt, never an authority grant). B: silent.
- **Anti-patterns beyond the two rules.** A forbids: dead connect buttons, generic integrations-marketplace look, fake success animation, hardcoding roadmap examples as live. B's "Do not" covers only roadmap-as-live and connection-grants-authority.

**Elements B has that A lacks:**
- **Labeled "First 3 seconds" entry.** B has the labeled section; A expresses the substance in R1 (orientation band) but lacks the labeled 3-second entry. Structural only, not substantive — A is complete on substance.
- **`[GLOBAL SEARCH]` in composition.** See C5 — its presence is a contradiction, not an advantage; listed here because A genuinely lacks any search control and a decision is owed.
- **"identity" as an explicit detail facet.** B's selected-door detail lists `capability | identity | auth | authority | health | receipts` — six facets including `identity`. A's sheets cover capability + authority (who granted/scopes/expiry) + auth modal (identity used), but "identity" is not named as a distinct door-detail facet. Substantive gap: A should confirm whether identity (which identity is in use per door) is surfaced per-door or only at auth time.

**No-Hub-Capture watchpoint (A, predicate 7 + R3 "Request a new door"):** A says the request "produces a governed request receipt — it never grants authority or creates a live door." This is consistent with the projection contract's Hub-action boundary (§10: the Hub may request/handoff intent; the upstream system owns execution and canonical persistence) — but only if the receipt is **issued by the governed runtime and observed by the Hub**, not minted by Hub form code. The spec never states which side mints the receipt. Not a violation as written (it says "governed"), but a freeze-grade clarification is required: "the request is submitted to the governed runtime; the receipt is observed from runtime, never minted in the room." Flagged as a required edit, not a blocker, because the wording "governed request workflow" currently leans compliant.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides' flagged items, deduplicated (A's six, none from B — B flags zero):

1. [NEEDS DIRECTOR TASTE] Accent: keep token law `--accent-connect: var(--green)` vs FUNCTIONAL-SPEC prose "teal / emerald"? (Reviewer: grounding hierarchy says `--green` — see C6 — but A explicitly asked, so recorded.)
2. [NEEDS DIRECTOR TASTE] Portal-bay geometry: exact geometry unspecified (ring count, ordering by status vs provider). A's R2 locks "radial around the core" but not ordering.
3. [NEEDS DIRECTOR TASTE] Authority sheet "who granted": owner name vs opaque identity id? Consent-sensitive; A defaults to opaque id pending direction.
4. [NEEDS DIRECTOR TASTE] "Test connection" semantics: successful test writes a Ledger receipt vs read-only probe with no receipt? A assumes probe writes no receipt.
5. [NEEDS DIRECTOR TASTE] Roadmap proposals: `"Request early access"` control allowed, or does any such control imply connectability? A defaults to no (only `"View proposal"`).
6. [NEEDS DIRECTOR TASTE] Naya door advice: inline `"Connect"` shortcut in the recommendation, or must advice and action stay visually separate so advice is never mistaken for a permission grant? A defaults to separate.
7. [NEEDS DIRECTOR TASTE] (new, from C5) Global search: is `[GLOBAL SEARCH]` intended as Hub-global chrome or room content? If the former, remove from room composition; if the latter, justify under the burden test.
8. [NEEDS DIRECTOR TASTE] (new, from A's decorative core) The NayaPOWER core emblem: A's wireframe locks it as decorative center; B's composition omits it entirely. Is the core emblem part of the signature instrument or disposable decor? (No grounding decides; both compositions work without a ruling.)
9. [NEEDS DIRECTOR TASTE] (new, gap above) Identity facet: should "identity in use" be an explicit per-door detail facet (B implies yes), or surface only at auth time and in the authority sheet (A's current shape)?

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION.** Blocking items (by name):

1. **C7 — Predicate 2 wording contradiction:** "never render a live connect button" for contract-only doors contradicts R2's `"Connect"` (never-connected) and the wireframe's Connect button on the REGISTERED_CONTRACT_ONLY door. Rewrite or the predicate fails its own spec.
2. **C8 — Wireframe R5 parity defect:** the CONNECTED/UNAUTHENTICATED door is missing from the accessible list; SPEC demands same doors, same order. Fix the artifact.
3. **C9 — "Live grouping" undefined:** predicate 2 references a portal-bay "live grouping" that exists nowhere in the spec. Define it or delete it.
4. **C10 — Undefined badge labels:** wireframe's `UNAUTHENTICATED` / `NOT GRANTED` / `UNKNOWN` labels are not in the (a)(7) door-state vocabulary; the value-vs-dash rule is undefined. Extend the vocabulary and bind badge colors.
5. **C11 — Verb drift:** R7's `"Authorize [scope summary]"` matches neither the allowed action `CONNECT_AUTHENTICATE` nor the per-state labels. Reconcile before build.
6. **C12 — "Request card" orphan:** inventory references a component no region defines. Define or delete.

Required non-blocking edits before build (can land with the same revision): receipt-minting clarification (No-Hub-Capture watchpoint — receipt observed from governed runtime, never minted in the room); per-door identity facet decision (#9 in taste questions).

Resolutions already decided by grounding (no director time needed): slide-over detail over inline panel (C1), Ledger handoff for Receipts (C2), exact per-state labels (C3), revoke gated inside authority sheet (C4), omit global search pending chrome ruling (C5), keep `--green` accent (C6).
