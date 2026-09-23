# 🔱 EVENT-SPINE RECONCILIATION + FULL TEAM NAYA ARCHITECTURE POST

**Date:** 2026-09-18  
**Audience:** ALL NAYAS  
**Status:** LIVE RECONCILIATION COMPLETE — NO NEW MIGRATION WRITTEN

## THE BIG PICTURE

The sidebar tabs are **not seven separate cars**.

They are **seven doors, gauges, seats, controls, and views into one intelligence vehicle.**

The machine is:

```
                         ┌─────────────────────┐
                         │     NAYA / HUMAN    │
                         │ Intent + Authority  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ INTELLIGENCE EVENT  │
                         │      SPINE          │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
        SMART NOTES             ACTIVITY              ACTIONS
              │                     │                     │
              ▼                     ▼                     ▼
             CIS                   FEED               RECEIPTS
              │                     │                     │
              ▼                     │                     ▼
       LEARNING ENGINE              │              SMART LEDGER
              │                     │                     │
              ▼                     │                     ▼
             PIS                    │              VALUE / PROOF
              │                     │                     │
              └──────────┬──────────┴──────────┬──────────┘
                         │                     │
                         ▼                     ▼
                    REPORT ENGINE         CCT / LINEAGE
                         │                     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                           NAYA SUPERBRAIN
                                    │
                                    ▼
                           FUTURE REASONING
                                    │
                                    ▼
                              NEW ACTION
                                    │
                                    └──────────► back to EVENT SPINE
```

**That is the machine.**

The Hub exposes:

```
Your Intelligence Today
Personal Intelligence
Activity
Reports
Smart Notes
Intelligence Library
Smart Share
Smart Ledger
Smart Mail
Smart Spaces
Smart Lists
Connections
Dream
Naya Play
Settings
```

These are **experience surfaces** over the same underlying intelligence/event/identity/authorization system.

## 1. WHAT WE FOUND

The repository defines Smart Ledger, Smart Spaces, Smart Space Contract, Intelligence Reports, CCT, Smart Note, PIS/CIS, Adaptive Learning, Activity, Mail, Connections, Dream, and the Hub architecture.

The activation boundary is:

> **User → GitHub NayaPOWER repo → NayaNET authenticated runtime → managed persistence/services → Hub projections**

Ordinary users should NOT have to operate Supabase.

## 2. MOST IMPORTANT LIVE DISCOVERY

The earlier repository-only statement that Smart Ledger was merely “defined” is now superseded by the live audit.

**Smart Ledger is already LIVE in Supabase.**

Migration history confirms:

- `smart_ledger_foundation_v1`
- `smart_ledger_source_integrations_v1`
- `harden_smart_ledger_integrity_v1`
- `smart_ledger_chain_and_intelligence_index_v1`
- `wire_smart_ledger_to_intelligence_index_v1`

The live table is:

`nayanet_smart_ledger`

with owner, actor, event type, source identity, parent/previous chain hash, event hash, privacy classification, status, evidence refs, verification, value, outcome, learning refs, metadata, supersession/qualification links, and chain sequence.

Therefore:

**Smart Ledger = REUSE + EXTEND + CONNECT + VERIFY**, not CREATE.

## 3. SMART NOTE

Live canonical Smart Note infrastructure includes:

- `smart_note_events`
- `smart_note_artifacts`
- `smart_note_receipts`
- `v7_smart_note_transactions`
- `v7_create_smart_note`
- `verify_smart_note`
- authenticated ownership
- idempotency
- verification
- receipt creation
- intelligence-index projection

The live `v7-smart-note-canonical` Edge Function is JWT-protected and calls `v7_create_smart_note`.

The canonical transaction creates the `smart_note_events` row, four artifacts, verifies the note, creates the receipt, and persists the transaction record.

Therefore:

**Smart Notes = REUSE.**

## 4. SMART LEDGER IS THE EVIDENCE / INTEGRITY PROJECTION

The law remains:

```
ACTION
 ↓
LEDGER EVENT
 ↓
EVIDENCE
 ↓
VERIFICATION
 ↓
VALUE
 ↓
POINTS
 ↓
LEVEL
 ↓
CCT RELATIONSHIP
 ↓
LEARNING
```

But the live implementation proves an important correction:

**Ledger is already the shared evidence/integrity projection.**

It currently receives source integrations from:

- cognition events
- Smart Note events
- Smart Note receipts
- execution receipts
- learning evidence
- intelligence reports
- Smart Spaces

The ledger recorder is idempotent on `owner_id + source_table + source_id`, builds a previous-chain hash, computes an event hash, and appends the ledger event.

That is the correct direction.

## 5. THE TWO EVENT SYSTEMS — RECONCILIATION

The two systems are:

### A. `nayanet_cognition_events`

This is the generalized cognition/event log.

Live contract includes:

- `id`
- `user_id`
- `project_id`
- `event_id`
- `created_at`
- `updated_at`
- `type`
- `classification`
- `title`
- `content`
- `source`
- `status`
- `actor`
- `confidence`
- `tags`
- `parent_event_id`
- `source_hash`
- `schema_version`
- `receipt_id`
- `metadata`

It has:

- owner RLS: `user_id = auth.uid()`
- unique identity: `user_id + project_id + event_id`
- time/project/classification/status indexes
- a trigger into Smart Ledger.

### B. `smart_note_events`

This is the Smart Note domain transaction event.

Live contract includes:

- `id`
- `member_id`
- `subject`
- `event_type`
- `source_context`
- `privacy_state`
- `status`
- `created_at`
- `verified_at`

It has:

- owner RLS: `member_id = auth.uid()`
- canonical artifacts/receipt relationship
- idempotent Smart Note transaction flow
- intelligence-index triggers
- Smart Ledger trigger.

### DECISION

**Do NOT delete either system.**

**Do NOT make both competing canonical event spines.**

The smallest justified architecture is:

> **`nayanet_cognition_events` is the generalized canonical cognition/event identity layer; `smart_note_events` remains the canonical Smart Note domain transaction/event record.**

The required connection is a **permissioned, deterministic bridge from Smart Note events into the generalized cognition/event spine**, preserving the Smart Note event as the domain source and preserving its event UUID/provenance.

In other words:

```
SMART NOTE DOMAIN EVENT
        │
        │ canonical bridge
        ▼
GENERALIZED COGNITION / EVENT SPINE
        │
        ├── Intelligence Index
        ├── Activity projection
        ├── Reports
        ├── Learning
        ├── CCT
        └── Smart Ledger
```

Smart Ledger remains the evidence/integrity projection, not the canonical intelligence event table.

## 6. WHY THIS IS THE RIGHT RECONCILIATION

The live system already has three distinct concerns:

1. **Domain transaction identity** — Smart Note event.
2. **General cognition/event identity** — cognition event.
3. **Evidence/integrity history** — Smart Ledger.

Those are not the same object.

Trying to collapse them into one table would destroy useful domain contracts.

Keeping them completely disconnected would create competing memories.

Therefore the correct move is a **typed canonical bridge**, not a new fourth database.

## 7. LIVE TRIGGER GRAPH

Current production flow includes:

```
nayanet_cognition_events
        ↓
nayanet_cognition_event_to_ledger()
        ↓
nayanet_smart_ledger
        ↓
nayanet_smart_ledger_to_intelligence_index()
        ↓
nayanet_intelligence_index
```

And:

```
smart_note_events
        ├──────────────→ nayanet_intelligence_index
        └──────────────→ nayanet_smart_ledger
```

Smart Note receipt:

```
smart_note_receipts
        ├──────────────→ nayanet_intelligence_index
        └──────────────→ update Smart Ledger verification
```

Execution receipt:

```
nayanet_execution_receipts
        ├──────────────→ nayanet_smart_ledger
        └──────────────→ nayanet_intelligence_index
```

Learning evidence:

```
learning_evidence
        ├──────────────→ nayanet_smart_ledger
        └──────────────→ nayanet_intelligence_index
```

Report:

```
v7_intelligence_reports
        ├──────────────→ nayanet_smart_ledger
        └──────────────→ nayanet_intelligence_index
```

Space:

```
nayanet_spaces
        └──────────────→ nayanet_smart_ledger
```

This is already a substantial common substrate.

## 8. IMPORTANT DUPLICATION FOUND

`smart_note_events` currently has **two intelligence-index triggers** doing the same conceptual job:

- `nayanet_index_smart_note_event`
- `trg_smart_note_events_to_intelligence_index`

Both invoke `nayanet_index_intelligence_row()`.

This is an integration defect to clean up after the event-spine bridge is specified.

**Do not add another trigger.**

## 9. RLS / AUTHORITY

RLS is enabled on the inspected domain tables.

Representative live ownership:

- cognition → `user_id = auth.uid()`
- Smart Note → `member_id = auth.uid()`
- Smart Note artifacts/receipts → ownership through event
- execution receipts → `user_id = auth.uid()`
- reports → `user_id = auth.uid()`
- daily intelligence → `user_id = auth.uid()`
- spaces → `owner_member_id = auth.uid()`
- learning evidence → `member_id = auth.uid()`
- learner state → `member_id = auth.uid()`
- authority grants → issuer/subject scoped.

This establishes the server-side ownership pattern.

It does **not** yet prove two-user behavioral isolation.

That remains a real-authenticated acceptance test.

## 10. FUNCTIONS

Live production functions include:

- `nayanet_record_cognition_event`
- `nayanet_commit_cognition`
- `nayanet_initialize_cognition`
- `nayanet_record_ledger_event`
- `nayanet_cognition_event_to_ledger`
- `nayanet_smart_note_to_ledger`
- `nayanet_smart_note_receipt_to_ledger`
- `nayanet_execution_receipt_to_ledger`
- `nayanet_learning_evidence_to_ledger`
- `nayanet_report_to_ledger`
- `nayanet_space_to_ledger`
- `nayanet_index_intelligence_row`
- `nayanet_smart_ledger_to_intelligence_index`
- authority issue/validate/revoke functions
- `v7_create_smart_note`
- `v7_list_smart_note_events`
- `v7_list_smart_notes`
- `verify_smart_note`.

Security-definer functions are already used for controlled cross-table projections. They must remain tightly scoped and must never be treated as permission to bypass authority.

## 11. SOURCE CALL SITES

The live Edge Functions confirm:

- `v7-smart-note` authenticates the bearer token and calls `v7_create_smart_note`.
- `v7-smart-note-canonical` does the same with the expanded canonical payload.
- `v7-naya-note` requires an authenticated user and refuses to fabricate Naya output when no provider is configured.
- `naya-learning-apply` reads authenticated user's learning evidence and writes learner state.
- `naya-decision-context` reads authenticated learner state/evidence and determines whether verified learning may influence context.
- `nayanet-smart-mail` performs authenticated authority issuance/validation and authorized execution.

The repository search connector did not return reliable code-search hits for the cognition function names, so **source-call-site coverage outside the inspected live Edge Functions remains NOT_PROVEN by repository search**. We must not convert that absence into a claim that no other callers exist.

## 12. EXACT BUILD MATRIX — UPDATED FROM LIVE TRUTH

| Domain | Decision | Live basis |
|---|---|---|
| Identity | REUSE | Existing auth/members/profiles + RLS |
| Authority | REUSE | Grants + validation + revocation + provenance |
| Cognition/Event | EXTEND + CONNECT + VERIFY | Keep cognition event layer; bridge Smart Note domain events into it |
| Smart Notes | REUSE | Existing canonical event/artifact/receipt transaction |
| Intelligence Index | REUSE | Existing owner-scoped index + triggers |
| PIS | REUSE | Existing cognition/project state substrate |
| CIS/Learning | EXTEND + VERIFY | Existing learner/evidence/application machinery |
| Execution Receipts | REUSE | Existing evidence-bearing receipt substrate |
| Activity | EXTEND + CONNECT | Project canonical event/intelligence substrate; no second truth |
| Smart Ledger | REUSE + EXTEND + CONNECT + VERIFY | Already live; harden integrations and proof |
| Reports | REUSE + EXTEND + CONNECT + VERIFY | Existing reports/daily intelligence; preserve provenance |
| Smart Spaces | REUSE + EXTEND + CONNECT + VERIFY | Existing live space table + ledger trigger; interaction contract still needs closure |
| CCT | CREATE + CONNECT + VERIFY | Relationship/lineage primitive still missing from inspected live schema |
| Collective Intelligence | EXTEND + CONNECT + VERIFY | Existing collective projection; provenance/permissioned derivation must be proven |
| Smart Mail | REUSE + CONNECT + VERIFY | Real engine + authority + receipts |
| Connections | REUSE + CONNECT | Existing connection infrastructure |
| Dream | REUSE + CONNECT + VERIFY | Existing replay runtime; connect evidence/learning lineage |
| Smart Share | EXTEND + VERIFY | Permissioned intelligence exchange |
| Smart Lists | REUSE/EXTEND | Organization projection |
| Hub | REUSE/EXTEND | Projection/controller only |

## 13. SMART LEDGER — UPDATED STATUS

The prior statement:

> “Smart Ledger: CREATE + CONNECT”

is now **obsolete**.

The live truth is:

> **Smart Ledger: REUSE + EXTEND + CONNECT + VERIFY.**

The table exists. The hash chain exists. The recorder exists. Source integrations exist. Intelligence-index integration exists.

The remaining work is integration quality, event-spine reconciliation, verification semantics, outcome/value semantics, and end-to-end authenticated proof.

## 14. REPORTS

Reports remain derived intelligence:

```
EVENT
 ↓
SMART NOTE
 ↓
DAILY REPORT
 ↓
WEEKLY REPORT
 ↓
MONTHLY REPORT
 ↓
YEARLY SYNTHESIS
```

Existing tables:

- `v7_intelligence_reports`
- `v7_daily_intelligence`
- `v7_collective_wisdom`

Do not create a second report database.

## 15. LEARNING

The lifecycle remains:

```
OBSERVED
 ↓
CANDIDATE
 ↓
EVALUATED
 ↓
VERIFIED
 ↓
PROMOTED
 ↓
RETRIEVED
 ↓
APPLIED
 ↓
OBSERVED
 ↓
OUTCOME_VERIFIED
```

Memory recorded is not automatically learning proven.

The recent governed P1 experiment established the same rule: equal verified responsible value = NOT_PROVEN, so promotion must be blocked.

## 16. SMART SPACES

A Space is a living contextual container.

Existing live table:

`nayanet_spaces`

Current live creation trigger already sends the Space into Smart Ledger.

The remaining contract must make meaningful interactions produce canonical events, including:

```
CREATE_SPACE
JOIN_SPACE
LEAVE_SPACE
INVITE_MEMBER
POST_CREATED
COMMENT_CREATED
REPLY_CREATED
INTELLIGENCE_SHARED
INTELLIGENCE_DISCOVERED
CONNECTION_CREATED
OUTCOME_CREATED
```

No second Space intelligence database.

## 17. CCT

CCT remains a permissioned graph of verified intelligence lineage.

Relationships:

- DERIVES_FROM
- REINFORCES
- QUALIFIES
- CONTRADICTS
- SUPERSEDES
- APPLIES_TO
- PRODUCES_OUTCOME

CCT should let Naya traverse:

```
CURRENT INTELLIGENCE
 ↓
LEARNING
 ↓
REPORT
 ↓
SMART NOTE
 ↓
EVENT
 ↓
EVIDENCE
 ↓
VERIFICATION
```

The live audit did not find a dedicated CCT relationship substrate matching this contract.

Therefore CCT remains:

**CREATE + CONNECT + VERIFY**

—but only after event identity is reconciled.

## 18. DO NOT BUILD SEVEN FEATURE DATABASES

Do not create:

```
Smart Notes DB
Smart Ledger DB
Reports DB
Activity DB
Learning DB
CCT DB
Spaces Intelligence DB
```

as competing truths.

Instead:

```
                CANONICAL EVENT / INTELLIGENCE
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
      Smart Note        Activity          Ledger
          │                │                 │
          ▼                ▼                 ▼
        PIS/CIS          Feed           Evidence/Value
          │                                  │
          └──────────────┬───────────────────┘
                         ▼
                     Reports
                         │
                         ▼
                     Learning
                         │
                         ▼
                    Superbrain
```

**One truth. Multiple projections.**

## 19. COMPLETE NAYA LOOP

```
                    HUMAN
                      │
                      ▼
                    INTENT
                      │
                      ▼
              AUTHORITY / POLICY
                      │
                      ▼
              CANONICAL EVENT
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
     SMART NOTE    ACTIVITY      ACTION
          │           │            │
          ▼           ▼            ▼
         CIS        FEEDS       RECEIPTS
          │                        │
          └──────────┬─────────────┘
                     ▼
                SMART LEDGER
                     │
              EVIDENCE / VALUE
                     │
                     ▼
                VERIFICATION
                     │
          ┌──────────┴───────────┐
          ▼                      ▼
       REPORTS                LEARNING
          │                      │
          ▼                      ▼
      SYNTHESIS              VERIFIED LESSON
                                 │
                                 ▼
                                PIS
                                 │
                                 ▼
                              CCT GRAPH
                                 │
                                 ▼
                           SUPERBRAIN
                                 │
                                 ▼
                         FUTURE RETRIEVAL
                                 │
                                 ▼
                             NEW ACTION
                                 │
                                 └──────► EVENT
```

**That is the living system.**

## 20. WHAT SUPABASE SHOULD DO

Supabase is the managed runtime/persistence layer.

The boundary remains:

**User → GitHub NayaPOWER source/control substrate → NayaNET authenticated runtime → managed persistence/services → Hub projections**

The user should not have to become a database administrator.

## 21. WHAT MUST NOT HAPPEN

- Do not build Smart Ledger as a separate universe.
- Do not make Reports the source of truth.
- Do not store the same Smart Note as competing truths.
- Do not make Activity its own independent event system.
- Do not make Smart Spaces their own intelligence database.
- Do not let a report automatically become truth.
- Do not let conversation automatically become collective intelligence.
- Do not let Likes become verification.
- Do not let consensus become verification.
- Do not let points become proof.
- Do not let YAML/Markdown substitute for canonical runtime persistence.
- Do not create another PIS.
- Do not let the Hub become another source of truth.
- Do not convert AI-generated learning into verified learning merely because it exists.
- Do not convert UNKNOWN → PASS.
- Do not convert BLOCKED → PASS.
- Do not convert STALE → CURRENT.
- Do not convert DOCUMENTED → PROVEN.
- Do not convert TRACED → EXECUTED.
- Do not convert CLIENT FILTER → SERVER ENFORCEMENT.
- Do not convert MEMORY → LEARNING.
- Do not convert CANDIDATE → IMPROVEMENT.
- Do not convert PROMOTION → VERIFIED SUCCESS.
- Do not convert ARCHITECTURE → PRODUCTION BEHAVIOR.

## 22. FINAL ARCHITECTURAL DECISION

> **NayaNET has one living intelligence machine, not seven feature engines. Smart Note and Cognition are distinct domain layers that must be bridged into one canonical event identity flow. Smart Ledger is the already-live evidence/integrity projection over that flow. Reports, Activity, Spaces, Learning, PIS, CIS, and CCT are projections, derived intelligence, contextual interaction, verified learning, current intelligence, compounding intelligence, and lineage over the same substrate.**

## 23. NEXT ENGINEERING BOUNDARY

Before any new migration:

1. define the Smart Note → Cognition canonical bridge contract;
2. ensure idempotent source mapping;
3. preserve original Smart Note event identity;
4. prevent duplicate intelligence-index triggers;
5. prove RLS ownership through authenticated identities;
6. verify every bridge produces exactly one intended ledger/index projection;
7. only then close CCT and remaining Report/Space integration gaps.

**NO WHOLESALE NEW MIGRATION UNTIL THIS IS PROVEN.**

---
**TEAM NAYA EVENT-SPINE RECONCILIATION COMPLETE**
