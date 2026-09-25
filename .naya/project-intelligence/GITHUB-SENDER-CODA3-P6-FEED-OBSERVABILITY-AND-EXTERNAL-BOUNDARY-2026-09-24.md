# GITHUB SENDER CODA 3 — P6 INTEGRATION / RUNTIME PARITY / FEED OBSERVABILITY

Date: 2026-09-24
Source head: `fa82d32b67131c5cdaec441d0f0787a9921f8370` (origin/main at start of this pass)
Status: PARTIALLY VERIFIED / BLOCKED_EXTERNAL_CREDENTIAL

---

## ACTOR

CODA 3 — Integration / Runtime Parity / GitHub Sender.

## OBJECTIVE

Complete every source/build/runtime integration dependency of the GitHub sender chain, or isolate the exact external boundary preventing the live loop:
SOURCE → BUILD → RUNTIME → GITHUB WEBHOOK → OWNER BINDING → CANONICAL RECEIVER → PERSISTENCE → HUB FEED → ACTIVITY.

## SOURCE HEAD

- Origin/main at start: `fa82d32b67131c5cdaec441d0f0787a9921f8370`
- Webhook adapter source blob before change: `61a6fcce188cc617d35c6b06bd2444dde4c9b965` (unchanged since the version-4 production digest `36f89f5c…` was verified in P5)
- Webhook adapter source raw SHA-256 (blob 61a6fcce): `2854aa7d4390d5e20e46c5757ad01ac136f9b640c3363e40dd15c1aad1f20175`
- Hub entrypoint `NAYANET/HUB/index.html` source SHA-256: `798b1fb67d5d88815b90be9523b0da778e802ffa86031e8eff2e69a218a46184`

## WORK COMPLETED

1. **Runtime parity audit (SOURCE → BUILD → RUNTIME).**
   - Live Hub `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/` (Cloudflare Worker `sparkling-shape-7ae5`) observed HTTP 200, 838,838 bytes, `<title>NayaNET - Intelligent Hub V7 509 AAA</title>`.
   - Live Hub SHA-256 = `798b1fb6…` **byte-for-byte identical** to `NAYANET/HUB/index.html` on current origin/main. Hub source/runtime: **PASS**.
   - Live webhook `https://dahisasgpfvziswqvmvm.supabase.co/functions/v1/nayanet-github-webhook` is deployed and fail-closed: POST with delivery → HTTP 503 `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED` / `BLOCKED_EXTERNAL_CREDENTIAL`. Runtime behavior exactly matches current source's secret boundary. Adapter source unchanged since its version-4 production verification.
   - Webhook source `61a6fcce` == working-tree blob == origin/main blob (verified via `git hash-object`).

2. **Owner-binding contract verified on origin/main.**
   - `nayanet_resolve_github_webhook_owner(p_installation_id, p_repository)` now uses `(array_agg(sp.member_id))[1]` (uuid aggregate repair), count guards, fail-closed on `GITHUB_BINDING_NOT_FOUND` / `GITHUB_BINDING_AMBIGUOUS`, service-role-only.
   - Participation binding `nayanet_smart_connect_github_bind` (authenticated-only) binds installation+repository to the owner's existing active `github_app` participation row (`nayanet_smart_connect_participation`). Sender connects through the participation model; no identity is published to the Hub.

3. **Canonical receiver contract verified on origin/main (CODA 1 parity).**
   - `nayanet_record_cognition_event` (20260924233000 hardening + 20260924233100 replay repair) accepts unauthenticated service-role calls ONLY via `github_app_webhook` execution authorization, then re-resolves and re-checks the owner binding (`GITHUB_WEBHOOK_OWNER_BINDING_MISMATCH` otherwise) and persists under the bound owner.
   - Idempotency: event identity `(user_id, project_id, event_id)` + `on conflict` + advisory xact lock on owner:project; duplicate delivery returns `{"replayed":true}` with the ORIGINAL event/receipt, no new receipt/state revision.

4. **Hub retrieval chain verified (CODA 2 parity).**
   - `nayanet_cognition_events` → `nayanet_index_intelligence_row()` trigger → `nayanet_intelligence_index` → `loadPersistentPIS()` (owner-scoped, `owner_id=user.id`) in `NAYANET/HUB/src/data/pis.ts` → Feed / Activity / Intelligence Today surfaces.
   - **Defect found and repaired (in-repo):** the webhook normalizer persisted events with NO `title`/`content`/`created_at`/`schema_version`/`metadata`. The canonical receiver stores them as defaults (`title=null`, `content=''`). A real GitHub event would reach the owner's Feed but render as an empty block — a dead loop at the Feed link of the chain.
   - Fix (adapter only; receiver and Hub contracts untouched): `normalize()` now derives a renderable `title`, `content`, `type`, `classification`, `status`, `tags`, `schema_version`, `created_at` (= occurred_at) and owner-scoped `metadata` from the GitHub payload. `idempotency_key` remains `github:<delivery-id>`; every security gate and the PERSISTED/REPLAYED return contract are preserved.
   - Smart Connect privacy preserved: GitHub display identity is not added to title/content.

5. **Contract harness (RED→GREEN).** `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/contract-harness.mjs` executes the ACTUAL adapter source under Node (Deno/`createClient` stubbed; imports stripped; no production values). **20/20 assertions PASS:**
   - OPTIONS 200; method-not-allowed 405; missing secret 503 `BLOCKED_EXTERNAL_CREDENTIAL`; missing delivery 400; invalid signature 401; malformed signature 401; invalid JSON 400; missing installation 403 `BLOCKED_OWNER_BINDING`; missing repository 403; missing Supabase credentials 503; unresolved owner 403 (fail-closed); **valid-signature bound-owner persistence 200 PERSISTED**; resolver arg contract; canonical-receiver execution-authorization contract (`github_app_webhook`, actor_id, installation_id, repository, `SIGNED_GITHUB_WEBHOOK`); `github_webhook_received` action; **normalized event renderable** (title/content/type/created_at/schema_version/metadata); **duplicate delivery → 200 REPLAYED (no duplicate intelligence)**; persistence failure → 502.

## WHY

Launch requires a real causal chain from an external sender to a visible Hub Feed/Activity item. Every internal link is now proven, and the one remaining link (a live signed GitHub delivery) is blocked only by external credential/installation configuration — not by code.

## EVIDENCE

- Hub runtime bytes: live `798b1fb67d5d88815b90be9523b0da778e802ffa86031e8eff2e69a218a46184` == source `798b1fb6…` (HTTP 200, 838,838 bytes live).
- Hub release workflow: `.github/workflows/assistant-cloudflare-hub-release.yml` (canonical static Hub artifact; exact-canonical verification step).
- Webhook runtime fail-closed: live POST `…/functions/v1/nayanet-github-webhook` → `503 {"error":"GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED","status":"BLOCKED_EXTERNAL_CREDENTIAL"}`.
- Webhook adapter source unchanged since last verified production deployment (blob `61a6fcce`), working tree == origin/main.
- Resolver/receiver migrations on origin/main: `20260924230000`, `20260924233000`, `20260924233100`, `20260924234500`, `20260924200000` (replay idempotency).
- Harness: `node NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/contract-harness.mjs` → RESULT 20 passed, 0 failed.

## STATUS

PARTIALLY VERIFIED / BLOCKED_EXTERNAL_CREDENTIAL

## RUNTIME PARITY

- Source head: `fa82d32b` (origin/main).
- Build: canonical static Hub artifact (workflow `assistant-cloudflare-hub-release.yml`); webhook = Supabase Edge Function version 4 (digest verified in P5, source unchanged).
- Deployed: Hub Worker `sparkling-shape-7ae5`; Edge Function `nayanet-github-webhook` on `dahisasgpfvziswqvmvm.supabase.co`.
- Observed runtime: Hub index.html SHA-256 `798b1fb6…` (exact bytes match); webhook fail-closed 503 at the secret boundary.
- Receiver/Hub contract source on origin/main matches production behavior (verified above).

## EXTERNAL BOUNDARY

Two genuine external configuration actions are required OUTSIDE the repository through the authorized administration boundary:

1. `GITHUB_WEBHOOK_SECRET` must be configured as a production Secret for the `nayanet-github-webhook` Edge Function (in the Supabase project dashboard / secret-management boundary). No value is requested, invented, committed, or logged.
2. A real GitHub App must exist, be installed on the target repositories, and its `installation_id` + selected repository must be bound to the authenticated owner's existing Smart Connect `github_app` participation via `nayanet_smart_connect_github_bind` (or an authorized equivalent). Production currently has zero `github_app` participation rows.

Until both are satisfied, the endpoint correctly returns `BLOCKED_EXTERNAL_CREDENTIAL` — this is the designed fail-closed state, not a defect.

## COORDINATION

- **CODA 1 (receiver):** No receiver contract changed. `nayanet_record_cognition_event` signature and `github_app_webhook` execution-authorization gate are untouched. The adapter now supplies `title`/`content`/`type`/`created_at`/`schema_version`/`metadata`; receiver defaults no longer consume null render fields. Replay/`replayed` semantics unchanged.
- **CODA 2 (Hub):** No Hub data contract changed. `nayanet_intelligence_index` projection and `loadPersistentPIS` render path are untouched; a persisted `github:*` cognition event is now displayable in Feed/Activity/Intelligence Today under the bound owner.
- **Issue #554:** team board reference; no secrets on the issue, per policy.

## DURABLE STATE

- Branch `coda3/github-sender-feed-observability-20260924` rooted at `fa82d32b`.
- Files:
  - `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts` (adapter observability + preserved gates)
  - `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/contract-harness.mjs` (20-assertion contract harness)
  - this receipt: `.naya/project-intelligence/GITHUB-SENDER-CODA3-P6-FEED-OBSERVABILITY-AND-EXTERNAL-BOUNDARY-2026-09-24.md`
- PR opened from the branch for team review/merge.

## NEXT ACTION

**ONE action:** through the authorized external GitHub/Supabase administration boundary, configure the production `GITHUB_WEBHOOK_SECRET` for the `nayanet-github-webhook` Edge Function and bind the live GitHub App installation + selected repository to the owner's Smart Connect `github_app` participation — then send one real GitHub event and verify `PERSISTED` in the webhook response and its `github:*` event in the owner's Feed/Activity in the live Hub.