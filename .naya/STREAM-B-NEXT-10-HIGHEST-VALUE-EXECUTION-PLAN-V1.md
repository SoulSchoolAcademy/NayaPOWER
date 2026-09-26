# 🔱 Stream B — Next 10 Highest-Value Execution Frontiers V1

Date: 2026-09-24
Current branch: `naya/stream-b-canonical-intelligence-commit-bridge-20260924`

## Priority order

1. **Provision the portable verifier public key**
   - Boundary: Supabase Edge Function secret `NAYANET_PORTABLE_AUTH_PUBLIC_KEY_HEX`.
   - Why: without a pinned public key, production cannot cryptographically distinguish a genuine portable artifact from caller JSON.
   - Status: **BLOCKED ON AUTHORIZED SECRET PROVISIONING**.
   - Private key must never enter the repository or chat.

2. **Wire the production Edge Function verifier**
   - Verify schema, Ed25519 signature, binding hash, TTL, actor, target, permission, production grant fingerprint, and current grant state.
   - Status: **IMPLEMENTATION PREPARED / DEPLOY NOT VERIFIED**.
   - The DB migration deliberately expects this boundary first.

3. **Complete the production-grant → canonical Authority adapter**
   - Production grant UUID remains `authority_id`.
   - Canonical Authority fields are deterministic: subject, mission, canonical JSON scope, actions, expiry, revocation.
   - Status: **IMPLEMENTED + LOCAL TEST VERIFIED**.

4. **Connect the adapter to UniversalExecutionGate + portable issuance**
   - Build the exact runtime path:
     `live grant -> production Authority -> UniversalExecutionGate -> ExecutionAuthorization -> portable artifact`.
   - Status: **NOT YET PRODUCTION-WIRED**.
   - This is the remaining gate-to-production issuance bridge.

5. **Migrate `nayanet-compound-intelligence` intelligence.capture**
   - Caller must supply the signed portable artifact.
   - Edge Function verifies it, then calls service-role-only canonical DB seam.
   - Status: **CALLER MIGRATION NOT DEPLOYED**.

6. **Apply the canonical DB migration only after #1–#5 are ready**
   - It creates the single persistence seam and blocks legacy intelligence.capture overload bypass.
   - Status: **REPO IMPLEMENTED / PRODUCTION NOT APPLIED**.
   - Applying earlier would intentionally block current intelligence.capture traffic.

7. **Run the fail-first live adversarial suite**
   - forged JSON
   - tampered actor/grant/permission/target/decision/action/binding
   - expired artifact
   - revoked grant after issuance
   - wrong grant
   - direct legacy 6-arg bypass
   - direct legacy 7-arg bypass
   - blocked execution creates no SUCCESS receipt
   - Status: **NOT YET LIVE**.

8. **Complete caller inventory before destructive removal**
   - SQL/RPC
   - all Edge Functions
   - Hub/runtime
   - tests/fixtures
   - workflows/scripts
   - production vs test-only
   - Status: **PARTIAL**; live SQL callers and active compound-intelligence caller are known, exhaustive application inventory remains open.

9. **Independently reconstruct one successful receipt**
   - Prove:
     **actor → production grant → canonical Authority → gate decision → portable credential → Edge verification → intelligence commit → persistence → receipt → cognition receipt_id**
   - Status: **NOT YET LIVE**.

10. **Retire the legacy authorization route and close the proof ledger**
    - Remove/block the old intelligence.capture overload only after caller migration is independently verified.
    - Update Issue #554, Smart Ledger evidence, current truth, and successor handoff.
    - Status: **NOT YET**.

## Holes in the job

- **Cryptographic issuer key provenance:** no verified production public-key pin currently exists.
- **Gate-to-production issuance:** the existing gate/portable verifier is proven in Python but is not yet connected to live production grants.
- **Edge Function source parity:** live version 38 exists; repository source/deploy parity for this exact verifier is not yet established.
- **Caller completeness:** GitHub code search did not provide an exhaustive application caller inventory.
- **Production mutation sequencing:** DB migration must not precede the verifier/caller boundary because it intentionally blocks the old intelligence.capture path.
- **Live causal proof:** no current live success has yet traversed the complete canonical chain after convergence.

## Already completed in this frontier

- Canonical production DB persistence seam added in repo.
- Legacy intelligence.capture overloads fail closed while non-intelligence behavior remains preserved.
- Production grant identity adapter implemented.
- Contract tests pass locally.
- Fresh-clone verification passed with exit 0.
- No production mutation performed.

## Stop condition

Do not declare Stream B production convergence VERIFIED until the live chain has been independently reconstructed from persisted evidence. DOCUMENTED or IMPLEMENTED is not enough.
