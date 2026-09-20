# Browser-Control Boundary — 2026-09-19

**Actor:** Naya E / Browser-Control Acquisition  
**Predecessor:** Issue #151 comment 5738596165  
**Status:** BROWSER CONTROL PROVEN; DEPLOYED AUTH BOUNDARY BLOCKED

## Evidence
- DESKTOP-OJ712N5 online.
- PyAutoGUI successfully controlled the visible Chrome UI.
- Puppeteer successfully launched a dedicated Chrome runtime and independently observed the deployed Hub DOM.
- Public runtime: https://aged-art-7c12.nayanet.workers.dev/
- Browser fetch of /NAYANET/name-first-auth-adapter.js returned HTTP 404.
- Deployed settings surface showed the older email/password authentication UI and remained unauthenticated.
- Browser-side NayaNETNameFirstAuth establishment returned ADAPTER_MISSING.
- Current main source contains the name-first adapter and AuthPanel contract, so the remaining blocker is deployed runtime/source parity, not browser-control availability.

## Not claimed
No authenticated deployed Smart Note, cognition, ledger/index retrieval, replay/no-duplicate, or second-user isolation proof is claimed.

## Protection
No credentials invented/extracted. No database proof relabeled as browser proof. No CCT. No production deployment change.

## Next
Repair and prove source -> build -> deployed runtime parity for the name-first auth adapter, then resume the browser transaction and second-user isolation proof.

**Observed main HEAD:** 1cb4ef7752b0664519890dce57c038f82a0fc160.
