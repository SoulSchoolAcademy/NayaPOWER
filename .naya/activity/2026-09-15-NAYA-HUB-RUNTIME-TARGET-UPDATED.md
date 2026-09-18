# NAYA HUB RUNTIME TARGET — UPDATED

**Date:** 2026-09-15  
**Change:** Replace the former Assistant Cloudflare Worker target with the current AppDeploy NayaNET canonical Hub source mirror.

## CURRENT TARGET

`https://nayanet-canonical-hub-source-mirror-tqp22y.v2.appdeploy.ai/`

**AppDeploy app:** `nayanet-canonical-hub-source-mirror-tqp22y`

The connected AppDeploy control plane currently reports this application as **ready** and provides the same live URL.

## PREVIOUS TARGET

`https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/`

The previous URL is no longer the current target for NayaNET Hub continuation work.

## PROVENANCE BOUNDARY

This update changes the machine-readable target used for future runtime verification. It does not retroactively convert prior Cloudflare evidence into AppDeploy evidence and does not claim that the AppDeploy mirror is production-equivalent to a specific Git commit.

## REQUIRED NEXT VERIFICATION

1. Resolve latest `main` HEAD.
2. Confirm the AppDeploy applied version contains the intended canonical Hub source.
3. Verify desktop/mobile rendering and interactions.
4. Capture exact source/runtime evidence.
5. Only then promote the runtime target from `CURRENT_TARGET_UNVERIFIED_PRODUCTION` to `VERIFIED_RUNTIME`.

## LESSON

Runtime destination is itself part of provenance. When the destination changes, the project brain must change with it while preserving the distinction between configured target, available deployment, verified runtime, and production proof.
