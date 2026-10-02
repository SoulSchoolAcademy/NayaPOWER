# 09 — SMART MAIL — RECONCILIATION

Independent review: `mail/SPEC.md` + `mail/wireframe.html` (lane A, "my lane", dir `mail/`) vs
`grounding/blueprints/09-smart-mail.md` (lane B, Naya 3's blueprint).
Grounding consulted: `INTELLIGENCE-PROJECTION-CONTRACT-V1.md` (projection contract),
`ROOM-FUNCTIONAL-CONTRACT-V1.md`, `1278-tokens.css`.
SHAWN'S LAW applied: "No blueprint, no building"; taste decided at blueprint stage, not build stage.

---

## 1. AGREEMENTS

Both specs lock these identically — a freeze can carry them as-is:

1. **Mode tabs (five of six labels).** A R2: "IMPORTANT · RESPOND · FOLLOW UP · DRAFTS · SENT · ALL". B desktop composition: `[ IMPORTANT | RESPOND | FOLLOW UP | DRAFTS | SENT ]`. The five named tabs match exactly.
2. **Real data only — no fake mailbox.** A: "never fabricate content to look populated"; "No row ever renders sample content." B: "Real connected mail/message adapter only." "Disconnected mailbox is a designed state, not fake sample mail."
3. **Control vocabulary.** B's controls (open, reply/draft, compose, archive, prioritize, follow-up, add to list/space, Ask Naya) are a strict subset of A's allowed actions (OPEN · REPLY (draft) · DRAFT_RESPONSE · COMPOSE · ARCHIVE · PRIORITIZE · FOLLOW_UP · ASK_NAYA · ADD_TO_LIST · LINK_TO_SPACE …). No control in B contradicts one in A.
4. **Smart Note = upstream handoff, never Hub capture.** B: "If user asks Naya to Smart Note a message, hand off upstream; no local canonical Smart Note creation." A field 9: "no Hub-local Smart Note creation (intent goes upstream through the governed pipeline)"; predicate 7 forbids minting IB identity or claiming persistence. Both are clean under the No-Hub-Capture law (projection contract §3).
5. **Send authority gate.** B: "Send only claims success when real send authority/runtime confirms it." A: `SendAuthorityBadge` "required/granted", Send disabled until authorization, explicit confirm (recipient + channel) even when granted. B states the principle; A states the mechanism. Compatible.
6. **Account/connection truth visible at entry.** B composition shows `[Smart Mail] [Account/connection truth]`. A R1 has "Account: <address/channel>" chip + truth-state badge. Both lock connection truth into the header.
7. **Derived ranking must show its basis.** A: "why it matters" chip with basis; predicate 3: "no ranking renders without one." B doesn't contradict it; its first-3-seconds "priority views" presuppose governed prioritization.
8. **Theme.** Both inherit mail's identity from `--accent-mail` (tokens are visual law; both lanes accept this).

---

## 2. CONTRADICTIONS

### C1. Signature instrument name — A says "Signal Console"; B says "Signal + Context Reader"
**Recommended resolution: adopt A's "Signal Console".** ROOM-FUNCTIONAL-CONTRACT-V1 §2's canonical instrument examples list "signal console" verbatim; B's "Signal + Context Reader" appears nowhere in grounding. Neither side's meaning differs — both describe signal list + contextual reading — so this is naming only, and the contract settles it.

### C2. Desktop layout — A: three columns (R3 signal list | R4 reader | R5 context panel); B: two columns (message list | selected message + context + related intelligence + suggested next action + draft/reply controls stacked in the right column)
**Recommended resolution: [NEEDS DIRECTOR TASTE].** Neither side's grounding wins. The functional contract says "Reuse components, not compositions" and "Do not force every room into the same layout" — composition is deliberately left to the room. A's version is fully specified (R1–R6, control labels exact); B's is a compositional sketch. This is a genuine product-shape decision and belongs to the director at blueprint stage (SHAWN'S LAW).

### C3. Sixth tab "ALL" — A has it ("ALL is the chronological inbox"); B's tab bar stops at SENT
**Recommended resolution: adopt A's six.** B's list is not an exclusion — nothing in B says ALL is forbidden — and A's acceptance predicate 2 names all six scopes with distinct runtime queries. The five-tab overlap (see Agreements §1) is intact; adding ALL is an addition, not a reversal.

### C4. Controls in A absent from B: OPEN_SENDER, VIEW_ACTIVITY_PROOF, SEND_IF_AUTHORIZED, CAPTURE_SMART_NOTE (intent), LINK_TO_SPACE
**Recommended resolution: adopt A's fuller set.** B's shorter list doesn't forbid these; A's predicate 8 requires the four cross-room handoffs to preserve canonical IDs, which grounding requires (functional contract §9 gate 7: "cross-room handoffs preserve object identity"). B has no handoffs section at all (see Gaps), so A is the only side with a handoff story. Note: B's flat "reply/draft" vs A's two actions "REPLY (draft)" + "DRAFT_RESPONSE" — A is internally redundant here (see C9/A-internal below); fold DRAFT_RESPONSE into REPLY (draft).

### C5. "Follow up" placement — A puts "Follow up" in the overflow "⋯"; B lists follow-up as a direct control
**Recommended resolution: [NEEDS DIRECTOR TASTE].** Functional contract §3 assigns overflow to "low-frequency operations," but neither spec evidences follow-up's actual frequency. This is downstream of A's open taste question 7 (what a follow-up *is*); placement follows mechanics, not the other way around.

### C6. Compose gating — B says "compose where connected"; A's Compose button is unguarded
**Recommended resolution: adopt B's guard into A.** A room with an unconnected door showing an enabled Compose would be a dead button, which the functional contract §3 ("No dead button") forbids. B's qualification is the safer, grounding-backed version; A's spec should add it.

### C7. "suggested next action" (B) vs "Potential response" (A) — B stacks a generic next-action section; A has specifically a response-direction section
**Recommended resolution: adopt A's "Potential response"** as the named section, with B's broader "suggested next action" surviving only if Naya's behavior section (which B lacks — see Gaps) defines non-response next actions. As written, B's generic section invites invented actions; A's is scoped and labeled "suggestion, not sent text."

### C8. Global search — B's composition opens with `[GLOBAL SEARCH]`; A has no global search in R1–R6
**Recommended resolution: not a true contradiction.** B's bar sits above the room composition and reads as Hub-global chrome, not room surface. A's regions are room-scoped; they don't contradict a global chrome row. Confirm in freeze notes that global search is out of room scope.

### C9 (A-INTERNAL). Wireframe heading "Capture" vs SPEC's "exact section headings" rule
A SPEC.md says R5 headings are "Exact" and names section 7 "Ask Naya to note this." A's own wireframe labels that section **"Capture"**. This is a lane-A self-contradiction. **Recommended resolution: the wireframe must change to "Ask Naya to note this."** Grounding wins decisively: projection contract §3 orders the "Capture Smart Note" control *removed from Hub product contracts*; a section heading literally named "Capture" revives the forbidden capture framing. No director taste needed — this is a compliance fix, and it blocks wireframe acceptance until corrected.

### C10 (A-INTERNAL). Wireframe "Important" as a response-state badge value
A SPEC.md limits the response-state badge to "Needs response" / "Waiting on someone" / "FYI". The wireframe's second thread row renders "Important" in that slot. **Recommended resolution: wireframe fix — "Important" is a why-matters concept, not a response-state value** (SPEC's own row structure keeps them distinct: WhyMattersChip vs ResponseStateBadge). Wireframe must pick one of the three locked values.

### C11 (A-INTERNAL). Tab↔group mapping is undefined
A R2 defines 6 tabs but the default view "groups by meaning" into 7 groups ("Needs response · Important · Waiting on someone · FYI / low urgency · Related to active Space · Sent · Drafts") that do not map 1:1 to tabs (e.g., which tab owns "Waiting on someone"? Is RESPOND ⊇ "Needs response"? Does IMPORTANT ⊇ "Important" + "Related to active Space"?). The wireframe repeats the ambiguity. **Recommended resolution: author fix before freeze** — A must state the group→tab membership rule. Not director taste; a spec-completeness defect.

### C12 (A-INTERNAL). Predicate 10 is not testable
"RUNTIME UNAVAILABLE … are real rendered states …; a fixture cannot improve the room's score." A score exists nowhere in the spec; "cannot improve the room's score" names no instrument, no measurement, no threshold. Predicates 1–9 are testable (distinct runtime queries, canonical-ID resolution, disabled-state rendering, persistence across reload). **Recommended resolution: rewrite predicate 10 mechanically** — e.g., "each truth state has a distinct rendered treatment with machine state, human wording, available actions, and a working Retry; the NO MAIL treatment renders with zero message rows." Vague predicates fail the evidence law; this one must be replaced, not waived.

### C13 (B-INTERNAL). "Data: Real connected mail/message adapter only" under-specified against B's own "compose where connected"
B never defines the disconnected compose treatment — if compose is "where connected," what does the disconnected state render for the Compose control? A has the truth-state framework (RUNTIME UNAVAILABLE etc.); B has only "Disconnected mailbox is a designed state." **Recommended resolution: fold A's truth-state set in; B's single line is insufficient** for a room whose signature instrument is a live signal console.

---

## 3. GAPS

Present in one side, missing in the other.

**Missing in B (Naya 3's blueprint) — despite the task's premise, B does NOT follow the full ROOM-BLUEPRINT-STANDARD-V1 section set:**
- **Handoffs.** No cross-room handoffs (Connections / Space / List / Ledger). A's field 8 + predicate 8 cover this; functional contract §9 gate 7 requires it. B cannot freeze without it.
- **Truthful states.** B has one line ("Disconnected mailbox is a designed state"). No truth-state inventory, machine states, human wording, or available-actions-per-state. A has the full set (R6 + field 7).
- **Naya behavior.** No "## Naya" section (peer blueprint 01-smart-feed.md has one). Naya appears only as the "Ask Naya" control and the smart-note handoff line. A's R5 sections 2–5 + "Potential response" carry this instead.
- **Anti-patterns.** No "## Do not" section (peers 01/02/07 have one). A's "Forbidden local substitutes" (field 9) is the equivalent.
- **Acceptance journey / predicates.** B has a 2-line "## Proof". A has 10 predicates.
- **Controls + placement.** B lists controls with no placement mapping; A's R1–R6 + exact control labels carry placement.
- **Accessibility, visual law, data contract detail.** Absent in B. A binds tokens explicitly ("no new tokens, no new components invented") and lists components with token references.

**Missing in A (my lane's spec):**
- **First-3-seconds entry.** B's "First 3 seconds" (mailbox truth state → priority views → first message needing attention) has no A counterpart. A's R1–R3 imply it but never lock the entry sequence. Fold B's entry into the freeze.
- **Composer surface contract detail.** B's desktop composition implies reply controls adjacent to the message; A's mobile line ("compose opens as full-screen sheet on mobile") is A's only compose-surface statement beyond R1. Minor.

**Structural asymmetry summary:** A is contract-heavy (acceptance predicates, component inventory, truth states, handoffs, open taste questions) and layout-fully-specified; B is entry-and-shape-heavy (first-3-seconds, composition sketch) but structurally incomplete against its own standard. The freeze must be composed, not chosen: A's contract sections + B's entry framing + the resolved layout.

---

## 4. TASTE QUESTIONS STILL OPEN

Union of both lanes, deduplicated. B flags none explicitly; A's seven carry, plus two surfaced by this reconciliation.

1. [NEEDS DIRECTOR TASTE] Consent model for projecting message content: whose messages may appear, redaction rules, who may see quoted text from other people? *(A Q1)*
2. [NEEDS DIRECTOR TASTE] Send authority granularity: per-message, per-thread, per-recipient, or standing grant — and what counts as "consequential"? *(A Q2)*
3. [NEEDS DIRECTOR TASTE] Mail vs messaging scope for V1: which doors (email only, or SMS/Messenger/other)? The Account chip assumes ≥1 bound door. *(A Q3)*
4. [NEEDS DIRECTOR TASTE] "Ask Naya to note this": confirmation UX, and where the resulting IB surfaces once the upstream pipeline completes? *(A Q4)*
5. [NEEDS DIRECTOR TASTE] Archive/delete semantics: does Archive act on the door or only the projection — and is there a Delete at all? *(A Q5)*
6. [NEEDS DIRECTOR TASTE] Theme: `--accent-mail: var(--blue)` (#55b9ee) vs functional spec's sapphire/cyan. Tokens are visual law so blue stands pending; note `--accent-library` also resolves to `--blue` — two rooms sharing one accent value deserves an explicit director look. *(A Q6, extended)*
7. [NEEDS DIRECTOR TASTE] Follow-up mechanics: timed reminder, FOLLOW UP lane, or List item — and who owns the reminder? *(A Q7; blocks C5 placement)*
8. [NEEDS DIRECTOR TASTE] Desktop layout: three-column R3|R4|R5 (A) vs stacked message+context right column (B)? *(C2 — the one layout decision SHAWN'S LAW puts at blueprint stage)*
9. Spec-internal, not director taste, but must be answered before freeze: the tab↔group membership rule (C11). Flagging here so it isn't lost.

---

## 5. FREEZE RECOMMENDATION

**NEEDS RESOLUTION** — do not freeze yet. Blocking items, by name:

1. **Layout decision (C2).** Three-column vs stacked composition is [NEEDS DIRECTOR TASTE]. This is the single biggest blocker: it changes every region boundary.
2. **Tab↔group mapping (C11).** Author fix required — the membership rule must be written into the spec; freeze is impossible while tab clicks have undefined group semantics.
3. **Predicate 10 rewrite (C12).** The untestable predicate must be replaced with a mechanical one; a spec with a slogan-predicate fails the evidence law.
4. **Wireframe "Capture" heading (C9).** Compliance fix: rename to "Ask Naya to note this" per the No-Hub-Capture law. Small, but it is a forbidden-framing violation in the lane's own artifact.
5. **B's missing structural sections.** Naya 3's blueprint cannot stand alone against its standard — handoffs, truthful states, Naya behavior, anti-patterns, acceptance journey must be added or formally adopted from A's spec before freeze.
6. **Open taste questions 1–8.** At minimum Q2 (send authority granularity) and Q3 (mail vs messaging scope) are load-bearing for the data contract and the SendAuthorityBadge mechanism; Q1 (consent model) gates whether any message content renders at all.

**Ready-now material (fold into the freeze once the above clear):** the eight agreements (§1); resolved adoptions — instrument name "Signal Console" (C1), sixth tab ALL (C3), A's control/handoff set (C4), B's "compose where connected" guard folded into A (C6), "Potential response" (C7), global search as Hub chrome (C8), wireframe "Important" badge fix (C10), disconnected-state treatment from B's "States" (C13), and B's first-3-seconds entry framing folded into A.
