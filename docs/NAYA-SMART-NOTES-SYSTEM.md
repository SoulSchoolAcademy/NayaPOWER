# NAYA SMART NOTES SYSTEM

**Synonyms:** Naya Note = Smart Note = durable Naya memory.

**Status:** ACTIVE REPOSITORY STANDARD
**Purpose:** Give Naya a durable, searchable, structured learning and memory system that improves future work without depending on conversation history.

## 1. CORE PRINCIPLE

Naya Notes are the durable memory layer for the project.

For **every project conversation**, Naya should automatically evaluate whether anything durable was created, changed, learned, decided, or made materially more useful for future work. If durable value exists, capture it by default rather than waiting for the user to ask.

Do not save conversational noise. Save durable value.

The note must preserve the information in a form another AI can discover, understand, verify, and reuse without access to the original conversation.

## 2. WHAT COUNTS AS DURABLE VALUE

Capture when the conversation creates or materially changes:

- a product decision;
- a goal or desired outcome;
- a requirement or constraint;
- a design principle;
- a technical discovery;
- a failure/root cause;
- a solution or guardrail;
- a workflow improvement;
- a user preference relevant to the project;
- a naming convention;
- a source-of-truth decision;
- a reusable prompt or operating rule;
- a research finding;
- an important person/resource/event;
- a lesson that should change future behavior;
- an insight that materially improves judgment.

If nothing durable was created, do not create a note merely because a conversation occurred.

## 3. NOTE CATEGORIES

Use exactly one primary category unless a special case genuinely requires another classification.

- IDEA — new concept or possibility
- LEARNING — something discovered
- GOAL — desired outcome
- DECISION — something explicitly decided
- FACT — important factual information
- RESOURCE — useful external/internal reference
- KNOWLEDGE — durable domain/product knowledge
- PROBLEM — something that went wrong
- SOLUTION — how a problem was solved
- PERSON — useful information about a person
- EVENT — meeting, appointment, milestone, future event
- TASK — action that needs to happen
- INSIGHT — meaningful realization or pattern

## 4. REQUIRED NOTE STRUCTURE

Every durable note should follow this structure:

```text
# [SHORT HUMAN-READABLE TITLE]

- Timestamp: YYYY-MM-DD HH:MM TZ
- Last Updated: YYYY-MM-DD HH:MM TZ (when updated)
- Category: [ONE CATEGORY]
- Status: [ACTIVE | SUPERSEDED | RESOLVED | REFERENCE]
- Scope: [PROJECT | PRODUCT | FEATURE | TECHNICAL | PERSONAL-PROJECT CONTEXT]
- Keywords: [5–15 plain-language search terms]
- Aliases: [synonyms, abbreviations, alternate wording]
- Related: [paths, documents, notes, concepts, features]

## Context
Why this note exists.

## What We Learned / Decided
The durable information.

## Why It Matters
The consequence for future work.

## Required Behavior
Exactly what Naya should do differently because of this note.

## Evidence / Source
Where the information came from or how it was verified.

## Follow-up
Only if an actual future action exists.
```

Never invent a timestamp. Use the actual timestamp available to the execution environment. If exact time is unavailable, preserve the known date and explicitly mark the time as unavailable rather than fabricating precision.

## 5. SEARCHABILITY LAW

Do not rely on exact phrasing.

A future AI may search using a synonym, abbreviation, concept, consequence, related term, date, category, or natural-language question rather than the exact wording used when the note was created.

Therefore:

1. Write a descriptive title using the main concept.
2. Add 5–15 plain-language keywords.
3. Add aliases and synonymous terms.
4. Mention important concepts naturally in the body.
5. Use stable category names.
6. Cross-link related notes/documents when known.
7. Update `docs/smart-notes/INDEX.md` for meaningful new retrieval targets.
8. Prefer one strong durable note over many fragmented notes.

Example:

`Naya Note`, `Smart Note`, `memory`, `durable memory`, `project memory`, `learning log`, `recall`, and `context restoration` should be discoverable as the same system concept.

## 6. TIMESTAMP LAW

Every note must carry an explicit timestamp.

Use the actual creation/update time available to the execution environment. Never invent a timestamp.

For significant updates, preserve the original timestamp and add:

`Last Updated: YYYY-MM-DD HH:MM TZ`

## 7. APPEND VS NEW NOTE

Append/update an existing note when the new information is the same durable subject.

Create a new note when:

- it is a genuinely different subject;
- the old note would become difficult to scan;
- the information represents a separate decision or event;
- historical separation materially matters.

Do not create a new file merely because a conversation happened.

## 8. CONFLICT LAW

If a new note conflicts with an older note:

1. Do not silently overwrite the historical fact.
2. Identify the conflict.
3. Determine whether the new information explicitly supersedes the old information.
4. Mark the old information `SUPERSEDED` when appropriate.
5. Preserve the relationship between old and new.
6. Update the active rule in the appropriate governing document if the change is architectural.

## 9. MEMORY VS GOVERNANCE

Smart Notes preserve learning and context.

They do not automatically become product law.

When a lesson becomes a governing rule, promote it deliberately into the appropriate authoritative document such as:

- `NAYA-OS.md`
- `docs/NAYA-NITRO-MODE.md`
- a product specification;
- a deployment/release contract;
- a design directive.

The note should then reference the promoted rule.

## 10. DEFAULT CONVERSATION BEHAVIOR

For every project conversation, Naya should internally ask:

**“Did this conversation create durable knowledge that future Naya should know?”**

If yes, capture it automatically.

The user does not need to remember the exact command `make a Naya Note` for the system to preserve clearly valuable learning.

The explicit command remains available when the user wants a guaranteed note even if the information would otherwise be considered lower-value.

## 11. RECALL BEHAVIOR

When asked:

- “What did we learn yesterday?”
- “What did we decide last week?”
- “Check the Smart Notes on X.”
- “What do you remember about X?”
- “Review the Naya Notes.”

Search by concept, date, category, aliases, related terms, and the retrieval index. Do not require exact keyword matches.

Summarize the relevant notes, distinguish decisions from observations, identify superseded information, and point to supporting notes/documents.

## 12. DAILY REVIEW

At the start of a substantial workday or execution cycle, review recent Smart Notes when they are relevant to the task.

Do not mechanically dump all notes into context. Retrieve the smallest relevant set that provides sufficient continuity.

## 13. LEARNING LOOP

The system should continuously move:

**CONVERSATION → CAPTURE → STRUCTURE → SEARCH → RECALL → APPLY → VERIFY → IMPROVE**

A repeated failure should become a guardrail where practical.

A repeated successful pattern should become a reusable method where practical.

## 14. QUALITY TEST

A Smart Note is good enough only if a different AI, with no access to the original conversation, can answer:

- What happened?
- What was learned?
- What was decided?
- Why does it matter?
- What should I do differently now?
- Where is the supporting evidence?

If those questions cannot be answered, improve the note.
