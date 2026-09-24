# GitHub Webhook P1 — Credential Boundary & Safe Preparation

**Date:** 2026-09-24
**Status:** BLOCKED_EXTERNAL_CREDENTIAL
**Repository:** SoulSchoolAcademy/NayaPOWER
**Current main SHA inspected:** e4bb2c20aec1e5d2811bf2030da7d4bb85365255
**Production Supabase project:** dahisasgpfvziswqvmvm (ca-central-1, ACTIVE_HEALTHY)
**Production Edge Function:** nayanet-github-webhook
**Production function version:** 3
**Production function deployment digest:** 081cc239fb9f6c662044ea13d3a56d4015baf0741d720b29bfbfa01bafa6349c
**Repository webhook source blob:** cf00cb52b424783f37d25a2a89f031724b19543a

## P1 result

The production credential boundary is explicit and fail-closed. The production receiver currently returns HTTP 503 with error `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED` and status `BLOCKED_EXTERNAL_CREDENTIAL` before delivery/signature processing or persistence.

Observed directly at 2026-09-24T22:11:01Z. Request id from Supabase gateway: `01a0d578-d6da-7399-97da-c85d71e0c8a9`. Deno execution id: `f0fed63d-a5cf-444b-a3c5-f52e1255436a`.

The secret value was not requested, read, transmitted, logged, or stored by this execution. The current permitted Supabase tool surface exposes function deployment metadata/source but no secret-value or secret-management write operation. The local machine has no Supabase CLI installed. GitHub repository Actions secret metadata was inspected and contains no `GITHUB_WEBHOOK_SECRET`; this does not prove the Supabase function secret state, which is established by the production 503 response above.

## Safe webhook call graph reconstructed from source

GitHub HTTP POST
→ `nayanet-github-webhook`
→ method check
→ read `x-github-delivery` + `x-hub-signature-256`
→ read `GITHUB_WEBHOOK_SECRET`
→ **FAIL CLOSED if absent**
→ delivery-id required
→ HMAC-SHA256 verification over the raw request body
→ JSON parse
→ normalization
→ service-role Supabase client
→ canonical RPC `nayanet_record_cognition_event`
→ canonical cognition event + project cognition state + execution receipt
→ HTTP response

No repository caller to the inbound webhook function was found. The caller is an external GitHub webhook delivery. The repository contains a separate outbound `nayanet-github-dispatch` Edge Function, but it is not an inbound webhook caller and must not be conflated with webhook ingress.

## Signature contract

- Header: `x-hub-signature-256`
- Required shape: `sha256=<64 hex characters>`
- Algorithm: HMAC-SHA256 over the exact raw request body
- Comparison: constant-time byte comparison after normalizing signature case
- Header: `x-github-delivery` is required after the secret exists

## Source / installation / repository binding

Current normalization extracts:

- repository: `payload.repository.full_name`
- actor: `payload.sender.login` or `payload.pusher.name`
- ref: `payload.ref`, PR base ref, or workflow-run branch
- commit SHA: push `after`, PR head SHA, or workflow-run head SHA
- delivery ID: `x-github-delivery`
- source system: `github`
- correlation/idempotency: `github:<delivery-id>`

**Important gap:** the receiver currently records repository and actor fields, but there is no explicit extraction/persistence of a GitHub installation ID in this function. Repository authorization/isolation is therefore not yet independently proven. The `authority` object currently says `source=github_app` and `scope=<repository>`; this is provenance metadata, not execution authority and is not itself issuer proof.

## Persistence contract

The receiver calls the existing canonical `nayanet_record_cognition_event` RPC using the service-role key. No second webhook database or event store exists in this path.

Production database inspection shows a unique cognition-event index on `(user_id, project_id, event_id)`.

**Critical preflight finding:** the current six-argument `nayanet_record_cognition_event` overload used by the webhook performs an `ON CONFLICT DO UPDATE` on the cognition event, but then creates a fresh execution receipt and increments project state on every call. Therefore exact replay/idempotency is **NOT VERIFIED** and the current source does not yet prove one receipt/no unintended state change for a duplicate delivery. This is a causal repair candidate for a later phase, not a P1 credential change.

No production GitHub cognition events were found in the canonical cognition table during this inspection.

## Downstream / projection audit

The normalized event declares projection targets (Personal Intelligence, Activity, Intelligence Today), but this receiver does not itself invoke downstream projection or retrieval services. No separate repository consumer of `github_webhook_received` was found. Therefore signed ingress, persistence, downstream observation, and fresh retrieval remain separate proof stages and must not be collapsed into an HTTP-200 claim.

## Authority-separation trace

The webhook receiver calls `nayanet_record_cognition_event` with action `github_webhook_received`, not `intelligence.capture`, and supplies no execution authorization object. The current seven-argument production function requires execution authorization only for `intelligence.capture`; the webhook action therefore does not itself request an `intelligence_commit` grant.

This is strong source-level evidence that the webhook is modeled as an event source rather than an execution-authority issuer. It is **not** yet live proof of the full UniversalExecutionGate → ExecutionAuthorization → canonical authority chain because no signed production webhook has been accepted while the credential is blocked.

## Legacy / fallback audit

- Inbound webhook implementation found: `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts`.
- Separate outbound GitHub dispatch function found: `NAYANET/EXECUTION-BRIDGE/nayanet-github-dispatch/index.ts`.
- No second inbound webhook implementation was found in repository source.
- No separate webhook event store was found.
- The persistence seam is canonical Supabase cognition/receipt storage.
- The six-argument cognition RPC overload remains a relevant legacy/alternate persistence path for webhook ingress and is the reason replay semantics must be explicitly tested before any green status.

## Adversarial matrix prepared — not executed in production

| Vector | Expected result | Current proof state |
|---|---|---|
| Missing signature | DENY | NOT_RUN while secret absent |
| Wrong signature | DENY | NOT_RUN while secret absent |
| Altered payload | DENY | NOT_RUN while secret absent |
| Wrong repository | DENY / isolated | NOT_VERIFIED |
| Wrong installation/source | DENY / isolated | NOT_VERIFIED; installation ID not currently persisted by receiver |
| Revoked/disabled source | DENY | NOT_VERIFIED |
| Duplicate delivery | Deterministic replay / idempotent effect | NOT_VERIFIED; preflight identifies fresh-receipt/state-update risk |
| Valid signed delivery | Accept + canonical persistence | BLOCKED_EXTERNAL_CREDENTIAL |
| Webhook → intelligence authority | Must not mint authority | SOURCE-LEVEL PASS; LIVE NOT_VERIFIED |

## Evidence

- Main SHA: `e4bb2c20aec1e5d2811bf2030da7d4bb85365255`
- Webhook source blob: `cf00cb52b424783f37d25a2a89f031724b19543a`
- Supabase function: `nayanet-github-webhook`, version 3
- Production function digest: `081cc239fb9f6c662044ea13d3a56d4015baf0741d720b29bfbfa01bafa6349c`
- Production probe: 2026-09-24T22:11:01Z → HTTP 503 → `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED`
- UAI privileged authority proof: run `36064087479`
- UAI deployment: run `36063359510`

## Truth boundary

**P1 = BLOCKED_EXTERNAL_CREDENTIAL.**

Safe source/repository preparation is complete. The real production secret remains an external operator/admin boundary. No secret was requested or handled, and no positive webhook mutation/proof was executed.

## Single next action

Run the controlled signed production GitHub webhook proof after the authorized operator has configured the real production secret.
