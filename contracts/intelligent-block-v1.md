# 🧠 NayaNET Intelligent Block V1 — Human-Readable Contract

**Schema:** `NAYANET_INTELLIGENT_BLOCK_V1`  
**Role:** Portable semantic representation of one canonical Intelligent Event.  
**Status:** Canonical contract.  
**Purpose:** Allow the same intelligence to travel between GitHub, Cloudflare, managed persistence, the Hub, ChatGPT, other AI agents, APIs, and future systems without silently changing meaning.

---

## 1. Fundamental rule

> **ONE INTELLIGENT EVENT → ONE CANONICAL MEANING → MANY AUTHORIZED REPRESENTATIONS**

The Intelligent Block is not a competing source of truth.

It is the portable, interpretable representation of the underlying event, claim, observation, decision, action, outcome, learning, or other intelligence object.

---

## 2. What every block must answer

An Intelligent Block should make it possible to determine, where applicable:

**WHO** — who created, observed, verified, authorized, executed, benefited, or was affected?

**WHAT** — what happened, what kind of object is it, and what is its subject?

**WHEN** — when did it occur, when was it observed, when did it become effective, and when is it valid?

**WHERE** — what project, scope, environment, audience, or context applies?

**WHY** — what was the intent, purpose, desired outcome, and expected value?

**HOW** — what action, method, or computation produced the result?

**WHY BELIEVE** — what source, provenance, evidence, and verification support the claim?

**WHO ALLOWS IT** — what authority, policy, consent, or constraints permit action?

**WHAT IS CONNECTED** — what caused, supported, contradicted, derived, depended on, verified, superseded, or otherwise relates to it?

**WHAT HAPPENED NEXT** — what outcome occurred?

**WHAT CHANGED** — what was learned?

**WHAT HAPPENS NEXT** — what successor action, question, test, owner, dependency, or event follows?

---

## 3. Required structural dimensions

A conforming block contains these top-level dimensions:

```text
identity
type
meaning
context
time
provenance
evidence
truth
authority
value
```

The following dimensions are strongly expected when materially applicable:

```text
actors
intent
relationships
action
outcome
learning
successor
lifecycle
integrity
projections
metadata
```

The portable V1 contract also requires an explicit lifecycle stage and a SHA-256 integrity hash so transport can be tested for semantic identity rather than visual similarity.

Unknown information must remain explicitly unknown rather than being invented.

---

## 4. Identity

Identity is stable across systems.

At minimum:

```text
object_id
event_id
version
schema_version
```

A representation may receive a local database ID, packet ID, or UI ID.

Those local IDs must not silently replace the canonical identity.

---

## 5. Truth

Truth is separate from confidence, authority, and value.

Canonical truth vocabulary:

```text
UNKNOWN
SUPPORTED
VERIFIED
CONFLICTED
REJECTED
SUPERSEDED
```

Evidence state may separately describe the proof level:

```text
ASSUMED
INFERRED
OBSERVED
IMPLEMENTED
VERIFIED
LIVE_VERIFIED
UNKNOWN
CONFLICTED
SUPERSEDED
REJECTED
BLOCKED
```

A system must never promote a claim merely because the language around it sounds certain.

---

## 6. Authority

Authority is a separate dimension:

```text
NONE
PROPOSED
AUTHORIZED
REVOKED
EXPIRED
```

The rule is absolute:

> **CAPABILITY DOES NOT CREATE AUTHORITY.**

A technically executable action may still be unauthorized.

---

## 7. Value

Value is separate from truth and authority.

Suggested fields:

```text
benefit
harm
cost
risk
effort
relevance
responsible_value
```

For Naya value evaluation, the bounded score is:

```text
-9 ... 0 ... +9
```

A prohibited action is **INVALID**, not merely zero-value.

---

## 8. Relationships

Relationships are evidence-bearing semantic connections.

Each relationship may contain:

```text
relationship_id
relation
source
target
reason
evidence_refs
authority_ref
created_at
effective_at
```

Supported relation vocabulary includes:

```text
DERIVED_FROM
REPRESENTS
PROJECTS
CAUSED
RESULTED_IN
TRIGGERED
SUPPORTS
CONTRADICTS
QUALIFIES
SUPERSEDES
VERIFIED_BY
DEPENDS_ON
REQUIRES
APPLIED_TO
PRODUCED_OUTCOME_FOR
LEARNED_FROM
GENERATED_LEARNING
CREATES_SUCCESSOR
AUTHORIZED_BY
REVOKED_BY
CONSTRAINED_BY
```

The relationship itself is part of the intelligence.

---

## 9. Projections

The same block can provide multiple authorized representations:

```text
human
naya
machine
simple
hub
api
```

These are representations, not separate truths.

For example:

**Human:** “The site now shows the verified Command Station.”

**Naya:** structured semantic statement with source and verification.

**Machine:** stable identifiers, status, hashes, and timestamps.

All three refer to the same canonical intelligence.

---

## 10. Lifecycle

An Intelligent Block may move through a lifecycle such as:

```text
CAPTURED
→ IDENTIFIED
→ CONTEXTUALIZED
→ SUPPORTED
→ VERIFIED
→ UNDERSTOOD
→ DISTILLED
→ OFFICIAL
→ SURFACED
→ APPLIED
→ MEASURED
→ LEARNED
→ RETAINED / SUPERSEDED
→ SUCCESSOR
```

This lifecycle is orthogonal to truth, authority, and value.

---

## 11. Outcome and learning

The preferred causal sequence is:

```text
ACTION
→ OUTCOME
→ INTERPRETATION
→ LEARNING
→ REUSE
```

An AI must not declare learning merely because it wrote a lesson.

Learning becomes stronger when future application demonstrates that the retained lesson improves a later result.

---

## 12. Portability rule

The block may travel as:

```text
Markdown
YAML
JSON
database row
API payload
event
stream message
UI projection
AI context
```

The encoding can change.

The semantic contract cannot silently change.

---

## 13. Minimum trustworthy block

A minimum meaningful block can say:

```text
WHO: known / unknown
WHAT: known
WHEN: known
WHERE: scope known / unknown
WHY: known / unknown
EVIDENCE: present / absent
TRUTH: state
AUTHORITY: state
VALUE: state
```

That is better than a richer-looking block containing fabricated detail.

---

## 14. Integrity and round-trip test

The V1 block carries:

```text
integrity.algorithm = SHA-256
integrity.content_hash = SHA-256(canonical block without integrity)
```

Canonical hashing must use deterministic key ordering and preserve the exact semantic payload. A receiving system may re-encode the block, but it must reproduce the same canonical content hash.

For an end-to-end transport proof, compare at minimum:

```text
identity.event_id
meaning.subject
meaning.content
meaning.human
meaning.naya
meaning.machine
context.scope
context.visibility
evidence.evidence_state
truth.state
authority.state
value.state
lifecycle.stage
integrity.content_hash
```

Any mismatch is a transport-integrity failure until explained by an explicit, authorized projection rule.

---

## 15. Acceptance test

An Intelligent Block is fit for cross-system use when:

1. its identity survives transport;
2. its meaning survives translation;
3. its provenance survives transport;
4. its truth state is preserved;
5. its authority state is preserved;
6. its scope/privacy survives transport;
7. its relationships remain interpretable;
8. its unknowns remain unknown;
9. its evidence can be retrieved;
10. a human and an AI can both understand what it means;
11. a machine can parse it deterministically;
12. the next authorized step can be identified where applicable.

---

## 16. North Star

> **ONE INTELLIGENCE. MANY REPRESENTATIONS. ONE CANONICAL MEANING.**

> **HUMANLY UNDERSTANDABLE. AI-REASONABLE. MACHINE-INTEROPERABLE. EVIDENCE-BOUND. AUTHORITY-AWARE. VALUE-AWARE. CONTINUABLE.**
