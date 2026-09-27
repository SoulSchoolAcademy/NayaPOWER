# Decision Brief — Nine Master Node Semantic Ratification

**Status:** AWAITING HUMAN RATIFICATION — nothing here is decided
**Base:** `6e5e8509` (`main`) · **Prepared by:** Coda 2 · **Blocks:** every Coda job that depends on "what the nine Nodes mean"
**Instrument:** `.naya/specifications/NAYA-MASTER-NODE-SEMANTIC-MAPPING.json`
**Schema:** `.naya/specifications/schemas/NAYA-MASTER-NODE-SEMANTIC-MAPPING-V1.schema.json`

---

## 1. Why this is blocked

Three ratified artifacts define the same nine ordinals and do not agree. The live runtime
(`supabase/functions/nayanet-compound-intelligence/index.ts:73-96`) hardcodes `MASTER_NODE_KEYS`
and **rejects** any positional mismatch. A Naya that follows the strategic model is rejected by
the kernel boot gate.

| Source | Status | Defines the nine as |
|---|---|---|
| North Star white paper §8 | RATIFIED, merged | Constitution/Mission/Scope … NayaNET Architecture/Hub/Production Proof |
| `NAYA-MASTER-NODE-KERNEL-V1.json` | `RATIFIED_BASELINE`, merged, deployed `IB-001233..241` | SELF, LAW, ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE |
| `CANONICAL-CONTRACT-REGISTRY.md` | LIVE, merged | `CC-000`..`CC-027` (26 present; **CC-005 and CC-007 absent**) |

## 2. Per-ordinal comparison

| # | White paper §8 | Kernel (deployed) | Verdict |
|---|---|---|---|
| 01 | Constitution, Mission & Scope | MN-01 SELF — Identity, Mission & Continuity | PARTIAL |
| 02 | Identity & Continuity | MN-02 LAW — Authority, Consent & Governance | **COLLISION** |
| 03 | Execution & Authorization | MN-03 ACT — Execution, Agency & Safe Action | PARTIAL |
| 04 | Intelligence Atom | MN-04 KNOW — Intelligence, Memory & Events | PARTIAL |
| 05 | Provenance, Evidence & Ledger | MN-05 PROVE — Truth, Provenance & Accountability | PARTIAL |
| 06 | Retrieval, Applicability & Smart Links | MN-06 CONNECT — Relationships, Retrieval & System Context | PARTIAL |
| 07 | Verification, Safety & Governed Action | MN-07 VERIFY — Outcome, Causality & Acceptance | PARTIAL |
| 08 | Learning, Reconciliation & Compounding | MN-08 LEARN — Learning, Reconciliation & Prediction | PARTIAL |
| 09 | NayaNET Architecture, Hub & Production Proof | MN-09 EVOLVE — Continuity, Experience & System Evolution | **COLLISION** |

## 3. The contract taxonomy question (the part that is easy to get wrong)

The kernel's contract keys are bare `"00".."26"` — the **director's 27-area list**. The registry
uses `CC-000..CC-027`. These are **not** the same scheme.

**Tested hypothesis:** kernel key `NN` == `CC-0NN`, so rebinding is mechanical.
**Result: incoherent for 9 of 9 nodes.** Eight score **0.00** domain overlap. Examples:

| Node | Declared | Would inherit under a CC rebind | Overlap |
|---|---|---|---|
| MN-02 LAW | Authority, Consent & Governance | Identity & Continuity; Causal Verification; Production Parity | 0.00 |
| MN-05 PROVE | Truth, Provenance & Accountability | Smart Ledger; Refusal/Revocation/Replay | 0.00 |
| MN-08 LEARN | Learning, Reconciliation & Prediction | Portable Authorization; Verification & Acceptance; Cold Successor | 0.00 |
| MN-09 EVOLVE | Continuity, Experience & System Evolution | Ratification/Release; Learning Loop; NayaNET Architecture | 0.00 |

**Therefore the kernel's contract ownership map is mis-specified, not merely unbound.** Rebinding
to CC ids would make it worse. This is the single most decision-relevant fact in this brief.

Two further holes, independently discovered:
- **`CC-005` and `CC-007` do not exist** in the registry — holes inside its own declared range.
- **`CC-027` (CI / Full-Suite Evidence) is owned by no Node.**

## 4. Decisions required (yours alone)

### D1 — Which source is canonical for the nine ordinals?
- **(a) `NORTH_STAR_WHITE_PAPER_SECTION_8`** — the strategic model governs. Consequence: the kernel JSON and the nine deployed Intelligent Blocks (`IB-001233..241`) must be re-keyed, and the runtime's hardcoded `MASTER_NODE_KEYS` must change.
- **(b) `MASTER_NODE_KERNEL_V1`** — the kernel governs. Consequence: the ratified white paper §8 must be amended to match, and the deployed Nodes need no change.
- **(c) `CANONICAL_CONTRACT_REGISTRY`** — the contract registry governs the *domains*, and the Node set is derived from it. Consequence: largest change; requires the CC taxonomy to be repaired first (CC-005, CC-007, CC-027).

### D2 — Which contract taxonomy do Nodes bind to?
- **(a) `KERNEL_00_26_AREAS`** — keep the director's 27-area list. Consequence: 16 areas must be authored as real contracts before MN-07/08/09 govern anything.
- **(b) `CC_000_027_REGISTRY`** — bind to the registry. Consequence: **proven incoherent as-is**; requires re-deriving every Node's ownership, plus repairing CC-005/CC-007/CC-027.
- **(c) `NEW_SINGLE_TAXONOMY`** — author one taxonomy that both the kernel and the registry adopt. Consequence: most work, but ends the three-way collision permanently.

### D3 — Contract binding for MN-07 / MN-08 / MN-09 *(the non-contending item)*
These three own **only** contracts that do not exist, and they are the Nodes that would verify
outcomes, force learning, and compound.
- **(a)** Author the missing contracts so the existing bindings become real.
- **(b)** Rebind MN-07/08/09 to contract ids that exist.
- **(c)** Mark the kernel's `contract_id_range` explicitly aspirational and require behavioural proof without contract backing until D2 lands.

## 5. How to ratify

Write `.naya/specifications/NAYA-MASTER-NODE-SEMANTIC-MAPPING.json` against the schema, setting:
`status: RATIFIED`, `canonical_source` (D1), `taxonomy_decision.selected_taxonomy` (D2),
nine `entries` with `agreement`, and a `ratification` block with a **human** `ratified_by`.

The schema refuses `status: RATIFIED` without a `ratification` block, and refuses any
`ratified_by` beginning `machine`, `naya`, `ai`, `agent`, `bot`, `system`, or `auto`.
`self_ratification_permitted` is `const: false`.

Then: `python scripts/verify-master-node-semantic-conformance.py` → **GREEN**.

**I did not write this file.** Authoring it means deciding what the nine Nodes mean, and the
schema is deliberately built so that a machine cannot do it and call it ratified.

---

## 6. PRECEDENCE EVIDENCE — D1 IS LARGELY DETERMINED, NOT FREE CHOICE

Newly established by inspection. This materially narrows the decision.

| Evidence | Finding |
|---|---|
| Commit order | White paper `3e68f14b` ratified **17:20:08**. Kernel `cb7887fe` activated **18:03:25** — 43 minutes later. The kernel is **not** an ancestor of the white paper commit. |
| Kernel's own declared authority | `NAYAPOWER-NINE-MASTER-NODES-ENFORCEABLE-SPEC-V1.md` L5: *"**Authority:** NayaPOWER System North Star + NayaNET Constitutional Contract Law"*, and L14: *"The nine Master Nodes are the semantic operating layer **compiled from that law**."* |
| Ratification record | `.naya/project-intelligence/NAYAPOWER-SYSTEM-NORTH-STAR-RATIFICATION-2026-09-26.md` L19: *"**Master Nodes** = semantic kernel."* — asserted, never enumerated. |
| Does the white paper know the kernel exists? | **No.** Zero occurrences of `MN-0`, `NAYA-MASTER-NODE-KERNEL`, `IB-001233`, `RATIFIED_BASELINE`, or `EVOLVE` in all 2,166 lines. |
| Does the white paper supersede it? | **No.** Its supersession rule covers prior *strategic plans*; it never names or carries the kernel forward. |
| AAA scorecard | `.naya/NAYAPOWER-SYSTEM-AAA-SCORECARD-V1.md` L101: *"GAP A — Semantic kernel is not yet the runtime kernel."* The gap is known; the enumeration mismatch is not recorded anywhere. |

### What this means

1. **The kernel is subordinate to the North Star by its own declaration.** It claims to be *compiled from* the North Star. A compiler that emits a different result than its source is a **defect in the compilation**, not a competing authority.
2. **The kernel is the later artifact and the acknowledged source of truth for the nine node identities** (the ratification record names them; the white paper never does).
3. Therefore **D1 is substantially answered by existing ratified evidence**: North Star §8 is the strategic source; `MN-01..MN-09` are the canonical *identities*; the kernel's *node names* are the defective compilation and should be corrected toward §8.

**What remains genuinely open:** whether to re-key the runtime (`MASTER_NODE_KEYS` is hardcoded and would have to change), D2 taxonomy, and D3 binding.

### Recommendation (a recommendation is not a ratification)

- **D1 → `NORTH_STAR_WHITE_PAPER_SECTION_8`** for the governing *domains*, retaining `MN-01..MN-09` as the stable *identities*. Correct the kernel's node names and the runtime keys toward §8. Evidence: the kernel's own subordination clause plus ratification order.
- **D2 → `NEW_SINGLE_TAXONOMY`.** Both existing taxonomies are provably defective: the CC rebind is incoherent 9/9, and the `00-26` map preserves 16 nonexistent areas. This is the most expensive option and that cost is real.
- **D3 → author the missing contracts** for MN-07/08/09, with the range marked aspirational until D2 lands. Rebinding those three to unrelated existing contracts would be a semantic lie; they are the Nodes that verify, learn and compound, which is the North Star's core claim.

## 7. A MACHINE-AUTHORED PROPOSAL NOW EXISTS

`.naya/specifications/NAYA-MASTER-NODE-SEMANTIC-MAPPING.json` is present with **`status: "PROPOSAL"`**, carrying the recommendation above, all nine ordinals, and **no ratification block**.

**The gate refuses to pass on it.** Verified:

```
- semantic mapping is status='PROPOSAL', not RATIFIED. A proposal authored by a
  machine may inform the decision but cannot satisfy this gate.
  Self-optimization must never become self-authorization.
```

This was a real hole in my own gate, found and closed: an earlier version would have
accepted a machine-authored proposal as satisfying conformance. Control
`machine PROPOSAL (no ratification) -> RED` now proves it cannot recur.

**To ratify:** edit the proposal — set `status` to `"RATIFIED"`, delete `proposal_note`,
and add a `ratification` block with your name. Then
`python scripts/verify-master-node-semantic-conformance.py` → **GREEN** (once D2's taxonomy
incoherence is also resolved, which no single edit can fix).
