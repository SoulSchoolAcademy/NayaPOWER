# Wave A — Authenticated Browser Handoff Acceptance — First Human-Facing Failure

**Date:** 2026-09-19  
**Repository:** SoulSchoolAcademy/NayaPOWER  
**Live Hub:** https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/  
**Workflow run:** 35463961160  
**Commit under test:** 3b4d388a1f2023e92a17eb7b34b5b8b3a5b6e335

## STATUS

**NOT_PROVEN — stopped at first failed human-facing gate.**

## What changed

Added the smallest dedicated Wave A browser-handoff acceptance harness:

- creates ephemeral authenticated A/B/C Supabase identities;
- joins the existing production Space through the canonical RPC;
- establishes the mutual A↔B Connection through the canonical RPC;
- issues a short-lived explicit `smart_mail_send` authority to A;
- hands the exact authenticated Supabase session into a fresh Playwright browser context through the canonical persisted Supabase session boundary;
- drives the live canonical Hub runtime;
- verifies each gate in sequence;
- stops on the first failure;
- writes a machine receipt only if every gate passes.

## Verified before the failure

1. Authenticated browser handoff — PASS
2. Existing production Space visible — PASS
3. A↔B membership visible — PASS
4. Connections — PASS
5. Smart List creation and connection membership — PASS

## First failure

**Gate 6 — Smart Mail**

The live Hub runtime call:

`window.NayaAssistantRuntime.sendSmartMail(...)`

failed with:

`TypeError: Failed to fetch`

Observed at:

`https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/assistant-runtime.js?v=20260919-wavea6:39:198`

The workflow therefore stopped before B retrieval, Intelligence retrieval, and C isolation.

## Interpretation

This is a **new, actionable runtime boundary finding**, not a reason to weaken security or bypass the Hub.

The authenticated browser handoff itself is now proven far enough to establish that the missing-session problem was solvable without impersonation or RLS changes.

The next bottleneck is specifically the **live Hub → `nayanet-smart-mail` browser request path**.

No synthetic Smart Mail result was recorded. No Wave A promotion occurred.

## Protected

- RLS unchanged.
- Authority model unchanged.
- Privacy boundaries unchanged.
- No service-role browser access.
- No direct production mutation used to fake UI state.
- No PRODUCTION_PROVEN claim.

## Next action

Inspect the live Smart Mail browser request boundary (URL, CORS/preflight, response status, and current deployed Edge Function contract) and make the smallest reversible repair only if the evidence identifies a real defect. Then rerun from the first failed gate.

**Proof rule:** no retry without new information.
