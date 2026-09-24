# GitHub Webhook P3 — Owner Identity / System-Caller Boundary

**Date:** 2026-09-24
**Status:** BLOCKED / ARCHITECTURAL IDENTITY GAP
**Repository:** SoulSchoolAcademy/NayaPOWER

## Finding

The controlled signed GitHub webhook proof has a deeper blocker beyond the missing production secret.

The inbound receiver creates a Supabase client with the server-side `SUPABASE_SERVICE_ROLE_KEY` and calls the canonical six-argument `nayanet_record_cognition_event` RPC. The canonical RPC requires `auth.uid() IS NOT NULL` and writes the cognition event owner from `auth.uid()`.

A Supabase service-role JWT is a server/admin token and its documented JWT shape contains `role=service_role` and project `ref`, but no user `sub`. Therefore the webhook's current service-role caller does not provide the human owner identity required by the canonical cognition persistence function.

## Why this matters

Even after `GITHUB_WEBHOOK_SECRET` is configured, the current inbound webhook path cannot safely prove the required:

**GitHub installation/repository → existing Smart Connect participation → canonical human owner → private cognition persistence**

without an explicit, governed source-to-owner binding.

The current `nayanet_smart_connect_participation` table contains `member_id` and `door` but no repository or GitHub installation identity field. The webhook normalizes `repository.full_name`, but it does not resolve that repository to a member before calling the owner-bound cognition RPC.

This is a privacy and authority boundary, not a reason to guess an owner or use a generic Naya/system member.

## Evidence

- Webhook source: `NAYANET/EXECUTION-BRIDGE/nayanet-github-webhook/index.ts`
  - creates Supabase client with `SUPABASE_SERVICE_ROLE_KEY`;
  - calls `nayanet_record_cognition_event`;
  - passes `github_webhook_received`;
  - supplies no authenticated human bearer token or owner UUID.
- Production canonical function read-back:
  - requires `auth.uid() IS NOT NULL`;
  - persists `user_id=auth.uid()`.
- Existing Smart Connect participation schema:
  - `id`, `member_id`, `door`, status/consent fields;
  - no GitHub repository or installation identity field.
- Supabase JWT documentation confirms service-role JWTs use `role=service_role` and do not include a user `sub` claim in the documented service-role token shape.
- Direct production webhook probe still returns HTTP 503 `GITHUB_WEBHOOK_SECRET_NOT_CONFIGURED`, so this downstream failure has not been allowed to mutate production.

## Safe architectural conclusion

Do **not** bypass the canonical owner-bound persistence function, invent a default owner, or create a second authority/persistence model.

The smallest legitimate repair is to extend the **existing Smart Connect participation seam** with an explicit GitHub installation/repository binding, then add a governed inbound resolver that:

1. authenticates the GitHub webhook;
2. resolves installation + repository to exactly one active GitHub App participation/member;
3. rejects missing/ambiguous/revoked bindings;
4. invokes the existing canonical cognition persistence boundary under that resolved owner context;
5. preserves the existing event-id replay contract;
6. never treats GitHub source authenticity as `intelligence_commit` authority.

That repair should be implemented only after the exact owner-binding contract is defined from the existing participation seam.

## Current truth

- Production secret: **BLOCKED_EXTERNAL_CREDENTIAL**
- Replay/idempotency repair: **VERIFIED / PRODUCTION APPLIED**
- Owner identity binding: **NOT IMPLEMENTED / NOT VERIFIED**
- Installation isolation: **NOT VERIFIED**
- Signed positive webhook journey: **NOT VERIFIED**
- Webhook-to-authority separation: **SOURCE-LEVEL PASS / LIVE NOT VERIFIED**

## Single next action

**Define and implement the smallest governed GitHub App installation + repository → existing Smart Connect participation/member binding on the existing participation seam, with fail-closed missing/ambiguous/revoked resolution, before attempting the live signed webhook proof.**
