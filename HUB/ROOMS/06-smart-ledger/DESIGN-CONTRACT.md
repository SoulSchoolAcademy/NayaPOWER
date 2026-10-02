# Smart Ledger — Design Contract V1

**Status:** PROPOSED · REVIEW OPEN
**Parent:** `HUB/DESIGN-CONTRACT.md`
**Metaphor:** **THE BLACK BOX / PROOF ROOM**
**Theme:** Yellow / Gold — evidence, consequence, durable proof

## Creative intent
Make system accountability legible and beautiful. A nontechnical human should understand a consequential chain without reading logs.

## Center-workspace composition
A calm gold-accented trust header sits above a large chronological causal timeline. Entries expand into receipt/evidence detail. Filters are compact and meaningful. Failed/unverified chains remain visible rather than disappearing.

## Signature instrument
The causal timeline / receipt chain.

## Visual hierarchy
Action + result first, authority and verification second, raw receipt/evidence on demand. Distinguish stages visually with exact language.

## Living-depth expression
Gold highlights consequence and proof. Verified nodes can illuminate subtly; unresolved/failed stages use semantic warning states without turning the room red everywhere.

## Motion / liveness
Timeline updates only on real new receipts/events. Verification completion can settle into a final state; no decorative scanning animations.

## Naya presence
Naya translates receipts into human language, points out missing verification and can trace 'why did this happen?' without asserting beyond evidence.

## States
LOADING · EMPTY · READY · BLOCKED · UNAUTHORIZED · NOT_VERIFIED · VERIFIED · ERROR · OFFLINE · UNKNOWN · DISABLED.

## Responsive
Chronological chain first. Receipt detail opens full-screen; filters collapse into a sheet. Stage vocabulary remains visible.

## Must never become
- financial ledger metaphor
- raw developer log dump
- green executor output treated as verified
- hidden failed events
- proof by animation

## Non-regression anchors
- RECEIVED/AUTHORIZED/EXECUTED/VERIFIED distinction
- receipt IDs
- authority/source visibility
- chronological durable record
- evidence links

## Design acceptance
The room must be unmistakably NayaNET, make the signature instrument obvious, and preserve real state/proof without generic-dashboard drift.
