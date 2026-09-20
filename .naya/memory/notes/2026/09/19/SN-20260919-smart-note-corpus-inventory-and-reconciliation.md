---
id: SN-20260919-smart-note-corpus-inventory-and-reconciliation
type: governance / inventory / lesson
status: CANONICAL
date: 2026-09-19
canonical_path: NayaPOWER/SMART-NOTES/2026/09/19
repository_path: .naya/memory/notes/2026/09/19/SN-20260919-smart-note-corpus-inventory-and-reconciliation.md
---

# Smart Note Corpus Inventory and Reconciliation

## In a Nutshell

The repository was inspected for Smart Note-like artifacts after the canonical Smart Note rule was established.

The inspection found that the repository already had a **higher-authority Smart Note resolver**:

- Logical namespace: `NayaPOWER/SMART-NOTES/YYYY/MM/DD/`
- Physical repository storage: `.naya/memory/notes/YYYY/MM/DD/`

That resolver is defined in **SUPERBRAIN/NAYA-REPOSITORY-OPERATING-STANDARD.md §19.1**.

Therefore the correct standard is **not** to create a second physical top-level `SMART-NOTES/` directory. The logical namespace and physical repository path are two representations of the same canonical location.

## Classification

### 1. CANONICAL HUMAN INTELLIGENCE / CANONICAL PHYSICAL ARTIFACTS

**Current canonical physical location:**

`.naya/memory/notes/YYYY/MM/DD/`

Observed 2026-09-19 canonical artifacts:

- `SN-20260919-day-wisdom.md`
  - Runtime source: `supabase:smart_note_events`
  - Runtime event: `4d4f2f3a-9f23-4922-ba63-38c7ea3b2957`
  - Status: VERIFIED
  - Privacy: PRIVATE
- `SN-20260919-nayapower-intelligence-must-be-used-to-test-the-engine.md`
  - Status: CANONICAL INTELLIGENCE - V1
  - Subject: using real Smart Notes as a genuine engine test input
- `SN-20260919-canonical-smart-note-path-contract.md`
  - Status: CANONICAL
  - Role: reusable governance/lesson defining the resolver itself

These are the current authoritative physical repository artifacts for the logical namespace `NayaPOWER/SMART-NOTES/2026/09/19/`.

### 2. MACHINE-RUNTIME / LEGACY MACHINE MEMORY ARTIFACTS

The root of `.naya/memory/notes/` contains older machine-readable and historical Smart Note artifacts, including:

- `MACHINE-NOTE-20260826-INTENT-MEANING-ONE-NAYA-OUTPUT-INTELLIGENCE.json`
- `NAYA-NOTE-20260826-INTENT-MEANING-ONE-NAYA-OUTPUT-INTELLIGENCE.md`
- `SHAWN-NOTE-20260826-INTENT-MEANING-ONE-NAYA-OUTPUT-INTELLIGENCE.md`
- `SN-20260823-220000-north-star.md.json`
- `SN-20260823-220001-memory-brain-principle.md.json`
- `SN-20260823-220002-temporal-history.md.json`
- `SN-20260823-220003-smart-note-quality.md.json`
- `SN-20260823-231200-restore-runtime-execution.md.json`
- `SN-20260824-020000-claim-evidence-runtime.md.json`
- `SN-20260824-023800-evidence-promotion-boundary.md.json`
- `SN-20260824-025400-oscar-provenance-hardening.md.json`
- `SN-20260824-110000-maxis-north-star-priority.md`
- `SN-20260825-101500-smart-notes-cis-architecture-human.json`
- `SN-20260825-101500-smart-notes-cis-architecture-naya.json`
- `SN-20260825-200000-smart-brain-hardening-human.json`
- `SN-20260825-200000-smart-brain-hardening-naya.json`
- `SN-20260825-203000-smart-note-operating-model-naya.md`
- `SN-20260825-203001-smart-note-operating-model-human.md`
- `SN-20260825-214500-superbrain-contract-enforcement-naya.md`
- `SN-20260825-214500-superbrain-contract-enforcement-shawn.md`
- `SN-20260826-INTENT-MEANING-ONE-NAYA-OUTPUT-INTELLIGENCE.md`
- `SN-20260911-070000-decision-calculus-unified-runtime.json`
- `SN-20260911-074500-note-event-to-pis-fresh-retrieval.json`
- `2026-09-10-excellence-by-default-smart-note.md`
- `2026-09-11-decision-calculus-unified-runtime-authority.md`

These must **not** be mass-moved or deleted merely to make the tree uniform. They are historical/machine/proof artifacts and may contain provenance required for audit, retrieval, tests, or learning.

### 3. HISTORICAL / NON-CANONICAL SMART NOTE LOCATION

`.naya/SUPERBRAIN/SMART-NOTES/2026/09/17/`

Currently contains:

`2026-09-17-GITHUB-FIRST-FREEZE-POINT-DELIVERY-SMART-NOTE.md`

Classification: **HISTORICAL DOCUMENT / LEGACY SMART NOTE ARTIFACT**.

It is explicitly prohibited from becoming a current canonical Smart Note home by the repository operating standard. Preserve it as history; do not create new notes there.

The directory itself may remain as historical repository structure unless a separate cleanup decision is made.

### 4. MASTER-NOTES / NAYA-NOTES

`MASTER-NOTES/NAYA-NOTES/` contains older Naya notes such as:

- `2026-08-29-NAYA-NOTE-GOVERNANCE-EXECUTION-BOUNDARY.md`
- `2026-08-29-PROMOTION-ENGINE-V1-EXECUTION-LEARNING.md`
- `2026-08-30-MEET-NAYA-SALES-OPENING.md`

Classification: **HISTORICAL DOCUMENT / LEGACY KNOWLEDGE CORPUS**.

They are not the current canonical Smart Note storage location. Preserve them for history and existing references. Do not create new canonical Smart Notes there.

### 5. MASTER-NOTES SMART-NOTE DOCUMENTS

Examples observed directly under `MASTER-NOTES/` include:

- `2026-08-30-SMART-NOTE-TRIGGER-EVENT-COLD-START-TEST.md`
- `2026-08-31-SMART-NOTE-PROTOCOL-RECEIPTS-AND-INTELLIGENT-FEED.md`

Classification: **HISTORICAL / ARCHITECTURAL DOCUMENTATION**.

They may describe Smart Note behavior or historical implementation, but they are not current canonical Smart Note artifacts.

### 6. PROJECTION / DERIVED INTELLIGENCE

Supabase persistence, `nayanet_intelligence_index`, Intelligent Blocks, learning evidence, reports, Dream/replay inputs, execution receipts, and Hub surfaces are downstream/runtime representations or uses.

Classification: **PROJECTION / DERIVED INTELLIGENCE / RUNTIME STATE**.

They must retain the Smart Note/event identity and provenance. They do not create another canonical repository object.

## Reconciliation Decision

The higher-authority resolver in `SUPERBRAIN/NAYA-REPOSITORY-OPERATING-STANDARD.md §19.1` wins over the newly-created top-level `SMART-NOTES/` physical directory.

Therefore:

**LOGICAL CANONICAL NAMESPACE**
`NayaPOWER/SMART-NOTES/YYYY/MM/DD/`

**PHYSICAL CANONICAL REPOSITORY**
`.naya/memory/notes/YYYY/MM/DD/`

This is one location expressed in two forms.

The temporary top-level physical file created during the prior standardization attempt was removed because it would have created a competing physical source of truth.

## Lifecycle

Smart Notes must remain traceable through:

**CREATE → RESOLVE → PERSIST → VERIFY → INDEX → LEARN → RETRIEVE → REPLAY/APPLY → VERIFY OUTCOME → COMPOUND**

A Markdown file existing in GitHub is not, by itself, proof of the complete runtime learning loop.

## Hard Rule For All Future Nayas

**Never invent a Smart Note directory.**

Resolve the date through the canonical resolver.

If two locations appear to claim canonical status:

**STOP → identify divergence → preserve historical evidence → reconcile to the resolver → verify references/retrieval → continue.**

## Truth State

**VERIFIED:** Current repository authority defines one Smart Note resolver.

**VERIFIED:** The current 2026-09-19 physical canonical corpus is present under `.naya/memory/notes/2026/09/19/`.

**VERIFIED:** The competing top-level `SMART-NOTES/2026/09/19/` file created during the standardization attempt has been removed.

**UNKNOWN:** Full mechanical enforcement of this resolver across every runtime create/read/list/migrate/retrieve code path still requires source-level/runtime verification.

**Principle:** Do not claim runtime unification until runtime enforcement proves it.
