# Nine-Node Kernel Conformance — Evidence Receipt

**Status:** EXECUTED / RED — findings open, not self-ratified, not landed
**Actor:** Coda 2
**Base HEAD:** `6e5e8509a59c844b8e148fcda996b70a91e8c97f` (`main`, 2026-09-26T18:34:20-07:00)
**Authority:** Human Director North Star directive 2026-09-26. Read-only diagnostics. No production, no constitutional mutation, no N9 implementation change.

## Finding 1 — The nine-node kernel has three sources of truth and no reconciliation

| Source | Status | What it says the nine Nodes are |
|---|---|---|
| `NAYAPOWER-SYSTEM-NORTH-STAR-WHITE-PAPER-...-V1.md` §8 | RATIFIED, merged | 01 Constitution/Mission/Scope … 09 NayaNET Architecture/Hub/Production Proof |
| `NAYA-MASTER-NODE-KERNEL-V1.json` | `RATIFIED_BASELINE`, merged, deployed as `IB-001233..IB-001241` | MN-01 SELF … MN-09 EVOLVE |
| `nayanet-compound-intelligence/index.ts:73-96` | live runtime | hardcodes `MASTER_NODE_KEYS`, rejects any positional key mismatch |

**Direct collisions at ordinals 02 and 09.** The runtime enforces the *kernel's* semantics
positionally. A Naya that reads the ratified strategic model and acts on it is **rejected by
the live kernel boot gate**. Neither artifact is wrong on its own; together they are a silent
semantic fork of the system's semantic foundation.

This is the exact condition white paper §46 forbids: *"The system must not silently pretend
its operating model is intact."*

## Finding 2 — The kernel is 63% unbound to real artifacts

- `scripts/verify-nine-master-nodes.py` → **PASS**, and **12/12 mutation negative controls rejected** (the shipped gate genuinely can fail).
- But it validates the kernel **against itself only**.
- **10 of 27** contract bindings resolve to an artifact on disk.
- **16 contracts (11–26) have no artifact.** Contract `00` is **AMBIGUOUS** (two artifacts — independently re-confirms the `00-` id collision).
- **MN-07 VERIFY, MN-08 LEARN, MN-09 EVOLVE own only phantom contracts.**
- `verify-nine-master-node-kernel.yml` runs only the static gate plus a unittest, so **CI cannot detect this**.

## What was built

| Artifact | Purpose | Result on main |
|---|---|---|
| `scripts/verify-nine-node-contract-binding.py` | Does every kernel-owned contract resolve to exactly one artifact? | **RED** — 10/27 bound, 17 unbound |
| `scripts/verify-master-node-semantic-conformance.py` | Do the three ratified sources agree, with a declared reconciliation? | **RED** — reconciliation ABSENT |
| `scripts/verify-nine-node-kernel-controls.py` | 12 mutation negative controls on the shipped gate | 12/12 rejected |
| `scripts/verify-nine-node-semantic-controls.py` | 7 positive/negative controls incl. GREEN path | 7/7 as specified |

## Defect found in my own work

The first version of the binding gate reported a deleted contract as BOUND, because
`git ls-files` reports the git index rather than the filesystem. My negative control caught it.
Fixed. The shipped kernel gate's negative controls would **not** have caught its equivalent,
because every one of them mutates the kernel and none removes a real-world artifact.

Boundary documented: the gate reads the **committed** tree, so an untracked competing artifact
is invisible to it.

## Verification state

- `PROVEN` — both findings, reproducibly, by gates that demonstrably fail and demonstrably pass.
- `NOT PROVEN` — any runtime behavioral effect of the nine Nodes. Nodes are owner-private; no
  credentials were available, so `kernel_boot` was never executed.

## Not done, deliberately

- Did not author `NAYA-MASTER-NODE-SEMANTIC-MAPPING.json`. Writing it would be deciding what the
  nine Nodes mean, which is a ratification I am not authorized to perform. The gate requires it
  and fails closed until a human supplies it.
- Did not commission contracts 11–26 or rebind MN-07/08/09. Same reason.
- Did not turn the kernel CI pipeline RED on `main`; that is an authority decision.

## Next action

A human must supply the semantic mapping and decide the contract binding for MN-07/08/09.
Until then: the kernel is structurally valid, internally self-consistent, and semantically forked.
