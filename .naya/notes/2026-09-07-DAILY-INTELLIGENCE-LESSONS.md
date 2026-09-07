# 🔱 Naya Note — 2026-09-07 Daily Intelligence Lessons

**Source event:** `INT-2026-09-07-001`
**Source of truth:** NayaPOWER `main` `2270db7582486926185786e455900c53770c4bb9`
**Related product state:** MAXIS `main` `e1f727da77eb04e6b79ed40c218b545a2b372e78`

## Durable lesson

A surgical user-facing patch may temporarily use an existing governed execution path, but the temporary mutation authority must be explicitly bounded and removed after the operation. A verification workflow should return to its canonical read-only role; leaving write-capable self-mutation behind creates authority drift and makes later evidence harder to interpret.

## Evidence boundary

Source history proves that the patch was introduced in the preceding commit and that the latest commit restored the Claim Evidence workflow, removed the temporary mutation steps, and changed permissions back to `contents: read`. It does **not** prove live deployment, public rendering, or browser behavior.

## Required successor behavior

1. Resolve live `main` before acting.
2. Inspect the final post-restoration workflow, not only the intermediate patch.
3. Verify the delivered artifact and live Hub at the exact final SHA.
4. Keep Smart Note/backend/runtime proof separate from the Hub UI patch.
5. Preserve UNKNOWN for deployment, browser, and country-accuracy questions until observed.

## Guardrail candidate

Any temporary workflow mutation must have an explicit scope, restoration commit or equivalent rollback, final permission check, and post-restoration verification step.
