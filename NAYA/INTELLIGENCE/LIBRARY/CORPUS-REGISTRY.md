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


## Second-pass individual-document normalization — 2026-09-21

This pass inspects individual candidates rather than treating directory names as authority.

### SUPERBRAIN/MASTER-NOTES

| Candidate | Classification | Disposition |
|---|---|---|
| NAYA-ELITE-SYSTEM-EXECUTION-LAW.md | ACTIVE CONTRACT | Keep. It governs execution excellence broadly and is not merely a design/coding standard. |
| NE-20260827-NAYA-CODE-OF-HONOR.md and dated SN-* records | HISTORICAL INTELLIGENCE | Keep. Dated records preserve provenance, decisions, lessons, failures, and evolution. |
| *-RECEIPT-*, execution receipts, forensic maps | EVIDENCE / HISTORICAL INTELLIGENCE | Keep. Receipts and forensic records are evidence, not competing standards. |
| remaining MASTER-NOTES documents | MIXED | Do not mass-delete. Classify by individual role before retirement. The directory is storage, not authority. |

### .naya

| Candidate family | Classification | Disposition |
|---|---|---|
| 00-NAYA-PREFLIGHT-GOVERNANCE-EXECUTION-GATE.md | ACTIVE CONTRACT | Keep. Mandatory preflight/decision gate with a distinct operational role. |
| dated 2026-09-11 and 2026-09-12 Smart Notes/contracts | HISTORICAL INTELLIGENCE / ACTIVE CONTRACT | Keep. These preserve project evolution and contract lineage; they do not silently outrank current standards. |
| NAYA-EXECUTION-*, NAYANET-*, NAYAPOWER-* laws/directives | MIXED | Classify individually. Many are specialized execution, runtime, continuity, release, or evidence contracts. |
| naya-context-manifest.json, runtime registry, trigger artifacts | IMPLEMENTATION / RUNTIME | Keep. Machine/runtime surfaces are not documentation duplicates. |
| retired PR #440 design/coding standards | OBSOLETE | Remain deleted. Never recreate them. |

### docs

| Candidate | Classification | Disposition |
|---|---|---|
| NAYA-LANGUAGE-DICTIONARY-V2.md | CURRENT / ACTIVE CONTRACT | Keep and promote as the single current language authority. |
| NAYA-LANGUAGE-DICTIONARY.md | OBSOLETE / DUPLICATE | Retire. V2 explicitly supersedes it; repository code search found no remaining reference to the old filename. |
| NAYA-UNIVERSAL-EXECUTION-LAW.md | ACTIVE CONTRACT | Keep. Broad universal operating layer; not equivalent to the design/engineering standard. |
| NAYA-MASTER-EXECUTION-GATE.md | HISTORICAL / SUPPORTING | Keep for now. Useful execution-gate provenance; current gating is governed by the active .naya preflight contract. |
| NAYANET_ARCHITECTURE_CONTRACT_V1.md | ACTIVE CONTRACT | Keep. Architecture-specific contract. |
| NAYANET-CANONICAL-ROUTING-CONTRACT-V1.md | ACTIVE CONTRACT | Keep. Current routing/runtime boundary. |
| NAYANET_INTELLIGENT_FEED_PRINCIPLE.md | ACTIVE CONTRACT | Keep. Feed-specific product intelligence principle. |
| MAXESS-*, Smart Note, learning, authority, deployment and product contracts | ACTIVE CONTRACT / EVIDENCE | Keep unless an individual replacement is proven. Product-specific scope is not a duplicate merely because it uses MASTER or V1 naming. |

### NAYANET

| Candidate | Classification | Disposition |
|---|---|---|
| README.md | CURRENT DIRECTORY INDEX | Keep. NayaNET planning/operating index and read-order map. |
| README_FIRST.md | ACTIVE CONTINUITY / EXECUTION CONTRACT | Keep. Fresh-Naya evidence/continuity entry point; distinct from the directory index. |
| 00-NAYANET-MASTER-DIRECTIVE.md | CURRENT / ACTIVE CONTRACT | Keep. Broad NayaNET directive; current Design + Engineering Intelligence governs design/coding details where scopes overlap. |
| E01-ULTIMATE-ENTRANCE-MASTER-DIRECTIVE.md | ACTIVE PRODUCT CONTRACT | Keep. Despite filename, this is E01-specific construction/product/QA guidance, not a global standard. |
| NAYANET-BUILD-MISSION.md | HISTORICAL / TASK-LOCAL CONTRACT | Keep for provenance, but its embedded historical HEAD must never be treated as current truth. |
| NAYANET-IMPLEMENTATION-ARCHAEOLOGY-BASELINE.md | EVIDENCE / BASELINE | Keep. Prior-state archaeology evidence, not current authority. |
| 03-DESIGN-SYSTEM-AND-LIVING-SUN-SPEC.md | ACTIVE PRODUCT DESIGN CONTRACT | Keep. Governed by current Design + Engineering Intelligence standard. |
| 04-ENGINEERING-BLUEPRINT.md | ACTIVE ENGINEERING CONTRACT | Keep. Concrete deployment/engineering rules remain operationally useful. |
| E01-* detailed/question/spec artifacts | ACTIVE PRODUCT CONTRACT / EVIDENCE | Keep individually; they define the E01 product and verification surface. |
| 509-* repair scripts | IMPLEMENTATION / HISTORICAL IMPLEMENTATION | Keep unless dependency analysis proves retirement is safe. Filename versioning alone is insufficient evidence. |

## Confirmed retirement from this second pass

### docs/NAYA-LANGUAGE-DICTIONARY.md

Reason: NAYA-LANGUAGE-DICTIONARY-V2.md explicitly identifies itself as the current NayaPOWER language revision and the older file as its predecessor. The old dictionary adds a second semantic authority without a distinct operational role. Repository code search for the old filename returned no remaining references.

Action: delete the old dictionary; V2 becomes the single current language authority.

## Second-pass result

This pass produces one confirmed deletion rather than speculative mass deletion. No duplicate blob SHAs were found across the inspected four directories, so the remaining cleanup requires semantic/reference analysis rather than filename or byte-identity assumptions.

Next normalization frontier: individual dependency/reference analysis of the remaining .naya laws/directives and the 509-* implementation history, followed by retirement only where current source, references, runtime behavior, and evidence establish that an artifact has no remaining operational or provenance value.


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
