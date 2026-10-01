# 🔱 NayaPOWER CONNECT-01 — Relationship-Aware Intelligence Retrieval Specification V1

**Status:** PROPOSED EXECUTABLE SPECIFICATION  
**Authority:** NayaPOWER System North Star + Nine Master Nodes Enforceable Specification V1  
**Primary Node:** MN-06 CONNECT  
**Related Nodes:** KNOW, PROVE, VERIFY, LEARN, EVOLVE  
**Scope:** One bounded capability only: relationship-aware retrieval over canonical Naya intelligence.  
**Implementation boundary:** Integrate with the existing canonical intelligence/Receiver path. Do not create a competing canonical memory store.

---

## 1. Purpose

CONNECT-01 makes relationships first-class retrieval context.

The capability MUST allow Naya to answer a question using both:

1. semantic relevance; and
2. governed relationships among canonical intelligence objects.

The objective is not to build a generic graph database or a new RAG subsystem. The objective is to prove that **applicable relationships materially improve retrieval and continuity**.

> Semantic retrieval answers “what is similar?”  
> Relationship retrieval answers “what is connected, through what relationship, and is that relationship applicable here?”

CONNECT-01 is successful only when the relationship path changes the retrieved context or outcome in a deterministic test.

---

## 2. Non-goals

CONNECT-01 MUST NOT:

- create a second canonical intelligence store;
- replace vector/semantic retrieval;
- require Neo4j or another new database;
- redesign the Hub;
- create a graph visualization;
- introduce autonomous relationship generation without evidence;
- create new authority;
- widen privacy scope;
- promote candidate relationships to verified truth;
- change constitutional law;
- implement generalized learning or self-building.

Only the minimum storage, retrieval, validation, and test machinery required for CONNECT-01 is in scope.

---

## 3. Canonical objects

The canonical intelligence object remains the existing Naya Node / Intelligent Block.

A relationship is metadata connecting two canonical intelligence objects.

~~~json
{
  "relationship_id": "REL-...",
  "source_id": "IB-...",
  "target_id": "IB-...",
  "type": "SUPPORTS",
  "status": "ACTIVE",
  "owner_id": "...",
  "scope": "...",
  "created_at": "ISO-8601",
  "effective_at": "ISO-8601|null",
  "expires_at": "ISO-8601|null",
  "supersedes_relationship_id": null,
  "provenance": [],
  "evidence": [],
  "authority_context": {},
  "epistemic_state": "CANDIDATE",
  "applicability": {}
}
~~~

### Required semantics

- source_id and target_id MUST reference canonical intelligence identities.
- relationship_id MUST be globally unique within the canonical intelligence boundary.
- type MUST be from the allowed V1 vocabulary.
- status MUST be explicit.
- ownership/scope MUST be preserved.
- timestamps MUST be preserved when temporal applicability matters.
- provenance MUST identify how the relationship was established.
- evidence MUST support any claim that materially affects trust or action.
- epistemic_state MUST NOT exceed available evidence.
- relationship metadata MUST NOT create authority.
- a relationship MUST NOT silently widen visibility.

---

## 4. Allowed V1 relationship vocabulary

Keep V1 intentionally small.

### Structural

- RELATED_TO
- PART_OF
- CONTAINS
- DEPENDS_ON

### Knowledge / epistemic

- SUPPORTS
- DERIVES_FROM
- REFINES
- CONTRADICTS

### Temporal

- SUPERSEDES
- SUPERSEDED_BY
- PRECEDES
- FOLLOWS

### Operational

- REQUIRES
- ENABLES
- PRODUCES
- APPLIES_TO

### Learning / continuity

- LEARNED_FROM
- IMPROVES
- INVALIDATES
- CREATED_BY
- HANDED_TO
- CONTINUES

No new relationship type is required for CONNECT-01. If implementation discovers a missing type, stop and document the gap rather than silently expanding the vocabulary.

---

## 5. Relationship status and epistemic state

Relationship status:

- ACTIVE
- SUPERSEDED
- RETIRED
- CONFLICTED

Epistemic state:

- UNKNOWN
- CANDIDATE
- SUPPORTED
- VERIFIED

Mandatory invariants:

~~~text
UNKNOWN != VERIFIED
CANDIDATE != VERIFIED
SUPPORTED != VERIFIED
SUPERSEDED != CURRENT
CONFLICTED != UNQUALIFIED CURRENT TRUTH
~~~

VERIFIED MUST require evidence appropriate to the relationship claim.

PROVE owns the truth/provenance boundary. CONNECT may retrieve and rank relationships but MUST NOT upgrade epistemic state.

---

## 6. Canonical Supabase boundary

The existing canonical persistence boundary remains authoritative.

CONNECT-01 MUST integrate with the existing Intelligent Block / Receiver persistence model.

Preferred implementation:

~~~text
canonical intelligence objects
        +
canonical relationship records
        ↓
same governed persistence boundary
~~~

A new relationship table MAY be introduced only if the current schema does not already provide an equivalent canonical relationship representation.

If a new table is required, its conceptual contract is:

~~~text
nayanet_intelligence_relationships

relationship_id
source_id
target_id
relationship_type
status
owner_id
scope
created_at
effective_at
expires_at
supersedes_relationship_id
epistemic_state
provenance
evidence
authority_context
applicability
metadata
~~~

Implementation MUST first inspect the live schema and reuse an existing equivalent representation if present.

### Database invariants

At minimum:

1. relationship_id unique.
2. source and target identities valid.
3. relationship type constrained to V1 vocabulary.
4. owner/scope cannot be null where canonical intelligence requires them.
5. epistemic state constrained to allowed values.
6. supersession references valid relationship identity.
7. indexes support lookup by source_id, target_id, and relationship_type.
8. row-level security/privacy MUST follow the existing canonical intelligence boundary.
9. relationship retrieval MUST NOT bypass owner/scope restrictions.

No production schema migration is authorized merely because this specification exists. Implement only after confirming the current schema boundary.

---

## 7. Relationship creation contract

CONNECT-01 MAY consume relationships produced by existing intelligence workflows.

For V1, relationship creation SHOULD be explicit/deterministic.

A relationship creation event MUST preserve:

~~~text
who/what created it
when
source
target
relationship type
scope/owner
provenance
epistemic state
supporting evidence, if claimed
~~~

An LLM suggestion alone MUST produce at most CANDIDATE.

The system MUST NOT silently treat generated relationship text as verified truth.

---

## 8. Retrieval algorithm

CONNECT-01 retrieval MUST follow this conceptual sequence:

~~~text
QUERY
  ↓
IDENTIFY USER / OWNER / SCOPE
  ↓
SEMANTIC RETRIEVAL
  ↓
SELECT SEED INTELLIGENCE
  ↓
EXPAND GOVERNED RELATIONSHIPS
  ↓
FILTER OWNER / PRIVACY / AUTHORITY
  ↓
FILTER TEMPORAL VALIDITY
  ↓
FILTER SUPERSEDED / RETIRED
  ↓
SURFACE CONFLICTS
  ↓
ASSESS APPLICABILITY
  ↓
RANK CONNECTED CONTEXT
  ↓
RETURN MINIMUM SUFFICIENT CONTEXT
~~~

### V1 expansion

Default maximum relationship hops: **3**.

Default seed count: implementation-defined, but MUST be bounded and deterministic for the acceptance fixture.

The implementation MUST avoid unbounded graph traversal.

### Applicability precedence

When choosing between merely similar and explicitly applicable intelligence:

~~~text
applicable + authorized + current
    >
relevant + current
    >
merely similar
~~~

This is a routing preference, not a truth upgrade.

---

## 9. Retrieval result contract

A CONNECT-01 result MUST expose enough metadata for downstream reasoning and verification:

~~~json
{
  "query_id": "...",
  "seeds": [],
  "nodes": [],
  "relationships": [],
  "excluded": [],
  "conflicts": [],
  "retrieval_policy": {
    "max_hops": 3,
    "owner_scope": "...",
    "temporal_filter": true
  },
  "provenance": [],
  "epistemic_summary": {},
  "generated_at": "ISO-8601"
}
~~~

The result MUST distinguish:

- retrieved;
- excluded;
- conflicted;
- superseded;
- unknown.

It MUST NOT collapse these states into a single relevance score.

---

## 10. Privacy and authority

CONNECT-01 inherits the canonical NayaPOWER rules.

### Privacy

The system MUST enforce:

> Private by default. Shared by choice. Collective by consent. Public by decision.

A relationship between two objects MUST NOT make either object visible outside its authorized scope.

### Authority

Capability does not create authority.

Retrieval relevance does not create authority.

A relationship does not create authority.

A highly connected Node does not become authoritative merely because it is highly connected.

LAW remains the authority boundary.

CONNECT MUST return sufficient authority context for downstream decisions when authority affects applicability, but MUST NOT grant permission.

---

## 11. Provenance

Every relationship materially used in a consequential answer/action MUST be traceable to its provenance.

At minimum:

~~~text
relationship_id
source_id
target_id
relationship_type
creator/source
created_at
evidence references
epistemic state
~~~

Where a relationship came from an event, the event identity SHOULD be preserved.

Where a relationship changes, the prior relationship state MUST remain reconstructable through the canonical lineage mechanism.

---

## 12. Temporal and supersession rules

If relationship A is superseded by relationship B:

~~~text
A → SUPERSEDED
B → ACTIVE
~~~

Retrieval MUST NOT return A as unqualified current context.

If both are materially relevant historically, A MAY be returned under an explicit historical/superseded classification.

If temporal validity cannot be determined and the distinction matters, return an explicit UNKNOWN/ambiguity boundary rather than assuming current truth.

---

## 13. Contradiction rules

If:

~~~text
A → SUPPORTS → B
~~~

and:

~~~text
C → CONTRADICTS → B
~~~

both within applicable scope, CONNECT MUST surface the conflict when it could affect the answer.

It MUST NOT average conflicting claims into false certainty.

Reconciliation belongs to the applicable KNOW/PROVE/LEARN flow.

---

## 14. Node mapping

CONNECT-01 is owned by MN-06 CONNECT.

| Node | CONNECT-01 responsibility |
|---|---|
| SELF | establishes identity, owner, scope, current intent |
| LAW | establishes authority/consent constraints |
| ACT | consumes retrieved context for authorized execution |
| KNOW | owns canonical intelligence objects |
| PROVE | owns evidence, provenance, epistemic status |
| CONNECT | stores/queries/ranks governed relationships |
| VERIFY | independently verifies the claimed retrieval/result behavior |
| LEARN | may consume verified outcomes; not part of initial implementation |
| EVOLVE | successor continuity consumes retained relationship context; not part of initial implementation |

CONNECT-01 MUST NOT duplicate responsibilities owned by these Nodes.

---

## 15. Sender → Receiver → Hub boundary

CONNECT-01 must support the existing continuity architecture without redesigning the surfaces.

### Sender

May produce:

~~~text
Intelligent Block
+
relationship metadata
+
evidence/provenance
+
next-action context
~~~

### Receiver

Remains the canonical persistence boundary.

It MUST preserve:

- canonical identity;
- owner/scope;
- relationship metadata;
- provenance;
- epistemic state;
- temporal/supersession information.

### Hub

Consumes a distilled projection.

The Hub MUST NOT become a second graph store or canonical intelligence source.

The Hub MAY display relationship-derived context such as:

~~~text
WHY THIS MATTERS
WHAT IT CONNECTS TO
WHAT CHANGED
WHAT SUPPORTS IT
WHAT IS UNKNOWN
WHAT IS NEXT
~~~

Hub UI work is explicitly OUT OF SCOPE for CONNECT-01.

---

## 16. Exact black-box acceptance fixture

Use a deterministic synthetic fixture. Do not depend on live project data for the primary test.

Create six canonical intelligence objects:

~~~text
IB-A = "Deployment action was completed."
IB-B = "Deployment completion depends on verification."
IB-C = "Verification proof confirms deployment outcome."
IB-D = "Older deployment verification procedure."
IB-E = "Owner-scoped project context."
IB-F = "Unrelated semantic distractor."
~~~

Relationships:

~~~text
IB-A --PRODUCES--> IB-B
IB-B --REQUIRES--> IB-C
IB-C --SUPERSEDES--> IB-D
IB-E --APPLIES_TO--> IB-A
IB-F --RELATED_TO--> unrelated context
~~~

Mark:

~~~text
IB-C → VERIFIED
IB-D → SUPERSEDED
IB-E → ACTIVE
IB-F → ACTIVE
~~~

Question:

> "What evidence should I use to establish whether the deployment outcome is actually verified?"

### Expected relationship path

~~~text
IB-A
 ↓ PRODUCES
IB-B
 ↓ REQUIRES
IB-C
~~~

IB-D MUST NOT be selected as current evidence because it is superseded.

IB-E MAY be selected only when owner/scope/applicability match.

IB-F MUST NOT displace the connected evidence merely because it is semantically similar.

---

## 17. Control experiment

Run the exact question twice.

### Control A — semantic retrieval only

Disable relationship expansion.

Record the retrieved objects and answer.

### Treatment B — CONNECT-01

Enable relationship expansion.

Record:

- seeds;
- relationship path;
- exclusions;
- final context;
- answer.

### Required observation

The treatment MUST retrieve the connected evidence path through IB-B → IB-C and exclude IB-D as superseded.

The test MUST demonstrate that the relationship path changes the retrieved context materially.

If semantic-only retrieval happens to produce the same correct context, the test does NOT prove CONNECT-01. Adjust the deterministic fixture so the control and treatment differ.

---

## 18. PASS criteria

CONNECT-01 = PASS only if ALL are true:

1. canonical identities are preserved;
2. relationship records persist through the canonical boundary;
3. allowed relationship vocabulary is enforced;
4. owner/privacy scope is enforced;
5. authority is not created by retrieval;
6. provenance is retained;
7. epistemic state is retained and not silently upgraded;
8. superseded relationships/objects are filtered from current context;
9. bounded multi-hop traversal works;
10. contradiction state is surfaced where material;
11. relationship-aware retrieval returns the expected path;
12. semantic-only control differs materially where the fixture requires it;
13. independent verification confirms the expected retrieval path;
14. no second canonical memory store is introduced;
15. existing unrelated retrieval behavior does not regress.

---

## 19. FAIL criteria

CONNECT-01 = FAIL if any of the following occurs:

- relationship exists only in transient memory;
- canonical identity is duplicated;
- relationship bypasses privacy scope;
- retrieval grants authority;
- candidate relationship is treated as verified without evidence;
- superseded context is silently presented as current;
- traversal is unbounded;
- conflict is silently collapsed;
- provenance is lost;
- control/treatment cannot be distinguished;
- result cannot be independently verified;
- implementation creates a competing canonical store;
- unrelated existing retrieval behavior regresses.

---

## 20. Evidence receipt

A PASS receipt MUST include:

~~~json
{
  "test_id": "CONNECT-01",
  "status": "PASS",
  "commit_sha": "...",
  "kernel_version": "...",
  "schema_version": "...",
  "fixture_id": "...",
  "query_id": "...",
  "control_result": {},
  "treatment_result": {},
  "relationship_paths": [],
  "excluded_items": [],
  "privacy_checks": [],
  "authority_checks": [],
  "provenance_checks": [],
  "temporal_checks": [],
  "independent_verification": {},
  "regression_checks": [],
  "unknowns": [],
  "next_action": "..."
}
~~~

A PASS MUST NOT be emitted if an essential field is unknown.

NOT_PROVEN is a valid verification outcome.

---

## 21. Required implementation tests

Minimum test classes:

### Schema tests

- relationship type validation;
- identity validation;
- status validation;
- epistemic-state validation;
- uniqueness;
- supersession reference validation.

### Security tests

- owner isolation;
- unauthorized relationship visibility;
- authority non-escalation.

### Retrieval tests

- one-hop retrieval;
- two-hop retrieval;
- three-hop retrieval;
- max-hop enforcement;
- supersession filtering;
- temporal filtering;
- contradiction surfacing;
- applicability filtering.

### Provenance tests

- relationship provenance survives persistence;
- relationship provenance survives retrieval;
- epistemic state survives persistence/retrieval.

### Regression tests

- existing Intelligent Block retrieval remains functional;
- existing Receiver behavior remains functional;
- no duplicate canonical intelligence path is introduced.

### Acceptance test

The exact fixture in Section 16 MUST pass independently of production data.

---

## 22. Implementation discipline

Coda MUST:

1. read the canonical North Star, Nine Master Node specification, current control-plane state, and current relevant retrieval/Receiver implementation;
2. inspect the existing Supabase schema before proposing migrations;
3. reuse existing canonical structures where equivalent;
4. implement only CONNECT-01;
5. add tests before or alongside implementation;
6. produce a proof receipt;
7. stop if the requested change would require a new authority model, new canonical memory store, constitutional change, or unrelated product work;
8. put implementation in a PR;
9. leave the exact next action in the Team Naya board.

Do not mix CONNECT-01 with Hub redesign, Welcome/front-door work, generalized learning, value calculus, or unrelated deployment polish.

---

## 23. Definition of done

CONNECT-01 is DONE only when:

~~~text
SPEC
 ↓
SCHEMA / EXISTING MODEL RECONCILED
 ↓
IMPLEMENTATION
 ↓
UNIT / INTEGRATION TESTS
 ↓
CONTROL vs TREATMENT
 ↓
INDEPENDENT VERIFICATION
 ↓
PROOF RECEIPT
 ↓
PR REVIEW
~~~

Documentation without behavioral proof is NOT DONE.

Implementation without independent verification is NOT VERIFIED.

---

## 24. Strategic outcome

The purpose of CONNECT-01 is not to make Naya “have a graph.”

The purpose is to prove:

> **Naya can reconstruct connected, applicable, governed intelligence instead of relying only on semantic similarity.**

This is the first concrete bridge from the ratified CONNECT contract to relationship-driven runtime reasoning.

---

## 25. Explicit boundary for future work

Future capabilities may build on CONNECT-01:

~~~text
CONNECT-02  relationship-aware successor continuity
CONNECT-03  relationship-aware learning
CONNECT-04  cross-Node causal graph
CONNECT-05  network/collective intelligence graph
~~~

These are NOT part of CONNECT-01.

**ONE CAPABILITY. ONE BOUNDARY. ONE PROOF.**

---

## 26. Final invariant

> **Relationships are intelligence context, not authority.**

> **A relationship is useful only when its provenance, scope, temporal validity, epistemic status, and applicability remain intact.**

> **The graph is a projection/index of the canonical intelligence system, never a competing brain.**
