# Engineering Truth Law V1

**Status:** CANONICAL BUILD CONTRACT

## Truth hierarchy
`CANONICAL SOURCE → RUNTIME OBSERVATION → VERIFIED RECEIPT → DERIVED CLAIM → UNKNOWN`

The exact ordering depends on the claim type; no lower-confidence artifact may overwrite a higher-confidence canonical fact.

## Mandatory distinctions
`UNKNOWN ≠ PASS`
`BLOCKED ≠ PASS`
`IMPLEMENTED ≠ VERIFIED`
`VERIFIED ≠ PRODUCTION_PROVEN`
`RETRIEVED ≠ AUTHORIZED`
`CANDIDATE ≠ PROMOTED`

## Engineering laws
1. Every critical claim names its source, revision, scope, and evidence.
2. Current runtime evidence outranks stale narrative.
3. Stale receipts are marked stale; they are never silently reused.
4. Conflicts are surfaced, not averaged away.
5. A change is complete only when implementation, test, verification, and current receipt agree.

## Acceptance
A truth audit can identify the canonical source for every race-critical claim and rejects unsupported PASS status.
