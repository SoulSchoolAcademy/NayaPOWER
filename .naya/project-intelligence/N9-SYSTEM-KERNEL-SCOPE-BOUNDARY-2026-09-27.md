# N9 System Kernel Scope Boundary — Evidence Note

**Date:** 2026-09-27  
**Truth status:** VERIFIED BLOCKER / NOT A PRODUCTION RUNTIME PROOF  
**Canonical repository:** `SoulSchoolAcademy/NayaPOWER`  
**Canonical main at investigation:** `6e5e8509a59c844b8e148fcda996b70a91e8c97f`

## What was proven

The nine Master Nodes exist and are structurally valid:

- IB-001233 → SELF
- IB-001234 → LAW
- IB-001235 → ACT
- IB-001236 → KNOW
- IB-001237 → PROVE
- IB-001238 → CONNECT
- IB-001239 → VERIFY
- IB-001240 → LEARN
- IB-001241 → EVOLVE

The live rows are ACTIVE, version 2, and marked as kernel-activated/structurally active.

## Blocking observation

All nine rows currently have:

- `owner_scope = PRIVATE`
- one shared owner: the member named **Naya Node Founder Proof**
- that owner is a Supabase **anonymous** user

The production loader on main historically bound kernel loading to the requesting user's owner identity. That makes the kernel unavailable to a fresh Naya that does not possess the transient owner session.

## Why this matters

The Master Nodes are classified as `system_intelligence`, but their access boundary behaves like private personal intelligence.

This is a continuity break:

`system kernel` → `transient private owner` → `fresh Naya cannot reliably boot`

That is incompatible with the requirement that a successor Naya can reconstruct and continue without inheriting a particular prior session.

## Repair prepared

Draft PR #818 proposes the smallest fail-closed repair:

- canonical kernel read scope: `SYSTEM_AUTHENTICATED`
- caller must already be authenticated by the Edge Function
- `owner_id` remains provenance only
- runtime loader uses the trusted server-side read path
- exact nine IDs, ACTIVE state, kernel activation, and `content.classification=system_intelligence` remain mandatory
- private data is never silently reclassified by runtime code
- kernel mutation authority remains separate

**PR:** #818  
**Current head:** `95a29146def7824695252e366f0a625f540634ca`

## Verification

N9 structural verification run **36289837010** completed with:

- canonical nine-node verifier: PASS
- `tests/test_nine_master_nodes_spec.py`: PASS

The test suite confirms the loader no longer binds kernel availability to `owner_id = auth.uid()` and explicitly enforces the proposed system scope.

## What is not proven

This note does **not** prove runtime behavioral kernel operation.

N9-001 remains NOT_PROVEN until an independently authenticated runtime can load the canonical nine nodes under the legitimate system scope and show material behavioral influence, ablation, outcome verification, learning, and successor continuity.

## Required external transition

The nine live rows must be legitimately reclassified from `PRIVATE` to `SYSTEM_AUTHENTICATED` (or another ratified equivalent) before this runtime repair can become a live capability.

**Do not bypass this boundary.**
