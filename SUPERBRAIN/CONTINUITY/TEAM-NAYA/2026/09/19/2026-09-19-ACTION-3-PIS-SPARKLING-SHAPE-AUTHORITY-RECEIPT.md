# Action 3 — Sparkling Shape React PIS Connection and Authority Receipt

**Date:** 2026-09-19

## Mission
Connect the real canonical PIS/intelligence object to the preserved Sparkling Shape React surface and prove the exact canonical event ID and title render.

## Proven React path
Sparkling Shape React shell → `App.tsx` → `HubHome` / `CommandCenter` → `loadPrimaryIntelligence()` → build projection `/intelligence/pis-feed.json` → `IntelligentEvent` → `SmartFeedBoard`.

The preserved shell carries runtime marker `NAYANET-HUB-REACT-CANONICAL`.

## Exact proof
Target event:
`CANONICAL-2026-09-17T17-20-00Z-WHAT-IS-A-SMART-NOTE`

Rendered title:
`What Is a Smart Note?`

Local production build: PASS, 86 modules.

Generated PIS:
- event_count=13
- target event present
- target title = `What Is a Smart Note?`

Browser proof against the built React Hub:
- runtime marker = `NAYANET-HUB-REACT-CANONICAL`
- rendered `data-event-id` = target canonical event ID
- rendered `data-event-title` = `What Is a Smart Note?`
- visible title = `What Is a Smart Note?`

A proofability-only PR is open as PR #318; it adds the event ID/title as DOM data attributes and changes no visual behavior.

## Production authority finding
The live Cloudflare worker `sparkling-shape-7ae5` currently serves the exact GitHub file `2026 09 17 NAYANET HUB.html`.

Exact SHA-256 parity was proven:
- GitHub current HTML: `55EC65FF2D145A16D9119268C5F17C72C16114E3BCD459981875050BF367634D`
- Live worker HTML: same hash

The live artifact contains `nayanet-direct-nine` and does not contain the React marker.

The repository's Assistant Cloudflare release workflow explicitly prepares `2026 09 17 NAYANET HUB.html` and deploys it to `sparkling-shape-7ae5`. Therefore the current production-authoritative Hub artifact is the existing V7/current HTML, not the React Hub yet.

`2026 09 17 NAYANET HUB V2.html` exists in repository history as a candidate artifact, but the current deployment path and live exact-parity proof do not identify it as the production artifact.

The React `NAYANET/HUB/wrangler.jsonc` names the same worker and points at `dist`, but that configuration is not the currently proven production deployment path. This is a source/deployment authority conflict that must be resolved before replacing the live artifact.

## Governance finding
`DEPLOYMENT-GOVERNANCE.json` is absent from current repository history available on this checkout. Git history search produced no proof that this exact file existed as a canonical tracked control. Do not recreate it merely to satisfy tests.

## Protected state
- Do not redesign Sparkling Shape.
- Do not create a second Hub.
- Do not use Vercel as a deployment path.
- Do not resolve the large reconciliation merge yet.
- Do not weaken RLS/security.
- Do not modify Supabase functions for this work.
- Do not enable live dispatch without an authorized execution path.

## Next highest-value action
Resolve the Hub deployment/source authority conflict from evidence: preserve the current live V7 visual contract while determining the canonical path by which the React Sparkling Shape Hub can replace that exact live artifact safely. Then deploy only through the verified authorized Cloudflare surface and prove source hash → deployment → runtime → canonical event rendering.
