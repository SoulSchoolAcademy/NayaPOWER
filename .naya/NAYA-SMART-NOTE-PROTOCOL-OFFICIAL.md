# 🧠 NAYA SMART NOTE PROTOCOL — OFFICIAL

**Document Class:** Canonical Naya Power Operating Protocol  
**Protocol ID:** NAYA-SMART-NOTE-PROTOCOL  
**Version:** 1.0  
**Effective Date:** 2026-09-15  
**Status:** OFFICIAL / CANONICAL  
**Scope:** All authorized Naya instances operating under Naya Power

## 1. PURPOSE

This protocol defines what Naya MUST do whenever an authorized human asks Naya to create a Smart Note.

The goal is not merely to generate formatted text. The goal is to turn meaningful intelligence into a durable, understandable, reusable intelligence object that can be stored canonically, surfaced by the Intelligent Hub, and used by future Naya.

The human should not need to remember, restate, or manage this protocol.

A natural-language request such as:

> “Naya, make a Smart Note about XYZ.”

MUST be interpreted as a request to invoke this protocol when the subject is sufficiently clear.

## 2. CORE PRINCIPLE

**ONE INTELLIGENCE EVENT → ONE CANONICAL SMART NOTE → MULTIPLE HUMAN-USEFUL PERSPECTIVES → DURABLE STORAGE → RETRIEVAL → APPLICATION → VERIFIED LEARNING.**

Naya must distill the highest-value intelligence rather than dump conversation text into a note.

The objective is future usefulness, clarity, truth, and continuity.

## 3. CANONICAL SMART NOTE OUTPUT CONTRACT

Every completed Smart Note MUST use this section order unless a higher-priority canonical implementation explicitly supersedes it:

1. **IN A NUTSHELL**
2. **HUMAN NOTE**
3. **CHILD NOTE**
4. **GRANDMA NOTE**
5. **NAYA NOTE**
6. **MACHINE NOTE**
7. **LEARNING LESSON**
8. **WHAT IT MEANS**
9. **HOW TO APPLY IT**
10. **WHAT'S IN IT FOR YOU?**

### Section purpose

**IN A NUTSHELL** — The shortest accurate statement of the core intelligence.

**HUMAN NOTE** — The normal human perspective: what a person needs to understand about the subject.

**CHILD NOTE** — A radically simple explanation using familiar language without losing the essential truth.

**GRANDMA NOTE** — A practical, everyday explanation that makes the subject intuitive and relatable.

**NAYA NOTE** — Naya's operational/intelligence perspective: implications, significance, relationships, risks, future relevance, and useful behavior where supported.

**MACHINE NOTE** — The structural/system representation of the intelligence. Use the actual canonical machine schema where one exists. Never invent machine fields or values merely to make the note look technical.

**LEARNING LESSON** — The durable lesson that should be learned from this subject or event. This is the lesson produced by the Smart Note, not a description of the overall Adaptive Learning system.

**WHAT IT MEANS** — Why the intelligence matters in the larger picture.

**HOW TO APPLY IT** — The practical bridge from understanding to action: what a person can actually do with this knowledge.

**WHAT'S IN IT FOR YOU?** — The direct human value, benefit, leverage, protection, clarity, or outcome.

## 4. PERSPECTIVE RULE

The sections are different lenses on the same underlying intelligence.

They MUST NOT become ten disconnected mini-articles.

The core meaning must remain consistent across perspectives while the language, abstraction level, and purpose change.

Naya must not manufacture differences merely to fill sections.

## 5. DISTILLATION RULE

When creating a Smart Note, Naya MUST:

1. Identify the actual subject.
2. Identify the meaningful intelligence.
3. Separate signal from conversational noise.
4. Preserve important nuance and uncertainty.
5. Distill to the most valuable direct-to-the-point information.
6. Generate the canonical perspectives.
7. Explain significance.
8. Provide practical application where supported.
9. State the human benefit.

A Smart Note is not a transcript.

A Smart Note is not a summary of everything said.

A Smart Note preserves what is worth remembering and using again.

## 6. TRUTH AND PROVENANCE

Naya MUST distinguish:

- human-stated information
- observed information
- derived intelligence
- inference
- external information
- verified information
- unknown or uncertain information

Naya MUST NOT invent facts, emotions, motives, causes, evidence, timestamps, IDs, relationships, verification, or outcomes.

Uncertainty MUST remain uncertainty.

This protocol inherits the existing Naya Power Smart Notes trust law: documentation, implementation, execution, observation, and verification are not interchangeable.

## 7. CREATE / UPDATE / CORRECT BEHAVIOR

### CREATE
“Make a Smart Note about XYZ” creates a new canonical Smart Note when no equivalent canonical intelligence object exists.

### UPDATE
“Update the Smart Note about XYZ” modifies the existing canonical Smart Note rather than blindly creating a duplicate.

### CORRECT
When a factual or structural error is identified, correct the canonical note while preserving appropriate provenance/history.

### SUPERSEDE
When newer verified information replaces an older state, preserve the history and establish the appropriate supersession relationship where the canonical architecture supports it.

### DUPLICATE PROTECTION
Same subject does not automatically mean same event. Naya must distinguish a genuinely new intelligence event from an existing note that should be updated.

## 8. CANONICAL PERSISTENCE

The canonical Smart Note MUST be persisted through the existing Naya Power/GitHub source-of-truth architecture.

Naya MUST use existing canonical Smart Note, event, storage, indexing, validation, and retrieval infrastructure where available.

Naya MUST NOT create a competing Smart Note database or duplicate canonical storage system merely because another implementation is convenient.

GitHub is the canonical operational source-of-truth layer for this Naya Power implementation. The Intelligent Hub is a presentation/retrieval layer over that underlying intelligence.

## 9. INTELLIGENT HUB / FEED FLOW

The intended end-to-end flow is:

**HUMAN REQUEST**
→ “Naya, make a Smart Note about XYZ.”

**NAYA SMART NOTE PROTOCOL**
→ understand subject
→ distill intelligence
→ generate canonical ten-part output
→ validate

**CANONICAL GITHUB**
→ persist the Smart Note / event
→ establish canonical identity and provenance

**AUTOMATION / GITHUB WORKFLOW**
→ detect the relevant canonical change/event
→ run the authorized ingestion/update process

**INTELLIGENT HUB**
→ ingest the canonical intelligence
→ render the Smart Note in the approved Intelligent Block presentation

**INTELLIGENT FEED**
→ surface the resulting intelligence according to the existing Feed rules

**VERIFICATION**
→ confirm the expected downstream state before claiming successful publication.

## 10. CRITICAL VERIFICATION RULE

Creation of a Markdown file or GitHub commit alone does NOT prove that the Intelligent Hub or Feed has updated.

The system MUST distinguish:

**CREATED IN GITHUB**
≠
**INGESTED BY APP**
≠
**VISIBLE IN HUB**
≠
**VISIBLE IN FEED**
≠
**VERIFIED END-TO-END**

If downstream evidence is unavailable, the status MUST remain unverified.

Naya MUST NEVER say “it is live in the Hub” merely because the GitHub write succeeded.

## 11. VALIDATION CONTRACT

Before final completion, Naya should validate at minimum:

- subject exists and is coherent
- all ten canonical sections exist
- section order is correct
- content is materially useful
- perspectives are consistent with the same underlying intelligence
- no unsupported facts were fabricated
- uncertainty is preserved
- machine representation uses supported structure
- duplicate/update state is resolved where possible
- canonical persistence succeeded
- downstream trigger state is known
- downstream Hub/Feed state is known

## 12. FAILURE STATES

Naya MUST report the actual state when a step fails.

Examples:

**CONTENT_CREATED / GITHUB_NOT_WRITTEN**

**GITHUB_WRITTEN / DOWNSTREAM_NOT_TRIGGERED**

**TRIGGERED / HUB_NOT_VERIFIED**

**HUB_VERIFIED / FEED_NOT_VERIFIED**

**END_TO_END_VERIFIED**

No failure state may be silently converted into success.

## 13. OFFICIAL EXAMPLE SET

The existing nine Smart Notes in the supplied canonical Smart Note set are to become the initial permanent reference set for this output contract after they are revised to include:

- LEARNING LESSON
- HOW TO APPLY IT

The revised notes will serve simultaneously as:

1. permanent Intelligent Hub knowledge;
2. canonical examples of the Smart Note output contract;
3. visual acceptance-test material for the Intelligent Block renderer;
4. human-facing explanations of the Naya Power system;
5. regression/reference material for future Smart Note generation.

They are not disposable demo content.

## 14. ACCEPTANCE STANDARD

The Smart Note system is successful only when a person can issue a simple natural-language preservation command and the system can reliably:

**UNDERSTAND → DISTILL → STRUCTURE → STORE → TRIGGER → INGEST → DISPLAY → VERIFY**

without requiring the human to manually restate the Smart Note format or manually move the resulting intelligence between systems.

The human supplies the intent and subject.

Naya carries the appropriate operational protocol.

The human remains the director and authority.

## 15. RELATIONSHIP TO EXISTING NAYA POWER LAW

This protocol extends—not replaces—the existing Naya Power Smart Notes + Receipts activation contract.

Existing requirements concerning source truth, no fabrication, evidence, provenance, verification, canonical infrastructure, duplicate protection, privacy, and receipt integrity remain in force.

Where this protocol conflicts with a higher-priority canonical law, the higher-priority law governs and the conflict MUST be resolved explicitly rather than silently ignored.

## 16. LOCKED DESIGN INTENT

The design intent is now:

**“Say ‘make a Smart Note,’ and Naya knows what a Smart Note is, how to think about it, how to structure it, where to put it, how it gets into the Intelligent Hub, and what evidence is required before saying it is done.”**

That is the intended portable behavior for authorized Naya instances operating under Naya Power.

---

**STATUS: OFFICIAL / CANONICAL / READY FOR IMPLEMENTATION AND END-TO-END ACCEPTANCE TESTING**
