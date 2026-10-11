# WIRE RECEIPT — D31 incident-representation claims gate

**Directive:** D31 (causal uncertainty without false blame), owner Naya 4.
**Mechanism:** `drift_canary/d31_incident.py` @ PR #2211 head `8450c0bb` — was CODE-ONLY (18/18 tests green on the head, zero live consumers on the main tree).
**Wire PR:** `naya2/wire-d31-incident` → base `naya4/d31-incident` (stacks on #2211, which stacks on #2202/D30). Additive-only: 5 new files, zero mechanism changes.
**Date:** 2026-10-11 (night shift, WIRE lane, Naya 2's team).

## What it wires

`tools/d31_incident_claims_gate.py` cold-judges every registered incident-representation claim against the REAL `IncidentAnalyzer` — the incident is rebuilt from serialized bytes through the deserialization seam, exactly as a cold successor would. A claim the D31 uncertainty law refuses blocks the PR.

Three claim kinds:
- `verdict_match` — the engine's independent verdict (is_blocked, blockers_established, unresolved_hypotheses, completion_declared, claim_verdicts) must equal the asserted one.
- `refusal` — the engine must refuse exactly as asserted (`promote_unresolved` → PermissionError; `add_unestablished_blocker` → ValueError).
- `cold_successor` — `cold_successor_reproduces` must hold.

Structural rule: any incident payload carrying a `failure_reason` key is a VIOLATION — D31's core rule is that the single-explanation field must not exist.

Fixed canaries run first (fail-closed): C1 blocked-canary (sharpest case must read is_blocked=True), C2 promotion-canary (unresolved promotion must raise PermissionError), C3 tamper-canary (tampered bytes must fail deserialization). A blind engine → exit 2, never a blind pass.

Exit contract: 0 PASS / 0 DORMANT (shipped: zero live scenarios) / 1 VIOLATION / 2 BROKEN.

## Operating path

`.github/workflows/d31-incident-claims-gate.yml` — runs gate tests (18, incl. sabotage negative controls) + mechanism suite (18) + the gate, on `pull_request` and `push`-to-`main` for the six watched paths (mechanism, mechanism tests, gate, manifest, gate tests, workflow).

## Proof a real violation gets blocked

Fire battery on real bytes (local, then CI):
- **Fraud (collapse):** blocked incident asserted `is_blocked=false, completion_declared=true` → exit 1: `is_blocked: asserted=False actual=True; completion_declared: asserted=True actual=False`.
- **Fraud (failure_reason):** payload with injected `failure_reason` key → exit 1: `forbidden collapse ... at root.failure_reason`.
- **Fraud (promotion):** unresolved hypothesis asserted promotable → exit 1: `PermissionError: hypothesis h-auth-cause is unresolved`.
- **Fraud (blocker):** unestablished blocker asserted acceptable → exit 1: `ValueError: blocker b-mystery has no establishing evidence`.
- **Fraud (single witness):** single-witness proposition asserted SUPPORTED → exit 1: `asserted=SUPPORTED actual=UNDETERMINED`.
- **Fraud (partial completion):** one-of-two blockers repaired, completion asserted → exit 1: `completion_declared: asserted=True actual=False`.
- **Honest:** sharpest case with exact asserted verdict → exit 0 PASS. Cold-successor → exit 0.
- **Sabotage:** neutered (blind) analyzer → canary C1 fails → exit 2; corrupt/missing manifest → exit 2; tampered incident bytes → exit 2 (or 1, never 0).

## Failure mode if the wiring breaks

- Workflow deleted/disabled → the gate never runs: detectable via the receipt (this file) + the manifest's `_comment` naming the workflow. Verify-still-connected: `gh-api GET /repos/SoulSchoolAcademy/NayaPOWER/actions/workflows` lists `d31-incident-claims-gate.yml`; the check must appear on every PR touching the six watched paths.
- Manifest edited to assert dishonest claims → the gate exits 1 and blocks the PR (that IS the enforcement).
- Mechanism drift (vocabulary change) → the gate's import-time vocabulary identity check fails closed (exit 2), never silently.

## Boundary

CI governance path only. Runtime kernel/KNOW/LAW/ACT wiring needs Shawn's word per the mechanism's own docstring. Merge order: #2202 → #2211 → this wire; the merge lane owns the order. No merge from the wire lane.

## Verify it's still connected

1. `python tools/d31_incident_claims_gate.py` → `D31-GATE DORMANT` (exit 0) on the shipped manifest.
2. `python -m pytest tests/test_d31_incident_claims_gate.py -q` → 18 passed.
3. On GitHub: the `d31-incident-claims-gate` check is green on the wire branch's clean tree and red on a temp fraud commit (L215 both-directions proof in the run log).
