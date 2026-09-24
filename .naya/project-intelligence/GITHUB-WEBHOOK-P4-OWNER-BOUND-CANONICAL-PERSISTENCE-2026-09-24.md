# GITHUB WEBHOOK P4 — OWNER-BOUND CANONICAL PERSISTENCE

Date: 2026-09-24
Repository: SoulSchoolAcademy/NayaPOWER
Status: PRODUCTION APPLIED / LIVE SIGNED PROOF BLOCKED BY EXTERNAL SECRET

## Objective

Close the owner identity gap in the inbound GitHub webhook without creating a second connection store, authority model, or persistence backend.

## Implemented

The existing webhook receiver now verifies the signed payload, extracts GitHub installation ID and repository full name, resolves the bound human owner through the existing Smart Connect participation seam, fails closed when the binding cannot be resolved, and passes the resolved owner through the existing canonical cognition persistence RPC.

The seven-argument canonical persistence function is now service-role aware only for the explicitly bounded action github_webhook_received with source github_app_webhook. It independently re-resolves the installation/repository binding and rejects an owner mismatch. Existing replay protection remains intact and returns the original event/state/receipt on exact replay.

## Production evidence

- Webhook source commit: da74234e2a44bd0d3a3710ac4f06b84de4569644
- Production Edge Function: nayanet-github-webhook
- Production version: 4
- Production deployment digest: 36f89f5c9beadcf77298ee0ccf8705a8e836cbdd4813ef1c70282d40bd366072
- Canonical persistence migrations: e61e1ff2c0d77f5af7386607459cfa91caf75114, f02038a6c32bf02d70785e88a798146872e8ca29
- Independent deployed-source read-back: PASS
- Independent canonical-function read-back: PASS
- Fresh production POST probe: HTTP 503 GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED / BLOCKED_EXTERNAL_CREDENTIAL

## Why the 503 is correct

The real production GitHub webhook secret is still not configured. The receiver therefore stops before signature acceptance, owner resolution, or canonical persistence. No secret value was requested, exposed, or stored in source.

## Remaining proof

The following cannot be promoted until the external secret-management boundary is completed:

1. signed GitHub delivery accepted;
2. installation + repository resolves to exactly one active human owner;
3. canonical event/state/receipt persistence under that owner;
4. exact delivery replay returns the original lineage without a second durable effect;
5. fresh retrieval reconstructs the same result;
6. wrong repository / non-owner / revoked binding is denied;
7. valid webhook remains an event source and does not create intelligence_commit authority;
8. source revocation blocks subsequent signed delivery.

## Architectural result

GitHub App/Webhook → existing Smart Connect participation → canonical owner resolution → existing canonical cognition persistence → existing receipt/retrieval path.

No second backend. No second authority model. No default/system owner. No Hub-to-Supabase bypass.

## Single next action

Configure GITHUB_WEBHOOK_SECRET through the authorized production secret-management boundary, then run the controlled signed webhook positive/replay/retrieval/revocation/authority-separation proof.
