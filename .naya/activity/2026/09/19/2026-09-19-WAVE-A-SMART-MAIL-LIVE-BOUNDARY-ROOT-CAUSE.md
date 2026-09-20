# Wave A — Smart Mail Boundary Investigation

**Date:** 2026-09-19  
**Live Hub:** https://sparkling-shape-7ae5.smartnetpodcast.workers.dev/

## STATUS

**NOT_PROVEN — concrete boundary mismatch identified. No production repair applied.**

## Evidence

The live root currently returns the React canonical Hub:

- `index-It174yfW.js`
- `index-BKAr1RiB.css`
- `NAYANET-HUB-REACT-CANONICAL`

A fresh browser context has:

- no service worker;
- no Cache API entries;
- `window.NayaAssistantRuntime === undefined`;
- only the React bundle, name-first adapter, and cognitive engine loaded.

The live `/assistant-runtime.js?v=20260919-wavea6` endpoint currently returns:

- HTTP 200
- `Content-Type: text/html`
- the React SPA HTML

It does **not** return `assistant-runtime.js`.

## Root cause

The current Cloudflare deployment is on the **sparkling-shape-react** release surface, while the Wave-A Smart Mail harness expects the **legacy-v7 Assistant runtime surface**, whose release workflow explicitly copies root `assistant-runtime.js` into the deployed `dist/` and verifies source parity.

Therefore the previous `sendSmartMail → TypeError: Failed to fetch` was not evidence of an RLS, authority, CORS, or Smart Mail function defect. The browser was executing a stale/legacy Assistant runtime contract against a live deployment that no longer serves that runtime asset.

## Important distinction

The live React Hub is healthy enough to render its canonical read surfaces, but it currently does not expose the Assistant runtime's governed Smart Mail write contract.

The smallest safe repair is therefore **deployment-contract alignment**, not an RLS/security change and not a Smart Mail backend rewrite.

## Protected

- No RLS changes.
- No authority changes.
- No production membership/relationship changes.
- No Smart Mail backend changes.
- No synthetic browser result.
- Wave A remains NOT_PROVEN.

## Next action

Before changing production surface, explicitly reconcile the intended canonical release surface:

**A.** restore/deploy the existing Assistant/legacy-v7 surface, which already contains the proven Smart Mail runtime contract; or

**B.** implement the governed Smart Mail write contract in the current React canonical surface, which is a larger frontend/backend integration change.

Do not silently choose B or roll production back to A.

