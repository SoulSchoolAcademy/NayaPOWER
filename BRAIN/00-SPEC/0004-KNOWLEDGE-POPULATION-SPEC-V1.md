# NayaPOWER Knowledge Population Specification V1

**Status:** CANONICAL SPECIFICATION — promotion/rejection contract defined  
**Objective:** Turn the existing knowledge bank into a connected, provenance-bound intelligence corpus without copying conversational bulk into the brain.

## Pipeline

```
SOURCE CORPUS
→ INVENTORY
→ EXTRACT
→ DISTILL
→ TYPE
→ RECONCILE
→ CONNECT
→ PROVE
→ PROMOTE
→ INDEX
```

## Required canonical object envelope

Every promoted proposition MUST contain, at minimum:

```text
stable_id
type
title
proposition
purpose
source_lineage[]
epistemic_state
status
applicability
relationships[]
authority_implications
proof_state
created_at
updated_at
```

Missing required fields cause **REJECTED / INCOMPLETE**, not implicit defaults.

## Required dispositions

Every source-derived proposition receives one disposition:

```
PROMOTE
MERGE
SUPERSEDE
RETAIN-AS-SOURCE
HISTORICAL
CONTRADICTED
UNKNOWN
ARCHIVE
```

A disposition is not itself proof. The proposition's evidence and epistemic state remain explicit.

## Promotion gates

A proposition may move to `CANONICAL` only when:

1. identity is stable and unique;
2. source lineage is resolvable;
3. type contract validates;
4. proposition is sufficiently distilled to stand alone;
5. applicability is explicit;
6. relationships are explicit or explicitly `[]` with a reason;
7. contradictions are surfaced;
8. authority implications are explicit;
9. proof state supports the requested status;
10. the canonical index accepts the object.

Otherwise the system MUST emit a machine-readable rejection/failure receipt containing:

```
object_id_or_candidate_id
disposition
failed_gate
reason
source_lineage
timestamp
validator_version
```

## Priority extraction

First extract:

1. system identity;
2. mission and North Star;
3. constitutional laws;
4. governance;
5. Nine Nodes;
6. canonical object model;
7. intelligence lifecycle;
8. memory/continuity;
9. graph/relationships;
10. proof/verification;
11. learning/compounding;
12. succession;
13. self-building;
14. NayaNET channels;
15. Hub boundary;
16. failure intelligence;
17. current reality;
18. acceptance tests.

Feature ideas that do not establish durable intelligence are not automatically promoted.

## Quality rule

The goal is not to maximize the number of canonical objects.

The goal is to maximize **useful, connected, verified intelligence with minimum unnecessary complexity**.

## Non-equivalence law

```
DISTILLED ≠ STRUCTURED
STRUCTURED ≠ VERIFIED
VERIFIED ≠ CANONICAL
CANONICAL ≠ CURRENTLY APPLICABLE
```

A later retrieval layer MUST evaluate applicability, freshness, scope and conflicts rather than assuming every canonical object belongs in working context.
