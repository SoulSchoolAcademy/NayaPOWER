# Nine-Node Genome — Acceptance Matrix V1

| Gate | Question | Required evidence |
|---|---|---|
| G1 Contract | Is the job unambiguous? | versioned contract + schema |
| G2 Identity | Is runtime bound to canonical identity? | manifest + runtime binding |
| G3 Inputs | Are trusted inputs explicit? | schema + negative tests |
| G4 State | Are transitions bounded? | state-machine tests |
| G5 Authority | Is permission external to intelligence? | LAW receipts + denial tests |
| G6 Provenance | Can claims trace to origin? | provenance chain |
| G7 Runtime | Does the real application invoke it? | runtime receipt |
| G8 Influence | Did invocation change behavior? | ablation/before-after evidence |
| G9 Outcome | Did the intended result occur? | observation evidence |
| G10 Verification | Is the result independently evidenced? | verification receipt |
| G11 Learning | Did verified experience change later behavior? | holdout behavioral delta |
| G12 Compounding | Did later comparable work improve? | controlled comparison |
| G13 Succession | Can a cold Naya continue? | successor replay |
| G14 Security | Do boundary/adversarial tests pass? | security suite |
| G15 Reliability | Does it survive failure/retry/concurrency? | reliability evidence |
| G16 Performance | Does it meet declared budgets? | p50/p95/p99 report |
| G17 Observability | Can another engineer reconstruct it? | receipts/logs/evidence |
| G18 Production | Is the actual production boundary proven? | production receipt + independent verification |

## Scoring law

Each gate is NOT_PROVEN, PARTIAL, PASS, or NOT_APPLICABLE with evidence. Numeric scores may summarize maturity but may never hide a critical gate failure.

AAA cannot be claimed while G7–G13 are unproven.

## Audit protocol

1. Read the node contract.
2. Locate the exact implementation.
3. Map every required function to code.
4. Run positive and negative tests.
5. Capture real receipts.
6. Inspect evidence independently.
7. Set status only to the highest state supported by evidence.
8. Record remaining gaps.
9. Hand the exact next action to the successor.