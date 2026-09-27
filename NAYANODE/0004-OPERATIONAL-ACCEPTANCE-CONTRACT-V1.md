# Naya Node Operational Acceptance Contract V1

## Objective

Prove that the Nine-Node kernel is a living operating system rather than a collection of stored objects.

## Acceptance ladder

| Level | Required proof |
|---|---|
| A1 EXISTS | Canonical Node definitions and persistent representations exist |
| A2 LOADS | Cold runtime loads all nine |
| A3 INVOKES | Runtime actually invokes the required Node responsibilities |
| A4 INFLUENCES | Node context changes an observable decision/output |
| A5 APPLIES | Changed output is actually used |
| A6 OUTCOME | Real task outcome is observed |
| A7 VERIFIES | Outcome has evidence sufficient for its claim |
| A8 LEARNS | Verified outcome changes future behavior |
| A9 COMPOUNDS | Later held-out work improves from prior learning |
| A10 SUCCEEDS | Cold successor inherits sufficient context and continues |
| A11 EVOLVES | System safely proposes/builds/tests/adopts an improvement |

## Required experiment

Run a consequential-but-reversible task in two comparable conditions:

### CONTROL
Nine-Node kernel disabled or unavailable.

### TREATMENT
Nine-Node kernel enabled.

Capture at minimum:

- task identifier;
- input/context hash;
- kernel version;
- Node versions;
- Node invocation trace;
- retrieved intelligence;
- retrieval rationale;
- decision/output;
- action;
- downstream consumer;
- outcome;
- verification evidence;
- learning candidate;
- future behavior;
- successor context.

## Required negative tests

At minimum test:

1. missing authority;
2. out-of-scope authority;
3. revoked authority;
4. stale intelligence;
5. conflicting intelligence;
6. poisoned Node content attempting to grant authority;
7. missing kernel Node;
8. failed retrieval;
9. failed verification;
10. continuity owner mismatch.

Every negative case must fail closed where required and retain a truthful evidence state.

## Passing rule

A test may be reported only at the highest level actually evidenced.

**BLOCKED is not PASS.**
**Implemented is not VERIFIED.**
**Verified is not PRODUCTION-PROVEN.**
