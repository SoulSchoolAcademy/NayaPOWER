# NayaNET Canonical Routing Contract V1

Status: CANONICAL ROUTING CONTRACT
Effective: 2026-09-19

## Authority

The protected Hub freeze point is:

- `2026 09 17 NAYANET HUB.html`
- canonical production worker: `sparkling-shape-7ae5`
- canonical production runtime: `https://sparkling-shape-7ae5.smartnetpodcast.workers.dev`

This artifact is the user-facing Intelligent Hub projection. The React/Vite implementation under `NAYANET/HUB/` is not the user-facing freeze point unless Shawn explicitly establishes a new freeze point.

## Required public route

`welcome.nayanet.app` is the front door.

Required route:

```
welcome.nayanet.app
    ->
NAME-FIRST ENTRY
    ->
AUTHENTICATED NayaNET
    ->
2026 09 17 NAYANET HUB.html
```

The Welcome surface must not silently route users to the React/Vite Hub, an obsolete Hub artifact, or an unrelated legacy surface.

## Projection rule

The canonical Cloudflare release workflow must project and verify byte-exact parity for:

- `2026 09 17 NAYANET HUB.html`
- `assistant-runtime.js`
- `identity.html`
- `NAYANET/name-first-auth-adapter.js`

The live canonical worker must pass exact SHA-256 parity and browser baseline verification before Welcome routing is changed.

## Routing ownership boundary

Changing `welcome.nayanet.app` requires control of the authoritative `nayanet.app` DNS/Cloudflare route boundary. A Worker deployment token for another Cloudflare account/zone is not sufficient authority.

Do not fabricate, bypass, or force a route change when the authoritative zone is unavailable.

## Freeze protection

Do not:

- replace the frozen Hub with React/Vite merely because it is present;
- redesign the frozen Hub while repairing routing;
- change the Welcome source before the canonical Hub projection is verified;
- create a second user-facing Hub;
- treat a workers.dev hostname as equivalent to the custom-domain front door;
- claim the Welcome route is fixed until an external request to `https://welcome.nayanet.app/` is verified to reach the canonical Hub.

## Verification

A routing repair is VERIFIED only when an external request to `welcome.nayanet.app` proves:

1. the expected public entry surface;
2. the expected name-first identity path;
3. the canonical Hub marker;
4. the canonical Hub SHA-256 or an equivalent immutable release identity;
5. no React/legacy Hub marker is served as the user-facing projection.

## Current state

As of 2026-09-19:

- canonical Hub projection: VERIFIED;
- canonical identity assets: VERIFIED;
- canonical Cloudflare release workflow: VERIFIED;
- GitHub Dispatch pre-issued-authority boundary: VERIFIED;
- `welcome.nayanet.app` -> canonical Hub: NOT VERIFIED;
- authoritative `nayanet.app` route-control ownership: NOT YET AVAILABLE in the currently authorized Cloudflare account.

## Next action

Recover or connect the authoritative `nayanet.app` Cloudflare/DNS control plane. Then inspect the existing custom-domain route and change only that routing/projection layer. Re-run the complete external Welcome -> identity -> Hub proof before declaring the route VERIFIED.
