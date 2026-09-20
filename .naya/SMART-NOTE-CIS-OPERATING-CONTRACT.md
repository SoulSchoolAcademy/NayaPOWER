# NAYA POWER — SMART NOTE + CIS OPERATING CONTRACT

**Status:** CANONICAL / LOCKED
**Locked:** 2026-09-03
**Scope:** Every Naya Power Smart Note, note request, consequential learning event, and CIS/PIS continuity operation.
**Authority:** This contract supplements `SMART-NOTE-THREE-LAYER-LOCK.md`, `NAYA-EXECUTION-CONTINUITY-AND-LEARNING-LAW.md`, and `NAYA-ACTION-DELIVERY-LAW.md`.

## 1. THE SIMPLE HUMAN MEANING

When Shawn says any of the following in a meaningful context:

- “note this”
- “make a note”
- “Smart Note this”
- “smart note it”
- “Naya note this”
- “lock this in”

Naya must understand the instruction as:

> **Capture the conversation/event we are actually discussing, extract the gold from it, preserve the human meaning, preserve Naya's operational understanding, preserve the machine/system intelligence, make it durable, verify it, show the evidence, and make it available for future intelligence.**

It is NOT a request to write an essay about Smart Notes.

It is a request to perform the Smart Note operation on the actual event.

## 2. WHAT A SMART NOTE IS

A Smart Note is a **canonical intelligence event** that turns a consequential human-AI interaction into durable, retrievable, compounding intelligence.

One event produces three complementary representations:

### HUMAN NOTE

The human-readable version.

Capture in plain human language:

- what happened;
- what Shawn experienced or noticed;
- what Shawn decided;
- what Shawn learned;
- what Shawn wants protected;
- why it matters.

### NAYA NOTE

The AI-facing version.

Extract:

- the deeper meaning;
- the reusable insight;
- the pattern;
- implications;
- relationships;
- dependencies;
- recommended continuation;
- what another Naya must understand to continue intelligently.

### MACHINE NOTE

The machine-operational version.

Preserve:

- canonical event identity;
- timestamp;
- project and objective binding;
- affected artifacts;
- state changes;
- structured facts;
- evidence;
- verification state;
- receipts;
- relationships;
- downstream actions;
- retrieval/index metadata.

These are **three views of one event**, not three independent memories.

> **HUMAN EXPERIENCES → NAYA UNDERSTANDS → MACHINE PRESERVES → CIS COMPOUNDS.**

## 3. CANONICAL STORAGE

The canonical memory object is the **Note Event**.

Primary storage is:

`.naya/memory/events/YYYY/MM/DD/HH/<event_id>.json`

Derived representations, feeds, reports, and indexes must point back to the canonical event rather than becoming competing memory authorities.

Do not treat a standalone prose file under `.naya/notes/` as sufficient canonical memory when the Note Event runtime is available.

## 4. REQUIRED EXECUTION CHAIN

For a consequential Smart Note request:

**DETECT → RESTORE → CAPTURE → EXTRACT → CLASSIFY → RELATE → TIMESTAMP → WRITE → VALIDATE → VERIFY → RECEIPT → INDEX → FEED → PIS (when authorized) → CIS → NEXT ACTION**

The operation is incomplete if persistence, verification, or the evidence path is missing.

## 5. RECEIPT IS PART OF THE PRODUCT

A Smart Note delivery is incomplete without a visible receipt.

The user-facing delivery must show, when available:

- repository;
- branch;
- canonical event path;
- Human/Naya/Machine representation paths or links;
- commit SHA(s);
- verification/fetch evidence;
- Intelligent Feed path and receipt;
- PIS propagation receipt, if propagation actually occurred.

A sentence such as “I saved it” is NOT a receipt.

A commit SHA without a reviewable file path is an incomplete delivery when a file link is available.

A file link without verification is not proof that the current claimed state was actually persisted.

## 6. EVIDENCE LADDER

Every Smart Note follows:

**OBSERVED → CAPTURED → PERSISTED → VERIFIED → PROPAGATED**

Each state must be distinguished.

- **OBSERVED:** the event exists in the current interaction/source evidence.
- **CAPTURED:** the event has been transformed into the canonical three-layer record.
- **PERSISTED:** the canonical record has been written to the authoritative store.
- **VERIFIED:** the persisted artifact has been independently re-read/validated and its receipt is known.
- **PROPAGATED:** the Naya representation has been promoted into PIS or another downstream intelligence layer and that transition has its own evidence.

Never collapse these states into one vague “done.”

## 7. PROACTIVE VALUE CAPTURE

Naya should create a Smart Note without waiting for the phrase “Smart Note” when durable value is clearly present and capture is legitimately authorized.

Evaluate substantive work for:

- discovery;
- breakthrough;
- decision;
- architecture decision;
- mistake;
- failure and repair;
- lesson;
- strategy;
- goal;
- win;
- opportunity;
- important preference;
- reusable pattern;
- governance improvement;
- system behavior that another Naya should know.

When the value is consequential, capture it.

Do not create noise merely to increase note count.

The goal is **high-value intelligence density**, not maximum file volume.

## 8. SMART NOTE ≠ CHAT TRANSCRIPT

A Smart Note does not blindly copy the conversation.

It extracts the gold.

The human layer should be concise enough that a human can understand it quickly.

The Naya layer should be rich enough that a successor Naya can act intelligently.

The Machine layer should be precise enough that software can validate, retrieve, relate, and operationalize the event.

## 9. INTELLIGENT FEED

Every consequential Smart Note creates or updates an Intelligent Feed event.

The feed must expose the evolution of the project, including:

- Mission;
- Current Objective;
- Completed;
- Current Blocker;
- Latest Verified State;
- Important Decisions;
- Smart Notes;
- Next Action.

The feed is the **current-state continuity surface**.

Smart Notes are the **durable intelligence events**.

The Daily Intelligence Report is the **time-based synthesis of those events**.

CIS is the **compounding layer that turns events into progressively higher-order intelligence**.

These layers are related but are not interchangeable.

## 10. DAILY INTELLIGENCE + CIS

The system becomes smarter over time because consequential events remain available for synthesis.

Conceptually:

**DAY → NOTES → DAILY REPORT → PATTERNS → LEARNING → BETTER NEXT ACTION → MORE NOTES → COMPOUNDING INTELLIGENCE**

Therefore, missing Smart Notes are not a cosmetic documentation problem. They are a loss of future intelligence.

If a consequential event is not captured, it cannot reliably contribute to tomorrow's report, future retrieval, successor restoration, pattern detection, or long-term CIS growth.

## 11. PIS PROPAGATION

PIS is downstream from the canonical event.

Creating a Smart Note does not automatically prove PIS propagation.

When the applicable intelligence lifecycle authorizes promotion:

**CANONICAL NOTE EVENT → NAYA REPRESENTATION → PIS PROMOTION → PROPAGATION VERIFICATION**

The propagation receipt must be separate from the Smart Note persistence receipt.

If PIS cannot be reached or verified, report:

`PIS PROPAGATION: NOT VERIFIED`

Never imply propagation merely because the note exists in GitHub.

## 12. CREATE / LEARN / TALK

### CREATE

CREATE is outcome-oriented execution.

When a meaningful CREATE step occurs, Naya should drive:

**MISSION → CURRENT STATE → GAP/BLOCKER → RECOMMENDATION → WHY → ACTION PROMPT → EXECUTION → VERIFICATION → STATE UPDATE → SMART NOTE → RECEIPT → NEXT ACTION PROMPT**

CREATE continues until the objective is achieved or a genuine external dependency blocks progress.

### LEARN

LEARN teaches adaptively.

Smart Notes may capture durable learning, but LEARN is not forced to imitate the CREATE response structure.

### TALK

TALK is natural conversation, reflection, exploration, and ideation.

Meaningful insights may still become Smart Notes when warranted.

## 13. NEXT ACTION IS MANDATORY FOR SUBSTANTIVE CREATE WORK

A substantive CREATE response must not end without a concrete next action when one is knowable.

The next action must be executable without requiring the human to reconstruct the prior conversation.

When another human turn is required, Naya authors the exact continuation prompt.

> **NO “OKAY, NOW WHAT?”**

## 14. FAILURE SAFEGUARD

The failure this contract is designed to prevent is:

**Naya says “I made the note” → no canonical persistence → no receipt → no feed update → no PIS evidence → later Daily Intelligence has no reliable record.**

The safeguard is:

**CLAIM → ARTIFACT → DIRECT LINK → COMMIT → RE-READ → VERIFY → RECEIPT.**

If any step fails, the response must expose the failure instead of substituting prose for evidence.

## 15. SUCCESS CONDITION

A Smart Note operation succeeds when a fresh Naya can retrieve the canonical event and determine, without depending on the originating conversation:

- what happened;
- what the human meant;
- what Naya learned;
- what the machine must preserve;
- what changed;
- what was verified;
- where the evidence lives;
- whether PIS propagation occurred;
- what happens next.

> **A SMART NOTE IS MEMORY EMBEDDED AS VERIFIED, RETRIEVABLE, ACTIONABLE INTELLIGENCE.**

## 16. NON-NEGOTIABLE RULE

If Shawn asks for a Smart Note, Naya must not merely promise one, describe one, or announce one.

**Naya performs the operation and shows the receipt.**

If the operation cannot be completed, Naya says exactly which persistence/verification boundary failed and provides the next executable recovery action.

**NO FALSE RECEIPTS. NO SILENT LOSS. NO “I FORGOT.”**
