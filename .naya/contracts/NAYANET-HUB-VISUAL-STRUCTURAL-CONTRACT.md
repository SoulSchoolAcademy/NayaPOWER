# NayaNET Hub — Visual & Structural Contract

**Status:** PROTECTED REFERENCE  
**Repository:** SoulSchoolAcademy/NayaPOWER  
**Canonical path:** NAYANET/HUB/index.html  
**Current source SHA:** f76ed6d6de6805a752dc81113ded42e67b3b6f80

NAYANET/HUB/index.html is the protected human-facing visual and structural reference for the NayaNET Hub.

The application implementation may be reorganized internally, but it must preserve the Hub's recognizable information architecture, visual language, navigation model, and interaction surfaces. Runtime code exists to make this surface operational; it does not replace the Hub as the visual source of truth.

Do not use the Welcome/front-door page as the Hub reference. Do not reopen the already-proven Smart Note → canonical event → PIS/Smart Feed compounding boundary for visual parity work.

## Existing controls → capability

| Surface/control | Capability | Implementation | Current evidence |
|---|---|---|---|
| Your Intelligence Today / Home | Authenticated canonical intelligence projection | HubRouter → FeedView → loadPrimaryIntelligence | Browser surface proven |
| Smart Feed | PIS retrieval/search/event render | FeedView + SmartFeedBoard + PIS | Runtime-proven |
| Smart Notes | Canonical capture/persist/retrieve | SmartNoteSurface + runtime.captureSmartNote | Production-proven |
| Intelligence Library | Canonical retrieval/search | FeedView(library) + PIS | Browser surface proven |
| Your Report | Report retrieval | ReportsSurface | Browser surface proven; deeper data proof remains |
| Smart Share | Explicit publication/consent | SmartShareSurface → publishSmartFeed | Runtime path implemented; adversarial proof next |
| Smart Lists | Create/list/retrieve | SmartListsSurface / FeatureSurface + canonical runtime/data | Browser surface proven; action proof remains |
| Your Connections | Relationship retrieval + consent | ConnectionsSurface + runtime relationship functions | Live membership traced; picker hydration repaired in acceptance |
| Smart Spaces | Permissioned space/membership | SmartSpacesSurface + runtime relationship functions | Browser surface proven; governance proof remains |
| Smart Mail | Thread/message + authority-bound send/verify | SmartMailSurface → sendSmartMail / verifySmartMail | Browser surface proven; adversarial send proof remains |
| Smart Ledger | Accountability/evidence inspection | FeatureSurface + ledger data + governed inspection | Browser surface proven; mutation/receipt proof remains |
| Dream | Dream/RSI scoring/replay | DreamSurface | Component proof exists; Hub journey continues |
| Naya Play | Canonical intelligence playback | NayaPlaySurface + runtime playback/receipt | Browser surface proven |
| Settings | Identity/system settings | SettingsSurface | Browser surface proven |
| Universal search / Talk to Naya | Canonical search/navigation | AppShellV3 + FeedView deep search | Browser surface proven |
| Capture Smart Note | Human capture entry point | AppShellV3 → canonical runtime | Production-proven |
| Explore Intelligence | Navigate to Feed | AppShellV3 → /feed | Implemented |
| Identity chip | Open Settings | AppShellV3 → /settings | Implemented |
| Feed lens → Smart Mail | Cross-surface navigation | FeedView custom event | Implemented |
| External ecosystem links | Explicit external destinations | Static Hub navigation | Present; outside runtime |

## First consequential unproven boundary

The Connections PERSON-selector issue was traced to Space selection → transient loading/empty state → asynchronous PERSON picker hydration. Live listSpaceMembers(spaceId) returned the expected membership, so this was an acceptance synchronization defect, not a missing product membership/runtime defect.

The next consequential boundary is governed action execution on the human-facing feature surfaces, starting with Smart Share and Smart Mail, then Connections, Spaces, and Lists. Stop at the first failed layer:

human control → runtime action → authority binding → owner/scope isolation → revocation/expiry → idempotency/replay → execution receipt → persisted outcome → rendered result.

No visual redesign is authorized by this contract.

## Evidence and non-regression

Rendering is not proof. A capability reaches VERIFIED/RUNTIME-PROVEN/PRODUCTION-PROVEN only when its runtime, persistence, authorization, receipt, and browser evidence exist.

Visual/structural work must not modify the already-proven Smart Note → canonical event → cognition/PIS persistence → Smart Feed → reload → learning/compounding boundary unless an independent defect is demonstrated.
