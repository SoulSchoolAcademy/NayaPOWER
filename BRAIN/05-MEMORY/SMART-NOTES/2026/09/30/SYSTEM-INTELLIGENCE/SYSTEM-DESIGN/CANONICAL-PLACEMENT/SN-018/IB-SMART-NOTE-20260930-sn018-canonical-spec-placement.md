# One Canonical Spec Per Node — The 0002 Placement Decision

**Intelligent Block:** IB-SMART-NOTE-20260930-sn018-canonical-spec-placement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-09-30
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-09-30 the two Naya lanes agreed on #554: each of the nine nodes gets exactly one canonical specification, at `BRAIN/03-KERNEL/NODES/<NODE>/0002-MASTER-SPEC-V1.md`. The 0001 contracts stay as thin contract summaries; the 0002s are the normative depth. The builder lane's branch-local `specs/` copies are working build input only — they retire as a parallel tree once their valid deltas return as amendment patches against the 0002s. PR #1224 (the verbatim PDF landings) does not merge until both lanes' corrections are folded in. The rule generalizes: never let a second normative lineage grow beside the canonical one; reconcile into it or retire the copy.

## 🩷 HUMAN NOTE

When two smart people write two versions of the truth, the answer is never "keep both." Pick the canonical address, make everything else feed into it or go away. Parallel truths are how teams slowly stop agreeing with each other.

## 🟣 CHILD NOTE

If there are two rulebooks, nobody knows which one counts. Keep one rulebook. If someone has a better rule, add it to the one rulebook.

## 🔵 GRANDMA NOTE

One recipe book in the kitchen. If someone improves a recipe, write it in the book — don't start a second book.

## 🟠 NAYA NOTE

A working copy is not a second canon. The moment a draft starts being treated as normative, you have two brains and zero agreement. Canonical address per node: the 0002. Everything else is input, and input retires.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "one_canonical_spec_per_node_at_0002_MASTER_SPEC_V1",
  "parallel_tree_policy": "working_input_only_retires_after_deltas_reconciled_as_amendments",
  "merge_gate": "PR_1224_blocked_until_both_lanes_corrections_folded_in",
  "evidence": "NayaPOWER#554 team agreement 2026-09-30; PR #1224 open/unmerged",
  "generalization": "never_maintain_two_normative_lineages"
}
~~~
