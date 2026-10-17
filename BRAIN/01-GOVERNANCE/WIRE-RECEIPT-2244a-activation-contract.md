# WIRE RECEIPT — #2244 req 1 worker activation-contract gate

**Directive:** #2244 req 1 / sequence A (machine-checkable wake/activation contract), owner Naya 2.
**Mechanism:** `tools/activation_contract.py` @ PR #2309 head `c0eca633cdd24a697ec678516199a8c3f6e91a84` — was CODE-ONLY (20/20 unit tests green on the head, zero live consumers: nothing invoked the verifier on any operating path).
**Wire PR:** `naya2/wire-2244a-activation-contract` → base `naya2/activation-contract-2244-req1` (stacks on #2309). Additive-only: 3 new files, zero mechanism changes.
**Date:** 2026-10-11 (night shift, WIRE lane, Naya 2's team).

## What it wires

`tools/activation_contract.py` verifies a worker's ActivationClaim against bytes recomputed from the live tree plus an independently-supplied live tip: fresh main SHA, mission-state and protocol byte-faithfulness, nine canonical specialty feeds, feed sign-in evidence (marked CLAIMED-UNVERIFIED — the gate never pretends the sign-in landed), live board #2175 ack, archive board #1354 rejection, TOC #1599 ack. Any failure → STAND_DOWN.

## Operating path

`.github/workflows/activation-contract-gate.yml` — runs the mechanism's unit tests (20, incl. sabotage negative controls) + the live violation drill (`tools/activation_contract_gate_drill.py`), on `pull_request` and `push`-to-`main` for the eight watched paths (verifier, drill, contract drafts, schema, unit tests, this receipt, workflow).

SCOPE NOTE: this is the WORKER orientation contract. It does not touch the Naya issuance/mint activation gates (`unified-activation-gate.yml`, `activation-delivery-gate.yml`, `activation-mint.yml`) — different mechanism, different path, no duplicate.

## Proof a real violation gets blocked

Drill battery against the REAL CLI on live bytes (local, then CI):
- **GREEN (honest):** well-formed claim built from the live tree's actual hashes, live tip = `git rev-parse HEAD` → exit 0 PROCEED.
- **DRIFT:** one appended byte in the protocol artifact (claim carries the TRUE hash) → exit 1 STAND_DOWN `PROTOCOL_DRIFT`.
- **STALE_SHA:** claim main SHA = 40 zeros → exit 1 STAND_DOWN `STALE_SHA`.
- **STALE_BOARD:** board ack naming #1354 as the live board → exit 1 STAND_DOWN `STALE_BOARD`.
- **UNKNOWN_FEED:** feeds_read containing feed 9999 → exit 1 STAND_DOWN `UNKNOWN_FEED`.
- **Sabotage:** verifier with the drift check neutered → DRIFT case PROCEEDs → drill exits 1 (wire-broken). The drill cannot pass on a blind verifier.

## Failure mode if the wiring breaks

- Workflow deleted/disabled → the gate never runs: detectable via this receipt + the drill's header naming the workflow. Verify-still-connected: `gh-api GET /repos/SoulSchoolAcademy/NayaPOWER/actions/workflows` lists `activation-contract-gate.yml`; the check must appear on every PR touching the eight watched paths.
- Verifier weakened (a check removed) → the drill's corresponding violation case PROCEEDs → drill exits 1 and blocks the PR (that IS the enforcement).
- Canonical constants changed (boards/feeds) without governance → unit test `test_canonical_feeds_are_the_nine_ratified` and board-ack tests fail → check red.

## Boundary

CI governance path only. Runtime wiring — invoking the verifier inside `tools/worker_entry.py` at worker shift start — is designed but NOT built: workers do not yet produce ActivationClaims, so a runtime gate would invent an operational requirement. Handed to the build lane as the next step; the merge lane owns merge order (#2309 → this wire). No merge from the wire lane.

## Verify it's still connected

1. `python3 tools/activation_contract_gate_drill.py` → `WIRE_PROVEN` (exit 0).
2. `python -m pytest tests/test_activation_contract.py -q` → 20 passed.
3. On GitHub: the `2244-A Activation Contract Gate` check is green on the wire branch's clean tree; the drill's violation cases prove the red direction on every run (L215 both-directions proof in the run log).
