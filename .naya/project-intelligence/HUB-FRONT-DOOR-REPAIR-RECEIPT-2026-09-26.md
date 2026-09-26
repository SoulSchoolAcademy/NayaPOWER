# NayaPOWER — Canonical Hub Front Door Repair Receipt

**Date:** 2026-09-26
**Status:** IMPLEMENTED + SOURCE-LEVEL_BROWSER_PROVEN · PRODUCTION_PROOF PENDING RELEASE
**Observed live main at start of work:** `93c9329d476945e47b8cf152c31c66133d88643a`
**Canonical active block:** `HUMAN-JOURNEY-P2`
**Canonical next action executed:** give a new human a working front door on the canonical Hub.

## Defect observed on live production (read-only evidence, no auth required)

The canonical unauthenticated entry path is a hard redirect to `/identity.html`:

- `NAYANET/HUB/public/assistant-runtime.js` — `rt.openAuth=()=>{location.assign('/identity.html')}`
- `NAYANET/HUB/public/hub-completeness.js` — `if(!snap?.authenticated && kind!=='settings'){location.assign('/identity.html');return}`

No `identity.html` exists anywhere in the repository. The deployed Worker is configured with
`not_found_handling: single-page-application`, so the redirect target resolves back to the Hub
index. Live probe of the deployed artifact:

| Path | HTTP | Bytes | Title |
| --- | --- | --- | --- |
| `/` | 200 | 849643 | `NayaNET — Intelligent Hub V7 · 509 AAA` |
| `/identity.html` | 200 | 849643 | `NayaNET — Intelligent Hub V7 · 509 AAA` |

**Consequence:** an unauthenticated human who touches any governed surface is bounced
`/` → `/identity.html` → `/` indefinitely. There is no sign-in surface at all, so
`sign-in → capture → feed → deep link` cannot begin. This is the exact defect named in the
canonical `BATON.json` next action.

## Repair (additive, fail-closed, no second identity authority)

1. Added `NAYANET/HUB/public/identity.html` — a minimal name-first identity page that loads the
   **one existing** adapter (`/NAYANET/name-first-auth-adapter.js`) and calls its
   `establish({name, alias})`. It holds no credentials, no Supabase URL/key, and no identity
   storage of its own; session authority remains the existing Supabase Auth boundary owned by
   the adapter. It fails closed with the real error code, preserves the requested surface via
   `?next=`, and never reports success unless `identity.authenticated === true`.
2. Wired the page into the governed release artifact in
   `.github/workflows/assistant-cloudflare-hub-release.yml`: it is copied to `dist/identity.html`,
   asserted non-empty, and a new post-deploy gate proves the live page is byte-identical to the
   released source **and is not the Hub SPA fallback** (`IDENTITY_FRONT_DOOR_SERVED_HUB_SPA_FALLBACK`
   fails the release).
3. Added `tests/test_hub_identity_front_door.py` (12 contract tests) covering adapter wiring,
   single-adapter/no-duplicate-credential enforcement, fail-closed behavior, redirect
   reachability, and release-artifact wiring.
4. Reconciled the control plane. `MAP.json` (3 surfaces), `STATE.json` (`next_action`,
   `current_frontier`) and `PROOF.json` still carried the superseded behavioral cold-Naya
   takeover action, which made `validate_control_plane.py` **RED** on current main with
   `MAP and BLOCK next actions disagree`. All now carry the single canonical action, and the
   baton was rebuilt from source.

The preserved canonical Hub entrypoint `NAYANET/HUB/index.html` was **not** modified, so the
Hub preservation freeze gate remains satisfied at blob `0c2b9381deda6db5935afc55c508d97a965ae412`.

## Verification performed

| Check | Result |
| --- | --- |
| `tests/test_hub_identity_front_door.py` + release authorization tests | 12 passed |
| Hub / deep-link / IB-boundary / deployment-verifier subset | 19 passed |
| `tests/test_control_plane_freshness.py` + front door | 25 passed |
| Full suite (excluding two pre-existing collection failures) | 337 passed, 30 failed, 37 errors — failure/error counts unchanged from baseline, no regression introduced |
| `validate_control_plane.py` | **GREEN** (was RED before reconciliation) |
| `validate_control_plane.py --self-test` | GREEN |
| `baton.py build-and-validate` | PASS |
| `cold_start_activation.py` | VERIFIED |
| `cold_start_control_plane_acceptance.py` | PASS (stale identity, recorded head, unknown proof, multiple next actions all REJECTED) |
| `cold_successor_test.py` | 14/14 questions answered from canonical sources |
| Release-gate simulation (preservation checkpoint reachability/ancestry, session lease ancestry, entrypoint blob) | all gates satisfied |
| Real headless-Chrome proof over CDP against the released source, live Supabase | **PASS** |

Real sign-in evidence from that browser proof (test identity, **not** the owner):

- Page state before: `READY · NAME-FIRST IDENTITY · NO PREVIEW IDENTITY IS PROMOTED`
- Adapter surface: exactly `["current","establish"]`, frozen
- After submit: `IDENTITY ESTABLISHED · CONTINUING TO THE HUB`, tone `ok`
- Real Supabase session established: user `e6e58314-a1f7-4c97-9da8-fd38eb8b6552`, anonymous session,
  smart name `Front Door Proof`, alias `frontdoorproof143340`
- `NayaNETNameFirstAuth.current()` returns the same identity
- Continued to `/` (the requested canonical surface)
- Empty name fails closed: `NAME_REQUIRED · tell NayaNET who you are to continue`, tone `blocked`

## What is NOT proven

- Production parity. The live Hub still serves the Hub at `/identity.html`; the repair is not
  released until the governed Cloudflare workflow is dispatched and its new live gate passes.
- Authorized owner sign-in for member `1112073e-08ee-407e-a47a-8b65b845f57b`; the browser proof
  used a throwaway anonymous member and must never be treated as owner attribution.
- `capture → feed → deep link` after sign-in; that proof requires the released artifact and an
  authorized owner session.
- Hub render completeness in the local harness: the harness served only the four proof files, so
  it proves the front door and identity boundary, not full Hub rendering. Full shell rendering
  remains the release workflow's own browser gate.

## PRODUCTION PROOF (added after release)

- PR `#795` merged to `main` as `8d7ee84875163ee28b86870cc24373ac462a022e`.
- Release workflow `assistant-cloudflare-hub-release.yml` run **`36262036641`**: `success`, with the
  new `Verify live name-first identity front door` step passing alongside
  `HUB_PRESERVATION_GATE_VERIFIED` and the Naya session/merge-boundary lease.
- Independent byte-parity probe (not the workflow's own check):

| Artifact | Source | Live | Byte identical |
| --- | --- | --- | --- |
| `/identity.html` | `4c8947633d1e0c0e36f12ff65df79479f55cbd0a5b6c77b82bb1106436988976` (7285 bytes) | same sha256 | yes |
| `/` index | `ece071671e1ea589bfa98dbfb9c182eb7b5021a07605231b3a43cd88e4e90681` | same sha256 | yes |

  Live `/identity.html` now serves `NayaNET — Identity`, is not the Hub SPA fallback, loads
  `/NAYANET/name-first-auth-adapter.js`, and calls `establish()`.

### Live journey proof: sign-in -> capture -> feed -> deep link -> reload -> canonical projection

Real headless-Chrome run against production, throwaway anonymous identity
`4df2803c-a048-4611-8e93-3f31e1d7c4a0` (alias `fdlive47000439`). **Test identity, never owner
attribution.**

| Stage | Evidence |
| --- | --- |
| Front door | title `NayaNET — Identity`, state `READY · NAME-FIRST IDENTITY · NO PREVIEW IDENTITY IS PROMOTED` |
| Sign in | `IDENTITY ESTABLISHED · CONTINUING TO THE HUB`; adapter `current().authenticated = true`; Supabase session present; runtime `snapshot().authenticated = true` |
| Hub | canonical shell present (`.shell`) |
| Capture | event `546d7a37-b155-43c4-9e48-4ba255c093d5`, receipt `4841cd24-0758-4ebe-8ac5-523c01759de4`, transaction `9af0d718-cec6-4a4a-ad35-2317173c9b19` |
| Receiver identity | **`IB-001223`**, issued by the canonical receiver, not guessed |
| Smart Link | `https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/.naya/memory/smart-notes/2026/09/26/system/front-door-live/IB-001223/smart-note.md` |
| Projection | `PROJECTION_VERIFIED`, authority grant `6b1ffbe4-9d41-42e3-aa28-00e9bf9f9796`, dispatch receipt `08b67dca-e890-4706-9a5c-8e0efb2d9f07`, run `36262371595` (success) |
| Repository | canonical Smart Note present on `main` at the exact Smart Link path |
| Feed | personal stream returned the event, `verification_state: active` |
| Retrieval | authorized retrieval returned the event |
| Deep link | `/hub?ib=IB-001223` renders the Intelligent Block |
| Reload | the same deep link re-renders it after a full reload |

`LIVE_JOURNEY_PROOF: PASS`

### What remains unproven

- The authorized **owner** journey for member `1112073e-08ee-407e-a47a-8b65b845f57b`, including the
  exact `LEARNING_OUTPUT` candidate acceptance recorded in `BLOCKS.json`.
- The orphaned conversation -> intelligence entry from the 2026-09-25 memory quarantine, which is
  still neither restored nor explicitly retired.

## Exact successor action

Dispatch `.github/workflows/assistant-cloudflare-hub-release.yml` against `main` with
`approval=EXPLICIT_APPROVAL_GRANTED` and a reason, confirm the new
`LIVE_IDENTITY_FRONT_DOOR_VERIFIED` gate, then use an authorized owner session to prove
`sign-in → capture → feed → deep link` at the exact release identity.
