# 🔱 2026-08-28 — MAXIS + NayaPOWER Execution Failures and Repairs

## Purpose

Preserve the exact failures discovered during real Team Naya execution so the next Naya does not rediscover them.

## NayaPOWER finding

The existing cold-start runtime gate failed before Smart Brain validation because the canonical Human Capability & Mastery protocol did not contain the exact machine-checked phrase:

`ready-to-run **NEXT EXECUTION**`

This was governance/documentation-to-runtime contract drift, not a product failure.

### Repair

Added the exact enforcement phrase to:

`.naya/codex/HUMAN-CAPABILITY-AND-MASTERY-OPERATING-PROTOCOL.md`

### Lesson

If a runtime validator checks a contractual phrase, that phrase is part of the executable contract. Human-readable equivalence is insufficient.

## MAXIS finding #1 — source parsing

The first current-source MAXIS Quality run failed at TypeScript parsing after the Guest Hub repair.

### Root cause

Malformed JSX was introduced in:

- `app/hub/page.tsx`
- `app/maxess/page.tsx`

### Repair

Both files were structurally repaired and subsequent verification proved:

- typecheck PASS
- build PASS
- front-door contract PASS
- current-HEAD production server startup PASS

## MAXIS finding #2 — golden-path contract drift

The current-source QMAX golden-path test failed because it expected one Hub continuation while the product correctly exposed two:

1. authenticated save/claim → Hub;
2. guest continuation → Guest Hub.

### Repair

The test was strengthened to require both explicit contracts rather than weakening the product:

- exactly one `Continue to Guest Hub` action;
- exactly one `Save result & enter Hub` member continuation.

## MAXIS finding #3 — Guest Hub auth boundary

Production initially redirected:

`/hub?guest=1 → /login?guest=1&next=%2Fhub`

### Root cause

`lib/supabase/proxy.ts` intercepted `/hub` before GuestHub could evaluate `guest=1`.

### Repair

`9aff6e9749a4c1a86788ffc42838fe625ac10998`

`fix(maxis): allow guest Hub route through auth proxy`

The `/hub` route was added to the public-path allowlist while member ownership remained authenticated and server-authoritative.

## MAXIS finding #4 — Guest Hub name continuity

After the route repair reached production, QMAX advanced to Guest Hub but failed at the personalized-name assertion.

### Root cause

`components/guest-hub.tsx` relied only on `maxis_ai_assessment_pending_claim_v1` for the participant name. The existing browser identity cookie `maxis_pending_username` was already part of the MAXIS identity flow, but GuestHub did not use it as a fallback when the pending result payload lacked the name.

### Repair

Current source repair:

`5329a9dae05b63c4cd18f6f49331033a8fceccb4`

`fix(maxis): restore guest Hub name from identity cookie`

The repair:

- reads the existing identity cookie;
- prefers the pending claim name;
- falls back to the cookie name;
- passes the restored name into the authoritative guest preview request;
- preserves the guest/member boundary.

### Verification

Current MAXIS Quality at the repair source is GREEN for typecheck, build, front-door contract, current-HEAD runtime, and QMAX golden path.

Production-final correctly remains RED because production still serves an older deployment.

## MAXIS finding #5 — production deployment rate limit

Current source SHA:

`5329a9dae05b63c4cd18f6f49331033a8fceccb4`

Vercel GitHub status reports:

`Deployment rate limited — retry in 24 hours.`

### Meaning

This is a deployment-quota boundary, not an application-code failure. The source is green, but the production-serving environment cannot accept another deployment through the current Vercel path while the quota is active.

### Team Naya rule

Do not convert deployment blockage into fake GREEN.

Do not weaken QMAX to accommodate stale production.

Do not create unnecessary code changes merely to wait for deployment.

Instead:

1. finish all legitimate source verification;
2. record the exact production/deployment boundary;
3. batch the next production release so one deployment contains all verified changes;
4. when an authorized production deployment path becomes available, deploy once;
5. verify SHA parity;
6. immediately rerun production-final;
7. continue from the first real runtime divergence.

## Reusable execution law

`SOURCE GREEN ≠ PRODUCTION GREEN`

`DEPLOYMENT READY + SHA PARITY + RUNTIME EVIDENCE` are required before a production claim is GREEN.

A platform quota is an explicit execution dependency and belongs in Mission State / execution receipts as a first-class boundary.

## Non-negotiable next move

Do not polish the UI.

Do not create another architecture.

Do not claim the Guest Hub block green.

When production deployment becomes available, deploy the current verified MAXIS source once, prove the exact SHA, rerun production-final, and repair only the first remaining runtime divergence.
