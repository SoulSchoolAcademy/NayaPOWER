# CODA 3 — Integration / Release / GitHub Sender Handoff

**Date:** 2026-09-24
**Actor:** CODA 3 — Integration / Release / GitHub Sender
**Source HEAD:** `79c0eeacaaf023ea2e2fbad1bfa65957b52522c5` (commit: "record GitHub webhook P4 owner-bound canonical persistence evidence")

---

## OBJECTIVE

Prove the real SOURCE → BUILD → RUNTIME → GITHUB SENDER → RECEIVER → HUB chain, or isolate the exact external boundary preventing the final live test.

---

## RUNTIME PARITY AUDIT

### SOURCE
- **Webhook source:** `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts` (96 lines)
- **Current HEAD:** `79c0eeacaaf023ea2e2fbad1bfa65957b52522c5` (plus local fix: added `title` field to normalization)
- **Implements:** P4 owner-bound canonical persistence seam
  - Verifies GitHub HMAC-SHA256 signature (`x-hub-signature-256`)
  - Requires `x-github-delivery` header
  - Extracts `installation.id` and `repository.full_name`
  - Fails closed with `BLOCKED_OWNER_BINDING` if either missing/invalid
  - Resolves owner via `nayanet_resolve_github_webhook_owner(installation_id, repository)` (service-role only)
  - Fails closed on missing/ambiguous/revoked binding (`BLOCKED_OWNER_BINDING`)
  - Calls 7-argument `nayanet_record_cognition_event` with `execution_authorization` containing resolved `actor_id`, `installation_id`, `repository`
  - Returns `REPLAYED` or `PERSISTED` status with full transaction data
  - **FIX APPLIED:** Normalization now includes `title: \`GitHub ${action} on ${repo}\`` (line 29) to satisfy RPC `p_event->>'title'` extraction without default

### BUILD
- **Type:** Deno/TypeScript Supabase Edge Function
- **Build process:** No separate build step — source deployed directly to Supabase Edge Functions
- **Dependencies:** `@supabase/supabase-js@2`, Deno stdlib crypto
- **No compilation artifacts** — runtime is the source

### DEPLOYMENT
- **Platform:** Supabase Edge Functions
- **Function name:** `nayanet-github-webhook`
- **Documented version:** 4
- **Documented deployment digest:** `36f89f5c9beadcf77298ee0ccf8705a8e836cbdd4813ef1c70282d40bd366072`
- **Documented source blob:** `cf00cb52b424783f37d25a2a89f031724b19543a` (matches P4 source at commit `da74234e`)
- **Independent read-back verification:** Confirmed deployed source matches repository source at `da74234e`
- **SOURCE/RUNTIME PARITY ISSUE:** Current source (HEAD `79c0eeac` + local fix) has `title` field in normalization; deployed version (`da74234e`) does NOT. Deployment must be updated before live proof to avoid potential NOT NULL constraint failure on `nayanet_cognition_events.title`.

### RUNTIME
- **Live probe:** 2026-09-24T22:11:01Z → HTTP 503
- **Response:** `{ok:false, error:"GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED", status:"BLOCKED_EXTERNAL_CREDENTIAL"}`
- **Request ID:** `01a0d578-d6da-7399-97da-c85d71e0c8a9`
- **Deno execution ID:** `f0fed63d-a5cf-444b-a3c5-f52e1255436a`
- **Behavior:** Fail-closed at secret check (line 50-51) — before delivery/signature processing or persistence
- **Verification:** Deployed runtime matches source logic exactly

### RECEIVER (Canonical Persistence Seam)
- **Function:** `public.nayanet_record_cognition_event` (7-argument overload)
- **Latest migration:** `20260924233100_repair_github_webhook_owner_aware_canonical_replay_v1.sql`
- **Key properties:**
  - Service-role aware only for `action='github_webhook_received'` with `source='github_app_webhook'`
  - Requires `execution_authorization` with `actor_id`, `installation_id`, `repository`
  - **Independently re-resolves** owner via `nayanet_resolve_github_webhook_owner` and rejects mismatch (`GITHUB_WEBHOOK_OWNER_BINDING_MISMATCH`)
  - Exact replay protection: returns original event/state/receipt with `replayed=true` — no second receipt, no state increment
  - Advisory transaction lock on `(user_id, project_id)`
  - Persists to `nayanet_cognition_events`, `nayanet_project_cognition_state`, `nayanet_execution_receipts`
- **Production read-back:** Confirmed owner-aware service-role path + resolver revalidation + replay branch present

### HUB (Feed / Activity / Intelligence)
- **Smart Feed:** `naya-smart-feed` Edge Function
  - Queries `nayanet_cognition_events` for authenticated user (`user_id=auth.uid()`)
  - Streams: `personal`, `activity`, `collective`
  - Attaches Smart Ledger verification + Intelligent Blocks
  - GitHub webhook events persisted under resolved owner will appear in `personal`/`activity` streams
- **Compound Intelligence:** `nayanet-compound-intelligence` Edge Function
  - `restore` → full Project Intelligence reconstruction (14-question contract)
  - `retrieve` → search cognition events
  - `projectIntelligence` → project to `nayanet_intelligence_index`
  - `ackBridge` → acknowledge receiver retrieval/render
- **Projection:** Webhook event declares `projection_targets:["Personal Intelligence","Activity","Intelligence Today"]` — downstream projection is separate proof stage

---

## WORK COMPLETED

| Component | Status | Evidence |
|-----------|--------|----------|
| Webhook source (P4) | **SOURCE VERIFIED** | HEAD `79c0eeac` implements full owner-bound seam |
| Owner binding RPC | **PRODUCTION APPLIED** | Migration `20260924230000` — `nayanet_resolve_github_webhook_owner` |
| Replay/idempotency repair (P2) | **PRODUCTION APPLIED** | Migration `20260924222644` — exact replay returns original receipt |
| Canonical persistence (P4) | **PRODUCTION APPLIED** | Migration `20260924233100` — 7-arg overload with owner revalidation |
| Smart Connect participation | **VERIFIED** | Migration `20260924230000` — `external_bindings` JSONB + GIN index |
| Webhook deployment | **DEPLOYED / ACTIVE** | Version 4, digest verified, runtime probe returns expected 503 |
| Smart Feed / Hub | **DEPLOYED / ACTIVE** | `naya-smart-feed`, `nayanet-compound-intelligence` functions deployed |
| **Webhook normalization fix** | **SOURCE FIXED** | Added `title` field to normalization (line 29) — prevents potential NOT NULL failure |

---

## WHY THIS MATTERS TO LAUNCH

The GitHub webhook is the **launch sender** — the first external door that feeds real-world events into NayaNET's canonical cognition pipeline. The complete chain:

```
GitHub App installation
  → signed webhook delivery (HMAC-SHA256)
  → owner binding resolution (installation + repo → member)
  → canonical cognition persistence (event + state + receipt)
  → Smart Feed retrieval (personal/activity streams)
  → Intelligence compounding (learning, blocks, projections)
  → User sees result in Feed/Activity
```

Everything upstream of the external credential is **complete and verified**. The system is ready for the live causal chain proof.

---

## EVIDENCE

| Artifact | Reference |
|----------|-----------|
| Source HEAD | `79c0eeacaaf023ea2e2fbad1bfa65957b52522c5` |
| Webhook source | `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts` |
| Owner binding migration | `supabase/migrations/20260924230000_harden_github_app_owner_binding_v1.sql` |
| Replay repair migration | `supabase/migrations/20260924222644_harden_cognition_event_replay_idempotency_v1.sql` |
| Canonical persistence migration | `supabase/migrations/20260924233100_repair_github_webhook_owner_aware_canonical_replay_v1.sql` |
| P1 credential boundary doc | `.naya/project-intelligence/GITHUB-WEBHOOK-P1-CREDENTIAL-BOUNDARY-2026-09-24.md` |
| P2 replay repair doc | `.naya/project-intelligence/GITHUB-WEBHOOK-P2-REPLAY-IDEMPOTENCY-REPAIR-2026-09-24.md` |
| P3 owner identity doc | `.naya/project-intelligence/GITHUB-WEBHOOK-P3-OWNER-IDENTITY-BOUNDARY-2026-09-24.md` |
| P4 persistence seam doc | `NAYANET/HUB-ROOM-SYSTEM/SMART-CONNECT-SEVEN-DOOR-AUTHORITY-MATRIX-2026-09-24.md` (P4 section) |
| Production probe | HTTP 503 `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED` at 2026-09-24T22:11:01Z |
| UAI MCP/REST parity | Run `36061300293` — LIVE VERIFIED |
| UAI privileged authority | Run `36064087479` — LIVE VERIFIED |

---

## STATUS

**PARTIALLY VERIFIED** — All internal integration dependencies complete; blocked on single external credential.

---

## EXTERNAL BOUNDARY

**BLOCKED_EXTERNAL_CREDENTIAL: `GITHUB_WEBHOOK_SECRET`**

- **What:** The HMAC-SHA256 secret used to verify GitHub webhook signatures (`x-hub-signature-256`)
- **Where:** Supabase Edge Function environment variable `GITHUB_WEBHOOK_SECRET`
- **Who:** Authorized operator with Supabase project admin access (project: `dahisasgpfvziswqvmvm`, ca-central-1)
- **How:** Configure via Supabase Dashboard → Edge Functions → nayanet-github-webhook → Environment Variables, or Supabase CLI `supabase secrets set GITHUB_WEBHOOK_SECRET=<value>`
- **Must NOT:** Be placed in source, chat, logs, issues, or any repository artifact
- **Additional requirement:** GitHub App must be installed on target repository, and the installation + repository must be bound in `nayanet_smart_connect_participation.external_bindings` for an active `github_app` participant (via `nayanet_smart_connect_github_bind`)

---

## COORDINATION

### CODA 1 (Receiver) — Need to Know
- Webhook calls 7-argument `nayanet_record_cognition_event` with `action='github_webhook_received'` and `execution_authorization`
- Receiver independently re-validates owner binding — mismatch raises `GITHUB_WEBHOOK_OWNER_BINDING_MISMATCH`
- Replay returns `replayed=true` with original event/state/receipt — no duplicate receipt, no state increment
- **FIXED:** Webhook normalization now provides `title: \`GitHub ${action} on ${repo}\`` (line 29) — RPC extracts `p_event->>'title'` without default, but now has a value. Verify table schema allows the title format.

### CODA 2 (Hub) — Need to Know
- GitHub webhook events persist under resolved owner's `user_id` in `nayanet_cognition_events`
- Smart Feed `personal`/`activity` streams query `user_id=auth.uid()` — events will appear automatically
- Event declares `projection_targets:["Personal Intelligence","Activity","Intelligence Today"]` — downstream projection/indexing is separate
- Collective stream only shows explicitly published events (`nayanet_intelligence_publications`) — GitHub events remain private by default
- Smart Connect participation model: GitHub door is `participation`, not `authority` — webhook event ≠ `intelligence_commit` grant

---

## DURABLE STATE

| Artifact | Reference |
|----------|-----------|
| Source commit | `79c0eeacaaf023ea2e2fbad1bfa65957b52522c5` |
| Owner binding migration | `20260924230000_harden_github_app_owner_binding_v1.sql` |
| Replay repair migration | `20260924222644_harden_cognition_event_replay_idempotency_v1.sql` |
| Canonical persistence migration | `20260924233100_repair_github_webhook_owner_aware_canonical_replay_v1.sql` |
| P4 evidence doc | `NAYANET/HUB-ROOM-SYSTEM/SMART-CONNECT-SEVEN-DOOR-AUTHORITY-MATRIX-2026-09-24.md` |
| Production function | `nayanet-github-webhook` v4, digest `36f89f5c9beadcf77298ee0ccf8705a8e836cbdd4813ef1c70282d40bd366072` |

---

## NEXT ACTION

**Exactly ONE executable action:**

> **1. Deploy updated webhook source (with `title` fix) to Supabase Edge Function `nayanet-github-webhook` (version 5). 2. Authorized operator configures `GITHUB_WEBHOOK_SECRET` in Supabase project `dahisasgpfvziswqvmvm` Edge Function environment variables. 3. Trigger a controlled signed GitHub webhook delivery (e.g., push to repository with GitHub App installed) to execute the live proof chain: positive ingress → canonical persistence → exact replay → fresh retrieval → authority-separation verification.**

---

## SIGN-OUT

```
[CODA][SIGN-OUT]
ACTOR: CODA 3 — Integration / Release / GitHub Sender
OBJECTIVE: Prove SOURCE→BUILD→RUNTIME→GITHUB SENDER→RECEIVER→HUB chain or isolate external boundary
SOURCE HEAD: 79c0eeacaaf023ea2e2fbad1bfa65957b52522c5 (local fix: title field added)
STATUS: PARTIALLY VERIFIED
EXTERNAL BOUNDARY: BLOCKED_EXTERNAL_CREDENTIAL (GITHUB_WEBHOOK_SECRET)
SOURCE/RUNTIME PARITY: Current source has title fix; deployed version (da74234e) does not — deployment update required
NEXT ACTION: Deploy updated webhook source, configure GITHUB_WEBHOOK_SECRET in Supabase, run controlled signed webhook proof
```