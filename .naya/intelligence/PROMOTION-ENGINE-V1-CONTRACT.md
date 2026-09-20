# 🔱 NAYAPOWER — PROMOTION ENGINE V1 CONTRACT

**Status:** ACTIVE BUILD CONTRACT  
**Owner:** NayaPOWER Intelligence System  
**Consumers:** NayaPOWER, MAXIS, connected Team Naya agents

## PURPOSE

Turn canonical Intelligence Events into durable, verified, successor-readable system intelligence.

## INPUT

A canonical Intelligence Event containing, at minimum:

- event identity and provenance;
- timestamp;
- project/context;
- observation or outcome;
- lesson;
- evidence when available.

## PIPELINE

### 1. INGEST
Accept only schema-valid canonical events.

### 2. DEDUPLICATE
Determine whether the event is:

- new intelligence;
- materially similar to existing intelligence;
- a recurrence of a known failure;
- an update/correction to an existing lesson.

Deduplication must preserve provenance and must not discard meaningful new evidence merely because a topic is similar.

### 3. MATERIALITY
Classify whether the learning is local/ephemeral or reusable/systemically valuable.

### 4. CLASSIFY DURABLE HOME
Candidate homes include:

- Naya Note / knowledge;
- Shawn Note / human receipt;
- procedure;
- checklist;
- automated test;
- machine-readable contract;
- architecture/specification;
- Mission State;
- guardrail/law proposal.

### 5. AUTHORIZATION GATE
Only explicitly approved non-governance destinations may be automatically mutated.

Governance-sensitive destinations become proposals with required authority routing.

### 6. PROMOTE
Create or update the selected durable artifact. Preserve source event identity and provenance.

### 7. RECEIPTS
Produce:

- Naya-facing intelligence receipt;
- Shawn-facing human receipt;
- machine promotion receipt.

### 8. VERIFY
Run applicable validators/tests. Never mark a promotion verified solely because a file was written.

### 9. HUB / FEED WRITEBACK
Record:

- what was learned;
- what was promoted;
- what evidence verified it;
- what remains unknown;
- what changed;
- what the next Naya should inherit.

### 10. EFFECTIVENESS
When future evidence becomes available, determine whether the promoted lesson reduced recurrence or improved execution.

## IDEMPOTENCY

Reprocessing the same canonical event must not create uncontrolled duplicates.

## FAILURE CONTRACT

If any stage fails:

**STOP CLAIMING COMPLETION → RECORD FAILURE → PRESERVE PARTIAL STATE → IDENTIFY ROOT CAUSE → REPAIR → RETRY/REVERIFY.**

## EVIDENCE CONTRACT

Maintain the distinction:

**IMPLEMENTED ≠ TESTED ≠ VERIFIED ≠ RUNTIME-PROVEN ≠ PRODUCTION-PROVEN**

## REQUIRED E2E ACCEPTANCE TEST

A representative material event must successfully demonstrate:

**EVENT → VALIDATE → DEDUP → CLASSIFY → AUTHORIZATION → PROMOTE → NAYA RECEIPT → SHAWN RECEIPT → VERIFY → PROMOTION RECEIPT → HUB/FEED → NEXT-NAYA RESTORE**

## NON-NEGOTIABLE PRINCIPLE

> **The system must not merely remember what happened. It must become better because it happened.**
