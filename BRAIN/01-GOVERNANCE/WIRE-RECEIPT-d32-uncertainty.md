# WIRE RECEIPT — D32 evidence-bounded uncertainty propagation

**Directive:** D32 (Evidence-Bounded Uncertainty Propagation)
**Mechanism:** `drift_canary/uncertainty_propagation.py` (on main, owner naya2)
**Wire PR:** (opened by this lane; see #2175 sign-out)
**Wired:** 2026-10-11 ~12:00Z by the Naya 2 night-shift BUILD lane
**Status:** WIRED-AT-SEAM, merge pending (merge lane owns the queue)

## What was CODE-ONLY

The D32 engine was a fixture with 90 real asserts and zero live callers:
a downstream claim can never become more certain, broader, or more
causally specific than its admissible evidence supports — but uncertainty
in one upstream source must not invalidate a genuinely independent,
sufficient alternative. Nothing ever asked it to judge.

## What is wired now

The engine sits on the **drift-canary governance-verification CI path**:

- `tools/d32_uncertainty_gate.py` — cold-judges every scenario in the
  manifest against the REAL engine (imported from the live tree, never
  reimplemented). Exit 0 PASS / 0 DORMANT / 1 VIOLATION / 2 BROKEN
  (fail-closed); three fixed canary probes (modality preservation,
  nonexplosion, kind discipline) must pass or the gate fails closed,
  never certifying through a blind engine.
- `tools/d32_uncertainty_manifest.json` — zero live scenarios
  (explicit DORMANT) + worked fraud `_example` (modality upgrade) +
  worked honest `_example_honest`, `_example_edge`, `_example_observation`.
- `tests/test_d32_uncertainty_gate.py` — 16 tests: DORMANT/PASS/
  VIOLATION directions, three fraud namings (upgrade, explosion,
  gap-overreach), malformed manifests, and three sabotage negative
  controls (blind engine, missing mechanism, hostile input).
- `.github/workflows/d32-uncertainty-gate.yml` — runs gate tests +
  gate on `pull_request` / `push-to-main` for the seven watched paths.

## Proof a real violation gets blocked

- **Canary:** fixed probes — `derive_modality("possible","summarize")`
  stays `possible`; conflict on P leaves Q `UNDETERMINED`; invented
  kinds refused. A blind always-`verified` engine fails the canary →
  exit 2.
- **Fraud:** the worked `_example` (assert `verified` for a `possible`
  cause via `summarize`) registered as a live claim → **exit 1
  VIOLATION**, `asserted modality=verified ... recomputed
  modality=possible (derivation_preserves_modality)` in the mechanism's
  own words.
- **Honest:** `_example_honest` / `_example_edge` /
  `_example_observation` → exit 0 PASS.
- **Mechanism dogfood:** the D32 fixture's own 90 tests green on the stack.
- **Live wire:** `uncertainty-gate` check expected GREEN on the clean PR
  tree; RED direction proven by the fraud/sabotage controls.

## Failure mode if the wiring breaks

- Workflow deleted → no check runs on drift-canary uncertainty PRs;
  re-add `.github/workflows/d32-uncertainty-gate.yml`.
- Manifest gains a live scenario with a wrong assertion → PR blocked
  (exit 1) until the assertion matches the engine.
- Mechanism file deleted/renamed → canary/load fails → exit 2 on any
  tree with live scenarios; DORMANT trees stay green (nothing to judge).
- Engine subtly neutered → canary fails → exit 2, never a blind pass.

## Verify it is still connected

1. `python tools/d32_uncertainty_gate.py --json` → exit 0, `"status": "DORMANT"`.
2. Copy `_example` to a live key → exit 1 naming
   `asserted modality=verified ... recomputed modality=possible`; revert → DORMANT.
3. The `d32-uncertainty-gate` check is present and required on PRs
   touching the seven watched paths.

## Boundary (honored)

CI governance path only. Runtime wiring into kernel/, KNOW, LAW, ACT
still needs Shawn's word — the gate judges uncertainty claims, it does
not authorize acts.
