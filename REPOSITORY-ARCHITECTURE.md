# NayaPOWER Repository — Canonical Ownership Map

**Status:** ACTIVE  
**Established:** 2026-09-22  
**Purpose:** Keep the repository understandable to a cold successor Naya without archaeology.

## Canonical domains

| Domain | Canonical location | Role |
|---|---|---|
| GitHub automation | `.github/` | CI, verification, release automation |
| Naya control plane | `.naya/` | execution state, authority, contracts, receipts, runtime control |
| Governance | `GOVERNANCE/` | canonical governance rules and constitutional material |
| Naya language | `NAYA-LANGUAGE/` | canonical vocabulary and semantic definitions |
| Team communication | `NAYA-TEAM/` | Naya-to-Naya coordination, handoffs, current state, team project records |
| Persistent intelligence | `SUPERBRAIN/` | memory, intelligent blocks, smart notes, learning, project intelligence |
| Technical intelligence primitives | `intelligence/` | event, block, indexing, retrieval, learning, compounding contracts |
| NayaPOWER | `NAYAPOWER/` | governed capability/product layer |
| NayaNET | `NAYANET/` | network/product layer; canonical human-facing Hub lives here |
| Contracts | `contracts/` | repository-wide technical contracts |
| Persistence | `supabase/` | managed persistence and backend functions |
| Verification | `tests/` + governed receipts | automated and adversarial proof |
| Reusable engineering tools | `tools/` | current reusable engineering utilities |
| Human documentation | `docs/` | explanatory documentation |
| Cold-start entry | `START-HERE/` | successor entry point |

## Consolidation performed

The following duplicate/historical storage locations were moved into their canonical owners without changing file contents:

- `MASTER-NOTES/` → `SUPERBRAIN/MASTER-NOTES/`
- `NayaNotes/` → `SUPERBRAIN/SMART-NOTES/2026/09/21/`
- `INTEL BLOCK - 01 - Naya Power /` → `SUPERBRAIN/INTELLIGENT-BLOCKS/2026/09/22/architecture/NAYA-POWER-01/`
- `NayaNETEngineeringSystem/` → `.naya/engineering-system/`
- `.naya/TEAM-NAYA/` → `NAYA-TEAM/CONTROL-PLANE/`
- `.naya/team-naya/` → `NAYA-TEAM/PROTOCOL/`

## Ownership rules

1. One concept has one canonical home.
2. Derived views may reference canonical intelligence but do not become competing truth.
3. Historical evidence is preserved when it remains useful; obsolete implementations are retired rather than renamed.
4. Product code belongs to its product boundary; control-plane material does not become product code.
5. Team communication belongs in `NAYA-TEAM/`.
6. Every meaningful engineering cycle records result, evidence, learning, and the next responsible action.
7. If a new folder cannot answer **what it owns, why it exists, and who uses it**, do not create it.

## Current cleanup frontier

The remaining repository cleanup is not a blind deletion exercise. Each remaining duplicate or historical namespace must be dependency-checked before retirement. The next pass should classify the remaining top-level legacy files and overlapping Naya/NayaPOWER/NayaNET namespaces, then retire only those proven obsolete.
