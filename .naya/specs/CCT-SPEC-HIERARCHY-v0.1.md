# CCT / NayaNet — Specification Hierarchy v0.1

**Status:** CANONICAL DERIVATION MAP  
**Master:** `CCT-NAYANET-ARCH-v0.1`

## Authority order

```text
CCT / NayaNet Canonical Architecture
                ↓
        Machine Specification
                ↓
          Naya Specification
                ↓
         Human Specification
                ↓
         Public White Paper
```

The Architecture Specification is the semantic master. The Machine Specification converts it into implementable contracts. The Naya Specification converts those contracts into autonomous-agent behavior. The Human Specification explains the same system in human language. The public white paper is derived last and MUST NOT introduce technical claims that are absent from the authoritative architecture or verified implementation evidence.

## Non-negotiable rule

No derived specification may silently change the meaning of:

- CCT;
- NayaNet;
- Intelligent Block;
- Smart Note;
- CIS;
- PIS;
- MPA;
- CCS;
- verification;
- provenance;
- permission;
- independent consumption;
- lifecycle state.

## Smart Note invariant

Every Smart Note is one canonical learning event with three linked representations:

`Human Note + Naya Note + Machine Note`

A Smart Note is complete only when all three exist or each missing representation has an explicit machine-readable reason.

## Evidence invariant

Specifications describe requirements. Execution evidence proves implementation. A specification, file, commit, or configured workflow MUST NOT be represented as a runtime GREEN result without execution evidence.

## Current implementation boundary

The first hard implementation requirement remains the two-independent-Naya Intelligent Block proof:

`Naya A → Block A → independent Naya B consumption → Block B → A→B lineage proof → independent second-pass verification`

Only after that proof is repeatably GREEN should CIS/PIS federation and larger NayaNet infrastructure become implementation priorities.
