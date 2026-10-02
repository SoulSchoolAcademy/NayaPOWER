# Connections Room — Reconciliation V1

**Date:** 2026-10-01 · **Reviewer role:** independent (neither lane)
**Side A:** `connections/SPEC.md` + `connections/wireframe.html` (my lane, SPEC-FIRST)
**Side B:** `grounding/blueprints/07-your-connections.md` (Naya 3's lane blueprint)
**Grounding cited:** `INTELLIGENCE-PROJECTION-CONTRACT-V1.md` (projection contract / No-Hub-Capture law), `ROOM-FUNCTIONAL-CONTRACT-V1.md`, `1278-tokens.css` (tokens = visual law), `blueprints/_STANDARD.md` (15 required blueprint sections).

Shawn's law: "No blueprint, no building"; taste belongs at blueprint stage.

---

## 1. AGREEMENTS

Locked identically on both sides (element named, both sides confirm):

1. **Human job.** A §(a)1: "Who and what am I connected to, and on what terms?" B Purpose: "Show who/what is meaningfully connected and why." Same job, same words in substance. LOCKED.
2. **Room title and theme.** A: title "Your Connections", theme orange (`--accent-connections`, confirmed present in `1278-tokens.css:45`). B: "Your Connections". LOCKED.
3. **Projection law — no Hub-owned relationship store.** A §(a)4: "The room owns no relationship store of its own; it projects" (identity + consent runtime via shared Hub runtime adapter); forbidden substitute: "no Hub-local relationship store diverging from the runtime." B Data: "Canonical relationships + consent/privacy + related intelligence" consumed, not authored. Both satisfy the projection contract. LOCKED.
4. **Consent/privacy scope always visible.** A: "Consent & privacy" panel section + `ConsentStateBadge` component. B: control "inspect consent/privacy"; anti-pattern "do not expose private relationship metadata". LOCKED as a requirement (exact badge wording is A's, uncontested).
5. **Space scope chip in header.** A R1: "Space: \<name\>" chip. B composition: `[Space]` chip next to title. LOCKED.
6. **Control inventory (existence).** Both lock: select relationship, constellation/graph view, view toggle to accessible list, open Mail / message, open shared Space, view shared intelligence, Ask Naya, adjust sharing (governed), disconnect/revoke with confirmation, inspect consent. B's "disconnect/revoke when governed" = A's DISCONNECT_REVOKE with authority + confirmation. LOCKED.
7. **Cross-room handoff destinations (core).** A §(a)8: Mail (communicate), Spaces (shared context), Ledger (proof/history), Feed/Library (shared intelligence), Connect (technical channel). B controls: "open Mail", "open Space", "Evidence" (= Ledger). Mail/Space/Evidence destinations agree. LOCKED for the three shared destinations; Feed/Library + Connect are A-only additions (see §3).
8. **Mobile posture.** A: "list-first (R3a defaults to the accessible list); constellation available via the 'Constellation' toggle; R3b opens full-screen on selection." B: "List first; relationship detail full-screen. Graph optional." LOCKED.
9. **Graph-is-not-the-product behavioral law.** A forbidden substitute: "no giant useless spiderweb". B: "do not make graph the product." Same prohibition, different words. LOCKED as law; the naming dispute underneath it is §2.1.
10. **Naya's read visually distinct from source truth.** A R3b §6: "Important context — Naya's read" with `--accent-connections` left border + `--fs-small`, labeled as Naya's read; predicate 3. B panel includes "why it matters" as a Naya-context slot (less specified). The *requirement* is locked; the *exact treatment* is A's uncontested detail.
11. **Pending requests are never auto-accepted.** A §(a)6. B is silent but does not contradict; no side asserts auto-accept. LOCKED by A's uncontested boundary.
12. **EMPTY state wording and no-invented-suggestions rule.** A R5: EMPTY = "No governed connections in this scope." + "No invented suggested people"; forbidden substitute + predicate 10: "No suggested person appears without a legitimate, shown discovery basis." B does not contradict. LOCKED (A's wording stands uncontested).

---

## 2. CONTRADICTIONS

### 2.1 Signature instrument: what is the room's primary object?

- **A says:** "Signature instrument: Relationship Constellation" (SPEC.md header + R3a, ~60% of the main split). The graph is the named instrument.
- **B says:** "Primary instrument: **Relationship Inspector**; graph is supporting visualization." The detail panel is the instrument; the graph is subordinate.
- **Recommended resolution:** A's naming wins, B's behavioral priority wins. Grounding: `ROOM-FUNCTIONAL-CONTRACT-V1.md` §2 literally enumerates **"relationship constellation"** as one of the canonical signature-instrument examples — that is the stronger grounding for the *name*, and B's file cites no grounding for "Relationship Inspector". But B's *substance* ("do not make graph the product") is already locked by both sides (§1.9), so the freeze should name the instrument "Relationship Constellation" and define it as **the inspector's visualization**: the room's jobs complete in the selected-relationship panel (B's Inspector), the graph is its navigational surface. Concretely: keep A's name, adopt B's panel-first product law explicitly in the spec text, and rename R3b to "Relationship Inspector panel" so a cold builder cannot read "constellation = product".

### 2.2 Category tabs: five tabs vs three

- **A says:** R2 tabs exactly "People" · "Nayas" · "Organizations" · "Shared Spaces" · "Requests" (with pending-count badge).
- **B says:** composition line `[People | Systems | All]` — three tabs, different taxonomy ("Systems", "All"; no "Nayas", "Organizations", "Shared Spaces", "Requests").
- **Recommended resolution:** A wins. Grounding: A's tabs map 1:1 onto A's canonical node types (human / Naya-agent / organization / Space / system-door, §(a)3), while B's "Systems" and "All" have no data-contract referent anywhere and B defines no Requests surface at all (see §3.6). B's taxonomy is ungrounded. Lock A's five tabs. The one salvageable question — whether "System" (A's badge type, R3b §1) needs its own tab — is already answered: no, A shows System as a badge, not a tab.

### 2.3 What does "Message" do? (also an A-internal contradiction)

- **A says (two things):** §(a)8 handoffs lock "communicate → Mail", but OPEN TASTE QUESTION 3 asks "What does 'Message' do — open Mail compose, open a chat surface, or hand off to the Connect room's channel? The button exists; its destination is undecided." **A contradicts itself**: the handoff field asserts Mail while the taste question reopens it.
- **B says:** control "open Mail" — asserts the Mail destination without flagging ambiguity.
- **Recommended resolution:** B + A's own handoff line outvote A's taste question. Lock: "Message" = handoff to Mail (communicate → Mail, §1.7). Strike or narrow A's Q3 to what is genuinely undecided — the exact Mail surface (compose vs. existing thread), which neither side specifies. Mark that remainder [NEEDS DIRECTOR TASTE].

### 2.4 Panel buttons: B's [Open] and [Evidence] vs A's action row

- **A says:** action row = "Message" (primary) + "Open shared Space", "View shared intelligence", "Adjust sharing…", "Ask Naya about this"; overflow "⋯" holds "Disconnect…" and "Open in Ledger".
- **B says:** panel buttons `[Open] [Message] [Ask Naya] [Evidence]`.
- **Recommended resolution:** A wins on inventory (exact labels, primary/secondary/overflow discipline per universal control rules, functional contract §3). B's "Evidence" maps to A's "Open in Ledger" (rename to B's shorter "Evidence" is taste, not substance — flag as director-taste micro-decision). B's bare "[Open]" is ambiguous and must not survive: every action needs a defined destination (functional contract §3, "Every action has a defined destination/result state"). If [Open] means "open the canonical relationship record," say so; otherwise delete it.

### 2.5 Panel section granularity

- **A says:** ten sections; "Last activity" (§7) and "Next relevant action" (§8) are separate.
- **B says:** merged "recent meaningful activity"; "why it matters" as one Naya slot (A splits "Important context" and "Next relevant action").
- **Wireframe says (third voice):** merges them — one section "Last activity · Next relevant action". So A is internally inconsistent: SPEC.md separates, wireframe merges.
- **Recommended resolution:** adopt the wireframe's merge (it is A's own annotated build reference and reduces panel scroll), but keep A's hard requirement that Naya's suggestion stays labeled and bound to one action button (§1.10). This is layout taste within locked requirements — no director decision needed unless he wants the split.

### 2.6 Constellation edge encoding: specified vs undecided

- **A says:** R3a requires a legend naming every encoding; TASTE Q4 leaves the line-style→meaning mapping undecided.
- **Wireframe says:** legend shows "— active" and "- - pending" as the actual encodings, preempting Q4.
- **Recommended resolution:** the wireframe overstepped the spec — treat its encodings as illustrative fixtures (the file itself marks content FIXTURE, though not on the legend specifically). Keep Q4 open; add a fixture tag to the wireframe legend or strip the example encodings. [NEEDS DIRECTOR TASTE] stands for the real mapping.

### 2.7 Internal A contradiction: identity type badge "System" with no tab and no definition

- **A says:** R3b §1 type badges include "System" alongside Person/Naya/Organization/Space; canonical node types (§(a)3) include "system-door nodes".
- **A also says:** no "Systems" tab (see §2.2), and nothing defines what a System connection is or which runtime owns it.
- **Recommended resolution:** not a freeze-blocker if scoped: lock "System" badge as *display-only for system-door nodes already in the governed graph*, with retrieval scope defined by the active tab's runtime query. If a System entity needs its own browsing scope, that is [NEEDS DIRECTOR TASTE].

### 2.8 Vague / untestable predicates inside A (adversarial findings)

- **Predicate 8:** "a fixture cannot improve the room's score." There is no scoring mechanism defined anywhere in either spec — "the room's score" is undefined, so this predicate is not testable. Rewrite or drop: e.g. "EMPTY/ERROR/OFFLINE states render from real runtime state; no fixture content is reachable in production data paths" (this restates projection contract §11, Sample Data Law, which *is* grounding).
- **Predicate 1:** "Every displayed connection shows its canonical relationship ID … without opening a second screen." Testable as written, but the wireframe shows nodes as "P1/N1/O1/S1" with no IDs rendered — the wireframe does not demonstrate the predicate. Either the wireframe must show ID affordances (e.g. truncated ID under node labels) or the predicate must define *where* the ID surfaces (list rows show it; graph nodes show it on hover/focus). Currently unverifiable against the wireframe.
- **Predicate 9** (reload preserves tab/selection/Space scope): legitimate, and NOT a No-Hub-Capture violation — persisting UI scope is display state, explicitly allowed ("manage display/preferences", projection contract §10). Confirming so this isn't misread later.

### 2.9 B's blueprint violates its own standard (structural, adversarial finding)

B claims to follow `ROOM-BLUEPRINT-STANDARD-V1`, which requires 15 sections. B ships ~9 and is missing: **States** (no loading/empty/ready/blocked/unauthorized/not-verified/verified/error/offline/unknown enumeration), **Cross-room handoffs** (has "open Mail/Space" as controls but no handoff section with object-identity rules), **Naya behavior**, **Accessibility**, **Visual law** (no theme, tokens, density), and **Acceptance journey** (has "Proof" but no click-by-click journey). Per the standard's own gate — "No room is implementation-ready until its blueprint is complete enough that a cold builder can reproduce the intended interface" — B as written is not implementation-ready. This is not a disagreement with A; it is B failing B's own cited bar.

---

## 3. GAPS

Asymmetries verified by reading both files (note: the task's example was inverted — in fact **A** holds the predicates/inventory/anti-patterns and **B** holds the first-3-seconds entry):

**Present in A, missing in B:**
1. **Acceptance predicates** — A's 11 predicates (§d); B has only a one-line "Proof".
2. **Component inventory** — A's 12 components with token bindings; B names none.
3. **Contract header** — A's 10 fields (human job, kernel responsibilities, canonical object, runtime owner, allowed actions, authority boundary, truth states, handoffs, forbidden substitutes, predicates); B has no contract block.
4. **Exact control labels and placement** — A's R1–R5 with exact strings ("List view", "Re-center", "Adjust sharing…", "⋯"); B lists control verbs without labels or placement.
5. **Requests view** — A's R4 (requester/type/date/scope rows, Accept-with-scope-confirmation, Decline, accepted requests move to category tabs). B has **no pending-request surface at all** despite its own tab line implying tabs exist. This is B's largest functional gap.
6. **Anti-patterns** — A's six forbidden substitutes; B has two "do not" lines.
7. **Legend mechanism** — A requires a complete encoding legend; B doesn't mention one.
8. **Truth-state machine wording** — A's 11 states with machine/human/visual/action/evidence per state (functional contract §6); B's standard requires a States section B didn't write.
9. **Reload-scope persistence** — A's predicate 9; B silent.
10. **Wireframe** — A ships an annotated grayscale wireframe with all content marked FIXTURE (projection contract §11, Sample Data Law, honored explicitly in the note-bar); B ships no visual reference.

**Present in B, missing in A:**
1. **First-3-seconds entry** — B: "connection summary; meaningful relationships; one selected relationship detail." A never states the entry state; R1–R3 imply it. (Structural gap in A against the blueprint standard §2.)
2. **"Why it matters" framing** — B's panel leads with *why* the relationship matters; A's panel is record-first (Identity → Relationship → …) with Naya's read at §6. Same ingredients, different hierarchy. B's ordering better serves the human job; worth adopting.
3. **Global search in composition** — B's desktop composition opens with `[GLOBAL SEARCH]`; A's R1–R5 have no search control. Either B invented a room-level search or A omitted one. Functional contract §3: "Search/filter controls appear only where they materially reduce burden" — for a constellation of potentially hundreds of nodes, search materially reduces burden, so this omission leans toward a real gap in A. Recommend adding search to A (scoped to the active tab's retrieval scope), or explicitly ruling it out with a reason.
4. **"Systems" as a browsable concept** — B's tab line (though ungrounded, §2.2).

**No-Hub-Capture audit (checked both sides adversarially):** no silent violations found. A's `INVITE_CONNECT` allowed action and "sharing editor" are the two mutation-adjacent surfaces; both are defensible only as **write-through to the identity/consent runtime via the Hub runtime adapter** ("manage connection/consent settings where governed", projection contract §10). A should state the write-through explicitly — currently §(a)4 says the room "projects" and the forbidden list bans a divergent local store, but the *write path* for invite/adjust/disconnect is never named. Recommend one sentence: "All mutations (invite, adjust sharing, disconnect) execute against the identity + consent runtime through the shared Hub runtime adapter; the room holds no pending-write local state beyond the confirmation dialog." Without that sentence a builder could reasonably invent a Hub-side outbox — which is exactly what the No-Hub-Capture law forbids.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both sides, deduplicated (B flags none explicitly; all six are A's):

1. [NEEDS DIRECTOR TASTE] **Invite/discovery source.** What is the legitimate discovery/invite source for "Invite / connect"? Which identity directory backs it, and what does an invite grant before acceptance? (A Q1)
2. [NEEDS DIRECTOR TASTE] **Disconnect ritual + post-revocation retention.** Two-step vs typed confirm for "Disconnect…"? After revocation, is already-projected shared intelligence retained, sealed, or withdrawn? (A Q2 — note the second half touches the governed revocation contract, projection contract §6 item 6)
3. [NEEDS DIRECTOR TASTE] **Message's exact Mail surface.** Destination locked to Mail (§2.3); open: compose vs existing thread. (Narrowed from A Q3)
4. [NEEDS DIRECTOR TASTE] **Constellation edge encoding mapping.** Which line styles map to which relationship types/states? Legend mechanism locked; values open. (A Q4; wireframe's "active/pending" example encodings are fixtures, §2.6)
5. [NEEDS DIRECTOR TASTE] **Organizations and Spaces as constellation nodes vs list-only.** (A Q5)
6. [NEEDS DIRECTOR TASTE] **Consent granularity for viewing another person's connection metadata** — their other connections, their activity — where is the line? (A Q6; sharpens B's "do not expose private relationship metadata")
7. [NEEDS DIRECTOR TASTE] **Micro-label:** "Open in Ledger" (A) vs "Evidence" (B) for the proof action. (from §2.4)

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION** — not ready to freeze. Blocking items by name:

1. **Signature instrument naming + prominence** (§2.1) — "Relationship Constellation" vs "Relationship Inspector / graph supporting". Structural: determines what the room *is*. Recommended synthesis is given; needs lane agreement or director call.
2. **Tab taxonomy** (§2.2) — A's five tabs vs B's "People | Systems | All". Structural: determines navigation and retrieval scopes. Recommended: A's five.
3. **B's missing Requests surface** (§3.5) — B defines no pending-request handling; A's R4 is uncontested but unreconciled. Either B adopts R4 or the lanes agree requests live elsewhere.
4. **B's blueprint-standard non-compliance** (§2.9) — missing States, Handoffs, Naya behavior, Accessibility, Visual law, Acceptance journey sections. B cannot be called blueprint-complete until these exist or are explicitly delegated to A's spec.
5. **Message destination self-contradiction in A** (§2.3) — A's handoff field vs A's taste Q3. One-line fix (lock Mail, narrow Q3), but it must be made.
6. **No-Hub-Capture write-path sentence** (§3, audit) — invite/adjust/disconnect must be explicitly write-through the runtime adapter. One sentence; blocks any builder handoff.
7. **Untestable predicate 8 + wireframe-undemonstrated predicate 1** (§2.8) — acceptance criteria must be executable by an independent reviewer (functional contract §9 item 13). Rewrite or drop.

Non-blocking (taste, can freeze with [NEEDS DIRECTOR TASTE] tags intact): items 1–7 in §4.

**Path to READY:** resolve blockers 1–2 (one decision each, recommendations supplied with grounding), B adopts A's R4 or proposes its replacement (blocker 3), B completes or formally delegates its six missing standard sections (blocker 4), and A applies the three surgical fixes (blockers 5–7). Estimated: a single lane-to-lane pass, no new research required — every blocker has a recommended resolution cited to grounding above.
