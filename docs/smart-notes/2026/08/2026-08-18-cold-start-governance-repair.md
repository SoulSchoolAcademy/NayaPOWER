# Naya Nitro Cold-Start Governance Repair — Main/Active Branch Model

- Timestamp: 2026-08-18 16:42 PDT
- Category: SOLUTION
- Status: ACTIVE
- Scope: PROJECT
- Keywords: cold start, governance, repository map, main branch, active branch, MaxRESULTS, Naya Nitro, Smart Notes, Naya Notes, source of truth, branch divergence, execution prompt, AI comprehension, Section 01
- Aliases: cold-start audit, governance bridge, branch bridge, repository operating system, AI entry system
- Related: `main:START-HERE.md`, `main:docs/REPOSITORY-MAP.md`, `main:docs/SOURCE-AND-MEMORY-MAP.md`, `main:docs/NAYA-SMART-NOTES-SYSTEM.md`, `maxess-results-v21-working:START-HERE.md`, `maxess-results-v21-working:docs/REPOSITORY-MAP.md`

## Context

A cold-start audit exposed that the repository had improved governance on `main` while the active Results branch contained a separate older execution/read-order system. That created a real risk of an AI entering the active branch and following duplicate or stale authority.

## What We Learned / Decided

1. `main` is the canonical governance/reference branch for the Naya Nitro operating system.
2. `maxess-results-v21-working` is the active Results engineering branch.
3. The active branch must not create a competing governance or memory system.
4. The active branch now contains a governance bridge in `START-HERE.md` and `docs/REPOSITORY-MAP.md` that explicitly routes the AI to canonical `main` governance first, then to branch-local implementation state.
5. Naya Note = Smart Note = durable Naya memory. There is one canonical memory system, not separate systems by wording.
6. `docs/smart-notes/INDEX.md` is the retrieval/navigation layer and must be maintained for meaningful new notes.
7. Smart Notes are memory, not authority. Governing documents and current human requirements outrank notes.
8. The fresh Section 01 build has no full approved baseline yet. The Orb + Orbital Bead core behavior is the explicitly protected working element; surrounding presentation remains open to refinement.
9. A GitHub commit proves repository state only. It does not prove GitHub Actions execution, Groove publication, or public visual parity.

## Why It Matters

Without this bridge, a cold-start AI could reasonably read the active branch's older `NAYA-OS`, Nitro protocol, and memory documents and follow a different operating system than the one currently intended. That is exactly the kind of structural ambiguity the Nitro repository is supposed to eliminate.

## Required Behavior

For consequential Results work:

- read canonical governance on `main` first;
- then inspect the active engineering branch;
- treat branch-local governance as subordinate when it conflicts with `main`;
- use the canonical Smart Notes system and retrieval index;
- never infer approval from filenames, branch names, commit recency, or file size;
- verify implementation, automation, and live deployment separately;
- end every consequential execution with the next action and a complete copy-paste execution prompt;
- ask **WHY IS THIS NOT A 10?** before declaring completion.

## Evidence / Source

This repair was executed directly in `SoulSchoolAcademy/MaxRESULTS` after comparing `main` and `maxess-results-v21-working`. The branch comparison showed substantial divergence, confirming that a governance bridge was necessary rather than assuming the branches were synchronized.

## Follow-up

Run the cold-start audit again from a fresh AI context against both `main` and `maxess-results-v21-working`. Verify that the AI can reconstruct the same operating model without conversation history and identify remaining external/unverified constraints.
