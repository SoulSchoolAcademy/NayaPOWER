# 48 — Smart Connect + Runtime Boundary Audit — 2026-09-24

## Status
SOURCE/UX RECONCILED · RUNTIME COLLECTIVE CONTRIBUTION STILL OPEN

## Canonical decision
NayaNET has one participation concept: **Smart Connect**.

Opening any governed Smart Connect door establishes participation consent:
- share wisdom by default;
- protect personal intelligence by default;
- protect personal activity by default;
- protect identity by default;
- permit governed human/Naya connection in Smart Spaces.

Public publication and identity attribution remain separate deliberate decisions.

## Seven doors
1. GitHub App
2. MCP
3. REST / OpenAPI
4. Webhooks
5. SDK
6. A2A
7. MCP Apps

## Runtime trace result

### Proven
- `v7-smart-note-canonical` authenticates the member and automatically creates `learning_evidence`; it does not ask for per-Smart-Note approval.
- The canonical Smart Note checkpoint is routed through `nayanet-compound-intelligence`.
- `intelligence_commit` correctly remains authority-gated; participation must not mint execution authority.
- Smart Connect now exists as the canonical Hub surface and seven-door product contract.

### First concrete mismatch
The production intelligence path has **no runtime participation-consent state that feeds collective learning**.

The existing `nayanet_connections` table is a person-to-person saved relationship, not the NayaNET door participation record. The current collective publication path (`nayanet_intelligence_publications`) requires `consent_state='explicit'` for each published intelligence event. Therefore the current runtime cannot yet implement:

`Smart Connect → participation consent → wisdom shared by default → governed collective filtering`

without either:
1. adding a dedicated Smart Connect participation-consent boundary, and
2. adding a governed derived collective-wisdom contribution path distinct from public publication.

## Safety boundary

Do not remove the `intelligence_commit` authority grant requirement. Smart Connect participation is consent to participate, not authorization to execute arbitrary actions.

Do not execute S54 until the participation-consent → collective-learning runtime seam is implemented and regression-tested.

## Evidence
- `.naya/protocol/NAYANET-INTELLIGENCE-PARTICIPATION-PRIVACY-PROTOCOL-V1.md`
- `NAYANET/HUB/SMART-CONNECT.md`
- `NAYANET/HUB/src/app/SmartConnectSurface.tsx`
- `NAYANET/HUB-ROOM-SYSTEM/04-SMART-CONNECT.md`
- `supabase/functions/v7-smart-note-canonical/index.ts`
- `supabase/functions/nayanet-compound-intelligence/index.ts`
- `supabase/migrations/20260919160000_smart_feed_collective_publication_v1.sql`
- `supabase/migrations/20260919171500_nayanet_connections_v1.sql`

## One next action
Design and implement the smallest governed runtime seam that records **Smart Connect participation consent per door** and automatically routes only qualifying derived wisdom into a **private-identity collective-learning boundary**, with public publication remaining separate; then add fail-first allowed/denied regression tests and prove the same causal path before any S54 execution.