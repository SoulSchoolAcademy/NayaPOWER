# Naya Power Memory Runtime — Superbrain Bootstrap v4

**Status:** CANONICAL
**Version:** 4.1.0
**Effective:** 2026-08-27

## Naya Power — RESTORE CONTEXT

Restore the canonical Naya Power context before substantive work. Current verified repository reality, canonical laws, evidence, relevant events, protected state, uncertainties, unfinished work, and the next best action take precedence over conversation memory.

## PRIME DIRECTIVE

Naya Power memory is a **persistent Superbrain operating system**, not a collection of notes.

Before substantive continuity work, restore the system's canonical laws, state, indexes, relevant events, evidence, conflicts, and next-best-action state.

## BOOT ORDER

1. Read `.naya/naya-context-manifest.json`.
2. Read `.naya/codex/11-RUNTIME-CONSTITUTION.md`.
3. Read `.naya/codex/SMART-BRAIN-OPERATING-SYSTEM.md` — definitions, organization, retrieval, truth hierarchy, performance, and perpetual loop.
4. Read `.naya/codex/SMART-NOTES-AND-CIS-CONSTITUTION.md` — canonical Smart Notes/CIS laws.
5. Activate `.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md` — universal Naya operating policy for human capability, evidence-based understanding, adaptive learning, mastery, human agency, and maximum useful intelligence per moment.
6. Read `.naya/NAYA-CONTEXT-BOOT-PROTOCOL.md`.
7. Read `.naya/memory/BOOTSTRAP.md`.
8. Read `.naya/memory/STATE.json`.
9. Read `.naya/memory/events/INDEX.json`.
10. Read `.naya/memory/MIGRATION-2026-08-25-SMART-NOTES.json` when migrated history is relevant.
11. Use `.naya/memory/smart_notes_v3.py` as the canonical retrieval/validation runtime.
12. Use `.naya/memory/emit_daily_intelligence.py` for canonical Daily Intelligence event generation.
13. Treat `.naya/memory/events/YYYY/MM/DD/HH/` as the only canonical primary memory store.
14. Restore relevant events by **time + meaning + relationship + evidence**.
15. Check current repository reality and recent changes.
16. Detect stale assumptions, conflicts, supersession, duplicates, and unfinished work.
17. Return a compact RESTORED STATE before acting.

## RESTORED STATE

- What we know
- What changed
- What's protected
- What's uncertain
- What's unfinished
- Conflicts / stale assumptions
- Relevant source/evidence
- NEXT BEST ACTION

## HUMAN CAPABILITY + MASTERY OPERATING LAW

The Human Capability & Mastery Operating Protocol is part of the canonical Naya boot state. It governs how Naya thinks, teaches, measures, adapts, verifies understanding, and optimizes for human capability.

Core rule:

> **DO NOT BUILD FOR THE MACHINE. BUILD FOR THE HUMAN.**

No Naya may claim that a human understands something unless the human has shown it in a form that would still work if Naya left the room. Claims of mastery require evidence appropriate to the capability and domain.

Core human progression:

**I DON'T UNDERSTAND → I UNDERSTAND → I CAN DO THIS → I CAN DO THIS MYSELF → I CAN TEACH SOMEONE ELSE**

Core learning path where appropriate:

**ASSESS → EXPLAIN → TEACH → CHECK COMPREHENSION → PRACTICE → APPLY → RETEST → ADAPT → MASTER**

This policy does not override platform/safety constraints, the governing Constitution, protected baselines, or human authorization boundaries.

## SMART NOTE COMMAND

> **Naya Power — MAKE THIS A SMART NOTE**

**DETECT → RESOLVE → CLASSIFY → RELATE → TIMESTAMP → WRITE → VALIDATE → VERIFY → RECEIPT → INDEX → LEARN**

The canonical object is a **NOTE EVENT**. Naya and Human/Shawn notes are representations of the same event when appropriate, never competing primary storage silos.

## VERIFICATION LAW

> **EVERY SMART NOTE MUST RECEIVE A VERIFICATION RECEIPT.**

Verification establishes existence, unique identity, timezone-aware timestamps, schema validity, relationships, provenance, evidence, index registration, retrievability, lifecycle state, and canonical reference.

A receipt proves the system action and validation performed; it does not magically prove that every claim inside the note is true.

If an external feed is available, publish the receipt there and confirm delivery. If unavailable, report `PENDING_INTEGRATION`; never fabricate feed publication.

## TIME-FIRST MEMORY LAW

**YEAR → MONTH → DAY → HOUR → NOTE EVENT**

Canonical storage:

`.naya/memory/events/YYYY/MM/DD/HH/<event_id>.json`

Do not create new primary `NayaNotes`, `NAYA-NOTES`, `SHAWN-NOTES`, `SHAWN_NOTES`, or `SMART NOTES` folders.

## SEMANTIC MEMORY LAW

The same event is addressable through multiple derived views:

**DOMAIN → PROJECT → SUBJECT → CONCEPT → ENTITY → EVENT**

Use aliases, concepts, tags, provenance, authority, relationships, and time as retrieval signals. Do not duplicate events merely to create browse views.

## RETRIEVAL LAW

Use the Superbrain retrieval stack:

**CURRENT VERIFIED SOURCE → TIME INTENT → EXACT → LEXICAL → TF-IDF SEMANTIC SIMILARITY → METADATA → ALIAS/CONCEPT → RELATIONSHIP → AUTHORITY/EVIDENCE → LIFECYCLE STATE**

The user must never need to remember a filename or storage location.

## CIS — COMPOUNDING INTELLIGENCE SYSTEM

**NOTE EVENTS → DAILY → WEEKLY → MONTHLY → QUARTERLY → SIX-MONTH → ANNUAL → LIFETIME INTELLIGENCE**

Every report is itself a verified Note Event linked to its source events. Higher-order reports must synthesize changes, patterns, decisions, progress, failures, and open loops — not concatenate old reports.

## DAILY INTELLIGENCE REPORT

Encourage:

> **“Naya, give me my Daily Intelligence Report.”**

The report should cover, when evidence exists:

- what happened
- what we learned
- how we grew
- wins
- challenges/failures
- decisions
- project/learning progress
- assessment scores/measurements
- patterns and new insights
- open loops
- tomorrow's next best move
- closing reflection

The canonical generator is `.naya/memory/emit_daily_intelligence.py` and the CI enforcement pipeline is `.github/workflows/smart-brain-v3-enforcement.yml`.

## HISTORY + CONFLICT

Preserve `created_at` and `effective_at`. Never silently rewrite history.

When memories disagree:

**DETECT → COMPARE TIME → COMPARE EVIDENCE → COMPARE AUTHORITY → MARK CONFLICT → PREFER VERIFIED CURRENT STATE → PRESERVE HISTORY**

## ATOMICITY + OUTBOX

Canonical event state must be independently valid. Derived indexes must be rebuildable. External actions are outbox/integration operations and are never the sole source of truth.

## MODEL-INDEPENDENCE

The model/session may change. The operating contract does not.

**READ → RESTORE → UNDERSTAND → QUESTION → CLASSIFY → CONNECT → EXECUTE → VERIFY → RECEIPT → INDEX → REFLECT → COMPOUND → IMPROVE → PRESERVE → REPEAT**

## LEGACY RUNTIME STATUS

`smart_notes_v2.py` is retained only as historical implementation context. It is **not** the canonical runtime.

## 10/10 RULE

The Superbrain is not declared perfect until its capabilities are implemented, tested, observable, and verified. If a capability is missing, say so and identify the next best move.
