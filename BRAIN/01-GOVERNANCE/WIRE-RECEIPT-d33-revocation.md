# WIRE RECEIPT — D33 selective evidence revocation + claim requalification

**Directive:** D33 (Selective Evidence Revocation and Claim Requalification)
**Mechanism:** `drift_canary/d33_revocation.py` (PR #2212, owner naya4)
**Wire PR:** (opened by this lane; see #2175 sign-out)
**Wired:** 2026-10-11 ~11:45Z by the Naya 2 night-shift WIRE lane
**Status:** WIRED-AT-SEAM, merge pending (merge lane owns the queue)

## What was CODE-ONLY

The D33 engine was a fixture with 55 real asserts and zero live callers:
revoke an ineligible evidence source, recompute every dependent
conclusion under one consistent snapshot, preserve independently
sufficient conclusions. Its own docstring declared it
"NOT wired into kernel/, KNOW, LAW, ACT, or any live path."

## What is wired now

The engine sits on the **drift-canary governance-verification CI path**:

- `tools/d33_revocation_gate.py` — cold-judges every scenario in the
  manifest against the REAL `RevocationEngine` (imported from the live
  tree, never reimplemented). Exit 0 PASS / 0 DORMANT / 1 VIOLATION /
  2 BROKEN (fail-closed).
- `tools/d33_revocation_manifest.json` — zero live scenarios
  (explicit DORMANT) + worked fraud `_example` + worked honest
  `_example_honest`.
- `tests/test_d33_revocation_gate.py` — 14 tests: DORMANT/PASS/
  VIOLATION directions, fraud naming, scope-divergence, malformed
  manifests, and two sabotage negative controls (blind engine,
  missing mechanism).
- `.github/workflows/d33-revocation-gate.yml` — runs gate tests +
  gate on `pull_request` / `push-to-main` for the five watched paths.

## Proof a real violation gets blocked

- **Canary:** fixed masquerade fixture → engine DOWNGRADEs C to
  staging-only; a blind always-REQUALIFIED engine fails the canary →
  exit 2.
- **Fraud:** the worked `_example` (naive REQUALIFIED assertion over a
  secretly-derived path) registered as a live claim → **exit 1
  VIOLATION**, `asserted=REQUALIFIED actual=DOWNGRADED` in the
  mechanism's own words.
- **Honest:** `_example_honest` (genuinely independent E2) → exit 0 PASS.
- **Mechanism dogfood:** the D33 fixture's own 24 tests green on the stack.
- **Live wire:** `d33-revocation-gate` check-run GREEN on the clean PR
  tree; RED direction proven by the fraud/sabotage controls.

## Failure mode if the wiring breaks

- Workflow deleted → no check runs on drift-canary revocation PRs;
  re-add `.github/workflows/d33-revocation-gate.yml`.
- Manifest gains a live scenario with a wrong assertion → PR blocked
  (exit 1) until the assertion matches the engine.
- Mechanism file deleted/renamed → canary/load fails → exit 2 on any
  tree with live scenarios; DORMANT trees stay green (nothing to judge).
- Engine subtly neutered → canary fails → exit 2, never a blind pass.

## Verify it is still connected

1. `python tools/d33_revocation_gate.py --json` → exit 0, `"status": "DORMANT"`.
2. Copy `_example` to a live key → exit 1 naming
   `asserted=REQUALIFIED actual=DOWNGRADED`; revert → DORMANT.
3. The `d33-revocation-gate` check is present and required on PRs
   touching the five watched paths.

## Boundary (honored)

CI governance path only. The certificate/ACT-boundary surface
(`issue_certificate`, `check_at_use`, `authorize_act`) and runtime
wiring into kernel/, KNOW, LAW, ACT still need Shawn's word — the
gate judges revocation claims, it does not authorize acts.
