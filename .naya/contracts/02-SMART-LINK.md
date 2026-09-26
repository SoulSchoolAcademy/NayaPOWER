# Contract 02 — Smart Link V1

**Owns:** exact semantic meaning and verification of the canonical human-readable Smart Link.  
**Does not own:** Receiver persistence, Hub runtime resolution, or generic evidence URLs.

## Exact definition

> **SMART LINK = direct navigable GitHub link to the canonical human-readable `smart-note.md` projection of an IB.**

Canonical shape:

`.naya/memory/smart-notes/YYYY/MM/DD/category/topic/IB-XXXXXX/smart-note.md`

## Never collapse these nouns

| Object | Meaning |
|---|---|
| Smart Link | Direct canonical GitHub Smart Note |
| Hub Deep Link | Runtime route that resolves an IB |
| Evidence Link | Receipt/event/test/workflow/commit evidence |

A Hub URL MUST NEVER be called a Smart Link.

## Verification gate

Before saying “Smart Link,” a Naya MUST establish:

1. direct GitHub `smart-note.md` target;
2. canonical path shape;
3. file exists on reported branch;
4. file contains the reported IB ID;
5. file corresponds to the Receiver-created canonical object.

If not established, report **SMART LINK: PENDING/UNKNOWN**, not an inferred URL.

## Handoff

A consequential Smart Note handoff SHOULD include IB ID, source event, receiver status, Smart Link, evidence links, Hub Deep Link if verified, and remaining unknowns.

## Acceptance tests

Receiver verified + repository projection pending = Smart Link PENDING.

Hub deep link verified + repository projection pending = Smart Link PENDING.

Projection exists with wrong IB ID = Smart Link CONFLICTED.

All verification conditions pass = Smart Link VERIFIED.