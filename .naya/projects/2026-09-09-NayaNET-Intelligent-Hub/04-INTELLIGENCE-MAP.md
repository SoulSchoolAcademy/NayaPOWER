# 04 — Intelligence Map

## North Star

**INTELLIGENCE MADE VISIBLE.**

The Hub's job is:

**CAPTURE → DISTILL → ORGANIZE → REMEMBER → FIND → COMPOUND**

## 1. The canonical event model

One meaningful user event should remain one intelligence event.

### Human Note
What the person actually experienced, thought, decided, learned, noticed, questioned, won, failed, or wants to remember.

### Naya Note
Naya's interpretation, synthesis, explanation, recommendation, or pattern recognition. This must come from the actual production intelligence service when connected.

### Machine Note
System evidence: event ID, timestamp, source, type, privacy boundary, persistence state, verification/receipt state and other machine facts.

### Intelligent Feed
The current-state projection that keeps the event visible, ordered, searchable and available for compounding.

## 2. Canonical flow

```text
HUMAN EXPERIENCE
      ↓
CAPTURE
      ↓
SMART NOTE / NOTE EVENT
      ↓
PERSIST
      ↓
VALIDATE / VERIFY
      ↓
INTELLIGENT FEED PROJECTION
      ↓
SEARCH / RETRIEVAL
      ↓
NAYA SYNTHESIS
      ↓
DAILY INTELLIGENCE
      ↓
LEARNING / PATTERN
      ↓
RULE / PREFLIGHT / NEXT ACTION
      ↓
COMPOUNDING INTELLIGENCE
```

## 3. What the current static package actually does

### Human input
A user types into the Smart Note textarea.

### Classification
A simple client-side `typeOf()` function infers a category from keywords.

### Persistence
The note is assigned an ID and ISO timestamp and stored in `localStorage` under `nayanet_v7_live_notes`.

### Feed projection
The Home Feed reads that local note store and renders an Intelligent Block.

### Naya perspective
The current static implementation intentionally displays a pending-service message instead of pretending to have an AI-generated interpretation.

### Machine perspective
The block exposes event ID, type, timestamp, local-persisted status and private state.

### Search
The Intelligence Index reads the locally available blocks and ranks matches by title/text/tags, favorites and recency.

### Daily report
The Reports surface compresses source events locally into What Mattered / Learned / Carries Forward / Attention Next.

### Compounding
The interface communicates Day 1 → Day 2 → Day 7 → Day 30 → Day 365 → Lifetime, but a true longitudinal learning engine is not implemented by this static HTML alone.

## 4. Feed doctrine

The repository's canonical feed document explicitly states:

**CURRENT STATE FEED = INTELLIGENT FEED = SMART NOTE FEED**

The feed is a prioritized projection over the durable Note Event store. It should answer:

- Where are we?
- What matters now?
- What changed?
- What did we learn?
- What is verified?
- What is not verified?
- What is protected?
- What remains unresolved?
- What is the next best action?

The required current-state structure is:

**WHAT CHANGED → WHAT MATTERS → WHAT WAS LEARNED → WHAT IS VERIFIED → WHAT REMAINS → WHAT HAPPENS NEXT.**

## 5. Board architecture

The current feed renderer's intended board model is a vertical intelligence object.

### Required visual intelligence sequence

**WISDOM → HUMAN → CHILD → GRANDMA → NAYA → MACHINE → WEAVER → LESSON / MEANING / ACTION**

This sequence is the target conceptual model for the rebuild. The current static source demonstrates related Human/Naya/Machine/Feed perspectives, but the exact full multi-perspective board sequence must be implemented as a single canonical renderer rather than assembled through competing enhancement scripts.

### Board identity
Each block needs:
- stable event ID
- title
- type
- created timestamp
- source
- privacy/visibility
- human source
- Naya interpretation
- machine evidence
- synthesis/weaver state
- lesson/meaning/action carry-forward
- tags
- engagement state
- verification state

## 6. Intelligence state machine

```text
OBSERVED
  ↓
CAPTURED
  ↓
PERSISTED
  ↓
VERIFIED
  ↓
PROJECTED
  ↓
RETRIEVABLE
  ↓
SYNTHESIZED
  ↓
LEARNED
  ↓
COMPOUNDED
```

No state may be promoted merely because a source file exists.

## 7. Verification state machine

```text
DOCUMENTED
→ SPECIFIED
→ IMPLEMENTED
→ TESTED
→ VERIFIED
→ DEPLOYED
→ LIVE-VERIFIED
→ PRODUCTION-PROVEN
```

The current static Hub is strongest in documented/implemented/local-persisted behavior. Production Naya synthesis, mail delivery, people discovery and server-backed public intelligence are not proven by this source alone.

## 8. Search intelligence

### Current index inputs
- title
- summary/body
- human perspective
- Naya perspective
- machine perspective
- tags
- favorite/collective state
- update time

### Current search behavior
- case-insensitive term matching
- title receives higher score
- body/tag match receives smaller score
- favorite and collective state can add score
- recency contributes score
- top results are surfaced

### Rebuild requirement
Search should become a first-class retrieval layer over the canonical event store, not a separate duplicate database.

## 9. Smart Notes → Feed contract

When a Smart Note is created:

1. Preserve original human text unchanged.
2. Create a canonical event identity.
3. Persist timestamp/type/source/privacy.
4. Generate or attach Naya interpretation only when real Naya processing occurs.
5. Attach machine evidence and verification state.
6. Project into the current-state feed.
7. Make it searchable.
8. Make it eligible for Daily Intelligence.
9. Record the next useful action where one exists.
10. Preserve historical retrieval without burying current state.

## 10. Collective intelligence contract

Private intelligence should move through:

**PRIVATE NOTE → PRIVATE REPORT → VALUE EXTRACTION → DE-IDENTIFICATION → EXPLICIT CONSENT → COLLECTIVE INTELLIGENCE**

No raw private event should become collective/public merely because it appears in a feed.

## 11. Naya connection contract

### Current source
- Naya visual identity is present.
- Ask Naya UI is present.
- Local retrieval/search can operate.

### Not currently connected
- authenticated Superbrain reasoning endpoint
- production Naya synthesis endpoint
- durable server-backed user intelligence service
- production voice endpoint

### Required future contract

```text
USER EVENT
→ NAYA POWER / SUPERSBRAIN
→ NAYA NOTE
→ MACHINE RECEIPT
→ SMART NOTE EVENT
→ INTELLIGENT FEED
→ RETRIEVAL
→ COMPOUNDING
```

The Naya service must return a machine-verifiable event/receipt or equivalent evidence so the Hub can distinguish real AI processing from local presentation.

## 12. Daily Intelligence contract

Daily Intelligence is not a generic dashboard.

It is a compression layer over source-backed events:

- WHAT MATTERED
- WHAT WAS LEARNED
- WHAT CARRIES FORWARD
- WHAT DESERVES ATTENTION NEXT

It should never invent an event to make the report look full.

## 13. Learning / adaptive learning

The existing interface contains an Adaptive Learning concept and pre-flight framing:

**Learning Event → Lesson → Rule → Preflight**

A future production implementation should persist the relationship between the source event and the learned rule so Naya can use it before the next consequential action.

## 14. Intelligence board interaction contract

Every board should make it possible to:

- understand the event without opening another system
- inspect perspective layers
- see verification state
- save/favorite
- rank
- comment
- share
- organize into a list/group
- search/retrieve later
- see what the event means now
- see what action or lesson carries forward

## 15. What must never happen

- Naya text fabricated as if generated remotely.
- Machine receipt fabricated.
- Local persistence described as server persistence.
- Demo activity described as real activity.
- Collective sharing silently enabled.
- Search result treated as semantic Naya reasoning.
- A feed becoming a second memory authority.
- Historical artifacts silently replacing current source authority.
