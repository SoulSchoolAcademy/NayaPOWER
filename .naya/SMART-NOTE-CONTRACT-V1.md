# 🔱 NayaPOWER — SMART NOTE / INTELLIGENT BLOCK CONTRACT V1

**Status:** SUPREME SMART NOTE CONTRACT — CURRENT / MANDATORY  
**Effective:** 2026-09-24  
**Scope:** Every Naya, NayaNET, Intelligent Hub, Superbrain, runtime, migration, retrieval, test, and documentation operation that creates, reads, updates, displays, or refers to a Smart Note.

---

## 1. THE SIMPLE DEFINITION

> **SMART NOTE = INTELLIGENT BLOCK.**

“Smart Note” is the human-friendly name.

“Intelligent Block” is the canonical system object.

A Smart Note is **one coherent, provenance-bound piece of understood intelligence** created because something is worth remembering, reusing, connecting, applying, verifying, learning from, or handing to the next Naya.

It is **not**:
- a chat transcript;
- a random Markdown file;
- a folder;
- a Feed card;
- a Report;
- a Learning record;
- a second database;
- five different notes for five perspectives.

The perspectives are views of **one intelligence object**.

---

## 2. THE CORE LAW

**ONE INTELLIGENCE EVENT → ONE CANONICAL SMART NOTE / INTELLIGENT BLOCK → MANY AUTHORIZED REPRESENTATIONS → RETRIEVE → APPLY → VERIFY → LEARN → COMPOUND.**

The system must preserve the semantic identity and provenance of the intelligence while allowing different human, AI, machine, Hub, API, Feed, Report, and replay representations.

> **ONE INTELLIGENCE. MANY REPRESENTATIONS. ONE CANONICAL MEANING.**

---

## 3. CANONICAL MACHINE CONTRACT

All canonical Smart Notes MUST conform to:

**Schema:** `NAYANET_INTELLIGENT_BLOCK_V1`  
**Machine schema:** `contracts/intelligent-block-v1.schema.json`  
**Human-readable contract:** `contracts/intelligent-block-v1.md`

The canonical Intelligent Block requires, at minimum:

```text
identity
type
meaning
context
time
provenance
evidence
truth
authority
value
lifecycle
integrity
```

When materially applicable it also carries:

```text
actors
intent
source_bundle
perspectives
distillation
relationships
action
outcome
learning
successor
projections
metadata
```

The block MUST preserve unknowns as unknowns and MUST NOT manufacture evidence, authority, certainty, outcomes, or relationships.

---

## 4. CANONICAL IDENTITY MODEL

There is one semantic identity chain:

```text
EVENT
  event_id
    ↓
INTELLIGENT BLOCK
  identity.object_id = IB:<event_id>
  identity.schema_version = NAYANET_INTELLIGENT_BLOCK_V1
    ↓
SMART NOTE HUMAN ADDRESS
  SN-YYYYMMDD-<short-slug>.md
```

Rules:

1. `event_id` identifies the canonical intelligence event / provenance root.
2. `identity.object_id` identifies the canonical Intelligent Block derived from that event.
3. The Smart Note filename is a deterministic human-readable address, not a competing semantic identity.
4. Local database IDs, UI IDs, Feed IDs, receipt IDs, and projection IDs MUST NOT replace canonical identity.
5. Replays MUST resolve to the existing canonical identity rather than create a second semantic object.

---

## 5. CANONICAL PHYSICAL STORAGE

### Logical namespace

`NayaPOWER/SMART-NOTES/YYYY/MM/DD/`

### Physical repository

`.naya/memory/notes/YYYY/MM/DD/`

### Filename

`SN-YYYYMMDD-[short-human-readable-slug].md`

### Day index

Each day MAY contain:

`INDEX.md`

The index is a navigation projection of that day's canonical Smart Notes. It is not a second source of truth.

The resolver is deterministic:

```text
Smart Note date
→ YYYY
→ MM
→ DD
→ .naya/memory/notes/YYYY/MM/DD/
```

No new canonical Smart Note may be written anywhere else.

---

## 6. WHAT IS NOT THE SMART NOTE STORE

These are NOT current canonical Smart Note homes:

- `.naya/SUPERBRAIN/SMART-NOTES/`
- `.naya/memory/smart-notes/`
- `.naya/project-intelligence/smart-notes/`
- `NAYA/SMART-NOTES/`
- `NAYANET/SMART-NOTES/`
- `SUPERBRAIN/SMART-NOTES/`
- `SUPERBRAIN/CONTINUITY/**/SMART-NOTES/`
- `SUPERBRAIN/INTELLIGENCE/**/SMART-NOTES/`
- `docs/smart-notes/`
- feature-local `SMART-NOTES/` folders
- `.naya/memory/events/` (canonical event/provenance store, not Smart Note home)

Existing files in those locations are classified as **historical, architectural, compatibility, or projection artifacts** unless separately designated by an explicit migration receipt.

Do not mass-delete history merely to make the tree look uniform.

Do not create new Smart Notes in historical locations.

---

## 7. CANONICAL HUMAN-READABLE SMART NOTE STRUCTURE

Every completed Smart Note uses this exact order:

1. **IN A NUTSHELL**
2. **HUMAN NOTE**
3. **CHILD NOTE**
4. **GRANDMA NOTE**
5. **NAYA NOTE**
6. **MACHINE NOTE**
7. **LEARNING LESSON**
8. **WHAT IT MEANS**
9. **HOW IT CONNECTS**
10. **HOW TO APPLY IT**
11. **WHAT'S IN IT FOR THEM / YOU / US**
12. **EVIDENCE / SMART LINKS**
13. **CURRENT STATE**
14. **ONE NEXT ACTION**

This is one object with multiple views.

### Perspective meaning

**IN A NUTSHELL**  
The smallest accurate statement that preserves the core intelligence.

**HUMAN NOTE**  
What a normal person needs to understand, remember, decide, or protect.

**CHILD NOTE**  
The simplest truthful explanation using familiar language.

**GRANDMA NOTE**  
The practical, everyday explanation or wisdom that makes the idea intuitive and memorable.

**NAYA NOTE**  
The AI/operational interpretation: implications, relationships, risks, relevance, and what a future Naya should understand or do differently, bounded by evidence.

**MACHINE NOTE**  
The software/system representation: canonical IDs, schema, state, provenance, evidence, relationships, authority, privacy, lifecycle, and executable implications. Machine truth belongs to the structured block, not prose pretending to be machine data.

**LEARNING LESSON**  
The durable lesson extracted from the event. A written lesson is not automatically verified learning.

**WHAT IT MEANS**  
Why the intelligence matters in the larger system or mission.

**HOW IT CONNECTS**  
The important relationships to prior intelligence, current state, people, projects, events, capabilities, or successor work.

**HOW TO APPLY IT**  
The practical bridge from understanding to future action.

**WHAT'S IN IT FOR THEM / YOU / US**  
The direct value for the relevant person(s), for the Naya/system, and for the collective mission.

**EVIDENCE / SMART LINKS**  
Direct links/IDs to the canonical event, source, receipt, commit, evidence, verification, and relevant projection where available.

**CURRENT STATE**  
What is true now, including uncertainty and unresolved gaps.

**ONE NEXT ACTION**  
Exactly one highest-value executable continuation action.

---

## 8. DISTILLATION LAW

A Smart Note preserves **meaning, not merely wording**.

Naya MUST:

1. identify the actual subject;
2. separate signal from conversational noise;
3. preserve consequential context;
4. preserve uncertainty and conflicts;
5. preserve provenance and evidence;
6. distill to the smallest representation that remains useful;
7. preserve the relationships necessary for future retrieval and reuse;
8. avoid manufacturing content simply to fill a section.

The note must be:

**clear, direct, concise, complete enough, and no larger than necessary.**

---

## 9. ONE OBJECT / MANY REPRESENTATIONS

The same Smart Note / Intelligent Block MAY appear as:

- canonical Markdown;
- canonical JSON/YAML;
- database persistence;
- event ledger;
- Hub block;
- Personal Feed item;
- Collective Feed projection after consent;
- Activity entry;
- Report synthesis;
- Learning evidence;
- Dream / Replay input;
- API/MCP/A2A payload.

These are projections or uses of the same intelligence.

They are NOT new Smart Note authorities.

---

## 10. EVENT VS BLOCK VS PROJECTION

**EVENT** = what happened / was captured.

**INTELLIGENT BLOCK / SMART NOTE** = what the system currently understands from that intelligence, with provenance and state.

**FEED / ACTIVITY / REPORT / LIBRARY / HUB** = where that intelligence is surfaced, summarized, navigated, or acted on.

**LEARNING** = what changed because of evidence and outcome.

**DREAM / REPLAY** = controlled reuse/reflection over retained intelligence.

This distinction prevents the system from confusing storage, interpretation, presentation, and learning.

---

## 11. CREATION CONTRACT

A request such as:

> “Make a Smart Note about X.”

means:

```text
RESTORE RELEVANT CONTEXT
→ IDENTIFY SUBJECT
→ DISTILL INTELLIGENCE
→ BUILD CANONICAL INTELLIGENT BLOCK
→ VALIDATE SCHEMA
→ RESOLVE CANONICAL PATH
→ PERSIST
→ READ BACK / VERIFY
→ REGISTER / INDEX
→ EMIT ACTIVITY
→ PROJECT TO AUTHORIZED FEEDS / HUB
→ RECORD RECEIPT
→ RETURN SMART LINK
→ IDENTIFY ONE NEXT ACTION
```

The human must supply intent/subject/authority as appropriate.

Naya owns the protocol.

The system MUST reject or fail closed when required identity, provenance, schema, authorization, or persistence evidence is missing.

---

## 12. RETRIEVAL CONTRACT

Retrieval MUST search the **canonical intelligence system**, not arbitrary GitHub folders.

The primary retrieval keyspace is:

- canonical `event_id`;
- canonical Intelligent Block identity;
- canonical Smart Note date;
- subject/topic;
- approved tags/relationships;
- owner/scope;
- truth/verification state;
- current/superseded state;
- relevant provenance.

Filesystem search across legacy folders is NOT the canonical retrieval strategy.

A retrieval result MUST preserve the canonical identity and point back to the canonical Smart Note/event.

---

## 13. DATE / TIME / TOPIC RETRIEVAL

Smart Notes must be navigable by:

**YEAR → MONTH → DAY → TIMESTAMP → TOPIC / SUBJECT → RELATIONSHIPS**

The physical day folder is the calendar partition.

The note metadata/event carries the exact timestamp.

A day index provides the human-friendly chronological map.

This lets a Naya answer:

- “What Smart Notes did we create today?”
- “Show me September.”
- “Find last Tuesday's notes.”
- “Find the notes about Smart Note governance.”
- “Show what we learned about the Hub.”

without searching every historical folder in the repository.

---

## 14. LEGACY / COMPATIBILITY LAW

Historical formats may remain readable.

Aliases include, where encountered:

- `ADAPTIVE LEARNING` → `LEARNING LESSON`
- `ADAPTER LEARNING` → `LEARNING LESSON`
- `CHILD / DERIVED NOTE` → `CHILD NOTE`
- `CHILD` → `CHILD NOTE`
- `GRANDMA` → `GRANDMA NOTE`
- `HUMAN` → `HUMAN NOTE`
- `NAYA` → `NAYA NOTE`
- `MACHINE` → `MACHINE NOTE`
- `ULTIMATE MEANING` → `WHAT IT MEANS`
- `WHY IT MATTERS` → `WHAT IT MEANS` only when the content is explanatory rather than causal;
- `HOW TO USE` → `HOW TO APPLY IT`
- `WHAT'S IN IT FOR ME / YOU / US` → `WHAT'S IN IT FOR THEM / YOU / US`
- `GRAMMAR NOTE` → legacy implementation metadata; not a canonical perspective.

Legacy artifacts MUST be reconciled by provenance and meaning, not blindly copied into new canonical notes.

---

## 15. HUB REPRESENTATION CONTRACT

The Hub is a **projection**, not the source of truth.

The current Hub architecture defines the intelligent object as:

```text
IDENTITY
→ NUTSHELL
→ PERSPECTIVES
→ WEAVER / CONNECTIONS
→ LESSON
→ MEANING
→ ACTION
```

The canonical Smart Note human structure above supplies the complete underlying intelligence.

The Hub may collapse, expand, rename, reorder, or progressively disclose authorized views for usability, but it MUST NOT change their meaning.

Missing intelligence MUST remain missing. The renderer must not invent it.

---

## 16. FEED / ACTIVITY CONTRACT

When a Smart Note is successfully persisted:

1. the canonical event is recorded;
2. the Activity/notification projection may announce that new intelligence exists;
3. authorized Feed/Hub projections may surface it;
4. learning may be recorded as candidate/observed/verified according to evidence;
5. the receipt records what actually happened.

Creation in GitHub alone does NOT prove:

**indexed → projected → retrieved → rendered → end-to-end verified.**

Those states must remain separate.

---

## 17. LEARNING / DREAM / COMPOUNDING

The Smart Note is the seed.

Preferred chain:

```text
SMART NOTE
→ RETAIN
→ RETRIEVE
→ APPLY
→ OBSERVE OUTCOME
→ VERIFY
→ LEARN
→ UPDATE / SUPERSEDE
→ REPLAY / DREAM
→ REUSE
→ COMPOUND
```

A Smart Note may create a **learning candidate** immediately.

Verified learning requires evidence beyond the existence of the note.

Dream / Replay operates on retained intelligence; it does not create a competing memory store.

---

## 18. DAILY DIARY / SCORECARD RULE

A daily scorecard is a Smart Note when it is intentionally preserved as reusable intelligence.

Use:

```text
YYYY-MM-DD
→ SCORECARD
→ INTELLIGENT BLOCK / SMART NOTE
```

The daily note may contain:

- what we are building;
- today's observed score;
- what the score means;
- the principal gaps;
- the most valuable immediate actions;
- what should be learned;
- how the day connects to the larger mission;
- current state;
- one next action.

A Daily Report is still a Report. It is not automatically a Smart Note.

---

## 19. MIGRATION RULE

When legacy Smart Note artifacts are found:

**IDENTIFY → CLASSIFY → PRESERVE → LINK → RECONCILE → VERIFY**

Do not mass-move historical files unless needed.

Do not delete historical evidence simply because it is in the wrong folder.

Current retrieval and creation MUST stop using legacy locations as write targets.

Today's notes MUST be migrated into the canonical path after the canonical contract is locked.

---

## 20. ACCEPTANCE TEST

A Smart Note implementation is GREEN only when a fresh Naya can:

1. identify the Smart Note as an Intelligent Block;
2. find it by canonical identity;
3. find it by date/topic;
4. read the canonical human structure;
5. identify the source event;
6. identify provenance/evidence;
7. distinguish truth from inference;
8. distinguish authority from capability;
9. see current learning state;
10. identify how it connects;
11. identify how to apply it;
12. identify the next action;
13. follow the Smart Link;
14. reach authorized projections without creating a second source of truth.

---

## 21. SUPREME RULE

> **WHEN SHAWN SAYS “MAKE A SMART NOTE,” NAYA CREATES ONE CANONICAL INTELLIGENT BLOCK, PUTS IT IN THE ONE CANONICAL SMART NOTE LOCATION, EMITS THE REQUIRED SYSTEM EVENTS, AND RETURNS THE SMART LINK + TRUE RECEIPT.**

No Naya may invent a new Smart Note format, folder, identity, or storage system.

**One object. One meaning. One canonical home. Many useful views.**

