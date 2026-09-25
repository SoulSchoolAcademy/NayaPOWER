# SDK Door Contract

**Door ID:** SDK
**Type:** EMBEDDED_SDK
**Status:** DOCUMENTED
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL N/A
- **Discoverable:** Not a visual Hub surface (embedded library)
- **Coherent:** SDK design compliance
- **Responsive:** N/A
- **Evidence:** N/A (library)

### 2. SENDER 📄
- **Single canonical event:** SDK method call → one event per call
- **Event schema:** `event_id=sdk:<method>:<idempotency_key>`, source_system=sdk
- **Title:** "SDK Call: {method_name}"
- **Source:** SDK client → bridge (not independently verified)
- **Evidence:** Adapter concept exists; independent production door proof open

### 3. BRIDGE 📄
- **Boundary:** SDK adapter → nayanet-project-intelligence-bridge (future)
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** Documented; no independent production proof

### 4. AUTHORITY 📄
- **Identity:** Application/client authentication
- **Scope:** App + project + user + action
- **Consent:** Explicit action consent where required
- **Ownership:** SDK client identity → resolved member
- **Policy:** SDK delegates authority to governed runtime; local capability ≠ authority
- **Fail-closed:** App credential/grant revocation must block
- **Evidence:** Documented only

### 5. PERSISTENCE 📄
- **Cognition event:** nayanet_cognition_events (future)
- **Execution receipt:** nayanet_execution_receipts
- **Smart Ledger:** Trigger on cognition insert
- **Intelligence index:** Trigger on cognition upsert
- **Evidence:** Future

### 6. RETRIEVAL 📄
- **Fresh context:** SDK client retrieval via bridge
- **Canonical object:** Same event_id, same receipt_id
- **Evidence:** Future

### 7. EVIDENCE 📄
- **Event ID:** Returned to SDK client
- **Receipt ID:** Returned to SDK client
- **Ledger hash:** Available via bridge
- **Source lineage:** SDK call → bridge → cognition event
- **Authority lineage:** Grant → SDK action traceable

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

- [ ] Audit whether actual SDK adapter exists in production source
- [ ] If absent: keep DOCUMENTED/UNPROVEN rather than inventing
- [ ] If present: implement SDK → bridge integration
- [ ] Define SDK identity resolution
- [ ] Prove SDK participation ≠ authority
- [ ] Prove revocation blocks subsequent SDK actions
- [ ] Prove replay/idempotency semantics
- [ ] Prove semantic parity with MCP/REST

---

## Next Authorized Action

Audit SDK adapter existence in production source; if absent, document as UNPROVEN.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: SDK
STATUS: DOCUMENTED
EVIDENCE: NO_INDEPENDENT_VERIFICATION / ADAPTER_AUDIT_REQUIRED
```