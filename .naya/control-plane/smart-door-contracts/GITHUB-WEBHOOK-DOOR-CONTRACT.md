# GitHub Webhook Door Contract

**Door ID:** GITHUB-WEBHOOK
**Type:** EXTERNAL_WEBHOOK
**Status:** BLOCKED_EXTERNAL_CREDENTIAL
**Version:** 1.0
**Last Updated:** 2026-09-25

---

## Seven Boundary Proof

### 1. VISUAL ⚠️
- **Discoverable:** Not a visual Hub surface (external webhook ingress)
- **Coherent:** N/A — external system
- **Responsive:** N/A
- **Evidence:** N/A (external sender)

### 2. SENDER ⚠️ (SOURCE IMPLEMENTED, DEPLOYMENT PENDING)
- **Single canonical event:** GitHub webhook delivery → one event per delivery
- **Event schema:** `event_id=github:<delivery-id>`, source_system=github
- **Title:** `GitHub ${action} on ${repo}` (added in fix commit 953364d1)
- **Source:** `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts` (v5 pending deploy)
- **Event fields:** repository, ref, commit_sha, actor, occurred_at, correlation_id, idempotency_key, authority, provenance, verification, projection_targets
- **Evidence:** Source verified at HEAD 953364d1; deployed v4 lacks title fix

### 3. BRIDGE ⚠️ (DEPLOYED, CREDENTIAL BLOCKED)
- **Boundary:** nayanet-github-webhook Edge Function (v4 deployed, v5 pending)
- **Contract:** RECEIVE → VERIFY SIGNATURE → NORMALIZE → OWNER BINDING → STORE → INDEX → PROJECT
- **Owner binding:** nayanet_resolve_github_webhook_owner(installation_id, repository)
- **Evidence:** Source verified; live probe returns HTTP 503 GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED

### 4. AUTHORITY ⚠️ (IMPLEMENTED, BLOCKED)
- **Identity:** GitHub installation + repository → Smart Connect participation → member owner
- **Scope:** Installation ID + repository (bound in Smart Connect external_bindings)
- **Consent:** Private by default; participation ≠ authority
- **Ownership:** Resolved via nayanet_resolve_github_webhook_owner (service-role only)
- **Policy:** action=github_webhook_received (NOT intelligence.capture); no authority minting
- **Fail-closed:** Missing secret, missing delivery, invalid signature, missing installation, missing repo, unresolved owner, ambiguous owner, revoked binding
- **Evidence:** Source logic verified; live proof BLOCKED

### 5. PERSISTENCE ⏳ (BLOCKED ON CREDENTIAL)
- **Cognition event:** nayanet_cognition_events (user_id = resolved owner)
- **Execution receipt:** nayanet_execution_receipts
- **Smart Ledger:** Trigger on cognition insert
- **Intelligence index:** Trigger on cognition upsert
- **Evidence:** NOT RUN — blocked on GITHUB_WEBHOOK_SECRET

### 6. RETRIEVAL ⏳ (BLOCKED ON CREDENTIAL)
- **Fresh context:** Smart Feed personal/activity streams for resolved owner
- **Canonical object:** Same event_id, same receipt_id
- **Evidence:** NOT RUN — blocked on credential

### 7. EVIDENCE ⏳ (BLOCKED ON CREDENTIAL)
- **Event ID:** Will be visible in Smart Feed
- **Receipt ID:** Will be visible in Smart Feed
- **Ledger hash:** Will be displayed
- **Source lineage:** GitHub delivery → owner binding → cognition event traceable
- **Authority lineage:** No authority grant (event source only)

---

## External Blockers

| Blocker | Type | Resolution |
|---------|------|------------|
| GITHUB_WEBHOOK_SECRET | EXTERNAL_CREDENTIAL | Authorized operator must configure in Supabase project dahisasgpfvziswqvmvm |
| GitHub App installation | PREREQUISITE | Human must install App on target repository |
| Smart Connect binding | PREREQUISITE | Bind installation+repo via nayanet_smart_connect_github_bind |

---

## Evidence Registry

| Proof Type | Run ID | Job ID | Status |
|------------|--------|--------|--------|
| Positive | — | — | BLOCKED_EXTERNAL_CREDENTIAL |
| Replay | — | — | BLOCKED_EXTERNAL_CREDENTIAL |
| Negative | — | — | BLOCKED_EXTERNAL_CREDENTIAL |
| Retrieval | — | — | BLOCKED_EXTERNAL_CREDENTIAL |
| Evidence | — | — | BLOCKED_EXTERNAL_CREDENTIAL |

---

## Remaining Work

- [ ] Deploy webhook v5 (with title fix) to Supabase Edge Function
- [ ] Configure GITHUB_WEBHOOK_SECRET in Supabase
- [ ] Install GitHub App on target repository
- [ ] Bind installation+repository in Smart Connect participation
- [ ] Execute controlled signed webhook delivery proof
- [ ] Verify exact replay returns original receipt
- [ ] Verify fresh retrieval by resolved owner
- [ ] Verify authority separation (webhook event ≠ intelligence_commit)

---

## Next Authorized Action

**Deploy webhook v5 to Supabase, then authorized operator configures GITHUB_WEBHOOK_SECRET.**

---

## Sign-off

```
[CONTROL PLANE][SMART-DOOR-CONTRACT]
DOOR: GITHUB-WEBHOOK
STATUS: BLOCKED_EXTERNAL_CREDENTIAL
EVIDENCE: SOURCE_VERIFIED / DEPLOYMENT_PENDING / LIVE_PROOF_BLOCKED
```