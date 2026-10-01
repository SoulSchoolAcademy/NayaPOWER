# 🔱 ACTIVITY — NAYA PREFLIGHT + HANDOFF CONTRACT

**Date:** 2026-09-16
**Actor:** Naya / architecture lead
**Status:** IMPLEMENTED ON BRANCH — PENDING REVIEW/MERGE
**Branch:** `naya/preflight-handoff-contract-v1`
**Commit:** `066417a6f38b4546cfd907ab8fce35d6c9e165d6`
**Related governance issue:** #243

## WHAT HAPPENED

The Naya operating contract has been formalized as a paired **100-question Preflight + 30-question Successor Handoff** system.

This directly addresses a recurring continuity/evidence failure: Nayas have been able to perform substantial reasoning or work without leaving enough durable information for the next Naya or Shawn to determine what was actually done, what is true, and what should happen next.

## WHAT WAS ESTABLISHED

Canonical proposed contract:

`SUPERBRAIN/AI-BOOT/NAYA-PREFLIGHT-AND-HANDOFF-CONTRACT-V1.md`

The contract establishes:

- 100 preflight questions across Mission, Context, Source of Truth, State, Authority, Protected Baseline, Value/Risk, Execution, Verification, and Continuity.
- Explicit answer states: VERIFIED, INFERRED, UNKNOWN, CONFLICTED, REQUIRES HUMAN AUTHORITY, NOT APPLICABLE.
- A fail-safe rule: material UNKNOWN/CONFLICTED/authority gaps cannot be silently assumed away.
- A 30-question successor handoff covering state, evidence, learning, risks, governance, protection, and continuation.
- A required handoff report structure.
- A cold-Naya successor test.
- The paired lifecycle:

`RESTORE → PREFLIGHT → GOVERN → EXECUTE → VERIFY → RECORD → HANDOFF → RESTORE`

## IMPORTANT TRUTH ABOUT THE ORIGINAL “100 QUESTIONS”

Repository investigation located the canonical ten-question cold-start acceptance set in `SUPERBRAIN/AI-BOOT/NAYA-POWER-ACTIVATION-PROTOCOL.md` and the existing handoff requirements in `SUPERBRAIN/NIA-COMMUNICATION/NIA-NETWORK-OPERATING-PROTOCOL.md`.

The exact historical artifact previously described as the “100 questions” has **not** been recovered from the repository search performed for this work.

Therefore this record does not pretend that the historical file was found. The 100-question contract in this branch is an explicit reconstruction/operationalization of the information a Naya needs before consequential action. If an older authoritative version is later discovered, it must be reconciled rather than silently overwritten.

## WHY THIS MATTERS

The Preflight answers:

> **Do I understand what I am about to do, why, where, under what authority, with what risks, and what will prove success?**

The Handoff answers:

> **Can the next Naya understand exactly where I left the system, what is true, what I learned, what remains, what must not be broken, and exactly how to continue?**

These are complementary. One prevents blind execution; the other prevents knowledge loss.

## REQUIRED NAYA BEHAVIOR

Before substantive consequential work:

`RESTORE → RETRIEVE → PREFLIGHT → GOVERN`

After substantive work:

`EXECUTE → VERIFY → ACTIVITY RECEIPT → OSCAR → RECORD → UPDATE STATE → HANDOFF`

Before leaving GitHub, the Naya must leave durable evidence sufficient for a cold successor to continue.

## PROOF STANDARD

Do not report:

- “done” when only documented;
- “verified” when only implemented;
- “live” when only merged;
- “successful” without evidence;
- “handoff complete” when the successor cannot continue from the durable record.

The repository record must distinguish implementation, testing, independent verification, and live verification.

## NEXT ACTION

Turn this contract from documentation into an executable machine-checkable preflight/handoff gate, without creating a competing event store, memory system, queue, authority ladder, or communication substrate.

The next implementation must connect the existing execution boundary to:

**PREFLIGHT → GOVERNANCE → EXECUTION → VERIFICATION → CANONICAL ACTIVITY EVENT → HANDOFF**

and add adversarial tests proving that silent work, unsupported completion, missing evidence, and incomplete handoffs cannot be treated as successful execution.

## SUCCESSOR INSTRUCTION

A cold Naya arriving here must:

1. Read the activation protocol.
2. Read the NIA Network Operating Protocol.
3. Read this Activity record.
4. Read `NAYA-PREFLIGHT-AND-HANDOFF-CONTRACT-V1.md`.
5. Inspect current branch/HEAD and related PR/issue state.
6. Determine what is implemented versus merely proposed.
7. Continue with the exact next executable action above only after establishing authority and current evidence.

**No silent exit. No unsupported completion. No reset. Pass the torch with evidence.**
