# NayaPOWER Naming & Addressing Law V1

**Status:** CANONICAL SPECIFICATION — machine-validation requirements defined  
**Purpose:** Keep navigation, identity, allocation, lineage and historical addressing deterministic.

## Core rule

**PATH IS NAVIGATION. ID IS IDENTITY.**

A path may change during migration. An object ID must not.

## Domain addressing

Top-level domains use stable numeric addresses because they represent architectural regions, not individual objects:

```
00 CONSTITUTION
01 GOVERNANCE
02 ARCHITECTURE
03 KERNEL
04 INTELLIGENCE
05 MEMORY
06 PROOF
07 LEARNING
08 SUCCESSION
09 EVOLUTION
10 INTERFACES
11 KNOWLEDGE
12 ENGINEERING
90 OPERATIONS
99 ARCHIVE
```

## Object IDs

Durable intelligence objects use the canonical schemes:

```
SN-<sequence>                          (Smart Notes, e.g. SN-0549)
IB-<TYPE>-<date>-<sequence>             (Intelligent Blocks, e.g. IB-SMART-NOTE-20261007-XXXX)
```

**Terminology law:** "Naya Node" for objects is RETIRED. The `NAYA-<TYPE>-<SEQUENCE>`
scheme below is superseded for durable objects; it remains valid only for
historical references. New durable objects MUST use SN-… or IB-… schemes.

Superseded scheme (historical only):

```
NAYA-<TYPE>-<SEQUENCE>
```

Canonical machine form (historical):

```regex
^NAYA-[A-Z][A-Z0-9_]*-[0-9]{4,}$
```

Historical examples (do not use for new objects):

```
NAYA-PRINCIPLE-0001
NAYA-DECISION-0001
NAYA-EVIDENCE-0001
NAYA-VERIFICATION-0001
NAYA-LEARNING-0001
NAYA-EVENT-0001
```

Nine kernel identities are reserved:

```
NAYA-KERNEL-SELF
NAYA-KERNEL-LAW
NAYA-KERNEL-ACT
NAYA-KERNEL-KNOW
NAYA-KERNEL-PROVE
NAYA-KERNEL-CONNECT
NAYA-KERNEL-VERIFY
NAYA-KERNEL-LEARN
NAYA-KERNEL-EVOLVE
```

Reserved kernel IDs are immutable and are not sequence-allocated.

## Deterministic allocation and collision law

1. Never encode mutable state in identity.
2. Never use a filename as the primary identity.
3. Never reuse an ID.
4. Never create IDs by guessing at runtime.
5. Machine allocation owns sequential allocation.
6. Historical IDs remain resolvable.
7. Supersession creates lineage; it does not rewrite history.
8. Human-readable titles may change without changing identity.
9. Allocation MUST reject an existing ID rather than silently overwrite it.
10. Allocation MUST be atomic at the canonical persistence boundary.
11. IDs MUST be compared after canonical normalization; case/whitespace variants MUST NOT create distinct identities.
12. A validator MUST prove uniqueness across all canonical object indexes before a promotion can become CANONICAL.
13. A deleted/archived object retains its ID forever; the ID may resolve to its terminal historical state but may never be reissued.
14. Relationship IDs obey the same immutability/non-reuse law.

## Required identity fields

Every canonical object MUST expose:

- `id`
- `type`
- `status`
- `provenance`
- `relationships`
- `created_at`
- `updated_at`

Object-specific contracts may require more fields.

## Validator acceptance

A naming validator is PASS only when it can prove:

```
FORMAT → NORMALIZATION → UNIQUENESS → RESERVED-ID SAFETY → NON-REUSE → RELATIONSHIP-ID SAFETY
```

Failure is fail-closed. A naming violation is never repaired by silently renaming an existing canonical identity.
