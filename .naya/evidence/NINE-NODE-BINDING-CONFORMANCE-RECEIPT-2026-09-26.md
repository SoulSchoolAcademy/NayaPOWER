# Nine-Node Kernel — Binding Conformance Action Receipt

**Status:** EXECUTED / FINDINGS OPEN — not self-ratified, not landed
**Actor:** Coda 2 (black-box test node)
**Base HEAD:** `6e5e8509a59c844b8e148fcda996b70a91e8c97f` (`main`, 2026-09-26T18:34:20-07:00)
**Kernel:** `.naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json` v1.0 `RATIFIED_BASELINE`

## Intent
Prove whether the nine-node kernel binds to real canonical artifacts, not merely to itself.

## Authority
Read-only diagnostic. Does not mutate the kernel, contracts, control plane, or production.
Adding this gate to CI would turn the kernel pipeline RED and is therefore an authority
decision, not a machine decision. Not self-authorized.

## Action
Added `scripts/verify-nine-node-contract-binding.py` (local clone only, unlanded).
Ran it plus three negative controls.

## Result
| Check | Expected | Actual |
|---|---|---|
| Static kernel gate on main | PASS | PASS |
| 12 kernel mutations rejected | 12/12 | **12/12** |
| Kernel contract bindings resolve | 27/27 | **10/27** — 17 unbound |
| MN-07 / MN-08 / MN-09 real bindings | >0 | **0** — all three own only phantom contracts |
| My gate: fully-bound fixture | GREEN | GREEN |
| My gate: contract 17 deleted | RED | RED (after fixing my bug) |
| My gate: duplicate contract 07 | RED | RED |

## Verification state
`PROVEN` — the unbound-binding finding, reproducibly, with a gate that fails on both sides.
`NOT PROVEN` — any runtime behavioral effect of the nine Nodes.

## Defect found in my own work
First version of the binding gate used `git ls-files` and passed a fixture where contract 17
had been deleted, because the git index still listed it. Fixed to require the file to exist on
disk. My negative control caught my bug; the audited gate's negative controls did not catch
its equivalent.

## Next action
A human must decide the contract-id binding for MN-07/08/09: ratify the missing contracts
11–26, or rebind those Nodes to real contract ids. Until then the kernel is structurally valid
and semantically unbound.
