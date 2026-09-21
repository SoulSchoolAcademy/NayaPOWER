# PROJECT INTELLIGENCE BRIDGE CONTRACT V1

STATUS: CANONICAL OPERATING CONTRACT
PROJECT: NayaNET
SENDER: GitHub / NayaPOWER
RECEIVER: NayaNET Intelligent Hub
BRIDGE: Project Intelligence Bridge

## PURPOSE

The Project Intelligence Bridge is the single canonical boundary between durable Project Intelligence in GitHub/NayaPOWER and living Project Intelligence in the NayaNET Intelligent Hub.

Closed loop:
SOURCE → PROJECT INTELLIGENCE → BRIDGE PACKET → RECEIVER → PERSIST → INDEX → PROJECT → RETRIEVE → RENDER → ACK → OUTCOME → LEARNING → PROJECT INTELLIGENCE

The bridge is governed transport and reconciliation, not a second memory authority.

## SENDER

Repository: SoulSchoolAcademy/NayaPOWER.
The sender resolves live main HEAD at execution time. Recorded HEAD values are evidence metadata only.

## RECEIVER

Canonical Hub source: NAYANET/HUB/index.html.

The receiver MUST:
1. authenticate transport and owner where required;
2. validate schema, authority, provenance, freshness and privacy;
3. reject malformed, unauthorized, stale and replayed packets according to policy;
4. persist the transaction;
5. preserve project, packet, source and object identity;
6. create/update canonical intelligence;
7. index it for retrieval;
8. project eligible intelligence to the Hub;
9. return a machine-readable receipt.

## CANONICAL PACKET

Every packet contains:
- protocol = NAYANET_PROJECT_INTELLIGENCE_BRIDGE_V1
- packet_id
- packet_type = PROJECT_INTELLIGENCE
- project_id = NayaNET
- sender and receiver identity
- source_ref = exact Git commit SHA
- created_at
- freshness
- operating_context
- intelligence objects
- provenance with exact source paths and SHA-256 hashes
- authority status
- privacy
- idempotency_key
- success_condition
- evidence_required
- content_hash

## OPERATING CONTEXT

Every packet carries:
YOU ARE HERE
MISSION
NORTH STAR
PROJECT
CURRENT STATE
CURRENT BLOCK
PROVEN
UNKNOWN
BLOCKED
PROTECTED
SENDER
RECEIVER
BRIDGE
BRIDGE STATUS
CURRENT NEXT ACTION
WHY THIS ACTION
SUCCESS CONDITION
EVIDENCE REQUIRED
HANDOFF REQUIREMENT

This is the minimum context a cold Naya needs to continue without Shawn reconstructing the project.

## IDENTITY / PROVENANCE

Identity survives every hop:
project_id → source_ref → packet_id → object_id → receiver_event_id → receipt_id

The receiver preserves sender repository, source commit/path/hash, packet hash, packet ID, object identity, owner identity where applicable, and receipt identity.

A projection is never an anonymous copy.

## FRESHNESS

Freshness is evaluated against the exact source commit used by the packet.
- live HEAD is resolved at execution;
- source_ref is immutable;
- newer packets may supersede older packets;
- older packets never silently overwrite newer intelligence;
- supersession is explicit;
- stale proof cannot certify a newer source state.

## CHANGE SEMANTICS

Supported operations:
UPSERT — create/update an intelligence object.
SUPERSEDE — replace an older object while preserving lineage.
RETRACT — remove an object from active projection while retaining audit lineage.
NO_CHANGE — no new material.

Historical truth remains recoverable.

## IDEMPOTENCY / REPLAY

The same idempotency_key produces the same logical receiver transaction. Replay never creates duplicate intelligence. The receiver returns the original receipt or an equivalent replay-safe acknowledgement.

## RECEIVER ACK

HTTP success alone is NOT proof.

A verified acknowledgement contains:
status = ACCEPTED or COMPLETED
packet_id
project_id
source_ref
content_hash
receiver_transaction_id
receiver_event_id
persisted = true
indexed = true
projected = true
receipt_id
accepted_at

Missing required fields means NOT VERIFIED.

## RECEIVER READY GATE

READY requires one real transaction proving:
RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT → RETRIEVE → RENDER → ACKNOWLEDGE

Partial implementation is not READY.

## COLD-NAYA RULE

A cold Naya:
1. reads the canonical cold-start index;
2. reads the operating context;
3. resolves live HEAD;
4. verifies freshness;
5. reads current block/state/proof;
6. selects exactly one authorized next action;
7. executes;
8. verifies the actual result;
9. records intelligence/activity/state as applicable;
10. leaves successor continuity.

No conversational explanation from Shawn is part of the protocol.

## SHAWN-MIDDLEWARE ELIMINATION

A blocked boundary MUST persist:
- exact blocked boundary;
- why blocked;
- authority required;
- what is already complete;
- what can proceed independently;
- exact continuation trigger;
- evidence required after unblocking.

Never leave a vague "Shawn needs to fix this" state.

## PRIVACY

Project Intelligence is private by default:
PRIVATE → SHARED_BY_CONSENT → PUBLIC_BY_DECISION

Crossing the bridge does not broaden visibility.

## BRIDGE STATES

NOT_READY
READY_TO_SEND
SENDING
ACCEPTED
COMPLETED
STALE
REPLAY_REJECTED
UNAUTHORIZED
INVALID
BLOCKED
CONFLICTED

Unknown is never promoted to completed.

## HOME RUN ACCEPTANCE

The bridge is PROVEN only when a cold-Naya-controlled test demonstrates:
GitHub canonical intelligence
→ packet from live HEAD
→ authorized receiver
→ persisted with identity/provenance
→ indexed
→ projected
→ retrieved
→ rendered
→ receipt returned and verified
→ outcome/learning recorded
→ fresh Naya retrieves the resulting intelligence
→ fresh Naya continues without Shawn supplying missing context.

The test includes duplicate/replay, stale, malformed, unauthorized, wrong-owner isolation where applicable, exact source SHA, packet hash, receiver event, receipt, and fresh-context retrieval.

## DEFINITION OF DONE

Operational completion requires:
- packet schema implemented;
- sender builds automatically;
- receiver accepts automatically;
- receipt verification automatic;
- freshness/current state automatic;
- Smart Note/Activity/intelligence projection automatic where applicable;
- cold restore works;
- successor retrieval works;
- no manual Shawn context transfer.

Until then the bridge remains NOT PROVEN.

## GOVERNING QUESTION

What intelligence crossed the boundary, how do we know it arrived intact, what became true because it arrived, and can the next Naya continue from that truth without being told?
