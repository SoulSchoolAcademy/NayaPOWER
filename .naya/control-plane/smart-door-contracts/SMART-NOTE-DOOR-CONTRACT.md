# Smart Note Door Contract

**Door ID:** SMART-NOTE
**Type:** HUMAN_UI
**Status:** PROVEN
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL ✅
- **Discoverable:** Central capture surface in Hub
- **Coherent:** Matches protected Hub DNA (2026 09 17 NAYANET HUB.html)
- **Responsive:** Desktop + mobile verified
- **Evidence:** Human Surface Completeness run 35773282882

### 2. SENDER ✅
- **Single canonical event:** Smart Note capture → one event per action
- **Event schema:** `event_id=smart_note:<idempotency_key>`, source_system=nayanet-hub
- **Title:** Human note subject (required by RPC)
- **Source:** `supabase/functions/v7-smart-note-canonical/index.ts`
- **Evidence:** Run 35898728927 — 17/17 machine checks PASS

### 3. BRIDGE ✅
- **Boundary:** v7-smart-note-canonical Edge Function
- **Contract:** RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT
- **Evidence:** Run 35898728927 bridge trace PASS

### 4. AUTHORITY ✅
- **Identity:** Authenticated user (Bearer token)
- **Scope:** User's own cognition events (RLS: user_id=auth.uid())
- **Consent:** Private by default; explicit consent for publication
- **Ownership:** Event user_id = auth.uid()
- **Policy:** intelligence_commit requires grant (not used by Smart Note capture)
- **Fail-closed:** Wrong owner rejected, unauthorized rejected
- **Evidence:** Run 35898728927 wrong-owner rejection PASS

### 5. PERSISTENCE ✅
- **Cognition event:** nayanet_cognition_events (user_id, project_id, event_id unique)
- **Execution receipt:** nayanet_execution_receipts (contiguous revision)
- **Smart Ledger:** nayanet_smart_ledger (trigger on cognition insert)
- **Intelligence index:** nayanet_intelligence_index (trigger on cognition upsert)
- **Evidence:** Run 35898728927 independent Supabase read PASS

### 6. RETRIEVAL ✅
- **Fresh context:** Smart Feed personal/activity streams
- **Canonical object:** Same event_id, same receipt_id, same Ledger hash
- **Evidence:** Run 35898728927 fresh retrieval + reload PASS

### 7. EVIDENCE ✅
- **Event ID:** Visible in Smart Feed
- **Receipt ID:** Visible in Smart Feed
- **Ledger hash:** Verification state + confidence displayed
- **Source lineage:** Smart Note → cognition event → index → Feed traceable
- **Authority lineage:** Not applicable (capture action)

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | 35898728927 | 107309129922 | PASS |
| Replay | 35898728927 | 107309129922 | PASS |
| Negative | 35898728927 | 107309129922 | PASS |
| Retrieval | 35898728927 | 107309129922 | PASS |
| Evidence | 35898728927 | 107309129922 | PASS |

---

## Remaining Work

- [ ] Universal meaningful-output promotion (generalize intelligence_commit boundary)
- [ ] Broader knowledge-type coverage beyond Smart Notes

---

## Next Authorized Action

Generalize the canonical intelligence-commit boundary to every meaningful Naya output available inside NayaPOWER.

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: SMART-NOTE
STATUS: PROVEN
EVIDENCE: COMPLETE
```