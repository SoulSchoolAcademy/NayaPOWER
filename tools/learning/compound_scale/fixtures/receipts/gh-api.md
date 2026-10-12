# Pinned truth-gate evidence fixture — gh-api (t0292 hermeticity fix)

Provenance: 2026-10-12, Lane 9 (Naya Smith). Replaces the pre-hermetic
`~/workspace/naya/bin/gh-api` receipt_file path, which did not exist on CI
minimal VMs (gate returned 0 = "receipt file missing").

The quoted lines below are captured VERBATIM from the gh-api usage
contract. This file is FROZEN: the truth gate asserts verbatim quote
presence, so edits here change what lessons L1, L2, and A1 can prove.

## L1 / L2 — gh-api JSON body contract

usage: gh-api METHOD PATH [BODY_JSON | --body-file PATH]

--body-file PATH: read the JSON body from a file

## Flag order

Flags go AFTER method and path:

if rest and rest[0] == "--body-file":
    path = rest[1]

## A1 — adversarial probe (must_contradict)

The A1 contradiction evidence: `read the JSON body from a file`
