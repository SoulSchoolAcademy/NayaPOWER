# Smart Mail Door Contract

**Door ID:** SMART-MAIL
**Type:** HUMAN_UI
**Status:** PARTIAL
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL ⚠️
- **Discoverable:** Smart Mail compose/send UI in Hub
- **Coherent:** Matches Hub DNA
- **Responsive:** Desktop + mobile (needs verification)
- **Evidence:** Route exists; whole-journey proof incomplete

### 2. SENDER ⚠️
- **Single canonical event:** Mail send → one event per action
- **Event schema:** `event_id=smart_mail:<idempotency_key>`, source_system=nayanet-smart-mail
- **Title:** "Smart Mail: {subject}"
- **Source:** `supabase/functions/nayanet-smart-mail/index.ts`
- **Evidence:** Learning bridge proven; full sender contract incomplete

### 3. BRIDGE ✅
- **Boundary:** nayanet-smart-mail Edge Function
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** Smart Mail learning bridge run proven

### 4. AUTHORITY ✅
- **Identity:** Authenticated user
- **Scope:** User's connections (mutual Connections required)
- **Consent:** Recipient consent via Connection
- **Ownership:** Sender = auth.uid(); recipient = connection target
- **Policy:** smart_mail_send authority grant required (explicit grant)
- **Fail-closed:** No grant denied, non-connection denied, revoked grant denied
- **Evidence:** Wave A security run 35462235010: smart_mail_send authority + revocation denial PASS

### 5. PERSISTENCE ✅
- **Mail record:** smart_mail table (sender, recipient, thread, status)
- **Cognition event:** nayanet_cognition_events for sender + recipient
- **Execution receipt:** nayanet_execution_receipts
- **Smart Ledger:** Trigger on cognition insert
- **Evidence:** Learning bridge: message → receipt → cognition → Ledger

### 6. RETRIEVAL ⚠️
- **Fresh context:** Smart Feed / mail thread view
- **Canonical object:** Same mail_id, same thread_id
- **Evidence:** Sender retrieval proven; recipient retrieval needs verification

### 7. EVIDENCE ✅
- **Event ID:** Visible in Smart Feed / mail thread
- **Receipt ID:** Visible
- **Ledger hash:** Verification state displayed
- **Source lineage:** Mail send → receipt → cognition → Ledger → learning evidence traceable
- **Authority lineage:** smart_mail_send grant → mail event traceable

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | Learning bridge | — | PASS |
| Replay | — | — | NOT VERIFIED |
| Negative | Wave A 35462235010 | — | PASS (authority) |
| Retrieval | — | — | PARTIAL |
| Evidence | Learning bridge | — | PASS |

---

## Remaining Work

- [ ] Complete sender contract (7 boundaries with independent evidence)
- [ ] Replay/idempotency proof for mail send
- [ ] Recipient fresh retrieval proof
- [ ] Visual verification on desktop + mobile
- [ ] Whole human journey: COMPOSE → SEND → RECEIPT → THREAD → REPLY → CONTINUE

---

## Next Authorized Action

Complete Smart Mail sender contract with independent runtime evidence for all 7 boundaries.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: SMART-MAIL
STATUS: PARTIAL
EVIDENCE: LEARNING_BRIDGE_PROVEN / SENDER_CONTRACT_INCOMPLETE
```