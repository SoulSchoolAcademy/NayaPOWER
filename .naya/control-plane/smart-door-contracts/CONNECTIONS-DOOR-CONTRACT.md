# Connections Door Contract

**Door ID:** CONNECTIONS
**Type:** HUMAN_UI
**Status:** PARTIAL
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL ⚠️
- **Discoverable:** Connections management in Hub
- **Coherent:** Matches Hub DNA
- **Responsive:** Desktop + mobile (needs verification)
- **Evidence:** Route exists; whole-journey proof incomplete

### 2. SENDER ⚠️
- **Single canonical event:** Connection create/revoke → one event per action
- **Event schema:** `event_id=connection:<action>:<idempotency_key>`, source_system=nayanet-hub
- **Title:** "Connection {action}: {target_name}"
- **Source:** Hub Connections UI → nayanet_connections RPCs
- **Evidence:** Substrate proven; sender contract incomplete

### 3. BRIDGE ✅
- **Boundary:** nayanet_connections RPCs (connect, revoke)
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** Wave A run 35462235010: relationship substrate proven

### 4. AUTHORITY ✅
- **Identity:** Authenticated user
- **Scope:** Owner's connections only (owner_member_id = auth.uid())
- **Consent:** Private by default; connection is owner's decision
- **Ownership:** Connection owned by creator (owner_member_id)
- **Policy:** Connection actions require ownership; no authority minting
- **Fail-closed:** Non-owner cannot create/revoke, wrong scope denied
- **Evidence:** Wave A run 35462235010: owner/non-owner isolation + revocation PASS

### 5. PERSISTENCE ✅
- **Connection record:** nayanet_connections (owner_member_id, connected_member_id, status)
- **Cognition event:** nayanet_cognition_events for connect/revoke
- **Execution receipt:** nayanet_execution_receipts
- **Smart Ledger:** Trigger on cognition insert
- **Evidence:** Wave A run 35462235010 persistence PASS

### 6. RETRIEVAL ⚠️
- **Fresh context:** Connections list + detail view
- **Canonical object:** Same connection_id, same owner
- **Evidence:** Non-owner retrieval = 0 (proven); owner retrieval needs fresh proof

### 7. EVIDENCE ✅
- **Event ID:** Visible in connection activity
- **Receipt ID:** Visible
- **Ledger hash:** Verification state displayed
- **Source lineage:** Connection action → nayanet_connections → cognition event traceable
- **Authority lineage:** Owner consent → action traceable

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | Wave A 35462235010 | — | PASS (substrate) |
| Replay | Wave A 35462235010 | — | PASS (idempotent) |
| Negative | Wave A 35462235010 | — | PASS (isolation) |
| Retrieval | Wave A 35462235010 | — | PARTIAL |
| Evidence | Wave A 35462235010 | — | PASS |

---

## Remaining Work

- [ ] Complete sender contract with independent evidence
- [ ] Fresh owner retrieval proof (post-reload)
- [ ] Whole human journey: CONNECT → VIEW → REVOKE → RELOAD → VERIFY

---

## Next Authorized Action

Complete Connections sender contract with independent runtime evidence.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: CONNECTIONS
STATUS: PARTIAL
EVIDENCE: SUBSTRATE_PROVEN / SENDER_CONTRACT_INCOMPLETE
```