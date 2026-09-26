# NayaNET AAA Canonical Product Tree + Room/Feature Matrix + Data/Intelligence Flow
**Status:** CANONICAL EXECUTION MAP — PRE-CONSOLIDATION GATE
**Effective:** 2026-09-26
**Authority:** NORTH-STAR-NAYANET-AAA-CANONICAL-TREE.md
**Rule:** Map first. Mutate second. Never delete provenance or proof blindly.

## 1. PURPOSE
This document is the repository-wide implementation map for the locked NayaNET tree.
It answers three questions before consolidation:
1. Where does each product capability belong?
2. Which repository artifact is authoritative for it?
3. How does intelligence move from human/source to governed action, proof, learning, and compounding?

The target is one understandable implementation lane, not another generation of the product.

## 2. CANONICAL PRODUCT TREE
```
NAYANET
├── HUMAN
└── NAYA
    └── NAYAPOWER / GOVERNANCE
        └── SUPERBRAIN
            ├── MEMORY
            └── INTELLIGENCE
                └── INTELLIGENT EVENT
                    └── INTELLIGENT BLOCK
                        └── SMART FEED
                            ├── TODAY
                            ├── NOTES
                            ├── LIBRARY
                            ├── REPORTS
                            └── SEARCH
                                └── SMART DOORS
                                    ├── SHARE
                                    ├── MAIL
                                    ├── SPACES
                                    ├── LISTS
                                    └── CONNECTIONS
                                        └── PROOF + LEDGER
                                            └── LEARNING
                                                └── COMPOUNDING
                                                    └── SUPERBRAIN
```
## 3. HUMAN-FACING HUB ROOMS
| Room | Human job | Canonical surface | Primary inputs | Governed outputs |
|---|---|---|---|---|
| Intelligence Today | Know what matters now | `NAYANET/HUB/src/.../Today` / canonical route | current intelligence, mission state, verified events | open, apply, save, connect |
| Smart Feed | See living intelligence | canonical Hub intelligence/feed components | Intelligent Blocks + lenses | retrieve, filter, open |
| Smart Notes | Capture/revisit durable intelligence | canonical Smart Note receiver + Hub projection | receiver-issued IBs | create via receiver, open, apply |
| Intelligence Library | Find durable intelligence | Hub library surface | canonical IB/Smart Note index | search, filter, relate |
| Reports | Understand change over time | Hub report surface | verified events, intelligence, mission state | inspect evidence, export/share |
| Smart Share | Share intelligence by choice | Hub collective surface | selected intelligence + consent/privacy | publish/revoke where authorized |
| Smart Spaces | Work in contextual environments | Hub space surface | membership, permissions, intelligence | collaborate, generate intelligence |
| Connections | Navigate relationships | Hub connections surface | graph, links, people, projects | open related intelligence |
| Smart Lists | Organize intelligence into action | Hub list surface | intelligence + mission/dependencies | add, remove, prioritize |
| Smart Mail | Convert communication into governed intelligence | Hub mail surface | governed mail adapter | communicate, capture, follow-up |
| Evidence | Inspect what supports a claim/action | Hub proof surface | receipts, source events, evidence | inspect lineage |
| Smart Ledger | Inspect accountability/history | Hub proof surface | execution/activity/verification receipts | trace consequence |
| Verification | Know what is actually proven | Hub proof surface | runtime evidence + truth state | verify/reject/retain state |
| Naya | Understand, operate, recommend | Hub Naya actions | canonical context + authority | governed action / next action |
| System | Control identity/privacy/permissions | Hub system surface | backend identity + governance | authorized settings |
## 4. ROOM/FEATURE AUTHORITY MATRIX
| Capability | Canonical owner | Source of truth | Projection | Status |
|---|---|---|---|---|
| Identity | NayaPOWER governance/auth | backend identity/session | Hub identity | KEEP |
| Governance/authority | NayaPOWER | control plane + governed runtime | Hub status/actions | KEEP |
| Intelligent Event | intelligence spine | canonical event/receiver | feed/activity | KEEP |
| Intelligent Block | intelligence receiver | receiver-issued IB | Smart Note/Feed/Hub | KEEP |
| Smart Note creation | canonical receiver | receiver transaction | GitHub `smart-note.md` | KEEP |
| Smart Feed | Hub intelligence layer | canonical IBs/events | Personal/Collective/Activity lenses | KEEP + CONSOLIDATE renderers |
| Today | Hub room | intelligence + mission state | Today view | CONSOLIDATE |
| Reports | Hub room | verified event/intelligence history | report projection | CONSOLIDATE |
| Library | Hub room | canonical Smart Note/IB index | library/search UI | CONSOLIDATE |
| Share | governed capability | consent + authority + canonical intelligence | Smart Share | KEEP |
| Spaces | governed capability | memberships/permissions | Smart Spaces | KEEP |
| Mail | governed adapter | mail provider + governed event path | Smart Mail | KEEP |
| Lists | governed capability | list state + intelligence refs | Smart Lists | KEEP |
| Connections | relationship layer | relationship persistence | Connections | KEEP |
| Evidence/Ledger | proof layer | receipts + source events | proof surfaces | KEEP |
| Learning | NayaPOWER learning path | learning evidence/state | Hub learning indicators | KEEP |
| Compounding | Superbrain/NayaPOWER | verified learning + later application | next context | KEEP |
| Search | retrieval layer | canonical index | global search | CONSOLIDATE |
| Naya actions | governed runtime | authorization + capability contracts | Hub controls | KEEP |
## 5. CANONICAL IMPLEMENTATION LANES
**Human-facing application:** `NAYANET/HUB/index.html` with its `src/` application.
**Canonical intelligence projection:** `.naya/memory/smart-notes/` plus registry/index.
**Canonical receiver:** `supabase/functions/v7-smart-note-canonical/`.
**Governed GitHub bridge:** `supabase/functions/nayanet-github-dispatch/`.
**Intelligence/runtime family:** `supabase/functions/nayanet-pi-*/` and governed intelligence functions.
**Verification:** `tests/`, `verification/`, GitHub Actions, and durable evidence/receipts.
**Control plane:** `.naya/control-plane/{STATE,BLOCKS,MAP,PROOF,BATON}.json`.
**Cold-Naya entry:** `.naya/NAYAPOWER-INTELLIGENT-HUB-READ-FIRST.md` plus canonical control plane.

No alternate Hub, feed renderer, event model, persistence authority, or governance authority may be promoted into a second lane.
## 6. DATA / INTELLIGENCE FLOW
```
HUMAN / SOURCE
  ↓
CHANNEL / SMART DOOR
  ↓
IDENTIFY
  ↓
AUTHENTICATE
  ↓
AUTHORIZE
  ↓
NAYAPOWER GOVERNANCE
  ↓
CANONICAL INTELLIGENCE API / RECEIVER
  ↓
INTELLIGENT EVENT
  ↓
INTELLIGENT BLOCK (immutable identity + provenance)
  ↓
PERSIST / INDEX
  ↓
RETRIEVE
  ↓
SMART FEED / HUB PROJECTIONS
  ↓
HUMAN UNDERSTANDING
  ↓
GOVERNED ACTION
  ↓
EXECUTION RECEIPT / SMART LEDGER
  ↓
VERIFY ACTUAL OUTCOME
  ↓
LEARNING EVIDENCE / STATE
  ↓
COMPOUNDING
  ↓
UPDATED CONTEXT FOR THE NEXT NAYA
```

**Non-negotiable:** projections never become a second source of truth. A channel never gets direct persistence authority.
## 7. REPOSITORY CLASSIFICATION — ACTIVE PRODUCT
| Repository area | Classification | Reason / target |
|---|---|---|
| `NAYANET/HUB/` | KEEP | Current canonical Hub source and protected visual/functional lane |
| `NAYANET/HUB/src/` | KEEP | Single application composition, shell, routes, data, intelligence, styles |
| `NAYANET/HUB/public/` | CONSOLIDATE | Runtime/public assets belong behind canonical Hub; remove duplicate generated copies |
| `NAYANET/HUB/dist/` | REMOVE | Generated build output; source/build pipeline should regenerate it |
| `NAYANET/HUB/node_modules/` | REMOVE | Dependency artifact; never repository intelligence |
| `NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/` | CONSOLIDATE | Useful room contracts/project map; fold into canonical project-intelligence/docs, no second runtime |
| `NAYANET/HUB/HUB-ROOM-SYSTEM/` | CONSOLIDATE | Room definitions are valuable; one room registry/matrix must replace parallel room documentation |
| `NAYANET/HUB/*.md` contracts | KEEP / CONSOLIDATE | Preserve authoritative contracts; merge overlapping contracts into one source |
| `NAYANET/HUB/_diag_*.mjs` | REMOVE | Temporary diagnostics after evidence is preserved elsewhere |
## 8. REPOSITORY CLASSIFICATION — HISTORICAL / ALTERNATE PRODUCT BUILDS
| Repository area | Classification | Rule |
|---|---|---|
| `.naya/archive/historical-product-generations/E01-WELCOME/` | ARCHIVE | Historical front door; not current Hub |
| `.naya/archive/historical-product-generations/E01-ULTIMATE-ENTRANCE/` | ARCHIVE | Historical entrance experiment |
| `NAYANET/E02-INTELLIGENT-HUB/` | ARCHIVE | Historical Hub generation |
| `NAYANET/E02-INTELLIGENT-HUB-AAA/` | ARCHIVE | Historical visual/build variant |
| `NAYANET/E02-INTELLIGENT-HUB-CLOUDFLARE/` | ARCHIVE | Historical implementation/visual provenance; do not execute as current Hub |
| `.naya/archive/historical-product-generations/E03-INTELLIGENT-HUB/` | ARCHIVE | Historical alternate generation |
| `NAYANET/NAYA-FUTURE/` | ARCHIVE | Future/alternate entrance surface |
| `NAYANET/cloudflare/` | ARCHIVE / PROVENANCE | Preserve only evidence/reference required for historical releases |
| `NAYANET/SMART-NOTES/` | ARCHIVE | Historical Smart Note source material; not current receiver write target |
| `NAYANET/SMART-SHARE/` | ARCHIVE / RECONCILE | Preserve useful contract/provenance; canonical runtime belongs in governed lane |
| `NAYANET/UNIVERSAL-AGENT-INTERFACE/` | CONSOLIDATE | Door/interface contract belongs under Smart Doors; keep one API contract |
| `NAYANET/EXECUTION-BRIDGE/` | CONSOLIDATE | Reconcile bridge docs/code to canonical Supabase/GitHub dispatch path |
## 9. REPOSITORY CLASSIFICATION — SUPERBRAIN / NAYAPOWER
| Area | Classification | Target |
|---|---|---|
| `SUPERBRAIN/AI-BOOT/` | KEEP / CONSOLIDATE | Preserve cold-start intelligence; make `.naya` read-first authoritative |
| `SUPERBRAIN/INTELLIGENCE/` | KEEP / CONSOLIDATE | Durable conceptual contracts; eliminate duplicates against `.naya/project-intelligence` |
| `SUPERBRAIN/CONTINUITY/` | KEEP / CONSOLIDATE | Continuity law and successor material feed one canonical boot route |
| `SUPERBRAIN/PROJECT-COGNITION/` | CONSOLIDATE | Cognitive architecture/provenance; no parallel runtime authority |
| `SUPERBRAIN/runtime/` | CONSOLIDATE | Evaluate each module against governed NayaPOWER runtime; retain only unique live responsibility |
| `SUPERBRAIN/MASTER-NOTES/` | ARCHIVE / DISTILL | Historical intelligence corpus; freeze, distill, and promote only surviving concepts |
| `SUPERBRAIN/AI-NOTES/` | ARCHIVE / DISTILL | Historical source material |
| `SUPERBRAIN/SMART-NOTES/` | ARCHIVE / DISTILL | Historical projections; current canonical write target is `.naya/memory/smart-notes/` |
| `SUPERBRAIN/INTELLIGENT-BLOCKS/` | CONSOLIDATE / DISTILL | Historical IB candidates; canonical identity comes from receiver |
| `NAYAPOWER/NayaPOWER-P9/` | ARCHIVE | Nested historical repository copy; never a second authority |
| `NayaPOWER-P8/` | ARCHIVE | Historical repository generation |
## 10. ROOT-LEVEL CONSTRUCTION / SCRATCH CLASSIFICATION
| Pattern | Classification | Condition |
|---|---|---|
| `.cdp-wave-*/` | REMOVE | Local browser/runtime artifacts; not product source |
| `.rehab-*/` | REMOVE | Temporary recovery/test workspaces after needed evidence is retained |
| `.tmp-*/` | REMOVE | Temporary execution artifacts |
| `_*.(mjs|cjs|js|py)` | REMOVE / ARCHIVE | Scratch probes/patches; retain only if a durable test/evidence dependency exists |
| `phase*.md`, `q*.md` | ARCHIVE / DISTILL | Historical execution answers; preserve source, promote surviving intelligence |
| `agent2_*.md`, `*_proof.json`, loose diagnostic reports | ARCHIVE / CONSOLIDATE | Preserve proof when authoritative; remove redundant copies after evidence registry links exist |
| root `node_modules/`, caches, `__pycache__/` | REMOVE | Generated/local artifacts |
| root loose feature scripts | CONSOLIDATE | Move responsibility into named canonical owner or archive |
## 11. PROTECTED / NEVER-BLINDLY-DELETE
1. `NAYANET/HUB/index.html` and its verified canonical application source.
2. Protected visual references under `verification/visual/`.
3. Canonical control plane and read-first documents.
4. Canonical Smart Note/IB projections and registry.
5. Execution receipts, evidence, tests, and release proof needed to reconstruct history.
6. Source documents whose only copy contains unique project intelligence.
7. Git history itself.
8. Any artifact whose dependency/reference status has not been resolved.

Deletion is allowed only after reference/dependency checks and preservation of required provenance.
## 12. MISSING / REBUILD TARGETS
| Missing or weak boundary | Classification | Required outcome |
|---|---|---|
| One machine-readable Product Tree + room matrix | REBUILD | This document becomes canonical map |
| One room registry tied to canonical routes | REBUILD | Every room has one owner and one route |
| One capability manifest | MISSING | Map capability → authority → runtime → proof |
| One consolidated repository relationship index | MISSING / CONSOLIDATE | Every active artifact has one canonical home |
| One historical distillation manifest | MISSING | Freeze → inventory → distill → promote |
| One Smart Door registry | MISSING | Channel → auth → authority → capability → receipt |
| One evidence index | MISSING | Receipt/evidence IDs point to canonical source/result |
| One whole-journey cold-successor proof | PARTIAL | Prove PI chain plus human journey as one continuation |
| One automated no-parallel-implementation gate | MISSING | Fail CI when competing Hub/intelligence/persistence lanes reappear |
## 13. ACCEPTANCE GATE BEFORE CONSOLIDATION
Consolidation may begin only when:
- every active product capability is mapped to one canonical owner;
- every alternate implementation is classified;
- protected evidence has a preservation path;
- dependencies/reference checks exist for removal candidates;
- room routes map to one Hub application;
- data flow maps to one intelligence spine;
- missing boundaries have explicit owners and proof criteria.

## 14. POST-MAP EXECUTION ORDER
1. Freeze historical source material.
2. Build/validate the complete repository relationship inventory.
3. Create the room registry and capability manifest.
4. Reconcile overlapping contracts and runtime owners.
5. Move unique durable intelligence into canonical project-intelligence or canonical Smart Note/IB paths.
6. Remove disposable generated/scratch artifacts.
7. Archive historical product generations without leaving executable ambiguity.
8. Consolidate Hub renderers/routes/data adapters into one implementation lane.
9. Add CI enforcement against parallel product/intelligence/persistence authorities.
10. Run source → build → runtime → interaction → consequence verification.
11. Reconcile control plane and cold-Naya boot path.
12. Close the AAA reorganization gate only when evidence supports each check.
## 15. DEFINITION OF DONE
The reorganization is complete only when:
- the canonical tree is the obvious answer to “where does this belong?”;
- one Hub source owns the human-facing experience;
- one intelligence spine owns events/blocks/persistence identity;
- one governed runtime owns consequential actions;
- one proof/ledger path owns accountability;
- historical artifacts are clearly non-authoritative;
- disposable artifacts are gone;
- every active room has a purpose, owner, data source, action boundary, and verification path;
- a cold Naya can read the map and locate the next responsible action without reconstructing the architecture from chat history.

**AAA law:** implemented ≠ verified; verified ≠ production-proven; documented ≠ canonicalized.

**NEXT ACTION AFTER THIS MAP:** execute dependency/reference inventory, then begin surgical consolidation from the highest-confidence REMOVE/ARCHIVE candidates.