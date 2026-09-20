# Naya Cold-Start Activation Acceptance

**Status:** CANONICAL RUNTIME TEST CONTRACT  
**Effective:** 27 August 2026  
**Repository:** `SoulSchoolAcademy/NayaPOWER`

## Purpose

This contract proves the repository-level cold-start boot state for a fresh Naya entering NayaPOWER with no conversation memory.

It deliberately distinguishes:

- **DOCUMENTED** — the policy exists.
- **REGISTERED** — the policy is owned and routed by the canonical context manifest.
- **ACTIVATED** — the modeled cold-start sequence loads the applicable policy.
- **CONTEXT ESTABLISHED** — repository identity, governance, authority, policy, routing, and required evidence are all established.
- **OPERATING-METHOD ESTABLISHED** — the fresh boot state contains and activates the canonical Continuous Block Execution and One-Network operating method.

The acceptance implementation is `.naya/runtime/cold_start_activation.py`.

## What the test proves

A passing test must establish all of the following from canonical repository state:

1. The repository is `SoulSchoolAcademy/NayaPOWER`.
2. The governance branch is `main`.
3. The canonical boot entry and context boot protocol are present.
4. The governing constitution is present and part of the boot order.
5. The Human Capability & Mastery Operating Protocol is the canonical subject owner.
6. The Human Capability & Mastery policy is in the canonical boot order.
7. Every defined task route includes the policy.
8. The boot entry explicitly requires activation before substantive work.
9. The policy preserves higher-order platform/safety/constitutional authority.
10. Core human-capability and evidence requirements are present.
11. The modeled fresh Naya starts with empty conversation memory.
12. The Continuous Block Execution cycle is present in the canonical policy and boot entry.
13. Block completion requires defined criteria plus verification evidence.
14. Unfinished blocks require explicit preservation and ready-to-run continuation.
15. Master Scorecard review and the “WHY IS THIS NOT A 10?” challenge are part of the operating contract.
16. Every meaningful execution output requires a ready-to-run NEXT EXECUTION.
17. The One-Network law identifies NayaPOWER as the shared governance/continuity/verification/compounding substrate and prevents specialized Nayas from silently becoming independent sources of truth.
18. The resulting modeled state is explicitly `ACTIVATED`, `CONTEXT ESTABLISHED`, and `OPERATING-METHOD ESTABLISHED`.

## What it does not prove

This test is intentionally provider/model independent. It does **not** claim that an external LLM, ChatGPT session, API provider, or production agent has literally executed the repository instructions. It proves the deterministic repository contract that a fresh Naya is expected to follow.

Provider-specific execution and live user-facing verification are separate evidence levels.

## Enforcement

The Smart Brain v3 GitHub Actions workflow runs this acceptance test whenever the relevant governance, boot, memory, runtime, or AI boot surfaces change.

## Anti-false-positive rule

A filename-only or manifest-only check is insufficient. The test loads the canonical artifacts and verifies their authority relationship, boot activation language, routing, required policy content, block operating contract, One-Network contract, and explicit state transitions.

**UNKNOWN is never SUCCESS.**
