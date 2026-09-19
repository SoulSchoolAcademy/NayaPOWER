# NayaNET Engineering System — Completion Pass
Date: 2026-09-19

## Purpose
Engine-first closure of the ten NayaNET Engineering System feature areas. Human onboarding is intentionally excluded.

## Review matrix

| Feature | Before | Work completed | Current truth |
|---|---|---|---|
| Smart Tabs | Defined | Canonical production Edge Function reconciled into source; migration source restored; persistent authenticated Hub bar added; owner-scoped CRUD | IMPLEMENTED · runtime auth proof started |
| Smart Feed | Defined / partial | Authenticated Hub lenses now call canonical `naya-smart-feed`; event adapter added; save/favorite/like/love and publication actions routed through governed backend | IMPLEMENTED SUBSTRATE · browser/runtime parity still to prove |
| Smart Ledger | Implemented substrate | Canonical Ledger remains the only evidence store; feature surface reads owner-scoped Ledger | SUBSTRATE VERIFIED · current human surface not fully accepted |
| Smart List | Implemented substrate | Canonical List surface now creates Lists through existing RPC and reads canonical Lists | IMPLEMENTED · two-user product proof pending |
| Smart Mail | Implemented substrate | Product surface now sends through existing governed Edge Function; feature RPC anon execution removed | IMPLEMENTED · real two-user browser proof pending |
| Smart Share | Defined | Publish/revoke routed through canonical Smart Feed publication boundary with explicit consent and owner checks | IMPLEMENTED SUBSTRATE · real recipient/privacy proof pending |
| Smart Spaces | Foundation | Create, join, leave UI wired to canonical Space store/RPCs | IMPLEMENTED SUBSTRATE · two-user lifecycle proof pending |
| Your Connections | Defined | Save/revoke UI wired to canonical Connection RPCs | IMPLEMENTED SUBSTRATE · two-user lifecycle proof pending |
| Your Intelligence Today | Defined | Daily derived view reads canonical intelligence index, supports date selection, source traceability and truthful empty-day state | IMPLEMENTED DERIVED VIEW · synthesis/refresh acceptance pending |
| Intelligent Reports | Defined | Report surface reads canonical `v7_intelligence_reports`, displays period/status/source evidence | IMPLEMENTED VIEW · generation/regeneration acceptance pending |

## Security work
The user-facing relationship, list, space and Smart Mail SECURITY DEFINER RPCs are now explicitly authenticated-only. Legacy anon EXECUTE grants were removed.

Verified after migration:
- `nayanet_join_space`: no longer in anon SECURITY DEFINER findings.
- `nayanet_leave_space`: no longer in anon SECURITY DEFINER findings.
- `nayanet_save_connection`: no longer in anon SECURITY DEFINER findings.
- `nayanet_revoke_connection`: no longer in anon SECURITY DEFINER findings.
- Smart List mutation RPCs: no longer in anon SECURITY DEFINER findings.
- Smart Mail mutation RPCs: no longer in anon SECURITY DEFINER findings.

Existing unrelated security-advisor findings remain and are not silently classified as solved by this pass.

## Deliberate boundaries
- No onboarding work.
- No fabricated A/B identities.
- No RLS weakening.
- No alternate event store.
- No alternate Ledger.
- No replacement of the proven Smart Mail engine.
- Today and Reports remain projections/derived views over canonical sources.

## Shared activity-engine work
A canonical activity projection was added to the Hub from the existing `public.nayanet_team_activity` table. It provides the required YEAR → MONTH → DAY → SESSION navigation without creating a second event store. The activity lens now reads canonical team activity rather than duplicating the intelligence feed.

Local isolated Hub build was rerun after the activity implementation: `npm run build` succeeded with 91 modules transformed. The only remaining build output is the existing chunk-size warning; no compiler/build failure occurred.

## Verification boundary
Source changes are on branch `nis-completion-20260919` and PR #329. Production Smart Tabs Edge Function was deployed as version 4 with JWT verification enabled.

Unauthenticated Smart Tabs POST was observed returning HTTP 401.

Full browser acceptance is still NOT VERIFIED. The next proof is authenticated runtime verification of the new Activity projection against the canonical `nayanet_team_activity` source, followed by the remaining ten-surface acceptance sequence. No onboarding or substitute deployment path is in scope.


## Engineering Activity live-source verification — 2026-09-19

**STATUS: OBSERVED / NOT YET RUNTIME-VERIFIED**

Live Supabase inspection confirms the canonical `public.nayanet_team_activity` source currently contains **13 events across 13 sessions**, all dated today, spanning `2026-09-19 19:25:36.529+00` through `21:08:24.64+00`. The newest observed event is `SE-20260919210824-41feea8a-28e`, with session/run/receipt `SMART-MAIL-6606123a-4914-4082-80a9-851b186d351d` / `6606123a-4914-4082-80a9-851b186d351d` and the expected Activity fields populated.

The Hub projection source was inspected and matches the canonical table/field contract. This proves the **data source exists and is populated**; it does not yet prove the deployed/browser Activity surface can authenticate, query, render, and navigate the live records. The next gate is therefore runtime proof, not another schema or storage change.
