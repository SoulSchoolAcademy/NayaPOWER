# Universal Meaningful-Output Adapter — Independent Contract Validation

Date: 2026-09-23
Scope: P0 universal meaningful-output promotion
Mode: READ-ONLY VALIDATION + REPRESENTATIVE INPUT SELECTION
Production mutation: NONE
Database mutation: NONE
Deployment: NONE
Readiness frontier: NOT ADVANCED

## Sources independently checked

- .naya/intelligence/PROMOTION-ENGINE-V1-CONTRACT.md
- .naya/contracts/SMART-NOTE-PROPOSAL-CONTRACT-V1.json
- NAYANET/HUB/public/assistant-runtime.js
- supabase/functions/nayanet-compound-intelligence/index.ts
- NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx

## Validation result

### 1. Promotion Engine V1 — compatible

The adapter preserves the canonical sequence:

MEANINGFUL OUTPUT → RECOGNIZE → NORMALIZE → DEDUPLICATE → MATERIALITY/CLASSIFY → AUTHORIZATION → ROUTE → PROVENANCE → RECEIPT → VERIFY.

The existing promotion contract already requires schema validation, deduplication, materiality, durable-home classification, authorization, promotion, receipts, verification, writeback, and later effectiveness.

The adapter adds no competing persistence layer. It is a semantic boundary before an existing destination.

### 2. Smart Note Proposal V1 — compatible with an intentional distinction

The Smart Note proposal contract establishes the AI recognition/governance pattern: recognition is not truth, recognition is not authority, provenance/uncertainty/privacy must survive, and the existing Smart Note/PIS/Smart Ledger boundaries remain authoritative.

The universal adapter reuses those laws but is broader than Smart Note. A meaningful output is NOT automatically a Smart Note. Destination selection remains explicit.

Therefore:
- Smart Note remains one possible canonical destination.
- The adapter must not call captureSmartNote merely because an output is meaningful.
- Non-Smart-Note destinations must remain behind their own canonical authority boundary.

### 3. Runtime record() primitive — compatible as persistence substrate, not as promotion engine

assistant-runtime.js record(input) is authenticated and routes through nayanet_record_cognition_event. It returns canonical event/receipt data and therefore can serve as a canonical event persistence primitive.

It does NOT itself implement universal materiality, destination classification, authorization, promotion verification, or effectiveness. Those must remain above/around the primitive.

The adapter must therefore not mistake successful record() persistence for promotion verification.

### 4. Runtime captureSmartNote() primitive — intentionally specialized

captureSmartNote() is an existing canonical Smart Note ingress into v7-smart-note-canonical. SmartNoteSurface then requires event + receipt and performs fresh retrieval verification.

This validates the architectural rule that universal recognition must route to destination-specific canonical ingress rather than replace it.

### 5. intelligence_commit — smallest proven promotion rung

commitIntelligence() in nayanet-compound-intelligence/index.ts:
- requires an idempotency key and content;
- derives a stable intelligence event identity;
- preserves idempotent identity/conflict detection;
- persists through nayanet_record_cognition_event;
- projects into the existing intelligence index;
- creates/retains learning evidence;
- checkpoints intelligence;
- materializes the existing Intelligent Block;
- explicitly states that capture + integration + checkpoint do NOT prove applicability, behavior change, outcome verification, or improvement.

This is the correct destination for the first bounded universal adapter proof because it is already a governed, idempotent, provenance-bound promotion rung and does not require opening a new consequential domain.

## Concrete non-Smart-Note output surface selected

The representative source class is a **private tool_result containing one explicit reusable lesson**.

Why this surface:
- source_type=tool_result is explicitly allowed by the Smart Note proposal contract's source vocabulary;
- it is not itself a Smart Note;
- it can remain PRIVATE;
- it requires no publication, communication, relationship, or external-action authority;
- it can be routed to existing_intelligence without inventing a second store;
- its semantic content is small enough to test the adapter boundary without coupling multiple domains.

## Single smallest representative input

The minimum proof input is one private, non-consequential tool result with one reusable lesson:

```json
{
  "output_id": "tool-result:adapter-proof-001",
  "output_version": 1,
  "event_at": "2026-09-23T20:00:00Z",
  "source_ref": "tool-result:adapter-proof-001",
  "source_type": "tool_result",
  "title": "Canonical resolver lesson",
  "content": "Use the existing canonical resolver instead of creating a parallel intelligence destination.",
  "meaning": "Prevents duplicate memory paths and preserves one authoritative intelligence system.",
  "materiality": "REUSABLE",
  "proposed_use": "Apply the canonical resolver rule when routing future meaningful outputs.",
  "applicable_scope": "NayaNET intelligence routing only.",
  "uncertainties": [],
  "provenance_refs": ["tool-result:adapter-proof-001"],
  "provenance_hash": null,
  "evidence_state": "OBSERVED",
  "source_event_id": null,
  "privacy": "PRIVATE",
  "authority_ref": null,
  "requested_action": "ROUTE_IF_AUTHORIZED",
  "destination_class": "existing_intelligence"
}
```

Expected bounded route:

TOOL_RESULT
→ UNIVERSAL_MEANINGFUL_OUTPUT_V1
→ existing-intelligence authorization check
→ intelligence_commit
→ canonical cognition event
→ existing intelligence index
→ learning evidence/checkpoint/Intelligent Block
→ receipt
→ fresh retrieval verification.

No Smart Note capture is part of this proof.

## What this validation establishes

- The derived adapter contract is compatible with the canonical promotion contract.
- The adapter correctly treats Smart Note as a destination, not as the universal destination.
- record() is a persistence primitive, not a substitute for governance/promotion verification.
- captureSmartNote() remains the specialized Smart Note boundary.
- intelligence_commit is the smallest existing proven promotion rung for the first universal proof.
- The first proof can be isolated to one private tool_result and one existing-intelligence destination.

## What remains unproven

- Runtime implementation of UNIVERSAL_MEANINGFUL_OUTPUT_V1.
- Automatic recognition.
- Automatic materiality/destination classification.
- Automatic authorization routing.
- Universal deduplication across source classes.
- End-to-end universal adapter production behavior.
- Future applicability, behavior change, outcome verification, and improvement.

## Hard stop boundary

Do NOT implement or deploy the adapter yet unless this contract/input selection is accepted as the single bounded causal proof.

Do NOT add a second persistence store.

Do NOT route the representative input through Smart Note.

Do NOT claim promotion success from storage alone.

Status: CONTRACT VALIDATED
Representative input: SELECTED
Production adapter: NOT IMPLEMENTED
Production proof: NOT CLAIMED
