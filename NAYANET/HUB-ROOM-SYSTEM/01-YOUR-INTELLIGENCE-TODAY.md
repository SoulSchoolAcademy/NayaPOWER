# 01 — Your Intelligence Today

**Contract class:** Product + UX + Intelligence  
**Room ID:** `INTELLIGENCE-TODAY`  
**Parent:** NayaNET → NayaPOWER → NAYANET → HUB → HUB-ROOM-SYSTEM  
**Lifecycle:** SPECIFIED (contract deepened 2026-09-23)  
**Implementation rule:** Do not code against memory or visual taste alone. Code against this contract plus current source/evidence.

---

## 1. Product purpose

**Your Intelligence Today** is the person's daily intelligence cockpit.

It is not a dashboard whose job is to make activity look impressive. Its job is to help a human understand the state of their intelligence **today** and move intelligently from awareness to action.

The room should help answer:

1. What happened?
2. What did I create or capture?
3. What did I learn?
4. What changed?
5. What matters now?
6. What should I remember?
7. What am I missing?
8. What can I do about it?
9. What can Naya actually substantiate?

The room is a human-facing projection of NayaPOWER intelligence. It is not a second brain and not a second source of truth.

### Product promise

> **When I open Your Intelligence Today, I should understand my intelligence today faster and more clearly than I could by reconstructing it myself.**

The room earns permanence through usefulness, not visual novelty.

---

## 2. Value law

Every component must materially help the user do at least one of:

**CAPTURE · UNDERSTAND · REMEMBER · CONNECT · DECIDE · ACT · VERIFY**

If a component does none of these, it does not belong merely because it looks good.

The room should optimize:

**maximum real human value per screen area, interaction, second, and piece of attention.**

Beauty supports comprehension and attachment; it must never substitute for utility or truth.

---

## 3. Relationship to the Hub

This room is rendered **inside the existing Hub middle workspace**.

### Must preserve
- Canonical Hub shell.
- Existing identity/authentication behavior.
- Existing search/header behavior.
- Existing runtime boundary.
- Existing privacy/governance rules.
- Existing navigation.
- Previously proven/frozen rooms.

### Must not introduce
- A second page.
- A second application shell.
- A competing navigation system.
- A permanent full-height right rail.
- A second source of truth.
- Browser-local fabricated intelligence.

### Workspace rule

The room should use the available middle workspace beneath the persistent search/header region. The compact Naya identity/assistant block remains part of the Hub shell; reclaiming or redesigning shell-level right-rail space is a separate bounded task.

---

## 4. Core information architecture

The room follows this human journey:

**ORIENT → SEE → UNDERSTAND → PRIORITIZE → REMEMBER → QUESTION → ACT → VERIFY**

### Layer A — Orient

#### Room Header
Display:
- Your Intelligence Today
- Current daily date/boundary
- One concise statement of the room's purpose
- Compact truth/retrieval state

Value:
- Immediately tells the human where they are and whether the information is live, partial, unavailable, or otherwise constrained.

Do not use decorative status badges whose meaning cannot be explained.

---

### Layer B — See

#### Today Pulse

A concise evidence-backed view of the day's intelligence state.

Candidate dimensions:
- Intelligence captured
- Meaningful changes
- Learning
- Decisions
- Activity

These are **not mandatory counters**. A dimension appears only when the runtime can substantiate it.

Each value has an explicit provenance path internally.

Rules:
- Observed zero may display as zero.
- Unknown must display as unknown.
- Unavailable must display as unavailable.
- Never convert missing data to zero.
- Never infer a metric from UI card count unless the underlying contract says the count is authoritative.
- Never generate a number merely to make the interface feel populated.

The pulse should prioritize meaning over quantity.

---

### Layer C — Understand

#### What Changed?

This is a first-class intelligence function, not a recent-items list.

Where the runtime supports comparison, compare today's intelligence against the previous daily boundary and surface **meaningful change**.

A change may include:
- New intelligence.
- Changed understanding/state.
- New decision.
- Corrected information.
- Newly learned information.
- Newly connected intelligence.
- Newly blocked/unblocked state.
- Newly available or unavailable capability.
- Significant activity affecting the user's intelligence.

Each change should expose, where available:
- What changed.
- When.
- Change type.
- Source.
- Provenance/evidence.
- Privacy scope.
- Why it is being surfaced, when that reasoning is evidence-grounded.

Do not call something “changed” merely because it was viewed or re-rendered.

If comparison evidence is unavailable, say so rather than pretending a comparison occurred.

---

### Layer D — Understand the meaning of the day

#### What Did I Learn?

Learning is more than information received.

Where evidence permits, distinguish:
- **INFORMATION** — something captured or encountered.
- **UNDERSTANDING** — a relationship or meaning became clearer.
- **CHANGE** — the known state changed.
- **DECISION** — a conclusion or commitment was made.
- **KNOWLEDGE** — information/understanding that has become durable enough to retain.

The UI should not falsely label an ordinary note as “learning.”

Each learning item should answer:
- What was learned?
- From what source/evidence?
- When?
- Is it durable knowledge, a current understanding, or still uncertain?

---

### Layer E — Prioritize

#### What Matters Now?

Surface evidence-backed items that may require attention, such as:
- Unresolved questions.
- Blocked work.
- Important discoveries.
- Decisions with consequences.
- Opportunities.
- Commitments.
- Items awaiting human action.
- Material uncertainty.
- New information that changes an existing direction.

Every surfaced item should have a reason.

Preferred pattern:

**MATTERS → BECAUSE → POSSIBLE ACTION**

Do not manufacture urgency. “Important” is a claim that requires a defensible basis.

---

### Layer F — Remember

#### What Should I Remember?

This is where the Intelligence Diary becomes human-centered.

The room should help the person retain meaningful intelligence from the day:
- A lesson.
- A decision.
- A discovery.
- A correction.
- A personal insight.
- A commitment.
- Something created or given.
- Something that happened because they acted.

The feature may recommend durable retention, but saving/committing durable memory must respect the user's authority and the governing Smart Note/memory contracts.

The room should distinguish:
- already retained;
- suggested for retention;
- temporary/current;
- uncertain.

---

### Layer G — Question

#### What Am I Missing?

Expose the edges of knowledge instead of hiding them.

Useful states:
- **KNOWN**
- **CHANGED**
- **UNCERTAIN**
- **MISSING**
- **BLOCKED**
- **NOT VERIFIED**

Examples of useful output:
- A capability is implemented but not yet proven.
- A source exists but current retrieval has not been verified.
- A decision depends on an unanswered question.
- A connection is configured but authorization is unknown.

This is especially important because NayaNET's governing truth is:

**Unknown ≠ success.**

The room must make uncertainty legible without turning the UI into an error console.

---

### Layer H — Interpret

#### Naya's View

Naya may provide a concise synthesis of the available evidence:

**What appears important · What changed in significance · What remains uncertain · What deserves attention**

Naya's interpretation must remain distinguishable from observed facts.

Every synthesis should be traceable to underlying intelligence when the system supports provenance.

Do not present model-generated interpretation as if it were an observed event.

Do not invent causality.

Do not claim confidence that the evidence does not support.

---

### Layer I — Act

#### High-value actions

The first actions should map directly to the room's job:

1. **Capture Intelligence** — create/capture a Smart Note without leaving the Hub.
2. **Ask Naya** — continue reasoning from the current intelligence context.
3. **View Evidence** — inspect the source/provenance behind a claim.
4. **Open Personal** — inspect the private intelligence projection.
5. **Open Collective** — inspect consented collective intelligence.
6. **Open Activity** — inspect actual activity events.

Actions should be physically obvious, tactile, and fast.

No action should exist solely because other software has buttons.

---

## 5. Intelligence stream modes

The existing Hub contract establishes:

- **Collective** = canonical default.
- **Personal** = private intelligence projection.
- **Activity** = actual activity projection.

Switching modes must change the underlying projected content, not merely a label or color.

### Collective
Show only intelligence the current authority permits the user to see as collective/shared.

### Personal
Show the user's private intelligence within the governing privacy/authority boundary.

### Activity
Show actual recorded events relevant to the current surface.

Activity must never be simulated to make the room appear alive.

### Mode behavior
- Collective is the default.
- Switching is in-place.
- The selected mode may persist where appropriate.
- Returning to the room must produce a coherent state.
- If a mode has no data, explain why and provide the most useful next action.
- Do not leak private content into Collective.
- Do not disguise unavailable Activity as an empty successful state.

**Important:** An “EVERYTHING” mode is not part of this contract unless explicitly added through a future contract revision. The current canonical modes remain Personal / Collective / Activity.

---

## 6. Visual and interaction language

The room should feel like a **premium intelligence instrument**, not a generic SaaS analytics dashboard.

### Visual direction
- Deep black spatial foundation.
- White/high-contrast primary typography.
- Deep purple/indigo used for intelligence, depth, focus, and interaction.
- Restrained green only where it communicates verified/healthy state.
- No light-purple/pink body text.
- No yellow/gold accent system.
- Large readable typography.
- Strong hierarchy.
- Generous spacing.
- Physical 3D/tactile controls where useful.
- Depth/glow used to establish hierarchy, not decorate empty space.
- Meaningful motion only.

### Density rule
Prefer a small number of highly useful information objects over a wall of tiny cards.

### Typography rule
Important intelligence must be readable at a glance. The current Hub's existing visual language is the foundation; do not solve the room by shrinking content to fit.

### Responsive rule
The room must remain useful when the middle workspace narrows. Priority order should be preserved rather than simply scaling every element down.

---

## 7. Data and provenance contract

The room is a projection layer.

Canonical path:

**SOURCE → RUNTIME/PERSISTENCE → RETRIEVAL → INTELLIGENCE PROJECTION → HUB**

The room may transform or format data for presentation, but it may not redefine canonical truth.

### Evidence levels

Where the runtime provides sufficient information, distinguish:
- **Observed** — directly returned from an authoritative source.
- **Derived** — computed from observed data using a defined rule.
- **Interpreted** — Naya/model synthesis over observed/derived information.
- **Unknown** — required information is not available.
- **Unavailable** — required capability/runtime path cannot currently provide it.
- **Not verified** — something exists or is configured, but proof is incomplete.

These labels need not all appear as verbose text; the underlying state must remain explicit.

### Privacy
- Personal intelligence remains within the authorized private boundary.
- Collective intelligence requires consent/authorized sharing.
- Activity is visible only according to the governing authority.
- Evidence views must not bypass privacy rules.
- A user's private content must never be exposed merely because it influenced a synthesis.

---

## 8. State model

Every major room region must have truthful behavior for:

### LOADING
Preserve hierarchy while showing that retrieval is in progress.

### READY
Show observed/derived intelligence with appropriate provenance.

### EMPTY
Explain what is genuinely absent and offer a useful capture/exploration action.

### PARTIAL
Show available intelligence and explicitly identify the missing portion.

### UNAVAILABLE
Identify the unavailable capability/boundary without breaking the Hub.

### ERROR
Expose the actual safe error class and preserve the rest of the interface.

### PRIVATE
Respect authorization and make privacy state clear without exposing content.

### NOT VERIFIED
Never upgrade an unproven condition to healthy merely because a configuration exists.

---

## 9. What the room is NOT

It is not:
- a generic KPI dashboard;
- a chronological dump of notes;
- a social feed;
- an AI chat screen with decorative cards;
- an activity log pretending to be intelligence;
- a replacement for Smart Ledger;
- a replacement for Reports;
- a replacement for Intelligent Library;
- a second Hub;
- a source of truth;
- a place to hide uncertainty.

### Boundary against other rooms

| Room | Primary question |
|---|---|
| Your Intelligence Today | **What is important about my intelligence today?** |
| Your Reports | What does my intelligence reveal over time? |
| Intelligent Library | What intelligence do I have? |
| Smart Connect | What systems can my intelligence connect to? |
| Smart Ledger | What can the system prove happened? |
| Your Connections | What is my intelligence connected to? |
| Smart Lists | What intelligence should become organized action? |
| Smart Mail | What intelligence exists in communications? |
| Smart Spaces | What intelligence belongs to this context? |
| Settings | How do I control my intelligence environment? |

This boundary prevents room duplication and feature drift.

---

## 10. Acceptance contract

Room 01 may move from **SPECIFIED** to **IMPLEMENTED** only when the implementation visibly and structurally reflects this contract.

It may move to **PROVEN** only with evidence that:

### Shell
- Opens from the sidebar inside the existing Hub shell.
- Does not create a second page or shell.
- Uses the available middle workspace appropriately.
- Does not require a permanent full-height right rail.
- Existing search/header behavior remains coherent.

### Product
- Answers the room's core daily-intelligence questions.
- Today Pulse uses real evidence.
- What Changed is based on actual comparison/change evidence where available.
- Learning is not conflated with raw note count.
- What Matters Now has evidence-grounded reasons.
- What Should I Remember respects memory authority.
- What Am I Missing exposes genuine uncertainty/gaps.
- Naya's View distinguishes interpretation from observation.

### Intelligence
- Collective is the canonical default.
- Personal, Collective, and Activity materially change the projected content when data exists.
- Activity is real events only.
- Unknown remains unknown.
- Privacy boundaries are preserved.
- Provenance is available where the runtime supports it.
- No fabricated metrics or events exist.

### Interaction
- High-value actions work in-place.
- Item detail/evidence follows existing Hub interaction patterns.
- Smart Note capture does not eject the user into a separate shell.
- Mode state behaves coherently across navigation/reload where intended.

### Regression
- Existing Hub navigation remains intact.
- Previously proven/frozen rooms remain intact.
- No unrelated shell redesign is bundled into Room 01.
- Source commit is identifiable.
- Proof run and/or artifact is identifiable.
- The final implementation can be reconstructed from this contract and repository evidence without relying on the original chat.

---

## 11. Implementation boundary

The implementation agent must:

1. Read `CURRENT-WORKING-MEMORY.md`.
2. Read `ROOM-REGISTRY.md`.
3. Read this contract.
4. Inspect the current canonical Hub source and existing `nayaIntelligenceWorkspace` implementation.
5. Identify what already exists versus what is missing.
6. Make the smallest causal implementation set that moves Room 01 toward this contract.
7. Avoid changing unrelated rooms.
8. Avoid shell-level right-rail redesign in the Room 01 change.
9. Run the relevant Hub/runtime/browser proof.
10. Record observed evidence.
11. Update working memory with durable discoveries/corrections.
12. Update the registry only from observed truth.

No “V2,” “V3,” or replacement Hub is permitted as a shortcut.

---

## 12. Freeze contract

Once Room 01 reaches **PROVEN → FROZEN**, this contract plus its proof become a durable regression boundary.

Later rooms may:
- reuse proven components;
- reuse shared data contracts;
- extend shared infrastructure safely;
- add navigation destinations.

Later rooms may not:
- silently remove Room 01 behavior;
- redefine Room 01's product job;
- replace its visual language without explicit contract change;
- weaken its privacy/evidence rules;
- cause its middle-workspace application to disappear.

A future change to Room 01 requires an explicit contract revision and a new proof cycle.

---

## 13. Design north star

**Your Intelligence Today should make the person feel that their intelligence has been seen, organized, understood, and made useful — without pretending to know what the system cannot prove.**

The room should leave the human with one clear outcome:

> **I understand what happened, what I learned, what changed, what matters, what I should remember, what I am missing, and what I can do next.**

That is the product.
