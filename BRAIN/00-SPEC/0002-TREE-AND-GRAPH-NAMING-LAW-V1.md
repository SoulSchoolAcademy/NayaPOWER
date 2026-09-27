# NayaPOWER Naming & Addressing Law V1

**Status:** PROPOSED CANONICAL

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

Object IDs use:

```
NAYA-<TYPE>-<SEQUENCE>
```

Examples:

```
NAYA-NODE-0001
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

## Rules

1. Never encode mutable state in identity.
2. Never use a filename as the primary identity.
3. Never reuse an ID.
4. Never create IDs by guessing at runtime.
5. Machine allocation owns sequential allocation.
6. Historical IDs remain resolvable.
7. Supersession creates lineage; it does not rewrite history.
8. Human-readable titles may change without changing identity.
