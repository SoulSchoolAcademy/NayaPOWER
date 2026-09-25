# 🔱 Smart Note / Intelligent Block Archaeology Inventory

**Date:** 2026-09-25
**Source HEAD:** bbdae40e63dca93fcacf84cbd60d037ee3d29a5c
**Status:** HISTORICAL ARCHAEOLOGY — PRE-FRESH-START BASELINE
> **2026-09-25 RECONCILIATION:** This inventory is historical archaeology from before the fresh-start memory boundary. It is not an authority, not a live migration queue, and its candidate IB numbers must not be used for allocation. Current canonical intelligence is resolved only through `.naya/memory/smart-notes/REGISTRY.json` and the live canonical receiver.

---

## INVENTORY METHODOLOGY

This inventory catalogs every Smart Note, Intelligent Block, cognition event, and related artifact in the repository to establish the pre-contract baseline. The goal: determine what survives, what migrates, what becomes projection, what retires.

**Classification Schema:**
- **CANONICAL_CANDIDATE** — Already aligns with IB contract; retain as-is
- **MIGRATE** — Valuable content; needs reformatting to canonical IB format
- **PROJECTION** — Not a source object; keep as downstream view
- **LEGACY** — Historical record; archive without mutation
- **DUPLICATE** — Redundant with another entry; consolidate
- **RETIRE** — Obsolete; remove from active truth surface

---

## 1. CANONICAL CONTRACTS & PROTOCOLS (Source of Truth)

| ID | Artifact | Location | Status | Notes |
|----|----------|----------|--------|-------|
| CC-001 | INTELLIGENT-BLOCK-PROTOCOL.md | SUPERBRAIN/INTELLIGENCE/ | CANONICAL_CANDIDATE | Core IB definition |
| CC-002 | INTELLIGENCE-DISTILLER-PROTOCOL.md | SUPERBRAIN/INTELLIGENCE/ | CANONICAL_CANDIDATE | Distillation process |
| CC-003 | INTELLIGENCE-ORGANIZATION-STANDARD.md | SUPERBRAIN/INTELLIGENCE/ | CANONICAL_CANDIDATE | Organization rules |
| CC-004 | INTELLIGENT-EVENT-V1.md | .naya/project-intelligence/ | CANONICAL_CANDIDATE | Event schema |
| CC-005 | INTELLIGENT-BLOCK-V1.md | .naya/project-intelligence/ | CANONICAL_CANDIDATE | Block schema |
| CC-006 | COLD-NAYA-14-QUESTION-RECONSTRUCTION-CONTRACT.md | .naya/project-intelligence/ | CANONICAL_CANDIDATE | Cold successor contract |
| CC-007 | PROJECT-INTELLIGENCE-BRIDGE-CONTRACT-V1.md | .naya/project-intelligence/ | CANONICAL_CANDIDATE | Bridge contract |
| CC-008 | SENDER-RECEIVER-READINESS-CONTRACT.md | .naya/control-plane/ | CANONICAL_CANDIDATE | 7-boundary door contract |
| CC-009 | AAA-VISUAL-INTERACTION-CHECKLIST.md | .naya/control-plane/ | CANONICAL_CANDIDATE | Visual standards |
| CC-010 | SMART-NOTE-DELIVERY-AND-PIS-TRIGGER-CONTRACT.md | docs/ | MIGRATE | Merge into CC-001/CC-002 |

---

## 2. EXISTING INTELLIGENT BLOCKS (IB Candidates)

| ID | Artifact | Location | IB-ID Candidate | Status | Notes |
|----|----------|----------|-----------------|--------|-------|
| IB-001 | INTELLIGENT-BLOCK-001-NAYANET-SYSTEM-MODEL.md | .naya/project-intelligence/ | **IB-000001** | CANONICAL_CANDIDATE | First official IB; system model |
| IB-002 | IB-20260922-001-NAYANET-HUB-SMART-DOORS.md | SUPERBRAIN/INTELLIGENT-BLOCKS/2026/09/22/architecture/ | **IB-000002** | CANONICAL_CANDIDATE | Smart Doors architecture |
| IB-003 | IB-20260922-002-INTELLIGENCE-DISTILLATION-PROTOCOL.md | SUPERBRAIN/INTELLIGENT-BLOCKS/2026/09/22/system/ | **IB-000003** | CANONICAL_CANDIDATE | Distillation protocol |
| IB-004 | architecture/IB-20260922-001-NAYANET-HUB-SMART-DOORS.md | SUPERBRAIN/INTELLIGENT-BLOCKS/2026/09/22/architecture/ | DUPLICATE | Duplicate of IB-002 |
| IB-005 | system/IB-20260922-002-INTELLIGENCE-DISTILLATION-PROTOCOL.md | SUPERBRAIN/INTELLIGENT-BLOCKS/2026/09/22/system/ | DUPLICATE | Duplicate of IB-003 |

**Observation:** Only 3 unique Intelligent Blocks exist in canonical locations. Duplicate paths exist.

---

## 3. SMART NOTES — MEMORY CORPUS (.naya/memory/smart-notes/)

### 2026-08-30 (12 notes)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| SN-001 | SMART-NOTE-20260830-SMART-LINK-LAW-SHAWN.md | LEGACY | Teaching artifact |
| SN-002 | SMART-NOTE-20260830-SMART-LINK-LAW-NAYA.md | LEGACY | Teaching artifact |
| SN-003 | SMART-NOTE-20260830-SMART-NOTE-DELIVERY-TEACHING-SHAWN.md | LEGACY | Teaching artifact |
| SN-004 | SMART-NOTE-20260830-SMART-NOTE-DELIVERY-TEACHING-NAYA.md | LEGACY | Teaching artifact |
| SN-005 | SMART-NOTE-20260830-SMART-NOTE-DELIVERY-TEACHING-MACHINE.md | LEGACY | Teaching artifact |
| SN-006 | SMART-NOTE-20260830-SUPERBRAIN-COMPOUNDING-SHAWN.md | LEGACY | Teaching artifact |
| SN-007 | SMART-NOTE-20260830-SUPERBRAIN-COMPOUNDING-NAYA.md | LEGACY | Teaching artifact |
| SN-008 | SMART-NOTE-20260830-SUPERBRAIN-COMPOUNDING-MACHINE.json | LEGACY | Teaching artifact |

### 2026-08-31 (6 notes)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| SN-009 | SMART-NOTE-20260831-NAYANET-E01-INTELLIGENT-HUB-NETWORK-SHAWN.md | LEGACY | Teaching artifact |
| SN-010 | SMART-NOTE-20260831-NAYANET-E01-INTELLIGENT-HUB-NETWORK-NAYA.md | LEGACY | Teaching artifact |
| SN-011 | SMART-NOTE-20260831-NAYANET-E01-INTELLIGENT-HUB-NETWORK-MACHINE.json | LEGACY | Teaching artifact |
| SN-012 | SMART-NOTE-20260831-SMART-NOTE-PROTOCOL-RECEIPTS-SHAWN.md | LEGACY | Teaching artifact |
| SN-013 | SMART-NOTE-20260831-SMART-NOTE-PROTOCOL-RECEIPTS-NAYA.md | LEGACY | Teaching artifact |
| SN-014 | SMART-NOTE-20260831-SMART-NOTE-PROTOCOL-RECEIPTS-MACHINE.json | LEGACY | Teaching artifact |

### 2026-09-17 (7 notes - Canonical Hub freeze point)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| SN-015 | 2026-09-17-GITHUB-FIRST-FREEZE-POINT-DELIVERY-SMART-NOTE.md | MIGRATE | Canonical freeze point; valuable |
| SN-016 | 2026-09-17T16-04-43Z__NAYAPOWER-CONTINUITY-NORTH-STAR.md | MIGRATE | Valuable continuity record |
| SN-017 | 2026-09-17T17-00-00Z__SUPERBRAIN-OPERATIONAL-NORTH-STAR.md | MIGRATE | Valuable |
| SN-018 | 2026-09-17T17-20-00Z__WHAT-IS-A-SMART-NOTE.md | MIGRATE | Definition artifact |
| SN-019 | 2026-09-17-CONTINUATION-IS-PASSING-THE-TORCH.md | MIGRATE | Valuable |
| SN-020 | 2026-09-17-ENGINE-BEFORE-DEPLOYMENT.md | MIGRATE | Valuable |
| SN-021 | 2026-09-17-EXECUTION-AUTOMATICALLY-COMMUNICATES-VERIFIED-WORK.md | MIGRATE | Valuable |
| SN-022 | 2026-09-17-HUB-SOURCE-AUTHORITY-COLD-NAYA-LEARNING.md | MIGRATE | Valuable |
| SN-023 | 2026-09-17-INTELLIGENT-HUB-IS-ONE-PUZZLE.md | MIGRATE | Valuable |
| SN-024 | 2026-09-17-MAIN-SHOW-VS-MINI-PROJECTS.md | MIGRATE | Valuable |
| SN-025 | 2026-09-17-TEAM-NAYA-COMMUNICATION-MUST-BE-RETRY-SAFE.md | MIGRATE | Valuable |
| SN-026 | 2026-09-17-TEAM-NAYA-MUST-BEHAVE-LIKE-A-TEAM.md | MIGRATE | Valuable |

### 2026-09-18 (5 notes)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| SN-027 | 2026-09-18-CONSTITUTIONAL-AUDIT-PRODUCE-WISDOM-VALUE-PROXY.md | MIGRATE | Constitutional audit |
| SN-028 | 2026-09-18-JEV-BOUNDED-DECISION-INTELLIGENCE-ACTION-8.md | MIGRATE | Bounded decision |
| SN-029 | 2026-09-18-NAYA-ACTIVITY-COMMUNICATION-RESPONSIBILITY.md | MIGRATE | Activity responsibility |
| SN-030 | 2026-09-18-PRODUCE-WISDOM-DONT-OPTIMIZE-WISDOM.md | MIGRATE | Core principle |
| SN-031 | 2026-09-18-P1-RUNTIME-AND-PROOF7-REAL-POLICY-COMPARISON.md | MIGRATE | P1 runtime proof |

### 2026-09-19 (6 notes)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| SN-032 | 2026-09-19-NEXT-NAYA-P1-LEARNING-EXECUTION-PROMPT.md | MIGRATE | P1 learning prompt |
| SN-033 | 2026-09-19-ULTIMATE-NAYA-SUPERBRAIN-EXECUTION-PROMPT.md | MIGRATE | Ultimate execution prompt |
| SN-034 | 2026-09-19-P1-CONTROLLED-PAIRED-POLICY-OUTCOME.md | MIGRATE | P1 outcome proof |
| SN-035 | SN-20260919-canonical-smart-note-path-contract.md | CANONICAL_CANDIDATE | Path contract |
| SN-036 | SN-20260919-smart-note-corpus-inventory-and-reconciliation.md | MIGRATE | Inventory/reconciliation |

### 2026-09-10 to 2026-09-22 (scattered)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| SN-037 | 2026-09-10-excellence-by-default-smart-note.md | MIGRATE | Excellence principle |
| SN-036 | SHAWN-SMART-NOTE-SUPERBRAIN-INTELLIGENCE-PASS-2026-08-25.md | LEGACY | Historical pass |
| SN-038 | 2026-09-20-COLD-START-INTELLIGENCE-TEST.md | MIGRATE | Cold start test |
| SN-039 | 2026-09-20-COLD-START-INTELLIGENCE-TEST-NAYA-NOTE.md | LEGACY | Naya note variant |
| SN-040 | 2026-09-20-COLD-START-INTELLIGENCE-TEST-SHAWN-NOTE.md | LEGACY | Shawn note variant |
| SN-041 | 2026-09-20-COLD-START-INTELLIGENCE-TEST-MACHINE-NOTE.md | LEGACY | Machine note variant |
| SN-042 | 2026-09-22-GAP-002-HUMAN-JOURNEY-SMARTFEED-VERIFIED.md | MIGRATE | GAP-002 verification |
| SN-043 | 2026-09-22-INTELLIGENT-BLOCK-SOURCE-BUNDLE-MODEL.md | CANONICAL_CANDIDATE | Source bundle model |
| SN-044 | 2026-09-22-MULTI-SOURCE-INTELLIGENT-BLOCK-PROOF-001.md | CANONICAL_CANDIDATE | Multi-source proof |

---

## 4. SMART NOTES — NAYA MEMORY NOTES (.naya/memory/notes/)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| MN-001 | SN-20260825-203000-smart-note-operating-model-naya.md | LEGACY | Early operating model |
| MN-002 | SN-20260825-203001-smart-note-operating-model-human.md | LEGACY | Human perspective |
| MN-003 | excellence-by-default-smart-note.md | MIGRATE | Excellence principle |
| MN-004 | SHAWN-SMART-NOTE-SUPERBRAIN-INTELLIGENCE-PASS-2026-08-25.md | LEGACY | Historical pass |

---

## 5. SMART NOTES — SUPERBRAIN CORPUS

### 2026-09-17 (INDEX + 7 notes)

| ID | Artifact | Status |
|----|----------|--------|
| SS-001 | INDEX.md | MIGRATE |
| SS-002 | 2026-09-17T16-04-43Z__NAYAPOWER-CONTINUITY-NORTH-STAR.md | DUPLICATE of SN-016 |
| SS-003 | 2026-09-17T17-00-00Z__SUPERBRAIN-OPERATIONAL-NORTH-STAR.md | DUPLICATE of SN-017 |
| SS-004 | 2026-09-17T17-20-00Z__WHAT-IS-A-SMART-NOTE.md | DUPLICATE of SN-018 |
| SS-005 | 2026-09-17-CONTINUATION-IS-PASSING-THE-TORCH.md | DUPLICATE of SN-019 |
| SS-006 | 2026-09-17-ENGINE-BEFORE-DEPLOYMENT.md | DUPLICATE of SN-020 |
| SS-007 | 2026-09-17-EXECUTION-AUTOMATICALLY-COMMUNICATES-VERIFIED-WORK.md | DUPLICATE of SN-021 |
| SS-008 | 2026-09-17-HUB-SOURCE-AUTHORITY-COLD-NAYA-LEARNING.md | DUPLICATE of SN-022 |
| SS-009 | 2026-09-17-INTELLIGENT-HUB-IS-ONE-PUZZLE.md | DUPLICATE of SN-023 |
| SS-010 | 2026-09-17-MAIN-SHOW-VS-MINI-PROJECTS.md | DUPLICATE of SN-024 |
| SS-011 | 2026-09-17-TEAM-NAYA-COMMUNICATION-MUST-BE-RETRY-SAFE.md | DUPLICATE of SN-025 |
| SS-012 | 2026-09-17-TEAM-NAYA-MUST-BEHAVE-LIKE-A-TEAM.md | DUPLICATE of SN-026 |
| SS-013 | 2026-09-17-GITHUB-CANONICAL-HUB-FREEZE-POINT-LEARNING.md | MIGRATE |
| SS-014 | 2026-09-17-TEAM-NAYA-COMMUNICATION-MUST-BE-RETRY-SAFE.md | DUPLICATE |
| SS-015 | 2026-09-17-TEAM-NAYA-MUST-BEHAVE-LIKE-A-TEAM.md | DUPLICATE |

### 2026-09-18 (5 notes)

| ID | Artifact | Status |
|----|----------|--------|
| SS-016 | 2026-09-18-P1-RUNTIME-AND-PROOF7-REAL-POLICY-COMPARISON.md | DUPLICATE of SN-031 |
| SS-017 | 2026-09-18-PRODUCE-WISDOM-DONT-OPTIMIZE-WISDOM.md | MIGRATE |
| SS-017 | 2026-09-18-NAYA-ACTIVITY-COMMUNICATION-RESPONSIBILITY.md | MIGRATE |
| SS-018 | 2026-09-18-JEV-BOUNDED-DECISION-INTELLIGENCE-ACTION-8.md | MIGRATE |
| SS-019 | 2026-09-18-CONSTITUTIONAL-AUDIT-PRODUCE-WISDOM-VALUE-PROXY.md | MIGRATE |

### 2026-09-19 (2 notes)

| ID | Artifact | Status |
|----|----------|--------|
| SS-020 | 2026-09-19-P1-CONTROLLED-PAIRED-POLICY-OUTCOME.md | DUPLICATE of SN-034 |
| SS-021 | 2026-09-19-NEXT-NAYA-P1-LEARNING-EXECUTION-PROMPT.md | DUPLICATE of SN-032 |
| SS-022 | 2026-09-19-ULTIMATE-NAYA-SUPERBRAIN-EXECUTION-PROMPT.md | DUPLICATE of SN-033 |

---

## 6. SMART NOTES — SUPERBRAIN/MASTER-NOTES (PIS Updates)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| PM-001 | SN-20260831-NAYANET-E01-INTELLIGENT-HUB-NETWORK-VISION.md | MIGRATE | Network vision |
| PM-002 | SN-20260831-NAYANET-INTELLIGENT-HUB-ARCHITECTURE-FREEZE.md | MIGRATE | Architecture freeze |
| PM-003 | SN-20260831-NAYANET-INTELLIGENT-HUB-SUCCESSOR-EXECUTION.md | MIGRATE | Successor execution |
| PM-004 | SN-20260907-HOW-NAYANETS-INTELLIGENT-FEEDS-WORK.md | MIGRATE | Feed mechanics |
| PM-004 | SN-20260907-NAYANET-INTELLIGENT-HUB-TEN-STAR-EXECUTION-PROMPT.md | MIGRATE | 10-star prompt |
| PM-005 | SN-20260909-NAYANET-INTELLIGENT-HUB-EXECUTION-RECEIPT.md | MIGRATE | Execution receipt |
| PM-006 | SN-20260909-NAYANET-INTELLIGENT-HUB-EXECUTION-RECEIPT.md | DUPLICATE | Duplicate |
| PM-005 | SN-20260909-NAYANET-INTELLIGENT-FEED-V7-PRESENTATION-DELIVERY-RECEIPT.md | MIGRATE | V7 presentation |
| PM-006 | SN-20260912-NAYAPOWER-CONTINUOUS-SMART-FLOW-AND-COLD-NAYA-RESTORE.md | CANONICAL_CANDIDATE | Continuous flow contract |

---

## 6. INTELLIGENCE RECEIPTS (Production Evidence)

| ID | Artifact | Location | Status | Notes |
|----|----------|----------|--------|-------|
| IR-001 | 2026-09-05-intelligent-hub-receipt.md | intelligence-receipts/ | PROJECTION | Hub receipt |
| IR-002 | 2026-09-05-intelligent-hub-smart-note-receipt.md | intelligence-receipts/ | PROJECTION | Smart Note receipt |
| IR-003 | 2026-09-05-intelligent-hub-smart-note-feed.md | intelligence-receipts/ | PROJECTION | Feed receipt |
| IR-004 | 2026-09-05-intelligent-hub-human-note.md | intelligence-receipts/ | PROJECTION | Human note |
| IR-005 | 2026-09-05-intelligent-hub-intelligence-feed.md | intelligence-receipts/ | PROJECTION | Feed content |
| IR-006 | 2026-09-05-intelligent-hub-naya-note.md | intelligence-receipts/ | PROJECTION | Naya note |
| IR-007 | 2026-09-05-intelligent-hub-smart-note-feed.md | intelligence-receipts/ | DUPLICATE | Duplicate |

---

## 7. COGNITION EVENTS & ACTIVITY (Production Runtime)

| ID | Artifact | Location | Type |
|----|----------|----------|------|
| CE-001 | nayanet_cognition_events table | Supabase | Production |
| CE-002 | nayanet_execution_receipts table | Supabase | Production |
| CE-003 | nayanet_smart_ledger table | Supabase | Production |
| CE-004 | nayanet_intelligence_index table | Supabase | Production |
| CE-005 | nayanet_intelligent_blocks table | Supabase | Production |

---

## 8. HUB CONTRACTS & SPECIFICATIONS

| ID | Artifact | Location | Status |
|----|----------|----------|--------|
| HC-001 | CONTRACT.md (Smart Notes) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/01-SMART-NOTES/ | CANONICAL_CANDIDATE |
| HC-002 | CONTRACT.md (Personal Intelligence) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/02-PERSONAL-INTELLIGENCE-FEED/ | CANONICAL_CANDIDATE |
| HC-003 | CONTRACT.md (Collective Intelligence) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/03-COLLECTIVE-INTELLIGENCE-FEED/ | CANONICAL_CANDIDATE |
| HC-004 | CONTRACT.md (Activity) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/04-ACTIVITY-FEED/ | CANONICAL_CANDIDATE |
| HC-005 | CONTRACT.md (Smart Connect) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/08-SMART-CONNECT/ | CANONICAL_CANDIDATE |
| HC-006 | CONTRACT.md (Smart Share) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/08-SMART-SHARE/ | CANONICAL_CANDIDATE |
| HC-007 | CONTRACT.md (Smart Ledger) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/09-SMART-LEDGER/ | CANONICAL_CANDIDATE |
| HC-008 | CONTRACT.md (Connections) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/10-CONNECTIONS/ | CANONICAL_CANDIDATE |
| HC-009 | CONTRACT.md (Smart Mail) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/11-SMART-MAIL/ | CANONICAL_CANDIDATE |
| HC-009 | CONTRACT.md (Smart Spaces) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/12-SMART-SPACES/ | CANONICAL_CANDIDATE |
| HC-010 | CONTRACT.md (Smart Lists) | NAYANET/HUB/INTELLIGENT-HUB-SUPERBRAIN/13-SMART-LIST/ | CANONICAL_CANDIDATE |

---

## 9. DOCS & LEGACY SMART NOTES (docs/smart-notes/)

**200+ legacy smart notes in docs/smart-notes/2026/08/ — mostly MAXESS/early execution artifacts**

| Category | Count | Status |
|----------|-------|--------|
| 2026-08-18 to 2026-08-23 | ~80 | LEGACY (MAXESS era) |
| 2026-08-19 to 2026-08-20 | ~60 | LEGACY (MAXESS era) |
| 2026-08-22 | ~20 | LEGACY (MAXESS era) |
| 2026-08-30 | ~5 | LEGACY (cold start tests) |

**Action:** ARCHIVE — These are historical MAXESS execution records, not canonical intelligence objects.

---

## 10. NAYANET/SMART-NOTES (Daily Intelligence)

| ID | Artifact | Status |
|----|----------|--------|
| DN-001 | 2026-09-22.md | MIGRATE (daily intelligence report) |
| DN-002 | 2026-09-02-KING-CHILD-COLLECTIVE-VALUE-STANDARD.md | MIGRATE |
| DN-003 | 2026-09-02-VISUAL-EXECUTION-ANTI-LOOP-STANDARD.md | MIGRATE |

---

## 11. SUPERBRAIN/INTELLIGENCE (Core Intelligence Artifacts)

| ID | Artifact | Status | Notes |
|----|----------|--------|-------|
| SI-001 | INTELLIGENT-BLOCK-PROTOCOL.md | CANONICAL_CANDIDATE | Core protocol |
| SI-002 | INTELLIGENT-HUB-KERNEL-IMPLEMENTATION.md | MIGRATE | Implementation |
| SI-003 | INTELLIGENT-HUB-MASTER-PLAN.md | MIGRATE | Master plan |
| SI-004 | SMART-FEED-BOARD-EXECUTION-RECEIPT.md | PROJECTION | Execution receipt |
| SI-005 | SMART-FEED-BOARD-SURGICAL-BUILD-CONTRACT.md | MIGRATE | Build contract |
| SI-006 | INTELLIGENT-HUB-SUPERBRAIN-CONNECTION-CONTRACT.md | CANONICAL_CANDIDATE | Connection contract |
| SI-007 | 2026-09-21-INTELLIGENT-BLOCK-V1-PROOF.md | CANONICAL_CANDIDATE | IB V1 proof |
| SI-008 | 2026-09-21-INTELLIGENT-EVENT-BLOCK-ARCHITECTURE.md | CANONICAL_CANDIDATE | Event-block architecture |
| SI-008 | 2026-09-22-GAP-002-HUMAN-JOURNEY-SMARTFEED-VERIFIED.md | MIGRATE | GAP-002 verification |
| SI-009 | 2026-09-22-INTELLIGENT-BLOCK-SOURCE-BUNDLE-MODEL.md | CANONICAL_CANDIDATE | Source bundle model |
| SI-009 | 2026-09-22-MULTI-SOURCE-INTELLIGENT-BLOCK-PROOF-001.md | CANONICAL_CANDIDATE | Multi-source proof |

---

## 12. CONTRACTS & SYSTEM MAPS

| ID | Artifact | Location | Status |
|----|----------|----------|--------|
| CS-001 | intelligent-block-v1.md | contracts/ | CANONICAL_CANDIDATE |
| CS-002 | NAYANET_ARCHITECTURE_CONTRACT_V1.md | docs/ | MIGRATE |
| CS-003 | NAYA-SMART-NOTE-DELIVERY-AND-PIS-TRIGGER-CONTRACT.md | docs/ | MIGRATE |
| CS-004 | NAYANET-CANONICAL-ROUTING-CONTRACT-V1.md | docs/ | MIGRATE |
| CS-005 | NAYAPOWER-MISSION-INTEGRITY-GATE-V2.md | .github/ | MIGRATE |
| CS-006 | NAYAPOWER-MISSION-INTEGRITY-GATE.yml | .github/ | MIGRATE |

---

## 13. TEAM NAYA CONTINUITY ARTIFACTS

| ID | Artifact | Status |
|----|----------|--------|
| TN-001 | INTELLIGENT-HUB-COLD-NAYA-READINESS-PROOF.md | MIGRATE |
| TN-002 | INTELLIGENT-HUB-MASTER-MAP.md | MIGRATE |
| TN-003 | INTELLIGENT-HUB-OFFICIAL-TEAM-NAYA-DIRECTIVE.md | MIGRATE |
| TN-004 | INTELLIGENT-HUB-READINESS-SCORECARD.md | MIGRATE |
| TN-005 | 2026-09-17-INTELLIGENT-HUB-COLD-NAYA-READINESS-RECEIPT.md | MIGRATE |
| TN-006 | 2026-09-17-INTELLIGENT-HUB-MASTER-MAP-AND-READINESS.md | MIGRATE |
| TN-007 | 2026-09-17-INTELLIGENT-HUB-OFFICIAL-PROJECT.md | MIGRATE |
| TN-008 | 2026-09-17-INTELLIGENT-HUB-PROJECT-ACTIVITY.md | MIGRATE |
| TN-009 | 2026-09-17T23-59-00Z__NAYANET-INTELLIGENT-HUB-CURRENT-MISSION.md | MIGRATE |
| TN-010 | 2026-09-17T23-59-30Z__NAYANET-INTELLIGENT-HUB-PROJECT-ACTIVITY.md | MIGRATE |
| TN-011 | 2026-09-17T23-59-45Z__NAYA-PRIME-INTELLIGENT-HUB-EXECUTION.md | MIGRATE |
| TN-012 | 2026-09-17T23-59-50Z__NAYA-INTELLIGENT-HUB-VERTICAL-SLICE.md | MIGRATE |
| TN-013 | 2026-09-18T21-00-00Z__SMART-LEDGER-HUB-PROJECTION-EXECUTION.md | MIGRATE |
| TN-014 | 2026-09-19T04-40-00Z__SMART-SPACES-VERTICAL-SLICE.md | MIGRATE |
| TN-015 | 2026-09-19__SMART-TABS-ENGINEERING-ACTIVITY.md | MIGRATE |

---

## 14. EXECUTION RECEIPTS & PROOFS (Production Verified)

| ID | Artifact | Run ID | Status |
|----|----------|--------|--------|
| PR-001 | 20260827-CIS-MEMORY-TO-INTELLIGENCE-SMART-NOTE-VERIFICATION.md | — | VERIFIED |
| PR-002 | MAXESS-SMART-NOTE-DELIVERY-RECEIPT-2026-08-26.md | — | VERIFIED |
| PR-003 | MAXESS-MASTER-DIRECTIVE-RECEIPT-2026-08-26.md | — | VERIFIED |
| PR-004 | MAXESS-MASTER-DIRECTIVE-V2-RECEIPT-2026-08-26.md | — | VERIFIED |
| PR-005 | SUPERBRAIN-P0-AUTHORITATIVE-GREEN-RECEIPT-2026-08-25.md | — | VERIFIED |
| PR-006 | SUPERBRAIN-P0-FINAL-GREEN-RECEIPT-2026-08-25-RUN119.md | 119 | VERIFIED |
| PR-007 | NAYA-POWER-MAXESS-CONTINUITY-RECEIPT-2026-08-26.md | — | VERIFIED |

---

## 15. DUPLICATE ANALYSIS

| Duplicate Group | Canonical Source | Duplicates | Action |
|-----------------|------------------|------------|--------|
| 2026-09-17 Smart Notes | .naya/memory/smart-notes/2026/09/17/ | SUPERBRAIN/SMART-NOTES/2026/09/17/ | Keep .naya/memory/ as canonical; archive SUPERBRAIN/ |
| INTELLIGENT-BLOCK-001 | .naya/project-intelligence/ | SUPERBRAIN/INTELLIGENT-BLOCKS/2026/09/22/architecture/ | Keep .naya/project-intelligence/ as canonical |
| INTELLIGENT-BLOCK-002 | .naya/project-intelligence/ | SUPERBRAIN/INTELLIGENT-BLOCKS/2026/09/22/system/ | Keep .naya/project-intelligence/ as canonical |

---

## 16. CLASSIFICATION SUMMARY

| Classification | Count | Action |
|----------------|-------|--------|
| **CANONICAL_CANDIDATE** | 15 | Retain as-is; reference in canonical contract |
| **MIGRATE** | 65 | Reformat to canonical IB format; assign IB-IDs |
| **PROJECTION** | 8 | Keep as downstream views |
| **LEGACY** | 40 | Archive in .naya/archival/ |
| **DUPLICATE** | 12 | Consolidate; keep single canonical source |
| **RETIRE** | 200+ (MAXESS era) | Archive to .naya/archival/maxess/ |

---

## 17. IB ID ALLOCATION PLAN

| IB-ID | Source | Title | Category |
|-------|--------|-------|----------|
| IB-000001 | .naya/project-intelligence/INTELLIGENT-BLOCK-001-NAYANET-SYSTEM-MODEL.md | NayaNET System Model | ARCHITECTURE |
| IB-000002 | .naya/project-intelligence/IB-20260922-001-NAYANET-HUB-SMART-DOORS.md | Smart Doors Architecture | ARCHITECTURE |
| IB-000003 | .naya/project-intelligence/IB-20260922-002-INTELLIGENCE-DISTILLATION-PROTOCOL.md | Intelligence Distillation Protocol | PROCESS |
| IB-000004 | (migrate) SN-20260919-canonical-smart-note-path-contract.md | Canonical Smart Note Path Contract | CONTRACT |
| IB-000005 | (migrate) SN-20260919-smart-note-corpus-inventory-and-reconciliation.md | Corpus Inventory & Reconciliation | INVENTORY |
| IB-000006 | (migrate) 2026-09-22-INTELLIGENT-BLOCK-SOURCE-BUNDLE-MODEL.md | Intelligent Block Source Bundle Model | MODEL |
| IB-000007 | (migrate) 2026-09-22-MULTI-SOURCE-INTELLIGENT-BLOCK-PROOF-001.md | Multi-Source Intelligent Block Proof 001 | PROOF |
| IB-000008 | (migrate) 2026-09-22-GAP-002-HUMAN-JOURNEY-SMARTFEED-VERIFIED.md | GAP-002 Human Journey SmartFeed Verified | VERIFICATION |
| IB-000009 | (migrate) 2026-09-17-GITHUB-FIRST-FREEZE-POINT-DELIVERY-SMART-NOTE.md | GitHub First Freeze Point Delivery | HISTORICAL |
| IB-000010 | (migrate) 2026-09-12-NAYAPOWER-CONTINUOUS-SMART-FLOW-AND-COLD-NAYA-RESTORE.md | Continuous Smart Flow & Cold Naya Restore | CONTRACT |
| IB-000011 | (migrate) 2026-09-18-PRODUCE-WISDOM-DONT-OPTIMIZE-WISDOM.md | Produce Wisdom Don't Optimize Wisdom | PRINCIPLE |
| IB-000012 | (migrate) 2026-09-18-P1-RUNTIME-AND-PROOF7-REAL-POLICY-COMPARISON.md | P1 Runtime & Proof7 Policy Comparison | PROOF |
| IB-000013 | (migrate) 2026-09-19-P1-CONTROLLED-PAIRED-POLICY-OUTCOME.md | P1 Controlled Paired Policy Outcome | PROOF |
| IB-000014 | (migrate) 2026-09-19-NEXT-NAYA-P1-LEARNING-EXECUTION-PROMPT.md | Next Naya P1 Learning Execution Prompt | PROMPT |
| IB-000015 | (migrate) 2026-09-19-ULTIMATE-NAYA-SUPERBRAIN-EXECUTION-PROMPT.md | Ultimate Naya Superbrain Execution Prompt | PROMPT |
| IB-000016 | (migrate) 2026-09-22-INTELLIGENT-BLOCK-SOURCE-BUNDLE-MODEL.md | (already allocated) | — |
| IB-000016 | (migrate) 2026-09-22-MULTI-SOURCE-INTELLIGENT-BLOCK-PROOF-001.md | (already allocated) | — |
| IB-000017 | CONTRACT.md (Smart Notes) | Hub Smart Notes Contract | CONTRACT |
| IB-000018 | CONTRACT.md (Personal Intelligence) | Personal Intelligence Feed Contract | CONTRACT |
| IB-000019 | CONTRACT.md (Collective Intelligence) | Collective Intelligence Feed Contract | CONTRACT |
| IB-000020 | CONTRACT.md (Activity) | Activity Feed Contract | CONTRACT |

---

## 18. NEXT ACTIONS

1. **Create canonical contract V1** — Define IB schema, ID allocation, lifecycle, projections
2. **Create migration scripts** — Automated transformation of MIGRATE items to canonical IB format
3. **Define enforcement protocol** — Linting, validation, CI gates for canonical compliance
4. **Archive legacy** — Move LEGACY/DUPLICATE/RETIRE to .naya/archival/
5. **Update control plane** — Register canonical IBs in control plane registry

---

**End of Archaeology Inventory**

*This inventory is the prerequisite for the Canonical Smart Note / Intelligent Block Contract V1. No new Smart Notes should be created until the contract is frozen and migration complete.*