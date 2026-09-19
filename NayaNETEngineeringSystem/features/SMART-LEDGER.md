# Smart Ledger — Engineering Specification

## What / why
Smart Ledger is the integrity/evidence/lineage layer for meaningful system events. It makes consequential activity reconstructable: what happened, who/what acted, under what authority, with what result and evidence.

## Human interface
A clear ledger view should show chronological events with filters for actor, object, action, time, status and verification. A detail view should expose lineage: source/context → authority → action → result → evidence/receipt. It should never pretend that a ledger entry itself proves the underlying claim.

## Front end requirements
- Authenticated ledger route.
- Timeline/table with event type, actor, target, time, state.
- Detail drawer/page with lineage and evidence references.
- Filters/search and stable deep links.
- Clear distinction between recorded, observed and verified.
- Unauthorized evidence must be hidden, not merely disabled.

## Back end requirements
- Append meaningful immutable or tamper-evident event records according to the canonical implementation.
- Stable event IDs, timestamps, actor, authority scope, target, source/correlation and result.
- Preserve receipts/provenance.
- Enforce access to ledger data.
- Support idempotent recording where retries can occur.
- Do not use Ledger as a replacement for domain state or canonical intelligence.

## Data / API contract
Conceptual event: `event_id, event_type, actor_id, actor_type, authority_scope, target_type, target_id, source_refs, correlation_id, occurred_at, recorded_at, result_state, verification_state, evidence_refs, receipt_ref`. Read APIs should support scoped timeline/detail retrieval. Exact routes follow existing runtime contracts.

## Connections
`execution → Ledger`; `Smart Share → sharing evidence`; `Smart Mail/Spaces → communication events`; `Smart Feed → activity provenance`; `PIS/CIS → intelligence lineage`; `verification → verified state`; `CCT → connected chain`.

## Verification
Create a real consequential event, observe its receipt/ledger record, retrieve it freshly, verify actor/authority/target/result lineage, test replay/idempotency, and test unauthorized access.

## Current state
**DEFINED; portions may be implemented in the existing runtime.** `.naya/14` and current production-closure artifacts must be treated as source-of-truth for actual state.

## Gap / next action
Map the existing production Smart Ledger implementation to this contract and prove the complete authenticated write → receipt → fresh retrieval chain.

## Source authority
`.naya/2026-09-11-NAYAPOWER-14-SMART-LEDGER-SMART-NOTE.md`; `.naya/2026-09-12-NAYAPOWER-39-CROSS-SYSTEM-EVENT-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-45-HUB-EVENT-INTEGRATION-PIS-ADAPTER-CONTRACT.md`; `.naya/2026-09-19-SMART-LEDGER-PRODUCTION-CLOSURE.md`.
