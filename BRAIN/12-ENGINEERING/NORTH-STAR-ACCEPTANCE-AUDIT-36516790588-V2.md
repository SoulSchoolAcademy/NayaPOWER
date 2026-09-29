# NayaPOWER — North-Star Acceptance Audit v2

**Historical acceptance run:** `36516790588`  
**Acceptance source revision:** `c9b31890c93f4f5f7d60bb8cd346093c11ab427f`  
**Historical checkpoint:** `a58dc3f0-5968-43dc-98ad-c31930777096`  
**Target learning:** `65b93cdb-3981-4504-badd-a38861ffb971`

## Result

**Checkpoint hole: CLOSED. Full North-Star acceptance: STILL OPEN because one previously identified independent-corroboration gap remains.**

### What changed

An immutable `public.nayanet_checkpoint_receipts` evidence ledger was created and backfilled from the canonical revision-800 intelligence-commit receipt and the target learning record.

The historical checkpoint is now independently reconstructable without depending on the mutable `nayanet_project_cognition_state` row.

Verified persisted checkpoint:

- checkpoint: `a58dc3f0-5968-43dc-98ad-c31930777096`
- revision: `800`
- project: `NayaNET`
- owner: `adfdf0b8-5558-41d1-9fed-ec51abf4fe2f`
- learning: `65b93cdb-3981-4504-badd-a38861ffb971`
- event: `aa735543-4f00-45ec-a9db-9bd6055e24d9`
- Intelligent Block: `IB-NAYA-FLOW-LESSON-7ccdf73c3c0049b4812599c28ba74386`
- lineage: `c7401602-90ee-4e8d-ae16-c34f3e4e9aa0`
- relationship: `cb5cc82a-c4a1-41cf-ad33-aceffbc10004`
- index: `ce6f92cb-5aa4-4b92-bcf7-0d8e67b91f53`
- source receipt: `32ff7884-e44b-46fc-84d2-682cd6f00161`
- checkpoint content hash: `f7be51315efdbbb46005e3ea61c2d91a1e839c1aed8626b11d73f1a5354c5071`

The stored content hash was independently recomputed from the canonical fields and matched exactly.

The database trigger `nayanet_checkpoint_receipts_immutable` is active for UPDATE and DELETE, making the historical receipt append-only/immutable at the database layer.

The live mutable cognition-state row has subsequently advanced to revision 834, demonstrating why the historical receipt must be object-local rather than relying on the mutable current-state row.

## Original 36516790588 reconstruction

The previous audit independently verified all 18 completed jobs and all 16 persisted artifacts. Artifact SHA-256 digests matched GitHub metadata. The persisted evidence independently supported:

- canonical Naya identity and owner binding
- OIDC identity separation
- deployed runtime/source revision parity for the historical run
- fresh intelligence persistence
- Event → Intelligent Block → Lineage → Relationship → Index → Learning
- causal control/treatment behavioral change
- independent causal recomputation
- promotion and retained-learning reread
- cold successor reconstruction
- no caller-supplied intelligence content
- no inherited successor authority
- related-task reuse
- unrelated-task refusal
- graph-context behavioral change
- independent graph recomputation

The checkpoint durability caveat from v1 is now closed by the immutable historical receipt.

## Remaining independent-evidence gap

The causal control/treatment execution receipt IDs:

- `5b072812-699f-415d-b759-2ed509c36367`
- `109944fc-9868-45e3-a532-f40952aea3a1`

still have **zero rows in `nayanet_execution_outcomes`**.

The causal result remains independently reconstructable from:

- the two persisted execution receipts,
- the target learning evidence,
- the source event,
- the Intelligent Block,
- lineage,
- relationship,
- index,
- and independent causal-verification artifact.

But there is no second persisted execution-outcome ledger entry for those exact executions. Therefore the North-Star acceptance remains OPEN under the existing evidence contract.

## Acceptance disposition

**Checkpoint durability = independently VERIFIED.**

**North-Star acceptance = OPEN.**

No acceptance semantics were changed. No second intelligence store was introduced. The new table is an evidence/provenance ledger for historical checkpoint reconstruction, not a second brain.

## Canonical next action

**Create or recover the immutable execution-outcome records for the exact causal control/treatment receipts, independently recompute them from persisted state, and rerun this same North-Star audit.**
