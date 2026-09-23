# Universal Meaningful-Output Promotion — Read-Only Archaeology Receipt

Date: 2026-09-23
Scope: P0 universal meaningful-output promotion
Mode: READ-ONLY ARCHAEOLOGY + CONTRACT DERIVATION
Production mutation: NONE
Control-plane frontier: NOT ADVANCED

## Evidence inspected

1. NAYANET/HUB/src/app/HubRouter.tsx — canonical Hub route inventory.
2. NAYANET/HUB/src/app/SmartNoteSurface.tsx — authenticated Smart Note capture, canonical ingress, receipt requirement, fresh retrieval verification.
3. NAYANET/HUB/public/assistant-runtime.js — generic authenticated record primitive plus specialized captureSmartNote ingress.
4. supabase/functions/nayanet-compound-intelligence/index.ts — intelligence_commit persistence/projection/learning/checkpoint/Intelligent Block rung.
5. NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx — downstream intelligence actions and their shared cognition/runtime persistence.
6. NAYANET/HUB/src/app/IntelligenceTodaySurface.tsx — projection over primary intelligence, not a second store.
7. NAYANET/HUB/src/app/ReportsSurface.tsx — time-horizon projection over canonical intelligence.
8. NAYANET/HUB/src/app/NayaPlaySurface.tsx — canonical event playback plus governed action recording.
9. .naya/intelligence/PROMOTION-ENGINE-V1-CONTRACT.md — existing ingest/dedup/materiality/classification/authorization/promotion/receipt/verification/effectiveness model.
10. .naya/contracts/SMART-NOTE-PROPOSAL-CONTRACT-V1.json — existing proposal/governance boundary and explicit anti-second-store rules.

## Output-surface inventory

- Smart Note: canonical capture/promotion ingress.
- Intelligence / Feed: canonical intelligence consumer/projection.
- Intelligence Today: intelligence summary projection.
- Intelligence Library: canonical retrieval/projection.
- Smart Feed actions: favorite, save, love/like, rating, comment, apply/use, share, Space and connection actions.
- Smart Mail: governed communication output with separate authority/receipt path.
- Smart Share: governed publication output with consent/provenance path.
- Smart Spaces: governed context/action output.
- Smart Lists: governed organization/action output.
- Connections: governed relationship output.
- Dream: governed replay/learning-candidate output.
- Reports: derived time-horizon projection.
- Naya Play: human experience output consuming canonical events.
- Smart Ledger: evidence/accountability projection, not an intelligence source.

## Key architectural finding

The smallest universal adapter should not replace any existing domain boundary.

It should normalize the common semantic boundary before destination-specific authorization/execution:

MEANINGFUL OUTPUT
→ RECOGNIZE
→ NORMALIZE
→ DEDUPLICATE
→ CLASSIFY
→ AUTHORIZE
→ ROUTE TO EXISTING CANONICAL DESTINATION
→ PRESERVE SOURCE PROVENANCE
→ RECEIPT
→ VERIFY

The adapter is a routing/normalization contract, not a new persistence system.

## Smallest proposed adapter contract: UNIVERSAL_MEANINGFUL_OUTPUT_V1

### Required identity

- output_id: stable idempotent identity.
- output_version: integer version.
- event_at: timezone-aware timestamp.
- source_ref: canonical originating event/output reference.
- source_type: conversation | execution | tool_result | document | existing_intelligence | other.

### Required semantic payload

- title
- content
- meaning: why the output may matter.
- materiality: LOCAL | REUSABLE | SYSTEMIC | UNKNOWN.
- proposed_use: justified future use.
- applicable_scope: explicit scope and limits.
- uncertainties: array, including empty when none are known.

### Required evidence/provenance

- provenance_refs: non-empty source/evidence references.
- provenance_hash: when available.
- evidence_state: OBSERVED | RECORDED | TESTED | VERIFIED | UNKNOWN.
- source_event_id: existing canonical event identity when one exists.

### Required governance

- privacy: PRIVATE | SHARED_BY_CHOICE | COLLECTIVE_BY_CONSENT | PUBLIC_BY_DECISION.
- authority_ref: required for consequential/non-private destinations.
- requested_action: PROPOSE_ONLY | CAPTURE_IF_AUTHORIZED | ROUTE_IF_AUTHORIZED.
- destination_class: knowledge | procedure | checklist | test | contract | architecture | mission_state | guardrail | existing_intelligence | other.

### Required routing result

- decision: ACCEPT | PROPOSE | REJECT | BLOCKED | UNKNOWN.
- canonical_destination: resolver-selected existing destination.
- canonical_event_id: existing event identity after accepted routing.
- receipt_ref: durable machine receipt when execution occurs.

## Hard rules

1. Recognition never grants authority.
2. Recognition never establishes truth.
3. A meaningful output is not automatically a Smart Note.
4. Reuse existing canonical persistence and evidence boundaries.
5. No second intelligence database, feed, memory store, ledger, or governance kernel.
6. Private source remains private unless explicit consent/authority is satisfied.
7. UNKNOWN and BLOCKED remain non-success states.
8. Destination-specific authority remains owned by the existing destination boundary.
9. Deduplication must not silently merge conflicting provenance.
10. Preserve original source identity and uncertainty.
11. Promotion verification is distinct from storage success.
12. Future learning/improvement is distinct from promotion success.

## What this archaeology proves

- Multiple meaningful-output surfaces already exist.
- They converge on a small set of canonical persistence/runtime primitives rather than independent memory stores.
- intelligence_commit is the smallest existing proven promotion rung available for generalization.
- Domain-specific consequential actions remain behind their own authority boundaries.
- A universal adapter can therefore be a semantic normalization and routing layer over existing canonical destinations without introducing a second intelligence store.

## What this archaeology does NOT prove

- Universal automatic recognition across every Naya output.
- Universal automatic promotion.
- A production universal adapter implementation.
- Automatic destination selection for governance-sensitive outputs.
- Complete coverage of every possible Naya output source.
- End-to-end universal promotion runtime behavior.

## Causal boundary

The next executable proof should test only:

one representative non-Smart-Note meaningful output
→ UNIVERSAL_MEANINGFUL_OUTPUT_V1 normalization
→ existing canonical destination selection
→ existing authorization gate
→ existing canonical persistence
→ source/provenance identity preserved
→ independent retrieval/receipt verification.

No production mutation should occur until the adapter contract itself is independently accepted and the representative output class is selected from evidence.

## Status

READ-ONLY ARCHAEOLOGY COMPLETE
CONTRACT DERIVED: YES
PRODUCTION IMPLEMENTATION: NOT STARTED
PRODUCTION PROOF: NOT CLAIMED
READINESS FRONTIER: NOT ADVANCED
