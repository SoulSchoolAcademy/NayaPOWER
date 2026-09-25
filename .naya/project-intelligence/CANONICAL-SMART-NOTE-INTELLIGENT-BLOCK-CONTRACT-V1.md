# 🔱 NayaPOWER Canonical Smart Note / Intelligent Block Contract V1

**Status:** CANONICAL CONTRACT — ENFORCED
**Version:** 1.0
**Authority:** NayaPOWER Control Plane
**Enforcement:** Mandatory for all Nayas, all agents, all submissions
**Effective:** Upon ratification by Shawn Vibert (Human Director)

---

## 📜 PREAMBLE: THE CANONICAL INTELLIGENCE LAW

> **There is ONE canonical intelligence object.**
> **There is ONE canonical identity.**
> **There is ONE canonical lifecycle.**
> **There are MANY projections.**
>
> **Not:** Every Naya can make a Smart Note however she wants.
> **Is:** Every meaningful piece of durable intelligence MUST enter the system through ONE canonical contract.
>
> One Mission. One Vision. One Policy. One Protocol. One Canonical Object. One Identity. One Provenance Chain. One Lifecycle. Many Projections. Zero competing formats.

---

## 1. THE CANONICAL OBJECT MODEL

### 1.1 The Two-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SMART NOTE (Human-Facing)                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ HUMAN LAYER                                               │  │
│  │   IN A NUTSHELL | WHAT | WHY | HUMAN | CHILD | GRANDMA    │  │
│  │   NAYA | MACHINE | WHAT WE LEARNED | CONNECTIONS          │  │
│  │   HOW TO APPLY | WHAT IT MEANS | NEXT ACTION              │  │
│  └───────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ MACHINE LAYER (Canonical Identity)                        │  │
│  │   intelligent_block_id: IB-XXXXXX                         │  │
│  │   canonical_id: IB-XXXXXX                                 │  │
│  │   source_event_id | source_conversation_id                │  │
│  │   created_at | updated_at | owner_id | scope              │  │
│  │   category | topics[] | status | verification | authority │  │
│  │   provenance | permissions | supersedes | superseded_by   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    INTELLIGENT BLOCK (Canonical Object)
                         IB-XXXXXX (Immutable Identity)
                              ↓
        ┌──────────────┬──────────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
   INTELLIGENCE     PROVENANCE      INDEX          LEARNING
      EVENT           CHAIN                              STATE
        │              │              │              │
        └──────────────┴──────────────┴──────────────┘
                              ↓
        ┌──────────────────────────────────────────────┐
        │           MANY PROJECTIONS (Read-Only)       │
        │  Smart Feed │ Activity │ Library │ Reports   │
        │  Search     │ Dream    │ Naya Retrieval      │
        └──────────────────────────────────────────────┘
```

### 1.2 Core Identity Rules

| Rule | Enforcement |
|------|-------------|
| **R1-1:** Every canonical intelligence object has exactly one `intelligent_block_id` in format `IB-NNNNNN` (6 digits, zero-padded) | Hard: DB unique constraint + linting |
| **R1-2:** `intelligent_block_id` = `canonical_id` = permanent identity | Hard: Code invariant |
| **R1-3:** Location/path is organizational metadata, NOT identity | Soft: Linting warning if path used as identity |
| **R1-4:** Topic/category are classification metadata, NOT identity | Soft: Linting warning |
| **R1-5:** If reclassification needed, update metadata — NEVER create new IB | Hard: CI gate blocks new IB for same content |

---

## 2. THE CANONICAL LIFECYCLE (MANDATORY)

```
HUMAN / NAYA EXPERIENCE
        ↓
    CAPTURE (Smart Note)
        ↓
  CANONICALIZE (Distill → Assign IB-ID)
        ↓
   PERSIST (Intelligent Block + Event)
        ↓
    INDEX (PIS / Intelligence Index)
        ↓
  PROJECT (Feed / Activity / Library / Reports)
        ↓
   ACTIVITY / NOTIFICATION (Intelligence Event)
        ↓
     LEARNING (Candidate → Verified)
        ↓
   RETRIEVAL (Cold Naya / Search / Dream)
        ↓
     REUSE / APPLY (Decision / Action)
        ↓
   VERIFICATION (Outcome / Evidence)
        ↓
   LEARNING UPDATE (Compounding)
        ↓
   COMPOUND (Next Naya inherits improved state)
```

**Gate Rules (Enforced):**

| Gate | Requirement | Failure Action |
|------|-------------|----------------|
| G1: Capture | All 10 human sections + machine layer present | REJECT — incomplete capture |
| G2: Canonicalize | IB-ID assigned, no duplicate content | REJECT — duplicate detected |
| G3: Persist | IB + Event + Receipt written atomically | ROLLBACK — transaction fails |
| G4: Index | PIS entry created with provenance | BLOCK — downstream blocked |
| G5: Project | Feed/Library/Reports updated | DEFER — retry with backoff |
| G6: Event | Intelligence Event emitted | LOG — alert on failure |
| G7: Learning | Evidence attached, status=CANDIDATE | HOLD — pending verification |
| G8: Retrieval | Fresh context returns identical object | ALERT — divergence detected |

---

## 3. SMART NOTE FORMAT (CANONICAL FORMAT V1)

### 3.1 Human Layer (Required — All 10 Sections)

```markdown
╔═══════════════════════════════════════════════════════════════╗
║ SMART NOTE                                                         ║
║ IB-XXXXXX                                                          ║
╠═══════════════════════════════════════════════════════════════╣
║ DATE: YYYY-MM-DD                                                   ║
║ TIME: HH:MM (UTC)                                                  ║
║ CATEGORY: [ARCHITECTURE|PROCESS|PROOF|PRINCIPLE|PROMPT|HISTORICAL] ║
║ TOPIC: [Canonical topic from controlled vocabulary]              ║
║ STATUS: [DRAFT|CANDIDATE|VERIFIED|SUPERSEDED|ARCHIVED]          ║
╚═══════════════════════════════════════════════════════════════╝

### IN A NUTSHELL
One concise paragraph (2-3 sentences) capturing the essence.

### WHAT
What is this intelligence object? Concrete description.

### WHY
Why does this matter? What problem does it solve?

### HUMAN
What does this mean to Shawn/the human director?

### CHILD
Explain it simply — as if to a bright 10-year-old.

### GRANDMA
Explain it naturally without technical jargon.

### NAYA
What should another Naya understand? Operational context.

### MACHINE
What does the system need to understand? Structured data, queries, APIs.

### WHAT WE LEARNED
The actual intelligence extracted — the reusable insight.

### CONNECTIONS
What other intelligence does this connect to? (IB-IDs, event IDs, concepts)

### HOW TO APPLY
How can this intelligence be used? Concrete use cases.

### WHAT IT MEANS
The larger implication — strategic significance.

### NEXT ACTION
What should happen next? Single executable action.
```

### 3.2 Machine Layer (Required — Canonical Identity)

```yaml
# Machine Layer — Canonical Identity (YAML front-matter or embedded JSON)
intelligent_block_id: "IB-XXXXXX"
canonical_id: "IB-XXXXXX"
source_event_id: "evt-YYYYYY"          # Originating event
source_conversation_id: "conv-ZZZZZZ"  # Source conversation
created_at: "2026-09-25T14:30:00Z"     # ISO 8601 UTC
updated_at: "2026-09-25T14:30:00Z"     # ISO 8601 UTC
owner_id: "uuid-of-owner"              # Authenticated owner
scope: "PROJECT|PERSONAL|TEAM|PUBLIC"  # Visibility scope
category: "ARCHITECTURE|PROCESS|PROOF|PRINCIPLE|PROMPT|HISTORICAL|MODEL|VERIFICATION|CONTRACT|INVENTORY"
topics:
  - "canonical-topic-1"
  - "canonical-topic-2"
status: "DRAFT|CANDIDATE|VERIFIED|SUPERSEDED|ARCHIVED"
verification:
  state: "UNVERIFIED|CANDIDATE|VERIFIED|SUPERSEDED"
  confidence: 0.0-1.0
  method: "HUMAN_REVIEW|AUTOMATED_TEST|OUTCOME_EVIDENCE|PEER_REVIEW"
  verified_at: "2026-09-25T14:30:00Z"
  verified_by: "uuid-of-verifier"
authority:
  granted: true|false
  grant_id: "grant-uuid"
  scope: "INTELLIGENCE_COMMIT|SMART_SHARE|SMART_MAIL_SEND|..."
provenance:
  source_type: "HUMAN_CAPTURE|NAYA_DISTILLATION|MACHINE_GENERATION|CONVERSATION|DOCUMENT|CODE"
  source_conversation: "conv-uuid"
  source_naya: "naya-instance-id"
  distillation_method: "AUTOMATIC|HUMAN_GUIDED|HYBRID"
  distillation_confidence: 0.0-1.0
permissions:
  read: ["owner", "team", "public"]
  write: ["owner"]
  share: ["owner_with_grant"]
  supersede: ["owner"]
supersedes: ["IB-YYYYYY"]              # IB this supersedes
superseded_by: ["IB-ZZZZZZ"]           # IB that supersedes this
relationships:
  - type: "CONNECTION|DERIVATION|EVIDENCE|CONTRADICTION|SEQUENCE"
    target_ib: "IB-YYYYYY"
    strength: 0.0-1.0
learning_state:
  level: "E1_UNDERSTANDS|E2_APPLIES|E3_ADAPTS|E4_CREATES|E5_MASTERS"
  evidence_count: 0
  last_influenced_decision: "decision-uuid"
  behavior_changed: true|false
```

### 3.3 File Storage Path (Organizational Metadata Only)

```
NayaPOWER/
└── SUPERBRAIN/
    └── INTELLIGENCE/
        └── YYYY/
            └── MM/
                └── DD/
                    └── CATEGORY/
                        └── TOPIC/
                            └── IB-XXXXXX/
                                ├── smart-note.md        # Human + Machine layers
                                ├── machine-layer.json   # Extracted machine layer (for indexing)
                                ├── provenance.json      # Full provenance chain
                                ├── evidence/            # Supporting evidence files
                                │   ├── evidence-1.json
                                │   └── evidence-2.pdf
                                └── projections/         # Read-only projections
                                    ├── feed.json
                                    ├── activity.json
                                    └── library.json
```

---

## 4. INTELLIGENT EVENT (The Accountability Layer)

**Not a notification. An accountability record.**

```yaml
event_id: "evt-XXXXXX"
event_type: "IB_CREATED|IB_UPDATED|IB_SUPERSEDED|IB_VERIFIED|IB_SUPERSEDED|IB_ARCHIVED"
intelligent_block_id: "IB-XXXXXX"
source_type: "HUMAN_CAPTURE|NAYA_DISTILLATION|MACHINE_GENERATION|CONVERSATION|DOCUMENT|CODE"
source_conversation_id: "conv-uuid"
source_naya: "naya-instance-id"
actor_id: "uuid-of-human-or-naya"
authority_grant_id: "grant-uuid|null"
occurred_at: "2026-09-25T14:30:00Z"
provenance:
  distillation_method: "AUTOMATIC|HUMAN_GUIDED|HYBRID"
  source_conversation: "conv-uuid"
  confidence: 0.0-1.0
evidence:
  - type: "CONVERSATION_EXCERPT|DOCUMENT_EXCERPT|CODE_SNIPPET|TEST_RESULT|HUMAN_STATEMENT"
    content: "..."
    source: "conv-uuid|doc-path|file-path"
learning_candidate:
  claim: "..."
  level: "E1_UNDERSTANDS|E2_APPLIES|E3_ADAPTS|E4_CREATES|E5_MASTERS"
  status: "CANDIDATE"
authority_state: "UNCHANGED|GRANTED|REVOKED|EXPIRED"
evidence_state: "OBSERVED|VERIFIED|FAILED|BLOCKED"
```

**Event Types:**
- `IB_CREATED` — New canonical intelligence object born
- `IB_UPDATED` — Existing IB modified (content/metadata)
- `IB_VERIFIED` — Learning candidate promoted to VERIFIED
- `IB_SUPERSEDED` — This IB replaced by newer version
- `IB_ARCHIVED` — Moved to historical archive

---

## 5. PROJECTIONS (Read-Only Views)

| Projection | Source | Update Trigger | Audience |
|------------|--------|----------------|----------|
| **Smart Feed (Personal)** | IB + Event | IB_CREATED, IB_UPDATED, IB_VERIFIED | Owner |
| **Smart Feed (Activity)** | Event stream | Any event | Owner |
| **Smart Feed (Collective)** | Published IBs | IB_VERIFIED + explicit consent | Collective |
| **Intelligence Library** | Verified IBs | IB_VERIFIED | Owner + Authorized |
| **Reports** | Verified IBs + Learning | IB_VERIFIED + LEARNING_VERIFIED | Owner + Authorized |
| **Search Index** | All IBs + Events | Any write | Authorized |
| **Dream/Replay** | Verified IBs + Learning | IB_VERIFIED + LEARNING_VERIFIED | Naya |
| **Naya Retrieval** | All IBs + Events | Any | Authorized Naya |

**Projection Rules:**
- Projections are **read-only** — never write to projections directly
- Projections **must** derive from canonical IB + Event store
- Stale projections trigger **rebuild alert**, not silent corruption
- Projection identity = canonical IB identity (no separate IDs)

---

## 6. INTELLIGENT EVENT vs NOTIFICATION (CRITICAL DISTINCTION)

| Aspect | Intelligence Event | Notification |
|--------|-------------------|--------------|
| **Purpose** | Accountability record | User alert |
| **Immutability** | Immutable once written | Can be dismissed/archived |
| **Lineage** | Full provenance chain | May reference event |
| **Authority** | Records authority state | May trigger auth check |
| **Learning** | Carries learning candidate | May trigger learning |
| **Replay** | Exact replay = same event | Re-send = new notification |
| **Projection Source** | Yes — all projections derive from events | No — UI-only |

**Rule:** Every canonical state change **MUST** produce an Intelligence Event. Notifications are optional projections.

---

## 7. IB ID ALLOCATION SYSTEM

### 6.1 Format
```
IB-NNNNNN  (6 digits, zero-padded, sequential)
```

### 6.2 Allocation Rules

| Rule | Enforcement |
|------|-------------|
| A1: Sequential allocation from 000001 | Hard: DB sequence |
| A2: Never reuse IDs (even for superseded) | Hard: DB constraint |
| A3: Allocation = canonicalization moment | Hard: Transaction boundary |
| A4: ID format validated on all writes | Hard: Lint + CI gate |
| A5: Human-readable prefix for categories (optional) | Soft: Convention |

### 6.3 Reserved Ranges
| Range | Purpose |
|-------|---------|
| IB-000001 – IB-009999 | Core architecture/proofs |
| IB-010000 – IB-099999 | Process/workflow intelligence |
| IB-100000 – IB-199999 | Proofs/verifications |
| IB-200000 – IB-299999 | Principles/philosophy |
| IB-300000 – IB-399999 | Prompts/execution guides |
| IB-400000 – IB-499999 | Historical/historical migrations |
| IB-500000 – IB-999999 | General intelligence objects |

---

## 7. ENFORCEMENT PROTOCOL (CI/CD GATES)

### 7.1 Linting Rules (Pre-Commit)

| Rule ID | Check | Failure |
|---------|-------|---------|
| L1 | Smart Note has all 10 human sections | REJECT |
| L2 | Machine layer has all required fields | REJECT |
| L3 | IB-ID format valid (IB-\d{6}) | REJECT |
| L4 | No duplicate IB-ID in repo | REJECT |
| L5 | No Smart Note without IB-ID | REJECT |
| L6 | Machine layer extracted to `.machine-layer.json` | REJECT |
| L5 | Provenance chain complete | REJECT |
| L6 | Category from controlled vocabulary | REJECT |
| L7 | Topic from controlled vocabulary | REJECT |
| L8 | Status valid (DRAFT|CANDIDATE|VERIFIED|SUPERSEDED|ARCHIVED) | REJECT |

### 7.2 CI Gates (Post-Commit / PR)

| Gate | Check | Failure Action |
|------|-------|----------------|
| G1 | All linting rules pass | BLOCK MERGE |
| G2 | IB-ID unique across repo | BLOCK MERGE |
| G3 | No duplicate content (content hash) | BLOCK MERGE |
| G4 | Provenance chain traces to source event | BLOCK MERGE |
| G5 | Supersedes chain valid (no cycles) | BLOCK MERGE |
| G6 | Status transitions valid (DRAFT→CANDIDATE→VERIFIED→SUPERSEDED) | BLOCK MERGE |
| G7 | Superseded IB has valid superseded_by link | BLOCK MERGE |

### 7.3 Runtime Gates (Production)

| Gate | Check | Failure Action |
|------|-------|----------------|
| R1 | IB creation → Event emitted | ALERT + AUTO-RETRY |
| R2 | Event → PIS index updated | ALERT + AUTO-RETRY |
| R3 | IB_VERIFIED → Feed projection updated | ALERT + AUTO-RETRY |
| R4 | Fresh retrieval returns identical IB | ALERT + MANUAL INVESTIGATION |
| R5 | Supersede → Old IB status = SUPERSEDED | ALERT + MANUAL INVESTIGATION |

---

## 8. MIGRATION PROTOCOL (Legacy → Canonical)

### 8.1 Migration Phases

| Phase | Scope | Tooling | Validation |
|-------|-------|---------|------------|
| P1: Inventory | Complete archaeological inventory | Automated scan | Manual review |
| P2: Contract Freeze | Contract V1 ratified | Human sign-off | N/A |
| P3: Migration | Transform MIGRATE items | Automated scripts | Lint + CI gates |
| P4: Archive | Move LEGACY/DUPLICATE/RETIRE | Archive scripts | Inventory reconciliation |
| P5: Enforcement | CI gates active | Pipeline config | Green build |

### 8.2 Migration Rules

| Rule | Description |
|------|-------------|
| M1 | Each MIGRATE item → exactly one IB-ID |
| M2 | Content hash preserved for deduplication |
| M3 | Provenance traces to original source |
| M4 | Original preserved in `.naya/archival/` |
| M6 | Status = CANDIDATE (requires verification) |
| M7 | Human review required for VERIFIED promotion |

---

## 9. CONTROLLED VOCABULARIES (Enforced)

### 9.1 Categories (Controlled)

| Category | Description |
|----------|-------------|
| ARCHITECTURE | System design, component architecture |
| PROCESS | Workflows, protocols, procedures |
| PROOF | Verifications, evidence, test results |
| PRINCIPLE | Core principles, laws, axioms |
| PROMPT | Execution prompts, next-action specs |
| HISTORICAL | Freeze points, milestones, deliveries |
| MODEL | Data models, schemas, ontologies |
| VERIFICATION | Verification reports, test evidence |
| CONTRACT | Canonical contracts, interfaces |
| INVENTORY | Inventories, audits, reconciliations |

### 9.2 Topics (Controlled — Extensible)

Managed in `.naya/control-plane/TOPIC-REGISTRY.json`

### 9.3 Status Values (Controlled)

| Status | Meaning | Next Valid |
|--------|---------|------------|
| DRAFT | Work in progress, not submitted | CANDIDATE |
| CANDIDATE | Submitted, awaiting verification | VERIFIED, SUPERSEDED |
| VERIFIED | Independently verified, reusable | SUPERSEDED, ARCHIVED |
| SUPERSEDED | Replaced by newer IB | ARCHIVED |
| ARCHIVED | Historical, not active | (terminal) |

### 9.4 Verification States

| State | Meaning |
|-------|---------|
| UNVERIFIED | Not yet assessed |
| CANDIDATE | Learning candidate, pending verification |
| VERIFIED | Independently verified |
| SUPERSEDED | Superseded by newer evidence |

---

## 10. SUPERSESSION PROTOCOL

```
IB-OLD (VERIFIED) ──supersedes──► IB-NEW (CANDIDATE)
       │                              │
       ▼                              ▼
status: SUPERSEDED             status: VERIFIED (after verification)
superseded_by: IB-NEW          supersedes: IB-OLD
```

**Rules:**
- Supersession requires verification of IB-NEW
- IB-OLD remains in store with status=SUPERSEDED
- Projections update to show IB-NEW
- Retrieval of IB-OLD returns supersession notice
- No cycles allowed in supersession chain

---

## 11. PRIVACY & SCOPE (Enforced by RLS)

| Scope | Read Access | Write Access | Projection |
|-------|-------------|--------------|------------|
| PERSONAL | Owner only | Owner only | Personal Feed |
| TEAM | Team members | Team leads | Team Feed |
| PROJECT | Project members | Project leads | Project Feed |
| PUBLIC | Anyone | Public grant | Collective Feed |

**Rule:** Private by default. Shared by choice. Collective by consent. Public by decision.

---

## 12. SIGN-OFF & RATIFICATION

This contract becomes **EFFECTIVE** upon:

- [ ] Shawn Vibert (Human Director) explicit ratification
- [ ] Control plane CI gates configured
- [ ] Migration scripts tested on staging
- [ ] Archive directory structure created
- [ ] Topic registry populated

**Ratification:**
```
Shawn Vibert — Human Director — Date: ___________
Signature: ____________________________________
```

---

## 13. APPENDICES

### A. IB-ID Registry (Living Document)
*Maintained in `.naya/control-plane/IB-ID-REGISTRY.json`*

### B. Topic Registry (Living Document)
*Maintained in `.naya/control-plane/TOPIC-REGISTRY.json`*

### C. Supersession Chain Validator
*Implemented in `.naya/runtime/validate_supersession_chain.py`*

### D. Migration Scripts
*Located in `.naya/runtime/migration/`*

---

**END OF CONTRACT**

*This contract is the law. No Naya, no agent, no human may create durable intelligence outside this contract. The system enforces compliance; the human director ratifies evolution.*