# GOVERNED CLOUDFLARE PORTABLE EXECUTION — VERIFIED

**Status:** VERIFIED  
**Workflow run:** #10 / 35414256599  
**Branch:** `feat/cloudflare-production-adapter-portable-v1`  
**Proof head:** `b1520c4690122026596ba891654d79536911ded9`

## What was actually proven

The governed execution boundary crossed from controlled runtime into the real Cloudflare external action surface.

The accepted path was:

**request → 13-question identity binding → canonical authority → consequential UEG → `execute_authorized()` → deployment-specific Cloudflare adapter → independent portable verification → real Cloudflare action → machine receipt → replay refusal → revocation-at-use refusal → authenticated NayaNET cognition/PIS persistence → live Hub retrieval → Activity rendering**

### External action

The protected independent GitHub Actions runner checked out the exact authorized repository commit:

`44b4829c8815ea4c62d15c0a74befb963054ccc0`

It built the exact Hub source, then verified and invoked the concrete Cloudflare adapter.

Observed Cloudflare result:

- Worker: `sparkling-shape-7ae5`
- Environment: `preview`
- Version ID: `4aeb34e3-16a2-406b-bf3d-b07e5f98cf26`
- Action ref: `cloudflare:sparkling-shape-7ae5:preview:CF-PORTABLE-PROOF-001`
- Source checkout: `44b4829c8815ea4c62d15c0a74befb963054ccc0`

The verified action created a real Worker version. It did **not** deploy that version to production traffic.

### Portable receipt

The independent runner wrote:

`.naya/receipts/2026-09-19-CF-PORTABLE-PROOF-001.json`

Receipt status:

`VERIFIED_EXTERNAL_ACTION`

Receipt binds:

- action `CF-PORTABLE-PROOF-001`
- decision `CF-PORTABLE-PROOF-DEC-001`
- authority `HUMAN-SOULSCHOOLACADEMY-HUB-DEPLOY-509`
- identity `SoulSchoolAcademy`
- identity fingerprint `a98dbac29153e7432f5753f7724ec69e36a5612f5c07fc7a29113ceda21c83cb`
- identity binding `a816dfd2c73f12b04b9fe0f6d7fa1f361f6b6fb98d95498300145aa4dd758e99`
- execution binding `c3d77abb58ac892b815f91cba5d659dd3718dc118621962e156b2aed29c0436a`
- portable artifact SHA-256 `c98b7ceb4a9520e2c23fc22e30fa568f39c18a73b8d4835a442687c7b3485562`

### Replay

A separate fresh GitHub Actions runner downloaded the first-use receipt and single-use marker, reconstructed the exact authorized source, and attempted the same portable authorization.

Result:

**REPLAY = REFUSED**  
**EXTERNAL_ADAPTER_INVOKED = FALSE**

The adapter was not called on the replay path.

### Revocation-at-use

A separate runner created an independently revoked view of the canonical Authority Registry and attempted use of the same signed portable authorization.

Result:

**REVOCATION_AT_USE = REFUSED**  
**EXTERNAL_ADAPTER_INVOKED = FALSE**

Revocation therefore remained an authorization property evaluated at use; the portable artifact did not become authority merely because it had previously been valid.

### Activity / PIS continuity

The portable receipt was persisted through the existing authenticated NayaNET cognition boundary:

`nayanet_record_cognition_event` → `nayanet_cognition_events`

The live Hub then retrieved the exact event through `NayaAssistantRuntime.retrieve()`.

Machine result from the fresh browser context:

`{"ok":true,"authenticated":true,"count":1,"found":true,"activity_rendered":true}`

Event ID:

`cloudflare-portable-CF-PORTABLE-PROOF-001`

This proves continuity into both the existing Personal Intelligence persistence path and the live Activity projection. No second execution-PIS store was introduced.

## Proof corrections made during execution

Two real harness defects were caught by the proof and fixed rather than papered over:

1. Portable issuance incorrectly required `validated_at == issued_at`; this was corrected to reject only impossible forward-time ordering.
2. The replay/PIS jobs initially had non-deterministic artifact/script placement; both were replaced with explicit artifact handoff and workspace-local execution.

The final run (#10) then passed all four jobs:

**first-use PASS · replay PASS · revocation PASS · activity-pis PASS**

## Boundary now established

NayaPOWER has now proven a real external action boundary without creating a second authority system:

**governed identity + canonical authority + consequential UEG + `execute_authorized()` + concrete external adapter + portable receipt + replay control + revocation-at-use + authenticated cognition continuity + live Activity projection**

The proof workflow is now **manual-only** so ordinary repository commits cannot trigger an external Cloudflare action.

The portable signing key was not committed.

### Continuation action

Issue a fresh short-lived authorization for the next concrete external action. Treat this artifact as historical proof, not a reusable standing credential.
