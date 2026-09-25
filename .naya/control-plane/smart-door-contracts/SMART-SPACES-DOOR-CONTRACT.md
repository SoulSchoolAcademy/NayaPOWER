# Smart Spaces Door Contract

**Door ID:** SMART-SPACES
**Type:** HUMAN_UI
**Status:** PARTIAL
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL ⚠️
- **Discoverable:** Spaces navigation in Hub sidebar
- **Coherent:** Matches Hub DNA
- **Responsive:** Desktop + mobile (needs verification)
- **Evidence:** Route exists; whole-journey proof incomplete

### 2. SENDER ⚠️
- **Single canonical event:** Space create/join/leave → one event per action
- **Event schema:** `event_id=space:<action>:<idempotency_key>`, source_system=nayanet-hub
- **Title:** "Space {action}: {space_name}"
- **Source:** Hub Smart Spaces UI → nayanet-space-membership RPCs
- **Evidence:** Substrate proven; sender contract incomplete

### 3. BRIDGE ✅
- **Boundary:** nayanet_space_membership RPCs (join, leave, create)
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** Wave A run 35462235010: private/shared substrate proven

### 4. AUTHORITY ✅
- **Identity:** Authenticated user
- **Scope:** Space membership (member_id = auth.uid())
- **Consent:** Private by default; shared by choice (invite/join)
- **Ownership:** Space creator = owner; members = participants
- **Policy:** Space actions require membership; no authority minting
- **Fail-closed:** Non-member cannot join/leave/create, revoked membership denied
- **Evidence:** Wave A run 35462235010: isolation + authorization PASS

### 5. PERSISTENCE ✅
- **Space record:** nayanet_spaces (owner_id, status, config)
- **Membership record:** nayanet_space_membership (member_id, space_id, status)
- **Cognition event:** nayanet_cognition_events for join/create
- **Execution receipt:** nayanet_execution_receipts
- **Smart Ledger:** Trigger on cognition insert
- **Evidence:** Wave A run 35462235010 persistence PASS

### 6. RETRIEVAL ⚠️
- **Fresh context:** Spaces list + space detail view
- **Canonical object:** Same space_id, same membership_id
- **Evidence:** Substrate retrieval proven; whole-journey incomplete

### 7. EVIDENCE ⚠️
- **Event ID:** Visible in space activity
- **Receipt ID:** Visible
- **Ledger hash:** Verification state displayed
- **Source lineage:** Space action → membership → cognition event traceable
- **Authority lineage:** Membership consent → action traceable

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | Wave A 35462235010 | — | PASS (substrate) |
| Replay | — | — | NOT VERIFIED |
| Negative | Wave A 35462235010 | — | PASS (isolation) |
| Retrieval | — | — | PARTIAL |
| Evidence | — | — | PARTIAL |

---

## Remaining Work

- [ ] Complete sender contract with independent evidence
- [ ] Replay/idempotency proof for space actions
- [ ] Whole human journey: CREATE → INVITE → JOIN → ACTIVITY → LEAVE → RELOAD

---

## Next Authorized Action

Complete Smart Spaces sender contract with independent runtime evidence.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: SMART-SPACES
STATUS: PARTIAL
EVIDENCE: SUBSTRATE_PROVEN / SENDER_CONTRACT_INCOMPLETE
```