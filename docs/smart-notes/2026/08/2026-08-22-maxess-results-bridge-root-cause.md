# MAXESS Results Bridge Root Cause — Downstream Event Contract + Payload Handling

**Date:** 2026-08-22
**Category:** PROBLEM / SOLUTION / LEARNING
**Status:** IMPLEMENTED IN SOURCE; LIVE DEPLOYMENT NOT VERIFIED

## North Star
The MAXESS assessment must pass the user's real result contract into the Results experience so the complete Results page renders and every score/data field is populated accurately. Visual polish is secondary until the end-to-end data path is proven.

## Evidence
The canonical Results integration uses `MAXESS_RESULT_V1` and the official Results target `results.nayanet.app`.

The Results consumer was found to have a fragile event/payload boundary: downstream sections can receive a `CustomEvent` whose `detail` shape does not match what a section expects. In addition, the consumer only read the hash payload even though the assessment/other integrations may use a query-string `result` payload.

The complete integrated Results artifact contains E01, E02, E03, and E04 code, so the observed failure is not evidence that those sections were deleted. The communication/hydration layer is the first confirmed material fault.

## Root cause ranked
1. **Confirmed:** Results hydration event contract was inconsistent with downstream section listeners. The integrated consumer emitted an event detail wrapper in one generated artifact while E03 expected the result object directly.
2. **Confirmed risk:** Payload transport was hash-only in the consumer even though a query-string result transport is also used by Results baselines/integrations.
3. **Secondary risk:** Generated integrated Results output can become stale if the build workflow does not execute after the consumer changes; GitHub source and generated artifact must be rechecked after each bridge mutation.

## Surgical repair
`MAXESS-RESULT-CONSUMER-V2.html` was updated without rewriting the Results renderer to:
- emit the actual result contract as `event.detail`;
- accept both `#maxess-result=` and `?result=` payloads;
- persist the validated contract to both sessionStorage and localStorage;
- continue hydrating E01/E02 from the authoritative contract;
- preserve the existing section renderers and event names.

## Guardrail
Never change the Results renderer to compensate for a broken assessment-to-results transport. Validate the contract at the bridge boundary first, normalize event detail to the authoritative result object, support the approved transport forms, rebuild generated artifacts, then verify every section against the same `window.MAXESS_RESULT` object.

## Verification rule
`IMPLEMENTED` is not `LIVE VERIFIED`. The generated Results artifact and public `results.nayanet.app` target must be re-fetched/verified before claiming the user-facing issue is solved.

## Retrieval terms
MAXESS, AIScore, result bridge, MAXESS_RESULT_V1, MAXESS_RESULT_READY, event detail, E03, E04, score hydration, results communication, hash payload, query payload, complete Results, North Star
