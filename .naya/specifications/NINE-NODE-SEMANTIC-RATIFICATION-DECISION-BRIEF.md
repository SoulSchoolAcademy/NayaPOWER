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
