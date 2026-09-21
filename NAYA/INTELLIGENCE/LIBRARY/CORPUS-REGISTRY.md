# 🔱 PROJECT INTELLIGENCE CORPUS REGISTRY

**Status:** CANONICAL NORMALIZATION INDEX
**Date:** 2026-09-21
**Repository:** `SoulSchoolAcademy/NayaPOWER`
**Base state:** `main` at `65c160909375065d96ea7c1c13e7166f287cfe84`

## Classification model

Every repository intelligence source is classified as exactly one primary role:

- **CURRENT** — current governing authority for its declared scope.
- **ACTIVE CONTRACT** — current product, architecture, deployment, security, runtime, or implementation contract that remains needed and is governed by current authority.
- **IMPLEMENTATION** — code, configuration, workflow, schema, or other executable/project machinery.
- **EVIDENCE** — proof, receipt, test result, runtime observation, or verification artifact.
- **HISTORICAL INTELLIGENCE** — retained because it records prior thinking, decisions, experiments, or provenance; not current authority.
- **DUPLICATE** — substantially repeats another current source without a distinct operational role.
- **OBSOLETE** — no longer needed and not required for provenance, compatibility, or evidence.

A document can contain useful intelligence without being current authority. Useful material is distilled upward; the original is then classified according to its remaining purpose.

## First-pass normalization

### `.naya`

| Candidate family | Classification | Rule |
|---|---|---|
| `00-NAYA-PREFLIGHT-GOVERNANCE-EXECUTION-GATE.md` | ACTIVE CONTRACT | Keep. Execution/preflight boundary is operational, not a duplicate of the design standard. |
| Dated `2026-09-11-NAYAPOWER-*-SMART-NOTE.md` intelligence records | HISTORICAL INTELLIGENCE | Keep as dated provenance/learning unless a specific item is promoted into current authority. Do not treat filename recency alone as authority. |
| Current project-intelligence pointer(s) | CURRENT / POINTER | Keep one pointer into the canonical Project Intelligence sources. |
| Retired design/coding laws removed by PR #440 | OBSOLETE | Already retired; do not recreate. |

### `NAYANET`

| Candidate | Classification | Rule |
|---|---|---|
| `00-NAYANET-MASTER-DIRECTIVE.md` | CURRENT / ACTIVE CONTRACT | Keep. It is the broad NayaNET planning/operating authority. Design/engineering details defer to the canonical Design + Engineering Intelligence standard. |
| `01-ARCHITECTURE-BLUEPRINT.md` | ACTIVE CONTRACT | Keep. Architecture blueprint has a distinct system-boundary role. |
| `02-PRODUCT-AND-UX-BLUEPRINT.md` | ACTIVE CONTRACT | Keep. Product/UX contract has a distinct scope. |
| `03-DESIGN-SYSTEM-AND-LIVING-SUN-SPEC.md` | ACTIVE CONTRACT | Keep, but subordinate to the current Design + Engineering Intelligence standard. Any conflicting design token/rule must be reconciled before use. |
| `03A-OFFICIAL-NAYA-BRAND-ASSET-LOCK.md` | ACTIVE CONTRACT | Keep. Brand asset lock is a specific protected-reference contract. |
| `04-ENGINEERING-BLUEPRINT.md` | ACTIVE CONTRACT | Keep. Engineering/deployment contract is distinct from the higher-level design+engineering intelligence standard. |
| `05-INTELLIGENCE-MEMORY-CIS-BLUEPRINT.md` | ACTIVE CONTRACT | Keep. Memory/CIS system contract. |
| `06-SUPERBRAIN-COLLECTIVE-WISDOM-BLUEPRINT.md` | ACTIVE CONTRACT | Keep. Superbrain/collective intelligence boundary. |
| `07-NETWORK-IDENTITY-CONNECTION-BLUEPRINT.md` | ACTIVE CONTRACT | Keep. Network identity/connection contract. |
| `08-MEDIA-POWERCAST-BLUEPRINT.md` | ACTIVE CONTRACT | Keep. Media-specific contract. |
| `09-SECURITY-PRIVACY-TRUST-BLUEPRINT.md` | ACTIVE CONTRACT | Keep. Security/privacy/trust contract. |
| `E01`/other feature directives | ACTIVE CONTRACT or HISTORICAL INTELLIGENCE | Keep only where they still define a concrete feature contract or provenance. Do not allow them to compete with current global standards. |

### `SUPERBRAIN`

| Candidate family | Classification | Rule |
|---|---|---|
| `INTELLIGENCE-DISTILLATION-AND-COMPREHENSION-PRINCIPLE.md` | ACTIVE CONTRACT | Keep. Human-comprehension principle complements, rather than duplicates, the design/engineering standard. |
| `10-10-SCORECARD.md`, readiness scorecards | EVIDENCE / ACCEPTANCE | Keep when they measure a defined readiness state. A scorecard is not a design law. |
| `CCT-*`, execution/control-plane documents | ACTIVE CONTRACT / EVIDENCE | Keep when they define or prove runtime governance. |
| `INDEX/` | IMPLEMENTATION / INDEX | Keep and reconcile with this library rather than creating another competing taxonomy. |
| `MASTER-NOTES/` | MIXED | Classify individual documents. Retire any remaining duplicate standards; retain unique decisions, evidence, or historical intelligence. |
| Retired `MASTER-NOTES/NAYA-ULTIMATE-MASTER-DESIGN-CODING-CONTRACT.md` | OBSOLETE | Already retired by PR #440. |

### `docs`

| Candidate family | Classification | Rule |
|---|---|---|
| `HMC-MAXIMUS-BUTTON-AND-ICON-SYSTEM.md` | ACTIVE CONTRACT / DESIGN SOURCE | Keep as product-specific button/icon reference, governed by the current Design + Engineering standard. |
| `AI-DEFINITION-OF-10.md` | ACTIVE CONTRACT / QUALITY DEFINITION | Keep if still referenced; reconcile wording with current AAA definition. |
| `AI-PRODUCT-CREATION-OS.md`, `MASTERCLASS-AI-PRODUCT-SYSTEM.md` | ACTIVE CONTRACT / PRODUCT INTELLIGENCE | Keep if used by product creation workflows; do not treat `MASTER` in the filename as authority. |
| `ADAPTIVE-LEARNING-*` | ACTIVE CONTRACT / IMPLEMENTATION GUIDANCE | Keep where tied to the current learning system. |
| `DEPLOYMENT-CONTRACT.md` | ACTIVE CONTRACT | Keep; deployment is a concrete operational contract. |
| `FRESH-NAYA-BEHAVIORAL-ACCEPTANCE.md` | EVIDENCE / ACCEPTANCE | Keep as acceptance material, not a governing design law. |
| `MAXESS-*` | ACTIVE PRODUCT CONTRACT | Keep; MAXESS is a distinct product contract. |
| Other docs | MIXED | Classify by role before deletion; do not delete solely because they are old or use `MASTER`/`FINAL` naming. |

### Major project directories

| Area | Classification | Rule |
|---|---|---|
| Application/source code | IMPLEMENTATION | Runtime source is authoritative for what is actually implemented; it does not automatically override governance. |
| `.github/workflows/` | IMPLEMENTATION / EVIDENCE PATH | Keep workflows that execute or verify real capabilities. Retire only proven redundant workflows after checking triggers, dependencies, and evidence value. |
| Protected visual source `2026 09 17 NAYANET HUB.html` | ACTIVE PROTECTED REFERENCE | Keep. It is a visual source/freeze point, not a competing global design standard. |
| Runtime/deployment artifacts | IMPLEMENTATION / EVIDENCE | Keep when operationally required or when they provide proof lineage. |
| `NAYA/ACTIVITY/` | EVIDENCE / ACTIVITY | Keep. Dated activity is continuity evidence, not a competing standard. |
| `NAYA/SMART-NOTES/` | INTELLIGENCE / MEMORY | Keep as durable intelligence records and normalize metadata/indexing over time. |

## Immediate duplicate/obsolescence result

PR #440 already retired the six confirmed competing design/coding standards:

1. `.naya/NAYANET-DESIGN-SYSTEM-STANDARD.md`
2. `.naya/NAYANET-LIVING-INTERFACE-DESIGN-LAW.md`
3. `.naya/MASTER-NAYA-POWER-AI-AGENT-DESIGN-CONTRACT-V1.md`
4. `SUPERBRAIN/MASTER-NOTES/NAYA-ULTIMATE-MASTER-DESIGN-CODING-CONTRACT.md`
5. `docs/NAYA-MASTER-DESIGN-CODER-LAWS.md`
6. `NAYANET/E01-DESIGN-DIRECTIVE.md`

These must remain retired.

## Known reconciliation needed

`NAYANET/03-DESIGN-SYSTEM-AND-LIVING-SUN-SPEC.md` is still useful as a product-specific design reference, but it contains token guidance that can conflict with the current canonical design standard. The current standard is the authority for conflicts; the product spec should be reconciled rather than duplicated or blindly deleted.

Likewise, `NAYANET/04-ENGINEERING-BLUEPRINT.md` contains useful concrete engineering/deployment rules. It should remain an active contract while its general laws are interpreted through the current canonical Design + Engineering Intelligence standard.

## Migration policy

Do **not** mass-move the repository merely to make the tree look tidy.

Normalization proceeds in this order:

**SEARCH → CLASSIFY → DISTILL → INDEX → RECONCILE → RETIRE DUPLICATES → MIGRATE ONLY WHEN VALUABLE → VERIFY**

The library is first a logical retrieval system. Physical relocation is a separate engineering change and must not break workflows, links, evidence, deployment, or provenance.
