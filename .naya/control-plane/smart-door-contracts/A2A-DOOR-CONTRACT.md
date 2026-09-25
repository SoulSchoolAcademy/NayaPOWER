# A2A Door Contract

**Door ID:** A2A
**Type:** AGENT_PROTOCOL
**Status:** DOCUMENTED
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL N/A
- **Discoverable:** Not a visual Hub surface (future protocol)
- **Coherent:** Protocol design compliance
- **Responsive:** N/A
- **Evidence:** N/A (future)

### 2. SENDER 📄
- **Single canonical event:** A2A message/task → one event per message
- **Event schema:** `event_id=a2a:<message_id>`, source_system=a2a
- **Title:** "A2A Message: {task_type}"
- **Source:** A2A client → bridge (not yet implemented)
- **Evidence:** Documented contract only; no implementation

### 3. BRIDGE 📄
- **Boundary:** A2A adapter → nayanet-project-intelligence-bridge (future)
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** Future channel; no broad-use production proof

### 4. AUTHORITY 📄
- **Identity:** A2A agent authentication
- **Scope:** Agent + task + project + target
- **Consent:** Explicit consent where required
- **Ownership:** A2A agent identity → resolved member
- **Policy:** Authority independently evaluated; agent relationship ≠ execution permission
- **Fail-closed:** Agent credential/grant/task revocation must block
- **Evidence:** Documented only

### 5. PERSISTENCE 📄
- **Cognition event:** nayanet_cognition_events (future)
- **Execution receipt:** nayanet_execution_receipts
- **Smart Ledger:** Trigger on cognition insert
- **Intelligence index:** Trigger on cognition upsert
- **Evidence:** Future

### 6. RETRIEVAL 📄
- **Fresh context:** A2A agent retrieval via bridge
- **Canonical object:** Same event_id, same receipt_id
- **Evidence:** Future

### 7. EVIDENCE 📄
- **Event ID:** Returned to A2A agent
- **Receipt ID:** Returned to A2A agent
- **Ledger hash:** Available via bridge
- **Source lineage:** A2A message → bridge → cognition event
- **Authority lineage:** Grant → A2A action traceable

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | — | — | DOCUMENTED ONLY |
| Replay | — | — | DOCUMENTED ONLY |
| Negative | — | — | DOCUMENTED ONLY |
| Retrieval | — | — | DOCUMENTED ONLY |
| Evidence | — | — | DOCUMENTED ONLY |

---

## Remaining Work

- [ ] Define A2A adapter architecture
- [ ] Implement A2A → bridge integration
- [ ] Define agent identity resolution
- [ ] Prove agent participation ≠ authority
- [ ] Prove revocation blocks subsequent A2A actions
- [ ] Prove replay/idempotency semantics
- [ ] Prove semantic parity with MCP/REST

---

## Next Authorized Action

Define A2A adapter architecture and integration seam.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: A2A
STATUS: DOCUMENTED
EVIDENCE: NO_IMPLEMENTATION / FUTURE_CHANNEL
```