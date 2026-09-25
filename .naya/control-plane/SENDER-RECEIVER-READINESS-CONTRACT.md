# Universal Sender / Receiver Readiness Contract

**Status:** CANONICAL CONTRACT  
**Version:** 1.0  
**Authority:** NayaPOWER Control Plane  
**Purpose:** Define the universal contract that every Smart Door sender must satisfy to connect to the NayaNET canonical receiver.

---

## 1. THE UNIVERSAL PATTERN

```
HUMAN/AGENT INTENT
       ↓
CANONICAL SENDER (one per door)
       ↓
GOVERNED CAPABILITY BOUNDARY
       ↓
NAYAPOWER AUTHORITY (identity + scope + consent + ownership + policy)
       ↓
CANONICAL EVENT / INTELLIGENT BLOCK
       ↓
MANAGED PERSISTENCE (Supabase / cognition events / receipts / Ledger)
       ↓
INDEX (nayanet_intelligence_index)
       ↓
RETRIEVAL (fresh context → same canonical result)
       ↓
HUB PROJECTION (Smart Feed / Activity / Intelligence Today / Library / Reports)
       ↓
EVIDENCE (provenance, lineage, receipt, Ledger)
       ↓
AUTHORIZED CONTINUATION (successor action with authority grant)
```

**No direct human/agent-to-Supabase architecture is accepted.**  
**The Hub is a projection/action surface, not a second brain.**

---

## 2. SENDER READINESS REQUIREMENTS (Per Door)

Every sender must satisfy ALL seven boundaries:

| Boundary | Requirement | Evidence Standard |
|----------|-------------|-------------------|
| **VISUAL** | Discoverable, coherent, responsive, consistent with protected Hub DNA | Browser render proof vs. protected visual reference |
| **SENDER** | User action produces exactly ONE canonical request/event | Single event identity; no duplicate emissions |
| **BRIDGE** | Request crosses governed capability boundary (Edge Function / RPC) | Bridge contract: RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT |
| **AUTHORITY** | Identity, scope, consent, ownership, policy enforced server-side | Fail-closed on missing/invalid/expired grants; RLS + authority validation |
| **PERSISTENCE** | Authoritative result durably recorded in canonical store | Cognition event + execution receipt + Smart Ledger entry |
| **RETRIEVAL** | Fresh context retrieves same canonical result | Independent Supabase read returns identical object |
| **EVIDENCE** | UI and receipt expose provenance to prove what happened | Event ID, receipt ID, Ledger hash, source event lineage visible |

---

## 3. RECEIVER READINESS REQUIREMENTS (Canonical)

The canonical receiver (`nayanet_record_cognition_event` + projection pipeline) must:

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Accept events from ANY authorized sender | PROVEN | Smart Note, Smart Share, GitHub webhook (P4), Smart Mail, Intelligent Block |
| Enforce authority boundary (`intelligence_commit` requires grant) | PROVEN | Run 35898728927: 17/17 checks PASS |
| Persist to canonical cognition events + receipts + Ledger | PROVEN | Smart Feed Ledger integration run 35460477460 |
| Project to intelligence index | PROVEN | Intelligent Block V1 lifecycle run 35906051544 |
| Support fresh retrieval by owner | PROVEN | Run 35898728927: fresh context retrieval PASS |
| Support exact replay (idempotent) | PROVEN | Migration 20260924222644: `replayed=true` returns original |
| Reject unauthorized/wrong-owner access | PROVEN | Run 35898728927: wrong-owner rejection PASS |
| Maintain privacy boundaries (private by default) | PROVEN | Run 35462235010: non-owner retrieval count = 0 |

---

## 4. PER-DOOR SENDER CONTRACT TEMPLATE

Each Smart Door MUST complete this contract before claiming readiness:

```markdown
# [DOOR NAME] Sender Contract

## Door Identity
- **Name:** (e.g., "GitHub Webhook", "Smart Note", "Smart Mail", "MCP", "REST/OpenAPI")
- **Type:** (EXTERNAL_WEBHOOK | HUMAN_UI | AGENT_PROTOCOL | EMBEDDED_SDK)
- **Canonical Sender Source:** (file path to sender implementation)

## Seven Boundary Proof

### 1. VISUAL
- [ ] Discoverable in Hub
- [ ] Coherent with Hub DNA
- [ ] Responsive (desktop + mobile)
- [ ] Evidence: browser render vs. protected reference

### 2. SENDER
- [ ] Single canonical event emitted per user action
- [ ] Event schema: event_id, source_event_id, source_system, event_type, title, repository/actor/ref/commit_sha, occurred_at, received_at, correlation_id, idempotency_key, authority, provenance, verification, processing_state, projection_targets, payload
- [ ] Evidence: sender source code + runtime emission test

### 3. BRIDGE
- [ ] Crosses governed capability boundary (Edge Function / RPC)
- [ ] Bridge contract: RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- [ ] Evidence: bridge workflow + runtime trace

### 4. AUTHORITY
- [ ] Identity verified (authenticated user / service-role / GitHub installation)
- [ ] Scope enforced (repository, installation, project, action)
- [ ] Consent explicit (private by default; shared by choice; collective by consent)
- [ ] Ownership resolved (GitHub → Smart Connect participation → member)
- [ ] Policy enforced (authority grant required for intelligence_commit)
- [ ] Fail-closed on all negative vectors
- [ ] Evidence: adversarial test matrix PASS

### 5. PERSISTENCE
- [ ] Cognition event created in nayanet_cognition_events
- [ ] Execution receipt created in nayanet_execution_receipts
- [ ] Smart Ledger entry created in nayanet_smart_ledger
- [ ] Project cognition state updated
- [ ] Evidence: independent Supabase read

### 6. RETRIEVAL
- [ ] Fresh context retrieves same canonical event
- [ ] Fresh context retrieves same Intelligent Block projection
- [ ] Fresh context retrieves same Smart Ledger verification
- [ ] Evidence: independent retrieval test

### 7. EVIDENCE
- [ ] Event ID visible in Hub
- [ ] Receipt ID visible in Hub
- [ ] Ledger hash/evidence visible
- [ ] Source event lineage traceable
- [ ] Authority grant lineage traceable
```

---

## 5. CURRENT DOOR STATUS MATRIX

| Door | Visual | Sender | Bridge | Authority | Persistence | Retrieval | Evidence | Overall |
|------|--------|--------|--------|-----------|-------------|-----------|----------|---------|
| **Smart Note** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **READY** |
| **Smart Share** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **READY** |
| **GitHub Webhook** | ⚠️ | ✅ (P4) | ✅ | ✅ | ✅ | ⏳ | ⏳ | **BLOCKED_EXTERNAL_CREDENTIAL** |
| **Smart Mail** | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | **PARTIAL** |
| **Smart Spaces** | ✅ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | **PARTIAL** |
| **Connections** | ✅ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | **PARTIAL** |
| **Smart Lists** | ✅ | ⚠️ | ✅ | ✅ | ✅ | ⚠️ | ⚠️ | **PARTIAL** |
| **MCP** | N/A | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | **PARTIAL** |
| **REST/OpenAPI** | N/A | ⚠️ | ✅ | ⚠️ | ⚠️ | ⚠️ | ⚠️ | **PARTIAL** |
| **A2A** | N/A | 📄 | 📄 | 📄 | 📄 | 📄 | 📄 | **DOCUMENTED** |
| **SDK** | N/A | 📄 | 📄 | 📄 | 📄 | 📄 | 📄 | **DOCUMENTED** |

**Legend:** ✅ PROVEN | ⚠️ PARTIAL/IMPLEMENTED | ⏳ BLOCKED | 📄 DOCUMENTED ONLY

---

## 6. SENDER IMPLEMENTATION STANDARDS

### 4.1 Event Schema (MANDATORY)
All senders MUST emit events conforming to `INTELLIGENT-EVENT-V1.md`:

```typescript
interface IntelligentEvent {
  event_id: string;           // "github:<delivery-id>" | "smart_note:<idempotency_key>" | "intelligence:<idempotency_key>"
  source_event_id: string;    // Original source identifier
  source_system: string;      // "github" | "nayanet-hub" | "nayanet-smart-mail" | "mcp" | "rest"
  event_type: string;         // Action type from source
  title: string;              // REQUIRED: Human-readable title (RPC extracts p_event->>'title')
  repository?: string;        // For GitHub: "owner/repo"
  ref?: string;               // Git ref
  commit_sha?: string;        // Commit SHA
  actor?: string;             // Actor identity
  occurred_at: string;        // ISO timestamp
  received_at: string;        // ISO timestamp (receiver sets)
  correlation_id: string;     // Correlation key
  idempotency_key: string;    // MUST be unique per logical event
  authority: {                // Provenance metadata, NOT execution authority
    source: string;
    scope: string;
  };
  provenance: {
    delivery_id?: string;
    provider?: string;
    installation_id?: string; // For GitHub
  };
  verification: {
    state: "SIGNED_WEBHOOK_VERIFIED" | "AUTHENTICATED_USER" | "SERVICE_ROLE" | "AGENT_PROTOCOL";
  };
  processing_state: "RECEIVED" | "PROCESSING" | "COMPLETED" | "FAILED";
  projection_targets: string[]; // ["Personal Intelligence", "Activity", "Intelligence Today"]
  payload: any;               // Full original payload
}
```

### 4.2 Idempotency (MANDATORY)
- `idempotency_key` MUST be globally unique per logical event
- Format: `<source_system>:<source_unique_identifier>`
- Examples: `github:<delivery-id>`, `smart_note:<idempotency_key>`, `intelligence:<idempotency_key>`
- Receiver uses `(user_id, project_id, event_id)` unique index for deduplication
- Exact replay returns `replayed=true` with original event/state/receipt

### 4.3 Authority Separation (MANDATORY)
- Sender events are **event sources**, NOT execution authority
- `action="github_webhook_received"` | `"smart_note_capture"` | `"smart_mail_send"` — NOT `"intelligence.capture"`
- `intelligence_commit` requires separate authority grant via `nayanet_issue_authority_grant`
- Sender MUST NOT mint or imply `intelligence_commit` authority

---

## 7. RECEIVER CONTRACT (Canonical)

The canonical receiver is the **single persistence seam**:

### 7.1 Entry Point
```sql
nayanet_record_cognition_event(
  p_project_id text,
  p_event jsonb,
  p_action text,
  p_expected_result text,
  p_observed_result text,
  p_learning jsonb,
  p_execution_authorization jsonb DEFAULT NULL
)
```

### 7.2 Authority Enforcement
- `action = 'intelligence.capture'` → REQUIRES `p_execution_authorization` with valid `intelligence_commit` grant
- `action = 'github_webhook_received'` | `'smart_note_capture'` | `'smart_feed_interaction'` → Service-role allowed WITH owner resolution
- Owner resolution: `auth.uid()` for authenticated; `execution_authorization.actor_id` for service-role
- Service-role path: independent re-validation via `nayanet_resolve_github_webhook_owner`

### 7.3 Persistence Guarantees
- Cognition event: `(user_id, project_id, event_id)` unique index
- Execution receipt: contiguous revision per user/project
- Smart Ledger: automatic trigger on cognition event insert
- Intelligence index: trigger on cognition event upsert

### 7.4 Replay Guarantee
```sql
-- If event exists with receipt_id:
SELECT original_event, original_state, original_receipt
RETURN {replayed: true, ...}
-- NO new receipt, NO state increment
```

---

## 8. VERIFICATION WORKFLOW (Per Door)

Each door MUST pass this workflow before claiming READY:

```yaml
# .github/workflows/verify-[door]-sender-receiver.yml
name: Verify [Door] Sender/Receiver Contract
on:
  workflow_dispatch:
  push:
    paths:
      - 'sender/source/**'
      - 'supabase/functions/[door]-**'
      - 'supabase/migrations/*[door]*'

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy sender (if Edge Function)
      - name: Deploy receiver migrations
      - name: Execute positive test (valid auth + payload)
      - name: Verify persistence (event + receipt + Ledger + index)
      - name: Execute replay test (same idempotency_key)
      - name: Verify replay returns original (replayed=true, no new receipt)
      - name: Execute negative tests (missing auth, wrong auth, wrong owner, invalid payload)
      - name: Verify all negative tests fail closed
      - name: Execute retrieval test (fresh context)
      - name: Verify retrieval returns canonical object
      - name: Execute evidence test (UI + receipt show provenance)
      - name: Generate evidence artifact
```

---

## 9. NEXT ACTIONS (Priority Order)

| Priority | Door | Action | Blocker |
|----------|------|--------|---------|
| P0 | GitHub Webhook | Deploy v5 (title fix) + configure GITHUB_WEBHOOK_SECRET + bind installation | External credential |
| P0 | GitHub Webhook | Execute controlled signed delivery proof | Credential + bind |
| P1 | Smart Mail | Complete sender contract (7 boundaries) | Sender implementation |
| P1 | Smart Spaces | Complete sender contract (7 boundaries) | Sender implementation |
| P1 | Connections | Complete sender contract (7 boundaries) | Sender implementation |
| P1 | Smart Lists | Complete sender contract (7 boundaries) | Sender implementation |
| P1 | MCP | Deploy + authenticate + prove 7 boundaries | Deployed source |
| P1 | REST/OpenAPI | Deploy + authenticate + prove 7 boundaries | Deployed source |
| P2 | A2A | Implement sender + prove 7 boundaries | Architecture decision |
| P2 | SDK | Implement sender + prove 7 boundaries | Architecture decision |

---

## 10. GOVERNANCE RULES

1. **No second persistence seam** — All doors converge on `nayanet_record_cognition_event`
2. **No second authority model** — All doors use `intelligence_commit` grant
3. **No second event store** — All doors write to `nayanet_cognition_events`
4. **No second index** — All doors project to `nayanet_intelligence_index`
5. **No second Ledger** — All doors trigger `nayanet_smart_ledger`
6. **Private by default** — Events visible only to resolved owner
7. **Shared by choice** — Publication requires explicit consent + authority grant
8. **Collective by consent** — Collective feed requires publication + consent
9. **Public by decision** — Human decision required for public exposure
10. **Sender ≠ Authority** — Event source never implies execution permission

---

## 11. EVIDENCE REGISTRY

| Door | Positive Proof | Replay Proof | Negative Proof | Retrieval Proof | Evidence Proof |
|------|----------------|--------------|----------------|-----------------|----------------|
| Smart Note | Run 35898728927 | Run 35898728927 | Run 35898728927 | Run 35898728927 | Run 35898728927 |
| Smart Share | Run 35553013422 | Run 35553013422 | Run 35553013422 | Run 35553013422 | Run 35553013422 |
| GitHub Webhook | **BLOCKED** | **BLOCKED** | **BLOCKED** | **BLOCKED** | **BLOCKED** |
| Smart Mail | Learning bridge | — | — | — | — |
| Intelligent Block | Run 35906051544 | Run 35906051544 | Run 35906051544 | Run 35906051544 | Run 35906051544 |

---

## 12. SIGN-OFF

This contract is the canonical sender/receiver readiness standard for NayaPOWER.

**A door is not complete because its screen exists.**  
**A door is complete when all seven boundaries have independent runtime evidence.**

```
[CONTROL PLANE][CONTRACT]
SENDER-RECEIVER-READINESS-CONTRACT-V1
Status: ACTIVE
Next Review: After each door proof completion
```