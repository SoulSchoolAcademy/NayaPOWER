# Contract 06 — Room V1

**Owns:** behavioral contract for each Hub surface.  
**Does not own:** canonical intelligence storage or global authority.

## Required 12-field room contract

Every Room MUST declare:

1. IDENTITY
2. PURPOSE
3. HUMAN QUESTION
4. INPUTS
5. ACTIONS
6. CREATION
7. RETRIEVAL
8. AUTHORITY
9. OUTPUT
10. EVIDENCE
11. RELATIONSHIPS
12. NEXT

## Mandatory rules

A Room MUST have one declared purpose.

A Room MUST NOT create a private copy of canonical intelligence for UI convenience.

Durable creation MUST use the canonical Sender/Receiver path.

A Room MUST distinguish loading, empty, failed, unavailable, unknown, and verified states.

A Room MUST expose evidence appropriate to consequential actions.

## Product naming

Current terminology MUST follow the latest authoritative Hub alignment. **SmartConnect is current terminology; Smart Share is historical where superseded.**

## Anti-patterns

Do not build a room merely because the Hub needs another page.

Do not add a capture control whose canonical creation path does not exist.

Do not call a visual shell complete when retrieval/action/evidence is unproven.

## Acceptance

A Room is complete only when its 12-field contract is populated, canonical inputs are identified, creation/retrieval is proven, and its evidence boundary is defined.