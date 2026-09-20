# 08 — SMART FEED / INTELLIGENT FEED — LOCKED PRODUCT SPECIFICATION

**Project:** NayaNET Intelligent Hub — 2026-09-09
**Status:** DESIGN + FUNCTIONAL CONTRACT — NEW BUILD
**Reference only:** `2026 09 08 452 NayaNET Hub.html`

> The reference HTML is frozen evidence. It is NOT the new source and must NOT be edited to implement this specification.

## 1. PURPOSE

The Smart Feed / Intelligent Feed is the primary intelligence surface of the Hub.

It is not a generic social feed, dashboard, card wall, or second memory database.

Its job is:

**CAPTURE → DISTILL → ORGANIZE → REMEMBER → FIND → COMPOUND**

The feed is the visible projection of canonical intelligence events. Smart Notes are the durable event record. The feed makes those events understandable, navigable, searchable, and useful now.

## 2. THREE FEED LAYERS

### A. PERSONAL INTELLIGENCE
The user's private intelligence stream.

Shows:
- current-state intelligence
- personal Smart Notes
- Naya interpretations when genuinely generated
- machine evidence
- lessons and next actions
- personal activity and progress

Privacy: private by default.

### B. COLLECTIVE INTELLIGENCE
A consent-controlled view of intelligence intentionally contributed to the collective layer.

Shows:
- de-identified insights
- patterns
- shared lessons
- collective wisdom
- contribution provenance/status

It MUST NOT expose raw private Smart Notes merely because they exist in the personal feed.

### C. ACTIVITY FEED
A chronological operational stream showing meaningful activity/events.

It answers:
- What happened?
- When?
- What changed?
- What was created?
- What was verified?
- What is pending?
- What needs attention?

Activity is evidence-oriented; Personal/Collective Intelligence is meaning-oriented. They share canonical event identity rather than maintaining duplicate event stores.

## 3. CURRENT-STATE DOCTRINE

The feed follows:

**CURRENT STATE FIRST → RELEVANT HISTORY SECOND**

Every important current-state presentation should make it easy to answer:

1. Where are we?
2. What matters now?
3. What changed?
4. What did we learn?
5. What is verified?
6. What is not verified?
7. What is protected?
8. What remains unresolved?
9. What happens next?

Canonical narrative:

**WHAT CHANGED → WHAT MATTERS → WHAT WAS LEARNED → WHAT IS VERIFIED → WHAT REMAINS → WHAT HAPPENS NEXT.**

## 4. INTELLIGENT BLOCK = ONE EVENT

One Intelligent Block represents one canonical intelligence event.

It has one stable identity and multiple perspectives. Perspectives are not separate events.

Minimum conceptual model:

```text
IntelligentBlock
├── identity
├── title
├── type
├── timestamps
├── source / provenance
├── privacy / visibility
├── verification state
├── WISDOM
├── HUMAN
├── CHILD
├── GRANDMA
├── NAYA
├── MACHINE
├── WEAVER
├── LESSON
├── MEANING
├── ACTION
├── tags
├── engagement
└── retrieval metadata
```

## 5. THE VISUAL INTELLIGENCE SEQUENCE

**WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION**

### WISDOM — the core
What is the distilled intelligence worth seeing first?

Visual role: strongest conceptual anchor. It should feel like the intelligence has crystallized.

### HUMAN — the source
What did the person actually experience, think, decide, notice, question, learn, win, lose, or want to remember?

Human text must never be silently rewritten by the system.

### CHILD — first-principles curiosity
What would a curious child notice? What simple question exposes the real issue? What assumption should be questioned?

Purpose: simplify, reveal, and challenge.

### GRANDMA — lived wisdom
What does experience, common sense, humanity, and long-range perspective say?

Purpose: practical wisdom and human meaning.

### NAYA — intelligent interpretation
Naya's actual reasoning, synthesis, questions, recommendations, and pattern recognition.

Rule: never fabricate a Naya response. If the service is unavailable, show an explicit pending/unavailable state.

### MACHINE — evidence
Machine-observable facts:
- event ID
- timestamp
- source
- system state
- verification
- receipts
- measurements
- code/runtime evidence where appropriate

Machine evidence is not allowed to masquerade as semantic interpretation.

### WEAVER — synthesis climax
Weaver connects the perspectives into one coherent understanding.

It answers:
- What do all perspectives collectively reveal?
- What is the strongest synthesis?
- What relationship between facts and meaning matters?

Weaver is visually and semantically the climax of the block.

### LESSON — retained intelligence
What should be remembered?

### MEANING — significance
Why does this matter?

### ACTION — next move
What should happen next?

Action must be concrete where possible.

## 6. BLOCK VISUAL CONTRACT

The block must feel **elevated**, dimensional, tactile, and exceptionally easy to read.

It should feel closer to an intelligent object than a flat card.

### Surface
- obsidian/near-black foundation
- layered depth
- subtle radial light
- thin luminous perimeter
- restrained internal highlights
- deep but controlled shadow
- no white SaaS-card appearance
- no excessive glassmorphism

### Elevation
Each major perspective is visually lifted from the parent surface through:
- depth hierarchy
- shadow separation
- edge highlight
- controlled glow
- spacing
- tonal contrast

Do not create nine unrelated cards. The layers must visually belong to one object.

### Intelligence spine
A luminous vertical intelligence spine should provide continuity through the object.

Color progression follows the established matrix rather than arbitrary rainbow decoration. Purple/magenta carries intelligence emphasis; sapphire/blue supports machine/source context; green supports verified/good states; gold marks significance, evidence, caution, or culmination.

### Icons
Icons must be:
- immediately understandable
- visually beautiful
- consistent in geometry
- accessible with text labels/tooltips where needed
- semantic, not decorative noise

## 7. READABILITY CONTRACT

The user should understand a block in layers:

**5-second scan → 20-second understanding → deep inspection**

### Scan
- Wisdom headline
- event type
- status
- time/source
- strongest action

### Understand
- Human
- Naya
- Machine
- Weaver

### Deep inspect
- Child
- Grandma
- provenance
- verification
- lesson
- meaning
- action
- engagement/organization

Long content must remain comfortable to read. No microscopic body copy merely to fit more information.

## 8. BOARD CONTROLS

Controls may include:
- Favorite
- Save
- Like / Love where enabled
- Rank
- Comment
- Share
- Add to List
- Add to Group
- Expand / collapse perspective
- Open source event
- Ask Naya about this

Every control requires a documented state transition and truthful feedback. No decorative controls.

## 9. FEED FILTERS

Filters operate over canonical intelligence, not duplicate UI state.

Required dimensions may include:
- All
- Personal
- Collective
- Activity
- event type
- time
- favorites
- lists/groups
- verified/pending

Exact final taxonomy is a product decision to be locked before implementation. Existing reference labels are evidence, not permission to invent a new taxonomy.

## 10. SEARCH RELATIONSHIP

Search queries the canonical intelligence index/store.

A result must retain:
- event ID
- why it matched
- source
- visibility
- verification
- destination/open behavior

Opening a result opens the canonical event/block. Search must never create a second copy of the intelligence.

## 11. SMART NOTE RELATIONSHIP

```text
Human input
   ↓
Canonical Smart Note / Note Event
   ↓
Persist
   ↓
Naya enrichment (if connected)
   ↓
Machine evidence / receipt
   ↓
Intelligent Block projection
   ↓
Search + Daily Intelligence + Learning
   ↓
Lesson / Meaning / Action
   ↓
Compounding Intelligence
```

## 12. COLLECTIVE RELATIONSHIP

```text
PRIVATE EVENT
   ↓
VALUE EXTRACTION
   ↓
DE-IDENTIFICATION
   ↓
USER CONSENT
   ↓
COLLECTIVE PROJECTION
```

The user remains in control of the boundary.

## 13. EMPTY / PENDING / ERROR STATES

Never show a blank hole or fake activity.

### Empty
Explain what the surface is for and give the next useful action.

### Pending
Show exactly what is waiting and why.

### Blocked
Explain the missing capability and provide a useful alternative route where possible.

### Error
State what failed, preserve user work, and offer retry/recovery.

## 14. RESPONSIVE BEHAVIOR

### Desktop
- full-width intelligence workspace
- left navigation only
- no right Hub sidebar
- large block composition
- comfortable reading width

### Tablet
- preserve hierarchy
- reduce ornamental spacing before reducing readability
- collapse secondary controls into menus when needed

### Mobile
- no persistent left sidebar
- mobile navigation control/bottom navigation
- one-column intelligence object
- perspectives remain stacked and readable
- controls become compact but accessible
- sticky bars must never cover content
- touch targets should be comfortably tappable

## 15. PERFORMANCE / ENGINEERING LAW

The feed must be rendered from state, not repeatedly repaired after rendering.

Forbidden architecture:

```text
renderer A
 + renderer B
 + overlay C
 + MutationObserver
 + interval
 + animation-frame repair loop
```

Required architecture:

```text
Canonical Event Store
       ↓
Selectors / Feed Query
       ↓
One Feed State
       ↓
One Intelligent Block Renderer
       ↓
DOM
```

## 16. DEFINITION OF DONE

The Smart Feed is complete only when:

- Personal Intelligence works.
- Collective Intelligence works truthfully.
- Activity Feed works truthfully.
- one event = one block identity.
- every perspective has a defined purpose.
- every perspective has defined visual treatment.
- blocks are dimensional/elevated and exceptionally readable.
- search opens canonical events.
- filters operate on canonical state.
- Smart Notes flow into the feed.
- Naya output is real or explicitly pending.
- machine evidence is distinguishable from interpretation.
- Weaver produces genuine synthesis when available.
- Lesson/Meaning/Action compound forward.
- no duplicate renderer exists.
- no debug/code artifacts appear.
- no fake data appears.
- desktop and mobile are intentionally designed.
- privacy state is visible and truthful.
