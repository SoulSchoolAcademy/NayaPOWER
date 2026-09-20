# Wave A — Smart Mail Boundary Repaired and Resume Proven

**Date:** 2026-09-19

## STATUS

**SMART MAIL RESUME = VERIFIED**

## Release-surface reconciliation

Selected the smallest path: **A — restore the already-proven Assistant runtime surface**.

Cloudflare release run `35464367238` deployed the legacy-v7 Assistant artifact to the canonical Worker and verified exact source parity plus desktop/mobile runtime baseline.

## Concrete boundary defect

The deployed `nayanet-smart-mail` Edge Function previously returned HTTP 405 to browser CORS preflight and supplied no CORS headers. The browser therefore surfaced `TypeError: Failed to fetch`.

## Smallest repair

Edge Function version 16 added only:
- `OPTIONS` → HTTP 204
- exact canonical Hub `Access-Control-Allow-Origin`
- `POST, OPTIONS` methods
- required request headers
- `Vary: Origin`
- the existing JSON response path now carries the same CORS headers.

No auth, RLS, authority, RPC, or Smart Mail transaction semantics were changed.

The repository source was synchronized in commit `0a8c67ee6880d9f38f457922c180e7b2e2737a14`.

## Resume proof

Workflow run `35464691600` completed SUCCESS.

Verified from the Smart Mail gate forward:
- Smart Mail send PASS
- Smart Mail render PASS
- receiver verification PASS
- receiver retrieval PASS
- intelligence retrieval PASS
- C isolation PASS

Canonical proof:
- message `8f6caee9-7d4a-42b8-99d6-9cd17f7b604a`
- thread `eee16b3f-4978-4834-8135-f4f8815d7c7a`
- artifact `10591145024`

Browser network evidence recorded an actual POST to `/functions/v1/nayanet-smart-mail` returning HTTP 200 with the exact Hub CORS origin.

Independent preflight probe now returns HTTP 204 with the expected CORS method/header contract.

## NOT YET PROVEN

Full Wave A human-facing acceptance remains subject to the broader acceptance receipt and any remaining gates outside this Smart Mail resume lane.

## PROTECTED

- RLS/security model unchanged.
- Explicit `smart_mail_send` authority remains required.
- No service-role browser access.
- No synthetic success.
- No policy-improvement claim.
- No unrelated reconciliation merge.

## NEXT ACTION

Continue Wave A from the next unproven human-facing acceptance gate, using the verified Smart Mail execution as the durable handoff point.