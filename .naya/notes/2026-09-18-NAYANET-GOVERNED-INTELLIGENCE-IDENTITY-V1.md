# NayaNET — Governed Intelligence Identity Protocol V1

**Status:** IMPLEMENTED CONTRACT + DETERMINISTIC VALIDATOR  
**Date:** 2026-09-18  
**Authority:** Subordinate to the existing NayaNET Identity, NayaPOWER Constitution, Governance Act, Authority Registry, Smart Ledger, and PIS contracts.

## The 13 questions

Every intelligence-bearing actor should be reconstructible through one governed identity/provenance envelope:

1. **WHO ARE YOU?** → `identity_id`
2. **WHAT ARE YOU?** → `actor_class`
3. **WHO CREATED / DELEGATED YOU?** → `who_created_or_delegated`
4. **WHAT DO YOU KNOW?** → `knowledge`
5. **WHAT CAN YOU DO?** → `capabilities`
6. **WHAT ARE YOU AUTHORIZED TO DO?** → `authority`
7. **WHO AUTHORIZED THAT?** → `authorized_by`
8. **WHAT DID YOU RECEIVE FROM ANOTHER AGENT?** → `received_artifacts`
9. **WHAT PROVENANCE CAME WITH IT?** → `provenance`
10. **WHAT CAN YOU DELEGATE?** → `delegation`
11. **WHAT DID YOU ACTUALLY DO?** → `actual_actions`
12. **WHAT HAPPENED?** → `outcomes`
13. **WHAT DID YOU LEARN?** → `learning`

## Constitutional separation

This is **not** a second account-identity system.

The canonical NayaNET identity registry remains authoritative for resolving current repository/product identities. The product/account identity service remains authoritative for human accounts and sessions.

This protocol answers a different question:

> **What intelligence-bearing actor is this, what lineage and provenance surround it, what power does it possess, what authority bounds it, and what actually happened?**

It also does not grant authority. A capability declaration can never manufacture authority.

## Core laws

**Identity is not authority.**

**Capability is not authority.**

**Knowledge is not automatically truth.**

**Receipt is not authority.**

**Connection is not permission.**

**Delegation requires a verifiable chain.**

**Actual action requires an execution receipt.**

**Outcome claims require evidence.**

**Learning requires identifiable source material.**

**UNKNOWN identity is not eligible for consequential action.**

## Why this matters

Without this envelope, a sufficiently capable network of agents can lose track of:

- which actor produced an artifact;
- who authorized the actor;
- whether the actor was delegated authority;
- where received information came from;
- what was actually done;
- what genuinely happened;
- which learning came from verified outcomes.

With it, the system can begin treating intelligence as a **lineage-bearing object** rather than an anonymous stream of model outputs.

## Next integration boundary

Bind the envelope to the existing Universal Execution Gate and Smart Ledger receipt so that every consequential action has one reconstructible identity chain:

`IDENTITY → LINEAGE → KNOWLEDGE → CAPABILITY → AUTHORITY → AUTHORIZER → INPUT PROVENANCE → DELEGATION → ACTION → OUTCOME → LEARNING`

No new authority model should be created.
