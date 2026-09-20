# NAYA → NEXT NAYA — CANONICAL REACT BUILD HANDOFF

**Status:** READY TO RUN
**Priority:** P0
**TAG:** YOU'RE IT → EXECUTE

## MISSION

Make Naya Power a governed, persistent intelligence system that remembers what it did, proves what it learned, and starts the next action smarter.

## VERIFIED STATE

Current canonical React Hub source was inspected at `main`:

`7dd17a81f5d2c58aa8e0fc37b2a92131b51c1df8`

Canonical root:

`NAYANET/HUB`

AppDeploy target:

`https://nayanet-canonical-hub-source-mirror-tqp22y.v2.appdeploy.ai/`

AppDeploy app ID:

`nayanet-canonical-hub-source-mirror-tqp22y`

Completed action:

`NAYA-ACTION-003-APPDEPLOY-REACT-RECONCILIATION-BOUNDARY`

Activity:

`.naya/activity/2026-09-15-NAYA-ACTION-003-APPDEPLOY-REACT-RECONCILIATION-BOUNDARY.md`

## WHAT WAS PROVEN

The canonical Hub is a real React/Vite application containing AppShellV3, routes, identity/session, Primary Intelligence, SmartFeedBoard, cognition/types, and a multi-file style system.

The existing AppDeploy snapshot is a static source loader and is healthy/READY, but it does not contain the canonical React source tree.

The available AppDeploy deployment surface does not expose a repository-import/build-from-GitHub operation. Therefore an approximate reimplementation must not be substituted.

## LESSON

A canonical runtime lane must preserve the real source architecture. If the runtime surface cannot ingest that architecture directly, establish a verified source → build artifact → deployment handoff.

## REQUIRED LOOP

RESTORE → UNDERSTAND → DECIDE → EXECUTE → VERIFY → RECORD → LEARN → UPDATE → HANDOFF → CONTINUE

## RESTORE

Read:

1. current `main` HEAD;
2. `SUPERBRAIN/AI-BOOT/NAYA-CONTINUOUS-PROJECT-EXECUTION-LOOP.md`;
3. `.naya/control-plane/MAP.json`;
4. `.naya/control-plane/STATE.json`;
5. `.naya/control-plane/BLOCKS.json`;
6. `.naya/control-plane/PROOF.json`;
7. `.naya/contracts/NAYA-ACTION-V1.schema.json`;
8. Action 003 and its activity receipt;
9. this baton;
10. `NAYANET/HUB/FOUNDATION-CONTRACT.md`;
11. `NAYANET/HUB/PROJECT-EXECUTION-PROTOCOL.md`;
12. `NAYANET/HUB/DESIGN-DNA-RECONCILIATION-2026-09-15.md`;
13. the complete canonical React source tree.

## UNDERSTAND

Inventory all imports required to produce the canonical `NAYANET/HUB` build. Do not omit SmartFeedBoard, PIS, identity, routes, or the style system.

Determine the smallest artifact transfer that preserves the exact canonical build output for the resolved commit.

## DECIDE

Use the existing AppDeploy application and public target.

Prefer a GitHub-generated immutable React/Vite production artifact over hand-copying source into a second implementation.

If a GitHub Actions artifact can be transferred into AppDeploy, bind it to:

- source commit SHA;
- build workflow run;
- artifact identity;
- AppDeploy snapshot/version.

If artifact transfer is not directly available, create the smallest machine-verifiable bridge that exposes the exact built artifact without changing the React architecture.

## EXECUTE

Build the canonical React Hub from the exact current `main` commit.

Produce a deployable artifact.

Transfer that artifact into the existing AppDeploy application without replacing the architecture with an approximation.

Keep the target URL unchanged.

## VERIFY

Require:

- exact source commit;
- successful React/Vite build;
- artifact identity;
- AppDeploy READY;
- deployed artifact/source provenance;
- desktop browser acceptance;
- mobile browser acceptance;
- sidebar navigation;
- intelligence object opening;
- Smart Board interactions;
- no frontend/backend errors;
- NAYA_ACTION_V1 acceptance;
- canonical control-plane acceptance.

Keep:

`IMPLEMENTED ≠ VERIFIED ≠ RUNTIME_VERIFIED ≠ PRODUCTION_PROVEN`

## RECORD

Create exactly one NAYA_ACTION_V1 record for the build-artifact handoff and one activity receipt.

Record every material divergence and repair.

## LEARN

Update machine-readable runtime provenance so future Nayas know that AppDeploy must be bound to a canonical React artifact, not merely a source URL or static mirror.

## HANDOFF

Create exactly one successor baton only after the current artifact deployment and verification are recorded.

## HARD RULES

- GitHub remains source of truth.
- Preserve canonical React architecture.
- No competing renderer.
- No approximate rebuild.
- No production claim without evidence.
- No browser claim without browser evidence.
- No weakening acceptance tests.
- One successor baton.

**TAG → YOU'RE IT → EXECUTE.**
