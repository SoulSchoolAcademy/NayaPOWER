# Smart Share Door Contract

**Door ID:** SMART-SHARE
**Type:** HUMAN_UI
**Status:** PROVEN
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL ✅
- **Discoverable:** Share action in Smart Feed item menu
- **Coherent:** Matches Hub DNA
- **Responsive:** Desktop + mobile verified
- **Evidence:** Smart Share production proof

### 2. SENDER ✅
- **Single canonical event:** Share action → one event per action
- **Event schema:** `event_id=intelligence:<idempotency_key>`, source_system=nayanet-hub
- **Title:** "Shared: {intelligence_event_title}"
- **Source:** `supabase/functions/nayanet-compound-intelligence/index.ts` (share action)
- **Evidence:** Run 35553013422 — all 27 gate requirements PASS

### 3. BRIDGE ✅
- **Boundary:** nayanet-compound-intelligence Edge Function (share action)
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** Run 35553013422 bridge trace PASS

### 4. AUTHORITY ✅
- **Identity:** Authenticated user (Bearer token)
- **Scope:** Owner's own intelligence events only
- **Consent:** Explicit consent_state='explicit' required for publication
- **Ownership:** intelligence_event_id must be owned by user (RLS)
- **Policy:** Publication requires explicit consent + owner validation
- **Fail-closed:** Non-owner cannot publish, wrong consent rejected
- **Evidence:** Run 35553013422 wrong-owner + wrong-consent rejection PASS

### 5. PERSISTENCE ✅
- **Publication record:** nayanet_intelligence_publications (upsert on intelligence_event_id)
- **Cognition event:** Original event unchanged
- **Execution receipt:** nayanet_execution_receipts for share action
- **Smart Ledger:** Trigger on publication insert
- **Evidence:** Run 35553013422 independent Supabase read PASS

### 6. RETRIEVAL ✅
- **Fresh context:** Collective Intelligence stream in Smart Feed
- **Canonical object:** Same publication_id, same intelligence_event_id
- **Evidence:** Run 35553013422 fresh retrieval PASS

### 7. EVIDENCE ✅
- **Publication ID:** Visible in collective stream
- **Receipt ID:** Visible in Smart Feed
- **Ledger hash:** Verification state displayed
- **Source lineage:** Original event → publication → collective stream traceable
- **Authority lineage:** Owner consent → publication grant traceable

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | 35553013422 | 10618664793 | PASS |
| Replay | 35553013422 | 10618664793 | PASS |
| Negative | 35553013422 | 10618664793 | PASS |
| Retrieval | 35553013422 | 10618664793 | PASS |
| Evidence | 35553013422 | 10618664793 | PASS |

---

## Remaining Work

- [ ] Current-head reconciliation where claim scope requires it

---

## Next Authorized Action

Apply Smart Door contract to next consequential door (Smart Mail).

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: SMART-SHARE
STATUS: PROVEN
EVIDENCE: COMPLETE
```