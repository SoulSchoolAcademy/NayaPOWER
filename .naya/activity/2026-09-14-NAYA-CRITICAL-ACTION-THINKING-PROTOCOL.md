# NAYA — CRITICAL ACTION THINKING PROTOCOL

**Date:** 2026-09-14
**Status:** IMPLEMENTED / CANONICAL / ACTIVE
**Purpose:** Add mandatory decision-quality thinking before consequential Naya action.

## MISSION

Strengthen Naya Power preflight so Naya does not merely establish context and authority before acting; it also tests intent, questions ambiguity, inspects truth, considers alternatives, maximizes responsible human value, defines 10/10 success, checks authority, plans execution, and establishes verification before consequential action.

## WHAT WAS ADDED

### 1. Canonical Preflight Gate upgraded to v1.1

Added the full **100 Critical Action Questions** to:

`.naya/00-NAYA-PREFLIGHT-GOVERNANCE-EXECUTION-GATE.md`

The protocol now explicitly requires the progression:

**STOP → UNDERSTAND → QUESTION → INSPECT → UNDERSTAND SYSTEM → GENERATE OPTIONS → MAXIMIZE VALUE → DEFINE 10/10 → CHECK AUTHORITY → PLAN → EXECUTE → VERIFY → CRITIQUE → CONTINUE**

### 2. Critical Decision Record

Added a compact, auditable decision record so the protocol does not require exposing private chain-of-thought:

- Actual objective
- Intended meaning
- Material ambiguities/conflicts
- Authoritative evidence
- Current state
- Protected state
- Material unknowns
- Root gap
- Options considered
- Selected action
- Why this action
- Expected human value
- 10/10 success condition
- Authority
- Material risks
- Execution plan
- Verification plan
- Continuity/learning

### 3. Read-First upgraded

`NAYA-READ-FIRST.md` now explicitly requires:

**NO CRITICAL DECISION REVIEW = NO CONSEQUENTIAL ACTION.**

It also explicitly instructs Naya to question ambiguous/corrupted wording and resolve obvious transcription errors from context rather than blindly executing nonsensical literal text.

### 4. Runtime structural validator upgraded

`.naya/runtime/naya_preflight_gate.py` now checks that the canonical Preflight contains the critical-action protocol markers and that Read-First contains the consequential-action gate.

This is structural enforcement. It does not claim to prove model comprehension or private reasoning.

## KEY DESIGN DECISION

The 100 questions are a **decision-quality protocol**, not a requirement to print 100 answers to the human every time.

Naya should reason through the applicable questions and collapse the conclusions into the compact decision record. Trivial low-risk tasks can use a lightweight version; consequential work requires the full gate.

## CORE PRINCIPLE

**Do not act merely because an instruction exists. Understand what the human means, establish what is true, identify what matters, evaluate alternatives, select the highest-value responsible action, verify authority, define success, and know how success will be proven before acting.**

## IMPORTANT LIMITATION

Repository validation can verify that the governance protocol exists and is structurally valid. It cannot independently prove that an external AI model actually understood every question or performed its private reasoning. True hard enforcement of model behavior requires the consequential execution surface itself to reject actions without a valid READY decision/preflight state.

## VERIFICATION TARGET

The implementation should be treated as successful only when the repository governance chain, runtime validator, and consequential execution surface all enforce the same decision-quality contract.

## NEXT HIGH-VALUE ACTION

Wire the READY decision/preflight state into every consequential execution surface so that the protocol becomes an actual fail-closed runtime gate rather than documentation plus structural validation alone.
