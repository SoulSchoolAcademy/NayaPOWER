# Wave A Session 007 — Live runtime cache-bust repair + browser boundary — 2026-09-19T17:10Z

## Objective

Close the newly discovered deployed-runtime/browser integration gap after Session 006: prove that the current Assistant Runtime actually executes in the live Hub, not merely that the file hash matches the release artifact.

## Discovery

The live Cloudflare Hub loaded an old Assistant Runtime query string:
assistant-runtime.js?v=20260918-r7

The current Hub source still referenced that stale cache version even though the current Assistant Runtime had changed.

CDP browser observation produced a real live exception from the stale cached runtime:
SyntaxError: Unexpected token async in assistant-runtime.js?v=20260918-r7.

Because that stale script failed to parse, window.NayaAssistantRuntime was absent and Smart Tabs could not initialize.

This is a concrete runtime-cache defect, not an authentication defect.

## Repair

Updated the canonical Hub source from:
/assistant-runtime.js?v=20260918-r7

to:
/assistant-runtime.js?v=20260919-wavea6

Commit:
6018ed5002ee09505767852e4f39d1d81c9c96ab

## Deployment proof

Cloudflare release:
35457054828

Head commit:
6018ed5002ee09505767852e4f39d1d81c9c96ab

Deploy job:
105934103331

Result:
SUCCESS

The workflow passed exact artifact deployment, exact live source parity, desktop runtime baseline, mobile runtime baseline, and final Assistant-lane runtime proof.

## Browser observation after repair

A live CDP browser observation at the early Hub lifecycle now reports:
- live Hub title: NayaNET — Intelligent Hub V7 · 509 AAA
- window.NayaAssistantRuntime: present
- NayaAssistantRuntime.init: function
- NayaAssistantRuntime.listSmartTabs: function

This proves the repaired Assistant Runtime is executing in the live browser before the Hub's unauthenticated redirect.

## Remaining browser boundary

A complete authenticated browser CRUD proof was not completed in this session. The live Hub redirects unauthenticated browser state to welcome.nayanet.app, and the available CDP route did not complete a legitimate UI authentication transaction before that redirect.

This is now a narrow product-facing browser boundary, not a backend authorization gap.

## Protected

No browser credential extraction. No token injection. No fake session. No service-role impersonation.

## Current truth

PROVEN: runtime cache-bust defect identified and repaired; repaired Hub deployed; live browser executes current Assistant Runtime; Smart Tabs runtime API is present in the live browser; backend authenticated Wave A closure from Session 006 remains valid.

NOT YET PROVEN: authenticated browser-level Smart Tabs/Feed visual CRUD and direct human target-navigation click proof.

## Successor

Use the canonical NayaNET authentication UI/adapter itself to establish the browser session legitimately, then perform browser-level Smart Tabs and Smart Feed UI proof. Do not inject tokens or bypass the identity flow.
