# SETTINGS — Lane Reconciliation (A = SPEC.md + wireframe.html · B = 11-settings.md)

**Reviewer stance:** adversarial toward both sides. A = my lane (SPEC-FIRST: SPEC.md + annotated wireframe.html). B = Naya 3's lane blueprint (claims ROOM-BLUEPRINT-STANDARD-V1). Settings is the authority/privacy/consent surface — protected boundaries, extra scrutiny applied.

---

## 1. AGREEMENTS

Locked identically on both sides — specific elements confirmed:

1. **Signature instrument = Control Deck.** A: metaphor "THE CONTROL DECK" (§header, §2). B: "Primary instrument: Control Deck with truthful setting ownership."
2. **Human job / purpose.** A: "How should NayaNET work for me?" B: "Let the human understand and control how NayaNET works for them." Same job.
3. **Four-way setting ownership truth.** A: ScopeBadge LOCAL / ACCOUNT / GOVERNED / UNAVAILABLE per row, no scope-less row (acceptance predicate 1). B: "Each setting must identify: local preference; account-backed setting; governed runtime policy; external connection state." Same four-way honesty model.
4. **No local toggle masquerading as server-enforced privacy.** A: forbidden substitute — "Never make a local toggle look like a server-enforced privacy guarantee" (contract header field 6). B: "do not make localStorage toggle look like server-enforced privacy." Identical lock.
5. **System Health is secondary, last, subdued — never primary.** A: predicate 7 + §2 ("always last, visually subdued", "never promoted to the rail"). B: "do not put System Health in primary rail", "do not expose raw technical diagnostics as default Settings", desktop composition shows `[ Advanced → System Health ]` as a separate trailing section. Agreed — with one internal-A tension noted in §2.
6. **No-Hub-Capture honored by both.** A: forbidden list bans "generate canonical report / create Smart Note" capture controls; "Ask Naya what this setting means" is "context-scoped ASK_NAYA (explains — never creates intelligence)"; canonical records "live in the runtime/consent law; the room never invents a second store." B's allowed surface is control-only. Neither side proposes a Hub-side canonical capture control. A is explicitly law-consistent with INTELLIGENCE-PROJECTION-CONTRACT-V1 §3/§10.
7. **Truthful proof for governed changes.** A: "Saved" must reflect a real write (reload preserves; LOCAL persists on device; ACCOUNT/GOVERNED persist server-side and re-read), UNAVAILABLE rendered with reason, consequential changes produce timestamped receipts + Ledger links. B: "Changing a governed setting shows the actual persisted result or an honest failure/blocked state." Same law.
8. **"Your Intelligence — your intelligence is yours" exists as a category.** A: category 3 of 9. B: full-width section in desktop composition. Presence agreed; *emphasis* differs (contradiction 5 below).
9. **Accent = neutral/silver.** A locks `--accent-settings: var(--muted)`. Verified in `1278-tokens.css:49` (`--accent-settings: var(--muted)`). B is silent — tokens ground A; no conflict.
10. **Search exists.** A: header search "Find a setting…" over labels + synonyms + plain-language descriptions. B: desktop composition opens with `[GLOBAL SEARCH]`. Presence agreed; A's human-language synonym layer is the stronger, tested elaboration (acceptance predicate 2).
11. **Core category overlap.** Both lock: Identity & Account, Privacy & Consent, Connections & Doors, Notifications, Appearance & Accessibility, Advanced → System Health. The deltas (Authority, Security, Data, Naya Preferences, Trust & Data) are contradictions — §2.

---

## 2. CONTRADICTIONS

### C1. Category taxonomy: standalone Authority / Security / Data vs folded
- **A says:** 9 categories — Identity & Account, Privacy & Consent, **Your Intelligence**, Connections & Doors, **Naya Preferences**, Notifications, Appearance & Accessibility, **Trust & Data**, System Health. AUTHORITY and SECURITY concepts are *folded* into Privacy & Consent / Identity; DATA is renamed "Trust & Data".
- **B says:** Identity & Account, Privacy & Consent, **Authority** (standalone), Connections & Doors, Notifications, **Data** (standalone), **Security** (standalone), Appearance & Accessibility, Your Intelligence, Advanced → System Health. No "Naya Preferences", no "Trust & Data".
- **Recommended resolution:** [NEEDS DIRECTOR TASTE]. Neither side wins on grounding alone. Adversarial note toward A: Settings is the authority/privacy/consent surface — folding AUTHORITY out of the visible taxonomy risks diluting exactly the protected envelope this room exists to make legible (collective participation, revocation, policy defaults are authority decisions; hiding them inside "Privacy & Consent" rows makes the authority boundary *less* discoverable, which cuts against the room's human job). Adversarial note toward B: B provides only a section-name list with zero rows, controls, or scope treatment for Authority/Security/Data, so its standalone categories are labels without law — a taxonomy without substance. A's taste question 3 already flags this exact fork; keep it flagged. Do not resolve by synthesis until Shawn tastes it.

### C2. Desktop composition: two-pane rail (A) vs category grid + section below (B)
- **A says:** left category rail (~260px) with state dots; detail panel right; one category open at a time; mobile = category list → focused detail.
- **B says:** `[GLOBAL SEARCH]`, `[Settings]`, a 3-column card grid of category tiles, then `[ selected settings section ]` below the grid, then `[ Advanced → System Health ]`.
- **Recommended resolution: A's rail wins on grounding.** Both sides forbid the giant scrolling control dump; B's grid-then-section-below composition forces scroll-to-reach-the-selected-section and puts navigation *above* content in a way that duplicates the rail's job without its affordances (per-category state dots like "1 unsaved" / "attention needed" are specified in A and have no home in B's grid). The Control Deck instrument reads as command-console, not dashboard-grid. Rail stays; grid dropped. ([NEEDS DIRECTOR TASTE] only if Shawn prefers the grid's scannability — but no grounding favors it.)

### C3. Internal-A: System Health placement ("not in the primary rail" vs wireframe)
- **A says (SPEC predicate 7):** "not in the primary rail, always last in the category list, visually subdued."
- **A says (wireframe):** System Health rendered *as a row inside the rail* (dimmed, "advanced · last · subdued").
- **B says:** `[ Advanced → System Health ]` — a separate trailing disclosure, not a rail row. B is internally consistent.
- **Recommended resolution: adopt B's placement.** The predicate's "not in the primary rail" is the stronger normative statement (it also matches ROOM-FUNCTIONAL-CONTRACT-V1 §10: "System health is an advanced control/diagnostic surface" — not a room, not a category). Fix the wireframe: move System Health out of the rail into a collapsed "Advanced → System Health" disclosure beneath it. This is a spec-internal repair, not a product decision.

### C4. Internal-A: "Sign out" row placement
- **A says (SPEC §2 category 1):** Identity & Account covers "authentication/session".
- **A says (wireframe):** the "Sign out" row is rendered inside the **Privacy & Consent** detail panel.
- **B says:** silent (no rows specified).
- **Recommended resolution:** wireframe is wrong; move "Sign out" to Identity & Account per SPEC §2. The wireframe's Privacy & Consent example panel currently mis-files an Identity row, which an independent builder would copy. Adversarial note: sensitive controls are the exact rows where misfiling is dangerous — a misplaced Sign out in front of consent wording invites misreads. Fix the wireframe fixture.

### C5. Internal-A: "Motion preference" example row placement
- **A says (SPEC §2 category 7):** Appearance & Accessibility covers motion/text/contrast.
- **A says (wireframe):** "Motion preference" toggle rendered inside the **Privacy & Consent** detail panel.
- **Recommended resolution:** wireframe fixture wrong; move to Appearance & Accessibility. Same repair class as C4. (Fixture rows are visual placeholders, but placement teaches the builder the category model — wrong examples propagate.)

### C6. "Your Intelligence" emphasis: rail category (A) vs full-width banner (B)
- **A says:** Your Intelligence is category 3 of 9 — equal weight in the rail.
- **B says:** `[ YOUR INTELLIGENCE — your intelligence is yours ]` as a full-width banner between the category grid and the selected section — elevated above all categories.
- **Recommended resolution:** [NEEDS DIRECTOR TASTE]. No grounding decides emphasis. Note for the taste brief: the banner reading "your intelligence is yours" is the room's strongest trust signal on the consent surface; A's equal-weight rail treatment undersells the single most differentiating promise of the product. But elevating it breaks rail symmetry and duplicates its content with Privacy & Consent rows. Shawn's call.

### C7. Per-row immediate save vs dirty-panel save model — tension, not contradiction
- **A says (SPEC §2):** action bar appears *only when dirty*; *also* "per-row save is allowed where the control is atomic (e.g. toggles write immediately with a 'Saved ✓' micro-confirmation)".
- **B says:** silent.
- **Recommended resolution:** sharpen, don't drop. The two modes are compatible *only* if atomic-immediate is restricted to LOCAL/ACCOUNT non-sensitive controls; any GOVERNED or sensitive row (privacy/consent/collective/delete/revoke) must route through the dirty-panel + ConfirmationFlow path per acceptance predicate 3 ("skipping it is impossible in the UI path"). Add an explicit predicate: "No GOVERNED or sensitive row may use atomic immediate-save; immediate-save is LOCAL/ACCOUNT non-sensitive only." Otherwise the spec contains a bypass-shaped loophole around its own consent gate.

### C8. B's "[GLOBAL SEARCH]" — scope ambiguity
- **A says:** settings-scoped human-language search ("Find a setting…", labels + synonyms + descriptions), placed in the room header.
- **B says:** `[GLOBAL SEARCH]` at the top of the desktop composition — unclear whether this is the Hub-global search shell element or a settings-scoped search.
- **Recommended resolution: A's wins.** If B's box means the shell's global search, it doesn't belong in a room blueprint at all; if it means settings search, A's specified, tested version (predicate 2's synonym set) supersedes it. Either way the room owns a settings-scoped search per A.

---

## 3. GAPS

**B (11-settings.md) is structurally incomplete against the standard it claims.** ROOM-BLUEPRINT-STANDARD-V1 lists: first-3-seconds entry, desktop composition, signature instrument, controls+placement, data contract, truthful states, handoffs, Naya behavior, mobile, accessibility, visual law, acceptance journey, anti-patterns, proof required. B actually contains: purpose, first-3-seconds ✓, desktop composition ✓ (thin), primary instrument ✓ (one line), controls ✓ (four bullets), sections list, do-not ✓ (three), proof ✓ (one line). **Missing from B:** data contract (only the four-way ownership sentence — no canonical object, no runtime owner, no allowed-actions list, no forbidden substitutes), truthful states beyond the single proof line (no LOADING/EMPTY/READY/BLOCKED/UNAUTHORIZED/ERROR/OFFLINE matrix), cross-room handoffs, Naya behavior, mobile composition, accessibility, visual law (no token/accent reference), acceptance journey, anti-patterns (only 3 do-nots), proof-required section. The file reads as a sketch of the standard's headings, not an instance of it.

**B is also missing every element that makes A's spec buildable:** acceptance predicates (A's 10 mechanical predicates), component inventory (ScopeBadge, ConfirmationFlow, SettingsCategoryNav, panels), the ConfirmationFlow modal and receipt/Ledger-link mechanics, scope legend, UNAVAILABLE honest-rendering rules, "Why this matters" explainers, Ask-Naya context-scoped behavior, and OPEN TASTE QUESTIONS (B flags zero).

**A's gaps vs B:** A lacks B's standalone Authority/Security categories (intentional fold — contested in C1, already a taste question); A lacks an explicit "external connection state" per-row truth distinct from the four ScopeBadge variants (B's fourth ownership bullet) — A's Connections & Doors *category* plus door-health tiles cover it, but no per-setting "connection state" badge exists. Minor: adopt as a row-level annotation inside Connections & Doors rather than a fifth badge.

**Wireframe-vs-SPEC gaps (A internal):** the wireframe contains no rendering of LOADING/EMPTY/ERROR/OFFLINE/UNAUTHORIZED states (only an annotation line claiming they exist), no dirty-state transition, no ConfirmationFlow receipt line rendered (only annotated), and no search-results state. The wireframe annotates more than it draws — a builder cannot verify predicates 8 or 4 from the wireframe alone.

**Grounding gap both sides inherit:** A's taste question 6 is correct and stands — no canonical consent/privacy state schema (fields, states, receipt format for MANAGE_CONSENT/CHANGE_PRIVACY) was found in grounding. The ConfirmationFlow's "receipt line" and "View in Ledger" link are specified without a receipt schema to bind to. This is a build-blocker owned by the governed consent law, not by either lane.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides, deduplicated. B flagged none; all six are A's, carried forward verbatim in substance:

1. [NEEDS DIRECTOR TASTE] **Privacy/consent policy defaults** — sharing defaults, collective participation default (opt-in vs opt-out at Hub activation), retention defaults, entry-consent wording. Protected boundary: Shawn's explicit word required. Spec wires controls only.
2. [NEEDS DIRECTOR TASTE] **Delete scope** — what "Delete my data" covers (local cache vs account intelligence vs collective distilled projections); revocation's historical handling needs his confirmation of the governed revocation contract's current state.
3. [NEEDS DIRECTOR TASTE] **Category order/merge** — A's 9-category fold vs B's standalone AUTHORITY / SECURITY / DATA categories (see C1). Is the fold correct, or do Authority and Security need their own categories?
4. [NEEDS DIRECTOR TASTE] **Who may see System Health details** — any user vs "authorized/advanced users"; what defines "authorized" here?
5. [NEEDS DIRECTOR TASTE] **Notifications** — which channels actually exist (push/email/in-Hub?) and quiet-mode semantics. Rows are wired; the supported set needs confirmation.
6. [NEEDS DIRECTOR TASTE] **Grounding gap: consent/privacy state schema** — builder needs the governed consent-law field contract (fields, states, receipt format for MANAGE_CONSENT/CHANGE_PRIVACY). Flagged, not invented.
7. [NEEDS DIRECTOR TASTE] **"Your Intelligence" emphasis** — equal-weight rail category (A) vs full-width trust banner (B). New from this reconciliation (C6).
8. [NEEDS DIRECTOR TASTE] **Composition** — two-pane rail (A, recommended) vs card grid (B). New from this reconciliation (C2); recommend rail, keep open only if Shawn prefers the grid.

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION.** Blocking items, by name:

1. **Category taxonomy (Authority/Security/Data)** — C1 / taste question 3. The two lanes specify mutually exclusive taxonomies; freezing either without Shawn's taste bakes in a contested information architecture on the consent surface.
2. **"Your Intelligence" emphasis** — C6 / taste question 7. Rail row vs full-width banner; affects the room's trust posture, not just layout.
3. **B's structural incompleteness** — Naya 3's lane must either fill the missing ROOM-BLUEPRINT-STANDARD-V1 sections (data contract, truthful states, handoffs, Naya behavior, mobile, accessibility, visual law, acceptance journey, proof required) or formally adopt A's elaborations as the shared detail layer. A blueprint that omits handoffs and truthful states on the *consent surface* cannot freeze.
4. **Consent/privacy receipt schema** — taste question 6. The ConfirmationFlow's receipt + "View in Ledger" link are specified against a schema that doesn't exist in grounding. Flagged correctly, not invented — but it stays a build-blocker until the governed consent-law contract lands.
5. **Policy defaults + delete scope** — taste questions 1–2. Protected boundaries; controls are wired, defaults are not. Cannot freeze as buildable.

**Non-blocking (repair inside the envelope before freeze, no director word needed):**
- R1. Fix wireframe: move System Health out of the rail into "Advanced → System Health" disclosure (C3).
- R2. Fix wireframe: move "Sign out" row to Identity & Account (C4).
- R3. Fix wireframe: move "Motion preference" example to Appearance & Accessibility (C5).
- R4. Add predicate: atomic immediate-save is LOCAL/ACCOUNT non-sensitive only; GOVERNED/sensitive rows always take the dirty-panel + ConfirmationFlow path (C7).
- R5. Wireframe should actually draw LOADING/ERROR/OFFLINE/UNAUTHORIZED states (or one state-sheet view) instead of annotating them — predicate 8 is unverifiable from the current wireframe.
- R6. Adopt A's settings-scoped search as the room search; clarify B's "[GLOBAL SEARCH]" is the shell element, not the room's (C8).

**Adversarial close:** both sides are clean on the No-Hub-Capture law — no element in either spec implies Hub-side creation of canonical objects; A's forbidden list explicitly bans capture controls, and consent/export/delete/revoke are correctly framed as governed *control* actions (allowed under the projection contract's Hub Action Boundary §10), not intelligence production. The spec's weakest point is not lawfulness but completeness: B is a sketch wearing the standard's name, and A's consent machinery points at a receipt schema that doesn't exist yet. Freeze the law, don't freeze the gaps.
