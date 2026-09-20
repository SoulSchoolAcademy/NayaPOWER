# NayaPOWER Repository Organization Audit V1

**Date:** 2026-09-17  
**Branch:** `main`  
**Purpose:** establish the organizational anatomy of NayaPOWER and prevent folder sprawl.

## Executive decision

The repository should be treated as a **system of systems**, not a flat document warehouse.

The strongest current separation is:

```text
GOVERNANCE       = authority + rules
.naya            = machine/runtime control plane + machine memory
SUPERBRAIN       = durable human-readable intelligence
NAYANET          = network / product / federation architecture
NAYA-TEAM        = cross-Naya continuity + handoff + communication
TESTS            = verification
TOOLS            = reusable operational tooling
SCRIPTS          = automation
DOCS             = general documentation, when not canonical elsewhere
```

A folder should only remain a permanent top-level organizational unit when it has a distinct job that cannot be expressed more clearly as a sub-area of one of the canonical systems above.

## Verified top-level units

| Unit | Classification | Purpose | Decision |
|---|---|---|---|
| `.github/` | KEEP | CI/CD workflows, repository automation, verification/deployment gates | Keep as infrastructure automation; do not use it as knowledge storage. |
| `.naya/` | KEEP | Naya machine/runtime control plane and machine-readable memory | Keep. This is the machine side of the Superbrain. Do not duplicate its state into human folders unless as projection. |
| `GOVERNANCE/` | KEEP | Governance contracts, collective agreements, policy, bootstrap, architecture mandates | Keep. Canonical authority layer. |
| `NAYANET/` | KEEP | NayaNET master/product/architecture/engineering/intelligence/network/security blueprints | Keep. Canonical NayaNET product/network layer. |
| `SUPERBRAIN/` | KEEP | Human-readable durable intelligence, Activity, Smart Notes, architecture | Keep. Canonical human-readable intelligence layer. |

## Strongly recommended organizational units

These are part of the intended architecture and should remain distinct if they exist as actual directories:

| Unit | Classification | Purpose | Decision |
|---|---|---|---|
| `NAYA-TEAM/` | ADD / KEEP | Cross-Naya identity, sign-in/out, messages, handoffs, decisions, warnings, lessons, successor context | **Added now.** This is intentionally separate from Activity and Smart Notes. |
| `TESTS/` | KEEP | Automated and adversarial verification | Keep. Tests are executable evidence, not documentation. |
| `TOOLS/` | KEEP | Reusable operational tools | Keep when tools are shared across multiple workflows. Project-specific one-off utilities belong with the project. |
| `SCRIPTS/` | KEEP | Automation and maintenance scripts | Keep, but avoid duplicating tooling. A script is an executable procedure; a tool is a reusable capability. |

## Candidate areas named during the audit

The following names were supplied as areas visible to the human operator. The current GitHub connector response was too large to independently enumerate every root entry in one response, so these are **not falsely claimed as verified directory names**. Their final classification requires the corresponding directory contents to be inspected.

| Named area | Provisional classification | Why |
|---|---|---|
| `MASTER NOTES` | MERGE / RETIRE AS A TOP-LEVEL CONCEPT | Its knowledge role overlaps `SUPERBRAIN/SMART-NOTES`. Do not maintain two canonical Smart Note homes. |
| `Naya Class Intelligence` | MERGE / MOVE unless it is executable code | Intelligence belongs in the Superbrain or a clearly defined Naya-class runtime area; avoid parallel knowledge silos. |
| `Naya Power Player` | KEEP ONLY IF PRODUCT-SPECIFIC | If this is a product/app implementation, it should have a clearly bounded product role; conceptual material belongs in NAYAPOWER/SUPERBRAIN. |
| `Start Here` | KEEP AS AN INDEX, NOT A KNOWLEDGE SILO | A start-here surface is useful, but it should point to canonical locations rather than duplicate them. |
| `Intelligent Receipts` | MERGE IF DUPLICATIVE | Receipts are evidence. If they are canonical execution evidence, they should have one authoritative machine location with human projections. |
| `Intelligence` | MERGE / DEFINE | Broad intelligence is already the purpose of SUPERBRAIN. Keep only if this directory has a distinct runtime/product role. |
| `Crew` | AUDIT REQUIRED | Could be human team operations or obsolete project material. It must not compete with `NAYA-TEAM` for Naya-to-Naya continuity. |
| `Snapshots` | KEEP IF IMMUTABLE RELEASE/STATE ARTIFACTS | Useful for frozen states and recovery; not useful as a second memory system. |
| `Superbase` | AUDIT REQUIRED | If this means Supabase infrastructure, it should be deployment/data infrastructure, not a knowledge folder. Exact current contents must determine whether it belongs in a dedicated infrastructure area. |
| `Docs` | KEEP, BUT NON-CANONICAL | General documentation is useful; canonical governance, architecture, and memory should stay in their authoritative locations. |

## Important root-level observation

The `main` root also contains many large, historically named activation documents and dated implementation artifacts. These are files, not necessarily organizational systems. They should not automatically become new top-level folders.

The repository currently contains both historical activation material and the newer canonical architecture. The solution is **not** to delete history casually. The solution is to establish canonical locations and make indexes point to them.

## `.git` vs `.naya`

`.git` is Git's internal repository metadata. It is not a Naya knowledge folder and should never be used as an organizational home for Naya records.

`.naya` is different: it is an intentional Naya machine/runtime directory containing runtime contracts, execution state, machine memory, sessions, event storage, and related control-plane artifacts. It is part of NayaPOWER's architecture and should remain separate from the human-readable Superbrain.

## Canonical human organization

Human-readable time-series records now use:

```text
SUPERBRAIN/NAYA-ACTIVITY/YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
SUPERBRAIN/SMART-NOTES/YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
NAYA-TEAM/YYYY/MM/DD/YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
```

Each day has an `INDEX.md`.

## Canonical machine organization

Machine events remain under:

```text
.naya/memory/events/YYYY/MM/DD/HH/EVENT.json
```

This distinction is intentional:

- machine canonicality = `.naya/memory`
- human Activity projection = `SUPERBRAIN/NAYA-ACTIVITY`
- human learning projection = `SUPERBRAIN/SMART-NOTES`
- cross-Naya continuity projection = `NAYA-TEAM`

## Anti-sprawl law

Do not create a new top-level folder because a new concept sounds important.

Before creating one, answer:

1. What unique job does it perform?
2. Who owns it?
3. Is it machine or human-readable?
4. Is it canonical or a projection?
5. What existing folder cannot perform the job without becoming less clear?
6. What is its lifecycle?
7. How will a cold Naya discover it?

If those questions cannot be answered, the concept belongs in an existing canonical system.

## Current status

- NAYA-TEAM has been created.
- NAYA-TEAM has a calendar day index for 2026-09-17.
- A cross-Naya continuity record has been created.
- A runtime calendar projection module has been created.
- Canonical Activity persistence now automatically projects verified Activity into the human Activity calendar and NAYA-TEAM calendar.
- Smart Note runtime integration and the cold-Naya proof remain the final verification seam.

## Exactly ONE Next Action

**Have Bionic perform the cold-Naya creation proof and verify that it discovers the canonical calendar structure from repository evidence alone, creates the required records without being told their paths, and leaves exactly one executable successor action.**
