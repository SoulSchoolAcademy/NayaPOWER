# Smart Lists Door Contract

**Door ID:** SMART-LISTS
**Type:** HUMAN_UI
**Status:** PARTIAL
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL ⚠️
- **Discoverable:** Lists management in Hub
- **Coherent:** Matches Hub DNA
- **Responsive:** Desktop + mobile (needs verification)
- **Evidence:** Route exists; whole-journey proof incomplete

### 2. SENDER ⚠️
- **Single canonical event:** List create/add/remove → one event per action
- **Event schema:** `event_id=list:<action>:<idempotency_key>`, source_system=nayanet-hub
- **Title:** "List {action}: {list_name}"
- **Source:** Hub Lists UI → nayanet_smart_list RPCs
- **Evidence:** Substrate proven; sender contract incomplete

### 3. BRIDGE ✅
- **Boundary:** nayanet_smart_list RPCs (create, add, remove)
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** Smart List substrate proven

### 4. AUTHORITY ✅
- **Identity:** Authenticated user
- **Scope:** Owner's lists only (owner_id = auth.uid())
- **Consent:** Private by default; list membership is owner's decision
- **Ownership:** List owned by creator
- **Policy:** List actions require ownership; no authority minting
- **Fail-closed:** Non-owner cannot create/add/remove, wrong scope denied
- **Evidence:** Smart List substrate proven

### 5. PERSISTENCE ✅
- **List record:** nayanet_smart_lists (owner_id, title, config)
- **List membership:** nayanet_smart_list_membership (list_id, connection_id, status)
- **Cognition event:** nayanet_cognition_events for list actions
- **Execution receipt:** nayanet_execution_receipts
- **Smart Ledger:** Trigger on cognition insert
- **Evidence:** Smart List substrate proven

### 6. RETRIEVAL ⚠️
- **Fresh context:** Lists view + list detail
- **Canonical object:** Same list_id, same membership_id
- **Evidence:** Substrate retrieval proven; whole-journey incomplete

### 7. EVIDENCE ⚠️
- **Event ID:** Visible in list activity
- **Receipt ID:** Visible
- **Ledger hash:** Verification state displayed
- **Source lineage:** List action → membership → cognition event traceable
- **Authority lineage:** Owner consent → action traceable

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | Substrate proofs | — | PASS |
| Replay | Substrate proofs | — | PASS |
| Negative | Substrate proofs | — | PASS |
| Retrieval | — | — | PARTIAL |
| Evidence | — | — | PARTIAL |

---

## Remaining Work

- [ ] Complete sender contract with independent evidence
- [ ] Fresh retrieval proof (post-reload)
- [ ] Whole human journey: CREATE → ADD → VIEW → REMOVE → RELOAD

---

## Next Authorized Action

Complete Smart Lists sender contract with independent runtime evidence.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: SMART-LISTS
STATUS: PARTIAL
EVIDENCE: SUBSTRATE_PROVEN / SENDER_CONTRACT_INCOMPLETE
```