# NayaNET Master Execution Prompt — Hub Finish Line

## Mission
Finish the existing NayaNET Intelligent Hub from its current working state to a real, persistent, production-ready product WITHOUT redesigning or regressing the canonical visual experience.

## Non-negotiable product rule
The canonical Hub design is protected product IP and the current visual foundation. Never replace it with a generic dashboard, new template, mobile-first substitute, or unrelated React reconstruction to solve an implementation problem.

**Keep the ladder. Replace the broken rung.**
**Replace plumbing, not presentation.**

## Source of truth
Repository: SoulSchoolAcademy/NayaPOWER
Default branch: main
Canonical visual reference: `2026 09 17 NAYANET HUB.html`
Canonical backend/runtime surfaces already present include:
- `supabase/functions/naya-smart-feed/index.ts`
- `supabase/functions/v7-smart-note-canonical/index.ts`
- Project Intelligence bridge/runtime workflows
- existing browser acceptance/proof workflows

## Current verified direction
The repository contains a premium canonical Hub surface and a real Smart Feed backend that:
- authenticates the user;
- reads personal/activity cognition events;
- reads explicitly published collective intelligence;
- attaches Smart Ledger verification/evidence;
- attaches Intelligent Block data;
- persists governed feed interactions;
- supports publish/revoke with authority validation.

The canonical Smart Note receiver creates a verified `NAYANET_INTELLIGENT_BLOCK_V1`, persists the event through `v7_create_smart_note`, records evidence, and marks the Hub feed as updated.

Therefore the next engineering problem is integration/projection: make the existing Hub reliably consume and operate on those canonical systems, then prove the complete user journey.

## Execution order
1. **Trace the canonical Hub runtime.** Identify exactly which scripts render the visible feed, where data originates, and which legacy/demo layers can override it.
2. **Make canonical Smart Feed the sole runtime data authority** for the visible feed while preserving the current renderer and CSS.
3. **Make Smart Note capture real end-to-end:** create -> canonical receiver -> persistence -> retrieve -> render in Hub -> refresh -> still present.
4. **Make Intelligent Blocks first-class feed objects** using the existing V1 contract; do not invent another schema.
5. **Make Personal / Collective / Activity true projections** of the same governed intelligence, with privacy and consent rules intact.
6. **Make feed actions persistent and verified:** Save, Favorite, Like, Love, Publish/Revoke where authorized.
7. **Wire sidebar destinations one surface at a time** using existing architecture, starting with Intelligence Today, Smart Feed, Smart Notes, Library, Reports.
8. **Then wire Smart Share, Smart Lists, Smart Spaces, Connections.**
9. **Then wire Smart Mail, Smart Ledger, Naya Play, Settings.**
10. **Run desktop browser acceptance and production closure** only after the real data path survives reload and the visual surface remains unchanged.

## Verification contract
No feature is called complete because a button clicks or a demo appears.
For each rung prove:
**source -> runtime -> persistence -> retrieval -> browser rendering -> refresh persistence -> governed receipt/evidence**.

Unknown is not success. Blocked is not pass. Do not retry without new information.

## Working protocol for Naya
At the start of every engineering turn:
1. Read this execution state.
2. Check current main HEAD.
3. Inspect the relevant source before changing anything.
4. State the single highest-value causal repair being attempted.
5. Make the smallest safe change.
6. Verify with source/build/workflow/browser evidence.
7. Update the execution state with what changed, what was proven, what remains, and the next action.
8. Never leave Shawn without a next action or a current execution prompt.

## Immediate next action
Trace the canonical Hub feed boot/render path against `naya-smart-feed` and identify the exact override/connection preventing the existing premium Hub renderer from being driven by canonical persisted Smart Feed data. Make one causal repair only, then run the narrowest existing acceptance proof for that path.

## Definition of done
Shawn can open the canonical Hub, see real persisted intelligence, create a Smart Note, see its Intelligent Block in the feed, refresh and still see it, switch Personal/Collective/Activity, perform authorized feed actions, navigate the sidebar into working surfaces, and pass desktop production acceptance without the design being downgraded.
