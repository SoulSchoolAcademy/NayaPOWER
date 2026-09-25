# REST/OpenAPI Door Contract

**Door ID:** REST-OPENAPI
**Type:** AGENT_PROTOCOL
**Status:** PARTIAL
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL N/A
- **Discoverable:** Not a visual Hub surface (API interface)
- **Coherent:** OpenAPI spec compliance
- **Responsive:** N/A
- **Evidence:** N/A (API)

### 2. SENDER ⚠️
- **Single canonical event:** REST API call → one event per call
- **Event schema:** `event_id=rest:<endpoint>:<idempotency_key>`, source_system=rest
- **Title:** "REST API Call: {method} {endpoint}"
- **Source:** REST client → nayanet-project-intelligence-bridge / nayanet-compound-intelligence
- **Evidence:** Architecture defined; authenticated deployed proof open

### 3. BRIDGE ⚠️
- **Boundary:** Universal Agent Interface → nayanet-project-intelligence-bridge
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** UAI bridge exists; REST transport proof open

### 4. AUTHORITY ⚠️
- **Identity:** API authentication (Bearer token / API key)
- **Scope:** Endpoint + project + target (server-side enforcement)
- **Consent:** Explicit consent where required
- **Ownership:** API client identity → resolved member
- **Policy:** Same authority lifecycle as MCP; transport ≠ authority
- **Fail-closed:** Credential/grant revocation must fail closed
- **Evidence:** Architecture defined; runtime proof open

### 5. PERSISTENCE ⚠️
- **Cognition event:** nayanet_cognition_events (via bridge)
- **Execution receipt:** nayanet_execution_receipts
- **Smart Ledger:** Trigger on cognition insert
- **Intelligence index:** Trigger on cognition upsert
- **Evidence:** Architecture defined; runtime proof open

### 6. RETRIEVAL ⚠️
- **Fresh context:** REST client retrieval via bridge
- **Canonical object:** Same event_id, same receipt_id
- **Evidence:** Architecture defined; runtime proof open

### 7. EVIDENCE ⚠️
- **Event ID:** Returned in API response
- **Receipt ID:** Returned in API response
- **Ledger hash:** Available via bridge retrieval
- **Source lineage:** REST call → bridge → cognition event traceable
- **Authority lineage:** Grant → API call traceable

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | — | — | NOT VERIFIED |
| Replay | — | — | NOT VERIFIED |
| Negative | — | — | NOT VERIFIED |
| Retrieval | — | — | NOT VERIFIED |
| Evidence | — | — | NOT VERIFIED |

---

## Remaining Work

- [ ] Deploy REST/OpenAPI gateway with authenticated transport
- [ ] Prove authenticated REST cold restore → understand → retrieve
- [ ] Prove REST participation ≠ authority (no grant from connection)
- [ ] Prove intelligence_commit authority via REST
- [ ] Prove revocation blocks subsequent REST calls
- [ ] Prove replay/idempotency semantics match canonical receiver
- [ ] Prove semantic parity with MCP (same identity → same authority → same canonical object → same persistence → same receipt → same retrieval)

---

## Next Authorized Action

Deploy REST/OpenAPI gateway and execute authenticated transport/persistence/retrieval proof with MCP parity.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: REST-OPENAPI
STATUS: PARTIAL
EVIDENCE: ARCHITECTURE_DEFINED / DEPLOYED_PROOF_OPEN
```