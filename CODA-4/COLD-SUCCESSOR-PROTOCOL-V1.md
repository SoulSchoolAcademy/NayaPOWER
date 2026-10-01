# Cold-Successor Retrieval & Continuity Protocol V1

**Seat:** Coda 4 · **Human Director:** Shawn Vibert (final authority)
**Scope:** retrieval, reconstruction, applicability, continuity, human usability
**Not in scope:** `naya_kernel/**`, `kernel/**`, persistence adapters, migrations,
calculator conformance (Coda 1), execution/handoff failure testing (Coda 2),
spec qualification (Coda 3).

**Candidate baseline:** PR #1216 head `f58adf0826e0ea2c96d6e4a781b5191d2f4b8d5b`,
base `main` `a726a8376559609a3620f948ec7bfcabdba50abb`. #1216 is an open
**draft**, unmerged, unratified. Nothing in this protocol is production proof.

---

## 0. The contract this executes

This is not an invented acceptance bar. It is the cold-successor clause already
ratified into the activation package:

- `NAYA-ACTIVATION/COLD-GITHUB-BOOTSTRAP-ACCEPTANCE-V1.md` — *"Cold-successor
  acceptance"* (ten questions; *"Success requires durable-state reconstruction and
  evidence/claim distinction."*)
- `NAYA-ACTIVATION/INTELLIGENCE/CONTINUITY.md` — *"Continuity is behavioral…
  A document saying continue here is not proof."*
- `NAYA-ACTIVATION/INTELLIGENCE/LEARNING.md` — *"A later authorized Naya must be
  able to obtain the lesson without the predecessor handing it over, recognize
  applicability, change behavior and leave evidence."*
- `NAYA-ACTIVATION/CURRENT-REALITY/SOURCE-PRECEDENCE-...-2026-09-29.md:86` — the
  recorded next action is already *"Run one genuinely cold Naya… require a
  durable activation receipt answering the ten cold-start questions, then have
  a second cold Naya independently reconstruct that receipt."*

## 1. Existing seams only — no new store

| Step | Existing callable seam |
|---|---|
| decision | `Kernel.decide(state)` — `naya_kernel/kernel.py:338` |
| receipt verify | `verify_decision_receipt(receipt)` |
| kernel continuity | `Kernel.cold_reconstruct(receipts)` — `kernel.py:479` |
| durable knowledge | `KnowNode.cold_reconstruct(receipts)` — `know_node.py:1362` |
| governed retrieval | `KnowNode.retrieve(query, principal)` — `know_node.py` |
| provenance | `KnowNode.cite_provenance(block_id)` |
| handoff seal | `EvolveNode.build_successor_package(fields)` — `evolve_node.py:1212` |
| successor boot | `SelfNode.gate(state)` w/ `successor_package` — `self_node.py:243` |

Receipts on disk are the persistence medium. There is no second store: the
predecessor writes receipts, the successor reads *only* receipts.

## 2. Isolation honesty

The successor in Step 3 receives **only**: the receipt files on disk, the
canonical contracts in the repo, and its own task statement. It does **not**
receive the builder's conclusions, chat, notes, or a prepared answer.

This is **process-level and in-repo isolation, not a fully independent cold
agent.** The protocol script is mine, so the harness is known to me. What is
genuinely tested is whether *durable evidence alone* suffices to reconstruct and
continue — which is the actual acceptance target. Cross-process durability in a
separate OS process is explicitly **out of scope here and not claimed** (the
existing handoff test states the same boundary); the receipts are written to
disk and re-read in a new process, but node state is rebuilt in-process.

## 3. Behavioral-reuse predeclaration

Predeclared **before** running, so success cannot be rationalized after the fact.

| Field | Value |
|---|---|
| **Lesson / evidence id** | `PROV-BEFORE-APPLY-1` — realized as the frozen lesson string in `LEARNING_REF` below, carried in `learning_refs` of the successor package and served by `KnowNode.retrieve` |
| **Applicable task** | successor must `cite_provenance(block_id)` **before** treating a retrieved block as current truth |
| **Expected observable behavior** | provenance citation recorded and block traceable; `citation_before_apply == True` |
| **Unrelated-task control** | a *different* retrieval whose lesson is `UNRELATED-REF-1` must **not** trigger provenance-before-apply attribution, and must not be reported as the applied lesson |
| **Authority requirement** | none — retrieval and citation are read-only. The successor must **refuse** any consequential action |
| **Success** | applicable task: cited before applying. Unrelated task: not attributed. No authority inherited. |
| **Failure** | applies without citing; cites the unrelated lesson; treats retrieval as permission; claims production proof |

**Causal-improvement bar.** Varying access to the intelligence is the *only*
variable; task, inputs, authority, and measurement are held constant. Even if
the successor cites provenance, that is **not** a performance improvement
claim — it is a *retrieval-and-applicability* result. No speed, quality, or
success-rate delta is claimed from a single-run demonstration.

## 4. Steps

1. **Decide** — `Kernel.decide` over a PASSing demo state; keep the decision receipt.
2. **Execute + persist** — ACT `execute()` → KNOW `ingest()`; keep the ingest receipt.
3. **Cold-successor retrieval** — fresh `KnowNode` built by `cold_reconstruct`
   from receipts *only*; assert store hash matches cycle 1; `retrieve()` the
   block; `cite_provenance()`.
4. **Reconstruct** — answer the ten cold questions **from retrieved evidence
   and repo contracts**, classifying VERIFIED / CANDIDATE / BLOCKED / UNKNOWN.
5. **One next action** — read from the sealed successor package; the successor
   confirms it and states its verification + preservation route. It does **not**
   execute it: no authority is transferred.
6. **Negative controls** — stale evidence, unrelated lesson, authority
   inheritance, unverified learning, concealed missing evidence, production
   overclaim.
7. **Preserve** — successor writes a successor receipt through the existing seam.
8. **Second cold reread** — a *fresh* `KnowNode`/`SelfNode` reconstructs the
   improved state from the successor's own receipts and recovers the same
   truth + next action.

## 5. Five labels kept separate

These are never collapsed, per `AGENTS.md` TRUTH/PROOF:

| Label | What it would take | Status here |
|---|---|---|
| **Document recovery** | successor reads files | PROVEN (steps 3–4) |
| **Runtime retrieval** | successor rebuilds state from receipts, hash-verified | PROVEN (steps 3, 8) |
| **Behavioral reuse** | preserved lesson changes observable behavior | PROVEN within stated scope (step 3 + control) |
| **Causal improvement** | controlled A/B, only intelligence varies | **NOT CLAIMED** — single run, no A/B |
| **Production proof** | ratified, merged, deployed, runtime-observed | **NOT CLAIMED** — #1216 draft; contract seam unagreed |

## 6. Honest blockers

### CS-01 — cold start does not populate the node (BLOCKS the core acceptance)

`KnowNode.cold_reconstruct` builds into a **local** `fresh = KnowNode()`
(`naya_kernel/nodes/know_node.py:1372`) and never assigns `fresh.blocks` /
`fresh._hash_index` back to `self`. Measured at `f58adf08`:

```
report["restored_block_count"] = 1      # the report says one block
report["store_hash"] == cycle1 hash     # the hash matches, exactly
successor.blocks                      = 0 # but the node is EMPTY
successor.retrieve(...)["blocks"]       = [] # nothing is retrievable
```

The receipt-hash contract is honored while the **usable state is absent** — a
green receipt over an empty store. This is `IMPLEMENTED != VERIFIED` in the
exact form `AGENTS.md` warns about.

Naya 4's `test_act_to_know_handoff_write_and_retrieve` asserts the **hash** but
never retrieves from the reconstructed node, which is why the gap is invisible
there. It is not a test bug; it is an untested seam.

**Consequence for this protocol:** acceptance step 3 ("a cold successor
*retrieves* the preserved evidence") is **BLOCKED**, not met. Steps 4–8 that
depend on it are blocked with it. The retrieval/applicability evidence in
`tests/test_coda4_cold_successor.py` therefore runs against the **cycle-1 live
store** and is labeled as such in the test docstrings — it is not presented as
cold continuity.

The two affected tests are `xfail(strict=True)`: they document the current
failure and will **XPASS → fail the run** once CS-01 is fixed, forcing this
protocol to be updated to the verified state instead of going stale.

Owner: **Naya 4** (`naya_kernel/` — not Coda 4's lane; not fixed here).

### Other blockers

- PR #1216 is a **draft**; the receipt/lineage interface (`naya-receipt-contract/1`)
  is **proposed, not agreed** (#1182, awaiting Naya 4). This protocol uses the
  kernel's own receipt shape and does not depend on the unagreed contract.
- **`core.autocrlf` defect** (Coda 4, routes to Naya 4): with a CRLF checkout
  and no `.gitattributes`, `node_base.v21_executable_status()` reports MISMATCH
  against the ratified calculator pin and EVOLVE fails closed. Any cold clone on
  Windows hits this at its first scoring decision.
- The unrelated-task control runs in-process against the same node objects: a
  genuine control for *attribution*, not a second environment.
- Cross-process durability in a separate OS process is **not attempted here**,
  matching the boundary Naya 4's own test docstring states.

## 7. Reproduce it

```powershell
git clone --branch coda4/cold-successor-continuity https://github.com/SoulSchoolAcademy/NayaPOWER.git
cd NayaPOWER
git config core.autocrlf false      # required, see the autocrlf defect above
python -m pytest tests/test_coda4_cold_successor.py -q
```

Expected on the current candidate: **18 passed, 2 xfailed** (the two xfails are
CS-01). The xfails turning into XPASS means CS-01 was fixed and this protocol
needs updating.

To see the CS-01 mechanism directly:

```python
import json, sys; sys.path[:0] = ["tests", "."]
from naya_kernel.nodes import know_node
kn = know_node.KnowNode()
succ = know_node.KnowNode()
report = succ.cold_reconstruct(receipts)   # from a real predecessor cycle
print(report["restored_block_count"], len(succ.blocks))   # 1  0
```

## 8. Human reading of the demonstration

> **Here is the task.** One cold successor must recover preserved work.
> **Here is what Naya used.** Receipts on disk; nothing else.
> **Here is what she did.** Rebuilt state from receipts, hash-checked, then
> retrieved through the governed seam with provenance cited first.
> **Here is the verified result.** Hash-identical store, sealed handoff, refusal
> to inherit authority, six negative controls held.
> **Here is what the next Naya recovered.** Everything above — and, honestly,
> the fact that cold-start **retrieval** is still blocked by CS-01, which is
> itself the most useful thing this protocol found.
