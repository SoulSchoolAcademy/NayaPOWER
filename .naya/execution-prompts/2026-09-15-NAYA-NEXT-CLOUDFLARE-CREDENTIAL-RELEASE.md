# NAYA — NEXT CLOUDFLARE CREDENTIAL RELEASE

CONTINUE FROM CURRENT MAIN.

Do NOT redesign the nine-board Hub.

Current evidence receipt:
`.naya/activity/2026-09-15-NAYA-RELEASE-EVIDENCE-CURRENT-RUN.md`

Current source/release commit before this receipt:
`0c79491ffa80bc60d18da956f0b65cc3cc3a1c60`

Actual Assistant release run:
`35012925083`

## VERIFIED

- Push-triggered Assistant Cloudflare workflow is real and enumerable.
- Current run checked out current HEAD exactly.
- Source Contract PASS: 9 boards, 10 sidebar entries, 10 layers, forbidden legacy PASS.
- Typecheck PASS.
- Production Build PASS.
- Current Wrangler Worker name: `sparkling-shape-7ae5`.

## BLOCKER

The hardened release preflight failed because:
`CLOUDFLARE_ACCOUNT_ID is missing from environment assistant-cloudflare-production`

Therefore Wrangler deployment was correctly skipped.

Do NOT guess the account ID, replace credentials, weaken the preflight, or modify the Hub presentation.

## NEXT EXECUTION

1. Obtain/restore the authorized Cloudflare account ID in GitHub Environment `assistant-cloudflare-production`.
2. Preserve the existing API token and credential preflight.
3. Trigger the Assistant Cloudflare release workflow from a release-path commit.
4. Retrieve the new run ID.
5. Capture Source Contract, Typecheck, Production Build, credential preflight, and Wrangler deployment.
6. Prove the deployed Worker is `sparkling-shape-7ae5.smartnetpodcast.workers.dev` and bind it to the exact released source SHA.
7. Only after deployment proof exists, verify exact runtime, canonical sidebar destinations, board mapping, Save/Favorite consequences, and desktop/tablet/mobile behavior.
8. Record exact evidence in Activity.
9. Create the next continuation.

## HARD PASS

SOURCE → GATE → TYPECHECK → BUILD → DEPLOYMENT → EXACT RUNTIME → INTERACTION → CONSEQUENCE → BROWSER → ACCEPTANCE

No unsupported PASS. Missing evidence remains UNKNOWN/BLOCKED.
