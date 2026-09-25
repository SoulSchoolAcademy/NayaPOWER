# MCP Door Contract

**Door ID:** MCP
**Type:** AGENT_PROTOCOL
**Status:** PARTIAL
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL N/A
- **Discoverable:** Not a visual Hub surface (protocol interface)
- **Coherent:** Protocol compliance
- **Responsive:** N/A
- **Evidence:** N/A (protocol)

### 2. SENDER ⚠️
- **Single canonical event:** MCP tool call → one event per call
- **Event schema:** `event_id=mcp:<tool>:<idempotency_key>`, source_system=mcp
- **Title:** "MCP Tool Call: {tool_name}"
- **Source:** MCP server → nayanet-compound-intelligence / nayanet-project-intelligence-bridge
- **Evidence:** Architecture defined; authenticated deployed proof open

### 3. BRIDGE ⚠️
- **Boundary:** Universal Agent Interface → nayanet-project-intelligence-bridge
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** UAI bridge exists; MCP transport proof open

### 4. AUTHORITY ⚠️
- **Identity:** MCP session authentication
- **Scope:** Tool + project + target (server-side enforcement)
- **Consent:** Explicit consent where required
- **Ownership:** MCP client identity → resolved member
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
- **Fresh context:** MCP client retrieval via bridge
- **Canonical object:** Same event_id, same receipt_id
- **Evidence:** Architecture defined; runtime proof open

### 7. EVIDENCE ⚠️
- **Event ID:** Returned to MCP client
- **Receipt ID:** Returned to MCP client
- **Ledger hash:** Available via bridge retrieval
- **Source lineage:** MCP call → bridge → cognition event traceable
- **Authority lineage:** Grant → tool call traceable

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

- [ ] Deploy MCP server with authenticated transport
- [ ] Prove authenticated MCP initialization → tools/list → cold restore → understand → retrieve
- [ ] Prove MCP participation ≠ authority (no grant from connection)
- [ ] Prove smart_mail_send authority via MCP
- [ ] Prove revocation blocks subsequent MCP calls
- [ ] Prove replay/idempotency semantics match canonical receiver
- [ ] Prove semantic parity with REST/OpenAPI

---

## Next Authorized Action

Deploy MCP server and execute authenticated transport/persistence/retrieval proof.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: MCP
STATUS: PARTIAL
EVIDENCE: ARCHITECTURE_DEFINED / DEPLOYED_PROOF_OPEN
```