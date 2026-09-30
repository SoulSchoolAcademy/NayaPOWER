# Intelligent Graph Contract V1

**Status:** CANONICAL SPECIFICATION — live query semantics defined  
**Purpose:** Make relationships executable context rather than decorative metadata.

The graph is a typed semantic overlay on canonical objects. It is not a second source of truth.

## Edge contract

```
relationship_id
relationship_type
source_id
target_id
status
epistemic_state
provenance[]
created_at
updated_at
```

A graph edge is a claim about a relationship and therefore requires provenance.

## Graph operations

```
FIND
GET
TRACE
COMPARE
EXPLAIN
VERIFY
CONNECT
SUPERSEDE
REPLAY
INHERIT
APPLY
```

## Runtime query contract

A relationship-aware retrieval request MUST define:

- requesting owner/subject;
- task or intent;
- starting object(s);
- allowed relationship types;
- maximum traversal depth;
- temporal boundary;
- scope/privacy boundary;
- minimum evidence state;
- conflict/supersession policy;
- context budget.

The retrieval result MUST return, for each selected object:

```
object_id
why_selected
relationship_path
provenance
epistemic_state
applicability
freshness
conflicts_or_exclusions
```

## Relationship expansion law

Relationship traversal MUST NOT bypass:

**owner → scope → provenance → epistemic state → temporal validity → supersession/conflict → context budget**

A related object that fails one of these gates is excluded or explicitly returned as excluded with a reason.

## Behavioral acceptance

CONNECT is proven only when:

```
SAME TASK
→ WITHOUT RELATIONSHIP CONTEXT
→ WITH RELATIONSHIP CONTEXT
→ DIFFERENT USABLE CONTEXT
→ DIFFERENT OR BETTER VERIFIED BEHAVIOR
```

A graph seed or successful query alone is not behavioral proof.

## Source-of-truth rule

The graph is a derived semantic overlay over canonical objects and relationships. Do not create a second canonical graph database merely to satisfy this contract.
