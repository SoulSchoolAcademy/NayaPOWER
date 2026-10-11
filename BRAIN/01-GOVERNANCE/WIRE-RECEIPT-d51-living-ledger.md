# WIRE RECEIPT — D51 living-ledger contract gate (2026-10-11, Naya 2 wire lane)

**Plain words:** Shawn's living-ledger vision got its first working machinery today
(`living_ledger/receipt.py` + `living_ledger/chain.py`, PR #2333) — receipts that
refuse to exist without evidence, and a verifier that re-computes every link of the
hash chain. Built and tested, but connected to nothing. This wire puts that
machinery on the CI path: any PR touching the ledger package must preserve its
contract, or the PR is blocked.

## What was wired

- Mechanism: D51 first slice — `LivingReceipt` (fail-closed envelope) and
  `verify_chain` (hash-chain verifier). Source: PR #2333, build-lane sign-out
  #2175/6108274346. The build lane's own doc (`BRAIN/01-GOVERNANCE/D51-LIVING-LEDGER-V1.md`)
  declares it CODE-ONLY and names wiring as the wire lane's call.
- Gate: `tools/d51_living_ledger_gate.py` — re-proves the contract on the live tree.
- Tests: `tests/test_d51_living_ledger_gate.py` — 10 tests incl. 3 sabotage
  negative controls and fail-closed loader paths.
- Workflow: `.github/workflows/d51-living-ledger-gate.yml` — the enforcement wire.

## Operating path now protected

The PR merge path for the living-ledger package.
- **Trigger:** any PR touching `living_ledger/**` (or the gate/workflow itself);
  also fires on push to main for those paths.
- **Block:** the `d51-living-ledger-gate` check goes red (exit 1) and the PR
  cannot merge under the standing merge protocol.
- **Defect class it catches:** a change that weakens receipt construction
  (accepts evidence-less receipts, bad scopes, malformed timestamps) or that
  neuters the chain verifier (lets a forged hash, dropped link, or regressed
  sequence pass silently).

## Proof (wire-lane standard)

Fire battery on the combined tree (#2333 head + this wire), Python 3.11
(the CI version — local is 3.12):

| Probe | Expected | Observed |
|---|---|---|
| Valid receipt + 3-event chain via `to_ledger_params` seam | PASS, CHAIN_VALID | PASS (30 checks) |
| Forged `event_hash` | HASH_MISMATCH @1 | HASH_MISMATCH @1 |
| Wrong `previous_chain_hash` | LINK_BROKEN @2 | LINK_BROKEN @2 |
| Dropped event (0 → 2) | LINK_BROKEN @1 | LINK_BROKEN @1 |
| Non-increasing `chain_seq` | SEQ_REGRESSION @2 | SEQ_REGRESSION @2 |
| Empty list | EMPTY_CHAIN, not a pass | EMPTY_CHAIN, not ok |
| 13 invalid receipt shapes | all raise ValueError | all raise |
| Sabotage: evidence check removed | gate exit 1 | exit 1, names evidence |
| Sabotage: `verify_chain` always-CHAIN_VALID | gate exit 1 | exit 1 |
| Sabotage: `canonical_event_hash` constant | gate ≠ PASS | exit 1 |
| Corrupt mechanism (SyntaxError) | exit 2 fail-closed | exit 2 |
| Contract surface removed | exit 2 fail-closed | exit 2 |
| Mechanism absent (pre-merge tree) | DORMANT exit 0 | DORMANT exit 0 |
| Gate test suite | 10/10 | 10/10 |
| Mechanism's own tests (dogfood) | green | green |

## Failure mode if the wiring breaks

- If the workflow file is deleted or its `paths:` filter narrowed, PRs touching
  the ledger stop being judged — detect via the quarterly workflow audit; the
  gate file itself remains runnable by hand (`python3 tools/d51_living_ledger_gate.py`).
- If the gate is neutered to always exit 0, the sabotage tests fail — the
  workflow runs the gate's test suite on every trigger, so a neutered gate
  cannot pass its own suite.
- If the mechanism is deleted from the tree, the gate reports DORMANT —
  explicit, never a false green.

## How to verify it's still connected

1. Open any PR touching `living_ledger/**` — the `d51-living-ledger-gate`
   check must appear and be green.
2. Temporarily break one receipt rule in the PR (e.g. allow empty evidence) —
   the check must go red naming the break; revert before merge.
3. `python3 tools/d51_living_ledger_gate.py` on the tree must print
   `D51-GATE PASS` (or `DORMANT` on a pre-mechanism tree).

## Boundary

CI governance path only. The gate judges the mechanism's contract; it
authorizes nothing and writes nothing. `to_ledger_params` builds the
stored-procedure call — execution stays behind the human-only database gate
per the mechanism's own docstring. Runtime wiring into kernel/, KNOW, LAW,
or ACT still needs Shawn's word.
